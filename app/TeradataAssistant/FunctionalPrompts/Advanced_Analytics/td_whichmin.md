# TD_WhichMin

### Function Name
**TD_WhichMin**

### Description
TD_WhichMin displays all rows that have the minimum value in a specified input table column. The minimum value represents the lower limit of a quantity or set of values. For example, if we have a set of numbers such as {3, 5, 1, 7, 2}, the minimum value would be 1 since it is the smallest number in the set.

Minimum values are often used in optimization problems to find the smallest possible value of a function within a given domain. This can be useful in various fields such as engineering, economics, and physics.

### When the Function Would Be Used
- **Quality Control**: Identifying potential errors in data (e.g., unexpected minimum values indicating data problems)
- **Data Normalization**: Providing a baseline for comparison by setting minimum value to zero
- **Outlier Detection**: Identifying unusual data points at the lower end of the distribution
- **Machine Learning**: Scaling data by setting minimum value as baseline
- **Optimization Problems**: Finding minimum cost, time, distance, or resource usage
- **Performance Analysis**: Identifying worst-case scenarios or bottlenecks
- **Data Validation**: Detecting impossible values (e.g., negative temperatures in Celsius below absolute zero)
- **Baseline Establishment**: Setting lower bounds for comparisons and analyses
- **Budget Planning**: Finding minimum costs or resource requirements

### Syntax
```sql
TD_WhichMin (
    ON { table | view | (query) } AS InputTable
    [ PARTITION BY ANY [ORDER BY order_by_column ] ]
    USING
    TargetColumn ('target_column')
)
```

### Required Syntax Elements for TD_WhichMin

**ON clause**
- Accept the InputTable clause
- Optionally accepts PARTITION BY ANY and ORDER BY clauses

**TargetColumn**
- Specify the target column name to check for minimum values
- Only one column can be specified

### Optional Syntax Elements for TD_WhichMin

**PARTITION BY ANY**
- Accept the order_by_column clause for ordering results

### Input Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | Any except BLOB, CLOB, and UDT | Column for which minimum values are checked |

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | Any except BLOB, CLOB, and UDT | All columns from input table for rows with minimum value |

### Code Examples

**Input Table: titanic_dataset**
```
passenger  survived  pclass  gender  age  sibsp  parch  fare   cabin  embarked
1          0         3       male    22   1      0      7.25   null   S
2          1         1       female  38   1      0      71.28  C85    C
3          1         3       female  26   0      0      7.93   null   S
4          1         1       female  35   1      0      53.10  C123   S
5          0         3       male    35   0      0      8.05   null   S
```

**Example 1: Find Minimum Fare**
```sql
SELECT * FROM TD_WhichMin (
    ON titanic_dataset AS InputTable
    USING
    TargetColumn ('fare')
) AS dt;
```

**Output:**
```
passenger  survived  pclass  gender  age  sibsp  parch  fare  cabin  embarked
1          0         3       male    22   1      0      7.25  null   S
```
The output shows the row that has the lowest value in the fare column.

**Example 2: Find Youngest Passenger**
```sql
SELECT * FROM TD_WhichMin (
    ON titanic_dataset AS InputTable
    USING
    TargetColumn ('age')
) AS dt;
```

**Example 3: Find Lowest Sales Amount**
```sql
-- Identify the lowest grossing transaction(s)
SELECT * FROM TD_WhichMin (
    ON sales_transactions AS InputTable
    USING
    TargetColumn ('transaction_amount')
) AS dt;
```

**Example 4: Find Minimum Temperature Reading**
```sql
-- Identify minimum temperature recorded
SELECT * FROM TD_WhichMin (
    ON weather_data AS InputTable
    USING
    TargetColumn ('temperature')
) AS dt;
```

**Example 5: Find Minimum Stock Price**
```sql
-- Find the record(s) with lowest stock closing price
SELECT * FROM TD_WhichMin (
    ON stock_prices AS InputTable
    USING
    TargetColumn ('closing_price')
) AS dt;
```

**Example 6: Find Lowest Product Rating**
```sql
-- Identify products with lowest customer rating
SELECT * FROM TD_WhichMin (
    ON product_reviews AS InputTable
    USING
    TargetColumn ('rating')
) AS dt;
```

**Example 7: Multiple Rows with Same Minimum**
```sql
-- If multiple rows share the minimum value, all are returned
SELECT * FROM TD_WhichMin (
    ON employee_salaries AS InputTable
    USING
    TargetColumn ('salary')
) AS dt;
```

**Example 8: With ORDER BY for Sorted Results**
```sql
SELECT * FROM TD_WhichMin (
    ON customer_purchases AS InputTable
    PARTITION BY ANY ORDER BY purchase_date DESC
    USING
    TargetColumn ('purchase_amount')
) AS dt;
```

**Example 9: Finding Minimum Response Times**
```sql
-- Identify fastest system response times
SELECT * FROM TD_WhichMin (
    ON api_metrics AS InputTable
    USING
    TargetColumn ('response_time_ms')
) AS dt;
```

**Example 10: Lowest Inventory Levels**
```sql
-- Find products with minimum stock levels
SELECT
    product_id,
    product_name,
    quantity_on_hand,
    warehouse_location
FROM TD_WhichMin (
    ON inventory AS InputTable
    USING
    TargetColumn ('quantity_on_hand')
) AS dt;
```

### Use Cases and Applications

**1. Data Quality & Validation**
- Detect impossible or erroneous values
- Example: Finding negative ages or prices
- Example: Identifying temperature readings below absolute zero
- Validate data entry accuracy

**2. Data Normalization**
- Set baseline for data scaling
- Create normalized scales starting from zero
- Enable fair comparisons across different scales
- Prepare data for machine learning algorithms

**3. Optimization**
- Find minimum costs in supply chain
- Identify shortest paths or routes
- Locate minimum resource requirements
- Determine lowest energy consumption

**4. Performance Analysis**
- Identify best performance times (minimum time = fastest)
- Find lowest latency periods
- Detect minimum resource utilization
- Analyze efficiency metrics

**5. Quality Control**
- Identify products below quality thresholds
- Find minimum acceptable standards
- Detect performance degradation
- Monitor lower control limits

**6. Financial Analysis**
- Find lowest prices for purchasing
- Identify minimum viable costs
- Detect price floors
- Analyze worst-case scenarios

### Important Notes
- Returns ALL rows that share the minimum value (not just one row)
- If multiple rows have the same minimum value, all matching rows are returned
- Target column can be any data type except BLOB, CLOB, and user-defined types (UDT)
- Useful for establishing lower bounds and identifying potential data errors
- Consider using with TD_UnivariateStatistics for comprehensive statistical analysis
- Minimum values can indicate data quality issues if unexpectedly low or negative
- Function returns entire rows, not just the minimum value
- Particularly useful in optimization and cost minimization scenarios

### Data Normalization Example

Setting the minimum value to zero for normalization:
```sql
-- Step 1: Find the minimum value
CREATE TABLE min_value AS
SELECT MIN(value) as min_val
FROM dataset;

-- Step 2: Normalize by subtracting minimum
SELECT
    id,
    value,
    value - min_val as normalized_value
FROM dataset, min_value;
```

### Comparison with Other Functions
- **TD_WhichMax**: Returns rows with maximum values (opposite of TD_WhichMin)
- **TD_UnivariateStatistics**: Provides MIN statistic among other measures
- **SQL MIN()**: Returns only the minimum value, not the entire rows
- **TD_Histogram**: Shows distribution including extreme values

### Related Functions
- TD_WhichMax - Returns rows with maximum values
- TD_UnivariateStatistics - Comprehensive statistics including MIN
- TD_Histogram - Distribution analysis including extremes
- TD_ColumnSummary - Column-level summaries including minimum values
- TD_ScaleFit/TD_ScaleTransform - For data normalization and scaling

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Data Exploration Functions
