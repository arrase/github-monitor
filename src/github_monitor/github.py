from dataclasses import dataclass, field

import requests

from github_monitor.config import Config

GRAPHQL_URL = "https://api.github.com/graphql"
TIMEOUT_SECONDS = 30

PULL_REQUESTS_QUERY = """
query($owner: String!, $name: String!, $after: String) {
  repository(owner: $owner, name: $name) {
    pullRequests(states: OPEN, first: 100, after: $after) {
      pageInfo { hasNextPage endCursor }
      nodes { number title url }
    }
  }
}
"""

ISSUES_QUERY = """
query($owner: String!, $name: String!, $after: String) {
  repository(owner: $owner, name: $name) {
    issues(states: OPEN, first: 100, after: $after) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number title url
        author { login }
        comments(last: 1) { nodes { author { login } } }
      }
    }
  }
}
"""


class GitHubError(Exception):
    pass


@dataclass(frozen=True)
class Item:
    repo: str
    number: int
    title: str
    url: str


@dataclass(frozen=True)
class RepoStatus:
    repo: str
    pull_requests: list[Item] = field(default_factory=list)
    issues: list[Item] = field(default_factory=list)
    error: str = ""

    @property
    def pending(self) -> list[Item]:
        return self.pull_requests + self.issues


def needs_attention(issue: dict, maintainers: frozenset[str]) -> bool:
    """Author is None when GitHub reports a deleted user ("ghost")."""
    comments = issue["comments"]["nodes"]
    author = comments[0]["author"] if comments else issue["author"]
    return not author or author["login"].lower() not in maintainers


def fetch_nodes(session: requests.Session, repo: str, query: str, connection: str) -> list[dict]:
    owner, name = repo.split("/")
    nodes = []
    after = None
    while True:
        variables = {"owner": owner, "name": name, "after": after}
        response = session.post(GRAPHQL_URL, json={"query": query, "variables": variables}, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        payload = response.json()
        if "errors" in payload:
            raise GitHubError(payload["errors"][0]["message"])
        page = payload["data"]["repository"][connection]
        nodes.extend(page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            return nodes
        after = page["pageInfo"]["endCursor"]


def to_item(repo: str, node: dict) -> Item:
    return Item(repo=repo, number=node["number"], title=node["title"], url=node["url"])


def fetch_repo_status(session: requests.Session, repo: str, maintainers: frozenset[str]) -> RepoStatus:
    pull_requests = fetch_nodes(session, repo, PULL_REQUESTS_QUERY, "pullRequests")
    issues = fetch_nodes(session, repo, ISSUES_QUERY, "issues")
    return RepoStatus(
        repo=repo,
        pull_requests=[to_item(repo, node) for node in pull_requests],
        issues=[to_item(repo, node) for node in issues if needs_attention(node, maintainers)],
    )


def fetch_all(config: Config, session: requests.Session) -> list[RepoStatus]:
    statuses = []
    for repo in config.repositories:
        try:
            statuses.append(fetch_repo_status(session, repo, config.maintainers))
        except (requests.RequestException, GitHubError) as exc:
            statuses.append(RepoStatus(repo=repo, error=str(exc)))
    return statuses


def create_session(token: str) -> requests.Session:
    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {token}"
    return session
