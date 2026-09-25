import pandas as pd
import numpy as np
import pickle
import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'ai_analysis', 'data')
MODEL_DIR = os.path.join(BASE_DIR, 'ai_analysis', 'models')

# AHP 가중치 (논문 기준)
AHP_WEIGHTS = {
    'participation_score': 0.50,  # XGBoost 참여 패턴
    'anomaly_score': 0.30,        # Isolation Forest 이상행위
    'did_effect': 0.20,           # DiD 정책 효과
}

def load_models():
    with open(os.path.join(MODEL_DIR, 'xgboost_model.pkl'), 'rb') as f:
        xgb_model = pickle.load(f)
    with open(os.path.join(MODEL_DIR, 'isolation_forest_model.pkl'), 'rb') as f:
        if_model = pickle.load(f)
    return xgb_model, if_model

def calculate_policy_score():
    print("⚖️ AHP 기반 정책 스코어링 시작...")

    # 데이터 로드
    citizen_df = pd.read_csv(f'{DATA_DIR}/Citizen_ESG_Participation.csv')
    from sklearn.preprocessing import LabelEncoder
    le_region = LabelEncoder()
    le_activity = LabelEncoder()
    le_category = LabelEncoder()
    citizen_df['region_enc'] = le_region.fit_transform(citizen_df['region'])
    citizen_df['activity_enc'] = le_activity.fit_transform(citizen_df['activity_type'])
    citizen_df['category_enc'] = le_category.fit_transform(citizen_df['esg_category'])

    features = ['region_enc', 'activity_enc', 'category_enc', 'reward_amount', 'is_anomaly']

    # 모델 로드
    xgb_model, if_model = load_models()

    # 1. XGBoost 참여 점수
    xgb_scores = xgb_model.predict(citizen_df[features])
    avg_participation = float(np.mean(xgb_scores))
    normalized_participation = min(avg_participation / 100.0, 1.0)

    # 2. Isolation Forest 이상행위 점수
    if_features = ['region_enc', 'activity_enc', 'category_enc', 'reward_amount', 'participation_score']
    anomaly_scores = if_model.decision_function(citizen_df[if_features])
    anomaly_rate = float(np.mean(if_model.predict(citizen_df[if_features]) == -1))
    normalized_anomaly = 1.0 - anomaly_rate  # 이상행위 적을수록 높은 점수

    # 3. DiD 효과 점수 (고정값 사용)
    did_effect = 0.4375
    normalized_did = min(abs(did_effect) / 10.0, 1.0)

    # AHP 종합 점수 계산
    policy_score = (
        normalized_participation * AHP_WEIGHTS['participation_score'] +
        normalized_anomaly * AHP_WEIGHTS['anomaly_score'] +
        normalized_did * AHP_WEIGHTS['did_effect']
    ) * 100

    print(f"  참여 패턴 점수 (XGBoost): {normalized_participation*100:.2f}")
    print(f"  이상행위 정상률 (IF): {normalized_anomaly*100:.2f}%")
    print(f"  정책 효과 점수 (DiD): {normalized_did*100:.2f}")
    print(f"  AHP 종합 정책 점수: {policy_score:.2f}")

    # 정책 파라미터 권고값 산출
    if policy_score >= 70:
        # 정책 강화
        new_params = {
            'reward_rate_env': 0.07,
            'sme_bonus_rate': 0.12,
            'anomaly_threshold': 0.15,
            'monthly_issue_cap': 12000,
            'policy_status': 'ACTIVE',
        }
        recommendation = '정책 강화'
    elif policy_score >= 50:
        # 현상 유지
        new_params = {
            'reward_rate_env': 0.05,
            'sme_bonus_rate': 0.10,
            'anomaly_threshold': 0.15,
            'monthly_issue_cap': 10000,
            'policy_status': 'ACTIVE',
        }
        recommendation = '현상 유지'
    else:
        # 정책 완화
        new_params = {
            'reward_rate_env': 0.03,
            'sme_bonus_rate': 0.08,
            'anomaly_threshold': 0.20,
            'monthly_issue_cap': 8000,
            'policy_status': 'ACTIVE',
        }
        recommendation = '정책 완화'

    print(f"\n  📋 정책 권고: {recommendation}")
    print(f"  권고 파라미터: {json.dumps(new_params, ensure_ascii=False)}")

    # 결과 저장
    result = {
        'timestamp': datetime.now().isoformat(),
        'policy_score': round(policy_score, 2),
        'recommendation': recommendation,
        'new_params': new_params,
        'metrics': {
            'participation': round(normalized_participation * 100, 2),
            'anomaly_normal_rate': round(normalized_anomaly * 100, 2),
            'did_effect': round(normalized_did * 100, 2),
        }
    }

    result_path = os.path.join(MODEL_DIR, 'policy_score_result.json')
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n  결과 저장 완료: {result_path}")
    print("✅ AHP 정책 스코어링 완료!")
    return result

if __name__ == '__main__':
    calculate_policy_score()