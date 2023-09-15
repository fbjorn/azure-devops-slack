import re
from abc import abstractmethod

from pydantic import BaseModel

from src.schemas import DevOpsEvent
from src.utils import convert_links_to_slack_md


class SlackMessage(BaseModel):
    receiver: str
    evt: DevOpsEvent

    @abstractmethod
    def get_blocks(self) -> list:
        raise NotImplementedError

    def get_payload(self):
        return {"blocks": [self.get_blocks()]}


class PRCreated(SlackMessage):
    def get_blocks(self):
        text = convert_links_to_slack_md(self.evt.message.markdown)
        text += " and added you as a reviewer"
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text,
                },
            }
        ]


class CommentAdded(SlackMessage):
    def get_blocks(self) -> list:
        author = self.evt.resource.comment.author.name
        pr_title = self.evt.resource.pr.title
        repo = self.evt.resource.pr.repository.name
        pr = self.evt.resource.pr
        pr_url = f"{pr.repository.url}/pullrequest/{pr.id}"
        comment_url = f"{pr_url}?discussionId={self.evt.resource.comment.thread_id}"

        text = self.evt.resource.comment.content
        pics = re.findall(r"!\[.*?]\(.*?\)", text)
        for i, pic in enumerate(pics):
            text = text.replace(pic, "[SCREENSHOT]")

        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{author} left a* <{comment_url}|comment>*:*",
                },
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"{text}"},
            },
            {
                "type": "context",
                "elements": [{"type": "mrkdwn", "text": f"*{repo}* / {pr_title}"}],
            },
        ]


class PRStatusChanged(SlackMessage):
    def get_blocks(self) -> list:
        approved = "approved pull request" in self.evt.message.text
        waiting = "waiting for" in self.evt.message.text
        text = convert_links_to_slack_md(self.evt.message.markdown)
        if approved:
            text = f"✅ {text}"
        elif waiting:
            text = f"🚧 {text}"

        if waiting or approved:
            return [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": text,
                    },
                },
            ]
