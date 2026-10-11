# localization Specification

## Purpose
Makes every user-facing text of github-monitor translatable, with English as the source language and the interface language chosen from the system locale.

## Requirements

### Requirement: English source strings
Every user-facing string (tray tooltip, menu entries, notifications and configuration error messages) SHALL be written in English in the source code and marked for translation with gettext. Data coming from GitHub (titles, repository names, API error messages) SHALL be shown as received.

#### Scenario: No translation available
- **WHEN** the application runs under a locale without a translation catalog
- **THEN** every user-facing string is shown in English

#### Scenario: GitHub data is not translated
- **WHEN** the UI shows an issue title or a GitHub API error message
- **THEN** it is shown exactly as returned by GitHub, regardless of the locale

### Requirement: Language selection from the system locale
The interface language SHALL be selected from the standard locale environment variables (`LANGUAGE`, `LC_ALL`, `LC_MESSAGES`, `LANG`), falling back to English when no matching catalog exists.

#### Scenario: Spanish locale
- **WHEN** the application starts with `LANG=es_ES.UTF-8`
- **THEN** the tooltip, menu, notifications and configuration errors are shown in Spanish

#### Scenario: Unsupported locale
- **WHEN** the application starts with `LANG=eo_EO.UTF-8` and there is no Esperanto catalog
- **THEN** the interface is shown in English

### Requirement: Plural-aware messages
Messages that include a count SHALL use gettext plural forms so that every language can express singular and plural correctly.

#### Scenario: Single new pending item
- **WHEN** a notification reports exactly one new pending item
- **THEN** its title uses the singular form in the active language

#### Scenario: Several new pending items
- **WHEN** a notification reports three new pending items
- **THEN** its title uses the plural form in the active language

### Requirement: Complete translation catalogs
The application SHALL ship translation catalogs that translate every translatable string, with no untranslated or fuzzy entries.

#### Scenario: Catalog completeness
- **WHEN** a translation catalog is checked against the extracted template
- **THEN** every message has a non-empty, non-fuzzy translation
