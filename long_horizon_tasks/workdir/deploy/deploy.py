#!/usr/bin/env python
from __future__ import annotations

import argparse
from pathlib import Path


def deploy(env: str, version: str) -> None:
    env_dir = Path("deploy")
    env_file = env_dir / f"env.{env}"
    if not env_file.exists():
        raise SystemExit(f"Unknown environment: {env}")

    releases = env_dir / "releases" / env
    releases.mkdir(parents=True, exist_ok=True)

    current = env_dir / "current" / env
    current.parent.mkdir(parents=True, exist_ok=True)

    target = releases / version
    target.mkdir(parents=True, exist_ok=True)

    # Simulate deployment by pointing current to version directory
    if current.exists() or current.is_symlink():
        current.unlink()
    current.symlink_to(target)


def rollback(env: str, version: str) -> None:
    env_dir = Path("deploy")
    releases = env_dir / "releases" / env
    target = releases / version
    if not target.exists():
        raise SystemExit(f"Unknown release version {version} for env {env}")

    current = env_dir / "current" / env
    current.parent.mkdir(parents=True, exist_ok=True)
    if current.exists() or current.is_symlink():
        current.unlink()
    current.symlink_to(target)


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("deploy")
    d.add_argument("--env", required=True, choices=["dev", "staging", "prod"])
    d.add_argument("--version", required=True)

    r = sub.add_parser("rollback")
    r.add_argument("--env", required=True, choices=["dev", "staging", "prod"])
    r.add_argument("--version", required=True)

    args = p.parse_args()
    if args.cmd == "deploy":
        deploy(args.env, args.version)
    else:
        rollback(args.env, args.version)


if __name__ == "__main__":
    main()
