# TD_CategoricalSummary

### Function Name
**TD_CategoricalSummary**

### Description
TD_CategoricalSummary displays the distinct values and their counts for each specified input table column. A categorical summary refers to a summary of data that is organized into distinct categories or groups. This type of summary is commonly used when dealing with data that is nominal or categorical in nature, such as demographic information, survey responses, or the type of products purchased by customers.

### When the Function Would Be Used
- **Data Exploration**: Identifying patterns, relationships, and outliers in categorical data
- **Feature Engineering**: Guiding the selection and transformation of features for predictive models
- **Model Evaluation**: Assessing the performance of models and comparing them with other models or benchmarks
- **Demographic Analysis**: Understanding distribution of categorical demographic information
- **Survey Analysis**: Analyzing survey responses and categorical feedback
- **Product Analysis**: Understanding product type distributions and customer purchase patterns
- **Healthcare**: Analyzing categorical health indicators and patient demographics
- **Quality Control**: Monitoring categorical quality metrics and defect classifications

### Syntax
```sql
TD_CategoricalSummary (
    ON { table | view | (query) } AS InputTable
    USING
    TargetColumns ({ 'target_column' | target_column_range }[,...])
)
```

### Required Syntax Elements for TD_CategoricalSummary

**ON clause**
- Accepts the InputTable clause

**TargetColumns**
- Specify the names of the InputTable columns for which to display the distinct values and their counts
- Supports column ranges using bracket notation (e.g., '[0:2]', '[:]')

### Optional Syntax Elements for TD_CategoricalSummary
All syntax elements are required.

### Input Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | CHAR, VARCHAR (CHARACTER SET LATIN or UNICODE) | Column to display distinct values and their counts |

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| ColumnName | VARCHAR (CHARACTER SET UNICODE) | Name of target_column |
| DistinctValue | VARCHAR (CHARACTER SET LATIN or UNICODE) | Name of distinct value in target_column. One row for each distinct value |
| DistinctValueCount | BIGINT | Count of distinct value in target_column. One row for each distinct value |

### Code Examples

**Input Table: cat_titanic_train**
```
passenger  survived  pclass  name                                         gender  age  embarked  cabin
97         0         1       Goldschmidt; Mr. George B                    male    71   C         A5
488        0         1       Kent; Mr. Edward Austin                      male    58   C         B37
505        1         1       Maioni; Miss. Roberta                        female  16   S         B79
631        1         1       Barkworth; Mr. Algernon Henry Wilson         male    80   S         A23
873        0         1       Carlsson; Mr. Frans Olof                     male    33   S         B51 B53 B55
```

**Example 1: Single Column Categorical Summary**
```sql
SELECT * FROM TD_CategoricalSummary (
    ON cat_titanic_train AS InputTable
    USING
    TargetColumns ('gender')
) AS dt;
```

**Output:**
```
ColumnName  DistinctValue  DistinctValueCount
gender      female         1
gender      male           4
```

**Example 2: Multiple Columns Categorical Summary**
```sql
SELECT * FROM TD_CategoricalSummary (
    ON cat_titanic_train AS InputTable
    USING
    TargetColumns ('embarked', 'gender')
) AS dt;
```

**Output:**
```
ColumnName  DistinctValue  DistinctValueCount
embarked    S              3
gender      female         1
embarked    C              2
gender      male           4
```

**Example 3: Using Column Range Indexing**
```sql
-- Using column indexes (0-based indexing)
-- Columns 0, 1, 2 from passengers_2 table
SELECT * FROM TD_CategoricalSummary (
    ON passengers_2 AS InputTable
    USING
    TargetColumns ('[0:2]')
) AS dt;
```

**Output:**
```
ColumnName  DistinctValue  DistinctValueCount
name        Ahmed          1
name        Jim            1
name        Harris         1
name        John           1
name        Taha           1
ticket      PC 1772        1
ticket      PC 17754       2
ticket      PC 1984        1
ticket      PC 1754        1
gender      male           5
```

**Example 4: All Columns Using Range Notation**
```sql
-- Select all columns using [:]
SELECT * FROM TD_CategoricalSummary (
    ON passengers_2 AS InputTable
    USING
    TargetColumns ('[:]')
) AS dt;
```

**Output:**
```
ColumnName  DistinctValue  DistinctValueCount
cabin       A3             1
name        Jim            1
cabin       A8             2
cabin       A5             2
name        Ahmed          1
ticket      PC 17754       2
embarked    B              1
embarked    A              1
ticket      PC 1772        1
name        Harris         1
embarked    C              3
ticket      PC 1984        1
gender      male           5
name        John           1
name        Taha           1
ticket      PC 1754        1
```

**Example 5: Customer Demographics Analysis**
```sql
-- Analyze customer categorical attributes
SELECT * FROM TD_CategoricalSummary (
    ON customer_data AS InputTable
    USING
    TargetColumns ('region', 'customer_segment', 'subscription_type')
) AS dt
ORDER BY ColumnName, DistinctValueCount DESC;
```

**Example 6: Product Category Distribution**
```sql
-- Understand product category distributions
SELECT * FROM TD_CategoricalSummary (
    ON sales_data AS InputTable
    USING
    TargetColumns ('product_category', 'sales_channel', 'payment_method')
) AS dt;
```

### Important Notes
- Using indexes in the TargetColumns parameter requires entering square brackets in quotes
- Column indexes are 0-based (first column is index 0)
- Entered column indexes must be of CHAR or VARCHAR datatype
- Select all columns by entering '[:]' in quotes
- Function only works on categorical (CHAR/VARCHAR) columns
- For numeric columns, consider using TD_ColumnSummary or TD_UnivariateStatistics

### Related Functions
- TD_ColumnSummary - For column-level summaries including numeric columns
- TD_UnivariateStatistics - For statistical measures of numeric columns
- TD_Histogram - For frequency distribution analysis

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Data Exploration Functions
