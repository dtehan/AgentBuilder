# TD_UnivariateStatistics

### Function Name
**TD_UnivariateStatistics**

### Description
TD_UnivariateStatistics displays descriptive statistics for each specified numeric input table column. This comprehensive function calculates a wide range of statistical measures including central tendency, dispersion, shape, and position statistics.

**Important Note**: There may be different statistics values on different runs due to precision differences for decimal and number columns.

### When the Function Would Be Used
- **Exploratory Data Analysis (EDA)**: Initial investigation of dataset characteristics
- **Data Profiling**: Understanding distribution, central tendency, and spread of numeric variables
- **Quality Assessment**: Identifying data quality issues through range, NULL counts, and outliers
- **Feature Selection**: Understanding variable characteristics before model development
- **Statistical Reporting**: Generating comprehensive statistical summaries for reports
- **Outlier Detection**: Using TOP5/BOTTOM5 to identify extreme values
- **Distribution Analysis**: Assessing skewness, kurtosis, and normality
- **Data Validation**: Verifying data meets expected ranges and distributions

### Syntax
```sql
TD_UnivariateStatistics (
    ON { table | view | (query) }
    AS InputTable [ PARTITION BY ANY ]
    USING
    TargetColumns ({ 'target_column' | target_column_range }[,...])
    [ PartitionColumns ('partition_column' [,...]) ]
    [ Stats ('statistic' [,...]) ]
    [ Centiles ('percentile' [,...]) ]
    [ TrimPercentile ('trimmed_percentile') ]
)
```

### Required Syntax Elements for TD_UnivariateStatistics

**ON clause**
- Accept the InputTable clause
- Optionally accepts PARTITION BY ANY

**TargetColumns**
- Specify the names of the numeric InputTable columns for which to compute statistics
- Supports column ranges using bracket notation

### Optional Syntax Elements for TD_UnivariateStatistics

**PartitionColumns**
- Specify the names of the InputTable columns on which to partition the input
- The function copies these columns to the output table
- Default: The function treats all rows as a single partition

**Stats**
- Specify the statistics to calculate
- **Default**: 'ALL' (calculates all available statistics)

Available statistics:

| Statistic | Aliases | Description |
|-----------|---------|-------------|
| SUM | - | Sum of all values |
| COUNT | CNT | Count of non-NULL values |
| MAXIMUM | MAX | Maximum value |
| MINIMUM | MIN | Minimum value |
| MEAN | - | Arithmetic mean (average) |
| UNCORRECTED SUM OF SQUARES | USS | Sum of squared values |
| NULL COUNT | NLC | Count of NULL values |
| POSITIVE VALUES COUNT | PVC | Count of positive values |
| NEGATIVE VALUES COUNT | NVC | Count of negative values |
| ZERO VALUES COUNT | ZVC | Count of zero values |
| TOP5 | TOP | Five largest values |
| BOTTOM5 | BTM | Five smallest values |
| RANGE | RNG | Difference between MAX and MIN |
| GEOMETRIC MEAN | GM | N-th root of product of N numbers |
| HARMONIC MEAN | HM | Reciprocal of arithmetic mean of reciprocals |
| VARIANCE | VAR | Measure of dispersion from mean |
| STANDARD DEVIATION | STD | Square root of variance |
| STANDARD ERROR | SE | Standard deviation of sampling distribution |
| SKEWNESS | SKW | Measure of asymmetry of distribution |
| KURTOSIS | KUR | Measure of tailedness of distribution |
| COEFFICIENT OF VARIATION | CV | Ratio of standard deviation to mean |
| CORRECTED SUM OF SQUARES | CSS | Sum of squared deviations from mean |
| MODE | - | Most frequently occurring value |
| MEDIAN | MED | Middle value (50th percentile) |
| UNIQUE ENTITY COUNT | UEC | Count of distinct values |
| INTERQUARTILE RANGE | IQR | Difference between 75th and 25th percentiles |
| TRIMMED MEAN | TM | Mean after removing extreme values |
| PERCENTILES | PRC | Specified percentile values |
| ALL | - | Calculate all available statistics |

**Centiles**
- Specify the centile (percentile) to calculate
- percentile is an INTEGER in the range [1, 100]
- Function ignores Centiles unless Stats specifies PERCENTILES, PRC, or ALL
- Default: 1, 5, 10, 25, 50, 75, 90, 95, 99

**TrimPercentile**
- Specify the trimmed lower percentile, an integer in the range [1, 50]
- Function calculates mean of values between trimmed lower percentile and trimmed upper percentile (1-trimmed_percentile)
- Function ignores TrimPercentile unless Stats specifies TRIMMED MEAN, TM, or ALL
- Default: 20

### Input Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | NUMERIC | Column to calculate statistics |
| partition_column | Any | Partition for statistics calculation |

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| partition_column | Any | Column copied from input table. Defines partition for statistics calculation |
| Attribute | VARCHAR | Target column for function calculated statistics |
| StatsName | VARCHAR | Statistic name (one column per specified statistic) |
| StatsValue | DOUBLE PRECISION | Statistic value (one column per specified statistic) |

### Code Examples

**Input Table: titanic_train**
```
passenger  survived  name                                         gender  age  fare
97         0         Goldschmidt; Mr. George B                    male    71   34.6542
488        0         Kent; Mr. Edward Austin                      male    58   29.7
505        1         Maioni; Miss. Roberta                        female  16   86.5
631        1         Barkworth; Mr. Algernon Henry Wilson         male    80   30
873        0         Carlsson; Mr. Frans Olof                     male    33   5
```

**Example 1: Calculate Mean, Median, and Mode**
```sql
SELECT * FROM TD_UnivariateStatistics (
    ON titanic_train AS InputTable
    USING
    TargetColumns ('age','fare')
    Stats ('MEAN', 'MEDIAN', 'MODE')
) AS dt;
```

**Output:**
```
ATTRIBUTE  StatName  StatValue
age        MEAN      5.16000000000000E 001
age        MEDIAN    5.80000000000000E 001
age        MODE      1.60000000000000E 001
fare       MEAN      3.71708400000000E 001
fare       MEDIAN    3.00000000000000E 001
fare       MODE      5.00000000000000E 000
```

**Example 2: Calculate All Statistics**
```sql
SELECT * FROM TD_UnivariateStatistics (
    ON customer_transactions AS InputTable
    USING
    TargetColumns ('transaction_amount')
    Stats ('ALL')
) AS dt;
```

**Example 3: Calculate Specific Percentiles**
```sql
SELECT * FROM TD_UnivariateStatistics (
    ON sales_data AS InputTable
    USING
    TargetColumns ('revenue', 'profit')
    Stats ('PERCENTILES')
    Centiles ('10', '25', '50', '75', '90', '95', '99')
) AS dt
ORDER BY Attribute, StatsName;
```

**Example 4: Basic Descriptive Statistics**
```sql
SELECT * FROM TD_UnivariateStatistics (
    ON product_metrics AS InputTable
    USING
    TargetColumns ('price', 'quantity', 'rating')
    Stats ('COUNT', 'MIN', 'MAX', 'MEAN', 'STD', 'VARIANCE')
) AS dt;
```

**Example 5: Distribution Shape Analysis**
```sql
-- Check for normality and distribution characteristics
SELECT * FROM TD_UnivariateStatistics (
    ON experiment_results AS InputTable
    USING
    TargetColumns ('measurement')
    Stats ('MEAN', 'MEDIAN', 'STD', 'SKEWNESS', 'KURTOSIS', 'IQR')
) AS dt;
```

**Example 6: Outlier Detection**
```sql
-- Identify extreme values
SELECT * FROM TD_UnivariateStatistics (
    ON sensor_readings AS InputTable
    USING
    TargetColumns ('temperature', 'pressure', 'humidity')
    Stats ('MIN', 'MAX', 'TOP5', 'BOTTOM5', 'RANGE')
) AS dt;
```

**Example 7: Data Quality Check**
```sql
-- Check for missing values and data distribution
SELECT * FROM TD_UnivariateStatistics (
    ON raw_data AS InputTable
    USING
    TargetColumns ('[:]')  -- All numeric columns
    Stats ('COUNT', 'NULL COUNT', 'POSITIVE VALUES COUNT',
           'NEGATIVE VALUES COUNT', 'ZERO VALUES COUNT', 'UEC')
) AS dt;
```

**Example 8: Statistics by Partition**
```sql
-- Calculate statistics separately for each category
SELECT * FROM TD_UnivariateStatistics (
    ON regional_sales AS InputTable
    USING
    TargetColumns ('sales_amount')
    PartitionColumns ('region', 'product_category')
    Stats ('MEAN', 'MEDIAN', 'STD', 'COUNT')
) AS dt
ORDER BY region, product_category;
```

**Example 9: Trimmed Mean Calculation**
```sql
-- Calculate mean after removing extreme 10% values
SELECT * FROM TD_UnivariateStatistics (
    ON noisy_measurements AS InputTable
    USING
    TargetColumns ('signal_strength')
    Stats ('MEAN', 'TRIMMED MEAN')
    TrimPercentile ('10')
) AS dt;
```

**Example 10: Comprehensive Statistical Profile**
```sql
-- Complete statistical summary for ML feature engineering
SELECT * FROM TD_UnivariateStatistics (
    ON ml_features AS InputTable
    USING
    TargetColumns ('feature1', 'feature2', 'feature3')
    Stats ('COUNT', 'NULL COUNT', 'MEAN', 'MEDIAN', 'MODE',
           'STD', 'VARIANCE', 'MIN', 'MAX', 'RANGE',
           'SKEWNESS', 'KURTOSIS', 'IQR', 'CV')
) AS dt
ORDER BY Attribute, StatsName;
```

### Statistical Measures Explanation

**Central Tendency**:
- **Mean**: Average value, sensitive to outliers
- **Median**: Middle value, robust to outliers
- **Mode**: Most frequent value
- **Geometric Mean**: Useful for growth rates and ratios
- **Harmonic Mean**: Useful for rates and averages of ratios
- **Trimmed Mean**: Mean after removing extreme values

**Dispersion**:
- **Variance**: Average squared deviation from mean
- **Standard Deviation**: Square root of variance, in original units
- **Range**: Difference between max and min
- **IQR (Interquartile Range)**: Range of middle 50% of data
- **Coefficient of Variation**: Standardized measure of dispersion

**Shape**:
- **Skewness**: Measure of asymmetry (negative = left-skewed, positive = right-skewed)
- **Kurtosis**: Measure of tailedness (high = heavy tails/outliers)

**Position**:
- **Percentiles**: Values below which given percentage of data falls
- **Quartiles**: 25th, 50th (median), 75th percentiles

### Important Notes
- Statistics values may vary slightly across runs for DECIMAL/NUMBER columns due to precision
- NULL values are excluded from most calculations but counted separately
- Choose appropriate statistics based on data distribution and analysis goals
- Skewness and kurtosis help assess whether data follows normal distribution
- Use partitioning for group-wise statistics
- Coefficient of variation is useful for comparing variability across different scales

### Related Functions
- TD_ColumnSummary - For column-level data quality summaries
- TD_Histogram - For frequency distribution visualization
- TD_QQNorm - For testing normality
- TD_CategoricalSummary - For categorical variable summaries

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Data Exploration Functions
