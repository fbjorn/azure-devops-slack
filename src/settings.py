from pathlib import Path
from typing import Optional

from pydantic import BaseModel, BaseSettings, SecretStr
from ruamel.yaml import YAML


class UserConfig(BaseModel):
    name_filter: str | None
    emails: list[str]
    slack_id: str


class Conf(BaseSettings):
    API_KEY: Optional[SecretStr]
    DEBUG: bool = False
    DEVOPS_PAT: Optional[SecretStr]
    SLACK_BOT_TOKEN: Optional[SecretStr]
    USERS: list[UserConfig] = []

    class Config:
        env_file = Path(__file__).parent.parent / ".env"

    def __init__(self):
        super().__init__()
        users_yaml = Path(__file__).parent.parent / "users.yaml"
        if users_yaml.exists():
            yaml = YAML()
            content = yaml.load(users_yaml.read_text())
            self.USERS = [UserConfig(**u) for u in content["users"]]


conf = Conf()
