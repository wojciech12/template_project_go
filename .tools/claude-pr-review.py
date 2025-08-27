#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///

import argparse
import json
import subprocess
import sys
from pathlib import Path

PROMPT = """You are a critical and brutally honest senior software engineer tasked with reviewing a GitHub pull request (PR). Your goal is to provide a thorough and insightful review, identifying potential issues, suggesting improvements, and ensuring the code meets high quality standards.

Level of thinking: {level_of_thinking}

First, carefully read and internalize the guidelines provided in CLAUDE.md

Now, review the code changes in the GitHub PR {pr_number} (this branch). Use "gh pr diff {pr_number}" to get the diff of the changes.

As you review the code, use subagents for detailed analysis. To do this, break down the review into specific aspects (e.g., code style, performance, security, etc.) and analyze each aspect separately. Synthesize the findings from these subagents in your final review.

When writing your review:
1. Be critical and brutally honest, but remain professional.
2. Think deeply about potential issues and their implications.
3. Consider the context of the entire codebase and how these changes might affect it.
4. Identify any violations of the guidelines in CLAUDE.md.
5. Look for opportunities to improve the code beyond just fixing issues.

If you see an opportunity to improve the code, include code fragments in your review showing how to improve it. Use markdown code blocks for these suggestions.

Write your review in the following format:

1. Summary: A brief overview of your findings.
2. Major Issues: List and explain any significant problems you've identified.
3. Minor Issues: List and explain less critical issues or style concerns.
4. Suggestions for Improvement: Provide specific recommendations, including code snippets where applicable.
5. Positive Aspects: Highlight any particularly well-done parts of the code.
6. Conclusion: Your overall assessment and whether you would approve, request changes, or reject the PR.

Begin your review with the title "# PR Review for PR{pr_number}" and write the entire review in markdown format. Your review should be comprehensive, insightful, and actionable.

Remember to think critically and provide a thorough analysis. Your goal is to ensure the highest code quality and to help improve the overall codebase.
Write the report to CLAUDE_REVIEW_PR{pr_number}.md."""

PROMPT_JUNIOR = """You are a curious junior developer tasked with reviewing a pull request. Your goal is to understand the code changes and ask insightful questions about the implementation. Here's how you should approach this task:

Level of thinking: {level_of_thinking}

First, carefully read and internalize the guidelines provided in CLAUDE.md

Now, review the code changes in the GitHub PR {pr_number} (this branch). Use "gh pr diff {pr_number}" to get the diff of the changes. As you review the code, use subagents for detailed analysis

As you review the code, follow these guidelines:

1. Carefully read through the code changes, paying attention to the logic, structure, and potential impacts on the existing codebase.
2. Look for areas where you don't fully understand the implementation or reasoning behind certain decisions.
3. Consider potential edge cases or scenarios that might not be covered by the current implementation.
4. Think about how this change might affect other parts of the system or impact performance.

Your main task is to ask questions about the code. As a curious junior developer:

1. Focus on understanding the "why" behind the changes, not just the "what".
2. Don't hesitate to ask for clarification on complex parts of the code.
3. Inquire about design decisions and alternative approaches that might have been considered.
4. Ask about any new concepts, libraries, or techniques used that you're not familiar with.
5. Seek explanations for any parts of the code that seem counterintuitive or could potentially be optimized.

Format your response as follows:

1. Begin with a brief summary of your understanding of the pull request and its purpose.
2. List your questions, numbering them for clarity. Aim for at least 3-5 thoughtful questions.
3. For each question, provide a brief explanation of why you're asking it or what led you to that question.
4. End with a statement expressing your eagerness to learn from the answers to these questions.

Present your review and questions within <review> tags. Here's an example structure:

<review>
Summary: [Your brief summary of the pull request]

Questions:
1. [Your first question]
   Reason: [Brief explanation of why you're asking this]

2. [Your second question]
   Reason: [Brief explanation of why you're asking this]

[Continue with more questions as needed]

I'm looking forward to learning from the answers to these questions and gaining a deeper understanding of this code change.
</review>

Remember, your goal is to demonstrate curiosity and a desire to learn, while also providing a thoughtful review of the code changes.

Write the report to CLAUDE_REVIEW_PR{pr_number}.md."""


def run_command(cmd, cwd=None, capture=True):
    """Run a shell command and return the result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=capture, text=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result.stdout.strip() if capture else None


def main():
    parser = argparse.ArgumentParser(description="PR Review Script")
    parser.add_argument("pr_number", help="PR number to review")
    parser.add_argument(
        "--use-existing-worktree",
        action="store_true",
        help="Use existing worktree vs recreating worktree (clean one)",
    )
    parser.add_argument(
        "--reviewer-type",
        choices=["senior", "junior"],
        default="senior",
        help="Type of reviewer (senior or junior). Senior is default.",
    )
    parser.add_argument(
        "--work-dir",
        help="Directory within the worktree where claude should run (default: worktree root)",
    )
    parser.add_argument(
        "--output-dir",
        help="Directory where review file should be written (default: current directory)",
    )
    parser.add_argument(
        "--level-of-thinking",
        choices=["think", "think hard", "think harder", "ultrathink"],
        default="think",
        help="Level of thinking intensity for the review (default: think)",
    )

    args = parser.parse_args()
    pr_number = args.pr_number

    print(f"Reviewing PR #{pr_number}...")

    # Step 1: Fetch PR Information
    print("Step 1: Fetching PR information...")
    run_command("git fetch")

    # Get PR details
    pr_info_json = run_command(f"gh pr view {pr_number} --json headRefName,title,files")
    pr_info = json.loads(pr_info_json)

    branch_name = pr_info["headRefName"]
    branch_dir_postfix = branch_name.replace("/", "-")
    pr_title = pr_info["title"]

    git_top_dir = run_command("git rev-parse --show-toplevel")
    temp_dir_for_ws = Path(git_top_dir) / "temp"
    worktree_dir = temp_dir_for_ws / f"golem-vanity.market-{branch_dir_postfix}"

    print(f"PR Title: {pr_title}")
    print(f"Branch: {branch_name}")

    # Step 2: Create Worktree
    print("Step 2: Creating worktree...")
    temp_dir_for_ws.mkdir(exist_ok=True)

    # Remove existing worktree if it exists and not using existing
    if not args.use_existing_worktree and worktree_dir.exists():
        print("Removing existing worktree...")
        run_command(f"git worktree remove {worktree_dir} --force")

    if not worktree_dir.exists():
        run_command(f"git worktree add {worktree_dir} {branch_name}")
    else:
        print("Using existing worktree...")

    # Step 3: Execute Review in Separate Claude Process
    print("Step 3: Executing review in separate claude process...")
    review_path = worktree_dir / args.work_dir if args.work_dir else worktree_dir

    print(f"Running claude review in {review_path}...")

    # Select and format the prompt based on reviewer type
    selected_prompt = PROMPT_JUNIOR if args.reviewer_type == "junior" else PROMPT
    formatted_prompt = selected_prompt.format(
        pr_number=pr_number, level_of_thinking=args.level_of_thinking
    )

    # Run claude command
    claude_cmd = [
        "claude",
        "-d",
        "--allowedTools",
        "Read,Write,Bash,Glob,Grep,LS",
        "-p",
        formatted_prompt,
    ]

    subprocess.run(claude_cmd, cwd=review_path)

    # Step 4: Copy Review Back
    print("Step 4: Copying review back to target directory...")
    review_file = review_path / f"CLAUDE_REVIEW_PR{pr_number}.md"

    # Determine target directory: use --output-dir if provided, else current working directory
    output_dir = Path(args.output_dir) if args.output_dir else Path.cwd()
    target_file = output_dir / f"CLAUDE_REVIEW_PR{pr_number}.md"

    if review_file.exists():
        review_file.rename(target_file)
        print(f"Review completed and saved to {target_file}")
    else:
        print("Warning: Review file not found")
        sys.exit(1)

    print(f"PR #{pr_number} review completed successfully!")


if __name__ == "__main__":
    main()
