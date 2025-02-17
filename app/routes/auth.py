from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.core.auth_service import AuthService
from app.core.security import create_access_token, verify_password
from app.crud.referral import get_referral_code_by_code
from app.crud.users import create_user, get_user_by_email
from app.db.databases import get_db
from app.schemas.users import Token, UserCreate

router = APIRouter()


@router.post("/register", response_model=Token)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Регистрация нового пользователя."""
    referral_code = None
    if user_data.referral_code:
        referral_code = await get_referral_code_by_code(db, user_data.referral_code)
        if not referral_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid referral code.")

    db_user = await get_user_by_email(db, email=user_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    created_user = await create_user(
        db, user_data, referrer_id=referral_code.user_id if referral_code else None)
    return await AuthService.create_token(created_user)


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
