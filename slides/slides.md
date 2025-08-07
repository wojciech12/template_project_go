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

<small>Wojciech Barczynski</small>

---
<!-- _class: lead -->
# Dev with AI

- Hype vs slot-machine
- Continuously evolving
- dev < dev + AI

---
<!-- _class: lead -->
# Goal

- What works for me (so far)
- Open Discussion

---
<!-- _class: lead -->

![width:900px](imgs/venn-diagram.png)

---
<!-- _class: lead -->

<p size="30"><b>+ Tools</b></p>

---
<!-- _class: lead -->
# Models

- Antrophic models lead
- `claude`  &#8594; better results
- [Cut-off](https://docs.anthropic.com/en/docs/about-claude/models/overview) - march 2025

---
<!-- _class: lead -->
# Models

Models have strengths and weaknesses:

- Claude Code
- Gemini

---
<!-- _class: lead -->
## Context

![width:900px](imgs/context.png)

---
<!-- _class: lead -->
## CLAUDE.md

- keep it up to date
- update after new feature*
- have a command for it

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

- Not read automatically
- Use for one-off prompts (e.g., `migration_sqlite_to_psql.md`)
- Reminders
- Keep them for later use (e.g., `memory-template`)

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
# Platform Engineer

1. Scaling up = self-service infra/platform
2. Guardrails
3. (eventual) best practices


---
<!-- _class: lead -->
# Software Engineer

1. Fast
2. Compose from large pieces
3. Stop me if I am going to cut my fingers off

---
<!-- _class: lead -->
# AI for IaC use cases

1. Self-service & reducing friction
2. Planning and pre-mortem
3. Accelerate IaC & CloudNative development
4. Security & Compliance

---
<!-- _class: lead -->
## Accelerate & Democratise

![width:700px](imgs/diagram.png)

---
<!-- _class: lead -->
# Best Practices

- Modules repository
- Example repos for new components
- Packages easy to consume by Agents
- Continuously built (and pruned)

---
<!-- _class: lead -->
# Control

- Enforced policies with, e.g., OPA
- Standardized tooling, e.g., `tfsec` & `conftest`
- CI/CD
- AI-assisted reviews

---
<!-- _class: lead -->
# Experience

- AI instructions and templates
- subagent configurations
- mcp server(s)

---
<!-- _class: lead -->
# Experience

- Make it easy to share prompts and ad-hoc plans and instructions
- Telemetry

---
<!-- _class: lead -->
# Continuous Effort

1. AI Retrospectives
2. Sharing experience and prompts

---
<!-- _class: lead -->
<!-- _class: lead -->
<h1>Demo &rarr; Claude for OpenTofu</h1> 

[github.com/wojciech12/talks](https://github.com/wojciech12/talks/) & [wbarczynski.pl](https://wbarczynski.pl)

---
<!-- _class: lead -->
# Thank you
