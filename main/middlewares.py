import jwt
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.conf import settings
from urllib.parse import parse_qs


@database_sync_to_async
def get_user(token):
    from django.contrib.auth.models import AnonymousUser
    from users.models import User
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = User.objects.get(id=payload['user_id'])
        return user
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist) as e:
        print(f"JWT authentication failed: {str(e)}")
        return AnonymousUser()

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        from django.contrib.auth.models import AnonymousUser
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token")
        if token:
            scope["user"] = await get_user(token[0])
        else:
            scope["user"] = AnonymousUser()
        
        return await super().__call__(scope, receive, send)
