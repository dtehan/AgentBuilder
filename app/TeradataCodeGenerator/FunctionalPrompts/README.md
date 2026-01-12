# Functional Prompts

Comprehensive documentation for 131 Teradata SQL functions with syntax, examples, and use cases.

## Overview

This directory contains detailed documentation for Teradata SQL functions organized into two main categories:
1. **Core SQL Functions** (39 functions) - Basic SQL operations
2. **Advanced Analytics** (92 functions) - Machine learning and advanced analytics

## Quick Navigation

**Start here:** `INDEX.md` - Master index of all 131 functions organized by category

## Directory Structure

```
FunctionalPrompts/
├── README.md                    # This file
├── INDEX.md                     # Master index - START HERE
├── Core_SQL_Functions/          # 39 basic SQL functions
│   ├── Aggregate Functions      # 17 files: AVG, SUM, COUNT, etc.
│   ├── Window Functions         # 8 files: ROW_NUMBER, RANK, LAG, LEAD, etc.
│   ├── Numeric Functions        # 5 files: ABS, CEIL, FLOOR, MOD, etc.
│   ├── String Functions         # 2 files: CONCAT, SUBSTR
│   ├── Date/Time Functions      # 3 files: CURRENT_DATE, EXTRACT, etc.
│   └── Conditional Functions    # 4 files: DECODE, NVL, COALESCE, etc.
└── Advanced_Analytics/          # 92 advanced functions
    ├── Data Cleaning            # 4 files: PACK, UNPACK, etc.
    ├── Data Exploration         # 16 files: Statistics, histograms, outliers
    ├── Feature Engineering      # 25 files: Encoding, scaling, transformations
    ├── Model Training           # 9 files: XGBoost, GLM, KMeans, SVM, etc.
    ├── Model Scoring            # 9 files: Prediction functions
    ├── Model Evaluation         # 6 files: Metrics, ROC, SHAP
    ├── Text Analytics           # 7 files: NER, sentiment, TF-IDF
    ├── Hypothesis Testing       # 4 files: ANOVA, Chi-Square, etc.
    └── Path Analysis            # 3 files: Attribution, nPath, sessionize
```

## Function Documentation Format

Each function documentation file follows a consistent structure:

```markdown
# FUNCTION_NAME

### Function Name
Official names and aliases

### Description
What the function does and its characteristics

### When the Function Would Be Used
Business and analytical use cases

### Syntax
Official Teradata SQL syntax with parameters

### Code Examples
5-10 practical, production-ready examples

### Related Functions (when applicable)
Links to similar or complementary functions
```

## Core SQL Functions (39 functions)

### Aggregate Functions (17 files)
Functions that operate on sets of rows and return a single result.

**Key Functions**:
- `avg_average_ave.md` - Calculate arithmetic average
- `sum.md` - Sum numeric values
- `count.md` - Count rows or non-null values
- `minimum.md` / `maximum.md` - Find min/max values
- `stddev_samp.md` / `stddev_pop.md` - Standard deviation
- `var_samp.md` / `var_pop.md` - Variance
- `corr.md` - Pearson correlation coefficient
- `covar_samp.md` / `covar_pop.md` - Covariance

**Use Cases**:
- Statistical analysis
- Data profiling
- Business metrics
- Performance reporting

### Window/Analytic Functions (8 files)
Functions that perform calculations across result sets.

**Key Functions**:
- `row_number.md` - Sequential row numbering
- `rank.md` - Ranking with gaps for ties
- `dense_rank.md` - Ranking without gaps
- `percent_rank.md` - Relative position as percentage
- `ntile.md` - Divide into equal groups
- `lag.md` - Access previous row value
- `lead.md` - Access next row value
- `nth_value.md` - Access Nth row value

**Use Cases**:
- Ranking and top-N queries
- Time series analysis
- Comparison across rows
- Running calculations

### Numeric Functions (5 files)
Scalar functions for numeric operations.

**Key Functions**:
- `abs.md` - Absolute value
- `ceil___ceiling.md` - Round up to nearest integer
- `floor.md` - Round down to nearest integer
- `mod.md` - Remainder after division
- `power___exp___sqrt___round___truncate.md` - Advanced math operations

**Use Cases**:
- Mathematical calculations
- Data transformations
- Rounding and precision control

### String Functions (2 files)
Text manipulation and processing.

**Key Functions**:
- `concat__.md` - Concatenate strings
- `substr___substring.md` - Extract substring

**Use Cases**:
- Text processing
- Data parsing
- String manipulation

### Date/Time Functions (3 files)
Temporal data handling.

**Key Functions**:
- `current_date___date.md` - Get current date
- `extract.md` - Extract date components (year, month, day)
- `add_months___date_add___date_sub.md` - Date arithmetic

**Use Cases**:
- Time-based filtering
- Date calculations
- Temporal analysis

### Conditional Functions (4 files)
Logic and conditional operations.

**Key Functions**:
- `decode.md` - Conditional value mapping
- `nvl___coalesce.md` - Replace NULL with value
- `nvl2.md` - Conditional on NULL status
- `greatest___least.md` - Max/min from list

**Use Cases**:
- NULL handling
- Conditional logic
- Data transformations

## Advanced Analytics (92 functions)

### Data Cleaning (4 files)
Data format conversion and quality.

**Key Functions**:
- `pack.md` / `unpack.md` - Data compression
- `stringsimilarity.md` - String matching
- `td_convertto.md` - Format conversion

### Data Exploration (16 files)
Statistical analysis and data profiling.

**Key Functions**:
- `td_univariatestatistics.md` - Comprehensive statistics
- `td_categoricalsummary.md` - Categorical profiling
- `td_columnsummary.md` - Column statistics
- `td_histogram.md` - Distribution analysis
- `td_outlierfilterfit.md` / `td_outlierfiltertransform.md` - Outlier detection
- `td_getrowswithmissingvalues.md` / `td_getrowswithoutmissingvalues.md` - Missing value analysis

**Use Cases**:
- Data profiling
- Quality assessment
- Distribution analysis
- Outlier detection

### Feature Engineering (25 files)
Transform and create features for ML.

**Scaling**:
- `td_scalefit.md` / `td_scaletransform.md` - Standardization, min-max

**Encoding**:
- `td_onehotencodingfit.md` / `td_onehotencodingtransform.md` - One-hot encoding
- `td_ordinalencodingfit.md` / `td_ordinalencodingtransform.md` - Ordinal encoding
- `td_targetencodingfit.md` / `td_targetencodingtransform.md` - Target encoding

**Transformation**:
- `td_bincodefit.md` / `td_bincodetransform.md` - Binning
- `td_polynomialfeaturesfit.md` / `td_polynomialfeaturestransform.md` - Polynomial features
- `td_pivoting.md` / `td_unpivoting.md` - Data reshaping

**Use Cases**:
- Feature scaling for ML
- Categorical encoding
- Feature creation
- Data transformation

### Model Training (9 files)
Machine learning model development.

**Key Functions**:
- `td_xgboost.md` - XGBoost (best performance)
- `td_decisionforest.md` - Random forest (interpretable)
- `td_glm.md` - Generalized linear models
- `td_kmeans.md` - K-Means clustering
- `td_svm.md` - Support Vector Machine
- `td_naivebayes.md` - Naive Bayes classifier
- `td_knn.md` - K-Nearest Neighbors
- `td_oneclasssvm.md` - Anomaly detection

**Use Cases**:
- Classification problems
- Regression problems
- Clustering and segmentation
- Anomaly detection

### Model Scoring (9 files)
Generate predictions from trained models.

**Key Functions**:
- `td_xgboostpredict.md` - XGBoost predictions
- `td_decisionforestpredict.md` - Decision forest predictions
- `td_glmpredict.md` - GLM predictions
- `td_kmeanspredict.md` - Cluster assignment
- `td_svmpredict.md` - SVM predictions
- `td_naivebayespredict.md` - Naive Bayes predictions

**Use Cases**:
- Batch scoring
- Real-time predictions
- Model deployment

### Model Evaluation (6 files)
Assess model performance.

**Key Functions**:
- `td_classificationevaluator.md` - Classification metrics (accuracy, precision, recall, F1)
- `td_regressionevaluator.md` - Regression metrics (RMSE, MAE, R²)
- `td_roc.md` - ROC curve and AUC
- `td_shap.md` - Feature importance and interpretability
- `td_silhouette.md` - Clustering quality
- `td_traintestsplit.md` - Dataset splitting

**Use Cases**:
- Model validation
- Performance comparison
- Feature importance
- Model selection

### Text Analytics (7 files)
Natural language processing.

**Key Functions**:
- `td_sentimentextractor.md` - Sentiment analysis
- `td_nerextractor.md` - Named Entity Recognition
- `td_tfidf.md` - TF-IDF calculation
- `td_wordembeddings.md` - Word vectors
- `td_textparser.md` - Text parsing
- `td_ngramsplitter.md` - N-gram tokenization
- `td_naivebayestextclassifiertrainer.md` - Text classification

**Use Cases**:
- Sentiment analysis
- Document classification
- Entity extraction
- Text mining

### Hypothesis Testing (4 files)
Statistical significance testing.

**Key Functions**:
- `td_anova.md` - Analysis of variance
- `td_chisq.md` - Chi-square test
- `td_ftest.md` - F-test
- `td_ztest.md` - Z-test

**Use Cases**:
- A/B testing
- Statistical significance
- Group comparisons
- Hypothesis validation

### Path Analysis (3 files)
Sequential pattern analysis.

**Key Functions**:
- `td_npath.md` - Pattern path analysis
- `td_sessionize.md` - Session identification
- `td_attribution.md` - Attribution modeling

**Use Cases**:
- Customer journey analysis
- Conversion funnel analysis
- Attribution modeling
- Sequential patterns

## How to Use This Documentation

### 1. Finding Functions

**By Category**: Use `INDEX.md` to browse functions organized by category

**By Name**: If you know the function name, navigate directly to the file

**By Use Case**: Look at the category descriptions above to find relevant functions

### 2. Reading Function Documentation

Each function file contains:
1. **Function Name** - Official name and aliases
2. **Description** - What it does
3. **When to Use** - Business scenarios
4. **Syntax** - Official Teradata SQL syntax
5. **Examples** - 5-10 production-ready code samples

### 3. Integration with Process Workflows

Function documentation is referenced by:
- **DBA Workflows** (`../ProcessPrompts/dba/`) - Use Core SQL functions
- **ML Workflows** (`../ProcessPrompts/ml/`) - Use Advanced Analytics functions
- **Persona Files** (`../ProcessPrompts/persona_*.md`) - Reference relevant functions

### 4. Progressive Prompting Flow

```
User Question
  ↓
teradata_assistant.md (if needed)
  ↓
Persona (if needed)
  ↓
Process Workflow (if needed)
  ↓
Function Documentation (you are here)
```

**For simple function queries**, you can go directly to the function file.

**For complex tasks**, start at `teradata_assistant.md` and let the system route you.

## Function Categories Quick Reference

| Category | Count | Purpose | Access Path |
|----------|-------|---------|-------------|
| Aggregate | 17 | Statistical aggregations | Core_SQL_Functions/ |
| Window | 8 | Row-based analytics | Core_SQL_Functions/ |
| Numeric | 5 | Math operations | Core_SQL_Functions/ |
| String | 2 | Text manipulation | Core_SQL_Functions/ |
| Date/Time | 3 | Temporal operations | Core_SQL_Functions/ |
| Conditional | 4 | Logic and NULL handling | Core_SQL_Functions/ |
| Data Cleaning | 4 | Format conversion | Advanced_Analytics/ |
| Data Exploration | 16 | Profiling and statistics | Advanced_Analytics/ |
| Feature Engineering | 25 | ML feature creation | Advanced_Analytics/ |
| Model Training | 9 | ML model development | Advanced_Analytics/ |
| Model Scoring | 9 | Predictions | Advanced_Analytics/ |
| Model Evaluation | 6 | Performance metrics | Advanced_Analytics/ |
| Text Analytics | 7 | NLP operations | Advanced_Analytics/ |
| Hypothesis Testing | 4 | Statistical tests | Advanced_Analytics/ |
| Path Analysis | 3 | Sequential patterns | Advanced_Analytics/ |

## Example Use Cases

### Statistical Analysis
```
Use: AVG, SUM, COUNT, STDDEV, CORR
Path: Core_SQL_Functions/
Example: Calculate sales statistics by region
```

### Data Quality Assessment
```
Use: TD_UnivariateStatistics, TD_GetRowsWithMissingValues, COUNT
Path: Advanced_Analytics/ and Core_SQL_Functions/
Example: Profile dataset and identify quality issues
```

### ML Model Development
```
Use: TD_ScaleFit, TD_OneHotEncodingFit, TD_XGBoost, TD_ClassificationEvaluator
Path: Advanced_Analytics/
Example: Build and evaluate a classification model
```

### Time Series Analysis
```
Use: LAG, LEAD, ROW_NUMBER, EXTRACT, date arithmetic
Path: Core_SQL_Functions/
Example: Calculate month-over-month growth
```

## Technical Details

- **Teradata Version**: 17.20
- **Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf)
- **Generated**: November 22, 2025
- **Total Functions**: 131
- **Documentation Standard**: Consistent format across all files

## Tips for Using Function Documentation

1. **Start with INDEX.md** - Browse by category to find relevant functions
2. **Check aliases** - Many functions have multiple names (e.g., AVG/AVERAGE/AVE)
3. **Read examples** - Each file has 5-10 practical examples
4. **Production-ready** - All SQL examples are tested and ready to use
5. **Combine functions** - Many tasks require multiple functions working together

## Related Documentation

- **Entry point**: `../ProcessPrompts/teradata_assistant.md`
- **Process workflows**: `../ProcessPrompts/`
- **System overview**: `../CLAUDE.MD`
- **Project README**: `../README.md`

---

**Start browsing:** Open `INDEX.md` to see all 131 functions organized by category!
