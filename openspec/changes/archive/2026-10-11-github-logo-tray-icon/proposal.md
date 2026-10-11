# Proposal

## Why

The current tray icon is a plain coloured circle with a number: it is readable but anonymous, so it is hard to tell at a glance which application it belongs to among other tray icons. Using the GitHub logo makes it instantly recognisable while keeping the pending count visible.

## What Changes

- The tray icon becomes the GitHub logo (Octicons `mark-github`) drawn in a single colour that follows the desktop theme's text colour (white on dark panels, black on light ones), re-rendered when the colour scheme changes.
- The state moves to a rounded badge in the bottom-right corner of the logo:
  - Orange badge with the pending count (`99+` above 99) when there are pending items.
  - Red badge with the pending count, or `!` with nothing pending, when any repository failed.
  - No badge when everything is clear (the green state disappears).
- While the first poll is running the logo is drawn semi-transparent, without a badge (the grey state disappears).
- The logo SVG ships with the package together with its MIT licence notice.

## Capabilities

### New Capabilities

### Modified Capabilities
- `tray-indicator`: "Icon visual state" changes from a coloured circle to the theme-coloured GitHub logo with a corner badge; "Pending count badge" moves the count into that corner badge and drops it when all is clear.

## Impact

- `src/github_monitor/tray.py`: icon rendering (`render_icon`, `state_color`) and repainting on colour scheme changes.
- New asset `src/github_monitor/assets/github-mark.svg` plus licence notice; `pyproject.toml` package data.
- Uses `PyQt6.QtSvg` (already shipped with the PyQt6 wheels); no new dependencies.
- README "Reading the icon" section.
