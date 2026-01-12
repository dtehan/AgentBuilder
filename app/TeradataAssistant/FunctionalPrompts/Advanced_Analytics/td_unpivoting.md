# TD_Unpivoting

### Function Name
**TD_Unpivoting**

### Description
TD_Unpivoting transforms data from dense (wide) format to sparse (long) format by converting multiple columns into attribute-value pairs. This function is the inverse operation of TD_Pivoting, taking a traditional tabular format with many columns and converting it into a normalized format with fewer columns where each row represents a single attribute-value combination.

Unpivoting is essential for normalizing denormalized data structures, preparing data for certain types of analysis, and converting wide-format data into formats suitable for sparse data processing or attribute-value storage systems. This transformation is particularly useful when dealing with time-series data, multi-attribute datasets, or when integrating data from different schemas.

### When the Function Would Be Used
- **Dense to Sparse Conversion**: Transform traditional tables to attribute-value format
- **Data Normalization**: Convert denormalized wide tables to normalized structure
- **Schema Flexibility**: Prepare data for schema-less or flexible schema storage
- **Time Series Transformation**: Convert column-based time data to row-based format
- **ETL Processing**: Reshape data for integration with sparse data systems
- **Dynamic Attribute Handling**: Work with variable numbers of attributes
- **Data Integration**: Standardize heterogeneous data formats
- **Vertical Partitioning**: Split wide tables into narrower structures
- **Metadata Extraction**: Convert column data into queryable attributes
- **Sparse Matrix Preparation**: Create input for sparse matrix algorithms

### Dense vs Sparse Format

**Dense Format (Wide) - Before Unpivoting:**
```
Passenger  pclass  gender  age
1          3       male    22
2          1       female  38
```

**Sparse Format (Long) - After Unpivoting:**
```
Passenger  AttributeName  AttributeValue
1          pclass         3
1          gender         male
1          age            22
2          pclass         1
2          gender         female
2          age            38
```

**Benefits of Sparse Format:**
- Normalized data structure
- Flexible schema (easy to add attributes)
- Efficient storage for sparse data
- Easier to query dynamic attributes
- Better for attribute-value databases

### Syntax

```sql
TD_Unpivoting (
    ON { table | view | (query) } AS InputTable [ PARTITION BY partition_column [,...] ]
    USING
    TargetColumns ({ 'target_column' | target_column_range }[,...])
    [ Accumulate ({ 'accumulate_column' | accumulate_column_range }[,...]) ]
    [ AttributeColumn ('attribute_column_name') ]
    [ ValueColumn ('value_column_name') ]
    [ InputTypes ('input_type' [,...]) ]
)
```

### Required Syntax Elements for TD_Unpivoting

**ON clause**
- Accept the InputTable clause
- Optional PARTITION BY clause for distributed processing

**TargetColumns**
- Specify columns from InputTable to unpivot
- These columns become attribute-value pairs
- Maximum 2018 columns
- Supports column range notation

### Optional Syntax Elements for TD_Unpivoting

**Accumulate**
- Specify columns to copy to output table
- Typically used for identifiers and keys
- Values repeated for each unpivoted attribute
- Supports column range notation

**AttributeColumn**
- Specify name for output column containing attribute names
- Default: 'attribute'
- This column will contain the original column names

**ValueColumn**
- Specify name for output column containing attribute values
- Default: 'value_col'
- This column will contain the original column values

**InputTypes**
- Specify data type for each target column
- Used to control output value column type
- Format: One type per target column
- Useful for type preservation

### Input Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| partition_column | ANY | [Optional] Column for partitioning |
| target_column | ANY | Columns to be unpivoted into attribute-value pairs |
| accumulate_column | ANY | Columns to preserve in output (typically identifiers) |

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| accumulate_column | Same as InputTable | Columns specified in Accumulate parameter (repeated for each attribute) |
| attribute_column | VARCHAR | Column containing original column names from TargetColumns |
| value_column | VARCHAR or specified type | Column containing values from TargetColumns |

### Code Examples

**Input Data: titanic_dense**
```
passenger  pclass  gender  age  fare
1          3       male    22   7.25
2          1       female  38   71.28
3          3       female  26   7.93
```

**Example 1: Basic Unpivoting**
```sql
SELECT * FROM TD_Unpivoting (
    ON titanic_dense AS InputTable
    USING
    TargetColumns('pclass', 'gender', 'age', 'fare')
    Accumulate('passenger')
) AS dt
ORDER BY passenger, attribute;
```

**Output:**
```
passenger  attribute  value_col
1          pclass     3
1          gender     male
1          age        22
1          fare       7.25
2          pclass     1
2          gender     female
2          age        38
2          fare       71.28
3          pclass     3
3          gender     female
3          age        26
3          fare       7.93
```

**Example 2: Custom Column Names**
```sql
SELECT * FROM TD_Unpivoting (
    ON titanic_dense AS InputTable
    USING
    TargetColumns('pclass', 'gender', 'age')
    Accumulate('passenger')
    AttributeColumn('feature_name')
    ValueColumn('feature_value')
) AS dt
ORDER BY passenger, feature_name;
```

**Output:**
```
passenger  feature_name  feature_value
1          pclass        3
1          gender        male
1          age           22
2          pclass        1
2          gender        female
2          age           38
```

**Example 3: Column Range Notation**
```sql
SELECT * FROM TD_Unpivoting (
    ON customer_data AS InputTable
    USING
    TargetColumns('[2:10]')  -- Unpivot columns 2 through 10
    Accumulate('customer_id', 'customer_name')
) AS dt
ORDER BY customer_id, attribute;
```

**Example 4: Time Series Unpivoting**
```sql
-- Convert monthly columns to time series format
CREATE TABLE sales_wide (
    product_id INTEGER,
    jan_sales DECIMAL(10,2),
    feb_sales DECIMAL(10,2),
    mar_sales DECIMAL(10,2),
    apr_sales DECIMAL(10,2)
);

SELECT * FROM TD_Unpivoting (
    ON sales_wide AS InputTable
    USING
    TargetColumns('jan_sales', 'feb_sales', 'mar_sales', 'apr_sales')
    Accumulate('product_id')
    AttributeColumn('month')
    ValueColumn('sales_amount')
) AS dt
ORDER BY product_id, month;
```

**Output:**
```
product_id  month       sales_amount
101         jan_sales   15000.00
101         feb_sales   18000.00
101         mar_sales   16500.00
101         apr_sales   19200.00
```

**Example 5: Survey Response Unpivoting**
```sql
-- Convert survey columns to long format
SELECT * FROM TD_Unpivoting (
    ON survey_responses AS InputTable
    USING
    TargetColumns('q1_response', 'q2_response', 'q3_response', 'q4_response', 'q5_response')
    Accumulate('respondent_id', 'survey_date')
    AttributeColumn('question')
    ValueColumn('response')
) AS dt
ORDER BY respondent_id, question;
```

**Example 6: Sensor Data Unpivoting**
```sql
-- Convert sensor reading columns to normalized format
SELECT * FROM TD_Unpivoting (
    ON sensor_readings_wide AS InputTable
    USING
    TargetColumns('temperature', 'humidity', 'pressure', 'wind_speed', 'air_quality')
    Accumulate('sensor_id', 'timestamp', 'location')
    AttributeColumn('measurement_type')
    ValueColumn('measurement_value')
) AS dt;
```

**Example 7: Financial Data Unpivoting**
```sql
-- Convert quarterly financial columns
SELECT * FROM TD_Unpivoting (
    ON company_financials AS InputTable
    USING
    TargetColumns('q1_revenue', 'q2_revenue', 'q3_revenue', 'q4_revenue',
                  'q1_profit', 'q2_profit', 'q3_profit', 'q4_profit')
    Accumulate('company_id', 'fiscal_year')
    AttributeColumn('metric_period')
    ValueColumn('amount')
) AS dt
ORDER BY company_id, fiscal_year, metric_period;
```

**Example 8: Product Attribute Unpivoting**
```sql
-- Convert product feature columns to attribute-value pairs
SELECT * FROM TD_Unpivoting (
    ON product_catalog AS InputTable
    USING
    TargetColumns('color', 'size', 'material', 'weight', 'price', 'stock_level')
    Accumulate('product_id', 'product_name', 'category')
    AttributeColumn('attribute_name')
    ValueColumn('attribute_value')
) AS dt;
```

**Example 9: Patient Vital Signs Unpivoting**
```sql
-- Convert patient vitals to long format for time-series analysis
SELECT * FROM TD_Unpivoting (
    ON patient_vitals AS InputTable
    USING
    TargetColumns('heart_rate', 'blood_pressure_systolic', 'blood_pressure_diastolic',
                  'temperature', 'oxygen_saturation', 'respiratory_rate')
    Accumulate('patient_id', 'measurement_datetime', 'nurse_id')
    AttributeColumn('vital_sign')
    ValueColumn('measurement')
) AS dt
ORDER BY patient_id, measurement_datetime, vital_sign;
```

**Example 10: Complete Pivot-Unpivot Round Trip**
```sql
-- Step 1: Start with sparse format
CREATE TABLE data_sparse (
    id INTEGER,
    attribute VARCHAR(50),
    value VARCHAR(50)
);

-- Step 2: Pivot to dense format
CREATE TABLE data_dense AS (
    SELECT * FROM TD_Pivoting (
        ON data_sparse AS InputTable
        PARTITION BY id
        USING
        PartitionColumns('id')
        TargetColumns('value')
        PivotColumn('attribute')
        PivotKeys('attr1', 'attr2', 'attr3')
    ) AS dt
) WITH DATA;

-- Step 3: Unpivot back to sparse format
SELECT * FROM TD_Unpivoting (
    ON data_dense AS InputTable
    USING
    TargetColumns('value_attr1', 'value_attr2', 'value_attr3')
    Accumulate('id')
    AttributeColumn('attribute')
    ValueColumn('value')
) AS dt;
```

### Use Cases and Applications

**1. Data Normalization**
- Convert denormalized wide tables to normalized structure
- Reduce data redundancy
- Prepare data for relational database storage
- Transform star schema to normalized form

**2. Time Series Preparation**
- Convert period-based columns to time-indexed rows
- Prepare data for time series analysis
- Create temporal event streams
- Generate time-stamped observations

**3. ETL and Data Integration**
- Transform source system formats to target formats
- Standardize heterogeneous data structures
- Prepare data for data lake ingestion
- Convert fixed schema to flexible schema

**4. Machine Learning Feature Engineering**
- Create sparse feature representations
- Prepare data for categorical analysis
- Generate attribute-based features
- Transform wide feature sets to long format

**5. Survey and Questionnaire Processing**
- Convert response matrices to analyzable format
- Prepare survey data for statistical analysis
- Create question-response pairs
- Enable flexible survey data queries

**6. IoT and Sensor Data Processing**
- Normalize multi-sensor readings
- Create unified measurement streams
- Prepare for time-series databases
- Enable cross-sensor analysis

**7. Financial Data Transformation**
- Convert period-based financials to transactions
- Prepare for audit trail creation
- Transform budgets to line items
- Create account activity streams

**8. Healthcare Data Management**
- Normalize patient measurements
- Create observation-based records
- Prepare for clinical data warehouses
- Transform EHR data to standard formats

**9. E-commerce Analytics**
- Convert product attributes to searchable format
- Create flexible product catalogs
- Prepare for NoSQL storage
- Enable dynamic attribute queries

**10. Reporting and Visualization**
- Transform data for visualization tools
- Create drill-down capable datasets
- Prepare for dynamic reporting
- Enable flexible data exploration

### Important Notes

**Output Characteristics:**
- Each target column becomes multiple rows in output
- Number of output rows = input rows × number of target columns
- Accumulate columns are repeated for each attribute
- Attribute column contains original column names

**Data Type Handling:**
- Value column typically VARCHAR to accommodate all types
- Use InputTypes to preserve specific data types
- Mixed data types in target columns may require casting
- NULL values are preserved in unpivoted format

**Performance Considerations:**
- Output size significantly larger than input (row explosion)
- Consider partitioning for large datasets
- Filter unnecessary columns before unpivoting
- Index on accumulate columns for queries

**NULL Handling:**
- NULL values in target columns are preserved
- Rows with NULL still appear in output
- Consider filtering NULLs post-unpivoting if needed
- Accumulate column NULLs are repeated

**Column Limits:**
- Maximum 2018 target columns
- Output limited by system row size
- Consider breaking into multiple unpivot operations for very wide tables

### Best Practices

**1. Choose Appropriate Columns**
- Only unpivot columns that should be attributes
- Keep identifiers in Accumulate
- Exclude columns not needed in output
- Group similar types together

**2. Name Columns Meaningfully**
- Use descriptive AttributeColumn names
- Choose clear ValueColumn names
- Consider downstream usage
- Maintain naming conventions

**3. Manage Output Size**
- Filter input data before unpivoting
- Consider incremental unpivoting for large tables
- Monitor output row counts
- Use appropriate partitioning

**4. Preserve Important Context**
- Include all necessary identifiers in Accumulate
- Keep temporal markers
- Preserve hierarchical relationships
- Maintain referential integrity

**5. Plan for Data Types**
- Understand type conversion implications
- Use InputTypes when type preservation critical
- Test with sample data first
- Document type handling approach

**6. Optimize Queries**
- Create indexes on accumulate columns
- Partition large unpivot operations
- Consider materialized views
- Monitor query performance

### Related Functions
- **TD_Pivoting** - Converts sparse format to dense format (inverse operation)
- **TD_ColumnTransformer** - Combined transformation pipeline
- **TD_Pack** - Alternative for certain data packing scenarios
- **TD_Unpack** - Alternative for certain data unpacking scenarios

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Transform Functions
