import requests
from requests.auth import HTTPBasicAuth

from src.schemas import APICommit
from src.settings import conf


class DevOpsClient:
    def __init__(self):
        self._auth = HTTPBasicAuth("", conf.DEVOPS_PAT.get_secret_value())

    def _fetch_url(self, url: str) -> dict:
        resp = requests.get(
            url,
            headers={"Content-type": "application/json"},
            auth=self._auth,
        )
        if resp.status_code != 200:
            resp.raise_for_status()

        return resp.json()

    def fetch_commit(self, url: str) -> APICommit | None:
        if not conf.DEVOPS_PAT:
            return None
        return APICommit(**self._fetch_url(url))
