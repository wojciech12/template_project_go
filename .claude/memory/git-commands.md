# Git Commands Memory

## Important Rules

- **NEVER use `git add .` or other `git add` options like `-A` or `-u`** - Always add files explicitly
- You **MUST ALWAYS** specify file paths when adding files to git
- Be selective about what gets committed

## Correct Usage

```bash
# Good - specific files
git add monitoring/README.md
git add monitoring/docker-compose.yml

# Bad - adds everything including unwanted files
git add .
```

## Reason

Using `git add .` can accidentally include:

- Temporary files
- Build artifacts
- IDE files
- Other unintended changes

Always be explicit about what files to stage for commit.
