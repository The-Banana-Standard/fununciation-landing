# FUNunciation marketing site

Public marketing site for FUNunciation, the iPad articulation-therapy app. Three pages:

- `/`: Home. Sells the app to SLPs and ends in the App Store call to action ($49.99 once, no subscription).
- `/our-story/`: Taylor Nizich's founding story. **The copy is verbatim from the owner; don't edit it.**
- `/contact/`: contact form. **Not connected yet**: until `CONTACT_FORM_ACTION` is set, submitting shows the thank-you state and sends nothing.

This project is separate from the iPad app (`../speech-therapy-app`). It adds no network calls, accounts or analytics to the app.

## Stack

[Astro](https://astro.build) 7, static output. No client framework. The only JavaScript is the mobile menu toggle in `SiteHeader.astro`, the contact form's thank-you state, the games picker (`GamePicker.astro`) and the clips' play-while-visible logic (`LoopVideo.astro`). Fonts (Grandstander and Nunito) are self-hosted from Fontsource, so the site makes no third-party requests.

```bash
npm install
npm run dev       # http://localhost:4321
npm run build     # writes static files to dist/
npm run preview   # serves dist/
```

`dist/` can be deployed to any static host (Netlify, Cloudflare Pages, GitHub Pages, S3).

## Deploy

Every push to `main` builds and deploys to GitHub Pages (`.github/workflows/deploy.yml`):
**https://the-banana-standard.github.io/fununciation-landing/**

The workflow reads the base path from Pages, so internal links go through `withBase()` in `src/paths.ts` rather than starting with `/`. Once a custom domain is set under Settings → Pages, the next deploy serves from the domain root with no code change. The preview pages are marked `noindex`; flip `ALLOW_SEARCH_INDEXING` in `src/config.ts` at launch.

## Where things live

| Path | What |
|---|---|
| `src/config.ts` | App Store and Privacy links, and where the contact form posts (all placeholders for now) |
| `src/styles/global.css` | Colour tokens from the app's design system, shared classes, mobile breakpoint |
| `src/layouts/Base.astro` | `<head>`, fonts, header |
| `src/components/SiteHeader.astro` | Logo, desktop nav, mobile menu |
| `src/components/AppStoreButton.astro` | The coral CTA (the only coral on the site) |
| `src/components/ClosingCta.astro` | "Ready for the next round?" + price box, shared by Home and Our Story |
| `src/components/StoryPhoto.astro` | Our Story photo frames; shows the striped placeholder until a photo is passed in |
| `src/assets/` | Logo and the design handoff's screenshots (optimised to WebP at build time); `words/` and unused games are kept for later |
| `src/assets/captures/` | Real stills from the app: every game (`games/<game id>.jpg`, each clip's first frame) and the History screen. See **Screenshots and clips** below |
| `public/media/` | The clips: `games/<game id>.mp4` (5 s each) and `history.mp4` |
| `src/components/GamePicker.astro` | The games: a numbered list beside one clip (desktop, tablet) or an accordion (phone). From the games picker handoff |
| `src/components/LoopVideo.astro` | A muted looping clip over its still: plays while 60% on screen, has a pause button, starts paused with reduced motion |
| `tools/screenshots/` | Scripts that make the stills and clips on the iPad simulator |
| `design-handoff/` | The Claude Design handoffs this was built from: the site (`prototype/`) and the games picker (`games-picker/`, options 3a, 4a and 4b). Prototypes are the source of truth for every value |

Breakpoints:

- **1100px and up**: the desktop design. At 1280px it matches the prototype to within 1px. Between 1100 and 1280 the grids shrink and headings scale down slightly.
- **768–1099px (tablet)**: the hero, progress and privacy blocks stack, because the hero button (416px, no wrap) and the CORRECT/CLOSE/INCORRECT chips no longer fit half-width columns. The three steps keep their grid.
- **Below 768px**: the mobile design.

The closing screenshots shrink with the viewport below 1280px so they stay tucked behind the price box.

To view the prototypes, serve `design-handoff/prototype/` (for example `python3 -m http.server --directory design-handoff/prototype`) and open the `.dc.html` files.

## Screenshots and clips

The games grid and the History section on Home use real captures from the app (iPad Pro 13-inch simulator, Debug build of `../speech-therapy-app`).

- **Games:** `bash tools/screenshots/capture_games.sh "<simulator name>"` opens each game through the app's DEBUG straight-to-game launch, with no client selected so nothing is saved, and writes `src/assets/captures/games/<game id>.jpg`. Add a new game to the script's list and to `games` in `src/pages/index.astro`.
- **Game clips:** `bash tools/screenshots/record_game.sh "<simulator>" <game id> <seed> <raw.mp4>` records a game with the app's DEBUG auto-demo, which plays one real attempt through the game's own touch handling about 1.5 s after it appears. Use the same seed as the still (11, 18, 25 … in the order of `capture_games.sh`) so the clip opens on the same word. `python3 -I tools/screenshots/make_clips.py <raw dir> public/media/games` then finds the moment each game appears, cuts 5 seconds, turns it upright and encodes it.
- **History:** `tools/screenshots/add_demo_client.py` adds a demo client, **Leo**, with ten sessions on K and G from Sep 22 to Oct 22. Quit the app and back up its `Application Support` folder first; the script's header has the steps. Then select Leo and open History. Remove Leo afterwards from History → Remove from this iPad → Delete client.
- **History clip:** `bash tools/screenshots/record_screen.sh "<simulator>" 45 <raw.mp4>` records while you tap Last 30 days, K · Initial, K · Final, then scroll down and back up. `tools/screenshots/make_history_clip.py` cuts the waits, draws a marker where each touch was (the simulator doesn't record touches) and crossfades the end into the start. Its tap times are from the current recording, so re-read them from a new one.

Copy on Home follows the app's own words: "trials", "time in app", "history". The app deliberately draws no trend line and never says a child is improving, so the site shouldn't either.

## Before launch

- [ ] Set `APP_STORE_URL` in `src/config.ts`. Swap in Apple's official badge only if the owner supplies it.
- [ ] Build the Privacy page and point `PRIVACY_URL` at it.
- [ ] Connect the contact form: set `CONTACT_FORM_ACTION` to a form endpoint (Formspree, Netlify Forms, a Worker). Until then, messages go nowhere even though the page says "Message sent". Confirm the note under the button ("We'll only use your email to reply to you.").
- [ ] Replace the design-handoff screenshots in `src/assets/` (`setup.png`, `games/*.png`, used in the hero, the three steps and the closing price box) with real captures like the ones in `src/assets/captures/`. The old `setup.png` shows earlier copy ("20 words a round", "Mark each word"). `srcset` is already wired, so larger files automatically get sharper 2× variants.
- [ ] Re-take the captures in `src/assets/captures/` from the release build, so they show the final app.
- [ ] Add the two Our Story photos: import them in `src/pages/our-story.astro` and pass `src={...}` to each `StoryPhoto`.
- [ ] Confirm the last line of Our Story with the owner. It says "Welcome to Say Then Play.", which may be an older product name.
- [ ] Get a vector or higher-resolution logo. The current `logo.png` is 789×211 (fine for 72px at 2×).
- [ ] Add a favicon and a social share image. Point the custom domain at GitHub Pages (Settings → Pages).
- [ ] Set `ALLOW_SEARCH_INDEXING` to `true` in `src/config.ts` so search engines can list the site.

## Content rules

- Don't name competitors.
- Don't claim "no in-app purchases" (paid games may come later). "No subscription" is fine.
- The site is for SLPs first. There is no parents section on Home.
- Text is never black, backgrounds are never white (except behind screenshots), and coral is only on the App Store button.
- Motion stays at 200ms or less, ease-out, no bounce.
