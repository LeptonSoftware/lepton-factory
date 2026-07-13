# tests/test_manifest.py
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]

def test_plugin_manifest_valid():
    m = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
    assert m["name"] == "lepton-factory"
    assert m["version"].count(".") == 2            # semver
    assert m["description"]

def test_marketplace_lists_plugin():
    mk = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    assert mk["name"] == "lepton-factory"
    names = [p["name"] for p in mk["plugins"]]
    assert "lepton-factory" in names
