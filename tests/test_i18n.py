import os
import subprocess
import sys

import pytest
from babel.messages.pofile import read_po

from github_monitor.i18n import DOMAIN, LOCALE_DIR

TEMPLATE = LOCALE_DIR / f"{DOMAIN}.pot"
SPANISH = LOCALE_DIR / "es" / "LC_MESSAGES" / f"{DOMAIN}.po"


def run_in_language(language: str, code: str) -> list[str]:
    """Run `code` in a fresh interpreter, since the catalog is chosen at import time."""
    env = os.environ | {"LANGUAGE": language}
    result = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True, check=True)
    return result.stdout.splitlines()


def test_spanish_catalog_is_complete():
    with TEMPLATE.open("rb") as template_file, SPANISH.open("rb") as spanish_file:
        template = read_po(template_file)
        spanish = read_po(spanish_file)

    for message in template:
        if not message.id:
            continue
        translated = spanish[message.id]
        assert translated is not None, message.id
        assert not translated.fuzzy, message.id
        strings = translated.string if isinstance(translated.string, tuple) else (translated.string,)
        assert all(strings), message.id


@pytest.mark.parametrize(
    ("language", "expected"),
    [
        ("es", ["Salir", "1 nuevo elemento pendiente en GitHub", "3 nuevos elementos pendientes en GitHub"]),
        ("de", ["Quit", "1 new pending item on GitHub", "3 new pending items on GitHub"]),
    ],
)
def test_language_follows_locale(language, expected):
    code = (
        "from github_monitor.i18n import _\n"
        "from github_monitor.tray import notification_title\n"
        "print(_('Quit')); print(notification_title(1)); print(notification_title(3))"
    )
    assert run_in_language(language, code) == expected
