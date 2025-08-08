# Template Project Golang

## Project structure

```
.
├── .claude/               # Claude Code configuration and customizations
│   ├── agents/           # Custom agents
│   ├── commands/         # Custom commands
│   ├── commands-template/ # Command templates
│   ├── hooks/            # Git and tool hooks
│   ├── memory/           # Memory files
│   ├── memory-template/  # Memory templates
│   ├── scripts/          # Utility scripts
│   ├── settings.json     # Claude Code settings
│   └── settings.local.json # Local Claude Code settings
├── .tools                 # scripts for running claude in the background
├── slides                 # slides
├── CLAUDE.md              # Project instructions for Claude Code
├── docs/                  # Documentation
│   └── testing.md
├── docs-ai/              # AI-related documentation
├── go.mod                # Go module definition
├── Justfile              # Task runner configuration
├── main.go               # Main application entry point
├── main_test.go          # Tests for main application
└── README.md             # This file
```

## Configuration

## Tools

- [Justfile](https://github.com/casey/just)
- [golangci-lint](https://github.com/golangci/golangci-lint)
- [gh](https://cli.github.com/)
- [eza](https://github.com/eza-community/eza)
- node with [nvm](https://github.com/nvm-sh/nvm) - running prettier
- [uv](https://docs.astral.sh/uv/) - claude hooks, scripts, and tools
- [ruff](https://docs.astral.sh/ruff/installation/) - fmt for Python (default language for scripts)
- [ccusage](https://github.com/ryoppippi/ccusage)

For consideration: [pre-commit](https://pre-commit.com/).

Recommended: [git-delta](https://github.com/dandavison/delta).

### Claude Code

1. `~/.claude/settings.json`:

   ```json
   "includeCoAuthoredBy": false
   ```

2. Voice notifications, requirements:
   - piper - [github](https://github.com/rhasspy/piper/releases) + [voice](https://rhasspy.github.io/piper-samples/) (I use `en_US-libritts_r-medium`)
   - [ffmpeg](https://ffmpeg.org/download.html) package for `ffpg`
   - add a `PIPER_HOME` env variable to your rc file
   - hooks scripts assumes that the voice model is `$PIPER_HOME/models`

3. TBA

## References

- [Claude Code Best Practises](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Claude code CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- [Example of Golang project](https://github.com/fwojciec/pgarrow/)
- [Notes on AI for software engineering](https://github.com/wojciech12/notes_ai_for_software_engineering/tree/main)
- [Example repo with hooks](https://github.com/disler/claude-code-hooks-mastery)
