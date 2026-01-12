# TD_GetFutileColumns

## Function Name
- **TD_GetFutileColumns**: Futile Column Detection Function - Identifies columns that provide no analytical value

## Description
TD_GetFutileColumns identifies and returns column names that are considered "futile" for analysis or modeling. Futile columns are those that contain data not useful for the analysis or modeling process, such as constant columns (same value in all rows), unique identifier columns (all different values), or high-cardinality columns where nearly every value is unique.

The function analyzes columns from a categorical summary table and returns names of columns meeting any of these futility criteria:
- **All values are unique** (e.g., transaction IDs, UUIDs)
- **All values are the same** (e.g., constant columns)
- **Distinct value ratio exceeds threshold** (distinct count / total rows ≥ threshold)

Removing futile columns simplifies analysis, reduces computational cost, and improves model accuracy by focusing on columns with meaningful patterns.

### Characteristics
- Identifies three types of futile columns (unique, constant, high-cardinality)
- Uses categorical summary statistics as input
- Configurable threshold for high-cardinality detection
- Helps streamline feature selection
- Reduces dimensionality before modeling
- Improves computational efficiency

### Benefits of Removing Futile Columns
1. **Focus on meaningful features**: Concentrate analysis on columns with useful patterns
2. **Reduce computational cost**: Fewer columns mean faster processing and training
3. **Improve model accuracy**: Remove noise from irrelevant features
4. **Simplify interpretation**: Smaller feature sets are easier to understand
5. **Prevent overfitting**: Unique identifiers can cause models to memorize training data

## When to Use TD_GetFutileColumns

TD_GetFutileColumns is essential for feature selection and data preparation:

### Feature Engineering and Selection
- **Dimensionality reduction**: Remove columns before machine learning
- **Feature set refinement**: Identify columns to exclude from analysis
- **Model preparation**: Clean feature space before training
- **Noise reduction**: Remove columns that don't provide signal
- **Prevent overfitting**: Exclude unique identifiers that memorize data

### Data Quality Analysis
- **Schema review**: Identify columns that should be excluded from analytics
- **Data profiling**: Understand which columns have useful variation
- **ETL optimization**: Remove unnecessary columns early in pipeline
- **Storage optimization**: Drop columns that consume space without value
- **Documentation**: Identify which columns are metadata vs features

### Machine Learning Pipelines
- **Pre-processing**: Remove futile columns before feature engineering
- **Model training**: Ensure feature set contains only useful variables
- **Cross-validation**: Prevent information leakage from unique IDs
- **Feature importance**: Focus on features that can have importance
- **Model explanation**: Simpler models with fewer futile columns

### Business Applications
- **Customer analytics**: Remove customer IDs, keep behavioral features
- **Fraud detection**: Exclude transaction IDs, use transaction patterns
- **Churn prediction**: Remove account numbers, use account characteristics
- **Marketing response**: Exclude campaign IDs, use campaign attributes
- **Sales forecasting**: Remove invoice numbers, use invoice characteristics
- **Product recommendations**: Exclude product SKUs, use product features

### Data Exploration
- **Initial assessment**: Quickly identify which columns are worth exploring
- **Column triage**: Prioritize columns with meaningful variation
- **Segmentation analysis**: Focus on columns that differentiate segments
- **Pattern detection**: Exclude columns that obscure patterns
- **Correlation analysis**: Remove constant columns (undefined correlation)

## Syntax

```sql
TD_GetFutileColumns(
    ON { table | view | (query) } AS InputTable PARTITION BY ANY
    ON { table | view | (query) } AS CategoryTable DIMENSION
    USING
    [ CategoricalSummaryColumn('target_column') ]
    [ ThresholdValue('threshold_value') ]
)
```

**Note:** You can call this function from:
- The FROM clause of a SELECT statement
- As part of a CREATE TABLE statement
- As part of a CREATE VIEW statement

## Required Syntax Elements

### ON Clause
Accepts the InputTable and CategoryTable clauses.

#### InputTable
- **Purpose**: Original data table to analyze
- **PARTITION BY ANY**: Required partitioning clause
- **Content**: The table containing raw data

#### CategoryTable (DIMENSION)
- **Purpose**: Categorical summary statistics table
- **Created by**: TD_CategoricalSummary function
- **DIMENSION keyword**: Required
- **Content**: Summary statistics (column name, distinct values, counts)

## Optional Syntax Elements

### CategoricalSummaryColumn
Specifies the column name from the CategoricalSummaryTable containing column names.
- **Data Type**: VARCHAR
- **Default**: 'ColumnName'
- **Purpose**: Identifies which column in summary table contains the column names
- **Example**: `CategoricalSummaryColumn('ColumnName')`

### ThresholdValue
Specifies the threshold ratio for determining column futility based on cardinality.
- **Data Type**: DECIMAL
- **Range**: 0 to 1
- **Default**: 0.95
- **Formula**: If (distinct_count / total_rows) ≥ threshold, column is futile
- **Example**: `ThresholdValue('0.7')` considers columns futile if 70%+ values are unique

**Threshold Interpretation**:
- **0.95** (default): Column futile if 95%+ of values are unique (very permissive)
- **0.8**: Column futile if 80%+ of values are unique (common choice)
- **0.5**: Column futile if 50%+ of values are unique (aggressive filtering)
- **0.3**: Column futile if 30%+ of values are unique (very aggressive)

## Input

### InputTable Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| Target_Column | VARCHAR | Input table columns from the Category Summary table |
| (any columns) | Any | Original data columns being analyzed |

### CategoryTable (Categorical Summary Table) Schema

Created by TD_CategoricalSummary function:

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| ColumnName | VARCHAR, CHARACTER SET UNICODE | The column name of the target column |
| DistinctValue | VARCHAR, CHARACTER SET UNICODE | The distinct value in the target column |
| DistinctValueCount | BIGINT | The count of distinct values in the target column |

## Output

### Output Table Schema

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| FutileColumns | VARCHAR, CHARACTER SET UNICODE | The column names that are futile |

**Output contains one row per futile column identified.**

## Futility Detection Logic

TD_GetFutileColumns identifies a column as futile if ANY of these conditions are met:

1. **All values are unique**: distinct_count = total_rows
   - Example: transaction_id, UUID, auto-increment IDs
   - Reason: Provides no generalizable pattern

2. **All values are the same**: distinct_count = 1
   - Example: country = 'USA' for all rows, constant flags
   - Reason: Provides no discrimination power

3. **High cardinality**: (distinct_count / total_rows) ≥ threshold
   - Example: email addresses, phone numbers (at high threshold)
   - Reason: Too sparse to provide useful patterns

## Code Examples

### Example 1: Basic Futile Column Detection (Titanic Dataset)

Identify futile columns in Titanic passenger data:

```sql
-- Create sample Titanic data
CREATE TABLE titanic_passengers (
    passenger INTEGER,
    gender VARCHAR(10),
    ticket VARCHAR(50),
    cabin VARCHAR(20),
    survived BYTEINT
);

INSERT INTO titanic_passengers VALUES
(1, 'male', 'A/5 21171', 'C', 0),
(2, 'female', 'PC 17599', 'C', 1),
(3, 'female', 'STON/O2. 3101282', 'C', 1),
(4, 'male', '113803', 'C', 1),
(5, 'female', '373450', 'C', 0);

-- Step 1: Create categorical summary
CREATE TABLE category_summary_table AS (
    SELECT * FROM TD_CategoricalSummary (
        ON titanic_passengers AS InputTable
        USING
        TargetColumns('cabin', 'gender', 'ticket')
    ) AS dt
) WITH DATA;

-- View summary
SELECT * FROM category_summary_table ORDER BY ColumnName, DistinctValue;

/*
Output:
ColumnName | DistinctValue      | DistinctValueCount
-----------|--------------------|-----------------
cabin      | C                  | 5
gender     | female             | 3
gender     | male               | 2
ticket     | 373450             | 1
ticket     | A/5 21171          | 1
ticket     | PC 17599           | 1
ticket     | STON/O2. 3101282   | 1
ticket     | 113803             | 1

Analysis:
- cabin: 1 distinct value out of 5 rows → constant column (futile)
- gender: 2 distinct values out of 5 rows → useful (not futile)
- ticket: 5 distinct values out of 5 rows → all unique (futile)
*/

-- Step 2: Identify futile columns
SELECT * FROM TD_GetFutileColumns(
    ON titanic_passengers AS InputTable PARTITION BY ANY
    ON category_summary_table AS CategoryTable DIMENSION
    USING
    CategoricalSummaryColumn('ColumnName')
    ThresholdValue('0.7')  -- 70% threshold
) AS dt;

/*
Output:
FutileColumns
--------------
ticket
cabin

Explanation:
- ticket: All 5 values are unique (5/5 = 100% ≥ 70%) → FUTILE
- cabin: All values are 'C' (constant) → FUTILE
- gender: 2 distinct values, useful variation → NOT FUTILE
*/
```

**Use Case**: Identify which passenger attributes are worth analyzing.

### Example 2: Customer Data Feature Selection

Remove futile columns before building churn model:

```sql
-- Customer dataset with mix of useful and futile columns
CREATE TABLE customer_data (
    customer_id INTEGER,
    account_number VARCHAR(50),
    customer_name VARCHAR(100),
    email VARCHAR(100),
    country VARCHAR(50),
    age_group VARCHAR(20),
    plan_type VARCHAR(20),
    tenure_months INTEGER,
    monthly_charges DECIMAL(10,2),
    churned BYTEINT
);

-- Insert sample data (10,000 customers)
-- ... data insertion ...

-- Step 1: Create categorical summary for all potential feature columns
CREATE TABLE customer_category_summary AS (
    SELECT * FROM TD_CategoricalSummary (
        ON customer_data AS InputTable
        USING
        TargetColumns('customer_id', 'account_number', 'customer_name', 'email',
                      'country', 'age_group', 'plan_type')
    ) AS dt
) WITH DATA;

-- Step 2: Identify futile columns with 95% threshold (default)
CREATE TABLE customer_futile_cols AS (
    SELECT * FROM TD_GetFutileColumns(
        ON customer_data AS InputTable PARTITION BY ANY
        ON customer_category_summary AS CategoryTable DIMENSION
        USING
        CategoricalSummaryColumn('ColumnName')
        ThresholdValue('0.95')
    ) AS dt
) WITH DATA;

-- View futile columns
SELECT FutileColumns FROM customer_futile_cols;

/*
Expected Output:
FutileColumns
-----------------
customer_id       -- All unique (10000/10000 = 100%)
account_number    -- All unique (10000/10000 = 100%)
customer_name     -- All unique (10000/10000 = 100%)
email             -- All unique (10000/10000 = 100%)
country           -- Constant 'USA' for all rows

NOT futile:
- age_group: 5 distinct values (Under 25, 25-34, 35-44, 45-54, 55+)
- plan_type: 4 distinct values (Basic, Standard, Premium, Enterprise)
*/

-- Step 3: Create feature set excluding futile columns
CREATE TABLE customer_features AS (
    SELECT
        -- Keep only useful columns
        age_group,
        plan_type,
        tenure_months,
        monthly_charges,
        churned
    FROM customer_data
) WITH DATA;

-- Step 4: Build churn model on clean feature set
CREATE TABLE churn_model AS (
    SELECT * FROM TD_GLM (
        ON customer_features AS InputTable
        USING
        TargetColumn('churned')
        InputColumns('age_group', 'plan_type', 'tenure_months', 'monthly_charges')
        Family('BINOMIAL')
        MaxIterNum(100)
    ) AS dt
) WITH DATA;
```

**Business Impact**: Focus model on actionable features, exclude irrelevant identifiers.

### Example 3: High-Cardinality Detection with Different Thresholds

Compare results at different threshold values:

```sql
-- E-commerce transaction data
CREATE TABLE transactions (
    transaction_id VARCHAR(50),
    customer_id INTEGER,
    product_category VARCHAR(50),
    product_sku VARCHAR(100),
    payment_method VARCHAR(20),
    shipping_country VARCHAR(50)
);

-- Assume 10,000 transactions with:
-- - 10,000 unique transaction_ids (100% unique)
-- - 2,500 unique customer_ids (25% unique)
-- - 15 product categories (0.15% unique)
-- - 500 product SKUs (5% unique)
-- - 5 payment methods (0.05% unique)
-- - 1 shipping country (constant)

-- Create categorical summary
CREATE TABLE trans_category_summary AS (
    SELECT * FROM TD_CategoricalSummary (
        ON transactions AS InputTable
        USING
        TargetColumns('[:]')  -- All columns
    ) AS dt
) WITH DATA;

-- Test with different thresholds

-- Threshold 0.95 (very permissive - only catches near-unique columns)
SELECT 'Threshold 0.95' as threshold_level, FutileColumns
FROM TD_GetFutileColumns(
    ON transactions AS InputTable PARTITION BY ANY
    ON trans_category_summary AS CategoryTable DIMENSION
    USING ThresholdValue('0.95')
) AS dt

UNION ALL

-- Threshold 0.7 (moderate - catches high-cardinality)
SELECT 'Threshold 0.70' as threshold_level, FutileColumns
FROM TD_GetFutileColumns(
    ON transactions AS InputTable PARTITION BY ANY
    ON trans_category_summary AS CategoryTable DIMENSION
    USING ThresholdValue('0.7')
) AS dt

UNION ALL

-- Threshold 0.3 (aggressive - catches medium-cardinality)
SELECT 'Threshold 0.30' as threshold_level, FutileColumns
FROM TD_GetFutileColumns(
    ON transactions AS InputTable PARTITION BY ANY
    ON trans_category_summary AS CategoryTable DIMENSION
    USING ThresholdValue('0.3')
) AS dt

UNION ALL

-- Threshold 0.05 (very aggressive)
SELECT 'Threshold 0.05' as threshold_level, FutileColumns
FROM TD_GetFutileColumns(
    ON transactions AS InputTable PARTITION BY ANY
    ON trans_category_summary AS CategoryTable DIMENSION
    USING ThresholdValue('0.05')
) AS dt

ORDER BY threshold_level, FutileColumns;

/*
Expected Output:
threshold_level  | FutileColumns
-----------------|------------------
Threshold 0.05   | transaction_id
Threshold 0.05   | shipping_country
Threshold 0.05   | product_sku
Threshold 0.30   | transaction_id
Threshold 0.30   | shipping_country
Threshold 0.30   | customer_id       -- NEW: 25% unique ≥ 30%? No, but close
Threshold 0.70   | transaction_id
Threshold 0.70   | shipping_country
Threshold 0.95   | transaction_id
Threshold 0.95   | shipping_country

Analysis by column:
- transaction_id: 100% unique → ALWAYS futile
- shipping_country: Constant → ALWAYS futile
- customer_id: 25% unique → Futile only if threshold ≤ 0.25
- product_sku: 5% unique → Futile only if threshold ≤ 0.05
- product_category: 0.15% unique → Useful at all reasonable thresholds
- payment_method: 0.05% unique → Useful at all reasonable thresholds

Recommendation: Use threshold 0.7-0.95 for most use cases
*/
```

**Insight**: Choose threshold based on desired balance between completeness and sparsity.

### Example 4: Using Column Indexes for Summary

Use column index ranges instead of column names:

```sql
-- Sample dataset
CREATE TABLE customer_survey (
    survey_id INTEGER,           -- Column 0
    respondent_name VARCHAR(100),-- Column 1
    age_bracket VARCHAR(20),     -- Column 2
    satisfaction VARCHAR(20),    -- Column 3
    region VARCHAR(50),          -- Column 4
    purchase_frequency VARCHAR(20) -- Column 5
);

-- Method 1: Using column names
CREATE TABLE survey_summary_by_name AS (
    SELECT * FROM TD_CategoricalSummary (
        ON customer_survey AS InputTable
        USING
        TargetColumns('survey_id', 'respondent_name', 'age_bracket', 'satisfaction', 'region')
    ) AS dt
) WITH DATA;

-- Method 2: Using column indexes (0-indexed)
-- Columns 0-4 = survey_id through region
CREATE TABLE survey_summary_by_index AS (
    SELECT * FROM TD_CategoricalSummary (
        ON customer_survey AS InputTable
        USING
        TargetColumns('[0:4]')  -- Include columns 0, 1, 2, 3, 4
    ) AS dt
) WITH DATA;

-- Method 3: All categorical columns
CREATE TABLE survey_summary_all AS (
    SELECT * FROM TD_CategoricalSummary (
        ON customer_survey AS InputTable
        USING
        TargetColumns('[:]')  -- All columns
    ) AS dt
) WITH DATA;

-- Identify futile columns
SELECT FutileColumns
FROM TD_GetFutileColumns(
    ON customer_survey AS InputTable PARTITION BY ANY
    ON survey_summary_by_index AS CategoryTable DIMENSION
    USING
    CategoricalSummaryColumn('ColumnName')
    ThresholdValue('0.8')
) AS dt;

/*
Output:
FutileColumns
-----------------
survey_id          -- All unique
respondent_name    -- All unique

NOT futile:
- age_bracket: 5-6 distinct values
- satisfaction: 5 distinct values (Very Dissatisfied to Very Satisfied)
- region: 10 distinct values (geographic regions)
- purchase_frequency: 4 distinct values (Never, Rarely, Sometimes, Often)
*/
```

**Note**: Index-based selection only works on categorical columns.

### Example 5: Automated Feature Cleaning Pipeline

Integrate futile column detection into automated ML pipeline:

```sql
-- Full pipeline: detect and remove futile columns, then train model

-- Step 1: Create categorical summary for all columns
CREATE TABLE raw_data_summary AS (
    SELECT * FROM TD_CategoricalSummary (
        ON customer_raw_data AS InputTable
        USING
        TargetColumns('[:]')  -- All categorical columns
    ) AS dt
) WITH DATA;

-- Step 2: Identify futile columns
CREATE TABLE futile_cols_list AS (
    SELECT * FROM TD_GetFutileColumns(
        ON customer_raw_data AS InputTable PARTITION BY ANY
        ON raw_data_summary AS CategoryTable DIMENSION
        USING
        CategoricalSummaryColumn('ColumnName')
        ThresholdValue('0.9')
    ) AS dt
) WITH DATA;

-- Step 3: Get list of useful columns (non-futile)
CREATE TABLE useful_cols AS (
    SELECT column_name
    FROM dbc.columns
    WHERE tablename = 'customer_raw_data'
    AND column_name NOT IN (SELECT FutileColumns FROM futile_cols_list)
) WITH DATA;

-- Step 4: Build dynamic SQL to create clean dataset
-- (In practice, use stored procedure or script to generate column list)
CREATE TABLE customer_clean_data AS (
    SELECT
        age_group,
        plan_type,
        region,
        payment_method,
        tenure_months,
        monthly_charges,
        total_charges,
        num_services,
        churned
    FROM customer_raw_data
    -- Excluded: customer_id, account_number, customer_name, email, etc.
) WITH DATA;

-- Step 5: Feature engineering on clean data
CREATE TABLE customer_features AS (
    SELECT * FROM TD_ColumnTransformer(
        ON customer_clean_data AS InputTable
        ON impute_fit AS SimpleImputeFitTable DIMENSION
        ON scale_fit AS ScaleFitTable DIMENSION
        ON onehot_fit AS OneHotEncodingFitTable DIMENSION
    ) AS dt
) WITH DATA;

-- Step 6: Train model on clean features
CREATE TABLE churn_model AS (
    SELECT * FROM TD_XGBoost (
        ON customer_features AS InputTable
        USING
        TargetColumn('churned')
        NumTrees(100)
        MaxDepth(6)
    ) AS dt
) WITH DATA;

-- Log which columns were removed
INSERT INTO feature_audit_log
SELECT
    'churn_model_v2' as model_version,
    CURRENT_DATE as audit_date,
    FutileColumns as removed_column,
    'Futile - automated detection' as removal_reason
FROM futile_cols_list;
```

**Production Best Practice**: Automate futile column detection in ML pipelines.

### Example 6: Regional Analysis - Different Futility by Segment

Futility can vary by data subset:

```sql
-- Some columns may be futile in subsets but not overall

-- Overall analysis
CREATE TABLE overall_summary AS (
    SELECT * FROM TD_CategoricalSummary (
        ON global_sales_data AS InputTable
        USING
        TargetColumns('country', 'region', 'city', 'product_line', 'sales_channel')
    ) AS dt
) WITH DATA;

SELECT 'Overall' as segment, FutileColumns
FROM TD_GetFutileColumns(
    ON global_sales_data AS InputTable PARTITION BY ANY
    ON overall_summary AS CategoryTable DIMENSION
    USING ThresholdValue('0.95')
) AS dt

UNION ALL

-- US-only analysis
SELECT 'US Only' as segment, FutileColumns
FROM TD_GetFutileColumns(
    ON (SELECT * FROM global_sales_data WHERE country = 'USA') AS InputTable PARTITION BY ANY
    ON (SELECT * FROM TD_CategoricalSummary (
            ON (SELECT * FROM global_sales_data WHERE country = 'USA') AS InputTable
            USING TargetColumns('country', 'region', 'city', 'product_line', 'sales_channel')
        ) AS dt
    ) AS CategoryTable DIMENSION
    USING ThresholdValue('0.95')
) AS dt;

/*
Expected Results:
segment  | FutileColumns
---------|---------------
Overall  | (none)         -- All columns useful globally
US Only  | country        -- Constant 'USA' in US-only subset

Insight: Futility depends on data context
- 'country' is useful globally (many countries)
- 'country' is futile for US-only analysis (constant)
- Filter data before futility detection for segment-specific models
*/
```

**Strategic Insight**: Futility is context-dependent; analyze subsets separately.

## Common Use Cases

### 1. Pre-Model Feature Selection

```sql
-- Quick filter before training
CREATE TABLE model_features AS (
    SELECT * EXCEPT futile_cols.*
    FROM training_data
    WHERE column_name NOT IN (
        SELECT FutileColumns FROM futile_column_detection
    )
);
```

### 2. Schema Optimization

```sql
-- Identify columns to drop from large tables
SELECT
    FutileColumns as column_to_drop,
    'Futile - no analytical value' as reason,
    'ALTER TABLE large_table DROP COLUMN ' || FutileColumns || ';' as drop_sql
FROM futile_detection_results;
```

### 3. Data Quality Reporting

```sql
-- Report on column usefulness
SELECT
    CASE
        WHEN c.column_name IN (SELECT FutileColumns FROM futile_cols) THEN 'Futile'
        ELSE 'Useful'
    END as column_status,
    COUNT(*) as column_count
FROM dbc.columns c
WHERE c.tablename = 'fact_sales'
GROUP BY column_status;
```

## Best Practices

1. **Choose Appropriate Threshold**:
   - **0.95-0.99**: Very permissive, catch only near-unique columns
   - **0.8-0.9**: Balanced, recommended for most use cases
   - **0.5-0.7**: Moderate, removes moderately sparse columns
   - **0.2-0.4**: Aggressive, only keeps low-cardinality columns
   - Consider domain: customer IDs always futile, product SKUs may be useful

2. **Run Before Feature Engineering**:
   - Detect futile columns early in pipeline
   - Remove before expensive transformations
   - Reduces processing time and memory

3. **Manual Review Recommended**:
   - Don't blindly remove all flagged columns
   - Some "futile" columns may have business value
   - Product SKUs futile for modeling but needed for predictions
   - Keep identifiers for joining results back

4. **Segment-Specific Analysis**:
   - Run futility detection per segment for targeted models
   - Columns useful overall may be futile in subsets
   - Example: 'country' futile in country-specific model

5. **Document Removed Columns**:
   - Log which columns were removed and why
   - Track futility threshold used
   - Enable reproducibility and auditing

6. **Combine with Other Selection Methods**:
   - Futility detection is first pass
   - Follow with correlation analysis
   - Use feature importance from models
   - Consider business requirements

7. **Handle False Positives**:
   - High-cardinality columns may still be useful
   - Zip codes: High cardinality but geographically meaningful
   - Consider grouping/binning instead of removing

8. **Update Periodically**:
   - Rerun as data distribution changes
   - Columns may become futile over time (data quality degradation)
   - Or become useful (increased variation)

## Related Functions

- **TD_CategoricalSummary**: Creates summary table required as input
- **TD_GetRowsWithMissingValues**: Identifies rows with missing values
- **TD_GetRowsWithoutMissingValues**: Filters to complete rows
- **TD_ConvertTo**: Convert data types after removing futile columns
- **TD_ColumnTransformer**: Feature engineering after futile column removal
- **TD_DecisionForest** (Feature Importance): Alternative feature selection method

## Notes and Limitations

1. **Requires Categorical Summary**:
   - Must run TD_CategoricalSummary first
   - Summary table must have correct schema
   - Only works on categorical/discrete columns

2. **Not for Continuous Numeric Columns**:
   - Function designed for categorical columns
   - Continuous numeric columns need different analysis
   - Use correlation, variance, feature importance for numeric

3. **Context-Dependent Futility**:
   - Columns futile in one context may be useful in another
   - Product SKUs futile for modeling but needed for recommendations
   - Always consider business requirements

4. **Threshold Selection Impact**:
   - Too high: Miss high-cardinality futile columns
   - Too low: Remove potentially useful columns
   - Experiment with different thresholds

5. **Doesn't Consider Relationships**:
   - Evaluates each column independently
   - Doesn't consider combinations (interactions)
   - Two individually futile columns might be useful together

6. **Identifiers Not Always Futile**:
   - Some IDs encode information (store ID, region code)
   - Parse IDs to extract meaningful components
   - Don't blindly remove all high-cardinality columns

7. **Constant Columns May Be Intentional**:
   - Filtered data may have constant columns (e.g., country='USA')
   - Constant in training set but varies in production
   - Verify constants before removing

8. **Performance on Large Datasets**:
   - Categorical summary on large tables can be expensive
   - Consider sampling for initial futility detection
   - Profile full dataset after initial filtering

## Usage Notes

Futile columns contain data that is not useful for analysis or modeling. Common types include:

1. **Constant columns**: Same value for all rows (no variation)
2. **Unique identifier columns**: All different values (no pattern)
3. **Redundant columns**: Same information as other columns
4. **High-cardinality columns**: Too sparse to provide useful patterns

**Why Remove Futile Columns**:

- **Improved accuracy**: Focus on columns with meaningful patterns
- **Enhanced efficiency**: Faster processing with fewer columns
- **Increased data quality**: Remove noise from irrelevant features
- **Better insights**: Concentrate on columns that differentiate outcomes
- **Prevent overfitting**: Unique identifiers cause models to memorize

**Common Futile Column Types**:
- Transaction IDs, UUIDs, auto-increment primary keys
- Constant flags or values (all rows same value)
- Email addresses, phone numbers (all unique)
- Free-text fields with high cardinality
- Metadata columns (creation timestamps, user IDs)

## Version Information

- **Function Version**: Based on Teradata Database Analytic Functions Version 17.20
- **Generated**: November 29, 2025
- **Category**: Data Cleaning Functions / Feature Selection / Dimensionality Reduction
