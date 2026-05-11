"""
Django Channels 自定义 JWT 认证中间件。
从 WebSocket 查询字符串 ?token=xxx 中读取 JWT，解析用户身份。
"""
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    """从 WebSocket URL query string 中读取 JWT token 并认证用户。"""

    async def __call__(self, scope, receive, send):
        # 解析 query string 中的 token
        query_string = parse_qs(scope.get('query_string', b'').decode())
        token_list = query_string.get('token', [])
        token = token_list[0] if token_list else None

        if token:
            try:
                access_token = AccessToken(token)
                scope['user'] = await get_user(access_token['user_id'])
            except Exception:
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)
