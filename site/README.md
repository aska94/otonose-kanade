# Karaoke dashboard

`python scripts/karaoke/build_dashboard.py` reads normalized performance records plus saved agy feature results and the Korean translation dictionary, then regenerates `site/data.json`. It makes no network or agy calls.

The feature section uses `tagProfile.denominator` for the explanatory sample size and displays all positive-count genre and mood tags in separate responsive treemap cards. `dashboard.js` partitions each card by `songCount` and displays the supplied `percent`; `ResizeObserver` recalculates the layout and hides labels that do not fit. Hover, keyboard focus, and tap expose the name, count, and percentage. Percentages use collected records, not performance frequency; multiple tags may overlap, so tile area represents a share of tag assignments, not a percentage of the whole card. No chart dependency or extra build step is required.

Tag labels are Korean. Song titles and artist credits retain their original spelling. `data/karaoke/normalization/feature-tags-ko.json` translates Japanese/Latin tags and merges equivalent Korean wording. Raw responses and original tags are retained. Unmapped foreign-language labels fail the build instead of leaking into the Korean display.

These are AI search candidates accepted by the user without additional source verification. Links open the corresponding Google query and are labelled as AI candidates. The older iTunes data remains preserved in `song-tags.json` but is not mixed into the new feature chart.

To export the translated records separately: `python -B scripts/karaoke/build_song_features.py`. Tests: `python -B -m unittest discover -s scripts/karaoke -p test_tag_profile.py`.

The dashboard intentionally shows only the 20 most-played songs overall and the 10 most-played songs within each year.

The main page omits the coverage fraction and per-song feature list/search. Underlying song records remain in data.json.
