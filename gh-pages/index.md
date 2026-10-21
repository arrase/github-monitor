---
hide:
  - toc
---

<div class="hero-section">
  <div class="hero-eyebrow">
    <i class="fa-brands fa-github" aria-hidden="true"></i>
    <span>Linux System Tray Notification Utility</span>
  </div>
  <h1>GitHub Monitor</h1>
  <p class="hero-subtitle">A lightweight background utility for the Linux system tray that polls your public and private repositories via the GitHub GraphQL API and shows, at a glance, how many pull requests and unanswered issues need your attention.</p>
  <div class="hero-badges">
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.12%2B-blue.svg" alt="Python 3.12+"></a>
    <a href="#"><img src="https://img.shields.io/badge/platform-Linux%20KDE%20%2F%20SNI-important.svg" alt="Platform"></a>
    <a href="https://riverbankcomputing.com/software/pyqt/"><img src="https://img.shields.io/badge/GUI-PyQt6-green.svg" alt="PyQt6"></a>
    <a href="https://docs.github.com/en/graphql"><img src="https://img.shields.io/badge/API-GitHub%20GraphQL-181717.svg" alt="GitHub GraphQL"></a>
    <a href="https://github.com/arrase/github-monitor/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  </div>
  <div class="hero-badges">
    <a href="https://sonarcloud.io/summary/overall?id=arrase_github-monitor"><img src="https://sonarcloud.io/api/project_badges/measure?project=arrase_github-monitor&amp;metric=alert_status" alt="Quality Gate Status"></a>
    <a href="https://sonarcloud.io/summary/overall?id=arrase_github-monitor"><img src="https://sonarcloud.io/api/project_badges/measure?project=arrase_github-monitor&amp;metric=coverage" alt="Coverage"></a>
    <a href="https://sonarcloud.io/summary/overall?id=arrase_github-monitor"><img src="https://sonarcloud.io/api/project_badges/measure?project=arrase_github-monitor&amp;metric=bugs" alt="Bugs"></a>
    <a href="https://sonarcloud.io/summary/overall?id=arrase_github-monitor"><img src="https://sonarcloud.io/api/project_badges/measure?project=arrase_github-monitor&amp;metric=vulnerabilities" alt="Vulnerabilities"></a>
    <a href="https://sonarcloud.io/summary/overall?id=arrase_github-monitor"><img src="https://sonarcloud.io/api/project_badges/measure?project=arrase_github-monitor&amp;metric=code_smells" alt="Code Smells"></a>
    <a href="https://sonarcloud.io/summary/overall?id=arrase_github-monitor"><img src="https://sonarcloud.io/api/project_badges/measure?project=arrase_github-monitor&amp;metric=sqale_index" alt="Technical Debt"></a>
    <a href="https://sonarcloud.io/summary/overall?id=arrase_github-monitor"><img src="https://sonarcloud.io/api/project_badges/measure?project=arrase_github-monitor&amp;metric=duplicated_lines_density" alt="Duplicated Lines (%)"></a>
    <a href="https://sonarcloud.io/summary/overall?id=arrase_github-monitor"><img src="https://sonarcloud.io/api/project_badges/measure?project=arrase_github-monitor&amp;metric=security_rating" alt="Security Rating"></a>
    <a href="https://sonarcloud.io/summary/overall?id=arrase_github-monitor"><img src="https://sonarcloud.io/api/project_badges/measure?project=arrase_github-monitor&amp;metric=reliability_rating" alt="Reliability Rating"></a>
    <a href="https://sonarcloud.io/summary/overall?id=arrase_github-monitor"><img src="https://sonarcloud.io/api/project_badges/measure?project=arrase_github-monitor&amp;metric=sqale_rating" alt="Maintainability Rating"></a>
    <a href="https://sonarcloud.io/summary/overall?id=arrase_github-monitor"><img src="https://sonarcloud.io/api/project_badges/measure?project=arrase_github-monitor&amp;metric=ncloc" alt="Lines of Code"></a>
  </div>
</div>

<div class="section-header">
  <h2>Key Features</h2>
  <span>At-a-glance repository monitoring</span>
</div>

<div class="projects-grid">
  <div class="feature-card">
    <i class="fa-solid fa-inbox feature-icon" aria-hidden="true"></i>
    <h3>System Tray Centric</h3>
    <p>A single icon with a badge counter. Left click refreshes immediately, right click opens a per-repository menu.</p>
  </div>

  <div class="feature-card">
    <i class="fa-solid fa-code-pull-request feature-icon" aria-hidden="true"></i>
    <h3>Pull Requests &amp; Issues</h3>
    <p>Every open pull request, plus every open issue whose last comment does not come from a maintainer.</p>
  </div>

  <div class="feature-card">
    <i class="fa-solid fa-lock feature-icon" aria-hidden="true"></i>
    <h3>Public &amp; Private Repos</h3>
    <p>Works with any repository your token can read, using a classic token or a read-only fine-grained one.</p>
  </div>

  <div class="feature-card">
    <i class="fa-solid fa-bell feature-icon" aria-hidden="true"></i>
    <h3>Desktop Notifications</h3>
    <p>A notification is shown whenever new pending items appear since the previous check.</p>
  </div>

  <div class="feature-card">
    <i class="fa-solid fa-palette feature-icon" aria-hidden="true"></i>
    <h3>Theme-Aware Icon</h3>
    <p>The GitHub logo is repainted with your theme's text colour at runtime, with an orange or red status badge.</p>
  </div>

  <div class="feature-card">
    <i class="fa-solid fa-language feature-icon" aria-hidden="true"></i>
    <h3>Translated Interface</h3>
    <p>English source strings with gettext catalogs. The language follows your system locale; Spanish is included.</p>
  </div>
</div>

## Reading the Icon

| Icon | Meaning |
| :--- | :--- |
| Semi-transparent logo | First check in progress. |
| Logo without badge | All clear. |
| Orange badge with a number | Total pending pull requests and issues (`99+` above 99). |
| Red badge | Some repository failed in the last check; shows the pending count, or `!` if there is none. |

<div class="section-header">
  <h2>Documentation</h2>
  <span>Architecture, attention rules &amp; setup guides</span>
</div>

<div class="projects-grid">
  <a href="architecture/" class="feature-card">
    <div class="card-top">
      <i class="fa-solid fa-sitemap feature-icon" aria-hidden="true"></i>
      <span class="card-badge">Read →</span>
    </div>
    <h3>Architecture &amp; Design</h3>
    <p>Module layout, the Qt main thread versus the polling thread, and how results flow back into the UI.</p>
  </a>

  <a href="detection/" class="feature-card">
    <div class="card-top">
      <i class="fa-solid fa-magnifying-glass feature-icon" aria-hidden="true"></i>
      <span class="card-badge">Read →</span>
    </div>
    <h3>Attention Rules</h3>
    <p>The GraphQL queries, pagination, and the rule that decides whether an issue is waiting for a reply.</p>
  </a>

  <a href="tray/" class="feature-card">
    <div class="card-top">
      <i class="fa-solid fa-bars-staggered feature-icon" aria-hidden="true"></i>
      <span class="card-badge">Read →</span>
    </div>
    <h3>Tray Icon &amp; Notifications</h3>
    <p>Icon rendering, badge states, tooltip, context menu, click behaviour and new-item notifications.</p>
  </a>

  <a href="configuration/" class="feature-card">
    <div class="card-top">
      <i class="fa-solid fa-gear feature-icon" aria-hidden="true"></i>
      <span class="card-badge">Read →</span>
    </div>
    <h3>Configuration</h3>
    <p>Reference for <code>config.toml</code>: token, repositories, maintainers and polling interval.</p>
  </a>

  <a href="localization/" class="feature-card">
    <div class="card-top">
      <i class="fa-solid fa-language feature-icon" aria-hidden="true"></i>
      <span class="card-badge">Read →</span>
    </div>
    <h3>Localization</h3>
    <p>How the language is selected and how to update or add gettext translation catalogs.</p>
  </a>

  <a href="installation/" class="feature-card">
    <div class="card-top">
      <i class="fa-solid fa-download feature-icon" aria-hidden="true"></i>
      <span class="card-badge">Read →</span>
    </div>
    <h3>Installation &amp; Setup</h3>
    <p>Install with <code>pipx</code> or <code>uv</code> and start the monitor automatically on login.</p>
  </a>

  <a href="development/" class="feature-card">
    <div class="card-top">
      <i class="fa-solid fa-code feature-icon" aria-hidden="true"></i>
      <span class="card-badge">Read →</span>
    </div>
    <h3>Development</h3>
    <p>Editable install, running the test suite, and the project's code principles.</p>
  </a>
</div>
