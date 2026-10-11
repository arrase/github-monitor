# Tray Icon & Notifications

The whole user interface is a `QSystemTrayIcon`. On KDE Plasma it is published as a StatusNotifierItem, so the context menu is rendered by the shell and notifications go through the desktop's standard service.

---

## Dynamic Icon Rendering

The icon is never loaded as a ready-made PNG. `render_icon` paints it at runtime on a 64×64 `QPixmap`:

1. The bundled GitHub `mark-github` SVG is rendered with `QSvgRenderer`.
2. Painting with the `SourceIn` composition mode keeps the logo's shape and repaints it in the theme's `WindowText` colour, so it is white on dark panels and black on light ones.
3. While the first check runs, the logo is drawn at 40% opacity.
4. If there is something to report, a rounded badge with bold white text is drawn in the bottom-right corner.

The icon is re-rendered whenever the colour scheme changes (`colorSchemeChanged`).

### Badge States

| Situation | Badge colour | Badge text |
| :--- | :--- | :--- |
| Nothing pending, no errors | *(none)* | |
| Pending items | Orange (`#ef6c00`) | Total count, `99+` above 99 |
| A repository failed, items pending | Red (`#c62828`) | Total count |
| A repository failed, nothing pending | Red (`#c62828`) | `!` |

The count is the sum of pending pull requests and issues across all repositories. An error always wins over the orange colour.

---

## Tooltip

The tooltip has one line per repository that has something to say, followed by the time of the last check:

```
arrase/github-monitor: 2 pull requests, 1 issue
arrase/other: error: Could not resolve to a Repository
Last update: 16:32
```

Repositories with nothing pending are omitted; if none remain, the summary reads `All clear`. Counts use gettext plural forms.

---

## Context Menu

Right-clicking the icon shows one submenu per repository that has pending items or an error, titled `owner/name (count)`:

- An error, if any, is shown as a disabled entry at the top.
- A **Pull requests** section and an **Issues** section list `#number title`; clicking an entry opens it in your browser with `QDesktopServices.openUrl`.

The menu always ends with **Refresh now** and **Quit**. Ampersands in titles are escaped, because a single `&` marks a keyboard mnemonic in Qt menus.

---

## Click Behaviour

| Action | Result |
| :--- | :--- |
| **Left click** | Refresh immediately. |
| **Right click** | Menu shown by the shell. |

!!! note "Why left click does not open the menu"
    On Wayland, `QMenu.popup()` without a focused parent window fails with "Failed to create grabbing popup", and Qt then marks the item as not being a menu. The menu is therefore left to the shell (right click) and the left click is used for refreshing.

---

## New-Item Notifications

`TrayIcon` keeps the set of pending item URLs from the previous poll (`None` before the first one).

1. After each poll, the new set is compared with the previous one.
2. Items whose URL was not present before are *new*.
3. If there is at least one new item and this is not the first poll, `showMessage` displays a notification titled `N new pending item(s) on GitHub`, with one `repo #number title` line per new item.

The first poll after startup never notifies, so launching the application does not flood you with everything that was already pending.
