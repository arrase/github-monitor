# monitor-config Specification

## Purpose
Defines where the github-monitor configuration lives, which fields it contains and how it is validated when the application starts.

## Requirements

### Requirement: Configuration file location
The application SHALL read its configuration from the TOML file `~/.config/github-monitor/config.toml` at startup.

#### Scenario: File present
- **WHEN** the application starts and `~/.config/github-monitor/config.toml` exists
- **THEN** the application loads its configuration from that file

#### Scenario: File missing
- **WHEN** the application starts and the file does not exist
- **THEN** the application exits with an error message showing the expected path

### Requirement: Configuration fields
The configuration SHALL contain: `token` (GitHub token, string), `repositories` (list of `"owner/name"`), `maintainers` (list of GitHub logins whose reply marks an issue as answered) and `poll_interval_minutes` (positive integer).

#### Scenario: Complete configuration
- **WHEN** the file defines `token`, `repositories`, `maintainers` and `poll_interval_minutes`
- **THEN** the application uses those values to authenticate, choose which repositories to query, filter issues and schedule polling

#### Scenario: Missing required field
- **WHEN** any of the four fields is missing
- **THEN** the application exits with an error message naming the missing field

### Requirement: Repository format
Every entry in `repositories` SHALL have the form `owner/name`.

#### Scenario: Malformed entry
- **WHEN** an entry in `repositories` does not contain exactly one `/` separating two non-empty parts
- **THEN** the application exits with an error message showing the invalid entry

### Requirement: Case-insensitive login comparison
Logins in `maintainers` SHALL be compared with GitHub authors case-insensitively.

#### Scenario: Login with different casing
- **WHEN** `maintainers` contains `Arrase` and the GitHub author is `arrase`
- **THEN** the author is considered a maintainer
