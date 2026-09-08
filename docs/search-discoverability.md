# Search discoverability audit and publishing runbook

Audited September 8, 2026. Implementation is local; this report does not claim
that the changes are deployed, submitted, indexed, or selected by an AI service.

## Existing production evidence

Production: https://yjay18.github.io/ballxpit-run-tracker/

The GitHub Pages API returned: public, HTTPS enforced, no custom domain,
`build_type: legacy`, source `main` at `/`, status `built`. Response headers
identify GitHub.com and Fastly. The Cloudflare script in the HTML is Web Analytics;
it is not evidence of a Cloudflare proxy or firewall configuration.

| Surface | Observed before changes |
| --- | --- |
| Homepage | HTTP 200, HTML, title `Pit Crew`, basic description and Open Graph title/description/type |
| Canonical, JSON-LD, Twitter card, verification tags | Absent |
| Origin `/robots.txt` | HTTP 404 |
| Project `/robots.txt`, `/sitemap.xml` | HTTP 404 |
| Unknown project URL | HTTP 404, not an app-shell soft 404 |
| Googlebot, bingbot, OAI-SearchBot, Claude-SearchBot, PerplexityBot user-agent probes | Homepage HTTP 200, 224899 bytes each, no X-Robots-Tag |
| HTML content | Hero explanation and credits are static; encyclopedia rows and tracking use JavaScript |
| Private routes | None in this repository; run state is browser-local, not a public user URL |

These are ordinary requests with crawler user-agent strings from this workstation.
They do not verify real crawler IP access, search engine rendering, or CDN internal
bot classification. No site firewall rules are checked into this repository.
No hosting/firewall restrictions were changed.

## Implemented

- Standard-library static build to `dist/`, preserving the tracker styling and application script.
- Two indexable canonical pages: the homepage and `guide.html`. Existing app tabs
  are UI states, not separate pages. No invented tab URLs or fragment sitemap entries.
- Unique titles/descriptions, absolute canonical URLs, Open Graph and Twitter
  metadata using the existing PNG logo (summary card, not a fabricated hero image).
- `WebSite` and `WebPage` JSON-LD matching public page descriptions. No prices,
  ratings, reviews, supported operating systems, or rich-result promises.
- Static visible guide and footer links available in the original HTML response.
  Guide and `llms.txt` share `content/site.json`; update that source when features change.
  The full interactive encyclopedia still requires JavaScript.
- Automatic sitemap from an explicit public route registry during every build.
  `lastmod` uses the latest Git commit affecting a page's inputs. Dirty or untracked
  inputs omit it. No build-time timestamps, priorities, or change-frequency claims.
  Full Git history is fetched in CI. A rebuild without content changes retains dates.
- Generated `robots.txt` with explicit search/retrieval agent groups. Deployment
  at the origin root is still required (see below).
- Experimental `llms.txt`, not a standard indexing requirement or access policy.
- Optional Google/Bing verification tokens and an opt-in IndexNow key file.
- `404.html` with noindex. Preview builds give every HTML page noindex, omit
  canonical/schema/verification tags, omit llms.txt, and emit an empty sitemap.
- An allowlisted publishing directory excludes source docs, scripts, and repository
  metadata. CI checks previews but does not publish PR previews.

## Activate publishing

The current hosting source must change before this generated build is published.
Do not push only the changed source homepage under the legacy publishing mode:
its new guide links rely on the generated artifact.

1. In this repository's Settings → Pages, change Source to **GitHub Actions**.
2. Review and merge/push the changes to `main`. The included workflow builds,
   checks, and deploys only `dist/`. It uses the GitHub Pages environment and does
   not deploy pull requests. Workflow dispatch is also available on `main`.
3. Confirm the deployment succeeded, then run `python3 scripts/check_search.py --production`.
4. Verify the canonical base in `content/site.json` before a domain migration.
   Generate again and redirect the old host/paths using hosting controls.

No repository setting, push, or deployment was performed during this task.
Custom workflow setup: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

## Origin-root crawler policy and training choice

Crawlers read **https://yjay18.github.io/robots.txt**, not the project copy at
`/ballxpit-run-tracker/robots.txt`. The origin currently returns 404 (no crawl
restriction). The generated file is a reviewable policy ready for installation
in the `yjay18.github.io` root-site repository, or at the root of a dedicated
custom domain. Merge it with any existing root policy instead of overwriting
rules for other projects. This project cannot independently install it there.

`OAI-SearchBot`, `Claude-SearchBot`, and `PerplexityBot` are search crawlers.
The user-directed fetch agents are listed separately. **Training permissions
remain as they were: unrestricted.** GPTBot, ClaudeBot, and Google-Extended are
not treated as search crawlers; an owner can adopt separate disallow rules for
those tokens. Do not silently introduce a training opt-in or opt-out while
changing search visibility. Review each provider's current token semantics.

- OpenAI: https://developers.openai.com/api/docs/bots
- Anthropic: https://support.anthropic.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler
- Perplexity: https://docs.perplexity.ai/docs/resources/perplexity-crawlers
- Google crawler controls: https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers
- Robots scope and limitations: https://developers.google.com/search/docs/crawling-indexing/robots/intro

If a CDN/WAF/custom domain is introduced, inspect bot rules, rate limits, managed
challenges, country/IP restrictions, and authentication. Permit verified search
bots using providers' documented IP verification where available; a spoofable
user-agent alone is not an authentication mechanism. Confirm with access logs
and Search Console/Bing live inspection. Do not disable the whole firewall.

## Private, utility, staging, and preview boundaries

There are no server-side accounts or private pages to protect in this app.
LocalStorage data is not published in sitemap URLs or guide content. Never put
saved run data or user identifiers into public canonical links.

For a review build use `python3 scripts/build_search.py --preview` and
`python3 scripts/check_search.py --preview`. Noindex pages must remain crawlable
for the directive to be observed. Robots.txt is not access control. Sensitive
previews must use hosting authentication returning 401/403 before serving content;
this repository's public GitHub Pages hosting is not such an authentication layer.
Do not publish secrets or sensitive previews there. No staging host was found
or modified. An unknown URL must continue to return HTTP 404.

## Google Search Console and Bing Webmaster Tools

1. Add the URL-prefix property `https://yjay18.github.io/ballxpit-run-tracker/`
   in Google Search Console. A DNS Domain property for github.io is not yours
   to verify. Select HTML meta-tag verification and copy the actual token.
2. Add repository Actions variable `GOOGLE_SITE_VERIFICATION` with the token
   value only. For Bing, set `BING_SITE_VERIFICATION` from its HTML meta-tag
   method, or use Bing's Search Console import when available.
3. Rebuild/deploy, check the public page source contains the supplied tokens,
   then complete verification in the respective account. Do not remove tokens
   after verification. No fake or placeholder tags are emitted when unset.
4. Submit `https://yjay18.github.io/ballxpit-run-tracker/sitemap.xml` through
   each console's Sitemaps interface. Do not use retired Google sitemap ping URLs.
5. Inspect the homepage and guide using live URL inspection. Request indexing
   if appropriate. Recheck reported canonical selection, crawl/index status, and
   coverage later; sitemap acceptance is not indexing confirmation.

Sitemap guidance: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
Bing sitemaps: https://www.bing.com/webmasters/help/sitemaps-3b5cf6ed

No verification tokens were available, no account was created/verified, and no
sitemap or indexing request was submitted during this task.

## Optional IndexNow

This is a small, infrequently changed site, so IndexNow is optional. The script
is explicit and never submits from CI, local builds, or previews.

Generate an 8–128 character alphanumeric/hyphen key and set repository variable
`INDEXNOW_KEY`; the production build publishes `<key>.txt`. Set the same environment
variable locally after deployment, then notify only genuinely changed URLs:

```sh
python3 scripts/indexnow.py 'https://yjay18.github.io/ballxpit-run-tracker/' 'https://yjay18.github.io/ballxpit-run-tracker/guide.html'
```

The script verifies production pages and the public key file first, uses
`keyLocation` for this subpath-hosted site, and rejects noncanonical/preview URLs.
A 200/202 receipt is not proof of indexing. It is not a Google submission route.
If a public route is removed later, extend the reviewed route list and deletion
handling explicitly; the current script only submits the two existing pages.
Protocol: https://www.indexnow.org/documentation

## Verification and limits

Run:

```sh
python3 scripts/build_search.py
python3 scripts/check_search.py
python3 scripts/build_search.py --preview
python3 scripts/check_search.py --preview
python3 scripts/build_search.py
python3 scripts/check_search.py --production
```

The production check intentionally fails against the old deployment until the
new guide and metadata are live. It checks status, MIME types, redirects,
canonical URLs, crawler directives, sitemap membership, linked anchors, static
content, JSON-LD syntax/content, social image response, crawler probes, and 404s.
An absent root robots file is reported as a separate installation action.
Local checks also ensure utility files and source directories are excluded.

Use https://validator.schema.org/ on the deployed homepage and guide for external
vocabulary validation, and Search Console's rendered HTML inspection for Google's
view. WebSite/WebPage markup does not imply eligibility for a special rich result.
No external structured-data validator or actual search crawler inspection has
been claimed as completed. llms.txt remains experimental: https://llmstxt.org/

No indexing or AI search placement is promised or confirmed.

### Results from this task

- Local production and preview checkers passed.
- Consecutive unchanged builds produced identical file hashes.
- Clean-file Git dates were available; untracked content correctly omitted lastmod.
- Test-only verification values survived HTML escaping; preview builds removed
  verification tags and the IndexNow key file. Final output contains no test tokens.
- Original application JavaScript and stylesheet contents are byte-for-byte
  unchanged; JavaScript syntax and `git diff --check` passed.
- Browser QA: homepage and guide inspected at desktop 1280px and mobile 390px;
  neither had document horizontal overflow. Guide navigation and the existing
  Start a run → character picker flow worked. No warning/error console entries
  were captured during those checks. The guide contains no executable JavaScript.
- Final production checker failed on HTTP 404 for the not-yet-deployed guide.
  This is expected evidence of pending deployment, not a production pass.
