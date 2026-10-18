import threading
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import QRectF, Qt, QTimer, QUrl, pyqtSignal
from PyQt6.QtGui import QColor, QDesktopServices, QFont, QGuiApplication, QIcon, QPainter, QPalette, QPixmap
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from github_monitor.config import Config
from github_monitor.github import Item, RepoStatus, create_session, fetch_all
from github_monitor.i18n import _, ngettext

ORANGE = "#ef6c00"
RED = "#c62828"
ICON_SIZE = 64
BADGE_HEIGHT = 34
BADGE_PADDING = 12
LOADING_OPACITY = 0.4
LOGO_PATH = Path(__file__).parent / "assets" / "github-mark.svg"


def badge_text(total: int, has_error: bool) -> str:
    if total > 99:
        return "99+"
    if total:
        return str(total)
    return "!" if has_error else ""


def state_color(total: int, has_error: bool) -> str:
    """Badge colour, or empty string when there is nothing to report."""
    if has_error:
        return RED
    return ORANGE if total else ""


def tooltip_text(statuses: list[RepoStatus], updated_at: datetime) -> str:
    lines = []
    for status in statuses:
        if status.error:
            lines.append(_("{repo}: error: {error}").format(repo=status.repo, error=status.error))
        elif status.pending:
            pull_requests = len(status.pull_requests)
            issues = len(status.issues)
            lines.append(_("{repo}: {pull_requests}, {issues}").format(
                repo=status.repo,
                pull_requests=ngettext("{count} pull request", "{count} pull requests", pull_requests).format(count=pull_requests),
                issues=ngettext("{count} issue", "{count} issues", issues).format(count=issues),
            ))
    summary = "\n".join(lines) if lines else _("All clear")
    return summary + "\n" + _("Last update: {time}").format(time=f"{updated_at:%H:%M}")


def notification_title(count: int) -> str:
    return ngettext("{count} new pending item on GitHub", "{count} new pending items on GitHub", count).format(count=count)


def draw_badge(painter: QPainter, text: str, color: str):
    font = QFont()
    font.setBold(True)
    font.setPixelSize(26)
    painter.setFont(font)
    width = max(BADGE_HEIGHT, painter.fontMetrics().horizontalAdvance(text) + BADGE_PADDING)
    rect = QRectF(ICON_SIZE - width, ICON_SIZE - BADGE_HEIGHT, width, BADGE_HEIGHT)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor(color))
    painter.drawRoundedRect(rect, BADGE_HEIGHT / 2, BADGE_HEIGHT / 2)
    painter.setPen(QColor("white"))
    painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)


def render_icon(text: str, color: str, loading: bool) -> QIcon:
    pixmap = QPixmap(ICON_SIZE, ICON_SIZE)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    QSvgRenderer(str(LOGO_PATH)).render(painter, QRectF(0, 0, ICON_SIZE, ICON_SIZE))
    # SourceIn keeps the logo's shape and repaints it in the theme text colour.
    logo_color = QApplication.palette().color(QPalette.ColorRole.WindowText)
    if loading:
        logo_color.setAlphaF(LOADING_OPACITY)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), logo_color)
    if color:
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        draw_badge(painter, text, color)
    painter.end()
    return QIcon(pixmap)


def escape_ampersand(text: str) -> str:
    # A single "&" marks a keyboard mnemonic in Qt menus.
    return text.replace("&", "&&")


def menu_label(item: Item) -> str:
    return escape_ampersand(f"#{item.number} {item.title}")


class TrayIcon(QSystemTrayIcon):
    results_ready = pyqtSignal(list)

    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self.session = create_session(config.token)
        self.polling = False
        self.previous_urls: dict[str, set[str]] = {}
        self.loading = True
        self.badge_text = ""
        self.badge_color = ""
        self.update_icon()
        self.setToolTip(_("Checking GitHub…"))
        self.build_menu([])
        self.results_ready.connect(self.show_results)
        self.activated.connect(self.on_activated)
        QGuiApplication.styleHints().colorSchemeChanged.connect(self.update_icon)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(config.poll_interval_minutes * 60_000)

    def update_icon(self):
        self.setIcon(render_icon(self.badge_text, self.badge_color, self.loading))

    def refresh(self):
        if self.polling:
            return
        self.polling = True
        threading.Thread(target=self.poll, daemon=True).start()

    def poll(self):
        self.results_ready.emit(fetch_all(self.config, self.session))

    def show_results(self, statuses: list[RepoStatus]):
        self.polling = False
        total = sum(len(status.pending) for status in statuses)
        has_error = any(status.error for status in statuses)
        self.loading = False
        self.badge_text = badge_text(total, has_error)
        self.badge_color = state_color(total, has_error)
        self.update_icon()
        self.setToolTip(tooltip_text(statuses, datetime.now()))
        self.build_menu(statuses)
        self.notify_new(statuses)

    def build_menu(self, statuses: list[RepoStatus]):
        self.menu = QMenu()
        for status in statuses:
            if status.pending or status.error:
                self.add_repo_menu(status)
        if not self.menu.isEmpty():
            self.menu.addSeparator()
        self.menu.addAction(_("Refresh now"), self.refresh)
        self.menu.addAction(_("Quit"), QApplication.quit)
        self.setContextMenu(self.menu)

    def add_repo_menu(self, status: RepoStatus):
        submenu = self.menu.addMenu(f"{status.repo} ({len(status.pending)})")
        if status.error:
            submenu.addAction(escape_ampersand(status.error)).setEnabled(False)
        for title, items in ((_("Pull requests"), status.pull_requests), (_("Issues"), status.issues)):
            if items:
                submenu.addSection(title)
            for item in items:
                submenu.addAction(menu_label(item), lambda url=item.url: QDesktopServices.openUrl(QUrl(url)))

    def notify_new(self, statuses: list[RepoStatus]):
        new_items = []
        for status in statuses:
            if status.error:
                continue
            if status.repo in self.previous_urls:
                new_items.extend(item for item in status.pending if item.url not in self.previous_urls[status.repo])
            self.previous_urls[status.repo] = {item.url for item in status.pending}
        if new_items:
            body = "\n".join(f"{item.repo} #{item.number} {item.title}" for item in new_items)
            self.showMessage(notification_title(len(new_items)), body)

    def on_activated(self, reason: QSystemTrayIcon.ActivationReason):
        # Wayland refuses QMenu popups without a focused parent window, so the
        # menu is left to the shell (right click) and left click refreshes.
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.refresh()
