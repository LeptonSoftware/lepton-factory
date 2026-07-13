import importlib.util, pathlib, json
ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("seed", ROOT/"scripts/seed.py")
seed = importlib.util.module_from_spec(spec); spec.loader.exec_module(seed)

def _ok():
    return {"tier":"internal","stack":"node","area":"CORE",
            "feature":{"slug":"greeting-cli","title":"Greeting CLI","user_story":"u",
                       "reqs":[{"id_seq":1,"statement":"s","acs":["a1"]}]},
            "container":{"slug":"app","name":"APP","title":"App","summary":"s",
                         "owner":"app-line","applies_to":["apps/app/**"],"body":"b"},
            "overview":{"product_description":"p"}, "glossary":[{"term":"T","definition":"d"}]}

def test_valid_seed_has_no_errors():
    assert seed.validate_seed(_ok()) == []

def test_missing_field_reported():
    s = _ok(); del s["container"]
    errs = seed.validate_seed(s)
    assert any("container" in e for e in errs)

def test_bad_tier_reported():
    s = _ok(); s["tier"] = "prototype"       # out of scope in V1
    assert any("tier" in e for e in seed.validate_seed(s))

def test_frontmatter_stable_order():
    fm = seed.frontmatter({"title":"T","summary":"s","owners":["o"],
                           "applies_to":["a/**"],"status":"draft","last_verified":"2026-07-13"})
    assert fm.startswith("---\n") and fm.rstrip().endswith("---")
    assert fm.index("title") < fm.index("summary") < fm.index("owners")
    assert "owners: [o]" in fm and "applies_to: [a/**]" in fm

def test_build_doc_puts_id_in_heading():
    doc = seed.build_doc({"title":"BP-CONT-APP — App"}, "BP-CONT-APP: App", "body")
    assert "# BP-CONT-APP: App" in doc and doc.strip().endswith("body")

def test_profiles_load(tmp_path):
    root = ROOT  # real profiles shipped in factory/profiles/
    p = seed.load_profile(root/"factory", "node")
    assert "owner_default" in p

def test_render_container(tmp_path):
    dst_rel, content = seed.render_container(_ok(), "2026-07-13", ROOT/"factory")
    assert dst_rel == "docs/architecture/containers/app.md"
    assert "# BP-CONT-APP: App" in content
    assert "applies_to: [apps/app/**]" in content
    bpid, meta = seed.config_blueprint_line(_ok(), ROOT/"factory")
    assert bpid == "BP-CONT-APP" and meta["applies_to"] == ["apps/app/**"]

def test_owner_defaults_consistent_when_omitted():
    s = _ok(); del s["container"]["owner"]      # node stack -> profile owner_default "app-line"
    _, content = seed.render_container(s, "2026-07-13", ROOT/"factory")
    _, meta = seed.config_blueprint_line(s, ROOT/"factory")
    assert "owners: [app-line]" in content
    assert meta["owner"] == "app-line"          # doc and config agree

import re
def test_render_frd_ids_match_grammar():
    dst_rel, content = seed.render_frd(_ok(), "2026-07-13")
    assert dst_rel == "docs/product/features/greeting-cli/requirements.md"
    assert re.search(r"REQ-CORE-001\b", content)
    assert re.search(r"AC-CORE-001\.1\b", content)
    assert "User Story" in content
