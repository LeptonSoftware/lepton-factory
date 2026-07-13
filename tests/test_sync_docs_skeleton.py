import pathlib, shutil, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLUGIN_SCRIPT = ROOT / "scripts" / "sync-from-source.py"

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

def _temp_plugin(tmp):
    # Throwaway plugin tree: sync-from-source derives its plugin root from
    # __file__, so running a copy of the script here materializes into this
    # temp tree — the real repo is only read, never mutated (no git clean).
    plugin = tmp / "plugin"
    (plugin / "scripts").mkdir(parents=True)
    shutil.copy2(PLUGIN_SCRIPT, plugin / "scripts" / "sync-from-source.py")
    for d in ("skills", "hooks", "factory"):
        (plugin / d).mkdir()
    return plugin

def test_sync_materializes_docs_skeleton(tmp_path):
    src = _fake_src(tmp_path / "src")
    plugin = _temp_plugin(tmp_path)
    subprocess.run([sys.executable, str(plugin / "scripts" / "sync-from-source.py"),
                    "--source", str(src)], cwd=str(plugin), check=True)
    ds = plugin / "factory/docs-skeleton"
    assert (ds/"architecture/containers/TEMPLATE.md").is_file()
    assert (ds/"product/features/README.md").is_file()
    assert (ds/"domain/glossary.md").is_file()
