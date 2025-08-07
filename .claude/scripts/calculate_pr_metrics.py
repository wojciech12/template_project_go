#!/usr/bin/env python3
"""
Calculate PR metrics for weekly summary reports.
This script calculates average time between opening and merging PRs to main.

Supports two modes:
1. Date range: Analyze PRs merged between two dates
2. Git tags: Analyze PRs included in commits between two git references
"""

import json
import subprocess
import sys
from datetime import datetime
from typing import List, Dict, Set


def run_gh_command(cmd: List[str]) -> str:
    """Run a GitHub CLI command and return the output."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(cmd)}: {e}", file=sys.stderr)
        sys.exit(1)


def get_merged_prs_in_date_range(start_date: str, end_date: str) -> List[Dict]:
    """
    Get all PRs merged to main within the specified date range.

    Args:
        start_date: Start date in ISO format (e.g., "2025-07-10T14:30:00+02:00")
        end_date: End date in ISO format (e.g., "2025-07-16T13:00:00+02:00")

    Returns:
        List of PR dictionaries with timing information
    """
    # Get all merged PRs
    cmd = [
        "gh",
        "pr",
        "list",
        "--state",
        "merged",
        "--base",
        "main",
        "--json",
        "number,title,createdAt,mergedAt,author",
        "--limit",
        "100",
    ]

    output = run_gh_command(cmd)
    prs = json.loads(output)

    # Parse date range
    start_dt = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
    end_dt = datetime.fromisoformat(end_date.replace("Z", "+00:00"))

    filtered_prs = []

    for pr in prs:
        if not pr.get("mergedAt"):
            continue

        merged_at = datetime.fromisoformat(pr["mergedAt"].replace("Z", "+00:00"))

        # Filter PRs merged within the date range
        if start_dt <= merged_at <= end_dt:
            created_at = datetime.fromisoformat(pr["createdAt"].replace("Z", "+00:00"))
            time_to_merge = merged_at - created_at

            filtered_prs.append(
                {
                    "number": pr["number"],
                    "title": pr["title"],
                    "author": pr["author"]["login"],
                    "created_at": created_at,
                    "merged_at": merged_at,
                    "time_to_merge_hours": time_to_merge.total_seconds() / 3600,
                    "time_to_merge_days": time_to_merge.total_seconds() / (3600 * 24),
                }
            )

    return filtered_prs


def get_pr_review_times(prs: List[Dict]) -> List[Dict]:
    """
    Get the time to first review for each PR.

    Args:
        prs: List of PR dictionaries

    Returns:
        List of PRs with review timing information added
    """
    for pr in prs:
        # Get review timeline for this PR
        cmd = [
            "gh",
            "pr",
            "view",
            str(pr["number"]),
            "--json",
            "reviews,reviewRequests",
        ]

        try:
            output = run_gh_command(cmd)
            pr_details = json.loads(output)

            reviews = pr_details.get("reviews", [])

            if reviews:
                # Find the earliest review
                earliest_review = min(reviews, key=lambda r: r["submittedAt"])
                first_review_at = datetime.fromisoformat(
                    earliest_review["submittedAt"].replace("Z", "+00:00")
                )
                time_to_first_review = first_review_at - pr["created_at"]

                pr["first_review_at"] = first_review_at
                pr["time_to_first_review_hours"] = (
                    time_to_first_review.total_seconds() / 3600
                )
                pr["time_to_first_review_days"] = (
                    time_to_first_review.total_seconds() / (3600 * 24)
                )
            else:
                pr["first_review_at"] = None
                pr["time_to_first_review_hours"] = None
                pr["time_to_first_review_days"] = None

        except Exception as e:
            print(
                f"Warning: Could not get review details for PR #{pr['number']}: {e}",
                file=sys.stderr,
            )
            pr["first_review_at"] = None
            pr["time_to_first_review_hours"] = None
            pr["time_to_first_review_days"] = None

    return prs


def calculate_pr_metrics(start_date: str, end_date: str) -> Dict:
    """
    Calculate PR metrics for the given date range.

    Args:
        start_date: Start date in ISO format
        end_date: End date in ISO format

    Returns:
        Dictionary with calculated metrics
    """
    print(f"Fetching PRs merged between {start_date} and {end_date}...")

    # Get merged PRs in date range
    prs = get_merged_prs_in_date_range(start_date, end_date)

    if not prs:
        return {
            "total_prs": 0,
            "avg_time_to_merge_hours": 0,
            "avg_time_to_merge_days": 0,
            "avg_time_to_first_review_hours": 0,
            "avg_time_to_first_review_days": 0,
            "prs": [],
        }

    print(f"Found {len(prs)} merged PRs. Getting review timelines...")

    # Get review timing information
    prs = get_pr_review_times(prs)

    # Calculate averages
    total_merge_time = sum(pr["time_to_merge_hours"] for pr in prs)
    avg_merge_time_hours = total_merge_time / len(prs)
    avg_merge_time_days = avg_merge_time_hours / 24

    # Calculate average time to first review (only for PRs that got reviewed)
    reviewed_prs = [pr for pr in prs if pr["time_to_first_review_hours"] is not None]
    if reviewed_prs:
        total_review_time = sum(pr["time_to_first_review_hours"] for pr in reviewed_prs)
        avg_review_time_hours = total_review_time / len(reviewed_prs)
        avg_review_time_days = avg_review_time_hours / 24
    else:
        avg_review_time_hours = 0
        avg_review_time_days = 0

    return {
        "total_prs": len(prs),
        "reviewed_prs": len(reviewed_prs),
        "avg_time_to_merge_hours": avg_merge_time_hours,
        "avg_time_to_merge_days": avg_merge_time_days,
        "avg_time_to_first_review_hours": avg_review_time_hours,
        "avg_time_to_first_review_days": avg_review_time_days,
        "prs": prs,
    }


def format_metrics_output(metrics: Dict) -> str:
    """
    Format the metrics for inclusion in the weekly summary.

    Args:
        metrics: Dictionary with calculated metrics

    Returns:
        Formatted string for the Engineering Metrics section
    """
    if metrics["total_prs"] == 0:
        return "- No PRs were merged during this period"

    output = []
    output.append(f"- **{metrics['total_prs']} PRs merged** during this period")
    output.append(
        f"- **Avg time to merge**: {metrics['avg_time_to_merge_hours']:.1f} hours ({metrics['avg_time_to_merge_days']:.1f} days)"
    )

    if metrics["reviewed_prs"] > 0:
        output.append(
            f"- **Avg time to first review**: {metrics['avg_time_to_first_review_hours']:.1f} hours ({metrics['avg_time_to_first_review_days']:.1f} days)"
        )
        output.append(
            f"- **{metrics['reviewed_prs']}/{metrics['total_prs']} PRs** received reviews"
        )
    else:
        output.append("- **No PRs received reviews** during this period")

    return "\n".join(output)


def get_commits_between_refs(start_ref: str, end_ref: str = "HEAD") -> Set[str]:
    """
    Get commit hashes between two git references.

    Args:
        start_ref: Starting git reference (tag, commit hash, branch)
        end_ref: Ending git reference (defaults to HEAD)

    Returns:
        Set of commit hashes
    """
    cmd = ["git", "rev-list", f"{start_ref}..{end_ref}"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        commits = (
            set(result.stdout.strip().split("\n")) if result.stdout.strip() else set()
        )
        return commits
    except subprocess.CalledProcessError as e:
        print(
            f"Error getting commits between {start_ref} and {end_ref}: {e}",
            file=sys.stderr,
        )
        sys.exit(1)


def get_prs_for_commits(commits: Set[str]) -> List[Dict]:
    """
    Get PRs that contain the specified commits.

    Args:
        commits: Set of commit hashes

    Returns:
        List of PR dictionaries with timing information
    """
    if not commits:
        return []

    # Get all merged PRs
    cmd = [
        "gh",
        "pr",
        "list",
        "--state",
        "merged",
        "--base",
        "main",
        "--json",
        "number,title,createdAt,mergedAt,author,mergeCommit",
        "--limit",
        "200",
    ]

    output = run_gh_command(cmd)
    all_prs = json.loads(output)

    matching_prs = []

    for pr in all_prs:
        if not pr.get("mergedAt") or not pr.get("mergeCommit"):
            continue

        # Check if this PR's merge commit or any of its commits are in our set
        merge_commit = pr["mergeCommit"]["oid"]

        # Get commits in this PR
        try:
            pr_commits_cmd = [
                "gh",
                "pr",
                "view",
                str(pr["number"]),
                "--json",
                "commits",
            ]
            pr_output = run_gh_command(pr_commits_cmd)
            pr_data = json.loads(pr_output)
            pr_commit_oids = {commit["oid"] for commit in pr_data.get("commits", [])}
            pr_commit_oids.add(merge_commit)

            # Check if any PR commits are in our target commit set
            if commits.intersection(pr_commit_oids):
                created_at = datetime.fromisoformat(
                    pr["createdAt"].replace("Z", "+00:00")
                )
                merged_at = datetime.fromisoformat(
                    pr["mergedAt"].replace("Z", "+00:00")
                )
                time_to_merge = merged_at - created_at

                matching_prs.append(
                    {
                        "number": pr["number"],
                        "title": pr["title"],
                        "author": pr["author"]["login"],
                        "created_at": created_at,
                        "merged_at": merged_at,
                        "time_to_merge_hours": time_to_merge.total_seconds() / 3600,
                        "time_to_merge_days": time_to_merge.total_seconds()
                        / (3600 * 24),
                    }
                )
        except Exception as e:
            print(
                f"Warning: Could not get commits for PR #{pr['number']}: {e}",
                file=sys.stderr,
            )
            continue

    return matching_prs


def calculate_pr_metrics_by_refs(start_ref: str, end_ref: str = "HEAD") -> Dict:
    """
    Calculate PR metrics for PRs between two git references.

    Args:
        start_ref: Starting git reference
        end_ref: Ending git reference (defaults to HEAD)

    Returns:
        Dictionary with calculated metrics
    """
    print(f"Fetching commits between {start_ref} and {end_ref}...")

    # Get commits between references
    commits = get_commits_between_refs(start_ref, end_ref)

    if not commits:
        print(f"No commits found between {start_ref} and {end_ref}")
        return {
            "total_prs": 0,
            "avg_time_to_merge_hours": 0,
            "avg_time_to_merge_days": 0,
            "avg_time_to_first_review_hours": 0,
            "avg_time_to_first_review_days": 0,
            "prs": [],
        }

    print(f"Found {len(commits)} commits. Finding associated PRs...")

    # Get PRs for these commits
    prs = get_prs_for_commits(commits)

    if not prs:
        print("No PRs found for the specified commit range")
        return {
            "total_prs": 0,
            "avg_time_to_merge_hours": 0,
            "avg_time_to_merge_days": 0,
            "avg_time_to_first_review_hours": 0,
            "avg_time_to_first_review_days": 0,
            "prs": [],
        }

    print(f"Found {len(prs)} PRs. Getting review timelines...")

    # Get review timing information
    prs = get_pr_review_times(prs)

    # Calculate averages
    total_merge_time = sum(pr["time_to_merge_hours"] for pr in prs)
    avg_merge_time_hours = total_merge_time / len(prs)
    avg_merge_time_days = avg_merge_time_hours / 24

    # Calculate average time to first review (only for PRs that got reviewed)
    reviewed_prs = [pr for pr in prs if pr["time_to_first_review_hours"] is not None]
    if reviewed_prs:
        total_review_time = sum(pr["time_to_first_review_hours"] for pr in reviewed_prs)
        avg_review_time_hours = total_review_time / len(reviewed_prs)
        avg_review_time_days = avg_review_time_hours / 24
    else:
        avg_review_time_hours = 0
        avg_review_time_days = 0

    return {
        "total_prs": len(prs),
        "reviewed_prs": len(reviewed_prs),
        "avg_time_to_merge_hours": avg_merge_time_hours,
        "avg_time_to_merge_days": avg_merge_time_days,
        "avg_time_to_first_review_hours": avg_review_time_hours,
        "avg_time_to_first_review_days": avg_review_time_days,
        "prs": prs,
    }


def main():
    """Main function to run the PR metrics calculation."""
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage:")
        print(
            "  Date mode:  python3 calculate_pr_metrics.py --dates <start_date> <end_date>"
        )
        print(
            "  Tag mode:   python3 calculate_pr_metrics.py --refs <start_ref> [end_ref]"
        )
        print("")
        print("Examples:")
        print(
            "  python3 calculate_pr_metrics.py --dates '2025-07-10T14:30:00+02:00' '2025-07-16T13:00:00+02:00'"
        )
        print("  python3 calculate_pr_metrics.py --refs v0.1.3 v0.1.4")
        print("  python3 calculate_pr_metrics.py --refs v0.1.3")
        print("  python3 calculate_pr_metrics.py --refs abc123def HEAD")
        sys.exit(1)

    mode = sys.argv[1]

    try:
        if mode == "--dates":
            if len(sys.argv) != 4:
                print("Date mode requires exactly 2 arguments: start_date and end_date")
                sys.exit(1)

            start_date = sys.argv[2]
            end_date = sys.argv[3]
            metrics = calculate_pr_metrics(start_date, end_date)
            print(f"\nAnalyzing PRs merged between {start_date} and {end_date}")

        elif mode == "--refs":
            if len(sys.argv) == 3:
                start_ref = sys.argv[2]
                end_ref = "HEAD"
            elif len(sys.argv) == 4:
                start_ref = sys.argv[2]
                end_ref = sys.argv[3]
            else:
                print("Ref mode requires 1 or 2 arguments: start_ref [end_ref]")
                sys.exit(1)

            metrics = calculate_pr_metrics_by_refs(start_ref, end_ref)
            print(f"\nAnalyzing PRs between git references {start_ref} and {end_ref}")

        else:
            print(f"Unknown mode: {mode}. Use --dates or --refs")
            sys.exit(1)

        print("\n" + "=" * 60)
        print("PR METRICS SUMMARY")
        print("=" * 60)
        print(format_metrics_output(metrics))

        if metrics["prs"]:
            print("\nDETAILED PR LIST:")
            print("-" * 40)
            for pr in metrics["prs"]:
                print(f"PR #{pr['number']}: {pr['title']}")
                print(f"  Author: {pr['author']}")
                print(
                    f"  Time to merge: {pr['time_to_merge_hours']:.1f}h ({pr['time_to_merge_days']:.1f}d)"
                )
                if pr["time_to_first_review_hours"] is not None:
                    print(
                        f"  Time to first review: {pr['time_to_first_review_hours']:.1f}h ({pr['time_to_first_review_days']:.1f}d)"
                    )
                else:
                    print("  No reviews received")
                print()

    except Exception as e:
        print(f"Error calculating PR metrics: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
