# Handoff: FUNunciation marketing site (landing + Our Story)

## Overview
A small public marketing site for FUNunciation, the iPad articulation-therapy app. Two pages:
1. **Home** (landing): sells the app to SLPs (primary) and parents (secondary). Ends in an App Store call to action at **$49.99 one-time, no subscription**.
2. **Our Story**: Taylor Nizich's founding story, copy supplied by the owner (use it **verbatim**).

There is a desktop design (1280 content width) and a mobile design (390 wide) for Home. Our Story is fluid (built with `clamp()` / `auto-fit` grids) but should get the same mobile treatment as Home.

This is a separate web project. It is **not** part of the iPad app (`speech-therapy-app/`), and it must not add network calls, accounts or analytics to the app.

## About the design files
The files in `prototype/` are **design references built in HTML**, not production code. Recreate them in whatever stack the site uses. With no existing site, a static build (Astro, Next static export or plain HTML/CSS) is enough: there is no backend and no state beyond the mobile menu. The `.dc.html` files open directly in a browser (they load `support.js` next to them). Inline styles in the prototypes are the source of truth for every value below.

## Fidelity
**High-fidelity.** Final colours, type, spacing, copy and assets. Recreate pixel-accurately.

## Global

### Fonts (Google Fonts)
- **Grandstander** 700 / 800 / 900: every heading, the price, CTA labels.
- **Nunito** 500–900: body, nav, eyebrows, captions. (The app uses SF Pro Rounded; Nunito is the web stand-in.)

### Colours (from the app's design system, `docs/styling-guide.md`)
| Token | Hex | Use |
|---|---|---|
| blushField | `#FBF2EE` | Page background |
| creamSurface | `#FFF9F4` | Bands, panels, price box |
| inkNavy | `#1F3247` | All text, outlines, iPad bezel |
| inkNavy2 | `#4A5B70` | Body copy, nav links, eyebrows |
| story body ink | `#3A4B60` | Long-form paragraphs on Our Story |
| lineHairline | `#EBD9CF` | Band top/bottom borders (1.5px) |
| line | `#E3CDC1` | Mobile menu borders |
| lineDivider | `#F0E2DA` | Mobile menu row dividers |
| cardShadow | `#F2C3BA` | Solid offset shadows (no blur) |
| accentStart | `#E2786B` | **CTA button only** |
| accentStartEdge | `#B9584C` | CTA's 6px solid bottom edge |
| lavenderTint / lavenderInk | `#F1ECF6` / `#574A7E` | Privacy band |
| peachPanel | `#F6E6DC` | Our Story photo placeholder stripes |
| slatePale | `#DCE5EE` | Our Story photo placeholder stripes |
| Mark chips | see below | Progress-tracking illustration |

Text is never black, backgrounds never white (except behind screenshots), and coral is used only on the App Store button.

### Common components
- **Eyebrow**: Nunito 900, 13px (12 on mobile), uppercase, letter-spacing .18em, `#4A5B70`.
- **CTA button "Download on the App Store →"**: pill (radius 999), bg `#E2786B`, `box-shadow: 0 6px 0 #B9584C`, Grandstander 900, 24px desktop hero / 22px elsewhere / 21px mobile hero / 19px mobile price box, padding 20×34 (hero) or 18×30, navy label, `transform: rotate(-1deg)`, `white-space: nowrap`. It links to the App Store listing (URL TBD). Use plain text, not Apple's badge, unless the owner later supplies the official badge.
- **Screenshot tile**: 3px navy border, radius 24 (20 mobile), `box-shadow: 8px 8px 0 #F2C3BA` (6px on mobile), image `aspect-ratio: 4/3; object-fit: cover`.
- **iPad frame** (hero): navy `#1F3247` box, radius 40, padding 16, image radius 26 inside, `rotate(1.5deg)`, `box-shadow: 14px 14px 0 #F2C3BA`. Mobile: radius 26, padding 9, image radius 18, shadow 8px.
- Headings that lean: hero H1 and the closing H2 use `rotate(-1.5deg)` (H1 with `transform-origin: left`).

### Header (both pages)
- Desktop: flex, space-between, padding 28px 64px. Left: logo `landing/logo.png`, **height 72px**, links to Home (no "Home" label). Right: **Our Story · Privacy · Contact**, Nunito 700 17px, `#4A5B70`, gap 36px. On Our Story, "Our Story" is navy 800 with a 2px navy underline (padding-bottom 2px) to mark the current page.
- Mobile: padding 18px 20px, logo 44px high on the left; a 48px cream circle menu button (1.5px `#E3CDC1` border, three 20×2.5 navy bars, gap 5) on the right. Tapping it toggles a dropdown card under the header: margin 0 20px 8px, cream, radius 24, rows Nunito 800 18px, padding 14px 0, dividers `#F0E2DA`.
- There is **no footer** on any page; Privacy and Contact live in the header only.
- Privacy and Contact pages don't exist yet. Link them to placeholders.

## Screen 1: Home, desktop (`FUNunciation Home.dc.html`)
Content max-width 1280, centred, page bg `#FBF2EE`. Sections top to bottom:

1. **Header** (above).
2. **Hero**: 2-col grid `minmax(0,1fr) minmax(0,1.15fr)`, gap 56, align center, padding 56px 64px 96px.
   - Left column, flex column gap 28: eyebrow "Articulation practice for iPad"; H1 "Who says working on speech goals can't be fun?" (Grandstander 800, 64px, line-height 1.04, letter-spacing −.01em, rotate −1.5°, `text-wrap: pretty`); paragraph "Pick a sound, pick a game, press Start. FUNunciation brings the words and the pictures, and gives the child a reason to say the next one." (Nunito 600, 21px/1.5, `#4A5B70`, max-width 480); a wrapping row (gap 20×24, margin-top 8) holding the CTA and "$49.99 once.<br>No subscription." (Nunito 700, 16px, `#4A5B70`).
   - Right column: iPad frame with `games/food-truck.png`.
3. **How a session works**: cream band, 1.5px `#EBD9CF` top and bottom borders, padding 88px 64px. Eyebrow "How a session works" (margin-bottom 14), H2 "Three steps, again and again." (Grandstander 800, 52px, line-height 1.05, margin-bottom 56). 3-col grid, gap 32; each column is flex column gap 18: screenshot tile, title (Grandstander 800, 28px), body (Nunito 600, 18px/1.5, `#4A5B70`).
   - `setup.png` (object-position top left) / "1 · You pick the sound" / "Choose the sound, the positions and a game. It takes seconds, even with a child already in the chair."
   - `games/firefly.png` / "2 · The child says the word" / "A picture and a word card come up. You judge the production. The app never grades speech and never moves on without you."
   - `games/dress.png` / "3 · Every try earns something" / "One quick tap, flick or drag. Some tries land, some miss in a silly way, and the child keeps something every time."
4. **Progress tracking**: 2-col grid 1fr/1fr, gap 72, padding 104px 64px.
   - Left: eyebrow "Progress tracking"; H2 "Scores the child never sees." (52px); body "Mark each try with one tap, or fill in the report from memory after the round. Results live on your setup screen, never on the game. No red, no green, no failing grade." (19px/1.55, max-width 480).
   - Right: cream panel, 1.5px `#EBD9CF` border, radius 32, padding 40, gap 20. Row 1: three chips (flex 1, radius 18, padding 20px 0, centred, 30px glyph above a Nunito 900 15px label, letter-spacing .08em): ✓ CORRECT (bg `#EEF5EA`, border `#CFE0C8`, ink `#3E5A39`), ≈ CLOSE (`#FDF5E1` / `#F1DFB2` / `#6A4E12`), − INCORRECT (`#FCEDEB` / `#F1CFCA` / `#8A3A3A`). Row 2: "You got it" (green set), "You're close" (butter set), "Try again" (`#EBF3FA` / `#C9DCEB` / `#2D5676`), Nunito 800 17px, padding 16px 0. Caption "Clinical or child-friendly marks. Marking is off until you turn it on." (15px, `#4A5B70`). These colours match the app's mark tokens; keep them.
5. **Privacy band**: margin 0 64px, bg `#F1ECF6`, radius 32, padding 56, grid `1fr 1.3fr`, gap 48. H2 "Everything stays on this iPad." (Grandstander 800, 44px/1.08). A 2×2 grid (gap 18×32, Nunito 700 18px, `#574A7E`): "No accounts or sign-in", "Works with no internet", "No ads, no tracking", "Clients saved by nickname or initials".
6. **Closing CTA**:
   - Headline block: padding-top 96, centred H2 "Ready for the next round?" (Grandstander 800, 56px/1.04, rotate −1.5°).
   - Scatter area: `position: relative; overflow: hidden; padding: 120px 64px; max-width: 1280`. Four absolutely positioned screenshots (3px navy border, radius 22, **no shadow**), painted *behind* the price box:
     - `basketball.png`: left 70, top 70, width 280, rotate −7°
     - `firefly.png`: right 70, top 90, width 280, rotate 6°
     - `photo-booth.png`: left 150, bottom 60, width 260, rotate 5°
     - `dress.png`: right 150, bottom 50, width 260, rotate −5°
   - Price box (`position: relative`, so it sits on top): width 622 total (`box-sizing: border-box`, max-width 100%), centred, cream `#FFF9F4`, 3px navy border, radius 36, padding 52px 48px, **no shadow**, centred column, gap 16. "$49.99" (Grandstander 900, 80px, line-height 1); "Once. No subscription." (Nunito 800, 19px, `#4A5B70`); CTA button (margin-top 14).

## Screen 2: Home, mobile (`FUNunciation Home Mobile.dc.html`, 390 wide)
Same content and order, single column, 20px side padding.
- Hero: padding 28px 20px 64px, gap 22. Eyebrow; H1 42px/1.06; paragraph 18px; iPad frame (margin 10px 6px 10px 0); **full-width** CTA (text centred, padding 18px 0, 21px) with "$49.99 once. No subscription." centred below (15px).
- How a session works: padding 56px 20px, gap 40. H2 34px. Each step is a column, gap 14, in this order: **title (24px), then summary (17px), then screenshot**.
- Progress tracking: padding 64px 20px. H2 34px, body 17px. Chip panel padding 20, radius 26; chips gap 8, glyph 24px, label 11px; second row 14px.
- Privacy: margin 0 20px, radius 28, padding 32px 24px; H2 30px; the four items stacked (gap 12, 17px).
- Closing CTA: headline padding 72px 20px 0, 36px. Scatter area padding 100px 20px 110px; screenshots radius 16: basketball left −10 top 20 w160 −7°; firefly right −10 top 34 w160 6°; photo-booth left 10 bottom 24 w150 5°; dress right 10 bottom 18 w150 −5°. Price box full width, radius 30, padding 36px 20px, "$49.99" 64px, line 17px, CTA 19px with padding 16×24.

Breakpoint: switch to the mobile layout below ~768px. Between 768 and 1280, keep the desktop structure and let grids shrink (`minmax(0,1fr)`). At the narrower desktop widths, scale the closing scatter down, or drop the bottom two screenshots, so none of them crowds the headline.

## Screen 3: Our Story (`FUNunciation Our Story.dc.html`)
Fluid page, side padding `clamp(24px,5vw,64px)`, wide blocks max-width 1152, text columns max-width 680. **All copy is verbatim from the owner. Do not edit it.** (The final line says "Welcome to Say Then Play." It may be an older product name; check with the owner before launch.)
1. Header (Our Story active).
2. Intro: `auto-fit minmax(min(100%,420px),1fr)` grid, gap 56. Eyebrow "Our Story"; H1 "Because “One More Time!” Should Be a Good Thing." (Grandstander 800, `clamp(44px,6vw,68px)`, rotate −1.5°). Right: photo placeholder, 4:5 (max-height 520), 3px navy border, radius 36, `10px 10px 0 #F2C3BA` shadow, label "photo: Taylor at work". **Needs a real photo.**
3. Cream band (hairline top and bottom), 680 column, padding 88px 24px, paragraphs Nunito 600 20px/1.65 `#3A4B60`, gap 24. Four paragraphs, then "Sounds like a win-win, right?" as Grandstander 800 28px navy.
4. Two-column block: photo placeholder 4:3, rotate −1°, "photo: Taylor and Jake" (**needs a real photo**), beside H2 "Enter Jake (and a Slightly Ambitious Idea)" (`clamp(34px,4vw,44px)`), three paragraphs, then "And so, Fununciation was born." (Grandstander 28px).
5. Cream band: H2 "Less “Let's Do These Cards Again.” More “Can We Play That Again?”" and four paragraphs.
6. Pull quote: centred, max-width 1000, padding 104: "We'll take “Can we play that again?” over “Do we have to do more cards?” any day." (Grandstander 800, `clamp(34px,4.6vw,52px)`, rotate −1.5°, `text-wrap: balance`).
7. Lavender band `#F1ECF6`: H2 "Speech Goals. Game On.", three paragraphs, then the closing line in Grandstander 28px.
8. The same closing CTA as Home.

## Interactions & behaviour
- Logo goes to Home; Our Story goes to the story page; Privacy and Contact are placeholders for now.
- App Store button goes to the App Store listing (URL TBD).
- Mobile menu: tap to toggle open/closed. No animation in the prototype; if you add one, keep it at ≤200ms ease-out with no bounce, per the app's therapist-register motion rule.
- Link colours: navy `#1F3247`, hover dusty rose `#8E4552`. Nav links have no underline.
- No auto-playing media and no carousels.

## State
Only `menuOpen: boolean` (mobile header).

## Assets (`prototype/landing/`)
- `logo.png`: FUNunciation wordmark (from the app's `brand-fununciation@2x.png`). Get a vector or higher-resolution master from the app repo (`tools/brand/build_logo.py`).
- `setup.png`: setup screen, cropped from the Basketball handoff screenshot.
- `games/*.png`: game screenshots cropped from the design handoffs (Food Truck, Firefly Pond, Dress the Guests, Basketball, Photo Booth; others unused here). They are about 700px wide, from prototype captures. **Replace them with real high-resolution iPad screenshots before launch.**
- `words/*.svg`: word pictures (not used on these pages; included for future use).
- Photos of Taylor, and of Taylor with Jake, are still needed.

## Content rules
- Don't name competitors.
- Don't claim "no in-app purchases" (paid games may come later). "No subscription" is fine.
- The site is for SLPs first. There is no parents section on Home.

## Files
- `prototype/FUNunciation Home.dc.html`: Home, desktop
- `prototype/FUNunciation Home Mobile.dc.html`: Home, mobile
- `prototype/FUNunciation Our Story.dc.html`: Our Story
- `prototype/support.js`: runtime that lets the `.dc.html` files open in a browser (reference only)
- `prototype/landing/`: assets
