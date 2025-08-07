# Memory: Slash Commands Creation

## Instructions

When asked to create new slash commands, ALWAYS first fetch the newest documentation from https://docs.anthropic.com/en/docs/claude-code/slash-commands to ensure using the most current slash command specifications, syntax, features, and best practices.

## Slash Commands Overview

- Purpose: Control Claude's behavior during interactive sessions
- Two main types: Built-in and Custom commands

## Built-in Slash Commands

Key examples include:

- `/help`: Get usage help
- `/clear`: Clear conversation history
- `/model`: Select or change AI model
- `/review`: Request code review
- `/init`: Initialize project with CLAUDE.md guide

## Custom Slash Commands

1. Types:

- Project commands (stored in `.claude/commands/`)
- Personal commands (stored in `~/.claude/commands/`)

2. Syntax: `/<command-name> [arguments]`

3. Features:

- Support arguments via `$ARGUMENTS` placeholder
- Can execute bash commands with `!` prefix
- Reference files using `@` prefix
- Support namespacing through subdirectories
- Include frontmatter for configuration

4. Frontmatter Options:

- `allowed-tools`: Specify permitted tools
- `argument-hint`: Describe expected arguments
- `description`: Command explanation
- `model`: Select specific AI model

5. Advanced Capabilities:

- Trigger extended thinking
- Dynamic command discovery
- Support for MCP (Model Context Protocol) server commands

## Example Custom Command Creation

```bash
mkdir -p .claude/commands
echo "Analyze this code for performance issues" > .claude/commands/optimize.md
```
