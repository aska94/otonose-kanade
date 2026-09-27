# Treemap layout update

- Run date: 2026-09-27 (Asia/Seoul).
- Scope: replace the main page genre/mood bars with responsive treemap cards.
- Sources inspected: AGENTS.md, site/index.html, site/dashboard.js, site/styles.css, site/data.json, site/README.md, scripts/karaoke/build_dashboard.py, scripts/karaoke/test_tag_profile.py, GitHub Pages and validation workflows. No external factual data collected.
- Records added/changed: none. Existing AI candidate status and source links remain visible. Data generation is unchanged and regenerates identical site/data.json.
- Implementation: dependency-free recursive area partition by positive songCount, all tags separated by axis, supplied percentages, count-weighted colors, ResizeObserver, hover/focus/tap tooltips, accessible tile labels, and mobile stacking.
- Validation: JavaScript syntax passed; six existing profile tests passed; scripts/validate_karaoke.py passed; dashboard generation passed with no data diff; git diff --check passed. Local HTTP + headless Edge checks passed at 1440, 390, and 320 px for all tile counts/labels and proportional areas, tooltips, focus, click, Escape, stacking, horizontal overflow, top songs, year groups, and search/empty/reset behavior. Desktop and mobile screenshots inspected. No browser errors.
- Unresolved conflicts: none found. Existing unrelated untracked research files were left in place.
- Human action: review and publish changes through the repository's usual GitHub Pages workflow. No push or deployment performed; production deployment itself was not tested.
