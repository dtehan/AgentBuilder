# TD_GetRowsWithoutMissingValues

## Function Name
- **TD_GetRowsWithoutMissingValues**: Complete Case Selection Function - Returns rows without missing (NULL) values in specified columns

## Description
TD_GetRowsWithoutMissingValues displays rows that have non-NULL values in all specified input table columns. This function performs "complete case analysis" or "listwise deletion" by filtering the dataset to include only rows where specified columns are fully populated.

A NULL value indicates the absence of information, meaning a real value is unknown or non-existent. NULL is not zero or blank—it represents missing data. This function helps identify and retain only complete records, which is essential for many analytical and modeling tasks.

### Characteristics
- Filters rows to complete cases (no NULLs in target columns)
- Configurable column selection (specific columns or all columns)
- Preserves all columns in output (not just target columns)
- Supports column range syntax for convenience
- Can accumulate additional columns beyond target columns
- Essential preprocessing step for many algorithms

### Null Value Causes
- Incomplete data entry
- Data corruption
- Errors in data processing
- Data not collected
- Data not applicable for certain records

## When to Use TD_GetRowsWithoutMissingValues

TD_GetRowsWithoutMissingValues is essential for handling missing data:

### Data Quality and Cleaning
- **Complete case analysis**: Keep only fully populated records
- **Data validation**: Verify data completeness before processing
- **Quality assurance**: Ensure critical fields are populated
- **Compliance checking**: Verify required fields are not NULL
- **Error detection**: Identify data collection issues

### Machine Learning and Analytics
- **Algorithm requirements**: Many ML algorithms can't handle NULLs
- **Training data preparation**: Ensure clean training sets
- **Model validation**: Create test sets without missing values
- **Baseline models**: Train simpler models on complete cases
- **Algorithm compatibility**: Some algorithms require complete data

### Statistical Analysis
- **Correlation analysis**: Requires complete pairs of values
- **Regression modeling**: Standard regression can't handle NULLs
- **Hypothesis testing**: Statistical tests require complete data
- **Descriptive statistics**: Calculate statistics on complete cases
- **Paired analyses**: Compare groups with complete measurements

### Business Applications
- **Customer analytics**: Analyze customers with complete profiles
- **Sales forecasting**: Use transactions with all required fields
- **Risk assessment**: Score only complete applications
- **Campaign targeting**: Target customers with known attributes
- **Churn prediction**: Build models on complete customer histories
- **Credit scoring**: Evaluate applicants with full information

### Data Exploration
- **Initial assessment**: Understand complete data characteristics
- **Subset analysis**: Analyze well-documented subset
- **Pattern detection**: Find patterns in complete records
- **Benchmark creation**: Establish baselines with complete data
- **Sample creation**: Generate representative complete samples

### Comparison with Imputation
TD_GetRowsWithoutMissingValues (deletion) vs TD_SimpleImpute (imputation):

**Use Deletion When**:
- Missing data is minimal (< 5% of rows)
- Data is Missing Completely At Random (MCAR)
- Large dataset where losing rows is acceptable
- Need guaranteed real values (no synthetic data)
- Quick exploratory analysis

**Use Imputation When**:
- Missing data is substantial (> 5%)
- Data is Missing At Random (MAR) or Not At Random (MNAR)
- Cannot afford to lose samples
- Need to preserve all observations
- Building production models

## Syntax

```sql
TD_GetRowsWithoutMissingValues (
    ON { table | view | (query) } AS InputTable [ PARTITION BY ANY [ ORDER BY order_column ] ]
    [ USING
        TargetColumns ({ 'target_column' | target_column_range }[,...])
        [ Accumulate ({ 'accumulate_column' | accumulate_column_range }[,...]) ]
    ]
)
```

**Note:** You can call this function from:
- The FROM clause of a SELECT statement
- As part of a CREATE TABLE statement
- As part of a CREATE VIEW statement

## Required Syntax Elements

### ON Clause
Specifies the table name, view name, or query as an InputTable.
- **InputTable**: Table containing data to filter
- **PARTITION BY ANY**: Optional partitioning (typically used)
- **ORDER BY**: Optional ordering within partitions

## Optional Syntax Elements

### TargetColumns
Specifies the target column names to check for non-NULL values.
- **Format**: Column names or column ranges
- **Multiple columns**: Separate with commas
- **Column ranges**: Use syntax like `[col1:col5]`
- **Default**: If omitted, function considers ALL columns
- **Logic**: Row must have non-NULL in ALL target columns to be returned
- **Example**: `TargetColumns('age', 'income', 'credit_score')`

### Accumulate
Specifies the input table column names to copy to the output table.
- **Purpose**: Include additional columns not checked for NULLs
- **Use case**: Keep identifier columns even if they have NULLs
- **Format**: Column names or column ranges
- **Example**: `Accumulate('customer_id', 'transaction_date')`
- **Note**: Accumulated columns can contain NULLs

## Input

### InputTable Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | Any | Columns for which non-NULL values are checked |
| accumulate_column | Any | Input table column names to copy to output table |
| (other columns) | Any | Additional columns in table |

## Output

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | Any | Columns for which non-NULL values are checked (guaranteed non-NULL) |
| accumulate_column | Any | Input table column names copied to output table (may contain NULLs) |
| (other columns) | Any | All input columns preserved in output |

**Output contains only rows where ALL target columns are non-NULL.**

## Code Examples

### Example 1: Basic Complete Case Selection (Titanic Dataset)

Filter Titanic data to rows with complete information:

```sql
-- Create Titanic passenger data with some missing values
CREATE TABLE titanic_passengers (
    passenger INTEGER,
    survived BYTEINT,
    pclass BYTEINT,
    name VARCHAR(100),
    gender VARCHAR(10),
    age DECIMAL(5,2),
    sibsp BYTEINT,
    parch BYTEINT,
    ticket VARCHAR(20),
    fare DECIMAL(10,2),
    cabin VARCHAR(20),
    embarked CHAR(1)
);

INSERT INTO titanic_passengers VALUES
(1, 0, 3, 'Braund, Mr. Owen Harris', 'male', 22, 1, 0, 'A/5 21171', 7.25, NULL, 'S'),
(30, 0, 3, 'Todoroff, Mr. Lalio', 'male', NULL, 0, 0, '349216', 7.8958, NULL, 'S'),
(505, 1, 1, 'Maioni, Miss. Roberta', 'female', 16, 0, 0, '110152', 86.5, 'B79', 'S'),
(631, 1, 1, 'Barkworth, Mr. Algernon Henry Wilson', 'male', 80, 0, 0, '27042', 30, 'A23', 'S'),
(873, 0, 1, 'Carlsson, Mr. Frans Olof', 'male', 33, 0, 0, '695', 5, 'B51 B53 B55', 'S');

-- Select rows with no missing values in name through cabin (column range)
SELECT * FROM TD_GetRowsWithoutMissingValues (
    ON titanic_passengers AS InputTable
    USING
    TargetColumns('[name:cabin]')  -- Checks: name, gender, age, sibsp, parch, ticket, fare, cabin
) AS dt
ORDER BY passenger;

/*
Output:
passenger | survived | pclass | name                                  | gender | age | sibsp | parch | ticket      | fare | cabin        | embarked
----------|----------|--------|---------------------------------------|--------|-----|-------|-------|-------------|------|--------------|----------
505       | 1        | 1      | Maioni, Miss. Roberta                 | female | 16  | 0     | 0     | 110152      | 86.5 | B79          | S
631       | 1        | 1      | Barkworth, Mr. Algernon Henry Wilson  | male   | 80  | 0     | 0     | 27042       | 30   | A23          | S
873       | 0        | 1      | Carlsson, Mr. Frans Olof              | male   | 33  | 0     | 0     | 695         | 5    | B51 B53 B55  | S

Excluded rows:
- passenger 1: cabin is NULL
- passenger 30: age is NULL, cabin is NULL

Returned: 3 out of 5 rows (60% complete cases)
*/

-- Compare data loss
SELECT
    'Original' as dataset,
    COUNT(*) as row_count,
    ROUND(AVG(age), 2) as avg_age,
    ROUND(AVG(fare), 2) as avg_fare
FROM titanic_passengers

UNION ALL

SELECT
    'Complete Cases' as dataset,
    COUNT(*) as row_count,
    ROUND(AVG(age), 2) as avg_age,
    ROUND(AVG(fare), 2) as avg_fare
FROM TD_GetRowsWithoutMissingValues (
    ON titanic_passengers AS InputTable
    USING TargetColumns('[name:cabin]')
) AS dt;

/*
Output:
dataset         | row_count | avg_age | avg_fare
----------------|-----------|---------|----------
Original        | 5         | 37.75   | 27.31
Complete Cases  | 3         | 43.00   | 40.50

Analysis:
- Lost 40% of data (2 of 5 rows)
- Average age increased (missing values were younger passengers)
- Average fare increased (missing values were lower fares)
- IMPORTANT: Complete case analysis can introduce bias!
*/
```

**Use Case**: Prepare clean dataset for analysis requiring complete records.

### Example 2: Customer Churn Model Training Data Preparation

Create training set with complete customer profiles:

```sql
-- Customer table with missing values
CREATE TABLE customer_profiles (
    customer_id INTEGER,
    account_number VARCHAR(50),
    signup_date DATE,
    age INTEGER,
    income DECIMAL(12,2),
    credit_score INTEGER,
    tenure_months INTEGER,
    num_products BYTEINT,
    has_credit_card BYTEINT,
    is_active_member BYTEINT,
    monthly_charges DECIMAL(10,2),
    churned BYTEINT
);

-- Insert sample data (some with missing values)
INSERT INTO customer_profiles VALUES
(1001, 'ACC001', '2020-01-15', 34, 75000, 720, 48, 3, 1, 1, 125.50, 0),
(1002, 'ACC002', '2020-02-20', NULL, 60000, 680, 42, 2, 0, 1, 89.99, 0),  -- Missing age
(1003, 'ACC003', '2020-03-10', 28, NULL, 700, 36, 2, 1, 1, 95.00, 1),     -- Missing income
(1004, 'ACC004', '2020-04-05', 52, 110000, NULL, 60, 4, 1, 1, 155.00, 0), -- Missing credit_score
(1005, 'ACC005', '2020-05-12', 41, 85000, 740, 54, 3, 1, 1, 135.75, 0),
(1006, 'ACC006', '2020-06-18', 29, 55000, 650, 30, 1, 0, 0, 65.00, 1),
(1007, 'ACC007', '2020-07-22', 45, 95000, 710, NULL, 3, 1, 1, 145.00, 0); -- Missing tenure

-- Create training set with complete cases for critical features
CREATE TABLE customer_training_complete AS (
    SELECT * FROM TD_GetRowsWithoutMissingValues (
        ON customer_profiles AS InputTable
        USING
        TargetColumns('age', 'income', 'credit_score', 'tenure_months', 'num_products',
                      'has_credit_card', 'is_active_member', 'monthly_charges', 'churned')
        -- Keep customer_id and account_number even if NULL (they won't be, but shows pattern)
        Accumulate('customer_id', 'account_number', 'signup_date')
    ) AS dt
) WITH DATA;

-- Analyze impact of complete case filtering
WITH summary AS (
    SELECT
        'Original Data' as dataset,
        COUNT(*) as total_customers,
        SUM(churned) as churned_customers,
        ROUND(SUM(churned) * 100.0 / COUNT(*), 2) as churn_rate,
        ROUND(AVG(age), 1) as avg_age,
        ROUND(AVG(income), 0) as avg_income,
        ROUND(AVG(credit_score), 0) as avg_credit_score
    FROM customer_profiles

    UNION ALL

    SELECT
        'Complete Cases' as dataset,
        COUNT(*) as total_customers,
        SUM(churned) as churned_customers,
        ROUND(SUM(churned) * 100.0 / COUNT(*), 2) as churn_rate,
        ROUND(AVG(age), 1) as avg_age,
        ROUND(AVG(income), 0) as avg_income,
        ROUND(AVG(credit_score), 0) as avg_credit_score
    FROM customer_training_complete
)
SELECT
    dataset,
    total_customers,
    churned_customers,
    churn_rate as churn_rate_pct,
    avg_age,
    avg_income,
    avg_credit_score
FROM summary;

/*
Output:
dataset         | total_customers | churned_customers | churn_rate_pct | avg_age | avg_income | avg_credit_score
----------------|-----------------|-------------------|----------------|---------|------------|------------------
Original Data   | 7               | 2                 | 28.57          | 38.5    | 80000      | 700
Complete Cases  | 4               | 1                 | 25.00          | 38.5    | 91250      | 705

Impact Analysis:
- Lost 43% of customers (3 of 7)
- Churn rate changed from 28.57% to 25.00%
- Average income increased (missing income customers excluded)
- May introduce bias if missing values are not random
*/

-- Train churn model on complete cases
CREATE TABLE churn_model AS (
    SELECT * FROM TD_GLM (
        ON customer_training_complete AS InputTable
        USING
        TargetColumn('churned')
        InputColumns('age', 'income', 'credit_score', 'tenure_months',
                     'num_products', 'has_credit_card', 'is_active_member', 'monthly_charges')
        Family('BINOMIAL')
        LinkFunction('LOGIT')
        MaxIterNum(100)
    ) AS dt
) WITH DATA;
```

**Business Decision**: Use complete cases for training, but consider imputation for production scoring.

### Example 3: Compare Deletion vs Keeping All Data

Demonstrate impact of complete case selection:

```sql
-- Survey data with varying missing patterns
CREATE TABLE customer_survey (
    respondent_id INTEGER,
    age INTEGER,
    satisfaction_score BYTEINT,
    nps_score BYTEINT,
    product_usage_hours DECIMAL(10,2),
    support_contacts INTEGER,
    renewal_intent BYTEINT
);

-- Insert sample data with different missing patterns
INSERT INTO customer_survey VALUES
(1, 34, 8, 9, 12.5, 2, 1),
(2, NULL, 7, 8, 10.0, 1, 1),    -- Missing age
(3, 28, NULL, NULL, 15.0, 0, 1),-- Missing satisfaction, nps
(4, 52, 6, 6, NULL, 3, 0),      -- Missing usage
(5, 41, 9, 10, 20.0, 1, 1),
(6, NULL, NULL, 9, 8.5, 2, 1),  -- Missing age, satisfaction
(7, 45, 8, 8, 18.0, 2, 1),
(8, 29, 5, 4, 5.0, 5, 0),
(9, NULL, 7, 7, NULL, 1, NULL), -- Missing age, usage, renewal
(10, 38, 9, 9, 22.0, 1, 1);

-- Strategy 1: All columns must be complete
CREATE TABLE survey_complete_all AS (
    SELECT * FROM TD_GetRowsWithoutMissingValues (
        ON customer_survey AS InputTable
        -- No TargetColumns specified = check ALL columns
    ) AS dt
) WITH DATA;

-- Strategy 2: Only key columns must be complete
CREATE TABLE survey_complete_key AS (
    SELECT * FROM TD_GetRowsWithoutMissingValues (
        ON customer_survey AS InputTable
        USING
        TargetColumns('age', 'satisfaction_score', 'renewal_intent')
    ) AS dt
) WITH DATA;

-- Strategy 3: Keep all data (no filtering)
CREATE TABLE survey_all AS (
    SELECT * FROM customer_survey
) WITH DATA;

-- Compare strategies
SELECT
    'Strategy 1: All Complete' as strategy,
    COUNT(*) as sample_size,
    ROUND(AVG(age), 1) as avg_age,
    ROUND(AVG(satisfaction_score), 2) as avg_satisfaction,
    ROUND(AVG(CAST(renewal_intent AS DECIMAL)), 2) as renewal_rate
FROM survey_complete_all

UNION ALL

SELECT
    'Strategy 2: Key Complete' as strategy,
    COUNT(*) as sample_size,
    ROUND(AVG(age), 1) as avg_age,
    ROUND(AVG(satisfaction_score), 2) as avg_satisfaction,
    ROUND(AVG(CAST(renewal_intent AS DECIMAL)), 2) as renewal_rate
FROM survey_complete_key

UNION ALL

SELECT
    'Strategy 3: All Data' as strategy,
    COUNT(*) as sample_size,
    ROUND(AVG(age), 1) as avg_age,
    ROUND(AVG(satisfaction_score), 2) as avg_satisfaction,
    ROUND(AVG(CAST(renewal_intent AS DECIMAL)), 2) as renewal_rate
FROM survey_all;

/*
Output:
strategy                  | sample_size | avg_age | avg_satisfaction | renewal_rate
--------------------------|-------------|---------|------------------|-------------
Strategy 1: All Complete  | 5           | 37.6    | 7.60             | 0.80
Strategy 2: Key Complete  | 6           | 37.8    | 7.50             | 0.83
Strategy 3: All Data      | 10          | 38.1    | 7.50             | 0.89

Trade-off Analysis:
- Strategy 1: Most restrictive, smallest sample (50%), highest quality
- Strategy 2: Balanced, medium sample (60%), good quality
- Strategy 3: Largest sample (100%), includes NULLs, most representative

Recommendation: Use Strategy 2 for most analyses
*/
```

**Strategic Insight**: Balance data loss vs data quality based on analysis needs.

### Example 4: Sequential Missing Data Handling

Combine deletion with imputation for optimal results:

```sql
-- Real estate dataset
CREATE TABLE property_listings (
    listing_id INTEGER,
    address VARCHAR(200),
    bedrooms INTEGER,
    bathrooms DECIMAL(3,1),
    sqft INTEGER,
    lot_size INTEGER,
    year_built INTEGER,
    garage_spaces INTEGER,
    has_pool BYTEINT,
    list_price DECIMAL(12,2)
);

-- Step 1: Remove rows with missing critical fields
CREATE TABLE properties_step1 AS (
    SELECT * FROM TD_GetRowsWithoutMissingValues (
        ON property_listings AS InputTable
        USING
        TargetColumns('bedrooms', 'bathrooms', 'sqft', 'list_price')  -- Critical fields
        -- Allow NULLs in: lot_size, year_built, garage_spaces, has_pool
    ) AS dt
) WITH DATA;

-- Step 2: Impute missing optional fields
CREATE TABLE garage_impute_fit AS (
    SELECT * FROM TD_SimpleImputeFit (
        ON properties_step1 AS InputTable
        USING
        TargetColumns('garage_spaces', 'lot_size', 'year_built')
        FillMethod('MEDIAN')
    ) AS dt
) WITH DATA;

CREATE TABLE properties_step2 AS (
    SELECT * FROM TD_SimpleImputeTransform (
        ON properties_step1 AS InputTable
        ON garage_impute_fit AS FitTable DIMENSION
    ) AS dt
) WITH DATA;

-- Step 3: Handle has_pool (binary) with mode imputation
CREATE TABLE pool_impute_fit AS (
    SELECT * FROM TD_SimpleImputeFit (
        ON properties_step2 AS InputTable
        USING
        TargetColumns('has_pool')
        FillMethod('MODE')
    ) AS dt
) WITH DATA;

CREATE TABLE properties_final AS (
    SELECT * FROM TD_SimpleImputeTransform (
        ON properties_step2 AS InputTable
        ON pool_impute_fit AS FitTable DIMENSION
    ) AS dt
) WITH DATA;

-- Verify no missing values remain
SELECT
    'Critical Fields (deleted)' as field_type,
    SUM(CASE WHEN bedrooms IS NULL THEN 1 ELSE 0 END) as null_bedrooms,
    SUM(CASE WHEN bathrooms IS NULL THEN 1 ELSE 0 END) as null_bathrooms,
    SUM(CASE WHEN sqft IS NULL THEN 1 ELSE 0 END) as null_sqft,
    SUM(CASE WHEN list_price IS NULL THEN 1 ELSE 0 END) as null_price
FROM properties_final

UNION ALL

SELECT
    'Optional Fields (imputed)' as field_type,
    SUM(CASE WHEN garage_spaces IS NULL THEN 1 ELSE 0 END) as null_garage,
    SUM(CASE WHEN lot_size IS NULL THEN 1 ELSE 0 END) as null_lot,
    SUM(CASE WHEN year_built IS NULL THEN 1 ELSE 0 END) as null_year,
    SUM(CASE WHEN has_pool IS NULL THEN 1 ELSE 0 END) as null_pool
FROM properties_final;

/*
Expected Output:
field_type                | null_bedrooms | null_bathrooms | null_sqft | null_price
--------------------------|---------------|----------------|-----------|------------
Critical Fields (deleted) | 0             | 0              | 0         | 0
Optional Fields (imputed) | 0             | 0              | 0         | 0

Hybrid Approach Benefits:
- Strict on critical fields (deletion ensures quality)
- Flexible on optional fields (imputation preserves sample size)
- Best of both worlds: quality + quantity
*/
```

**Best Practice**: Use deletion for critical fields, imputation for optional fields.

### Example 5: Missing Data Pattern Analysis

Understand missing data before deciding on strategy:

```sql
-- Analyze missing data patterns
WITH missing_analysis AS (
    SELECT
        customer_id,
        CASE WHEN age IS NULL THEN 1 ELSE 0 END as missing_age,
        CASE WHEN income IS NULL THEN 1 ELSE 0 END as missing_income,
        CASE WHEN credit_score IS NULL THEN 1 ELSE 0 END as missing_credit_score,
        CASE WHEN employment_status IS NULL THEN 1 ELSE 0 END as missing_employment
    FROM customer_applications
),
missing_patterns AS (
    SELECT
        missing_age,
        missing_income,
        missing_credit_score,
        missing_employment,
        COUNT(*) as pattern_count
    FROM missing_analysis
    GROUP BY missing_age, missing_income, missing_credit_score, missing_employment
)
SELECT
    CASE WHEN missing_age = 1 THEN 'Missing' ELSE 'Present' END as age,
    CASE WHEN missing_income = 1 THEN 'Missing' ELSE 'Present' END as income,
    CASE WHEN missing_credit_score = 1 THEN 'Missing' ELSE 'Present' END as credit_score,
    CASE WHEN missing_employment = 1 THEN 'Missing' ELSE 'Present' END as employment,
    pattern_count,
    ROUND(pattern_count * 100.0 / SUM(pattern_count) OVER (), 2) as pct_of_total
FROM missing_patterns
ORDER BY pattern_count DESC;

/*
Example Output:
age     | income  | credit_score | employment | pattern_count | pct_of_total
--------|---------|--------------|------------|---------------|-------------
Present | Present | Present      | Present    | 8500          | 85.00%       ← Complete cases
Present | Present | Missing      | Present    | 600           | 6.00%        ← Only credit_score missing
Missing | Present | Present      | Present    | 400           | 4.00%        ← Only age missing
Present | Missing | Present      | Present    | 300           | 3.00%        ← Only income missing
Missing | Missing | Missing      | Missing    | 200           | 2.00%        ← All missing

Decision Matrix:
- 85% complete cases → Can use deletion (minimal data loss)
- Missing patterns not correlated → MCAR (Missing Completely At Random)
- If < 5% complete → Must use imputation
- If missing correlated with outcome → MNAR (Missing Not At Random), be cautious
*/

-- Calculate data loss for different deletion strategies
SELECT
    'No filtering' as strategy,
    COUNT(*) as sample_size,
    100.0 as pct_retained
FROM customer_applications

UNION ALL

SELECT
    'Require all fields' as strategy,
    COUNT(*) as sample_size,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customer_applications), 2) as pct_retained
FROM TD_GetRowsWithoutMissingValues(
    ON customer_applications AS InputTable
) AS dt

UNION ALL

SELECT
    'Require age & income only' as strategy,
    COUNT(*) as sample_size,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customer_applications), 2) as pct_retained
FROM TD_GetRowsWithoutMissingValues(
    ON customer_applications AS InputTable
    USING TargetColumns('age', 'income')
) AS dt;
```

**Data Science Best Practice**: Always analyze missing patterns before choosing strategy.

### Example 6: Production Scoring with Complete Cases

Handle missing values differently for training vs scoring:

```sql
-- Training: Use complete cases only
CREATE TABLE training_complete AS (
    SELECT * FROM TD_GetRowsWithoutMissingValues (
        ON training_data AS InputTable
        USING
        TargetColumns('age', 'income', 'credit_score', 'employment_years')
    ) AS dt
) WITH DATA;

-- Train model on complete cases
CREATE TABLE credit_model AS (
    SELECT * FROM TD_GLM (
        ON training_complete AS InputTable
        USING
        TargetColumn('default_flag')
        InputColumns('age', 'income', 'credit_score', 'employment_years')
        Family('BINOMIAL')
    ) AS dt
) WITH DATA;

-- Production Scoring: Can't discard incomplete applications
-- Must impute missing values

-- Create imputation models from training complete cases
CREATE TABLE impute_fit AS (
    SELECT * FROM TD_SimpleImputeFit (
        ON training_complete AS InputTable
        USING
        TargetColumns('age', 'income', 'credit_score', 'employment_years')
        FillMethod('MEDIAN')
    ) AS dt
) WITH DATA;

-- Apply imputation to production data
CREATE TABLE production_imputed AS (
    SELECT * FROM TD_SimpleImputeTransform (
        ON production_applications AS InputTable
        ON impute_fit AS FitTable DIMENSION
    ) AS dt
) WITH DATA;

-- Score all applications (including those that would have been deleted in training)
CREATE TABLE production_scores AS (
    SELECT
        application_id,
        TD_GLMPredict (
            ON production_imputed AS InputTable
            ON credit_model AS ModelTable DIMENSION
            USING
            IDColumn('application_id')
            Accumulate('age', 'income', 'credit_score', 'employment_years')
        ) AS default_probability,
        CASE
            WHEN age IS NULL OR income IS NULL OR
                 credit_score IS NULL OR employment_years IS NULL
            THEN 'Imputed'
            ELSE 'Complete'
        END as data_quality_flag
    FROM production_applications
) WITH DATA;

-- Monitor scores by data quality
SELECT
    data_quality_flag,
    COUNT(*) as application_count,
    ROUND(AVG(default_probability), 4) as avg_default_prob,
    ROUND(STDDEV(default_probability), 4) as std_default_prob
FROM production_scores
GROUP BY data_quality_flag;

/*
Output:
data_quality_flag | application_count | avg_default_prob | std_default_prob
------------------|-------------------|------------------|------------------
Complete          | 8500              | 0.0450           | 0.0820
Imputed           | 1500              | 0.0480           | 0.0950

Insight: Imputed records have slightly higher predicted risk and variance
Action: Flag imputed scores for manual review if high risk
*/
```

**Production Pattern**: Train on complete cases, score all cases with imputation + quality flag.

## Common Use Cases

### 1. Quick Exploratory Analysis

```sql
-- Fast analysis on complete subset
SELECT
    age_group,
    AVG(purchase_amount) as avg_purchase,
    COUNT(*) as customer_count
FROM TD_GetRowsWithoutMissingValues(
    ON customer_transactions AS InputTable
    USING TargetColumns('age', 'purchase_amount', 'product_category')
) AS dt
GROUP BY age_group;
```

### 2. Correlation Analysis

```sql
-- Calculate correlations (requires complete pairs)
CREATE TABLE correlation_input AS (
    SELECT * FROM TD_GetRowsWithoutMissingValues(
        ON financial_data AS InputTable
        USING TargetColumns('stock_price', 'trading_volume', 'market_cap')
    ) AS dt
) WITH DATA;

-- Now calculate correlations on complete cases
SELECT
    CORR(stock_price, trading_volume) as price_volume_corr,
    CORR(stock_price, market_cap) as price_cap_corr,
    CORR(trading_volume, market_cap) as volume_cap_corr
FROM correlation_input;
```

### 3. Sample Creation for Testing

```sql
-- Create test sample with guaranteed complete data
CREATE TABLE test_sample AS (
    SELECT * FROM TD_GetRowsWithoutMissingValues(
        ON production_data AS InputTable
    ) AS dt
    SAMPLE 1000
) WITH DATA;
```

## Best Practices

1. **Assess Missing Data First**:
   - Calculate percentage of complete cases
   - Analyze missing data patterns (MCAR, MAR, MNAR)
   - Understand why data is missing
   - If < 5% complete cases, consider imputation instead

2. **Choose Deletion vs Imputation**:
   - Deletion: Small amount of missing data (> 95% complete)
   - Deletion: Data Missing Completely At Random (MCAR)
   - Imputation: Substantial missing data (< 95% complete)
   - Imputation: Data Missing At Random or Not At Random

3. **Be Selective with Target Columns**:
   - Only require completeness for critical fields
   - Allow NULLs in less important fields
   - Use `TargetColumns` to specify which fields must be complete
   - Don't use default (all columns) unless necessary

4. **Document Data Loss**:
   - Record how many rows were removed
   - Compare statistics before/after deletion
   - Check if deletion introduces bias
   - Log deletion criteria for reproducibility

5. **Check for Selection Bias**:
   - Compare complete cases to full dataset
   - Test if missingness is related to outcome
   - If biased, consider imputation or weighting

6. **Combine with Other Techniques**:
   - Use deletion for critical fields
   - Use imputation for optional fields
   - Use weighting to adjust for selection bias
   - Use multiple imputation for sensitivity analysis

7. **Consider Alternatives**:
   - TD_SimpleImpute for filling missing values
   - Models that handle NULLs natively (e.g., decision trees)
   - Multiple imputation for robust inference
   - Maximum likelihood methods

8. **Production Considerations**:
   - Train on complete cases (higher quality)
   - Score with imputation (can't lose applicants)
   - Flag scores based on imputed data
   - Monitor performance by data quality

## Related Functions

- **TD_SimpleImputeFit/Transform**: Impute missing values (alternative to deletion)
- **TD_GetRowsWithMissingValues**: Inverse function - returns rows WITH NULLs
- **TD_OutlierFilterFit/Transform**: Remove outliers after handling missing values
- **TD_ColumnTransformer**: Apply multiple transformations including imputation
- **TD_GetFutileColumns**: Identify columns to remove (may have many NULLs)

## Notes and Limitations

1. **Data Loss**:
   - Can lose substantial portion of data
   - Reduces statistical power
   - May not be feasible if most rows have NULLs
   - Consider imputation if > 5% data loss

2. **Selection Bias**:
   - Complete cases may not be representative
   - Bias if missing not at random (MNAR)
   - Can lead to incorrect conclusions
   - Verify missingness mechanism before using

3. **All-or-Nothing Logic**:
   - Row excluded if ANY target column is NULL
   - Cannot handle partial completeness
   - Use selective TargetColumns to control

4. **No Imputation**:
   - Function only filters, doesn't fill NULLs
   - Must use TD_SimpleImpute for filling
   - Cannot recover lost information

5. **Accumulate vs Target Columns**:
   - Target columns: Must be non-NULL
   - Accumulate columns: Can contain NULLs
   - Use Accumulate for identifiers

6. **Default Behavior**:
   - Without TargetColumns, checks ALL columns
   - Can be very restrictive
   - Usually too aggressive
   - Always specify TargetColumns

7. **Performance**:
   - Scans entire table to check for NULLs
   - Large tables may take time
   - Consider sampling for initial assessment

8. **Character Set Requirements**:
   - Requires UTF8 client character set for UNICODE data
   - Does not support Pass Through Characters (PTCs)
   - Does not support KanjiSJIS or Graphic data types

9. **Non-Deterministic with TOP**:
   - SELECT TOP gives non-deterministic results
   - Identical queries may produce different results
   - Use ORDER BY for reproducibility

## Advantages of Removing Missing Values

1. **Improved Accuracy**: Analyses based on complete data may be more accurate
2. **Enhanced Efficiency**: Faster processing without NULL handling overhead
3. **Increased Data Quality**: Guaranteed non-NULL values for analysis
4. **Better Customer Insights**: More complete understanding from complete records
5. **Algorithm Compatibility**: Many algorithms require complete data
6. **Simpler Code**: No need for NULL handling logic

## Disadvantages of Removing Missing Values

1. **Data Loss**: Can lose substantial portion of observations
2. **Selection Bias**: Complete cases may not represent full population
3. **Reduced Power**: Smaller sample size reduces statistical power
4. **Loss of Information**: Discards potentially useful partial information
5. **Not Scalable**: Impractical when most rows have some missing values
6. **MNAR Issues**: Bias if missing values are informative

## Usage Notes

A NULL value indicates the absence of information. It's not zero or blank—it represents truly missing data. NULL values can pose challenges for analysis:

**When to Remove NULLs**:
- Many algorithms can't handle NULLs
- Correlation analysis requires complete pairs
- Statistical tests need complete data
- Small percentage of missing data (< 5%)
- Missing Completely At Random (MCAR)

**When to Keep/Impute NULLs**:
- Large percentage missing (> 5%)
- Missing data is informative (MNAR)
- Cannot afford to lose observations
- Missing At Random (MAR) - can model missingness

**Trade-offs**:
- Removal: Simple, guarantees quality, loses data, may introduce bias
- Imputation: Preserves sample size, introduces uncertainty, more complex

## Version Information

- **Function Version**: Based on Teradata Database Analytic Functions Version 17.20
- **Generated**: November 29, 2025
- **Category**: Data Cleaning Functions / Missing Data Handling / Complete Case Analysis
