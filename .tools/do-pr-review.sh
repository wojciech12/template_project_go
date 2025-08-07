#!/bin/bash

# PR Review Script
# Usage: ./pr-review.sh <pr_number>

set -e

# Check if PR number is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <pr_number>"
    echo "Example: $0 50"
    exit 1
fi

PR_NUMBER="$1"

echo "Reviewing PR #$PR_NUMBER..."

# Step 1: Fetch PR Information
echo "Step 1: Fetching PR information..."
git fetch

# Get PR details
PR_INFO=$(gh pr view "$PR_NUMBER" --json headRefName,title,files)
BRANCH_NAME=$(echo "$PR_INFO" | jq -r '.headRefName')
BRANCH_DIR_POSTFIX=$(echo "$PR_INFO" | jq -r '.headRefName' | tr '/' '-')
PR_TITLE=$(echo "$PR_INFO" | jq -r '.title')

GIT_TOP_DIR=$(git rev-parse --show-toplevel)
TEMP_DIR_FOR_WS="${GIT_TOP_DIR}/temp"
WORKTREE_DIR="${TEMP_DIR_FOR_WS}/golem-vanity.market-$BRANCH_DIR_POSTFIX"

echo "PR Title: $PR_TITLE"
echo "Branch: $BRANCH_NAME"

# Step 2: Create Worktree
echo "Step 2: Creating worktree..."
mkdir -p "${TEMP_DIR_FOR_WS}"

# Remove existing worktree if it exists
if [ -d "$WORKTREE_DIR" ]; then
    echo "Removing existing worktree..."
    git worktree remove "$WORKTREE_DIR" --force
fi

git worktree add "$WORKTREE_DIR" "$BRANCH_NAME"

# Step 3: Analyze Changes and Determine Review Directory
echo "Step 3: Analyzing changes..."
FILES=$(echo "$PR_INFO" | jq -r '.files[].path')

CLI_CHANGES=0
WEBAPP_CHANGES=0
INFRA_CHANGES=0

while IFS= read -r file; do
    if [[ "$file" == cli/* ]]; then
        CLI_CHANGES=$((CLI_CHANGES + 1))
    elif [[ "$file" == webapp/* ]]; then
        WEBAPP_CHANGES=$((WEBAPP_CHANGES + 1))
    elif [[ "$file" == infra/* ]]; then
        INFRA_CHANGES=$((INFRA_CHANGES + 1))
    fi
done <<< "$FILES"

echo "CLI changes: $CLI_CHANGES"
echo "Webapp changes: $WEBAPP_CHANGES"
echo "Infrastructure changes: $INFRA_CHANGES"

# Determine review directory - prioritize infra if most changes are there
if [ "$INFRA_CHANGES" -gt "$CLI_CHANGES" ] && [ "$INFRA_CHANGES" -gt "$WEBAPP_CHANGES" ]; then
    REVIEW_DIR="infra"
    echo "Most changes in Infrastructure directory - reviewing from infra"
elif [ "$CLI_CHANGES" -gt "$WEBAPP_CHANGES" ]; then
    REVIEW_DIR="cli"
    echo "Most changes in CLI directory - reviewing from cli"
else
    REVIEW_DIR="webapp"
    echo "Most changes in Webapp directory"
fi

# Step 4: Execute Review in Separate Claude Process
echo "Step 4: Executing review in separate claude process..."
cd "$WORKTREE_DIR/$REVIEW_DIR"

# https://www.anthropic.com/engineering/claude-code-best-practices
# https://github.com/anthropics/claude-code-base-action
# https://console.anthropic.com/dashboard <- prompt optimiser
echo "Running claude review in $(pwd)..."
claude \
    -d \
    --allowedTools "Read,Write,Bash,Glob,Grep,LS" \
    -p <<-EOF
You are a critical and brutally honest senior software engineer tasked with reviewing a GitHub pull request (PR). Your goal is to provide a thorough and insightful review, identifying potential issues, suggesting improvements, and ensuring the code meets high quality standards.

First, carefully read and internalize the guidelines provided in CLAUDE.md

Now, review the code changes in the GitHub PR ${PR_NUMBER} (this branch). Use "gh pr diff ${PR_NUMBER}" to get the diff of the changes.

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
2. Major Issues: List and explain any significant problems you\'ve identified.
3. Minor Issues: List and explain less critical issues or style concerns.
4. Suggestions for Improvement: Provide specific recommendations, including code snippets where applicable.
5. Positive Aspects: Highlight any particularly well-done parts of the code.
6. Conclusion: Your overall assessment and whether you would approve, request changes, or reject the PR.

Begin your review with the title "# PR Review for PR${PR_NUMBER}" and write the entire review in markdown format. Your review should be comprehensive, insightful, and actionable.

Remember to think critically and provide a thorough analysis. Your goal is to ensure the highest code quality and to help improve the overall codebase.
Write the report to CLAUDE_REVIEW_PR${PR_NUMBER}.md. Write all the steps, you took in CLAUDE_REVIEW_PR${PR_NUMBER}_LOG.md.
EOF

# Step 5: Copy Review Back
echo "Step 5: Copying review back to original repository..."
if [ -f "CLAUDE_REVIEW_PR$PR_NUMBER.md" ]; then
    mv "CLAUDE_REVIEW_PR$PR_NUMBER.md" "${GIT_TOP_DIR}/CLAUDE_REVIEW_PR$PR_NUMBER.md"
    echo "Review completed and saved to CLAUDE_REVIEW_PR$PR_NUMBER.md"
else
    echo "Warning: Review file not found"
    exit 1
fi

echo "PR #$PR_NUMBER review completed successfully!"
