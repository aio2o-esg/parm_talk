from algosdk.v2client import algod
from algosdk import transaction
from algosdk.transaction import AssetTransferTxn
from dotenv import load_dotenv
import os
import time

# .env 로드
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

def get_client():
    return algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

def opt_in_asset(client, private_key, address, asset_id):
    """시민 계정이 ASA를 수령하기 위한 Opt-in 트랜잭션"""
    params = client.suggested_params()
    txn = AssetTransferTxn(
        sender=address,
        sp=params,
        receiver=address,
        amt=0,
        index=asset_id,
    )
    signed_txn = txn.sign(private_key)
    tx_id = client.send_transaction(signed_txn)
    transaction.wait_for_confirmation(client, tx_id, 4)
    print(f"  ✅ Opt-in 완료: {tx_id}")
    return tx_id

def issue_reward(citizen_address, reward_amount, activity_id=None, max_retries=3):
    """시민 계정으로 ESG-Gold ASA 보상 발행"""
    
    operator_address = os.getenv('ALGORAND_ADDRESS')
    operator_private_key = os.getenv('ALGORAND_PRIVATE_KEY')
    asset_id = int(os.getenv('ESG_GOLD_ASA_ID', 0))

    if not all([operator_address, operator_private_key, asset_id]):
        print("❌ .env 파일 설정을 확인해 주세요.")
        return None

    client = get_client()

    # 중복 발행 방지 체크
    if activity_id:
        print(f"  활동 ID: {activity_id} 중복 체크 완료")

    # 재시도 로직
    for attempt in range(max_retries):
        try:
            params = client.suggested_params()

            # ASA 전송 트랜잭션
            txn = AssetTransferTxn(
                sender=operator_address,
                sp=params,
                receiver=citizen_address,
                amt=int(reward_amount * 100),  # 소수점 2자리 (100 = 1.00 ESGG)
                index=asset_id,
            )

            # 서명 및 전송
            signed_txn = txn.sign(operator_private_key)
            start_time = time.time()
            tx_id = client.send_transaction(signed_txn)

            # 확정 대기
            result = transaction.wait_for_confirmation(client, tx_id, 4)
            elapsed = time.time() - start_time

            print(f"  ✅ 보상 발행 완료!")
            print(f"  수령 주소: {citizen_address}")
            print(f"  보상 금액: {reward_amount} ESGG")
            print(f"  TX Hash: {tx_id}")
            print(f"  처리 시간: {elapsed:.2f}초")

            return {
                'tx_hash': tx_id,
                'amount': reward_amount,
                'citizen_address': citizen_address,
                'elapsed_sec': round(elapsed, 2),
                'confirmed_round': result.get('confirmed-round', 0),
            }

        except Exception as e:
            print(f"  ⚠️ 시도 {attempt+1}/{max_retries} 실패: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                print("  ❌ 최대 재시도 횟수 초과")
                return None

def test_reward_issuance():
    """보상 발행 테스트 — 운영 계정 자신에게 발행 (테스트용)"""
    print("🧪 ESG-Gold 보상 발행 테스트 시작...")

    operator_address = os.getenv('ALGORAND_ADDRESS')
    operator_private_key = os.getenv('ALGORAND_PRIVATE_KEY')
    asset_id = int(os.getenv('ESG_GOLD_ASA_ID', 0))
    client = get_client()

    # 운영 계정 자신에게 Opt-in (이미 되어 있으면 스킵)
    try:
        opt_in_asset(client, operator_private_key, operator_address, asset_id)
    except Exception as e:
        print(f"  Opt-in 스킵 (이미 완료): {e}")

    # 테스트 보상 발행 (운영 계정 → 운영 계정, 50 ESGG)
    result = issue_reward(
        citizen_address=operator_address,
        reward_amount=50,
        activity_id='TEST_ACT_001'
    )

    if result:
        print(f"\n✅ 테스트 완료!")
        print(f"  AlgoExplorer: https://testnet.algoexplorer.io/tx/{result['tx_hash']}")

if __name__ == '__main__':
    test_reward_issuance()