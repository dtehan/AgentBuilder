<!-- Fetched: 2025-12-31 -->
<!-- Source: https://code.claude.com/docs/en/sub-agents -->

# Subagents - Claude Code Documentation

## What are subagents?

Subagents are pre-configured AI personalities that Claude Code can delegate tasks to. Each subagent:

- Has a specific purpose and expertise area
- Uses its own context window separate from the main conversation
- Can be configured with specific tools it's allowed to use
- Includes a custom system prompt that guides its behavior

When Claude Code encounters a task that matches a subagent's expertise, it can delegate that task to the specialized subagent, which works independently and returns results.

## Key Benefits

### Context Preservation
Each subagent operates in its own context, preventing pollution of the main conversation and keeping it focused on high-level objectives.

### Specialized Expertise
Subagents can be fine-tuned with detailed instructions for specific domains, leading to higher success rates on designated tasks.

### Reusability
Once created, you can use subagents across different projects and share them with your team for consistent workflows.

### Flexible Permissions
Each subagent can have different tool access levels, allowing you to limit powerful tools to specific subagent types.

## Quick Start

To create your first subagent:

1. **Open the subagents interface**: Run the following command:
   ```
   /agents
   ```

2. **Select 'Create New Agent'**: Choose whether to create a project-level or user-level subagent

3. **Define the subagent**:
   - Describe your subagent in detail, including when Claude should use it
   - Select the tools you want to grant access to, or leave this blank to inherit all tools
   - The interface shows all available tools
   - If generating with Claude, edit the system prompt in your own editor by pressing `e`

4. **Save and use**: Your subagent is now available. Claude uses it automatically when appropriate, or you can invoke it explicitly:
   ```
   > Use the code-reviewer subagent to check my recent changes
   ```

## Subagent Configuration

### File Locations

| Type | Location | Scope | Priority |
|------|----------|-------|----------|
| **Project subagents** | `.claude/agents/` | Available in current project | Highest |
| **User subagents** | `~/.claude/agents/` | Available across all projects | Lower |

When subagent names conflict, project-level subagents take precedence over user-level subagents.

### Plugin Agents

Plugins can provide custom subagents that integrate seamlessly with Claude Code. Plugin agents work identically to user-defined agents and appear in the `/agents` interface.

- **Plugin agent locations**: plugins include agents in their `agents/` directory
- **Using plugin agents**: appear in `/agents` alongside custom agents, can be invoked explicitly or automatically

### CLI-based Configuration

You can define subagents dynamically using the `--agents` CLI flag:

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

**Priority**: CLI-defined subagents have lower priority than project-level subagents but higher priority than user-level subagents.

### File Format

Each subagent is defined in a Markdown file with this structure:

```markdown
---
name: your-sub-agent-name
description: Description of when this subagent should be invoked
tools: tool1, tool2, tool3  # Optional - inherits all tools if omitted
model: sonnet  # Optional - specify model alias or 'inherit'
permissionMode: default  # Optional - permission mode for the subagent
skills: skill1, skill2  # Optional - skills to auto-load
---

Your subagent's system prompt goes here. This can be multiple paragraphs
and should clearly define the subagent's role, capabilities, and approach
to solving problems.

Include specific instructions, best practices, and any constraints
the subagent should follow.
```

### Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier using lowercase letters and hyphens |
| `description` | Yes | Natural language description of the subagent's purpose |
| `tools` | No | Comma-separated list of specific tools. If omitted, inherits all tools from the main thread |
| `model` | No | Model to use for this subagent. Can be a model alias (`sonnet`, `opus`, `haiku`) or `'inherit'` |
| `permissionMode` | No | Permission mode for the subagent. Valid values: `default`, `acceptEdits`, `bypassPermissions`, `plan`, `ignore` |
| `skills` | No | Comma-separated list of skill names to auto-load when the subagent starts |

### Model Selection

The `model` field allows you to control which AI model the subagent uses:

- **Model alias**: Use `sonnet`, `opus`, or `haiku`
- **`'inherit'`**: Use the same model as the main conversation
- **Omitted**: Uses the default model configured for subagents (`sonnet`)

## Managing Subagents

### Using the /agents Command (Recommended)

```
/agents
```

This opens an interactive menu where you can:
- View all available subagents (built-in, user, and project)
- Create new subagents with guided setup
- Edit existing custom subagents, including their tool access
- Delete custom subagents
- See which subagents are active when duplicates exist
- Manage tool permissions with a complete list of available tools

### Direct File Management

```bash
# Create a project subagent
mkdir -p .claude/agents
echo '---
name: test-runner
description: Use proactively to run tests and fix failures
---

You are a test automation expert. When you see code changes, proactively run the appropriate tests. If tests fail, analyze the failures and fix them while preserving the original test intent.' > .claude/agents/test-runner.md

# Create a user subagent
mkdir -p ~/.claude/agents
# ... create subagent file
```

## Using Subagents Effectively

### Automatic Delegation

Claude Code proactively delegates tasks based on:
- The task description in your request
- The `description` field in subagent configurations
- Current context and available tools

To encourage more proactive subagent use, include phrases like "use PROACTIVELY" or "MUST BE USED" in your `description` field.

### Explicit Invocation

Request a specific subagent by mentioning it:

```
> Use the test-runner subagent to fix failing tests
> Have the code-reviewer subagent look at my recent changes
> Ask the debugger subagent to investigate this error
```

## Built-in Subagents

### General-purpose Subagent

A capable agent for complex, multi-step tasks that require both exploration and action.

**Key characteristics:**
- **Model**: Uses Sonnet for more capable reasoning
- **Tools**: Has access to all tools
- **Mode**: Can read and write files, execute a wider range of operations
- **Purpose**: Complex research tasks, multi-step operations, code modifications

### Plan Subagent

A specialized built-in agent designed for use during plan mode.

**Key characteristics:**
- **Model**: Uses Sonnet for more capable analysis
- **Tools**: Has access to Read, Glob, Grep, and Bash tools
- **Purpose**: Searches files, analyzes code structure, gathers context
- **Automatic invocation**: Claude automatically uses this agent in plan mode when researching the codebase

### Explore Subagent

A fast, lightweight agent optimized for searching and analyzing codebases. Operates in strict read-only mode.

**Key characteristics:**
- **Model**: Uses Haiku for fast, low-latency searches
- **Mode**: Strictly read-only - cannot create, modify, or delete files
- **Tools available**: Glob, Grep, Read, Bash (read-only commands only)

**Thoroughness levels:**
- **Quick** - Fast searches with minimal exploration
- **Medium** - Moderate exploration, balances speed and thoroughness
- **Very thorough** - Comprehensive analysis across multiple locations

## Example Subagents

### Code Reviewer

```markdown
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

### Debugger

```markdown
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not the symptoms.
```

### Data Scientist

```markdown
---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
model: sonnet
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

For each analysis:
- Explain the query approach
- Document any assumptions
- Highlight key findings
- Suggest next steps based on data

Always ensure queries are efficient and cost-effective.
```

## Best Practices

- **Start with Claude-generated agents**: Generate your initial subagent with Claude and iterate to make it personally yours
- **Design focused subagents**: Create subagents with single, clear responsibilities
- **Write detailed prompts**: Include specific instructions, examples, and constraints in your system prompts
- **Limit tool access**: Only grant tools necessary for the subagent's purpose
- **Version control**: Check project subagents into version control for team collaboration

## Advanced Usage

### Chaining Subagents

For complex workflows, you can chain multiple subagents:

```
> First use the code-analyzer subagent to find performance issues, then use the optimizer subagent to fix them
```

### Dynamic Subagent Selection

Claude Code intelligently selects subagents based on context. Make your `description` fields specific and action-oriented for best results.

### Resumable Subagents

Subagents can be resumed to continue previous conversations.

**How it works:**
- Each subagent execution is assigned a unique `agentId`
- The agent's conversation is stored in: `agent-{agentId}.jsonl`
- Resume a previous agent by providing its `agentId` via the `resume` parameter
- When resumed, the agent continues with full context from its previous conversation

**Example workflow:**

Initial invocation:
```
> Use the code-analyzer agent to start reviewing the authentication module

[Agent completes initial analysis and returns agentId: "abc123"]
```

Resume the agent:
```
> Resume agent abc123 and now analyze the authorization logic as well

[Agent continues with full context from previous conversation]
```

**Use cases:**
- Long-running research: Break down large codebase analysis into multiple sessions
- Iterative refinement: Continue refining a subagent's work without losing context
- Multi-step workflows: Have a subagent work on related tasks sequentially

## Performance Considerations

- **Context efficiency**: Agents help preserve main context, enabling longer overall sessions
- **Latency**: Subagents start with a clean slate each invocation and may add latency as they gather required context

## Related Documentation

- [Plugins](/docs/en/plugins) - Extend Claude Code with custom agents through plugins
- [Slash commands](/docs/en/slash-commands) - Learn about other built-in commands
- [Settings](/docs/en/settings) - Configure Claude Code behavior
- [Hooks](/docs/en/hooks) - Automate workflows with event handlers
