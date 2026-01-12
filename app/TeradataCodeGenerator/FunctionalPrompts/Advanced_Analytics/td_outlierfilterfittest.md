# TD_OutlierFilterFit

## Function Name
**TD_OutlierFilterFit** - Outlier Detection Model Training

**Aliases:** OutlierFilterFit

## Description

TD_OutlierFilterFit calculates statistical metrics (percentiles, medians, counts) for specified columns to identify outliers in data. This function trains an outlier detection model by computing thresholds based on three statistical methods: Percentile, Tukey, or Carling. The output model is used by TD_OutlierFilterTransform to filter or replace outliers in new data. Outlier detection is critical for data quality, model training, and identifying anomalous patterns that could indicate data errors, fraud, or unusual events.

**Key Characteristics:**
- **Three Detection Methods**: Percentile-based, Tukey (IQR), and Carling (adaptive IQR) methods
- **Configurable Thresholds**: Adjust sensitivity to outliers with percentile ranges and IQR multipliers
- **Multiple Handling Strategies**: Delete outliers, replace with NULL, median, or custom values
- **Group-wise Detection**: Detect outliers separately for each group (e.g., by product category, region)
- **Fit-Transform Pattern**: Train once, apply to multiple datasets
- **Production-Ready**: Optimized for large-scale data cleaning pipelines

The function produces a FIT table containing statistical thresholds that define what constitutes an outlier for each target column.

## When to Use TD_OutlierFilterFit

**Business Applications:**
- **Data Quality**: Remove data entry errors before analysis or modeling
- **Fraud Detection**: Identify unusual transaction amounts or frequencies
- **Sensor Data Cleaning**: Filter faulty sensor readings in IoT applications
- **Price Optimization**: Remove pricing anomalies from historical data
- **Inventory Management**: Identify unusual demand spikes or drops
- **Customer Analytics**: Filter extreme values in purchase amounts or engagement metrics
- **Healthcare**: Remove erroneous lab values or vital sign readings
- **Manufacturing**: Detect out-of-spec measurements in quality control

**Use TD_OutlierFilterFit When You Need To:**
- Train an outlier detection model for consistent filtering across datasets
- Define statistical thresholds for identifying extreme values
- Prepare training data for machine learning (outliers can skew models)
- Clean historical data before time series forecasting
- Establish data quality rules for production pipelines
- Create group-specific outlier definitions (different thresholds per category)

**Analytical Use Cases:**
- Data preparation for machine learning model training
- Exploratory data analysis and data profiling
- Time series anomaly detection preprocessing
- A/B test data validation (remove test corruption)
- Financial data cleansing (remove erroneous transactions)

## Syntax

```sql
SELECT * FROM TD_OutlierFilterFit (
    ON { table | view | (query) } AS InputTable
    [ OUT [ PERMANENT | VOLATILE ] TABLE OutputTable (output_table_name) ]
    USING
    TargetColumns ({ 'target_column' | target_column_range } [,...])
    [ GroupColumns ('group_column') ]
    [ OutlierMethod ({ 'percentile' | 'tukey' | 'carling' }) ]
    [ LowerPercentile (min_value) ]
    [ UpperPercentile (max_value) ]
    [ IQRMultiplier (k) ]
    [ ReplacementValue ({ 'delete' | 'null' | 'median' | replacement_value }) ]
    [ RemoveTail ({ 'both' | 'upper' | 'lower' }) ]
    [ PercentileMethod ({ 'PercentileCont' | 'PercentileDISC' }) ]
) AS dt;
```

## Required Elements

### InputTable
The table containing numeric columns for outlier threshold calculation.

### TargetColumns
Specifies the numeric columns for which to compute outlier detection metrics.

**Syntax:** `TargetColumns('column1', 'column2', ...)`

**Column Ranges:** You can specify ranges like `'[1:5]'` for columns 1-5, or `'-[2:4]'` to exclude columns 2-4.

**Example:**
```sql
TargetColumns('price', 'quantity', 'discount_amount')
TargetColumns('[1:10]')  -- Columns 1 through 10
```

## Optional Elements

### OUT TABLE OutputTable
Specifies the output FIT table name and persistence.

**Options:**
- `PERMANENT TABLE`: Persists after session ends
- `VOLATILE TABLE`: Temporary, deleted at session end
- Default: Output returned as result set

**Example:**
```sql
OUT TABLE OutputTable(product_outlier_model)
OUT PERMANENT TABLE OutputTable(outlier_fit_v1)
```

### GroupColumns
Calculates separate outlier thresholds for each group value.

**Use Case:** Different outlier definitions for different categories (e.g., luxury vs. budget products have different price outlier ranges).

**Syntax:** `GroupColumns('category_column')`

**Example:**
```sql
GroupColumns('product_category')
GroupColumns('region')
```

### OutlierMethod
Specifies the statistical method for defining outliers.

**Options:**
1. **'percentile'** (default): Values outside [LowerPercentile, UpperPercentile] range are outliers
2. **'tukey'**: Values outside [Q1 - k×IQR, Q3 + k×IQR] are outliers (IQR = Q3 - Q1)
3. **'carling'**: Adaptive method using Q2 ± c×IQR where c adjusts based on sample size

**Syntax:** `OutlierMethod('tukey')`

**Guidance:**
- Use **percentile** for simple, interpretable thresholds
- Use **tukey** (k=1.5) for standard outlier detection, (k=3.0) for extreme outliers only
- Use **carling** when sample sizes vary across groups (auto-adjusts sensitivity)

### LowerPercentile
Lower percentile threshold (0 to 1). Values below this percentile are outliers.

**Default:** 0.05 (5th percentile)

**Example:**
```sql
LowerPercentile(0.01)  -- Flag bottom 1%
LowerPercentile(0.10)  -- Flag bottom 10%
```

### UpperPercentile
Upper percentile threshold (0 to 1). Values above this percentile are outliers.

**Default:** 0.95 (95th percentile)

**Example:**
```sql
UpperPercentile(0.99)  -- Flag top 1%
UpperPercentile(0.90)  -- Flag top 10%
```

### IQRMultiplier
Interquartile range multiplier (k) for Tukey method.

**Values:**
- **k = 1.5**: Standard outlier detection (moderate outliers)
- **k = 3.0**: Extreme outlier detection only (serious outliers)

**Default:** 1.5

**Formula:** Outliers are values outside [Q1 - k×IQR, Q3 + k×IQR]

### ReplacementValue
How to handle outliers when transforming data.

**Options:**
- **'delete'** (default): Remove rows with outliers
- **'null'**: Replace outliers with NULL
- **'median'**: Replace outliers with group median
- **numeric_value**: Replace outliers with specified value (e.g., '0', '999')

**Example:**
```sql
ReplacementValue('median')  -- Replace with median
ReplacementValue('null')     -- Set to NULL
ReplacementValue('0')        -- Replace with 0
```

### RemoveTail
Specifies which tail(s) to check for outliers.

**Options:**
- **'both'** (default): Check both upper and lower tails
- **'upper'**: Only flag values above upper threshold
- **'lower'**: Only flag values below lower threshold

**Use Cases:**
- **'upper'**: Remove unusually high prices (but keep low sale prices)
- **'lower'**: Remove negative values in strictly positive data
- **'both'**: Standard symmetric outlier detection

### PercentileMethod
Method for calculating percentiles.

**Options:**
- **'PercentileDISC'** (default): Discrete - returns actual data value at percentile
- **'PercentileCont'**: Continuous - interpolates between values

**Example:**
```sql
PercentileMethod('PercentileCont')  -- Interpolated percentiles
```

## Input Schema

### InputTable
| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | NUMERIC | Column for outlier detection (BYTEINT, SMALLINT, INTEGER, BIGINT, DECIMAL, FLOAT, DOUBLE PRECISION) |
| group_column | ANY | [Optional] Column for grouping data |
| other_columns | ANY | Other columns (passed through to output if needed) |

**Requirements:**
- TargetColumns must be numeric types
- No NULL handling required (function calculates stats on non-NULL values)
- GroupColumns can be any data type (typically categorical)

## Output Schema

### FitTable (Output Model)
| Column | Data Type | Description |
|--------|-----------|-------------|
| TD_OutlierMethod_OFTFIT | VARCHAR | Outlier method used ('percentile', 'tukey', 'carling') |
| group_column | Same as input | [If GroupColumns specified] Group identifier |
| TD_IQRMultiplier_OFTFIT | NUMERIC | IQR multiplier (k) value |
| TD_RemoveTail_OFTFIT | VARCHAR | Tail removal specification ('both', 'upper', 'lower') |
| TD_ReplacementValue_OFTFIT | VARCHAR | Replacement strategy ('delete', 'null', 'median', or value) |
| TD_MinThreshold_OFTFIT | NUMERIC | Lower percentile threshold |
| TD_MaxThreshold_OFTFIT | NUMERIC | Upper percentile threshold |
| TD_AttributeValue_OFTFIT | VARCHAR | Target column name |
| TD_CountValue_OFTFIT | NUMERIC | Row count in group (or total if no grouping) |
| TD_MedianValue_OFTFIT | NUMERIC | Median value for target column |
| TD_LowerPercentile_OFTFIT | NUMERIC | Calculated lower threshold value |
| TD_UpperPercentile_OFTFIT | NUMERIC | Calculated upper threshold value |

**Notes:**
- One row per target column per group
- If no GroupColumns, one row per target column for entire dataset
- Thresholds define the range [TD_LowerPercentile_OFTFIT, TD_UpperPercentile_OFTFIT]
- Values outside this range are classified as outliers

## Code Examples

### Example 1: Basic Percentile-Based Outlier Detection

**Business Context:** An e-commerce company wants to remove extreme price outliers from product data before training a pricing recommendation model.

```sql
-- Train outlier model on product prices
CREATE TABLE price_outlier_model AS (
    SELECT * FROM TD_OutlierFilterFit (
        ON product_catalog AS InputTable
        OUT TABLE OutputTable(price_outlier_model)
        USING
        TargetColumns('unit_price')
        LowerPercentile(0.01)  -- Flag bottom 1%
        UpperPercentile(0.99)  -- Flag top 1%
        OutlierMethod('percentile')
        ReplacementValue('median')  -- Replace outliers with median
        RemoveTail('both')
    ) AS dt
) WITH DATA;

-- View the trained model
SELECT * FROM price_outlier_model;

/*
Sample Output:
TD_OutlierMethod_OFTFIT | TD_IQRMultiplier_OFTFIT | TD_RemoveTail_OFTFIT | TD_ReplacementValue_OFTFIT | TD_MinThreshold_OFTFIT | TD_MaxThreshold_OFTFIT | TD_AttributeValue_OFTFIT | TD_CountValue_OFTFIT | TD_MedianValue_OFTFIT | TD_LowerPercentile_OFTFIT | TD_UpperPercentile_OFTFIT
------------------------|-------------------------|----------------------|----------------------------|------------------------|------------------------|--------------------------|----------------------|----------------------|---------------------------|---------------------------
percentile              | 1.5                     | both                 | median                     | 0.01                   | 0.99                   | unit_price               | 10000                | 29.99                | 5.99                      | 249.99

Interpretation:
- Median price: $29.99
- Lower threshold: $5.99 (1st percentile)
- Upper threshold: $249.99 (99th percentile)
- Products priced below $5.99 or above $249.99 will be considered outliers
- Outliers will be replaced with median value ($29.99) during transformation
*/

-- Business Impact:
-- Removed 200 products with data entry errors (e.g., $0.01, $9999.99)
-- Pricing model accuracy improved by 18% after outlier removal
```

### Example 2: Group-Specific Outlier Detection (Tukey Method)

**Business Context:** Different product categories have vastly different price ranges. Detect outliers separately for each category using Tukey's IQR method.

```sql
-- Train category-specific outlier models
CREATE TABLE category_outlier_model AS (
    SELECT * FROM TD_OutlierFilterFit (
        ON product_inventory AS InputTable
        OUT PERMANENT TABLE OutputTable(category_outlier_model)
        USING
        TargetColumns('unit_price', 'monthly_sales_units')
        GroupColumns('product_category')
        OutlierMethod('tukey')
        IQRMultiplier(1.5)  -- Standard outlier detection
        ReplacementValue('delete')  -- Remove outlier rows
        RemoveTail('both')
    ) AS dt
) WITH DATA;

-- View model for each category
SELECT * FROM category_outlier_model
ORDER BY TD_AttributeValue_OFTFIT, product_category;

/*
Sample Output:
TD_OutlierMethod_OFTFIT | product_category | TD_IQRMultiplier_OFTFIT | TD_AttributeValue_OFTFIT | TD_MedianValue_OFTFIT | TD_LowerPercentile_OFTFIT | TD_UpperPercentile_OFTFIT
------------------------|------------------|-------------------------|--------------------------|-----------------------|---------------------------|---------------------------
tukey                   | Electronics      | 1.5                     | unit_price               | 299.99                | 50.00                     | 1499.99
tukey                   | Clothing         | 1.5                     | unit_price               | 39.99                 | 10.00                     | 149.99
tukey                   | Groceries        | 1.5                     | unit_price               | 5.99                  | 1.00                      | 24.99
tukey                   | Electronics      | 1.5                     | monthly_sales_units      | 150                   | 10                        | 850
tukey                   | Clothing         | 1.5                     | monthly_sales_units      | 320                   | 50                        | 1200
tukey                   | Groceries        | 1.5                     | monthly_sales_units      | 2500                  | 500                       | 8000

Interpretation:
- Electronics: Price outliers are < $50 or > $1,500
- Clothing: Price outliers are < $10 or > $150
- Groceries: Price outliers are < $1 or > $25
- Different categories have dramatically different ranges
- Group-specific thresholds prevent misclassification
*/

-- Business Impact:
-- Prevented false flagging of luxury electronics as outliers
-- Correctly identified data entry errors within each category
-- 95% reduction in manual data review time
```

### Example 3: Extreme Outlier Detection with Tukey (k=3.0)

**Business Context:** A bank wants to flag only the most extreme transaction amounts for fraud investigation, not moderate outliers.

```sql
-- Train extreme outlier model for fraud detection
CREATE TABLE fraud_outlier_model AS (
    SELECT * FROM TD_OutlierFilterFit (
        ON transaction_history AS InputTable
        OUT TABLE OutputTable(fraud_outlier_model)
        USING
        TargetColumns('transaction_amount')
        GroupColumns('account_type')  -- Different thresholds for checking vs. savings
        OutlierMethod('tukey')
        IQRMultiplier(3.0)  -- Only flag extreme outliers
        ReplacementValue('null')  -- Keep rows but mark outliers as NULL
        RemoveTail('upper')  -- Only flag unusually high amounts
    ) AS dt
) WITH DATA;

-- View fraud detection thresholds
SELECT
    account_type,
    TD_AttributeValue_OFTFIT AS metric,
    TD_MedianValue_OFTFIT AS median_amount,
    TD_UpperPercentile_OFTFIT AS fraud_threshold,
    TD_CountValue_OFTFIT AS sample_size
FROM fraud_outlier_model
ORDER BY account_type;

/*
Sample Output:
account_type | metric              | median_amount | fraud_threshold | sample_size
-------------|---------------------|---------------|-----------------|------------
Checking     | transaction_amount  | 150.00        | 8500.00         | 125000
Savings      | transaction_amount  | 500.00        | 25000.00        | 45000
Business     | transaction_amount  | 2500.00       | 95000.00        | 8000

Interpretation:
- Checking account transactions > $8,500 flagged for review (k=3.0 catches only extreme)
- Savings account withdrawals > $25,000 flagged
- Business accounts have higher threshold ($95,000) appropriate to their usage
- Using k=1.5 would have flagged 3x more transactions (too many false positives)
*/

-- Calculate expected fraud detection rate
SELECT
    account_type,
    TD_CountValue_OFTFIT AS total_transactions,
    CAST(TD_CountValue_OFTFIT * 0.003 AS INTEGER) AS expected_extreme_outliers,
    -- With k=3.0, expect ~0.3% of data as extreme outliers
    TD_UpperPercentile_OFTFIT AS fraud_alert_threshold
FROM fraud_outlier_model;

-- Business Impact:
-- Reduced fraud review queue from 5,000 to 400 transactions daily
-- Focused investigators on truly suspicious activity
-- Fraud detection rate: 12% of flagged transactions (vs. 2% with k=1.5)
```

### Example 4: Carling Method for Variable Sample Sizes

**Business Context:** A retailer analyzes stores with vastly different sizes (from small boutiques to megastores). Carling method auto-adjusts sensitivity based on sample size.

```sql
-- Train store-specific sales outlier model
CREATE TABLE store_sales_outlier_model AS (
    SELECT * FROM TD_OutlierFilterFit (
        ON daily_store_sales AS InputTable
        OUT TABLE OutputTable(store_sales_outlier_model)
        USING
        TargetColumns('daily_revenue', 'transaction_count')
        GroupColumns('store_id')
        OutlierMethod('carling')  -- Auto-adjusts for sample size
        ReplacementValue('median')
        RemoveTail('both')
        LowerPercentile(0.25)  -- Q1
        UpperPercentile(0.75)  -- Q3
    ) AS dt
) WITH DATA;

-- Compare thresholds across different store sizes
SELECT
    s.store_id,
    s.store_size,
    m.TD_CountValue_OFTFIT AS days_of_data,
    m.TD_AttributeValue_OFTFIT AS metric,
    m.TD_MedianValue_OFTFIT AS median_value,
    m.TD_LowerPercentile_OFTFIT AS lower_threshold,
    m.TD_UpperPercentile_OFTFIT AS upper_threshold
FROM store_sales_outlier_model m
JOIN store_master s ON m.store_id = s.store_id
WHERE m.TD_AttributeValue_OFTFIT = 'daily_revenue'
ORDER BY s.store_size DESC;

/*
Sample Output:
store_id | store_size | days_of_data | metric         | median_value | lower_threshold | upper_threshold
---------|------------|--------------|----------------|--------------|-----------------|----------------
ST001    | Large      | 365          | daily_revenue  | 125000       | 85000           | 175000
ST015    | Medium     | 365          | daily_revenue  | 45000        | 28000           | 68000
ST042    | Small      | 180          | daily_revenue  | 8500         | 4200            | 14500

Interpretation:
- Carling method calculated c = (17.63*r - 23.64) / (7.74*r - 3.71) for each store
- Large stores (more data points) have tighter relative thresholds
- Small stores (fewer data points) have wider relative thresholds to account for variability
- This prevents over-flagging outliers in small stores with limited data
*/

-- Business Impact:
-- Appropriate sensitivity for stores of all sizes
-- Detected holiday sales anomalies in large stores
-- Avoided false alerts in newly opened small stores
```

### Example 5: Multiple Columns with Different Handling Strategies

**Business Context:** A logistics company wants to clean shipment data - some outliers should be deleted, others investigated.

```sql
-- Train multi-column outlier model
CREATE TABLE shipment_outlier_model AS (
    SELECT * FROM TD_OutlierFilterFit (
        ON shipment_records AS InputTable
        OUT TABLE OutputTable(shipment_outlier_model)
        USING
        TargetColumns('weight_kg', 'distance_km', 'delivery_days', 'cost_usd')
        OutlierMethod('percentile')
        LowerPercentile(0.02)
        UpperPercentile(0.98)
        ReplacementValue('null')  -- Keep rows for investigation
        RemoveTail('both')
        PercentileMethod('PercentileCont')  -- Interpolated percentiles
    ) AS dt
) WITH DATA;

-- View thresholds for all metrics
SELECT
    TD_AttributeValue_OFTFIT AS metric,
    TD_CountValue_OFTFIT AS total_shipments,
    TD_MedianValue_OFTFIT AS median,
    TD_LowerPercentile_OFTFIT AS lower_threshold,
    TD_UpperPercentile_OFTFIT AS upper_threshold,
    ROUND((TD_UpperPercentile_OFTFIT - TD_LowerPercentile_OFTFIT) /
          TD_MedianValue_OFTFIT * 100, 2) AS range_pct_of_median
FROM shipment_outlier_model
ORDER BY metric;

/*
Sample Output:
metric        | total_shipments | median  | lower_threshold | upper_threshold | range_pct_of_median
--------------|-----------------|---------|-----------------|-----------------|--------------------
cost_usd      | 50000           | 125.50  | 15.20           | 985.00          | 772.73
delivery_days | 50000           | 3.00    | 1.00            | 12.00           | 366.67
distance_km   | 50000           | 450.00  | 50.00           | 2800.00         | 611.11
weight_kg     | 50000           | 25.00   | 2.50            | 180.00          | 710.00

Interpretation:
- Weight outliers: < 2.5 kg or > 180 kg
- Distance outliers: < 50 km or > 2,800 km
- Delivery outliers: < 1 day or > 12 days
- Cost outliers: < $15.20 or > $985
- Cost has highest variability (772% range relative to median)
*/

-- Create action plan based on outliers
SELECT
    'weight_kg' AS metric,
    CASE
        WHEN TD_LowerPercentile_OFTFIT < 1 THEN 'Investigate: Possible empty packages'
        WHEN TD_UpperPercentile_OFTFIT > 500 THEN 'Investigate: Freight misclassification'
        ELSE 'Normal range'
    END AS action
FROM shipment_outlier_model
WHERE TD_AttributeValue_OFTFIT = 'weight_kg'
UNION ALL
SELECT
    'delivery_days' AS metric,
    CASE
        WHEN TD_UpperPercentile_OFTFIT > 10 THEN 'Investigate: Delayed shipments'
        ELSE 'Normal range'
    END AS action
FROM shipment_outlier_model
WHERE TD_AttributeValue_OFTFIT = 'delivery_days';

-- Business Impact:
-- Identified 120 shipments with erroneous weight data (data entry errors)
-- Flagged 85 severely delayed shipments for customer service follow-up
-- Cost outliers revealed pricing errors requiring correction
```

### Example 6: Production Pipeline with Seasonal Adjustment

**Business Context:** A retailer retrains outlier models quarterly to adjust for seasonal patterns in sales data.

```sql
-- Train Q1 outlier model
CREATE TABLE sales_outlier_model_2024_q1 AS (
    SELECT * FROM TD_OutlierFilterFit (
        ON sales_2024_q1 AS InputTable
        OUT PERMANENT TABLE OutputTable(sales_outlier_model_2024_q1)
        USING
        TargetColumns('daily_revenue', 'units_sold')
        GroupColumns('store_region')
        OutlierMethod('tukey')
        IQRMultiplier(1.5)
        ReplacementValue('median')
        RemoveTail('both')
    ) AS dt
) WITH DATA;

-- Compare Q1 vs Q4 thresholds (holiday season impact)
SELECT
    'Q4_2023' AS period,
    store_region,
    TD_AttributeValue_OFTFIT AS metric,
    TD_MedianValue_OFTFIT AS median,
    TD_UpperPercentile_OFTFIT AS upper_threshold
FROM sales_outlier_model_2023_q4
WHERE TD_AttributeValue_OFTFIT = 'daily_revenue'
UNION ALL
SELECT
    'Q1_2024' AS period,
    store_region,
    TD_AttributeValue_OFTFIT AS metric,
    TD_MedianValue_OFTFIT AS median,
    TD_UpperPercentile_OFTFIT AS upper_threshold
FROM sales_outlier_model_2024_q1
WHERE TD_AttributeValue_OFTFIT = 'daily_revenue'
ORDER BY store_region, period;

/*
Sample Output:
period    | store_region | metric         | median   | upper_threshold
----------|--------------|----------------|----------|----------------
Q4_2023   | Northeast    | daily_revenue  | 185000   | 425000
Q1_2024   | Northeast    | daily_revenue  | 125000   | 285000
Q4_2023   | Southeast    | daily_revenue  | 165000   | 380000
Q1_2024   | Southeast    | daily_revenue  | 110000   | 250000

Interpretation:
- Q4 (holiday season) has 48% higher median revenue and 49% higher outlier threshold
- Using Q4 thresholds in Q1 would miss true outliers (thresholds too high)
- Using Q1 thresholds in Q4 would flag normal holiday sales as outliers
- Quarterly retraining adapts to seasonal patterns
*/

-- Automate quarterly model retraining
CREATE TABLE model_metadata AS (
    SELECT
        CURRENT_DATE AS model_date,
        EXTRACT(QUARTER FROM CURRENT_DATE) AS model_quarter,
        EXTRACT(YEAR FROM CURRENT_DATE) AS model_year,
        'sales_outlier_model_2024_q1' AS model_table_name,
        COUNT(*) AS total_rows_trained
    FROM sales_outlier_model_2024_q1
) WITH DATA;

-- Business Impact:
-- Seasonal model adjustment reduced false positive rate by 65%
-- Correctly identified post-holiday inventory clearance sales as normal
-- Detected unusual sales drops indicating supply chain issues
```

## Common Use Cases

### Data Quality and Preparation
- **ML Training Data**: Remove outliers before training models (prevent skewing)
- **Data Profiling**: Understand extreme value ranges in datasets
- **ETL Validation**: Flag data quality issues during ingestion
- **Historical Data Cleaning**: Prepare legacy data for analysis

### Fraud and Anomaly Detection
- **Transaction Monitoring**: Identify unusual amounts for investigation
- **Claims Processing**: Flag unusually high insurance claims
- **Credit Card Fraud**: Detect out-of-pattern purchases
- **Expense Auditing**: Identify questionable expense reports

### Operations and Monitoring
- **Sensor Data**: Filter faulty IoT sensor readings
- **Performance Metrics**: Remove anomalous system measurements
- **Quality Control**: Detect manufacturing defects
- **Supply Chain**: Identify delivery time anomalies

### Financial and Pricing
- **Price Optimization**: Remove pricing errors from historical data
- **Revenue Forecasting**: Clean revenue data of one-time events
- **Inventory Valuation**: Filter extreme cost variations
- **Budget Analysis**: Remove atypical spending patterns

### Healthcare and Research
- **Clinical Data**: Remove erroneous lab values
- **Patient Monitoring**: Detect abnormal vital sign readings
- **Research Studies**: Clean experimental data
- **Drug Trials**: Identify adverse event outliers

## Best Practices

### Method Selection
1. **Percentile Method**: Use for simple, interpretable thresholds (good starting point)
2. **Tukey Method (k=1.5)**: Standard outlier detection, widely accepted in statistics
3. **Tukey Method (k=3.0)**: Only flag extreme outliers (reduce false positives)
4. **Carling Method**: Use when sample sizes vary significantly across groups

### Threshold Configuration
1. **Conservative (0.01, 0.99)**: Flag only 1% of data as outliers
2. **Standard (0.05, 0.95)**: Flag 5% of data (typical default)
3. **Aggressive (0.10, 0.90)**: Flag 10% of data (more sensitive)
4. **Custom**: Adjust based on business requirements and data distribution

### Grouping Strategy
1. **Use GroupColumns**: When categories have fundamentally different ranges
2. **Examples**: Product category, region, customer segment, time period
3. **Avoid**: Over-grouping (creates too many small samples, unreliable stats)
4. **Minimum**: Ensure each group has at least 100 data points for stable statistics

### Replacement Strategy
1. **'delete'**: For training data (don't want outliers in models)
2. **'null'**: For investigation (keep rows, flag values as suspicious)
3. **'median'**: For forecasting (replace with typical value, maintain data continuity)
4. **Custom value**: For domain-specific handling (e.g., replace with 0 or cap at max)

### Production Deployment
1. **Version Models**: Name with date/version (outlier_model_2024_q1)
2. **Retrain Regularly**: Quarterly or when data patterns change
3. **Monitor Stats**: Track median and threshold changes over time
4. **Document Decisions**: Record why specific thresholds were chosen

## Related Functions

### Transformation
- **TD_OutlierFilterTransform**: Apply trained outlier model to new data
- **TD_ScaleTransform**: Scale data after outlier removal
- **TD_BincodeTransform**: Bin data after removing extremes

### Alternative Outlier Detection
- **TD_OneClassSVMPredict**: ML-based anomaly detection
- **TD_KMeansPredict**: Distance-based outlier detection (OutputDistance)
- **TD_IsolationForest**: Tree-based anomaly detection

### Data Quality
- **TD_SimpleImputeFit/Transform**: Handle missing values
- **TD_UnivariateStatistics**: Profile data distributions
- **TD_Histogram**: Visualize data distributions to identify outliers

### Feature Engineering
- **TD_BincodeFit**: Bin continuous variables after outlier removal
- **TD_ScaleFit**: Standardize features after outlier removal

## Notes and Limitations

### General Limitations
1. **Numeric Data Only**: TargetColumns must be numeric (BYTEINT, SMALLINT, INTEGER, BIGINT, DECIMAL, FLOAT, DOUBLE PRECISION)
2. **Univariate Detection**: Each column analyzed independently (no multivariate outlier detection)
3. **Static Thresholds**: Thresholds fixed at training time (retrain if data distribution changes)
4. **Group Size**: Small groups (<30 rows) may have unreliable statistics

### Method-Specific Notes
1. **Percentile Method**: Sensitive to extreme values in data (outliers influence percentile calculation)
2. **Tukey Method**: Assumes roughly symmetric distribution around median
3. **Carling Method**: Best for varying sample sizes, but more complex to interpret
4. **IQR Methods**: Require LowerPercentile=0.25, UpperPercentile=0.75

### Performance Considerations
1. **Large Datasets**: Function is optimized but percentile calculation can be slow on very large tables
2. **Many Groups**: Each group requires separate statistics - avoid excessive grouping
3. **Output Table Size**: One row per (target column × group), can be large with many groups/columns

### Best Use Cases
- **When to Use**: Preparing data for ML, data quality validation, fraud detection
- **When to Avoid**: Need multivariate outlier detection, data is categorical, need real-time streaming detection
- **Alternatives**: Consider TD_OneClassSVM for multivariate/ML-based anomaly detection

### Teradata-Specific Notes
1. **UTF8 Support**: Supports Unicode character sets for column names
2. **PERMANENT vs VOLATILE**: Choose based on reuse needs (PERMANENT for production models)
3. **Partitioning**: GroupColumns enables parallel processing per group
4. **FIT Table Reuse**: Train once, apply to multiple datasets with TD_OutlierFilterTransform

## Version Information

**Documentation Generated:** November 29, 2025
**Based on:** Teradata Database Analytic Functions Version 17.20
**Function Category:** Data Cleaning - Outlier Detection
**Last Updated:** 2025-11-29
