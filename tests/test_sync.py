import json
import os
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLUGIN_SCRIPT = ROOT / "scripts" / "sync-from-source.py"


def _make_fake_source(tmp_path: pathlib.Path) -> pathlib.Path:
    src = tmp_path / "fake-vinxi-platform"

    skill_dir = src / ".claude" / "skills" / "demo"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# demo skill\n", encoding="utf-8")

    settings = {
        "hooks": {
            "SessionStart": [
                {
                    "matcher": "startup|resume|compact",
                    "hooks": [{"type": "command", "command": "echo hi"}],
                }
            ]
        }
    }
    (src / ".claude" / "settings.json").write_text(json.dumps(settings), encoding="utf-8")

    factory_dir = src / ".factory"
    factory_dir.mkdir(parents=True)
    (factory_dir / "README.md").write_text("# factory readme\n", encoding="utf-8")
    (factory_dir / "config.yaml").write_text("key: value\n", encoding="utf-8")
    (factory_dir / "policies").mkdir()
    (factory_dir / "policies" / "x.md").write_text("policy x\n", encoding="utf-8")
    (factory_dir / "templates").mkdir()
    (factory_dir / "templates" / "y.md").write_text("template y\n", encoding="utf-8")

    tools_dir = src / "tools" / "agent"
    tools_dir.mkdir(parents=True)
    z = tools_dir / "z"
    z.write_text("#!/usr/bin/env python3\nprint('z')\n", encoding="utf-8")
    z.chmod(0o755)

    return src


def _make_temp_plugin(tmp_path: pathlib.Path) -> pathlib.Path:
    """A throwaway plugin tree so the sync writes here, never the real repo.

    sync-from-source.py derives its plugin root from ``__file__`` (its own
    location), so running a COPY of the script from this temp dir makes it
    materialize into the temp tree. The real repo is only read (to copy the
    script) and never mutated — no git checkout/clean cleanup needed.
    """
    plugin = tmp_path / "plugin"
    (plugin / "scripts").mkdir(parents=True)
    shutil.copy2(PLUGIN_SCRIPT, plugin / "scripts" / "sync-from-source.py")
    for d in ("skills", "hooks", "factory"):
        (plugin / d).mkdir()
    return plugin


def test_sync_materializes_skills_hooks_and_payload(tmp_path):
    src = _make_fake_source(tmp_path)
    plugin = _make_temp_plugin(tmp_path)

    result = subprocess.run(
        [sys.executable, str(plugin / "scripts" / "sync-from-source.py"), "--source", str(src)],
        cwd=str(plugin),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr

    # skills
    assert (plugin / "skills" / "demo" / "SKILL.md").is_file()
    assert (plugin / "skills" / "demo" / "SKILL.md").read_text() == "# demo skill\n"

    # hook
    hooks_doc = json.loads((plugin / "hooks" / "hooks.json").read_text())
    assert "SessionStart" in hooks_doc["hooks"]
    assert hooks_doc["hooks"]["SessionStart"][0]["hooks"][0]["command"] == "echo hi"

    # payload
    assert (plugin / "factory" / "README.md").read_text() == "# factory readme\n"
    assert (plugin / "factory" / "config.yaml").read_text() == "key: value\n"
    assert (plugin / "factory" / "policies" / "x.md").read_text() == "policy x\n"
    assert (plugin / "factory" / "templates" / "y.md").read_text() == "template y\n"

    z_dst = plugin / "factory" / "tools" / "z"
    assert z_dst.is_file()
    assert os.access(z_dst, os.X_OK)
