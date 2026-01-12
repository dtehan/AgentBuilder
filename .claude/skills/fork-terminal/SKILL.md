---
name: fork-terminal-skill
description: A skill that allows forking terminal sessions. Use this when the user requests to `fork a terminal` or `create a terminal` or `fork session` or `new terminal: <command>`.
---

# Purpose

Fork terminal sessions upon user request. using raw cli command.
Follow the `instructions`, execute the `workflow`, based on the `cookbooks`.

## Variables

ENABLED_RAW_CLI_COMMANDS: true
ENABLED_GEMINI_CLI: false
ENABLED_CLAUDE_CODE: true
AGENTIC_CODING_TOOLS: claude code

## Instructions

- based on the user's request, follow the `cookbooks` to determine which tool to use.

### Fork Summary User Prompt

- IF: The user requests a frk terminal with a summary.  This ONLY works fr our agentic coding tools `AGENTIC_CODING_TOOLS`. The tool must be enables as well
- THEN: 
    - read the template `.claude/skills/fork-terminal/prompts/fork_user_summary_prompt.md` file  and replace with the history of the conversation between you and the user so far.
    - include the next users request in the `Next User Request` section.
    - `.claude/skills/fork-terminal/prompts/fork_user_summary_prompt.md` file will be what you pass into the PROMPT parameter of the agentic coding tool.
    - IMPORTANT: to be clear, don't update the file `.claude/skills/fork-terminal/prompts/fork_user_summary_prompt.md` file, only read it and use it to craft a new prompt in the structure provided for the new fork agent
- EXAMPLES:
    - "fork terminal use claude code to <xyz> summarize work so far"
    - "spin up a terminal running claude code with a summary of the conversation so far and run <xyz> including summary"


## Workflow

1. understand the user's request.
2. READ: `.claude/skills/fork-terminal/tools/fork_terminal.py` to understand our tooling.
3. identify the appropriate cookbook based on the request.
4. execute `.claude/skills/fork-terminal/tools/fork_terminal.py: fork_terminal(command: str)` with the command from the user's request.

## Cookbooks

### Raw CLI Commands
- IF: the user requests a non-agentic coding tool AND `ENABLED_RAW_CLI_COMMANDS` is true.
- THEN: read and execute `.claude/skills/fork-terminal/cookbooks/cli-command.md`
- EXAMPLES: 
    - "create a new terminal to <xyz> with ffmpeg"
    - "fork a terminal to run <xyz> with curl"

### Claude Code Agent
- IF: the user requests an agentic coding tool AND `ENABLED_CLAUDE_CODE` is true.
- THEN: read and execute `.claude/skills/fork-terminal/cookbooks/claude-code.md`
- EXAMPLES:
    - "create a claude code agent to run <xyz>"
    - "fork a terminal with a claude code agent to execute <xyz>"
    
