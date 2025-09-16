# Mermaid Diagram Validation Best Practices

## Tool: mmdc (mermaid-cli)

**Installation**: `npm install -g @mermaid-js/mermaid-cli`

## Validation Commands for AI Development

### Basic Validation and Export

```bash
mmdc -i diagram_file.md -s 20 -o output.png
```

### Optimized for Complex Diagrams

```bash
# MetricsCollector diagram
mmdc -i COL_DIAGRAM.md -s 15 -o metrics_overview.png

# Architecture diagrams
mmdc -i ARCH_FLOW.md -s 25 -o architecture_flow.png

# Database schema
mmdc -i DB_SCHEMA.md -s 20 -o database_schema.png
```

### Syntax Validation (No --parse flag available)

```bash
# Validate by converting to temporary file (mmdc has no --parse option)
mmdc -i diagram_file.md -o temp_validation.svg
rm temp_validation*.svg  # Clean up validation files
```

### Custom Themes and Configurations

```bash
mmdc -i diagram_file.md -t dark -s 25 -o diagram_dark.png
```

## AI Agent Optimization Guidelines

### Scale Factor Recommendations

- **Simple diagrams**: `-s 15`
- **Complex diagrams with multiple nodes**: `-s 20-25`
- **High-detail enterprise diagrams**: `-s 30`

### File Naming Conventions

- Use descriptive prefixes: `COL_DIAGRAM.md`, `ARCH_FLOW.md`, `DB_SCHEMA.md`
- Keep consistent naming pattern for batch processing

### Validation Workflow

1. **Validate by conversion**: Convert to SVG/PNG to check syntax (no --parse flag)
2. **Export for docs**: Generate PNG for GitHub display and documentation
3. **Split complexity**: Break large diagrams into focused sub-diagrams by domain

## Batch Processing Patterns

### Validate All Mermaid Files

```bash
# Validate by attempting conversion to temporary files
find . -name "*_DIAGRAM.md" -exec mmdc -i {} -o {}.validation.svg \;
# Clean up validation files
find . -name "*.validation.svg" -delete
```

### Batch Export with Consistent Scaling

```bash
for file in *_DIAGRAM.md; do
  mmdc -i "$file" -s 20 -o "${file%.md}.png"
done
```

### Project-Specific Examples

#### MetricsCollector Validation

```bash
mmdc -i COL_DIAGRAM.md -s 20 -o metrics_collector.png
```

#### Architecture Documentation

```bash
mmdc -i GOLEM_ARCH_DIAGRAM.md -s 25 -o golem_architecture.png
```

## Memory Optimization for Claude

- **Pre-validate syntax** before creating complex diagrams
- **Use consistent scaling** across project diagrams
- **Export to PNG** for reduced token usage in future conversations
- **Focus on domain separation** to avoid overwhelming single diagrams
