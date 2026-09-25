from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models.esg_activity import ESGActivity
from models.merchant import Merchant

router = APIRouter(prefix="/esg", tags=["ESG 활동"])

REWARD_RATE = 0.05

class QRVerifyRequest(BaseModel):
    user_id: int
    qr_code: str
    activity_type: str

class GPSVerifyRequest(BaseModel):
    user_id: int
    distance_km: float
    transport_type: str

@router.post("/verify/qr")
def verify_qr(req: QRVerifyRequest, db: Session = Depends(get_db)):
    merchant = db.query(Merchant).filter(Merchant.qr_code == req.qr_code).first()
    if not merchant:
        raise HTTPException(status_code=404, detail="유효하지 않은 QR 코드입니다")
    reward = round(100 * REWARD_RATE, 2)
    activity = ESGActivity(
        user_id=req.user_id,
        merchant_id=merchant.id,
        activity_type=req.activity_type,
        verification_method="qr",
        reward_amount=reward,
        status="completed"
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return {"message": "ESG 활동 인증 완료", "activity_id": activity.id, "reward_amount": reward, "merchant": merchant.store_name}

@router.post("/verify/gps")
def verify_gps(req: GPSVerifyRequest, db: Session = Depends(get_db)):
    reward = round(req.distance_km * 10 * REWARD_RATE, 2)
    activity = ESGActivity(
        user_id=req.user_id,
        activity_type="이동",
        verification_method="gps",
        reward_amount=reward,
        status="completed"
    )
    db.add(activity)
    db.commit()
    return {"message": "GPS 활동 인증 완료", "distance_km": req.distance_km, "reward_amount": reward}

@router.get("/activities")
def get_activities(user_id: int = 1, db: Session = Depends(get_db)):
    activities = db.query(ESGActivity).filter(ESGActivity.user_id == user_id).all()
    return {"activities": [{"id": a.id, "activity_type": a.activity_type, "reward_amount": a.reward_amount, "status": a.status, "created_at": str(a.created_at)} for a in activities]}
