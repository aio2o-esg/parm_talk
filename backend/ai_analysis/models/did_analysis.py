import pandas as pd
import numpy as np
from statsmodels.formula.api import ols
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'ai_analysis', 'data')

def run_did_analysis():
    print("📈 DiD 정책 효과 분석 시작...")

    # 데이터 로드
    citizen_df = pd.read_csv(f'{DATA_DIR}/Citizen_ESG_Participation.csv')
    policy_df = pd.read_csv(f'{DATA_DIR}/Local_Government_Policy.csv')

    # 날짜 변환
    citizen_df['date'] = pd.to_datetime(citizen_df['date'])
    policy_df['date'] = pd.to_datetime(policy_df['date'])

    # 정책 적용 시점 기준 (중간 날짜)
    policy_start = citizen_df['date'].median()

    # 처치군/통제군 설정
    # 처치군: 서울 (정책 강화 적용)
    # 통제군: 부산 (정책 변화 없음)
    treatment_region = '서울'
    control_region = '부산'

    df_did = citizen_df[citizen_df['region'].isin([treatment_region, control_region])].copy()
    df_did['treated'] = (df_did['region'] == treatment_region).astype(int)
    df_did['post'] = (df_did['date'] >= policy_start).astype(int)
    df_did['did'] = df_did['treated'] * df_did['post']

    # DiD 회귀 분석
    model = ols('participation_score ~ treated + post + did', data=df_did).fit()

    # 결과 추출
    did_coef = model.params.get('did', 0)
    did_pvalue = model.pvalues.get('did', 1)
    r_squared = model.rsquared

    print(f"  정책 적용 시점: {policy_start.date()}")
    print(f"  처치군: {treatment_region} / 통제군: {control_region}")
    print(f"  DiD 계수 (정책 효과): {did_coef:.4f}")
    print(f"  p-value: {did_pvalue:.4f}")
    print(f"  R-squared: {r_squared:.4f}")

    # 정책 효과 해석
    if did_pvalue < 0.05:
        significance = "통계적으로 유의함 (p<0.05)"
    elif did_pvalue < 0.10:
        significance = "약한 유의성 (p<0.10)"
    else:
        significance = "통계적으로 유의하지 않음"

    effect_direction = "긍정적" if did_coef > 0 else "부정적"

    print(f"  정책 효과 방향: {effect_direction}")
    print(f"  통계적 유의성: {significance}")

    # 전후 평균 참여율 비교
    pre_treatment = df_did[(df_did['treated']==1) & (df_did['post']==0)]['participation_score'].mean()
    post_treatment = df_did[(df_did['treated']==1) & (df_did['post']==1)]['participation_score'].mean()
    pre_control = df_did[(df_did['treated']==0) & (df_did['post']==0)]['participation_score'].mean()
    post_control = df_did[(df_did['treated']==0) & (df_did['post']==1)]['participation_score'].mean()

    print(f"\n  [정책 적용 전/후 평균 참여율]")
    print(f"  처치군 전: {pre_treatment:.2f} → 후: {post_treatment:.2f} (변화: {post_treatment-pre_treatment:+.2f})")
    print(f"  통제군 전: {pre_control:.2f} → 후: {post_control:.2f} (변화: {post_control-pre_control:+.2f})")

    result = {
        'did_coefficient': round(did_coef, 4),
        'p_value': round(did_pvalue, 4),
        'r_squared': round(r_squared, 4),
        'effect_direction': effect_direction,
        'significance': significance,
        'pre_treatment_mean': round(pre_treatment, 2),
        'post_treatment_mean': round(post_treatment, 2),
        'policy_effect_score': round(abs(did_coef) * 100, 2),
    }

    print("\n✅ DiD 분석 완료!")
    return result

if __name__ == '__main__':
    run_did_analysis()