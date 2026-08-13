# BALL x PIT Evolution Tracker

An unofficial, single-page tracker for every ball, passive, and evolution in
**BALL x PIT**, with check-off progress that saves in your browser, and a
Matchmaker team builder that recommends character pairings.

**Live site:** https://cryphixi.github.io/ballxpit-tracker/

Data current through the **Shadow Update (April 27, 2026)**. The Naturalist
Update (July 2026) is not yet included.

## Features

- **Base Balls** — all 20, with damage types, status effects, starting characters, and unlock conditions.
- **Evolutions** — all 59 evolved balls with exact recipes, sortable and filterable by tier or by which base ball they use. Every row expands into a detail panel.
- **By Base Ball** — pick a base ball, see everything it makes (direct recipes and full-chain indirect ones).
- **Passives** — all 53 base passives plus the 13 evolved passives with recipes.
- **Team Builder** — drag or tap two characters into the Matchmaker slots. Recommendations are scored on two separate axes: **ball fusion** (do their starting balls evolve together?) and **ability synergy** (do their abilities actually complement each other?), plus curated community combos.
- Check-off boxes on every evolution and evolved passive, saved to `localStorage`, with live progress counters.
- Works offline once loaded. No build step, no framework, no tracking, no backend.

## Running locally

Clone or download, then open `index.html` in a browser. That's it.

## Contributing / updating data

All game data lives in a single `GAME_DATA` object at the top of the `<script>`
block in `index.html`. Add or edit entries there — the tables, filters,
by-base-ball grouping, and team-builder scoring all derive from it at runtime.
Console assertions check the expected counts on load.

Sprite images live in `img/balls/`, `img/passives/`, and `img/characters/`.
Filenames are slugified item names (`Frozen Flame` → `frozen-flame.png`); see
`sprite-manifest.txt` for the full list. Any missing file automatically falls
back to a generated placeholder, so new entries render fine before art exists.

Corrections and additions are welcome, open an issue or PR.

## Credits & disclaimer

Game data compiled from [ballxpit.wiki.gg](https://ballxpit.wiki.gg).
Curated team combos credit: [Dexerto](https://www.dexerto.com).

**BALL x PIT** and all associated artwork are the property of Kenny Sun and
Devolver Digital. This is an unofficial fan project and is **not affiliated with
or endorsed by** the developer or publisher. Sprite assets are included for the
convenience of players and **will be removed on request** — open an issue or
contact the repository owner.

The original code in this repository is released under the MIT License. That
license covers the code only, not the game assets or game data.
