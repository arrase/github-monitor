# Tasks

## 1. Logo asset

- [x] 1.1 Add `src/github_monitor/assets/github-mark.svg` (Octicons `mark-github-24.svg`) and `src/github_monitor/assets/LICENSE-octicons`, and include `assets/*` in the package data of `pyproject.toml`; verify both files are inside a wheel built with `.venv/bin/pip wheel --no-deps .`

## 2. Icon rendering (`tray-indicator`)

- [x] 2.1 Change `state_color(total, has_error)` to return `None` when nothing is pending and there is no error (orange with pending items, red on error) and update `tests/test_tray.py`; verify with `.venv/bin/pytest tests/test_tray.py`
- [x] 2.2 Replace `render_icon` with `render_icon(text, color, loading)`: theme-coloured logo via `QSvgRenderer` + `CompositionMode_SourceIn`, 0.4 opacity while loading, bottom-right rounded badge sized to the text when `color` is set; verify with an offscreen script that saves PNGs for loading, clear, `5`, `99+` and `!` and inspect them
- [x] 2.3 Add a test that renders the icon offscreen (`QT_QPA_PLATFORM=offscreen`) and checks that the badge corner pixel has the badge colour when a badge is requested and is not that colour when there is none; verify with `.venv/bin/pytest tests/test_tray.py`
- [x] 2.4 In `TrayIcon`, start with `render_icon("", None, loading=True)`, remember the last rendered text/colour, and re-render on `styleHints().colorSchemeChanged`; verify the full suite with `.venv/bin/pytest`

## 3. Documentation

- [x] 3.1 Update the "Reading the icon" table in `README.md` (semi-transparent logo, logo without badge, orange badge, red badge) and credit the Octicons logo and GitHub logo guidelines; verify the README matches the rendered PNGs
