import importlib.util, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("fi", ROOT / "scripts/factory_init.py")
fi = importlib.util.module_from_spec(spec); spec.loader.exec_module(fi)

def test_banner_md_is_html_comment():
    b = fi.banner_for(".factory/policies/testing.md")
    assert b.startswith("<!--") and b.rstrip().endswith("-->")
    assert "do not hand-edit" in b.lower()

def test_banner_yaml_is_hash_comment():
    b = fi.banner_for(".factory/config.yaml")
    assert all(line.startswith("#") for line in b.strip().splitlines())

def test_banner_empty_for_python():
    assert fi.banner_for("tools/agent/init-work-order") == ""

def test_stamp_prepends_only_for_supported_types():
    md = fi.stamp("# Title\n", ".factory/README.md")
    assert md.startswith("<!--") and "# Title" in md
    py = fi.stamp("#!/usr/bin/env python3\n", "tools/agent/x")
    assert py == "#!/usr/bin/env python3\n"

def test_manifest_roundtrip(tmp_path):
    fi.write_manifest(tmp_path, {"b": "2", "a": "1"})
    assert fi.read_manifest(tmp_path) == {"a": "1", "b": "2"}
    raw = (tmp_path / ".factory/.factory-manifest.json").read_text()
    assert raw.index('"a"') < raw.index('"b"')     # sorted

def test_read_manifest_absent(tmp_path):
    assert fi.read_manifest(tmp_path) == {}

def test_sha_stable():
    assert fi.sha256_text("x") == fi.sha256_text("x")
    assert fi.sha256_text("x") != fi.sha256_text("y")

def _payload(tmp_path):
    p = tmp_path / "payload"
    (p / "policies").mkdir(parents=True)
    (p / "tools").mkdir(parents=True)
    (p / "README.md").write_text("# Manual\n")
    (p / "policies" / "testing.md").write_text("# Testing\n")
    tool = p / "tools" / "init-work-order"
    tool.write_text("#!/usr/bin/env python3\nprint('x')\n")
    tool.chmod(0o755)
    return p

def test_fresh_install_copies_and_stamps(tmp_path):
    payload = _payload(tmp_path); target = tmp_path / "repo"; target.mkdir()
    report = fi.copy_payload(payload, target, upgrade=False)
    readme = (target / ".factory/README.md").read_text()
    assert readme.startswith("<!--")                        # stamped
    tool = target / "tools/agent/init-work-order"
    assert tool.read_text().startswith("#!/usr/bin/env python3")  # NOT stamped
    import os; assert os.access(tool, os.X_OK)               # exec bit preserved
    assert ".factory/README.md" in report["written"]
    assert report["manifest"][".factory/README.md"] == fi.sha256_text(readme)

def test_state_dirs_created(tmp_path):
    fi.ensure_state_dirs(tmp_path)
    for d in ["work-orders","feedback","indexes","overrides"]:
        assert (tmp_path / ".factory" / d / ".gitkeep").is_file()

def test_config_written_once_then_preserved(tmp_path):
    payload = tmp_path / "payload"; payload.mkdir()
    (payload / "config.yaml").write_text("version: 1\n")
    assert fi.install_config(payload, tmp_path) is True
    (tmp_path / ".factory/config.yaml").write_text("version: 1\nedited: true\n")
    assert fi.install_config(payload, tmp_path) is False        # not clobbered
    assert "edited: true" in (tmp_path / ".factory/config.yaml").read_text()

def test_apply_block_create_and_idempotent():
    once = fi.apply_managed_block(None, "HELLO")
    assert fi.MARK_START in once and "HELLO" in once and fi.MARK_END in once
    twice = fi.apply_managed_block(once, "HELLO")
    assert twice == once                                  # idempotent

def test_apply_block_preserves_outside_text():
    existing = "# My repo\n\n" + fi.apply_managed_block(None, "OLD") + "\n\nfooter\n"
    updated = fi.apply_managed_block(existing, "NEW")
    assert "# My repo" in updated and "footer" in updated
    assert "NEW" in updated and "OLD" not in updated

def test_write_routers(tmp_path):
    fi.write_routers(tmp_path)
    agents = (tmp_path / "AGENTS.md").read_text()
    assert "wo-execute" in agents and fi.MARK_START in agents
    assert "@AGENTS.md" in (tmp_path / "CLAUDE.md").read_text()
