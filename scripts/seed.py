"""Seed contract for wizard-driven /factory-init. See plan Task 3 for the shape."""
from __future__ import annotations
import json, pathlib

TIERS = ("internal", "production")
STACKS = ("generic", "node")

def validate_seed(seed: dict) -> list:
    errs = []
    if seed.get("tier") not in TIERS:
        errs.append(f"tier must be one of {TIERS}, got {seed.get('tier')!r}")
    if seed.get("stack") not in STACKS:
        errs.append(f"stack must be one of {STACKS}, got {seed.get('stack')!r}")
    if not (isinstance(seed.get("area"), str) and seed["area"].isalnum() and seed["area"].isupper()):
        errs.append("area must be an uppercase alphanumeric token")
    f = seed.get("feature")
    if not isinstance(f, dict) or not f.get("slug") or not f.get("reqs"):
        errs.append("feature{slug,title,user_story,reqs[]} required")
    else:
        for i, r in enumerate(f["reqs"]):
            if not r.get("statement") or not r.get("acs"):
                errs.append(f"feature.reqs[{i}] needs statement + acs[]")
    c = seed.get("container")
    if not isinstance(c, dict) or not c.get("slug") or not c.get("name") or not c.get("applies_to"):
        errs.append("container{slug,name,title,summary,owner,applies_to,body} required")
    return errs

def load_seed(path) -> dict:
    return json.loads(pathlib.Path(path).read_text(encoding="utf-8"))

FM_ORDER = ["title", "summary", "owners", "applies_to", "status", "last_verified"]

def _fm_val(v):
    if isinstance(v, list):
        return "[" + ", ".join(str(x) for x in v) + "]"
    return str(v)

def frontmatter(d: dict) -> str:
    lines = [f"{k}: {_fm_val(d[k])}" for k in FM_ORDER if k in d]
    return "---\n" + "\n".join(lines) + "\n---\n"

def build_doc(front: dict, heading: str, body: str) -> str:
    return f"{frontmatter(front)}\n# {heading}\n\n{body.rstrip()}\n"

def load_profile(factory_root, stack: str) -> dict:
    return json.loads((pathlib.Path(factory_root)/"profiles"/stack/"profile.json").read_text(encoding="utf-8"))

def render_container(seed: dict, date: str, factory_root) -> tuple:
    c = seed["container"]; name = c["name"]; bpid = f"BP-CONT-{name}"
    front = {"title": f"{bpid} — {c['title']}", "summary": c["summary"],
             "owners": [c.get("owner") or load_profile(factory_root, seed['stack'])['owner_default']],
             "applies_to": c["applies_to"], "status": "draft", "last_verified": date}
    dst_rel = f"docs/architecture/containers/{c['slug']}.md"
    return dst_rel, build_doc(front, f"{bpid}: {c['title']}", c["body"])

def config_blueprint_line(seed: dict) -> tuple:
    c = seed["container"]
    return f"BP-CONT-{c['name']}", {"applies_to": c["applies_to"],
                                    "owner": c.get("owner") or "product-owner"}
