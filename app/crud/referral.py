from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.referral import ReferralCode
from app.models.users import User


async def create_referral_code(db: AsyncSession, user_id: int, code: str, expiration_date: datetime):
    """Создает новый реферальный код для пользователя."""
    db_referral_code = ReferralCode(
        user_id=user_id,
        code=code,
        expiration_date=expiration_date
    )
    db.add(db_referral_code)
    await db.commit()
    await db.refresh(db_referral_code)
    return db_referral_code


async def get_referral_code_by_code(db: AsyncSession, code: str):
    """Получает реферальный код по уникальному значению code."""
    result = await db.execute(select(ReferralCode).filter(ReferralCode.code == code))
    return result.scalars().first()


async def get_referral_code_by_user_id(db: AsyncSession, user_id: int):
    """Получает реферальный код по ID пользователя."""
    result = await db.execute(select(ReferralCode).filter(ReferralCode.user_id == user_id))
    return result.scalars().first()


async def delete_referral_code(db: AsyncSession, user_id: int):
    """Удаляет реферальный код пользователя."""
    result = await db.execute(select(ReferralCode).filter(ReferralCode.user_id == user_id))
    db_referral_code = result.scalars().first()
    if db_referral_code:
        await db.delete(db_referral_code)
        await db.commit()
    return db_referral_code


async def get_referrals_by_referrer_id(db: AsyncSession, referrer_id: int):
    """Получает список рефералов по ID реферера."""
    result = await db.execute(select(User).filter(User.referrer_id == referrer_id))
    return result.scalars().all()
