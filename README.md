# Pit Crew

Pit Crew is an unofficial, mobile-friendly companion for following a **BALL x
PIT** run as it happens. Pick a character, add the balls and passives offered by
the game, match their levels, and let the build coach surface compatible
evolutions and character-specific next picks.

The app is a static site with no framework, account, analytics, or backend. Run
state and encyclopedia checkmarks stay in the browser's `localStorage`.

## What it does

- Starts with a play-first character picker covering 23 character profiles.
- Shows only the active character, 4 current ball slots, current passives, and
  the best next pickups so the screen stays readable during active play.
- Tracks levels 1–3 for base balls, evolved balls, base passives, and evolved
  passive artifacts.
- Compares only the 2–3 items currently offered by the game and ranks the best
  choice for the active character and build.
- Supports one-step Undo for run changes, a compact icon-focused layout, and a
  pinned ball evolution or passive artifact target.
- Hides encyclopedia navigation during active runs and keeps recommendations in
  a collapsible mobile tray at the bottom of the screen.
- Detects ball evolutions when every recipe component is level 3.
- Detects passive artifacts as soon as all required components are held.
- Applies a ready evolution from the recommendation panel, consumes its
  ingredients, and adds the result at level 1.
- Re-scores ball and passive suggestions whenever the loadout changes.
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
- `sprite-manifest.txt` — expected image names and paths.
- `GAME_INFO.txt` — plain-text game explanation, tracker model, and recipe
  quick reference.

## Data status

The encyclopedia foundation is current through the **Shadow Update (April 27,
2026)**. The supplied systems brief adds strategy profiles for the Hoary
Hoarder and Ballbearer. The wider Naturalist Update data set has not been fully
audited, so community corrections are welcome.

Recommendations are practical heuristics, not a claim of a solved optimal
meta. Character rules act as hard filters where appropriate; recipe proximity,
current loadout, conditional loot requirements, and an optional pinned target
then contribute to the ranking.

## Visit analytics

Pit Crew does not ship with analytics. GitHub's repository
[**Insights → Traffic**](https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository)
page reports visits to the repository itself, not reliable page-view analytics
for the deployed site.

To track the live GitHub Pages site, create an account with an analytics
provider and place its generated script in `index.html`:

- [Cloudflare Web Analytics](https://developers.cloudflare.com/web-analytics/get-started/)
  provides a lightweight site beacon. Use its manual setup and place the
  generated script immediately before `</body>`.
- [Google Analytics](https://support.google.com/analytics/answer/9304153)
  provides realtime, acquisition, geography, and event reports. Create a GA4
  web data stream and place its Google tag immediately after `<head>`.

After adding either provider, commit and push the changed `index.html`. Review
the provider's privacy and consent requirements for the locations where the
site is offered.

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
