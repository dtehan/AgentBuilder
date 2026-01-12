# Antiselect

## Function Name
**Antiselect** (alias: **TD_ANTISELECT**, **ANTI_SELECT**)

## Description
Antiselect is a data transformation utility function that returns all columns from an input table EXCEPT those explicitly specified in the Exclude parameter. Rather than listing dozens of columns to keep (as in a traditional SELECT statement), Antiselect allows you to specify only the few columns to remove, simplifying SQL for wide tables. This is particularly useful for feature engineering, data masking, PII redaction, and working with tables containing 50+ columns where selecting all-but-a-few is cumbersome.

**Key Characteristics:**
- **Inverse Selection**: Specify what to exclude rather than what to include (opposite of SELECT)
- **Wide Table Efficiency**: Simplifies queries on tables with 50-100+ columns
- **Column Range Support**: Exclude contiguous column ranges using `[start:end]` notation
- **Index-Based Selection**: Reference columns by position (0-indexed) or by name
- **Range Exclusions**: Exclude columns within ranges using minus notation
- **Schema Flexibility**: Automatically adapts to schema changes (new columns included by default)

## When to Use

### Business Applications
1. **Data Privacy and PII Redaction**
   - Remove sensitive columns before sharing data externally
   - Exclude SSN, credit card numbers, salary information from reports
   - Create anonymized datasets for analytics or third-party vendors
   - Mask personally identifiable information (PII) for GDPR/CCPA compliance
   - Generate privacy-compliant datasets for development/testing environments

2. **Machine Learning Feature Engineering**
   - Exclude target variable and ID columns from feature matrices
   - Remove non-predictive columns (metadata, audit timestamps)
   - Create training datasets by excluding validation/test set indicators
   - Prepare feature sets by removing highly correlated or redundant columns
   - Simplify feature selection by excluding low-importance features

3. **Data Export and Integration**
   - Remove internal-use columns before sending data to partners
   - Exclude system-generated columns (row_created_date, last_modified_by)
   - Prepare datasets for external reporting or regulatory submissions
   - Clean data for API responses (remove backend-only fields)
   - Create vendor-specific datasets by excluding irrelevant columns

4. **Report Generation and Business Intelligence**
   - Exclude technical columns from business user reports
   - Remove clutter from wide denormalized tables for readability
   - Create simplified views for self-service BI tools
   - Prepare executive dashboards by excluding operational details
   - Generate focused reports by excluding non-essential columns

5. **Development and Testing**
   - Create development datasets by excluding production-only columns
   - Remove audit trail columns for simplified testing
   - Generate sample datasets by excluding verbose description fields
   - Prepare unit test data by excluding unnecessary context columns
   - Simplify data quality checks by focusing on core business columns

6. **Data Quality and Profiling**
   - Exclude known-quality columns to focus profiling on problematic fields
   - Remove calculated/derived columns when profiling source data
   - Prepare data quality reports by excluding metadata columns
   - Analyze business data by excluding technical housekeeping columns
   - Focus data validation on transactional vs. administrative columns

### Analytical Use Cases
- **Feature Matrix Creation**: Exclude non-feature columns (IDs, timestamps, targets)
- **Schema Simplification**: Reduce column count for easier analysis
- **Data Sampling**: Exclude large text/blob columns for faster sampling
- **Column Subsetting**: Keep "almost all" columns without listing 50+ names
- **Dynamic Column Handling**: Automatically include new columns as schema evolves
- **Data Masking**: Remove sensitive columns for secure analytics
- **Performance Optimization**: Exclude unused columns to reduce query I/O

## Syntax

```sql
SELECT * FROM Antiselect (
    ON { table | view | (query) } AS InputTable
    USING
    Exclude ({ 'exclude_column' | exclude_column_range }[,...])
) AS alias;
```

## Required Elements

### InputTable
The table, view, or query containing columns to filter. Can have any schema with any number of columns.

**Typical Use Cases:**
- Wide tables (50-100+ columns) where selecting desired columns is verbose
- Denormalized tables with many unnecessary columns for specific analysis
- Tables with sensitive columns that need removal
- Feature tables for machine learning with metadata to exclude

### Exclude
**Required parameter** specifying which columns to exclude from the output.

**Syntax Options:**

1. **Exclude by Column Name:**
```sql
Exclude('column1', 'column2', 'column3')
```

2. **Exclude Column Range by Name:**
```sql
Exclude('start_column:end_column')
-- Includes start_column, end_column, and all columns between them
```

3. **Exclude Column Range by Index (0-based):**
```sql
Exclude('[0:4]')
-- Excludes columns at positions 0, 1, 2, 3, 4 (first 5 columns)
```

4. **Exclude Columns Up To Index:**
```sql
Exclude('[:4]')
-- Excludes all columns from start up to and including index 4
```

5. **Exclude Columns From Index Onward:**
```sql
Exclude('[4:]')
-- Excludes column at index 4 and all subsequent columns
```

6. **Exclude All Columns in Range EXCEPT Specific Columns:**
```sql
Exclude('[0:99]', '-[50]', '-column10')
-- Excludes columns 0-99 EXCEPT column at index 50 and column named 'column10'
-- The minus sign (-) indicates "keep this column within the range"
```

**Special Character Handling:**
- Column names with special characters: Use double quotes `"column*name"`
- Column names with double quotes: Escape with double quotes `"column""name"`

**Important Notes:**
- **Column indexes are 0-based**: First column is index 0, not 1
- **Column ranges are inclusive**: `[0:4]` includes columns 0, 1, 2, 3, 4
- **Ranges cannot overlap**: Multiple ranges must not include the same columns
- **Range exclusions use minus**: `-column_name` or `-[index]` keeps column within range

## Input Specification

### InputTable Schema
```sql
-- Example: Wide customer table with 20+ columns
CREATE TABLE customer_data (
    customer_id INTEGER,              -- Column 0 (index-based)
    ssn VARCHAR(11),                  -- Column 1 - SENSITIVE
    first_name VARCHAR(50),           -- Column 2
    last_name VARCHAR(50),            -- Column 3
    email VARCHAR(100),               -- Column 4
    phone VARCHAR(15),                -- Column 5
    date_of_birth DATE,               -- Column 6
    annual_income DECIMAL(12,2),      -- Column 7 - SENSITIVE
    credit_score INTEGER,             -- Column 8
    address VARCHAR(200),             -- Column 9
    city VARCHAR(50),                 -- Column 10
    state VARCHAR(2),                 -- Column 11
    zip VARCHAR(10),                  -- Column 12
    account_status VARCHAR(20),       -- Column 13
    account_open_date DATE,           -- Column 14
    last_transaction_date DATE,       -- Column 15
    total_balance DECIMAL(15,2),      -- Column 16
    created_date TIMESTAMP,           -- Column 17 - METADATA
    created_by VARCHAR(50),           -- Column 18 - METADATA
    last_modified_date TIMESTAMP,     -- Column 19 - METADATA
    last_modified_by VARCHAR(50)      -- Column 20 - METADATA
);
```

**Requirements:**
- No specific column type requirements (Antiselect works with all data types)
- Column names must be valid SQL object names
- For UNICODE data, UTF8 client character set required
- Any number of columns supported (1 to 1000+)

## Output Specification

### Output Table Schema
Output contains all input columns EXCEPT those specified in Exclude parameter. Column order preserved from input table.

**Example:**
```sql
-- Input: 21 columns (customer_id through last_modified_by)
-- Exclude: 'ssn', 'annual_income', 'created_date', 'created_by', 'last_modified_date', 'last_modified_by'
-- Output: 15 columns (all except the 6 excluded)

SELECT * FROM Antiselect (
    ON customer_data AS InputTable
    USING
    Exclude('ssn', 'annual_income', 'created_date', 'created_by', 'last_modified_date', 'last_modified_by')
) AS dt;

-- Output schema:
-- customer_id, first_name, last_name, email, phone, date_of_birth, credit_score,
-- address, city, state, zip, account_status, account_open_date, last_transaction_date, total_balance
```

**Output Characteristics:**
- **Column order**: Same as input table (excluding removed columns)
- **Data types**: Unchanged from input
- **Row count**: Same as input (no filtering)
- **NULL handling**: NULLs preserved (no special handling)

## Code Examples

### Example 1: PII Redaction for Data Sharing - Healthcare Patient Data

**Business Context:**
A hospital needs to share patient outcome data with a university research team for a clinical study on treatment effectiveness. The dataset contains 35 columns including sensitive PII (SSN, date of birth, full address, insurance details). HIPAA regulations require removing all PII before sharing. Rather than manually selecting 28 non-PII columns, they use Antiselect to exclude the 7 sensitive columns, ensuring compliance and simplifying maintenance as the schema evolves.

**SQL Code:**
```sql
-- Input: Patient outcomes table with 35 columns
CREATE TABLE patient_outcomes (
    patient_id INTEGER,              -- Internal ID (exclude)
    mrn VARCHAR(20),                 -- Medical Record Number (exclude)
    ssn VARCHAR(11),                 -- SENSITIVE PII (exclude)
    first_name VARCHAR(50),          -- SENSITIVE PII (exclude)
    last_name VARCHAR(50),           -- SENSITIVE PII (exclude)
    date_of_birth DATE,              -- SENSITIVE PII (exclude)
    full_address VARCHAR(300),       -- SENSITIVE PII (exclude)
    -- ... 28 clinical and outcome columns (KEEP)
    diagnosis_code VARCHAR(10),
    treatment_protocol VARCHAR(100),
    admission_date DATE,
    discharge_date DATE,
    length_of_stay INTEGER,
    primary_diagnosis VARCHAR(200),
    secondary_diagnoses VARCHAR(500),
    surgery_performed VARCHAR(3),
    surgery_type VARCHAR(200),
    complications VARCHAR(500),
    readmission_30day VARCHAR(3),
    mortality VARCHAR(3),
    age_at_admission INTEGER,       -- Derived, not exact DOB (OK to share)
    gender VARCHAR(1),
    race VARCHAR(50),
    ethnicity VARCHAR(50),
    insurance_type VARCHAR(50),     -- General type OK (not policy number)
    hospital_region VARCHAR(50),    -- Geographic region OK (not exact address)
    attending_physician_specialty VARCHAR(100),
    icu_stay VARCHAR(3),
    ventilator_used VARCHAR(3),
    blood_transfusion VARCHAR(3),
    medication_count INTEGER,
    lab_test_count INTEGER,
    imaging_count INTEGER,
    total_cost DECIMAL(12,2),
    outcome_score DECIMAL(5,2),
    quality_measure_met VARCHAR(3)
);

-- Step 1: Create de-identified dataset for research sharing
CREATE TABLE patient_outcomes_deidentified AS (
    SELECT * FROM Antiselect (
        ON patient_outcomes AS InputTable
        USING
        Exclude('patient_id', 'mrn', 'ssn', 'first_name', 'last_name', 'date_of_birth', 'full_address')
    ) AS dt
) WITH DATA;

-- Step 2: Verify PII removal
SELECT
    'Original Table' AS table_name,
    COUNT(*) AS column_count
FROM (
    SELECT * FROM patient_outcomes LIMIT 1
) AS cols
UNION ALL
SELECT
    'De-identified Table' AS table_name,
    COUNT(*) AS column_count
FROM (
    SELECT * FROM patient_outcomes_deidentified LIMIT 1
) AS cols;

-- Step 3: Validate no PII columns remain
-- Should return 0 rows (no PII columns found)
SELECT column_name
FROM DBC.Columns
WHERE DatabaseName = 'hospital_db'
  AND TableName = 'patient_outcomes_deidentified'
  AND column_name IN ('patient_id', 'mrn', 'ssn', 'first_name', 'last_name', 'date_of_birth', 'full_address');

-- Step 4: Generate research dataset summary
SELECT
    'Total Patients' AS metric,
    COUNT(*) AS value
FROM patient_outcomes_deidentified
UNION ALL
SELECT
    'Average Age at Admission',
    CAST(AVG(age_at_admission) AS INTEGER)
FROM patient_outcomes_deidentified
UNION ALL
SELECT
    'Readmission Rate (30-day)',
    CAST(100.0 * SUM(CASE WHEN readmission_30day = 'Yes' THEN 1 ELSE 0 END) / COUNT(*) AS DECIMAL(5,2))
FROM patient_outcomes_deidentified
UNION ALL
SELECT
    'Mortality Rate',
    CAST(100.0 * SUM(CASE WHEN mortality = 'Yes' THEN 1 ELSE 0 END) / COUNT(*) AS DECIMAL(5,2))
FROM patient_outcomes_deidentified;

-- Step 5: Sample de-identified records (safe to share)
SELECT * FROM patient_outcomes_deidentified
ORDER BY RANDOM()
LIMIT 5;
```

**Sample Output:**
```
-- Step 2: Column count verification
table_name                | column_count
--------------------------+--------------
Original Table            | 35           ← Full dataset
De-identified Table       | 28           ← 7 PII columns removed

-- Step 3: PII validation
(0 rows returned) ← PASS: No PII columns found in de-identified table

-- Step 4: Research dataset summary
metric                    | value
--------------------------+-------
Total Patients            | 15,432
Average Age at Admission  | 58
Readmission Rate (30-day) | 12.5
Mortality Rate            | 2.3

-- Step 5: Sample de-identified records (first 3 columns shown)
diagnosis_code | treatment_protocol      | admission_date | discharge_date | length_of_stay | ... (23 more columns)
---------------+-------------------------+----------------+----------------+----------------+
I21.0          | STEMI Protocol A        | 2024-03-15     | 2024-03-20     | 5              |
J18.9          | Community CAP Protocol  | 2024-04-02     | 2024-04-08     | 6              |
N18.5          | ESRD Management         | 2024-05-10     | 2024-05-25     | 15             |
(All 28 clinical columns present, no PII)
```

**Business Impact:**

**HIPAA Compliance:**
- **PII Removal**: Successfully removed 7 PII columns (SSN, names, DOB, address, internal IDs)
- **Safe Harbor Method**: De-identified data meets HIPAA Safe Harbor requirements
  - No direct identifiers (names, SSNs, addresses)
  - Ages aggregated (no exact DOB, only age at admission)
  - Geographic data limited to region (not full address)
- **Regulatory Risk**: Eliminated potential $50K+ HIPAA violation penalties per patient record

**Research Collaboration Efficiency:**
- **Simplified SQL**: Antiselect with 7 excludes vs. SELECT with 28 column names
  - 4 lines of SQL vs. 30+ lines (86% code reduction)
  - Easier to maintain as schema evolves (new clinical columns auto-included)
- **Faster Data Sharing**: De-identified dataset ready in minutes vs. hours of manual review
- **Reproducibility**: Single SQL statement ensures consistent de-identification

**Schema Evolution Benefits:**
- **Automatic Inclusion**: New clinical columns added to patient_outcomes automatically appear in de-identified table
  - Example: Hospital adds "sepsis_protocol_used" column next month
  - Antiselect query doesn't need updating (new column auto-included)
  - Traditional SELECT would require manual addition of new column
- **Maintenance Reduction**: 90% less schema maintenance vs. explicit column listing

**Research Value:**
- **Comprehensive Dataset**: 28 clinical variables enable robust statistical analysis
- **Sample Size**: 15,432 patients provide strong statistical power
- **Key Metrics Available**: Readmission (12.5%), mortality (2.3%), costs, quality measures
- **Publication-Ready**: De-identified data suitable for peer-reviewed research publication

**Cost-Benefit Analysis:**
- **Compliance Cost Avoidance**: Prevent $50K × 15,432 patients = $771M potential liability (if PII leaked)
- **IRB Approval Time**: Faster Institutional Review Board approval (clear de-identification)
- **IT Effort Savings**: 2 hours/month maintenance saved (vs. explicit column listing) = $3K annual savings
- **Research Collaboration**: Enable $500K NIH grant project (required de-identified data sharing)

**Quality Assurance:**
- **Automated Validation**: Step 3 query confirms zero PII columns (automated test)
- **Audit Trail**: Document Antiselect query in data sharing agreement
- **Reversibility**: Cannot re-identify patients from de-identified dataset (one-way transformation)

---

### Example 2: Machine Learning Feature Engineering - Customer Churn Prediction

**Business Context:**
A telecom company is building a churn prediction model using XGBoost. Their customer table has 87 columns: 65 potential features, 5 target/ID columns (customer_id, churn_flag, churn_date, account_number, billing_id), and 17 metadata columns (created_date, updated_date, data_source, etc.). For model training, they need to exclude non-feature columns. Using Antiselect simplifies feature matrix creation and automatically adapts when new features are added.

**SQL Code:**
```sql
-- Input: Customer data with 87 total columns
-- Columns 0-4: IDs and target (customer_id, account_number, billing_id, churn_flag, churn_date)
-- Columns 5-69: Features (65 columns)
-- Columns 70-86: Metadata (17 columns)

-- Step 1: Create feature matrix by excluding non-features
CREATE TABLE customer_features AS (
    SELECT * FROM Antiselect (
        ON customer_master AS InputTable
        USING
        Exclude(
            -- Exclude ID columns
            'customer_id', 'account_number', 'billing_id',
            -- Exclude target variables (to prevent leakage)
            'churn_flag', 'churn_date',
            -- Exclude metadata columns (not predictive)
            'record_created_date', 'record_created_by',
            'record_updated_date', 'record_updated_by',
            'data_source_system', 'data_load_timestamp',
            'data_quality_score', 'data_validation_flag',
            'etl_batch_id', 'etl_run_date',
            'last_audit_date', 'audit_status',
            'archive_flag', 'archive_date',
            'legal_hold_flag', 'gdpr_consent_flag',
            'data_classification'
            -- 22 columns excluded, 65 features remain
        )
    ) AS dt
) WITH DATA;

-- Step 2: Verify feature count
SELECT
    'Total Columns (Original)' AS metric,
    87 AS column_count
UNION ALL
SELECT
    'Feature Columns (After Antiselect)',
    (SELECT COUNT(*) FROM DBC.Columns
     WHERE DatabaseName = 'telecom_db'
     AND TableName = 'customer_features')
FROM (SELECT 1) AS dummy;

-- Step 3: Create separate target table (for supervised learning)
CREATE TABLE customer_targets AS (
    SELECT
        customer_id,
        churn_flag,
        churn_date
    FROM customer_master
) WITH DATA PRIMARY INDEX (customer_id);

-- Step 4: Verify no target leakage in features
-- Should return 0 rows (no target columns in features)
SELECT column_name
FROM DBC.Columns
WHERE DatabaseName = 'telecom_db'
  AND TableName = 'customer_features'
  AND column_name IN ('churn_flag', 'churn_date', 'customer_id');

-- Step 5: Train/test split using features only
CREATE TABLE customer_features_train AS (
    SELECT f.*
    FROM customer_features f
    INNER JOIN customer_targets t ON f.ROWID = t.ROWID  -- Join by row position
    WHERE t.customer_id MOD 5 != 0  -- 80% train (rows where ID % 5 != 0)
) WITH DATA;

CREATE TABLE customer_features_test AS (
    SELECT f.*
    FROM customer_features f
    INNER JOIN customer_targets t ON f.ROWID = t.ROWID
    WHERE t.customer_id MOD 5 = 0  -- 20% test (rows where ID % 5 = 0)
) WITH DATA;

-- Step 6: Prepare for XGBoost model training
-- All 65 columns are features (no manual column listing needed)
SELECT
    'Training Set' AS dataset,
    COUNT(*) AS row_count,
    (SELECT COUNT(*) FROM DBC.Columns
     WHERE DatabaseName = 'telecom_db'
     AND TableName = 'customer_features_train') AS feature_count
FROM customer_features_train
UNION ALL
SELECT
    'Test Set' AS dataset,
    COUNT(*) AS row_count,
    (SELECT COUNT(*) FROM DBC.Columns
     WHERE DatabaseName = 'telecom_db'
     AND TableName = 'customer_features_test') AS feature_count
FROM customer_features_test;

-- Step 7: Example - Use features for model training (pseudocode)
-- SELECT * FROM TD_XGBoost (
--     ON customer_features_train AS InputTable
--     ON customer_targets AS TargetTable
--     USING
--     TargetColumn('churn_flag')
--     -- All 65 feature columns automatically used (no need to list)
--     NumTrees(100)
--     MaxDepth(6)
--     LearningRate(0.1)
-- ) AS model;
```

**Sample Output:**
```
-- Step 2: Feature count verification
metric                              | column_count
------------------------------------+--------------
Total Columns (Original)            | 87
Feature Columns (After Antiselect)  | 65           ← 22 non-features excluded

-- Step 4: Target leakage check
(0 rows returned) ← PASS: No target or ID columns in feature matrix

-- Step 6: Train/test split summary
dataset      | row_count | feature_count
-------------+-----------+---------------
Training Set | 400,000   | 65            ← 80% of 500K customers
Test Set     | 100,000   | 65            ← 20% of 500K customers

-- Feature matrix sample (first 5 features shown, 60 more exist)
tenure_months | monthly_charges | total_charges | contract_type | internet_service | ... (60 more features)
--------------+-----------------+---------------+---------------+------------------+
24            | 79.99           | 1,919.76      | Month-to-Month| Fiber Optic      |
36            | 65.50           | 2,358.00      | One Year      | DSL              |
12            | 89.95           | 1,079.40      | Month-to-Month| Fiber Optic      |
(All 65 feature columns, no IDs or targets)
```

**Business Impact:**

**Model Development Efficiency:**
- **Simplified Feature Matrix**: One Antiselect query vs. listing 65 column names
  - SQL code: 25 lines vs. 70+ lines (64% reduction)
  - Human error risk: Minimal (explicit exclusions) vs. high (easy to miss one of 65 features)
  - Development time: 15 minutes vs. 2 hours (88% faster)

**Data Science Workflow:**
- **No Target Leakage**: Excluded churn_flag and churn_date prevents data leakage
  - Common mistake: Accidentally including target in features
  - Antiselect approach: Explicit exclusion ensures leakage prevention
  - Model validation: Step 4 automated check confirms no leakage

- **No ID Leakage**: Excluded customer_id, account_number prevents model overfitting on IDs
  - XGBoost could memorize IDs if included
  - Proper separation: IDs only in targets table, not features

**Schema Evolution (Critical Benefit):**
- **Automatic Feature Addition**: New features auto-included without code changes
  - **Scenario**: Marketing team adds "social_media_engagement_score" next month
  - **Traditional SELECT**: Requires updating SELECT list (easy to forget)
  - **Antiselect approach**: New column automatically included in customer_features
  - **Benefit**: Zero maintenance for schema additions (only excluded columns need specification)

- **Real-world Example**:
  - Month 1: 65 features
  - Month 2: Marketing adds 5 new engagement metrics → 70 features (auto-included)
  - Month 3: Product team adds 3 app usage metrics → 73 features (auto-included)
  - Month 4: No code changes needed, model retraining uses all 73 features

**Production Deployment:**
- **Reproducible Pipeline**: Same Antiselect query ensures consistent feature sets
- **Version Control**: Single SQL statement tracks excluded columns (not 65 feature names)
- **Auditable**: Clear documentation of what's excluded and why

**Model Performance:**
- **Baseline Model** (65 features): AUC = 0.8234
- **After Schema Evolution** (+8 new features): AUC = 0.8567 (+4.0% improvement)
  - New features auto-included without code changes
  - Retraining captured additional signal from new data

**Cost-Benefit:**
- **Development Time Savings**: 1.75 hours per model iteration × 12 iterations/year = 21 hours saved
  - 21 hours × $150/hour data scientist rate = **$3,150 annual savings**

- **Reduced Errors**: Prevent 1-2 target leakage incidents per year
  - Each incident: 40 hours debugging + model retraining
  - Avoided cost: 40 hours × $150/hour × 1.5 incidents = **$9,000 savings**

- **Faster Time-to-Production**: 2-week faster deployment per model iteration
  - 2 weeks × 4 iterations/year = 8 weeks faster
  - Business value: Earlier churn prevention = **$500K additional revenue retained**

**Total Annual Impact**: $512,150 benefit (time savings + error prevention + revenue)

---

### Example 3: Column Range Exclusion - Removing Audit Trail Columns

**Business Context:**
A financial services firm maintains transaction tables with comprehensive audit trails. Each table has 8 standard audit columns at the end: created_by, created_date, created_system, created_ip, modified_by, modified_date, modified_system, modified_ip (columns 42-49 in a 50-column table). For business reporting and analytics, these audit columns add clutter without providing analytical value. Using Antiselect with column range notation efficiently excludes all 8 audit columns.

**SQL Code:**
```sql
-- Input: Transaction table with 50 columns
-- Columns 0-41: Business columns (42 total)
-- Columns 42-49: Audit trail (8 columns)

-- Method 1: Exclude by column range (index-based)
CREATE TABLE transactions_clean AS (
    SELECT * FROM Antiselect (
        ON transactions_full AS InputTable
        USING
        Exclude('[42:49]')  -- Exclude columns at index 42 through 49 (audit columns)
    ) AS dt
) WITH DATA;

-- Method 2: Exclude by column range (name-based)
CREATE TABLE transactions_clean_v2 AS (
    SELECT * FROM Antiselect (
        ON transactions_full AS InputTable
        USING
        Exclude('created_by:modified_ip')  -- Range from first audit col to last
    ) AS dt
) WITH DATA;

-- Method 3: Exclude from index onward (all trailing columns)
CREATE TABLE transactions_clean_v3 AS (
    SELECT * FROM Antiselect (
        ON transactions_full AS InputTable
        USING
        Exclude('[42:]')  -- Exclude column 42 and all subsequent columns
    ) AS dt
) WITH DATA;

-- Verify results
SELECT
    'Original Table' AS table_name,
    COUNT(*) AS column_count
FROM (SELECT * FROM transactions_full LIMIT 1) AS cols
UNION ALL
SELECT
    'Cleaned Table (Method 1)',
    COUNT(*)
FROM (SELECT * FROM transactions_clean LIMIT 1) AS cols
UNION ALL
SELECT
    'Cleaned Table (Method 2)',
    COUNT(*)
FROM (SELECT * FROM transactions_clean_v2 LIMIT 1) AS cols
UNION ALL
SELECT
    'Cleaned Table (Method 3)',
    COUNT(*)
FROM (SELECT * FROM transactions_clean_v3 LIMIT 1) AS cols;

-- Compare query performance (with vs. without audit columns)
-- Query 1: Sum of transaction amounts by merchant (business query)
SELECT
    merchant_name,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount
FROM transactions_full  -- 50 columns (includes audit)
WHERE transaction_date >= CURRENT_DATE - 30
GROUP BY merchant_name
ORDER BY total_amount DESC
LIMIT 10;
-- Execution time: 3.2 seconds, I/O: 1.2 GB

SELECT
    merchant_name,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount
FROM transactions_clean  -- 42 columns (no audit)
WHERE transaction_date >= CURRENT_DATE - 30
GROUP BY merchant_name
ORDER BY total_amount DESC
LIMIT 10;
-- Execution time: 2.6 seconds, I/O: 980 MB (18.3% faster, 18.3% less I/O)
```

**Sample Output:**
```
-- Column count verification
table_name                  | column_count
----------------------------+--------------
Original Table              | 50           ← Full table with audit columns
Cleaned Table (Method 1)    | 42           ← 8 audit columns removed via [42:49]
Cleaned Table (Method 2)    | 42           ← 8 audit columns removed via name range
Cleaned Table (Method 3)    | 42           ← 8 audit columns removed via [42:]

-- Performance comparison
Query Type                  | Execution Time | I/O       | Improvement
----------------------------+----------------+-----------+-------------
With Audit Columns (50 col) | 3.2 seconds    | 1.2 GB    | Baseline
Without Audit (42 col)      | 2.6 seconds    | 980 MB    | 18.3% faster

-- Sample cleaned data (last 3 business columns + verify no audit columns)
transaction_id | amount    | merchant_name      | payment_method | transaction_status
---------------+-----------+--------------------+----------------+--------------------
12345          | 125.50    | Amazon             | Visa           | Completed
12346          | 89.99     | Walmart            | Mastercard     | Completed
12347          | 45.00     | Starbucks          | Debit          | Completed
(42 business columns present, 8 audit columns excluded)
```

**Business Impact:**

**Query Performance Improvement:**
- **I/O Reduction**: 18.3% less data read (980 MB vs. 1.2 GB)
  - 50 columns → 42 columns = 16% fewer columns
  - Actual I/O savings: 18.3% (includes block-level efficiency)
  - Applies to ALL queries on transactions table

- **Execution Time**: 18.3% faster (2.6 sec vs. 3.2 sec)
  - Merchant summary query: 0.6 seconds saved per execution
  - With 10,000 report queries per day: 10,000 × 0.6 sec = 6,000 seconds = 1.67 hours saved daily
  - Annual time savings: 1.67 hours/day × 365 days = 609 hours = 25 days of query time saved

**Storage Efficiency:**
- **Table Size Reduction**:
  - Original: 100M rows × 50 columns × avg 20 bytes/column = 100 GB
  - Cleaned: 100M rows × 42 columns × avg 20 bytes/column = 84 GB
  - **Storage Saved**: 16 GB (16% reduction)

- **Backup Efficiency**:
  - Daily backup: 16 GB less data to backup
  - Annual backup savings: 16 GB × 365 days = 5.84 TB
  - Backup time reduction: 18% faster backups

**Development Efficiency:**
- **Column Range Syntax**: One-line exclusion vs. listing 42 columns to keep
  - Antiselect: `Exclude('[42:49]')` or `Exclude('[42:]')`
  - Traditional SELECT: List 42 column names (42 lines of SQL)
  - **Code simplification**: 97.6% less code (1 line vs. 42 lines)

**Business Intelligence:**
- **Cleaner Reports**: Business users see only relevant 42 columns (not cluttered with 8 audit columns)
- **Faster BI Tool Loading**: Tableau/Power BI load 18% faster with fewer columns
- **Simplified Data Models**: Analysts work with focused business data

**Maintenance:**
- **Schema Evolution**: If business columns added, Antiselect adapts
  - Add column 41a (new business metric) → automatically included in clean table
  - Audit columns remain at end (42-49) → still excluded by `[42:]`

**Cost-Benefit:**
- **Storage Savings**: 16 GB × $0.50/GB/month = $8/month = **$96/year**
- **Query Performance**: 609 hours/year saved × $0.10/hour compute cost = **$61/year**
- **Development Time**: 5 reports/month × 30 minutes saved/report × $100/hour = **$2,500/year**
- **Total Annual Benefit**: **$2,657**

---

### Example 4: Complex Range with Exclusions - Keeping Specific Columns in Range

**Business Context:**
A marketing analytics team has a customer table with 100 columns organized by category: Demographics (columns 0-19), Purchase History (20-49), Website Behavior (50-69), Email Engagement (70-89), and System Metadata (90-99). They want to exclude most columns except for: key demographics (columns 0-5) and email engagement (70-89). Using Antiselect with range exclusions and the minus notation, they can efficiently specify complex exclusion patterns.

**SQL Code:**
```sql
-- Scenario: Keep columns 0-5 (key demographics) and 70-89 (email engagement)
-- Exclude: columns 6-69 and 90-99

-- Method 1: Exclude two separate ranges
CREATE TABLE customer_focused_v1 AS (
    SELECT * FROM Antiselect (
        ON customer_full AS InputTable
        USING
        Exclude('[6:69]', '[90:99]')  -- Exclude middle and trailing columns
    ) AS dt
) WITH DATA;

-- Method 2: Exclude all except specific columns (using minus notation)
CREATE TABLE customer_focused_v2 AS (
    SELECT * FROM Antiselect (
        ON customer_full AS InputTable
        USING
        Exclude('[6:]', '-[70:89]')
        -- Exclude columns 6 onward, BUT keep columns 70-89 (minus = exception)
    ) AS dt
) WITH DATA;

-- Method 3: Exclude specific columns within a range
CREATE TABLE customer_demographics_plus AS (
    SELECT * FROM Antiselect (
        ON customer_full AS InputTable
        USING
        Exclude(
            '[20:99]',            -- Exclude columns 20-99 (everything after demographics)
            '-email_open_rate',   -- BUT keep this specific email metric (within excluded range)
            '-email_click_rate',  -- AND keep this specific metric
            '-[72]'               -- AND keep column at index 72 (unsubscribe_date)
        )
    ) AS dt
) WITH DATA;

-- Verify column counts
SELECT
    'Original Table' AS table_name,
    100 AS column_count,
    'All customer data' AS description
UNION ALL
SELECT
    'Method 1 (Two Ranges)',
    (SELECT COUNT(*) FROM DBC.Columns WHERE DatabaseName = 'marketing_db' AND TableName = 'customer_focused_v1'),
    'Demographics (0-5) + Email (70-89)'
FROM (SELECT 1) AS dummy
UNION ALL
SELECT
    'Method 2 (Range + Exception)',
    (SELECT COUNT(*) FROM DBC.Columns WHERE DatabaseName = 'marketing_db' AND TableName = 'customer_focused_v2'),
    'Demographics (0-5) + Email (70-89)'
FROM (SELECT 1) AS dummy
UNION ALL
SELECT
    'Method 3 (Specific Exceptions)',
    (SELECT COUNT(*) FROM DBC.Columns WHERE DatabaseName = 'marketing_db' AND TableName = 'customer_demographics_plus'),
    'Demographics (0-19) + 3 email metrics'
FROM (SELECT 1) AS dummy;

-- Analyze excluded vs. included columns
WITH column_categories AS (
    SELECT
        CASE
            WHEN column_index BETWEEN 0 AND 19 THEN 'Demographics'
            WHEN column_index BETWEEN 20 AND 49 THEN 'Purchase History'
            WHEN column_index BETWEEN 50 AND 69 THEN 'Website Behavior'
            WHEN column_index BETWEEN 70 AND 89 THEN 'Email Engagement'
            WHEN column_index BETWEEN 90 AND 99 THEN 'System Metadata'
        END AS category,
        COUNT(*) AS column_count
    FROM (
        SELECT ROW_NUMBER() OVER (ORDER BY ColumnId) - 1 AS column_index
        FROM DBC.Columns
        WHERE DatabaseName = 'marketing_db'
          AND TableName = 'customer_full'
    ) AS indexed_columns
    GROUP BY category
)
SELECT * FROM column_categories ORDER BY MIN(column_index);
```

**Sample Output:**
```
-- Column count verification
table_name                  | column_count | description
----------------------------+--------------+---------------------------------------
Original Table              | 100          | All customer data
Method 1 (Two Ranges)       | 26           | Demographics (0-5=6) + Email (70-89=20)
Method 2 (Range + Exception)| 26           | Demographics (0-5=6) + Email (70-89=20)
Method 3 (Specific Exceptions)| 23         | Demographics (0-19=20) + 3 email metrics

-- Column category breakdown (original table)
category          | column_count
------------------+--------------
Demographics      | 20           ← Columns 0-19
Purchase History  | 30           ← Columns 20-49
Website Behavior  | 20           ← Columns 50-69
Email Engagement  | 20           ← Columns 70-89
System Metadata   | 10           ← Columns 90-99

-- Sample: Method 1 output (26 columns)
customer_id | age | gender | state | income_tier | account_status | ... | email_open_rate | email_click_rate | email_unsubscribe_date | ...
------------+-----+--------+-------+-------------+----------------+-----+-----------------+------------------+------------------------+
10001       | 34  | F      | CA    | High        | Active         | ... | 0.45            | 0.12             | NULL                   |
10002       | 52  | M      | TX    | Medium      | Active         | ... | 0.62            | 0.18             | NULL                   |
(6 demographic columns + 20 email columns = 26 total)

-- Sample: Method 3 output (23 columns - demographics + 3 specific email metrics)
customer_id | age | gender | state | income_tier | ... (15 more demo cols) | email_open_rate | email_click_rate | unsubscribe_date
------------+-----+--------+-------+-------------+-------------------------+-----------------+------------------+------------------
10001       | 34  | F      | CA    | High        | ...                     | 0.45            | 0.12             | NULL
10002       | 52  | M      | TX    | Medium      | ...                     | 0.62            | 0.18             | NULL
(20 demographic columns + 3 specific email metrics = 23 total)
```

**Business Impact:**

**Focused Analytics:**
- **Method 1 (Demographics + Full Email)**: 26 columns (74% reduction from 100)
  - **Use Case**: Email campaign performance analysis
  - **Benefit**: Focus on who customers are (demographics) and how they engage (email)
  - **Excluded**: Purchase history, website behavior not relevant for email analysis

- **Method 3 (Demographics + Key Email Metrics)**: 23 columns (77% reduction)
  - **Use Case**: Executive dashboard (high-level metrics only)
  - **Benefit**: 3 key email metrics (open rate, click rate, unsubscribe date) vs. all 20
  - **Cleaner**: Removes low-value email metrics (bounce rates, preview counts, etc.)

**Query Performance:**
- **Original 100-column query**: 5.2 seconds execution, 2.3 GB I/O
- **26-column query**: 1.4 seconds execution, 600 MB I/O (73% faster, 74% less I/O)
- **23-column query**: 1.2 seconds execution, 530 MB I/O (77% faster, 77% less I/O)
- **Daily Query Volume**: 5,000 reports × 4 seconds saved = 20,000 seconds = **5.6 hours saved daily**

**Complex Exclusion Patterns:**
- **Minus Notation Power**: `Exclude('[6:]', '-[70:89]')`
  - Reads as: "Exclude everything from column 6 onward, EXCEPT columns 70-89"
  - Alternative without Antiselect: List all 26 column names explicitly (26 lines vs. 1 line)
  - **Code Simplification**: 96% less code

- **Specific Column Exceptions**: `'-email_open_rate'`, `'-[72]'`
  - Keep specific high-value columns within excluded range
  - Enables surgical precision in column selection
  - Example: Exclude all purchase history (30 columns) but keep "lifetime_value" column

**Business Intelligence Tool Integration:**
- **Tableau/Power BI**: 26-column table vs. 100-column table
  - Load time: 2 seconds vs. 12 seconds (83% faster)
  - Data model simplicity: Users see only relevant columns
  - Report refresh: 5.6 hours saved daily = **140 hours/month**

**Data Governance:**
- **Principle of Least Privilege**: Marketing team gets demographics + email data only
  - No access to purchase history (20-49) → handled by sales team
  - No access to website behavior (50-69) → handled by web analytics team
  - No access to system metadata (90-99) → internal IT only

**Maintenance:**
- **Schema Evolution**: If new email columns added (e.g., column 71a "email_mobile_open_rate")
  - Method 1: Automatically included (within range 70-89)
  - Method 2: Automatically included (within exception range)
  - Traditional SELECT: Manual addition required

**Cost-Benefit:**
- **Query Time Savings**: 5.6 hours/day × 365 days × $0.10/hour = **$204/year**
- **BI Tool Performance**: 140 hours/month × 12 months × $0.05/hour = **$84/year**
- **Developer Productivity**: 10 hours/year saved (vs. explicit column listing) × $150/hour = **$1,500/year**
- **Storage Savings**: 74% column reduction × 50 GB table = 37 GB saved × $0.50/GB/month = **$222/year**
- **Total Annual Benefit**: **$2,010**

**Technical Advantages:**
- **Range Flexibility**: Mix index-based `[0:5]` and name-based `column1:column99` ranges
- **Exception Handling**: Minus notation `'-column_name'` or `'-[index]'` keeps specific columns
- **Readability**: `Exclude('[6:]', '-[70:89]')` clearer than listing 26 column names
- **Testability**: Easy to verify exclusions (Step: list excluded column indexes)

---

### Example 5: Data Export with Sensitive Column Removal - Third-Party Vendor Sharing

**Business Context:**
A retail company needs to share customer purchase data with a marketing analytics vendor for campaign optimization. The purchase_history table has 45 columns including sensitive financial data (credit card numbers, bank account info, exact purchase amounts) and internal operational data (supplier costs, profit margins, internal product codes). They must exclude 12 sensitive columns before export while maintaining the remaining 33 columns needed for marketing analysis.

**SQL Code:**
```sql
-- Input: Purchase history table (45 columns)
-- Sensitive columns to exclude (12):
--   - credit_card_number, credit_card_cvv, bank_account_number, routing_number
--   - ssn_last_four, customer_ip_address, customer_device_id
--   - supplier_cost, profit_margin, internal_sku, wholesale_price, vendor_contract_id

-- Step 1: Create vendor-safe dataset
CREATE TABLE purchases_vendor_export AS (
    SELECT * FROM Antiselect (
        ON purchase_history AS InputTable
        USING
        Exclude(
            -- Payment sensitive data
            'credit_card_number',
            'credit_card_cvv',
            'bank_account_number',
            'routing_number',
            -- Customer PII
            'ssn_last_four',
            'customer_ip_address',
            'customer_device_id',
            -- Internal financial data
            'supplier_cost',
            'profit_margin',
            'internal_sku',
            'wholesale_price',
            'vendor_contract_id'
        )
    ) AS dt
) WITH DATA;

-- Step 2: Add export metadata
ALTER TABLE purchases_vendor_export ADD export_date DATE DEFAULT CURRENT_DATE;
ALTER TABLE purchases_vendor_export ADD export_version VARCHAR(10) DEFAULT 'v2.1';
ALTER TABLE purchases_vendor_export ADD data_classification VARCHAR(20) DEFAULT 'Vendor-Safe';

-- Step 3: Validate no sensitive columns remain
CREATE TABLE sensitive_column_audit AS (
    SELECT
        'FAIL - Sensitive Column Found: ' || column_name AS audit_result
    FROM DBC.Columns
    WHERE DatabaseName = 'retail_db'
      AND TableName = 'purchases_vendor_export'
      AND column_name IN (
          'credit_card_number', 'credit_card_cvv', 'bank_account_number', 'routing_number',
          'ssn_last_four', 'customer_ip_address', 'customer_device_id',
          'supplier_cost', 'profit_margin', 'internal_sku', 'wholesale_price', 'vendor_contract_id'
      )
    UNION ALL
    SELECT 'PASS - No Sensitive Columns Found' AS audit_result
    WHERE NOT EXISTS (
        SELECT 1 FROM DBC.Columns
        WHERE DatabaseName = 'retail_db'
          AND TableName = 'purchases_vendor_export'
          AND column_name IN (
              'credit_card_number', 'credit_card_cvv', 'bank_account_number', 'routing_number',
              'ssn_last_four', 'customer_ip_address', 'customer_device_id',
              'supplier_cost', 'profit_margin', 'internal_sku', 'wholesale_price', 'vendor_contract_id'
          )
    )
) WITH DATA;

SELECT * FROM sensitive_column_audit;

-- Step 4: Generate export summary
SELECT
    'Total Purchase Records' AS metric,
    COUNT(*) AS value
FROM purchases_vendor_export
UNION ALL
SELECT
    'Date Range (Start)',
    CAST(MIN(purchase_date) AS VARCHAR(50))
FROM purchases_vendor_export
UNION ALL
SELECT
    'Date Range (End)',
    CAST(MAX(purchase_date) AS VARCHAR(50))
FROM purchases_vendor_export
UNION ALL
SELECT
    'Total Revenue (Vendor View)',
    CAST(SUM(final_price) AS VARCHAR(50))  -- Customer-paid price, not internal cost
FROM purchases_vendor_export
UNION ALL
SELECT
    'Unique Customers',
    CAST(COUNT(DISTINCT customer_id) AS VARCHAR(50))
FROM purchases_vendor_export;

-- Step 5: Export to CSV format (simulated)
-- In practice, use Teradata FastExport or similar
SELECT * FROM purchases_vendor_export
ORDER BY purchase_date DESC, customer_id
LIMIT 10;

-- Step 6: Document data sharing agreement
CREATE TABLE vendor_data_sharing_log (
    export_date DATE,
    vendor_name VARCHAR(100),
    table_name VARCHAR(100),
    record_count INTEGER,
    column_count INTEGER,
    sensitive_columns_excluded VARCHAR(500),
    exported_by VARCHAR(50),
    approval_manager VARCHAR(50),
    contract_reference VARCHAR(50)
);

INSERT INTO vendor_data_sharing_log VALUES (
    CURRENT_DATE,
    'Marketing Analytics Corp',
    'purchases_vendor_export',
    (SELECT COUNT(*) FROM purchases_vendor_export),
    (SELECT COUNT(*) FROM DBC.Columns WHERE DatabaseName = 'retail_db' AND TableName = 'purchases_vendor_export'),
    'credit_card, bank_account, ssn, IP, supplier_cost, profit_margin, internal_sku, wholesale_price, vendor_contract_id',
    USER,
    'Jane Smith - VP Marketing',
    'Contract-2024-MA-001'
);
```

**Sample Output:**
```
-- Step 3: Sensitive column audit
audit_result
------------------------------------------------
PASS - No Sensitive Columns Found               ← Validation successful

-- Step 4: Export summary
metric                      | value
----------------------------+----------------------
Total Purchase Records      | 2,345,678
Date Range (Start)          | 2023-01-01
Date Range (End)            | 2024-11-29
Total Revenue (Vendor View) | $123,456,789.50      ← Customer-paid prices only (no supplier costs)
Unique Customers            | 456,789

-- Step 5: Sample vendor-safe data (first 8 of 33 columns shown)
purchase_id | customer_id | purchase_date | product_name         | quantity | final_price | payment_method | shipping_address  | ... (25 more safe columns)
------------+-------------+---------------+----------------------+----------+-------------+----------------+-------------------+
P-9876543   | C-123456    | 2024-11-28    | Wireless Headphones  | 1        | 89.99       | **** REDACTED  | 123 Main St, ...  |
P-9876542   | C-234567    | 2024-11-28    | Smart Watch          | 1        | 299.99      | **** REDACTED  | 456 Oak Ave, ...  |
P-9876541   | C-345678    | 2024-11-27    | Laptop Stand         | 2        | 49.99       | **** REDACTED  | 789 Elm Blvd, ... |
(33 vendor-safe columns, 12 sensitive columns excluded)

-- Step 6: Data sharing log entry
export_date | vendor_name               | record_count | column_count | sensitive_columns_excluded          | exported_by | approval_manager
------------+---------------------------+--------------+--------------+-------------------------------------+-------------+--------------------
2024-11-29  | Marketing Analytics Corp  | 2,345,678    | 33           | credit_card, bank, ssn, costs, ... | john_doe    | Jane Smith - VP Marketing
```

**Business Impact:**

**Data Security and Compliance:**
- **PCI-DSS Compliance**: Removed credit card numbers (PCI-DSS requirement)
  - Violation cost: $5K-$100K per month non-compliance
  - Data breach: $200+ per compromised credit card
  - Antiselect ensures: Zero payment data in vendor export

- **SOX Compliance**: Excluded internal financial data (supplier costs, profit margins)
  - Competitive intelligence risk: Profit margins must remain confidential
  - Regulatory requirement: Financial data protection
  - Vendor contract: Explicitly prohibits sharing cost structure

- **Privacy Compliance (CCPA/GDPR)**: Removed SSN, IP addresses, device IDs
  - GDPR fine: Up to 4% of annual revenue
  - CCPA fine: $2,500-$7,500 per violation
  - Privacy risk mitigation: No PII beyond necessary for marketing analysis

**Vendor Relationship:**
- **Contract Compliance**: Data sharing agreement specifies "marketing data only"
  - 12 sensitive columns excluded per contract terms
  - Audit trail: vendor_data_sharing_log documents exact exclusions
  - Legal protection: Clear record of data minimization

- **Competitive Protection**: Internal pricing data secured
  - Supplier costs hidden: Prevents vendor from inferring margins
  - Wholesale prices redacted: Protects supplier relationships
  - Internal SKUs excluded: Prevents reverse-engineering product catalog

**Operational Efficiency:**
- **Export Simplification**: One Antiselect query vs. listing 33 column names
  - SQL code: 20 lines vs. 40+ lines (50% reduction)
  - Human error risk: Explicit exclusions vs. easy-to-miss inclusions
  - Maintenance: Update exclusions if sensitivity changes (not 33-column list)

**Automated Validation (Step 3):**
- **Security Gate**: Automated check ensures no sensitive columns in export
  - Runs before every export
  - Fails export if sensitive column detected
  - Audit trail: Log shows "PASS - No Sensitive Columns Found"

**Cost-Benefit Analysis:**
- **Data Breach Prevention**: Avoid $2M average data breach cost
  - 2.3M purchase records × $200/record if credit cards leaked = **$469M potential liability**
  - Antiselect approach: Zero payment data shared = **$469M risk eliminated**

- **Compliance Cost Avoidance**: PCI-DSS, SOX, GDPR/CCPA
  - PCI-DSS non-compliance: $100K/month fines = **$1.2M/year**
  - GDPR violations: 4% of $500M revenue = **$20M potential fine**
  - Antiselect ensures compliance: **$21.2M annual risk mitigation**

- **Competitive Intelligence Protection**: Internal pricing secured
  - Profit margin leak: Could enable vendor to compete directly
  - Estimated risk: $5M revenue loss if vendor uses data to compete
  - Antiselect protection: **$5M annual revenue protection**

- **Operational Efficiency**: Faster export process
  - Manual column review: 2 hours per export × 12 exports/year = 24 hours
  - Automated Antiselect: 15 minutes per export × 12 = 3 hours
  - Time savings: 21 hours × $150/hour = **$3,150/year**

**Total Annual Benefit**: $21.2M (compliance) + $5M (competitive protection) + $3K (efficiency) = **$26.2M risk mitigation**

**Governance:**
- **Data Classification**: Export table labeled "Vendor-Safe" (metadata column)
- **Audit Trail**: vendor_data_sharing_log tracks all exports
  - Who exported (exported_by)
  - Who approved (approval_manager)
  - What was excluded (sensitive_columns_excluded)
  - Contract reference (contract_reference)

**Reproducibility:**
- **Version Control**: export_version = 'v2.1' tracks export format changes
- **Consistent Exclusions**: Same Antiselect query ensures identical exclusions every export
- **Regulatory Audits**: Clear SQL statement documents data minimization approach

---

### Example 6: Development vs. Production Column Sets - Environment-Specific Views

**Business Context:**
A SaaS company maintains customer subscription tables with different column requirements for development and production environments. Production needs full audit trails (created_by, modified_by, etc.) and security columns (encryption_key_id, data_classification). Development environments should exclude these to: (1) simplify testing, (2) avoid exposing production security metadata, (3) reduce development database size. Using Antiselect, they create environment-specific views from a single source table.

**SQL Code:**
```sql
-- Source table: Full production schema (60 columns)
-- Production-only columns (10): audit trail, security, monitoring
-- Development columns (50): business data only

-- Step 1: Create development-friendly view (exclude production overhead)
CREATE VIEW subscriptions_dev AS
SELECT * FROM Antiselect (
    ON subscriptions_prod AS InputTable
    USING
    Exclude(
        -- Audit trail columns (not needed in dev)
        'created_by',
        'created_date',
        'created_system',
        'modified_by',
        'modified_date',
        'modified_system',
        -- Security columns (should not be in dev)
        'encryption_key_id',
        'data_classification_level',
        -- Production monitoring (not relevant for dev)
        'last_accessed_date',
        'access_count'
    )
) AS dt;

-- Step 2: Create staging-environment view (exclude only security columns)
CREATE VIEW subscriptions_staging AS
SELECT * FROM Antiselect (
    ON subscriptions_prod AS InputTable
    USING
    Exclude(
        -- Security columns only (staging has audit trails but not prod security)
        'encryption_key_id',
        'data_classification_level'
    )
) AS dt;

-- Step 3: Production view (all columns, explicit for clarity)
CREATE VIEW subscriptions_prod_view AS
SELECT * FROM subscriptions_prod;

-- Step 4: Compare environment schemas
SELECT
    'Production' AS environment,
    COUNT(*) AS column_count,
    'Full schema with audit, security, monitoring' AS description
FROM DBC.Columns
WHERE DatabaseName = 'saas_db' AND TableName = 'subscriptions_prod'
UNION ALL
SELECT
    'Staging',
    COUNT(*),
    'Full schema minus security columns'
FROM DBC.Columns
WHERE DatabaseName = 'saas_db' AND TableName = 'subscriptions_staging'
UNION ALL
SELECT
    'Development',
    COUNT(*),
    'Business columns only (no overhead)'
FROM DBC.Columns
WHERE DatabaseName = 'saas_db' AND TableName = 'subscriptions_dev';

-- Step 5: Test data refresh script (for dev environment)
-- Copy production data to dev, automatically excluding sensitive columns
CREATE TABLE subscriptions_dev_copy AS (
    SELECT * FROM subscriptions_dev  -- View with exclusions
    WHERE subscription_date >= CURRENT_DATE - 90  -- Last 90 days only
) WITH DATA;

-- Step 6: Verify development environment has no sensitive data
SELECT
    CASE
        WHEN NOT EXISTS (
            SELECT 1 FROM DBC.Columns
            WHERE DatabaseName = 'saas_db_dev'
              AND TableName = 'subscriptions_dev_copy'
              AND column_name IN ('encryption_key_id', 'data_classification_level', 'created_by')
        )
        THEN 'PASS: Dev environment has no production-only columns'
        ELSE 'FAIL: Sensitive columns detected in dev'
    END AS validation_result;

-- Step 7: Storage comparison
SELECT
    'Production Table' AS dataset,
    COUNT(*) AS row_count,
    60 AS column_count,
    SUM(CurrentPerm) / 1024 / 1024 / 1024 AS size_gb
FROM subscriptions_prod, DBC.TableSize
WHERE DatabaseName = 'saas_db' AND TableName = 'subscriptions_prod'
UNION ALL
SELECT
    'Development Copy',
    COUNT(*),
    50,
    SUM(CurrentPerm) / 1024 / 1024 / 1024
FROM subscriptions_dev_copy, DBC.TableSize
WHERE DatabaseName = 'saas_db_dev' AND TableName = 'subscriptions_dev_copy';
```

**Sample Output:**
```
-- Step 4: Environment schema comparison
environment | column_count | description
------------+--------------+------------------------------------------------
Production  | 60           | Full schema with audit, security, monitoring
Staging     | 58           | Full schema minus security columns
Development | 50           | Business columns only (no overhead)

-- Step 6: Development environment validation
validation_result
--------------------------------------------------------
PASS: Dev environment has no production-only columns    ← Security check passed

-- Step 7: Storage comparison
dataset            | row_count | column_count | size_gb
-------------------+-----------+--------------+---------
Production Table   | 5,000,000 | 60           | 45.5    ← Full production data
Development Copy   | 400,000   | 50           | 2.2     ← Last 90 days, fewer columns (95% smaller)

-- Sample: Development view (first 6 of 50 business columns shown, 10 overhead columns excluded)
subscription_id | customer_id | plan_name     | monthly_price | billing_cycle | start_date | ... (44 more business columns)
----------------+-------------+---------------+---------------+---------------+------------+
SUB-100001      | CUST-5001   | Premium       | 99.99         | Monthly       | 2024-01-15 |
SUB-100002      | CUST-5002   | Standard      | 49.99         | Annual        | 2024-02-01 |
SUB-100003      | CUST-5003   | Enterprise    | 299.99        | Monthly       | 2024-03-10 |
(No audit columns: created_by, modified_by, etc. - simpler for development)
```

**Business Impact:**

**Development Environment Efficiency:**
- **Simplified Schema**: 50 columns vs. 60 columns (17% reduction)
  - Developers work with business-relevant columns only
  - No clutter from audit trails (created_by, modified_by)
  - No confusion about security columns (encryption_key_id)
  - **Developer productivity**: 20% faster query writing (fewer columns to navigate)

- **Cleaner Test Data**: Development database 95% smaller
  - Production: 5M rows × 60 columns = 45.5 GB
  - Development: 400K rows × 50 columns = 2.2 GB (95% reduction)
  - **Benefits**:
    - Faster database refresh (15 min vs. 4 hours)
    - Lower dev infrastructure costs ($500/month vs. $50/month = $5,400/year savings)
    - Faster unit test execution (queries run 10x faster on smaller dev DB)

**Security and Compliance:**
- **Production Security Metadata Isolated**: Development environments excluded
  - encryption_key_id: Encryption keys not visible to developers (prevent misuse)
  - data_classification_level: Classification policies not in dev (prevent confusion)
  - **Security benefit**: Developers can't accidentally leak production security config

- **Audit Trail Protection**: created_by, modified_by excluded from dev
  - Real production usernames not in development
  - GDPR compliance: Production user IDs not exposed to all developers
  - **Privacy benefit**: Developer access doesn't reveal who modified production data

**Multi-Environment Strategy:**
- **Production** (60 columns): Full schema
  - All audit trails, security columns, monitoring metrics
  - Use case: Live customer data, regulatory compliance

- **Staging** (58 columns): Nearly full schema
  - Audit trails included (testing audit functionality)
  - Security columns excluded (staging uses different encryption)
  - Use case: Pre-production testing, integration tests

- **Development** (50 columns): Business columns only
  - No audit trails, security, or monitoring
  - Use case: Feature development, unit testing

**Cost-Benefit Analysis:**
- **Infrastructure Savings**: Development database 95% smaller
  - Prod DB cost: $6,000/year (45.5 GB)
  - Dev DB cost: $600/year (2.2 GB)
  - **Savings**: $5,400/year per development environment × 5 dev environments = **$27,000/year**

- **Developer Productivity**: 20% faster query writing
  - 50 developers × 20 queries/day × 1 minute saved/query × 250 workdays = 250,000 minutes/year
  - 250,000 min / 60 = 4,167 hours
  - 4,167 hours × $100/hour blended developer rate = **$416,700/year productivity gain**

- **Database Refresh Speed**: 4 hours → 15 minutes (93.75% faster)
  - Daily dev refresh: 1 time/day × 250 workdays = 250 refreshes/year
  - Time saved: 3.75 hours × 250 = 937.5 hours/year
  - DBA time savings: 937.5 hours × $120/hour = **$112,500/year**

- **Security Risk Reduction**: Prevented production security metadata exposure
  - Value: Avoid potential security breach ($5M average cost)
  - Probability reduction: 5% (developers can't leak what they don't have access to)
  - Expected value: 0.05 × $5M = **$250K/year risk mitigation**

**Total Annual Benefit**: $27K (infrastructure) + $417K (productivity) + $113K (DBA time) + $250K (security) = **$807,000**

**Governance and Maintainability:**
- **Single Source of Truth**: All environments based on subscriptions_prod table
  - Schema changes in production automatically propagate to staging/dev views
  - No schema drift between environments (common problem with separate tables)

- **Environment-Specific Exclusions**: Clear documentation via Antiselect
  - `subscriptions_dev`: Excludes 10 production-only columns
  - `subscriptions_staging`: Excludes 2 security columns
  - Easy to understand what differs between environments

- **Automated Refresh**: Dev environment refresh script simple
```sql
-- Single line to refresh dev with proper exclusions
CREATE TABLE subscriptions_dev_copy AS (SELECT * FROM subscriptions_dev) WITH DATA;
-- Antiselect view handles exclusions automatically
```

---

## Common Use Cases

### Data Privacy and Security
- **PII redaction**: Remove SSN, credit cards, addresses before data sharing
- **De-identification**: Exclude direct identifiers for HIPAA Safe Harbor compliance
- **Secure analytics**: Remove sensitive columns for untrusted environments
- **Data masking**: Exclude columns requiring masking, leaving safe columns
- **Third-party sharing**: Remove internal-only columns before vendor export

### Machine Learning and Analytics
- **Feature matrix creation**: Exclude IDs, targets, metadata from ML feature sets
- **Training data prep**: Remove non-predictive columns for model training
- **Test set creation**: Exclude validation indicators and leakage-prone columns
- **Model deployment**: Remove unused columns from scoring datasets
- **Data profiling**: Exclude known-quality columns to focus profiling efforts

### Application Development
- **Development environments**: Remove production-only audit/security columns
- **Unit testing**: Simplify test data by excluding unnecessary columns
- **API responses**: Remove backend-only fields before client delivery
- **Report generation**: Exclude technical columns from business reports
- **Data sampling**: Remove large text/blob columns for faster sampling

### Data Management
- **Wide table simplification**: Reduce 100-column tables to manageable size
- **Schema documentation**: Focus documentation on business columns only
- **Data quality**: Exclude metadata to focus on transactional data quality
- **Performance tuning**: Remove unused columns to reduce query I/O
- **Storage optimization**: Exclude rarely-accessed columns from hot tables

### Business Intelligence
- **Self-service BI**: Create simplified views for non-technical users
- **Executive dashboards**: Remove operational details, keep KPIs only
- **Report templates**: Standardize column sets by excluding variations
- **Data exports**: Remove internal columns before CSV/Excel export
- **Cross-functional analysis**: Exclude department-specific columns for shared reports

## Best Practices

### When to Use Antiselect
**Use Antiselect when:**
1. **Wide tables (50+ columns)**: Listing all keep-columns is verbose
2. **Few exclusions**: Excluding 5-10 columns vs. listing 40+ to keep
3. **Sensitive data removal**: Clear documentation of what's excluded
4. **Schema evolution**: New columns should be auto-included by default
5. **Development views**: Remove production-only overhead columns

**Don't use Antiselect when:**
1. **Narrow tables (<10 columns)**: Traditional SELECT is simpler
2. **Many exclusions**: Excluding 30 of 50 columns → just SELECT the 20 you need
3. **Performance-critical**: Antiselect adds slight overhead vs. explicit SELECT
4. **Column order matters**: Antiselect preserves input order, can't reorder

### Column Range Best Practices
1. **Index-based ranges for contiguous exclusions**:
```sql
-- Exclude trailing audit columns (columns 42-49)
Exclude('[42:49]')  -- Clear, concise

-- vs. listing individually
Exclude('created_by', 'created_date', 'created_system', ...)  -- Verbose
```

2. **Name-based ranges for semantic grouping**:
```sql
-- Exclude all columns from first_address_field to last_address_field
Exclude('street_address:country')  -- Semantic meaning clear
```

3. **Use minus notation for exceptions within ranges**:
```sql
-- Exclude columns 20-99 except column 50 and email_column
Exclude('[20:99]', '-[50]', '-email_address')
-- Reads clearly: "Exclude 20-99, but keep 50 and email_address"
```

### Documentation and Maintainability
1. **Comment your exclusions**:
```sql
SELECT * FROM Antiselect (
    ON customer_data AS InputTable
    USING
    Exclude(
        -- PII removal for GDPR compliance
        'ssn', 'credit_card', 'passport_number',
        -- Internal financial data (competitive sensitive)
        'supplier_cost', 'profit_margin',
        -- Production metadata (not needed in reports)
        'created_by', 'modified_by'
    )
) AS dt;
```

2. **Create named views for reusable exclusions**:
```sql
-- Create once
CREATE VIEW customer_external_safe AS
SELECT * FROM Antiselect (
    ON customer_master AS InputTable
    USING Exclude('ssn', 'credit_card', 'annual_income')
) AS dt;

-- Reuse everywhere
SELECT * FROM customer_external_safe WHERE state = 'CA';
```

3. **Version control exclusion patterns**:
```sql
-- Version 1.0: Exclude only SSN
-- Version 2.0: Added credit_card exclusion
-- Version 2.1: Added annual_income exclusion (GDPR)
```

### Security Best Practices
1. **Validate exclusions before sharing**:
```sql
-- Automated check: Ensure sensitive columns not present
SELECT column_name
FROM DBC.Columns
WHERE TableName = 'export_table'
  AND column_name IN ('ssn', 'credit_card', 'passport')
HAVING COUNT(*) > 0;  -- Should return 0 rows
```

2. **Document what's excluded in metadata**:
```sql
ALTER TABLE export_table ADD COMMENT 'Antiselect excluded: SSN, credit_card, passport, salary';
```

3. **Audit trail for data sharing**:
```sql
INSERT INTO data_export_log VALUES (
    CURRENT_DATE,
    'vendor_name',
    'table_name',
    'columns excluded: ssn, credit_card',
    USER,
    'export_reference_id'
);
```

### Performance Considerations
1. **Antiselect overhead**: Minimal (milliseconds) but exists
   - Use for development/reporting (query complexity dominates)
   - Avoid in ultra-low-latency OLTP queries (explicit SELECT faster)

2. **Materialize for repeated access**:
```sql
-- If querying antiselect view frequently, materialize it
CREATE TABLE customer_clean AS (
    SELECT * FROM customer_antiselect_view
) WITH DATA;

-- Then query materialized table (no antiselect overhead per query)
```

3. **Column range efficiency**:
```sql
-- Efficient: Single range
Exclude('[42:49]')

-- Less efficient: Many individual columns (but still acceptable)
Exclude('col1', 'col2', 'col3', ..., 'col15')
```

### Testing and Validation
1. **Unit test exclusions**:
```sql
-- Test 1: Verify correct column count
SELECT CASE
    WHEN COUNT(*) = 50  -- Expected 50 columns after exclusions
    THEN 'PASS'
    ELSE 'FAIL'
END AS test_result
FROM DBC.Columns
WHERE TableName = 'antiselect_output';

-- Test 2: Verify specific column excluded
SELECT CASE
    WHEN NOT EXISTS (SELECT 1 FROM DBC.Columns WHERE TableName = 'output' AND column_name = 'ssn')
    THEN 'PASS'
    ELSE 'FAIL'
END;
```

2. **Compare before/after**:
```sql
-- List excluded columns
SELECT column_name FROM DBC.Columns WHERE TableName = 'source_table'
EXCEPT
SELECT column_name FROM DBC.Columns WHERE TableName = 'antiselect_table';
```

## Related Functions

### Column Selection
- **SELECT**: Traditional explicit column selection (opposite of Antiselect)
- **SELECT ***: Select all columns (Antiselect selects "all except")
- **CAST**: Cast columns after Antiselect (data type transformations)

### Data Security
- **MASK**: Mask sensitive column values (alternative to excluding)
- **ENCRYPT**: Encrypt sensitive columns (keep column, protect value)
- **HASH**: Hash PII columns (one-way transformation vs. exclusion)

### View Creation
- **CREATE VIEW**: Combine with Antiselect for reusable exclusions
- **CREATE TABLE AS**: Materialize Antiselect results
- **CREATE VOLATILE TABLE**: Temporary exclusion for session

### Feature Engineering
- **Pack**: Pack multiple columns into one (reduce column count differently)
- **Unpack**: Unpack single column to multiple (opposite of Pack)
- **TD_ColumnTransformer**: Transform columns (often used after Antiselect)

### Data Preparation
- **TD_TrainTestSplit**: Split data (often after Antiselect removes non-features)
- **TD_ScaleFit/Transform**: Scale features (after Antiselect creates feature matrix)
- **TD_OneHotEncodingFit**: Encode features (after Antiselect)

## Notes and Limitations

### Function Constraints
- **UTF8 requirement**: UNICODE data requires UTF8 client character set
- **Column range restrictions**:
  - Ranges cannot overlap
  - Cannot exclude same column multiple times
  - Cannot include excluded column in range exclusion
- **Column naming**: Special characters require double-quote escaping

### Performance Considerations
1. **Slight overhead vs. explicit SELECT**:
   - Antiselect: Parse exclusions, determine remaining columns, build result
   - Explicit SELECT: Direct column projection
   - Overhead: Milliseconds (negligible for most use cases)
   - Impact: Only matters for ultra-high-frequency queries (millions per second)

2. **Query optimization**:
   - Optimizer may not push predicates through Antiselect as efficiently as explicit SELECT
   - For complex queries with WHERE clauses, consider materializing Antiselect result
   - Use EXPLAIN to verify query plan

3. **View performance**:
   - Views with Antiselect recompute exclusions on each query
   - For frequently accessed views (>1000 queries/day), consider materializing

### Schema Evolution
**Advantages:**
- New columns automatically included (default behavior)
- No need to update Antiselect query when adding columns

**Risks:**
- If new sensitive column added, Antiselect won't exclude it (until manually added to Exclude)
- **Mitigation**: Establish naming conventions (e.g., all PII columns prefixed with "pii_")
  ```sql
  -- Exclude all PII columns (current and future)
  -- Note: This requires custom SQL, Antiselect doesn't support regex patterns
  ```

**Best Practice:**
- Document exclusion rationale: "Excludes all PII and audit columns"
- Review Antiselect queries quarterly to ensure new columns properly handled

### Common Pitfalls
1. **Forgetting to exclude new sensitive columns**:
   - Problem: New SSN-like column added, Antiselect doesn't know to exclude
   - Solution: Regular reviews, naming conventions, automated validation

2. **Overlapping ranges**:
   ```sql
   -- ERROR: Overlapping ranges
   Exclude('[0:10]', '[5:15]')  -- Columns 5-10 in both ranges

   -- FIX: Non-overlapping ranges
   Exclude('[0:15]')  -- Single range, no overlap
   ```

3. **Excluding column also in range exclusion**:
   ```sql
   -- ERROR: Column 'id' explicitly excluded AND in range
   Exclude('id', '[0:10]')  -- If 'id' is in range [0:10]

   -- FIX: Use range only
   Exclude('[0:10]')
   ```

4. **Index confusion (0-based vs. 1-based)**:
   ```sql
   -- WRONG: Thinking first column is index 1
   Exclude('[1:5]')  -- Excludes columns 1-5 (second through sixth)

   -- CORRECT: First column is index 0
   Exclude('[0:4]')  -- Excludes columns 0-4 (first through fifth)
   ```

### Business Considerations
1. **Data governance**: Document why columns excluded
   - Regulatory requirement (GDPR, HIPAA)?
   - Competitive sensitivity (profit margins)?
   - Simplification (audit trails)?

2. **Compliance**: Ensure exclusions meet legal requirements
   - GDPR: Is PII properly redacted?
   - PCI-DSS: Are payment card numbers excluded?
   - SOX: Is internal financial data protected?

3. **Vendor contracts**: Verify exclusions match data sharing agreements
   - What columns can be shared?
   - What must be excluded?
   - Document compliance in export logs

### Recommendations
1. **Start simple**: Exclude a few columns by name before using ranges
2. **Test thoroughly**: Verify excluded columns not present in output
3. **Document rationale**: Why each column excluded (PII, security, performance)
4. **Version control**: Track exclusion changes over time
5. **Automate validation**: Check no sensitive columns in exports (SQL tests)
6. **Review quarterly**: Ensure new columns properly handled
7. **Use views**: Create reusable Antiselect views for common patterns

---

**Generated from Teradata Database Analytic Functions Version 17.20**
**Function Category**: Utility Functions - Column Selection
**Last Updated**: November 29, 2025
