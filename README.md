# AgentBuilder

A framework for building specialized AI agents that work with the Teradata platform. AgentBuilder provides templates, configurations, and agent definitions for developing domain-specific agents powered by Claude Code.

## Overview

AgentBuilder enables the creation of intelligent agents that can automate complex Teradata operations including database administration, security auditing, space management, SQL optimization, and more. The framework leverages Claude Code's sub-agent architecture and integrates with the teradataMCP server for comprehensive database operations.

## Key Features

- **Modular Agent Architecture**: Pre-built specialized agents for common Teradata operations
- **MCP Integration**: Direct connection to Teradata via teradataMCP server with 40+ tools
- **Security Auditing**: Comprehensive permission analysis and risk assessment
- **Space Management**: Automated database space monitoring and reallocation recommendations
- **Compression Advisor**: Analysis of compression ratios and optimization suggestions
- **SQL Optimization**: Query clustering and performance analysis capabilities
- **Agent Generation**: Meta-agent for creating new specialized agents on demand
- **Documentation Loading**: Automated fetching and management of AI documentation resources
- **Build Schema**: Consistent structure for defining new agents

## Project Structure

```
AgentBuilder/
├── .claude/
│   ├── agents/              # Agent definitions
│   │   ├── teradata/        # Teradata-specific agents
│   │   │   ├── teradata-security-auditor.md
│   │   │   └── teradata-space-manager.md
│   │   └── util/                 # Utility agents
│   │       ├── meta-agent.md     #main agent for building new agents
│   │       └── load_doc_agent.md #agent for loading documentation from URLs
│   │       └── build_schemas.md  #agent for loading database schema information
│   └── commands/            # Skill/command definitions
│       └── utils/
│           ├── all_skills.md
│           ├── load_ai_docs.md
│           └── prime.md
├── ai_docs/                 # Documentation resources
│   ├── README.md            # Document source index
│   ├── doc_overview.md
│   ├── doc_sub-agents.md
│   ├── doc_skills.md
│   ├── doc_output-styles.md
│   ├── doc_hooks-guide.md
│   ├── doc_headless.md
│   ├── doc_mcp.md
│   └── doc_teradataMCP.md
│   └── doc_TDSQL.md
├── .mcp.json               # MCP server configuration
├── AGENTS.md               # Agent documentation
├── CLAUDE.md               # Project instructions for AI
├── settings.json           # Permission settings
└── README.md               # This file
```

## Available Agents

### Teradata-Specific Agents

#### teradata-security-auditor
**Color**: Red | **Model**: Sonnet

A specialist agent for generating comprehensive security reports and analyzing user permissions within Teradata environments.

**Capabilities:**
- Analyzes database permissions and role assignments
- Reviews role hierarchies and inherited permissions
- Identifies security risks (excessive permissions, privilege escalation, grant option abuse)
- Generates actionable recommendations with SQL remediation scripts
- Performs comparative multi-user security analysis
- Provides risk categorization (Critical, High, Medium, Low)

**Use Cases:**
- Security compliance audits
- User access reviews
- Permission cleanup and optimization
- Identifying separation of duties violations
- Security hardening initiatives

#### teradata-space-manager
**Color**: Orange | **Model**: Sonnet

A DBA specialist agent focused on database space management and optimization.

**Capabilities:**
- Monitors space utilization across all databases
- Identifies databases at risk of running out of space
- Generates space reallocation recommendations
- Creates SQL scripts for space modifications
- Analyzes database hierarchy for space reallocation
- Categorizes databases by risk level (Critical >90%, Warning 80-90%, Healthy <80%)

**Use Cases:**
- Proactive space management
- Preventing out-of-space errors
- Space allocation optimization
- Capacity planning
- Database cleanup identification

### Utility Agents

#### meta-agent
**Color**: Cyan | **Model**: Opus

An expert agent architect that generates new sub-agent configuration files from user descriptions.

**Capabilities:**
- Analyzes requirements and generates complete agent definitions
- Selects appropriate tools and models for new agents
- Creates structured markdown agent configuration files
- Incorporates best practices and proper delegation descriptions
- Writes agents to the appropriate directory structure

**Use Cases:**
- Rapid agent prototyping
- Creating domain-specific agents
- Extending the framework with new capabilities

#### load_doc_agent
**Model**: Default

A research specialist for fetching and managing documentation resources.

**Capabilities:**
- Fetches markdown documentation from specified URLs
- Checks for recently updated documents (30-day threshold)
- Supports parallel document fetching
- Stores structured documentation in ai_docs/ directory
- Integrates with Firecrawl for web scraping

**Use Cases:**
- Keeping documentation up to date
- Loading AI Docs resources
- Managing knowledge base content

#### build_schemas
**Model**: Default

A database schema builder and manager.

**Capabilities:**
- Generates database schema definitions

**Use Cases:**
- input into building business agents that require database schema knowledge22

### Available Skills/Commands
- **`/utils:load_ai_docs`** - Loads or updates AI documentation resources
- **`/utils:all_skills`** - Lists all available skills from system prompt

## MCP Integration

AgentBuilder connects to a teradataMCP server providing comprehensive tooling for Teradata operations:

### Tool Categories

**Base/Core Database Tools** (9 tools)
- Database and table listing
- Query execution with bind parameters
- Column descriptions and DDL generation
- Table previews and usage analysis
- Table affinity (relationship inference)

**DBA Tools** (13 tools)
- Database space management
- Version information
- Feature and flow control metrics
- Resource usage summaries
- Session information
- Table and user SQL analysis
- Table usage impact measurement

**Quality Analysis Tools** (7 tools)
- Column summary statistics
- Missing and negative value detection
- Standard deviation and univariate statistics
- Distinct category analysis

**Security Tools** (3 tools)
- User database permissions
- User role assignments
- Role permission details

**Vector Store (TDVS) Tools** (9 tools)
- Vector store creation, update, and management
- RAG-based question answering
- Similarity search
- User permission management

**SQL Optimization Tools** (3 tools)
- Query clustering and performance analysis
- Cluster statistics analysis
- Query pattern identification

**RAG Tools** (1 tool)
- Document-based question answering workflow

**Feature Store Tools** (8 tools)
- Dataset creation from features
- Feature catalog access
- Data domain and entity management

**Plotting Tools** (4 tools)
- Line, pie, polar, and radar chart generation

## Configuration

### MCP Server Connection

```json
{
  "teradataMCP": {
    "type": "http",
    "url": "http://54.213.236.135:8001/mcp/",
    "env": {
      "DATABASE_URI": "teradata://data_scientist:password@44.232.94.89:1025/data_scientist"
    }
  }
}
```

### Permissions

The framework has pre-configured permissions for common operations:
- Bash operations: mkdir, uv, find, mv, grep, npm, ls, cp, chmod, touch
- File operations: Write, Edit
- All standard Claude Code tools

## Code Style Guidelines

When contributing to or extending this project:

- Use Teradata SQL and Python 3.12+ features and syntax
- Use 4 spaces for indentation
- Follow PEP 8 guidelines for Python code
- Use descriptive variable and function names
- Include docstrings for all functions and classes

## Getting Started

1. Ensure you have Claude Code installed and configured
2. Clone this repository
3. Configure your Teradata connection in `.mcp.json`
4. Invoke agents using the `@agent-name` syntax in Claude Code
5. Use skills with `/skill-name` syntax

## Usage Examples

### Security Audit
```
@teradata-security-auditor analyze security for user john_smith
```

### Space Management
```
@teradata-space-manager check database space utilization
```

### Create New Agent
```
@meta-agent create an agent that monitors query performance and sends alerts
```

### Load Documentation
```
/utils:load_ai_docs
```

## Extending the Framework

To create a new agent:

1. Use the meta-agent to generate a template: `@meta-agent create an agent that [description]`
2. Review and customize the generated agent definition
3. Place the agent file in the appropriate directory (`.claude/agents/teradata/` or `.claude/agents/util/`)
4. Update agent metadata (name, description, tools, model, color)
5. Test the agent with sample scenarios

## Agent Architecture

Each agent follows a consistent structure:

```markdown
---
name: agent-name
description: When to use this agent
tools: tool1, tool2, tool3
model: sonnet | opus | haiku
color: red | blue | green | yellow | purple | orange | pink | cyan
---

# Purpose
[Agent role and responsibilities]

## Instructions
[Step-by-step workflow]

## Report / Response
[Output format and structure]
```

## Recent Updates

- Reorganized agent structure into domain-specific subdirectories
- Added teradata-security-auditor for comprehensive security analysis
- Added teradata-space-manager for DBA operations
- Moved utility agents to dedicated util/ directory
- Organized skills/commands into utils/ subdirectory

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Support

[Add support information here]