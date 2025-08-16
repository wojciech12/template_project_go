---
marp: true
theme: gaia
color: #000
colorSecondary: #333
backgroundColor: #fff
style: |
  section.lead h1 {
  text-align: center;
  }
---

<!-- _class: lead 
backgroundColor: black
color: #fff

-->

## Accelerating Go Development<br />with Claude Code

![width:300px](imgs/claude_code.png)![width:250px](imgs/GOPHER_LAPTOP.png) 
<!-- small>Wojciech Barczynski</small -->

---
<!-- _class: lead -->
## Development with AI

- AI boosts productivity.
- Tools and models evolve rapidly.
- The challenge is to find what works.

---
<!-- _class: lead -->
## Goal

- Share a pragmatic AI workflow for Go development.
- Discuss effective strategies and tools.

---
<!-- _class: lead -->

![width:900px](imgs/venn-diagram.png)

---
<!-- _class: lead -->

<p size="30"><b>+ Tools</b></p>

---
<!-- _class: lead -->
## Models

- Anthropic models lead
- `claude`  &#8594; better results
- [Cut-off](https://docs.anthropic.com/en/docs/about-claude/models/overview) - march 2025

---
<!-- _class: lead -->
## Models

Models have strengths and weaknesses:

- Claude Code
- Gemini

---
<!-- _class: lead -->
## Context

![width:1200px](imgs/context.png)

---
<!-- _class: lead -->
## CLAUDE.md

- Keep it up-to-date.
- Update it when new features are added.
- Create a command for easy updates.

---
<!-- _class: lead -->
## CLAUDE.md

For Go-specific context, include:

- Project coding conventions.
- Go design patterns, with examples (e.g., for error handling).

---
<!-- _class: lead -->
## Plan.md

- Keep the model on the track
- When it double, create it
- MUST for anything more complicated
- Benefits for the model

---
<!-- _class: lead -->
## context7 mcp

- Fetches on-demand documentation and code snippets.
- Additionally:
  - Add links to [prompts](https://github.com/wojciech12/local_grafana_observability_stack).
  - Add information to `memory/`.
  - Or save to `docs-ai/`.

---
<!-- _class: lead -->
## .claude/memory
Memory (`.claude/memory`):

- Convention, not automatically read ([docs](https://docs.anthropic.com/en/docs/claude-code/memory)).
- Use for one-off prompts (e.g., `migration_sqlite_to_psql.md`).
- Store best practices.
- Save prompts for future use (e.g., `memory-template`).

---
<!-- _class: lead -->
## docs-ai / ai-docs

- More extensive docs and larger mds.
- You can link them in `CLAUDE.md`.

---
<!-- _class: lead -->
## Repository

- Modular design
- Vertical project structure
- `CLAUDE.md` files in subfolders

---
<!-- _class: lead -->
## Context

```
Read .claude/memory/* and ... use command ... 
```

---
<!-- _class: lead -->
## context hygiene

Once the task is complete:

- Save any essential information.
- Clear the context using the `/clear` command.
- `git worktree` for isolated environments.

---
<!-- _class: lead -->
## Prompt for Claude Code

- The CLEAR Framework
- Keywords, e.g., exactly, detaile, [...](https://github.com/wojciech12/notes_ai_for_software_engineering/blob/main/PROMPTS.md)
- Role-task format pattern
  
  ```
  You are a [ROLE] with expertise in [DOMAIN].
  Your task is to [SPECIFIC_ACTION].
  ```

---
<!-- _class: lead -->
## The CLEAR Framework

- Context: Background information
- Limitations: Constraints and boundaries
- Examples: Sample inputs/outputs
- Action: Specific task to perform
- Result: Expected deliverable format

---
<!-- _class: lead -->
![width:70%, bg left](imgs/prompt_structure.png)

Will help:

- Good to watch 1-2 videos about prompt engineering
- [prompt optimizer](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-improver) at claude.ai
- Claude can review your prompts as well.

---
<!-- _class: lead -->
## Claude Code

- **`ESC`**: Provide additional information.
- **`ESC` `ESC`**: Cancel the current action.
- **Planning Mode**: Deconstruct complex tasks into smaller steps.

---
<!-- _class: lead -->
<!-- _class: lead -->
## Claude Code Tools

- **Hooks**: Customize behavior with pre/post-action scripts.
- **OpenTelemetry**: Integrated for observability and performance monitoring.
- **`ccusage`**: CLI tool to track token usage and costs.

---
<!-- _class: lead -->
## Choosing Your Tools

How I approach it:

1. **CLI Tools (`gh`, `eza`, ...):** Fast and efficient for common tasks.
2. **Python Scripts (with `uv`)**: Best for automation and complex logic.
3. **Mcp** few use cases.

---
<!-- _class: lead -->
## Go-Specific

Claude benefits from Go's rapid feedback loop:

- **Strongly-typed language**: Catches errors before runtime.
- **Strict formatting**: Enforced by tools like `gofmt` and `golangci-lint`.

I typically use [Claude hooks](https://github.com/wojciech12/template_project_go/blob/master/.claude/settings.json#L4) to automate these checks.

---
<!-- _class: lead -->
## Accelerating Go Development

- Continuous Process

---
<!-- _class: lead -->
## Accelerating Go Development

- Share the learnings with your team
- e.g., AI retrospectives

---
<!-- _class: lead -->
## Accelerating Go Development

- More verticals in your app, the easier for the model

---
<!-- _class: lead -->
## Accelerating Go Development

- Model
- Context
- Prompt
- Tools

---
<!-- _class: lead -->
<h1>Demo &rarr; Claude</h1> 

[github.com/wojciech12/talks](https://github.com/wojciech12/talks/) & [wbarczynski.pl](https://wbarczynski.pl)

---
<!-- _class: lead -->
# Thank you
