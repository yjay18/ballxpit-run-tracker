# Pit Crew

Pit Crew is an unofficial, mobile-friendly companion for following a **BALL x
PIT** run as it happens. Pick one or two characters, add the balls and passives offered by
the game, match their levels, and let the build coach surface compatible
evolutions and character-specific next picks.

The app is a static site with no framework, account, or backend. Run
state and encyclopedia checkmarks stay in the browser's `localStorage`.

## What it does

- Starts with a play-first single or duo character picker covering 23 character profiles.
- Duo runs include both starting balls and combine character-aware recommendation weights.
- Shows only the active character party, 4 current ball slots, current passives, and
  the best next pickups so the screen stays readable during active play.
- Keeps level tracking off by default for fast play, with an optional levels
  toggle for balls, passives, and evolved items.
- Compares only the 2–3 items currently offered by the game and ranks the best
  choice for the active character and build.
- Supports one-step Undo for run changes, a compact icon-focused layout, and a
  pinned ball evolution or passive artifact target.
- Hides encyclopedia navigation during active runs and keeps recommendations in
  a collapsible mobile tray at the bottom of the screen.
- Detects ball evolutions when every recipe component is level 3.
- Detects passive artifact recipes when all components are held, and enforces
  level 3 for every component when level tracking is enabled.
- Applies a ready evolution from the recommendation panel, consumes its
  ingredients, and adds the result at level 1.
- Routes ball and passive suggestions through the detected build strategy,
  including baby-ball swarm, status/AOE, bounce, crit, sustain, close-range,
  summon, and deep-evolution builds.
- Suggests the next relevant passive evolution and its missing ingredients.
- Lets any two eligible unfused balls evolve or fuse, previews both inherited
  abilities, and records fused balls as level 3.
- Handles character overrides such as Sisyphus's zero direct damage,
  Tactician's irrelevant Speed stat, Empty Nester's missing baby balls, Hoary
  Hoarder's 2/8 slot split, and Ballbearer's 10/0 slot split.
- Surfaces ready ball evolutions and passive artifacts directly above the next
  pickup suggestions.
- Keeps the original searchable encyclopedia for 20 base balls, 59 ball
  evolutions, 53 base passives, 13 passive artifacts, and Matchmaker pairs.
- Works as a single responsive page on desktop and mobile.

## Run locally

Open `index.html` directly in a modern browser. No install or build command is
required.

For a local web server, run:

```sh
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Project layout

- `index.html` — UI, game database, recommendation rules, and persistence.
- `img/balls/` — base and evolved ball sprites.
- `img/passives/` — base passive and artifact sprites.
- `img/characters/` — character sprites.
- `img/pit-crew-logo.svg` and `.png` — reusable Pit Crew logo and browser icon.
- `sprite-manifest.txt` — expected image names and paths.
- `GAME_INFO.txt` — plain-text game explanation, tracker model, and recipe
  quick reference.

## Data status

The encyclopedia foundation is current through the **Shadow Update (April 27,
2026)**. The supplied systems brief adds strategy profiles for the Hoary
Hoarder and Ballbearer. The wider Naturalist Update data set has not been fully
audited, so community corrections are welcome.

Recommendations are deterministic practical heuristics, not a claim of a
solved optimal meta. The current character and loadout select a strategy route;
recipe proximity, fusion carriers, passive evolution paths, conditional loot
requirements, and an optional pinned target then contribute to the ranking.

## Visit analytics

Pit Crew uses the privacy-first Cloudflare Web Analytics beacon installed
manually in `index.html`. Analytics are reported in the owner's Cloudflare
dashboard; no analytics credentials are stored in this repository.

## Original tracker credit

This project is built on the excellent **BALL x PIT Evolution Tracker** by
**Allena Oglivie / Cryphixi**:

- Original live tracker: <https://cryphixi.github.io/ballxpit-tracker/>
- Original project: <https://github.com/cryphixi/ballxpit-tracker>

The original tracker supplied the encyclopedia structure, recipe coverage,
Matchmaker logic, and sprite collection that made this run companion possible.
Its MIT license and copyright notice are preserved in `LICENSE`. Thank you to
the original creator and contributors.

Additional game data was compiled from
[ballxpit.wiki.gg](https://ballxpit.wiki.gg). Curated Matchmaker combinations in
the inherited tracker credit [Dexerto](https://www.dexerto.com).

## Disclaimer and asset ownership

**BALL x PIT**, its names, characters, and all associated artwork are the
property of Kenny Sun and Devolver Digital. This is an unofficial fan project
and is not affiliated with or endorsed by the developer or publisher.

Sprite assets are included only for player convenience and will be removed on
request. The MIT license applies to the original code, not to game data or game
artwork.
