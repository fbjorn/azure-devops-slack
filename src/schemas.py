from datetime import datetime

from pydantic import BaseModel, Field


class Person(BaseModel):
    name: str = Field(..., alias="displayName")
    email: str = Field(..., alias="uniqueName")
    id: str


class Links(BaseModel):
    class _Link(BaseModel):
        href: str

    self: _Link
    repository: _Link
    threads: _Link | None


class Comment(BaseModel):
    content: str
    published_date: datetime = Field(..., alias="publishedDate")
    links: Links = Field(..., alias="_links")
    author: Person

    @property
    def thread_id(self) -> str | None:
        if not self.links.threads:
            return None
        threads_url = self.links.threads.href
        return threads_url.split("/")[-1]


class Repository(BaseModel):
    name: str
    url: str = Field(..., alias="webUrl")


class PullRequest(BaseModel):
    repository: Repository
    author: Person = Field(..., alias="createdBy")
    title: str
    description: str | None
    url: str
    reviewers: list[Person]
    id: str = Field(..., alias="pullRequestId")


class Resource(BaseModel):
    comment: Comment | None
    pr: PullRequest | None = Field(None, alias="pullRequest")
    created_by: Person | None = Field(None, alias="createdBy")
    reviewers: list[Person] | None


class Message(BaseModel):
    text: str
    html: str
    markdown: str


class DevOpsEvent(BaseModel):
    event_type: str = Field(..., alias="eventType")
    resource: Resource
    message: Message
    detailed_message: Message = Field(..., alias="detailedMessage")


class EventType:
    PR_COMMENT = "ms.vss-code.git-pullrequest-comment-event"
    PR_UPDATE = "git.pullrequest.updated"
    PR_CREATED = "git.pullrequest.created"
