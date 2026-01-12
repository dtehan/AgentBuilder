# Process Prompts

Progressive prompting system for Teradata workflows organized by domain expertise.

## Overview

This directory contains the progressive prompting architecture that routes user requests through specialized personas to appropriate process workflows.

## Architecture

```
../teradata_assistant.md (Entry Point - Root Directory)
        ↓
   [Personas]
   ↓    ↓    ↓
  DBA  DS   DE
   ↓    ↓    ↓
[Process Workflows]
   ↓         ↓
 dba/   ml/
```

## Files in This Directory

### Entry Point
- **../teradata_assistant.md** ⭐ **START HERE** (located in root directory)
  - Main routing system
  - Analyzes user requests
  - Routes to appropriate persona based on keywords and intent
  - Can route directly to function documentation for simple queries

### Personas (Expert Roles)

#### persona_dba.md
**Database Administrator Expert**
- System health and performance monitoring
- Data lineage and impact analysis
- Data quality assessments and profiling
- Table archiving and retention strategies
- Business metadata and documentation
- Routes to: `dba/` workflows

**Use when:**
- Keywords: health, performance, lineage, quality, archive, metadata
- Tasks: DBA operations, monitoring, governance

#### persona_data_scientist.md
**Data Science & Machine Learning Expert**
- ML model development and training
- Statistical analysis and hypothesis testing
- Model scoring and prediction
- Model evaluation and validation
- Feature importance and interpretability (SHAP)
- Text analytics and NLP
- Routes to: `ml/` workflows and Advanced Analytics functions

**Use when:**
- Keywords: model, prediction, classification, regression, clustering, statistics
- Tasks: Building ML models, statistical testing, predictions

#### persona_data_engineer.md
**Data Engineering Expert**
- Data preparation and cleansing
- ETL/ELT pipeline development
- Missing value handling and imputation
- Outlier detection and removal
- Feature engineering and transformation
- Data quality validation
- Routes to: `ml/` workflows and transformation functions

**Use when:**
- Keywords: prepare, clean, ETL, pipeline, missing values, outliers, transform
- Tasks: Data prep, cleansing, quality, pipeline development

## Subdirectories

### dba/
Contains 6 specialized DBA workflow processes:
- Database health assessments
- Data lineage analysis
- Data quality profiling
- Business descriptions
- Table archiving
- Controlling agent for complex workflows

See `dba/README.md` for details.

### ml/
Contains ML and data engineering workflow processes:
- Complete data preparation for ML (7-stage pipeline)
- Future: Model training workflows
- Future: Model evaluation workflows

See `ml/README.md` for details.

## How Progressive Prompting Works

### 1. User Request
User provides natural language question or task to `teradata_assistant.md`

### 2. Intent Analysis
Entry point analyzes:
- Keywords (health, model, clean, etc.)
- Task type (administration, ML, data prep)
- Domain (DBA, data science, data engineering)

### 3. Persona Routing
Routes to appropriate persona:
- **DBA keywords** → persona_dba.md
- **ML/model keywords** → persona_data_scientist.md
- **Data prep keywords** → persona_data_engineer.md
- **SQL function query** → Direct to FunctionalPrompts/

### 4. Process Selection
Persona identifies specific process needed:
- DBA → routes to dba/ workflows
- Data Scientist → routes to ml/ workflows or function docs
- Data Engineer → routes to ml/ workflows or function docs

### 5. Execution
Process workflow:
- Provides step-by-step guidance
- Generates SQL code
- References function documentation as needed
- Returns complete solution

## Example Flows

### Example 1: DBA Health Check
```
User: "Check database health"
  ↓
../teradata_assistant.md
  ↓ (keywords: health, database)
persona_dba.md
  ↓ (task: health assessment)
dba/dba_databaseHealthAssessment.md
  ↓
SQL scripts + health report
```

### Example 2: ML Model Training
```
User: "Build churn prediction model"
  ↓
../teradata_assistant.md
  ↓ (keywords: model, prediction, churn)
persona_data_scientist.md
  ↓ (task: classification model)
ml/ml_dataPreparation.md
  ↓
Prepared data
  ↓
persona_data_scientist.md (continues)
  ↓ (model selection: XGBoost)
../FunctionalPrompts/Advanced_Analytics/td_xgboost.md
  ↓
Complete ML workflow
```

### Example 3: Data Cleaning
```
User: "Clean data with missing values"
  ↓
../teradata_assistant.md
  ↓ (keywords: clean, missing values)
persona_data_engineer.md
  ↓ (task: data preparation)
ml/ml_dataPreparation.md
  ↓ (stages: profiling, imputation)
../FunctionalPrompts/Advanced_Analytics/td_simpleimputefit.md
  ↓
Cleaned dataset + validation
```

### Example 4: Direct Function Query
```
User: "How do I calculate AVG in Teradata?"
  ↓
../teradata_assistant.md
  ↓ (direct function query)
../FunctionalPrompts/Core_SQL_Functions/avg_average_ave.md
  ↓
Function syntax + examples
```

## Routing Decision Matrix

| Keywords | Route To | Output |
|----------|----------|--------|
| health, performance, monitoring | persona_dba.md → dba/ | SQL health scripts |
| lineage, dependencies, impact | persona_dba.md → dba/ | Lineage analysis |
| quality, profiling, validation | persona_dba.md → dba/ | Quality reports |
| archive, retention, cleanup | persona_dba.md → dba/ | Archiving strategy |
| model, training, prediction | persona_data_scientist.md → ml/ | ML workflow |
| classification, regression, clustering | persona_data_scientist.md → functions | Model guidance |
| prepare, clean, missing values | persona_data_engineer.md → ml/ | Data prep pipeline |
| ETL, pipeline, transform | persona_data_engineer.md → functions | ETL guidance |
| specific SQL function | Direct → FunctionalPrompts/ | Function docs |

## Adding New Content

### Adding a New Persona
1. Create `persona_[name].md` in this directory
2. Define expertise areas and routing logic
3. Update `teradata_assistant.md` routing logic
4. Add references to relevant process workflows

### Adding a New Process Workflow
1. Create new subdirectory or add to existing (dba/ or ml/)
2. Create workflow .md file with structured steps
3. Reference relevant function documentation
4. Update persona files to route to new workflow
5. Update subdirectory README.md

### Adding a New Process Category
1. Create new subdirectory (e.g., `data_governance/`)
2. Create subdirectory README.md
3. Add process workflow files
4. Create or update relevant persona
5. Update this README.md

## Best Practices

### For Users
1. **Always start at ../teradata_assistant.md** - Don't skip the entry point (located in root directory)
2. **Be specific** - More context helps routing
3. **Follow the flow** - Let personas route you to processes
4. **Reference outputs** - Personas provide SQL you can execute

### For AI Assistants
1. **Respect the hierarchy** - Entry → Persona → Process → Function
2. **Don't skip layers** - Each layer adds value and context
3. **Load on-demand** - Only read relevant documentation
4. **Follow references** - Process files reference specific functions

### For Content Creators
1. **Clear separation** - Each file has single responsibility
2. **Reference, don't duplicate** - Link to function docs instead of copying
3. **Examples matter** - Include practical SQL code
4. **Document arguments** - Specify expected inputs clearly

## File Naming Conventions

- **Entry point**: `teradata_assistant.md`
- **Personas**: `persona_[role].md`
- **DBA processes**: `dba_[process_name].md`
- **ML processes**: `ml_[process_name].md`
- **README files**: `README.md` in each directory

## Related Documentation

- **Entry point**: `../teradata_assistant.md` (Main entry point in root directory)
- **System overview**: `../CLAUDE.MD`
- **Project README**: `../README.md`
- **Function index**: `../FunctionalPrompts/INDEX.md`
- **DBA workflows**: `dba/README.md`
- **ML workflows**: `ml/README.md`

---

**Ready to start?**
Open `../teradata_assistant.md` and provide your task or question!
