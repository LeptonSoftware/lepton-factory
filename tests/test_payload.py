import pathlib, os
ROOT = pathlib.Path(__file__).resolve().parents[1]
F = ROOT / "factory"

def test_payload_shape():
    assert (F / "README.md").is_file()
    assert (F / "config.yaml").is_file()
    for p in ["architecture","code-reuse","delivery","documentation",
              "model-routing","security","testing"]:
        assert (F / "policies" / f"{p}.md").is_file()
    for t in ["checklist","context","contract","feedback","implementation-plan",
              "incident","release-note","review-log","state","work-order"]:
        assert list(F.glob(f"templates/{t}.*")), f"missing template {t}"

def test_tools_present_and_executable():
    tools = F / "tools"
    for exe in ["init-work-order","update-state","validate-work-order",
                "check-traceability","generate-indexes","risk-tier",
                "agent-review","check-drift","review-package"]:
        p = tools / exe
        assert p.is_file(), f"missing tool {exe}"
        assert os.access(p, os.X_OK), f"{exe} not executable"
    assert (tools / "_lib.py").is_file()
