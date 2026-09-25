from algosdk.v2client import algod, indexer

# Algorand 테스트넷 엔드포인트 (무료 공개 노드)
ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

INDEXER_ADDRESS = "https://testnet-idx.algonode.cloud"
INDEXER_TOKEN = ""

def get_algod_client():
    return algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

def get_indexer_client():
    return indexer.IndexerClient(INDEXER_TOKEN, INDEXER_ADDRESS)

def test_connection():
    print("🔗 Algorand 테스트넷 연결 확인...")
    try:
        client = get_algod_client()
        status = client.status()
        print(f"  ✅ 연결 성공!")
        print(f"  최신 블록: {status['last-round']}")
        print(f"  네트워크: testnet")
        return True
    except Exception as e:
        print(f"  ❌ 연결 실패: {e}")
        return False

if __name__ == '__main__':
    test_connection()