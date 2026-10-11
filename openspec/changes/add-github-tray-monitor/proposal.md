# Proposal

## Why

Following several GitHub repositories (public and private) means checking the web regularly to find out whether there are pull requests to review or issues waiting for an answer. A system tray icon that summarises that state at a glance, and ignores issues whose last reply already comes from the team, removes that manual work.

## What Changes

- New Python desktop application (`github-monitor`) living in the system tray.
- Reads its configuration from `~/.config/github-monitor/config.toml`: GitHub token, list of repositories, list of "maintainer" users and polling interval.
- Periodically queries the GitHub GraphQL API with the configured token (which gives access to private repositories).
- Considers as "needing attention":
  - Every open pull request.
  - Every open issue whose last comment (or its author, if there are no comments) does not belong to a user in the maintainers list.
- The icon shows the state: colour depending on whether there are pending items, errors or everything is clear, and a badge with the total number of pending items.
- The tooltip summarises pending items per repository and the context menu lists every pending PR/issue; clicking one opens it in the browser.
- Desktop notification when new pending items appear compared to the previous poll.
- "Refresh now" and "Quit" menu actions; left click refreshes.
- English is the base language; every user-facing string is translatable with gettext, the UI follows the system locale and a complete Spanish translation ships with the first version.

## Capabilities

### New Capabilities
- `monitor-config`: Format, location and validation of the configuration file.
- `github-activity-detection`: Fetching open PRs and issues of the configured repositories and the rules that decide what needs attention.
- `tray-indicator`: How the state is represented in the system tray icon (icon, badge, tooltip, menu, notifications and periodic refresh).
- `localization`: English source strings, language selection from the system locale and the shipped translations.

### Modified Capabilities

## Impact

- New (greenfield) project: Python package `github_monitor` with `pyproject.toml` and the `github-monitor` entry point.
- Dependencies: `PyQt6` (system tray, timer, notifications) and `requests` (HTTP to the GraphQL API). `tomllib` and `gettext` from the standard library. `Babel` as a development dependency to extract and compile translation catalogs.
- External system: GitHub GraphQL API (`https://api.github.com/graphql`); requires a token with read access to the repositories (`repo` scope for private ones).
