# Otonose Kanade Fan Activity Archive Plan

## 1. Objective

Build an AI-maintained archive of every karaoke broadcast and set list for Otonose Kanade, then publish searchable statistics and generate reviewed YouTube Music playlist exports.

The source of truth is layered:

1. Setlist Index for structured broadcast set lists
2. Local raw snapshots for reproducibility
3. Normalized catalogue for analysis and site generation
4. Holodex comments and broadcast timelines for conflict resolution

## 2. Repository data layout

The karaoke data area will use:

- data/karaoke/raw/setlist-index/ — retrieved source-shaped snapshots, never silently overwritten
- data/karaoke/candidates/ — imported but not fully verified records
- data/karaoke/review/ — conflicts and records needing human decisions
- data/karaoke/normalized/ — normalized broadcasts, performances, original-song mappings, and tags
- data/karaoke/playlist/ — generated playlist manifests and unmatched-song reports
- data/karaoke/broadcasts.json — public catalogue input
- data/karaoke/songs.json — public performance input

Each snapshot must record retrieval date, source URL, source identifier, and parser version.

## 3. Normalized data model

A broadcast contains its ID, title, date, video URLs, source references, availability, and confidence status.

A performance contains broadcast ID, order, displayed title, normalized title, displayed artist, normalized artist, candidate or confirmed timestamp, evidence, and confidence status.

An original-song mapping contains the normalized song identity, preferred original recording, YouTube URL or video ID, mapping status, and review notes.

A song may also have optional reviewed metadata:

- genre
- mood
- language
- energy
- source of the tag
- tag confidence

Genre and mood must not be inferred from play count alone. Frequency produces popularity rankings; metadata or human-reviewed tags produce qualitative categories.

## 4. Source acquisition and import

Setlist Index is the primary structured source for matching Kanade karaoke broadcasts. The importer will:

1. Retrieve the channel listing and preserve a dated raw snapshot.
2. Identify every broadcast entry and its source URL.
3. Extract title, date, video URL, order, song title, artist, and timestamp.
4. Store the raw values unchanged.
5. Normalize values into the analysis model.
6. Deduplicate broadcasts and performances by stable video ID.
7. Send missing or conflicting fields to the review queue.
8. Create a report showing imported, changed, unmatched, and unresolved records.

Holodex is a fallback and verification source. It is used only when Setlist Index is missing, incomplete, or inconsistent, and for checking timestamps or song identity.

## 5. Dashboard output

The GitHub Pages dashboard will provide:

- yearly set-list song table
- song usage count across all broadcasts
- artist usage count
- top 50 frequently performed songs
- yearly song-list export links
- filters by year, song, artist, status, genre, mood, and language
- broadcast and timestamp links
- visible source and confidence status
- a qualitative section for reviewed genre and mood tags

With no reviewed tag data, the dashboard must show that qualitative analysis is unavailable rather than inventing categories.

## 6. Playlist generation

Generate reviewable manifests before using any YouTube account.

Required exports:

- one manifest per year containing distinct original recordings used in that year's set lists
- one manifest containing the 50 most frequently performed original recordings
- unmatched and ambiguous mappings
- duplicate removals
- source performance references

After human review and account authorization, a playlist adapter may create or update YouTube Music-compatible playlists. It must show a diff first, preserve existing playlist items unless explicitly removed, and stop on authentication or quota errors.

## 7. Automation

Planned agents and scripts:

- setlist-index importer
- normalization and deduplication script
- dashboard builder
- statistics and tag report generator
- original-song matcher
- playlist manifest generator
- validation workflow
- GitHub Pages deployment workflow

Every automated run writes a report under agent-runs/ and proposes reviewable changes.

## 8. Acceptance criteria

Phase A — Source mirror:

- all available Kanade karaoke entries are saved locally
- every raw record has source URL and retrieval metadata
- re-running import produces a stable diff

Phase B — Normalized catalogue:

- every performance has a stable broadcast reference
- duplicates and conflicts are reported
- source-confirmed and confirmed records are distinct

Phase C — Dashboard:

- yearly lists and usage counts render from normalized data
- top-50 list is reproducible
- filters and source links work
- mood and genre are shown only for tagged records

Phase D — Playlists:

- yearly and top-50 manifests are generated
- unmatched mappings are reported
- human review occurs before playlist mutation

## 9. Human intervention points

Human review is required for:

- ambiguous or conflicting set-list records
- original-song matching
- genre and mood tags when metadata is unclear
- approval of the first complete import
- YouTube account authorization and playlist mutation
- final public dashboard review
