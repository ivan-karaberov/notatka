from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class SMTPSettings(BaseSettings):
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str


class BrokerSettings(BaseSettings):
    BROKER_HOST: str
    BROKER_PORT: int

    def get_url(self):
        return f"{self.BROKER_HOST}:{self.BROKER_PORT}"

class Settings(BaseSettings):
    smtp: SMTPSettings = SMTPSettings()
    broker: BrokerSettings = BrokerSettings()
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    TEMPLATES_DIR: Path = BASE_DIR / "templates"


settings = Settings()