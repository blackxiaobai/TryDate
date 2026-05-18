from datetime import timedelta
from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ChatRoom, Message, Report
from .serializers import ChatRoomSerializer, MessageSerializer, ReportSerializer
from matching.models import Match
from users.models import BlackList

CHAT_EXPIRY_DAYS = 7


def _expire_old_rooms():
    """将超过 7 天的聊天室标记为不活跃。"""
    cutoff = timezone.now() - timedelta(days=CHAT_EXPIRY_DAYS)
    ChatRoom.objects.filter(is_active=True, created_at__lt=cutoff).update(is_active=False)


def _check_room_expired(room):
    """检查聊天室是否已过期，返回 True 表示已过期。"""
    if not room.is_active:
        return True
    if timezone.now() > room.created_at + timedelta(days=CHAT_EXPIRY_DAYS):
        room.is_active = False
        room.save(update_fields=['is_active'])
        return True
    return False


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def room_detail(request, room_id):
    try:
        room = ChatRoom.objects.select_related('match__user_a', 'match__user_b').get(id=room_id)
    except ChatRoom.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user not in (room.match.user_a, room.match.user_b):
        return Response(status=status.HTTP_403_FORBIDDEN)

    expired = _check_room_expired(room)
    serializer = ChatRoomSerializer(room, context={'request': request})
    data = serializer.data
    data['expired'] = expired
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def room_list(request):
    _expire_old_rooms()
    rooms = ChatRoom.objects.filter(
        Q(match__user_a=request.user) | Q(match__user_b=request.user),
        is_active=True,
    ).select_related('match__user_a', 'match__user_b').order_by('-last_message_at')
    serializer = ChatRoomSerializer(rooms, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def room_messages(request, room_id):
    try:
        room = ChatRoom.objects.get(id=room_id)
    except ChatRoom.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user not in (room.match.user_a, room.match.user_b):
        return Response(status=status.HTTP_403_FORBIDDEN)

    if _check_room_expired(room):
        return Response({'detail': '聊天已过期'}, status=status.HTTP_410_GONE)

    messages = room.messages.order_by('created_at')
    return Response(MessageSerializer(messages, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image(request, room_id):
    try:
        room = ChatRoom.objects.get(id=room_id)
    except ChatRoom.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user not in (room.match.user_a, room.match.user_b):
        return Response(status=status.HTTP_403_FORBIDDEN)

    image = request.FILES.get('image')
    if not image:
        return Response({'detail': '请上传图片'}, status=status.HTTP_400_BAD_REQUEST)

    msg = Message.objects.create(
        chat_room=room,
        sender=request.user,
        msg_type=Message.MsgType.IMAGE,
        content=image.name,
    )
    msg.content = request.build_absolute_uri(f'/media/chat/{image.name}')

    from django.core.files.storage import default_storage
    default_storage.save(f'chat/{image.name}', image)
    msg.save()

    return Response(MessageSerializer(msg).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_user(request):
    data = request.data.copy()
    # 举报动态/评论时自动填充 target_user
    if not data.get('target_user'):
        if data.get('target_post'):
            from posts.models import Post
            try:
                data['target_user'] = str(Post.objects.get(id=data['target_post']).author_id)
            except Post.DoesNotExist:
                pass
        elif data.get('target_comment'):
            from posts.models import Comment
            try:
                data['target_user'] = str(Comment.objects.get(id=data['target_comment']).author_id)
            except Comment.DoesNotExist:
                pass
    serializer = ReportSerializer(data=data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'detail': '举报已提交，我们会尽快处理'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def block_user(request, user_id):
    from users.models import User
    try:
        target = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if target == request.user:
        return Response({'detail': '不能屏蔽自己'}, status=status.HTTP_400_BAD_REQUEST)

    BlackList.objects.get_or_create(blocker=request.user, blocked=target)
    ChatRoom.objects.filter(
        Q(match__user_a=request.user, match__user_b=target) |
        Q(match__user_a=target, match__user_b=request.user)
    ).update(is_active=False)

    return Response({'detail': f'已屏蔽 {target.nickname}'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unblock_user(request, user_id):
    BlackList.objects.filter(blocker=request.user, blocked_id=user_id).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

