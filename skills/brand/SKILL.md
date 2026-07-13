---
name: brand
description: Use when building ANY standalone HTML, explainer, visualization, infographic, diagram, slide/poster, landing page, dashboard mockup, report, or static page/document — including harness-emitted HTML (architecture reports, evidence, dashboards). Applies THIS PROJECT'S brand design system (tokens, fonts, canonical components) so output is on-brand instead of generic. Ships with a default (Vinxi/Lepton) that you replace with your own tokens. Compose WITH the frontend-design skill for layout craft.
---

# Project brand system — for standalone HTML & visualizations

Any HTML artifact, explainer, infographic, chart, slide, static page, or harness report you
produce for this project **must** look like YOUR project's brand, not like generic AI output.
This skill carries the brand so you don't reinvent (or drift from) it. It is the design system
for **every HTML artifact the harness emits** — architecture reports, evidence pages,
dashboards — not one skill's private stylesheet.

> **This skill ships a DEFAULT brand — replace it.** Out of the box it carries the Vinxi/Lepton
> system (`assets/brand.css` plus the tokens/fonts/palette/geometry documented below). That is a
> worked example, not a mandate. The skill's real value is **"apply the project's brand
> consistently across every artifact."** Adopters SHOULD swap `assets/brand.css`, the fonts, the
> palette, and the token names here for their own brand. Everything below is the reference
> implementation you adapt — keep the *structure* (drop-in tokens, canonical components,
> anti-patterns) and change the *specifics*.

## How to use it (every time)

1. **Drop in the base tokens.** Copy `assets/brand.css` (in this skill dir) into a `<style>`
   block, or `@import` it. It defines the `:root` tokens, fonts, and the canonical components.
   The shipped default is vendored from the Vinxi/Lepton design system — if your project has its
   own brand, replace `assets/brand.css` with your tokens and components and keep using this
   skill to apply them.
2. **Load the fonts** (Google CDN, since self-hosted woff2 isn't available standalone). The
   default pairs Hanken Grotesk + Geist Mono — swap these for your brand's typefaces:
   ```html
   <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
   <link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700;800;900&family=Geist+Mono:wght@400;500;600&display=swap" rel="stylesheet">
   ```
3. **Also invoke `frontend-design`** for composition, hierarchy, and motion craft — this skill
   sets the *palette/voice*, frontend-design sets the *craft*. They compose.

## The non-negotiables (what makes it YOUR brand)

The output must look like your project's brand — **this repo's default is Vinxi/Lepton, documented
below; swap each of these for your own brand's equivalents.** The point is that *some* deliberate
brand governs every artifact, not that these particular values do.

- **Palette:** midnight `#1A2040` text on snow `#FBFDFF`; blue `#0066E3` is the single accent;
  semantic green/amber/red used sparingly. Never pure black/white. Tint neutrals toward midnight.
- **Type:** **Hanken Grotesk** (display + body, weights 400–900) paired with **Geist Mono** for
  labels, codes, numbers, metadata. Never Inter/Roboto/system defaults.
- **Geometry:** sharp. `border-radius: 0` by default; thin 1px borders in `--silver`/`--fog`;
  elevation is sparse and tinted (`--shadow-*`), not generic gray drop-shadows.
- **Texture is contained, never full-bleed.** Use `.dot-grid` on a *specific element*. **Never**
  put a full-bleed background grid/gradient behind page content — its lines won't align to your
  content-width dividers/borders and every hairline reads as "off" (this is a real bug we hit).
- **Section dividers = the canonical `.section-label` pattern**, not an ad-hoc `border-top` on the
  section. Number + label + a `flex:1` rule line live on ONE row, so the rule is part of the
  heading and can't drift:
  ```html
  <div class="section-label">
    <span class="section-label-num">01</span>
    <span class="section-label-text">Overview</span>
    <span class="section-label-line"></span>
  </div>
  ```
- **Motion:** `--ease-out` (cubic-bezier(.2,.8,.2,1)), 120/240/400ms. One orchestrated load with
  staggered reveals beats scattered micro-interactions. Respect `prefers-reduced-motion`.

## Anti-patterns (the "is this on-brand?" test)

These are the generic-AI tells the default brand exists to avoid. If the result has cyan-on-dark,
purple→blue gradients, neon glow, glassmorphism, rounded cards with drop shadows, gradient text on
metrics, full-bleed background grids, monospace-everywhere, or icon-above-every-heading — it's
generic, not on-brand. Stop and re-apply your project's tokens (the default's are above).

## Common pitfalls (cost us real rework)

These are brand-agnostic — they bite whatever tokens you ship.

- **Shorthand padding collisions kill vertical rhythm.** If a wrapper class sets `padding: 0 Xpx`
  it overrides a `section { padding: Y 0 }` (class beats element selector) and silently zeroes your
  section spacing. Split the axes: wrapper owns `padding-inline`, section owns `padding-block` —
  different properties, no collision regardless of specificity.
- **Section spacing lives on the section, dividers live on the heading.** Don't conflate them.

## Scope

- ✅ explainers, dossiers, infographics, diagrams (inline SVG), slides, landing/marketing one-pagers,
  static dashboards/mockups, reports (incl. harness architecture reports), any single-file HTML.
- ❌ a real component/vite **React app** → use your project's app conventions (routing/components),
  not this standalone-HTML brand layer.
- Marketing density vs app density differ: a roomy marketing scale vs a tight dashboard scale —
  match the context. (The Vinxi source splits these into `scale-marketing.css` / `scale-dashboard.css`;
  your brand may organize it differently.)
