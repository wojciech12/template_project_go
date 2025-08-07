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

PR_INFO=$(gh pr view "$PR_NUMBER" --json headRefName,title,files)
BRANCH_NAME=$(echo "$PR_INFO" | jq -r '.headRefName')
BRANCH_DIR_POSTFIX=$(echo "$PR_INFO" | jq -r '.headRefName' | tr '/' '-')

GIT_TOP_DIR=$(git rev-parse --show-toplevel)
WORKTREE_DIR="$GIT_TOP_DIR/temp/golem-vanity.market-$BRANCH_DIR_POSTFIX"

echo "Copy .claude config (main and cli) files to worktree..."
cp "$GIT_TOP_DIR/.claude/settings.local.json" "$WORKTREE_DIR/.claude/settings.local.json"
