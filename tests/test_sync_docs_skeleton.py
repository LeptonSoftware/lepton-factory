import importlib.util, pathlib, subprocess, sys, json
ROOT = pathlib.Path(__file__).resolve().parents[1]

def _fake_src(tmp):
    for rel in ["docs/architecture/containers/TEMPLATE.md",
                "docs/architecture/components/TEMPLATE.md",
                "docs/architecture/features/TEMPLATE.md",
                "docs/architecture/README.md",
                "docs/product/README.md",
                "docs/product/features/README.md",
                "docs/product/overview/product-description.md",
                "docs/domain/glossary.md"]:
        p = tmp / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text("stub\n")
    (tmp / ".claude/skills/demo").mkdir(parents=True)
    (tmp / ".claude/skills/demo/SKILL.md").write_text("---\nname: demo\ndescription: d\n---\n")
    (tmp / ".claude/settings.json").write_text('{"hooks":{"SessionStart":[]}}')
    (tmp / ".factory/policies").mkdir(parents=True); (tmp/".factory/policies/x.md").write_text("x")
    (tmp / ".factory/templates").mkdir(parents=True); (tmp/".factory/templates/y.md").write_text("y")
    (tmp / ".factory/README.md").write_text("m"); (tmp/".factory/config.yaml").write_text("v: 1")
    (tmp / "tools/agent").mkdir(parents=True); (tmp/"tools/agent/z").write_text("#!/bin/sh\n")
    return tmp

def test_sync_materializes_docs_skeleton(tmp_path):
    src = _fake_src(tmp_path / "src")
    try:
        subprocess.run([sys.executable, str(ROOT/"scripts/sync-from-source.py"),
                        "--source", str(src)], cwd=ROOT, check=True)
        ds = ROOT / "factory/docs-skeleton"
        assert (ds/"architecture/containers/TEMPLATE.md").is_file()
        assert (ds/"product/features/README.md").is_file()
        assert (ds/"domain/glossary.md").is_file()
    finally:
        # restore the real plugin state via git so this test doesn't leave
        # the working tree dirty with fixture content (matches tests/test_sync.py)
        subprocess.run(
            ["git", "checkout", "--", "skills", "hooks", "factory"],
            cwd=ROOT,
            check=False,
        )
        subprocess.run(
            ["git", "clean", "-fd", "skills", "hooks", "factory"],
            cwd=ROOT,
            check=False,
        )
