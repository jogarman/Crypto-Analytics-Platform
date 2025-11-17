from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    mongo_uri: str = Field("mongodb://localhost:27017", env="MONGO_URI")
    mongo_db: str = Field("crypto_analytics", env="MONGO_DB")
    data_provider: str = Field("mock", env="DATA_PROVIDER")
    secret_key: str = Field("change-me", env="SECRET_KEY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

