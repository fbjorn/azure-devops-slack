import requests

from src.messages import SlackMessage
from src.settings import conf

POST_MESSAGE_URL = "https://slack.com/api/chat.postMessage"


def send_direct_message(message: SlackMessage):
    if not conf.SLACK_BOT_TOKEN:
        raise ValueError("Slack bot token is missing")

    resp = requests.post(
        POST_MESSAGE_URL,
        headers={
            "Accept": "Application/JSON",
            "Authorization": f"Bearer {conf.SLACK_BOT_TOKEN.get_secret_value()}",
        },
        json={
            "channel": message.receiver,
            "blocks": message.get_blocks(),
        },
    )
    if resp.status_code != 200:
        print("Error while sending Slack message")
