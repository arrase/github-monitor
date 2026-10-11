# github-monitor

System tray icon that monitors GitHub repositories (public and private) and tells you about open pull requests and issues waiting for a reply.

## Configuration

The application reads `~/.config/github-monitor/config.toml`. Start from the bundled example:

```sh
mkdir -p ~/.config/github-monitor
cp config.example.toml ~/.config/github-monitor/config.toml
chmod 600 ~/.config/github-monitor/config.toml
```

| Field | Description |
|---|---|
| `token` | GitHub token. Classic with the `repo` scope (required for private repositories) or fine-grained with read access to "Issues" and "Pull requests". |
| `repositories` | List of `owner/name` repositories. |
| `maintainers` | Logins whose reply marks an issue as answered (case-insensitive). |
| `poll_interval_minutes` | Minutes between checks. |

The file stores the token in plain text: keep its permissions at `600`. Changes require restarting the application.

## Installation and usage

```sh
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/github-monitor
```

Tests: `.venv/bin/pip install -e .[dev] && .venv/bin/pytest`.

## What needs attention

- Every open pull request.
- Every open issue whose last comment (or its author, if it has no comments) does not come from someone in `maintainers`.

## Reading the icon

| Icon | Meaning |
|---|---|
| Grey circle | First check in progress. |
| Green circle | All clear. |
| Orange circle with a number | Total pending pull requests and issues (`99+` above 99). |
| Red circle | Some repository failed in the last check; shows the pending count, or `!` if there is none. |

- **Tooltip**: per-repository summary (`org/app: 2 pull requests, 1 issue`) and time of the last check.
- **Menu** (right click): one submenu per repository with pending items or errors; clicking `#number title` opens it in the browser. Also "Refresh now" and "Quit".
- **Left click**: refresh immediately.
- **Notifications**: desktop notification when new pending items appear since the previous check.

## Translations

The interface is written in English and translated with gettext. The language follows the system locale (`LANGUAGE`, `LC_ALL`, `LC_MESSAGES`, `LANG`) and falls back to English. Available: Spanish (`es`).

Catalogs live in `src/github_monitor/locale/`. After changing user-facing strings (requires the `dev` extra):

```sh
.venv/bin/pybabel extract -F babel.cfg --no-location --project=github-monitor -o src/github_monitor/locale/github_monitor.pot src/
.venv/bin/pybabel update -i src/github_monitor/locale/github_monitor.pot -d src/github_monitor/locale -D github_monitor
# translate the new entries in src/github_monitor/locale/<lang>/LC_MESSAGES/github_monitor.po
.venv/bin/pybabel compile -d src/github_monitor/locale -D github_monitor --statistics
```

To add a language, replace `update` with `init -l <lang>`. Compiled `.mo` files are committed so a plain `pip install` works without Babel.

Try a language with `LANGUAGE=es .venv/bin/github-monitor`.
