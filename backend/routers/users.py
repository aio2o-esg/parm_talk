from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models.user import User
from models.merchant import Merchant

router = APIRouter(prefix="/users", tags=["사용자"])

class UserUpdateRequest(BaseModel):
    region: Optional[str] = None
    algorand_address: Optional[str] = None

class MerchantRegisterRequest(BaseModel):
    store_name: str
    address: Optional[str] = None
    business_number: Optional[str] = None
    esg_types: Optional[str] = None

@router.get("/me")
def get_me(user_id: int = 1, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    return {"id": user.id, "email": user.email, "user_type": user.user_type, "region": user.region, "algorand_address": user.algorand_address}

@router.put("/me")
def update_me(req: UserUpdateRequest, user_id: int = 1, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    if req.region:
        user.region = req.region
    if req.algorand_address:
        user.algorand_address = req.algorand_address
    db.commit()
    return {"message": "프로필 수정 완료"}
