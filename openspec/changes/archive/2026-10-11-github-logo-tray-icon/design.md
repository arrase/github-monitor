# Design

## Context

`tray.py` currently draws the icon with `QPainter` on a 64×64 `QPixmap` (`render_icon(color, text)`), with `state_color(total, has_error)` choosing between green, orange and red and a grey icon at startup. See proposal.md for motivation and the `tray-indicator` delta for the required behaviour.

## Goals / Non-Goals

**Goals:**
- Recognisable GitHub logo that stays legible on light and dark panels.
- Keep icon rendering a single function with pure helpers that are easy to test.

**Non-Goals:**
- Per-state logo colours (GitHub's logo guidelines only allow the mark in black or white).
- Icon themes or user-configurable icons.

## Decisions

### Logo source: Octicons `mark-github` SVG
Ship `src/github_monitor/assets/github-mark.svg` (Octicons `mark-github-24.svg`, MIT licence) as package data, with its licence in `src/github_monitor/assets/LICENSE-octicons`. Rendered with `QSvgRenderer` from `PyQt6.QtSvg`, which is part of the PyQt6 wheels. Alternatives: hand-drawn `QPainterPath` (fragile, hard to keep faithful), PNG assets (blurry at other sizes, one per theme).

### Monochrome via composition
Render the SVG onto a transparent pixmap, then fill it with the theme colour using `CompositionMode_SourceIn`, which keeps the logo's alpha and replaces its colour. The theme colour is `QApplication.palette().color(QPalette.ColorRole.WindowText)`. While loading, the logo is painted with opacity 0.4.

### Badge
A rounded rectangle anchored at the bottom-right corner, 34 px high on the 64 px canvas, its width growing with the text (minimum a circle) so `99+` stays legible; the text is bold white. `badge_text(total, has_error)` stays as is (empty string means no badge); `state_color(total, has_error)` returns the badge colour or `None` when there is nothing to report, replacing the green state. A thin outline in the logo colour is not added: the coloured badge over the logo is enough contrast in both themes.

`render_icon(text: str, color: str | None, loading: bool) -> QIcon` replaces `render_icon(color, text)`; the startup call becomes `render_icon("", None, loading=True)`.

### Reacting to theme changes
`TrayIcon` keeps the last `(text, color)` it rendered and connects `QGuiApplication.styleHints().colorSchemeChanged` to a slot that re-renders with the current palette. Alternative: an event filter for `ApplicationPaletteChange` (more code for the same effect on Plasma 6).

## Risks / Trade-offs

- [The application palette may not match the panel (e.g. light windows with a dark panel)] → On Plasma the panel follows the global colour scheme, which is what the palette reflects; if a mismatch shows up, a follow-up can expose a setting. Out of scope now.
- [Badge covers part of the logo at 16–22 px tray sizes] → The badge is placed in the corner and the logo remains recognisable by its silhouette; verified visually in the panel.
- [GitHub trademark] → The mark is used unmodified, in black/white, to refer to GitHub, as allowed by GitHub's logo guidelines; noted in the README.
