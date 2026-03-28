import jwt
from decouple import config
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from apps.users.models import CustomUser


class JWTCookieMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.COOKIES.get('access_token')
        if not token:
            request.user = AnonymousUser()
        try:
            payload = jwt.decode(token, config('SECRET_KEY'), algorithms=['HS256'])
            user_id = payload.get('user_id')
            user = CustomUser.objects.get(id=user_id)
            request.user = user
        except (jwt.ExpiredSignatureError,
                jwt.InvalidTokenError,
                jwt.DecodeError,
                CustomUser.DoesNotExist):
            request.user = AnonymousUser()

