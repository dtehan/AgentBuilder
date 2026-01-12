# TD_FillRowID

### Function Name
**TD_FillRowID**

### Description
TD_FillRowID adds a column of unique row identifiers to an input table, assigning each row a distinct numeric identifier. This function automatically generates sequential identifiers that uniquely identify each row within the table, enabling efficient row-level operations, data tracking, and table relationships essential for relational database design and data engineering workflows.

Row identifiers serve as the fundamental building block for data integrity and relational database operations. They provide a unique, immutable reference to each record, enabling precise row retrieval, updates, and deletions without ambiguity. When combined with PARTITION BY and ORDER BY clauses, TD_FillRowID can generate identifiers that respect logical groupings and orderings within the data, making it ideal for creating sequence numbers within categories, generating surrogate keys, or establishing hierarchical relationships.

The function operates efficiently on large datasets by leveraging Teradata's parallel processing capabilities. Row IDs are assigned during execution and can vary between runs if the underlying data order changes, making them suitable for transient identifiers or when combined with deterministic ordering. TD_FillRowID is particularly valuable in data preparation pipelines where unique identifiers are needed for downstream processing, join operations, or creating primary keys for tables that lack them.

### When the Function Would Be Used
- **Generate Surrogate Keys**: Create artificial primary keys for tables lacking natural keys
- **Data Integrity**: Ensure each row has a unique identifier for reliable referencing
- **Efficient Row Retrieval**: Enable fast row lookups using numeric identifiers
- **Table Relationships**: Create foreign keys for relational database design
- **Sequence Generation**: Assign sequential numbers within partitions or groups
- **Deduplication Workflows**: Identify and number duplicate records for processing
- **Row Versioning**: Track multiple versions of records with sequential identifiers
- **Sampling and Testing**: Create systematic samples using row number ranges
- **Data Lineage**: Track individual records through complex ETL pipelines
- **Ordered Processing**: Maintain processing order with explicit sequence numbers
- **Pagination**: Support paginated queries and result set chunking
- **Audit Trails**: Generate unique identifiers for audit and logging systems
- **Merge Operations**: Track source rows during data integration workflows
- **Cross-Reference Tables**: Build mapping tables with explicit row identifiers
- **Machine Learning**: Create observation IDs for training/test split tracking

### Syntax

```sql
TD_FillRowID (
    ON { table | view | (query) } AS InputTable [ PARTITION BY ANY [ ORDER BY order_column ] ]
    USING
    [ RowIDColumnName ('row_id_column') ]
)
```

### Required Syntax Elements for TD_FillRowID

**ON clause (InputTable)**
- Accepts the InputTable clause containing data to which row IDs will be added
- Supports PARTITION BY to generate IDs within partitions
- Supports ORDER BY to control ID assignment order
- PARTITION BY ANY generates IDs across entire table

### Optional Syntax Elements for TD_FillRowID

**RowIDColumnName**
- Specify the name for the output column containing row identifiers
- Column name must follow standard SQL naming conventions
- Default: 'row_id'

**PARTITION BY clause**
- Specifies partitioning columns for grouping rows
- IDs restart at each partition boundary
- PARTITION BY ANY treats entire table as single partition
- Enables sequential numbering within logical groups

**ORDER BY clause**
- Specifies ordering for deterministic ID assignment
- Controls which rows receive which IDs
- Without ORDER BY, ID assignment order is non-deterministic
- Essential for reproducible results

### Input Table Schema

**InputTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| any_column | ANY | Input table can have any schema with any columns |

TD_FillRowID accepts any input table structure and adds a row ID column.

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| row_id_column | BIGINT | Column of unique row identifiers (name specified by RowIDColumnName) |
| input_column | Same as InputTable | All columns copied from InputTable |

All input columns are preserved, with row ID column added.

### Code Examples

**Input Data: titanic_passengers**
```
passenger_name                age  pclass  survived
Mrs. Jacques Heath            35   3       0
Mr. Owen Harris               22   3       0
Mrs. Laina                    26   3       1
Mrs. John Bradley             38   1       1
```

**Example 1: Basic Row ID Generation**
```sql
-- Add unique row IDs to entire table
SELECT * FROM TD_FillRowID (
    ON titanic_passengers AS InputTable PARTITION BY ANY
    USING
    RowIDColumnName ('passenger_id')
) AS dt
ORDER BY passenger_id;
```

**Output:**
```
passenger_id  passenger_name         age  pclass  survived
1             Mrs. Jacques Heath     35   3       0
2             Mr. Owen Harris        22   3       0
3             Mrs. Laina             26   3       1
4             Mrs. John Bradley      38   1       1
```

**Example 2: Partitioned Row IDs (Sequential Within Groups)**
```sql
-- Generate row IDs within each passenger class
SELECT * FROM TD_FillRowID (
    ON titanic_passengers AS InputTable
    PARTITION BY pclass
    ORDER BY age
    USING
    RowIDColumnName ('class_sequence')
) AS dt
ORDER BY pclass, class_sequence;
```

**Output:**
```
class_sequence  pclass  passenger_name         age  survived
1               1       Mrs. John Bradley      38   1
1               3       Mr. Owen Harris        22   0
2               3       Mrs. Laina             26   1
3               3       Mrs. Jacques Heath     35   0
```

**Note**: IDs restart at 1 for each pclass partition.

**Example 3: Ordered Row IDs**
```sql
-- Assign IDs based on age ordering
SELECT * FROM TD_FillRowID (
    ON titanic_passengers AS InputTable
    PARTITION BY ANY
    ORDER BY age ASC
    USING
    RowIDColumnName ('age_rank')
) AS dt
ORDER BY age_rank;
```

**Output (youngest to oldest):**
```
age_rank  passenger_name         age  pclass  survived
1         Mr. Owen Harris        22   3       0
2         Mrs. Laina             26   3       1
3         Mrs. Jacques Heath     35   3       0
4         Mrs. John Bradley      38   1       1
```

**Example 4: Create Surrogate Primary Key**
```sql
-- Add surrogate key to table without natural key
CREATE TABLE customers_with_key AS (
    SELECT * FROM TD_FillRowID (
        ON raw_customers AS InputTable PARTITION BY ANY
        ORDER BY import_date, customer_name
        USING
        RowIDColumnName ('customer_sk')
    ) AS dt
) WITH DATA;

-- customer_sk becomes the surrogate primary key
```

**Example 5: Row Numbering for Deduplication**
```sql
-- Number duplicate records within each group
SELECT * FROM TD_FillRowID (
    ON customer_records AS InputTable
    PARTITION BY customer_email
    ORDER BY created_date DESC
    USING
    RowIDColumnName ('version_num')
) AS dt
WHERE version_num = 1;  -- Keep only most recent record per email

-- Filters to latest version of each customer by email
```

**Example 6: Pagination Support**
```sql
-- Generate row IDs for pagination
CREATE TABLE products_paginated AS (
    SELECT * FROM TD_FillRowID (
        ON products AS InputTable
        PARTITION BY ANY
        ORDER BY product_name
        USING
        RowIDColumnName ('page_row')
    ) AS dt
) WITH DATA;

-- Fetch page 3 (rows 21-30, assuming 10 per page)
SELECT *
FROM products_paginated
WHERE page_row BETWEEN 21 AND 30
ORDER BY page_row;
```

**Example 7: Train-Test Split Identification**
```sql
-- Add row IDs for reproducible ML splits
CREATE TABLE ml_data_with_ids AS (
    SELECT * FROM TD_FillRowID (
        ON ml_dataset AS InputTable
        PARTITION BY ANY
        ORDER BY RANDOM(1, 1000000)  -- Random but reproducible
        USING
        RowIDColumnName ('obs_id')
    ) AS dt
) WITH DATA;

-- Split: 80% train (1-8000), 20% test (8001-10000)
CREATE TABLE training_set AS (
    SELECT * FROM ml_data_with_ids WHERE obs_id <= 8000
) WITH DATA;

CREATE TABLE test_set AS (
    SELECT * FROM ml_data_with_ids WHERE obs_id > 8000
) WITH DATA;
```

**Example 8: Sequence Within Categories**
```sql
-- Generate transaction sequence per customer
SELECT * FROM TD_FillRowID (
    ON transactions AS InputTable
    PARTITION BY customer_id
    ORDER BY transaction_date, transaction_id
    USING
    RowIDColumnName ('txn_sequence')
) AS dt
ORDER BY customer_id, txn_sequence;

-- txn_sequence shows 1st, 2nd, 3rd transaction per customer
-- Useful for cohort analysis and customer journey analytics
```

**Example 9: Sampling with Systematic Selection**
```sql
-- Create 10% systematic sample using row IDs
CREATE TABLE sample_10pct AS (
    SELECT *
    FROM TD_FillRowID (
        ON large_dataset AS InputTable
        PARTITION BY ANY
        ORDER BY RANDOM(1, 999999)
        USING
        RowIDColumnName ('sample_id')
    ) AS dt
    WHERE MOD(sample_id, 10) = 0  -- Every 10th row
) WITH DATA;

-- Systematic sampling ensures even distribution
```

**Example 10: Audit Trail Row Identification**
```sql
-- Generate unique audit IDs for change tracking
CREATE TABLE audit_log_with_ids AS (
    SELECT * FROM TD_FillRowID (
        ON audit_changes AS InputTable
        PARTITION BY table_name
        ORDER BY change_timestamp
        USING
        RowIDColumnName ('audit_seq')
    ) AS dt
) WITH DATA;

-- audit_seq provides unique, sequential audit trail per table
-- Enables precise replay of changes in chronological order
```

### Row ID Generation Process

**Before TD_FillRowID:**
```
passenger_name         age  pclass  survived
Mrs. Jacques Heath     35   3       0
Mr. Owen Harris        22   3       0
Mrs. Laina             26   3       1
Mrs. John Bradley      38   1       1
```

**After TD_FillRowID (with PARTITION BY pclass ORDER BY age):**
```
row_id  pclass  passenger_name         age  survived
4       1       Mrs. John Bradley      38   1
4       3       Mr. Owen Harris        22   0
8       3       Mrs. Laina             26   1
12      3       Mrs. Jacques Heath     35   0
```

**Key Characteristics:**
- Row IDs assigned based on PARTITION BY and ORDER BY
- IDs unique within partition scope
- Sequential numbering respects ordering
- All original columns preserved
- BIGINT data type supports very large row counts

### Use Cases and Applications

**1. Surrogate Key Generation**
- Create artificial primary keys for dimension tables
- Generate keys for tables without natural identifiers
- Support slowly changing dimensions (SCD Type 2)
- Enable star schema and dimensional modeling

**2. Relational Database Design**
- Establish primary keys for table relationships
- Create foreign keys for referential integrity
- Support normalization and denormalization
- Enable efficient join operations

**3. Data Deduplication**
- Number duplicate records for identification
- Identify latest/earliest versions within groups
- Support merge and upsert operations
- Track data quality and duplicate patterns

**4. Pagination and Chunking**
- Support paginated API responses
- Enable batch processing of large datasets
- Implement efficient result set navigation
- Support parallel processing by row ranges

**5. Machine Learning Workflows**
- Create observation IDs for train/test splits
- Track individual predictions and residuals
- Support cross-validation fold assignment
- Enable reproducible sampling

**6. Data Versioning**
- Track multiple versions of records
- Implement temporal tables and histories
- Support audit trails and compliance
- Enable rollback and recovery

**7. Sequential Processing**
- Maintain processing order in ETL pipelines
- Implement ordered message queues
- Support sequential business logic
- Enable resumable batch processing

**8. Customer Journey Analytics**
- Number customer interactions chronologically
- Track event sequences and funnels
- Identify first/last/nth interactions
- Support cohort and retention analysis

**9. Sampling and Testing**
- Create systematic and stratified samples
- Generate test and control groups
- Support A/B testing group assignment
- Enable reproducible sampling strategies

**10. Data Migration and Integration**
- Track source system records during ETL
- Create cross-reference mapping tables
- Support incremental loads and CDC
- Enable data lineage and provenance

### Important Notes

**Non-Deterministic Without ORDER BY:**
- IMPORTANT: Row IDs may differ between executions without ORDER BY
- Always use ORDER BY for reproducible, deterministic results
- Non-deterministic IDs acceptable for transient identifiers
- Consider data distribution and parallel execution effects

**PARTITION BY Behavior:**
- PARTITION BY ANY assigns IDs across entire table
- PARTITION BY column(s) restarts IDs at partition boundaries
- Each partition gets independent ID sequence
- Useful for hierarchical or grouped numbering

**Data Type:**
- Row IDs are BIGINT (64-bit signed integer)
- Supports up to 9,223,372,036,854,775,807 rows
- Sufficient for virtually all practical applications
- Consider BIGINT for downstream join operations

**Performance Considerations:**
- Function leverages parallel processing
- PARTITION BY enables distributed ID generation
- ORDER BY may require sorting overhead
- Efficient for both small and very large tables

**ID Gaps:**
- IDs may not be strictly sequential across partitions
- Gaps can occur due to parallel processing
- IDs are unique but not necessarily consecutive
- Do not rely on consecutive numbering

**Comparison to ROW_NUMBER():**
- TD_FillRowID materializes IDs as table column
- ROW_NUMBER() computes IDs in query result
- TD_FillRowID suitable for persistent identifiers
- ROW_NUMBER() suitable for analytical queries

**Column Name Conflicts:**
- RowIDColumnName must not conflict with existing columns
- Choose descriptive names (id, seq, row_num, etc.)
- Default 'row_id' may conflict with existing schemas
- Validate column names before execution

**NULL Handling:**
- Row IDs never NULL (always assigned)
- Input columns can contain NULLs
- NULLs do not affect ID assignment
- All rows receive IDs regardless of NULL values

### Best Practices

**1. Always Use ORDER BY for Reproducibility**
- Specify ORDER BY to ensure deterministic ID assignment
- Order by unique or near-unique columns
- Combine multiple columns for stable ordering
- Document ordering rationale for future reference

**2. Choose Meaningful Column Names**
- Use descriptive names (customer_id, transaction_seq, obs_id)
- Follow organizational naming conventions
- Avoid generic names like 'id' or 'seq'
- Document purpose in data dictionary

**3. Partition Appropriately**
- PARTITION BY logical groupings (customer, category, region)
- Consider downstream analysis requirements
- Balance between granularity and performance
- Document partitioning strategy

**4. Validate ID Uniqueness**
- Verify IDs are unique within intended scope
- Check for gaps or duplicates after generation
- Test with sample data first
- Monitor for parallel processing anomalies

**5. Document ID Semantics**
- Document whether IDs are surrogate keys or sequences
- Explain partitioning and ordering logic
- Clarify ID scope (global vs. partition-level)
- Maintain metadata and lineage information

**6. Use for Appropriate Purposes**
- Surrogate keys: Use for tables without natural keys
- Sequences: Use for ordering and ranking
- Transient IDs: Acceptable without ORDER BY
- Avoid using for business logic (use natural keys)

**7. Consider Alternative Approaches**
- ROW_NUMBER() for analytical queries
- Identity columns for auto-incrementing keys
- GUID/UUID for distributed systems
- Natural keys when available and appropriate

**8. Test ID Generation**
- Test with small datasets first
- Verify ordering and partitioning behavior
- Check for expected ID ranges
- Validate with edge cases and NULL values

**9. Monitor Performance**
- Profile execution time on large datasets
- Optimize ORDER BY expressions
- Consider partitioning for parallel processing
- Monitor resource utilization

**10. Combine with Other Operations**
- Use with deduplication workflows
- Integrate into ETL pipelines
- Combine with sampling strategies
- Support train-test split generation

### Related Functions
- **ROW_NUMBER()** - Window function for analytical row numbering (alternative)
- **RANK()** - Window function for ranking with ties
- **DENSE_RANK()** - Window function for dense ranking
- **TD_Analyze** - Data profiling and quality assessment
- **TD_RANDOMSAMPLE** - Statistical sampling functions

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Utility Functions
