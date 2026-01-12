# TD_Pivoting

### Function Name
**TD_Pivoting**

### Description
TD_Pivoting transforms data from sparse (long) format to dense (wide) format by pivoting rows into columns. This function reorganizes data by taking unique values from a pivot column and converting them into separate columns in the output table. The transformation is essential for converting attribute-value pair formats into traditional tabular formats suitable for machine learning and analytical processing.

Unlike TD_Pivot which is designed for general SQL queries, TD_Pivoting is specifically optimized for use with in-database analytic functions and machine learning workflows. It supports multiple pivoting modes including row-based pivoting, key-based pivoting, and aggregation-based pivoting, making it highly flexible for various data transformation scenarios.

### When the Function Would Be Used
- **Sparse to Dense Conversion**: Transform attribute-value pairs to traditional table format
- **Feature Matrix Creation**: Convert sparse features to dense format for ML models
- **Data Reshaping**: Restructure data from long to wide format
- **Time Series Pivoting**: Convert time-based measurements into column-based format
- **Category Expansion**: Spread categorical values across multiple columns
- **Aggregation with Pivoting**: Combine aggregation and pivoting in single operation
- **ML Pipeline Preparation**: Prepare sparse data for algorithms requiring dense input
- **Report Generation**: Transform transactional data into summary reports
- **Cross-tabulation**: Create pivot tables for analytical insights
- **Feature Engineering**: Generate wide-format features from sparse representations

### Sparse vs Dense Format

**Sparse Format (Long):**
```
Passenger  AttributeName  AttributeValue
1          pclass         3
1          gender         male
2          pclass         1
2          gender         female
```

**Dense Format (Wide):**
```
Passenger  pclass  gender
1          3       male
2          1       female
```

**Benefits of Dense Format:**
- Traditional table structure
- Easier to query specific attributes
- Compatible with most ML algorithms
- Better for visualization
- Efficient for analysis

### Syntax

```sql
TD_Pivoting (
    ON { table | view | (query) } AS InputTable PARTITION BY partition_column [,...]
    [ ORDER BY order_column [,...] ]
    USING
    PartitionColumns({'partition_column' | partition_column_range} [,...])
    TargetColumns({'target_column' | target_column_range} [,...])
    [ Accumulate({'accumulate_column' | accumulate_column_range} [,...]) ]
    {
        [ RowsPerPartition (rows_per_partition) ]
        |
        [ PivotColumn('pivot_column') ]
        [ PivotKeys('pivot_key' [,...]) ]
        [ PivotKeysAlias('pivot_key_alias' [,...]) ]
        [ DefaultPivotValues ('default_pivot_value' [,...]) ]
        |
        [ Aggregation({'{CONCAT|UNIQUE_CONCAT|SUM|MIN|MAX|AVG}' |
          'ColumnName:{CONCAT|UNIQUE_CONCAT|SUM|MIN|MAX|AVG}' [,...]}) ]
    }
    [ Delimiters('single_char' | 'ColumnName:single_char' [,...]) ]
    [ CombinedColumnSizes(size_value | 'ColumnName:size_value' [,...]) ]
    [ TruncateColumns({'truncate_column' | truncate_column_range} [,...]) ]
    [ OutputColumnNames('output_column_name' [,...]) ]
)
```

### Required Syntax Elements for TD_Pivoting

**ON clause**
- Accept the InputTable clause
- Must include PARTITION BY clause with partition columns

**PartitionColumns**
- Specify columns from InputTable used in PARTITION BY clause
- Must match the columns in PARTITION BY clause exactly
- Defines grouping for pivot operation

**TargetColumns**
- Specify columns from InputTable to be pivoted
- Maximum 2018 unique columns
- These columns' values will become new columns in output

### Optional Syntax Elements for TD_Pivoting

**Accumulate**
- Specify columns to copy to output table
- Values from last row of partition are copied
- Useful for preserving metadata and identifiers

**RowsPerPartition**
- Specify maximum number of rows per partition to pivot
- Range: 1 to 2047 (without aggregation), INT_MAX (with aggregation)
- Function adds NULL for partitions with fewer rows
- Function omits extra rows for partitions with more rows
- Requires ORDER BY clause to ensure consistent results
- Cannot be used with PivotColumn
- Required if both PivotColumn and Aggregation are omitted

**PivotColumn**
- Specify input column containing pivot keys
- Values in this column become output column names
- Cannot be used with RowsPerPartition
- Required if both RowsPerPartition and Aggregation are omitted

**PivotKeys**
- Specify pivot_column values to use as pivot keys
- Function ignores rows with other pivot_column values
- Required if PivotColumn is specified

**PivotKeysAlias**
- Specify aliases for pivot keys
- One alias for each pivot key
- nth alias applies to nth pivot key
- Optional with PivotKeys

**DefaultPivotValues**
- Specify default value for each pivot key
- One default value per pivot key
- Data type must be compatible with target column
- Optional with PivotKeys

**Aggregation**
- Specify aggregation method for target columns
- Options: CONCAT, UNIQUE_CONCAT, SUM, MIN, MAX, AVG
- Can specify single value for all columns or per-column values
- Format: 'ColumnName:{AGGREGATION}' for per-column specification
- Required if both RowsPerPartition and PivotColumn are omitted
- Default: No aggregation, one value is picked

**Delimiters**
- Specify delimiter for concatenation (CONCAT, UNIQUE_CONCAT)
- Single character string
- Can specify single delimiter for all or per-column delimiters
- Format: 'ColumnName:single_char'
- Default: comma (,)

**CombinedColumnSizes**
- Specify maximum size for concatenated strings
- Default: 64000
- Maximum: 2097088000
- If size ≤ 64000: VARCHAR output
- If size > 64000: CLOB output
- Format: 'ColumnName:size_value' for per-column specification

**TruncateColumns**
- Specify columns to truncate if concatenation exceeds size
- Columns must be part of target columns
- Optional with CONCAT and UNIQUE_CONCAT

**OutputColumnNames**
- Specify custom names for output columns
- nth name applies to nth output column

### Input Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| partition_column | Any allowed by PARTITION BY | Column to partition input data. One per specified partition_column |
| target_column | CHAR, VARCHAR, BYTE, VARBYTE, BYTEINT, SMALLINT, INTEGER, BIGINT, FLOAT, REAL, DOUBLE PRECISION, DECIMAL, NUMBER, DATE, TIME, TIMESTAMP, TIME WITH TIME ZONE, TIMESTAMP WITH TIME ZONE, INTERVAL types | Column to be pivoted |
| accumulate_column | ANY | Column to copy to output table |

### Output Table Schema

**OutputTable Schema - RowsPerPartition Only:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| partition_column | Same as InputTable | Columns copied to output table |
| <target_column_name>_<i> or User-specified name | Same as target_column | Pivoted value (i in range [0, rows_per_partition-1]). Columns in TargetColumns order |
| accumulate_column | Same as InputTable | Columns copied to output table |

**OutputTable Schema - PivotColumn Only or PivotColumn with Aggregation:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| partition_column | Same as InputTable | Columns copied to output table |
| <target_column_name>_<pivot_key> or <target_column_name>_<pivot_key_alias> or User-specified name | Same as target_column | Pivoted or aggregated value. Columns in TargetColumns and pivot keys order |
| accumulate_column | Same as InputTable | Columns copied to output table |

**OutputTable Schema - Aggregation Only or RowsPerPartition with Aggregation:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| partition_column | Same as InputTable | Columns copied to output table |
| <target_column_name>_combined or User-specified name | VARCHAR or CLOB | Aggregated value. Columns in TargetColumns order |
| accumulate_column | Same as InputTable | Columns copied to output table |

### Code Examples

**Input Data: titanic_dataset_unpivoted**
```
passenger  AttributeName  AttributeValue  survived
2          pclass         1               1
2          gender         female          1
4          pclass         1               1
4          gender         female          1
7          pclass         1               0
7          gender         male            0
10         pclass         2               1
10         gender         female          1
```

**Example 1: RowsPerPartition - Basic Sparse to Dense**
```sql
SELECT * FROM TD_Pivoting (
    ON titanic_dataset_unpivoted AS InputTable
    PARTITION BY passenger
    ORDER BY AttributeName
    USING
    PartitionColumns('passenger')
    TargetColumns('AttributeValue')
    Accumulate('survived')
    RowsPerPartition(2)
) AS dt
ORDER BY passenger;
```

**Output:**
```
passenger  AttributeValue_0  AttributeValue_1  survived
2          1                 female            1
4          1                 female            1
7          1                 male              0
10         2                 female            1
```

**Example 2: PivotColumn - Named Attribute Columns**
```sql
SELECT * FROM TD_Pivoting (
    ON titanic_dataset_unpivoted AS InputTable
    PARTITION BY passenger
    USING
    PartitionColumns('passenger')
    TargetColumns('AttributeValue')
    Accumulate('survived')
    PivotColumn('AttributeName')
    PivotKeys('pclass', 'gender')
) AS dt
ORDER BY passenger;
```

**Output:**
```
passenger  AttributeValue_pclass  AttributeValue_gender  survived
2          1                      female                 1
4          1                      female                 1
7          1                      male                   0
10         2                      female                 1
```

**Example 3: Aggregation with PivotColumn - Sales Summary**
```sql
CREATE TABLE star1(
    country VARCHAR(20),
    state VARCHAR(10),
    yr INTEGER,
    qtr VARCHAR(3),
    sales INTEGER,
    cogs INTEGER,
    rating VARCHAR(10)
);

INSERT INTO star1 VALUES('USA', 'CA', 2001, 'Q1', 30, 15, 'A');
INSERT INTO star1 VALUES('Canada', 'ON', 2001, 'Q2', 10, 0, 'B');
INSERT INTO star1 VALUES('Canada', 'BC', 2001, 'Q3', 15, 0, 'A');
INSERT INTO star1 VALUES('USA', 'CA', 2001, 'Q2', 50, 20, 'A');
INSERT INTO star1 VALUES('USA', 'CA', 2001, 'Q2', 5, 5, 'B');

SELECT * FROM TD_Pivoting (
    ON star1 AS InputTable
    PARTITION BY country, state
    ORDER BY qtr
    USING
    PartitionColumns('country', 'state')
    TargetColumns('sales', 'cogs', 'rating')
    Accumulate('yr')
    PivotColumn('qtr')
    PivotKeys('Q1', 'Q2', 'Q3')
    Aggregation('sales:SUM', 'cogs:AVG', 'rating:CONCAT')
    Delimiters('|')
) AS dt
ORDER BY country;
```

**Output:**
```
country  state  sales_Q1  sales_Q2  sales_Q3  cogs_Q1  cogs_Q2   cogs_Q3  rating_Q1  rating_Q2  rating_Q3  yr
Canada   BC     NULL      NULL      15        NULL     NULL      0.0      NULL       NULL       A          2001
Canada   ON     NULL      10        NULL      NULL     0.0       NULL     NULL       B          NULL       2001
USA      CA     30        55        NULL      15.0     12.5      NULL     A          A|B        NULL       2001
```

**Example 4: Aggregation Only - Complete Rollup**
```sql
SELECT * FROM TD_Pivoting (
    ON star1 AS InputTable
    PARTITION BY country
    ORDER BY state
    USING
    PartitionColumns('country')
    TargetColumns('sales', 'cogs', 'state', 'rating')
    Accumulate('yr')
    Aggregation('sales:SUM', 'cogs:AVG', 'state:UNIQUE_CONCAT', 'rating:CONCAT')
    Delimiters('|')
) AS dt
ORDER BY country;
```

**Output:**
```
country  sales_combined  cogs_combined  state_combined  rating_combined  yr
Canada   25              0.0            BC|ON           A|A|B            2001
USA      85              13.33          CA              A|A|B            2001
```

**Example 5: Custom Output Column Names**
```sql
SELECT * FROM TD_Pivoting (
    ON titanic_dataset_unpivoted AS InputTable
    PARTITION BY passenger
    ORDER BY AttributeName
    USING
    PartitionColumns('passenger')
    TargetColumns('AttributeValue')
    Accumulate('survived')
    RowsPerPartition(2)
    OutputColumnNames('FirstAttribute', 'SecondAttribute')
) AS dt
ORDER BY passenger;
```

**Example 6: Default Pivot Values**
```sql
SELECT * FROM TD_Pivoting (
    ON customer_attributes AS InputTable
    PARTITION BY customer_id
    USING
    PartitionColumns('customer_id')
    TargetColumns('attribute_value')
    PivotColumn('attribute_name')
    PivotKeys('age', 'income', 'score')
    DefaultPivotValues('0', '0', '-1')
) AS dt;
```

**Example 7: Pivot Keys with Aliases**
```sql
SELECT * FROM TD_Pivoting (
    ON survey_data AS InputTable
    PARTITION BY respondent_id
    USING
    PartitionColumns('respondent_id')
    TargetColumns('response_value')
    PivotColumn('question_id')
    PivotKeys('Q1', 'Q2', 'Q3')
    PivotKeysAlias('Question1', 'Question2', 'Question3')
) AS dt
ORDER BY respondent_id;
```

**Example 8: Large String Concatenation with CLOB**
```sql
SELECT * FROM TD_Pivoting (
    ON text_data AS InputTable
    PARTITION BY document_id
    ORDER BY sentence_id
    USING
    PartitionColumns('document_id')
    TargetColumns('sentence_text')
    Aggregation('CONCAT')
    Delimiters(' ')
    CombinedColumnSizes(100000)  -- CLOB output for large text
) AS dt;
```

**Example 9: Multiple Target Columns with Different Aggregations**
```sql
SELECT * FROM TD_Pivoting (
    ON product_metrics AS InputTable
    PARTITION BY product_id
    ORDER BY metric_date
    USING
    PartitionColumns('product_id')
    TargetColumns('revenue', 'units_sold', 'customer_count')
    Aggregation('revenue:SUM', 'units_sold:SUM', 'customer_count:MAX')
) AS dt;
```

**Example 10: Time Series Pivoting**
```sql
SELECT * FROM TD_Pivoting (
    ON daily_metrics AS InputTable
    PARTITION BY store_id
    USING
    PartitionColumns('store_id')
    TargetColumns('daily_sales')
    PivotColumn('day_of_week')
    PivotKeys('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
    PivotKeysAlias('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
    Aggregation('AVG')
) AS dt
ORDER BY store_id;
```

### Pivoting Modes

**1. RowsPerPartition Mode:**
- Pivots fixed number of rows per partition
- No pivot column needed
- Requires ORDER BY for consistency
- Output columns: target_column_0, target_column_1, etc.
- Use when: Data has no natural pivot column but fixed structure

**2. PivotColumn Mode:**
- Pivots based on unique values in pivot column
- Creates named columns from pivot keys
- Output columns: target_column_pivotkey
- Use when: Data has attribute-name column with known values

**3. Aggregation Mode:**
- Aggregates all values in partition
- Creates single combined column per target
- Output columns: target_column_combined
- Use when: Need to roll up all values with aggregation

**4. Combined Modes:**
- PivotColumn + Aggregation: Aggregate within each pivot key
- RowsPerPartition + Aggregation: Aggregate first N rows

### Use Cases and Applications

**1. Machine Learning Feature Engineering**
- Convert sparse features to dense matrix format
- Prepare attribute-value data for ML algorithms
- Transform categorical expansions into feature columns
- Create wide-format datasets for model training

**2. Data Warehousing**
- Transform transactional data to dimensional format
- Create summary tables from detailed records
- Reshape ETL outputs for reporting
- Generate star schema dimensions from normalized data

**3. Time Series Analysis**
- Pivot daily/hourly data into column-based time series
- Create period-over-period comparison tables
- Transform temporal attributes into time-indexed columns
- Generate lag features for forecasting models

**4. Survey and Questionnaire Analysis**
- Convert question-answer pairs to response matrix
- Pivot survey responses into analysis-ready format
- Create cross-tabulation from long-format survey data
- Transform Likert scale responses to columnar format

**5. Financial Reporting**
- Pivot quarterly/monthly data into columnar reports
- Create financial statement formats from transactions
- Transform budget vs actual comparisons
- Generate period-based financial analysis tables

**6. Healthcare Analytics**
- Pivot patient measurements into observation matrix
- Transform diagnosis codes to indicator columns
- Create patient timelines from event data
- Generate feature matrices for clinical models

**7. E-commerce Analytics**
- Pivot product attributes into comparison tables
- Transform customer interactions into behavior features
- Create product-customer matrices for recommendations
- Generate sales summaries by time period

**8. IoT and Sensor Data**
- Pivot sensor readings into time-series columns
- Transform device measurements to analysis format
- Create multi-sensor observation matrices
- Generate aggregated metrics from stream data

**9. Text Analytics**
- Pivot document attributes into feature columns
- Transform term frequencies into document-term matrix
- Create categorical text features for NLP models
- Generate aggregated text statistics

**10. Cross-Tabulation and Reporting**
- Create pivot tables for business intelligence
- Transform OLTP data to OLAP format
- Generate summary reports from detail data
- Create multi-dimensional analysis tables

### Important Notes

**Partition Requirements:**
- PARTITION BY clause is mandatory
- PartitionColumns must match PARTITION BY columns exactly
- ORDER BY recommended for RowsPerPartition mode

**Column Limits:**
- Maximum 2018 unique columns in TargetColumns
- Maximum 2047 rows per partition (RowsPerPartition without aggregation)
- Maximum INT_MAX rows per partition (with aggregation)

**Mode Restrictions:**
- RowsPerPartition cannot be used with PivotColumn
- Must specify at least one: RowsPerPartition, PivotColumn, or Aggregation
- PivotKeys required when PivotColumn specified

**Aggregation Options:**
- CONCAT: Concatenate all values
- UNIQUE_CONCAT: Concatenate unique values only
- SUM: Sum numeric values
- MIN: Minimum value
- MAX: Maximum value
- AVG: Average of values

**Performance Considerations:**
- Large partitions may impact performance
- High cardinality pivot columns create many output columns
- CLOB operations are expensive (use only when size > 64000)
- Aggregation mode generally more efficient than row-based pivoting

**NULL Handling:**
- NULL values in pivot column are ignored
- Default values can be specified for missing pivot keys
- Accumulate copies values from last row in partition

### Best Practices

**1. Choose Appropriate Mode**
- Use RowsPerPartition for fixed-structure data
- Use PivotColumn for attribute-value pairs
- Use Aggregation for summary/rollup needs
- Combine modes for complex transformations

**2. Optimize Partitioning**
- Partition on logical grouping keys
- Avoid too many or too few partitions
- Consider downstream analysis requirements
- Balance partition size for performance

**3. Handle NULL Values**
- Specify DefaultPivotValues for missing keys
- Use Accumulate to preserve important metadata
- Consider NULL handling in aggregations
- Test edge cases with sparse data

**4. Manage Output Size**
- Monitor output column count
- Use appropriate CombinedColumnSizes
- Consider TruncateColumns for large concatenations
- Validate output doesn't exceed limits

**5. Ensure Reproducibility**
- Use ORDER BY with RowsPerPartition
- Document pivot key ordering
- Maintain consistent partition definitions
- Version pivot specifications

**6. Validate Results**
- Check output column names
- Verify aggregation results
- Test with sample data first
- Validate against source row counts

### Related Functions
- **TD_Unpivoting** - Converts dense format back to sparse format (inverse operation)
- **TD_Pivot** - General SQL pivot function (not optimized for inDB analytics)
- **TD_ColumnTransformer** - Combined transformation pipeline
- **TD_ScaleTransform** - Often used after pivoting for feature scaling

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Transform Functions
