from unittest.mock import MagicMock

import pytest
from pydantic import SecretStr

from src.flask_app import create_app
from src.messages import SlackMessage
from tests.helpers import read_payload_as_json


@pytest.fixture()
def client():
    app = create_app()
    app.config.update({"TESTING": True})
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def random_event():
    return read_payload_as_json("comment_added")


@pytest.fixture
def slack(monkeypatch):
    mocked_slack = MagicMock()
    monkeypatch.setattr("src.api.send_direct_message", mocked_slack)
    return mocked_slack


def test_request_not_authorized(client, monkeypatch):
    monkeypatch.setattr("src.settings.conf.API_KEY", SecretStr("foo"))

    resp = client.post("/")
    assert resp.status_code == 401, "X-API-KEY is missing"

    resp = client.post("/", headers={"X-API-KEY": "bar"})
    assert resp.status_code == 401, "X-API-KEY is not correct"


def test_request_is_parsed(client, monkeypatch, random_event, slack, snapshot):
    monkeypatch.setattr("src.settings.conf.API_KEY", SecretStr("foo"))

    resp = client.post("/", headers={"X-API-KEY": "foo"}, json=random_event)
    assert resp.status_code == 200

    msg: SlackMessage = slack.call_args_list[0][0][0]
    assert msg.receiver == "jack-slack-id"
    assert msg.get_blocks() == snapshot


def test_request_is_parsed_without_api_key(
    client, monkeypatch, random_event, slack, snapshot
):
    monkeypatch.setattr("src.settings.conf.API_KEY", None)
    resp = client.post("/", json=random_event)
    assert resp.status_code == 200

    msg: SlackMessage = slack.call_args_list[0][0][0]
    assert msg.receiver == "jack-slack-id"
    assert msg.get_blocks() == snapshot
