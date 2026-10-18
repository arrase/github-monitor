import tomllib
from dataclasses import dataclass
from pathlib import Path

from github_monitor.i18n import _

CONFIG_PATH = Path.home() / ".config" / "github-monitor" / "config.toml"


class ConfigError(Exception):
    pass


@dataclass(frozen=True)
class Config:
    token: str
    repositories: list[str]
    maintainers: frozenset[str]
    poll_interval_minutes: int


def load_config(path: Path) -> Config:
    if not path.is_file():
        raise ConfigError(_("Configuration file not found: {path}").format(path=path))
    data = tomllib.loads(path.read_text())

    for field in Config.__dataclass_fields__:
        if field not in data:
            raise ConfigError(_("Missing required field '{field}' in {path}").format(field=field, path=path))

    for repo in data["repositories"]:
        parts = repo.split("/")
        if len(parts) != 2 or not all(parts):
            raise ConfigError(_("Invalid repository '{repo}', expected 'owner/name'").format(repo=repo))

    return Config(
        token=data["token"],
        repositories=data["repositories"],
        maintainers=frozenset(login.lower() for login in data["maintainers"]),
        poll_interval_minutes=data["poll_interval_minutes"],
    )
