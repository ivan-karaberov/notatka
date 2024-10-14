from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

BASE_DIR = Path(__file__).parent.parent


class DbSettings(BaseSettings):
    DB_USER: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_PASS: str
    echo: bool = False

    def get_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int


class AuthJWT(BaseSettings):
    private_key_path: Path = BASE_DIR / "core" / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "core" / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_minutes: int = 4300


class AppSettings(BaseSettings):
    APP_HOST: str
    APP_PORT: int
    confirmation_code_expire_minutes: int = 5

    def get_url(self):
        return f"{self.APP_HOST}:{self.APP_PORT}"


class BrokerSettings(BaseSettings):
    KAFKA_HOST: str
    KAFKA_PORT: int

    def get_url(self):
        return f"{self.KAFKA_HOST}:{self.KAFKA_PORT}"


class Settings(BaseSettings):
    db: DbSettings = DbSettings()
    app: AppSettings = AppSettings()
    redis: RedisSettings = RedisSettings()
    broker: BrokerSettings = BrokerSettings()
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()