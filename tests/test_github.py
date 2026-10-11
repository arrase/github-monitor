import pytest
import requests

from github_monitor.config import Config
from github_monitor.github import fetch_all, needs_attention

MAINTAINERS = frozenset({"arrase"})


class FakeResponse:
    def __init__(self, payload: dict):
        self.payload = payload

    def raise_for_status(self):
        pass

    def json(self) -> dict:
        return self.payload


class FakeSession:
    """Serves queued GraphQL pages per (repo, connection)."""

    def __init__(self, pages: dict[tuple[str, str], list[dict]]):
        self.pages = pages

    def post(self, url, json, timeout):
        repo = f"{json['variables']['owner']}/{json['variables']['name']}"
        connection = "pullRequests" if "pullRequests" in json["query"] else "issues"
        return FakeResponse(self.pages[(repo, connection)].pop(0))


def page(connection: str, nodes: list[dict], end_cursor: str | None = None) -> dict:
    page_info = {"hasNextPage": end_cursor is not None, "endCursor": end_cursor}
    return {"data": {"repository": {connection: {"pageInfo": page_info, "nodes": nodes}}}}


def pr(number: int) -> dict:
    return {"number": number, "title": f"PR {number}", "url": f"https://github.com/o/r/pull/{number}"}


def issue(number: int, author: str | None, last_commenter: str | None = None, has_comments: bool = False) -> dict:
    comments = [{"author": {"login": last_commenter} if last_commenter else None}] if has_comments else []
    return {
        "number": number,
        "title": f"Issue {number}",
        "url": f"https://github.com/o/r/issues/{number}",
        "author": {"login": author} if author else None,
        "comments": {"nodes": comments},
    }


def config(*repos: str) -> Config:
    return Config(token="t", repositories=list(repos), maintainers=MAINTAINERS, poll_interval_minutes=5)


@pytest.mark.parametrize(
    ("author", "expected"),
    [("arrase", False), ("ARRASE", False), ("stranger", True), (None, True)],
)
def test_needs_attention(author, expected):
    assert needs_attention(author, MAINTAINERS) is expected


def test_issue_filtering_by_last_responder():
    issues = [
        issue(1, "stranger", "arrase", has_comments=True),
        issue(2, "arrase", "stranger", has_comments=True),
        issue(3, "stranger"),
        issue(4, "Arrase"),
        issue(5, "arrase", None, has_comments=True),
    ]
    session = FakeSession({("o/r", "pullRequests"): [page("pullRequests", [])], ("o/r", "issues"): [page("issues", issues)]})

    [status] = fetch_all(config("o/r"), session)

    assert [item.number for item in status.issues] == [2, 3, 5]


def test_pagination_collects_all_pages():
    session = FakeSession({
        ("o/r", "pullRequests"): [page("pullRequests", [pr(1)], "c1"), page("pullRequests", [pr(2)])],
        ("o/r", "issues"): [page("issues", [issue(3, "x")], "c1"), page("issues", [issue(4, "y")])],
    })

    [status] = fetch_all(config("o/r"), session)

    assert [item.number for item in status.pull_requests] == [1, 2]
    assert [item.number for item in status.issues] == [3, 4]
    assert all(item.kind == "pr" for item in status.pull_requests)


def test_error_is_isolated_per_repository():
    not_found = {"data": {"repository": None}, "errors": [{"message": "Could not resolve to a Repository"}]}
    session = FakeSession({
        ("o/missing", "pullRequests"): [not_found],
        ("o/r", "pullRequests"): [page("pullRequests", [pr(1)])],
        ("o/r", "issues"): [page("issues", [])],
    })

    missing, ok = fetch_all(config("o/missing", "o/r"), session)

    assert missing.error == "Could not resolve to a Repository"
    assert missing.pending == []
    assert ok.error is None
    assert len(ok.pending) == 1


def test_network_error_is_reported():
    class BrokenSession:
        def post(self, url, json, timeout):
            raise requests.ConnectionError("offline")

    [status] = fetch_all(config("o/r"), BrokenSession())

    assert status.error == "offline"
