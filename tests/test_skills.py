import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPECTED = {
    "adversarial-qa",
    "audit-verification",
    "challenge-plan",
    "clarify-intent",
    "codebase-design",
    "compile-contract",
    "domain-model",
    "converge-work-order",
    "execute-slice",
    "factory-learn",
    "factory-sweep",
    "finish-work-order",
    "night-shift",
    "review-slice",
    "synthesize-review",
    "systematic-debugging",
    "wayfinder",
    "wo-author",
    "wo-execute",
    "wo-review",
    "write-implementation-plan",
    "writing-factory-skills",
}


def test_all_skills_present_with_frontmatter():
    skills = {p.name for p in (ROOT / "skills").iterdir() if p.is_dir()}
    assert skills == EXPECTED
    for name in EXPECTED:
        text = (ROOT / "skills" / name / "SKILL.md").read_text()
        assert text.startswith("---"), f"{name} missing frontmatter"
        assert "name:" in text and "description:" in text
