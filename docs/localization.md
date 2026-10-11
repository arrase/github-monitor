# Localization

The interface is written in English and translated with the standard library's `gettext`. Spanish (`es`) is included.

---

## Language Selection

`i18n.py` builds the translation once at import time:

```python
translation = gettext.translation(DOMAIN, localedir=LOCALE_DIR, fallback=True)
_ = translation.gettext
ngettext = translation.ngettext
```

`gettext` picks the language from `LANGUAGE`, `LC_ALL`, `LC_MESSAGES` and `LANG`, in that order. With `fallback=True`, a locale without a catalog simply shows the English source strings.

Try a language without changing your system locale:

```bash
LANGUAGE=es github-monitor
```

---

## What Is Translated

- Tray tooltip, menu entries and notifications, including plural forms (`ngettext`).
- Configuration error messages.

Data coming from GitHub (issue titles, repository names, API error messages) is always shown exactly as received.

Placeholders are named (`{repo}`, `{count}`, …) so translators can reorder them freely.

---

## Updating the Catalogs

Catalogs live in `src/github_monitor/locale/`. After changing user-facing strings (requires the `dev` extra):

```bash
.venv/bin/pybabel extract -F babel.cfg --no-location --project=github-monitor -o src/github_monitor/locale/github_monitor.pot src/
.venv/bin/pybabel update -i src/github_monitor/locale/github_monitor.pot -d src/github_monitor/locale -D github_monitor
# translate the new entries in src/github_monitor/locale/<lang>/LC_MESSAGES/github_monitor.po
.venv/bin/pybabel compile -d src/github_monitor/locale -D github_monitor --statistics
```

To add a language, replace `update` with `init -l <lang>`.

Compiled `.mo` files are committed and shipped as package data, so a plain `pip install` works without Babel.

---

## Catalog Tests

`tests/test_i18n.py` uses Babel to verify that:

- the Spanish catalog covers every message of the template, with no fuzzy entries;
- the compiled catalog switches strings to Spanish under `LANGUAGE=es`, which also catches a stale or missing `.mo` file.
