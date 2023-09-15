import pytest
from syrupy.extensions.json import JSONSnapshotExtension

from src.settings import UserConfig, conf


@pytest.fixture(autouse=True)
def known_users(monkeypatch):
    conf.USERS = [
        UserConfig(
            name_filter="Jack Jackson",
            emails=["jack.jackson@myorg.com"],
            slack_id="jack-slack-id",
        ),
        UserConfig(
            name_filter="Jane Doe",
            emails=["jane.doe@myorg.com"],
            slack_id="jane-slack-id",
        ),
        UserConfig(
            name_filter="Kyle Walker",
            emails=["kyle.walker@myorg.com"],
            slack_id="kyle-slack-id",
        ),
        UserConfig(
            name_filter="Jamal",
            emails=["fabrikamfiber4@hotmail.com"],
            slack_id="jamal-slack-id",
        ),
    ]
    yield


@pytest.fixture
def snapshot_json(snapshot):
    return snapshot.with_defaults(extension_class=JSONSnapshotExtension)
