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
