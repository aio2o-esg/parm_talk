from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from database import get_db
from models.user import User
from config import settings

router = APIRouter(prefix="/auth", tags=["인증"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    user_type: str = "citizen"
    region: str = None

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
    if db.query(User).filter(User.email == req.email).first():
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다")
    user = User(
        email=req.email,
        hashed_password=pwd_context.hash(req.password),
        user_type=req.user_type,
        region=req.region
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "회원가입 성공", "user_id": user.id}

@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not pwd_context.verify(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다")
    token = create_token({"sub": str(user.id), "email": user.email, "user_type": user.user_type})
    return {"access_token": token, "token_type": "bearer", "user_type": user.user_type}

@router.post("/wallet-connect")
def wallet_connect(req: WalletConnectRequest, db: Session = Depends(get_db)):
    return {"message": "지갑 연결 성공", "address": req.algorand_address}
