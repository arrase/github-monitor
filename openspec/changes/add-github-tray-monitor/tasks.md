# Tasks

## 1. Project structure

- [x] 1.1 Create `pyproject.toml` (dependencies `PyQt6`, `requests`; `dev` extra with `pytest`; `github-monitor` script), the `src/github_monitor/` package and `tests/`; verify with `python3 -m venv .venv && .venv/bin/pip install -e .[dev]` without errors
- [x] 1.2 Add `.gitignore` (`.venv/`, `__pycache__/`, `*.egg-info/`) and verify that `git status` does not list those files

## 2. Configuration (`monitor-config`)

- [x] 2.1 Implement `Config` and `load_config(path)` in `config.py` with `tomllib`, validating required fields and the `owner/name` format and normalising `maintainers` to lowercase; raise `ConfigError` with a message naming the field or invalid entry
- [x] 2.2 Tests in `tests/test_config.py`: valid configuration, missing file, missing field, malformed repository and mixed-case logins; verify with `.venv/bin/pytest tests/test_config.py`
- [x] 2.3 Add `config.example.toml` and a configuration section in `README.md` (path, fields, `600` permissions, token scopes); verify the example loads with `load_config`

## 3. GitHub detection (`github-activity-detection`)

- [x] 3.1 Implement in `github.py` the `Item` (repo, kind, number, title, url) and `RepoStatus` (repo, pull_requests, issues, error) dataclasses and the pure function `needs_attention(last_author, maintainers)`
- [x] 3.2 Implement the paginated GraphQL query (`pullRequests` and `issues` in `OPEN` state, `comments(last: 1)`), `fetch_repo_status(session, repo, maintainers)` and `fetch_all(config, session)` isolating errors per repository
- [x] 3.3 Tests in `tests/test_github.py`: `needs_attention` (maintainer, outsider, no comments, deleted author, casing), pagination and per-repository errors using a fake session with simulated GraphQL responses; verify with `.venv/bin/pytest tests/test_github.py`

## 4. Tray icon (`tray-indicator`)

- [x] 4.1 Implement in `tray.py` the pure functions `badge_text(total, has_error)`, `state_color(total, has_error)` and `tooltip_text(statuses, updated_at)`, and `render_icon(color, text) -> QIcon` with `QPainter`
- [x] 4.2 Tests in `tests/test_tray.py` for `badge_text` (0, 5, 120, error without pending items), `state_color` (clear, pending, error) and `tooltip_text`; verify with `.venv/bin/pytest tests/test_tray.py`
- [x] 4.3 Implement `TrayIcon` (`QSystemTrayIcon`): menu with one submenu per repository, entries that open the URL, error as a disabled entry, "Refresh now" and "Quit"; left click triggers "Refresh now"
- [x] 4.4 Implement polling: `QTimer` with `poll_interval_minutes`, initial poll, background thread with a results signal and no concurrent polls; `showMessage` notification with new pending items except on the first poll
- [x] 4.5 Implement `main()` in `__main__.py` (loads `~/.config/github-monitor/config.toml`, prints to stderr and exits 1 on `ConfigError`, `setQuitOnLastWindowClosed(False)`) and document usage and colour/badge meaning in `README.md`

## 5. English base and localization (`localization`)

- [x] 5.1 Add `Babel` to the `dev` extra, `babel.cfg`, package data for `locale/**/*.mo` in `pyproject.toml`, and `i18n.py` exposing `_` and `ngettext` over `gettext.translation(..., fallback=True)`; verify `.venv/bin/pip install -e .[dev]` succeeds and `from github_monitor.i18n import _, ngettext` works
- [x] 5.2 Rewrite every user-facing string in `config.py`, `tray.py` and `__main__.py` in English, wrapped in `_()` / `ngettext()` with named placeholders (notification title and tooltip counts use plurals); update tests to the English strings and verify with `.venv/bin/pytest`
- [x] 5.3 Extract `github_monitor.pot` and initialise the `es` catalog with `pybabel`; verify the `.pot` contains every wrapped string
- [x] 5.4 Delegate the Spanish translation of `es/LC_MESSAGES/github_monitor.po` to a flash-model subagent, review the result, and compile it with `pybabel compile`; verify `LANGUAGE=es` shows Spanish strings and `LANGUAGE=de` shows English ones
- [x] 5.5 Add `tests/test_i18n.py`: Spanish catalog covers every template message with no fuzzy or empty entries, `LANGUAGE=es` yields Spanish and an unsupported locale yields English, singular/plural notification titles; verify with `.venv/bin/pytest tests/test_i18n.py`
- [x] 5.6 Rewrite `README.md` and `config.example.toml` comments in English and add a "Translations" section documenting the extract/update/translate/compile workflow; verify the documented commands run as written

## 6. Integration verification

- [x] 6.1 Run the full `.venv/bin/pytest` suite and verify every test passes
- [ ] 6.2 Start `github-monitor` with a real configuration including a public, a private and a non-existent repository, under both `LANG=es_ES.UTF-8` and `LANG=en_US.UTF-8`; verify the red icon with a number, translated tooltip and menu, submenus, opening a URL in the browser, left-click refresh and the notification when a new issue is opened
