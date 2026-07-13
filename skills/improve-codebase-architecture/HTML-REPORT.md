<!-- adapted from mattpocock/skills improve-codebase-architecture HTML-REPORT.md (MIT);
restyled from generic Tailwind to the project's brand design system, applied via the
`brand` skill (assets/brand.css). -->

# HTML Report Format (brand-styled)

The architectural review is rendered as a single self-contained HTML file in the OS temp directory, styled with the project's **brand** design system (via the `brand` skill) — not generic Tailwind. Run the `brand` skill first and honour its non-negotiables. Mermaid still handles graph-shaped diagrams; hand-built divs and inline SVG handle the more editorial visuals (mass diagrams, cross-sections). Mix the two — don't lean on Mermaid for everything, it'll start to look generic.

## Brand setup (do this first)

- **Inline the tokens.** Copy the `brand` skill's `assets/brand.css` into a `<style>` block (inline, so the file is self-contained and portable out of the repo). It defines the `:root` tokens, fonts, and canonical components. (The shipped default is the Vinxi/Lepton system — if your project has replaced it, you inherit your own tokens automatically.)
- **Load the fonts** from the CDN the brand uses — the default pairs a display/body family (Hanken Grotesk) with a mono family (Geist Mono) for labels, file paths, module names, and badges. Never Inter/Roboto/system defaults.
- **Palette:** the default brand is midnight `#1A2040` text on snow `#FBFDFF`; blue `#0066E3` as the single accent; green/amber/red are semantic and used sparingly (recommendation strength, leakage, warnings). Never pure black/white. Swap for your brand's tokens if it has replaced the default.
- **Geometry:** sharp — `border-radius: 0`, thin 1px borders in `--silver`/`--fog`, tinted `--shadow-*` elevation, not gray drop-shadows.
- **No full-bleed background grid.** `.dot-grid` on a specific element only — a full-bleed grid's hairlines won't align to your content-width borders (a real bug).

## Scaffold

The scaffold below wires up the shipped default brand tokens. If your project has swapped `assets/brand.css` (and its fonts/Mermaid theme variables), mirror those values here.

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Architecture review — {{repo name}}</title>
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700;800;900&family=Geist+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      // theme: "base" + brand variables so diagrams read as your brand, not neutral-gray
      mermaid.initialize({
        startOnLoad: true,
        securityLevel: "loose",
        theme: "base",
        themeVariables: {
          fontFamily: "'Hanken Grotesk', sans-serif",
          primaryColor: "#FBFDFF", primaryTextColor: "#1A2040",
          primaryBorderColor: "#DFE3EA", lineColor: "#6B7280"
        }
      });
    </script>
    <style>
      /* 1. inline the whole of the brand skill's assets/brand.css here (:root tokens + components) */
      /* 2. then the small review-specific layer below */
      body { background: var(--snow); color: var(--midnight); font-family: var(--font-sans); }
      main { max-width: var(--content-width); margin: 0 auto; padding-inline: var(--space-6); }
      section { padding-block: var(--space-12); }              /* spacing on the section */
      .mono { font-family: var(--font-mono); }
      .seam { stroke: var(--ash); stroke-dasharray: 4 4; }     /* dashed seam lines */
      .leak { stroke: var(--red); stroke-width: 2px; }         /* leakage edges */
      .deep { background: var(--midnight); color: var(--snow); } /* the deep module */
    </style>
  </head>
  <body>
    <main>
      <header>...</header>
      <section id="candidates">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## Header

Repo name, date, and a compact legend: solid box = module, dashed line = seam, red arrow = leakage, midnight-filled box = deep module. No introduction paragraph — straight into the candidates.

## Section dividers

Use the canonical brand `.section-label` pattern for every section heading — number + label + a `flex:1` rule line on ONE row — never an ad-hoc `border-top`:

```html
<div class="section-label">
  <span class="section-label-num">01</span>
  <span class="section-label-text">Deepening candidates</span>
  <span class="section-label-line"></span>
</div>
```

## Candidate card

The diagrams carry the weight. Prose is sparse, plain, and uses the glossary terms (from the `codebase-design` skill) without ceremony.

Each candidate is one `<article>` with thin 1px `--silver` borders and sharp corners:

- **Title** — short, names the deepening (e.g. "Collapse the Statement intake pipeline").
- **Badge row** — recommendation strength (`Strong` = `--green-deep`, `Worth exploring` = `--amber-text`, `Speculative` = `--steel`), plus a tag for the dependency category (`in-process`, `local-substitutable`, `ports & adapters`, `mock`). Badges use the mono font, uppercase, `--space-1`/`--space-2` padding, sharp corners.
- **Files** — monospaced list in the mono font (`.mono`), small.
- **Before / After diagram** — the centrepiece. Two columns, side by side. See patterns below.
- **Problem** — one sentence. What hurts.
- **Solution** — one sentence. What changes.
- **Wins** — bullets, ≤6 words each. e.g. "Tests hit one interface", "Pricing logic stops leaking", "Delete 4 shallow wrappers".
- **ADR callout** (if applicable) — one line in an `--amber-bg` box.

No paragraphs of explanation. If the diagram needs a paragraph to be understood, redraw the diagram.

## Diagram patterns

Pick the pattern that fits the candidate. Mix them. Don't make every diagram look the same — variety is part of the point. Colour from the brand tokens only: `--blue` for the accented path, `--red`/`.leak` for leakage, `--ash`/`.seam` for seams, `--midnight`/`.deep` for the deep module.

### Mermaid graph (the workhorse for dependencies / call flow)

Use a Mermaid `flowchart` or `graph` when the point is "X calls Y calls Z, and look at the mess." Wrap it in a bordered `--silver` card so it doesn't feel parachuted in. Style with classDef to colour leakage edges `--red` and the deep module `--midnight`. Sequence diagrams work well for "before: 6 round-trips; after: 1."

```html
<div style="border:1px solid var(--silver); background:var(--snow); padding:var(--space-4)">
  <pre class="mermaid">
    flowchart LR
      A[StatementHandler] --> B[StatementValidator]
      B --> C[StatementRepo]
      C -.leak.-> D[OntologyClient]
      classDef leak stroke:#C8362F,stroke-width:2px;
      class C,D leak
  </pre>
</div>
```

### Hand-built boxes-and-arrows (when Mermaid's layout fights you)

Modules as `<div>`s with 1px `--silver` borders and mono-font labels. Arrows as inline SVG `<line>`/`<path>` positioned absolutely over a relative container. Reach for this when you want the "after" diagram to feel like one `.deep` midnight-filled deep module with greyed-out (`--ash`) internals — Mermaid won't render that with the right weight.

### Cross-section (good for layered shallowness)

Stack horizontal bands (`border-left: 4px solid var(--fog)`, `--space-8` tall) to show layers a call passes through. Before: 6 thin layers each doing nothing. After: 1 thick band labelled with the consolidated responsibility.

### Mass diagram (good for "interface as wide as implementation")

Two rectangles per module — one for interface surface area, one for implementation. Before: interface rectangle nearly as tall as the implementation rectangle (shallow). After: interface rectangle short, implementation rectangle tall (deep). Fill the implementation with `--midnight`, the interface with `--blue-tint`.

### Call-graph collapse

Before: a tree of function calls rendered as nested boxes. After: the same tree collapsed into one `.deep` box, with the now-internal calls shown faded (`--ash`) inside it.

## Style guidance

- Lean editorial, not corporate-dashboard. Generous whitespace on the 8px scale (`--space-*`). Display-font headings at 700–900 weight.
- Colour sparingly: `--blue` is the one accent; `--red` for leakage, `--amber-text` for warnings, `--green-deep` for a `Strong` badge. Everything else is the midnight/snow/silver neutral range.
- Keep diagrams ~320px tall so before/after sits comfortably side by side without scrolling.
- Module labels inside diagrams: mono font, `text-transform: uppercase`, `letter-spacing`, small — they should read as schematic, not as UI.
- Split spacing axes: the content wrapper owns `padding-inline`, sections own `padding-block` (avoids the shorthand-padding collision that zeroes section spacing).
- The only scripts are the Mermaid ESM import (fonts are the Google CDN link). The report is otherwise static — no app code, no interactivity beyond Mermaid's rendering. Respect `prefers-reduced-motion` on any reveal animation.

## Top recommendation section

One larger card, `.deep` midnight-filled for emphasis. Candidate name, one sentence on why, anchor link to its card. That's it.

## Tone

Plain English, concise — but the architectural nouns and verbs come straight from the `codebase-design` skill. Concision is not an excuse to drift.

**Use exactly:** module, interface, implementation, depth, deep, shallow, seam, adapter, leverage, locality.

**Never substitute:** component, service, unit (for module) · API, signature (for interface) · boundary (for seam) · layer, wrapper (for module, when you mean module).

**Phrasings that fit the style:**

- "Statement intake module is shallow — interface nearly matches the implementation."
- "Ontology lookup leaks across the seam."
- "Deepen: one interface, one place to test."
- "Two adapters justify the seam: HTTP in prod, in-memory in tests."

**Wins bullets** name the gain in glossary terms: *"locality: bugs concentrate in one module"*, *"leverage: one interface, N call sites"*, *"interface shrinks; implementation absorbs the wrappers"*. Don't write *"easier to maintain"* or *"cleaner code"* — those aren't in the glossary and don't earn their place.

No hedging, no throat-clearing, no "it's worth noting that…". If a sentence could be a bullet, make it a bullet. If a bullet could be cut, cut it. If a term isn't in the `codebase-design` glossary, reach for one that is before inventing a new one.
