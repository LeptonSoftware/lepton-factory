"""Bootstrap/upgrade the Vinxi factory harness in a target repo. Stdlib only."""
from __future__ import annotations
import hashlib, json, os, pathlib, re, shutil

BANNER_TEXT = (
    "MANAGED BY vinxi-factory — do not hand-edit. "
    "Run /factory-init --upgrade to update. "
    "To diverge, add a shadowing file under .factory/overrides/."
)

def banner_for(dst_rel: str) -> str:
    suffix = pathlib.PurePosixPath(dst_rel).suffix
    if suffix == ".md":
        return f"<!-- {BANNER_TEXT} -->"
    if suffix in (".yaml", ".yml"):
        return "\n".join(f"# {line}" for line in
                         ["MANAGED BY vinxi-factory — do not hand-edit.",
                          "Run /factory-init --upgrade to update.",
                          "To diverge, add a shadowing file under .factory/overrides/."])
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
    return json.loads(p.read_text())

def write_manifest(target_root: pathlib.Path, entries: dict) -> None:
    p = target_root / MANIFEST_REL
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(entries, indent=2, sort_keys=True) + "\n")

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
        content = src.read_text()
        out = stamp(content, dst_rel) if do_stamp else content
        new_sha = sha256_text(out)
        dst = target_root / dst_rel
        if upgrade and dst.exists() and dst_rel in prior \
                and sha256_text(dst.read_text()) != prior[dst_rel]:
            skipped.append(dst_rel)                 # adopter-edited: preserve
            manifest[dst_rel] = prior[dst_rel]
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(out)
        if mode:
            shutil.copymode(src, dst)
        written.append(dst_rel)
        manifest[dst_rel] = new_sha
    return {"written": written, "skipped_edited": skipped, "manifest": manifest}

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
    dst.write_text((payload_root / "config.yaml").read_text())
    return True

MARK_START = "<!-- vinxi-factory:managed:start -->"
MARK_END = "<!-- vinxi-factory:managed:end -->"

ROUTER_BLOCK = """# AGENTS.md — Router

This repository runs the **Vinxi software factory**. All delivery work runs
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
        existing = p.read_text() if p.exists() else None
        p.write_text(apply_managed_block(existing, block))
