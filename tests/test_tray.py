from datetime import datetime

import pytest
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication

from github_monitor.github import Item, RepoStatus
from github_monitor.tray import (
    BADGE_HEIGHT,
    ICON_SIZE,
    ORANGE,
    RED,
    badge_text,
    menu_label,
    render_icon,
    state_color,
    tooltip_text,
)

UPDATED_AT = datetime(2026, 10, 11, 15, 30)


def item(kind: str, number: int) -> Item:
    return Item(repo="org/app", kind=kind, number=number, title=f"t{number}", url=f"u{number}")


@pytest.mark.parametrize(
    ("total", "has_error", "expected"),
    [(0, False, ""), (5, False, "5"), (120, False, "99+"), (0, True, "!"), (3, True, "3")],
)
def test_badge_text(total, has_error, expected):
    assert badge_text(total, has_error) == expected


@pytest.mark.parametrize(
    ("total", "has_error", "expected"),
    [(0, False, None), (2, False, ORANGE), (0, True, RED), (2, True, RED)],
)
def test_state_color(total, has_error, expected):
    assert state_color(total, has_error) == expected


def test_tooltip_lists_only_repos_needing_attention():
    statuses = [
        RepoStatus("org/app", pull_requests=[item("pr", 1), item("pr", 2)], issues=[item("issue", 3)]),
        RepoStatus("org/quiet"),
        RepoStatus("org/missing", error="Not found"),
    ]

    text = tooltip_text(statuses, UPDATED_AT)

    assert "org/app: 2 pull requests, 1 issue" in text
    assert "org/missing: error: Not found" in text
    assert "org/quiet" not in text
    assert "15:30" in text


def test_tooltip_all_clear():
    text = tooltip_text([RepoStatus("org/quiet")], UPDATED_AT)

    assert "All clear" in text
    assert "15:30" in text


def test_menu_label_escapes_ampersand():
    assert menu_label(Item("o/r", "pr", 7, "Fix A & B", "u")) == "#7 Fix A && B"


@pytest.fixture(scope="module")
def qapp():
    return QApplication.instance() or QApplication([])


# Inside the badge, left of its centred text.
BADGE_PROBE = (ICON_SIZE - BADGE_HEIGHT + 6, ICON_SIZE - BADGE_HEIGHT // 2)


@pytest.mark.parametrize(("text", "color"), [("5", ORANGE), ("!", RED)])
def test_render_icon_draws_badge(qapp, text, color):
    image = render_icon(text, color, loading=False).pixmap(ICON_SIZE, ICON_SIZE).toImage()
    assert image.pixelColor(*BADGE_PROBE) == QColor(color)


@pytest.mark.parametrize("loading", [True, False])
def test_render_icon_without_badge(qapp, loading):
    image = render_icon("", None, loading).pixmap(ICON_SIZE, ICON_SIZE).toImage()
    assert image.pixelColor(*BADGE_PROBE) not in (QColor(ORANGE), QColor(RED))
