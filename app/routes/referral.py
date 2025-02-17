from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth_service import AuthService
from app.crud.referral import (create_referral_code, delete_referral_code,
                               get_referral_code_by_user_id)
from app.db.databases import get_db
from app.models.users import User
from app.schemas.referral import (ReferralCodeCreate, ReferralCodeResponse,
                                  ReferrerResponse)

router = APIRouter()


@router.post("/create-code", response_model=ReferralCodeResponse)
def create_code(
    referral_data: ReferralCodeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    existing_code = get_referral_code_by_user_id(db, current_user.id)
    if existing_code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="A referral code already exists.")
    referral_code = create_referral_code(
        db,
        user_id=current_user.id,
        code=referral_data.code,
        expiration_date=referral_data.expiration_date
    )
    return referral_code


@router.delete("/delete-code", response_model=ReferralCodeResponse)
def delete_code(
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    deleted_code = delete_referral_code(db, current_user.id)
    if not deleted_code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Referral code not found.")
    return deleted_code


@router.get("/get-code", response_model=ReferrerResponse)
def get_code(
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    referral_code = get_referral_code_by_user_id(db, current_user.id)
    return ReferrerResponse(
        id=current_user.id,
        email=current_user.email,
        referral_code=referral_code
    )
