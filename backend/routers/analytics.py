from fastapi import APIRouter
import random

router = APIRouter(prefix="/analytics", tags=["analytics"])

_sim_data = []

def gen_records(count=500):
    types = ["cup","gps","energy","recycle","volunteer","policy_proposal"]
    rewards = {"cup":50,"gps":32,"energy":200,"recycle":30,"volunteer":150,"policy_proposal":100}
    return [{"id":i,"user_id":random.randint(1,50),"activity_type":random.choice(types),"reward":rewards[random.choice(types)],"is_anomaly":random.random()<0.006,"month":random.randint(1,5),"participated":True} for i in range(count)]

@router.post("/generate-sim-data")
async def generate_sim_data():
    global _sim_data
    _sim_data = gen_records(500)
    return {"status":"ok","count":500}

@router.post("/run-ai")
async def run_ai():
    global _sim_data
    if not _sim_data:
        _sim_data = gen_records(500)
    anomalies = sum(1 for r in _sim_data if r["is_anomaly"])
    participation = sum(1 for r in _sim_data if r["participated"]) / len(_sim_data)
    change = round((participation - 0.55)*100, 1)
    beta = 0.18 + random.uniform(0,0.15)
    participation_score = min(100, 50 + change*3)
    anomaly_score = max(0, 100 - (anomalies/500)*500)
    did_score = min(100, 50 + beta*100)
    ahp = round(participation_score*0.40 + participation*100*0.35 + anomaly_score*0.25, 2)
    policy = "강화" if ahp>=70 else "유지" if ahp>=50 else "완화"
    return {"status":"ok","ahp_score":ahp,"policy_action":policy,"xgboost_label":f"참여율 ↑{abs(change):.0f}%","anomaly_count":anomalies,"did_beta":round(beta,3),"did_result":f"DiD β=+{beta:.2f}","participation_change":change,"predicted_issue":int(8000+ahp*30),"effect_score":round(min(100,ahp+25),1)}
