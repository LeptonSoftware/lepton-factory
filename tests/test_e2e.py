import importlib.util, json, os, pathlib, shutil, subprocess
ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("fi", ROOT / "scripts/factory_init.py")
fi = importlib.util.module_from_spec(spec); spec.loader.exec_module(fi)

def test_fresh_install_against_real_payload(tmp_path):
    repo = tmp_path / "adopter"; repo.mkdir()
    fi.run(repo, ROOT / "factory", upgrade=False)
    # real payload landed at repo-relative paths the skills expect
    assert (repo / ".factory/README.md").read_text().startswith("<!--")
    assert (repo / ".factory/policies/testing.md").is_file()
    for t in ["state","work-order","contract","implementation-plan"]:
        assert list((repo / ".factory/templates").glob(f"{t}.*"))
    exe = repo / "tools/agent/validate-work-order"
    assert exe.is_file() and os.access(exe, os.X_OK)
    assert not (exe.read_text().startswith("<!--"))        # tool not stamped
    # tools/agent/README.md is a .md file but lives under the tools payload,
    # which is do_stamp=False — it must NOT carry the managed banner.
    tools_readme = repo / "tools/agent/README.md"
    assert tools_readme.is_file()
    assert not tools_readme.read_text().startswith("<!--")
    for d in ["work-orders","feedback","indexes","overrides"]:
        assert (repo / ".factory" / d / ".gitkeep").is_file()
    assert "wo-execute" in (repo / "AGENTS.md").read_text()

def test_clone_portability(tmp_path):
    # simulate `git clone` to a machine WITHOUT the plugin cache: copy only the repo
    repo = tmp_path / "adopter"; repo.mkdir()
    fi.run(repo, ROOT / "factory", upgrade=False)
    clone = tmp_path / "clone"
    shutil.copytree(repo, clone)
    # no plugin, no payload — the harness content is still fully present
    assert (clone / ".factory/README.md").is_file()
    assert (clone / "tools/agent/_lib.py").is_file()

def test_upgrade_preserves_edit_against_real_payload(tmp_path):
    repo = tmp_path / "adopter"; repo.mkdir()
    fi.run(repo, ROOT / "factory", upgrade=False)
    pol = repo / ".factory/policies/security.md"
    pol.write_text(pol.read_text() + "\n<!-- team override note -->\n")
    s = fi.run(repo, ROOT / "factory", upgrade=True)
    assert ".factory/policies/security.md" in s["skipped_edited"]
    assert "team override note" in pol.read_text()

def test_seed_produces_validator_passing_repo(tmp_path):
    repo = tmp_path/"adopter"; repo.mkdir()
    subprocess.run(["git","init","-q"], cwd=repo, check=True)
    fi.run(repo, ROOT/"factory", upgrade=False)          # scaffold + docs skeleton + tools
    s = { "tier":"internal","stack":"node","area":"CORE",
          "feature":{"slug":"greeting-cli","title":"Greeting CLI","user_story":"As a user I greet",
                     "reqs":[{"id_seq":1,"statement":"prints a greeting","acs":["prints hi to stdout"]}]},
          "container":{"slug":"app","name":"APP","title":"App","summary":"the app",
                       "owner":"app-line","applies_to":["apps/app/**"],"body":"The app container."},
          "overview":{"product_description":"A greeter."}, "glossary":[{"term":"Greeting","definition":"a hi"}]}
    seedfile = tmp_path/"seed.json"; seedfile.write_text(json.dumps(s))
    rc = fi.main(["--target", str(repo), "--seed", str(seedfile), "--tier","internal","--stack","node"])
    assert rc == 0
    assert (repo/"docs/architecture/containers/app.md").is_file()
    assert (repo/".factory/work-orders/WO-0001/work-order.md").is_file()

def test_missing_seed_file_returns_rc2(tmp_path):
    repo = tmp_path/"adopter"; repo.mkdir()
    rc = fi.main(["--target", str(repo), "--seed", "/nonexistent.json",
                  "--tier", "internal", "--stack", "node"])
    assert rc == 2
    # scaffolding still ran before the seed load failed
    assert (repo/".factory/README.md").is_file()
