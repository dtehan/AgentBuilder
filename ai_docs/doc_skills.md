<!-- Fetched: 2025-12-31 -->
<!-- Source: https://code.claude.com/docs/en/skills -->

# Agent Skills - Claude Code Documentation

## Overview

Agent Skills are markdown files that teach Claude how to do something specific. They extend Claude's capabilities in Claude Code by providing specialized knowledge for tasks like reviewing PRs using team standards, generating commit messages in preferred formats, or querying company databases.

**Key Concept:** Skills are **model-invoked** - Claude automatically decides which Skills to use based on your request without needing explicit activation.

---

## Create Your First Skill

### Step 1: Check Available Skills

```
What Skills are available?
```

Claude will list any Skills currently loaded.

### Step 2: Create the Skill Directory

Personal Skills are available across all projects:

```bash
mkdir -p ~/.claude/skills/explaining-code
```

### Step 3: Write SKILL.md

Every Skill requires a `SKILL.md` file with YAML metadata and Markdown instructions.

Example: `~/.claude/skills/explaining-code/SKILL.md`

```markdown
---
name: explaining-code
description: Explains code with visual diagrams and analogies. Use when explaining how code works, teaching about a codebase, or when the user asks "how does this work?"
---

When explaining code, always include:

1. **Start with an analogy**: Compare the code to something from everyday life
2. **Draw a diagram**: Use ASCII art to show the flow, structure, or relationships
3. **Walk through the code**: Explain step-by-step what happens
4. **Highlight a gotcha**: What's a common mistake or misconception?

Keep explanations conversational. For complex concepts, use multiple analogies.
```

### Step 4: Load and Verify

Exit and restart Claude Code, then verify:

```
What Skills are available?
```

### Step 5: Test the Skill

```
How does this code work?
```

Claude should ask to use the `explaining-code` Skill, then include an analogy and ASCII diagram.

---

## How Skills Work

### Discovery → Activation → Execution

1. **Discovery**: Claude loads only the name and description of each available Skill
2. **Activation**: When your request matches a Skill's description, Claude asks for confirmation
3. **Execution**: Claude follows the Skill's instructions and loads referenced files as needed

---

## Where Skills Live

| Location | Path | Applies to |
|----------|------|-----------|
| Enterprise | See managed settings | All users in organization |
| Personal | `~/.claude/skills/` | You, across all projects |
| Project | `.claude/skills/` | Anyone in this repository |
| Plugin | Bundled with plugins | Anyone with plugin installed |

**Priority:** Enterprise > Personal > Project > Plugin

---

## When to Use Skills vs Other Options

| Use this | When you want to… | When it runs |
|----------|-------------------|------------|
| **Skills** | Give Claude specialized knowledge | Claude chooses when relevant |
| **Slash commands** | Create reusable prompts | You type `/command` |
| **CLAUDE.md** | Set project-wide instructions | Every conversation |
| **Subagents** | Delegate tasks separately | Claude delegates or you invoke |
| **Hooks** | Run scripts on events | On specific tool events |
| **MCP servers** | Connect to external tools/data | Claude calls as needed |

---

## Configure Skills

### SKILL.md Structure

```markdown
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it
---

# Your Skill Name

## Instructions
Provide clear, step-by-step guidance for Claude.

## Examples
Show concrete examples of using this Skill.
```

### Available Metadata Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase letters, numbers, hyphens (max 64 chars) |
| `description` | Yes | What it does and when to use (max 1024 chars) - Claude uses this for activation |
| `allowed-tools` | No | Tools Claude can use without asking permission |
| `model` | No | Specific model to use (e.g., `claude-sonnet-4-20250514`) |

### Update or Delete a Skill

- **Update**: Edit `SKILL.md` directly
- **Delete**: Delete the Skill directory
- **Apply changes**: Exit and restart Claude Code

---

## Progressive Disclosure Pattern

Keep `SKILL.md` under 500 lines. Use supporting files for detailed documentation:

```
my-skill/
├── SKILL.md (required - overview and navigation)
├── reference.md (detailed API docs)
├── examples.md (usage examples)
└── scripts/
    └── helper.py (utility script)
```

### Example SKILL.md with References

```markdown
---
name: pdf-processing
description: Extract text, fill forms, merge PDFs. Use when working with PDF files, forms, or document extraction.
allowed-tools: Read, Bash(python:*)
---

# PDF Processing

## Quick start

Extract text:
```python
import pdfplumber
with pdfplumber.open("doc.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

For form filling, see [FORMS.md](FORMS.md).
For detailed API reference, see [REFERENCE.md](REFERENCE.md).

## Utility scripts

Run the validation script:
```bash
python scripts/validate_form.py input.pdf
```
```

---

## Restrict Tool Access with allowed-tools

Use `allowed-tools` to limit which tools Claude can use when a Skill is active:

```yaml
---
name: reading-files-safely
description: Read files without making changes. Use when you need read-only file access.
allowed-tools: Read, Grep, Glob
---

# Safe File Reader

This Skill provides read-only file access.

## Instructions
1. Use Read to view file contents
2. Use Grep to search within files
3. Use Glob to find files by pattern
```

---

## Use Skills with Subagents

Subagents don't automatically inherit Skills. Give custom subagents access to specific Skills in `.claude/agents/`:

```yaml
# .claude/agents/code-reviewer/AGENT.md
---
name: code-reviewer
description: Review code for quality and best practices
skills: pr-review, security-check
---
```

---

## Distribute Skills

- **Project Skills**: Commit `.claude/skills/` to version control
- **Plugins**: Create `skills/` directory in plugin with `SKILL.md` files
- **Enterprise**: Deploy organization-wide through managed settings

---

## Examples

### Simple Skill (Single File)

```
commit-helper/
└── SKILL.md
```

**SKILL.md:**
```markdown
---
name: generating-commit-messages
description: Generates clear commit messages from git diffs. Use when writing commit messages or reviewing staged changes.
---

# Generating Commit Messages

## Instructions

1. Run `git diff --staged` to see changes
2. I'll suggest a commit message with:
   - Summary under 50 characters
   - Detailed description
   - Affected components

## Best practices

- Use present tense
- Explain what and why, not how
```

### Multi-File Skill with Progressive Disclosure

```
pdf-processing/
├── SKILL.md
├── FORMS.md
├── REFERENCE.md
└── scripts/
    ├── fill_form.py
    └── validate.py
```

---

## Troubleshooting

### Skill Not Triggering

The description is how Claude decides whether to use your Skill. Good descriptions answer:

1. **What does this Skill do?** - List specific capabilities
2. **When should Claude use it?** - Include trigger terms users would say

**Good example:**
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

### Skill Doesn't Load

**Check file path:**
- Personal: `~/.claude/skills/my-skill/SKILL.md`
- Project: `.claude/skills/my-skill/SKILL.md`
- Filename must be exactly `SKILL.md` (case-sensitive)

**Check YAML syntax:**
- Start with `---` on line 1 (no blank lines before)
- End with `---` before Markdown content
- Use spaces for indentation (not tabs)

**Run debug mode:**
```bash
claude --debug
```

### Skill Has Errors

- Check external packages are installed
- Ensure script permissions: `chmod +x scripts/*.py`
- Use forward slashes in paths: `scripts/helper.py` not `scripts\helper.py`

### Multiple Skills Conflict

Make each description distinct with specific trigger terms. Instead of both having "data analysis," differentiate: one for "sales data in Excel/CRM" and another for "log files and system metrics."

### Plugin Skills Not Appearing

Clear cache and reinstall:

```bash
rm -rf ~/.claude/plugins/cache
```

Then restart Claude Code and reinstall the plugin:

```bash
/plugin install plugin-name@marketplace-name
```

Verify plugin structure:
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── my-skill/
        └── SKILL.md
```

---

## Next Steps

- [Authoring best practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)
- [Agent Skills overview](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Use Skills with Agent SDK](https://docs.claude.com/en/docs/agent-sdk/skills)
