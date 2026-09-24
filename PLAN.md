# Otonose Kanade Fan Activity Archive Plan

## 1. Purpose

This repository is a long-term archive of fan-made research and creative activities related to Otonose Kanade. Multiple activities must remain separated by directory, data model, and documentation. The first activity is a searchable catalogue of Kanade karaoke broadcasts, set lists, original songs, and useful timestamps.

The repository is designed for AI-agent-assisted maintenance. Agents may discover and prepare changes, but uncertain facts must remain visible for human review.

## 2. Repository identity

Recommended GitHub repository name:

```text
otonose-kanade
```

The repository is public so GitHub Pages can publish the catalogue.

## 3. Target structure

```text
.
├─ AGENTS.md
├─ PLAN.md
├─ README.md
├─ CONTRIBUTING.md
├─ CHANGELOG.md
├─ data/
│  └─ karaoke/
│     ├─ broadcasts.json
│     ├─ songs.json
│     ├─ candidates/
│     └─ review/
├─ activities/
│  └─ karaoke/
├─ scripts/
│  └─ karaoke/
├─ site/
├─ agent-runs/
└─ .github/
   └─ workflows/
```

## 4. Data model

Keep these entities separate:

- `broadcast`: the karaoke stream or archive
- `performance`: Kanade's performance of a song in a broadcast
- `originalSong`: the original song and artist
- `evidence`: Setlist Index entry, Holodex comment, broadcast description, video, or other source

Each performance should store the broadcast ID and order, source title and artist, normalized title and artist, candidate and confirmed timestamps, original-song URL, evidence URLs and notes, and confidence status.

## 5. Set-list collection workflow

Setlist Index is the primary structured source when it has a matching Kanade broadcast entry.

1. Find candidate Kanade singing/karaoke broadcasts.
2. Match each broadcast to the Setlist Index entry.
3. Import title, date, song order, artists, and timestamps as source-confirmed candidates.
4. Preserve the Setlist Index URL and original displayed text.
5. Use Holodex comments and the broadcast timeline where the structured entry is missing, incomplete, or conflicting.
6. Record conflicts as `needs-review`.
7. Promote only verified entries to the confirmed catalogue.

Setlist Index timestamps are useful candidates but are not automatically exact song-start positions.

## 6. AI-agent automation

Discovery, set-list, original-song, validation, and site-build agents should create reports under `agent-runs/`. Automated collection should propose changes through reviewable pull requests once GitHub Actions is enabled.

## 7. GitHub Pages

The site should provide a broadcast list, broadcast detail pages, ordered set lists, song and artist search, YouTube links, verified timestamp links, and evidence/confidence status.

The GitHub Pages site is the catalogue and timestamp index. YouTube Music is the original-song playlist destination.

## 8. YouTube Music integration

First create and review an original-song mapping. Then create or update a playlist using authenticated YouTube access. Store playlist IDs and mapping results as metadata, never as credentials.

Automation must avoid duplicate tracks, avoid replacing an existing playlist without a diff, report unmatched songs, and stop safely when authentication or quota fails.

## 9. Execution phases

1. Project rules
2. Local repository skeleton
3. Sample catalogue
4. Validation and agent reports
5. GitHub repository and CI
6. GitHub Pages
7. Playlist integration

## 10. Human intervention points

Human review is required for ambiguous set-list entries, original-song matches, GitHub authentication, the first production deployment, and playlist mutation.

## 11. Immediate next actions

1. Import additional Setlist Index broadcast records into the candidate area.
2. Add original-song mappings only after title and artist normalization.
3. Build the first static catalogue from source-confirmed candidates.
4. Add GitHub Actions for validation and reviewable collection PRs.
5. Stop before GitHub or YouTube account mutations that require additional authorization.
