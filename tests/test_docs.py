import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_readme_has_install_flow():
    r = (ROOT / "README.md").read_text()
    assert "/plugin marketplace add LeptonSoftware/vinxi-factory" in r
    assert "/plugin install vinxi-factory@vinxi-factory" in r
    assert "/factory-init" in r
    assert "Python 3" in r


def test_changelog_has_first_version():
    assert "0.1.0" in (ROOT / "CHANGELOG.md").read_text()
