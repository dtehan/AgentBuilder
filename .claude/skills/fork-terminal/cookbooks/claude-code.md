# Purpose
create a new claude code agent to execute a command.

## Variables
DEFAULT_MODEL: sonnet
FAST_MODEL: haiku
HEAVY_MODEL: opus

## Instructions
- before running any command, run `claude --help` to check for correct usage and flags.
- always use interactive mode (so leave off -p), use the DEFAULT_MODEL unless specified otherwise by the user. if heavy processing is needed, use HEAVY_MODEL, if fast response is needed, use FAST_MODEL.
- Always run with `--dangerously-skip-permissions`, always run with `--verbose` flag.