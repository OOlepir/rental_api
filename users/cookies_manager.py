from datetime import datetime
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def set_jwt_cookies(response: Response, user: User) -> Response:
    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token

    access_expiry = datetime.fromtimestamp(access_token["exp"])
    refresh_expiry = datetime.fromtimestamp(refresh_token["exp"])

    response.set_cookie(
        key="access_token",
        value=str(access_token),
        httponly=True,
        secure=False,
        samesite="Lax",
        expires=access_expiry,
    )
    response.set_cookie(
        key="refresh_token",
        value=str(refresh_token),
        httponly=True,
        secure=False,
        samesite="Lax",
        expires=refresh_expiry,
    )

    return response
