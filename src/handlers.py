from functools import wraps
from typing import List

from src.messages import CommentAdded, PRCreated, PRStatusChanged, SlackMessage
from src.schemas import DevOpsEvent, EventType, Person
from src.settings import UserConfig, conf

EVENT_HANDLERS = {}


def find_user(person: Person) -> UserConfig | None:
    for user in conf.USERS:
        for user_email in user.emails:
            if user_email == person.email:
                return user
    for user in conf.USERS:
        if user.name_filter in person.name.lower():
            return user
    return None


def event_handler(event: EventType):
    def handle_event(fn):
        @wraps(fn)
        def _handle_event(*args, **kwargs):
            result = fn(*args, **kwargs)
            return result if result is not None else []

        EVENT_HANDLERS[event] = _handle_event
        return _handle_event

    return handle_event


def compose_messages_from_event(evt: DevOpsEvent) -> List[SlackMessage]:
    return EVENT_HANDLERS[evt.event_type](evt)


@event_handler(EventType.PR_COMMENT)
def parse_comment_added(evt: DevOpsEvent) -> List[SlackMessage]:
    pr_author_id = evt.resource.pr.author.id
    comment_author_id = evt.resource.comment.author.id

    if pr_author_id != comment_author_id:
        if author := find_user(evt.resource.pr.author):
            return [CommentAdded(receiver=author.slack_id, evt=evt)]
    else:
        # TODO: Author left the comment. Need to check if it's a reply
        #   to another user and notify that user
        return []


@event_handler(EventType.PR_CREATED)
def parse_pr_created_event(evt: DevOpsEvent) -> List[SlackMessage] | None:
    messages = []
    for reviewer in evt.resource.reviewers:
        if user := find_user(reviewer):
            messages.append(PRCreated(receiver=user.slack_id, evt=evt))
    return messages


@event_handler(EventType.PR_UPDATE)
def parse_pr_updated_event(evt: DevOpsEvent) -> List[SlackMessage] | None:
    messages = []
    approved = "approved pull request"
    waits = "is waiting for the author"
    if approved in evt.message.text or waits in evt.message.text:
        if user := find_user(evt.resource.created_by):
            messages.append(PRStatusChanged(receiver=user.slack_id, evt=evt))
    # else:
    #     for reviewer in evt.resource.reviewers:
    #         if user := find_user(reviewer):
    #             messages.append(PRCreated(receiver=user.slack_id, evt=evt))
    return messages
