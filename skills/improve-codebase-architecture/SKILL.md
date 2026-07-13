---
name: improve-codebase-architecture
description: Scan a chosen area of the codebase for deepening opportunities, present them as a visual brand-styled HTML report, then grill through whichever one the user picks. Run as /improve-codebase-architecture [area].
disable-model-invocation: true
---
<!-- adapted from mattpocock/skills improve-codebase-architecture (MIT);
grilling retargeted to this repo's clarify-intent, domain-modeling to domain-model,
CONTEXT.md to docs/domain/glossary.md, ADRs to blueprint-local, and the HTML report
restyled from generic Tailwind to the project's brand design system (via the `brand` skill). -->

# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities** — refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability. This deepens *one chosen module*; it is not a repo-wide drift sweep.

This command is _informed_ by the project's domain model and built on a shared design vocabulary:

- Run the `codebase-design` skill for the architecture vocabulary (**module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**) and its principles (the deletion test, "the interface is the test surface", "one adapter = hypothetical seam, two = real"). Use these terms exactly in every suggestion — don't drift into "component," "service," "API," or "boundary." They are the review-enforced design language in `docs/architecture/principles.md`.
- The domain language in `docs/domain/glossary.md` gives names to good seams; ADRs (blueprint-local in `docs/architecture/`, or `docs/architecture/decisions/` when cross-cutting) record decisions this command should not re-litigate.

**Relation to `factory-sweep`:** they do not overlap. `factory-sweep` finds *cross-commit drift* across the whole repo and files findings as WOs. This command *deepens one chosen module* interactively, right now. If a sweep finding is "this module is shallow," this is the command that explores the fix.

## Process

### 1. Explore

Read the project's domain glossary (`docs/domain/glossary.md`) and any ADRs in the area you're touching first.

Then use the Agent tool with `subagent_type=Explore` to walk the codebase. Don't follow rigid heuristics — explore organically and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow** — interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or just move it? A "yes, concentrates" is the signal you want.

### 2. Present candidates as a brand-styled HTML report

Write a self-contained HTML file to the OS temp directory so nothing lands in the repo. Resolve the temp dir from `$TMPDIR`, falling back to `/tmp` (or `%TEMP%` on Windows), and write to `<tmpdir>/architecture-review-<timestamp>.html` so each run gets a fresh file. Open it for the user — `xdg-open <path>` on Linux, `open <path>` on macOS, `start <path>` on Windows — and tell them the absolute path.

The report is styled with the project's brand design system (via the `brand` skill), not generic Tailwind. Run the `brand` skill and follow it: inline its `assets/brand.css` into a `<style>` block, load the brand's fonts from the fonts CDN, and use the project's palette and canonical components (`.section-label` for dividers, etc.). Keep **Mermaid via CDN** for graph-shaped diagrams. Mix Mermaid with hand-crafted CSS/SVG visuals — Mermaid when relationships are graph-shaped (call graphs, dependencies, sequences), hand-built divs/SVG when you want something more editorial (mass diagrams, cross-sections, collapse animations). Each candidate gets a **before/after visualisation**. Be visual.

For each candidate, render a card with:

- **Files** — which files/modules are involved
- **Problem** — why the current architecture is causing friction
- **Solution** — plain English description of what would change
- **Benefits** — explained in terms of locality and leverage, and how tests would improve
- **Before / After diagram** — side-by-side, custom-drawn, illustrating the shallowness and the deepening
- **Recommendation strength** — one of `Strong`, `Worth exploring`, `Speculative`, rendered as a badge

End the report with a **Top recommendation** section: which candidate you'd tackle first and why.

**Use `docs/domain/glossary.md` vocabulary for the domain, and the `codebase-design` vocabulary for the architecture.** If the glossary defines "Statement," talk about "the Statement intake module" — not "the FooBarHandler," and not "the Statement service."

**ADR conflicts**: if a candidate contradicts an existing ADR, only surface it when the friction is real enough to warrant revisiting the ADR. Mark it clearly in the card (e.g. a warning callout: _"contradicts BP-COMP-<X> ADR-NNN — but worth reopening because…"_). Don't list every theoretical refactor an ADR forbids.

See [HTML-REPORT.md](HTML-REPORT.md) for the full brand-styled HTML scaffold, diagram patterns, and styling guidance.

Do NOT propose interfaces yet. After the file is written, ask the user: "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, run the `clarify-intent` skill to walk the design tree with them one question at a time — constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive. Grill until the design is resolved, not to a fixed count.

Side effects happen inline as decisions crystallize — run the `domain-model` skill to keep the domain model current as you go:

- **Naming a deepened module after a concept not in `docs/domain/glossary.md`?** Add the term to the glossary right there.
- **Sharpening a fuzzy term during the conversation?** Update the glossary inline.
- **User rejects the candidate with a load-bearing reason?** Offer an ADR (blueprint-local, format in `docs/architecture/README.md`), framed as: _"Want me to record this as an ADR so future architecture reviews don't re-suggest it?"_ Only offer when the reason would actually be needed by a future explorer to avoid re-suggesting the same thing — skip ephemeral reasons ("not worth it right now") and self-evident ones.
- **Want to explore alternative interfaces for the deepened module?** Run the `codebase-design` skill and use its design-it-twice parallel sub-agent pattern.

This command deepens a module interactively; it does not itself land code. Turning the resolved design into a change goes through a Work Order (`wo-author`).
