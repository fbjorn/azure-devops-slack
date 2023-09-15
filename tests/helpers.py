import json
from pathlib import Path

from src.handlers import compose_messages_from_event
from src.messages import SlackMessage
from src.schemas import DevOpsEvent


def read_payload_as_json(name: str) -> dict:
    path = Path(__file__).parent / "samples" / f"{name}.json"
    return json.loads(path.read_text("utf-8"))


def read_payload(name: str) -> DevOpsEvent:
    raw_json = read_payload_as_json(name)
    return DevOpsEvent(**raw_json)


def slack_message_repr(msg: SlackMessage):
    return {
        "send_to": msg.receiver,
        "payload": msg.get_blocks(),
    }


def get_slack_payload_list(name: str) -> list[dict]:
    event = read_payload(name)
    messages = compose_messages_from_event(event)
    return [slack_message_repr(m) for m in messages]
