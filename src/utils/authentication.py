from rest_framework import authentication, exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('access_token')
        if not token:
            return None
        jwt_auth = JWTAuthentication()
        try:
            validation_token = jwt_auth.get_validated_token(token)
            user = jwt_auth.get_user(validation_token)
            return (user, validation_token)
        except exceptions.AuthenticationFailed:
            raise exceptions.AuthenticationFailed(
                'Invalid token from cookies'
            )