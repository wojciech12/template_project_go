#!/bin/bash

# PR Review Script
# Usage: ./do-pr-review-gemini.sh <pr_number>

set -o nounset
set -o errexit
set -o pipefail
set -x

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

echo "PR Title: $PR_TITLE"
echo "Branch: $BRANCH_NAME"

GIT_TOP_DIR=$(git rev-parse --show-toplevel)
TEMP_DIR_FOR_WS="${GIT_TOP_DIR}/temp"

# Step 2: Create Worktree
echo "Step 2: Creating worktree..."
mkdir -p $TEMP_DIR_FOR_WS

# Remove existing worktree if it exists
if [ -d "${TEMP_DIR_FOR_WS}/golem-vanity.market-$BRANCH_DIR_POSTFIX" ]; then
    echo "Removing existing worktree..."
    git worktree remove "${TEMP_DIR_FOR_WS}/golem-vanity.market-$BRANCH_DIR_POSTFIX" --force
fi

git worktree add "${TEMP_DIR_FOR_WS}/golem-vanity.market-$BRANCH_DIR_POSTFIX" "$BRANCH_NAME"

# Step 3: Analyze Changes and Determine Review Directory
echo "Step 3: Analyzing changes..."
FILES=$(echo "$PR_INFO" | jq -r '.files[].path')

CLI_CHANGES=0
WEBAPP_CHANGES=0

while IFS= read -r file; do
    if [[ "$file" == cli/* ]]; then
        CLI_CHANGES=$((CLI_CHANGES + 1))
    elif [[ "$file" == webapp/* ]]; then
        WEBAPP_CHANGES=$((WEBAPP_CHANGES + 1))
    fi
done <<< "$FILES"

echo "CLI changes: $CLI_CHANGES"
echo "Webapp changes: $WEBAPP_CHANGES"

# Determine review directory
if [ "$CLI_CHANGES" -gt "$WEBAPP_CHANGES" ]; then
    REVIEW_DIR="cli"
    echo "Most changes in CLI directory"
else
    REVIEW_DIR="webapp"
    echo "Most changes in Webapp directory"
fi

# Step 4: Execute Review in Separate Gemini Process
echo "Step 4: Executing review in separate Gemini process..."
cd "${TEMP_DIR_FOR_WS}/golem-vanity.market-$BRANCH_DIR_POSTFIX/$REVIEW_DIR"

echo "Running Gemini review in $(pwd)..."
gemini \
    -y \
    -p <<-EOF
Read the guidelines in CLAUDE.md.
Review the code changes in github PR ${PR_NUMBER} (this branch), use gh cli if needed.
Act as a critical and brutally honest senior software engineer.
Write the report to GEMINI_REVIEW_PR${PR_NUMBER}.md.
If you see an opportunity to improve, include code fragments in the report showing how to improve the code.
EOF


# Step 5: Copy Review Back
echo "Step 5: Copying review back to original repository..."
if [ -f "GEMINI_REVIEW_PR$PR_NUMBER.md" ]; then
    mv "GEMINI_REVIEW_PR$PR_NUMBER.md" "../../../GEMINI_REVIEW_PR$PR_NUMBER.md"
    echo "Review completed and saved to GEMINI_EVIEW_PR$PR_NUMBER.md"
else
    echo "Warning: Review file not found"
    exit 1
fi
