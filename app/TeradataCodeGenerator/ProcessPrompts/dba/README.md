# DBA Process Workflows

Database Administrator workflows for Teradata health, quality, lineage, and governance.

## Overview

This directory contains 6 specialized workflow processes for common database administration tasks. These workflows are accessed through the `persona_dba.md` persona.

## Available Workflows


### dba_databaseHealthAssessment.md
**System Health Assessment & Performance Monitoring**

Comprehensive database health check including:
- Space usage and capacity analysis
- Table and index statistics
- Performance metrics
- Resource consumption
- Query performance
- System bottlenecks

**Arguments**: None (or database_name)

**Output**:
- SQL scripts for health assessment
- Space utilization reports
- Performance metrics
- Recommendations for optimization

**SQL Functions Used**:
- COUNT, SUM, AVG (aggregations)
- System tables (DBC.TableSize, DBC.DiskSpace)
- Performance views

**Example Use Case**:
```
User: "Check the health of my production database"
→ Generates comprehensive health check SQL
→ Returns space, performance, and resource metrics
```

---

### dba_databaseLineage.md
**Data Lineage & Impact Analysis**

Analyzes table dependencies and data flow:
- Upstream data sources
- Downstream data consumers
- Impact analysis for changes
- Dependency mapping
- Cross-database relationships

**Arguments**: `database_name` `max_depth`
- `database_name`: Target database to analyze
- `max_depth`: How many levels deep to trace (e.g., 100)

**Output**:
- Lineage graph showing dependencies
- Upstream source tables
- Downstream dependent objects
- Impact analysis report

**SQL Functions Used**:
- Recursive queries
- System catalog tables (DBC.Tables, DBC.Columns)
- Dependency views

**Example Use Case**:
```
User: "Show me lineage for demo_user database with depth 100"
→ Traces 100 levels of dependencies
→ Maps all upstream and downstream relationships
→ Provides impact analysis for changes
```

---

### dba_databaseQuality.md
**Data Quality Assessment & Profiling**

Comprehensive data quality analysis:
- Completeness (NULL value analysis)
- Uniqueness (duplicate detection)
- Validity (data type and range checks)
- Consistency (cross-table validation)
- Statistical profiling
- Distribution analysis

**Arguments**: `database_name`

**Output**:
- Data quality scorecard
- NULL value percentages by column
- Duplicate record counts
- Data distribution statistics
- Quality improvement recommendations

**SQL Functions Used**:
- COUNT, AVG, MIN, MAX, STDDEV
- TD_UnivariateStatistics
- TD_CategoricalSummary
- TD_GetRowsWithMissingValues

**Function References**:
- `FunctionalPrompts/Advanced_Analytics/td_columnsummary.md`
- `FunctionalPrompts/Advanced_Analytics/td_univariatestatistics.md`
- `FunctionalPrompts/Advanced_Analytics/td_getrowswithmissingvalues.md`
- `FunctionalPrompts/Core_SQL_Functions/count.md`

**Example Use Case**:
```
User: "Assess data quality for demo_user database"
→ Profiles all tables in database
→ Identifies completeness, validity, consistency issues
→ Returns quality scorecard with recommendations
```

---

### dba_databaseBusinessDescription.md
**Business Metadata & Documentation**

Manages business metadata and documentation:
- Business glossary terms
- Table and column descriptions
- Business rules documentation
- Data ownership information
- Usage guidelines
- Metadata standardization

**Arguments**: `database_name`

**Output**:
- Business metadata templates
- Documentation scripts
- Glossary of business terms
- Ownership and stewardship information

**SQL Functions Used**:
- System catalog updates
- COMMENT ON statements
- Metadata management views

**Example Use Case**:
```
User: "Generate business descriptions for demo_user database"
→ Creates metadata templates
→ Provides documentation structure
→ Suggests business terms and descriptions
```

---

### dba_tableArchive.md
**Table Archiving & Retention Management**

Manages table archiving and data retention:
- Archive table creation
- Data migration scripts
- Retention policy implementation
- Cleanup procedures
- Space reclamation
- Historical data management

**Arguments**: `database_name` `retention_days`
- `database_name`: Target database
- `retention_days`: Days to retain (e.g., 7, 30, 90)

**Output**:
- Archive table DDL
- Data migration SQL
- Cleanup scripts
- Retention policy implementation
- Space savings estimates

**SQL Functions Used**:
- Date functions (CURRENT_DATE, DATE arithmetic)
- CREATE TABLE AS
- DELETE with date filters
- EXTRACT

**Function References**:
- `FunctionalPrompts/Core_SQL_Functions/current_date___date.md`
- `FunctionalPrompts/Core_SQL_Functions/extract.md`
- `FunctionalPrompts/Core_SQL_Functions/add_months___date_add___date_sub.md`

**Example Use Case**:
```
User: "Archive demo_user tables older than 7 days"
→ Identifies tables with data older than 7 days
→ Creates archive tables
→ Generates migration and cleanup scripts
→ Estimates space savings
```

---

## Workflow Routing

Users interact with DBA workflows through the routing hierarchy:

```
teradata_assistant.md
  ↓ (DBA keywords detected)
persona_dba.md
  ↓ (specific task identified)
dba/[specific_workflow].md
  ↓
SQL scripts + recommendations
```

## Keyword Routing Guide

| User Keywords | Routes To | Purpose |
|--------------|-----------|---------|
| health, performance, monitoring, system check | dba_databaseHealthAssessment.md | System health analysis |
| lineage, dependencies, impact, relationships | dba_databaseLineage.md | Dependency mapping |
| quality, profiling, validation, completeness | dba_databaseQuality.md | Data quality assessment |
| metadata, descriptions, business terms, glossary | dba_databaseBusinessDescription.md | Business documentation |
| archive, retention, cleanup, purge, historical | dba_tableArchive.md | Archiving strategy |

## Common DBA Use Cases

### 1. Production Health Check
```
Workflow: dba_databaseHealthAssessment.md
Output:
  - Space utilization by database/table
  - Query performance metrics
  - Resource consumption
  - Recommendations
```

### 2. Change Impact Analysis
```
Workflow: dba_databaseLineage.md
Input: database_name, depth
Output:
  - All dependent objects
  - Upstream data sources
  - Impact of dropping/modifying table
```

### 3. Data Quality Initiative
```
Workflow: dba_databaseQuality.md
Input: database_name
Output:
  - Quality scorecard
  - Issues by severity
  - Remediation recommendations
```

### 4. Compliance & Retention
```
Workflow: dba_tableArchive.md
Input: database_name, retention_days
Output:
  - Archive strategy
  - Compliance-ready retention policy
  - Space recovery plan
```

### 5. Documentation Sprint
```
Workflow: dba_databaseBusinessDescription.md
Input: database_name
Output:
  - Metadata templates
  - Business glossary
  - Documentation guidelines
```

## Best Practices

### Before Running DBA Workflows

1. **Understand the scope** - Know which database/tables are affected
2. **Check permissions** - Ensure you have required access
3. **Review system load** - Run intensive queries during off-peak hours
4. **Backup first** - For workflows that modify data or structure
5. **Test on dev** - Validate scripts on non-production first

### When Using Outputs

1. **Review before executing** - Understand what each SQL statement does
2. **Run incrementally** - Execute in stages, validate results
3. **Monitor performance** - Watch for long-running queries
4. **Document changes** - Keep records of actions taken
5. **Communicate** - Inform stakeholders of findings

### For Production Systems

1. **Schedule appropriately** - Run during maintenance windows
2. **Resource limits** - Set query timeout and resource limits
3. **Incremental approach** - Process in batches for large datasets
4. **Rollback plan** - Have recovery procedures ready
5. **Monitor impact** - Watch system performance during execution

## Integration with Function Documentation

DBA workflows reference SQL functions documented in:
- `../../FunctionalPrompts/Core_SQL_Functions/` - Basic SQL functions
- `../../FunctionalPrompts/Advanced_Analytics/` - Advanced analytics functions

When a workflow references a function:
1. The function name is specified (e.g., TD_UnivariateStatistics)
2. A path reference is provided to the function documentation
3. Users can read detailed syntax and examples from function files


