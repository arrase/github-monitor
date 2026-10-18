from datetime import datetime

import pytest
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication

from github_monitor.config import Config
from github_monitor.github import Item, RepoStatus
from github_monitor.tray import (
    BADGE_HEIGHT,
    ICON_SIZE,
    ORANGE,
    RED,
    TrayIcon,
    badge_text,
    menu_label,
    render_icon,
    state_color,
    tooltip_text,
)

UPDATED_AT = datetime(2026, 10, 11, 15, 30)
CONFIG = Config(token="t", repositories=["org/app"], maintainers=frozenset(), poll_interval_minutes=5)


def item(number: int) -> Item:
    return Item(repo="org/app", number=number, title=f"t{number}", url=f"u{number}")


@pytest.mark.parametrize(
    ("total", "has_error", "expected"),
    [(0, False, ""), (5, False, "5"), (120, False, "99+"), (0, True, "!"), (3, True, "3")],
)
def test_badge_text(total, has_error, expected):
    assert badge_text(total, has_error) == expected


@pytest.mark.parametrize(
    ("total", "has_error", "expected"),
    [(0, False, ""), (2, False, ORANGE), (0, True, RED), (2, True, RED)],
)
def test_state_color(total, has_error, expected):
    assert state_color(total, has_error) == expected


def test_tooltip_lists_only_repos_needing_attention():
    statuses = [
        RepoStatus("org/app", pull_requests=[item(1), item(2)], issues=[item(3)]),
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
    assert menu_label(Item("o/r", 7, "Fix A & B", "u")) == "#7 Fix A && B"


@pytest.fixture(scope="module")
def qapp():
    return QApplication([])


# Inside the badge, left of its centred text.
BADGE_PROBE = (ICON_SIZE - BADGE_HEIGHT + 6, ICON_SIZE - BADGE_HEIGHT // 2)


@pytest.mark.parametrize(("text", "color"), [("5", ORANGE), ("!", RED)])
def test_render_icon_draws_badge(qapp, text, color):
    image = render_icon(text, color, loading=False).pixmap(ICON_SIZE, ICON_SIZE).toImage()
    assert image.pixelColor(*BADGE_PROBE) == QColor(color)


@pytest.mark.parametrize("loading", [True, False])
def test_render_icon_without_badge(qapp, loading):
    image = render_icon("", "", loading).pixmap(ICON_SIZE, ICON_SIZE).toImage()
    assert image.pixelColor(*BADGE_PROBE) not in (QColor(ORANGE), QColor(RED))


def test_notify_new_only_notifies_new_items_after_initial_poll(qapp, monkeypatch):
    tray = TrayIcon(CONFIG)
    messages = []
    monkeypatch.setattr(tray, "showMessage", lambda title, body: messages.append((title, body)))

    tray.notify_new([RepoStatus("org/app", pull_requests=[item(1)])])
    tray.notify_new([RepoStatus("org/app", pull_requests=[item(1), item(2)])])
    tray.notify_new([RepoStatus("org/app", pull_requests=[item(1), item(2)])])

    assert messages == [("1 new pending item on GitHub", "org/app #2 t2")]


def test_notify_new_ignores_failed_polls(qapp, monkeypatch):
    tray = TrayIcon(CONFIG)
    messages = []
    monkeypatch.setattr(tray, "showMessage", lambda title, body: messages.append((title, body)))

    tray.notify_new([RepoStatus("org/app", error="offline")])
    tray.notify_new([RepoStatus("org/app", pull_requests=[item(1)])])
    tray.notify_new([RepoStatus("org/app", error="offline")])
    tray.notify_new([RepoStatus("org/app", pull_requests=[item(1)])])

    assert messages == []


def test_build_menu_populates_pending_and_error_submenus(qapp):
    tray = TrayIcon(CONFIG)
    statuses = [
        RepoStatus("org/app", pull_requests=[item(1)], issues=[item(2)]),
        RepoStatus("org/quiet"),
        RepoStatus("org/broken", error="A & B"),
    ]

    tray.build_menu(statuses)

    submenus = {action.text(): action.menu() for action in tray.menu.actions() if action.menu()}
    assert list(submenus) == ["org/app (2)", "org/broken (0)"]
    assert [action.text() for action in submenus["org/app (2)"].actions()] == [
        "Pull requests",
        "#1 t1",
        "Issues",
        "#2 t2",
    ]
    [error_action] = submenus["org/broken (0)"].actions()
    assert error_action.text() == "A && B"
    assert not error_action.isEnabled()
