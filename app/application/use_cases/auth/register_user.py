from uuid import uuid4
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.application.interfaces.password_services import PasswordService
from app.application.interfaces.token_service import TokenService
from app.application.dto.auth_dto import RegisterRequest, TokenResponse

class RegisterUserUseCase:
    def __init__(
        self,
        user_repo: UserRepository,
        password_service: PasswordService,
        token_service: TokenService,
    ):
        self.user_repo = user_repo
        self.password_service = password_service
        self.token_service = token_service

    async def execute(self, data: RegisterRequest) -> TokenResponse:
        existing = await self.user_repo.get_by_email(data.email)
        if existing:
            raise ValueError("Email already registered")

        hashed = self.password_service.hash_password(data.password)

        user = User(
            id=uuid4(),
            email=data.email.lower(),
            full_name=data.full_name.strip(),
            hashed_password=hashed,
        )

        created_user = await self.user_repo.create(user)
        access_token = self.token_service.create_access_token(created_user.id)
        refresh_token = self.token_service.create_refresh_token(user.id)
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=str(created_user.id),
            email=created_user.email,
            full_name=created_user.full_name,
        )