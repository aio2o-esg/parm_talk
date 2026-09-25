import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
import pickle
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'ai_analysis', 'data')
MODEL_DIR = os.path.join(BASE_DIR, 'ai_analysis', 'models')

def train_isolation_forest():
    print("🔍 Isolation Forest 이상행위 탐지 모델 학습 시작...")

    # 데이터 로드
    citizen_df = pd.read_csv(f'{DATA_DIR}/Citizen_ESG_Participation.csv')

    # 전처리
    le_region = LabelEncoder()
    le_activity = LabelEncoder()
    le_category = LabelEncoder()

    citizen_df['region_enc'] = le_region.fit_transform(citizen_df['region'])
    citizen_df['activity_enc'] = le_activity.fit_transform(citizen_df['activity_type'])
    citizen_df['category_enc'] = le_category.fit_transform(citizen_df['esg_category'])

    # 피처 설정
    features = ['region_enc', 'activity_enc', 'category_enc',
                'reward_amount', 'participation_score']
    X = citizen_df[features]

    # 모델 학습
    anomaly_threshold = 0.15
    model = IsolationForest(
        contamination=anomaly_threshold,
        random_state=42,
        n_estimators=100
    )
    model.fit(X)

    # 이상 점수 계산
    citizen_df['anomaly_score'] = model.decision_function(X)
    citizen_df['predicted_anomaly'] = model.predict(X)
    # -1: 이상, 1: 정상 → 0/1로 변환
    citizen_df['is_predicted_anomaly'] = (citizen_df['predicted_anomaly'] == -1).astype(int)

    # 결과 분석
    total = len(citizen_df)
    detected = citizen_df['is_predicted_anomaly'].sum()
    actual = citizen_df['is_anomaly'].sum()

    print(f"  전체 데이터: {total}건")
    print(f"  실제 이상행위: {actual}건")
    print(f"  탐지된 이상행위: {detected}건")
    print(f"  탐지율: {detected/total*100:.1f}%")

    # 모델 저장
    model_path = os.path.join(MODEL_DIR, 'isolation_forest_model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"  모델 저장 완료: {model_path}")

    # 탐지 함수 테스트
    def detect_anomaly(region_enc, activity_enc, category_enc, reward_amount, participation_score):
        X_new = pd.DataFrame(
            [[region_enc, activity_enc, category_enc, reward_amount, participation_score]],
            columns=features
        )
        score = model.decision_function(X_new)[0]
        is_anomaly = model.predict(X_new)[0] == -1
        return {
            'anomaly_score': round(float(score), 4),
            'is_anomaly': bool(is_anomaly)
        }

    # 테스트
    result = detect_anomaly(0, 0, 0, 1000, 99.9)
    print(f"  테스트 탐지 (비정상 케이스): {result}")

    print("✅ Isolation Forest 모델 학습 완료!")
    return model

if __name__ == '__main__':
    train_isolation_forest()