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

## Installation

Install it straight from GitHub with [pipx](https://pipx.pypa.io) or [uv](https://docs.astral.sh/uv/); either one puts `github-monitor` in `~/.local/bin`:

```sh
pipx install git+https://github.com/arrase/github-monitor.git
# or
uv tool install git+https://github.com/arrase/github-monitor.git
```

Upgrade with `pipx upgrade github-monitor` or `uv tool upgrade github-monitor`, and remove with `pipx uninstall github-monitor` or `uv tool uninstall github-monitor`.

Then create the [configuration file](#configuration) and run `github-monitor`.

## Start on login

Desktop environments that follow the XDG autostart specification (KDE Plasma, GNOME, Xfce…) start every `.desktop` file found in `~/.config/autostart` when you log in. Create one for github-monitor (it records the absolute path of the installed command, because `~/.local/bin` is not always in `PATH` that early in the session):

```sh
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/github-monitor.desktop <<EOF
[Desktop Entry]
Type=Application
Name=GitHub Monitor
Comment=Monitor GitHub pull requests and issues from the system tray
Exec=$(command -v github-monitor)
Terminal=false
EOF
```

It takes effect at your next login. To disable it, delete `~/.config/autostart/github-monitor.desktop` (on KDE Plasma you can also manage it in System Settings → Autostart).

## Development

```sh
git clone https://github.com/arrase/github-monitor.git
cd github-monitor
python3 -m venv .venv
.venv/bin/pip install -e .[dev]
.venv/bin/github-monitor
```

Tests: `.venv/bin/pytest`.

## What needs attention

- Every open pull request.
- Every open issue whose last comment (or its author, if it has no comments) does not come from someone in `maintainers`.

## Reading the icon

The icon is the GitHub logo in your theme's text colour (white on dark panels, black on light ones); the state is shown by a badge in its bottom-right corner.

| Icon | Meaning |
|---|---|
| Semi-transparent logo | First check in progress. |
| Logo without badge | All clear. |
| Orange badge with a number | Total pending pull requests and issues (`99+` above 99). |
| Red badge | Some repository failed in the last check; shows the pending count, or `!` if there is none. |

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

## License

[MIT](LICENSE)

The tray icon uses the `mark-github` icon from [Octicons](https://github.com/primer/octicons) (MIT, see `src/github_monitor/assets/LICENSE-octicons`). The GitHub logo is a trademark of GitHub, Inc. and is used unmodified, as a single-colour mark in the theme's light or dark text colour, following the [GitHub logo guidelines](https://github.com/logos).
