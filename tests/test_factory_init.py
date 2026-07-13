import importlib.util, pathlib, re
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

def test_copy_payload_preserves_unicode_utf8(tmp_path):
    payload = tmp_path / "payload"; (payload / "policies").mkdir(parents=True)
    (payload / "README.md").write_text("# Manual — em dash\n", encoding="utf-8")
    (payload / "policies" / "testing.md").write_text("policy — dashy\n", encoding="utf-8")
    target = tmp_path / "repo"; target.mkdir()
    fi.copy_payload(payload, target, upgrade=False)
    got = (target / ".factory/README.md").read_text(encoding="utf-8")
    assert "—" in got                      # em dash survived the copy
    assert "—" in (target / ".factory/policies/testing.md").read_text(encoding="utf-8")

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

def test_apply_block_handles_backslashes_in_block():
    block = r"path C:\1\2 and \g<x>"
    once = fi.apply_managed_block(None, block)
    assert block in once
    twice = fi.apply_managed_block(once, block)   # replace-path must not raise or corrupt
    assert twice == once
    assert block in twice

def test_write_routers(tmp_path):
    fi.write_routers(tmp_path)
    agents = (tmp_path / "AGENTS.md").read_text()
    assert "wo-execute" in agents and fi.MARK_START in agents
    assert "@AGENTS.md" in (tmp_path / "CLAUDE.md").read_text()

def test_run_fresh_then_upgrade_preserves_edits(tmp_path):
    payload = _payload(tmp_path); (payload / "config.yaml").write_text("version: 1\n")
    target = tmp_path / "repo"; target.mkdir()
    s1 = fi.run(target, payload, upgrade=False)
    assert s1["config_written"] is True
    assert (target / ".factory/.factory-manifest.json").is_file()
    # adopter edits a managed policy, then upgrades
    pol = target / ".factory/policies/testing.md"
    pol.write_text(pol.read_text() + "\n<!-- local tweak -->\n")
    s2 = fi.run(target, payload, upgrade=True)
    assert ".factory/policies/testing.md" in s2["skipped_edited"]
    assert "local tweak" in pol.read_text()             # preserved
    assert s2["config_written"] is False                # config never re-written

def test_main_returns_zero(tmp_path):
    payload = _payload(tmp_path); (payload / "config.yaml").write_text("version: 1\n")
    target = tmp_path / "repo"; target.mkdir()
    rc = fi.main(["--target", str(target), "--payload", str(payload)])
    assert rc == 0 and (target / "AGENTS.md").is_file()

def test_docs_skeleton_materialized(tmp_path):
    payload = tmp_path/"payload"; (payload/"docs-skeleton/architecture/containers").mkdir(parents=True)
    (payload/"docs-skeleton/architecture/containers/TEMPLATE.md").write_text("# BP-CONT-<NAME>\n")
    (payload/"docs-skeleton/product/features").mkdir(parents=True)
    (payload/"docs-skeleton/product/features/README.md").write_text("FRD guide\n")
    (payload/"docs-skeleton/domain").mkdir(parents=True)
    (payload/"docs-skeleton/domain/glossary.md").write_text("# Glossary\n")
    (payload/"README.md").write_text("# m\n"); (payload/"config.yaml").write_text("v: 1\n")
    (payload/"policies").mkdir(); (payload/"templates").mkdir(); (payload/"tools").mkdir()
    target = tmp_path/"repo"; target.mkdir()
    fi.copy_docs_skeleton(payload, target)
    assert (target/"docs/architecture/containers/TEMPLATE.md").read_text().startswith("<!--")  # managed banner
    assert (target/"docs/product/features/README.md").is_file()
    # glossary is seed-once: pre-existing content preserved
    (target/"docs/domain/glossary.md").write_text("MY TERMS\n")
    fi.copy_docs_skeleton(payload, target)
    assert (target/"docs/domain/glossary.md").read_text() == "MY TERMS\n"

import importlib.util, subprocess
_seedspec = importlib.util.spec_from_file_location("seed", ROOT/"scripts/seed.py")
_seed = importlib.util.module_from_spec(_seedspec); _seedspec.loader.exec_module(_seed)

def test_apply_seed_writes_kebab_artifacts(tmp_path):
    target = tmp_path/"repo"; (target/".factory").mkdir(parents=True)
    (target/".factory/config.yaml").write_text("blueprints:\n")
    s = { "tier":"internal","stack":"node","area":"CORE",
          "feature":{"slug":"greeting-cli","title":"Greeting CLI","user_story":"u",
                     "reqs":[{"id_seq":1,"statement":"greet","acs":["prints hi"]}]},
          "container":{"slug":"app","name":"APP","title":"App","summary":"s",
                       "owner":"app-line","applies_to":["apps/app/**"],"body":"b"},
          "overview":{"product_description":"p"}, "glossary":[{"term":"Greeting","definition":"d"}]}
    written = fi.apply_seed(s, target, "2026-07-13")
    assert (target/"docs/architecture/containers/app.md").is_file()
    assert (target/"docs/product/features/greeting-cli/requirements.md").is_file()
    cfg_text = (target/".factory/config.yaml").read_text()
    assert "BP-CONT-APP" in cfg_text
    # config mirror uses the real `paths:` list convention (matches check-drift's
    # spec.get("paths") — NOT the doc front-matter's `applies_to:` key).
    assert "    paths:\n      - apps/app/**\n" in cfg_text

def test_apply_seed_preserves_existing_blueprints_entries(tmp_path):
    # Regression: apply_seed used to append a NEW top-level `blueprints:` block.
    # Duplicate top-level YAML keys resolve last-write-wins, so pre-existing
    # blueprint entries silently vanished from the parsed config. The new entry
    # must be inserted UNDER the existing `blueprints:` key instead.
    target = tmp_path/"repo"; (target/".factory").mkdir(parents=True)
    (target/".factory/config.yaml").write_text(
        "version: 1\n\nblueprints:\n  BP-CONT-EXISTING:\n    applies_to: [x/**]\n    owner: o\n")
    s = { "tier":"internal","stack":"node","area":"CORE",
          "feature":{"slug":"greeting-cli","title":"Greeting CLI","user_story":"u",
                     "reqs":[{"id_seq":1,"statement":"greet","acs":["prints hi"]}]},
          "container":{"slug":"app","name":"APP","title":"App","summary":"s",
                       "owner":"app-line","applies_to":["apps/app/**"],"body":"b"},
          "overview":{"product_description":"p"}, "glossary":[{"term":"Greeting","definition":"d"}]}
    fi.apply_seed(s, target, "2026-07-13")
    text = (target/".factory/config.yaml").read_text()
    assert "BP-CONT-EXISTING" in text
    assert "BP-CONT-APP" in text
    assert len(re.findall(r"^blueprints:\s*$", text, re.MULTILINE)) == 1
    # seeded entry uses the real `paths:` list convention
    assert "    paths:\n      - apps/app/**\n" in text

def test_mirror_blueprint_into_config_creates_key_when_absent():
    text = fi.mirror_blueprint_into_config("version: 1\n", "BP-CONT-APP",
                                           {"paths": ["apps/app/**"], "owner": "o"})
    assert text.count("blueprints:") == 1
    assert "BP-CONT-APP" in text
    assert "    paths:\n      - apps/app/**\n" in text

def test_mirror_blueprint_into_config_idempotent():
    text = fi.mirror_blueprint_into_config("blueprints:\n", "BP-CONT-APP",
                                           {"paths": ["a/**"], "owner": "o"})
    twice = fi.mirror_blueprint_into_config(text, "BP-CONT-APP",
                                            {"paths": ["a/**"], "owner": "o"})
    assert twice == text

def test_fill_section_replaces_content_keeps_order():
    md = "# T\n\n## A\n\nold a\n\n## B\n\nold b\n\n## C\n\nold c\n"
    out = fi.fill_section(md, "B", "new b")
    headings = re.findall(r"^## .*$", out, re.MULTILINE)
    assert headings == ["## A", "## B", "## C"]
    assert "new b" in out and "old b" not in out
    assert "old a" in out and "old c" in out

def test_fill_section_missing_heading_raises():
    import pytest
    with pytest.raises(ValueError):
        fi.fill_section("# T\n\n## A\n\nx\n", "Missing", "y")

def test_author_wo1_fills_sections_in_place_no_duplicate_headings(tmp_path):
    payload = _payload(tmp_path)
    for name in ["templates", "docs-skeleton"]:
        (payload/name).mkdir(exist_ok=True)
    (payload/"config.yaml").write_text("version: 1\n")
    target = tmp_path/"repo"; target.mkdir()
    fi.run(target, payload, upgrade=False)
    # scaffold a real tools/agent + templates from the plugin's own factory/ dir
    real_factory = ROOT/"factory"
    for rel in ["templates", "tools"]:
        src = real_factory/rel
        dst = target/(".factory/templates" if rel == "templates" else "tools/agent")
        if dst.exists():
            import shutil as _shutil; _shutil.rmtree(dst)
        import shutil as _shutil; _shutil.copytree(src, dst)
    (target/".factory/config.yaml").write_text((real_factory/"config.yaml").read_text())
    s = { "tier":"internal","stack":"node","area":"CORE",
          "feature":{"slug":"greeting-cli","title":"Greeting CLI","user_story":"u",
                     "reqs":[{"id_seq":1,"statement":"greet","acs":["prints hi"]}]},
          "container":{"slug":"app","name":"APP","title":"App","summary":"s",
                       "owner":"app-line","applies_to":["apps/app/**"],"body":"b"}}
    fi.author_wo1(s, target, "2026-07-13")
    wo = target/".factory/work-orders/WO-0001/work-order.md"
    text = wo.read_text()
    headings = re.findall(r"^## .*$", text, re.MULTILINE)
    assert headings == ["## Summary", "## In Scope", "## Out of Scope",
                        "## Requirements", "## Blueprints",
                        "## Decision classification", "## E2E Acceptance Tests"]
    assert "REQ-CORE-001" in text and "BP-CONT-APP" in text
    # idempotent: re-running does not duplicate or append anything
    fi.author_wo1(s, target, "2026-07-13")
    text2 = wo.read_text()
    assert re.findall(r"^## .*$", text2, re.MULTILINE) == headings
    assert text2.count("REQ-CORE-001") == 1
