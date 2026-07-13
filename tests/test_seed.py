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
