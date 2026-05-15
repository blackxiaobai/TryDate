from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from users.models import User
from matching.models import Match
from chat.models import Message, Report
from posts.models import Post


class IsStaff:
    """Custom permission check for staff users."""
    pass


def staff_required(view_func):
    """Decorator that checks user.is_staff."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'detail': '需要管理员权限'}, status=status.HTTP_403_FORBIDDEN)
        return view_func(request, *args, **kwargs)
    return wrapper


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@staff_required
def dashboard(request):
    week_ago = timezone.now() - timedelta(days=7)
    return Response({
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(status='active').count(),
        'weekly_matches': Match.objects.filter(matched_at__gte=week_ago).count(),
        'matched_pairs': Match.objects.filter(status='matched').count(),
        'total_messages': Message.objects.count(),
        'total_posts': Post.objects.filter(status='active').count(),
        'pending_reports': Report.objects.filter(status='pending').count(),
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@staff_required
def user_list(request):
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    page = int(request.GET.get('page', 1))
    page_size = 20

    qs = User.objects.all().order_by('-created_at')
    if search:
        qs = qs.filter(Q(nickname__icontains=search) | Q(email__icontains=search) | Q(phone__icontains=search))
    if status_filter:
        qs = qs.filter(status=status_filter)

    total = qs.count()
    users = qs[(page - 1) * page_size:page * page_size]

    return Response({
        'total': total,
        'page': page,
        'results': [{
            'id': str(u.id),
            'nickname': u.nickname,
            'email': u.email,
            'phone': u.phone,
            'gender': u.gender,
            'status': u.status,
            'is_active': u.is_active,
            'is_staff': u.is_staff,
            'questionnaire_completion': u.questionnaire_completion,
            'created_at': u.created_at.isoformat(),
        } for u in users],
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@staff_required
def ban_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'detail': '用户不存在'}, status=404)
    user.status = 'banned'
    user.is_active = False
    user.save(update_fields=['status', 'is_active'])
    return Response({'detail': f'已封禁 {user.nickname}'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@staff_required
def unban_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'detail': '用户不存在'}, status=404)
    user.status = 'active'
    user.is_active = True
    user.save(update_fields=['status', 'is_active'])
    return Response({'detail': f'已解封 {user.nickname}'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@staff_required
def match_list(request):
    status_filter = request.GET.get('status', '')
    page = int(request.GET.get('page', 1))
    page_size = 20

    qs = Match.objects.select_related('user_a', 'user_b').order_by('-matched_at')
    if status_filter:
        qs = qs.filter(status=status_filter)

    total = qs.count()
    matches = qs[(page - 1) * page_size:page * page_size]

    return Response({
        'total': total,
        'page': page,
        'results': [{
            'id': m.id,
            'user_a': m.user_a.nickname,
            'user_b': m.user_b.nickname,
            'compatibility_score': m.compatibility_score,
            'status': m.status,
            'week_number': m.week_number,
            'user_a_action': m.user_a_action,
            'user_b_action': m.user_b_action,
            'matched_at': m.matched_at.isoformat(),
        } for m in matches],
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@staff_required
def post_list(request):
    status_filter = request.GET.get('status', '')
    page = int(request.GET.get('page', 1))
    page_size = 20

    qs = Post.objects.select_related('author').order_by('-created_at')
    if status_filter:
        qs = qs.filter(status=status_filter)

    total = qs.count()
    posts = qs[(page - 1) * page_size:page * page_size]

    return Response({
        'total': total,
        'page': page,
        'results': [{
            'id': p.id,
            'author': p.author.nickname,
            'content': p.content,
            'is_anonymous': p.is_anonymous,
            'like_count': p.like_count,
            'status': p.status,
            'created_at': p.created_at.isoformat(),
        } for p in posts],
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@staff_required
def hide_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'detail': '动态不存在'}, status=404)
    post.status = 'hidden'
    post.save(update_fields=['status'])
    return Response({'detail': '已隐藏'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@staff_required
def restore_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'detail': '动态不存在'}, status=404)
    post.status = 'active'
    post.save(update_fields=['status'])
    return Response({'detail': '已恢复'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@staff_required
def report_list(request):
    status_filter = request.GET.get('status', '')
    page = int(request.GET.get('page', 1))
    page_size = 20

    qs = Report.objects.select_related('reporter', 'target_user').order_by('-created_at')
    if status_filter:
        qs = qs.filter(status=status_filter)

    total = qs.count()
    reports = qs[(page - 1) * page_size:page * page_size]

    return Response({
        'total': total,
        'page': page,
        'results': [{
            'id': r.id,
            'reporter': r.reporter.nickname,
            'target_user': r.target_user.nickname,
            'reason': r.reason,
            'description': r.description,
            'status': r.status,
            'created_at': r.created_at.isoformat(),
        } for r in reports],
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@staff_required
def resolve_report(request, report_id):
    try:
        report = Report.objects.get(id=report_id)
    except Report.DoesNotExist:
        return Response({'detail': '举报不存在'}, status=404)
    action = request.data.get('action', 'resolved')
    if action not in ('reviewed', 'resolved', 'dismissed'):
        return Response({'detail': '无效操作'}, status=400)
    report.status = action
    report.save(update_fields=['status'])
    return Response({'detail': f'已更新为{action}'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@staff_required
def reset_match_count(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'detail': '用户不存在'}, status=404)
    user.weekly_match_count = 0
    user.save(update_fields=['weekly_match_count'])
    return Response({'detail': f'已重置 {user.nickname} 的匹配次数'})
