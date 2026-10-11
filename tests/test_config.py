from pathlib import Path

import pytest

from github_monitor.config import ConfigError, load_config

VALID = """
token = "secret"
poll_interval_minutes = 5
maintainers = ["Arrase", "bob"]
repositories = ["arrase/github-monitor", "org/private"]
"""


def write(tmp_path: Path, content: str) -> Path:
    path = tmp_path / "config.toml"
    path.write_text(content)
    return path


def test_valid_config(tmp_path):
    config = load_config(write(tmp_path, VALID))
    assert config.token == "secret"
    assert config.poll_interval_minutes == 5
    assert config.repositories == ["arrase/github-monitor", "org/private"]


def test_maintainers_are_case_insensitive(tmp_path):
    config = load_config(write(tmp_path, VALID))
    assert config.maintainers == frozenset({"arrase", "bob"})


def test_missing_file(tmp_path):
    path = tmp_path / "missing.toml"
    with pytest.raises(ConfigError, match=str(path)):
        load_config(path)


@pytest.mark.parametrize("field", ["token", "repositories", "maintainers", "poll_interval_minutes"])
def test_missing_field(tmp_path, field):
    content = "\n".join(line for line in VALID.splitlines() if not line.startswith(field))
    with pytest.raises(ConfigError, match=field):
        load_config(write(tmp_path, content))


@pytest.mark.parametrize("repo", ["noslash", "/name", "owner/", "a/b/c"])
def test_invalid_repository(tmp_path, repo):
    content = VALID.replace('"org/private"', f'"{repo}"')
    with pytest.raises(ConfigError, match=repo):
        load_config(write(tmp_path, content))
