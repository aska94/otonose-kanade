# Korean song feature dashboard deployment — 2026-09-27

- Scope: publish 65 saved agy song-feature candidates with Korean tags, genre/mood charts and song/tag search.
- Sources: saved AI-derived results and query metadata under `data/karaoke/review/agy-song-features-2026-09-26/`; no additional agy requests or source HTML uploads.
- Data: Korean translation preserves original names and raw tags; all AI records remain candidate. 491 title/artist pairs remain uncollected due to the recorded account quota.
- Validation prerequisite: corrected the validator's repository root. It revealed two existing malformed timestamp display strings. For `Ec8OAZot2-w-08`, timestampSeconds=3584 and the matching sourceUrl offset give `59:44`; for `woCEixptAPY-34`, timestampSeconds=7189 and the matching offset give `1:59:49`. Previous displays `1:60:44` and `2:60:49` are preserved in `timestampNormalization.previousDisplay`. No navigation offset, evidence URL, record ID or confidence status changed.
- Corrected display values are recorded in the two broadcast sources and both tracked performance aggregates. This is an internally supported formatting correction, not new broadcast research.
- Validation: full catalogue validation, six feature tests, JavaScript syntax, reproducible generated artifacts and desktop/mobile browser checks. CI also runs feature tests and checks reproducibility.
- Deployment path: reviewable GitHub pull request, then merge to main for the existing GitHub Pages workflow. User explicitly authorized deployment.
- Local collection scripts, CLI execution logs and failed/superseded probes are not needed for site publication and remain local.
