# GitHub Monitor

[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Linux%20KDE%20%2F%20SNI-important.svg)](#)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green.svg)](https://riverbankcomputing.com/software/pyqt/)
[![GitHub GraphQL](https://img.shields.io/badge/API-GitHub%20GraphQL-181717.svg)](https://docs.github.com/en/graphql)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/arrase/github-monitor/blob/main/LICENSE)

**System Tray Watcher for Pull Requests & Unanswered Issues**

GitHub Monitor is a small background utility for Linux that lives in the system tray. It polls your public and private repositories through the GitHub GraphQL API and tells you, at a glance, how many pull requests and issues are waiting for you.

---

## Key Features

<div class="projects-grid">
  <div class="feature-card">
    <i class="fa-solid fa-inbox feature-icon"></i>
    <h3>System Tray Centric</h3>
    <p>A single icon with a badge counter. Left click refreshes immediately, right click opens a per-repository menu.</p>
  </div>

  <div class="feature-card">
    <i class="fa-solid fa-code-pull-request feature-icon"></i>
    <h3>Pull Requests & Issues</h3>
    <p>Every open pull request, plus every open issue whose last comment does not come from a maintainer.</p>
  </div>

  <div class="feature-card">
    <i class="fa-solid fa-lock feature-icon"></i>
    <h3>Public & Private Repos</h3>
    <p>Works with any repository your token can read, using a classic token or a read-only fine-grained one.</p>
  </div>

  <div class="feature-card">
    <i class="fa-solid fa-bell feature-icon"></i>
    <h3>Desktop Notifications</h3>
    <p>A notification is shown whenever new pending items appear since the previous check.</p>
  </div>

  <div class="feature-card">
    <i class="fa-solid fa-palette feature-icon"></i>
    <h3>Theme-Aware Icon</h3>
    <p>The GitHub logo is repainted with your theme's text colour at runtime, with an orange or red status badge.</p>
  </div>

  <div class="feature-card">
    <i class="fa-solid fa-language feature-icon"></i>
    <h3>Translated Interface</h3>
    <p>English source strings with gettext catalogs. The language follows your system locale; Spanish is included.</p>
  </div>
</div>

---

## Reading the Icon

| Icon | Meaning |
| :--- | :--- |
| Semi-transparent logo | First check in progress. |
| Logo without badge | All clear. |
| Orange badge with a number | Total pending pull requests and issues (`99+` above 99). |
| Red badge | Some repository failed in the last check; shows the pending count, or `!` if there is none. |

---

## Documentation Overview

<div class="projects-grid">
  <a href="architecture.md" class="feature-card">
    <i class="fa-solid fa-sitemap feature-icon"></i>
    <h3>Architecture & Design</h3>
    <p>Module layout, the Qt main thread versus the polling thread, and how results flow back into the UI.</p>
  </a>

  <a href="detection.md" class="feature-card">
    <i class="fa-solid fa-magnifying-glass feature-icon"></i>
    <h3>Attention Rules</h3>
    <p>The GraphQL queries, pagination, and the rule that decides whether an issue is waiting for a reply.</p>
  </a>

  <a href="tray.md" class="feature-card">
    <i class="fa-solid fa-bars-staggered feature-icon"></i>
    <h3>Tray Icon & Notifications</h3>
    <p>Icon rendering, badge states, tooltip, context menu, click behaviour and new-item notifications.</p>
  </a>

  <a href="configuration.md" class="feature-card">
    <i class="fa-solid fa-gear feature-icon"></i>
    <h3>Configuration</h3>
    <p>Reference for <code>config.toml</code>: token, repositories, maintainers and polling interval.</p>
  </a>

  <a href="localization.md" class="feature-card">
    <i class="fa-solid fa-language feature-icon"></i>
    <h3>Localization</h3>
    <p>How the language is selected and how to update or add gettext translation catalogs.</p>
  </a>

  <a href="installation.md" class="feature-card">
    <i class="fa-solid fa-download feature-icon"></i>
    <h3>Installation & Setup</h3>
    <p>Install with <code>pipx</code> or <code>uv</code> and start the monitor automatically on login.</p>
  </a>

  <a href="development.md" class="feature-card">
    <i class="fa-solid fa-code feature-icon"></i>
    <h3>Development</h3>
    <p>Editable install, running the test suite, and the project's code principles.</p>
  </a>
</div>
