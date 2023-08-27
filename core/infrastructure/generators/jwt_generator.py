from datetime import datetime, timedelta

from django.conf import settings

from core.domain.models.user import User
import jwt


class JWTGenerator:
    def generate(self, user: User, refresh_token: bool = False) -> str:
        payload = {
            "user_id": user.id,
            "exp": datetime.utcnow() + timedelta(days=1),
            "iat": datetime.utcnow(),
            "refresh_token": refresh_token,
        }

        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
