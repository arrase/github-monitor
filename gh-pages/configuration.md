# Configuration

GitHub Monitor reads a single TOML file at `~/.config/github-monitor/config.toml`. All four fields are required; the application refuses to start if the file is missing or incomplete.

---

## Creating the File

Start from the bundled example and restrict its permissions, since the token is stored in plain text:

```bash
mkdir -p ~/.config/github-monitor
cp config.example.toml ~/.config/github-monitor/config.toml
chmod 600 ~/.config/github-monitor/config.toml
```

!!! note
    If you installed with `pipx` or `uv`, `config.example.toml` is not on disk. Copy it from the [repository](https://github.com/arrase/github-monitor/blob/main/config.example.toml) or use the example below.

---

## Example

```toml
# GitHub token with read access to the repositories (classic: "repo" scope;
# fine-grained: read-only "Issues" and "Pull requests").
token = "ghp_your_token_here"

# Minutes between checks.
poll_interval_minutes = 5

# Logins whose reply marks an issue as answered (case-insensitive).
maintainers = ["arrase"]

# Repositories to monitor, as "owner/name". Public and private are supported.
repositories = [
    "arrase/github-monitor",
]
```

---

## Field Reference

| Field | Type | Description |
| :--- | :--- | :--- |
| `token` | string | GitHub token. Classic with the `repo` scope (required for private repositories) or fine-grained with read access to "Issues" and "Pull requests". |
| `repositories` | list of strings | Repositories to monitor, each as `owner/name`. |
| `maintainers` | list of strings | Logins whose reply marks an issue as answered (case-insensitive). See [Attention Rules](detection.md). |
| `poll_interval_minutes` | integer | Minutes between checks. |

---

## Validation

Configuration errors are printed to the terminal and the process exits with a non-zero status:

| Problem | Message |
| :--- | :--- |
| File does not exist | `Configuration file not found: <path>` |
| A required field is absent | `Missing required field '<field>' in <path>` |
| A repository is not `owner/name` | `Invalid repository '<repo>', expected 'owner/name'` |

Messages are translated according to the system locale (see [Localization](localization.md)).

---

## Applying Changes

The file is read once at startup. After editing it, quit the application from the tray menu and start it again.

!!! warning
    Keep the file at permissions `600`. A read-only token (fine-grained, or classic with `repo`) is enough, because GitHub Monitor never writes anything to GitHub.
