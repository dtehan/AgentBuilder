# TD_Histogram

### Function Name
**TD_Histogram**

### Description
TD_Histogram calculates the frequency distribution of a dataset using one of the following methods: Sturges, Scott, Variable-width, or Equal-width. A histogram is a graphical representation of the distribution of numerical data consisting of rectangles (bars) that represent the frequency of occurrences of data values within certain intervals or "bins."

### When the Function Would Be Used
- **Data Distribution Analysis**: Visualizing and understanding the distribution of numerical data
- **Outlier Identification**: Detecting outliers or unusual data points that fall outside typical ranges
- **Pattern Recognition**: Identifying patterns, peaks, or trends in data distributions
- **Data Quality Assessment**: Assessing data quality and identifying anomalies
- **Exploratory Data Analysis (EDA)**: Initial data exploration to understand data characteristics
- **Statistical Analysis**: Determining if data is normally distributed, skewed, or follows other patterns
- **Feature Engineering**: Understanding feature distributions before model training
- **Comparison Analysis**: Comparing distributions across different datasets or variables

### Histogram Types
1. **Continuous Histograms**: For continuous data like height or weight with equal-width intervals
2. **Discrete Histograms**: For discrete data like counts, with integer values as bins
3. **Frequency Polygon**: Lines connecting points instead of bars
4. **Cumulative Histogram**: Shows cumulative frequency with stacked bars
5. **2D Histogram**: Represents joint distribution of two variables
6. **Kernel Density Estimation Histogram**: Smooth version estimating probability density function

### Syntax
```sql
TD_Histogram (
    ON { table | view | (query) } AS InputTable
    [ ON { table | view | (query) } AS MinMax DIMENSION ]
    USING
    MethodType ({ 'Sturges' | 'Scott' | 'Variable-Width' | 'Equal-Width' })
    TargetColumn ({'target_column' | 'target_column_range'[,...] })
    [ NBins ({'nbin' | nbin_i,... }) ]
    [ Inclusion ({ 'inclusion_val' | 'inclusion_val_i',... }) ]
    [ GroupbyColumns ({ 'group_column_i',... }) ]
)
```

### Required Syntax Elements for TD_Histogram

**ON clause for InputTable**
- Accept the InputTable clause

**MethodType**
- Specify the method for calculating the frequency distribution:

  | Method | Description |
  |--------|-------------|
  | **Sturges** | Best for normally distributed data with n ≥ 30. Bin width: w = r/(1 + log₂n) where r = range, n = elements |
  | **Scott** | Best for normally distributed data. Bin width: w = 3.49s/(n^1/3) where s = std dev, n = elements |
  | **Variable-Width** | Requires MinMax table specifying min/max values for each bin. Max 10000 bins per column |
  | **Equal-Width** | Divides data into k equal-width intervals. Bin width: w = (max - min)/k. Optional MinMax table |

**TargetColumn**
- Specify the InputTable columns for which the histogram is to be calculated

**NBins**
- [Required with Equal-Width and Variable-Width methods]
- Specify the integer value for the number of ranges or bins
- If only one value specified, applies to all target columns
- Maximum value: 10000

### Optional Syntax Elements for TD_Histogram

**ON clause for Dimension**
- Accept the MinMax table clause
- For **Variable-Width**:
  - One column: min (column1), max (column2), label (column3)
  - Multiple columns: ColumnName (column1), min (column2), max (column3), label (column4)
- For **Equal-Width**:
  - One column: min (column1), max (column2)
  - Multiple columns: ColumnName (column1), min (column2), max (column3)

**Inclusion**
- Specify whether to include points on bin boundaries in left or right bin
- If only one value specified, applies to all target columns
- Default: 'left'

**GroupByColumns**
- Specify names of InputTable columns containing group values for binning
- Must not include columns already in TargetColumn
- Does not support range notation
- Maximum unique columns: 2042

### Input Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | Numeric | Column for which histogram is calculated |
| group_column | Any | Optional grouping column for binning |

### Advantages of Histograms
- **Clear Visual Representation**: Easy to understand data distribution at a glance
- **No Advanced Statistics Required**: Accessible to wide range of audiences
- **Easy Comparisons**: Multiple histograms can be plotted for comparison
- **Central Tendency & Variability**: Shape indicates skewness, spread shows variability
- **Outlier Identification**: Easily identifies unusual data points

### Code Examples

**Example 1: Sturges Method Histogram**
```sql
-- Best for normally distributed data with sample size >= 30
SELECT * FROM TD_Histogram (
    ON sales_data AS InputTable
    USING
    MethodType ('Sturges')
    TargetColumn ('transaction_amount')
) AS dt
ORDER BY bin_start;
```

**Example 2: Scott Method Histogram**
```sql
-- Best for normally distributed data
SELECT * FROM TD_Histogram (
    ON temperature_readings AS InputTable
    USING
    MethodType ('Scott')
    TargetColumn ('temperature')
) AS dt;
```

**Example 3: Equal-Width Histogram**
```sql
-- Divide data into 10 equal-width bins
SELECT * FROM TD_Histogram (
    ON customer_ages AS InputTable
    USING
    MethodType ('Equal-Width')
    TargetColumn ('age')
    NBins ('10')
    Inclusion ('left')
) AS dt
ORDER BY bin_number;
```

**Example 4: Equal-Width with MinMax Table**
```sql
-- Specify custom min/max values for binning
SELECT * FROM TD_Histogram (
    ON product_prices AS InputTable
    ON price_ranges AS MinMax DIMENSION
    USING
    MethodType ('Equal-Width')
    TargetColumn ('price')
    NBins ('5')
) AS dt;
```

**Example 5: Variable-Width Histogram**
```sql
-- Custom bin widths for non-uniform distributions
SELECT * FROM TD_Histogram (
    ON income_data AS InputTable
    ON income_bins AS MinMax DIMENSION
    USING
    MethodType ('Variable-Width')
    TargetColumn ('annual_income')
    NBins ('6')
) AS dt;
```

**Example 6: Histogram with Grouping**
```sql
-- Create separate histograms for each category
SELECT * FROM TD_Histogram (
    ON sales_transactions AS InputTable
    USING
    MethodType ('Equal-Width')
    TargetColumn ('sale_amount')
    NBins ('8')
    GroupbyColumns ('region', 'product_category')
) AS dt
ORDER BY region, product_category, bin_number;
```

**Example 7: Multiple Columns Histogram**
```sql
-- Analyze distribution of multiple numeric columns
SELECT * FROM TD_Histogram (
    ON health_metrics AS InputTable
    USING
    MethodType ('Sturges')
    TargetColumn ('blood_pressure', 'heart_rate', 'glucose_level')
) AS dt
ORDER BY column_name, bin_number;
```

**Example 8: Different Bin Counts per Column**
```sql
-- Use different number of bins for different columns
SELECT * FROM TD_Histogram (
    ON financial_data AS InputTable
    USING
    MethodType ('Equal-Width')
    TargetColumn ('revenue', 'expenses', 'profit')
    NBins ('10', '8', '12')
    Inclusion ('left')
) AS dt;
```

**Example 9: Age Distribution Analysis**
```sql
-- Analyze customer age distribution with custom ranges
SELECT * FROM TD_Histogram (
    ON customer_demographics AS InputTable
    USING
    MethodType ('Equal-Width')
    TargetColumn ('customer_age')
    NBins ('7')  -- Creates bins: 0-10, 11-20, 21-30, etc.
) AS dt;
```

**Example 10: Performance Metrics Histogram**
```sql
-- Analyze response time distributions
SELECT
    bin_label,
    frequency,
    (frequency * 100.0 / SUM(frequency) OVER()) as percentage
FROM TD_Histogram (
    ON api_response_times AS InputTable
    USING
    MethodType ('Scott')
    TargetColumn ('response_time_ms')
) AS dt
ORDER BY bin_number;
```

### Important Notes
- Maximum number of bins: 10000 per column
- Sturges method: Best when n ≥ 30 and data is normally distributed
- Scott method: Assumes normal distribution
- Variable-Width: Allows custom bin boundaries for skewed distributions
- Equal-Width: Simplest method, divides range into equal intervals
- Use GroupbyColumns for category-wise histograms
- Inclusion parameter controls bin boundary behavior
- Choose method based on data distribution and analysis needs

### Related Functions
- TD_UnivariateStatistics - For detailed statistical measures
- TD_CategoricalSummary - For categorical data distributions
- TD_ColumnSummary - For column-level summaries
- TD_QQNorm - For normality testing

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Data Exploration Functions
