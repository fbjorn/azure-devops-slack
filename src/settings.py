from pathlib import Path
from typing import Optional

from pydantic import BaseModel, BaseSettings, SecretStr


class UserConfig(BaseModel):
    name_filter: str | None
    emails: list[str]
    slack_id: str


class Conf(BaseSettings):
    API_KEY: Optional[SecretStr]
    SLACK_BOT_TOKEN: Optional[SecretStr]
    USERS: list[UserConfig] = []
    LOG_EVENTS: bool = False

    class Config:
        env_file = Path(__file__).parent.parent / ".env"


conf = Conf()
