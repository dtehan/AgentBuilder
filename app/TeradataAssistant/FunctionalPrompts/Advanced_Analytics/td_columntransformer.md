# TD_ColumnTransformer

## Function Name
- **TD_ColumnTransformer**: Multi-Transform Pipeline Function - Applies multiple feature transformations in a single operation

## Description
TD_ColumnTransformer transforms input table columns in a single operation by applying multiple pre-fitted transformation models. Instead of chaining individual transform functions sequentially, you provide all the FIT tables to this function, and it executes all required transformations in a single, efficient operation.

This function is the "transform" step in the fit-transform pattern used throughout Teradata's feature engineering functions. After training individual FIT functions on your training data, use TD_ColumnTransformer to apply all those transformations consistently to training, validation, and test datasets.

### Supported Transformations

TD_ColumnTransformer can apply the following transformations:
1. **TD_ScaleTransform**: Standardization, normalization, min-max scaling
2. **TD_BincodeTransform**: Discretization of continuous variables into bins
3. **TD_FunctionTransform**: Mathematical transformations (log, sqrt, exp, etc.)
4. **TD_NonLinearCombineTransform**: Interaction features and non-linear combinations
5. **TD_OutlierFilterTransform**: Remove or cap outlier values
6. **TD_PolynomialFeaturesTransform**: Generate polynomial and interaction features
7. **TD_RowNormalizeTransform**: Row-wise normalization
8. **TD_OrdinalEncodingTransform**: Encode categorical variables as ordered integers
9. **TD_OneHotEncodingTransform**: Create binary indicator variables for categories
10. **TD_SimpleImputeTransform**: Fill missing values with statistics from training

### Characteristics
- **Single-operation pipeline**: Apply multiple transformations in one function call
- **Consistent transformations**: Use same FIT parameters across train/test splits
- **Order preservation**: FIT tables must be provided in training sequence order
- **Multiple instances**: Supports multiple NonLinearCombineFit tables, single instance for others
- **Efficient execution**: Optimized for applying multiple transformations
- **Schema changes**: Some transformations create new columns or modify schemas

### Limitations
- Maximum 128 columns in FIT tables
- TD_BincodeFit limited to 5 columns with variable-width method
- Only one instance allowed for most FIT table types (except NonLinearCombineFit)
- Must create FIT tables before using this function
- FIT tables must be provided in same order as training sequence

## When to Use TD_ColumnTransformer

TD_ColumnTransformer is essential for consistent feature engineering across datasets:

### Machine Learning Pipelines
- **Train-test consistency**: Apply identical transformations to training, validation, and test sets
- **Production scoring**: Transform new data using parameters learned from training data
- **Cross-validation**: Ensure each fold uses consistent transformation parameters
- **Model deployment**: Single function call applies entire transformation pipeline
- **Prevent data leakage**: Transformations based only on training data statistics

### Feature Engineering Workflows
- **Multi-step transformations**: Combine scaling, encoding, imputation, and feature creation
- **Complex pipelines**: Apply 5-10 different transformations in sequence
- **Categorical and numeric**: Handle both variable types in single operation
- **Feature creation**: Generate polynomial features and interactions while transforming
- **Reproducibility**: Ensure exact same transformations across different runs

### Data Preprocessing
- **Missing value handling**: Impute missing values using training statistics
- **Outlier treatment**: Apply consistent outlier filtering rules
- **Scaling**: Standardize features using training mean/std
- **Encoding**: Convert categories to numeric using training category mappings
- **Binning**: Discretize continuous variables using training-derived bins

### Production ML Systems
- **Batch scoring**: Transform large datasets for batch predictions
- **Real-time inference**: Apply transformation pipeline to new observations
- **Model retraining**: Consistently transform new training data
- **A/B testing**: Ensure consistent feature engineering across model versions
- **Model monitoring**: Track feature distributions with consistent transformations

### Business Applications
- **Customer scoring**: Transform customer data for churn, propensity, lifetime value models
- **Credit risk models**: Prepare loan applications with consistent feature engineering
- **Fraud detection**: Transform transaction data using learned patterns
- **Demand forecasting**: Prepare time-series features with consistent scaling
- **Recommendation systems**: Transform user/item features for scoring
- **Marketing campaigns**: Prepare customer data for response prediction

## Syntax

```sql
TD_ColumnTransformer (
    ON { table | view | (query) } AS InputTable
    [ ON { table | view | (query) } AS BincodeFitTable DIMENSION ]
    [ ON { table | view | (query) } AS FunctionFitTable DIMENSION ]
    [ ON { table | view | (query) } AS NonLinearCombineFitTable DIMENSION ]
    [ ON { table | view | (query) } AS OneHotEncodingFitTable DIMENSION ]
    [ ON { table | view | (query) } AS OrdinalEncodingFitTable DIMENSION ]
    [ ON { table | view | (query) } AS OutlierFilterFitTable DIMENSION ]
    [ ON { table | view | (query) } AS PolynomialFeaturesFitTable DIMENSION ]
    [ ON { table | view | (query) } AS RowNormalizeFitTable DIMENSION ]
    [ ON { table | view | (query) } AS ScaleFitTable DIMENSION ]
    [ ON { table | view | (query) } AS SimpleImputeFitTable DIMENSION ]
    USING
    [ FillRowIDColumnName('output_column_name') ]
)
```

**Note:** You can call this function from:
- The FROM clause of a SELECT statement
- As part of a CREATE TABLE statement
- As part of a CREATE VIEW statement

## Required Syntax Elements

### ON InputTable Clause
The function accepts the InputTable clause containing data to be transformed.
- **InputTable**: Table with raw features to be transformed
- **Required**: Must have columns matching those used in FIT tables
- **Note**: Only one InputTable allowed

### At Least One FIT Table
You must provide at least one FIT table (BincodeFitTable, ScaleFitTable, etc.).
- **FIT Tables**: Created by running corresponding Fit functions on training data
- **DIMENSION keyword**: All FIT tables must use DIMENSION keyword
- **Order matters**: Provide FIT tables in same order as training transformation sequence

## Optional Syntax Elements

### FillRowIDColumnName
Specify name for output column containing unique row identifiers.
- **Data Type**: VARCHAR
- **Purpose**: Adds unique identifier column to output
- **Usage**: `FillRowIDColumnName('row_id')`
- **Benefit**: Helps track rows through transformation pipeline

## FIT Table Types

### BincodeFitTable
Created by TD_BincodeFit - discretizes continuous variables into bins.
- **Function**: TD_BincodeFit
- **Purpose**: Bin numerical features into discrete intervals
- **Limitation**: Maximum 5 columns with variable-width method
- **Example**: Age binned into [0-18, 18-35, 35-65, 65+]

### FunctionFitTable
Created by TD_FunctionFit - applies mathematical transformations.
- **Function**: TD_FunctionFit
- **Purpose**: Apply log, sqrt, exp, power transformations
- **Use Case**: Handle skewed distributions, normalize variance

### NonLinearCombineFitTable
Created by TD_NonLinearCombineFit - creates feature interactions.
- **Function**: TD_NonLinearCombineFit
- **Purpose**: Generate interaction terms (e.g., age × income)
- **Special**: Multiple instances allowed (only FIT table type that allows this)
- **Output**: Creates new columns for combined features

### OneHotEncodingFitTable
Created by TD_OneHotEncodingFit - converts categories to binary indicators.
- **Function**: TD_OneHotEncodingFit
- **Purpose**: Create dummy variables for categorical features
- **Output**: Creates new columns (one per category)
- **Example**: Color (Red, Blue, Green) → Color_Red, Color_Blue, Color_Green

### OrdinalEncodingFitTable
Created by TD_OrdinalEncodingFit - encodes categories as integers.
- **Function**: TD_OrdinalEncodingFit
- **Purpose**: Map categories to ordered integers
- **Schema Change**: Modifies target column data type
- **Example**: Size (Small, Medium, Large) → (0, 1, 2)

### OutlierFilterFitTable
Created by TD_OutlierFilterFit - handles outlier values.
- **Function**: TD_OutlierFilterFit
- **Purpose**: Remove or cap extreme values
- **Methods**: IQR, z-score, percentile-based
- **Use Case**: Prevent outliers from affecting model training

### PolynomialFeaturesFitTable
Created by TD_PolynomialFeaturesFit - generates polynomial features.
- **Function**: TD_PolynomialFeaturesFit
- **Purpose**: Create x², x³, and interaction terms
- **Output**: Creates new columns for polynomial features
- **Example**: age → age, age², age³

### RowNormalizeFitTable
Created by TD_RowNormalizeFit - normalizes rows.
- **Function**: TD_RowNormalizeFit
- **Purpose**: Scale each row to unit norm
- **Methods**: L1, L2, max normalization
- **Use Case**: Text feature vectors, recommendation systems

### ScaleFitTable
Created by TD_ScaleFit - scales numerical features.
- **Function**: TD_ScaleFit
- **Purpose**: Standardization (z-score), min-max, robust scaling
- **Use Case**: Ensure features on similar scales
- **Example**: Scale income and age to mean=0, std=1

### SimpleImputeFitTable
Created by TD_SimpleImputeFit - fills missing values.
- **Function**: TD_SimpleImputeFit
- **Purpose**: Replace missing values with mean, median, mode, or constant
- **Use Case**: Handle missing data before modeling
- **Example**: Missing age → median age from training set

## Input

### InputTable Schema

| Column Type | Data Type | Description |
|-------------|-----------|-------------|
| TargetColumn (categorical) | CHAR, VARCHAR | Categorical columns requiring transformation via OrdinalEncoding or OneHotEncoding |
| TargetColumn (numeric) | INTEGER, REAL, DECIMAL, NUMBER | Numeric columns requiring transformation via Scale, Bincode, Function, NonLinearCombine, OutlierFilter, PolynomialFeatures, RowNormalize, or SimpleImpute |
| Other columns | Any | Pass-through columns not involved in transformations |

**Requirements**:
- Input columns must match those used when creating FIT tables
- Column names must match exactly
- Data types must be compatible with transformation types

## Output

### Output Table Schema

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| TargetColumn | CHAR, VARCHAR, INTEGER, REAL, DECIMAL, NUMBER | Columns transformed by ColumnTransformer function |
| otherColumns | CHAR, VARCHAR, INTEGER, REAL, DECIMAL, NUMBER | Default columns from input passed through unchanged |
| NewColumns | CHAR, VARCHAR, INTEGER, REAL, DECIMAL, NUMBER | New columns created by PolynomialFeatures, NonLinearCombine, or OneHotEncoding |

**Schema Changes**:
- **TD_BincodeFit**: Changes target column schema (continuous → discrete)
- **TD_OrdinalEncodingFit**: Changes target column schema (categorical → integer)
- **TD_PolynomialFeaturesFit**: Adds new columns (polynomial terms)
- **TD_NonLinearCombineFit**: Adds new columns (interaction terms)
- **TD_OneHotEncodingFit**: Adds new columns (binary indicators)

## Code Examples

### Example 1: Complete ML Pipeline - Titanic Survival Prediction

End-to-end feature engineering pipeline with multiple transformations:

```sql
-- Step 1: Create training dataset
CREATE TABLE titanic_train AS (
    SELECT * FROM titanic_data WHERE dataset_split = 'train'
) WITH DATA;

-- Step 2: Extract title from Name using Unpack and TD_strApply
DROP TABLE IF EXISTS getSubtitles;
CREATE MULTISET TABLE getSubtitles AS (
    SELECT * FROM Unpack(
        ON titanic_train
        USING
        TargetColumn('Name')
        OutputColumns('NTitle')
        OutputDatatypes('VARCHAR')
        Delimiter(' ')
        Regex('([A-Za-z]+)\.')
    ) AS dt
) WITH DATA;

-- Extract first character of Cabin
DROP TABLE IF EXISTS getCabin;
CREATE MULTISET TABLE getCabin AS (
    SELECT * FROM TD_strApply (
        ON getSubtitles AS InputTable
        USING
        TargetColumns('cabin')
        StringOperation('getNchars')
        StringLength(1)
        Accumulate('[:]', '-cabin')
        InPlace('True')
    ) AS dt
) WITH DATA;

-- Step 3: Create FIT tables on training data
-- 3a. Impute missing values (Age, Fare)
CREATE TABLE imputeFit AS (
    SELECT * FROM TD_SimpleImputeFit(
        ON getCabin AS InputTable
        USING
        TargetColumns('age', 'fare')
        FillMethod('MEAN')
    ) AS dt
) WITH DATA;

-- 3b. Create family size feature (non-linear combination)
CREATE TABLE NonLinearCombineFit AS (
    SELECT * FROM TD_NonLinearCombineFit(
        ON getCabin AS InputTable
        USING
        TargetColumns('sibsp', 'parch')
        Formula('col1 + col2 + 1')  -- Family size = siblings + parents + self
        NewColumnName('FamilySize')
    ) AS dt
) WITH DATA;

-- 3c. Ordinal encode gender and embarked
CREATE TABLE ordinalFit AS (
    SELECT * FROM TD_OrdinalEncodingFit(
        ON getCabin AS InputTable
        USING
        TargetColumns('gender', 'embarked')
    ) AS dt
) WITH DATA;

-- 3d. One-hot encode cabin prefix
CREATE TABLE onehotfittable AS (
    SELECT * FROM TD_OneHotEncodingFit(
        ON getCabin AS InputTable
        USING
        TargetColumns('cabin')
        CategoryCounts('10')  -- Top 10 cabin prefixes
        IsOutputDense('true')
    ) AS dt
) WITH DATA;

-- 3e. Scale numerical features
CREATE TABLE ScaleFit AS (
    SELECT * FROM TD_ScaleFit(
        ON getCabin AS InputTable
        USING
        TargetColumns('age', 'fare', 'pclass', 'sibsp', 'parch')
        ScaleMethod('STD')  -- Z-score standardization
    ) AS dt
) WITH DATA;

-- Step 4: Apply all transformations to training data
CREATE TABLE titanic_train_transformed AS (
    SELECT * FROM TD_ColumnTransformer(
        ON getCabin AS InputTable
        ON imputeFit AS SimpleImputeFitTable DIMENSION
        ON NonLinearCombineFit AS NonLinearCombineFitTable DIMENSION
        ON ordinalFit AS OrdinalEncodingFitTable DIMENSION
        ON onehotfittable AS OneHotEncodingFitTable DIMENSION
        ON ScaleFit AS ScaleFitTable DIMENSION
        USING
        FillRowIDColumnName('row_id')
    ) AS dt
) WITH DATA;

-- Step 5: Apply SAME transformations to test data
CREATE TABLE titanic_test_transformed AS (
    SELECT * FROM TD_ColumnTransformer(
        ON titanic_test AS InputTable
        ON imputeFit AS SimpleImputeFitTable DIMENSION
        ON NonLinearCombineFit AS NonLinearCombineFitTable DIMENSION
        ON ordinalFit AS OrdinalEncodingFitTable DIMENSION
        ON onehotfittable AS OneHotEncodingFitTable DIMENSION
        ON ScaleFit AS ScaleFitTable DIMENSION
        USING
        FillRowIDColumnName('row_id')
    ) AS dt
) WITH DATA;

-- View sample output
SELECT
    row_id,
    passenger_id,
    survived,
    pclass,
    gender,
    age,
    sibsp,
    parch,
    fare,
    embarked,
    cabin,
    FamilySize,
    cabin_A,
    cabin_B,
    cabin_C,
    cabin_other
FROM titanic_train_transformed
ORDER BY passenger_id
LIMIT 10;

/*
Sample Output:
row_id | passenger_id | survived | pclass | gender | age   | sibsp | parch | fare  | embarked | cabin | FamilySize | cabin_A | cabin_B | cabin_C | cabin_other
-------|--------------|----------|--------|--------|-------|-------|-------|-------|----------|-------|------------|---------|---------|---------|-------------
1      | 149          | 0        | 0.52   | 1      | 0.15  | -0.47 | 0.77  | 0.04  | 2        | B     | 3.0        | 0       | 1       | 0       | 0
2      | 152          | 1        | -1.56  | 2      | 0.00  | 0.43  | -0.47 | 0.59  | 2        | C     | 2.0        | 0       | 0       | 1       | 0
3      | 581          | 1        | 0.52   | 2      | -0.22 | 0.43  | 0.77  | 0.05  | 2        | ?     | 3.0        | 0       | 0       | 0       | 1
4      | 663          | 1        | -1.56  | 1      | 0.82  | -0.47 | -0.47 | 0.04  | 2        | A     | 1.0        | 1       | 0       | 0       | 0

Interpretation:
- Age, fare, pclass scaled to mean=0, std=1
- Gender encoded (1=male, 2=female)
- Embarked encoded (1=C, 2=S, 3=Q)
- FamilySize created from sibsp + parch + 1
- Cabin one-hot encoded into cabin_A, cabin_B, cabin_C, cabin_other
- Missing cabin values represented as '?' → cabin_other=1
*/
```

**Use Case**: Prepare Titanic dataset for binary classification (survived/not survived).

### Example 2: Customer Churn Feature Engineering Pipeline

Multiple transformations for customer churn prediction:

```sql
-- Step 1: Create FIT tables on training set
-- Handle missing values
CREATE TABLE churn_impute_fit AS (
    SELECT * FROM TD_SimpleImputeFit(
        ON customer_train AS InputTable
        USING
        TargetColumns('tenure', 'monthly_charges', 'total_charges')
        FillMethod('MEDIAN')
    ) AS dt
) WITH DATA;

-- Remove outliers from charges
CREATE TABLE churn_outlier_fit AS (
    SELECT * FROM TD_OutlierFilterFit(
        ON customer_train AS InputTable
        USING
        TargetColumns('monthly_charges', 'total_charges')
        OutlierMethod('IQR')
        Multiplier(1.5)
    ) AS dt
) WITH DATA;

-- Create interaction features
CREATE TABLE churn_interaction_fit AS (
    SELECT * FROM TD_NonLinearCombineFit(
        ON customer_train AS InputTable
        USING
        TargetColumns('tenure', 'monthly_charges')
        Formula('col1 * col2')  -- Lifetime value proxy
        NewColumnName('tenure_x_charges')
    ) AS dt
) WITH DATA;

-- One-hot encode categorical features
CREATE TABLE churn_onehot_fit AS (
    SELECT * FROM TD_OneHotEncodingFit(
        ON customer_train AS InputTable
        USING
        TargetColumns('contract_type', 'payment_method', 'internet_service')
        CategoryCounts('20')
        IsOutputDense('true')
    ) AS dt
) WITH DATA;

-- Scale numerical features
CREATE TABLE churn_scale_fit AS (
    SELECT * FROM TD_ScaleFit(
        ON customer_train AS InputTable
        USING
        TargetColumns('tenure', 'monthly_charges', 'total_charges')
        ScaleMethod('MINMAX')  -- Scale to [0, 1]
    ) AS dt
) WITH DATA;

-- Step 2: Transform training data
CREATE TABLE customer_train_features AS (
    SELECT * FROM TD_ColumnTransformer(
        ON customer_train AS InputTable
        ON churn_impute_fit AS SimpleImputeFitTable DIMENSION
        ON churn_outlier_fit AS OutlierFilterFitTable DIMENSION
        ON churn_interaction_fit AS NonLinearCombineFitTable DIMENSION
        ON churn_onehot_fit AS OneHotEncodingFitTable DIMENSION
        ON churn_scale_fit AS ScaleFitTable DIMENSION
        USING
        FillRowIDColumnName('customer_row_id')
    ) AS dt
) WITH DATA;

-- Step 3: Transform test data with SAME parameters
CREATE TABLE customer_test_features AS (
    SELECT * FROM TD_ColumnTransformer(
        ON customer_test AS InputTable
        ON churn_impute_fit AS SimpleImputeFitTable DIMENSION
        ON churn_outlier_fit AS OutlierFilterFitTable DIMENSION
        ON churn_interaction_fit AS NonLinearCombineFitTable DIMENSION
        ON churn_onehot_fit AS OneHotEncodingFitTable DIMENSION
        ON churn_scale_fit AS ScaleFitTable DIMENSION
        USING
        FillRowIDColumnName('customer_row_id')
    ) AS dt
) WITH DATA;

-- Verify consistent feature engineering
SELECT
    'Training' as dataset,
    COUNT(*) as row_count,
    COUNT(DISTINCT customer_id) as unique_customers,
    ROUND(AVG(tenure), 4) as avg_tenure_scaled,
    ROUND(AVG(monthly_charges), 4) as avg_charges_scaled
FROM customer_train_features

UNION ALL

SELECT
    'Test' as dataset,
    COUNT(*) as row_count,
    COUNT(DISTINCT customer_id) as unique_customers,
    ROUND(AVG(tenure), 4) as avg_tenure_scaled,
    ROUND(AVG(monthly_charges), 4) as avg_charges_scaled
FROM customer_test_features;
```

**Business Impact**: Consistent feature engineering prevents train-test mismatch and ensures reliable model performance.

### Example 3: Credit Scoring with Polynomial Features

Create complex features for credit risk assessment:

```sql
-- Step 1: Create polynomial features for non-linear relationships
CREATE TABLE credit_poly_fit AS (
    SELECT * FROM TD_PolynomialFeaturesFit(
        ON credit_applications_train AS InputTable
        USING
        TargetColumns('income', 'debt_ratio', 'credit_history_length')
        Degree(2)  -- Include squared terms and interactions
        InteractionOnly('false')
    ) AS dt
) WITH DATA;

-- Step 2: Apply log transformation to skewed variables
CREATE TABLE credit_function_fit AS (
    SELECT * FROM TD_FunctionFit(
        ON credit_applications_train AS InputTable
        USING
        TargetColumns('income', 'loan_amount')
        Functions('log')
    ) AS dt
) WITH DATA;

-- Step 3: Bin credit score into risk categories
CREATE TABLE credit_bin_fit AS (
    SELECT * FROM TD_BincodeFit(
        ON credit_applications_train AS InputTable
        USING
        TargetColumns('credit_score')
        BinningMethod('quantile')
        NumBins(5)  -- Quintiles: Very Low, Low, Medium, High, Very High
    ) AS dt
) WITH DATA;

-- Step 4: Ordinal encode employment status
CREATE TABLE credit_ordinal_fit AS (
    SELECT * FROM TD_OrdinalEncodingFit(
        ON credit_applications_train AS InputTable
        USING
        TargetColumns('employment_status')
        -- Implicit ordering: Unemployed < Part-time < Full-time < Self-employed
    ) AS dt
) WITH DATA;

-- Step 5: Scale all numerical features
CREATE TABLE credit_scale_fit AS (
    SELECT * FROM TD_ScaleFit(
        ON credit_applications_train AS InputTable
        USING
        TargetColumns('income', 'debt_ratio', 'credit_history_length', 'loan_amount')
        ScaleMethod('ROBUST')  -- Use median and IQR (robust to outliers)
    ) AS dt
) WITH DATA;

-- Step 6: Apply full transformation pipeline
CREATE TABLE credit_train_ml_ready AS (
    SELECT * FROM TD_ColumnTransformer(
        ON credit_applications_train AS InputTable
        ON credit_poly_fit AS PolynomialFeaturesFitTable DIMENSION
        ON credit_function_fit AS FunctionFitTable DIMENSION
        ON credit_bin_fit AS BincodeFitTable DIMENSION
        ON credit_ordinal_fit AS OrdinalEncodingFitTable DIMENSION
        ON credit_scale_fit AS ScaleFitTable DIMENSION
    ) AS dt
) WITH DATA;

-- Transform test set
CREATE TABLE credit_test_ml_ready AS (
    SELECT * FROM TD_ColumnTransformer(
        ON credit_applications_test AS InputTable
        ON credit_poly_fit AS PolynomialFeaturesFitTable DIMENSION
        ON credit_function_fit AS FunctionFitTable DIMENSION
        ON credit_bin_fit AS BincodeFitTable DIMENSION
        ON credit_ordinal_fit AS OrdinalEncodingFitTable DIMENSION
        ON credit_scale_fit AS ScaleFitTable DIMENSION
    ) AS dt
) WITH DATA;

-- Inspect new features created
SELECT column_name, data_type
FROM dbc.columns
WHERE tablename = 'credit_train_ml_ready'
AND columnname LIKE '%poly%' OR columnname LIKE '%log%'
ORDER BY column_name;

/*
New features created:
- income_poly_2: income²
- debt_ratio_poly_2: debt_ratio²
- credit_history_length_poly_2: credit_history_length²
- income_debt_ratio_interaction: income × debt_ratio
- income_credit_history_interaction: income × credit_history_length
- debt_ratio_credit_history_interaction: debt_ratio × credit_history_length
- log_income: log(income)
- log_loan_amount: log(loan_amount)
*/
```

**Strategic Value**: Polynomial features capture non-linear relationships (e.g., high income + high debt ratio interaction).

### Example 4: Time-Series Feature Engineering for Demand Forecasting

Transform time-series features consistently:

```sql
-- Step 1: Create lag features using NonLinearCombine
CREATE TABLE demand_lag_fit AS (
    SELECT * FROM TD_NonLinearCombineFit(
        ON sales_history_train AS InputTable
        USING
        TargetColumns('daily_sales')
        Formula('LAG(col1, 7)')  -- 7-day lag
        NewColumnName('sales_lag_7d')
    ) AS dt
) WITH DATA;

-- Step 2: Create rolling average features
CREATE TABLE demand_rolling_fit AS (
    SELECT * FROM TD_NonLinearCombineFit(
        ON sales_history_train AS InputTable
        USING
        TargetColumns('daily_sales')
        Formula('AVG(col1) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)')
        NewColumnName('sales_rolling_7d')
    ) AS dt
) WITH DATA;

-- Step 3: Handle missing values in weather data
CREATE TABLE demand_impute_fit AS (
    SELECT * FROM TD_SimpleImputeFit(
        ON sales_history_train AS InputTable
        USING
        TargetColumns('temperature', 'precipitation')
        FillMethod('FORWARD_FILL')  -- Use last known value
    ) AS dt
) WITH DATA;

-- Step 4: One-hot encode day of week, month
CREATE TABLE demand_temporal_fit AS (
    SELECT * FROM TD_OneHotEncodingFit(
        ON sales_history_train AS InputTable
        USING
        TargetColumns('day_of_week', 'month')
        IsOutputDense('true')
    ) AS dt
) WITH DATA;

-- Step 5: Scale numerical features
CREATE TABLE demand_scale_fit AS (
    SELECT * FROM TD_ScaleFit(
        ON sales_history_train AS InputTable
        USING
        TargetColumns('daily_sales', 'temperature', 'precipitation', 'promotion_flag')
        ScaleMethod('STD')
    ) AS dt
) WITH DATA;

-- Step 6: Apply transformation pipeline
CREATE TABLE sales_train_features AS (
    SELECT * FROM TD_ColumnTransformer(
        ON sales_history_train AS InputTable
        ON demand_lag_fit AS NonLinearCombineFitTable DIMENSION
        ON demand_rolling_fit AS NonLinearCombineFitTable DIMENSION  -- Multiple NonLinearCombine allowed!
        ON demand_impute_fit AS SimpleImputeFitTable DIMENSION
        ON demand_temporal_fit AS OneHotEncodingFitTable DIMENSION
        ON demand_scale_fit AS ScaleFitTable DIMENSION
    ) AS dt
) WITH DATA;

-- Transform forecast period (test set)
CREATE TABLE sales_forecast_features AS (
    SELECT * FROM TD_ColumnTransformer(
        ON sales_history_test AS InputTable
        ON demand_lag_fit AS NonLinearCombineFitTable DIMENSION
        ON demand_rolling_fit AS NonLinearCombineFitTable DIMENSION
        ON demand_impute_fit AS SimpleImputeFitTable DIMENSION
        ON demand_temporal_fit AS OneHotEncodingFitTable DIMENSION
        ON demand_scale_fit AS ScaleFitTable DIMENSION
    ) AS dt
) WITH DATA;
```

**Key Insight**: Multiple NonLinearCombineFit tables allow creating multiple lag/rolling features in single transform operation.

### Example 5: Text and Numeric Features for Sentiment Analysis

Combine text feature transformations with numeric scaling:

```sql
-- Assuming text features already extracted (TF-IDF, embeddings)
-- Step 1: Row-normalize text feature vectors
CREATE TABLE sentiment_rownorm_fit AS (
    SELECT * FROM TD_RowNormalizeFit(
        ON review_features_train AS InputTable
        USING
        TargetColumns('tfidf_1', 'tfidf_2', 'tfidf_3', 'tfidf_4', 'tfidf_5')
        NormType('L2')  -- Unit norm
    ) AS dt
) WITH DATA;

-- Step 2: Handle missing numeric features
CREATE TABLE sentiment_impute_fit AS (
    SELECT * FROM TD_SimpleImputeFit(
        ON review_features_train AS InputTable
        USING
        TargetColumns('review_length', 'avg_word_length', 'exclamation_count')
        FillMethod('MEAN')
    ) AS dt
) WITH DATA;

-- Step 3: Scale numeric metadata features
CREATE TABLE sentiment_scale_fit AS (
    SELECT * FROM TD_ScaleFit(
        ON review_features_train AS InputTable
        USING
        TargetColumns('review_length', 'avg_word_length', 'exclamation_count', 'caps_ratio')
        ScaleMethod('MINMAX')
    ) AS dt
) WITH DATA;

-- Step 4: Ordinal encode star rating
CREATE TABLE sentiment_ordinal_fit AS (
    SELECT * FROM TD_OrdinalEncodingFit(
        ON review_features_train AS InputTable
        USING
        TargetColumns('star_rating')  -- 1, 2, 3, 4, 5 → 0, 1, 2, 3, 4
    ) AS dt
) WITH DATA;

-- Step 5: Apply combined transformations
CREATE TABLE review_train_ml_features AS (
    SELECT * FROM TD_ColumnTransformer(
        ON review_features_train AS InputTable
        ON sentiment_rownorm_fit AS RowNormalizeFitTable DIMENSION
        ON sentiment_impute_fit AS SimpleImputeFitTable DIMENSION
        ON sentiment_scale_fit AS ScaleFitTable DIMENSION
        ON sentiment_ordinal_fit AS OrdinalEncodingFitTable DIMENSION
        USING
        FillRowIDColumnName('review_id')
    ) AS dt
) WITH DATA;

-- Transform test reviews
CREATE TABLE review_test_ml_features AS (
    SELECT * FROM TD_ColumnTransformer(
        ON review_features_test AS InputTable
        ON sentiment_rownorm_fit AS RowNormalizeFitTable DIMENSION
        ON sentiment_impute_fit AS SimpleImputeFitTable DIMENSION
        ON sentiment_scale_fit AS ScaleFitTable DIMENSION
        ON sentiment_ordinal_fit AS OrdinalEncodingFitTable DIMENSION
        USING
        FillRowIDColumnName('review_id')
    ) AS dt
) WITH DATA;
```

**Use Case**: Prepare both text features (TF-IDF) and numeric metadata for sentiment classification.

### Example 6: Production Scoring Pipeline

Apply transformations to new production data:

```sql
-- Production scoring workflow
-- FIT tables already exist from training phase

-- Step 1: Load new customers to score
CREATE TABLE new_customers_to_score AS (
    SELECT * FROM customer_data
    WHERE score_date = CURRENT_DATE
    AND churn_score IS NULL
) WITH DATA;

-- Step 2: Apply transformation pipeline (same FIT tables from training)
CREATE TABLE new_customers_features AS (
    SELECT * FROM TD_ColumnTransformer(
        ON new_customers_to_score AS InputTable
        ON production_impute_fit AS SimpleImputeFitTable DIMENSION
        ON production_outlier_fit AS OutlierFilterFitTable DIMENSION
        ON production_interaction_fit AS NonLinearCombineFitTable DIMENSION
        ON production_onehot_fit AS OneHotEncodingFitTable DIMENSION
        ON production_scale_fit AS ScaleFitTable DIMENSION
        USING
        FillRowIDColumnName('scoring_row_id')
    ) AS dt
) WITH DATA;

-- Step 3: Score with trained model
CREATE TABLE new_customer_scores AS (
    SELECT
        scoring_row_id,
        customer_id,
        score_date,
        TD_GLMPredict(
            ON new_customers_features AS InputTable
            ON churn_model AS ModelTable DIMENSION
            USING
            IDColumn('customer_id')
            Accumulate('score_date')
        ) AS churn_probability
    FROM new_customers_features
) WITH DATA;

-- Step 4: Update customer table with scores
UPDATE customer_data
SET
    churn_score = cs.churn_probability,
    score_timestamp = CURRENT_TIMESTAMP
FROM new_customer_scores cs
WHERE customer_data.customer_id = cs.customer_id
AND customer_data.score_date = cs.score_date;

-- Monitor feature drift
SELECT
    'Training' as dataset,
    ROUND(AVG(tenure), 4) as avg_tenure,
    ROUND(STDDEV(monthly_charges), 4) as std_charges
FROM customer_train_features

UNION ALL

SELECT
    'Production' as dataset,
    ROUND(AVG(tenure), 4) as avg_tenure,
    ROUND(STDDEV(monthly_charges), 4) as std_charges
FROM new_customers_features;

/*
If production features drift significantly from training distribution,
consider retraining the model
*/
```

**Production Best Practice**: Store FIT tables permanently and version them with model versions.

## Common Use Cases

### 1. Ensure Train-Test Consistency

```sql
-- BAD: Separate transformations can lead to inconsistency
-- Don't do this:
CREATE TABLE train_scaled AS (
    SELECT * FROM TD_ScaleTransform(
        ON train_data AS InputTable
        ON (SELECT * FROM TD_ScaleFit(ON train_data USING ...) AS fitdt) AS FitTable DIMENSION
        USING ...
    ) AS dt
) WITH DATA;

CREATE TABLE test_scaled AS (
    SELECT * FROM TD_ScaleTransform(
        ON test_data AS InputTable
        ON (SELECT * FROM TD_ScaleFit(ON test_data USING ...) AS fitdt) AS FitTable DIMENSION  -- WRONG! Uses test statistics
        USING ...
    ) AS dt
) WITH DATA;

-- GOOD: Use same FIT table for both train and test
CREATE TABLE scale_fit AS (SELECT * FROM TD_ScaleFit(ON train_data USING ...) AS dt) WITH DATA;

CREATE TABLE train_scaled AS (
    SELECT * FROM TD_ColumnTransformer(
        ON train_data AS InputTable
        ON scale_fit AS ScaleFitTable DIMENSION
    ) AS dt
) WITH DATA;

CREATE TABLE test_scaled AS (
    SELECT * FROM TD_ColumnTransformer(
        ON test_data AS InputTable
        ON scale_fit AS ScaleFitTable DIMENSION  -- CORRECT! Uses training statistics
    ) AS dt
) WITH DATA;
```

### 2. Version Control for Feature Engineering

```sql
-- Store FIT tables with version identifiers
CREATE TABLE fit_tables_registry (
    model_version VARCHAR(50),
    fit_table_type VARCHAR(100),
    fit_table_name VARCHAR(255),
    created_date DATE,
    training_data_start_date DATE,
    training_data_end_date DATE,
    row_count BIGINT,
    description VARCHAR(500)
);

-- Register FIT tables
INSERT INTO fit_tables_registry VALUES
('churn_model_v1.2', 'SimpleImputeFit', 'churn_impute_fit_v1_2', CURRENT_DATE, '2024-01-01', '2024-10-31', 50000, 'Median imputation for tenure and charges'),
('churn_model_v1.2', 'ScaleFit', 'churn_scale_fit_v1_2', CURRENT_DATE, '2024-01-01', '2024-10-31', 50000, 'Standard scaling for numerical features'),
('churn_model_v1.2', 'OneHotEncodingFit', 'churn_onehot_fit_v1_2', CURRENT_DATE, '2024-01-01', '2024-10-31', 50000, 'One-hot encoding for contract type and payment method');

-- Retrieve FIT tables for specific model version
SELECT fit_table_type, fit_table_name
FROM fit_tables_registry
WHERE model_version = 'churn_model_v1.2'
ORDER BY fit_table_type;
```

### 3. Cross-Validation with Consistent Transformations

```sql
-- For each fold, create FIT tables on training portion
FOR fold IN 1..5 DO
    -- Create FIT tables on fold training data
    CREATE TABLE fold_${fold}_scale_fit AS (
        SELECT * FROM TD_ScaleFit(
            ON training_data AS InputTable
            WHERE fold_id != ${fold}  -- Exclude validation fold
            USING TargetColumns('age', 'income') ScaleMethod('STD')
        ) AS dt
    ) WITH DATA;

    -- Transform training portion
    CREATE TABLE fold_${fold}_train_features AS (
        SELECT * FROM TD_ColumnTransformer(
            ON training_data AS InputTable
            WHERE fold_id != ${fold}
            ON fold_${fold}_scale_fit AS ScaleFitTable DIMENSION
        ) AS dt
    ) WITH DATA;

    -- Transform validation portion (using training fold FIT)
    CREATE TABLE fold_${fold}_val_features AS (
        SELECT * FROM TD_ColumnTransformer(
            ON training_data AS InputTable
            WHERE fold_id = ${fold}
            ON fold_${fold}_scale_fit AS ScaleFitTable DIMENSION
        ) AS dt
    ) WITH DATA;

    -- Train model and evaluate
    -- ...
END FOR;
```

## Best Practices

1. **Always Create FIT Tables on Training Data Only**:
   - Never create FIT tables on test data (causes data leakage)
   - Never create FIT tables on combined train+test data
   - FIT tables should represent only what model would see during training

2. **Maintain FIT Table Order**:
   - Provide FIT tables in the same order as transformation sequence
   - Order matters for reproducibility
   - Document the transformation sequence in comments

3. **Version FIT Tables with Models**:
   - Store FIT tables permanently with model version identifiers
   - If you retrain model, create new FIT tables
   - Don't overwrite existing FIT tables used by production models

4. **Test Transformation Pipeline Before Model Training**:
   - Verify no missing values after imputation
   - Check feature distributions after scaling
   - Ensure one-hot encoding creates expected columns
   - Validate polynomial features are created correctly

5. **Monitor Feature Drift in Production**:
   - Compare production feature distributions to training
   - Alert if features drift significantly
   - Consider retraining if drift exceeds thresholds

6. **Use FillRowIDColumnName for Traceability**:
   - Add unique row identifiers to track data through pipeline
   - Helps debug transformation issues
   - Useful for joining back to original data

7. **Handle Categorical Cardinality**:
   - Limit one-hot encoding to reasonable number of categories
   - Use CategoryCounts parameter to cap number of dummy variables
   - Consider target encoding for high-cardinality categoricals

8. **Document Transformation Rationale**:
   - Comment why each transformation is applied
   - Note business logic behind feature engineering choices
   - Document acceptable ranges for features

9. **Performance Optimization**:
   - Maximum 128 columns in FIT tables
   - Limit polynomial degree to avoid feature explosion
   - Consider feature selection after transformation

10. **Error Handling**:
    - Check for column name mismatches between input and FIT tables
    - Validate data types are compatible
    - Test with small sample before applying to full dataset

## Transformation Sequence Best Practices

Recommended order of transformations:

1. **SimpleImpute**: Handle missing values first
2. **OutlierFilter**: Remove/cap outliers before scaling
3. **Function**: Apply log/sqrt transformations to normalize distributions
4. **NonLinearCombine**: Create interaction features
5. **PolynomialFeatures**: Generate polynomial terms
6. **Bincode**: Discretize continuous variables (if needed)
7. **OrdinalEncoding**: Encode ordinal categoricals
8. **OneHotEncoding**: Encode nominal categoricals (creates many columns)
9. **Scale**: Scale after all features are created
10. **RowNormalize**: Row normalization last (if needed for specific algorithms)

## Related Functions

### FIT Functions (Create FIT Tables)
- **TD_SimpleImputeFit**: Create imputation parameters
- **TD_ScaleFit**: Create scaling parameters
- **TD_BincodeFit**: Create binning boundaries
- **TD_FunctionFit**: Create function transformation parameters
- **TD_NonLinearCombineFit**: Create interaction feature specifications
- **TD_OutlierFilterFit**: Create outlier filtering rules
- **TD_PolynomialFeaturesFit**: Create polynomial feature specifications
- **TD_RowNormalizeFit**: Create row normalization parameters
- **TD_OrdinalEncodingFit**: Create ordinal encoding mappings
- **TD_OneHotEncodingFit**: Create one-hot encoding mappings

### Individual Transform Functions
- **TD_SimpleImputeTransform**: Apply imputation (alternative to ColumnTransformer)
- **TD_ScaleTransform**: Apply scaling (alternative to ColumnTransformer)
- **TD_BincodeTransform**: Apply binning (alternative to ColumnTransformer)
- And others for each transformation type

### Model Training Functions
- **TD_GLM**: Train models on transformed features
- **TD_DecisionForest**: Train random forests on transformed features
- **TD_XGBoost**: Train gradient boosting on transformed features

## Notes and Limitations

1. **Maximum Column Limit**:
   - FIT tables limited to 128 columns maximum
   - Plan feature engineering to stay within limit
   - Consider feature selection if approaching limit

2. **BincodeFit Variable-Width Limitation**:
   - Maximum 5 columns when using variable-width binning
   - Use fixed-width or quantile binning for more columns
   - Or apply binning in multiple batches

3. **FIT Table Instance Limits**:
   - Only NonLinearCombineFit allows multiple instances
   - All other FIT table types: single instance only
   - To apply same transformation type differently, use separate transform calls

4. **FIT Table Order Requirement**:
   - FIT tables must be provided in training transformation sequence
   - Order affects reproducibility
   - Changing order may produce different results (e.g., scale before vs after polynomial features)

5. **Schema Changes**:
   - OneHotEncoding creates new columns (increases column count)
   - PolynomialFeatures creates new columns (can explode feature count)
   - NonLinearCombine creates new columns
   - BincodeFit and OrdinalEncodingFit modify target column schema
   - Plan for increased column count in output

6. **Data Type Requirements**:
   - Input columns must match FIT table column specifications
   - Data types must be compatible
   - Column names must match exactly (case-sensitive)

7. **Missing Value Handling**:
   - Apply SimpleImpute early in pipeline to handle missing values
   - Many transformations fail on NULL values
   - Test that all NULLs are handled before model training

8. **Performance Considerations**:
   - Large FIT tables (many columns) increase processing time
   - Polynomial features with high degree create many columns
   - One-hot encoding with high cardinality creates many columns
   - Consider sampling for initial testing

9. **Training vs Scoring**:
   - FIT tables created once on training data
   - Same FIT tables used for all future scoring
   - Never create new FIT tables on production scoring data

10. **Debugging**:
    - Test each transformation individually before combining
    - Use FillRowIDColumnName to trace rows through pipeline
    - Compare input/output column lists to verify expected changes
    - Check for unexpected NULL values in output

## Version Information

- **Function Version**: Based on Teradata Database Analytic Functions Version 17.20
- **Generated**: November 28, 2025
- **Category**: Feature Engineering Transform Functions / Data Preprocessing / ML Pipeline
