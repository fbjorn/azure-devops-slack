import json
import os
from pathlib import Path

import functions_framework
from flask import Request

from src.api import handle_api_event


@functions_framework.http
def devops_webhook(request: Request):
    return handle_api_event(request)


@functions_framework.http
def debug(request: Request):
    payload = request.get_json(silent=True) or {}
    print(payload)
    return "OK"


@functions_framework.http
def save_sample(request: Request):
    filename = os.environ["NAME"]

    payload = request.get_json(silent=True) or {}
    path = Path(__file__).parent / "tests" / "samples" / f"{filename}.json"
    path.write_text(json.dumps(payload), "utf-8")
    print(f"{path} written")
    return "OK"
