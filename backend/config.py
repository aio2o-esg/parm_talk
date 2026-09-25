from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str = "postgresql://smetalk:smetalk1234@localhost:5432/smetalk"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str = "your-super-secret-jwt-key"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440
    algod_address: str = "https://testnet-api.algonode.cloud"
    algod_token: str = ""
    indexer_address: str = "https://testnet-idx.algonode.cloud"
    algorand_operator_address: str = ""
    algorand_operator_private_key: str = ""
    esg_gold_asset_id: Optional[int] = None
    app_env: str = "development"

    model_config = {"env_file": "../.env", "extra": "ignore"}

settings = Settings()
