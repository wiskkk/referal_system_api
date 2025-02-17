from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Связь с реферальным кодом
    referral_code_id = Column(Integer, ForeignKey("referral_codes.id"), nullable=True)
    referral_code = relationship("ReferralCode", back_populates="user", uselist=False)

    # Связь с рефералами
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    referrals = relationship("User", remote_side=[id], back_populates="referrer")
    referrer = relationship("User", remote_side=[referrer_id], back_populates="referrals")