from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Match
from .serializers import MatchSerializer
from .tasks import find_match_for_user, get_week_number


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_match(request):
    user = request.user
    if not user.is_eligible_for_matching:
        return Response({'detail': '请先完成灵魂问卷（完成度 ≥ 70%）'}, status=status.HTTP_400_BAD_REQUEST)
    if not user.can_match:
        return Response({'detail': '本周匹配次数已用完（2次/周）'}, status=status.HTTP_400_BAD_REQUEST)

    # 检查是否有用户尚未回应的待处理匹配
    week = get_week_number()
    pending = Match.objects.filter(
        week_number=week
    ).filter(
        Q(user_a=user, user_a_action=Match.Action.PENDING) |
        Q(user_b=user, user_b_action=Match.Action.PENDING)
    ).filter(
        status=Match.MatchStatus.PENDING,
    ).first()

    if pending:
        return Response({
            'matched': True,
            'match': MatchSerializer(pending, context={'request': request}).data,
        })

    match = find_match_for_user(user)
    if not match:
        return Response({'detail': '暂时没有找到合适的匹配，过段时间再来试试吧～', 'matched': False})

    return Response({
        'matched': True,
        'match': MatchSerializer(match, context={'request': request}).data,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_match(request):
    user = request.user
    user.reset_weekly_count_if_needed()
    week = get_week_number()

    # 找到用户尚未回应的待处理匹配（即使对方已回应也要显示）
    match = Match.objects.filter(
        week_number=week
    ).filter(
        Q(user_a=user, user_a_action=Match.Action.PENDING) |
        Q(user_b=user, user_b_action=Match.Action.PENDING)
    ).filter(
        status=Match.MatchStatus.PENDING,
    ).first()

    if not match:
        # 检查是否有最近匹配成功的
        recent = Match.objects.filter(
            week_number=week
        ).filter(
            Q(user_a=user) | Q(user_b=user)
        ).filter(
            status=Match.MatchStatus.MATCHED
        ).order_by('-matched_at').first()

        if recent:
            return Response({
                'matched': True,
                'match': MatchSerializer(recent, context={'request': request}).data,
                'remaining': user.MAX_WEEKLY_MATCHES - user.weekly_match_count,
            })

        return Response({
            'matched': False,
            'remaining': user.MAX_WEEKLY_MATCHES - user.weekly_match_count,
        })

    return Response({
        'matched': True,
        'match': MatchSerializer(match, context={'request': request}).data,
        'remaining': user.MAX_WEEKLY_MATCHES - user.weekly_match_count,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respond_match(request, match_id):
    action = request.data.get('action')
    if action not in (Match.Action.LIKED, Match.Action.PASSED):
        return Response({'detail': '无效操作'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        match = Match.objects.get(id=match_id)
    except Match.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user not in (match.user_a, match.user_b):
        return Response(status=status.HTTP_403_FORBIDDEN)

    if match.status != Match.MatchStatus.PENDING:
        return Response({'detail': '该匹配已结束'}, status=status.HTTP_400_BAD_REQUEST)

    if timezone.now() > match.action_deadline:
        match.status = Match.MatchStatus.MISSED
        match.save(update_fields=['status'])
        return Response({'detail': '确认时间已过期'}, status=status.HTTP_400_BAD_REQUEST)

    if match.get_action_for(request.user) != Match.Action.PENDING:
        return Response({'detail': '已经操作过了'}, status=status.HTTP_400_BAD_REQUEST)

    match.set_action_for(request.user, action)

    user = request.user
    return Response({
        **MatchSerializer(match, context={'request': request}).data,
        'remaining': user.MAX_WEEKLY_MATCHES - user.weekly_match_count,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def match_history(request):
    matches = Match.objects.filter(
        Q(user_a=request.user) | Q(user_b=request.user)
    ).order_by('-matched_at')
    serializer = MatchSerializer(matches, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def trigger_match(request):
    if not request.user.is_staff:
        return Response(status=status.HTTP_403_FORBIDDEN)
    match = find_match_for_user(request.user)
    if match:
        return Response({'detail': f'匹配完成', 'match_id': match.id})
    return Response({'detail': '未找到合适匹配'})
