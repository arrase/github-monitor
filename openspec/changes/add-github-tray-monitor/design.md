# Design

## Context

Greenfield project. Target environment: Linux desktop (KDE Plasma on Wayland, with StatusNotifierItem support), Python 3.12+ (3.14 available). See proposal.md for motivation and specs/ for requirements.

## Goals / Non-Goals

**Goals:**
- Minimal single-process application with no persistent state on disk.
- Filtering and formatting logic separated from Qt so it can be tested with pytest without a UI.
- English source strings with gettext-based translations.

**Non-Goals:**
- GitHub Enterprise, OAuth device flow or reading the token from `gh`.
- Hot reload of the configuration (requires a restart).
- Configuration or preferences windows.
- Special handling of draft PRs, reviews or bots.
- Choosing the UI language from the configuration file.

## Decisions

### Package layout
```
pyproject.toml
babel.cfg
src/github_monitor/
  i18n.py     # gettext setup: exposes _ and ngettext
  config.py   # Config (dataclass) + load_config(path) -> Config
  github.py   # Item, RepoStatus (dataclasses) + fetch_repo_status(...) + needs_attention(...)
  tray.py     # TrayIcon: icon rendering, tooltip, menu, polling and notifications
  __main__.py # main(): loads config, creates QApplication and TrayIcon
  locale/
    github_monitor.pot
    es/LC_MESSAGES/github_monitor.po
    es/LC_MESSAGES/github_monitor.mo
tests/
  test_config.py
  test_github.py
  test_tray.py
  test_i18n.py
```
Entry point `github-monitor = "github_monitor.__main__:main"` in `pyproject.toml`.

### TOML configuration with `tomllib`
`tomllib` is in the standard library and TOML is human-friendly. Alternatives: YAML (extra dependency), JSON (no comments). Example:
```toml
token = "ghp_..."
poll_interval_minutes = 5
maintainers = ["arrase"]
repositories = ["arrase/github-monitor", "org/private-repo"]
```
`load_config` validates fields and repository format and raises `ConfigError` with a clear message; `main` prints it to stderr and exits with code 1. `maintainers` is normalised to lowercase in a `frozenset`.

### GitHub GraphQL API with `requests`
GraphQL returns, in a single request per page, the last comment of every issue (`comments(last: 1)`), which REST can only do with one request per issue. GraphQL `issues` also excludes PRs, so no filtering is needed. Each repository is queried with two paginated connections (`pullRequests(states: OPEN)` and `issues(states: OPEN)`, `first: 100`, `after` cursor). Alternatives: PyGithub (heavy dependency, REST, N+1 requests), `gh api` via subprocess (requires `gh`).

Errors: `raise_for_status()` for HTTP and an exception when the response contains `errors`. `fetch_all(config, session)` wraps each repository in `try/except` and returns `RepoStatus(error=str(exc))`, fulfilling the per-repository failure isolation requirement. The session is a parameter so tests can inject a fake one.

### Attention rule as a pure function
`needs_attention(last_author: str | None, maintainers: frozenset[str]) -> bool`, where `last_author` is the login of the last comment or, if there is none, of the issue author; `None` represents a deleted user. Tested directly with pytest.

### UI with PyQt6 `QSystemTrayIcon`
PyQt6 is already available and `QSystemTrayIcon` uses StatusNotifierItem on KDE, offering a context menu and `showMessage` for notifications without extra dependencies. Alternatives: `pystray` (no native notifications, limited menus), AppIndicator/GTK (worse KDE integration).

The icon is drawn at runtime with `QPainter` on a 64×64 `QPixmap`: a filled circle in the state colour and the badge text centred in bold white. The number is part of the icon itself, so it is visible in any panel without relying on desktop badge support. Pure functions `badge_text(total, has_error)` and `state_color(total, has_error)` keep it testable.

The menu is published through DBusMenu and shown by the shell on right click. Left click (`activated` with `Trigger`) starts an immediate poll: on Wayland a `QMenu.popup()` without a focused parent window fails ("Failed to create grabbing popup") and Qt sets `ItemIsMenu=false`, so left click cannot be delegated to the shell. URLs open with `QDesktopServices.openUrl`.

### Background polling
A `QTimer` triggers `refresh()`. `refresh()` returns early while a poll is running; otherwise it starts a `threading.Thread` that runs `fetch_all` and emits a `pyqtSignal(list)` with the `RepoStatus` list. Being a cross-thread Qt signal, the slot runs in the UI thread, where icon, tooltip and menu are updated. Alternative: `QThread`/`QThreadPool` (more code, no benefit here).

### New pending item detection
The set of pending URLs from the previous poll is kept (`None` before the first one). New items are the set difference; if it is not empty and this is not the first poll, `showMessage` is called.

### Internationalization with stdlib `gettext` and Babel tooling
`i18n.py` builds `gettext.translation("github_monitor", localedir=<package>/locale, fallback=True)` once at import and exposes `_ = translation.gettext` and `ngettext = translation.ngettext`. `gettext` reads `LANGUAGE`, `LC_ALL`, `LC_MESSAGES` and `LANG` by itself, and `fallback=True` returns the English source strings when no catalog matches, which is exactly the required behaviour. Strings are formatted with named `str.format` placeholders so translators can reorder them.

Alternative considered: Qt's `tr()` with `.ts`/`.qm` files. Rejected because `lrelease` is not shipped with the PyQt6 wheels, and the configuration errors are printed before any `QApplication` exists.

Catalog workflow, driven by `Babel` (dev dependency) and `babel.cfg`:
1. `pybabel extract -F babel.cfg -o src/github_monitor/locale/github_monitor.pot src/`
2. `pybabel update` (or `init` for a new language) on `src/github_monitor/locale`
3. Translate the `.po` file (delegated to a flash-model subagent, then reviewed)
4. `pybabel compile -d src/github_monitor/locale -D github_monitor`

Compiled `.mo` files are committed and shipped as package data, so a plain `pip install` works without Babel. `tests/test_i18n.py` uses Babel to check that the Spanish catalog covers every template message without fuzzy entries, and that the compiled catalog switches strings to Spanish under `LANGUAGE=es`.

## Risks / Trade-offs

- [Plain-text token in the configuration file] → The README states that the file must have `600` permissions and that a read-only token is enough (fine-grained with read access to "Issues" and "Pull requests", or classic with `repo`).
- [GraphQL API rate limit (5000 points/hour)] → With a polling interval of minutes and few pages per repository the usage is very low; the interval is configurable.
- [Desktops without a system tray] → Out of scope; the target is KDE / StatusNotifierItem desktops.
- [Bot comments count as outsiders] → Accepted; bot logins can be added to `maintainers`.
- [Committed `.mo` files can drift from `.po` files] → The README documents the compile step and the i18n test compiles nothing itself but fails if Spanish strings are not active, which catches a stale or missing `.mo`.
- [Machine translations can be inaccurate] → The main agent reviews the flash subagent output before compiling; the catalog is small.
