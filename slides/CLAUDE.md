# CLAUDE.md

This file provides guidance to Claude Code when working with this Marp presentation repository.

# Repository Purpose

This directory contains Marp presentation slides for "Accelerating Go Development with Claude Code: A Pragmatic Approach" - a talk about practical AI integration in Go development workflows.

# Bash Commands

**IMPORTANT: Always run these commands to maintain presentation quality**

- `just slides`: Generate PDF from slides.md (PRIMARY command for building presentation)
- `just slides-watch`: Watch and auto-regenerate PDF on slides.md changes
- `just slides-html`: Generate HTML version of presentation
- `just prettier`: Format slides.md and other files with prettier
- `just diagrams`: Generate PNG diagrams from mermaid (.mmd) files in imgs/
- `just compile_and_open`: Build slides and open PDF automatically

**Image Generation Commands:**
- `just html-to-png HTML_FILE`: Convert HTML file to PNG screenshot
- `just slides-pdf-to-png`: Convert slides PDF to individual PNG files

# Core Files

- `slides.md`: Main presentation file in Marp format with Gaia theme
- `slides.pdf`: Generated PDF version (auto-generated)
- `slides.html`: Generated HTML version (auto-generated)
- `Justfile`: Task runner with all build and formatting commands
- `imgs/`: Directory with presentation assets and diagrams

# Images and Diagrams

**Current image assets in imgs/:**
- `claude_code.png`: Claude Code logo for title slide
- `GOPHER_LAPTOP.png`: Go mascot for title slide  
- `gofersyrenka.png`: Go mascot for thank you slide
- `context.png`: Context management visualization (generated from context.mmd)
- `prompt_structure.png`: Prompt engineering structure diagram
- `venn-diagram.png`: Intersection of effective AI development practices

**HTML source files for image generation:**
- `claude_code.html`: Source for generating claude_code.png
- `prompt_structure.html`: Source for generating prompt_structure.png
- `venn-diagram.html`: Source for generating venn-diagram.png

**Mermaid source files:**
- `context.mmd`: Source for context.png diagram

# Marp Configuration

**YOU MUST maintain these settings when editing slides.md:**

- **Theme**: Gaia (specified in frontmatter)
- **Colors**: Black text (#000) on white background (#fff)
- **Layout**: Use `<!-- _class: lead -->` for ALL slides except title
- **Image sizing**: Consistent widths (900px for diagrams, 300px for logos)

# AI-Specific Workflow

**CRITICAL: Follow this workflow when making changes:**

1. **Edit slides.md** - Make content changes
2. **Run `just prettier`** - Format the file  
3. **Run `just slides`** - Generate updated PDF
4. **Review slides.pdf** - Verify changes appear correctly

**When adding new diagrams:**
1. Create `.mmd` file in imgs/ for mermaid diagrams
2. Run `just diagrams` to generate PNG
3. Reference in slides.md with appropriate width

# Content Guidelines

**YOU MUST follow these rules when editing slides.md:**

- Use `<!-- _class: lead -->` for ALL slide layouts (already established pattern)
- Keep bullet points concise and action-oriented (max 3-4 per slide)
- Use consistent image sizing: `width:900px` for diagrams, `width:300px` for logos
- Maintain conversational, practical tone (avoid academic language)
- Focus on real-world experiences over theoretical concepts
- Keep slides digestible - avoid text-heavy content

# Presentation Content Focus

**The presentation covers practical AI development:**
- AI development realities (hype vs practical application)  
- Model selection and capabilities (Claude Code, Gemini)
- Context management strategies (CLAUDE.md, .claude/memory, docs-ai/)
- Prompt engineering techniques (CLEAR framework, role-based prompts)
- Repository structure for AI-assisted development
- Tools and workflow optimization

**Key messaging priorities:**
- Emphasize human-AI collaboration
- Share practical experiences over theoretical benefits
- Encourage audience participation and knowledge sharing
- Focus on continuous learning in AI-assisted development
