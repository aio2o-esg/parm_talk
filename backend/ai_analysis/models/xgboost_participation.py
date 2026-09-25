import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
import shap
import pickle
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'ai_analysis', 'data')
MODEL_DIR = os.path.join(BASE_DIR, 'ai_analysis', 'models')

def train_participation_model():
    print("📊 XGBoost 참여 패턴 분석 모델 학습 시작...")

    # 데이터 로드
    citizen_df = pd.read_csv(f'{DATA_DIR}/Citizen_ESG_Participation.csv')
    policy_df = pd.read_csv(f'{DATA_DIR}/Local_Government_Policy.csv')

    # 전처리
    le_region = LabelEncoder()
    le_activity = LabelEncoder()
    le_category = LabelEncoder()

    citizen_df['region_enc'] = le_region.fit_transform(citizen_df['region'])
    citizen_df['activity_enc'] = le_activity.fit_transform(citizen_df['activity_type'])
    citizen_df['category_enc'] = le_category.fit_transform(citizen_df['esg_category'])

    # 피처 및 타겟 설정
    features = ['region_enc', 'activity_enc', 'category_enc', 'reward_amount', 'is_anomaly']
    target = 'participation_score'

    X = citizen_df[features]
    y = citizen_df[target]

    # 학습/테스트 분리
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 모델 학습
    model = XGBRegressor(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42
    )
    model.fit(X_train, y_train)

    # 평가
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"  RMSE: {rmse:.4f}")

    # SHAP 설명 가능성
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test[:10])
    print(f"  SHAP 분석 완료 (상위 10개 샘플)")

    # 모델 저장
    model_path = os.path.join(MODEL_DIR, 'xgboost_model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"  모델 저장 완료: {model_path}")

    # E/S/G 축별 점수 예측 함수
    def predict_esg_scores(region, activity_type, reward_amount):
        scores = {}
        for category, enc in [('E', 0), ('S', 1), ('G', 2)]:
            region_enc = le_region.transform([region])[0] if region in le_region.classes_ else 0
            activity_enc = le_activity.transform([activity_type])[0] if activity_type in le_activity.classes_ else 0
            X_new = pd.DataFrame([[region_enc, activity_enc, enc, reward_amount, 0]],
                                 columns=features)
            score = model.predict(X_new)[0]
            scores[category] = round(float(score), 2)
        return scores

    # 테스트 예측
    test_scores = predict_esg_scores('서울', 'qr', 100)
    print(f"  테스트 예측 (서울/QR/100ESGG): E={test_scores['E']}, S={test_scores['S']}, G={test_scores['G']}")

    print("✅ XGBoost 모델 학습 완료!")
    return model

if __name__ == '__main__':
    train_participation_model()