from src.handlers import compose_messages_from_event
from tests.helpers import get_slack_payload_list, read_payload


def test_pr_created_no_reviewers():
    event = read_payload("pr_created_no_reviewers")
    messages = compose_messages_from_event(event)
    assert messages == []


def test_pr_created_with_reviewers(snapshot_json):
    payload_list = get_slack_payload_list("pr_created_with_reviewers")
    assert payload_list == snapshot_json


def test_comment_added(snapshot_json):
    payload_list = get_slack_payload_list("comment_added")
    assert payload_list == snapshot_json


def test_comment_with_screenshot(snapshot_json):
    payload_list = get_slack_payload_list("comment_with_screenshot")
    assert payload_list == snapshot_json


def test_comment_left_for_a_specific_line(snapshot_json):
    payload_list = get_slack_payload_list("comment_for_a_line")
    assert payload_list == snapshot_json


def test_general_comment_left(snapshot_json):
    payload_list = get_slack_payload_list("comment_without_a_file")
    assert payload_list == snapshot_json


def test_pr_approved(snapshot_json):
    payload_list = get_slack_payload_list("pr_approved")
    assert payload_list == snapshot_json


def test_wait_for_changes(snapshot_json):
    payload_list = get_slack_payload_list("wait_for_changes")
    assert payload_list == snapshot_json


def test_ms_event_comment_added(snapshot_json):
    # TODO: Fix None in the URL
    payload_list = get_slack_payload_list("ms_comment_added")
    assert payload_list == snapshot_json


# TODO:
# def test_reviewer_assigned(snapshot_json):
