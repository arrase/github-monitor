import sys

from PyQt6.QtWidgets import QApplication

from github_monitor.config import CONFIG_PATH, ConfigError, load_config
from github_monitor.tray import TrayIcon


def main() -> None:
    try:
        config = load_config(CONFIG_PATH)
    except ConfigError as exc:
        sys.exit(f"github-monitor: {exc}")

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    tray = TrayIcon(config)
    tray.show()
    tray.refresh()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
