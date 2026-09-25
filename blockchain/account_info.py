from algosdk.v2client import algod, indexer
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
INDEXER_ADDRESS = "https://testnet-idx.algonode.cloud"

def get_account_assets(address):
    """계정 보유 자산 조회"""
    client = algod.AlgodClient("", ALGOD_ADDRESS)
    info = client.account_info(address)
    
    algo_balance = info['amount'] / 1_000_000
    assets = []
    
    for asset in info.get('assets', []):
        assets.append({
            'asset_id': asset['asset-id'],
            'amount': asset['amount'],
        })
    
    return {
        'address': address,
        'algo_balance': algo_balance,
        'assets': assets,
    }

def get_transaction_history(address, limit=10):
    """계정 온체인 거래 내역 조회"""
    idx = indexer.IndexerClient("", INDEXER_ADDRESS)
    
    response = idx.search_transactions(
        address=address,
        limit=limit,
    )
    
    transactions = []
    for tx in response.get('transactions', []):
        tx_type = tx.get('tx-type', '')
        asset_transfer = tx.get('asset-transfer-transaction', {})
        
        transactions.append({
            'tx_hash': tx.get('id', ''),
            'type': tx_type,
            'amount': asset_transfer.get('amount', 0) / 100 if asset_transfer else 0,
            'asset_id': asset_transfer.get('asset-id', 0),
            'sender': tx.get('sender', ''),
            'receiver': asset_transfer.get('receiver', ''),
            'round': tx.get('confirmed-round', 0),
        })
    
    return transactions

def test_account_info():
    """계정 정보 및 거래 내역 조회 테스트"""
    print("📊 계정 정보 조회 테스트...")
    
    address = os.getenv('ALGORAND_ADDRESS')
    asset_id = int(os.getenv('ESG_GOLD_ASA_ID', 0))
    
    # 자산 조회
    info = get_account_assets(address)
    print(f"\n  주소: {info['address'][:20]}...")
    print(f"  ALGO 잔액: {info['algo_balance']} ALGO")
    
    for asset in info['assets']:
        if asset['asset_id'] == asset_id:
            print(f"  ESG-Gold 잔액: {asset['amount'] / 100} ESGG")
    
    # 거래 내역 조회
    print(f"\n  최근 거래 내역 (최대 5건):")
    txs = get_transaction_history(address, limit=5)
    for tx in txs:
        print(f"    TX: {tx['tx_hash'][:20]}... | {tx['amount']} ESGG | Round: {tx['round']}")
    
    print("\n✅ 계정 정보 조회 완료!")

if __name__ == '__main__':
    test_account_info()