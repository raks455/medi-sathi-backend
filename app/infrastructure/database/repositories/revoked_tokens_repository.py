from datetime import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.models.revoked_token import RevokedTokenModel

class SQLAlchemyRevokedTokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def is_revoked(self, jti: str) -> bool:
        return await self.session.get(RevokedTokenModel, jti) is not None

    async def revoke(self, jti: str, user_id: UUID, expires_at: datetime) -> None:
        if await self.is_revoked(jti):
            return
        self.session.add(RevokedTokenModel(jti=jti, user_id=user_id, expires_at=expires_at))
        await self.session.commit()