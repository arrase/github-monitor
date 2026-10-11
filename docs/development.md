# Development

---

## Local Setup

```bash
git clone https://github.com/arrase/github-monitor.git
cd github-monitor
python3 -m venv .venv
.venv/bin/pip install -e .[dev]
.venv/bin/github-monitor
```

The `dev` extra installs `pytest` and `Babel`.

---

## Running the Tests

```bash
.venv/bin/pytest
```

`tests/conftest.py` pins the session to English (`LANGUAGE=en`) before any module imports `github_monitor.i18n`, and sets `QT_QPA_PLATFORM=offscreen` so Qt pixmaps render without a display server.

| Test module | Covers |
| :--- | :--- |
| `test_github.py` | Attention rule, pagination, per-repository error isolation. |
| `test_config.py` | Required fields, repository format validation. |
| `test_tray.py` | Badge text and colour, tooltip, menu label escaping, icon rendering. |
| `test_i18n.py` | Spanish catalog completeness and activation. |

---

## Code Principles

- Keep it simple: no speculative fallbacks or dead defensive code.
- Fail fast on invalid configuration and report actionable errors.
- All state changes happen on the Qt main thread; only the network access runs on a background thread and reports back through a signal.
- Pure functions (`needs_attention`, `badge_text`, `state_color`, `tooltip_text`) keep the logic testable without a display.

---

## Building These Docs

The documentation is built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/):

```bash
pip install mkdocs-material
mkdocs serve
```

Pushing to `main` publishes the site to GitHub Pages through `.github/workflows/deploy.yml`.

---

## License

[MIT](https://github.com/arrase/github-monitor/blob/main/LICENSE). The tray icon uses the `mark-github` icon from [Octicons](https://github.com/primer/octicons) (MIT). The GitHub logo is a trademark of GitHub, Inc. and is used unmodified, as a single-colour mark in the theme's light or dark text colour, following the [GitHub logo guidelines](https://github.com/logos).
