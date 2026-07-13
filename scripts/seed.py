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
