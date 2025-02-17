from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class ReferralCodeBase(BaseModel):
    code: str
    expiration_date: datetime


class ReferralCodeCreate(ReferralCodeBase):
    pass


class ReferralCodeResponse(ReferralCodeBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class ReferrerResponse(BaseModel):
    id: int
    email: EmailStr
    referral_code: Optional[ReferralCodeResponse] = None

    class Config:
        orm_mode = True


class ReferralResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
