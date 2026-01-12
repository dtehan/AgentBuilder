# AgentBuilder

A framework for building specialized AI agents that work with the Teradata platform. AgentBuilder provides templates, configurations, and agent definitions for developing domain-specific agents powered by Claude Code.

## Overview

AgentBuilder enables the creation of intelligent agents that can automate complex Teradata operations including database administration, security auditing, space management, SQL optimization, and more. The framework leverages Claude Code's sub-agent architecture and integrates with the teradataMCP server for comprehensive database operations.

## Project Structure

```
AgentBuilder/
├── .claude/
│   ├── agents/              # Agent definitions
│   │   ├── teradata/        # Teradata-specific agents
│   │   │   ├── teradata-code-generator.md           # Main routing agent (entry point)
│   │   │   ├── teradata-security-auditor.md
│   │   │   ├── teradata-space-manager.md
│   │   │   ├── compression-advisor.md
│   │   │   └── teradata-statistics-collector.md
│   │   ├── business/        # Business domain agents
│   │   │   └── retail-analytics.md
│   │   └── util/            # Utility agents
│   │       ├── meta-agent.md          # Main agent for building new agents
│   │       ├── load_doc_agent.md      # Agent for loading documentation from URLs
│   │       ├── build_schemas.md       # Agent for loading database schema information
│   │       └── build_DBHierarchy.md   # Agent for generating database hierarchy docs
│   └── commands/            # Skill/command definitions
│       └── utils/
│           ├── all_skills.md
│           ├── load_ai_docs.md
│           └── prime.md
├── app/                     # TeradataCodeGenerator prompt library
│   └── TeradataCodeGenerator/
│       ├── FunctionalPrompts/
│       │   ├── Core_SQL_Functions/      # 126+ SQL function prompts
│       │   ├── Advanced_Analytics/      # Advanced analytics prompts
│       │   └── INDEX.md                 # Function index
│       └── ProcessPrompts/
│           ├── persona_dba.md           # DBA persona routing
│           ├── persona_data_scientist.md # Data Scientist persona routing
│           ├── persona_data_engineer.md  # Data Engineer persona routing
│           ├── dba/                     # DBA process workflows (6)
│           └── ml/                      # ML process workflows
├── ai_docs/                 # Documentation resources
│   ├── README.md            # Document source index
│   ├── doc_overview.md
│   ├── doc_sub-agents.md
│   ├── doc_skills.md
│   ├── doc_output-styles.md
│   ├── doc_hooks-guide.md
│   ├── doc_headless.md
│   ├── doc_mcp.md
│   ├── doc_teradataMCP.md
│   └── doc_TDSQL.md
├── .mcp.json               # MCP server configuration
├── AGENTS.md               # Agent documentation
├── CLAUDE.md               # Project instructions for AI
├── settings.json           # Permission settings
└── README.md               # This file
```

## Available Agents

### Teradata-Specific Agents

#### Agent: teradata-security-auditor
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

#### Agent: teradata-space-manager
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

#### Agent: compression-advisor
**Model**: Default

An analytics specialist agent that performs rigorous cost-benefit analysis to identify optimal Multi-Value Compression (MVC) candidates.

**Capabilities:**
- Analyzes tables using compression equation for accurate space savings
- Identifies high-cardinality columns suitable for compression
- Generates production-ready ALTER TABLE statements
- Calculates compression ratios and storage optimization
- Provides cost-benefit analysis for compression decisions

**Use Cases:**
- Storage optimization initiatives
- Reducing table space consumption
- Identifying compression opportunities across databases
- Performance improvement through I/O reduction
- Cost reduction in cloud environments

#### Agent: teradata-statistics-collector
**Model**: Default

A specialist agent for Teradata statistics analysis and maintenance.

**Capabilities:**
- Identifies missing or stale statistics
- Analyzes statistics health across databases
- Generates optimized COLLECT STATS recommendations
- Improves query optimizer performance
- Provides statistics maintenance schedules

**Use Cases:**
- Query performance optimization
- Statistics health assessment
- Proactive statistics maintenance
- Troubleshooting slow queries
- Database performance tuning

#### Agent: teradata-code-generator
**Color**: Orange | **Model**: Sonnet

An intelligent routing agent that serves as the main entry point for all Teradata assistance. Uses progressive prompting to route requests to specialized personas based on task analysis.

**Capabilities:**
- Routes requests to appropriate persona (DBA, Data Scientist, Data Engineer)
- Analyzes user intent from keywords and context
- Progressive prompting through hierarchical workflow structure
- Access to 126+ documented Teradata SQL functions
- Coordinates multi-persona workflows for complex tasks
- Direct SQL function lookup and documentation

**Personas:**
1. **Database Administrator (DBA)**: Health assessments, performance monitoring, lineage, data quality, archiving, metadata, maintenance
2. **Data Scientist**: ML model development, statistical analysis, predictive modeling, feature engineering, model evaluation
3. **Data Engineer**: Data preparation, ETL/ELT pipelines, data transformation, quality validation, missing value handling, outlier detection

**Use Cases:**
- Unified entry point for all Teradata tasks
- Automatic routing to domain experts
- Complex workflows requiring multiple specializations
- SQL function documentation and examples
- End-to-end data science pipelines (prep → train → deploy)

### Business Domain Agents

#### Agent: retail-analytics
**Model**: Default

A business intelligence specialist for analyzing retail data and generating insights.

**Capabilities:**
- Analyzes sales, customer, product, and inventory data
- Generates business reports and dashboards
- Performs statistical analysis on retail datasets
- Answers questions about retail_sample_data schema
- Creates data-driven business insights

**Use Cases:**
- Sales performance analysis
- Customer behavior insights
- Product performance tracking
- Inventory optimization
- Business intelligence reporting

### Utility Agents

#### Agent: meta-agent
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

#### Agent: load_doc_agent
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

#### Agent: build_schemas
**Model**: Default

A database schema documentation generator that creates comprehensive markdown documentation from existing SQL database schemas.

**Capabilities:**
- Generates structured markdown documentation for database schemas
- Extracts table structures, column descriptions, and relationships
- Documents table usage patterns and affinities
- Creates preview data samples
- Integrates with teradataMCP for schema analysis

**Use Cases:**
- Building business agents that require database schema knowledge
- Database documentation generation
- Onboarding new developers to data models
- Data governance and lineage tracking
- Schema change management

#### Agent: build_DBHierarchy
**Model**: Default

A database hierarchy documentation generator that creates structured documentation of database relationships.

**Capabilities:**
- Generates database hierarchy documentation in markdown format
- Maps parent-child relationships between databases
- Documents database structure and organization
- Creates visual hierarchy representations
- Integrates with teradataMCP for metadata extraction

**Use Cases:**
- Understanding database architecture
- Database organization documentation
- Impact analysis for database changes
- Security boundary identification
- Data governance hierarchy mapping

### Available Skills/Commands
- **`/utils:all_skills`** - Lists all available skills from system prompt

- **fork-terminal skill** - allows the user to open a terminal session within Claude Code or CLI to run tasks


## TeradataCodeGenerator Prompt Library

The `app/TeradataCodeGenerator/` directory contains a comprehensive library of reusable prompts and templates for Teradata operations, organized using a **progressive prompting architecture**.

### Progressive Prompting Architecture

The TeradataCodeGenerator uses a hierarchical routing system:

```
Entry Point → Persona Files → Process Prompts → Functional Prompts
```

**Flow:**
1. **teradata-code-generator.md** (Entry Point) - Analyzes user intent and routes to appropriate persona
2. **Persona Files** - Specialized experts (DBA, Data Scientist, Data Engineer)
3. **Process Prompts** - Step-by-step workflows for specific tasks
4. **Functional Prompts** - Detailed documentation for individual SQL functions (126+ functions)

### Personas

**Database Administrator (DBA)** (`ProcessPrompts/persona_dba.md`)
- Health assessments, performance monitoring, lineage analysis
- Data quality assessments, archiving strategies
- Business metadata and documentation
- Database maintenance and optimization
- **6 DBA process workflows available**

**Data Scientist** (`ProcessPrompts/persona_data_scientist.md`)
- Machine learning model development and training
- Statistical analysis and hypothesis testing
- Predictive modeling, feature engineering
- Model evaluation and performance metrics
- **ML process workflows expanding**

**Data Engineer** (`ProcessPrompts/persona_data_engineer.md`)
- Data preparation and ETL/ELT pipelines
- Data transformation and quality validation
- Missing value handling and outlier detection
- Data profiling and integration
- **Data engineering workflows**

### Process Prompts

**DBA Process Prompts** (`ProcessPrompts/dba/`)
Process-oriented prompts for database administration tasks including maintenance, monitoring, and optimization workflows.

**ML Process Prompts** (`ProcessPrompts/ml/`)
Machine learning and predictive analytics workflow templates for Teradata ML capabilities.

### Functional Prompts (126+ Functions)

**Core SQL Functions** (40+ prompts)
Detailed prompt templates for Teradata SQL functions including:
- Date/time functions (current_date, add_months, extract)
- Aggregate functions (avg, sum, count, max, min)
- Statistical functions (stddev_samp, var_pop, kurtosis)
- Window functions (rank, lead, percent_rank)
- String and mathematical operations (mod, ceil, nvl, coalesce)
- Data transformation (pivot, decode, greatest, least)

**Advanced Analytics**
Templates for complex analytical operations and advanced SQL patterns.

### Usage
These prompts serve as building blocks for:
- Intelligent routing to domain-specific expertise
- Progressive workflow execution (entry → persona → process → function)
- Multi-persona task coordination
- Standardizing SQL function usage with 126+ documented functions
- Ensuring best practices in Teradata SQL
- End-to-end data science pipelines
- Training and documentation purposes

## MCP Integration

teradata-code-generator connects to a teradataMCP server providing comprehensive tooling for Teradata operations:

For complete list of MCP capabilities, refer to the [teradataMCP documentation](ai_docs/doc_teradataMCP.md).

## Configuration

### MCP Server Connection

```json
{
  "teradataMCP": {
    "type": "http",
    "url": "http://MCP_host_address:8001/mcp/",
    "env": {
      "DATABASE_URI": "teradata://username:password@Database_host_address:1025/default_database"
    }
  }
}
```


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

### teradata-code-generator (Unified Entry Point)
```
@teradata-code-generator Check the health of my production database
@teradata-code-generator How do I train an XGBoost model for customer churn prediction?
@teradata-code-generator I need to clean my dataset and handle missing values before analysis
@teradata-code-generator How do I calculate moving averages in Teradata?
```

### Security Audit
```
@teradata-security-auditor analyze security for user john_smith
```

### Space Management
```
@teradata-space-manager check database space utilization and identify at-risk databases
```

### Compression Analysis
```
@compression-advisor analyze compression opportunities for database retail_db
```

### Statistics Health Check
```
@teradata-statistics-collector analyze statistics for database analytics_db
```

### Retail Analytics
```
@retail-analytics analyze top 10 products by revenue for Q4 2024
```

### Build Database Schema Documentation
```
@build_schemas generate schema documentation for database customer_data
```

### Build Database Hierarchy
```
@build_DBHierarchy document the hierarchy for database prod_environment
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
