import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)
N = 500
start_date = datetime(2025, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(N)]

# Table Ⅳ-1: 지자체 정책 데이터
policy_df = pd.DataFrame({
    'date': dates,
    'policy_id': [f'POL{i:04d}' for i in range(N)],
    'region': np.random.choice(['서울', '부산', '대구', '인천'], N),
    'reward_rate': np.random.uniform(0.03, 0.10, N).round(3),
    'sme_bonus_rate': np.random.uniform(0.05, 0.20, N).round(3),
    'anomaly_threshold': np.random.uniform(0.10, 0.30, N).round(3),
    'monthly_issue_cap': np.random.randint(5000, 20000, N),
    'policy_status': np.random.choice(['ACTIVE', 'SUSPENDED'], N, p=[0.9, 0.1]),
})

# Table Ⅳ-2: 소상공인 ESG 활동 데이터
merchant_df = pd.DataFrame({
    'date': np.random.choice(dates, N),
    'merchant_id': [f'MER{i:04d}' for i in np.random.randint(0, 100, N)],
    'region': np.random.choice(['서울', '부산', '대구', '인천'], N),
    'esg_type': np.random.choice(['E', 'S', 'G'], N),
    'activity_count': np.random.randint(1, 50, N),
    'reward_issued': np.random.randint(100, 5000, N),
    'verified': np.random.choice([True, False], N, p=[0.85, 0.15]),
})

# Table Ⅳ-3: 시민 ESG 참여 데이터
citizen_df = pd.DataFrame({
    'date': np.random.choice(dates, N),
    'citizen_id': [f'CIT{i:04d}' for i in np.random.randint(0, 200, N)],
    'region': np.random.choice(['서울', '부산', '대구', '인천'], N),
    'activity_type': np.random.choice(['qr', 'gps', 'auto'], N),
    'esg_category': np.random.choice(['E', 'S', 'G'], N),
    'participation_score': np.random.uniform(0, 100, N).round(2),
    'reward_amount': np.random.randint(10, 200, N),
    'is_anomaly': np.random.choice([0, 1], N, p=[0.95, 0.05]),
})

# Table Ⅳ-4: ESG-Gold 온체인 트랜잭션
transaction_df = pd.DataFrame({
    'date': np.random.choice(dates, N),
    'tx_hash': [f'TX{i:08x}' for i in np.random.randint(0, 10**8, N)],
    'from_address': [f'ALGO{i:06d}' for i in np.random.randint(0, 1000, N)],
    'to_address': [f'ALGO{i:06d}' for i in np.random.randint(0, 1000, N)],
    'amount': np.random.randint(10, 500, N),
    'asset_id': np.random.choice([12345678], N),
    'confirmed': np.random.choice([True, False], N, p=[0.98, 0.02]),
    'confirm_time_sec': np.random.uniform(3.0, 6.0, N).round(2),
})

# Table Ⅳ-5: ESG 스폰서 펀딩
sponsor_df = pd.DataFrame({
    'date': np.random.choice(dates, N),
    'sponsor_id': [f'SPO{i:04d}' for i in np.random.randint(0, 50, N)],
    'region': np.random.choice(['서울', '부산', '대구', '인천'], N),
    'funding_amount': np.random.randint(100000, 5000000, N),
    'esg_category': np.random.choice(['E', 'S', 'G'], N),
    'used_amount': np.random.randint(50000, 3000000, N),
})

# 저장
output_dir = os.path.dirname(os.path.abspath(__file__))
policy_df.to_csv(f'{output_dir}/Local_Government_Policy.csv', index=False)
merchant_df.to_csv(f'{output_dir}/Local_Producer_ESG_Activity.csv', index=False)
citizen_df.to_csv(f'{output_dir}/Citizen_ESG_Participation.csv', index=False)
transaction_df.to_csv(f'{output_dir}/ESG_Gold_OnChain_Transaction.csv', index=False)
sponsor_df.to_csv(f'{output_dir}/ESG_Sponsor_Funding.csv', index=False)

print("✅ 시뮬레이션 데이터 생성 완료!")
print(f"  - Local_Government_Policy.csv: {len(policy_df)}행")
print(f"  - Local_Producer_ESG_Activity.csv: {len(merchant_df)}행")
print(f"  - Citizen_ESG_Participation.csv: {len(citizen_df)}행")
print(f"  - ESG_Gold_OnChain_Transaction.csv: {len(transaction_df)}행")
print(f"  - ESG_Sponsor_Funding.csv: {len(sponsor_df)}행")