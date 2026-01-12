<!-- Fetched: 2025-12-31 -->
<!-- Source: https://code.claude.com/docs/en/output-styles -->

# Claude Code - Output Styles Documentation

## Overview

Output styles allow you to use Claude Code as any type of agent while keeping its core capabilities, such as running local scripts, reading/writing files, and tracking TODOs.

## Built-in Output Styles

Claude Code includes three output styles:

1. **Default** - The existing system prompt, designed to help you complete software engineering tasks efficiently.

2. **Explanatory** - Provides educational "Insights" in between helping you complete software engineering tasks. Helps you understand implementation choices and codebase patterns.

3. **Learning** - Collaborative, learn-by-doing mode where Claude will not only share "Insights" while coding, but also ask you to contribute small, strategic pieces of code yourself. Claude Code will add `TODO(human)` markers in your code for you to implement.

## How Output Styles Work

Output styles directly modify Claude Code's system prompt:

- All output styles exclude instructions for efficient output (such as responding concisely)
- Custom output styles exclude instructions for coding (such as verifying code with tests), unless `keep-coding-instructions` is true
- All output styles have their own custom instructions added to the end of the system prompt
- All output styles trigger reminders for Claude to adhere to the output style instructions during the conversation

## Changing Your Output Style

You can change your output style in two ways:

1. **Interactive menu:**
   ```
   /output-style
   ```
   Or access from the `/config` menu

2. **Direct command:**
   ```
   /output-style [style]
   ```
   Example: `/output-style explanatory`

These changes apply at the [local project level](/docs/en/settings) and are saved in `.claude/settings.local.json`. You can also directly edit the `outputStyle` field in a settings file at a different level.

## Creating a Custom Output Style

Custom output styles are Markdown files with frontmatter and the text that will be added to the system prompt:

```markdown
---
name: My Custom Style
description:
  A brief description of what this style does, to be displayed to the user
---

# Custom Style Instructions

You are an interactive CLI tool that helps users with software engineering
tasks. [Your custom instructions here...]

## Specific Behaviors

[Define how the assistant should behave in this style...]
```

You can save these files at:
- **User level:** `~/.claude/output-styles`
- **Project level:** `.claude/output-styles`

### Frontmatter Options

| Field | Purpose | Default |
|-------|---------|---------|
| `name` | Name of the output style, if not the file name | Inherits from file name |
| `description` | Description of the output style. Used only in the UI of `/output-style` | None |
| `keep-coding-instructions` | Whether to keep the parts of Claude Code's system prompt related to coding. | false |

## Comparisons to Related Features

### Output Styles vs. CLAUDE.md vs. —append-system-prompt

- **Output styles** completely "turn off" the parts of Claude Code's default system prompt specific to software engineering
- **CLAUDE.md** and **`--append-system-prompt`** do NOT edit Claude Code's default system prompt
- **CLAUDE.md** adds the contents as a user message _following_ Claude Code's default system prompt
- **`--append-system-prompt`** appends the content to the system prompt

### Output Styles vs. Agents

- **Output styles** directly affect the main agent loop and only affect the system prompt
- **Agents** are invoked to handle specific tasks and can include additional settings like the model to use, the tools they have available, and some context about when to use the agent

### Output Styles vs. Custom Slash Commands

- **Output styles** can be thought of as "stored system prompts"
- **Custom slash commands** can be thought of as "stored prompts"
