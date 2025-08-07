#!/bin/bash
set -o nounset
set -o errexit
set -o pipefail

# Check if PR number is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <pr_number>"
    echo "Example: $0 50"
    exit 1
fi

PR_NUMBER="$1"

echo "Removing worktree for PR #$PR_NUMBER..."

# Get PR details
PR_INFO=$(gh pr view "$PR_NUMBER" --json headRefName,title,files)
BRANCH_NAME=$(echo "$PR_INFO" | jq -r '.headRefName')
BRANCH_DIR_POSTFIX=$(echo "$PR_INFO" | jq -r '.headRefName' | tr '/' '-')
PR_TITLE=$(echo "$PR_INFO" | jq -r '.title')

echo "PR Title: $PR_TITLE"
echo "Branch: $BRANCH_NAME"

GIT_TOP_DIR=$(git rev-parse --show-toplevel)
TEMP_DIR_FOR_WS="${GIT_TOP_DIR}/temp"

# Remove existing worktree if it exists
if [ -d "$TEMP_DIR_FOR_WS/golem-vanity.market-$BRANCH_DIR_POSTFIX" ]; then
    echo "Removing existing worktree..."
    git worktree remove "$TEMP_DIR_FOR_WS/golem-vanity.market-$BRANCH_DIR_POSTFIX" --force
fi
