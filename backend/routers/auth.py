from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Literal, Optional
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
import uuid
from database import get_db
from models.user import User
from models.merchant import Merchant
from config import settings

router = APIRouter(prefix="/auth", tags=["인증"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    user_type: Literal["citizen", "merchant"]
    region: str = "해남군"
    store_name: Optional[str] = Field(default=None, max_length=100)
    address: Optional[str] = Field(default=None, max_length=200)
    business_number: Optional[str] = Field(default=None, max_length=30)
    esg_types: Optional[str] = Field(default=None, max_length=200)

    @model_validator(mode="after")
    def validate_merchant_fields(self):
        if self.user_type == "merchant" and not self.store_name:
            raise ValueError("소상공인은 상호명을 입력해야 합니다")
        return self

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class WalletConnectRequest(BaseModel):
    algorand_address: str

def create_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expire_minutes)
    data.update({"exp": expire})
    return jwt.encode(data, settings.jwt_secret, algorithm=settings.jwt_algorithm)

@router.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    email = req.email.lower()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다")
    try:
        user = User(
            full_name=req.full_name.strip(),
            email=email,
            hashed_password=pwd_context.hash(req.password),
            user_type=req.user_type,
            region=req.region.strip() if req.region else "해남군"
        )
        db.add(user)
        db.flush()

        merchant_id = None
        if req.user_type == "merchant":
            merchant = Merchant(
                user_id=user.id,
                store_name=req.store_name.strip(),
                address=req.address.strip() if req.address else None,
                business_number=req.business_number.strip() if req.business_number else None,
                esg_types=req.esg_types.strip() if req.esg_types else None,
                qr_code=str(uuid.uuid4())
            )
            db.add(merchant)
            db.flush()
            merchant_id = merchant.id

        db.commit()
        db.refresh(user)
        return {
            "message": "회원가입 성공",
            "user_id": user.id,
            "user_type": user.user_type,
            "merchant_id": merchant_id
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="이미 등록된 이메일 또는 사업자 정보입니다")
    except Exception:
        db.rollback()
        raise

@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email.lower()).first()
    if not user or not pwd_context.verify(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다")
    token = create_token({"sub": str(user.id), "email": user.email, "user_type": user.user_type})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "user_type": user.user_type,
        "region": user.region
    }

@router.post("/wallet-connect")
def wallet_connect(req: WalletConnectRequest, db: Session = Depends(get_db)):
    return {"message": "지갑 연결 성공", "address": req.algorand_address}
