import uuid
from datetime import datetime, timedelta, timezone
from uuid import UUID
from jose import jwt, JWTError
from app.application.interfaces.token_service import TokenService
from app.config import settings

class JWTTokenService(TokenService):
    def _create_token(self, user_id: UUID, token_type: str, expires_delta: timedelta) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user_id),
            "type": token_type,
            "iat": now,
            "exp": now + expires_delta,
            "jti": str(uuid.uuid4()),
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def create_access_token(self, user_id: UUID) -> str:
        return self._create_token(
            user_id, "access", timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

    def create_refresh_token(self, user_id: UUID) -> str:
        return self._create_token(
            user_id, "refresh", timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )

    def verify_token(self, token: str, token_type: str = "access") -> UUID | None:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            if payload.get("type") != token_type:
                return None
            user_id = payload.get("sub")
            return UUID(user_id) if user_id else None
        except (JWTError, ValueError):
            return None
    
    def decode_token(self, token: str, token_type: str) -> dict | None:
     try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
     except JWTError:
        return None
     if payload.get("type") != token_type or not payload.get("sub") or not payload.get("jti"):
        return None
     return payload