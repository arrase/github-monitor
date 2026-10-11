# Attention Rules

GitHub Monitor does not list everything that is open: it reports what is *waiting for you*. This page describes exactly how each repository is queried and which items count as pending.

---

## What Needs Attention

- **Every open pull request.**
- **Every open issue** whose last comment (or its author, if it has no comments) does not come from someone in `maintainers`.

An issue stops being reported as soon as a maintainer replies, and comes back if someone else comments after that.

---

## The Attention Rule

The rule is a pure function in `github.py`:

```python
def needs_attention(last_author: str | None, maintainers: frozenset[str]) -> bool:
    return last_author is None or last_author.lower() not in maintainers
```

`last_author` is the login of the issue's last comment or, when there are no comments, of the issue author. GitHub reports a deleted account ("ghost") as a `null` author, which is represented by `None` and always needs attention.

| Last activity on the issue | Pending? |
| :--- | :--- |
| Opened by an outsider, no comments | Yes |
| Last comment by an outsider | Yes |
| Last comment by a maintainer | No |
| Opened by a maintainer, no comments | No |
| Last author is a deleted user | Yes |

!!! note
    Bots count as outsiders. If a bot's comments should mark an issue as answered, add its login to `maintainers`.

---

## GitHub GraphQL Queries

Each repository is queried with two paginated connections, both with `states: OPEN`, `first: 100` and an `after` cursor.

=== "Pull requests"

    ```graphql
    query($owner: String!, $name: String!, $after: String) {
      repository(owner: $owner, name: $name) {
        pullRequests(states: OPEN, first: 100, after: $after) {
          pageInfo { hasNextPage endCursor }
          nodes { number title url }
        }
      }
    }
    ```

=== "Issues"

    ```graphql
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
    ```

### Why GraphQL

- `comments(last: 1)` returns the last comment of every issue in the same request. REST can only do that with one request per issue.
- The GraphQL `issues` connection excludes pull requests, so no filtering is needed.
- A repository with fewer than 100 open pull requests and 100 open issues costs two requests per poll, which keeps usage far below the 5000 points/hour rate limit.

---

## Pagination & Errors

`fetch_nodes` loops over pages until `hasNextPage` is false, following `endCursor`. Each request uses a 30-second timeout and an `Authorization: Bearer <token>` header set once on the shared `requests.Session`.

A failure is raised, not hidden:

- `response.raise_for_status()` for HTTP errors (bad token, network failures, rate limiting).
- `GitHubError` carrying the first message when the payload contains `errors` (for example, an unknown repository).

`fetch_all` turns these into a `RepoStatus` with `error` set; see [Architecture & Design](architecture.md#3-per-repository-failure-isolation).
