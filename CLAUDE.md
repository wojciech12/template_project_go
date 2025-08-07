# Bash commands

- `just build`: Build the Go project to bin/app
- `just lint`: Run golangci-lint for code quality checks
- `just fmt`: Format Go code using golangci-lint
- `just test`: Run all Go tests
- `just prettier`: Format markdown and other files with prettier
- `go run .`: Run the main application
- `eza . --git-ignore --tree -I example -I slides`: Analyze the current state of the code

# Core files

- `main.go`: Main application entry point
- `go.mod`: Go module definition
- `Justfile`: Task runner configuration with build, lint, and format commands

# Code style

- Follow standard Go conventions (gofmt, golangci-lint)
- Use Go modules for dependency management
- Keep main.go simple and focused

# Testing

- Use Go's built-in testing framework
- Run tests with `just test` or `go test ./...`
- Test files should end with `_test.go`

# Working with Git and Github

## Git branch

Git branch _MUST_ follow the name conventions:

- prefix: 'feature/' 'bugfix/' 'chore/', 'refactor/', 'experiment/', 'docs/'
- followed by descriptive name, words connected with dashes

## Git commit message

You *MUST* follow:

- Use imperative mood (e.g., "Add feature" not "Added feature")
- Keep subject line concise (50 chars or less)
- Start with capital letter and don't end with period
- Separate subject from body with a blank line for detailed explanations
- For security updates, prefix with "Security:" or document vulnerability fixes
- NEVER ever mention a co-authored-by or similar aspects. In particular, never mention the tool used to create the commit message or PR.

## Pull Requests

- Create a detailed message of what changed. Focus on the high level description of the problem it tries to solve, and how it is solved. Don't go into the specifics of the code unless it adds clarity.
- You must use _gh_ to work with Github Pull Requests.

# Workflow

- Run `just lint` after code changes
- Use `just build` to verify compilation
- Format code with `just fmt` before committing