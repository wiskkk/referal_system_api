from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import Settings

# Контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """Проверяет соответствие обычного пароля и его хеша."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Генерирует хеш пароля."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Создает JWT токен с указанными данными и сроком действия.

    :param data: Данные для включения в токен.
    :param expires_delta: Срок действия токена (опционально).
    :return: Закодированный JWT токен.
    """
    to_encode = data.copy()
    if expires_delta:
        # Используем timezone-aware datetime
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(
            timezone.utc) + timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
    return encoded_jwt
