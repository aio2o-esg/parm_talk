from algosdk.v2client import algod
from algosdk import transaction, account
from algosdk.transaction import AssetConfigTxn
import os

# .env 로드
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

def create_esg_gold_asa():
    print("🪙 ESG-Gold ASA 생성 시작...")

    # 환경변수에서 계정 정보 로드
    address = os.getenv('ALGORAND_ADDRESS')
    private_key = os.getenv('ALGORAND_PRIVATE_KEY')

    if not address or not private_key:
        print("❌ .env 파일에 ALGORAND_ADDRESS, ALGORAND_PRIVATE_KEY를 설정해 주세요.")
        return

    print(f"  운영 계정: {address}")

    # Algod 클라이언트
    client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

    # 트랜잭션 파라미터
    params = client.suggested_params()

    # ASA 생성 트랜잭션
    txn = AssetConfigTxn(
        sender=address,
        sp=params,
        default_frozen=False,
        unit_name="ESGG",
        asset_name="ESG-Gold",
        manager=address,
        reserve=address,
        freeze=address,
        clawback=address,
        url="https://sme-talk.algorand.io",
        total=10_000_000,        # 총 발행량 1천만 ESGG
        decimals=2,              # 소수점 2자리
    )

    # 서명 및 전송
    signed_txn = txn.sign(private_key)
    tx_id = client.send_transaction(signed_txn)
    print(f"  트랜잭션 전송 완료: {tx_id}")

    # 확정 대기
    print("  블록 확정 대기 중...")
    result = transaction.wait_for_confirmation(client, tx_id, 4)

    # ASA ID 확인
    asset_id = result['asset-index']
    print(f"  ✅ ESG-Gold ASA 생성 완료!")
    print(f"  ASA ID: {asset_id}")
    print(f"  TX Hash: {tx_id}")
    print(f"  AlgoExplorer: https://testnet.algoexplorer.io/asset/{asset_id}")

    # .env에 ASA ID 저장 안내
    print(f"\n  📝 .env 파일에 아래 내용을 추가하세요:")
    print(f"  ESG_GOLD_ASA_ID={asset_id}")

    return asset_id, tx_id

if __name__ == '__main__':
    create_esg_gold_asa()