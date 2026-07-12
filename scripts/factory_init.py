"""Bootstrap/upgrade the Vinxi factory harness in a target repo. Stdlib only."""
from __future__ import annotations
import hashlib, json, os, pathlib, shutil

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
