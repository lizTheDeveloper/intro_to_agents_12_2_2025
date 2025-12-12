from pathlib import Path


def test_deploy_to_staging_does_not_affect_prod(tmp_path, monkeypatch):
    # Run deploy script in a temp working dir to avoid touching repo files
    import subprocess
    import sys

    # Copy deploy/ directory structure into temp
    repo_root = Path(__file__).resolve().parents[1]
    deploy_dir = repo_root / "deploy"

    work = tmp_path / "work"
    work.mkdir()

    # minimal copy of deploy script + env files
    (work / "deploy").mkdir()
    for name in ["deploy.py", "env.dev", "env.staging", "env.prod"]:
        (work / "deploy" / name).write_text((deploy_dir / name).read_text())

    # deploy v1 to prod
    subprocess.check_call([sys.executable, "deploy/deploy.py", "deploy", "--env", "prod", "--version", "v1"], cwd=work)

    # deploy v2 to staging
    subprocess.check_call([sys.executable, "deploy/deploy.py", "deploy", "--env", "staging", "--version", "v2"], cwd=work)

    prod_current = (work / "deploy" / "current" / "prod").resolve()
    staging_current = (work / "deploy" / "current" / "staging").resolve()

    assert prod_current.name == "v1"
    assert staging_current.name == "v2"


def test_rollback_restores_previous_good_version(tmp_path):
    import subprocess
    import sys

    repo_root = Path(__file__).resolve().parents[1]
    deploy_dir = repo_root / "deploy"

    work = tmp_path / "work"
    work.mkdir()

    (work / "deploy").mkdir()
    for name in ["deploy.py", "env.dev", "env.staging", "env.prod"]:
        (work / "deploy" / name).write_text((deploy_dir / name).read_text())

    subprocess.check_call([sys.executable, "deploy/deploy.py", "deploy", "--env", "prod", "--version", "good"], cwd=work)
    subprocess.check_call([sys.executable, "deploy/deploy.py", "deploy", "--env", "prod", "--version", "bad"], cwd=work)

    # rollback to good
    subprocess.check_call([sys.executable, "deploy/deploy.py", "rollback", "--env", "prod", "--version", "good"], cwd=work)

    prod_current = (work / "deploy" / "current" / "prod").resolve()
    assert prod_current.name == "good"
