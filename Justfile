set shell := ["bash", "-eEuo", "pipefail", "-c"]

golint := require("golangci-lint")
npx := require("npx")
uvx := require("uvx")

[group("go")]
lint:
    golangci-lint run

[group("go")]
fmt:
    golangci-lint fmt

[group("go")]
build:
    go build -o bin/app .

[group("go")]
test:
    go test ./...

[group("claude")]
[group("docs")]
prettier:
    npx prettier --write .

[group("claude")]
fmt_tools:
    ruff format .claude/*/*.py
