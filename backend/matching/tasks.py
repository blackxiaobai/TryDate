"""
按需匹配：用户主动触发，系统找最佳候选人。
每人每周最多成功匹配 2 次。
"""
from django.utils import timezone
from django.db.models import Q
from users.models import User, BlackList
from questionnaire.models import Questionnaire
from .models import Match
from .algorithm import compute_compatibility, generate_highlights


def get_week_number() -> str:
    return timezone.now().strftime('%Y-W%W')


def find_match_for_user(user) -> Match | None:
    """为指定用户找到最佳匹配候选人，返回 Match 对象或 None。"""
    if not user.is_eligible_for_matching or not user.can_match:
        return None

    week = get_week_number()

    # 排除：本周已有过匹配记录的用户
    existing_matches = Match.objects.filter(
        week_number=week
    ).filter(
        Q(user_a=user) | Q(user_b=user)
    )
    excluded_ids = set()
    for m in existing_matches:
        if m.user_a_id == user.id:
            excluded_ids.add(m.user_b_id)
        else:
            excluded_ids.add(m.user_a_id)

    # 排除：黑名单
    blocked = set(BlackList.objects.filter(blocker=user).values_list('blocked_id', flat=True))
    blocked_by = set(BlackList.objects.filter(blocked=user).values_list('blocker_id', flat=True))
    excluded_ids.update(blocked)
    excluded_ids.update(blocked_by)
    excluded_ids.add(user.id)

    # 排除：本周已达成 2 次匹配的用户
    matched_out = User.objects.filter(
        weekly_match_count__gte=User.MAX_WEEKLY_MATCHES,
        match_week=week,
    ).values_list('id', flat=True)
    excluded_ids.update(matched_out)

    # 性别偏好筛选
    if user.gender == User.Gender.MALE:
        pref_filter = Q(gender_preference__in=[User.GenderPreference.FEMALE, User.GenderPreference.BOTH])
    elif user.gender == User.Gender.FEMALE:
        pref_filter = Q(gender_preference__in=[User.GenderPreference.MALE, User.GenderPreference.BOTH])
    else:
        pref_filter = Q()

    if user.gender_preference == User.GenderPreference.MALE:
        gender_filter = Q(gender=User.Gender.MALE)
    elif user.gender_preference == User.GenderPreference.FEMALE:
        gender_filter = Q(gender=User.Gender.FEMALE)
    else:
        gender_filter = Q()

    # 查找候选人
    candidates = User.objects.filter(
        questionnaire_completion__gte=70,
        status=User.Status.ACTIVE,
        is_active=True,
    ).exclude(
        id__in=excluded_ids
    ).filter(
        gender_filter
    ).filter(
        pref_filter
    )

    if not candidates.exists():
        return None

    # 获取问卷数据
    user_q = Questionnaire.objects.filter(user=user).first()
    user_answers = user_q.answers if user_q else {}

    candidate_ids = [c.id for c in candidates]
    candidate_qs = {
        q.user_id: q.answers
        for q in Questionnaire.objects.filter(user_id__in=candidate_ids)
    }

    # 计算契合度，找最佳候选人
    best_score = 0
    best_candidate = None
    best_dim_scores = {}
    best_highlights = []

    for candidate in candidates:
        candidate_answers = candidate_qs.get(candidate.id, {})
        score, dim_scores = compute_compatibility(user_answers, candidate_answers)
        if score > best_score:
            best_score = score
            best_candidate = candidate
            best_dim_scores = dim_scores
            best_highlights = generate_highlights(user_answers, candidate_answers)

    if not best_candidate or best_score < 20:
        return None

    # 确保 user_a < user_b（规范化）
    if str(user.id) > str(best_candidate.id):
        user_a, user_b = best_candidate, user
    else:
        user_a, user_b = user, best_candidate

    match, created = Match.objects.get_or_create(
        user_a=user_a,
        user_b=user_b,
        week_number=week,
        defaults={
            'compatibility_score': best_score,
            'dimension_scores': best_dim_scores,
            'compatibility_highlights': best_highlights,
        },
    )
    return match
