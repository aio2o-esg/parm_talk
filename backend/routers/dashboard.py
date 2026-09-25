from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.esg_activity import ESGActivity
from models.coupon import Coupon

router = APIRouter(prefix="/dashboard", tags=["대시보드"])

POLICY_PARAMS = {
    "reward_rate_env": 0.05,
    "sme_bonus_rate": 0.10,
    "anomaly_threshold": 0.15,
    "monthly_issue_cap": 10000,
    "policy_status": "ACTIVE"
}

@router.get("/summary")
def get_summary(user_id: int = 1, db: Session = Depends(get_db)):
    activities = db.query(ESGActivity).filter(ESGActivity.user_id == user_id).all()
    total_reward = sum(a.reward_amount for a in activities)
    recent = activities[-3:] if len(activities) >= 3 else activities
    return {
        "esg_gold_balance": total_reward,
        "esg_score": {"E": 75, "S": 60, "G": 80},
        "recent_activities": [{"type": a.activity_type, "reward": a.reward_amount, "date": str(a.created_at)} for a in recent]
    }

@router.get("/policy")
def get_policy():
    return {"policy_params": POLICY_PARAMS}

@router.get("/ai-results")
def get_ai_results():
    return {
        "participation_rate_change": "+12%",
        "anomaly_count": 2,
        "predicted_issuance": 8500,
        "policy_effect_score": 78.5,
        "last_updated": "2026-04-01"
    }
