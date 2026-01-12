---
name: ML Data Preparation Workflow
allowed-tools:
description: Comprehensive workflow for preparing data for machine learning algorithms
argument-hint: [database_name] [table_name] [target_column]
---

# ML Data Preparation Workflow

## Overview
This workflow guides you through the complete data preparation process for machine learning in Teradata. It covers data structuring, cleansing, missing value handling, and encoding to ensure your data is ML-ready.

## Variables
DATABASE_NAME: $1
TABLE_NAME: $2
TARGET_COLUMN: $3

## Prerequisites
- Source table must exist in the specified database
- User must have SELECT privileges on source tables
- User must have CREATE TABLE privileges for output tables
- Teradata Analytic Functions must be available

## Workflow Stages

### Stage 1: Data Profiling and Assessment

**Objective**: Understand the data structure, quality, and characteristics before transformation.

#### Step 1.1: Assess Data Structure
```sql
-- Get column information and data types
SELECT
    ColumnName,
    ColumnType,
    ColumnLength,
    Nullable
FROM DBC.ColumnsV
WHERE DatabaseName = '${DATABASE_NAME}'
  AND TableName = '${TABLE_NAME}'
ORDER BY ColumnId;
```

#### Step 1.2: Identify Missing Values
Use **TD_GetRowsWithMissingValues** to identify rows with NULL values:
```sql
-- Create view of rows with missing values for analysis
CREATE VIEW ${DATABASE_NAME}.${TABLE_NAME}_missing_rows AS
SELECT TD_GetRowsWithMissingValues(...)
FROM ${DATABASE_NAME}.${TABLE_NAME};

-- Count missing values by column
SELECT
    COUNT(*) as total_rows,
    COUNT(column1) as column1_non_null,
    COUNT(*) - COUNT(column1) as column1_missing,
    CAST((COUNT(*) - COUNT(column1)) AS FLOAT) / COUNT(*) * 100 as column1_pct_missing
FROM ${DATABASE_NAME}.${TABLE_NAME};
```

**Reference Functions**:
- FunctionalPrompts/Advanced_Analytics/td_getrowswithmissingvalues.md
- FunctionalPrompts/Advanced_Analytics/td_getrowswithoutmissingvalues.md
- FunctionalPrompts/Advanced_Analytics/td_columnsummary.md

#### Step 1.3: Statistical Summary
Use **TD_UnivariateStatistics** for numeric columns:
```sql
-- Generate statistical summary
SELECT TD_UnivariateStatistics(...)
FROM ${DATABASE_NAME}.${TABLE_NAME};
```

**Reference Functions**:
- FunctionalPrompts/Advanced_Analytics/td_univariatestatistics.md
- FunctionalPrompts/Core_SQL_Functions/avg_average_ave.md
- FunctionalPrompts/Core_SQL_Functions/stddev_samp.md
- FunctionalPrompts/Core_SQL_Functions/minimum.md
- FunctionalPrompts/Core_SQL_Functions/maximum.md

#### Step 1.4: Categorical Data Summary
Use **TD_CategoricalSummary** for categorical columns:
```sql
-- Analyze categorical distributions
SELECT TD_CategoricalSummary(...)
FROM ${DATABASE_NAME}.${TABLE_NAME};
```

**Reference Functions**:
- FunctionalPrompts/Advanced_Analytics/td_categoricalsummary.md
- FunctionalPrompts/Core_SQL_Functions/count.md

### Stage 2: Data Cleansing

**Objective**: Remove or fix data quality issues including outliers, duplicates, and invalid values.

#### Step 2.1: Identify and Handle Outliers
Use **TD_OutlierFilterFit** to detect outliers:
```sql
-- Fit outlier detection model
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_outlier_model AS
SELECT TD_OutlierFilterFit(...)
FROM ${DATABASE_NAME}.${TABLE_NAME}
WITH DATA;

-- Transform data to remove or flag outliers
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_no_outliers AS
SELECT TD_OutlierFilterTransform(...)
FROM ${DATABASE_NAME}.${TABLE_NAME}, ${DATABASE_NAME}.${TABLE_NAME}_outlier_model
WITH DATA;
```

**Reference Functions**:
- FunctionalPrompts/Advanced_Analytics/td_outlierfilterfit.md
- FunctionalPrompts/Advanced_Analytics/td_outlierfiltertransform.md

#### Step 2.2: Remove Futile Columns
Identify columns with low variance or information:
```sql
-- Identify columns with no predictive value
SELECT TD_GetFutileColumns(...)
FROM ${DATABASE_NAME}.${TABLE_NAME};
```

**Reference Functions**:
- FunctionalPrompts/Advanced_Analytics/td_getfutilecolumns.md
- FunctionalPrompts/Advanced_Analytics/antiselect.md

#### Step 2.3: Handle Duplicates
```sql
-- Identify duplicates using ROW_NUMBER
SELECT *
FROM (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY key_column1, key_column2
            ORDER BY date_column DESC
        ) as row_num
    FROM ${DATABASE_NAME}.${TABLE_NAME}
) t
WHERE row_num = 1;
```

**Reference Functions**:
- FunctionalPrompts/Core_SQL_Functions/row_number.md

### Stage 3: Missing Data Handling

**Objective**: Address NULL values through imputation or removal strategies.

#### Step 3.1: Simple Imputation Strategy
Use **TD_SimpleImputeFit** and **TD_SimpleImputeTransform**:
```sql
-- Fit imputation model (mean, median, mode)
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_impute_model AS
SELECT TD_SimpleImputeFit(...)
FROM ${DATABASE_NAME}.${TABLE_NAME}
WITH DATA;

-- Apply imputation
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_imputed AS
SELECT TD_SimpleImputeTransform(...)
FROM ${DATABASE_NAME}.${TABLE_NAME}, ${DATABASE_NAME}.${TABLE_NAME}_impute_model
WITH DATA;
```

**Reference Functions**:
- FunctionalPrompts/Advanced_Analytics/td_simpleimputefit.md
- FunctionalPrompts/Advanced_Analytics/td_simpleimputetransform.md

#### Step 3.2: Alternative - COALESCE for Simple Cases
For simple NULL replacement:
```sql
-- Replace NULLs with default values
SELECT
    id,
    COALESCE(numeric_col, 0) as numeric_col_clean,
    COALESCE(category_col, 'UNKNOWN') as category_col_clean,
    NVL(amount, AVG(amount) OVER ()) as amount_imputed
FROM ${DATABASE_NAME}.${TABLE_NAME};
```

**Reference Functions**:
- FunctionalPrompts/Core_SQL_Functions/nvl___coalesce.md

#### Step 3.3: Remove Rows with Excessive Missing Data
```sql
-- Keep only complete rows if imputation not suitable
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_complete AS
SELECT TD_GetRowsWithoutMissingValues(...)
FROM ${DATABASE_NAME}.${TABLE_NAME}
WITH DATA;
```

**Reference Functions**:
- FunctionalPrompts/Advanced_Analytics/td_getrowswithoutmissingvalues.md

### Stage 4: Feature Engineering and Transformation

**Objective**: Transform raw data into features suitable for ML algorithms.

#### Step 4.1: Numeric Feature Scaling
Use **TD_ScaleFit** and **TD_ScaleTransform** for normalization/standardization:
```sql
-- Fit scaling model (standardization, min-max, etc.)
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_scale_model AS
SELECT TD_ScaleFit(...)
FROM ${DATABASE_NAME}.${TABLE_NAME}_imputed
WITH DATA;

-- Apply scaling transformation
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_scaled AS
SELECT TD_ScaleTransform(...)
FROM ${DATABASE_NAME}.${TABLE_NAME}_imputed, ${DATABASE_NAME}.${TABLE_NAME}_scale_model
WITH DATA;
```

**Reference Functions**:
- FunctionalPrompts/Advanced_Analytics/td_scalefit.md
- FunctionalPrompts/Advanced_Analytics/td_scaletransform.md

#### Step 4.2: Binning Continuous Variables
Use **TD_BinCodeFit** and **TD_BinCodeTransform**:
```sql
-- Create bins for continuous variables
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_bin_model AS
SELECT TD_BinCodeFit(...)
FROM ${DATABASE_NAME}.${TABLE_NAME}_scaled
WITH DATA;

-- Apply binning
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_binned AS
SELECT TD_BinCodeTransform(...)
FROM ${DATABASE_NAME}.${TABLE_NAME}_scaled, ${DATABASE_NAME}.${TABLE_NAME}_bin_model
WITH DATA;
```

**Reference Functions**:
- FunctionalPrompts/Advanced_Analytics/td_bincodefit.md
- FunctionalPrompts/Advanced_Analytics/td_bincodetransform.md

#### Step 4.3: Create Polynomial Features
Use **TD_PolynomialFeaturesFit** for non-linear relationships:
```sql
-- Create polynomial and interaction features
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_poly_model AS
SELECT TD_PolynomialFeaturesFit(...)
FROM ${DATABASE_NAME}.${TABLE_NAME}_scaled
WITH DATA;

-- Apply polynomial transformation
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_poly_features AS
SELECT TD_PolynomialFeaturesTransform(...)
FROM ${DATABASE_NAME}.${TABLE_NAME}_scaled, ${DATABASE_NAME}.${TABLE_NAME}_poly_model
WITH DATA;
```

**Reference Functions**:
- FunctionalPrompts/Advanced_Analytics/td_polynomialfeaturesfit.md
- FunctionalPrompts/Advanced_Analytics/td_polynomialfeaturestransform.md

### Stage 5: Categorical Encoding

**Objective**: Convert categorical variables into numeric representations for ML algorithms.

#### Step 5.1: One-Hot Encoding
Use **TD_OneHotEncodingFit** and **TD_OneHotEncodingTransform** for nominal categories:
```sql
-- Fit one-hot encoding model
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_onehot_model AS
SELECT TD_OneHotEncodingFit(...)
FROM ${DATABASE_NAME}.${TABLE_NAME}_scaled
WITH DATA;

-- Apply one-hot encoding
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_onehot AS
SELECT TD_OneHotEncodingTransform(...)
FROM ${DATABASE_NAME}.${TABLE_NAME}_scaled, ${DATABASE_NAME}.${TABLE_NAME}_onehot_model
WITH DATA;
```

**Reference Functions**:
- FunctionalPrompts/Advanced_Analytics/td_onehotencodingfit.md
- FunctionalPrompts/Advanced_Analytics/td_onehotencodingtransform.md

#### Step 5.2: Ordinal Encoding
Use **TD_OrdinalEncodingFit** for ordinal categories:
```sql
-- Fit ordinal encoding model
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_ordinal_model AS
SELECT TD_OrdinalEncodingFit(...)
FROM ${DATABASE_NAME}.${TABLE_NAME}_scaled
WITH DATA;

-- Apply ordinal encoding
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_ordinal AS
SELECT TD_OrdinalEncodingTransform(...)
FROM ${DATABASE_NAME}.${TABLE_NAME}_scaled, ${DATABASE_NAME}.${TABLE_NAME}_ordinal_model
WITH DATA;
```

**Reference Functions**:
- FunctionalPrompts/Advanced_Analytics/td_ordinalencodingfit.md
- FunctionalPrompts/Advanced_Analytics/td_ordinalencodingtransform.md

#### Step 5.3: Target Encoding
Use **TD_TargetEncodingFit** for high-cardinality categorical features:
```sql
-- Fit target encoding model
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_target_model AS
SELECT TD_TargetEncodingFit(...)
FROM ${DATABASE_NAME}.${TABLE_NAME}_scaled
WITH DATA;

-- Apply target encoding
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_target_encoded AS
SELECT TD_TargetEncodingTransform(...)
FROM ${DATABASE_NAME}.${TABLE_NAME}_scaled, ${DATABASE_NAME}.${TABLE_NAME}_target_model
WITH DATA;
```

**Reference Functions**:
- FunctionalPrompts/Advanced_Analytics/td_targetencodingfit.md
- FunctionalPrompts/Advanced_Analytics/td_targetencodingtransform.md

#### Step 5.4: Alternative - DECODE for Simple Mappings
For simple categorical mappings:
```sql
-- Manual encoding using DECODE
SELECT
    id,
    DECODE(status,
        'Active', 1,
        'Inactive', 0,
        'Pending', 2,
        -1) as status_encoded,
    DECODE(priority,
        'Low', 1,
        'Medium', 2,
        'High', 3,
        'Critical', 4,
        0) as priority_encoded
FROM ${DATABASE_NAME}.${TABLE_NAME};
```

**Reference Functions**:
- FunctionalPrompts/Core_SQL_Functions/decode.md

### Stage 6: Train-Test Split

**Objective**: Divide data into training and testing sets for model validation.

#### Step 6.1: Create Train-Test Split
Use **TD_TrainTestSplit**:
```sql
-- Split data into train and test sets
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_train AS
SELECT TD_TrainTestSplit(...)
FROM ${DATABASE_NAME}.${TABLE_NAME}_final
WITH DATA;
```

**Reference Functions**:
- FunctionalPrompts/Advanced_Analytics/td_traintestsplit.md

#### Step 6.2: Alternative - Manual Split Using ROW_NUMBER
```sql
-- Manual train-test split (80-20)
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_with_split AS
SELECT
    *,
    CASE
        WHEN MOD(ROW_NUMBER() OVER (ORDER BY RANDOM()), 10) < 8 THEN 'TRAIN'
        ELSE 'TEST'
    END as dataset_split
FROM ${DATABASE_NAME}.${TABLE_NAME}_final;
```

**Reference Functions**:
- FunctionalPrompts/Core_SQL_Functions/row_number.md
- FunctionalPrompts/Core_SQL_Functions/mod.md

### Stage 7: Final Validation

**Objective**: Verify the prepared dataset meets ML requirements.

#### Step 7.1: Verify No Missing Values
```sql
-- Check for remaining NULL values
SELECT
    COUNT(*) as total_rows,
    SUM(CASE WHEN col1 IS NULL THEN 1 ELSE 0 END) as col1_nulls,
    SUM(CASE WHEN col2 IS NULL THEN 1 ELSE 0 END) as col2_nulls
FROM ${DATABASE_NAME}.${TABLE_NAME}_final;
```

#### Step 7.2: Verify Data Types
```sql
-- Ensure all features are numeric for ML
SELECT ColumnName, ColumnType
FROM DBC.ColumnsV
WHERE DatabaseName = '${DATABASE_NAME}'
  AND TableName = '${TABLE_NAME}_FINAL'
  AND ColumnType NOT IN ('I', 'I1', 'I2', 'I8', 'F', 'D', 'N')
ORDER BY ColumnId;
```

#### Step 7.3: Review Distribution Statistics
```sql
-- Final statistical check
SELECT
    COUNT(*) as row_count,
    AVG(feature1) as feature1_mean,
    STDDEV_SAMP(feature1) as feature1_std,
    MIN(feature1) as feature1_min,
    MAX(feature1) as feature1_max
FROM ${DATABASE_NAME}.${TABLE_NAME}_final;
```

**Reference Functions**:
- FunctionalPrompts/Core_SQL_Functions/count.md
- FunctionalPrompts/Core_SQL_Functions/avg_average_ave.md
- FunctionalPrompts/Core_SQL_Functions/stddev_samp.md
- FunctionalPrompts/Core_SQL_Functions/minimum.md
- FunctionalPrompts/Core_SQL_Functions/maximum.md

## Complete Example Workflow

```sql
-- Example: Complete data preparation for customer churn prediction

-- 1. Profile the data
SELECT TD_UnivariateStatistics(*)
FROM customer_data;

-- 2. Handle missing values
CREATE TABLE customer_impute_model AS
SELECT TD_SimpleImputeFit(
    InputColumns('age', 'tenure', 'monthly_charges'),
    Strategy('mean')
)
FROM customer_data
WITH DATA;

CREATE TABLE customer_imputed AS
SELECT TD_SimpleImputeTransform(
    InputTable(customer_data),
    InputColumns('age', 'tenure', 'monthly_charges'),
    ModelTable(customer_impute_model)
)
FROM customer_data
WITH DATA;

-- 3. Detect and remove outliers
CREATE TABLE customer_outlier_model AS
SELECT TD_OutlierFilterFit(
    TargetColumns('monthly_charges', 'total_charges'),
    LowerPercentile(0.01),
    UpperPercentile(0.99)
)
FROM customer_imputed
WITH DATA;

CREATE TABLE customer_clean AS
SELECT TD_OutlierFilterTransform(
    InputTable(customer_imputed),
    ModelTable(customer_outlier_model)
)
FROM customer_imputed
WITH DATA;

-- 4. Scale numeric features
CREATE TABLE customer_scale_model AS
SELECT TD_ScaleFit(
    TargetColumns('age', 'tenure', 'monthly_charges', 'total_charges'),
    ScaleMethod('standardization')
)
FROM customer_clean
WITH DATA;

CREATE TABLE customer_scaled AS
SELECT TD_ScaleTransform(
    InputTable(customer_clean),
    ModelTable(customer_scale_model)
)
FROM customer_clean
WITH DATA;

-- 5. Encode categorical features
CREATE TABLE customer_encode_model AS
SELECT TD_OneHotEncodingFit(
    TargetColumns('contract_type', 'payment_method', 'internet_service')
)
FROM customer_scaled
WITH DATA;

CREATE TABLE customer_encoded AS
SELECT TD_OneHotEncodingTransform(
    InputTable(customer_scaled),
    ModelTable(customer_encode_model)
)
FROM customer_scaled
WITH DATA;

-- 6. Train-test split
CREATE TABLE customer_ml_ready AS
SELECT TD_TrainTestSplit(
    TestSize(0.2),
    Seed(42),
    IdColumn('customer_id')
)
FROM customer_encoded
WITH DATA;

-- 7. Ready for ML model training!
```

## Decision Guide: Which Techniques to Use

### Missing Data Strategy
- **Few missing values (<5%)**: Use TD_GetRowsWithoutMissingValues to remove rows
- **Numeric columns**: Use TD_SimpleImputeFit with mean/median strategy
- **Categorical columns**: Use TD_SimpleImputeFit with mode or create 'UNKNOWN' category
- **Simple cases**: Use NVL or COALESCE for direct replacement

### Encoding Strategy
- **Nominal categories (no order)**: Use TD_OneHotEncodingFit
- **Ordinal categories (ordered)**: Use TD_OrdinalEncodingFit
- **High cardinality (>50 categories)**: Use TD_TargetEncodingFit
- **Binary categories**: Use DECODE to map to 0/1
- **Low cardinality (<5 categories)**: Use DECODE for manual mapping

### Scaling Strategy
- **Tree-based models (DecisionForest, XGBoost)**: Scaling optional
- **Distance-based models (KNN, SVM, K-Means)**: Use TD_ScaleFit with standardization
- **Neural networks**: Use TD_ScaleFit with min-max normalization
- **Linear models (GLM)**: Use TD_ScaleFit with standardization

### Feature Engineering
- **Non-linear relationships expected**: Use TD_PolynomialFeaturesFit
- **Age/time-based bucketing**: Use TD_BinCodeFit
- **High-dimensional data**: Consider TD_RandomProjectionFit

## Output Artifacts

This workflow produces:
1. `${TABLE_NAME}_missing_rows` - Rows with missing values (VIEW)
2. `${TABLE_NAME}_impute_model` - Imputation model table
3. `${TABLE_NAME}_imputed` - Data with missing values imputed
4. `${TABLE_NAME}_outlier_model` - Outlier detection model
5. `${TABLE_NAME}_no_outliers` - Data with outliers removed
6. `${TABLE_NAME}_scale_model` - Scaling transformation model
7. `${TABLE_NAME}_scaled` - Scaled numeric features
8. `${TABLE_NAME}_onehot_model` - One-hot encoding model
9. `${TABLE_NAME}_encoded` - Final encoded features
10. `${TABLE_NAME}_ml_ready` - Train/test split dataset ready for ML

## Best Practices

1. **Always profile first**: Understand your data before applying transformations
2. **Document decisions**: Keep track of why specific techniques were chosen
3. **Preserve original data**: Never overwrite source tables
4. **Validate each stage**: Check data quality after each transformation
5. **Version models**: Keep transformation models for applying to new data
6. **Test reproducibility**: Use same models on test data as used on training data
7. **Monitor data drift**: Compare new data distributions to training data

## Common Pitfalls to Avoid

1. **Data leakage**: Don't fit transformations on entire dataset before train-test split
2. **Scaling before imputation**: Impute first, then scale
3. **Dropping too many rows**: Prefer imputation over deletion when possible
4. **One-hot encoding high cardinality**: Creates too many features, use target encoding
5. **Ignoring outliers**: Can significantly impact model performance
6. **Forgetting to save models**: Needed to transform production data consistently

## Next Steps

After data preparation is complete:
1. Select appropriate ML algorithm (TD_DecisionForest, TD_XGBoost, TD_GLM, etc.)
2. Train model using prepared training dataset
3. Evaluate model using test dataset
4. Apply same transformation pipeline to production data

## Function Reference Summary

### Core SQL Functions Used
- COUNT, AVG, SUM, MIN, MAX - Statistical aggregations
- NVL, COALESCE - NULL handling
- DECODE - Simple categorical mapping
- ROW_NUMBER, RANK - Row identification and ranking
- STDDEV_SAMP, VAR_SAMP - Statistical measures
- MOD - Modulo for train-test splitting

### Advanced Analytics Functions Used
- TD_UnivariateStatistics - Numeric profiling
- TD_CategoricalSummary - Categorical profiling
- TD_ColumnSummary - General column analysis
- TD_GetRowsWithMissingValues - Missing value identification
- TD_GetRowsWithoutMissingValues - Complete rows filtering
- TD_SimpleImputeFit / TD_SimpleImputeTransform - Missing value imputation
- TD_OutlierFilterFit / TD_OutlierFilterTransform - Outlier detection
- TD_GetFutileColumns - Feature selection
- TD_ScaleFit / TD_ScaleTransform - Feature scaling
- TD_BinCodeFit / TD_BinCodeTransform - Discretization
- TD_OneHotEncodingFit / TD_OneHotEncodingTransform - Nominal encoding
- TD_OrdinalEncodingFit / TD_OrdinalEncodingTransform - Ordinal encoding
- TD_TargetEncodingFit / TD_TargetEncodingTransform - High-cardinality encoding
- TD_PolynomialFeaturesFit / TD_PolynomialFeaturesTransform - Non-linear features
- TD_TrainTestSplit - Dataset splitting

---

**File Created**: 2025-11-28
**Version**: 1.0
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Author**: Teradata ML Workflow Template
