import secrets

from flask import Request, Response

from src.handlers import compose_messages_from_event
from src.schemas import DevOpsEvent
from src.settings import conf
from src.slack import send_direct_message


def handle_api_event(request: Request):
    api_key = request.headers.get("X-API-KEY")
    if conf.API_KEY and not secrets.compare_digest(
        conf.API_KEY.get_secret_value(), api_key
    ):
        return Response(status=401)

    payload = request.get_json(silent=True) or {}
    if conf.LOG_EVENTS:
        print(payload)

    event = DevOpsEvent(**payload)
    messages = compose_messages_from_event(event)
    for message in messages:
        send_direct_message(message)

    return "OK"
