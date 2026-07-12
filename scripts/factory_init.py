"""Bootstrap/upgrade the Vinxi factory harness in a target repo. Stdlib only."""
from __future__ import annotations
import hashlib, json, pathlib

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
