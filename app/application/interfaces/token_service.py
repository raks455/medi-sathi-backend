from abc import ABC, abstractmethod
from uuid import UUID

class TokenService(ABC):
    @abstractmethod
    def create_access_token(self, user_id: UUID) -> str: ...

    @abstractmethod
    def create_refresh_token(self, user_id: UUID) -> str: ...

    @abstractmethod
    def verify_token(self, token: str, token_type: str = "access") -> UUID | None: ...
    
    @abstractmethod
    def decode_token(self, token: str, token_type: str) -> dict | None: ...