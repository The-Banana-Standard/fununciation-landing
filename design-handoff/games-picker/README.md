# Handoff: Games section, "picker list" redesign

## Overview
This replaces the games carousel on Home (`src/components/GameCarousel.astro`, used in `src/pages/index.astro` under "The games"). The carousel has arrows and 13 dots. The new design puts a named list of all 13 games next to one large clip of the selected game. Selecting a row swaps the clip.

The section heading ("The games" / "13 games, one routine." / body copy) and the `games` array in `index.astro` stay as they are.

## About the design files
`Games Section Options.dc.html` is a design reference built in HTML. It is not production code. Rebuild it in the existing Astro site: plain Astro component, scoped `<style>`, a small vanilla `<script>`, the tokens in `src/styles/global.css`. Don't add a client framework.

The file is an exploration canvas. Only these options were chosen:
- **3a**: desktop (1100px and up)
- **4a**: tablet (768–1099px)
- **4b**: mobile (below 768px)

Ignore the others (1a–1c, 2a–2c, 3b, 3c).

## Fidelity
High-fidelity. Every color, size and radius comes from the existing site tokens and the current `GameCarousel` / `LoopVideo` styles. Match the values below exactly.

## Media
The prototype shows still images. In production, keep using `LoopVideo` for the stage (desktop and tablet) and for the opened row on mobile. Keep its poster, the 60%-visible autoplay, the pause button, `group="games"` and reduced-motion behavior. Only one clip is mounted or visible at a time.

---

## Desktop (3a), 1100px and up

**Section**: unchanged (`.games`, padding `96px var(--gutter) 0`, head `margin-bottom: 48px`).

**Layout**: `display:grid; grid-template-columns: minmax(0,1fr) minmax(0,1.75fr); gap:48px; align-items:start`. List on the left, stage on the right.

**List** (left column): `flex-direction: column; gap: 4px`. One `<button>` per game.
- Inactive row: padding `9px 16px`, background transparent, radius `14px`, text `--ink-navy`.
  - Number: Nunito 900, 12px, letter-spacing .12em, `--ink-navy-2`, fixed width 22px, format `01`–`13`.
  - Name: Grandstander 800, 19px.
  - Number and name: `display:flex; align-items:baseline; gap:14px`.
- Active row: padding `16px 16px 18px`, background `--ink-navy` (#1F3247), text `--cream-surface` (#FFF9F4). Number color `--line-divider` (#F0E2DA). Name 26px.
  - Below the name, the game's `how` line: Nunito 600, 16px, line-height 1.45, color #F0E2DA, `padding-left: 36px` (lines up with the name).
- Row stack: `flex-direction:column; gap:4px; text-align:left`.

**Stage** (right column): `position: sticky; top: 40px`, wrapper padding `0 10px 10px 0` (room for the shadow).
- Frame: `aspect-ratio: 4/3; border: 3px solid var(--ink-navy); border-radius: 28px; box-shadow: 10px 10px 0 var(--card-shadow); background:#fff; overflow:hidden`. Same as the current `.slide-media`.

## Tablet (4a), 768–1099px

Section padding 80px top, `--gutter` sides. Head gap 12px, margin-bottom 40px. Title 42px. Body 18px.

**Layout**: `grid-template-columns: minmax(0,1fr) minmax(0,1.45fr); gap:28px; align-items:stretch`.

**The list scrolls inside itself and never gets taller than the stage.**
- The list column is `position:relative; min-height:0`. Inside it, the scroller is `position:absolute; inset:0 0 8px 0; overflow-y:auto` (the 8px matches the stage's shadow padding), so the stage's height sets the column height.
- Scroller: `display:flex; flex-direction:column; gap:2px; padding:6px 6px 6px 0; border-top:1.5px solid var(--line); border-bottom:1.5px solid var(--line); scrollbar-width:thin; scrollbar-color: var(--line) transparent`.
- When the active row changes, scroll it into view inside the scroller only. Use `scroller.scrollTo({ top: row.offsetTop - …, behavior })`, not `scrollIntoView`, so the page doesn't jump.

Rows:
- Inactive: padding `7px 12px`, radius 12px. Number 11px, width 18px. Name 16px. Gap 10px.
- Active: padding `12px 12px 14px`, navy background, name 21px, `how` 14px with `padding-left:28px`.

**Stage**: wrapper padding `0 8px 8px 0`, not sticky. Frame border 3px, radius 22px, shadow `8px 8px 0 var(--card-shadow)`.

## Mobile (4b), below 768px

Section `64px 20px 0`. Head gap 10px, margin-bottom 32px. Eyebrow 12px. Title 34px / 1.08. Body 17px. These are the existing mobile values.

**Accordion**, one column, `gap:4px`. No separate stage.
- Each item is a wrapper with `border-radius:16px` and a background (transparent, or navy when open).
- Header button: `min-height:48px; padding:0 14px; display:flex; align-items:center; gap:12px`.
  - Number 11px, width 18px. Name Grandstander 800, 17px (21px when open), `flex:1`. Marker on the right: Grandstander 900, 18px, `+` when closed, `−` when open.
- Open body: padding `0 14px 16px`, `flex-direction:column; gap:12px`.
  - `how` line: 15px / 1.45, color #F0E2DA, `padding-left:30px`.
  - Clip frame: `aspect-ratio:4/3; border:2px solid var(--cream-surface); border-radius:14px; overflow:hidden`.
- Basketball starts open. Tapping the open item closes it, so none are open. Tapping another item opens it and closes the previous one (one open at a time).

---

## Interactions and behavior
- **Select**: click or tap a row to make it active. On desktop and tablet one row is always active; the default is index 0 (Basketball).
- **Hover** (inactive rows, desktop/tablet): optional background `--cream-surface`.
- **Keyboard**: the rows are real `<button>`s. Add arrow-key handling on the list: ArrowUp/ArrowDown moves the active row and focus, and Home/End jump to the first and last game. Keep the global `:focus-visible` outline.
- **Accessibility**: mark it up as a listbox (`role="listbox"` with `role="option"` + `aria-selected`) or as tabs (`role="tablist"`/`tab` + `aria-controls` the stage, `role="tabpanel"`). On mobile use disclosure buttons with `aria-expanded` + `aria-controls`. The clip's alt is `"{name}, one of the games"`, as today.
- **Motion**: 150ms ease-out on background and color only. No size animation and no bounce (site rule: 200ms or less). With `prefers-reduced-motion`, transitions are off (already global).
- **Clip swap**: when the active game changes, swap the `LoopVideo` src and poster, or show/hide 13 pre-rendered `LoopVideo`s with only the active one visible. Videos are `preload="none"`, so hidden ones don't download.

## State
- `activeIndex` (0–12), default 0.
- Mobile: `openIndex` (−1 to 12), default 0.
- No data fetching. Data is the existing `games` array (`id`, `name`, `how`, plus `poster` from `captures/games/<id>.jpg` and the clip at `/media/games/<id>.mp4`).

## Design tokens (from `global.css`)
- `--blush-field` #FBF2EE: section background
- `--cream-surface` #FFF9F4: active text, hover row, mobile clip border
- `--ink-navy` #1F3247: active row background, names, stage border
- `--ink-navy-2` #4A5B70: inactive numbers, body copy
- `--line` #E3CDC1: tablet scroller rules, scrollbar
- `--line-divider` #F0E2DA: numbers and `how` text on the navy row
- `--card-shadow` #F2C3BA: stage offset shadow
- Fonts: `--font-display` (Grandstander) for names and title, `--font-body` (Nunito) for everything else
- Radii: stage 28 / 22 / 14px (desktop / tablet / mobile). Rows 14 / 12 / 16px.
- Shadows: `10px 10px 0` / `8px 8px 0` of `--card-shadow`. None on mobile.

Navy on blush and cream on navy both pass AA contrast. #F0E2DA on #1F3247 is about 11:1.

## Assets
- Stills: `src/assets/captures/games/<id>.jpg` (already in the repo; the copies in `games/` are for the prototype only)
- Clips: `public/media/games/<id>.mp4` (already in the repo)
- No new icons. The `+`/`−` markers are text glyphs.

## Files
- `Games Section Options.dc.html`: the prototype. See options 3a, 4a and 4b. Serve this folder (e.g. `python3 -m http.server`) and open it.
- `support.js`: the prototype runtime, needed only to view the file.
- `games/*.jpg`: stills the prototype uses.
- To change in the repo: `src/components/GameCarousel.astro` (replace or rename, e.g. `GamePicker.astro`), the usage in `src/pages/index.astro`. `LoopVideo.astro` is reused unchanged.
