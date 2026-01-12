# TD_ConvertTo

## Function Name
- **TD_ConvertTo**: Data Type Conversion Function - Converts specified input table columns to target data types

## Description
TD_ConvertTo converts specified input table columns to target data types to ensure that data is in the correct format for efficient data processing. This function performs conversion operations on specified columns, enabling users to convert input table columns to desired data types for consistency and compatibility with downstream operations.

The function is essential for data cleaning and preparation, ensuring that columns have appropriate data types before analysis, modeling, or storage optimization.

### Process
1. Select the column(s) for which you want to alter the data type
2. Use TD_ConvertTo to convert the data in the selected input table column(s) into specific data types

### Characteristics
- Converts multiple columns in single operation
- Supports wide range of data types (numeric, string, date/time, binary, LOB)
- Allows individual data type specification per column
- Preserves non-target columns via Accumulate parameter
- Reduces storage requirements through appropriate type selection
- Detects data inconsistencies during conversion

### Common Use Cases
- Convert text representations to numeric types for calculations
- Convert string dates to DATE/TIMESTAMP for temporal operations
- Optimize storage by converting oversized types (INTEGER → BYTEINT)
- Ensure type compatibility for downstream functions
- Standardize column types across datasets
- Handle type mismatches before JOIN operations

## When to Use TD_ConvertTo

TD_ConvertTo is essential for data type management and optimization:

### Data Quality and Consistency
- **Format standardization**: Ensure columns have consistent data types across tables
- **Error detection**: Identify data inconsistencies when conversions fail
- **Data validation**: Verify data conforms to expected types
- **Schema alignment**: Match column types between source and target tables
- **Type safety**: Prevent type-related errors in downstream operations

### Storage Optimization
- **Reduce storage costs**: Convert oversized types to smaller appropriate types
- **Space efficiency**: BYTEINT (1 byte) vs INTEGER (4 bytes) for 0/1 flags
- **Performance improvement**: Smaller data types improve query performance
- **Optimize indexes**: Appropriate types create more efficient indexes
- **Compression benefits**: Proper types enable better compression

### Data Preparation for Analysis
- **Enable calculations**: Convert text numbers to numeric types for math operations
- **Date/time operations**: Convert string dates to DATE/TIMESTAMP for temporal analysis
- **Statistical analysis**: Ensure numeric types for aggregations and statistics
- **Machine learning prep**: Convert data types for ML algorithm requirements
- **Joins and comparisons**: Match data types for efficient JOIN operations

### ETL and Data Integration
- **Source system differences**: Handle varying data types from different sources
- **Data migration**: Convert types when moving data between systems
- **API integration**: Transform JSON/XML strings to appropriate database types
- **Legacy system integration**: Convert old data formats to modern types
- **Cross-platform compatibility**: Ensure types work across different databases

### Business Applications
- **Financial systems**: Convert string amounts to DECIMAL for precise calculations
- **Customer data**: Convert age stored as VARCHAR to INTEGER
- **E-commerce**: Convert string prices to DECIMAL for aggregations
- **Log analysis**: Convert string timestamps to TIMESTAMP for temporal queries
- **IoT data**: Convert sensor readings from VARCHAR to appropriate numeric types
- **Survey data**: Convert string responses to numeric codes for analysis

### Performance Optimization
- **Query optimization**: Proper types enable optimizer to choose better plans
- **Index efficiency**: Smaller types create more efficient indexes
- **Memory usage**: Reduce memory footprint with appropriate types
- **Network transfer**: Smaller types reduce data transfer overhead
- **Join performance**: Matching types avoid implicit conversions during joins

## Syntax

```sql
TD_ConvertTo (
    ON { table | view | (query) } AS InputTable
    USING
    TargetColumns ({ 'target_column' | target_column_range }[,...])
    TargetDataType ('target_datatype' [,...])
    [ Accumulate ({ 'accumulate_column' | accumulate_column_range }[,...]) ]
)
```

**Note:** You can call this function from:
- The FROM clause of a SELECT statement
- As part of a CREATE TABLE statement
- As part of a CREATE VIEW statement

## Required Syntax Elements

### ON Clause
Accept the InputTable clause.
- **InputTable**: Table containing columns to convert
- **Required**: Exactly one InputTable

### TargetColumns
Specify the names of InputTable columns to convert to another data type.
- **Format**: Column names or column ranges
- **Multiple columns**: Separate with commas
- **Column ranges**: Use syntax like `[col1:col5]`
- **Example**: `TargetColumns('age', 'salary', 'flag')`

### TargetDataType
Specify either a single target data type for all target columns or a target data type for each target column.
- **Single type**: One data type applied to all target columns
- **Multiple types**: Nth data type assigned to nth target column
- **Must match**: Number of data types must be 1 or equal to number of target columns
- **Example**: `TargetDataType('INTEGER')` or `TargetDataType('INTEGER', 'DECIMAL', 'BYTEINT')`

## Supported Data Types

### Numeric Types

| TargetDataType Value | Output Data Type | Storage | Range |
|---------------------|------------------|---------|-------|
| BYTEINT | BYTEINT | 1 byte | -128 to 127 |
| SMALLINT | SMALLINT | 2 bytes | -32,768 to 32,767 |
| INTEGER | INTEGER | 4 bytes | -2,147,483,648 to 2,147,483,647 |
| BIGINT | BIGINT | 8 bytes | -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807 |
| REAL | REAL | 8 bytes | Floating-point numbers |
| DECIMAL | DECIMAL(total_digits, precision) | Variable | Up to 38 total digits, 19 decimal places |

### Character Types

| TargetDataType Value | Output Data Type | Notes |
|---------------------|------------------|-------|
| VARCHAR | Depends on input type | Preserves character set and case-specific settings |
| VARCHAR(charlen=len, charset={LATIN\|UNICODE}, casespecific={YES\|NO}) | VARCHAR(len) with specified properties | Custom length and properties |
| CHAR | Depends on input type | Fixed-length character |
| CHAR(charlen=len, charset={LATIN\|UNICODE}, casespecific={YES\|NO}) | CHAR(len) with specified properties | Custom length and properties |
| CLOB | Large character object | Default: CLOB(1048544000) |
| CLOB(charlen=len, charset={LATIN\|UNICODE}) | CLOB(len) with specified charset | Custom size LOB |

### Date and Time Types

| TargetDataType Value | Output Data Type |
|---------------------|------------------|
| DATE | DATE FORMAT 'YYYY/MM/DD' |
| TIME | TIME(6) |
| TIMESTAMP | TIMESTAMP(6) |
| TIME WITH ZONE | TIME(6) WITH ZONE |
| TIMESTAMP WITH ZONE | TIMESTAMP(6) WITH ZONE |

### Interval Types

| TargetDataType Value | Output Data Type |
|---------------------|------------------|
| INTERVAL YEAR | INTERVAL YEAR(4) |
| INTERVAL MONTH | INTERVAL MONTH(4) |
| INTERVAL DAY | INTERVAL DAY(4) |
| INTERVAL HOUR | INTERVAL HOUR(4) |
| INTERVAL MINUTE | INTERVAL MINUTE(4) |
| INTERVAL SECOND | INTERVAL SECOND(4,6) |
| INTERVAL YEAR TO MONTH | INTERVAL YEAR(4) TO MONTH |
| INTERVAL DAY TO HOUR | INTERVAL DAY(4) TO HOUR |
| INTERVAL DAY TO MINUTE | INTERVAL DAY(4) TO MINUTE |
| INTERVAL DAY TO SECOND | INTERVAL DAY(4) TO SECOND(6) |
| INTERVAL HOUR TO MINUTE | INTERVAL HOUR(4) TO MINUTE |
| INTERVAL HOUR TO SECOND | INTERVAL HOUR(4) TO SECOND(6) |
| INTERVAL MINUTE TO SECOND | INTERVAL MINUTE(4) TO SECOND(6) |

### Binary Types

| TargetDataType Value | Output Data Type |
|---------------------|------------------|
| BYTE | BYTE(32000) |
| BYTE(charlen=len) | BYTE(len) |
| VARBYTE | VARBYTE(32000) |
| VARBYTE(charlen=len) | VARBYTE(len) |
| BLOB | BLOB(2097088000) |
| BLOB(charlen=len) | BLOB(len) |

### Structured Types

| TargetDataType Value | Output Data Type |
|---------------------|------------------|
| JSON | JSON(32000), CHARACTER SET UNICODE |
| XML | XML(2097088000) INLINE LENGTH 4046 |

## Optional Syntax Elements

### Accumulate
Specify the input table column names to copy to the output table.
- **Purpose**: Pass through columns that don't need conversion
- **Format**: Column names or column ranges
- **Example**: `Accumulate('passenger_id', 'name', 'ticket')`
- **Use case**: Preserve identifier and metadata columns

## Input

### InputTable Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | Any | Column to convert to target_datatype |
| other columns | Any | Additional columns (can be passed through via Accumulate) |

## Output

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | target_datatype | Column converted to target_datatype |
| input_column | Same as in InputTable | Column copied from InputTable |
| AccumulateColumns | Any | Specified columns copied to output table |

## Code Examples

### Example 1: Basic Type Conversion - Decimal to Integer (Titanic Dataset)

Convert fare from decimal to integer:

```sql
-- Input table: Titanic passenger data
CREATE TABLE titanic_sample (
    passenger INTEGER,
    survived BYTEINT,
    pclass BYTEINT,
    name VARCHAR(100),
    gender VARCHAR(10),
    age DECIMAL(5,2),
    sibsp BYTEINT,
    parch BYTEINT,
    ticket VARCHAR(20),
    fare DECIMAL(10,4),
    cabin VARCHAR(20),
    embarked CHAR(1)
);

INSERT INTO titanic_sample VALUES
(97, 0, 1, 'Goldschmidt, Mr. George B', 'male', 71, 0, 0, 'PC 17754', 34.6542, 'A5', 'C'),
(488, 0, 1, 'Kent, Mr. Edward Austin', 'male', 58, 0, 0, '11771', 29.7000, 'B37', 'C'),
(505, 1, 1, 'Maioni, Miss. Roberta', 'female', 16, 0, 0, '110152', 86.5000, 'B79', 'S'),
(631, 1, 1, 'Barkworth, Mr. Algernon Henry Wilson', 'male', 80, 0, 0, '27042', 30.0000, 'A23', 'S'),
(873, 0, 1, 'Carlsson, Mr. Frans Olof', 'male', 33, 0, 0, '695', 5.0000, 'B51 B53 B55', 'S');

-- Convert fare from DECIMAL to INTEGER
SELECT * FROM TD_ConvertTo (
    ON titanic_sample AS InputTable
    USING
    TargetColumns ('fare')
    TargetDataType ('INTEGER')
) AS dt ORDER BY passenger;

/*
Output:
passenger | survived | pclass | name                                  | gender | age | sibsp | parch | ticket    | fare | cabin        | embarked
----------|----------|--------|---------------------------------------|--------|-----|-------|-------|-----------|------|--------------|----------
97        | 0        | 1      | Goldschmidt, Mr. George B             | male   | 71  | 0     | 0     | PC 17754  | 34   | A5           | C
488       | 0        | 1      | Kent, Mr. Edward Austin               | male   | 58  | 0     | 0     | 11771     | 29   | B37          | C
505       | 1        | 1      | Maioni, Miss. Roberta                 | female | 16  | 0     | 0     | 110152    | 86   | B79          | S
631       | 1        | 1      | Barkworth, Mr. Algernon Henry Wilson  | male   | 80  | 0     | 0     | 27042     | 30   | A23          | S
873       | 0        | 1      | Carlsson, Mr. Frans Olof              | male   | 33  | 0     | 0     | 695       | 5    | B51 B53 B55  | S

Note: Fare values truncated to integers (34.6542 → 34, 29.7 → 29, etc.)
*/
```

**Use Case**: Simplify fare analysis by removing decimal precision when not needed.

### Example 2: Storage Optimization - Flag Columns

Convert binary flags from INTEGER to BYTEINT to save storage:

```sql
-- Sample customer table with flags stored as INTEGER (inefficient)
CREATE TABLE customer_flags_raw (
    customer_id INTEGER,
    name VARCHAR(50),
    is_active INTEGER,  -- 0 or 1, but using 4 bytes!
    is_premium INTEGER,  -- 0 or 1, but using 4 bytes!
    has_subscription INTEGER,  -- 0 or 1, but using 4 bytes!
    total_orders INTEGER
);

-- Insert sample data
INSERT INTO customer_flags_raw VALUES
(1001, 'John Smith', 1, 0, 1, 45),
(1002, 'Jane Doe', 1, 1, 1, 120),
(1003, 'Bob Johnson', 0, 0, 0, 5),
(1004, 'Alice Williams', 1, 1, 0, 89),
(1005, 'Charlie Brown', 1, 0, 1, 34);

-- Convert flag columns to BYTEINT (saves 15 bytes per flag per row!)
CREATE TABLE customer_flags_optimized AS (
    SELECT * FROM TD_ConvertTo (
        ON customer_flags_raw AS InputTable
        USING
        TargetColumns ('is_active', 'is_premium', 'has_subscription')
        TargetDataType ('BYTEINT', 'BYTEINT', 'BYTEINT')
        Accumulate ('customer_id', 'name', 'total_orders')
    ) AS dt
) WITH DATA;

-- Compare storage
SELECT
    'Original (INTEGER)' as table_type,
    COUNT(*) as row_count,
    COUNT(*) * (4 + 4 + 4) as flag_bytes,
    'Inefficient' as efficiency
FROM customer_flags_raw

UNION ALL

SELECT
    'Optimized (BYTEINT)' as table_type,
    COUNT(*) as row_count,
    COUNT(*) * (1 + 1 + 1) as flag_bytes,
    'Efficient - 75% savings' as efficiency
FROM customer_flags_optimized;

/*
Output:
table_type           | row_count | flag_bytes | efficiency
---------------------|-----------|------------|-------------------------
Original (INTEGER)   | 5         | 60         | Inefficient
Optimized (BYTEINT)  | 5         | 15         | Efficient - 75% savings

Storage savings: 45 bytes for 5 rows
For 10 million rows: 450 MB saved!
*/
```

**Business Impact**: Significant storage and performance improvements for large tables.

### Example 3: Multiple Column Type Conversions

Convert multiple columns to appropriate types in single operation:

```sql
-- Raw data with suboptimal types
CREATE TABLE sales_raw (
    transaction_id VARCHAR(50),
    transaction_date VARCHAR(20),  -- Should be DATE
    customer_age VARCHAR(10),      -- Should be INTEGER
    product_price VARCHAR(20),     -- Should be DECIMAL
    quantity VARCHAR(10),          -- Should be INTEGER
    discount_pct VARCHAR(10),      -- Should be DECIMAL
    is_member VARCHAR(5)           -- Should be BYTEINT
);

INSERT INTO sales_raw VALUES
('TXN001', '2024-01-15', '34', '129.99', '2', '10.5', '1'),
('TXN002', '2024-01-16', '28', '49.50', '1', '0', '0'),
('TXN003', '2024-01-16', '52', '299.99', '3', '15.0', '1'),
('TXN004', '2024-01-17', '41', '79.99', '1', '5.0', '1'),
('TXN005', '2024-01-17', '29', '19.99', '5', '0', '0');

-- Convert all columns to appropriate types
CREATE TABLE sales_clean AS (
    SELECT * FROM TD_ConvertTo (
        ON sales_raw AS InputTable
        USING
        TargetColumns ('transaction_date', 'customer_age', 'product_price', 'quantity', 'discount_pct', 'is_member')
        TargetDataType ('DATE', 'INTEGER', 'DECIMAL', 'INTEGER', 'DECIMAL', 'BYTEINT')
        Accumulate ('transaction_id')
    ) AS dt
) WITH DATA;

-- Now can perform proper calculations
SELECT
    transaction_id,
    transaction_date,
    customer_age,
    product_price,
    quantity,
    discount_pct,
    product_price * quantity as subtotal,
    (product_price * quantity) * (discount_pct / 100) as discount_amount,
    (product_price * quantity) * (1 - discount_pct / 100) as total_amount,
    CASE WHEN is_member = 1 THEN 'Member' ELSE 'Non-Member' END as membership_status
FROM sales_clean
ORDER BY transaction_date, transaction_id;

/*
Output:
transaction_id | transaction_date | customer_age | product_price | quantity | discount_pct | subtotal | discount_amount | total_amount | membership_status
---------------|------------------|--------------|---------------|----------|--------------|----------|-----------------|--------------|------------------
TXN001         | 2024-01-15       | 34           | 129.99        | 2        | 10.5         | 259.98   | 27.30           | 232.68       | Member
TXN002         | 2024-01-16       | 28           | 49.50         | 1        | 0.0          | 49.50    | 0.00            | 49.50        | Non-Member
TXN003         | 2024-01-16       | 52           | 299.99        | 3        | 15.0         | 899.97   | 135.00          | 764.97       | Member
TXN004         | 2024-01-17       | 41           | 79.99         | 1        | 5.0          | 79.99    | 4.00            | 75.99        | Member
TXN005         | 2024-01-17       | 29           | 19.99         | 5        | 0.0          | 99.95    | 0.00            | 99.95        | Non-Member

Benefits:
- Can perform date arithmetic on transaction_date
- Can calculate age statistics on customer_age (INTEGER)
- Precise financial calculations on DECIMAL columns
- Efficient storage with BYTEINT for is_member flag
*/
```

**Strategic Value**: Enable proper analytics and calculations on correctly typed data.

### Example 4: String to Date Conversion for Temporal Analysis

Convert string dates to DATE type for time-based analysis:

```sql
-- Log data with string dates
CREATE TABLE user_activity_log (
    user_id INTEGER,
    activity_date VARCHAR(20),
    login_time VARCHAR(20),
    activity_count INTEGER
);

INSERT INTO user_activity_log VALUES
(1001, '2024-01-15', '09:30:00', 12),
(1001, '2024-01-16', '08:45:00', 8),
(1002, '2024-01-15', '10:15:00', 5),
(1002, '2024-01-17', '14:20:00', 15),
(1003, '2024-01-16', '11:00:00', 22);

-- Convert date and time strings to proper types
CREATE TABLE user_activity_typed AS (
    SELECT * FROM TD_ConvertTo (
        ON user_activity_log AS InputTable
        USING
        TargetColumns ('activity_date', 'login_time')
        TargetDataType ('DATE', 'TIME')
        Accumulate ('user_id', 'activity_count')
    ) AS dt
) WITH DATA;

-- Now can perform temporal analysis
SELECT
    user_id,
    activity_date,
    login_time,
    activity_count,
    EXTRACT(DAY FROM activity_date) as day_of_month,
    CASE
        WHEN EXTRACT(DOW FROM activity_date) IN (6, 0) THEN 'Weekend'
        ELSE 'Weekday'
    END as day_type,
    CASE
        WHEN login_time BETWEEN TIME '00:00:00' AND TIME '11:59:59' THEN 'Morning'
        WHEN login_time BETWEEN TIME '12:00:00' AND TIME '17:59:59' THEN 'Afternoon'
        ELSE 'Evening'
    END as time_of_day,
    activity_date - DATE '2024-01-15' as days_since_start
FROM user_activity_typed
ORDER BY activity_date, user_id;

-- Aggregate by time periods
SELECT
    CASE
        WHEN login_time BETWEEN TIME '00:00:00' AND TIME '11:59:59' THEN 'Morning'
        WHEN login_time BETWEEN TIME '12:00:00' AND TIME '17:59:59' THEN 'Afternoon'
        ELSE 'Evening'
    END as time_period,
    COUNT(*) as session_count,
    SUM(activity_count) as total_activities,
    ROUND(AVG(activity_count), 2) as avg_activities
FROM user_activity_typed
GROUP BY time_period
ORDER BY time_period;
```

**Use Case**: Enable date/time operations for user behavior analysis.

### Example 5: Precision Control with DECIMAL

Control decimal precision for financial calculations:

```sql
-- Raw financial data with inconsistent precision
CREATE TABLE financial_transactions (
    transaction_id INTEGER,
    account_id INTEGER,
    amount_usd VARCHAR(50),
    exchange_rate VARCHAR(50),
    tax_rate VARCHAR(50)
);

INSERT INTO financial_transactions VALUES
(1, 1001, '1234.567890', '1.25678', '0.0825'),
(2, 1002, '567.89', '1.25', '0.0825'),
(3, 1003, '9876.5432100', '1.2567', '0.0825');

-- Convert to DECIMAL with controlled precision
CREATE TABLE financial_transactions_clean AS (
    SELECT * FROM TD_ConvertTo (
        ON financial_transactions AS InputTable
        USING
        TargetColumns ('amount_usd', 'exchange_rate', 'tax_rate')
        TargetDataType ('DECIMAL(18,2)', 'DECIMAL(10,4)', 'DECIMAL(5,4)')
        Accumulate ('transaction_id', 'account_id')
    ) AS dt
) WITH DATA;

-- Perform precise financial calculations
SELECT
    transaction_id,
    account_id,
    amount_usd,
    exchange_rate,
    tax_rate,
    ROUND(amount_usd * exchange_rate, 2) as amount_local,
    ROUND(amount_usd * tax_rate, 2) as tax_amount,
    ROUND(amount_usd * (1 + tax_rate), 2) as amount_with_tax
FROM financial_transactions_clean
ORDER BY transaction_id;

/*
Output:
transaction_id | account_id | amount_usd | exchange_rate | tax_rate | amount_local | tax_amount | amount_with_tax
---------------|------------|------------|---------------|----------|--------------|------------|----------------
1              | 1001       | 1234.57    | 1.2568        | 0.0825   | 1551.69      | 101.85     | 1336.42
2              | 1002       | 567.89     | 1.2500        | 0.0825   | 709.86       | 46.85      | 614.74
3              | 1003       | 9876.54    | 1.2567        | 0.0825   | 12412.80     | 814.81     | 10691.35

Benefits:
- Consistent 2 decimal places for currency amounts
- 4 decimal places for exchange rates (standard)
- 4 decimal places for tax rates (percentage precision)
- Prevents floating-point arithmetic errors
- Ensures regulatory compliance for financial reporting
*/
```

**Critical for Finance**: Precise decimal control prevents rounding errors in financial calculations.

### Example 6: Batch Data Type Standardization

Standardize types across multiple tables for integration:

```sql
-- Multiple source tables with inconsistent types
CREATE TABLE customer_source_a (
    id VARCHAR(20),
    age VARCHAR(10),
    income VARCHAR(20),
    join_date VARCHAR(20)
);

CREATE TABLE customer_source_b (
    id BIGINT,
    age DECIMAL(5,2),
    income INTEGER,
    join_date TIMESTAMP
);

-- Need to standardize to common schema for union/integration

-- Standardize Source A
CREATE TABLE customer_source_a_typed AS (
    SELECT * FROM TD_ConvertTo (
        ON customer_source_a AS InputTable
        USING
        TargetColumns ('id', 'age', 'income', 'join_date')
        TargetDataType ('INTEGER', 'INTEGER', 'DECIMAL(12,2)', 'DATE')
    ) AS dt
) WITH DATA;

-- Standardize Source B
CREATE TABLE customer_source_b_typed AS (
    SELECT
        CAST(id AS INTEGER) as id,
        CAST(age AS INTEGER) as age,
        CAST(income AS DECIMAL(12,2)) as income,
        CAST(join_date AS DATE) as join_date
    FROM customer_source_b
) WITH DATA;

-- Now can combine data from both sources
CREATE TABLE customer_unified AS (
    SELECT 'Source A' as source, * FROM customer_source_a_typed
    UNION ALL
    SELECT 'Source B' as source, * FROM customer_source_b_typed
) WITH DATA;

-- Analyze combined data
SELECT
    source,
    COUNT(*) as customer_count,
    ROUND(AVG(age), 1) as avg_age,
    ROUND(AVG(income), 2) as avg_income,
    MIN(join_date) as earliest_join,
    MAX(join_date) as latest_join
FROM customer_unified
GROUP BY source;
```

**ETL Use Case**: Enable data integration from heterogeneous sources.

## Common Use Cases

### 1. Detect Data Quality Issues

```sql
-- Attempt conversion to detect invalid data
CREATE TABLE validation_results AS (
    SELECT
        *,
        CASE
            WHEN TRY_CAST(age_string AS INTEGER) IS NULL THEN 'Invalid age'
            ELSE 'Valid'
        END as validation_status
    FROM customer_data
) WITH DATA;

-- Count invalid records
SELECT
    validation_status,
    COUNT(*) as record_count
FROM validation_results
GROUP BY validation_status;
```

### 2. Prepare Data for Machine Learning

```sql
-- ML models require specific numeric types
CREATE TABLE customer_ml_ready AS (
    SELECT * FROM TD_ConvertTo (
        ON customer_raw AS InputTable
        USING
        TargetColumns ('age', 'income', 'credit_score', 'tenure_months')
        TargetDataType ('INTEGER', 'DECIMAL', 'INTEGER', 'INTEGER')
        Accumulate ('customer_id', 'segment')
    ) AS dt
) WITH DATA;

-- Now ready for TD_ScaleFit, TD_GLM, etc.
```

### 3. Optimize Existing Tables

```sql
-- Analyze current types
SELECT
    columnname,
    columntype,
    CASE
        WHEN columntype = 'I' AND columnname LIKE '%flag%' THEN 'Consider BYTEINT'
        WHEN columntype = 'CV' AND columnname LIKE '%date%' THEN 'Consider DATE'
        ELSE 'OK'
    END as recommendation
FROM dbc.columns
WHERE tablename = 'large_fact_table';

-- Apply optimizations
CREATE TABLE large_fact_table_optimized AS (
    SELECT * FROM TD_ConvertTo (
        ON large_fact_table AS InputTable
        USING
        TargetColumns ('is_active_flag', 'is_premium_flag', 'order_date_str')
        TargetDataType ('BYTEINT', 'BYTEINT', 'DATE')
    ) AS dt
) WITH DATA;
```

## Best Practices

1. **Validate Before Conversion**:
   - Check data ranges fit target type
   - Identify invalid values before conversion
   - Use TRY_CAST or CASE to preview conversion results
   - Test on sample data first

2. **Choose Appropriate Precision**:
   - DECIMAL(18,2) for currency (dollars and cents)
   - DECIMAL(10,4) for exchange rates
   - DECIMAL(5,4) for percentages and tax rates
   - Don't use excessive precision (wastes storage)

3. **Consider Storage Implications**:
   - BYTEINT for flags (0/1) - 1 byte
   - SMALLINT for small counts - 2 bytes
   - INTEGER for general numeric - 4 bytes
   - Use smallest type that fits data range

4. **Handle Conversion Errors**:
   - Test conversions on sample data
   - Invalid conversions may result in NULLs or errors
   - Validate data quality before converting
   - Consider data cleansing first

5. **Document Type Choices**:
   - Comment why specific types chosen
   - Document precision requirements
   - Note business rules for data types
   - Track conversion logic for reproducibility

6. **Performance Optimization**:
   - Convert early in ETL pipeline
   - Index on properly typed columns
   - Avoid implicit type conversions in queries
   - Match types across JOIN keys

7. **DATE/TIME Conversions**:
   - Ensure source format matches target
   - Use consistent date formats across tables
   - Consider time zones for TIMESTAMP WITH ZONE
   - Validate date ranges are valid

8. **Character Set Considerations**:
   - Specify LATIN for English-only data (saves space)
   - Use UNICODE for international characters
   - Match character set across related columns
   - Consider case-specific settings

## Related Functions

- **TD_SimpleImputeFit/Transform**: Handle missing values before type conversion
- **TD_OutlierFilterFit/Transform**: Remove outliers before conversion
- **TD_ColumnTransformer**: Apply multiple transformations including type conversions
- **CAST/TRY_CAST**: Standard SQL type conversion (alternative approach)
- **TD_GetFutileColumns**: Identify columns to remove before type optimization

## Notes and Limitations

1. **Conversion Rules**:
   - Conversions must be logically valid
   - String to numeric requires parseable numeric strings
   - Precision loss may occur (DECIMAL → INTEGER truncates)
   - Invalid conversions may produce NULLs or errors

2. **Data Loss**:
   - INTEGER → BYTEINT fails if value > 127 or < -128
   - DECIMAL → INTEGER truncates decimal places
   - VARCHAR(50) → VARCHAR(20) truncates if data longer
   - Always validate data ranges before conversion

3. **Character Set Changes**:
   - LATIN to UNICODE conversion always safe
   - UNICODE to LATIN may fail if non-Latin characters present
   - CLOB conversions preserve character set by default
   - Specify charset explicitly when needed

4. **Performance**:
   - Type conversions add processing overhead
   - Large tables may take significant time
   - Consider parallel processing for very large datasets
   - Test performance on representative data size

5. **NULL Handling**:
   - NULL values pass through unchanged
   - NULL in any type converts to NULL in target type
   - Does not impute or remove NULLs

6. **VARCHAR/CHAR Defaults**:
   - Default lengths may be larger than needed
   - Explicitly specify length for storage optimization
   - VARCHAR(32000) default may be excessive
   - Review defaults and adjust as appropriate

7. **Date Format Requirements**:
   - String to DATE requires valid date format
   - Default format: 'YYYY/MM/DD' or 'YYYY-MM-DD'
   - Invalid formats cause conversion errors
   - Consider data cleansing before conversion

8. **DECIMAL Precision**:
   - Maximum 38 total digits
   - Maximum 19 decimal places
   - Exceeding limits causes errors
   - Choose precision carefully

## Usage Notes

Data types define the kind of data that can be stored in a column, such as text, numbers, dates, or Boolean values. Converting a column's data type may be necessary to ensure that the data is in the appropriate format for analysis or modeling.

**Benefits of Type Conversion**:

1. **Improved Accuracy**: Proper types enable correct calculations and comparisons
2. **Enhanced Efficiency**: Appropriate types improve query performance and reduce storage
3. **Error Detection**: Conversions identify data inconsistencies and quality issues
4. **Space Reduction**: Converting INTEGER (4 bytes) to BYTEINT (1 byte) saves 75% storage
5. **Enable Operations**: DATE types enable temporal operations, numeric types enable math

**Example Benefits**:
- Convert string dates to DATE to perform date arithmetic
- Convert text numbers to INTEGER/DECIMAL for aggregations
- Convert large INTEGER to BYTEINT for binary flags (saves 15 bytes per row)
- Detect invalid data when conversions fail

## Version Information

- **Function Version**: Based on Teradata Database Analytic Functions Version 17.20
- **Generated**: November 29, 2025
- **Category**: Data Cleaning Functions / Data Type Management / Schema Optimization
