from datetime import datetime, timezone
from uuid import UUID

class LogoutUserUseCase:
    def __init__(self, token_service, revoked_repo):
        self.token_service = token_service
        self.revoked_repo = revoked_repo

    async def execute(self, refresh_token: str, access_token: str | None = None) -> None:
        for token, token_type in ((refresh_token, "refresh"), (access_token, "access")):
            if not token:
                continue
            payload = self.token_service.decode_token(token, token_type)
            if payload:
                await self.revoked_repo.revoke(
                    jti=payload["jti"],
                    user_id=UUID(payload["sub"]),
                    expires_at=datetime.fromtimestamp(payload["exp"], tz=timezone.utc),
                )