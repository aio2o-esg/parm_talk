from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta
import uuid
from database import get_db
from models.coupon import Coupon

router = APIRouter(prefix="/coupons", tags=["쿠폰"])

class IssueRequest(BaseModel):
    user_id: int
    amount: float

class UseRequest(BaseModel):
    qr_code: str

@router.post("/issue")
def issue_coupon(req: IssueRequest, db: Session = Depends(get_db)):
    coupon = Coupon(
        user_id=req.user_id,
        qr_code=str(uuid.uuid4()),
        amount=req.amount,
        status="active",
        expires_at=datetime.utcnow() + timedelta(days=30)
    )
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return {"message": "쿠폰 발행 완료", "coupon_id": coupon.id, "qr_code": coupon.qr_code, "amount": coupon.amount}

@router.post("/use")
def use_coupon(req: UseRequest, db: Session = Depends(get_db)):
    coupon = db.query(Coupon).filter(Coupon.qr_code == req.qr_code, Coupon.status == "active").first()
    if not coupon:
        raise HTTPException(status_code=404, detail="유효하지 않은 쿠폰입니다")
    if coupon.expires_at < datetime.utcnow():
        coupon.status = "expired"
        db.commit()
        raise HTTPException(status_code=400, detail="만료된 쿠폰입니다")
    coupon.status = "used"
    coupon.used_at = datetime.utcnow()
    db.commit()
    return {"message": "쿠폰 사용 완료", "amount": coupon.amount}

@router.get("/my")
def get_my_coupons(user_id: int = 1, db: Session = Depends(get_db)):
    coupons = db.query(Coupon).filter(Coupon.user_id == user_id).all()
    return {"coupons": [{"id": c.id, "amount": c.amount, "status": c.status, "expires_at": str(c.expires_at)} for c in coupons]}
