# Spec Delta

## MODIFIED Requirements

### Requirement: Icon visual state
The icon SHALL be the GitHub logo drawn in the desktop theme's text colour, re-rendered when the colour scheme changes. The global state is shown by a badge in its bottom-right corner: no badge with nothing pending, orange with pending items and red if any repository failed in the last poll. Before the first poll finishes the logo SHALL be semi-transparent and without a badge.

#### Scenario: Startup before the first poll
- **WHEN** the application has just started and the first poll has not finished
- **THEN** the icon is the semi-transparent GitHub logo without a badge

#### Scenario: All clear
- **WHEN** the last poll finished without errors and without pending items
- **THEN** the icon is the opaque GitHub logo without a badge

#### Scenario: Pending items
- **WHEN** the last poll finished without errors and with pending items
- **THEN** the icon shows an orange badge

#### Scenario: Failed repository
- **WHEN** at least one repository failed in the last poll
- **THEN** the icon shows a red badge

#### Scenario: Theme colour
- **WHEN** the desktop colour scheme changes between light and dark
- **THEN** the logo is redrawn in the new theme text colour, keeping the current badge

### Requirement: Pending count badge
The corner badge SHALL show the total number of pending items (PRs plus issues) across all repositories, or `99+` if it exceeds 99. If there is an error and nothing pending, it SHALL show `!`. With nothing pending and no errors there SHALL be no badge.

#### Scenario: Several pending items
- **WHEN** there are 2 pending pull requests and 3 pending issues in total
- **THEN** the badge shows `5`

#### Scenario: More than 99 pending items
- **WHEN** the total of pending items is 120
- **THEN** the badge shows `99+`

#### Scenario: Error without pending items
- **WHEN** some repository failed and nothing is pending
- **THEN** the badge shows `!`

#### Scenario: Nothing to report
- **WHEN** nothing is pending and no repository failed
- **THEN** no badge is drawn
