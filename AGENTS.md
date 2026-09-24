# AGENTS.md

## Project mission

This repository records fan-made research and creative activities related to Otonose Kanade. Multiple activities may coexist, so each activity must remain separated by directory, data model, and documentation.

The first activity is a catalogue of Kanade karaoke broadcasts, their set lists, original songs, and broadcast timestamps.

## Required behavior

1. Read this file before changing project files.
2. Do not add factual data without recording an evidence source.
3. Treat Holodex comments as the primary set-list discovery source when available.
4. Do not confuse a karaoke broadcast, a performed song, and the original song.
5. Never mark uncertain information as `confirmed`.
6. Preserve existing records unless evidence shows that they are incorrect.
7. Do not delete records merely because a video is private, deleted, or unavailable; record the availability state.
8. Keep unrelated activities out of `data/karaoke/`.
9. Generated site files must be reproducible from source data and build scripts.
10. Automated collection must propose changes for review; it must not silently write directly to the default branch.

## Evidence and confidence

Use these statuses:

- `candidate`: discovered but not sufficiently checked
- `source-confirmed`: supported by a reliable source such as Holodex comments or a broadcast description
- `confirmed`: checked against the broadcast or multiple independent sources
- `needs-review`: conflicting or incomplete evidence

For every broadcast and song, preserve source URLs and, where practical, the relevant comment text or a short evidence note.

## Holodex comment workflow

1. Discover candidate broadcasts from the Kanade channel and singing-related results.
2. Collect Holodex comments for each broadcast.
3. Extract song-title, artist, order, and timestamp candidates.
4. Normalize Japanese, English, abbreviations, and obvious spelling variants without discarding the original text.
5. Compare repeated comments and secondary sources.
6. Treat comment time as a candidate timestamp until checked against the video timeline.
7. Send conflicts and low-confidence matches to `needs-review`.

## Data safety

Preferred writable areas for automated collection:

- `data/karaoke/candidates/`
- `data/karaoke/review/`
- `agent-runs/`

Changes to confirmed catalogues, schemas, workflows, and this file require an explicit reviewable change. Do not introduce credentials, cookies, access tokens, or private account data into the repository.

## Validation

Before submitting a change, check:

- JSON or YAML syntax
- required fields and unique IDs
- duplicate broadcasts and songs
- valid YouTube and evidence URLs
- timestamp format and timestamp links
- status/evidence consistency
- generated pages build from source data

If validation cannot be run yet because the scripts do not exist, state that clearly in the change report.

## Change reporting

Every automated run should report:

- run date and scope
- sources inspected
- records added or changed
- unresolved conflicts
- validation results
- human actions required
