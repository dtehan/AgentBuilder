# MovingAverage

### Function Name
**MovingAverage**

### Description
The MovingAverage function computes average values in a series, using the specified moving average type. Moving Average (MA) is a widely used technical analysis indicator that is used to smooth out fluctuations in a data series and to identify trends.

### When the Function Would Be Used
- **Financial Analysis**: Stock price analysis, identifying market trends, support and resistance levels, and potential buy or sell signals
- **Weather Forecasting**: Smoothing out variations in temperature, humidity, or wind speed over time to identify weather patterns
- **Traffic Analysis**: Analyzing traffic flow and congestion patterns to identify peak travel times
- **Manufacturing**: Monitoring quality control and production efficiency over time
- **Healthcare**: Analyzing trends in disease outbreaks, patient outcomes, and health-related data
- **Time Series Analysis**: Any situation where fluctuations and trends need to be identified and analyzed over time

### Moving Average Types
1. **Weighted Moving Average ('W')**: Applies weights to older values that decrease arithmetically
2. **Triangular Moving Average ('T')**: Computes double-smoothed average of points in series
3. **Simple Moving Average ('S')**: Computes unweighted mean of previous n data points
4. **Modified Moving Average ('M')**: First value as simple moving average, subsequent values by adding new value and subtracting last average
5. **Exponential Moving Average ('E')**: Applies damping factor that exponentially decreases weights of older values
6. **Cumulative Moving Average ('C')**: Computes cumulative moving average from beginning of series

### Syntax
```sql
MovingAverage (
    ON { table | view | (query) }
    [ PARTITION BY partition_column [,...] ]
    [ ORDER BY order_column [,...] ]
    [ USING
        [ MAvgType ({ 'C' | 'E' | 'M' | 'S' | 'T' | 'W' }) ]
        [ TargetColumns ({'target_column'| 'target_column_range'}[,...])]
        [ Alpha (alpha) ]
        [ StartRows (n) ]
        [ IncludeFirst ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
        [ WindowSize (window_size) ]
    ]
)
```

### Required Syntax Elements for MovingAverage

**ON clause**
- Accepts the PARTITION BY and ORDER BY clauses
- **Important**: If the ON clause does not include the PARTITION BY and ORDER BY clauses, results are nondeterministic
- The ORDER BY clause supports only ASCII collation
- The PARTITION BY clause assumes column names are in Normalization Form C (NFC)

### Optional Syntax Elements for MovingAverage

**MAvgType**
- Specify one of the following moving average types:
  - `'C'` (Default): Cumulative moving average
  - `'E'`: Exponential moving average
  - `'M'`: Modified moving average
  - `'S'`: Simple moving average
  - `'T'`: Triangular moving average
  - `'W'`: Weighted moving average

**TargetColumns**
- Specify the input column names for which to compute the moving average
- Default: The function copies every input column to the output table but does not compute any moving averages

**Alpha**
- [Optional with MAvgType E, otherwise ignored]
- Specify the damping factor, a value in the range [0, 1]
- Represents a percentage in the range [0, 100]
- Higher alpha discounts older observations faster
- Default: 0.1

**StartRows**
- [Optional with MAvgType E, otherwise ignored]
- Specify the number of rows to skip before calculating the exponential moving average
- The function uses the arithmetic average of these rows as the initial value
- Default: 2

**IncludeFirst**
- [Ignored with MAvgType C, otherwise optional]
- Specify whether to include the starting rows in the output table
- If 'true', output columns for starting rows contain NULL
- Default: 'false'

**WindowSize**
- [Optional with MAvgType M, S, T, and W; otherwise ignored]
- Specify the number of previous values to consider when computing the new moving average
- Data type must be BYTEINT, SMALLINT, or INTEGER
- Minimum value: 3
- Default: '10'

### Input Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| partition_column | Any | Column by which input data is partitioned. Must contain all rows of an entity |
| order_column | Any | Column by which input table is ordered |
| target_column | INTEGER, SMALLINT, BIGINT, NUMERIC, NUMBER, or DOUBLE PRECISION | Values to average |

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| partition_column | Same as input | Column by which input data is partitioned |
| order_column | Same as input | Column by which input table is ordered |
| target_column | Same as input | Column copied from input table |
| target_column_typemavg | DOUBLE PRECISION | Moving average of target_column values |

### Code Examples

**Input Table: company1_stock**
```
id    name      period                      stockprice
1     Company1  1961-05-17 00:00:00.000000  460.000000000000
2     Company1  1961-05-18 00:00:00.000000  457.000000000000
3     Company1  1961-05-19 00:00:00.000000  452.000000000000
...
```

**Example 1: Simple Moving Average**
```sql
SELECT * FROM MovingAverage (
    ON company1_stock PARTITION BY name ORDER BY period
    USING
    MAvgType ('S')
    TargetColumns ('stockprice')
    WindowSize (10)
    IncludeFirst ('true')
) AS dt ORDER BY id;
```

**Example 2: Weighted Moving Average**
```sql
SELECT * FROM MovingAverage (
    ON company1_stock PARTITION BY name ORDER BY period
    USING
    MAvgType ('W')
    TargetColumns ('stockprice')
    WindowSize (10)
    IncludeFirst ('true')
) AS dt ORDER BY id;
```

**Example 3: Exponential Moving Average**
```sql
SELECT * FROM MovingAverage (
    ON company1_stock PARTITION BY name ORDER BY period
    USING
    MAvgType ('E')
    TargetColumns ('stockprice')
    StartRows (10)
    Alpha (0.1)
    IncludeFirst ('true')
) AS dt ORDER BY id;
```

**Example 4: Modified Moving Average**
```sql
SELECT * FROM MovingAverage (
    ON company1_stock PARTITION BY name ORDER BY period
    USING
    MAvgType ('M')
    TargetColumns ('stockprice')
    WindowSize (10)
    IncludeFirst ('true')
) AS dt ORDER BY id;
```

**Example 5: Cumulative Moving Average**
```sql
SELECT * FROM MovingAverage (
    ON company1_stock PARTITION BY name ORDER BY period
    USING
    MAvgType ('C')
    TargetColumns ('stockprice')
) AS dt ORDER BY id;
```

**Example 6: Triangular Moving Average**
```sql
SELECT * FROM MovingAverage (
    ON company1_stock PARTITION BY name ORDER BY period
    USING
    MAvgType ('T')
    TargetColumns ('stockprice')
    WindowSize (10)
    IncludeFirst ('true')
) AS dt ORDER BY id;
```

### Related Functions
- TD_UnivariateStatistics - For basic statistical measures
- TD_Histogram - For frequency distribution analysis
- Other time series analysis functions in the Data Exploration category

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Data Exploration Functions
