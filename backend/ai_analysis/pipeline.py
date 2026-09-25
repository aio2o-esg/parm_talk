import os
import sys

# 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from ai_analysis.models.xgboost_participation import train_participation_model
from ai_analysis.models.isolation_forest import train_isolation_forest
from ai_analysis.models.did_analysis import run_did_analysis
from ai_analysis.policy_scoring import calculate_policy_score

def run_full_pipeline():
    print("=" * 50)
    print("🚀 SME-TALK AI 분석 파이프라인 시작")
    print("=" * 50)

    # Step 1: XGBoost 참여 패턴 분석
    print("\n[Step 1/4] XGBoost 참여 패턴 분석")
    print("-" * 40)
    train_participation_model()

    # Step 2: Isolation Forest 이상행위 탐지
    print("\n[Step 2/4] Isolation Forest 이상행위 탐지")
    print("-" * 40)
    train_isolation_forest()

    # Step 3: DiD 정책 효과 분석
    print("\n[Step 3/4] DiD 정책 효과 분석")
    print("-" * 40)
    did_result = run_did_analysis()

    # Step 4: AHP 정책 스코어링
    print("\n[Step 4/4] AHP 정책 스코어링")
    print("-" * 40)
    score_result = calculate_policy_score()

    print("\n" + "=" * 50)
    print("✅ AI 분석 파이프라인 전체 완료!")
    print(f"  종합 정책 점수: {score_result['policy_score']}")
    print(f"  정책 권고: {score_result['recommendation']}")
    print(f"  권고 파라미터:")
    for k, v in score_result['new_params'].items():
        print(f"    {k}: {v}")
    print("=" * 50)

    return score_result

if __name__ == '__main__':
    run_full_pipeline()