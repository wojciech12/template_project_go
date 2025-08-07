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

<!-- _class: lead -->

# Accelerating Go Development with Claude Code: A Pragmatic Approach

<small>Wojciech Barczynski (Unoperate)</small>

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
## Plan.md

- Keep the model on the track
- When it double, create it
- MUST for anything more complicated
- Benefits for the model

---
<!-- _class: lead -->
## Prompt for Claude Code

- The CLEAR Framework
- Keywords, e.g., exactly, detaile, [...](https://github.com/wojciech12/notes_ai_for_software_engineering/blob/main/PROMPTS.md)
- Role-based
  
  ```
  You are a [ROLE] with expertise in [DOMAIN].
  Your task is to [SPECIFIC_ACTION].
  ```

---
<!-- _class: lead -->
![width:70%, bg left](imgs/prompt_structure.png)

Will help:

- Good to watch 1-2 videos about prompt engineering
- [prompt optimizer](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-improver) at claude.ai
- Claude can review your prompts as well.

---
<!-- _class: lead -->
## Tools

Claude:

- hooks
- Opentelemetry
- `ccusage`

---
<!-- _class: lead -->
## Tools

Basic:

- CLI: gh
- Python - ad hoc
- mcp - few really worth it 

---
<!-- _class: lead -->
## Go-Specific AI Integration

- Go modules and dependency management
- Strict formatting (`gofmt`, `golangci-lint`) 
- Testing conventions (`*_test.go`)
- Interface design patterns

---
<!-- _class: lead -->
# Accelerating Go Development

- Continuous Effort

---
<!-- _class: lead -->
# Accelerating Go Development

- Share the learnings with your team
- AI retrospectives

---
<!-- _class: lead -->
# Accelerating Go Development

- More verticals in your app, the easier for the model

---
<!-- _class: lead -->
# Accelerating Go Development

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
