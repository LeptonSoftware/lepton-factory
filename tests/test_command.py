import pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]

def test_command_invokes_script_via_plugin_root():
    txt = (ROOT / "commands/factory-init.md").read_text()
    assert "${CLAUDE_PLUGIN_ROOT}/scripts/factory_init.py" in txt
    assert "--target" in txt and "$(pwd)" in txt
    assert "--upgrade" in txt          # documents upgrade path
    assert txt.lstrip().startswith("---")   # frontmatter present

def test_command_is_a_wizard():
    t = (ROOT/"commands/factory-init.md").read_text()
    for token in ["clarify-intent","tier","stack","--seed","WO-0001","one question at a time"]:
        assert token in t, token
