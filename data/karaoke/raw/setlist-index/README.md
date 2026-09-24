# Setlist Index raw snapshots

Setlist Index is downloaded locally first. GitHub Actions does not access the external site directly.

## Required local upload file

Upload the current page HTML as:

    data/karaoke/raw/setlist-index/latest.html

Keep dated copies when possible, for example:

    data/karaoke/raw/setlist-index/2026-09-24.html

Each snapshot must include or be accompanied by:

- retrieval date
- source URL
- source identifier or video ID
- importer/parser version
- retrieval result or error

Do not overwrite a dated snapshot. The workflow reads latest.html, parses it, and stores the result as a reviewable artifact.
