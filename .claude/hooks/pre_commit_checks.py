#!/usr/bin/env python3
"""Pre-commit checks for Claude Code hooks"""

import argparse
import subprocess
import sys


def run_command(cmd, description):
    """Run a command and handle its output"""
    print(f"🔍 {description}...")
    try:
        result = subprocess.run(
            cmd, shell=True, check=True, capture_output=True, text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        return False


def run_format_check():
    """Run format check and attempt to fix if needed"""
    print("🎨 Checking format...")
    if not run_command("just fmt", "Format check"):
        print("❌ Format check failed. Running format fix...")
        if run_command("just fmt", "Format fix"):
            print("✅ Format fixed")
        else:
            return False
    return True


def run_lint():
    """Run lint and attempt to fix if needed"""
    print("🔍 Running lint...")
    if not run_command("just lint", "Lint check"):
        print("❌ Lint failed. Please fix before committing.")
        return False
    return True


def run_tests():
    """Run tests"""
    print("🧪 Running tests...")
    if not run_command("npm test", "Tests"):
        print("❌ Tests failed. Please fix before committing.")
        return False
    return True


def run_pre_commit_checks(format_only=False, no_tests=False):
    """Run pre-commit checks programmatically

    Args:
        format_only: If True, run only format and lint checks
        no_tests: If True, skip tests

    Returns:
        bool: True if all checks passed, False otherwise
    """
    print("Running pre-commit checks...")

    # Run format check
    if not run_format_check():
        return False

    # Run lint
    if not run_lint():
        return False

    # Run tests if requested
    if not format_only and not no_tests:
        if not run_tests():
            return False

    print("✅ All checks passed!")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Pre-commit checks for Claude Code hooks"
    )
    parser.add_argument(
        "--format-only", action="store_true", help="Run only format and lint checks"
    )
    parser.add_argument("--no-tests", action="store_true", help="Skip tests")

    args = parser.parse_args()

    success = run_pre_commit_checks(
        format_only=args.format_only, no_tests=args.no_tests
    )

    sys.exit(0 if success else 2)


if __name__ == "__main__":
    main()
