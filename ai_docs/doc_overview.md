<!-- Fetched: 2025-12-31 -->
<!-- Source: https://code.claude.com/docs/en/overview -->

# Claude Code Overview

Claude Code is Anthropic's official CLI for Claude, an agentic coding tool that lives in your terminal and helps you turn ideas into code faster than ever before.

## Get Started in 30 Seconds

### Prerequisites
- A [Claude.ai](https://claude.ai) (recommended) or [Claude Console](https://console.anthropic.com/) account

### Installation

**macOS, Linux, WSL:**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows PowerShell:**
```powershell
irm https://claude.ai/install.ps1 | iex
```

**Windows CMD:**
```cmd
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

**Via Homebrew:**
```bash
brew install --cask claude-code
```

**Via NPM (requires Node.js 18+):**
```bash
npm install -g @anthropic-ai/claude-code
```

### Start Using Claude Code

```bash
cd your-project
claude
```

You'll be prompted to log in on first use. Claude Code automatically keeps itself up to date.

## What Claude Code Does for You

- **Build features from descriptions** - Tell Claude what you want to build in plain English. It will make a plan, write the code, and ensure it works.

- **Debug and fix issues** - Describe a bug or paste an error message. Claude Code will analyze your codebase, identify the problem, and implement a fix.

- **Navigate any codebase** - Ask anything about your team's codebase, and get a thoughtful answer back. Claude Code maintains awareness of your entire project structure, can find up-to-date information from the web, and with MCP can pull from external data sources like Google Drive, Figma, and Slack.

- **Automate tedious tasks** - Fix fiddly lint issues, resolve merge conflicts, and write release notes. Do all this in a single command from your developer machines, or automatically in CI.

## Why Developers Love Claude Code

- **Works in your terminal** - Not another chat window. Not another IDE. Claude Code meets you where you already work, with the tools you already love.

- **Takes action** - Claude Code can directly edit files, run commands, and create commits. Need more? MCP lets Claude read your design docs in Google Drive, update your tickets in Jira, or use your custom developer tooling.

- **Unix philosophy** - Claude Code is composable and scriptable. For example:
  ```bash
  tail -f app.log | claude -p "Slack me if you see any anomalies appear in this log stream"
  ```
  Your CI can run:
  ```bash
  claude -p "If there are new text strings, translate them into French and raise a PR for @lang-fr-team to review"
  ```

- **Enterprise-ready** - Use the Claude API, or host on AWS or GCP. Enterprise-grade security, privacy, and compliance is built-in.

## Next Steps

- **[Quickstart](/docs/en/quickstart)** - See Claude Code in action with practical examples
- **[Common workflows](/docs/en/common-workflows)** - Step-by-step guides for common workflows
- **[Troubleshooting](/docs/en/troubleshooting)** - Solutions for common issues with Claude Code
- **[IDE setup](/docs/en/vs-code)** - Add Claude Code to your IDE

## Additional Resources

- [About Claude Code](https://claude.com/product/claude-code) - Learn more about Claude Code on claude.com
- [Build with the Agent SDK](https://docs.claude.com/en/docs/agent-sdk/overview) - Create custom AI agents with the Claude Agent SDK
- [Host on AWS or GCP](/docs/en/third-party-integrations) - Configure Claude Code with Amazon Bedrock or Google Vertex AI
- [Settings](/docs/en/settings) - Customize Claude Code for your workflow
- [Commands](/docs/en/cli-reference) - Learn about CLI commands and controls
- [Security](/docs/en/security) - Discover Claude Code's safeguards and best practices
- [Privacy and data usage](/docs/en/data-usage) - Understand how Claude Code handles your data
