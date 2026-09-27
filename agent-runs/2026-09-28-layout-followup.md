# Main page layout follow-up

- Run date: 2026-09-28 (Asia/Seoul).
- Scope: rename overview labels to 노래 횟수 and 곡 수; remove the genre coverage fraction and per-song feature list/search.
- Sources inspected: repository AGENTS.md, site/index.html, site/dashboard.js, site/README.md. No external data collected.
- Records added/changed: none; source records and site/data.json remain unchanged.
- Changes: removed the corresponding HTML and JavaScript rendering/event handlers; updated site documentation. Treemap percentages, tooltips, and sample-size explanation remain.
- Validation: JavaScript syntax and git diff --check passed. Headless Edge checks passed at 1440, 390, and 320 px for updated labels, absence of removed sections, proportional tile areas, data labels, tooltip/focus/click/Escape behavior, responsive layout, overflow, rankings, and year lists. No browser errors.
- Unresolved conflicts: none found.
- Human action: review the local preview. Changes have not been pushed or deployed.

## Section heading alignment

- Inspected site/styles.css and site/index.html; unified all section heading columns, font sizes, and line heights. Removed the genre-only overrides and gave each main section title the same wider column.
- No data records changed and no unresolved conflicts found.
- Headless Edge checks passed at 1440, 1024, 800, 761, 760, 390, and 320 px: identical heading font sizes and left alignment, single-line headings, and no horizontal overflow. git diff --check passed.
- Restarted the local preview server for review. No deployment performed.
