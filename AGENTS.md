# AGENTS.md

## Project mission

This repository records fan-made research and creative activities related to Otonose Kanade. Multiple activities may coexist, so each activity must remain separated by directory, data model, and documentation.

The first activity is a catalogue of Kanade karaoke broadcasts, their set lists, original songs, and broadcast timestamps.

## Required behavior

1. Read this file before changing project files.
2. Do not add factual data without recording an evidence source.
3. Use Setlist Index as the primary structured source for karaoke set lists when a matching broadcast entry exists.
4. Use Holodex comments and the broadcast timeline to resolve missing or conflicting information.
5. Do not confuse a karaoke broadcast, a performed song, and the original song.
6. Never mark uncertain information as `confirmed`.
7. Preserve existing records unless evidence shows that they are incorrect.
8. Do not delete records merely because a video is private, deleted, or unavailable; record the availability state.
9. Keep unrelated activities out of `data/karaoke/`.
10. Generated site files must be reproducible from source data and build scripts.
11. Automated collection must propose changes for review; it must not silently write directly to the default branch.

## Evidence and confidence

Use these statuses:

- `candidate`: discovered but not sufficiently checked
- `source-confirmed`: supported by a reliable source such as Setlist Index, Holodex comments, or a broadcast description
- `confirmed`: checked against the broadcast or multiple independent sources
- `needs-review`: conflicting or incomplete evidence

For every broadcast and song, preserve source URLs and, where practical, the relevant comment text or a short evidence note.

## Set-list workflow

1. Find the matching Setlist Index entry.
2. Import its title, date, song order, artist, and timestamp as source-confirmed candidates.
3. Preserve the original displayed text and source URL.
4. Use Holodex comments and the video timeline to resolve omissions, duplicates, alternate names, and timestamp offsets.
5. Send conflicts and low-confidence matches to `needs-review`.

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
