import os
import subprocess
import sys
from pathlib import Path

import pytest
from babel.messages.pofile import read_po

from github_monitor.i18n import DOMAIN, LOCALE_DIR

TEMPLATE = LOCALE_DIR / f"{DOMAIN}.pot"
PO_FILES = sorted(LOCALE_DIR.glob("*/LC_MESSAGES/github_monitor.po"))


@pytest.mark.parametrize("po_path", PO_FILES, ids=[p.parent.parent.name for p in PO_FILES])
def test_catalog_is_complete(po_path: Path) -> None:
    with TEMPLATE.open("rb") as template_file, po_path.open("rb") as catalog_file:
        template = read_po(template_file)
        catalog = read_po(catalog_file)

    for message in template:
        if not message.id:
            continue
        translated = catalog[message.id]
        assert translated is not None, f"Missing {message.id} in {po_path}"
        assert not translated.fuzzy, f"Fuzzy {message.id} in {po_path}"
        strings = translated.string if isinstance(translated.string, tuple) else (translated.string,)
        assert all(strings), f"Empty translation for {message.id} in {po_path}"


def run_in_language(language: str, code: str) -> list[str]:
    """Run `code` in a fresh interpreter, since the catalog is chosen at import time."""
    env = os.environ | {"LANGUAGE": language}
    result = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True, check=True)
    return result.stdout.splitlines()


@pytest.mark.parametrize(
    ("language", "expected"),
    [
        ("es", ["Salir", "1 nuevo elemento pendiente en GitHub", "3 nuevos elementos pendientes en GitHub"]),
        ("de", ["Beenden", "1 neues ausstehendes Element auf GitHub", "3 neue ausstehende Elemente auf GitHub"]),
        ("fr", ["Quitter", "1 nouvel élément en attente sur GitHub", "3 nouveaux éléments en attente sur GitHub"]),
        ("eo", ["Quit", "1 new pending item on GitHub", "3 new pending items on GitHub"]),
    ],
)
def test_language_follows_locale(language: str, expected: list[str]) -> None:
    code = (
        "from github_monitor.i18n import _\n"
        "from github_monitor.tray import notification_title\n"
        "print(_('Quit')); print(notification_title(1)); print(notification_title(3))"
    )
    assert run_in_language(language, code) == expected
