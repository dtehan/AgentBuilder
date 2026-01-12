# TD_ColumnSummary

### Function Name
**TD_ColumnSummary**

### Description
TD_ColumnSummary is a function where the contents of a column are grouped and presented with respect to certain standard values. Summarizing a column in terms of positive, negative, null, and other similar values can be useful for data cleaning, exploration, validation, and reporting.

TD_ColumnSummary displays the following for each specified input table column:
- Column name
- Column data type
- Count of non-NULL, NULL, blank, zero, positive, and negative values
- Percentage of NULL and non-NULL values

### When the Function Would Be Used
- **Data Cleaning**: Identifying missing data (NULL values) which can be removed or imputed
- **Data Exploration**: Identifying trends or patterns in positive vs negative values
- **Data Validation**: Identifying errors or anomalies (e.g., negative values where impossible)
- **Reporting**: Providing quick summaries for reports or presentations
- **Quality Assessment**: Understanding data completeness and distribution
- **Correlation Analysis**: Understanding dependency between columns based on their summaries
- **Exploratory Data Analysis (EDA)**: Getting a quick overview of column characteristics

### Syntax
```sql
TD_ColumnSummary (
    ON { table | view | (query) } AS InputTable
    USING
    TargetColumns ({ 'target_column' | target_column_range }[,...])
)
```

### Required Syntax Elements for TD_ColumnSummary

**ON clause**
- Accept the InputTable clause

**TargetColumns**
- Specify the names of the InputTable columns to summarize
- Supports column ranges using bracket notation (e.g., '[10:11]', '[:]')

### Optional Syntax Elements for TD_ColumnSummary
All syntax elements are required.

### Input Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | Any | Column to display summary |

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| ColumnName | VARCHAR (CHARACTER SET UNICODE) | Name of target column |
| DataType | VARCHAR (CHARACTER SET LATIN) | Data type of target column |
| NonNullCount | BIGINT | Count of non-NULL values in target column |
| NullCount | BIGINT | Count of NULL values in target column |
| BlankCount | BIGINT | Count of blank values (all spaces) when data type is CHAR or VARCHAR; otherwise NULL |
| ZeroCount | BIGINT | Count of zero values when data type is NUMERIC; otherwise NULL |
| PositiveCount | BIGINT | Count of positive values when data type is NUMERIC; otherwise NULL |
| NegativeCount | BIGINT | Count of negative values when data type is NUMERIC; otherwise NULL |
| NullPercentage | DOUBLE PRECISION | Percentage of NULL values in target column |
| NonNullPercentage | DOUBLE PRECISION | Percentage of non-NULL values in target column |

### Code Examples

**Input Table: col_titanic_train**
```
passenger  survived  pclass  name                                         gender  age   embarked  cabin
49         0         3       Samaan; Mr. Youssef                          male    null  C         null
78         0         3       Moutal; Mr. Rahamin Haim                     male    null  S         null
505        1         1       Maioni; Miss. Roberta                        female  16    S         B79
631        1         1       Barkworth; Mr. Algernon Henry Wilson         male    80    S         A23
873        0         1       Carlsson; Mr. Frans Olof                     male    33    S         B51 B53 B55
```

**Example 1: Using Column Names**
```sql
SELECT * FROM TD_ColumnSummary (
    ON col_titanic_train AS InputTable
    USING
    TargetColumns ('age','pclass','embarked','cabin')
) AS dt;
```

**Example 2: Using Column Range Indexing**
```sql
-- Select columns at positions 10 and 11 (0-based indexing)
SELECT * FROM TD_ColumnSummary (
    ON col_titanic_train AS InputTable
    USING
    TargetColumns ('[10:11]')
) AS dt;
```

**Output:**
```
ColumnName  DataType                         NonNullCount  NullCount  BlankCount  ZeroCount  PositiveCount  NegativeCount  NullPercentage  NonNullPercentage
age         INTEGER                          3             2          null        0          3              0              40.0            60.0
cabin       VARCHAR(20) CHARACTER SET LATIN  3             2          0           null       null           null           40.0            60.0
embarked    VARCHAR(20) CHARACTER SET LATIN  5             0          0           null       null           null           0.0             100.0
pclass      INTEGER                          5             0          null        0          5              0              0.0             100.0
```

**Example 3: Analyzing Multiple Columns for Data Quality**
```sql
-- Check data quality across numeric and text columns
SELECT * FROM TD_ColumnSummary (
    ON customer_transactions AS InputTable
    USING
    TargetColumns ('transaction_amount', 'customer_id', 'transaction_date', 'status')
) AS dt;
```

**Example 4: Using All Columns**
```sql
-- Summarize all columns in the table using [:]
SELECT * FROM TD_ColumnSummary (
    ON sales_data AS InputTable
    USING
    TargetColumns ('[:]')
) AS dt
ORDER BY NullPercentage DESC;
```

**Example 5: Identifying Columns with Missing Data**
```sql
-- Find columns with more than 20% NULL values
SELECT * FROM TD_ColumnSummary (
    ON patient_records AS InputTable
    USING
    TargetColumns ('blood_pressure', 'heart_rate', 'temperature', 'glucose_level')
) AS dt
WHERE NullPercentage > 20.0;
```

**Example 6: Checking for Invalid Numeric Values**
```sql
-- Identify columns with negative values that shouldn't have them
SELECT
    ColumnName,
    NegativeCount,
    NonNullCount,
    (NegativeCount * 100.0 / NonNullCount) AS NegativePercentage
FROM TD_ColumnSummary (
    ON product_inventory AS InputTable
    USING
    TargetColumns ('quantity_on_hand', 'price', 'weight')
) AS dt
WHERE NegativeCount > 0;
```

### Column Summary Calculation Steps

For each target column:
1. Count the total number of values (n) in the column
2. Count the number of blank values (b) in the column
3. Count the number of zero values (z) in the column
4. Count the number of null values (null) in the column
5. Count the number of not null values (n - null) in the column
6. Count the number of positive values (pos) in the column
7. Count the number of negative values (neg) in the column
8. Calculate the percentage of blank values (b/n * 100)
9. Calculate the percentage of zero values (z/n * 100)
10. Calculate the percentage of null values (null/n * 100)
11. Calculate the percentage of positive values (pos/n * 100)
12. Calculate the percentage of negative values (neg/n * 100)

### Important Notes
- For numeric data types: ZeroCount, PositiveCount, and NegativeCount are calculated
- For character data types: BlankCount is calculated (values with all space characters)
- NULL values are counted separately for all data types
- Percentages help quickly assess data completeness
- Useful for initial data profiling before ML model development
- Can identify data quality issues early in the analysis pipeline

### Related Functions
- TD_CategoricalSummary - For categorical column value distributions
- TD_UnivariateStatistics - For detailed statistical measures
- TD_GetRowsWithMissingValues - For retrieving rows with NULL values
- TD_Histogram - For frequency distribution analysis

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Data Exploration Functions
