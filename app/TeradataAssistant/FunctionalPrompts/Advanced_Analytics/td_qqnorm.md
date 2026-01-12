# TD_QQNorm

### Function Name
**TD_QQNorm**

### Description
The TD_QQNorm function is a Q-Q (quantile-quantile) norm method that compares the distribution of a data set to a normal distribution. TD_QQNorm checks whether the values in input table columns are normally distributed. The function returns the quantiles of the column values and corresponding theoretical quantile values from a normal distribution. If the column values are normally distributed, then the quantiles of column values and normal quantile values appear in a straight line with a slope of 1 when plotted on a graph.

### When the Function Would Be Used
- **Normality Testing**: Checking assumptions of statistical models that rely on normality (e.g., linear regression)
- **Bioinformatics**: Preprocessing gene expression data with quartile normalization
- **Data Quality Assessment**: Identifying deviations from normal distribution (skewness, heavy-tailedness)
- **Model Validation**: Ensuring data meets assumptions for parametric statistical tests
- **Distribution Comparison**: Comparing observed data distribution to theoretical normal distribution
- **Outlier Detection**: Identifying points that deviate significantly from normal distribution
- **Preprocessing**: Data normalization before applying ML algorithms that assume normality

### How QQ Norm Works

The QQ norm process:
1. Data is sorted in ascending order
2. Corresponding quantiles are calculated
3. Expected quantiles are calculated based on theoretical distribution
4. For normal distribution, expected quantiles use mean and standard deviation
5. When plotted, quantiles of dataset vs expected quantiles show normality
6. Straight line indicates normal distribution; deviations indicate non-normality

### Quantile Normalization Process

To formulate QQ norm data using quantile normalization:
1. **Rank**: For each element, rank expression values from smallest to largest
2. **Average Rank**: Calculate average rank for each value across all samples
3. **Sort**: Sort average ranks in ascending order
4. **Calculate Quantiles**: Divide sorted ranks into bins and calculate quantiles
5. **Map Values**: Map original expression values to corresponding quantiles
6. **Create QQ Plot**: Tabulate observed quantiles against expected theoretical quantiles

### Syntax
```sql
TD_QQNorm (
    ON { table | view | (query) } AS InputTable
    [ PARTITION BY ANY [ ORDER BY order_column ] ]
    USING
    TargetColumns ({ 'target_column' | target_column_range }[,...])
    RankColumns ({ 'rank_column' | rank_column_range }[,...])
    [ OutputColumns ('output_column' [,...]) ]
    [ Accumulate ({ 'accumulate_column' | accumulate_column_range }[,...]) ]
)
```

### Required Syntax Elements for TD_QQNorm

**ON clause**
- Accept the InputTable clause
- Optionally accepts PARTITION BY ANY and ORDER BY clauses

**TargetColumns**
- Specify the names of the numeric InputTable columns to check for normal distribution
- Supports column ranges using bracket notation

**RankColumns**
- Specify the names of the InputTable columns that contain the ranks for the target columns
- Must correspond to the target columns

### Optional Syntax Elements for TD_QQNorm

**OutputColumns**
- Specify names for the output table columns that contain the theoretical quantiles of the target columns
- Default: target_column_theoretical_quantiles

**Accumulate**
- Specify the names of the InputTable columns to copy to the output table
- Useful for preserving identifier or grouping columns

### Input Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | BYTEINT, SMALLINT, INTEGER, BIGINT, DECIMAL/NUMERIC, FLOAT, REAL, DOUBLE PRECISION | Column to check for normal distribution |
| rank_column | BYTEINT, SMALLINT, INTEGER, or BIGINT | Ranks for target column |
| accumulate_column | Any | Column to copy to output table |

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| accumulate_column | Any | Column copied from InputTable |
| target_column | DOUBLE PRECISION | Column checked for normal distribution |
| output_column or target_column_theoretical_quantiles | DOUBLE PRECISION | Theoretical quantile values for target column |

### Code Examples

**Input Table: input_table**
```
passenger  survived  pclass  name                                         gender  age  fare
97         0         1       Goldschmidt; Mr. George B                    male    71   34.6542
488        0         1       Kent; Mr. Edward Austin                      male    58   29.7
505        1         1       Maioni; Miss. Roberta                        female  16   86.5
631        1         1       Barkworth; Mr. Algernon Henry Wilson         male    80   30
873        0         1       Carlsson; Mr. Frans Olof                     male    33   5
```

**Example 1: Creating Rank Table for QQ Norm**
```sql
-- First, create a rank table with ROW_NUMBER() for each target column
CREATE TABLE RankTable AS (
    SELECT age, fare,
        CAST (ROW_NUMBER() OVER (ORDER BY age ASC NULLS LAST) AS BIGINT) AS rank_age,
        CAST (ROW_NUMBER() OVER (ORDER BY fare ASC NULLS LAST) AS BIGINT) AS rank_fare
    FROM input_table AS dt
) WITH DATA;
```

**RankTable Output:**
```
age  fare      rank_age  rank_fare
16   86.5      1         5
33   5         2         1
58   29.7      3         2
71   34.6542   4         4
80   30        5         3
```

**Example 2: TD_QQNorm Using Column Names**
```sql
SELECT * FROM TD_QQNorm (
    ON RankTable AS InputTable
    USING
    TargetColumns ('age', 'fare')
    RankColumns ('rank_age', 'rank_fare')
) AS dt;
```

**Example 3: TD_QQNorm Using Column Numbers**
```sql
-- Using 0-based column indexing
SELECT * FROM TD_QQNorm (
    ON RankTable AS InputTable
    USING
    TargetColumns ('[0:1]')
    RankColumns ('[2:3]')
) AS dt;
```

**Example 4: TD_QQNorm with PARTITION BY ANY**
```sql
SELECT * FROM TD_QQNorm (
    ON RankTable AS InputTable
    PARTITION BY ANY
    USING
    TargetColumns ('age', 'fare')
    RankColumns ('rank_age', 'rank_fare')
) AS dt;
```

**Output:**
```
age  age_theoretical_quantiles  fare   fare_theoretical_quantiles
16   -1.17986882170049          86.5   1.17986882170049
33   -0.496788749686441         5      -1.17986882170049
58   -0.000000101006675468085   29.7   -0.496788749686441
71   0.496788749686441          34.6542 0.496788749686441
80   1.17986882170049           30     -0.000000101006675468085
```

**Example 5: QQ Norm with Custom Output Columns**
```sql
SELECT * FROM TD_QQNorm (
    ON RankTable AS InputTable
    USING
    TargetColumns ('age', 'fare')
    RankColumns ('rank_age', 'rank_fare')
    OutputColumns ('age_norm_quantile', 'fare_norm_quantile')
) AS dt;
```

**Example 6: QQ Norm with Accumulate Columns**
```sql
-- Include additional columns in output for context
SELECT * FROM TD_QQNorm (
    ON RankTable_with_ids AS InputTable
    USING
    TargetColumns ('measurement1', 'measurement2')
    RankColumns ('rank_m1', 'rank_m2')
    Accumulate ('sample_id', 'patient_id', 'date')
) AS dt
ORDER BY sample_id;
```

**Example 7: Multi-Column Normality Check**
```sql
-- Check multiple variables for normality simultaneously
CREATE TABLE health_metrics_ranked AS (
    SELECT
        blood_pressure, heart_rate, glucose,
        CAST(ROW_NUMBER() OVER (ORDER BY blood_pressure ASC) AS BIGINT) AS rank_bp,
        CAST(ROW_NUMBER() OVER (ORDER BY heart_rate ASC) AS BIGINT) AS rank_hr,
        CAST(ROW_NUMBER() OVER (ORDER BY glucose ASC) AS BIGINT) AS rank_gluc
    FROM health_data
) WITH DATA;

SELECT * FROM TD_QQNorm (
    ON health_metrics_ranked AS InputTable
    USING
    TargetColumns ('blood_pressure', 'heart_rate', 'glucose')
    RankColumns ('rank_bp', 'rank_hr', 'rank_gluc')
) AS dt;
```

### Interpreting QQ Plot Results

When plotting the output:
- **Straight Line (slope = 1)**: Data is normally distributed
- **S-Shaped Curve**: Data has heavier or lighter tails than normal distribution
- **Points Above Line at Ends**: Distribution has heavier tails (more outliers)
- **Points Below Line at Ends**: Distribution has lighter tails
- **Curved Pattern**: Data may be skewed (left or right)

### Important Notes
- Input table must contain pre-calculated ranks for target columns
- Use ROW_NUMBER() OVER (ORDER BY column ASC NULLS LAST) to create ranks
- Ranks must be BIGINT data type
- Function commonly used to validate assumptions for linear regression and other parametric tests
- QQ plots are visual tools; statistical tests (e.g., Shapiro-Wilk) provide quantitative normality assessment
- Useful for identifying data transformation needs before modeling

### Related Functions
- TD_UnivariateStatistics - For descriptive statistics including skewness and kurtosis
- TD_Histogram - For visualizing data distributions
- TD_ColumnSummary - For basic data quality checks

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Data Exploration Functions
