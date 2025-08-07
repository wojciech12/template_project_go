# Update CLAUDE.md Command

## Purpose

Systematically update CLAUDE.md based on repository changes to ensure documentation accuracy for AI development. This command provides a comprehensive workflow for AI assistants to maintain the development guide.

## Prerequisites

- Working directory: git repo root directory
- Git repository with recent changes
- Access to Read, Grep, Glob, LS, and Bash tools
- CLAUDE.md exists and is readable

## Assessment Phase

### 1. Detect Repository Changes

```bash
# Find the last commit that updated CLAUDE.md
LAST_CLAUDE_COMMIT=$(git log --oneline --follow CLAUDE.md | head -1 | cut -d' ' -f1)
echo "Last CLAUDE.md update commit: $LAST_CLAUDE_COMMIT"

# Get all changes since that commit
git diff --name-only $LAST_CLAUDE_COMMIT..HEAD
git log --oneline $LAST_CLAUDE_COMMIT..HEAD

# Alternative method using git commands directly
git log --oneline --follow CLAUDE.md | head -1
git diff --name-only 4670819..HEAD  # Replace with actual commit hash
git log --oneline 4670819..HEAD     # Replace with actual commit hash

# Get current status
git status --porcelain
```

### 2. Categorize Changes

Use these patterns to identify change types:

- **Structure**: New/moved/deleted directories or key files
- **Interfaces**: Changes to `.go` files
- **Dependencies**: `go.mod`, `go.sum` changes
- **Commands**: `Justfile` scripts section changes
- **Configuration**: Config files, environment variables
- **Tests**: Changes in test directory

### 3. Read Current CLAUDE.md

```bash
# Always read current version first
```

Use Read tool on `CLAUDE.md`

## Update Procedures

### Section 1: Critical File Locations (HIGH PRIORITY)

**Validation Steps:**

1. Verify all file paths using LS tool
2. Check line number references using Grep tool
3. Update any moved/renamed files

**Update Process:**

```bash
# Verify core entry points exist
eza . --tree
```

**Action:** Update file paths and line numbers if any files moved or structure changed.

### Section 2: Critical Interfaces (HIGH PRIORITY)

**Target Files to Check:**

FILL_ME - ask

**Validation Process:**

1. Read each target file
2. Compare interface definitions with documented versions
3. Update parameter types, add new fields, remove deprecated ones

**Example Validation:**

```bash

```

### Section 3: Development Commands (HIGH PRIORITY)

**Validation Steps:**

1. Extract all targets from Justfile
2. Compare with documented commands
3. Test critical commands work

**Process:**

```bash
just
```

**Update:** Add new targets, scripts, remove deprecated ones, update descriptions.

### Section 4: Dependencies (MEDIUM PRIORITY)

**Process:**

```bash
# Get current dependencies with versions
cat package.json | grep -A 30 '"dependencies":'
cat package.json | grep -A 20 '"devDependencies":'
```

**Update:** Version numbers, new dependencies, removed packages.

### Section 5: Architecture Patterns (MEDIUM PRIORITY)

**Check for:**

- New design patterns in changed files
- Modified class structures
- Updated data flow patterns

**Process:**

1. Review significantly changed `.ts` files
2. Look for new architectural decisions
3. Update pattern documentation if needed

### Section 6: Database Schema (HIGH PRIORITY if schema.ts changed)

**If `/src/lib/db/schema.ts` changed:**

1. Read complete schema file
2. Update table definitions
3. Update relationship documentation
4. Check for new enums or types

### Section 7: Configuration Patterns (MEDIUM PRIORITY)

**Check:**

- Environment variables in code
- Config file changes
- New configuration options

**Process:**

```bash
# Find environment variable usage
grep -r "process.env" src/ | head -10
grep -r "export.*CONFIG" src/
```

## Validation Phase

### File Path Verification

For each file path mentioned in CLAUDE.md:

1. Use LS tool to verify existence
2. If missing, use Glob tool to find new location
3. Update path or remove if deleted

### Line Number Verification

For each line number reference:

1. Use Grep tool with context to find current location
2. Update line numbers if code moved

### Interface Verification

For each documented interface:

1. Read actual TypeScript file
2. Compare field by field
3. Update documentation to match code

### Command Verification

For each documented npm command:

1. Check exists in package.json
2. Verify command description is accurate

## Common Update Scenarios

### Scenario 1: New TypeScript Interface

1. Identify the new interface location
2. Document in "Critical Interfaces" section
3. Add usage examples if applicable
4. Update related sections

### Scenario 2: File Structure Changes

1. Update "Critical File Locations" section
2. Update any affected code examples
3. Update import path references

### Scenario 3: New npm Scripts

1. Add to "Development Commands" section
2. Include usage examples
3. Categorize by purpose (build/test/dev/etc.)

### Scenario 4: Dependency Updates

1. Update version numbers in dependencies section
2. Note any breaking changes
3. Update related configuration if needed

### Scenario 5: Database Schema Changes

1. Update table definitions
2. Update relationship documentation
3. Update example queries if provided

## Quality Checklist

### Before Finalizing Updates:

- [ ] All file paths verified to exist
- [ ] All line numbers checked and updated
- [ ] All interface definitions match current code
- [ ] All npm commands tested or verified in package.json
- [ ] Version information current
- [ ] No broken internal references
- [ ] Code examples are syntactically correct
- [ ] Consistent formatting maintained

### Final Validation Commands:

```bash
# Verify all mentioned files exist
grep -o '`/[^`]*`' CLAUDE.md | sort -u
# Check for outdated line number references
grep -o '(lines [0-9-]*)'CLAUDE.md
```

## Error Handling

### Common Issues:

- **File not found**: Use Glob to search for moved files
- **Interface mismatch**: Read actual TypeScript file to get current definition
- **Command not found**: Check package.json scripts section
- **Line number outdated**: Use Grep with context to find new location

### Recovery Actions:

- Always preserve existing structure when updating
- Flag uncertain changes for human review
- Make incremental updates rather than wholesale replacement
- Document reasoning for significant changes

## Output Requirements

### Document Changes Made:

- List each section updated
- Summarize nature of changes
- Flag any items needing human review
- Note any missing information discovered

### Summary Format:

```
CLAUDE.md Update Summary:
- Updated file paths: [list]
- Updated interfaces: [list]
- Updated commands: [list]
- Sections modified: [list]
- Items flagged for review: [list]
```

## Success Criteria

- All documented file paths exist and are accurate
- All interface definitions match current TypeScript code
- All npm commands are valid and current
- All line number references are accurate
- Documentation reflects current repository state
- No broken internal references or examples
