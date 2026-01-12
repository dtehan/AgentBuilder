# TD_WhichMax

### Function Name
**TD_WhichMax**

### Description
TD_WhichMax displays all rows that have the maximum value in a specified input table column. The maximum value represents the upper limit of a quantity or set of values. For example, if we have a set of numbers such as {3, 5, 1, 7, 2}, the maximum value would be 7 since it is the largest number in the set.

### When the Function Would Be Used
- **Outlier Identification**: Maximum values may indicate the presence of outliers that can skew statistical analyses
- **Range Understanding**: Knowing maximum values helps understand the range and spread of data
- **Performance Benchmarking**: Establishing performance benchmarks (e.g., fastest time, highest stock price)
- **Safety Standards**: Establishing safety standards based on maximum load, wind speed, or other parameters
- **Data Quality**: Identifying potential errors or unexpected extreme values
- **Business Intelligence**: Finding top performers, highest sales, peak values
- **Measurement Accuracy**: Determining precision of measurements
- **Goal Setting**: Using maximum values as benchmarks for future performance
- **Anomaly Detection**: Detecting unusual or suspicious maximum values

### Syntax
```sql
TD_WhichMax (
    ON { table | view | (query) } AS InputTable
    [ PARTITION BY ANY [ORDER BY order_by_column ] ]
    USING
    TargetColumn ('target_column')
)
```

### Required Syntax Elements for TD_WhichMax

**ON clause**
- Accept the InputTable clause
- Optionally accepts PARTITION BY ANY and ORDER BY clauses

**TargetColumn**
- Specify the target column name to determine maximum values
- Only one column can be specified

### Optional Syntax Elements for TD_WhichMax

**PARTITION BY ANY**
- Accept the order_by_column clause for ordering results

### Input Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | Any except BLOB, CLOB, and UDT | Column for which maximum values are checked |

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | Any except BLOB, CLOB, and UDT | All columns from input table for rows with maximum value |

### Code Examples

**Input Table: titanic_dataset**
```
passenger  survived  pclass  gender  age  sibsp  parch  fare    cabin  embarked
1          0         3       male    22   1      0      7.25    null   S
2          1         1       female  38   1      0      71.28   C85    C
3          1         3       female  26   0      0      7.93    null   S
4          1         1       female  35   1      0      53.10   C123   S
5          0         3       male    35   0      0      8.05    null   S
```

**Example 1: Find Maximum Fare**
```sql
SELECT * FROM TD_WhichMax (
    ON titanic_dataset AS InputTable
    USING
    TargetColumn ('fare')
) AS dt;
```

**Output:**
```
passenger  survived  pclass  gender  age  sibsp  parch  fare   cabin  embarked
2          1         1       female  38   1      0      71.28  C85    C
```

**Example 2: Find Oldest Passenger**
```sql
SELECT * FROM TD_WhichMax (
    ON titanic_dataset AS InputTable
    USING
    TargetColumn ('age')
) AS dt;
```

**Example 3: Find Highest Sales Amount**
```sql
-- Identify the highest grossing transaction(s)
SELECT * FROM TD_WhichMax (
    ON sales_transactions AS InputTable
    USING
    TargetColumn ('transaction_amount')
) AS dt;
```

**Example 4: Find Peak Temperature Reading**
```sql
-- Identify maximum temperature recorded
SELECT * FROM TD_WhichMax (
    ON weather_data AS InputTable
    USING
    TargetColumn ('temperature')
) AS dt;
```

**Example 5: Find Maximum Stock Price**
```sql
-- Find the record(s) with highest stock closing price
SELECT * FROM TD_WhichMax (
    ON stock_prices AS InputTable
    USING
    TargetColumn ('closing_price')
) AS dt;
```

**Example 6: Find Top Product Rating**
```sql
-- Identify products with highest customer rating
SELECT * FROM TD_WhichMax (
    ON product_reviews AS InputTable
    USING
    TargetColumn ('rating')
) AS dt;
```

**Example 7: Multiple Rows with Same Maximum**
```sql
-- If multiple rows share the maximum value, all are returned
SELECT * FROM TD_WhichMax (
    ON employee_salaries AS InputTable
    USING
    TargetColumn ('salary')
) AS dt;
```

**Example 8: With ORDER BY for Sorted Results**
```sql
SELECT * FROM TD_WhichMax (
    ON customer_purchases AS InputTable
    PARTITION BY ANY ORDER BY purchase_date DESC
    USING
    TargetColumn ('purchase_amount')
) AS dt;
```

**Example 9: Finding Peak Load Times**
```sql
-- Identify when system experienced maximum load
SELECT * FROM TD_WhichMax (
    ON system_metrics AS InputTable
    USING
    TargetColumn ('cpu_utilization')
) AS dt;
```

**Example 10: Highest Revenue by Category**
```sql
-- Find maximum revenue record
SELECT
    category,
    product_name,
    revenue,
    date
FROM TD_WhichMax (
    ON product_revenue AS InputTable
    USING
    TargetColumn ('revenue')
) AS dt;
```

### Use Cases and Applications

**1. Engineering & Safety**
- Determine maximum load bridges can support
- Establish maximum wind speeds buildings must withstand
- Set safety guidelines based on maximum stress levels

**2. Financial Markets**
- Identify highest stock prices for benchmarking
- Find peak trading volumes
- Detect maximum price volatility periods

**3. Sports & Performance**
- Record fastest times in races
- Track highest scores or best performances
- Establish performance benchmarks

**4. Weather & Climate**
- Identify record high temperatures
- Track maximum rainfall or snowfall
- Monitor peak wind speeds

**5. Business Intelligence**
- Find top-selling products or services
- Identify highest-revenue customers
- Locate peak sales periods

**6. Quality Control**
- Detect maximum defect rates
- Identify peak failure times
- Monitor maximum response times

### Important Notes
- Returns ALL rows that share the maximum value (not just one row)
- If multiple rows have the same maximum value, all matching rows are returned
- Target column can be any data type except BLOB, CLOB, and user-defined types (UDT)
- Useful for identifying outliers and establishing upper bounds
- Consider using with TD_UnivariateStatistics for comprehensive statistical analysis
- Maximum values can indicate data quality issues if unexpectedly high
- Function returns entire rows, not just the maximum value

### Comparison with Other Functions
- **TD_WhichMin**: Returns rows with minimum values (opposite of TD_WhichMax)
- **TD_UnivariateStatistics**: Provides MAX statistic among other measures
- **SQL MAX()**: Returns only the maximum value, not the entire rows
- **TD_Histogram**: Shows distribution including extreme values

### Related Functions
- TD_WhichMin - Returns rows with minimum values
- TD_UnivariateStatistics - Comprehensive statistics including MAX
- TD_Histogram - Distribution analysis including extremes
- TD_ColumnSummary - Column-level summaries including maximum values

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Data Exploration Functions
