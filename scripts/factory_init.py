"""Bootstrap/upgrade the Lepton factory harness in a target repo. Stdlib only."""
from __future__ import annotations
import argparse, hashlib, json, pathlib, re, shutil, sys

BANNER_LINES = [
    "MANAGED BY lepton-factory — do not hand-edit.",
    "Run /factory-init --upgrade to update.",
    "To diverge, add a shadowing file under .factory/overrides/.",
]
BANNER_TEXT = " ".join(BANNER_LINES)

def banner_for(dst_rel: str) -> str:
    suffix = pathlib.PurePosixPath(dst_rel).suffix.lower()
    if suffix == ".md":
        return f"<!-- {BANNER_TEXT} -->"
    if suffix in (".yaml", ".yml"):
        return "\n".join(f"# {line}" for line in BANNER_LINES)
    return ""

def stamp(content: str, dst_rel: str) -> str:
    banner = banner_for(dst_rel)
    return f"{banner}\n\n{content}" if banner else content

MANIFEST_REL = ".factory/.factory-manifest.json"

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def read_manifest(target_root: pathlib.Path) -> dict:
    p = target_root / MANIFEST_REL
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))

def write_manifest(target_root: pathlib.Path, entries: dict) -> None:
    p = target_root / MANIFEST_REL
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(entries, indent=2, sort_keys=True) + "\n", encoding="utf-8")

PAYLOAD = [
    ("README.md",   ".factory/README.md",   True,  False),
    ("policies",    ".factory/policies",    True,  False),
    ("templates",   ".factory/templates",   False, False),
    ("tools",       "tools/agent",          False, True),
]

def iter_payload_files(payload_root):
    for src_rel, dst_rel, do_stamp, mode in PAYLOAD:
        src = payload_root / src_rel
        if src.is_file():
            yield src, dst_rel, do_stamp, mode
        else:
            for f in sorted(src.rglob("*")):
                if f.is_file():
                    rel = f.relative_to(src).as_posix()
                    yield f, f"{dst_rel}/{rel}", do_stamp, mode

def copy_payload(payload_root, target_root, *, upgrade: bool) -> dict:
    prior = read_manifest(target_root)
    written, skipped, manifest = [], [], {}
    for src, dst_rel, do_stamp, mode in iter_payload_files(payload_root):
        content = src.read_text(encoding="utf-8")
        out = stamp(content, dst_rel) if do_stamp else content
        new_sha = sha256_text(out)
        dst = target_root / dst_rel
        if upgrade and dst.exists() and dst_rel in prior \
                and sha256_text(dst.read_text(encoding="utf-8")) != prior[dst_rel]:
            skipped.append(dst_rel)                 # adopter-edited: preserve
            manifest[dst_rel] = prior[dst_rel]
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(out, encoding="utf-8")
        if mode:
            shutil.copymode(src, dst)
        written.append(dst_rel)
        manifest[dst_rel] = new_sha
    return {"written": written, "skipped_edited": skipped, "manifest": manifest}

SKELETON_SRC = "docs-skeleton"
SKELETON_MANAGED_SUFFIX = ("TEMPLATE.md", "README.md", "principles.md")  # authoring refs → stamped/managed

def _is_seed_once(dst_rel: str) -> bool:
    # overview stubs + glossary become human-owned; never overwrite once present
    return dst_rel.startswith("docs/product/overview/") or dst_rel == "docs/domain/glossary.md"

def copy_docs_skeleton(payload_root, target_root) -> dict:
    src_root = pathlib.Path(payload_root) / SKELETON_SRC
    written, skipped = [], []
    if not src_root.is_dir():
        return {"written": written, "skipped": skipped}
    for f in sorted(src_root.rglob("*")):
        if not f.is_file():
            continue
        dst_rel = "docs/" + f.relative_to(src_root).as_posix()
        dst = pathlib.Path(target_root) / dst_rel
        if _is_seed_once(dst_rel) and dst.exists():
            skipped.append(dst_rel); continue
        content = f.read_text(encoding="utf-8")
        if dst_rel.endswith(SKELETON_MANAGED_SUFFIX):
            content = stamp(content, dst_rel)     # banner on authoring references
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(content, encoding="utf-8"); written.append(dst_rel)
    return {"written": written, "skipped": skipped}

STATE_DIRS = ["work-orders", "feedback", "indexes", "overrides"]

def ensure_state_dirs(target_root) -> list:
    created = []
    for d in STATE_DIRS:
        p = target_root / ".factory" / d
        p.mkdir(parents=True, exist_ok=True)
        (p / ".gitkeep").touch()
        created.append(d)
    return created

def install_config(payload_root, target_root) -> bool:
    dst = target_root / ".factory/config.yaml"
    if dst.exists():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text((payload_root / "config.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    return True

MARK_START = "<!-- lepton-factory:managed:start -->"
MARK_END = "<!-- lepton-factory:managed:end -->"

ROUTER_BLOCK = """# AGENTS.md — Router

This repository runs the **Lepton software factory**. All delivery work runs
through a Work Order under `.factory/work-orders/`. Pure `docs/` edits are exempt.

- Author new work: invoke the `wo-author` skill.
- Execute work: invoke the `wo-execute` skill (`/wo-execute WO-<id>`).
- Reviews / sweeps / autonomous runs: `wo-review`, `factory-sweep`, `night-shift`, `factory-learn`.
- Lifecycle, gates, risk tiers, precedence: `.factory/README.md` — the operating manual.

Deterministic tools live in `tools/agent/` (all support `--help`; exit codes are gates).
Never create competing artifacts (`spec.md`, `design.md`, `tasks.md`). The canonical
artifact set is defined in `.factory/README.md`.
"""

CLAUDE_BLOCK = "# CLAUDE.md\n\nRead and follow @AGENTS.md — it is the router for this repository.\n"

def apply_managed_block(existing: str | None, block: str) -> str:
    marked = f"{MARK_START}\n{block.rstrip()}\n{MARK_END}"
    if not existing:
        return marked + "\n"
    pattern = re.compile(re.escape(MARK_START) + r".*?" + re.escape(MARK_END), re.DOTALL)
    if pattern.search(existing):
        return pattern.sub(lambda m: marked, existing)
    return existing.rstrip() + "\n\n" + marked + "\n"

def write_routers(target_root) -> None:
    for name, block in (("AGENTS.md", ROUTER_BLOCK), ("CLAUDE.md", CLAUDE_BLOCK)):
        p = target_root / name
        existing = p.read_text(encoding="utf-8") if p.exists() else None
        p.write_text(apply_managed_block(existing, block), encoding="utf-8")

def default_payload_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parent.parent / "factory"

def run(target_root, payload_root, *, upgrade: bool) -> dict:
    target_root = pathlib.Path(target_root); payload_root = pathlib.Path(payload_root)
    report = copy_payload(payload_root, target_root, upgrade=upgrade)
    copy_docs_skeleton(payload_root, target_root)
    ensure_state_dirs(target_root)
    config_written = install_config(payload_root, target_root)
    write_routers(target_root)
    write_manifest(target_root, report["manifest"])
    return {"written": report["written"], "skipped_edited": report["skipped_edited"],
            "config_written": config_written, "upgrade": upgrade}

import importlib.util as _ilu, subprocess as _sp

def _seedmod():
    p = pathlib.Path(__file__).resolve().parent / "seed.py"
    sp = _ilu.spec_from_file_location("seed", p); m = _ilu.module_from_spec(sp); sp.loader.exec_module(m)
    return m

def _write_if_absent(target_root, dst_rel, content, human_owned):
    dst = pathlib.Path(target_root) / dst_rel
    if human_owned and dst.exists():
        return None
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(content, encoding="utf-8"); return dst_rel

BLUEPRINTS_KEY_RE = re.compile(r"^blueprints:\s*$", re.MULTILINE)

def mirror_blueprint_into_config(text: str, bpid: str, meta: dict) -> str:
    """Insert a `  {bpid}:` entry UNDER the existing top-level `blueprints:` key
    (or create that key if absent), never as a second top-level `blueprints:`
    block — duplicate top-level keys resolve last-write-wins in this repo's YAML
    parser, which would silently drop every pre-existing blueprint entry."""
    entry_lines = [f"  {bpid}:", "    paths:"] + [f"      - {p}" for p in meta["paths"]] + [f"    owner: {meta['owner']}"]
    if re.search(rf"^  {re.escape(bpid)}:\s*$", text, re.MULTILINE):
        return text                                 # already present
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if BLUEPRINTS_KEY_RE.match(line):
            new_lines = lines[:i + 1] + entry_lines + lines[i + 1:]
            return "\n".join(new_lines) + "\n"
    sep = [""] if lines else []
    new_lines = lines + sep + ["blueprints:"] + entry_lines
    return "\n".join(new_lines) + "\n"

def apply_seed(seed, target_root, date, factory_root=None) -> list:
    s = _seedmod(); factory_root = factory_root or (pathlib.Path(target_root)/".factory")
    written = []
    dst, content = s.render_container(seed, date, factory_root)
    written.append(_write_if_absent(target_root, dst, content, True))
    dst, content = s.render_frd(seed, date); written.append(_write_if_absent(target_root, dst, content, True))
    for dst, content in s.render_overview(seed):
        written.append(_write_if_absent(target_root, dst, content, True))
    dst, content = s.render_glossary(seed); written.append(_write_if_absent(target_root, dst, content, True))
    # mirror blueprint into config.yaml blueprints: (in place — see
    # mirror_blueprint_into_config for why we never append a new top-level key)
    bpid, meta = s.config_blueprint_line(seed, factory_root)
    cfg = pathlib.Path(target_root)/".factory/config.yaml"
    text = cfg.read_text(encoding="utf-8")
    new_text = mirror_blueprint_into_config(text, bpid, meta)
    if new_text != text:
        cfg.write_text(new_text, encoding="utf-8")
    return [w for w in written if w]

def validator_gate(target_root) -> tuple:
    tools = pathlib.Path(target_root)/"tools/agent"
    out = []
    for cmd in (["generate-indexes"], ["check-traceability"], ["validate-work-order", "--all"]):
        r = _sp.run(["python3", str(tools/cmd[0]), *cmd[1:]], cwd=target_root,
                    capture_output=True, text=True, encoding="utf-8")
        out.append(f"$ {cmd[0]} {' '.join(cmd[1:])}\n{r.stdout}{r.stderr}")
        if r.returncode != 0:
            return r.returncode, "\n".join(out)
    return 0, "\n".join(out)

SECTION_HEADING_RE = re.compile(r"^## .*$", re.MULTILINE)

def fill_section(md: str, heading: str, body_text: str) -> str:
    """Replace the content between a `## {heading}` line and the next `## `
    heading (or EOF) with body_text. Never appends a new heading — the section
    must already exist in the document (work-order.md's template already ships
    every section a freshly-authored WO needs); raises if it is absent so a
    caller can't silently corrupt the artifact's structure by re-adding a
    heading in the wrong place."""
    target = f"## {heading}"
    start = None
    for m in SECTION_HEADING_RE.finditer(md):
        if m.group(0).strip() == target:
            start = m.end()
            break
    if start is None:
        raise ValueError(f"fill_section: heading '{target}' not found in document")
    next_m = SECTION_HEADING_RE.search(md, start)
    end = next_m.start() if next_m else len(md)
    filled = f"\n\n{body_text.rstrip()}\n\n"
    return md[:start] + filled + md[end:]

def author_wo1(seed, target_root, date) -> None:
    tools = pathlib.Path(target_root)/"tools/agent"; s = seed
    _sp.run(["python3", str(tools/"init-work-order"), "--wo", "WO-0001",
             "--title", s["feature"]["title"]], cwd=target_root, check=True)
    wo = pathlib.Path(target_root)/".factory/work-orders/WO-0001/work-order.md"
    if not wo.exists():
        return
    area = s["area"]
    reqs_body = "\n".join(f"- REQ-{area}-{int(r['id_seq']):03d}" for r in s["feature"]["reqs"])
    bp_body = f"- BP-CONT-{s['container']['name']}"
    decision_body = "- HITL decisions: (none)\n- AFK: all other execution decisions"
    md = wo.read_text(encoding="utf-8")
    md = fill_section(md, "Requirements", reqs_body)
    md = fill_section(md, "Blueprints", bp_body)
    md = fill_section(md, "Decision classification", decision_body)
    wo.write_text(md, encoding="utf-8")

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="factory-init",
        description="Bootstrap or upgrade the Lepton factory harness in a repo.")
    ap.add_argument("--target", default=".")
    ap.add_argument("--payload", default=str(default_payload_root()))
    ap.add_argument("--upgrade", action="store_true")
    a = ap.parse_args(argv)
    s = run(a.target, a.payload, upgrade=a.upgrade)
    mode = "Upgraded" if a.upgrade else "Installed"
    print(f"{mode} factory harness: {len(s['written'])} managed files written.")
    if s["skipped_edited"]:
        print("Preserved adopter-edited files (move divergences to .factory/overrides/):")
        for f in s["skipped_edited"]:
            print(f"  - {f}")
    if s["config_written"]:
        print("Wrote .factory/config.yaml (adopter-owned; edit freely).")
    print("Next: run /wo-author to create your first Work Order.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
