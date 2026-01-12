# TD_GetRowsWithMissingValues

### Function Name
**TD_GetRowsWithMissingValues**

### Description
TD_GetRowsWithMissingValues is a function that retrieves all rows or records from a dataset that contain one or more missing or null values in specified columns. This function is essential for identifying and handling missing values in datasets during data cleaning and preprocessing tasks.

### When the Function Would Be Used
- **Imputation**: Identifying rows with missing values before imputing them with estimated values
- **Outlier Detection**: Missing values can sometimes indicate outliers or extreme values that need investigation
- **Data Quality Assessment**: Assessing overall data quality and determining if data is suitable for analysis
- **Feature Engineering**: Identifying missing value patterns for creating new features in machine learning
- **Data Cleaning**: Removing or handling rows with missing values before analysis
- **Bias Prevention**: Ensuring missing values don't lead to biased or inaccurate analysis results
- **Model Preparation**: Many ML algorithms cannot handle missing values, so identification is crucial

### Syntax
```sql
TD_GetRowsWithMissingValues (
    ON { table | view | (query) } AS InputTable
    [ PARTITION BY ANY [ORDER BY order_column ] ]
    [ USING
        TargetColumns ({ 'target_column' | target_column_range }[,...])
        [ Accumulate ({ 'accumulate_column' | accumulate_column_range }[,...]) ]
    ]
)
```

### Required Syntax Elements for TD_GetRowsWithMissingValues

**ON clause**
- Accept the InputTable clause
- Optionally accepts PARTITION BY ANY and ORDER BY clauses

### Optional Syntax Elements for TD_GetRowsWithMissingValues

**TargetColumns**
- Specify the target column names to check for NULL values
- Supports column ranges using bracket notation
- Default: If omitted, the function considers all columns of the InputTable

**Accumulate**
- Specify the input table column names to copy to the output table
- Useful for retaining identifier columns or other important columns

### Input Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | Any | Columns for which NULL values are checked |
| accumulate_column | Any | Input table column names to copy to output table |

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | Any | Columns for which NULL values are checked |
| accumulate_column | Any | Input table column names copied to output table |

### Code Examples

**Input Table: input_table**
```
passenger  survived  pclass  name                                         gender  age  ticket     fare    cabin  embarked
1          0         3       Braund; Mr. Owen Harris                      male    22   A/5 21171  7.25    null   S
30         0         3       Todoroff; Mr. Lalio                          male    null 349216     7.8958  null   S
505        1         1       Maioni; Miss. Roberta                        female  16   110152     86.5    B79    S
631        1         1       Barkworth; Mr. Algernon Henry Wilson         male    80   27042      30      A23    S
873        0         1       Carlsson; Mr. Frans Olof                     male    33   695        5       B51    S
```

**Example 1: Find Rows with Missing Values in Specific Columns**
```sql
SELECT * FROM TD_getRowsWithMissingValues (
    ON input_table AS InputTable
    USING
    TargetColumns ('[name:cabin]')
) AS dt;
```

**Output:**
```
passenger  survived  pclass  name                     gender  age   ticket     fare    cabin  embarked
1          0         3       Braund; Mr. Owen Harris  male    22    A/5 21171  7.25    null   S
30         0         3       Todoroff; Mr. Lalio      male    null  349216     7.8958  null   S
```

**Example 2: Check All Columns for Missing Values**
```sql
-- Check all columns by omitting TargetColumns parameter
SELECT * FROM TD_getRowsWithMissingValues (
    ON customer_data AS InputTable
) AS dt;
```

**Example 3: Find Missing Values with Specific Accumulate Columns**
```sql
-- Check for missing values in key columns while keeping identifiers
SELECT * FROM TD_getRowsWithMissingValues (
    ON sales_transactions AS InputTable
    USING
    TargetColumns ('transaction_amount', 'customer_id', 'product_id')
    Accumulate ('transaction_id', 'transaction_date')
) AS dt;
```

**Example 4: Identify Incomplete Patient Records**
```sql
-- Find patient records with missing critical health data
SELECT * FROM TD_getRowsWithMissingValues (
    ON patient_health_records AS InputTable
    USING
    TargetColumns ('blood_pressure', 'heart_rate', 'temperature', 'glucose_level')
    Accumulate ('patient_id', 'visit_date', 'doctor_name')
) AS dt
ORDER BY patient_id, visit_date;
```

**Example 5: Detect Missing Product Information**
```sql
-- Find products with incomplete catalog information
SELECT * FROM TD_getRowsWithMissingValues (
    ON product_catalog AS InputTable
    USING
    TargetColumns ('product_description', 'price', 'category', 'supplier_id')
    Accumulate ('product_id', 'product_name')
) AS dt;
```

**Example 6: Quality Check for Survey Responses**
```sql
-- Identify survey responses with missing answers
SELECT * FROM TD_getRowsWithMissingValues (
    ON survey_responses AS InputTable
    USING
    TargetColumns ('q1_response', 'q2_response', 'q3_response', 'q4_response', 'q5_response')
    Accumulate ('respondent_id', 'survey_date', 'demographic_group')
) AS dt;
```

**Example 7: Count Missing Values by Category**
```sql
-- Combine with aggregate functions to understand missing value patterns
SELECT
    category,
    COUNT(*) as rows_with_missing_values
FROM TD_getRowsWithMissingValues (
    ON inventory_data AS InputTable
    USING
    TargetColumns ('quantity', 'reorder_point', 'last_order_date')
    Accumulate ('category', 'warehouse_location')
) AS dt
GROUP BY category
ORDER BY rows_with_missing_values DESC;
```

### Important Notes
- This function returns ONLY rows that have at least one NULL value in the specified target columns
- If no TargetColumns are specified, all columns are checked for NULL values
- The function helps ensure analyses are based on complete and accurate data
- Use in conjunction with TD_SimpleImputeFit for handling missing values
- Complements TD_GetRowsWithoutMissingValues which returns rows WITHOUT missing values
- Essential step before training machine learning models
- Can be used to understand missing data patterns and mechanisms

### Related Functions
- TD_GetRowsWithoutMissingValues - Returns rows WITHOUT missing values
- TD_ColumnSummary - Provides statistics on NULL counts and percentages
- TD_SimpleImputeFit - Imputes missing values
- TD_SimpleImputeTransform - Applies imputation to data

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Data Exploration Functions
