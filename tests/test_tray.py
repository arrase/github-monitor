from datetime import datetime

import pytest

from github_monitor.github import Item, RepoStatus
from github_monitor.tray import GREEN, ORANGE, RED, badge_text, menu_label, state_color, tooltip_text

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
    [(0, False, GREEN), (2, False, ORANGE), (0, True, RED), (2, True, RED)],
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
