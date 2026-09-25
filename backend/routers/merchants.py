from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import uuid
from database import get_db
from models.merchant import Merchant

router = APIRouter(prefix="/merchants", tags=["소상공인"])

class MerchantRegisterRequest(BaseModel):
    user_id: int
    store_name: str
    address: Optional[str] = None
    business_number: Optional[str] = None
    esg_types: Optional[str] = None

@router.post("/register")
def register_merchant(req: MerchantRegisterRequest, db: Session = Depends(get_db)):
    qr_code = str(uuid.uuid4())
    merchant = Merchant(
        user_id=req.user_id,
        store_name=req.store_name,
        address=req.address,
        business_number=req.business_number,
        esg_types=req.esg_types,
        qr_code=qr_code
    )
    db.add(merchant)
    db.commit()
    db.refresh(merchant)
    return {"message": "매장 등록 완료", "merchant_id": merchant.id, "qr_code": qr_code}

@router.get("/{merchant_id}")
def get_merchant(merchant_id: int, db: Session = Depends(get_db)):
    merchant = db.query(Merchant).filter(Merchant.id == merchant_id).first()
    if not merchant:
        raise HTTPException(status_code=404, detail="매장을 찾을 수 없습니다")
    return merchant

@router.get("/{merchant_id}/qr")
def get_merchant_qr(merchant_id: int, db: Session = Depends(get_db)):
    merchant = db.query(Merchant).filter(Merchant.id == merchant_id).first()
    if not merchant:
        raise HTTPException(status_code=404, detail="매장을 찾을 수 없습니다")
    return {"merchant_id": merchant_id, "qr_code": merchant.qr_code}
