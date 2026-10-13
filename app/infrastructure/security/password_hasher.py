from passlib.context import CryptContext
import bcrypt
from app.application.interfaces.password_services import PasswordService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class BcryptPasswordService(PasswordService):
    def hash_password(self, password: str) -> str:
       return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))