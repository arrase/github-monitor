# tray-indicator Specification

## Purpose
Shows the state of the monitored repositories in a system tray icon and lets the user open every pending item in the browser.

## Requirements

### Requirement: Icon visual state
The icon SHALL be a circle whose colour reflects the global state: grey while there is no data yet, green with nothing pending, orange with pending items and red if any repository failed in the last poll.

#### Scenario: Startup before the first poll
- **WHEN** the application has just started and the first poll has not finished
- **THEN** the icon is grey

#### Scenario: All clear
- **WHEN** the last poll finished without errors and without pending items
- **THEN** the icon is green and shows no number

#### Scenario: Pending items
- **WHEN** the last poll finished without errors and with pending items
- **THEN** the icon is orange

#### Scenario: Failed repository
- **WHEN** at least one repository failed in the last poll
- **THEN** the icon is red

### Requirement: Pending count badge
The icon SHALL show inside it the total number of pending items (PRs plus issues) across all repositories, or `99+` if it exceeds 99. If there is an error and nothing pending, it SHALL show `!`.

#### Scenario: Several pending items
- **WHEN** there are 2 pending pull requests and 3 pending issues in total
- **THEN** the icon shows `5`

#### Scenario: More than 99 pending items
- **WHEN** the total of pending items is 120
- **THEN** the icon shows `99+`

#### Scenario: Error without pending items
- **WHEN** some repository failed and nothing is pending
- **THEN** the icon shows `!`

### Requirement: Summary tooltip
The tooltip SHALL list, for every repository with pending items or an error, its number of pending pull requests and issues or the error, together with the time of the last poll. With nothing pending and no errors, it SHALL state that everything is clear.

#### Scenario: Summary with pending items
- **WHEN** `org/app` has 2 pending PRs and 1 pending issue and the other repositories have nothing
- **THEN** the tooltip contains a line for `org/app` with 2 PRs and 1 issue and does not mention the other repositories

#### Scenario: Nothing pending
- **WHEN** no repository has pending items or errors
- **THEN** the tooltip states that everything is clear and shows the time of the last poll

### Requirement: Menu with pending items
The icon menu SHALL contain one submenu per repository with pending items or an error, titled `owner/name (N)`, listing its pending PRs and issues as `#number title`, followed by the "Refresh now" and "Quit" actions. The menu SHALL open on right click and left click SHALL trigger "Refresh now".

#### Scenario: Open a pending item
- **WHEN** the user clicks a `#number title` menu entry
- **THEN** its GitHub URL opens in the default browser

#### Scenario: Failed repository
- **WHEN** a repository failed in the last poll
- **THEN** its submenu shows the error message as a non-selectable entry

#### Scenario: Left click
- **WHEN** the user left-clicks the icon
- **THEN** an immediate poll starts, as with "Refresh now"

#### Scenario: Quit
- **WHEN** the user clicks "Quit"
- **THEN** the application exits

### Requirement: Periodic polling without blocking the UI
The application SHALL poll every repository at startup and then every `poll_interval_minutes`, outside the UI thread. "Refresh now" SHALL start an immediate poll unless one is already running.

#### Scenario: Scheduled poll
- **WHEN** `poll_interval_minutes` have elapsed since the last scheduled poll
- **THEN** every repository is queried again and the icon, tooltip and menu are updated

#### Scenario: Manual refresh during a poll
- **WHEN** the user clicks "Refresh now" while a poll is running
- **THEN** no second poll is started

### Requirement: New pending items notification
After every poll except the first one, the application SHALL show a desktop notification if pending items appear that were not present in the previous poll, stating how many there are and their titles.

#### Scenario: A new pending item appears
- **WHEN** a poll finds a pending PR or issue that was not in the previous poll
- **THEN** a notification shows its repository, `#number` and title

#### Scenario: First poll
- **WHEN** the first poll after startup finishes
- **THEN** no notification is shown

#### Scenario: No changes
- **WHEN** a poll returns the same pending items as the previous one or a subset of them
- **THEN** no notification is shown
