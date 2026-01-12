# TD_SimpleImputeTransform

## Function Name
**TD_SimpleImputeTransform**

## Description
TD_SimpleImputeTransform applies a trained missing value imputation model (created by TD_SimpleImputeFit) to fill NULL values in datasets. This function uses the learned imputation strategies (mean, median, mode, or literal values) to consistently replace missing values across training, testing, and production datasets.

**Key Characteristics:**
- **Model-Based Application**: Uses pre-trained model from TD_SimpleImputeFit
- **Consistent Treatment**: Applies same imputation rules across all datasets
- **Automatic Type Handling**: Correctly imputes numeric and categorical columns
- **Group-Aware**: Maintains group-specific imputation values when model was trained by groups
- **Multiple Columns**: Can process multiple columns simultaneously
- **Production-Ready**: Designed for ETL pipelines and ML workflows

The function preserves the imputation strategies and replacement values defined during model training, ensuring consistent data completeness treatment across development, testing, and production environments.

## When to Use

### Business Applications

**Machine Learning Pipelines:**
- Clean scoring datasets using same rules as training data
- Prepare consistent train/test/validation splits
- Handle missing values in production model inputs
- Ensure feature completeness for model predictions
- Prevent model failures due to NULL values

**Data Quality Operations:**
- Complete operational datasets for reporting
- Fill gaps in historical data reconstruction
- Handle incomplete data imports and integrations
- Maintain consistent data quality standards
- Automate missing value handling in ETL workflows

**Financial Analytics:**
- Complete transaction records for analysis
- Fill gaps in market data feeds
- Handle incomplete customer financial profiles
- Prepare credit scoring datasets
- Clean trading data for risk models

**Healthcare and Life Sciences:**
- Complete patient records for clinical analysis
- Fill gaps in vital signs monitoring
- Handle incomplete lab results
- Prepare datasets for clinical research
- Clean medical imaging metadata

**E-commerce and Retail:**
- Complete product catalogs for merchandising
- Fill missing customer demographics
- Handle incomplete order information
- Prepare recommendation system inputs
- Clean marketing attribution data

**Manufacturing and IoT:**
- Fill sensor data gaps for monitoring
- Complete production logs for analysis
- Handle equipment telemetry dropouts
- Prepare predictive maintenance datasets
- Clean quality control measurements

## Syntax

```sql
SELECT * FROM TD_SimpleImputeTransform (
    ON { table_name | view_name | query } AS InputTable PARTITION BY { ANY | column_name [,...] }
    ON { table_name | view_name | query } AS FitTable DIMENSION
    USING
    [ Accumulate ('column_name' [,...]) ]
    [ OutputImputationFlag ({ 'true' | 'false' }) ]
) AS alias;
```

## Required and Optional Elements

### Required Elements

**InputTable (ON ... AS InputTable):**
- Input table or view containing data with missing values
- Must contain all columns referenced in FitTable
- Can include additional columns (accumulated with Accumulate clause)
- **PARTITION BY specification:**
  - `PARTITION BY ANY`: Distributes rows randomly for parallel processing (use when model trained without groups)
  - `PARTITION BY column_name`: Partitions by group columns (must match columns used in TD_SimpleImputeFit training)

**FitTable (ON ... AS FitTable DIMENSION):**
- Pre-trained imputation model from TD_SimpleImputeFit
- Contains imputation strategies, replacement values, and group definitions
- Broadcast to all AMPs using DIMENSION keyword
- Must be compatible with InputTable column types

### Optional Elements

**Accumulate:**
- Specifies columns to copy from InputTable to output without modification
- Useful for preserving identifiers, timestamps, and metadata
- Format: `Accumulate('column1', 'column2', ...)`
- **Common columns to accumulate:**
  - Primary keys and identifiers
  - Date/timestamp columns
  - Columns not needing imputation
  - Descriptive text fields

**OutputImputationFlag:**
- Controls whether to output indicator columns showing which values were imputed
- Format: `OutputImputationFlag('true')` or `OutputImputationFlag('false')`
- **Default**: 'false'
- **When 'true'**: Creates additional columns named `is_imputed_[column_name]` (1=imputed, 0=original)
- **Use cases**: Audit trails, model features, data quality tracking

## Input Specifications

### InputTable Schema

| Column | Data Type | Description | Required |
|--------|-----------|-------------|----------|
| Target columns | Same as FitTable | Columns to impute (must match FitTable columns) | Yes |
| Group columns | Same as FitTable | Columns used for group-specific imputation (if used in Fit) | Conditional* |
| Additional columns | Any type | Other columns to accumulate in output | No |

*Required if model was trained with group-specific imputation (GroupByColumns in Fit)

### FitTable Schema

Generated by TD_SimpleImputeFit, containing:
- Column names and imputation strategies
- Replacement values (mean, median, mode, or literal)
- Group identifiers (if group-specific model)
- Data types and metadata

**Important:** FitTable structure is determined by TD_SimpleImputeFit training parameters.

## Output Specifications

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| [Original columns] | Same as input | Target columns with NULL values replaced according to model |
| [Accumulated columns] | Same as input | Columns specified in Accumulate clause |
| is_imputed_[column]* | INTEGER | Flag (1=imputed, 0=original) for each target column |

*Only included when `OutputImputationFlag('true')` is specified

### Imputation Behavior

**Numeric Columns:**
- Mean strategy: NULL → calculated mean from training data
- Median strategy: NULL → calculated median from training data
- Mode strategy: NULL → most frequent value from training data
- Literal strategy: NULL → specified constant value

**Categorical Columns:**
- Mode strategy: NULL → most frequent value from training data
- Literal strategy: NULL → specified constant value

**Group-Specific:**
- When model trained with groups: Uses group-specific replacement value
- For new groups not in model: Error or requires fallback handling

## Code Examples

### Example 1: Basic Missing Value Imputation for ML Pipeline
**Business Context:** E-commerce company applying imputation model to new customers for churn prediction.

```sql
-- Step 1: Apply imputation model to new customer data
CREATE TABLE customers_complete AS (
    SELECT * FROM TD_SimpleImputeTransform (
        ON new_customers AS InputTable PARTITION BY ANY
        ON customer_impute_model AS FitTable DIMENSION
        USING
        Accumulate('customer_id', 'signup_date', 'account_status')
        OutputImputationFlag('true')
    ) AS dt
) WITH DATA;

-- Step 2: Review imputation statistics
SELECT
    COUNT(*) as total_customers,
    SUM(is_imputed_age) as age_imputed,
    SUM(is_imputed_income) as income_imputed,
    SUM(is_imputed_account_balance) as balance_imputed,
    SUM(is_imputed_years_as_customer) as years_imputed,
    CAST(SUM(is_imputed_age + is_imputed_income + is_imputed_account_balance + is_imputed_years_as_customer) AS FLOAT) /
         (COUNT(*) * 4) * 100 as avg_imputation_rate
FROM customers_complete;

-- Step 3: Compare before and after imputation
SELECT
    'BEFORE' as stage,
    COUNT(*) as total_records,
    COUNT(age) as age_non_null,
    COUNT(income) as income_non_null,
    AVG(income) as avg_income
FROM new_customers
UNION ALL
SELECT
    'AFTER' as stage,
    COUNT(*) as total_records,
    COUNT(age) as age_non_null,
    COUNT(income) as income_non_null,
    AVG(income) as avg_income
FROM customers_complete;

-- Step 4: Identify heavily imputed records for review
SELECT
    customer_id,
    age,
    income,
    account_balance,
    years_as_customer,
    is_imputed_age + is_imputed_income + is_imputed_account_balance + is_imputed_years_as_customer as total_imputations,
    CASE
        WHEN is_imputed_age = 1 THEN 'AGE ' ELSE ''
    END ||
    CASE
        WHEN is_imputed_income = 1 THEN 'INCOME ' ELSE ''
    END ||
    CASE
        WHEN is_imputed_account_balance = 1 THEN 'BALANCE ' ELSE ''
    END ||
    CASE
        WHEN is_imputed_years_as_customer = 1 THEN 'YEARS' ELSE ''
    END as imputed_fields
FROM customers_complete
WHERE (is_imputed_age + is_imputed_income + is_imputed_account_balance + is_imputed_years_as_customer) >= 2
ORDER BY total_imputations DESC
SAMPLE 20;
```

**Sample Output:**
```
total_customers | age_imputed | income_imputed | balance_imputed | years_imputed | avg_imputation_rate
----------------|-------------|----------------|-----------------|---------------|--------------------
         15,000 |       1,050 |          1,875 |             468 |           281 |                6.16

stage  | total_records | age_non_null | income_non_null | avg_income
-------|---------------|--------------|-----------------|------------
BEFORE |        15,000 |       13,950 |          13,125 |   58,234.56
AFTER  |        15,000 |       15,000 |          15,000 |   59,102.34

customer_id | age | income     | account_balance | years_as_customer | total_imputations | imputed_fields
------------|-----|------------|-----------------|-------------------|-------------------|----------------------
CUST-45678  |  38 |  62,500.00 |        4,250.50 |                 3 |                 4 | AGE INCOME BALANCE YEARS
CUST-45679  |  38 |  62,500.00 |        4,250.50 |                 5 |                 3 | AGE INCOME BALANCE
CUST-45680  |  42 |  62,500.00 |        8,940.12 |                 3 |                 3 | AGE INCOME YEARS
CUST-45681  |  38 |  71,200.00 |        4,250.50 |                 7 |                 2 | AGE BALANCE
```

**Business Impact:** Successfully imputed 3,674 missing values across 15K new customers, achieving 100% completeness for churn prediction model input, and flagged 127 customers with 2+ imputations for data quality review.

---

### Example 2: Group-Specific Imputation for Product Catalog
**Business Context:** Retail company filling missing product attributes using category-specific learned values.

```sql
-- Step 1: Apply category-specific imputation to new products
CREATE TABLE product_catalog_complete AS (
    SELECT * FROM TD_SimpleImputeTransform (
        ON new_product_imports AS InputTable PARTITION BY product_category, brand_tier
        ON product_impute_model AS FitTable DIMENSION
        USING
        Accumulate('product_id', 'product_name', 'import_date', 'supplier_id')
        OutputImputationFlag('true')
    ) AS dt
) WITH DATA;

-- Step 2: Review imputation by product category
SELECT
    product_category,
    COUNT(*) as total_products,
    SUM(is_imputed_unit_price) as price_imputed,
    SUM(is_imputed_weight_kg) as weight_imputed,
    SUM(is_imputed_shelf_life_days) as shelf_life_imputed,
    SUM(is_imputed_warranty_months) as warranty_imputed,
    AVG(CASE WHEN is_imputed_unit_price = 0 THEN unit_price END) as avg_original_price,
    AVG(CASE WHEN is_imputed_unit_price = 1 THEN unit_price END) as avg_imputed_price
FROM product_catalog_complete
GROUP BY product_category
ORDER BY price_imputed DESC;

-- Step 3: Validate imputed prices are reasonable
SELECT
    product_category,
    brand_tier,
    COUNT(*) as imputed_products,
    MIN(unit_price) as min_imputed_price,
    AVG(unit_price) as avg_imputed_price,
    MAX(unit_price) as max_imputed_price,
    -- Compare to category statistics
    (SELECT AVG(unit_price) FROM product_catalog_complete WHERE product_category = pc.product_category AND is_imputed_unit_price = 0) as category_avg_original
FROM product_catalog_complete pc
WHERE is_imputed_unit_price = 1
GROUP BY product_category, brand_tier
ORDER BY product_category, brand_tier;

-- Step 4: Catalog readiness report
SELECT
    product_category,
    COUNT(*) as total_products,
    SUM(CASE WHEN is_imputed_unit_price + is_imputed_weight_kg + is_imputed_shelf_life_days + is_imputed_warranty_months = 0 THEN 1 ELSE 0 END) as fully_complete,
    SUM(CASE WHEN is_imputed_unit_price + is_imputed_weight_kg + is_imputed_shelf_life_days + is_imputed_warranty_months BETWEEN 1 AND 2 THEN 1 ELSE 0 END) as partially_imputed,
    SUM(CASE WHEN is_imputed_unit_price + is_imputed_weight_kg + is_imputed_shelf_life_days + is_imputed_warranty_months >= 3 THEN 1 ELSE 0 END) as heavily_imputed,
    CAST(SUM(CASE WHEN is_imputed_unit_price + is_imputed_weight_kg + is_imputed_shelf_life_days + is_imputed_warranty_months = 0 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 as pct_fully_complete
FROM product_catalog_complete
GROUP BY product_category
ORDER BY pct_fully_complete;
```

**Sample Output:**
```
product_category | total_products | price_imputed | weight_imputed | shelf_life_imputed | warranty_imputed | avg_original_price | avg_imputed_price
-----------------|----------------|---------------|----------------|--------------------|------------------|--------------------|-----------------
Electronics      |          5,678 |           234 |            189 |                456 |              123 |             324.56 |            249.99
Home & Garden    |          3,456 |           156 |            234 |                 67 |               89 |             128.90 |            179.95
Food             |         23,456 |            89 |             45 |                234 |                0 |              15.67 |             12.49

product_category | brand_tier | imputed_products | min_imputed_price | avg_imputed_price | max_imputed_price | category_avg_original
-----------------|------------|------------------|-------------------|-------------------|-------------------|---------------------
Electronics      | Premium    |               87 |            549.99 |            899.99 |            899.99 |               867.45
Electronics      | Standard   |              147 |            199.99 |            249.99 |            249.99 |               238.90
Food             | Standard   |               89 |             12.49 |             12.49 |             12.49 |                12.34
Home & Garden    | Premium    |               56 |            179.95 |            179.95 |            179.95 |               182.30

product_category | total_products | fully_complete | partially_imputed | heavily_imputed | pct_fully_complete
-----------------|----------------|----------------|-------------------|-----------------|-------------------
Electronics      |          5,678 |          4,912 |               658 |             108 |              86.51
Food             |         23,456 |         23,089 |               345 |              22 |              98.44
Home & Garden    |          3,456 |          3,034 |               389 |              33 |              87.79
```

**Business Impact:** Completed 32K+ product records using category/brand-specific imputation (e.g., premium electronics at $900 median vs. standard food at $12), achieved 90%+ catalog completeness, and identified 163 heavily imputed products for supplier follow-up.

---

### Example 3: Production ETL Pipeline with Imputation Tracking
**Business Context:** Manufacturing company integrating missing value imputation into nightly sensor data processing.

```sql
-- Production ETL: Impute sensor readings and track data quality
CREATE MULTISET TABLE sensor_data_complete AS (
    SELECT
        dt.*,
        -- Calculate data quality score
        100 - (is_imputed_temperature + is_imputed_pressure + is_imputed_vibration +
               is_imputed_rpm + is_imputed_power_consumption) * 20 as quality_score,
        -- Categorize record quality
        CASE
            WHEN (is_imputed_temperature + is_imputed_pressure + is_imputed_vibration +
                  is_imputed_rpm + is_imputed_power_consumption) = 0 THEN 'COMPLETE'
            WHEN (is_imputed_temperature + is_imputed_pressure + is_imputed_vibration +
                  is_imputed_rpm + is_imputed_power_consumption) <= 2 THEN 'ACCEPTABLE'
            ELSE 'POOR_QUALITY'
        END as data_quality_category,
        CURRENT_TIMESTAMP as processing_timestamp,
        'v1.3_median_impute' as model_version
    FROM TD_SimpleImputeTransform (
        ON sensor_readings_staging AS InputTable PARTITION BY sensor_type, equipment_id
        ON sensor_impute_model AS FitTable DIMENSION
        USING
        Accumulate('reading_id', 'sensor_type', 'equipment_id', 'reading_timestamp', 'shift_id')
        OutputImputationFlag('true')
    ) AS dt
) WITH DATA PRIMARY INDEX (equipment_id, reading_timestamp);

-- Generate data quality report
SELECT
    sensor_type,
    data_quality_category,
    COUNT(*) as reading_count,
    AVG(quality_score) as avg_quality_score,
    SUM(is_imputed_temperature) as temp_imputations,
    SUM(is_imputed_pressure) as pressure_imputations,
    SUM(is_imputed_vibration) as vibration_imputations,
    SUM(is_imputed_rpm) as rpm_imputations,
    SUM(is_imputed_power_consumption) as power_imputations
FROM sensor_data_complete
GROUP BY sensor_type, data_quality_category
ORDER BY sensor_type,
    CASE data_quality_category
        WHEN 'COMPLETE' THEN 1
        WHEN 'ACCEPTABLE' THEN 2
        ELSE 3
    END;

-- Identify equipment with poor data quality
SELECT
    equipment_id,
    sensor_type,
    COUNT(*) as total_readings,
    SUM(CASE WHEN data_quality_category = 'POOR_QUALITY' THEN 1 ELSE 0 END) as poor_quality_readings,
    CAST(SUM(CASE WHEN data_quality_category = 'POOR_QUALITY' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 as pct_poor_quality,
    AVG(quality_score) as avg_quality_score,
    -- Flag which sensors have most imputations
    CASE
        WHEN SUM(is_imputed_temperature) = MAX(SUM(is_imputed_temperature)) OVER (PARTITION BY equipment_id)
            THEN 'TEMPERATURE'
        WHEN SUM(is_imputed_pressure) = MAX(SUM(is_imputed_pressure)) OVER (PARTITION BY equipment_id)
            THEN 'PRESSURE'
        WHEN SUM(is_imputed_vibration) = MAX(SUM(is_imputed_vibration)) OVER (PARTITION BY equipment_id)
            THEN 'VIBRATION'
        WHEN SUM(is_imputed_rpm) = MAX(SUM(is_imputed_rpm)) OVER (PARTITION BY equipment_id)
            THEN 'RPM'
        ELSE 'POWER'
    END as most_problematic_sensor
FROM sensor_data_complete
GROUP BY equipment_id, sensor_type
HAVING SUM(CASE WHEN data_quality_category = 'POOR_QUALITY' THEN 1 ELSE 0 END) >= 10
ORDER BY pct_poor_quality DESC, total_readings DESC;

-- Compare imputed vs original values
SELECT
    sensor_type,
    'temperature' as metric,
    AVG(CASE WHEN is_imputed_temperature = 0 THEN temperature END) as avg_original,
    AVG(CASE WHEN is_imputed_temperature = 1 THEN temperature END) as avg_imputed,
    ABS(AVG(CASE WHEN is_imputed_temperature = 0 THEN temperature END) -
        AVG(CASE WHEN is_imputed_temperature = 1 THEN temperature END)) as difference
FROM sensor_data_complete
GROUP BY sensor_type
UNION ALL
SELECT
    sensor_type,
    'pressure' as metric,
    AVG(CASE WHEN is_imputed_pressure = 0 THEN pressure END) as avg_original,
    AVG(CASE WHEN is_imputed_pressure = 1 THEN pressure END) as avg_imputed,
    ABS(AVG(CASE WHEN is_imputed_pressure = 0 THEN pressure END) -
        AVG(CASE WHEN is_imputed_pressure = 1 THEN pressure END)) as difference
FROM sensor_data_complete
GROUP BY sensor_type
ORDER BY sensor_type, metric;
```

**Sample Output:**
```
sensor_type | data_quality_category | reading_count | avg_quality_score | temp_imputations | pressure_imputations | vibration_imputations | rpm_imputations | power_imputations
------------|----------------------|---------------|-------------------|------------------|---------------------|----------------------|-----------------|------------------
TYPE_A      | COMPLETE             |        18,934 |            100.00 |                0 |                   0 |                    0 |               0 |                 0
TYPE_A      | ACCEPTABLE           |         1,234 |             84.32 |              234 |                 345 |                  189 |             267 |               199
TYPE_A      | POOR_QUALITY         |            89 |             48.76 |               34 |                  45 |                   23 |              56 |                67
TYPE_B      | COMPLETE             |        12,456 |            100.00 |                0 |                   0 |                    0 |               0 |                 0
TYPE_B      | ACCEPTABLE           |           678 |             86.78 |              123 |                 156 |                   89 |             134 |                98

equipment_id | sensor_type | total_readings | poor_quality_readings | pct_poor_quality | avg_quality_score | most_problematic_sensor
-------------|-------------|----------------|----------------------|------------------|-------------------|-----------------------
EQUIP-0045   | TYPE_A      |            234 |                   45 |            19.23 |             72.34 | RPM
EQUIP-0123   | TYPE_C      |            189 |                   34 |            17.99 |             75.67 | VIBRATION
EQUIP-0234   | TYPE_B      |            156 |                   23 |            14.74 |             78.90 | TEMPERATURE

sensor_type | metric      | avg_original | avg_imputed | difference
------------|-------------|--------------|-------------|------------
TYPE_A      | pressure    |       110.25 |      110.23 |       0.02
TYPE_A      | temperature |        72.48 |       72.45 |       0.03
TYPE_B      | pressure    |        98.45 |       98.45 |       0.00
TYPE_B      | temperature |        68.90 |       68.90 |       0.00
```

**Business Impact:** Processed 33K+ sensor readings with automated imputation, maintained 94% COMPLETE/ACCEPTABLE quality score, identified 3 equipment units with persistent data quality issues (>10 poor-quality readings), and validated imputed values match originals within 0.03 units confirming accurate model application.

---

### Example 4: Healthcare Patient Data with Mixed Imputation Types
**Business Context:** Hospital completing patient vital signs and categorical health information for clinical analysis.

```sql
-- Step 1: Apply imputation to patient records (numeric vitals + categorical fields)
CREATE TABLE patient_vitals_complete AS (
    SELECT * FROM TD_SimpleImputeTransform (
        ON patient_vitals_today AS InputTable PARTITION BY age_group, gender
        ON patient_impute_model AS FitTable DIMENSION
        USING
        Accumulate('patient_id', 'patient_mrn', 'reading_timestamp', 'ward', 'nurse_id')
        OutputImputationFlag('true')
    ) AS dt
) WITH DATA;

-- Step 2: Clinical data completeness report by ward
SELECT
    ward,
    COUNT(*) as total_readings,
    COUNT(*) - SUM(is_imputed_heart_rate + is_imputed_blood_pressure_sys + is_imputed_blood_pressure_dia +
                   is_imputed_oxygen_saturation + is_imputed_temperature + is_imputed_blood_type +
                   is_imputed_smoking_status + is_imputed_insurance_type) as fully_complete,
    SUM(is_imputed_heart_rate + is_imputed_blood_pressure_sys + is_imputed_blood_pressure_dia +
        is_imputed_oxygen_saturation + is_imputed_temperature) as vital_signs_imputed,
    SUM(is_imputed_blood_type + is_imputed_smoking_status + is_imputed_insurance_type) as categorical_imputed,
    CAST((COUNT(*) - SUM(is_imputed_heart_rate + is_imputed_blood_pressure_sys + is_imputed_blood_pressure_dia +
                         is_imputed_oxygen_saturation + is_imputed_temperature + is_imputed_blood_type +
                         is_imputed_smoking_status + is_imputed_insurance_type)) AS FLOAT) / COUNT(*) * 100 as pct_complete
FROM patient_vitals_complete
GROUP BY ward
ORDER BY pct_complete;

-- Step 3: Review imputed vs. original vital signs statistics
SELECT
    age_group,
    gender,
    'ORIGINAL' as data_source,
    COUNT(*) as record_count,
    AVG(heart_rate) as avg_hr,
    AVG(blood_pressure_sys) as avg_bp_sys,
    AVG(oxygen_saturation) as avg_o2_sat
FROM patient_vitals_complete
WHERE is_imputed_heart_rate = 0 AND is_imputed_blood_pressure_sys = 0 AND is_imputed_oxygen_saturation = 0
GROUP BY age_group, gender
UNION ALL
SELECT
    age_group,
    gender,
    'IMPUTED' as data_source,
    SUM(is_imputed_heart_rate + is_imputed_blood_pressure_sys + is_imputed_oxygen_saturation) as record_count,
    AVG(CASE WHEN is_imputed_heart_rate = 1 THEN heart_rate END) as avg_hr,
    AVG(CASE WHEN is_imputed_blood_pressure_sys = 1 THEN blood_pressure_sys END) as avg_bp_sys,
    AVG(CASE WHEN is_imputed_oxygen_saturation = 1 THEN oxygen_saturation END) as avg_o2_sat
FROM patient_vitals_complete
WHERE is_imputed_heart_rate = 1 OR is_imputed_blood_pressure_sys = 1 OR is_imputed_oxygen_saturation = 1
GROUP BY age_group, gender
ORDER BY age_group, gender, data_source;

-- Step 4: Identify patients with excessive imputations for clinical review
SELECT
    patient_mrn,
    patient_id,
    ward,
    age_group,
    reading_timestamp,
    is_imputed_heart_rate + is_imputed_blood_pressure_sys + is_imputed_blood_pressure_dia +
    is_imputed_oxygen_saturation + is_imputed_temperature + is_imputed_blood_type +
    is_imputed_smoking_status + is_imputed_insurance_type as total_imputations,
    CASE WHEN is_imputed_heart_rate = 1 THEN 'HR ' ELSE '' END ||
    CASE WHEN is_imputed_blood_pressure_sys = 1 THEN 'BP_SYS ' ELSE '' END ||
    CASE WHEN is_imputed_blood_pressure_dia = 1 THEN 'BP_DIA ' ELSE '' END ||
    CASE WHEN is_imputed_oxygen_saturation = 1 THEN 'O2_SAT ' ELSE '' END ||
    CASE WHEN is_imputed_temperature = 1 THEN 'TEMP ' ELSE '' END ||
    CASE WHEN is_imputed_blood_type = 1 THEN 'BLOOD_TYPE ' ELSE '' END ||
    CASE WHEN is_imputed_smoking_status = 1 THEN 'SMOKING ' ELSE '' END ||
    CASE WHEN is_imputed_insurance_type = 1 THEN 'INSURANCE' ELSE '' END as imputed_fields,
    'REVIEW_REQUIRED' as action
FROM patient_vitals_complete
WHERE (is_imputed_heart_rate + is_imputed_blood_pressure_sys + is_imputed_blood_pressure_dia +
       is_imputed_oxygen_saturation + is_imputed_temperature) >= 3  -- 3+ vital signs imputed
ORDER BY total_imputations DESC, reading_timestamp DESC
SAMPLE 50;
```

**Sample Output:**
```
ward | total_readings | fully_complete | vital_signs_imputed | categorical_imputed | pct_complete
-----|----------------|----------------|---------------------|---------------------|-------------
ICU  |            229 |            189 |                 134 |                  67 |        82.53
ER   |            267 |            223 |                 156 |                  89 |        83.52
MED  |            445 |            398 |                 189 |                  45 |        89.44
SURG |            334 |            298 |                 123 |                  34 |        89.22

age_group | gender | data_source | record_count | avg_hr | avg_bp_sys | avg_o2_sat
----------|--------|-------------|--------------|--------|------------|------------
45-54     | F      | ORIGINAL    |        5,556 |  72.34 |     125.67 |      97.82
45-54     | F      | IMPUTED     |          678 |  72.00 |     125.00 |      98.00
45-54     | M      | ORIGINAL    |        4,234 |  74.56 |     128.90 |      97.45
45-54     | M      | IMPUTED     |          456 |  75.00 |     129.00 |      98.00
55-64     | F      | ORIGINAL    |        3,890 |  74.23 |     130.45 |      97.23
55-64     | F      | IMPUTED     |          390 |  74.00 |     131.00 |      98.00

patient_mrn | patient_id | ward | age_group | reading_timestamp   | total_imputations | imputed_fields                                | action
------------|------------|------|-----------|---------------------|-------------------|-----------------------------------------------|----------------
MRN-123456  | PAT-45678  | ICU  | 65-74     | 2024-01-15 23:52:18 |                 7 | HR BP_SYS BP_DIA O2_SAT BLOOD_TYPE SMOKING INSURANCE | REVIEW_REQUIRED
MRN-123457  | PAT-45679  | ER   | 55-64     | 2024-01-15 23:48:33 |                 6 | HR BP_SYS O2_SAT TEMP BLOOD_TYPE INSURANCE    | REVIEW_REQUIRED
MRN-123458  | PAT-45680  | MED  | 75-84     | 2024-01-15 23:45:12 |                 5 | BP_SYS BP_DIA TEMP SMOKING INSURANCE          | REVIEW_REQUIRED
```

**Business Impact:** Completed 1,275 patient readings with age/gender-appropriate imputation (e.g., heart rate 72 bpm for females 45-54), achieved 85%+ data completeness across wards, validated imputed vitals match age-group demographics, and flagged 50 patients with 3+ vital signs imputed for clinical review and data collection process improvement.

---

### Example 5: Credit Scoring Application with Business Rule Imputations
**Business Context:** Financial institution completing credit applications using conservative business-defined defaults.

```sql
-- Step 1: Apply business rule imputation to credit applications
CREATE TABLE credit_applications_complete AS (
    SELECT * FROM TD_SimpleImputeTransform (
        ON credit_applications_pending AS InputTable PARTITION BY ANY
        ON credit_impute_model AS FitTable DIMENSION
        USING
        Accumulate('application_id', 'applicant_name', 'application_date', 'loan_amount', 'loan_purpose')
        OutputImputationFlag('true')
    ) AS dt
) WITH DATA;

-- Step 2: Application completeness and imputation summary
SELECT
    loan_purpose,
    COUNT(*) as total_applications,
    SUM(is_imputed_credit_score) as credit_score_imputed,
    SUM(is_imputed_debt_to_income_ratio) as dti_imputed,
    SUM(is_imputed_employment_years) as employment_imputed,
    SUM(is_imputed_num_credit_accounts) as credit_accounts_imputed,
    AVG(CASE WHEN is_imputed_credit_score = 1 THEN credit_score END) as avg_imputed_score,
    AVG(CASE WHEN is_imputed_credit_score = 0 THEN credit_score END) as avg_actual_score,
    CAST(SUM(is_imputed_credit_score + is_imputed_debt_to_income_ratio + is_imputed_employment_years + is_imputed_num_credit_accounts) AS FLOAT) /
         (COUNT(*) * 4) * 100 as avg_imputation_rate
FROM credit_applications_complete
GROUP BY loan_purpose
ORDER BY avg_imputation_rate DESC;

-- Step 3: Risk assessment with imputation flags
SELECT
    application_id,
    applicant_name,
    loan_amount,
    credit_score,
    debt_to_income_ratio,
    employment_years,
    -- Risk score calculation
    CASE
        WHEN credit_score >= 750 THEN 'LOW_RISK'
        WHEN credit_score >= 650 THEN 'MEDIUM_RISK'
        ELSE 'HIGH_RISK'
    END as risk_category,
    -- Confidence score (lower with more imputations)
    100 - (is_imputed_credit_score * 30 + is_imputed_debt_to_income_ratio * 20 +
           is_imputed_employment_years * 15 + is_imputed_num_credit_accounts * 10) as confidence_score,
    -- Imputation details
    is_imputed_credit_score + is_imputed_debt_to_income_ratio +
    is_imputed_employment_years + is_imputed_num_credit_accounts as total_imputations,
    CASE
        WHEN (is_imputed_credit_score + is_imputed_debt_to_income_ratio +
              is_imputed_employment_years + is_imputed_num_credit_accounts) = 0 THEN 'FULL_DATA'
        WHEN (is_imputed_credit_score + is_imputed_debt_to_income_ratio +
              is_imputed_employment_years + is_imputed_num_credit_accounts) <= 2 THEN 'ACCEPTABLE'
        ELSE 'MANUAL_REVIEW'
    END as review_status
FROM credit_applications_complete
ORDER BY
    CASE review_status
        WHEN 'MANUAL_REVIEW' THEN 1
        WHEN 'ACCEPTABLE' THEN 2
        ELSE 3
    END,
    loan_amount DESC;

-- Step 4: Compare approved vs. imputed applications
SELECT
    'APPLICATIONS_WITH_IMPUTATIONS' as category,
    COUNT(*) as application_count,
    AVG(credit_score) as avg_credit_score,
    AVG(loan_amount) as avg_loan_amount,
    SUM(CASE WHEN credit_score >= 650 THEN 1 ELSE 0 END) as potentially_approvable,
    CAST(SUM(CASE WHEN credit_score >= 650 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 as approval_rate
FROM credit_applications_complete
WHERE (is_imputed_credit_score + is_imputed_debt_to_income_ratio +
       is_imputed_employment_years + is_imputed_num_credit_accounts) > 0
UNION ALL
SELECT
    'APPLICATIONS_WITHOUT_IMPUTATIONS' as category,
    COUNT(*) as application_count,
    AVG(credit_score) as avg_credit_score,
    AVG(loan_amount) as avg_loan_amount,
    SUM(CASE WHEN credit_score >= 650 THEN 1 ELSE 0 END) as potentially_approvable,
    CAST(SUM(CASE WHEN credit_score >= 650 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 as approval_rate
FROM credit_applications_complete
WHERE (is_imputed_credit_score + is_imputed_debt_to_income_ratio +
       is_imputed_employment_years + is_imputed_num_credit_accounts) = 0;
```

**Sample Output:**
```
loan_purpose        | total_applications | credit_score_imputed | dti_imputed | employment_imputed | credit_accounts_imputed | avg_imputed_score | avg_actual_score | avg_imputation_rate
--------------------|--------------------|--------------------|-------------|--------------------|-----------------------|-------------------|------------------|--------------------
Personal Loan       |              3,456 |                345 |         456 |                234 |                   189 |            650.00 |           698.45 |                8.86
Auto Loan           |              5,678 |                234 |         345 |                456 |                   234 |            650.00 |           712.34 |                5.58
Mortgage            |              8,901 |                456 |         567 |                345 |                   456 |            650.00 |           723.56 |                5.13
Home Equity         |              2,345 |                123 |         156 |                 89 |                    98 |            650.00 |           715.23 |                4.95

application_id | applicant_name  | loan_amount | credit_score | debt_to_income_ratio | employment_years | risk_category | confidence_score | total_imputations | review_status
---------------|-----------------|-------------|--------------|----------------------|------------------|---------------|------------------|-------------------|---------------
APP-456789     | John Smith      |  450,000.00 |          650 |                 0.35 |                0 |  MEDIUM_RISK  |               55 |                 3 | MANUAL_REVIEW
APP-456790     | Jane Doe        |  325,000.00 |          650 |                 0.28 |                5 |  MEDIUM_RISK  |               70 |                 2 | ACCEPTABLE
APP-456791     | Bob Johnson     |  275,000.00 |          720 |                 0.35 |                8 |  LOW_RISK     |               80 |                 2 | ACCEPTABLE
APP-456792     | Alice Williams  |  425,000.00 |          750 |                 0.22 |               12 |  LOW_RISK     |              100 |                 0 | FULL_DATA

category                          | application_count | avg_credit_score | avg_loan_amount | potentially_approvable | approval_rate
----------------------------------|-------------------|------------------|-----------------|------------------------|---------------
APPLICATIONS_WITH_IMPUTATIONS     |              2,347 |           672.34 |       185,456.78 |                  1,987 |         84.66
APPLICATIONS_WITHOUT_IMPUTATIONS  |             18,033 |           708.90 |       203,234.56 |                 16,789 |         93.10
```

**Business Impact:** Completed 2,347 credit applications using conservative business rule defaults (650 credit score for missing values vs. 709 average), enabled processing of applications that would otherwise be rejected for incompleteness, flagged 234 applications with 3+ imputations for manual underwriting review, and maintained 85% approval rate for imputed applications (vs. 93% for complete applications).

---

### Example 6: Survey Data Completion with Mode-Based Categorical Imputation
**Business Context:** Market research firm completing customer satisfaction surveys using most frequent responses per segment.

```sql
-- Step 1: Apply mode-based imputation to survey responses
CREATE TABLE survey_responses_complete AS (
    SELECT * FROM TD_SimpleImputeTransform (
        ON survey_responses_raw AS InputTable PARTITION BY customer_segment, survey_month
        ON survey_impute_model AS FitTable DIMENSION
        USING
        Accumulate('response_id', 'respondent_id', 'survey_date', 'response_channel')
        OutputImputationFlag('true')
    ) AS dt
) WITH DATA;

-- Step 2: Survey completion statistics by segment
SELECT
    customer_segment,
    COUNT(*) as total_responses,
    SUM(is_imputed_satisfaction_rating + is_imputed_product_category +
        is_imputed_purchase_likelihood + is_imputed_age_range +
        is_imputed_income_bracket + is_imputed_preferred_channel) as total_imputations,
    SUM(CASE WHEN (is_imputed_satisfaction_rating + is_imputed_product_category +
                   is_imputed_purchase_likelihood + is_imputed_age_range +
                   is_imputed_income_bracket + is_imputed_preferred_channel) = 0 THEN 1 ELSE 0 END) as fully_complete_responses,
    CAST(SUM(CASE WHEN (is_imputed_satisfaction_rating + is_imputed_product_category +
                        is_imputed_purchase_likelihood + is_imputed_age_range +
                        is_imputed_income_bracket + is_imputed_preferred_channel) = 0 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 as pct_complete,
    SUM(is_imputed_satisfaction_rating) as satisfaction_imputed,
    SUM(is_imputed_purchase_likelihood) as likelihood_imputed
FROM survey_responses_complete
GROUP BY customer_segment
ORDER BY pct_complete;

-- Step 3: Satisfaction distribution (original vs. imputed)
SELECT
    customer_segment,
    satisfaction_rating,
    SUM(CASE WHEN is_imputed_satisfaction_rating = 0 THEN 1 ELSE 0 END) as original_count,
    SUM(CASE WHEN is_imputed_satisfaction_rating = 1 THEN 1 ELSE 0 END) as imputed_count,
    SUM(CASE WHEN is_imputed_satisfaction_rating = 0 THEN 1 ELSE 0 END) +
    SUM(CASE WHEN is_imputed_satisfaction_rating = 1 THEN 1 ELSE 0 END) as total_count,
    CAST(SUM(CASE WHEN is_imputed_satisfaction_rating = 1 THEN 1 ELSE 0 END) AS FLOAT) /
         (SUM(CASE WHEN is_imputed_satisfaction_rating = 0 THEN 1 ELSE 0 END) +
          SUM(CASE WHEN is_imputed_satisfaction_rating = 1 THEN 1 ELSE 0 END)) * 100 as pct_imputed
FROM survey_responses_complete
GROUP BY customer_segment, satisfaction_rating
ORDER BY customer_segment, satisfaction_rating;

-- Step 4: Report: Sentiment analysis with imputation transparency
SELECT
    customer_segment,
    -- Satisfaction scores
    SUM(CASE WHEN satisfaction_rating IN ('Very Satisfied', 'Satisfied') THEN 1 ELSE 0 END) as positive_responses,
    SUM(CASE WHEN satisfaction_rating = 'Neutral' THEN 1 ELSE 0 END) as neutral_responses,
    SUM(CASE WHEN satisfaction_rating IN ('Dissatisfied', 'Very Dissatisfied') THEN 1 ELSE 0 END) as negative_responses,
    -- Net Promoter Score proxy
    CAST(SUM(CASE WHEN satisfaction_rating IN ('Very Satisfied', 'Satisfied') THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 as satisfaction_score,
    -- Data quality metrics
    COUNT(*) as total_responses,
    SUM(is_imputed_satisfaction_rating) as satisfaction_imputed,
    CAST(SUM(is_imputed_satisfaction_rating) AS FLOAT) / COUNT(*) * 100 as pct_satisfaction_imputed,
    -- Confidence rating (lower with more imputation)
    100 - (CAST(SUM(is_imputed_satisfaction_rating) AS FLOAT) / COUNT(*) * 100 / 2) as confidence_rating
FROM survey_responses_complete
GROUP BY customer_segment
ORDER BY satisfaction_score DESC;
```

**Sample Output:**
```
customer_segment | total_responses | total_imputations | fully_complete_responses | pct_complete | satisfaction_imputed | likelihood_imputed
-----------------|-----------------|-------------------|--------------------------|--------------|---------------------|-------------------
Premium          |           9,544 |             2,456 |                    8,778 |        92.00 |                  766 |                890
Standard         |          20,456 |             5,789 |                   18,234 |        89.14 |                1,456 |              1,789
Budget           |          15,678 |             4,234 |                   14,012 |        89.38 |                1,234 |              1,456

customer_segment | satisfaction_rating | original_count | imputed_count | total_count | pct_imputed
-----------------|---------------------|----------------|---------------|-------------|------------
Premium          | Very Satisfied      |          3,890 |           345 |       4,235 |        8.15
Premium          | Satisfied           |          2,345 |           234 |       2,579 |        9.07
Premium          | Neutral             |          1,234 |           123 |       1,357 |        9.06
Premium          | Dissatisfied        |            456 |            45 |         501 |        8.98
Premium          | Very Dissatisfied   |            234 |            19 |         253 |        7.51
Standard         | Satisfied           |          8,934 |           678 |       9,612 |        7.05
Standard         | Neutral             |          6,789 |           489 |       7,278 |        6.72
Standard         | Dissatisfied        |          2,345 |           189 |       2,534 |        7.46

customer_segment | positive_responses | neutral_responses | negative_responses | satisfaction_score | total_responses | satisfaction_imputed | pct_satisfaction_imputed | confidence_rating
-----------------|--------------------|-----------------|--------------------|--------------------|-----------------|--------------------|-------------------------|------------------
Premium          |              6,814 |           1,357 |                754 |              71.39 |           9,544 |                766 |                     8.03 |                95.99
Standard         |             10,567 |           7,278 |              2,611 |              51.66 |          20,456 |              1,456 |                     7.12 |                96.44
Budget           |              7,234 |           6,012 |              2,432 |              46.13 |          15,678 |              1,234 |                     7.87 |                96.07
```

**Business Impact:** Completed 45,678 survey responses using segment-specific mode imputation (e.g., Premium customers default to "Very Satisfied", Standard to "Neutral"), achieved 90%+ response completeness, validated satisfaction distributions remain consistent between original and imputed responses (8% imputation rate), and calculated sentiment scores with 96%+ confidence ratings for market research insights.

---

## Common Use Cases

### By Industry

**Financial Services:**
- Credit application data completion
- Trading data gap filling for risk models
- Customer profile enrichment for marketing
- Fraud detection feature preparation
- Regulatory reporting data completion

**Healthcare:**
- Patient record completion for EHR systems
- Vital signs gap filling for monitoring
- Lab result imputation for clinical research
- Medical imaging metadata completion
- Health survey response completion

**Retail & E-commerce:**
- Product catalog completion for merchandising
- Customer demographic enrichment for segmentation
- Order data completion for analytics
- Marketing attribution data filling
- Recommendation system input preparation

**Manufacturing:**
- Sensor data gap filling for monitoring
- Quality control measurement completion
- Production log data filling
- Equipment maintenance record completion
- Supply chain data preparation

**Telecommunications:**
- Network metrics gap filling for SLA tracking
- Customer usage data completion
- Service quality measurement imputation
- Billing data preparation
- Churn prediction feature completion

**Market Research:**
- Survey response completion
- Panel data imputation
- Customer feedback enrichment
- A/B test data completion
- Sentiment analysis data preparation

### By Analytics Task

**Machine Learning:**
- Training dataset completion
- Test/validation dataset preparation
- Production scoring input preparation
- Feature engineering pipelines
- Model serving data preparation

**Data Quality:**
- Completeness improvement workflows
- Historical data reconstruction
- Operational dashboard data preparation
- Report dataset completion
- Data governance compliance

**Statistical Analysis:**
- Time series gap filling
- Experimental data completion
- Hypothesis testing dataset preparation
- Regression analysis input preparation
- Correlation analysis data preparation

**Business Intelligence:**
- Dashboard data completion
- KPI calculation input preparation
- Executive report data filling
- Trend analysis dataset preparation
- Performance metric completion

## Best Practices

### Application Strategy

**1. Ensure Model Compatibility:**
- InputTable must contain all columns referenced in FitTable
- Column data types must match exactly (numeric/categorical)
- If model trained with groups, partition by same columns
- Verify no schema changes since model training

**2. Use Appropriate PARTITION BY:**
```sql
-- Non-grouped model (trained without GroupByColumns)
... ON data AS InputTable PARTITION BY ANY  -- Random distribution

-- Grouped model (trained with GroupByColumns)
... ON data AS InputTable PARTITION BY product_category, region  -- Match training groups
```

**3. Enable Imputation Flags for Transparency:**
- Always use `OutputImputationFlag('true')` in production
- Track which values were imputed for auditing
- Use flags as features in ML models (signals missing data pattern)
- Monitor imputation rates over time for data quality

**4. Validate Imputed Values:**
```sql
-- Compare original vs. imputed statistics
SELECT
    'Original' as source,
    COUNT(*) as record_count,
    AVG(column_name) as avg_value,
    STDDEV_SAMP(column_name) as std_dev
FROM output_table
WHERE is_imputed_column_name = 0
UNION ALL
SELECT
    'Imputed' as source,
    COUNT(*) as record_count,
    AVG(column_name) as avg_value,
    STDDEV_SAMP(column_name) as std_dev
FROM output_table
WHERE is_imputed_column_name = 1;
```

### Production Implementation

**1. Build Comprehensive Pipelines:**
```sql
-- Complete production imputation pipeline
CREATE TABLE production_data_complete AS (
    SELECT
        dt.*,
        CURRENT_TIMESTAMP as processing_timestamp,
        'impute_model_v1.2_20240115' as model_version,
        -- Calculate data quality score
        100 - (is_imputed_col1 + is_imputed_col2 + is_imputed_col3) * 20 as quality_score
    FROM TD_SimpleImputeTransform (
        ON source_data AS InputTable PARTITION BY group_col
        ON impute_model AS FitTable DIMENSION
        USING
        Accumulate('id', 'timestamp', 'metadata')
        OutputImputationFlag('true')
    ) AS dt
) WITH DATA;

-- Separate high-quality vs. heavily-imputed records
CREATE TABLE high_quality_data AS
SELECT * FROM production_data_complete
WHERE quality_score >= 80
WITH DATA;

CREATE TABLE review_required_data AS
SELECT * FROM production_data_complete
WHERE quality_score < 60
WITH DATA;
```

**2. Monitor Imputation Rates:**
```sql
-- Track imputation statistics over time
INSERT INTO imputation_monitoring
SELECT
    CURRENT_DATE as process_date,
    'customer_data' as dataset_name,
    COUNT(*) as total_records,
    SUM(is_imputed_age) as age_imputations,
    SUM(is_imputed_income) as income_imputations,
    CAST(SUM(is_imputed_age + is_imputed_income) AS FLOAT) / (COUNT(*) * 2) * 100 as avg_imputation_rate
FROM customers_complete;

-- Alert on sudden imputation rate changes
SELECT
    process_date,
    avg_imputation_rate,
    LAG(avg_imputation_rate) OVER (ORDER BY process_date) as previous_rate,
    avg_imputation_rate - LAG(avg_imputation_rate) OVER (ORDER BY process_date) as rate_change
FROM imputation_monitoring
WHERE ABS(avg_imputation_rate - LAG(avg_imputation_rate) OVER (ORDER BY process_date)) > 5
ORDER BY process_date DESC;
```

**3. Handle New Groups:**
- Log warnings when new group combinations encountered
- Implement fallback strategies (global mean/median/mode)
- Schedule model retraining when new groups appear
- Document group expansion procedures

**4. Version Control and Auditing:**
- Tag output tables with model version and date
- Maintain transformation logs
- Document imputation decisions
- Enable reproducibility with model versioning

### Performance Optimization

**1. Leverage Parallelization:**
- Use `PARTITION BY ANY` for non-grouped models (random distribution)
- Use `PARTITION BY group_cols` for group-specific models (match training)
- DIMENSION keyword broadcasts small FitTable to all AMPs
- Process large datasets in batches by date/ID ranges

**2. Minimize Data Movement:**
```sql
-- Good: Filter before transformation
CREATE TABLE recent_data_complete AS (
    SELECT * FROM TD_SimpleImputeTransform (
        ON (SELECT * FROM source WHERE load_date >= CURRENT_DATE - 7) AS InputTable PARTITION BY ANY
        ON model AS FitTable DIMENSION
        USING Accumulate('id', 'date')
        OutputImputationFlag('true')
    ) AS dt
) WITH DATA;
```

**3. Optimize Accumulate Clause:**
- Only accumulate columns needed downstream
- Avoid accumulating large TEXT/CLOB columns
- Consider separate lookups for metadata

**4. Index Strategy:**
- Create primary index on frequently joined columns
- Index imputation flag columns for filtering
- Add secondary indexes on partition columns

### Data Quality and Validation

**1. Pre-Transformation Checks:**
```sql
-- Verify model compatibility
SELECT
    model.column_name,
    model.imputation_strategy,
    CASE
        WHEN source_col.column_name IS NULL THEN 'MISSING_IN_SOURCE'
        WHEN source_col.data_type != model.data_type THEN 'TYPE_MISMATCH'
        ELSE 'OK'
    END as compatibility
FROM impute_model model
LEFT JOIN information_schema.columns source_col
    ON model.column_name = source_col.column_name
    AND source_col.table_name = 'source_data_table';
```

**2. Post-Transformation Validation:**
- Check that all NULLs were handled
- Validate imputed values are within expected ranges
- Compare distributions before/after imputation
- Review heavily imputed records

**3. Quality Scoring:**
```sql
-- Create data quality scorecard
SELECT
    CASE
        WHEN total_imputations = 0 THEN 'GOLD'
        WHEN total_imputations <= 2 THEN 'SILVER'
        WHEN total_imputations <= 4 THEN 'BRONZE'
        ELSE 'NEEDS_REVIEW'
    END as data_quality_tier,
    COUNT(*) as record_count,
    AVG(quality_score) as avg_quality_score
FROM production_data_complete
GROUP BY 1
ORDER BY avg_quality_score DESC;
```

**4. Establish Monitoring:**
- Track imputation rates by column and group
- Alert on sudden rate changes (>10% variance)
- Monitor model staleness metrics
- Log transformation errors and warnings

## Related Functions

### Imputation Workflow
- **TD_SimpleImputeFit**: Train missing value imputation model (prerequisite)
- **TD_SimpleImputeTransform**: Apply trained imputation model (this function)

### Data Cleaning Functions
- **TD_OutlierFilterFit / TD_OutlierFilterTransform**: Handle outliers before/after imputation
- **PACK / UNPACK**: Data transformation and structuring
- **TD_StringSimilarity**: Handle data entry variations

### Data Exploration
- **TD_UnivariateStatistics**: Calculate statistics to validate imputation
- **TD_ColumnSummary**: Summarize column-level statistics
- **TD_Histogram**: Visualize distributions before/after imputation

### Feature Engineering
- **TD_ScaleFit / TD_ScaleTransform**: Normalize features after imputation
- **TD_BinCodeFit / TD_BinCodeTransform**: Bin continuous values
- **TD_OneHotEncodingFit**: Encode categorical values

## Notes and Limitations

### Important Considerations

**1. Model Compatibility:**
- InputTable must contain all columns from FitTable
- Column names and data types must match exactly
- Group columns (if used) must match training PARTITION BY
- FitTable cannot be reused if source schema changes

**2. PARTITION BY Requirements:**
- Non-grouped models: Use `PARTITION BY ANY`
- Grouped models: Use `PARTITION BY group_columns` matching training
- Incorrect partitioning causes errors or incorrect results
- All group combinations must exist in FitTable

**3. New Group Handling:**
- New groups not in FitTable cause errors
- Requires fallback strategy or model retraining
- Consider hierarchical grouping for rare combinations
- Log warnings for unseen group combinations

**4. Performance Considerations:**
- FitTable broadcast to all AMPs (must be small)
- Large InputTables partition across AMPs for parallel processing
- Group-specific processing requires hash redistribution
- Imputation flags add storage overhead (1 INTEGER column per imputed column)

**5. Data Quality Impact:**
- Imputation reduces variance in imputed columns
- May affect correlation structures between variables
- Can introduce bias if missingness not random (MNAR)
- Always track which values were imputed for transparency

**6. Imputation Strategy Preservation:**
- Always uses strategies defined in FitTable
- Cannot override strategy at transform time
- Numeric columns imputed with learned mean/median/mode
- Categorical columns imputed with learned mode

### Technical Constraints

**1. Column Requirements:**
- All columns in FitTable must exist in InputTable
- Data types must match (NUMERIC for numeric columns, VARCHAR/CHAR for categorical)
- Column names are case-sensitive
- NULL values in non-target columns are preserved

**2. OutputImputationFlag Behavior:**
- Creates one `is_imputed_[column]` column per imputed column
- Values: 1 = imputed, 0 = original value
- Increases output width significantly with many imputed columns
- Consider storage impact when enabling flags

**3. Error Conditions:**
- Missing columns in InputTable that exist in FitTable
- Type mismatch between InputTable and FitTable
- New group values not in FitTable (if group-based model)
- Invalid or corrupted FitTable
- Memory constraints with very large group counts

### Best Practices Summary

1. **Always use OutputImputationFlag('true')** for production tracking
2. **Validate model compatibility** before transformation
3. **Use appropriate PARTITION BY** matching training configuration
4. **Monitor imputation rates** over time for data quality trends
5. **Implement quality scoring** based on imputation counts
6. **Version control models** and track lineage
7. **Handle new groups** with fallback strategies
8. **Validate imputed values** against expected ranges
9. **Document imputation rules** for auditing and compliance
10. **Retrain models periodically** when data distribution shifts

## Version Information

- **Teradata Vantage Version**: 17.20
- **Function Category**: Machine Learning - Data Transformation
- **Documentation Generated**: November 2024
- **Model Type**: Fit-Transform Pattern (requires trained model from TD_SimpleImputeFit)
