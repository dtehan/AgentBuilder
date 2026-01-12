# TD_SimpleImputeFit

## Function Name
**TD_SimpleImputeFit**

## Description
TD_SimpleImputeFit trains a missing value imputation model that learns strategies for filling missing (NULL) values in numeric and categorical columns. This function analyzes data to calculate appropriate replacement values (mean, median, mode, or custom constants) and stores them in a model for consistent application across multiple datasets.

**Key Characteristics:**
- **Model Training**: Learns imputation strategies from historical data
- **Multiple Strategies**: Supports mean, median, mode, constant, or custom values
- **Mixed Data Types**: Handles both numeric and categorical columns
- **Group-Aware**: Can learn group-specific imputation values
- **Statistical Methods**: Calculates statistics from non-missing values only
- **Reusable Model**: Generates model table for consistent transformation

The function is part of the Fit-Transform pattern, where this function trains the imputation model (Fit) and TD_SimpleImputeTransform applies the learned strategies to clean datasets (Transform).

## When to Use

### Business Applications

**Data Preparation for Machine Learning:**
- Prepare training datasets with complete values
- Ensure consistent missing value treatment across train/test splits
- Prevent model training failures due to NULL values
- Maintain statistical properties of original data distribution

**Data Quality and Completeness:**
- Clean operational datasets for reporting and analytics
- Fill gaps in historical data due to system outages
- Handle incomplete survey responses
- Address sensor data dropout in IoT applications

**Financial Analytics:**
- Impute missing transaction amounts
- Fill gaps in market data feeds
- Handle incomplete customer financial profiles
- Address missing values in credit scoring features

**Healthcare and Life Sciences:**
- Impute missing lab results or vital signs
- Handle incomplete patient medical records
- Fill gaps in clinical trial data
- Address missing values in health surveys

**E-commerce and Retail:**
- Fill missing product attributes
- Impute customer demographic data
- Handle incomplete order information
- Address missing marketing channel data

**Manufacturing and Operations:**
- Impute missing sensor readings
- Fill gaps in production logs
- Handle incomplete quality control measurements
- Address missing equipment maintenance records

## Syntax

```sql
CREATE TABLE model_table AS (
    SELECT * FROM TD_SimpleImputeFit (
        ON { table_name | view_name | query } AS InputTable
        OUT TABLE OutputTable(model_table_name)
        USING
        InputColumns ({ 'column_name' | 'column1,column2,...' })
        [ Strategy ({ 'mean' | 'median' | 'mode' | 'literal' | 'custom' }) ]
        [ FillValue ('value') ]
        [ GroupByColumns ('column_name' [,...]) ]
        [ StatsDatabase ('database_name') ]
    ) AS dt
) WITH DATA;
```

## Required and Optional Elements

### Required Elements

**InputTable (ON ... AS InputTable):**
- Input table or view containing columns with missing values
- Can contain mix of numeric and categorical columns
- NULL values in target columns will be used to train imputation strategies
- Must contain sufficient non-NULL values for statistics calculation

**OUT TABLE OutputTable:**
- Specifies name of the imputation model table to create
- Format: `OUT TABLE OutputTable(model_table_name)`
- Model table will contain imputation strategies and replacement values
- This table is required input for TD_SimpleImputeTransform

**InputColumns:**
- Specifies which columns to analyze for missing value imputation
- Format: Single column `'column_name'` or comma-separated `'column1,column2,...'`
- Can include both numeric and categorical columns
- Must contain at least one non-NULL value for statistics calculation

### Optional Elements

**Strategy:**
- Specifies the imputation method for missing values
- **Available strategies:**
  - `'mean'`: Replace with arithmetic mean (numeric columns only)
  - `'median'`: Replace with median value (numeric columns only, default)
  - `'mode'`: Replace with most frequent value (works for all data types)
  - `'literal'`: Replace with fixed constant specified in FillValue
  - `'custom'`: Custom column-specific strategies (advanced)
- **Default**: 'median'
- **For categorical columns**: Automatically uses mode regardless of specified strategy

**FillValue:**
- Constant value to use when Strategy is 'literal'
- Must be compatible with target column data types
- Can specify different values for different columns
- Ignored when Strategy is 'mean', 'median', or 'mode'

**GroupByColumns:**
- Specifies columns to group by for group-specific imputation
- Enables different imputation values per category/segment
- Example: Different median income by state or age group
- Format: `GroupByColumns('column1', 'column2')`
- All group combinations will have separate imputation values

**StatsDatabase:**
- Database where model table will be created
- If not specified, uses current database
- Useful for centralizing ML models across projects
- Format: `StatsDatabase('database_name')`

## Input Specifications

### InputTable Schema

| Column | Data Type | Description | Required |
|--------|-----------|-------------|----------|
| Target columns | NUMERIC or VARCHAR/CHAR | Columns to learn imputation strategies for | Yes |
| Group columns | Any type | Columns defining groups for group-specific imputation | Conditional* |
| Other columns | Any type | Additional columns (not used in model training) | No |

*Required if GroupByColumns parameter is specified

### Data Requirements

- **Minimum non-NULL values**: At least one non-NULL value required per column for statistics
- **Numeric columns**: Support mean, median, mode strategies
- **Categorical columns**: Automatically use mode strategy
- **Group columns**: Each group must have at least one non-NULL value
- **Data types supported**: INTEGER, BIGINT, FLOAT, DOUBLE, DECIMAL, VARCHAR, CHAR, DATE

## Output Specifications

### Model Table Schema

The output model table contains imputation strategies and replacement values:

| Column | Data Type | Description |
|--------|-----------|-------------|
| column_name | VARCHAR | Name of column to impute |
| imputation_strategy | VARCHAR | Strategy used (mean, median, mode, literal) |
| imputation_value | VARCHAR | Calculated replacement value |
| data_type | VARCHAR | Original column data type |
| group_columns | VARCHAR | Group column names (if GroupByColumns used) |
| group_values | VARCHAR | Specific group values (if GroupByColumns used) |
| null_count | INTEGER | Number of NULL values in training data |
| total_count | INTEGER | Total number of rows analyzed |
| null_percentage | FLOAT | Percentage of NULL values |

### Statistics Output

The function also returns a summary table showing:
- Columns analyzed
- Missing value counts and percentages
- Imputation strategies selected
- Calculated replacement values per column (and per group if applicable)

## Code Examples

### Example 1: Basic Missing Value Imputation with Median Strategy
**Business Context:** E-commerce company preparing customer dataset for churn prediction model.

```sql
-- Step 1: Examine missing value patterns
SELECT
    COUNT(*) as total_customers,
    SUM(CASE WHEN age IS NULL THEN 1 ELSE 0 END) as missing_age,
    SUM(CASE WHEN income IS NULL THEN 1 ELSE 0 END) as missing_income,
    SUM(CASE WHEN account_balance IS NULL THEN 1 ELSE 0 END) as missing_balance,
    CAST(SUM(CASE WHEN age IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 as pct_missing_age
FROM customers;

-- Step 2: Train imputation model with median strategy (default)
CREATE TABLE customer_impute_model AS (
    SELECT * FROM TD_SimpleImputeFit (
        ON customers AS InputTable
        OUT TABLE OutputTable(customer_impute_model)
        USING
        InputColumns('age,income,account_balance,years_as_customer')
        Strategy('median')
    ) AS dt
) WITH DATA;

-- Step 3: Review learned imputation values
SELECT
    column_name,
    imputation_strategy,
    imputation_value,
    null_count,
    total_count,
    CAST(null_count AS FLOAT) / total_count * 100 as null_percentage
FROM customer_impute_model
ORDER BY null_percentage DESC;
```

**Sample Output:**
```
total_customers | missing_age | missing_income | missing_balance | pct_missing_age
----------------|-------------|----------------|-----------------|----------------
        125,000 |       8,750 |         12,500 |           3,125 |            7.00

column_name         | imputation_strategy | imputation_value | null_count | total_count | null_percentage
--------------------|---------------------|------------------|------------|-------------|----------------
income              | median              | 62500.00         |     12,500 |     125,000 |           10.00
age                 | median              | 38.00            |      8,750 |     125,000 |            7.00
account_balance     | median              | 4250.50          |      3,125 |     125,000 |            2.50
years_as_customer   | median              | 3.00             |      1,875 |     125,000 |            1.50
```

**Business Impact:** Trained imputation model learning median values from 125K customers, ready to consistently fill missing values across training and scoring datasets, ensuring no data loss due to missing values.

---

### Example 2: Group-Specific Imputation by Category
**Business Context:** Retail company imputing product attributes with category-specific values.

```sql
-- Step 1: Train group-specific imputation model
CREATE TABLE product_impute_model AS (
    SELECT * FROM TD_SimpleImputeFit (
        ON product_catalog AS InputTable
        OUT TABLE OutputTable(product_impute_model)
        USING
        InputColumns('unit_price,weight_kg,shelf_life_days,warranty_months')
        Strategy('median')
        GroupByColumns('product_category,brand_tier')
    ) AS dt
) WITH DATA;

-- Step 2: Review group-specific imputation values
SELECT
    group_values,
    column_name,
    imputation_value,
    null_count,
    total_count,
    CAST(null_count AS FLOAT) / total_count * 100 as null_pct
FROM product_impute_model
WHERE column_name = 'unit_price'
ORDER BY null_pct DESC;

-- Step 3: Compare imputation values across categories
SELECT
    SUBSTR(group_values, 1, 50) as category_brand,
    MAX(CASE WHEN column_name = 'unit_price' THEN CAST(imputation_value AS DECIMAL(10,2)) END) as median_price,
    MAX(CASE WHEN column_name = 'weight_kg' THEN CAST(imputation_value AS DECIMAL(10,2)) END) as median_weight,
    MAX(CASE WHEN column_name = 'shelf_life_days' THEN CAST(imputation_value AS INTEGER) END) as median_shelf_life,
    MAX(CASE WHEN column_name = 'warranty_months' THEN CAST(imputation_value AS INTEGER) END) as median_warranty
FROM product_impute_model
GROUP BY 1
ORDER BY median_price DESC;
```

**Sample Output:**
```
group_values                      | column_name | imputation_value | null_count | total_count | null_pct
----------------------------------|-------------|------------------|------------|-------------|----------
Electronics,Premium               | unit_price  | 899.99           |        234 |       5,678 |     4.12
Electronics,Standard              | unit_price  | 249.99           |        189 |      12,345 |     1.53
Home & Garden,Premium             | unit_price  | 179.95           |        156 |       3,456 |     4.51
Food,Standard                     | unit_price  | 12.49            |         89 |      23,456 |     0.38

category_brand                     | median_price | median_weight | median_shelf_life | median_warranty
-----------------------------------|--------------|---------------|-------------------|----------------
Electronics,Premium                |       899.99 |          1.25 |               730 |              24
Electronics,Standard               |       249.99 |          0.85 |               365 |              12
Home & Garden,Premium              |       179.95 |          3.50 |              NULL |               6
Food,Standard                      |        12.49 |          0.45 |                30 |            NULL
```

**Business Impact:** Created category-specific imputation model with different median values per product category and brand tier, ensuring missing prices reflect appropriate market segments (e.g., premium electronics at $900 vs. standard food at $12).

---

### Example 3: Mixed Strategies for Different Column Types
**Business Context:** Healthcare system handling missing patient data with appropriate methods per field.

```sql
-- Step 1: Analyze missing patterns across different data types
SELECT
    'Numeric' as data_category,
    SUM(CASE WHEN heart_rate IS NULL THEN 1 ELSE 0 END) as hr_missing,
    SUM(CASE WHEN blood_pressure_sys IS NULL THEN 1 ELSE 0 END) as bp_missing,
    SUM(CASE WHEN weight_kg IS NULL THEN 1 ELSE 0 END) as weight_missing,
    COUNT(*) as total_records
FROM patient_vitals
UNION ALL
SELECT
    'Categorical' as data_category,
    SUM(CASE WHEN blood_type IS NULL THEN 1 ELSE 0 END) as blood_type_missing,
    SUM(CASE WHEN smoking_status IS NULL THEN 1 ELSE 0 END) as smoking_missing,
    SUM(CASE WHEN insurance_type IS NULL THEN 1 ELSE 0 END) as insurance_missing,
    COUNT(*) as total_records
FROM patient_vitals;

-- Step 2: Train imputation model (numeric: median, categorical: mode)
CREATE TABLE patient_impute_model AS (
    SELECT * FROM TD_SimpleImputeFit (
        ON patient_vitals AS InputTable
        OUT TABLE OutputTable(patient_impute_model)
        USING
        InputColumns('heart_rate,blood_pressure_sys,blood_pressure_dia,weight_kg,height_cm,blood_type,smoking_status,insurance_type')
        Strategy('median')  -- Will use mode for categorical columns automatically
        GroupByColumns('age_group,gender')
    ) AS dt
) WITH DATA;

-- Step 3: Review imputation strategies by data type
SELECT
    data_type,
    column_name,
    imputation_strategy,
    imputation_value,
    null_count,
    total_count
FROM patient_impute_model
WHERE group_values = 'age_group:45-54,gender:F'
ORDER BY data_type, column_name;

-- Step 4: Validate mode values for categorical fields
SELECT
    column_name,
    imputation_value as most_common_value,
    null_count,
    CAST(null_count AS FLOAT) / total_count * 100 as null_pct
FROM patient_impute_model
WHERE column_name IN ('blood_type', 'smoking_status', 'insurance_type')
    AND group_values LIKE '%age_group:45-54%'
ORDER BY null_pct DESC;
```

**Sample Output:**
```
data_category | hr_missing | bp_missing | weight_missing | total_records
--------------|------------|------------|----------------|---------------
Numeric       |      1,234 |      2,345 |          3,456 |        50,000
Categorical   |        234 |      5,678 |          1,234 |        50,000

data_type  | column_name         | imputation_strategy | imputation_value | null_count | total_count
-----------|---------------------|---------------------|------------------|------------|------------
DECIMAL    | blood_pressure_dia  | median              | 78.00            |      1,123 |       6,234
DECIMAL    | blood_pressure_sys  | median              | 125.00           |      1,098 |       6,234
DECIMAL    | heart_rate          | median              | 72.00            |        678 |       6,234
DECIMAL    | height_cm           | median              | 165.00           |        234 |       6,234
DECIMAL    | weight_kg           | median              | 68.50            |        456 |       6,234
VARCHAR    | blood_type          | mode                | O+               |         34 |       6,234
VARCHAR    | insurance_type      | mode                | PRIVATE          |        178 |       6,234
VARCHAR    | smoking_status      | mode                | NEVER            |        892 |       6,234

column_name      | most_common_value | null_count | null_pct
-----------------|-------------------|------------|----------
smoking_status   | NEVER             |        892 |    14.31
insurance_type   | PRIVATE           |        178 |     2.86
blood_type       | O+                |         34 |     0.55
```

**Business Impact:** Created comprehensive imputation model handling both numeric vitals (using median) and categorical attributes (using mode) with age/gender-specific values, ensuring clinically appropriate replacements (e.g., 72 bpm heart rate for females age 45-54).

---

### Example 4: Literal Value Imputation for Business Rules
**Business Context:** Financial institution using business-defined defaults for missing credit application fields.

```sql
-- Step 1: Define business rules for missing value defaults
-- Missing credit score → 650 (industry average for new applicants)
-- Missing debt_to_income → 0.35 (conservative assumption)
-- Missing employment_years → 0 (assume entry-level)

CREATE TABLE credit_impute_model AS (
    SELECT * FROM TD_SimpleImputeFit (
        ON credit_applications AS InputTable
        OUT TABLE OutputTable(credit_impute_model)
        USING
        InputColumns('credit_score,debt_to_income_ratio,employment_years,num_credit_accounts')
        Strategy('literal')
        FillValue('credit_score:650,debt_to_income_ratio:0.35,employment_years:0,num_credit_accounts:1')
    ) AS dt
) WITH DATA;

-- Step 2: Review business-defined imputation values
SELECT
    column_name,
    imputation_strategy,
    imputation_value,
    null_count,
    total_count,
    CAST(null_count AS FLOAT) / total_count * 100 as null_pct,
    -- Compare to actual median
    (SELECT MEDIAN(credit_score) FROM credit_applications WHERE credit_score IS NOT NULL) as actual_median_score
FROM credit_impute_model
WHERE column_name = 'credit_score';

-- Step 3: Compare literal values to statistical alternatives
SELECT
    ca.column_name,
    ca.imputation_value as literal_value,
    CASE ca.column_name
        WHEN 'credit_score' THEN CAST(AVG(apps.credit_score) AS VARCHAR(50))
        WHEN 'debt_to_income_ratio' THEN CAST(AVG(apps.debt_to_income_ratio) AS VARCHAR(50))
        WHEN 'employment_years' THEN CAST(AVG(apps.employment_years) AS VARCHAR(50))
        WHEN 'num_credit_accounts' THEN CAST(AVG(apps.num_credit_accounts) AS VARCHAR(50))
    END as actual_mean,
    CASE ca.column_name
        WHEN 'credit_score' THEN CAST(MEDIAN(apps.credit_score) AS VARCHAR(50))
        WHEN 'debt_to_income_ratio' THEN CAST(MEDIAN(apps.debt_to_income_ratio) AS VARCHAR(50))
        WHEN 'employment_years' THEN CAST(MEDIAN(apps.employment_years) AS VARCHAR(50))
        WHEN 'num_credit_accounts' THEN CAST(MEDIAN(apps.num_credit_accounts) AS VARCHAR(50))
    END as actual_median
FROM credit_impute_model ca
CROSS JOIN credit_applications apps
WHERE ca.imputation_strategy = 'literal'
GROUP BY ca.column_name, ca.imputation_value
ORDER BY ca.column_name;
```

**Sample Output:**
```
column_name            | imputation_strategy | imputation_value | null_count | total_count | null_pct | actual_median_score
-----------------------|---------------------|------------------|------------|-------------|----------|--------------------
credit_score           | literal             | 650              |      2,345 |      25,000 |     9.38 |              712.00

column_name            | literal_value | actual_mean | actual_median
-----------------------|---------------|-------------|---------------
credit_score           | 650           | 698.45      | 712.00
debt_to_income_ratio   | 0.35          | 0.28        | 0.26
employment_years       | 0             | 8.50        | 6.00
num_credit_accounts    | 1             | 5.20        | 4.00
```

**Business Impact:** Applied conservative business rule defaults for missing credit application data (650 credit score vs. actual median of 712), ensuring risk-averse assumptions that protect against default risk while processing incomplete applications.

---

### Example 5: Production ML Pipeline with Mean Strategy
**Business Context:** Manufacturing company preparing sensor data for predictive maintenance model.

```sql
-- Step 1: Profile missing data across sensor types
SELECT
    sensor_type,
    COUNT(*) as total_readings,
    SUM(CASE WHEN temperature IS NULL THEN 1 ELSE 0 END) as missing_temp,
    SUM(CASE WHEN pressure IS NULL THEN 1 ELSE 0 END) as missing_pressure,
    SUM(CASE WHEN vibration IS NULL THEN 1 ELSE 0 END) as missing_vibration,
    SUM(CASE WHEN rpm IS NULL THEN 1 ELSE 0 END) as missing_rpm,
    CAST(SUM(CASE WHEN temperature IS NULL OR pressure IS NULL OR vibration IS NULL OR rpm IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 as pct_incomplete
FROM sensor_readings_historical
GROUP BY sensor_type
ORDER BY pct_incomplete DESC;

-- Step 2: Train imputation model with mean strategy (sensor-type-specific)
CREATE TABLE sensor_impute_model AS (
    SELECT * FROM TD_SimpleImputeFit (
        ON sensor_readings_historical AS InputTable
        OUT TABLE OutputTable(sensor_impute_model)
        USING
        InputColumns('temperature,pressure,vibration,rpm,power_consumption')
        Strategy('mean')
        GroupByColumns('sensor_type,equipment_id')
        StatsDatabase('ml_models_db')
    ) AS dt
) WITH DATA;

-- Step 3: Review mean values by sensor type
SELECT
    SUBSTR(group_values, 1, 40) as sensor_equipment,
    MAX(CASE WHEN column_name = 'temperature' THEN CAST(imputation_value AS DECIMAL(10,2)) END) as mean_temp,
    MAX(CASE WHEN column_name = 'pressure' THEN CAST(imputation_value AS DECIMAL(10,2)) END) as mean_pressure,
    MAX(CASE WHEN column_name = 'vibration' THEN CAST(imputation_value AS DECIMAL(10,2)) END) as mean_vibration,
    MAX(CASE WHEN column_name = 'rpm' THEN CAST(imputation_value AS DECIMAL(10,2)) END) as mean_rpm,
    MAX(null_count) as max_missing_count
FROM ml_models_db.sensor_impute_model
GROUP BY 1
ORDER BY max_missing_count DESC;

-- Step 4: Validate imputation values against operational ranges
SELECT
    sim.sensor_type,
    sim.column_name,
    CAST(sim.imputation_value AS DECIMAL(10,2)) as learned_mean,
    CAST(AVG(sr.reading_value) AS DECIMAL(10,2)) as actual_mean,
    specs.min_operational_value,
    specs.max_operational_value,
    CASE
        WHEN CAST(sim.imputation_value AS DECIMAL(10,2)) BETWEEN specs.min_operational_value AND specs.max_operational_value
        THEN 'VALID'
        ELSE 'OUT_OF_RANGE'
    END as validation_status
FROM (
    SELECT
        SUBSTR(group_values, 1, POSITION(',' IN group_values) - 1) as sensor_type,
        column_name,
        imputation_value
    FROM ml_models_db.sensor_impute_model
) sim
INNER JOIN sensor_operational_specs specs
    ON sim.sensor_type = specs.sensor_type
    AND sim.column_name = specs.metric_name
LEFT JOIN (
    SELECT sensor_type, 'temperature' as metric, AVG(temperature) as reading_value FROM sensor_readings_historical GROUP BY 1
    UNION ALL
    SELECT sensor_type, 'pressure', AVG(pressure) FROM sensor_readings_historical GROUP BY 1
    UNION ALL
    SELECT sensor_type, 'vibration', AVG(vibration) FROM sensor_readings_historical GROUP BY 1
    UNION ALL
    SELECT sensor_type, 'rpm', AVG(rpm) FROM sensor_readings_historical GROUP BY 1
) sr ON sim.sensor_type = sr.sensor_type AND sim.column_name = sr.metric
ORDER BY validation_status, sim.sensor_type, sim.column_name;
```

**Sample Output:**
```
sensor_type  | total_readings | missing_temp | missing_pressure | missing_vibration | missing_rpm | pct_incomplete
-------------|----------------|--------------|------------------|-------------------|-------------|---------------
TYPE_C       |        12,345  |          234 |              456 |               123 |         345 |          9.45
TYPE_A       |        45,678  |          345 |              234 |               456 |         123 |          2.53
TYPE_B       |        23,456  |          123 |              345 |               234 |         456 |          4.98

sensor_equipment              | mean_temp | mean_pressure | mean_vibration | mean_rpm  | max_missing_count
------------------------------|-----------|---------------|----------------|-----------|-------------------
TYPE_C,EQUIP_0045             |     85.23 |        125.67 |           2.34 |   1850.45 |               456
TYPE_A,EQUIP_0012             |     72.45 |        110.23 |           1.89 |   2200.12 |               456
TYPE_B,EQUIP_0089             |     68.90 |         98.45 |           1.56 |   1950.78 |               345

sensor_type | column_name  | learned_mean | actual_mean | min_operational_value | max_operational_value | validation_status
------------|--------------|--------------|-------------|----------------------|----------------------|------------------
TYPE_A      | pressure     |       110.23 |      110.25 |                 90.00 |               130.00 | VALID
TYPE_A      | rpm          |      2200.12 |     2199.89 |               1800.00 |              2400.00 | VALID
TYPE_A      | temperature  |        72.45 |       72.48 |                 60.00 |                90.00 | VALID
TYPE_A      | vibration    |         1.89 |        1.88 |                  1.00 |                 3.00 | VALID
TYPE_C      | temperature  |        85.23 |       85.20 |                 60.00 |                82.00 | OUT_OF_RANGE
```

**Business Impact:** Trained equipment-specific imputation model using mean values from historical sensor data, validated that learned means fall within operational specifications (flagged TYPE_C temperature at 85.2°C exceeding 82°C max), and prepared model for consistent missing value handling in production predictive maintenance pipeline processing 80K+ daily sensor readings.

---

### Example 6: Mode Strategy for Survey Data with Categorical Fields
**Business Context:** Market research company handling missing responses in customer satisfaction survey.

```sql
-- Step 1: Analyze survey completion rates
SELECT
    COUNT(*) as total_responses,
    SUM(CASE WHEN satisfaction_rating IS NULL THEN 1 ELSE 0 END) as missing_satisfaction,
    SUM(CASE WHEN product_category IS NULL THEN 1 ELSE 0 END) as missing_category,
    SUM(CASE WHEN purchase_likelihood IS NULL THEN 1 ELSE 0 END) as missing_likelihood,
    SUM(CASE WHEN age_range IS NULL THEN 1 ELSE 0 END) as missing_age,
    SUM(CASE WHEN income_bracket IS NULL THEN 1 ELSE 0 END) as missing_income,
    CAST(SUM(CASE WHEN satisfaction_rating IS NOT NULL AND product_category IS NOT NULL AND purchase_likelihood IS NOT NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 as pct_complete
FROM customer_survey_responses;

-- Step 2: Train mode-based imputation for categorical survey fields
CREATE TABLE survey_impute_model AS (
    SELECT * FROM TD_SimpleImputeFit (
        ON customer_survey_responses AS InputTable
        OUT TABLE OutputTable(survey_impute_model)
        USING
        InputColumns('satisfaction_rating,product_category,purchase_likelihood,age_range,income_bracket,preferred_channel')
        Strategy('mode')  -- Most frequent value for each field
        GroupByColumns('customer_segment,survey_month')
    ) AS dt
) WITH DATA;

-- Step 3: Review most frequent values by customer segment
SELECT
    SUBSTR(group_values, 1, 50) as segment_month,
    MAX(CASE WHEN column_name = 'satisfaction_rating' THEN imputation_value END) as mode_satisfaction,
    MAX(CASE WHEN column_name = 'purchase_likelihood' THEN imputation_value END) as mode_likelihood,
    MAX(CASE WHEN column_name = 'preferred_channel' THEN imputation_value END) as mode_channel,
    MAX(CASE WHEN column_name = 'satisfaction_rating' THEN null_count END) as missing_satisfaction_count
FROM survey_impute_model
GROUP BY 1
ORDER BY missing_satisfaction_count DESC;

-- Step 4: Compare mode values across customer segments
SELECT
    customer_segment,
    MAX(CASE WHEN column_name = 'satisfaction_rating' THEN imputation_value END) as most_common_rating,
    MAX(CASE WHEN column_name = 'satisfaction_rating' THEN null_count END) as rating_missing_count,
    MAX(CASE WHEN column_name = 'satisfaction_rating' THEN total_count END) as total_responses,
    CAST(MAX(CASE WHEN column_name = 'satisfaction_rating' THEN null_count END) AS FLOAT) /
         MAX(CASE WHEN column_name = 'satisfaction_rating' THEN total_count END) * 100 as pct_missing
FROM survey_impute_model
CROSS JOIN (SELECT DISTINCT SUBSTR(group_values, 1, POSITION(',' IN group_values)-1) as customer_segment FROM survey_impute_model) segments
WHERE group_values LIKE customer_segment || '%'
GROUP BY customer_segment
ORDER BY pct_missing DESC;
```

**Sample Output:**
```
total_responses | missing_satisfaction | missing_category | missing_likelihood | missing_age | missing_income | pct_complete
----------------|----------------------|------------------|--------------------|-----------|--------------|--------------
         45,678 |                3,456 |            2,345 |              4,567 |       1,234 |         5,678 |        72.34

segment_month                           | mode_satisfaction | mode_likelihood | mode_channel | missing_satisfaction_count
----------------------------------------|-------------------|-----------------|--------------|---------------------------
Premium,2024-11                         | Satisfied         | Very Likely     | Online       |                       234
Standard,2024-11                        | Neutral           | Likely          | In-Store     |                       567
Budget,2024-11                          | Satisfied         | Neutral         | Online       |                       123
Premium,2024-10                         | Very Satisfied    | Very Likely     | Online       |                       189

customer_segment | most_common_rating | rating_missing_count | total_responses | pct_missing
-----------------|--------------------|--------------------|-----------------|------------
Budget           | Satisfied          |                1,234 |          15,678 |        7.87
Standard         | Neutral            |                1,456 |          20,456 |        7.12
Premium          | Very Satisfied     |                  766 |           9,544 |        8.03
```

**Business Impact:** Created segment-specific mode-based imputation model revealing different most-common responses by customer segment (Premium customers: "Very Satisfied", Standard: "Neutral"), enabling completion of 45K+ surveys with 7-8% missing values while preserving segment-specific response patterns for accurate market research analysis.

---

## Common Use Cases

### By Industry

**Financial Services:**
- Credit application missing data imputation
- Trading data gap filling
- Customer demographic completion
- Risk scoring feature preparation
- Fraud detection dataset preparation

**Healthcare:**
- Patient vital signs gap filling
- Lab result imputation
- Medical record completion
- Clinical trial missing data handling
- Health survey response completion

**Retail & E-commerce:**
- Product attribute completion
- Customer profile enrichment
- Order data gap filling
- Marketing attribution completion
- Inventory data preparation

**Manufacturing:**
- Sensor data gap filling
- Quality control measurement imputation
- Production log completion
- Equipment maintenance record filling
- Supply chain data preparation

**Telecommunications:**
- Network metrics gap filling
- Customer usage data completion
- Service quality measurement imputation
- Billing data preparation
- Churn prediction feature engineering

**Market Research:**
- Survey response completion
- Panel data imputation
- Customer feedback enrichment
- A/B test data preparation
- Sentiment analysis data cleaning

### By Analytics Task

**Machine Learning:**
- Training data preparation
- Feature engineering
- Missing value handling
- Model input validation
- Cross-validation dataset preparation

**Data Quality:**
- Completeness improvement
- Gap filling in historical data
- Operational data cleaning
- Reporting dataset preparation
- Data governance compliance

**Statistical Analysis:**
- Time series gap filling
- Survey data completion
- Experimental data preparation
- Hypothesis testing datasets
- Regression analysis preparation

**Business Intelligence:**
- Dashboard data preparation
- KPI calculation inputs
- Executive report preparation
- Trend analysis datasets
- Performance metric completion

## Best Practices

### Strategy Selection

**1. Choose Appropriate Strategy per Column Type:**

**Numeric Columns:**
- **Mean**: Best for normally distributed data, sensitive to outliers
- **Median**: Robust to outliers, works with skewed distributions (RECOMMENDED)
- **Mode**: Use for discrete numeric values (e.g., product quantities 1, 2, 3)

**Categorical Columns:**
- **Mode**: Always use mode (most frequent value) for text/categorical fields
- Automatically applied regardless of specified strategy

**Business-Driven Columns:**
- **Literal**: Use when business rules dictate specific default values
- Example: Missing credit score = 650 (industry average), not statistical median

**2. Evaluate Missing Data Patterns:**
```sql
-- Analyze missingness correlation
SELECT
    CASE WHEN col1 IS NULL AND col2 IS NULL THEN 'Both Missing'
         WHEN col1 IS NULL THEN 'Col1 Missing Only'
         WHEN col2 IS NULL THEN 'Col2 Missing Only'
         ELSE 'Complete'
    END as missing_pattern,
    COUNT(*) as record_count,
    CAST(COUNT(*) AS FLOAT) / (SELECT COUNT(*) FROM data_table) * 100 as percentage
FROM data_table
GROUP BY 1
ORDER BY record_count DESC;
```

**3. Group-Based vs. Global Imputation:**
- Use **global** (no GroupByColumns) when data is homogeneous
- Use **grouped** (with GroupByColumns) when segments have different characteristics
- Examples of good grouping: customer segments, product categories, geographic regions, time periods

**4. Validate Imputation Values:**
- Check that learned values are within expected ranges
- Compare to business knowledge and domain expertise
- Review outlier impact on mean-based imputation
- Validate mode values represent majority appropriately

### Data Quality and Validation

**1. Pre-Training Analysis:**
```sql
-- Comprehensive missing data profiling
SELECT
    column_name,
    COUNT(*) as total_rows,
    SUM(CASE WHEN column_value IS NULL THEN 1 ELSE 0 END) as null_count,
    CAST(SUM(CASE WHEN column_value IS NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 as null_percentage,
    MIN(column_value) as min_value,
    MAX(column_value) as max_value,
    AVG(column_value) as mean_value,
    MEDIAN(column_value) as median_value
FROM data_table;
```

**2. Post-Training Validation:**
- Review all learned imputation values for plausibility
- Check null counts and percentages match expectations
- Verify group-specific values show expected variation
- Document imputation rationale for audit purposes

**3. Handle High Missingness:**
- Columns with >50% missing may need special handling
- Consider if column should be excluded from analysis
- Evaluate if pattern of missingness is informative (MNAR - Missing Not At Random)
- Document decision to impute vs. exclude

**4. Model Versioning:**
```sql
-- Add metadata to model table
ALTER TABLE impute_model ADD model_version VARCHAR(20);
ALTER TABLE impute_model ADD training_date DATE;
ALTER TABLE impute_model ADD source_table VARCHAR(100);
UPDATE impute_model
SET model_version = 'v1.2',
    training_date = CURRENT_DATE,
    source_table = 'customer_data_2024';
```

### Production Implementation

**1. Separate Training and Inference:**
- Train models on historical "clean" periods
- Apply to new data with Transform function
- Maintain model versioning and lineage
- Schedule periodic retraining

**2. Monitor Imputation Rates:**
```sql
-- Track imputation statistics over time
CREATE TABLE imputation_monitoring AS
SELECT
    CURRENT_DATE as process_date,
    'customer_data' as dataset_name,
    COUNT(*) as total_records,
    SUM(CASE WHEN age_imputed = 1 THEN 1 ELSE 0 END) as age_imputations,
    SUM(CASE WHEN income_imputed = 1 THEN 1 ELSE 0 END) as income_imputations,
    AVG(imputation_count_per_record) as avg_imputations_per_record
FROM transformed_data
WITH DATA;
```

**3. Handle New Groups:**
- Plan for groups not seen during training
- Consider default/fallback imputation values
- Log warnings for unseen group combinations
- Periodically retrain with updated data

**4. Document Imputation Decisions:**
- Record strategy choice rationale
- Document group definitions
- Maintain change log for model updates
- Include in data dictionary and documentation

### Performance Optimization

**1. Minimize Model Training Frequency:**
- Train on representative sample if data is very large (>100M rows)
- Use time-windowed data (e.g., last 12 months)
- Schedule retraining based on data drift monitoring
- Balance freshness vs. computational cost

**2. Optimize Group Definitions:**
- Avoid too many groups (explosion of group combinations)
- Ensure each group has sufficient data (minimum 30-50 records)
- Consider hierarchical grouping (broader groups for rare combinations)

**3. Column Selection:**
- Only include columns that actually need imputation
- Exclude columns with <1% missing (negligible benefit)
- Prioritize columns critical for downstream analytics

**4. Database and Storage:**
- Use StatsDatabase parameter to centralize models
- Implement retention policies for old models
- Compress large model tables
- Index model tables on frequently queried columns

## Related Functions

### Imputation Workflow
- **TD_SimpleImputeFit**: Train missing value imputation model (this function)
- **TD_SimpleImputeTransform**: Apply trained imputation model to data

### Data Cleaning Functions
- **TD_OutlierFilterFit / TD_OutlierFilterTransform**: Handle outliers before imputation
- **PACK / UNPACK**: Data transformation and structuring
- **TD_StringSimilarity**: Handle data entry variations

### Data Exploration
- **TD_UnivariateStatistics**: Calculate statistics including missing value counts
- **TD_ColumnSummary**: Summarize column-level statistics
- **TD_Histogram**: Visualize distributions before/after imputation

### Feature Engineering
- **TD_ScaleFit / TD_ScaleTransform**: Normalize features after imputation
- **TD_BinCodeFit / TD_BinCodeTransform**: Bin continuous values
- **TD_OneHotEncodingFit**: Encode categorical values

## Notes and Limitations

### Important Considerations

**1. Missing Data Assumptions:**
- **MCAR (Missing Completely At Random)**: Safest assumption for imputation
- **MAR (Missing At Random)**: Group-based imputation can help
- **MNAR (Missing Not At Random)**: Imputation may introduce bias, consider alternative approaches
- Always evaluate missingness patterns before imputation

**2. Strategy Limitations:**
- **Mean**: Sensitive to outliers, may not represent typical value in skewed distributions
- **Median**: More robust but ignores data distribution shape
- **Mode**: May not be unique (multiple values with same frequency)
- **Literal**: Requires domain knowledge and business rules

**3. Data Requirements:**
- Minimum 1 non-NULL value per column per group required
- Groups with all NULL values will cause errors
- Very sparse data (>90% missing) may not benefit from imputation
- Categorical columns automatically use mode regardless of strategy

**4. Model Retraining:**
- Required when data distribution shifts significantly
- Needed when new groups or categories appear
- Recommended periodically (e.g., quarterly for dynamic datasets)
- Consider seasonal patterns for time-dependent data

**5. Imputation Impact:**
- Reduces variance in imputed columns
- May introduce bias if missingness is not random
- Can affect correlation structures between variables
- Should document which values were imputed for transparency

**6. Performance Considerations:**
- Large numbers of groups increase model size and training time
- Model table size grows with number of columns × number of groups
- Training on very large datasets (>100M rows) may require sampling
- Consider computational cost vs. benefit for columns with minimal missingness

### Technical Constraints

**1. Data Type Support:**
- Numeric: INTEGER, BIGINT, SMALLINT, FLOAT, DOUBLE, DECIMAL, NUMERIC
- Categorical: VARCHAR, CHAR, DATE
- Not supported: BLOB, CLOB, complex types

**2. Strategy-Data Type Compatibility:**
| Strategy | Numeric Columns | Categorical Columns |
|----------|----------------|---------------------|
| mean     | ✓ Supported    | ✗ Not applicable    |
| median   | ✓ Supported    | ✗ Not applicable    |
| mode     | ✓ Supported    | ✓ Supported         |
| literal  | ✓ Supported    | ✓ Supported         |

**3. Null Handling:**
- Columns with 100% NULL values will error
- Groups with 100% NULL values will error
- At least 1 non-NULL value required for statistics calculation

**4. Group Considerations:**
- Each group combination must have sufficient data
- Empty groups (no records) will be absent from model
- New groups at transform time require fallback strategy

### Best Practices Summary

1. **Choose median strategy** for numeric columns as default (robust to outliers)
2. **Use mode strategy** for categorical/text columns (automatically applied)
3. **Apply grouping** when segments have different characteristics
4. **Validate learned values** against domain knowledge and business rules
5. **Document strategy choices** and rationale for audit purposes
6. **Monitor imputation rates** over time to detect data quality issues
7. **Handle outliers first** before imputation to avoid biased statistics
8. **Retrain periodically** when data distribution shifts significantly
9. **Test on holdout data** before production deployment
10. **Version control models** with metadata for reproducibility

## Version Information

- **Teradata Vantage Version**: 17.20
- **Function Category**: Machine Learning - Data Preparation
- **Documentation Generated**: November 2024
- **Model Type**: Fit-Transform Pattern (requires TD_SimpleImputeTransform for application)
