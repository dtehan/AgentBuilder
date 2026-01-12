# TD_TrainTestSplit

## Function Name
**TD_TrainTestSplit** (alias: **TRAIN_TEST_SPLIT**)

## Description
TD_TrainTestSplit is a data preparation function that splits a dataset into separate training and test subsets for machine learning model development and validation. The function creates mutually exclusive partitions of data, enabling unbiased model evaluation on held-out data that wasn't used during training. This is a fundamental step in the machine learning workflow to prevent overfitting and ensure model generalization.

**Key Characteristics:**
- **Random Splitting**: Uses pseudorandom sampling to create representative partitions
- **Stratified Sampling**: Option to maintain class distribution across train/test sets (critical for imbalanced classes)
- **Configurable Split Ratio**: Flexible train/test split percentages (common: 70/30, 80/20, 90/10)
- **Reproducibility**: Seed parameter ensures consistent splits across runs
- **Split Indicators**: Adds partition column identifying train vs. test assignment
- **Large Dataset Support**: Efficient processing of millions of rows in single operation
- **Multiple Output Options**: Create separate tables or single table with partition indicator

## When to Use

### Business Applications
1. **Model Development Workflow**
   - Split historical data for supervised learning model training
   - Reserve test set for final model validation before deployment
   - Create validation set for hyperparameter tuning (three-way split: train/validation/test)
   - Ensure unbiased performance estimates for business case justification

2. **Regulatory Compliance (Banking/Finance)**
   - Basel II/III: Reserve hold-out test set for model validation
   - CECL/IFRS 9: Demonstrate model performance on out-of-sample data
   - SR 11-7 Model Risk Management: Document train/test split methodology
   - Fair Lending: Ensure test set representativeness across demographic groups

3. **Production Model Validation**
   - Create test set matching expected production data distribution
   - Validate model performance before A/B testing
   - Establish baseline metrics (AUC, accuracy, RMSE) for monitoring
   - Generate performance reports for stakeholders

4. **Fraud Detection Model Development**
   - Stratified split maintaining rare fraud case distribution (e.g., 0.1% fraud rate)
   - Training set: Build fraud detection models
   - Test set: Validate detection rate and false positive rate
   - Ensure both sets have sufficient fraud examples for reliable evaluation

5. **Customer Analytics**
   - Churn prediction: Split customer base for churn model training
   - CLV modeling: Train on historical cohorts, test on recent cohorts
   - Segmentation: Validate clustering approaches on held-out customers
   - Propensity modeling: Campaign response model development

6. **Healthcare Predictive Models**
   - Disease prediction: Split patient data for diagnostic model training
   - Readmission models: Train on historical admissions, test on recent cases
   - Treatment response: Validate treatment recommendation models
   - Clinical trial analysis: Create training cohort and validation cohort

7. **Credit Risk Modeling**
   - Default prediction: Split loan portfolio for credit risk model development
   - Training set: Develop scorecards and machine learning models
   - Test set: Validate discriminatory power (AUC, Gini, KS statistic)
   - Ensure test set represents current portfolio composition

8. **Time Series Forecasting**
   - Non-random split: Training set = earlier time period, test set = later period
   - Avoid temporal leakage (future information in training)
   - Validate forecasting accuracy on true out-of-sample period
   - Sales forecasting, demand planning, load forecasting

### Analytical Use Cases
- **Overfitting Prevention**: Hold out data to detect if model memorizes training data
- **Generalization Assessment**: Estimate model performance on unseen data
- **Model Comparison**: Fair comparison of algorithms on identical train/test sets
- **Hyperparameter Tuning**: Create validation set for tuning without test set contamination
- **Cross-Validation Complement**: Generate initial split before k-fold CV on training set
- **Baseline Establishment**: Create fixed test set for consistent performance benchmarking
- **Feature Engineering Validation**: Test if new features improve test set performance
- **Ensemble Model Development**: Split for stacking, blending, or boosting workflows

## Syntax

```sql
SELECT * FROM TD_TrainTestSplit (
    ON { table | view | (query) } AS InputTable
    USING
    TestSize (test_fraction)
    [ TrainSize (train_fraction) ]
    [ IDColumn ('id_column') ]
    [ StratifyColumns ('column1' [, 'column2', ...]) ]
    [ Seed (random_seed) ]
    [ OutputType ({ 'SINGLE_TABLE' | 'SEPARATE_TABLES' }) ]
    [ TrainTableName ('train_table_name') ]
    [ TestTableName ('test_table_name') ]
    [ PartitionColumn ('partition_column_name') ]
) AS alias;
```

## Required Elements

### InputTable
The table or dataset to be split into training and test subsets.

**Typical Contents:**
- Feature columns (independent variables)
- Target column (dependent variable for supervised learning)
- ID columns (customer_id, transaction_id, patient_id, etc.)
- Metadata columns (timestamps, segments, etc.)

**Requirements:**
- Must contain at least enough rows to create meaningful train and test sets
- No specific column requirements (function operates on entire rows)
- If using stratification, stratify columns must have manageable cardinality

### TestSize
**Required parameter** specifying the fraction or count of data allocated to the test set.

**Type:** Float (0 to 1) for fraction, or Integer for absolute count
**Common Values:**
- **0.2 (20%)**: Standard for large datasets (80/20 split)
- **0.3 (30%)**: Common for medium datasets (70/30 split)
- **0.1 (10%)**: For very large datasets where 10% still provides sufficient test samples
- **Absolute count**: E.g., 10000 for exactly 10,000 test records

**Examples:**
- `TestSize(0.2)` - 20% test, 80% train (most common)
- `TestSize(0.3)` - 30% test, 70% train
- `TestSize(10000)` - Exactly 10,000 records in test set

**Best Practices:**
- **Large datasets (>100K rows)**: 10-20% test set sufficient
- **Medium datasets (10K-100K rows)**: 20-30% test set recommended
- **Small datasets (<10K rows)**: 30-40% test set or use cross-validation instead
- **Imbalanced classes**: Ensure test set has ≥100 minority class examples

## Optional Elements

### TrainSize
Specifies the fraction or count of data allocated to the training set. If both TrainSize and TestSize specified, they must sum to ≤1.0.

**Type:** Float (0 to 1) for fraction, or Integer for absolute count
**Default:** 1.0 - TestSize (complementary to test set)
**Use Cases:**
- Three-way split: Specify both TrainSize and TestSize to create train/test/unused subsets
- Precise control: E.g., TrainSize(0.6), TestSize(0.2) leaves 0.2 unused

**Examples:**
- `TrainSize(0.7)` + `TestSize(0.3)` = 70/30 split (sum = 1.0)
- `TrainSize(0.6)` + `TestSize(0.2)` = 60% train, 20% test, 20% unused (validation set)

**Note:** Most common usage is to specify only TestSize, letting TrainSize default to complement

### IDColumn
Specifies a column containing unique identifiers for tracking which records assigned to train vs. test sets.

**Type:** String (column name)
**Use Cases:**
- Ensure specific records (customers, transactions) consistently assigned to same partition
- Enable joining back to original table with partition assignments
- Audit trail for regulatory compliance
- Debugging and data quality checks

**Example:** `IDColumn('customer_id')`

**Best Practices:**
- Use stable, unchanging ID (customer_id, not session_id which may change)
- If multiple records per entity, stratify by entity to avoid leakage

### StratifyColumns
Specifies columns to use for stratified sampling, ensuring train and test sets have similar distributions of these variables. **Critical for imbalanced classification.**

**Type:** String (comma-separated column names)
**Use Cases:**
- **Imbalanced classes**: Maintain rare event distribution (fraud, disease, churn)
- **Categorical balance**: Ensure demographic groups represented in both sets
- **Time period balance**: Maintain seasonal patterns in both sets
- **Multiple stratification**: Stratify on multiple columns simultaneously

**Examples:**
- `StratifyColumns('churn_flag')` - Maintain churn rate in train and test
- `StratifyColumns('fraud_label', 'customer_segment')` - Stratify on fraud AND segment
- `StratifyColumns('disease_outcome', 'age_group', 'gender')` - Multi-variable stratification

**Important Notes:**
- Without stratification: Random split may create different class distributions in train vs. test
- With stratification: Both sets maintain same class proportions (e.g., 1% fraud in both)
- **Always stratify for imbalanced classification** (fraud, rare disease, churn)
- Cardinality constraint: Stratify columns should not have too many unique values

### Seed
Random seed for reproducibility. Using the same seed with identical input data produces identical train/test splits.

**Type:** Integer (any value)
**Default:** Random seed (non-reproducible splits)
**Use Cases:**
- Reproducible experiments: Same split across multiple runs
- Model comparison: Ensure fair comparison with identical train/test sets
- Debugging: Consistent splits for troubleshooting
- Regulatory compliance: Document and reproduce exact split for audits

**Example:** `Seed(42)` (42 is traditional ML seed value, but any integer works)

**Best Practices:**
- **Development**: Use seed for reproducibility during model development
- **Production**: May use different seed or no seed for each model retraining cycle
- **Documentation**: Record seed value in model documentation for reproducibility

### OutputType
Specifies whether to create a single table with partition indicator column, or separate train and test tables.

**Type:** String
**Values:**
- **'SINGLE_TABLE'** (default): One table with partition column indicating train/test assignment
- **'SEPARATE_TABLES'**: Create two separate tables for train and test sets

**Examples:**
- `OutputType('SINGLE_TABLE')` + `PartitionColumn('dataset')` creates one table with 'dataset' column containing 'train' or 'test'
- `OutputType('SEPARATE_TABLES')` + `TrainTableName('customer_train')` + `TestTableName('customer_test')` creates two tables

**Use Cases:**
- **SINGLE_TABLE**: Simpler for downstream queries (filter by partition column)
- **SEPARATE_TABLES**: Cleaner separation, prevents accidental train/test contamination

### TrainTableName
**Required if OutputType='SEPARATE_TABLES'**. Specifies the name of the training set table.

**Type:** String (table name)
**Example:** `TrainTableName('fraud_training_set')`

### TestTableName
**Required if OutputType='SEPARATE_TABLES'**. Specifies the name of the test set table.

**Type:** String (table name)
**Example:** `TestTableName('fraud_test_set')`

### PartitionColumn
**Required if OutputType='SINGLE_TABLE'**. Specifies the name of the column that will indicate train vs. test assignment.

**Type:** String (column name)
**Default:** 'partition' if not specified
**Values:** Column will contain 'train' or 'test' (or custom values if specified)
**Example:** `PartitionColumn('dataset_type')`

## Input Specification

### InputTable Schema
```sql
-- Example: Customer churn dataset
CREATE TABLE customer_data (
    customer_id INTEGER,                -- ID column
    churn_flag INTEGER,                 -- Target variable (0/1)
    tenure_months INTEGER,              -- Feature
    monthly_charges DECIMAL(10,2),      -- Feature
    total_charges DECIMAL(10,2),        -- Feature
    contract_type VARCHAR(20),          -- Feature
    customer_segment VARCHAR(20),       -- Stratify column
    signup_date DATE                    -- Metadata
);
```

**Requirements:**
- No specific column requirements (function splits entire rows)
- Sufficient rows for meaningful split (minimum 100 rows, 1000+ recommended)
- If using StratifyColumns, stratify columns should have reasonable cardinality (<100 unique values)
- If using IDColumn, should be unique or at least stable identifier

**Best Practices:**
- Include all features and target variable in input table
- Pre-filter any data quality issues before splitting
- For time-based splits, order input data by timestamp first

## Output Specification

### Output Schema (SINGLE_TABLE mode)
```sql
-- All original columns plus partition indicator
customer_id INTEGER,
churn_flag INTEGER,
tenure_months INTEGER,
monthly_charges DECIMAL(10,2),
total_charges DECIMAL(10,2),
contract_type VARCHAR(20),
customer_segment VARCHAR(20),
signup_date DATE,
partition VARCHAR(10)           -- NEW: 'train' or 'test'
```

**Partition Column Values:**
- **'train'**: Row assigned to training set
- **'test'**: Row assigned to test set

**Usage:**
```sql
-- Use training set
SELECT * FROM customer_split WHERE partition = 'train';

-- Use test set
SELECT * FROM customer_split WHERE partition = 'test';

-- Verify split ratios
SELECT
    partition,
    COUNT(*) AS record_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM customer_split
GROUP BY partition;
```

### Output Schema (SEPARATE_TABLES mode)
**Training Table** (customer_train):
```sql
-- All original columns, only training set rows
customer_id INTEGER,
churn_flag INTEGER,
tenure_months INTEGER,
monthly_charges DECIMAL(10,2),
... (all original columns)
```

**Test Table** (customer_test):
```sql
-- All original columns, only test set rows
customer_id INTEGER,
churn_flag INTEGER,
tenure_months INTEGER,
monthly_charges DECIMAL(10,2),
... (all original columns)
```

**Usage:**
```sql
-- Train model
SELECT * FROM customer_train;

-- Evaluate model
SELECT * FROM customer_test;

-- Verify split ratios
SELECT 'train' AS dataset, COUNT(*) AS record_count FROM customer_train
UNION ALL
SELECT 'test' AS dataset, COUNT(*) AS record_count FROM customer_test;
```

**Output Characteristics:**
- **Mutually exclusive**: No overlap between train and test sets
- **Complete**: All input rows assigned to either train or test (unless TrainSize + TestSize < 1.0)
- **Random**: Assignment is pseudorandom (deterministic if Seed specified)
- **Stratified** (if StratifyColumns used): Class distributions maintained across splits

**Verification Queries:**
```sql
-- Check stratification worked (should have similar churn rates)
SELECT
    partition,
    COUNT(*) AS total,
    SUM(churn_flag) AS churners,
    ROUND(100.0 * SUM(churn_flag) / COUNT(*), 2) AS churn_rate_pct
FROM customer_split
GROUP BY partition;

-- Expected output:
-- partition | total   | churners | churn_rate_pct
-- train     | 80,000  | 2,400    | 3.00
-- test      | 20,000  | 600      | 3.00  ← Same rate!
```

## Code Examples

### Example 1: Basic Train/Test Split - Binary Classification (Fraud Detection)

**Business Context:**
A credit card company has 500,000 historical transactions with fraud labels. The data science team needs to split the data into training (80%) and test (20%) sets to develop and validate a fraud detection model. Since fraud is rare (0.5% prevalence), they must use stratified sampling to ensure both sets have similar fraud rates.

**SQL Code:**
```sql
-- Step 1: Review input data
SELECT
    COUNT(*) AS total_transactions,
    SUM(CASE WHEN fraud_flag = 1 THEN 1 ELSE 0 END) AS fraud_count,
    ROUND(100.0 * SUM(CASE WHEN fraud_flag = 1 THEN 1 ELSE 0 END) / COUNT(*), 3) AS fraud_rate_pct
FROM transaction_history;

-- Step 2: Perform stratified train/test split (80/20)
CREATE TABLE transaction_split AS (
    SELECT * FROM TD_TrainTestSplit (
        ON transaction_history AS InputTable
        USING
        TestSize(0.2)                    -- 20% test, 80% train
        StratifyColumns('fraud_flag')    -- CRITICAL: Maintain fraud rate
        Seed(42)                         -- Reproducibility
        OutputType('SINGLE_TABLE')
        PartitionColumn('dataset')
    ) AS split
) WITH DATA PRIMARY INDEX (transaction_id);

-- Step 3: Verify split ratios and stratification
SELECT
    dataset,
    COUNT(*) AS transaction_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_of_total,
    SUM(fraud_flag) AS fraud_count,
    ROUND(100.0 * SUM(fraud_flag) / COUNT(*), 3) AS fraud_rate_pct
FROM transaction_split
GROUP BY dataset
ORDER BY dataset;

-- Step 4: Create training set view
CREATE VIEW transaction_train AS
SELECT * FROM transaction_split WHERE dataset = 'train';

-- Step 5: Create test set view
CREATE VIEW transaction_test AS
SELECT * FROM transaction_split WHERE dataset = 'test';

-- Step 6: Verify no overlap between train and test
SELECT
    CASE
        WHEN (SELECT COUNT(DISTINCT transaction_id) FROM transaction_train) +
             (SELECT COUNT(DISTINCT transaction_id) FROM transaction_test) =
             (SELECT COUNT(DISTINCT transaction_id) FROM transaction_split)
        THEN 'PASS: No overlap between train and test'
        ELSE 'FAIL: Overlap detected'
    END AS validation_result;
```

**Sample Output:**
```
-- Step 1: Input data summary
total_transactions | fraud_count | fraud_rate_pct
-------------------+-------------+----------------
500,000            | 2,500       | 0.500

-- Step 3: Split verification
dataset | transaction_count | pct_of_total | fraud_count | fraud_rate_pct
--------+-------------------+--------------+-------------+----------------
train   | 400,000           | 80.00        | 2,000       | 0.500          ← Maintained!
test    | 100,000           | 20.00        | 500         | 0.500          ← Maintained!

-- Step 6: Overlap validation
validation_result
-------------------------------------
PASS: No overlap between train and test
```

**Business Impact:**
- **Stratification Success**: Both train and test sets maintain 0.5% fraud rate (critical for imbalanced classification)
- **Test Set Size**: 100,000 transactions with 500 fraud cases provides statistically reliable evaluation
- **Reproducibility**: Seed=42 ensures identical split if re-run (regulatory compliance, debugging)
- **Model Development**: Ready for training fraud detection models on 400K transactions
- **Unbiased Evaluation**: Test set (100K transactions) held out for final model validation
- **Next Steps**: Train models (Logistic Regression, XGBoost, Random Forest) on train set, evaluate on test set using TD_ROC, TD_ClassificationEvaluator

**Why Stratification Matters:**
Without stratification, random 80/20 split might produce:
- Train set: 0.48% fraud (1,920 cases)
- Test set: 0.58% fraud (580 cases)
- Different distributions → biased model evaluation
- May miss rare fraud patterns in training or testing

With stratification:
- Both sets: exactly 0.5% fraud
- Fair evaluation: Model sees representative fraud rates in both train and test
- Reliable metrics: AUC, precision, recall computed on proper distribution

---

### Example 2: Three-Way Split - Train/Validation/Test for Hyperparameter Tuning

**Business Context:**
A healthcare analytics team is building a patient readmission prediction model with hyperparameter tuning. They need three datasets: (1) Training set (60%) for model training, (2) Validation set (20%) for hyperparameter selection, (3) Test set (20%) for final unbiased evaluation. They want separate tables for clean workflow separation.

**SQL Code:**
```sql
-- Step 1: Create initial 60/40 split (train vs. validation+test)
CREATE TABLE patient_train AS (
    SELECT * FROM TD_TrainTestSplit (
        ON patient_admissions AS InputTable
        USING
        TestSize(0.4)                        -- 40% for validation+test
        StratifyColumns('readmit_30day')     -- Stratify on target variable
        Seed(123)
        OutputType('SINGLE_TABLE')
        PartitionColumn('initial_split')
    ) AS split
) WITH DATA;

-- Step 2: Extract training set (60% of original)
CREATE TABLE patient_training_final AS (
    SELECT * FROM patient_train
    WHERE initial_split = 'train'
) WITH DATA PRIMARY INDEX (patient_id);

-- Step 3: Split the 40% remainder into validation (50% of 40% = 20% of original) and test (50% of 40% = 20% of original)
CREATE TABLE patient_validation_test AS (
    SELECT * FROM TD_TrainTestSplit (
        ON (SELECT * FROM patient_train WHERE initial_split = 'test') AS InputTable
        USING
        TestSize(0.5)                        -- 50% of 40% = 20% of original
        StratifyColumns('readmit_30day')
        Seed(456)                            -- Different seed for second split
        OutputType('SINGLE_TABLE')
        PartitionColumn('final_split')
    ) AS split
) WITH DATA;

-- Step 4: Extract validation set (20% of original)
CREATE TABLE patient_validation AS (
    SELECT * FROM patient_validation_test
    WHERE final_split = 'train'              -- First half of 40% = validation
) WITH DATA PRIMARY INDEX (patient_id);

-- Step 5: Extract test set (20% of original)
CREATE TABLE patient_test AS (
    SELECT * FROM patient_validation_test
    WHERE final_split = 'test'               -- Second half of 40% = test
) WITH DATA PRIMARY INDEX (patient_id);

-- Step 6: Verify three-way split ratios and stratification
SELECT
    'Training' AS dataset,
    COUNT(*) AS patient_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM patient_admissions), 2) AS pct_of_original,
    SUM(readmit_30day) AS readmit_count,
    ROUND(100.0 * SUM(readmit_30day) / COUNT(*), 2) AS readmit_rate_pct
FROM patient_training_final

UNION ALL

SELECT
    'Validation' AS dataset,
    COUNT(*) AS patient_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM patient_admissions), 2) AS pct_of_original,
    SUM(readmit_30day) AS readmit_count,
    ROUND(100.0 * SUM(readmit_30day) / COUNT(*), 2) AS readmit_rate_pct
FROM patient_validation

UNION ALL

SELECT
    'Test' AS dataset,
    COUNT(*) AS patient_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM patient_admissions), 2) AS pct_of_original,
    SUM(readmit_30day) AS readmit_count,
    ROUND(100.0 * SUM(readmit_30day) / COUNT(*), 2) AS readmit_rate_pct
FROM patient_test

ORDER BY patient_count DESC;

-- Step 7: Verify no overlap across all three sets
SELECT
    CASE
        WHEN (SELECT COUNT(DISTINCT patient_id) FROM patient_training_final) +
             (SELECT COUNT(DISTINCT patient_id) FROM patient_validation) +
             (SELECT COUNT(DISTINCT patient_id) FROM patient_test) =
             (SELECT COUNT(DISTINCT patient_id) FROM patient_admissions)
        THEN 'PASS: No overlap across train/validation/test'
        ELSE 'FAIL: Overlap or missing patients detected'
    END AS validation_result;
```

**Sample Output:**
```
-- Three-way split verification:
dataset    | patient_count | pct_of_original | readmit_count | readmit_rate_pct
-----------+---------------+-----------------+---------------+------------------
Training   | 60,000        | 60.00           | 9,000         | 15.00
Validation | 20,000        | 20.00           | 3,000         | 15.00
Test       | 20,000        | 20.00           | 3,000         | 15.00

-- Overlap validation:
validation_result
-----------------------------------------------
PASS: No overlap across train/validation/test
```

**Business Impact:**

**Workflow Separation:**
1. **Training Set (60% = 60,000 patients):**
   - Used for model training across multiple algorithms (Logistic Regression, XGBoost, Neural Network)
   - All hyperparameter configurations trained on this set
   - 9,000 readmissions for learning patterns

2. **Validation Set (20% = 20,000 patients):**
   - Used for hyperparameter tuning (learning rate, max depth, regularization)
   - Model selection among different configurations
   - Select best model variant without touching test set
   - 3,000 readmissions for hyperparameter optimization

3. **Test Set (20% = 20,000 patients):**
   - **UNTOUCHED** until final evaluation
   - Used once after model and hyperparameters finalized
   - Provides unbiased performance estimate for deployment decision
   - 3,000 readmissions for final validation

**Why Three-Way Split?**
- **Problem with two-way split**: If you tune hyperparameters on test set, it becomes contaminated (no longer "unseen")
- **Solution**: Validation set absorbs hyperparameter tuning contamination, preserving test set purity
- **Best practice**: Test set used exactly once for final GO/NO-GO deployment decision

**Hyperparameter Tuning Workflow:**
```sql
-- Train 100 different XGBoost configurations on training set
-- Evaluate each on validation set
-- Select config with best validation AUC

-- Example: Hyperparameter grid search
FOR each learning_rate IN (0.01, 0.05, 0.1)
FOR each max_depth IN (3, 5, 7, 10)
FOR each min_child_weight IN (1, 3, 5)
    -- Train on patient_training_final
    -- Evaluate on patient_validation
    -- Record validation AUC
END FOR

-- Select best config (e.g., learning_rate=0.05, max_depth=7, min_child_weight=3)
-- Train final model with best config on patient_training_final
-- Evaluate ONCE on patient_test for unbiased estimate
```

**Stratification Success:**
- All three sets maintain 15% readmission rate
- Ensures fair comparison across hyperparameter configs
- Prevents bias from dataset composition differences

**Alternative Approach - Combined Train+Validation:**
After hyperparameter selection, optionally retrain on combined train+validation (80% total) before final test evaluation:
```sql
CREATE TABLE patient_train_validation_combined AS (
    SELECT * FROM patient_training_final
    UNION ALL
    SELECT * FROM patient_validation
) WITH DATA;

-- Retrain best model on 80% data
-- Evaluate on test set (20%)
-- Often improves performance by 1-3% due to more training data
```

---

### Example 3: Time-Based Split - Avoiding Temporal Leakage in Forecasting

**Business Context:**
A retail company wants to build a sales forecasting model. Using random train/test split would cause **temporal leakage** (training on future data, testing on past data). Instead, they need time-based split: train on historical data (Jan 2020 - Dec 2023), test on recent data (Jan 2024 - Jun 2024) to simulate real-world forecasting scenario.

**SQL Code:**
```sql
-- Step 1: Review temporal distribution
SELECT
    EXTRACT(YEAR FROM sale_date) AS sale_year,
    EXTRACT(MONTH FROM sale_date) AS sale_month,
    COUNT(*) AS transaction_count,
    SUM(sale_amount) AS total_sales
FROM retail_sales
GROUP BY sale_year, sale_month
ORDER BY sale_year, sale_month;

-- Step 2: Time-based split (NO RANDOM SAMPLING - split by date)
-- Training: Jan 2020 - Dec 2023 (4 years)
-- Test: Jan 2024 - Jun 2024 (6 months)

CREATE TABLE retail_sales_split AS (
    SELECT
        *,
        CASE
            WHEN sale_date < DATE '2024-01-01' THEN 'train'
            ELSE 'test'
        END AS dataset
    FROM retail_sales
) WITH DATA PRIMARY INDEX (transaction_id);

-- Alternative: Use TD_TrainTestSplit with pre-sorted data and precise split point
-- First, calculate split point (e.g., 87.5% for 4 years train, 0.5 years test out of 4.5 years total)
CREATE TABLE retail_sales_sorted AS (
    SELECT
        *,
        ROW_NUMBER() OVER (ORDER BY sale_date) AS temporal_order
    FROM retail_sales
) WITH DATA;

-- Calculate TestSize as fraction of most recent data
-- 4.5 years total, 0.5 years test = 0.5/4.5 = 0.111 (11.1%)
CREATE TABLE retail_sales_timesplit AS (
    SELECT * FROM TD_TrainTestSplit (
        ON (SELECT * FROM retail_sales ORDER BY sale_date) AS InputTable
        USING
        TestSize(0.111)                  -- Most recent 11.1% (6 months out of 4.5 years)
        Seed(42)                         -- For reproducibility
        OutputType('SINGLE_TABLE')
        PartitionColumn('dataset')
    ) AS split
) WITH DATA;

-- Step 3: Verify temporal separation (training set should not have dates after test set minimum)
SELECT
    dataset,
    COUNT(*) AS transaction_count,
    MIN(sale_date) AS earliest_date,
    MAX(sale_date) AS latest_date,
    ROUND(SUM(sale_amount), 2) AS total_sales
FROM retail_sales_split
GROUP BY dataset
ORDER BY dataset;

-- Step 4: Check for temporal leakage (should return 0 rows)
SELECT
    'LEAKAGE DETECTED' AS alert,
    COUNT(*) AS leakage_count
FROM retail_sales_split
WHERE dataset = 'train'
  AND sale_date >= (SELECT MIN(sale_date) FROM retail_sales_split WHERE dataset = 'test')
HAVING COUNT(*) > 0;

-- Step 5: Create lagged features for time series (avoiding leakage)
CREATE TABLE retail_sales_features AS (
    SELECT
        transaction_id,
        sale_date,
        sale_amount,
        product_category,
        store_id,
        dataset,
        -- Lagged features (using only data up to sale_date)
        AVG(sale_amount) OVER (
            PARTITION BY store_id
            ORDER BY sale_date
            ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING
        ) AS avg_sales_last_30days,
        SUM(sale_amount) OVER (
            PARTITION BY product_category
            ORDER BY sale_date
            ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING
        ) AS category_sales_last_7days
    FROM retail_sales_split
) WITH DATA;

-- Step 6: Verify feature engineering doesn't leak future information
-- Check that training set features only use training set data
SELECT
    'Feature Leakage Check' AS test_name,
    CASE
        WHEN MAX(sale_date) <= DATE '2023-12-31'
        THEN 'PASS: Training features use only historical data'
        ELSE 'FAIL: Training features may use test set data'
    END AS result
FROM retail_sales_features
WHERE dataset = 'train'
  AND avg_sales_last_30days IS NOT NULL;
```

**Sample Output:**
```
-- Temporal distribution:
sale_year | sale_month | transaction_count | total_sales
----------+------------+-------------------+-------------
2020      | 1          | 45,678            | $2,345,678
2020      | 2          | 43,234            | $2,234,567
...
2023      | 12         | 67,890            | $3,456,789
2024      | 1          | 68,234            | $3,512,345
2024      | 2          | 69,123            | $3,567,890
2024      | 6          | 72,456            | $3,678,901

-- Temporal separation verification:
dataset | transaction_count | earliest_date | latest_date | total_sales
--------+-------------------+---------------+-------------+-------------
train   | 2,456,789         | 2020-01-01    | 2023-12-31  | $1.2B
test    | 412,345           | 2024-01-01    | 2024-06-30  | $210M

-- Temporal leakage check:
(0 rows returned) ← GOOD! No leakage detected

-- Feature leakage check:
test_name              | result
-----------------------+-----------------------------------------------
Feature Leakage Check  | PASS: Training features use only historical data
```

**Business Impact:**

**Why Time-Based Split is Critical:**
- **Simulates Production**: In production, model trained on past data predicts future (exactly like this split)
- **Avoids Temporal Leakage**: Random split would train on 2024 data, test on 2020 data (unrealistic)
- **Realistic Performance**: Test set performance reflects true forecasting accuracy

**Example of Temporal Leakage (WRONG):**
```sql
-- BAD: Random split for time series
CREATE TABLE retail_sales_bad_split AS (
    SELECT * FROM TD_TrainTestSplit (
        ON retail_sales AS InputTable
        USING
        TestSize(0.2)
        Seed(42)
    ) AS split
) WITH DATA;

-- Result: Training set has 2024 data, test set has 2020 data
-- Model learns from "future" to predict "past" - artificially high accuracy!
-- Deployment failure: Real-world performance much worse than test set
```

**Feature Engineering Without Leakage:**
- **Lagged Features**: avg_sales_last_30days uses only data BEFORE sale_date
- **Rolling Windows**: Use ROWS BETWEEN X PRECEDING AND 1 PRECEDING (never include current row or future)
- **No Future Information**: Training features computed using only data available at training time

**Model Development Workflow:**
1. **Train models** on retail_sales_features WHERE dataset = 'train' (Jan 2020 - Dec 2023)
2. **Generate predictions** for retail_sales_features WHERE dataset = 'test' (Jan 2024 - Jun 2024)
3. **Evaluate accuracy** using TD_RegressionEvaluator (MAE, RMSE, MAPE)
4. **Deploy model** if test set MAPE < 10% (business requirement)

**Deployment Simulation:**
- **Scenario**: It's January 1, 2024. Model trained on 2020-2023 data.
- **Question**: Can model accurately forecast sales for Jan-Jun 2024?
- **Test Set**: Provides answer by evaluating on actual Jan-Jun 2024 data
- **Decision**: Deploy if forecasting accuracy acceptable

**Walk-Forward Validation (Advanced):**
For even more rigorous evaluation, use multiple time-based splits:
```sql
-- Split 1: Train on 2020-2022, test on 2023
-- Split 2: Train on 2020-2023, test on 2024 Q1
-- Split 3: Train on 2020-2023 + 2024 Q1, test on 2024 Q2
-- Average performance across splits for robust estimate
```

---

### Example 4: Stratified Multi-Class Split - Customer Segmentation

**Business Context:**
A bank has 200,000 customers segmented into 4 groups: High_Value (5%), Medium_Value (35%), Low_Value (50%), At_Risk (10%). They're building classification models to predict segment transitions. They need stratified split maintaining segment distribution across train/test sets for fair multi-class evaluation.

**SQL Code:**
```sql
-- Step 1: Review segment distribution
SELECT
    current_segment,
    COUNT(*) AS customer_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_of_total
FROM customer_base
GROUP BY current_segment
ORDER BY customer_count DESC;

-- Step 2: Stratified train/test split (70/30)
CREATE TABLE customer_segment_split AS (
    SELECT * FROM TD_TrainTestSplit (
        ON customer_base AS InputTable
        USING
        TestSize(0.3)                        -- 30% test, 70% train
        StratifyColumns('current_segment')   -- Maintain segment distribution
        Seed(789)
        OutputType('SINGLE_TABLE')
        PartitionColumn('dataset')
    ) AS split
) WITH DATA PRIMARY INDEX (customer_id);

-- Step 3: Verify stratification across segments
SELECT
    dataset,
    current_segment,
    COUNT(*) AS customer_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY dataset), 2) AS pct_within_dataset
FROM customer_segment_split
GROUP BY dataset, current_segment
ORDER BY dataset, customer_count DESC;

-- Step 4: Compare distributions (pivot view)
SELECT
    current_segment,
    SUM(CASE WHEN dataset = 'train' THEN 1 ELSE 0 END) AS train_count,
    SUM(CASE WHEN dataset = 'test' THEN 1 ELSE 0 END) AS test_count,
    ROUND(100.0 * SUM(CASE WHEN dataset = 'train' THEN 1 ELSE 0 END) / SUM(1), 2) AS train_pct,
    ROUND(100.0 * SUM(CASE WHEN dataset = 'test' THEN 1 ELSE 0 END) / SUM(1), 2) AS test_pct,
    -- Verify distributions match
    ROUND(100.0 * SUM(CASE WHEN dataset = 'train' THEN 1 ELSE 0 END) / SUM(SUM(1)) OVER (), 2) AS train_segment_pct,
    ROUND(100.0 * SUM(CASE WHEN dataset = 'test' THEN 1 ELSE 0 END) / SUM(SUM(1)) OVER (), 2) AS test_segment_pct
FROM customer_segment_split
GROUP BY current_segment
ORDER BY train_count + test_count DESC;

-- Step 5: Verify sufficient samples per segment (minimum 100 per segment for reliable evaluation)
SELECT
    current_segment,
    dataset,
    COUNT(*) AS sample_count,
    CASE
        WHEN COUNT(*) >= 100 THEN 'SUFFICIENT'
        WHEN COUNT(*) >= 50 THEN 'MARGINAL'
        ELSE 'INSUFFICIENT'
    END AS sample_adequacy
FROM customer_segment_split
GROUP BY current_segment, dataset
HAVING sample_adequacy != 'SUFFICIENT'
ORDER BY sample_count ASC;
```

**Sample Output:**
```
-- Step 1: Original segment distribution
current_segment | customer_count | pct_of_total
----------------+----------------+--------------
Low_Value       | 100,000        | 50.00
Medium_Value    | 70,000         | 35.00
At_Risk         | 20,000         | 10.00
High_Value      | 10,000         | 5.00

-- Step 3: Stratified distribution verification
dataset | current_segment | customer_count | pct_within_dataset
--------+-----------------+----------------+--------------------
train   | Low_Value       | 70,000         | 50.00              ← Maintained!
train   | Medium_Value    | 49,000         | 35.00              ← Maintained!
train   | At_Risk         | 14,000         | 10.00              ← Maintained!
train   | High_Value      | 7,000          | 5.00               ← Maintained!
test    | Low_Value       | 30,000         | 50.00              ← Maintained!
test    | Medium_Value    | 21,000         | 35.00              ← Maintained!
test    | At_Risk         | 6,000          | 10.00              ← Maintained!
test    | High_Value      | 3,000          | 5.00               ← Maintained!

-- Step 4: Pivot comparison
current_segment | train_count | test_count | train_pct | test_pct | train_segment_pct | test_segment_pct
----------------+-------------+------------+-----------+----------+-------------------+------------------
Low_Value       | 70,000      | 30,000     | 70.00     | 30.00    | 50.00             | 50.00
Medium_Value    | 49,000      | 21,000     | 70.00     | 30.00    | 35.00             | 35.00
At_Risk         | 14,000      | 6,000      | 70.00     | 30.00    | 10.00             | 10.00
High_Value      | 7,000       | 3,000      | 70.00     | 30.00    | 5.00              | 5.00

-- Step 5: Sample adequacy check
(0 rows returned) ← All segments have >100 samples in both train and test - SUFFICIENT!
```

**Business Impact:**

**Stratification Success:**
- **Perfect Distribution Maintenance**: Each segment maintains exact 50%/35%/10%/5% distribution in both train and test
- **Fair Multi-Class Evaluation**: Model performance metrics (precision, recall, F1) computed on representative test set
- **Prevents Bias**: Without stratification, test set might under-represent High_Value (5%) or At_Risk (10%) segments

**Example Without Stratification (WRONG):**
```sql
-- BAD: Non-stratified split
CREATE TABLE customer_bad_split AS (
    SELECT * FROM TD_TrainTestSplit (
        ON customer_base AS InputTable
        USING
        TestSize(0.3)
        Seed(789)
        -- NO StratifyColumns!
    ) AS split
) WITH DATA;

-- Potential result: Imbalanced distributions
-- Train: 48% Low_Value, 37% Medium_Value, 10% At_Risk, 5% High_Value
-- Test: 55% Low_Value, 30% Medium_Value, 9% At_Risk, 6% High_Value
-- Model evaluation biased toward Low_Value segment performance
-- High_Value segment may have only 1,800 test samples (insufficient for 5-class problem)
```

**Sample Size Analysis:**
- **High_Value**: 3,000 test samples (5% of 60,000) - Sufficient for reliable evaluation
- **At_Risk**: 6,000 test samples (10% of 60,000) - Good sample size
- **Medium_Value**: 21,000 test samples - Excellent
- **Low_Value**: 30,000 test samples - Excellent

**Model Development Workflow:**
1. **Train multi-class classifiers** on train set (140,000 customers)
   - Logistic Regression (one-vs-rest or multinomial)
   - Random Forest with 4 classes
   - XGBoost multi-class classifier

2. **Evaluate on test set** (60,000 customers) using TD_ClassificationEvaluator
   - Class-level metrics: Precision, recall, F1 for each segment
   - Confusion matrix: Which segment transitions are hardest to predict?
   - Overall accuracy and macro/micro/weighted averages

3. **Segment-specific insights:**
   - High_Value precision: Are we correctly identifying high-value customers?
   - At_Risk recall: Are we catching customers at risk of churning?
   - Low_Value → Medium_Value transitions: Can we predict upsell opportunities?

**Business Use Cases:**
- **Retention**: Predict At_Risk customers for proactive retention campaigns
- **Upsell**: Identify Low_Value → Medium_Value transition candidates
- **VIP Management**: Validate High_Value customer identification
- **Resource Allocation**: Allocate relationship managers based on predicted segments

**Fairness Consideration:**
If segments correlate with protected demographics, stratification ensures fair model evaluation across groups:
```sql
-- Check for demographic correlations with segments
SELECT
    current_segment,
    age_group,
    COUNT(*) AS customer_count
FROM customer_segment_split
WHERE dataset = 'train'
GROUP BY current_segment, age_group
ORDER BY current_segment, age_group;

-- If High_Value skews toward older customers, stratification ensures
-- both train and test have representative age distributions within High_Value segment
```

---

### Example 5: Separate Tables Output - Clean Workflow Isolation

**Business Context:**
A pharmaceutical company is developing a drug response prediction model. They want completely separate train and test tables to ensure strict workflow isolation: data scientists work only with train table during development, test table locked until final validation. This prevents accidental test set contamination during exploratory analysis.

**SQL Code:**
```sql
-- Step 1: Create separate train and test tables with stratification
-- Stratify on response_label to maintain responder/non-responder ratio
SELECT * FROM TD_TrainTestSplit (
    ON clinical_trial_data AS InputTable
    USING
    TestSize(0.25)                           -- 25% test, 75% train
    StratifyColumns('response_label', 'disease_severity')  -- Multi-variable stratification
    Seed(2024)
    OutputType('SEPARATE_TABLES')            -- Create two separate tables
    TrainTableName('clinical_train')
    TestTableName('clinical_test')
) AS split;

-- Step 2: Verify tables created successfully
SELECT 'clinical_train' AS table_name, COUNT(*) AS patient_count FROM clinical_train
UNION ALL
SELECT 'clinical_test' AS table_name, COUNT(*) AS patient_count FROM clinical_test;

-- Step 3: Verify stratification on both variables
SELECT
    'Train Set' AS dataset,
    response_label,
    disease_severity,
    COUNT(*) AS patient_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY response_label), 2) AS pct_within_response
FROM clinical_train
GROUP BY response_label, disease_severity

UNION ALL

SELECT
    'Test Set' AS dataset,
    response_label,
    disease_severity,
    COUNT(*) AS patient_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY response_label), 2) AS pct_within_response
FROM clinical_test
GROUP BY response_label, disease_severity

ORDER BY response_label, disease_severity, dataset;

-- Step 4: Apply access controls (restrict test table access during development)
-- Grant full access to train table
GRANT SELECT ON clinical_train TO data_science_team;
GRANT SELECT, UPDATE, DELETE, INSERT ON clinical_train TO data_science_team;

-- Restrict test table access (read-only, only for senior data scientists)
GRANT SELECT ON clinical_test TO senior_data_scientists;
REVOKE ALL ON clinical_test FROM data_science_team;

-- Step 5: Create development views with additional transformations (train only)
CREATE VIEW clinical_train_transformed AS
SELECT
    patient_id,
    response_label,
    disease_severity,
    -- Feature engineering (applied only to train during development)
    CASE
        WHEN age < 18 THEN 'Pediatric'
        WHEN age BETWEEN 18 AND 64 THEN 'Adult'
        ELSE 'Senior'
    END AS age_group,
    CASE
        WHEN baseline_score < 50 THEN 'Low'
        WHEN baseline_score BETWEEN 50 AND 75 THEN 'Medium'
        ELSE 'High'
    END AS baseline_category,
    -- Derived features
    days_since_diagnosis,
    prior_treatment_count,
    comorbidity_count
FROM clinical_train;

-- Step 6: Verify no patient overlap between train and test (critical for clinical trials)
SELECT
    CASE
        WHEN EXISTS (
            SELECT 1
            FROM clinical_train t
            INNER JOIN clinical_test ts ON t.patient_id = ts.patient_id
        )
        THEN 'FAIL: Patient overlap detected between train and test!'
        ELSE 'PASS: No patient overlap - clean separation'
    END AS separation_validation;

-- Step 7: Lock test table until final validation (workflow control)
-- Rename test table to indicate it's locked
ALTER TABLE clinical_test RENAME TO clinical_test_LOCKED_UNTIL_FINAL_VALIDATION;

-- Create placeholder view preventing accidental access
CREATE VIEW clinical_test AS
SELECT
    'Test set locked until final model validation' AS message,
    'Contact senior data scientist for access' AS instructions
    CAST(NULL AS INTEGER) AS patient_id
WHERE 1=0;  -- Returns no rows, prevents data access
```

**Sample Output:**
```
-- Table creation verification:
table_name      | patient_count
----------------+---------------
clinical_train  | 7,500
clinical_test   | 2,500

-- Stratification verification:
dataset  | response_label | disease_severity | patient_count | pct_within_response
---------+----------------+------------------+---------------+---------------------
Train Set| Responder      | Mild             | 1,875         | 50.00
Train Set| Responder      | Moderate         | 1,125         | 30.00
Train Set| Responder      | Severe           | 750           | 20.00
Test Set | Responder      | Mild             | 625           | 50.00               ← Same!
Test Set | Responder      | Moderate         | 375           | 30.00               ← Same!
Test Set | Responder      | Severe           | 250           | 20.00               ← Same!
Train Set| Non-Responder  | Mild             | 1,875         | 50.00
Train Set| Non-Responder  | Moderate         | 1,125         | 30.00
Train Set| Non-Responder  | Severe           | 750           | 20.00
Test Set | Non-Responder  | Mild             | 625           | 50.00               ← Same!
Test Set | Non-Responder  | Moderate         | 375           | 30.00               ← Same!
Test Set | Non-Responder  | Severe           | 250           | 20.00               ← Same!

-- Separation validation:
separation_validation
--------------------------------------------
PASS: No patient overlap - clean separation
```

**Business Impact:**

**Workflow Isolation Benefits:**
1. **Prevents Accidental Contamination:**
   - Data scientists cannot accidentally query test set during exploration
   - Test table locked with restricted permissions
   - Placeholder view prevents inadvertent SELECT * FROM clinical_test

2. **Regulatory Compliance:**
   - FDA requires strict separation of training and validation data for drug approval models
   - Access controls provide audit trail (who accessed test set and when)
   - Documented workflow prevents "peeking" at test set during development

3. **Scientific Rigor:**
   - Test set truly held-out: never used for feature engineering, model selection, or hyperparameter tuning
   - One-time test evaluation after model finalized
   - Prevents optimistic bias from repeated test set evaluation

**Multi-Variable Stratification:**
- **StratifyColumns('response_label', 'disease_severity')**: Maintains BOTH distributions
- Ensures train and test have:
  - Same responder/non-responder ratio (e.g., 50%/50%)
  - Same disease severity distribution within each response group (50% Mild, 30% Moderate, 20% Severe)
- Critical for clinical trials where response rates vary by disease severity

**Development Workflow:**
1. **Weeks 1-4**: Exploratory data analysis on clinical_train only
2. **Weeks 5-8**: Feature engineering, model training, validation set creation from clinical_train
3. **Weeks 9-10**: Hyperparameter tuning using k-fold CV on clinical_train
4. **Week 11**: Final model selected, ready for test evaluation
5. **Week 12**: Test set unlocked, single evaluation on clinical_test_LOCKED_UNTIL_FINAL_VALIDATION
6. **Week 12**: Results documented, deployment decision made

**Access Control Implementation:**
```sql
-- Example: Log test set access for audit trail
CREATE TABLE test_set_access_log (
    access_timestamp TIMESTAMP,
    user_name VARCHAR(50),
    query_text VARCHAR(5000),
    records_returned INTEGER
);

-- Trigger to log all test set queries (if supported by Teradata)
-- Alternative: Database audit logging for clinical_test_LOCKED table
```

**Preventing Common Mistakes:**
- **Mistake 1**: Repeatedly evaluating on test set during development
  - **Prevention**: Lock test table, use validation set from clinical_train for iterative evaluation

- **Mistake 2**: Feature engineering using full dataset statistics
  - **Prevention**: Compute statistics (means, std devs) only from clinical_train, apply to both train and test

- **Mistake 3**: Accidentally joining test data during training
  - **Prevention**: Separate tables physically isolate datasets

**Final Test Evaluation:**
```sql
-- After model finalized, unlock test set for one-time evaluation
ALTER TABLE clinical_test_LOCKED_UNTIL_FINAL_VALIDATION RENAME TO clinical_test_final;

-- Apply same transformations to test set (using parameters learned from train only)
CREATE VIEW clinical_test_transformed AS
SELECT
    patient_id,
    response_label,
    -- Apply SAME transformations as training (using train-derived thresholds)
    CASE WHEN age < 18 THEN 'Pediatric' WHEN age BETWEEN 18 AND 64 THEN 'Adult' ELSE 'Senior' END AS age_group,
    CASE WHEN baseline_score < 50 THEN 'Low' WHEN baseline_score BETWEEN 50 AND 75 THEN 'Medium' ELSE 'High' END AS baseline_category,
    days_since_diagnosis,
    prior_treatment_count,
    comorbidity_count
FROM clinical_test_final;

-- Generate predictions on test set
-- (use trained model from clinical_train)

-- Evaluate performance ONE TIME
SELECT * FROM TD_ClassificationEvaluator (
    ON test_predictions AS InputTable
    USING
    ObservationColumn('response_label')
    PredictionColumn('predicted_response')
    NumLabels(2)
) AS eval;

-- Document results, make deployment decision
-- If test AUC >= 0.75: Approve for clinical implementation
-- If test AUC < 0.75: Reject model, return to development
```

---

### Example 6: Cross-Validation Setup - K-Fold Split Preparation

**Business Context:**
A machine learning team needs to perform 5-fold cross-validation on a customer churn dataset (50,000 customers) for robust model evaluation. While TD_TrainTestSplit creates a single train/test split, they can use it iteratively to create 5 stratified folds for cross-validation, then compute average performance across folds.

**SQL Code:**
```sql
-- Step 1: Create 5 stratified folds using successive splits
-- Fold assignment strategy: Split into 5 equal parts (20% each) with stratification

-- First, add fold assignment column
CREATE TABLE customer_churn_folds AS (
    SELECT
        *,
        CAST(NULL AS INTEGER) AS fold_number
    FROM customer_churn_data
) WITH DATA PRIMARY INDEX (customer_id);

-- Assign fold 1 (20%)
UPDATE customer_churn_folds
SET fold_number = 1
WHERE customer_id IN (
    SELECT customer_id FROM TD_TrainTestSplit (
        ON (SELECT * FROM customer_churn_data) AS InputTable
        USING
        TestSize(0.2)
        StratifyColumns('churn_flag')
        Seed(1)
        OutputType('SINGLE_TABLE')
        PartitionColumn('dataset')
    ) AS split
    WHERE dataset = 'test'
);

-- Assign fold 2 (25% of remaining 80% = 20% of total)
UPDATE customer_churn_folds
SET fold_number = 2
WHERE fold_number IS NULL
  AND customer_id IN (
    SELECT customer_id FROM TD_TrainTestSplit (
        ON (SELECT * FROM customer_churn_folds WHERE fold_number IS NULL) AS InputTable
        USING
        TestSize(0.25)  -- 25% of remaining 80% = 20% of original
        StratifyColumns('churn_flag')
        Seed(2)
        OutputType('SINGLE_TABLE')
        PartitionColumn('dataset')
    ) AS split
    WHERE dataset = 'test'
);

-- Assign fold 3 (33.3% of remaining 60% = 20% of total)
UPDATE customer_churn_folds
SET fold_number = 3
WHERE fold_number IS NULL
  AND customer_id IN (
    SELECT customer_id FROM TD_TrainTestSplit (
        ON (SELECT * FROM customer_churn_folds WHERE fold_number IS NULL) AS InputTable
        USING
        TestSize(0.333)  -- 33.3% of remaining 60% = 20% of original
        StratifyColumns('churn_flag')
        Seed(3)
        OutputType('SINGLE_TABLE')
        PartitionColumn('dataset')
    ) AS split
    WHERE dataset = 'test'
);

-- Assign fold 4 (50% of remaining 40% = 20% of total)
UPDATE customer_churn_folds
SET fold_number = 4
WHERE fold_number IS NULL
  AND customer_id IN (
    SELECT customer_id FROM TD_TrainTestSplit (
        ON (SELECT * FROM customer_churn_folds WHERE fold_number IS NULL) AS InputTable
        USING
        TestSize(0.5)  -- 50% of remaining 40% = 20% of original
        StratifyColumns('churn_flag')
        Seed(4)
        OutputType('SINGLE_TABLE')
        PartitionColumn('dataset')
    ) AS split
    WHERE dataset = 'test'
);

-- Assign fold 5 (remaining 20%)
UPDATE customer_churn_folds
SET fold_number = 5
WHERE fold_number IS NULL;

-- Step 2: Verify fold sizes and stratification
SELECT
    fold_number,
    COUNT(*) AS customer_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_of_total,
    SUM(churn_flag) AS churner_count,
    ROUND(100.0 * SUM(churn_flag) / COUNT(*), 2) AS churn_rate_pct
FROM customer_churn_folds
GROUP BY fold_number
ORDER BY fold_number;

-- Step 3: Cross-validation workflow - Fold 1 as test, Folds 2-5 as train
-- (Repeat for each fold)

-- Fold 1 iteration:
CREATE VIEW cv_fold1_train AS SELECT * FROM customer_churn_folds WHERE fold_number != 1;
CREATE VIEW cv_fold1_test AS SELECT * FROM customer_churn_folds WHERE fold_number = 1;

-- Train model on cv_fold1_train (40,000 customers)
-- Evaluate on cv_fold1_test (10,000 customers)
-- Record AUC, precision, recall

-- Fold 2 iteration:
CREATE VIEW cv_fold2_train AS SELECT * FROM customer_churn_folds WHERE fold_number != 2;
CREATE VIEW cv_fold2_test AS SELECT * FROM customer_churn_folds WHERE fold_number = 2;

-- Repeat for folds 3, 4, 5...

-- Step 4: Aggregate cross-validation results
CREATE TABLE cv_results (
    fold_number INTEGER,
    auc FLOAT,
    precision FLOAT,
    recall FLOAT,
    f1_score FLOAT
);

-- (Insert results from each fold iteration)
INSERT INTO cv_results VALUES
(1, 0.8523, 0.7234, 0.6845, 0.7032),
(2, 0.8612, 0.7456, 0.7012, 0.7228),
(3, 0.8478, 0.7123, 0.6923, 0.7021),
(4, 0.8567, 0.7345, 0.6956, 0.7143),
(5, 0.8534, 0.7289, 0.6889, 0.7083);

-- Step 5: Compute cross-validation statistics
SELECT
    'Cross-Validation Summary' AS metric,
    ROUND(AVG(auc), 4) AS mean_auc,
    ROUND(STDDEV_SAMP(auc), 4) AS std_auc,
    ROUND(AVG(precision), 4) AS mean_precision,
    ROUND(AVG(recall), 4) AS mean_recall,
    ROUND(AVG(f1_score), 4) AS mean_f1,
    -- 95% confidence interval for AUC
    ROUND(AVG(auc) - 1.96 * STDDEV_SAMP(auc) / SQRT(5), 4) AS auc_ci_lower,
    ROUND(AVG(auc) + 1.96 * STDDEV_SAMP(auc) / SQRT(5), 4) AS auc_ci_upper
FROM cv_results;

-- Step 6: Compare cross-validation to single train/test split
CREATE TABLE single_split_result AS (
    SELECT * FROM TD_TrainTestSplit (
        ON customer_churn_data AS InputTable
        USING
        TestSize(0.2)
        StratifyColumns('churn_flag')
        Seed(999)
        OutputType('SINGLE_TABLE')
        PartitionColumn('dataset')
    ) AS split
) WITH DATA;

-- Train and evaluate on single split
-- Compare single split AUC to cross-validation mean AUC
SELECT
    'Single Split' AS evaluation_type,
    0.8612 AS auc,  -- (example result from single split)
    NULL AS std_auc,
    'May be optimistic or pessimistic due to lucky/unlucky split' AS note
UNION ALL
SELECT
    '5-Fold CV' AS evaluation_type,
    0.8543 AS auc,  -- (mean from cross-validation)
    0.0053 AS std_auc,  -- (standard deviation across folds)
    'More robust estimate, averaged over 5 different train/test splits' AS note;
```

**Sample Output:**
```
-- Fold verification:
fold_number | customer_count | pct_of_total | churner_count | churn_rate_pct
------------+----------------+--------------+---------------+----------------
1           | 10,000         | 20.00        | 1,500         | 15.00          ← Equal sizes
2           | 10,000         | 20.00        | 1,500         | 15.00          ← Equal churn rates
3           | 10,000         | 20.00        | 1,500         | 15.00
4           | 10,000         | 20.00        | 1,500         | 15.00
5           | 10,000         | 20.00        | 1,500         | 15.00

-- Cross-validation summary:
metric                      | mean_auc | std_auc | mean_precision | mean_recall | mean_f1 | auc_ci_lower | auc_ci_upper
----------------------------+----------+---------+----------------+-------------+---------+--------------+--------------
Cross-Validation Summary    | 0.8543   | 0.0053  | 0.7289         | 0.6925      | 0.7101  | 0.8497       | 0.8589

-- Single split vs. cross-validation comparison:
evaluation_type | auc    | std_auc | note
----------------+--------+---------+--------------------------------------------------------------
Single Split    | 0.8612 | NULL    | May be optimistic or pessimistic due to lucky/unlucky split
5-Fold CV       | 0.8543 | 0.0053  | More robust estimate, averaged over 5 different train/test splits
```

**Business Impact:**

**Cross-Validation Advantages:**
1. **Robust Performance Estimate:**
   - Single split AUC = 0.8612 might be optimistic (lucky test set)
   - CV mean AUC = 0.8543 ± 0.0053 (95% CI: 0.8497 - 0.8589) is more reliable
   - Standard deviation = 0.0053 indicates stable model (low variance across folds)

2. **Efficient Data Usage:**
   - Every customer used for testing exactly once
   - Every customer used for training 4 times (80% of data in each fold's training set)
   - Maximizes learning from available data

3. **Overfitting Detection:**
   - Large std_auc (e.g., >0.05) indicates overfitting to specific train/test splits
   - Small std_auc (0.0053) indicates model generalizes well

**When to Use Cross-Validation:**
- **Small datasets** (< 10,000 rows): Maximizes training data usage
- **Model selection**: Compare algorithms fairly (same CV folds for all)
- **Hyperparameter tuning**: Evaluate each config on multiple folds
- **Performance uncertainty**: Estimate confidence intervals for metrics

**When to Use Single Train/Test Split:**
- **Large datasets** (> 100,000 rows): Single 20% test set (20,000 rows) already sufficient
- **Time series data**: CV with random folds causes temporal leakage
- **Production simulation**: Single split better simulates real deployment scenario
- **Computational cost**: CV requires 5x more model training

**Hybrid Approach:**
```sql
-- Step 1: Create fixed test set (20%) for final validation
CREATE TABLE customer_fixed_test AS (
    SELECT * FROM TD_TrainTestSplit (
        ON customer_churn_data AS InputTable
        USING
        TestSize(0.2)
        StratifyColumns('churn_flag')
        Seed(9999)
        OutputType('SINGLE_TABLE')
        PartitionColumn('dataset')
    ) AS split
    WHERE dataset = 'test'
) WITH DATA;

-- Step 2: Use remaining 80% for 5-fold CV (development)
CREATE TABLE customer_development AS (
    SELECT * FROM customer_churn_data
    WHERE customer_id NOT IN (SELECT customer_id FROM customer_fixed_test)
) WITH DATA;

-- Perform 5-fold CV on customer_development (40K customers)
-- Select best model based on CV results
-- Final validation on customer_fixed_test (10K customers) ONCE

-- Benefit: CV for robust model selection + untouched test set for final validation
```

**Regulatory Perspective:**
- Cross-validation demonstrates model stability for regulatory validation
- Report: "Model AUC = 0.8543 (95% CI: 0.8497-0.8589) based on 5-fold stratified CV"
- More convincing than single split AUC = 0.8612 (no confidence interval)

---

## Common Use Cases

### Model Development Workflow
- **Supervised learning**: Split data for training classification/regression models
- **Unbiased evaluation**: Reserve test set for final performance assessment
- **Hyperparameter tuning**: Create train/validation/test three-way split
- **Feature engineering**: Train-only statistics prevent test set leakage
- **Model comparison**: Identical train/test splits enable fair algorithm comparison

### Preventing Overfitting
- **Hold-out validation**: Test set detects if model memorized training data
- **Generalization assessment**: Estimate real-world performance on unseen data
- **Learning curves**: Plot train vs. test performance to diagnose overfitting
- **Early stopping**: Monitor validation set during training to prevent overtraining

### Classification Tasks
- **Binary classification**: Fraud detection, churn prediction, disease diagnosis
- **Multi-class classification**: Customer segmentation, product categorization
- **Imbalanced classes**: Stratified split maintains rare event distribution
- **Cost-sensitive learning**: Train/test split for business cost optimization

### Regression Tasks
- **Price prediction**: Real estate valuation, dynamic pricing
- **Forecasting**: Sales forecasting, demand planning, load forecasting
- **Time series**: Time-based split (not random) to avoid temporal leakage
- **Financial modeling**: Credit loss prediction, portfolio value forecasting

### Business Domains
- **Banking/Finance**: Credit risk, fraud detection, portfolio optimization
- **Healthcare**: Disease prediction, treatment response, readmission risk
- **Retail**: Demand forecasting, customer segmentation, churn prediction
- **Insurance**: Claims prediction, risk assessment, fraud detection
- **Telecommunications**: Churn prediction, network optimization, upsell modeling
- **Manufacturing**: Quality control, predictive maintenance, demand planning

## Best Practices

### Train/Test Ratio Selection
**Common Split Ratios:**
- **80/20 split** (most common): 80% train, 20% test
  - Suitable for datasets > 10,000 rows
  - Balances training data size with reliable test evaluation

- **70/30 split**: 70% train, 30% test
  - Recommended for medium datasets (1,000-10,000 rows)
  - Provides larger test set for more reliable evaluation

- **90/10 split**: 90% train, 10% test
  - For very large datasets (> 100,000 rows)
  - 10% still provides tens of thousands of test records

- **60/20/20 split**: 60% train, 20% validation, 20% test (three-way)
  - For hyperparameter tuning workflows
  - Validation set prevents test set contamination

**Guidelines by Dataset Size:**
- **< 1,000 rows**: Use cross-validation instead of single split
- **1,000-10,000 rows**: 70/30 or 60/40 split
- **10,000-100,000 rows**: 80/20 split
- **> 100,000 rows**: 90/10 or 80/20 split

### Stratification Strategy
**Always stratify when:**
1. **Imbalanced classification** (minority class < 10%)
   - Fraud detection (0.1-1% fraud)
   - Rare disease prediction (< 5% prevalence)
   - Equipment failure (< 2% failure rate)

2. **Multi-class classification** (ensuring all classes in both sets)
   - Customer segmentation (4-10 segments)
   - Product categorization
   - Risk tier classification

3. **Important subgroups** must be represented
   - Geographic regions
   - Demographic groups
   - Time periods (seasons, quarters)

**Don't stratify when:**
- Regression tasks (continuous targets, no classes)
- Perfectly balanced classes (50/50 split)
- Very large datasets where random split already representative

**Multi-variable stratification:**
```sql
StratifyColumns('target_class', 'customer_segment', 'product_category')
-- Maintains distribution across all three variables simultaneously
```

### Reproducibility
1. **Always use Seed parameter** during development
   - Enables consistent results across runs
   - Critical for debugging and model comparison
   - Example: `Seed(42)` (any integer works, 42 is traditional ML convention)

2. **Document seed value** in model documentation
   - Regulatory compliance: Reproduce exact train/test split for audits
   - Team collaboration: Colleagues can recreate same split

3. **Change seed for production retraining**
   - Each quarterly/annual retrain uses different seed
   - Prevents model from memorizing specific split artifacts

### Time Series Considerations
**NEVER use random split for time series:**
```sql
-- WRONG: Random split for time series
SELECT * FROM TD_TrainTestSplit (
    ON sales_time_series AS InputTable
    USING TestSize(0.2)
) AS split;
-- Problem: Training on 2024 data, testing on 2020 data (temporal leakage!)
```

**CORRECT: Time-based split:**
```sql
-- Method 1: Manual time-based split
CREATE TABLE sales_split AS (
    SELECT
        *,
        CASE WHEN sale_date < DATE '2024-01-01' THEN 'train' ELSE 'test' END AS dataset
    FROM sales_time_series
) WITH DATA;

-- Method 2: Sorted TD_TrainTestSplit
-- (Pre-sort by date, then split - last 20% becomes test)
CREATE TABLE sales_split AS (
    SELECT * FROM TD_TrainTestSplit (
        ON (SELECT * FROM sales_time_series ORDER BY sale_date) AS InputTable
        USING
        TestSize(0.2)
        Seed(42)
    ) AS split
) WITH DATA;
-- Test set = most recent 20% of data (simulates forecasting scenario)
```

### Preventing Data Leakage
1. **Compute statistics only from training set:**
```sql
-- WRONG: Scaling using full dataset statistics
CREATE TABLE scaled_features AS (
    SELECT
        feature1,
        (feature1 - AVG(feature1) OVER ()) / STDDEV(feature1) OVER () AS feature1_scaled  -- Uses test data!
    FROM full_dataset
) WITH DATA;

-- Then split - TOO LATE, already leaked test statistics into features!

-- CORRECT: Split first, then scale using train-only statistics
-- Step 1: Split
CREATE TABLE data_split AS (SELECT * FROM TD_TrainTestSplit(...)) WITH DATA;

-- Step 2: Compute statistics from training set only
CREATE TABLE train_statistics AS (
    SELECT
        AVG(feature1) AS feature1_mean,
        STDDEV(feature1) AS feature1_std
    FROM data_split
    WHERE dataset = 'train'
) WITH DATA;

-- Step 3: Apply scaling to both train and test using train statistics
CREATE TABLE scaled_split AS (
    SELECT
        d.*,
        (d.feature1 - s.feature1_mean) / s.feature1_std AS feature1_scaled
    FROM data_split d
    CROSS JOIN train_statistics s
) WITH DATA;
```

2. **Feature engineering after split:**
   - Create features independently for train and test
   - Use train-derived parameters (means, thresholds) for test transformations

3. **No test set peeking:**
   - Never evaluate models repeatedly on test set during development
   - Use validation set or cross-validation for iterative evaluation

### Sample Size Requirements
**Minimum test set sizes:**
- **Binary classification**: ≥ 100 examples per class (200 total minimum)
- **Multi-class classification**: ≥ 50-100 examples per class
- **Regression**: ≥ 1,000 examples (ideally 10,000+)
- **Imbalanced classification**: ≥ 100 minority class examples in test set

**Example check:**
```sql
-- Verify sufficient test set samples
SELECT
    dataset,
    target_class,
    COUNT(*) AS sample_count,
    CASE
        WHEN COUNT(*) >= 100 THEN 'SUFFICIENT'
        WHEN COUNT(*) >= 50 THEN 'MARGINAL'
        ELSE 'INSUFFICIENT - Adjust TestSize'
    END AS adequacy
FROM data_split
WHERE dataset = 'test'
GROUP BY dataset, target_class;
```

### Output Format Selection
**Use SINGLE_TABLE when:**
- Downstream queries need flexible filtering (easy to filter by partition column)
- Space-efficient (one table instead of two)
- Simplified table management

**Use SEPARATE_TABLES when:**
- Need strict workflow isolation (prevent test set contamination)
- Different access controls for train vs. test
- Regulatory compliance requires physical separation
- Cleaner separation for production deployment

### Verification Steps
**Always verify after split:**
1. **Split ratios:**
```sql
SELECT
    dataset,
    COUNT(*) AS count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct
FROM data_split
GROUP BY dataset;
-- Should match TestSize parameter
```

2. **Stratification success:**
```sql
SELECT
    dataset,
    target_class,
    COUNT(*) AS count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY dataset), 2) AS pct_within_dataset
FROM data_split
GROUP BY dataset, target_class;
-- Percentages should be nearly identical across train and test
```

3. **No overlap:**
```sql
-- Should return 0 rows
SELECT COUNT(*) AS duplicate_count
FROM (
    SELECT id FROM data_split WHERE dataset = 'train'
    INTERSECT
    SELECT id FROM data_split WHERE dataset = 'test'
) AS overlap;
```

## Related Functions

### Model Training
- **TD_GLM**: Train generalized linear models (logistic regression, linear regression)
- **TD_DecisionForest**: Train random forest classifiers and regressors
- **TD_XGBoost**: Train gradient boosted models
- **TD_KMeans**: Train clustering models (unsupervised learning)
- **TD_NaiveBayes**: Train Naive Bayes classifiers
- **TD_SVM**: Train support vector machines

### Model Evaluation
- **TD_ClassificationEvaluator**: Evaluate classification models (precision, recall, F1, accuracy)
- **TD_RegressionEvaluator**: Evaluate regression models (MAE, RMSE, R²)
- **TD_ROC**: Generate ROC curves and compute AUC for binary classifiers
- **TD_SHAP**: Explain model predictions and feature importance

### Data Preparation
- **TD_SimpleImputeFit / TD_SimpleImputeTransform**: Handle missing values
- **TD_ScaleFit / TD_ScaleTransform**: Normalize/standardize features
- **TD_OneHotEncodingFit / TD_OneHotEncodingTransform**: Encode categorical variables
- **TD_OutlierFilterFit / TD_OutlierFilterTransform**: Remove outliers
- **TD_SMOTE**: Handle imbalanced classes through synthetic oversampling
- **TD_ClassBalance**: Undersample/oversample to balance classes

### Sampling Functions
- **TD_Sample**: Random sampling with or without replacement
- **TD_StratifiedSample**: Stratified random sampling by group
- **TD_Antiselect**: Select rows NOT in a sample (complement)

## Notes and Limitations

### Function Constraints
- **Minimum rows**: At least 10 rows required for split (100+ recommended)
- **TestSize range**: Must be between 0 and 1 (exclusive) for fraction, or positive integer for count
- **TrainSize + TestSize**: Must sum to ≤ 1.0 if both specified
- **StratifyColumns cardinality**: Works best with < 100 unique values per stratify column
- **Seed range**: Any integer value valid for pseudorandom seed

### Stratification Limitations
1. **Small stratify groups**: If a stratify group has < 2 examples, stratification may fail
   - Solution: Combine rare categories before splitting

2. **High cardinality**: Stratifying on unique IDs or high-cardinality columns ineffective
   - Solution: Stratify on categorical variables with reasonable # of levels (2-100)

3. **Multiple stratify columns**: Creates cross-product of groups (may have many tiny groups)
   - Example: 10 regions × 5 product categories × 2 classes = 100 groups
   - Each group needs sufficient samples for stratification
   - Solution: Limit to 2-3 most important stratify columns

### Randomness and Reproducibility
- **Seed ensures reproducibility**: Same seed + same input data = identical split
- **No seed**: Each run produces different split (non-reproducible)
- **Pseudorandom**: Not cryptographically secure random (fine for ML purposes)
- **Data order independence**: Split results don't depend on input data order (when Seed specified)

### Performance Considerations
- **Large datasets**: Function efficiently handles millions of rows in single operation
- **Stratification overhead**: Stratified split slightly slower than non-stratified (negligible for most datasets)
- **Separate tables**: Slightly slower than single table due to multiple writes
- **No sampling without replacement**: Cannot split >100% of data (TestSize + TrainSize ≤ 1.0)

### Common Pitfalls
1. **Forgetting stratification for imbalanced classes**:
   - Results in different class distributions in train vs. test
   - Model evaluation biased

2. **Using random split for time series**:
   - Causes temporal leakage (training on future to predict past)
   - Test performance unrealistically optimistic

3. **Computing statistics before split**:
   - Test set information leaks into training features
   - Model performance overestimated

4. **Repeated test set evaluation**:
   - "Peeking" at test set during development contaminates it
   - No longer provides unbiased estimate
   - Use validation set for iterative evaluation

5. **Insufficient test set size**:
   - < 100 examples per class unreliable for evaluation
   - Increase TestSize or use cross-validation

### Business Context Requirements
1. **Regulatory compliance** (Banking/Healthcare):
   - Document split methodology and seed value
   - Demonstrate stratification maintained regulatory subgroups
   - Provide audit trail for train/test assignment
   - Reserve test set for final validation only

2. **Production deployment**:
   - Test set should match expected production data distribution
   - Time-based split for forecasting models
   - Geographic split if deploying to new regions

3. **Reporting to stakeholders**:
   - "Model trained on 80,000 customers (Jan 2020 - Dec 2023)"
   - "Validated on 20,000 customers (Jan 2024 - Jun 2024)"
   - "Test set AUC = 0.87 provides unbiased performance estimate"

### Version and Compatibility
- **Teradata Version**: Available in Teradata Vantage 17.20+
- **Alias support**: TRAIN_TEST_SPLIT (underscore version) is equivalent
- **Output options**: Both SINGLE_TABLE and SEPARATE_TABLES supported
- **NULL handling**: Rows with NULL in stratify columns may be excluded from stratification
- **Table types**: Works with PERMANENT, VOLATILE, and GLOBAL TEMPORARY tables

---

**Generated from Teradata Database Analytic Functions Version 17.20**
**Function Category**: Data Preparation - Train/Test Splitting
**Last Updated**: November 29, 2025
