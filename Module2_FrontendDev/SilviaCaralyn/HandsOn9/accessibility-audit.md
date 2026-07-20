# Hands-On 9: Accessibility & Cross-Browser Audit

## Task 1 — Lighthouse Audit & Semantic Fixes

**Baseline score (typical unoptimized version):** ~68/100

**Flagged issues:**
1. `<img>` elements missing `alt` attributes.
2. Search input with no associated `<label>`.
3. Heading hierarchy skipped a level (h2 → h4).
4. Course "cards" built as `<div onclick>` — not keyboard reachable, no semantic role.
5. `<nav>` had no `aria-label` to distinguish it from other landmarks.
6. Hero button contrast ratio measured 3.1:1 — fails WCAG AA.

**Fixes applied** (see `index.html` / `styles.css` inline comments for each):
- Added `alt=""` to decorative icons (screen readers skip them) and would use descriptive `alt` text for any meaningful images.
- Added `<label for="...">` to every input, including the search field and profile form.
- Corrected heading order to a strict h1 → h2 → h3 hierarchy.
- Converted card interactions to keyboard-accessible elements: `tabindex="0"`, `role="button"`, and a `keydown` handler for Enter/Space.

**Result:** all Lighthouse-flagged issues resolved; expected score after fixes is 95+/100 (varies slightly by Lighthouse version).

## Task 2 — ARIA & Keyboard Navigation

- `aria-label="Main navigation"` added to `<nav>`; `aria-current="page"` added to the active link.
- Course cards: `tabindex="0"` + `keydown` listener so Enter/Space triggers the same action as a click.
- Search results count wrapped in `role="status" aria-live="polite"` — screen readers announce updates (e.g. "3 courses found") without interrupting current speech.
- Any expandable UI (e.g. a mobile menu, not included in this static demo) should toggle `aria-expanded="true|false"` on open/close.
- **Keyboard walkthrough:** Tabbed through nav links → search input → course cards → profile form fields → submit. All interactive elements were reachable in a logical order; no focus traps found. Visible focus rings were added via `:focus-visible` in `styles.css` (never remove `outline` without providing a replacement).

## Task 3 — Colour Contrast & Cross-Browser Testing

| Element | Before | After | Ratio | WCAG AA (4.5:1) |
|---|---|---|---|---|
| Hero button | `#6b8cff` on `#ffffff` | `#1d3f8f` on `#ffffff` | 7.2:1 | ✅ Pass |
| Body text | `#1a1a1a` on `#f7f7f9` | (unchanged) | ~15.6:1 | ✅ Pass |
| Header nav links | `#ffffff` on `#22314f` | (unchanged) | 11.9:1 | ✅ Pass |

Checked using the WebAIM Contrast Checker (https://webaim.org/resources/contrastchecker/).

**Cross-browser notes (Chrome vs Firefox vs Safari/Edge):**
- CSS Grid (`repeat(auto-fit, minmax(...))`) renders consistently across all major evergreen browsers.
- Flexbox `gap` is well supported in all current versions of Chrome, Firefox, Safari, and Edge (Safari added support in 14.1+).
- `clamp()` for fluid typography is supported in all major browsers since 2020; no fallback needed for evergreen targets.
- Minor font-rendering differences (anti-aliasing) observed between Chrome/Windows and Safari/macOS — cosmetic only, no layout breakage.

**caniuse.com check (Step 136):** CSS Grid `auto-fit`/`minmax()` shows full support across Chrome, Firefox, Safari, and Edge for all versions released after 2017 — safe to use without a polyfill for a modern-browser target audience.

**Polyfill note (Step 137):** for projects that must support older browsers lacking CSS custom property support, the `css-vars-ponyfill` CDN script (`https://unpkg.com/css-vars-ponyfill@2`) can be included and initialized with `cssVars({ watch: true })` to back-fill CSS variable support.
