# Installation & Setup

This guide covers the prerequisites, installing GitHub Monitor, and starting it automatically when you log in.

---

## System Requirements

| Component | Requirement | Notes |
| :--- | :--- | :--- |
| **Operating System** | Linux | Target desktops are KDE Plasma and others that support StatusNotifierItem or a system tray. |
| **Python** | Python 3.12+ | Required for `tomllib` and modern typing syntax. |
| **GitHub token** | Read access to the repositories | See [Configuration](configuration.md). |
| **Notifications** | Desktop notification service | Used to announce new pending items. |

Desktops without any system tray are out of scope.

---

## Installation Methods

### Method 1: Using `uv`

[`uv`](https://github.com/astral-sh/uv) is a fast Python package installer.

```bash
uv tool install git+https://github.com/arrase/github-monitor.git
```

Upgrade or remove:

```bash
uv tool upgrade github-monitor
uv tool uninstall github-monitor
```

### Method 2: Using `pipx`

[`pipx`](https://pipx.pypa.io/) installs Python CLI tools into isolated virtual environments:

```bash
pipx install git+https://github.com/arrase/github-monitor.git
```

Upgrade or remove:

```bash
pipx upgrade github-monitor
pipx uninstall github-monitor
```

Both methods put the `github-monitor` command in `~/.local/bin`.

### Method 3: Local Development Installation

See [Development](development.md).

---

## First Run

1. Create the [configuration file](configuration.md).
2. Run:

    ```bash
    github-monitor
    ```

3. The tray icon appears semi-transparent while the first check runs, then shows the current state.

---

## Start on Login

Desktop environments that follow the XDG autostart specification (KDE Plasma, GNOME, Xfce…) start every `.desktop` file found in `~/.config/autostart` when you log in.

Create one for GitHub Monitor. It records the absolute path of the installed command, because `~/.local/bin` is not always in `PATH` that early in the session:

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/github-monitor.desktop <<EOF
[Desktop Entry]
Type=Application
Name=GitHub Monitor
Comment=Monitor GitHub pull requests and issues from the system tray
Exec=$(command -v github-monitor)
Terminal=false
EOF
```

It takes effect at your next login. To disable it, delete `~/.config/autostart/github-monitor.desktop` (on KDE Plasma you can also manage it in **System Settings → Autostart**).
