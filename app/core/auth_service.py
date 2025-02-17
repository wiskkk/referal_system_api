from datetime import timedelta
from typing import Optional

from jose import JWTError, jwt

from app.core.config import Settings
from app.core.security import create_access_token, verify_password
from app.crud.users import get_user_by_email
from app.models.users import User
from app.schemas.users import TokenData


class AuthService:
    def __init__(self, db_session):
        self.db = db_session

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Аутентифицирует пользователя по email и паролю."""
        user = await get_user_by_email(self.db, email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    async def create_token(self, user: User) -> dict:
        """Создает JWT токен для пользователя."""
        access_token_expires = timedelta(
            minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token_data = {"sub": user.email}
        return {
            "access_token": create_access_token(token_data, expires_delta=access_token_expires),
            "token_type": "bearer"
        }

    async def get_current_user(self, token: str) -> Optional[User]:
        """Получает текущего пользователя из JWT токена."""
        try:
            payload = jwt.decode(token, Settings.SECRET_KEY,
                                 algorithms=[Settings.ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                return None
            token_data = TokenData(email=email)
        except JWTError:
            return None
        user = await get_user_by_email(self.db, email=token_data.email)
        return user
