# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Repository Purpose

This directory contains Marp presentation slides for "Accelerating Go Development with Claude Code: A Pragmatic Approach" - a talk about practical AI integration in Go development workflows.

# Presentation Content

The slides cover:

- AI development realities (hype vs practical application)
- Model selection and capabilities (Anthropic models, Claude Code, Gemini)
- Context management strategies (CLAUDE.md, .claude/memory, docs-ai/)
- Prompt engineering techniques (CLEAR framework, role-based prompts)
- Repository structure for AI-assisted development
- Tools and workflow optimization
- Best practices for continuous improvement

# Bash Commands

- `just prettier`: Format slides.md with prettier
- View slides: Open slides.pdf or use Marp preview for slides.md
- Generate PDF: Use Marp CLI or VS Code Marp extension to export slides.md to PDF

# File Structure

- `slides.md`: Main presentation file in Marp format with Gaia theme
- `slides.pdf`: Generated PDF version of the presentation
- `slides.html`: Generated HTML version of the presentation
- `imgs/`: Directory containing presentation diagrams and images
  - `context.png`: Context management visualization
  - `diagram.png`: AI-assisted development workflow
  - `prompt_structure.png`: Prompt engineering structure diagram
  - `venn-diagram.png`: Intersection of effective AI development practices

# Marp Configuration

The presentation uses:

- **Theme**: Gaia
- **Colors**: Black text (#000) on white background (#fff)
- **Layout**: Lead class for centered content on most slides
- **Custom styling**: Flexbox layouts for image/text combinations

# Content Guidelines

When editing slides:

- Use `<!-- _class: lead -->` for centered slide layouts
- Keep bullet points concise and action-oriented
- Use consistent image sizing (e.g., `width:900px` for diagrams)
- Maintain the conversational, practical tone established in the content
- Focus on real-world experiences rather than theoretical concepts

# Visual Elements

- Images should illustrate key concepts (context management, workflow diagrams)
- Use flexbox for side-by-side layouts (text + image)
- Maintain consistent spacing and alignment
- Keep slide content digestible - avoid text-heavy slides

# Presentation Flow

The talk is structured as:

1. Opening: Setting realistic expectations about AI development
2. Core concepts: Models, context, prompts, tools
3. Practical implementation: Repository structure, workflows
4. Interactive discussion: Audience participation and experience sharing
5. Demo: Live Claude Code demonstration

# Key Messages

- Emphasize collaboration between human and AI
- Share practical experiences over theoretical benefits
- Encourage audience participation and knowledge sharing
- Focus on continuous learning and adaptation in AI-assisted development
