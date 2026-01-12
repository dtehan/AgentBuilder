<!-- Fetched: 2025-12-31 -->
<!-- Source: https://code.claude.com/docs/en/mcp -->

# Connect Claude Code to Tools via MCP

Claude Code can connect to hundreds of external tools and data sources through the **Model Context Protocol (MCP)**, an open source standard for AI-tool integrations. MCP servers give Claude Code access to your tools, databases, and APIs.

## What You Can Do with MCP

With MCP servers connected, you can ask Claude Code to:

- **Implement features from issue trackers**: "Add the feature described in JIRA issue ENG-4521 and create a PR on GitHub."
- **Analyze monitoring data**: "Check Sentry and Statsig to check the usage of the feature described in ENG-4521."
- **Query databases**: "Find emails of 10 random users who used feature ENG-4521, based on our PostgreSQL database."
- **Integrate designs**: "Update our standard email template based on the new Figma designs that were posted in Slack"
- **Automate workflows**: "Create Gmail drafts inviting these 10 users to a feedback session about the new feature."

## Installing MCP Servers

MCP servers can be configured in three different ways:

### Option 1: Add a Remote HTTP Server

HTTP servers are recommended for connecting to remote MCP servers.

```bash
# Basic syntax
claude mcp add --transport http <name> <url>

# Real example: Connect to Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Example with Bearer token
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

### Option 2: Add a Remote SSE Server

The SSE (Server-Sent Events) transport is deprecated. Use HTTP servers instead.

```bash
# Basic syntax
claude mcp add --transport sse <name> <url>

# Real example: Connect to Asana
claude mcp add --transport sse asana https://mcp.asana.com/sse

# Example with authentication header
claude mcp add --transport sse private-api https://api.company.com/sse \
  --header "X-API-Key: your-key-here"
```

### Option 3: Add a Local Stdio Server

Stdio servers run as local processes on your machine.

```bash
# Basic syntax
claude mcp add --transport stdio <name> <command> [args...]

# Real example: Add Airtable server
claude mcp add --transport stdio airtable --env AIRTABLE_API_KEY=YOUR_KEY \
  -- npx -y airtable-mcp-server
```

**Important**: The `--` (double dash) separates Claude's CLI flags from the command and arguments passed to the MCP server.

### Managing Your Servers

```bash
# List all configured servers
claude mcp list

# Get details for a specific server
claude mcp get github

# Remove a server
claude mcp remove github

# Within Claude Code: Check server status
/mcp
```

**Tips**:
- Use `--scope` flag: `local` (default), `project`, or `user`
- Set environment variables with `--env` flags
- Configure timeout with `MCP_TIMEOUT` environment variable
- Increase output limit with `MAX_MCP_OUTPUT_TOKENS` environment variable
- Use `/mcp` to authenticate with OAuth 2.0 servers

## MCP Installation Scopes

### Local Scope
Stored in `~/.claude.json`, available only in current project. Ideal for personal servers or sensitive credentials.

```bash
claude mcp add --transport http stripe https://mcp.stripe.com
```

### Project Scope
Stored in `.mcp.json` at project root, shared with team via version control.

```bash
claude mcp add --transport http paypal --scope project https://mcp.paypal.com/mcp
```

### User Scope
Stored in `~/.claude.json`, available across all projects on your machine.

```bash
claude mcp add --transport http hubspot --scope user https://mcp.hubspot.com/anthropic
```

## Scope Hierarchy and Precedence

When servers with the same name exist at multiple scopes:
1. **Local scope** (highest priority)
2. **Project scope**
3. **User scope** (lowest priority)

## Environment Variable Expansion in .mcp.json

Claude Code supports environment variable expansion in `.mcp.json` files:

```json
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

**Syntax**:
- `${VAR}` - Expands to environment variable `VAR`
- `${VAR:-default}` - Uses `default` if `VAR` is not set

## Practical Examples

### Example: Monitor Errors with Sentry

```bash
# 1. Add the Sentry MCP server
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# 2. Use /mcp to authenticate with your Sentry account
> /mcp

# 3. Debug production issues
> "What are the most common errors in the last 24 hours?"
> "Show me the stack trace for error ID abc123"
> "Which deployment introduced these new errors?"
```

### Example: Connect to GitHub for Code Reviews

```bash
# 1. Add the GitHub MCP server
claude mcp add --transport http github https://api.githubcopilot.com/mcp/

# 2. In Claude Code, authenticate if needed
> /mcp

# 3. Work with GitHub
> "Review PR #456 and suggest improvements"
> "Create a new issue for the bug we just found"
> "Show me all open PRs assigned to me"
```

### Example: Query Your PostgreSQL Database

```bash
# 1. Add the database server with your connection string
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://readonly:[email protected]:5432/analytics"

# 2. Query your database naturally
> "What's our total revenue this month?"
> "Show me the schema for the orders table"
> "Find customers who haven't made a purchase in 90 days"
```

## Authenticate with Remote MCP Servers

Many cloud-based MCP servers require OAuth 2.0 authentication:

1. **Add the server**:
   ```bash
   claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
   ```

2. **Use /mcp within Claude Code**:
   ```bash
   > /mcp
   ```

3. Follow the steps in your browser to login

**Tips**:
- Authentication tokens are stored securely and refreshed automatically
- Use "Clear authentication" in the `/mcp` menu to revoke access
- If your browser doesn't open automatically, copy the provided URL

## Add MCP Servers from JSON Configuration

```bash
# Basic syntax
claude mcp add-json <name> '<json>'

# Example: HTTP server with JSON
claude mcp add-json weather-api '{"type":"http","url":"https://api.weather.com/mcp","headers":{"Authorization":"Bearer token"}}'

# Example: Stdio server with JSON
claude mcp add-json local-weather '{"type":"stdio","command":"/path/to/weather-cli","args":["--api-key","abc123"],"env":{"CACHE_DIR":"/tmp"}}'
```

## Import MCP Servers from Claude Desktop

```bash
# Basic syntax
claude mcp add-from-claude-desktop

# Verify the servers were imported
claude mcp list
```

**Note**: Only works on macOS and Windows Subsystem for Linux (WSL)

## Use Claude Code as an MCP Server

```bash
# Start Claude as a stdio MCP server
claude mcp serve
```

Add to Claude Desktop's `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

**Finding the full path**:
```bash
which claude
```

Then use the full path in your configuration if `claude` is not in your system PATH.

## MCP Output Limits and Warnings

- **Warning threshold**: 10,000 tokens
- **Default maximum**: 25,000 tokens
- **Configure limit**: Set `MAX_MCP_OUTPUT_TOKENS` environment variable

```bash
export MAX_MCP_OUTPUT_TOKENS=50000
claude
```

## Use MCP Resources

### Reference MCP Resources

1. **List available resources**: Type `@` in your prompt

2. **Reference a specific resource**:
   ```bash
   > Can you analyze @github:issue://123 and suggest a fix?
   > Please review the API documentation at @docs:file://api/authentication
   ```

3. **Multiple resource references**:
   ```bash
   > Compare @postgres:schema://users with @docs:file://database/user-model
   ```

**Tips**:
- Resources are automatically fetched and included as attachments
- Resource paths are fuzzy-searchable in @ mention autocomplete
- Resources can contain any type of content the MCP server provides

## Use MCP Prompts as Slash Commands

### Execute MCP Prompts

1. **Discover available prompts**: Type `/` to see all commands including MCP prompts

2. **Execute a prompt without arguments**:
   ```bash
   > /mcp__github__list_prs
   ```

3. **Execute a prompt with arguments**:
   ```bash
   > /mcp__github__pr_review 456
   > /mcp__jira__create_issue "Bug in login flow" high
   ```

**Tips**:
- MCP prompts are dynamically discovered from connected servers
- Arguments are parsed based on the prompt's defined parameters
- Prompt results are injected directly into the conversation
- MCP prompt format: `/mcp__servername__promptname`

## Enterprise MCP Configuration

### Option 1: Exclusive Control with managed-mcp.json

Deploy a `managed-mcp.json` file for complete control over MCP servers. Users cannot add or modify servers.

**System-wide paths** (require administrator privileges):
- macOS: `/Library/Application Support/ClaudeCode/managed-mcp.json`
- Linux and WSL: `/etc/claude-code/managed-mcp.json`
- Windows: `C:\Program Files\ClaudeCode\managed-mcp.json`

**Example**:
```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "sentry": {
      "type": "http",
      "url": "https://mcp.sentry.dev/mcp"
    },
    "company-internal": {
      "type": "stdio",
      "command": "/usr/local/bin/company-mcp-server",
      "args": ["--config", "/etc/company/mcp-config.json"],
      "env": {
        "COMPANY_API_URL": "https://internal.company.com"
      }
    }
  }
}
```

### Option 2: Policy-Based Control with Allowlists and Denylists

Allow users to configure their own MCP servers while enforcing restrictions.

#### Restriction Options

Each entry can restrict servers by:
1. **By server name** (`serverName`)
2. **By command** (`serverCommand`) - for stdio servers
3. **By URL pattern** (`serverUrl`) - with wildcard support

**Important**: Each entry must have exactly ONE of these three fields.

#### Example Configuration

```json
{
  "allowedMcpServers": [
    // Allow by server name
    { "serverName": "github" },
    { "serverName": "sentry" },

    // Allow by exact command (for stdio servers)
    { "serverCommand": ["npx", "-y", "@modelcontextprotocol/server-filesystem"] },
    { "serverCommand": ["python", "/usr/local/bin/approved-server.py"] },

    // Allow by URL pattern (for remote servers)
    { "serverUrl": "https://mcp.company.com/*" },
    { "serverUrl": "https://*.internal.corp/*" }
  ],
  "deniedMcpServers": [
    // Block by server name
    { "serverName": "dangerous-server" },

    // Block by exact command
    { "serverCommand": ["npx", "-y", "unapproved-package"] },

    // Block by URL pattern
    { "serverUrl": "https://*.untrusted.com/*" }
  ]
}
```

#### How Command-Based Restrictions Work

**Exact matching required**:
- Command arrays must match exactly - both command and all arguments in correct order
- `["npx", "-y", "server"]` will NOT match `["npx", "server"]`

**Stdio server behavior**:
- When allowlist contains ANY `serverCommand` entries, stdio servers MUST match one
- Stdio servers cannot pass by name alone when command restrictions are present

**Non-stdio server behavior**:
- Remote servers use URL-based matching when `serverUrl` entries exist
- If no URL entries exist, remote servers fall back to name-based matching

#### How URL-Based Restrictions Work

URL patterns support wildcards using `*` to match any sequence of characters:
- `https://mcp.company.com/*` - Allow all paths on a specific domain
- `https://*.example.com/*` - Allow any subdomain of example.com
- `http://localhost:*/*` - Allow any port on localhost

**Remote server behavior**:
- When allowlist contains ANY `serverUrl` entries, remote servers MUST match one
- Remote servers cannot pass by name alone when URL restrictions are present

#### Allowlist Behavior (`allowedMcpServers`)

- `undefined` (default): No restrictions - users can configure any MCP server
- Empty array `[]`: Complete lockdown - users cannot configure any MCP servers
- List of entries: Users can only configure servers matching by name, command, or URL pattern

#### Denylist Behavior (`deniedMcpServers`)

- `undefined` (default): No servers are blocked
- Empty array `[]`: No servers are blocked
- List of entries: Specified servers are explicitly blocked across all scopes

#### Important Notes

- **Option 1 and Option 2 can be combined**: If `managed-mcp.json` exists, it has exclusive control. Allowlists/denylists still apply to enterprise servers themselves.
- **Denylist takes absolute precedence**: If a server matches a denylist entry, it will be blocked even if on the allowlist
- **Servers pass if they match**: A server passes if it matches EITHER a name entry, a command entry, or a URL pattern (unless blocked by denylist)

---

**Security Warning**: Use third party MCP servers at your own risk - Anthropic has not verified the correctness or security of all these servers. Make sure you trust MCP servers you are installing. Be especially careful when using MCP servers that could fetch untrusted content, as these can expose you to prompt injection risk.
