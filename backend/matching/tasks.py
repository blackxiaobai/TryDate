"""
按需匹配：用户主动触发，系统找最佳候选人。
每人每周最多成功匹配 2 次（接受后才扣减）。
"""
from django.utils import timezone
from django.db.models import Q
from users.models import User, BlackList
from questionnaire.models import Questionnaire
from .models import Match
from .algorithm import compute_compatibility, generate_highlights


def get_week_number() -> str:
    return timezone.now().strftime('%Y-W%W')


def _compute_bidirectional_score(user_answers, candidate_answers):
    """双向平均契合度，避免单向评分偏差。"""
    forward_score, forward_dims = compute_compatibility(user_answers, candidate_answers)
    backward_score, backward_dims = compute_compatibility(candidate_answers, user_answers)
    avg_score = round((forward_score + backward_score) / 2, 1)
    avg_dims = {
        key: round((forward_dims[key] + backward_dims[key]) / 2, 1)
        for key in forward_dims
    }
    return avg_score, avg_dims


def find_match_for_user(user) -> Match | None:
    """为指定用户找到最佳匹配候选人，返回 Match 对象或 None。"""
    user.reset_weekly_count_if_needed()
    if not user.is_eligible_for_matching or not user.can_match:
        return None

    week = get_week_number()

    # 排除：本周已有匹配记录的用户（不论状态）
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

    # 排除：本周匹配次数已用完的用户
    matched_out = User.objects.filter(
        weekly_match_count__gte=User.MAX_WEEKLY_MATCHES,
        match_week=week,
    ).values_list('id', flat=True)
    excluded_ids.update(matched_out)

    # 排除：有待处理匹配尚未回应的用户（避免一个人同时被多个人匹配）
    pending_users = Match.objects.filter(
        week_number=week,
        status=Match.MatchStatus.PENDING,
    ).filter(
        Q(user_a_action=Match.Action.PENDING) | Q(user_b_action=Match.Action.PENDING)
    ).values_list('user_a_id', 'user_b_id')
    for a_id, b_id in pending_users:
        excluded_ids.add(a_id)
        excluded_ids.add(b_id)
    # 把当前用户自己从排除列表移除（自己的待处理不应该排除自己）
    excluded_ids.discard(user.id)
    # 但永远不能匹配自己，重新加回来
    excluded_ids.add(user.id)

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

    # 计算双向契合度，找最佳候选人
    best_score = 0
    best_candidate = None
    best_dim_scores = {}
    best_highlights = []

    for candidate in candidates:
        candidate_answers = candidate_qs.get(candidate.id, {})
        score, dim_scores = _compute_bidirectional_score(user_answers, candidate_answers)
        if score > best_score:
            best_score = score
            best_candidate = candidate
            best_dim_scores = dim_scores
            best_highlights = generate_highlights(user_answers, candidate_answers)

    if not best_candidate or best_score < 20 or best_candidate.id == user.id:
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

    if created:
        # 发送邮件通知被匹配的用户
        partner = best_candidate if user == user_a else user_a
        _send_match_notification(user, partner)

    return match


def _send_match_notification(requester, partner):
    """给被匹配的用户发送邮件提醒"""
    import logging
    import resend
    from django.conf import settings

    logger = logging.getLogger(__name__)

    if not partner.email:
        return

    try:
        resend.api_key = settings.RESEND_API_KEY
        resend.Emails.send({
            'from': 'TryDate <noreply@dlnu-love.top>',
            'to': [partner.email],
            'subject': '【TryDate】你收到一个新的匹配请求 💝',
            'html': f'''
                <div style="max-width:480px;margin:0 auto;padding:32px 24px;font-family:sans-serif;">
                    <h2 style="color:#e84393;text-align:center;">💝 有人想认识你！</h2>
                    <p style="color:#333;font-size:15px;line-height:1.8;">
                        你好 <strong>{partner.nickname}</strong>，
                    </p>
                    <p style="color:#555;font-size:14px;line-height:1.8;">
                        <strong>{requester.nickname}</strong> 与你匹配成功啦！
                        快来 TryDate 查看你的匹配结果，决定是否心动吧～
                    </p>
                    <div style="text-align:center;margin:28px 0;">
                        <a href="https://dlnu-love.top/app/match"
                           style="display:inline-block;padding:12px 32px;background:linear-gradient(135deg,#e84393,#fd79a8);color:#fff;border-radius:12px;text-decoration:none;font-weight:bold;font-size:15px;">
                            查看匹配结果
                        </a>
                    </div>
                    <p style="color:#aaa;font-size:12px;text-align:center;">
                        此邮件由 TryDate 系统自动发送，请勿回复。
                    </p>
                </div>
            ''',
        })
    except Exception as e:
        logger.warning(f'匹配通知邮件发送失败: {e}')
