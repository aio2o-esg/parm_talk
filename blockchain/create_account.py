from algosdk import account, mnemonic
import os

def create_algorand_account():
    print("🔑 Algorand 계정 생성...")
    
    # 새 계정 생성
    private_key, address = account.generate_account()
    mnemonic_phrase = mnemonic.from_private_key(private_key)
    
    print(f"  주소: {address}")
    print(f"  Private Key: {private_key}")
    print(f"  Mnemonic: {mnemonic_phrase}")
    print()
    print("⚠️  위 정보를 .env 파일에 저장하세요!")
    print("⚠️  절대 GitHub에 업로드하지 마세요!")
    print()
    print("💧 테스트넷 ALGO 받기:")
    print(f"  https://bank.testnet.algorand.network/")
    print(f"  위 사이트에서 주소를 입력하면 무료 ALGO를 받을 수 있습니다.")
    
    return address, private_key, mnemonic_phrase

if __name__ == '__main__':
    create_algorand_account()