import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


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


def test_sync_materializes_skills_hooks_and_payload(tmp_path):
    src = _make_fake_source(tmp_path)

    result = subprocess.run(
        [sys.executable, "scripts/sync-from-source.py", "--source", str(src)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr

    try:
        # skills
        assert (ROOT / "skills" / "demo" / "SKILL.md").is_file()
        assert (ROOT / "skills" / "demo" / "SKILL.md").read_text() == "# demo skill\n"

        # hook
        hooks_doc = json.loads((ROOT / "hooks" / "hooks.json").read_text())
        assert "SessionStart" in hooks_doc["hooks"]
        assert hooks_doc["hooks"]["SessionStart"][0]["hooks"][0]["command"] == "echo hi"

        # payload
        assert (ROOT / "factory" / "README.md").read_text() == "# factory readme\n"
        assert (ROOT / "factory" / "config.yaml").read_text() == "key: value\n"
        assert (ROOT / "factory" / "policies" / "x.md").read_text() == "policy x\n"
        assert (ROOT / "factory" / "templates" / "y.md").read_text() == "template y\n"

        z_dst = ROOT / "factory" / "tools" / "z"
        assert z_dst.is_file()
        assert os.access(z_dst, os.X_OK)
    finally:
        # restore the real plugin state via git so this test doesn't leave
        # the working tree dirty with fixture content
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
