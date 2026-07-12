"""Bootstrap/upgrade the Vinxi factory harness in a target repo. Stdlib only."""
from __future__ import annotations
import pathlib

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
