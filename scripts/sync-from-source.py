"""Sync the plugin's behavior + payload FROM a vinxi-platform checkout.

This is the inverse of factory_init.py (source -> plugin, not plugin -> adopter).
It re-materializes:
  - skills/          <- <source>/.claude/skills/
  - hooks/hooks.json <- <source>/.claude/settings.json (SessionStart hook only)
  - factory/         <- <source>/.factory/{README.md,config.yaml,policies,templates}
                         and <source>/tools/agent (as factory/tools)
  - factory/docs-skeleton/ <- <source>/docs/{architecture,product,domain} authoring
                         templates/guides (a curated subset, not a full mirror)

Run manually after upstream vinxi-platform changes. Does NOT commit anything.
Stdlib only, Python 3.9+.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import sys


def plugin_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parent.parent


def count_files(root: pathlib.Path) -> int:
    if not root.exists():
        return 0
    return sum(1 for f in root.rglob("*") if f.is_file())


def mirror_dir(src: pathlib.Path, dst: pathlib.Path) -> int:
    """Remove dst (if present) then copytree src -> dst. Returns file count copied."""
    if dst.exists():
        shutil.rmtree(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst)
    return count_files(dst)


def sync_skills(source: pathlib.Path, target: pathlib.Path) -> int:
    src = source / ".claude" / "skills"
    dst = target / "skills"
    return mirror_dir(src, dst)


def sync_hook(source: pathlib.Path, target: pathlib.Path) -> None:
    settings_path = source / ".claude" / "settings.json"
    settings = json.loads(settings_path.read_text(encoding="utf-8"))
    session_start = settings["hooks"]["SessionStart"]
    hooks_doc = {"hooks": {"SessionStart": session_start}}
    dst = target / "hooks" / "hooks.json"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(hooks_doc, indent=2) + "\n", encoding="utf-8")


def sync_payload(source: pathlib.Path, target: pathlib.Path) -> dict:
    factory_dir = target / "factory"
    factory_dir.mkdir(parents=True, exist_ok=True)

    counts = {}

    readme_src = source / ".factory" / "README.md"
    readme_dst = factory_dir / "README.md"
    shutil.copyfile(readme_src, readme_dst)
    counts["README.md"] = 1

    config_src = source / ".factory" / "config.yaml"
    config_dst = factory_dir / "config.yaml"
    shutil.copyfile(config_src, config_dst)
    counts["config.yaml"] = 1

    counts["policies"] = mirror_dir(source / ".factory" / "policies", factory_dir / "policies")
    counts["templates"] = mirror_dir(source / ".factory" / "templates", factory_dir / "templates")
    counts["tools"] = mirror_dir(source / "tools" / "agent", factory_dir / "tools")

    return counts


DOCS_SKELETON = [
    "docs/architecture/README.md",
    "docs/architecture/principles.md",
    "docs/architecture/containers/TEMPLATE.md",
    "docs/architecture/components/TEMPLATE.md",
    "docs/architecture/features/TEMPLATE.md",
    "docs/architecture/decisions/README.md",
    "docs/product/README.md",
    "docs/product/features/README.md",
    "docs/domain/glossary.md",
]
DOCS_SKELETON_DIRS = ["docs/product/overview"]   # whole dir of stubs


def sync_docs_skeleton(source: pathlib.Path, plugin_root: pathlib.Path) -> list:
    dst_root = plugin_root / "factory/docs-skeleton"
    copied = []
    for rel in DOCS_SKELETON:
        src = source / rel
        if not src.is_file():
            continue
        # strip leading "docs/" so it lands under docs-skeleton/architecture/... etc.
        dst = dst_root / pathlib.Path(rel).relative_to("docs")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst); copied.append(str(dst.relative_to(plugin_root)))
    for rel in DOCS_SKELETON_DIRS:
        src = source / rel
        if src.is_dir():
            dst = dst_root / pathlib.Path(rel).relative_to("docs")
            if dst.exists(): shutil.rmtree(dst)
            shutil.copytree(src, dst); copied.append(str(dst.relative_to(plugin_root)) + "/**")
    return copied


def verify_tools_executable(source: pathlib.Path, target: pathlib.Path) -> list:
    """Return list of tool files under factory/tools that were executable in the
    source but lost their exec bit on copy."""
    src_dir = source / "tools" / "agent"
    dst_dir = target / "factory" / "tools"
    non_exec = []
    if not dst_dir.exists():
        return non_exec
    for f in sorted(dst_dir.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(dst_dir)
        src_f = src_dir / rel
        if src_f.is_file() and (src_f.stat().st_mode & 0o111) and not (f.stat().st_mode & 0o111):
            non_exec.append(f.relative_to(target).as_posix())
    return non_exec


def run(source: pathlib.Path, target: pathlib.Path) -> dict:
    skills_count = sync_skills(source, target)
    sync_hook(source, target)
    payload_counts = sync_payload(source, target)
    docs_skeleton = sync_docs_skeleton(source, target)
    non_exec = verify_tools_executable(source, target)
    return {
        "skills_files": skills_count,
        "payload": payload_counts,
        "docs_skeleton": docs_skeleton,
        "non_exec_tools": non_exec,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="sync-from-source",
        description="Re-materialize the plugin's skills/hooks/payload from a vinxi-platform checkout.",
    )
    ap.add_argument("--source", default=".", help="Path to a vinxi-platform checkout (default: '.')")
    args = ap.parse_args(argv)

    source = pathlib.Path(args.source).resolve()
    if not (source / ".claude" / "skills").is_dir():
        print(
            f"error: --source {source} does not look like a vinxi-platform checkout "
            f"(missing .claude/skills)",
            file=sys.stderr,
        )
        return 1

    target = plugin_root()
    result = run(source, target)

    print(f"Synced skills: {result['skills_files']} files -> skills/")
    print("Synced hook: hooks/hooks.json (SessionStart)")
    print("Synced payload into factory/:")
    for key, n in result["payload"].items():
        print(f"  - {key}: {n} file(s)")
    print(f"Synced docs skeleton: {len(result['docs_skeleton'])} entr(y/ies) -> factory/docs-skeleton/")
    if result["non_exec_tools"]:
        print("WARNING: the following tool files lost their executable bit:")
        for f in result["non_exec_tools"]:
            print(f"  - {f}")
    else:
        print("All factory/tools files retained their executable bit.")
    print()
    print("Next: run `python3 -m pytest tests/ -q` and review `git status` / `git diff`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
