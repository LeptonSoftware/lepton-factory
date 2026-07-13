import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]

def test_sessionstart_hook_reminds_about_agents_md():
    h = json.loads((ROOT / "hooks/hooks.json").read_text())
    entries = h["hooks"]["SessionStart"]
    cmd = entries[0]["hooks"][0]["command"]
    assert "AGENTS.md" in cmd and "state.yaml" in cmd
    assert entries[0]["matcher"] == "startup|resume|compact"

def test_hook_has_firstrun_nudge():
    h = json.loads((ROOT/"hooks/hooks.json").read_text())
    cmds = " ".join(e["hooks"][0]["command"] for e in h["hooks"]["SessionStart"])
    assert "factory-init" in cmds and ".factory" in cmds
