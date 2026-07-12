import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]

def test_sessionstart_hook_reminds_about_agents_md():
    h = json.loads((ROOT / "hooks/hooks.json").read_text())
    entries = h["hooks"]["SessionStart"]
    cmd = entries[0]["hooks"][0]["command"]
    assert "AGENTS.md" in cmd and "state.yaml" in cmd
    assert entries[0]["matcher"] == "startup|resume|compact"
