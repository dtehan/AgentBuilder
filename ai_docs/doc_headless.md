<!-- Fetched: 2025-12-31 -->
<!-- Source: https://code.claude.com/docs/en/headless -->

# Run Claude Code Programmatically

## Overview

Use the Agent SDK to run Claude Code programmatically from the CLI, Python, or TypeScript. The Agent SDK gives you the same tools, agent loop, and context management that power Claude Code.

**Note:** The CLI was previously called "headless mode." The `-p` flag and all CLI options work the same way.

---

## Basic Usage

Add the `-p` (or `--print`) flag to any `claude` command to run it non-interactively. All [CLI options](/docs/en/cli-reference) work with `-p`, including:

- `--continue` for continuing conversations
- `--allowedTools` for auto-approving tools
- `--output-format` for structured output

### Simple Example

```bash
claude -p "What does the auth module do?"
```

---

## Examples

### Get Structured Output

Use `--output-format` to control how responses are returned:

- `text` (default): plain text output
- `json`: structured JSON with result, session ID, and metadata
- `stream-json`: newline-delimited JSON for real-time streaming

**Basic JSON output:**
```bash
claude -p "Summarize this project" --output-format json
```

**Structured output with JSON Schema:**
```bash
claude -p "Extract the main function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

**Parse output with jq:**
```bash
# Extract the text result
claude -p "Summarize this project" --output-format json | jq -r '.result'

# Extract structured output
claude -p "Extract function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}' \
  | jq '.structured_output'
```

### Auto-approve Tools

Use `--allowedTools` to let Claude use certain tools without prompting:

```bash
claude -p "Run the test suite and fix any failures" \
  --allowedTools "Bash,Read,Edit"
```

### Create a Commit

```bash
claude -p "Look at my staged changes and create an appropriate commit" \
  --allowedTools "Bash(git diff:*),Bash(git log:*),Bash(git status:*),Bash(git commit:*)"
```

**Note:** Slash commands like `/commit` are only available in interactive mode. In `-p` mode, describe the task you want to accomplish instead.

### Customize the System Prompt

Use `--append-system-prompt` to add instructions while keeping Claude Code's default behavior:

```bash
gh pr diff "$1" | claude -p \
  --append-system-prompt "You are a security engineer. Review for vulnerabilities." \
  --output-format json
```

See [system prompt flags](/docs/en/cli-reference#system-prompt-flags) for more options including `--system-prompt` to fully replace the default prompt.

### Continue Conversations

Use `--continue` to continue the most recent conversation, or `--resume` with a session ID to continue a specific conversation:

```bash
# First request
claude -p "Review this codebase for performance issues"

# Continue the most recent conversation
claude -p "Now focus on the database queries" --continue
claude -p "Generate a summary of all issues found" --continue
```

**Resume a specific conversation:**
```bash
session_id=$(claude -p "Start a review" --output-format json | jq -r '.session_id')
claude -p "Continue that review" --resume "$session_id"
```

---

## Next Steps

- **[Agent SDK quickstart](https://platform.claude.com/docs/en/agent-sdk/quickstart)** - Build your first agent with Python or TypeScript
- **[CLI reference](/docs/en/cli-reference)** - Explore all CLI flags and options
- **[GitHub Actions](/docs/en/github-actions)** - Use the Agent SDK in GitHub workflows
- **[GitLab CI/CD](/docs/en/gitlab-ci-cd)** - Use the Agent SDK in GitLab pipelines
