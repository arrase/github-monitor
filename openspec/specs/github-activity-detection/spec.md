# github-activity-detection Specification

## Purpose
Fetches the open pull requests and issues of the configured repositories from GitHub and decides which ones need the user's attention.

## Requirements

### Requirement: Authenticated access to public and private repositories
Every GitHub query SHALL be authenticated with the configured `token`, so that both public and private repositories the token can read are queried.

#### Scenario: Accessible private repository
- **WHEN** a configured repository is private and the token has read access to it
- **THEN** its open pull requests and issues are fetched exactly like those of a public repository

#### Scenario: Inaccessible repository
- **WHEN** a configured repository does not exist or the token has no access to it
- **THEN** that repository is marked as failed with the message returned by GitHub and the remaining repositories are still queried

### Requirement: Open pull requests need attention
Every open pull request of a configured repository SHALL be considered as needing attention.

#### Scenario: Repository with open pull requests
- **WHEN** a repository has open pull requests
- **THEN** each one is reported as pending with its number, title and URL

#### Scenario: Closed or merged pull request
- **WHEN** a pull request is closed or merged
- **THEN** it is not reported as pending

### Requirement: Open issues need attention based on the last responder
An open issue SHALL be considered pending only if the author of its last comment is not in `maintainers`. If it has no comments, the issue author is used. A deleted author (no login) counts as a non-maintainer.

#### Scenario: Last comment by a maintainer
- **WHEN** the last comment of an open issue was written by a user in `maintainers`
- **THEN** the issue is not reported as pending

#### Scenario: Last comment by an outsider
- **WHEN** the last comment of an open issue was written by a user not in `maintainers`
- **THEN** the issue is reported as pending with its number, title and URL

#### Scenario: Issue without comments opened by an outsider
- **WHEN** an open issue has no comments and its author is not in `maintainers`
- **THEN** the issue is reported as pending

#### Scenario: Issue without comments opened by a maintainer
- **WHEN** an open issue has no comments and its author is in `maintainers`
- **THEN** the issue is not reported as pending

### Requirement: Complete retrieval with pagination
Retrieval of open pull requests and issues SHALL walk through every page of GitHub results.

#### Scenario: More results than the page size
- **WHEN** a repository has more open pull requests or issues than the API page size
- **THEN** all of them are retrieved
