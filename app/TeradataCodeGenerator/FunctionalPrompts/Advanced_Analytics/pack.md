# Pack

## Function Name
**Pack** (alias: **TD_PACK**)

## Description
Pack is a data cleaning and transformation function that combines data from multiple input columns into a single packed column. The packed column contains virtual columns for each input column, with values optionally labeled by their source column names and separated by a configurable delimiter. This function is essential for data profiling, data quality assessment, deduplication, and preparing data for text analysis or transmission.

**Key Characteristics:**
- **Column Consolidation**: Combines multiple columns into a single VARCHAR column
- **Virtual Column Structure**: Each source column becomes a virtual column in the packed output
- **Flexible Formatting**: Configurable delimiter and optional column name labels
- **Data Type Handling**: Automatically converts all data types (numeric, date, VARCHAR) to string format
- **Complementary to Unpack**: Packed data can be unpacked using the Unpack function
- **Data Quality Tool**: Simplifies data profiling, deduplication, and error detection
- **Efficient Storage**: Can reduce storage requirements for sparse or repetitive data

## When to Use

### Business Applications
1. **Data Quality Assessment and Profiling**
   - Combine multiple columns to identify duplicate or near-duplicate records
   - Create single-column view of complete records for pattern analysis
   - Detect inconsistencies across related fields
   - Profile data combinations to identify quality issues
   - Simplify data exploration by viewing all fields together

2. **Master Data Management (MDM)**
   - Pack customer attributes for deduplication analysis
   - Create composite keys for entity resolution
   - Identify duplicate customers, products, or accounts
   - Prepare data for fuzzy matching algorithms
   - Consolidate multi-column identifiers into single match keys

3. **Data Migration and ETL**
   - Pack source columns before transmission (reduce column count)
   - Create compact data format for inter-system data transfer
   - Prepare data for legacy system import (single-column format)
   - Archive historical data in compressed format
   - Simplify data lineage tracking (single column to track vs. many)

4. **Text Analytics Preparation**
   - Combine multiple text fields for sentiment analysis
   - Create unified text corpus from fragmented columns
   - Prepare customer feedback data (subject + body + metadata)
   - Consolidate product descriptions, reviews, and attributes
   - Generate training data for NLP models from structured columns

5. **Data Comparison and Change Detection**
   - Pack current and historical records for change detection
   - Create before/after snapshots for audit trails
   - Identify which fields changed between record versions
   - Simplify record comparison logic (single column comparison)
   - Track data evolution over time

6. **Data Export and Reporting**
   - Pack multiple columns for CSV/flat file export
   - Create human-readable concatenated fields for reports
   - Generate email body content from database columns
   - Prepare data for external API calls (single payload field)
   - Create formatted output for business users

7. **Data Archival and Compression**
   - Pack infrequently accessed columns to reduce storage
   - Create single-column archives of historical data
   - Compress sparse data (many NULL columns) into compact format
   - Archive old versions of records before updates
   - Reduce table width for better performance

### Analytical Use Cases
- **Deduplication**: Pack records to identify exact or fuzzy duplicates
- **Clustering Preparation**: Create single feature for distance calculations
- **Hashing**: Generate hash keys from packed multi-column data
- **String Matching**: Prepare data for StringSimilarity function
- **Data Profiling**: Analyze unique value combinations across columns
- **Cardinality Analysis**: Count distinct combinations efficiently
- **Pattern Detection**: Identify common multi-column patterns
- **Data Sampling**: Select representative records based on packed values

## Syntax

```sql
SELECT * FROM Pack (
    ON { table | view | (query) } AS InputTable
    USING
    [ TargetColumns ({ 'target_column' | target_column_range }[,...]) ]
    [ Delimiter ('delimiter') ]
    [ IncludeColumnName ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
    OutputColumn ('output_column')
    [ Accumulate ({ 'accumulate_column' | accumulate_column_range }[,...]) ]
    [ ColCast ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
) AS alias;
```

## Required Elements

### InputTable
The table containing columns to pack into a single output column.

**Typical Contents:**
- Multiple columns of any data type (VARCHAR, numeric, DATE, TIMESTAMP)
- Columns can have different data types (function handles type conversion)
- Columns can contain NULL values (represented as NULL or empty in packed output)
- Typically includes ID columns for tracking records

### OutputColumn
**Required parameter** specifying the name of the packed output column.

**Type:** String (column name)
**Output Type:** VARCHAR (all data types converted to string)
**Constraints:** Must be a valid SQL object name

**Example:** `OutputColumn('packed_data')`

**Best Practices:**
- Use descriptive names: 'customer_packed', 'address_combined', 'record_snapshot'
- Avoid generic names like 'col1' or 'result'
- Include timestamp suffix for historical packs: 'customer_packed_2024'

## Optional Elements

### TargetColumns
Specifies which input columns to pack into the output column. Columns not specified are copied unchanged to the output table (unless excluded entirely).

**Type:** String (column names or column ranges)
**Column Range Syntax:** '[start_column:end_column]' (e.g., '[1:5]' packs columns 1 through 5)
**Default:** All input columns are packed (no columns passed through unchanged)

**Examples:**
- `TargetColumns('city', 'state', 'zip')` - Pack specific named columns
- `TargetColumns('[1:4]')` - Pack columns 1, 2, 3, 4 by position
- `TargetColumns('[2:5]', 'additional_col')` - Combine range and specific columns

**Use Cases:**
- **Pack subset**: Pack only relevant columns, pass through ID columns unchanged
- **Exclude sensitive data**: Don't pack SSN or credit card columns
- **Selective packing**: Pack address columns but keep customer_id separate

### Delimiter
Specifies the character used to separate virtual columns in the packed output.

**Type:** String (single Unicode character in Normalization Form C)
**Default:** ',' (comma)
**Case-Sensitive:** Yes

**Common Delimiters:**
- **','** (comma): Default, CSV-compatible format
- **'|'** (pipe): Common for database exports, less likely to appear in data
- **';'** (semicolon): Alternative to comma for European formats
- **'\t'** (tab): Tab-delimited format
- **':'** (colon): Simple separator for key:value pairs

**Examples:**
- `Delimiter(',')` - Comma-separated: "col1:value1,col2:value2"
- `Delimiter('|')` - Pipe-separated: "col1:value1|col2:value2"
- `Delimiter(';')` - Semicolon-separated: "col1:value1;col2:value2"

**Important Considerations:**
- Choose delimiter that doesn't appear in your data (avoid commas if data contains addresses with commas)
- Pipe (|) often safest choice (rarely appears in text data)
- Document delimiter choice for unpacking operations

### IncludeColumnName
Specifies whether to label each virtual column value with its source column name.

**Type:** Boolean string ('true'/'false' or variants)
**Default:** 'true'
**Values:**
- **'true'** (or 't', 'yes', 'y', '1'): Include column names → "city:Nashville,state:TN"
- **'false'** (or 'f', 'no', 'n', '0'): Exclude column names → "Nashville,TN"

**Examples:**
- `IncludeColumnName('true')` → "city:Nashville,state:Tennessee,temp:35.1"
- `IncludeColumnName('false')` → "Nashville,Tennessee,35.1"

**When to Use 'true' (include names):**
- Data profiling and quality analysis (identify which columns have issues)
- Debugging and data exploration
- Self-documenting packed data (readers understand each value)
- Unpacking data later (column names guide unpacking)
- Variable column structures (not all records have same columns)

**When to Use 'false' (exclude names):**
- Minimize storage size (column names add overhead)
- Create CSV-like format for export
- Data already has fixed, known structure
- Performance optimization (shorter strings)
- Compatibility with systems expecting positional values

### Accumulate
Specifies columns to copy unchanged from input to output table (pass-through columns).

**Type:** String (column names or column ranges)
**Use Cases:**
- ID columns (customer_id, transaction_id)
- Timestamp columns for tracking
- Partition keys for performance
- Foreign keys for joins

**Examples:**
- `Accumulate('customer_id')` - Pass through single ID column
- `Accumulate('id', 'created_date', 'updated_date')` - Multiple tracking columns
- `Accumulate('[0:1]')` - Pass through first two columns by position

**Note:** Columns specified in Accumulate are NOT packed into OutputColumn (they remain separate columns).

### ColCast
Specifies whether to cast numeric columns to VARCHAR before packing.

**Type:** Boolean string ('true'/'false' or variants)
**Default:** 'false'
**Values:**
- **'true'**: Explicitly cast numeric columns to VARCHAR (improves performance)
- **'false'**: Automatic type conversion (slower but handles all types)

**When to Use 'true':**
- Input contains many numeric columns (INTEGER, FLOAT, DECIMAL)
- Performance optimization for large datasets
- Reduce query compilation time

**Example:** `ColCast('true')`

**Performance Impact:**
- Can reduce run time by 10-30% for numeric-heavy tables
- Negligible impact on small datasets (<10K rows)
- Most beneficial with 10+ numeric columns

## Input Specification

### InputTable Schema
```sql
-- Example: Temperature readings table
CREATE TABLE temperature_data (
    sn INTEGER,                      -- ID column (typically accumulated)
    city VARCHAR(50),                -- String column to pack
    state VARCHAR(50),               -- String column to pack
    period TIMESTAMP,                -- Timestamp column to pack (auto-converted to string)
    temp_f DECIMAL(5,2)              -- Numeric column to pack (auto-converted to string)
);
```

**Requirements:**
- No specific data type requirements (Pack handles all Teradata data types)
- Columns can be any type: VARCHAR, CHAR, INTEGER, DECIMAL, FLOAT, DATE, TIMESTAMP, etc.
- NULL values supported (represented as empty or NULL in packed output)
- No minimum or maximum column count

**Data Type Handling:**
- **VARCHAR/CHAR**: Passed through as-is
- **Numeric (INTEGER, DECIMAL, FLOAT)**: Converted to string representation
- **DATE**: Converted to 'YYYY-MM-DD' format
- **TIMESTAMP**: Converted to 'YYYY-MM-DD HH:MI:SS' format (or with fractional seconds)
- **NULL**: Represented as empty string or NULL token

**Best Practices:**
- Include ID/key columns for tracking (use Accumulate to pass through)
- Consider data types when choosing delimiter (avoid conflicts with data content)
- Profile data first to understand NULL frequency and special characters

## Output Specification

### Output Table Schema
```sql
-- Pack output with IncludeColumnName('true')
sn                  | INTEGER          -- Accumulated column (passed through unchanged)
packed_data         | VARCHAR          -- Packed column containing all target columns

-- Example packed_data value (with column names):
-- "city:Nashville,state:Tennessee,period:2022-01-01 00:00:00,temp_f:35.1"
```

```sql
-- Pack output with IncludeColumnName('false')
sn                  | INTEGER          -- Accumulated column
packed_data         | VARCHAR          -- Packed column (values only, no labels)

-- Example packed_data value (without column names):
-- "Nashville,Tennessee,2022-01-01 00:00:00,35.1"
```

**Output Characteristics:**
- **OutputColumn**: VARCHAR column containing all packed data
- **Format**: `column1:value1<delimiter>column2:value2<delimiter>...` (with IncludeColumnName='true')
- **Format**: `value1<delimiter>value2<delimiter>...` (with IncludeColumnName='false')
- **Accumulate columns**: Copied unchanged from input
- **Other columns**: Not in TargetColumns, not in Accumulate → not in output

**VARCHAR Length:**
- Output column length = sum of all input column lengths + delimiters + column name labels
- Teradata automatically determines appropriate VARCHAR length
- May be very long if packing many columns or long text fields

**NULL Handling:**
- NULL values in source columns represented as empty strings in packed output
- Example: If state column is NULL → "city:Nashville,state:,temp_f:35.1"

## Code Examples

### Example 1: Basic Packing with Default Options - Temperature Data

**Business Context:**
A weather analytics company collects hourly temperature readings for multiple cities. They have a table with separate columns for city, state, timestamp, and temperature. For data quality analysis, they need to pack all reading attributes into a single column to identify duplicate or anomalous records, then use the packed data for deduplication and pattern analysis.

**SQL Code:**
```sql
-- Step 1: Review input data structure
SELECT * FROM ville_temperature ORDER BY sn LIMIT 5;

-- Step 2: Pack temperature reading attributes (default: include column names, comma delimiter)
SELECT * FROM Pack (
    ON ville_temperature AS InputTable
    USING
    TargetColumns('[1:4]')              -- Pack columns 1-4 (city, state, period, temp_f)
    Delimiter(',')                      -- Comma separator (default)
    IncludeColumnName('true')           -- Include column names (default)
    OutputColumn('packed_data')
    Accumulate('sn')                    -- Keep serial number as separate column
) AS packed_temps
ORDER BY sn;

-- Step 3: Identify duplicate readings (exact duplicates)
SELECT
    packed_data,
    COUNT(*) AS duplicate_count,
    MIN(sn) AS first_occurrence,
    MAX(sn) AS last_occurrence
FROM packed_temps
GROUP BY packed_data
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;

-- Step 4: Profile unique city/state combinations
SELECT
    REGEXP_SUBSTR(packed_data, 'city:([^,]+)', 1, 1, 'i', 1) AS city,
    REGEXP_SUBSTR(packed_data, 'state:([^,]+)', 1, 1, 'i', 1) AS state,
    COUNT(*) AS reading_count,
    COUNT(DISTINCT packed_data) AS unique_readings
FROM packed_temps
GROUP BY city, state
ORDER BY reading_count DESC;

-- Step 5: Find anomalous temperature readings (temp differs significantly from others at same time)
WITH temp_stats AS (
    SELECT
        REGEXP_SUBSTR(packed_data, 'period:([^,]+)', 1, 1, 'i', 1) AS reading_period,
        CAST(REGEXP_SUBSTR(packed_data, 'temp_f:([^,]+)', 1, 1, 'i', 1) AS DECIMAL(5,2)) AS temperature,
        packed_data,
        sn
    FROM packed_temps
)
SELECT
    reading_period,
    temperature,
    AVG(temperature) OVER (PARTITION BY reading_period) AS avg_temp,
    temperature - AVG(temperature) OVER (PARTITION BY reading_period) AS temp_deviation,
    packed_data,
    sn
FROM temp_stats
WHERE ABS(temperature - AVG(temperature) OVER (PARTITION BY reading_period)) > 5.0
ORDER BY ABS(temp_deviation) DESC;
```

**Sample Output:**
```
-- Step 2: Packed temperature data
sn | packed_data
---+------------------------------------------------------------------------------
1  | city:Nashville,state:Tennessee,period:2022-01-01 00:00:00,temp_f:35.1
2  | city:Nashville,state:Tennessee,period:2022-01-01 01:00:00,temp_f:36.2
3  | city:Nashville,state:Tennessee,period:2022-01-01 02:00:00,temp_f:34.5
4  | city:Nashville,state:Tennessee,period:2022-01-01 03:00:00,temp_f:33.6
5  | city:Nashville,state:Tennessee,period:2022-01-01 04:00:00,temp_f:33.1
6  | city:Knoxville,state:Tennessee,period:2022-01-01 03:00:00,temp_f:33.2
7  | city:Knoxville,state:Tennessee,period:2022-01-01 04:00:00,temp_f:32.8
8  | city:Knoxville,state:Tennessee,period:2022-01-01 05:00:00,temp_f:32.4
9  | city:Knoxville,state:Tennessee,period:2022-01-01 06:00:00,temp_f:32.2
10 | city:Knoxville,state:Tennessee,period:2022-01-01 07:00:00,temp_f:32.4

-- Step 3: Duplicate readings (if any)
packed_data                                                                       | duplicate_count | first_occurrence | last_occurrence
----------------------------------------------------------------------------------+-----------------+------------------+-----------------
city:Nashville,state:Tennessee,period:2022-01-01 03:00:00,temp_f:33.6            | 2               | 4                | 47
(Example: Same reading recorded twice - potential sensor issue or duplicate transmission)

-- Step 4: City/state reading distribution
city      | state     | reading_count | unique_readings
----------+-----------+---------------+-----------------
Nashville | Tennessee | 5             | 5
Knoxville | Tennessee | 5             | 4                ← One duplicate reading

-- Step 5: Anomalous temperature readings
reading_period       | temperature | avg_temp | temp_deviation | packed_data                                                          | sn
--------------------+-------------+----------+----------------+----------------------------------------------------------------------+----
2022-01-01 03:00:00 | 45.6        | 33.4     | +12.2          | city:Memphis,state:Tennessee,period:2022-01-01 03:00:00,temp_f:45.6  | 23
(Outlier: Memphis temp 12.2°F above average for that hour - potential sensor error)
```

**Business Impact:**
- **Data Quality Detection**: Identified 1 duplicate record (sn 4 and 47) - same reading recorded twice
- **Sensor Validation**: Found anomalous reading (Memphis at 45.6°F vs. 33.4°F average) - likely sensor malfunction
- **Efficient Profiling**: Single packed column simplifies pattern analysis vs. checking 4 columns individually
- **Deduplication Prep**: Packed format ready for fuzzy matching to find near-duplicates
- **Storage Efficiency**: Can archive packed historical data more efficiently than wide-table format
- **Next Steps**: Investigate duplicate causes (sensor reset, data pipeline duplication), validate outlier readings with alternative sources

**Why Pack for Data Quality?**
- **Simplifies Comparison**: Easier to compare complete records as single strings
- **Pattern Detection**: Can apply text analytics to packed data (REGEXP, LIKE patterns)
- **Deduplication**: Pack → hash → group by hash for efficient duplicate detection
- **Human Readable**: Packed format with column names easy for analysts to review

---

### Example 2: Compact Packing Without Column Names - CSV Export

**Business Context:**
A retail company needs to export customer address data to a legacy system that expects CSV format with positional values (no column headers in data). They want to pack address components (street, city, state, zip) into a single pipe-delimited field for transmission, excluding column names to minimize data size and match legacy format.

**SQL Code:**
```sql
-- Input: Customer address data
CREATE TABLE customer_addresses AS (
    SELECT 1 AS customer_id, '123 Main St' AS street, 'Nashville' AS city, 'TN' AS state, '37201' AS zip
    UNION ALL
    SELECT 2, '456 Oak Ave', 'Memphis', 'TN', '38103'
    UNION ALL
    SELECT 3, '789 Elm Blvd', 'Knoxville', 'TN', '37919'
    UNION ALL
    SELECT 4, '321 Pine Dr', 'Chattanooga', 'TN', '37402'
    UNION ALL
    SELECT 5, '654 Maple Ln', 'Franklin', 'TN', '37064'
) WITH DATA;

-- Step 1: Pack address components without column names (compact format)
SELECT * FROM Pack (
    ON customer_addresses AS InputTable
    USING
    TargetColumns('street', 'city', 'state', 'zip')
    Delimiter('|')                      -- Pipe delimiter (less likely to appear in addresses)
    IncludeColumnName('false')          -- NO column names (positional values only)
    OutputColumn('packed_address')
    Accumulate('customer_id')           -- Keep customer_id separate for tracking
) AS packed_addresses
ORDER BY customer_id;

-- Step 2: Calculate storage savings
SELECT
    'Original Table' AS format,
    SUM(LENGTH(street) + LENGTH(city) + LENGTH(state) + LENGTH(zip)) AS total_chars,
    COUNT(*) AS row_count,
    CAST(AVG(LENGTH(street) + LENGTH(city) + LENGTH(state) + LENGTH(zip)) AS DECIMAL(10,2)) AS avg_chars_per_row
FROM customer_addresses

UNION ALL

SELECT
    'Packed Format (with names)' AS format,
    SUM(LENGTH('street:' || street || ',city:' || city || ',state:' || state || ',zip:' || zip)) AS total_chars,
    COUNT(*) AS row_count,
    CAST(AVG(LENGTH('street:' || street || ',city:' || city || ',state:' || state || ',zip:' || zip)) AS DECIMAL(10,2)) AS avg_chars_per_row
FROM customer_addresses

UNION ALL

SELECT
    'Packed Format (no names)' AS format,
    SUM(LENGTH(packed_address)) AS total_chars,
    COUNT(*) AS row_count,
    CAST(AVG(LENGTH(packed_address)) AS DECIMAL(10,2)) AS avg_chars_per_row
FROM packed_addresses;

-- Step 3: Export to flat file format (simulated)
SELECT
    customer_id || '|' || packed_address AS export_record
FROM packed_addresses
ORDER BY customer_id;

-- Step 4: Validate packed data can be unpacked correctly
-- (Simulated unpacking using string functions)
SELECT
    customer_id,
    packed_address,
    SPLIT_PART(packed_address, '|', 1) AS unpacked_street,
    SPLIT_PART(packed_address, '|', 2) AS unpacked_city,
    SPLIT_PART(packed_address, '|', 3) AS unpacked_state,
    SPLIT_PART(packed_address, '|', 4) AS unpacked_zip
FROM packed_addresses
ORDER BY customer_id;
```

**Sample Output:**
```
-- Step 1: Packed addresses (no column names)
customer_id | packed_address
------------+--------------------------------------------
1           | 123 Main St|Nashville|TN|37201
2           | 456 Oak Ave|Memphis|TN|38103
3           | 789 Elm Blvd|Knoxville|TN|37919
4           | 321 Pine Dr|Chattanooga|TN|37402
5           | 654 Maple Ln|Franklin|TN|37064

-- Step 2: Storage comparison
format                      | total_chars | row_count | avg_chars_per_row
----------------------------+-------------+-----------+-------------------
Original Table              | 182         | 5         | 36.40
Packed Format (with names)  | 267         | 5         | 53.40             ← 47% overhead from column names!
Packed Format (no names)    | 186         | 5         | 37.20             ← Only 2% overhead from delimiters

-- Step 3: Export records
export_record
---------------------------------------------------
1|123 Main St|Nashville|TN|37201
2|456 Oak Ave|Memphis|TN|38103
3|789 Elm Blvd|Knoxville|TN|37919
4|321 Pine Dr|Chattanooga|TN|37402
5|654 Maple Ln|Franklin|TN|37064

-- Step 4: Unpacking validation
customer_id | packed_address                        | unpacked_street | unpacked_city | unpacked_state | unpacked_zip
------------+---------------------------------------+-----------------+---------------+----------------+--------------
1           | 123 Main St|Nashville|TN|37201       | 123 Main St     | Nashville     | TN             | 37201
2           | 456 Oak Ave|Memphis|TN|38103         | 456 Oak Ave     | Memphis       | TN             | 38103
(All 5 records successfully unpacked - validation passed)
```

**Business Impact:**
- **Storage Efficiency**: Compact format (IncludeColumnName='false') reduces storage by 30% vs. labeled format
  - With column names: 267 total chars (53.4 avg per row)
  - Without column names: 186 total chars (37.2 avg per row)
  - Original 4-column table: 182 total chars (but requires 4 columns vs. 1)

- **Legacy System Compatibility**: Pipe-delimited positional format matches legacy system expectations
  - Export format: `customer_id|street|city|state|zip`
  - No column headers or labels in data (as required by legacy system)
  - Fixed positional format (street always position 1, city position 2, etc.)

- **Transmission Efficiency**: Smaller payload for data transfer
  - 30% reduction in data size for network transmission
  - Fewer bytes = faster transmission over slow connections
  - Lower bandwidth costs for large-scale exports

- **Format Flexibility**: Pipe delimiter avoids conflicts with address data
  - Commas common in addresses ("123 Main St, Suite 200")
  - Pipes rarely appear in address fields
  - Reduces need for escaping/quoting special characters

- **Roundtrip Validation**: Successfully validated unpacking (all values recovered correctly)
  - SPLIT_PART correctly extracts each address component
  - No data loss or corruption
  - Ready for production deployment

**Use Case Extensions:**
- **Bulk Export**: Export 1M customer addresses for nightly batch transfer to legacy CRM
- **API Payload**: Single packed field simplifies REST API responses
- **Flat File Integration**: Generate pipe-delimited files for third-party vendors
- **Archival**: Archive old addresses in compact format (reduce historical data storage by 30%)

---

### Example 3: Customer Deduplication - Master Data Management

**Business Context:**
A financial services company has 500,000 customer records with suspected duplicates from multiple system mergers. They need to identify potential duplicate customers by packing name, address, and contact information into a single column, then using fuzzy matching to find near-duplicates (typos, variations, data entry errors). This is critical for regulatory compliance (KYC) and preventing fraudulent account openings.

**SQL Code:**
```sql
-- Input: Customer master data with potential duplicates
CREATE TABLE customer_master (
    customer_id INTEGER,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    street_address VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(2),
    zip VARCHAR(10),
    phone VARCHAR(15),
    email VARCHAR(100),
    date_of_birth DATE,
    ssn_last4 VARCHAR(4),
    account_opened_date DATE
);

-- Step 1: Pack customer identifying attributes for deduplication
CREATE TABLE customer_packed AS (
    SELECT * FROM Pack (
        ON customer_master AS InputTable
        USING
        TargetColumns('first_name', 'last_name', 'street_address', 'city', 'state', 'zip', 'phone', 'date_of_birth', 'ssn_last4')
        Delimiter('|')
        IncludeColumnName('true')           -- Keep column names for interpretability
        OutputColumn('packed_identity')
        Accumulate('customer_id', 'email', 'account_opened_date')
    ) AS dt
) WITH DATA PRIMARY INDEX (customer_id);

-- Step 2: Create MD5 hash of packed identity for exact duplicate detection
CREATE TABLE customer_with_hash AS (
    SELECT
        *,
        HASHMD5(packed_identity) AS identity_hash
    FROM customer_packed
) WITH DATA PRIMARY INDEX (customer_id);

-- Step 3: Identify exact duplicates (same hash)
CREATE TABLE exact_duplicates AS (
    SELECT
        identity_hash,
        COUNT(*) AS duplicate_count,
        MIN(customer_id) AS master_customer_id,
        ARRAY_AGG(customer_id) AS duplicate_customer_ids,
        MIN(account_opened_date) AS earliest_account,
        MAX(account_opened_date) AS latest_account,
        MIN(packed_identity) AS packed_record
    FROM customer_with_hash
    GROUP BY identity_hash
    HAVING COUNT(*) > 1
) WITH DATA PRIMARY INDEX (identity_hash);

-- Step 4: Fuzzy matching for near-duplicates (using StringSimilarity)
-- Compare all customer pairs within same last name and state (reduce Cartesian product)
CREATE TABLE potential_duplicates AS (
    SELECT
        c1.customer_id AS customer_id_1,
        c2.customer_id AS customer_id_2,
        c1.packed_identity AS identity_1,
        c2.packed_identity AS identity_2,
        sim.jaro_sim,
        sim.ld_sim,
        -- Calculate component similarities
        TD_StringSimilarity(c1.first_name, c2.first_name, 'jaro') AS first_name_sim,
        TD_StringSimilarity(c1.last_name, c2.last_name, 'jaro') AS last_name_sim,
        TD_StringSimilarity(c1.street_address, c2.street_address, 'jaro') AS address_sim,
        -- Business rule: Likely duplicate if high overall similarity
        CASE
            WHEN sim.jaro_sim >= 0.95 THEN 'Very Likely Duplicate'
            WHEN sim.jaro_sim >= 0.90 THEN 'Likely Duplicate'
            WHEN sim.jaro_sim >= 0.85 THEN 'Possible Duplicate'
            ELSE 'Unlikely Duplicate'
        END AS duplicate_likelihood
    FROM customer_with_hash c1
    INNER JOIN customer_with_hash c2
        ON c1.last_name = c2.last_name              -- Same last name
        AND c1.state = c2.state                     -- Same state
        AND c1.customer_id < c2.customer_id         -- Avoid duplicate pairs (1,2) and (2,1)
    CROSS APPLY (
        SELECT
            TD_StringSimilarity(c1.packed_identity, c2.packed_identity, 'jaro') AS jaro_sim,
            TD_StringSimilarity(c1.packed_identity, c2.packed_identity, 'LD') AS ld_sim
        ) AS sim
    WHERE sim.jaro_sim >= 0.85                      -- Filter to likely duplicates only
) WITH DATA;

-- Step 5: Prioritize duplicates by risk (higher similarity = higher risk)
SELECT
    duplicate_likelihood,
    COUNT(*) AS pair_count,
    ROUND(AVG(jaro_sim), 3) AS avg_similarity,
    ROUND(MIN(jaro_sim), 3) AS min_similarity,
    ROUND(MAX(jaro_sim), 3) AS max_similarity
FROM potential_duplicates
GROUP BY duplicate_likelihood
ORDER BY
    CASE duplicate_likelihood
        WHEN 'Very Likely Duplicate' THEN 1
        WHEN 'Likely Duplicate' THEN 2
        WHEN 'Possible Duplicate' THEN 3
        ELSE 4
    END;

-- Step 6: Sample very likely duplicates for review
SELECT
    customer_id_1,
    customer_id_2,
    jaro_sim AS similarity_score,
    first_name_sim,
    last_name_sim,
    address_sim,
    identity_1,
    identity_2
FROM potential_duplicates
WHERE duplicate_likelihood = 'Very Likely Duplicate'
ORDER BY jaro_sim DESC
LIMIT 10;

-- Step 7: Calculate deduplication impact
SELECT
    'Total Customers' AS metric,
    COUNT(*) AS count
FROM customer_master

UNION ALL

SELECT
    'Exact Duplicates',
    SUM(duplicate_count - 1)
FROM exact_duplicates

UNION ALL

SELECT
    'Fuzzy Duplicates (Very Likely)',
    COUNT(*)
FROM potential_duplicates
WHERE duplicate_likelihood = 'Very Likely Duplicate'

UNION ALL

SELECT
    'Total Potential Duplicates',
    (SELECT SUM(duplicate_count - 1) FROM exact_duplicates) +
    (SELECT COUNT(*) FROM potential_duplicates WHERE duplicate_likelihood IN ('Very Likely Duplicate', 'Likely Duplicate'));
```

**Sample Output:**
```
-- Step 1: Packed customer identities
customer_id | packed_identity                                                                                                          | email                    | account_opened_date
------------+--------------------------------------------------------------------------------------------------------------------------+--------------------------+---------------------
1001        | first_name:John|last_name:Smith|street_address:123 Main St|city:Nashville|state:TN|zip:37201|phone:615-555-1234|...  | john.smith@email.com     | 2020-03-15
1002        | first_name:Jon|last_name:Smith|street_address:123 Main Street|city:Nashville|state:TN|zip:37201|phone:615-555-1234|... | jon.smith@email.com      | 2021-08-22
(Note: customer_id 1001 and 1002 are likely the same person - typo in first name, street vs. St abbreviation)

-- Step 3: Exact duplicates identified
identity_hash                    | duplicate_count | master_customer_id | duplicate_customer_ids | earliest_account | latest_account | packed_record
---------------------------------+-----------------+--------------------+------------------------+------------------+----------------+---------------
a3f5e7c9... (MD5 hash)           | 3               | 2045               | [2045, 2156, 2389]     | 2019-05-12       | 2022-11-30     | first_name:Mary|last_name:Johnson|...
b8d2f1a4... (MD5 hash)           | 2               | 3012               | [3012, 3278]           | 2020-07-18       | 2021-04-05     | first_name:Robert|last_name:Williams|...
(32 exact duplicate groups found, totaling 87 duplicate records)

-- Step 5: Duplicate risk summary
duplicate_likelihood    | pair_count | avg_similarity | min_similarity | max_similarity
-----------------------+------------+----------------+----------------+----------------
Very Likely Duplicate  | 234        | 0.963          | 0.950          | 0.998
Likely Duplicate       | 567        | 0.912          | 0.900          | 0.949
Possible Duplicate     | 1,234      | 0.878          | 0.850          | 0.899

-- Step 6: Sample very likely duplicates
customer_id_1 | customer_id_2 | similarity_score | first_name_sim | last_name_sim | address_sim | identity_1                                    | identity_2
--------------+---------------+------------------+----------------+---------------+-------------+-----------------------------------------------+-----------------------------------------------
1001          | 1002          | 0.978            | 0.933          | 1.000         | 0.967       | first_name:John|last_name:Smith|street_address:123 Main St|...  | first_name:Jon|last_name:Smith|street_address:123 Main Street|...
2345          | 2389          | 0.972            | 0.967          | 1.000         | 0.978       | first_name:Jennifer|last_name:Davis|street_address:456 Oak Ave|... | first_name:Jenifer|last_name:Davis|street_address:456 Oak Avenue|...
(High similarity scores indicate data entry errors: John/Jon, Main St/Main Street, Jennifer/Jenifer, Ave/Avenue)

-- Step 7: Deduplication impact
metric                             | count
-----------------------------------+-------
Total Customers                    | 500,000
Exact Duplicates                   | 87
Fuzzy Duplicates (Very Likely)     | 234
Total Potential Duplicates         | 888           ← 0.18% duplicate rate
```

**Business Impact:**

**Duplicate Detection Results:**
- **Exact Duplicates**: 87 records (0.017%) - 100% confidence, safe to merge immediately
  - 32 duplicate groups (2-3 accounts per person)
  - Caused by: System mergers, data imports, user error
  - Action: Merge accounts, transfer balances to master_customer_id

- **Very Likely Duplicates**: 234 records (0.047%) - 95%+ similarity, high confidence
  - Caused by: Typos (John/Jon, Jennifer/Jenifer), abbreviations (St/Street, Ave/Avenue)
  - Action: Manual review recommended, auto-merge if rules permit

- **Likely Duplicates**: 567 records (0.113%) - 90-95% similarity, moderate confidence
  - May include: Middle name variations, recent address changes, phone number updates
  - Action: Case-by-case review required

- **Total Impact**: 888 potential duplicates (0.18% of 500K customers)
  - Lower than expected 2-5% duplicate rate (good data quality)
  - Deduplication will consolidate 888 duplicate accounts → ~888 fewer records

**Regulatory Compliance (KYC - Know Your Customer):**
- **Fraud Prevention**: Identified 234 very likely duplicate accounts
  - Prevents fraudulent multiple account openings
  - Detects synthetic identity fraud (same SSN, slightly different names)
  - Regulatory requirement: Single view of customer across all accounts

- **AML Compliance (Anti-Money Laundering):**
  - Duplicate accounts used to structure transactions below reporting thresholds
  - Packed identity enables cross-account pattern detection
  - Auditors require documented deduplication methodology

**Financial Impact:**
- **Operational Efficiency**: Reduce duplicate account maintenance costs
  - 888 duplicate accounts × $50/year maintenance = $44,400 annual savings
  - Customer service efficiency: Single account view reduces call handling time

- **Fraud Loss Prevention**: Detecting duplicate identities prevents fraud
  - Industry average: $2,000 fraud loss per duplicate identity
  - 234 very likely duplicates × 10% fraud rate × $2,000 = $46,800 potential fraud prevented

- **Regulatory Penalty Avoidance**: Failure to maintain single customer view = fines
  - Regulatory fines for KYC failures: $100K - $10M range
  - Documented deduplication process demonstrates compliance

**Technical Benefits of Pack Function:**
- **Single-Column Comparison**: Pack enables efficient similarity calculation
  - Without Pack: Must compare 9 columns individually (first_name, last_name, address, etc.)
  - With Pack: Single StringSimilarity call on packed_identity column
  - 80% reduction in query complexity

- **Hash-Based Exact Match**: MD5(packed_identity) enables instant exact duplicate detection
  - GROUP BY hash vs. 9-way JOIN on all columns
  - 100x faster exact match detection

- **Interpretable Results**: Packed format with column names aids manual review
  - Analysts see: "first_name:John|last_name:Smith|..."
  - Easy to spot differences: John vs. Jon, St vs. Street
  - Faster manual review (5 minutes vs. 15 minutes per duplicate group)

**Next Steps:**
1. **Auto-Merge Exact Duplicates**: 87 records with 100% confidence
2. **Manual Review Very Likely Duplicates**: 234 records flagged for compliance team
3. **Implement Real-Time Duplicate Detection**: Check packed_identity at account opening
4. **Quarterly Deduplication**: Re-run process every quarter to catch new duplicates

---

### Example 4: Change Data Capture and Audit - Tracking Record Evolution

**Business Context:**
A healthcare provider must maintain complete audit trails for patient records per HIPAA compliance. When patient demographic or insurance information changes, they need to capture: (1) what changed, (2) when it changed, (3) who changed it. They pack current and previous record states to identify exactly which fields changed and create detailed audit logs.

**SQL Code:**
```sql
-- Current patient records
CREATE TABLE patient_current (
    patient_id INTEGER,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    ssn VARCHAR(11),
    street_address VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(2),
    zip VARCHAR(10),
    insurance_provider VARCHAR(100),
    insurance_policy_number VARCHAR(50),
    primary_physician VARCHAR(100),
    last_updated_date TIMESTAMP,
    last_updated_by VARCHAR(50)
);

-- Historical patient records (before recent update)
CREATE TABLE patient_historical (
    patient_id INTEGER,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    ssn VARCHAR(11),
    street_address VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(2),
    zip VARCHAR(10),
    insurance_provider VARCHAR(100),
    insurance_policy_number VARCHAR(50),
    primary_physician VARCHAR(100),
    snapshot_date TIMESTAMP
);

-- Step 1: Pack current patient records
CREATE TABLE patient_current_packed AS (
    SELECT * FROM Pack (
        ON patient_current AS InputTable
        USING
        TargetColumns('first_name', 'last_name', 'date_of_birth', 'ssn', 'street_address',
                      'city', 'state', 'zip', 'insurance_provider', 'insurance_policy_number',
                      'primary_physician')
        Delimiter('|')
        IncludeColumnName('true')
        OutputColumn('current_state')
        Accumulate('patient_id', 'last_updated_date', 'last_updated_by')
    ) AS dt
) WITH DATA;

-- Step 2: Pack historical patient records (same fields)
CREATE TABLE patient_historical_packed AS (
    SELECT * FROM Pack (
        ON patient_historical AS InputTable
        USING
        TargetColumns('first_name', 'last_name', 'date_of_birth', 'ssn', 'street_address',
                      'city', 'state', 'zip', 'insurance_provider', 'insurance_policy_number',
                      'primary_physician')
        Delimiter('|')
        IncludeColumnName('true')
        OutputColumn('historical_state')
        Accumulate('patient_id', 'snapshot_date')
    ) AS dt
) WITH DATA;

-- Step 3: Identify changed records (compare packed states)
CREATE TABLE changed_patients AS (
    SELECT
        c.patient_id,
        c.current_state,
        h.historical_state,
        c.last_updated_date,
        c.last_updated_by,
        h.snapshot_date AS previous_snapshot_date,
        -- Flag if states differ
        CASE WHEN c.current_state != h.historical_state THEN 1 ELSE 0 END AS has_changes
    FROM patient_current_packed c
    INNER JOIN patient_historical_packed h ON c.patient_id = h.patient_id
    WHERE c.current_state != h.historical_state
) WITH DATA;

-- Step 4: Detailed field-level change detection
CREATE TABLE patient_audit_log AS (
    SELECT
        patient_id,
        last_updated_date AS change_date,
        last_updated_by AS changed_by,
        previous_snapshot_date,
        -- Extract and compare each field
        CASE
            WHEN REGEXP_SUBSTR(current_state, 'first_name:([^|]+)', 1, 1, 'i', 1) !=
                 REGEXP_SUBSTR(historical_state, 'first_name:([^|]+)', 1, 1, 'i', 1)
            THEN 'first_name'
        END AS changed_field_1,
        CASE
            WHEN REGEXP_SUBSTR(current_state, 'last_name:([^|]+)', 1, 1, 'i', 1) !=
                 REGEXP_SUBSTR(historical_state, 'last_name:([^|]+)', 1, 1, 'i', 1)
            THEN 'last_name'
        END AS changed_field_2,
        CASE
            WHEN REGEXP_SUBSTR(current_state, 'street_address:([^|]+)', 1, 1, 'i', 1) !=
                 REGEXP_SUBSTR(historical_state, 'street_address:([^|]+)', 1, 1, 'i', 1)
            THEN 'street_address'
        END AS changed_field_3,
        CASE
            WHEN REGEXP_SUBSTR(current_state, 'insurance_provider:([^|]+)', 1, 1, 'i', 1) !=
                 REGEXP_SUBSTR(historical_state, 'insurance_provider:([^|]+)', 1, 1, 'i', 1)
            THEN 'insurance_provider'
        END AS changed_field_4,
        CASE
            WHEN REGEXP_SUBSTR(current_state, 'insurance_policy_number:([^|]+)', 1, 1, 'i', 1) !=
                 REGEXP_SUBSTR(historical_state, 'insurance_policy_number:([^|]+)', 1, 1, 'i', 1)
            THEN 'insurance_policy_number'
        END AS changed_field_5,
        -- Store both states for audit
        current_state,
        historical_state
    FROM changed_patients
) WITH DATA;

-- Step 5: Summarize changes by field
SELECT
    changed_field,
    COUNT(*) AS change_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM changed_patients), 2) AS pct_of_changes
FROM (
    SELECT patient_id, changed_field_1 AS changed_field FROM patient_audit_log WHERE changed_field_1 IS NOT NULL
    UNION ALL
    SELECT patient_id, changed_field_2 FROM patient_audit_log WHERE changed_field_2 IS NOT NULL
    UNION ALL
    SELECT patient_id, changed_field_3 FROM patient_audit_log WHERE changed_field_3 IS NOT NULL
    UNION ALL
    SELECT patient_id, changed_field_4 FROM patient_audit_log WHERE changed_field_4 IS NOT NULL
    UNION ALL
    SELECT patient_id, changed_field_5 FROM patient_audit_log WHERE changed_field_5 IS NOT NULL
) AS all_changes
GROUP BY changed_field
ORDER BY change_count DESC;

-- Step 6: Audit trail for specific patient (compliance reporting)
SELECT
    patient_id,
    change_date,
    changed_by,
    changed_field_1,
    changed_field_2,
    changed_field_3,
    changed_field_4,
    changed_field_5,
    -- Extract old and new values for key fields
    REGEXP_SUBSTR(historical_state, 'insurance_provider:([^|]+)', 1, 1, 'i', 1) AS old_insurance,
    REGEXP_SUBSTR(current_state, 'insurance_provider:([^|]+)', 1, 1, 'i', 1) AS new_insurance,
    REGEXP_SUBSTR(historical_state, 'street_address:([^|]+)', 1, 1, 'i', 1) AS old_address,
    REGEXP_SUBSTR(current_state, 'street_address:([^|]+)', 1, 1, 'i', 1) AS new_address
FROM patient_audit_log
WHERE patient_id = 12345
ORDER BY change_date DESC;

-- Step 7: Compliance reporting - recent changes by user
SELECT
    changed_by AS user_name,
    COUNT(DISTINCT patient_id) AS patients_modified,
    COUNT(*) AS total_changes,
    MIN(change_date) AS first_change,
    MAX(change_date) AS last_change
FROM patient_audit_log
WHERE change_date >= CURRENT_DATE - 30  -- Last 30 days
GROUP BY changed_by
ORDER BY total_changes DESC;
```

**Sample Output:**
```
-- Step 3: Changed patients identified
patient_id | current_state                                                                                  | historical_state                                                                             | last_updated_date    | last_updated_by | has_changes
-----------+------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+----------------------+-----------------+-------------
12345      | first_name:John|last_name:Smith|...|street_address:789 New St|...|insurance_provider:BlueCross|... | first_name:John|last_name:Smith|...|street_address:456 Old Ave|...|insurance_provider:Aetna|... | 2024-11-15 14:32:00  | nurse_station_3 | 1
67890      | first_name:Mary|last_name:Johnson|...|insurance_policy_number:BC-9876543|...                      | first_name:Mary|last_name:Johnson|...|insurance_policy_number:BC-1234567|...                    | 2024-11-14 09:15:00  | admin_user_7    | 1

-- Step 5: Change frequency by field
changed_field            | change_count | pct_of_changes
-------------------------+--------------+----------------
street_address           | 1,234        | 45.6           ← Most common change (patients moving)
insurance_provider       | 892          | 32.9           ← Frequent (open enrollment, job changes)
insurance_policy_number  | 756          | 27.9
primary_physician        | 234          | 8.6
first_name               | 12           | 0.4            ← Rare (name corrections, marriage)
last_name                | 8            | 0.3

-- Step 6: Audit trail for patient 12345
patient_id | change_date          | changed_by       | changed_field_1   | changed_field_2        | old_insurance | new_insurance | old_address    | new_address
-----------+----------------------+------------------+-------------------+------------------------+---------------+---------------+----------------+-------------
12345      | 2024-11-15 14:32:00  | nurse_station_3  | street_address    | insurance_provider     | Aetna         | BlueCross     | 456 Old Ave    | 789 New St
12345      | 2024-08-22 10:15:00  | admin_user_7     | insurance_provider| insurance_policy_number| UnitedHealth  | Aetna         | (no address change)
12345      | 2024-03-10 16:45:00  | registration_desk| street_address    | NULL                   | (same)        | (same)        | 123 First St   | 456 Old Ave

-- Step 7: User activity summary (last 30 days)
user_name        | patients_modified | total_changes | first_change         | last_change
-----------------+-------------------+---------------+----------------------+----------------------
nurse_station_3  | 234               | 456           | 2024-10-16 08:00:00  | 2024-11-15 17:30:00
admin_user_7     | 189               | 312           | 2024-10-17 09:15:00  | 2024-11-14 16:45:00
registration_desk| 145               | 234           | 2024-10-18 07:30:00  | 2024-11-13 18:00:00
```

**Business Impact:**

**HIPAA Compliance (Audit Trail Requirements):**
- **Complete Change History**: Captured all field-level changes for 2,706 patient records
  - What changed: street_address (1,234), insurance_provider (892), insurance_policy_number (756)
  - When changed: Timestamp for each modification (last_updated_date)
  - Who changed: User identification (nurse_station_3, admin_user_7, etc.)
  - Before/After States: Both historical_state and current_state preserved

- **Regulatory Requirement**: HIPAA mandates audit trails for Protected Health Information (PHI)
  - Must track: "Who accessed or changed what data, when, and where"
  - Pack function enables: Efficient before/after comparison
  - Audit Log: patient_audit_log table satisfies HIPAA audit requirements

**Operational Insights:**
- **Address Changes**: 1,234 changes (45.6%) - highest frequency
  - Action: Prompt patients to update address at check-in
  - Business impact: Accurate addresses ensure proper billing and mail delivery

- **Insurance Changes**: 892 provider changes (32.9%) + 756 policy number changes (27.9%)
  - Peak periods: January (open enrollment), job changes throughout year
  - Action: Verify insurance at every visit to reduce claim denials
  - Financial impact: Incorrect insurance = $500 avg claim denial × 5% error rate = significant revenue leakage

- **Rare Changes**: first_name (12), last_name (8) - only 0.7% combined
  - Indicates: High data quality (names rarely need correction)
  - When occurs: Marriage, legal name changes, data entry error corrections

**User Activity Monitoring:**
- **High-Volume Users**: nurse_station_3 (456 changes), admin_user_7 (312 changes)
  - Normal: High activity from registration and nursing staff
  - Audit Review: Verify changes are legitimate (no suspicious patterns)

- **Anomaly Detection**: If user suddenly makes 10x normal changes → investigate
  - Possible: Legitimate (mass insurance update project)
  - Possible: Security breach (unauthorized access)

**Technical Benefits of Pack for Change Detection:**
- **Single-Column Comparison**: current_state != historical_state (simple, fast)
  - Alternative: Compare 11 columns individually (complex SQL, 11x slower)
  - Pack method: 90% less code, 10x faster execution

- **Human-Readable Audit**: Packed format with column names
  - Auditors see: "insurance_provider:Aetna" → "insurance_provider:BlueCross"
  - Easy to understand what changed without decoding database values

- **Storage Efficient**: Single packed VARCHAR vs. maintaining full historical snapshots
  - Historical snapshot: 11 columns × average 50 bytes = 550 bytes per record version
  - Packed format: ~300 bytes (45% storage savings)
  - At 1M patients × 5 versions: 2.75GB saved storage

**Cost-Benefit Analysis:**
- **Compliance Cost Avoidance**:
  - HIPAA violation fines: $100 - $50,000 per record (potentially millions)
  - Audit trail prevents violations: "Failed to maintain access logs"
  - Pack-based audit system: $50K implementation cost
  - ROI: Avoidance of single $100K fine = 2:1 return

- **Operational Efficiency**:
  - Manual audit trail review time: 15 min/patient → 5 min/patient (Pack format)
  - 1,000 audits/year × 10 min savings × $60/hour = $10K annual savings

**Next Steps:**
1. **Automated Monitoring**: Alert when > 100 changes by single user in 1 day (anomaly detection)
2. **Patient Portal**: Show patients their change history (transparency, HIPAA right of access)
3. **Predictive Analytics**: Identify patients likely to change insurance (proactive verification)
4. **Extend to Clinical Data**: Pack/track changes to diagnoses, medications, procedures

---

### Example 5: Text Analytics Preparation - Consolidating Multi-Column Text

**Business Context:**
An e-commerce company collects customer product reviews across multiple fields: review_title, review_body, pros, cons, and reviewer_comments. For sentiment analysis and topic modeling using NLP, they need to consolidate all text fields into a single column while preserving field labels to understand which text comes from which source. Pack enables efficient text consolidation for feeding into TD_Sentiment, TD_TextParser, or external NLP models.

**SQL Code:**
```sql
-- Input: Product reviews with multiple text fields
CREATE TABLE product_reviews (
    review_id INTEGER,
    product_id INTEGER,
    reviewer_name VARCHAR(100),
    review_date DATE,
    rating INTEGER,                  -- 1-5 stars
    review_title VARCHAR(200),       -- Short headline
    review_body VARCHAR(2000),       -- Main review text
    pros VARCHAR(500),               -- What customer liked
    cons VARCHAR(500),               -- What customer disliked
    reviewer_comments VARCHAR(1000), -- Additional comments
    helpful_votes INTEGER
);

-- Step 1: Pack all text fields for sentiment analysis
CREATE TABLE reviews_packed AS (
    SELECT * FROM Pack (
        ON product_reviews AS InputTable
        USING
        TargetColumns('review_title', 'review_body', 'pros', 'cons', 'reviewer_comments')
        Delimiter('|')
        IncludeColumnName('true')        -- Keep field labels for interpretability
        OutputColumn('packed_review_text')
        Accumulate('review_id', 'product_id', 'reviewer_name', 'review_date', 'rating', 'helpful_votes')
    ) AS dt
) WITH DATA PRIMARY INDEX (review_id);

-- Step 2: Analyze text length distribution
SELECT
    product_id,
    COUNT(*) AS review_count,
    ROUND(AVG(LENGTH(packed_review_text)), 0) AS avg_text_length,
    ROUND(MIN(LENGTH(packed_review_text)), 0) AS min_text_length,
    ROUND(MAX(LENGTH(packed_review_text)), 0) AS max_text_length,
    -- Categorize reviews by completeness
    SUM(CASE WHEN LENGTH(packed_review_text) < 100 THEN 1 ELSE 0 END) AS minimal_reviews,
    SUM(CASE WHEN LENGTH(packed_review_text) BETWEEN 100 AND 500 THEN 1 ELSE 0 END) AS short_reviews,
    SUM(CASE WHEN LENGTH(packed_review_text) BETWEEN 501 AND 1500 THEN 1 ELSE 0 END) AS medium_reviews,
    SUM(CASE WHEN LENGTH(packed_review_text) > 1500 THEN 1 ELSE 0 END) AS detailed_reviews
FROM reviews_packed
GROUP BY product_id
ORDER BY review_count DESC
LIMIT 10;

-- Step 3: Sentiment analysis on packed text (using hypothetical TD_Sentiment function)
CREATE TABLE review_sentiment AS (
    SELECT
        review_id,
        product_id,
        rating,
        packed_review_text,
        TD_Sentiment(packed_review_text) AS sentiment_score,  -- Hypothetical: -1 (negative) to +1 (positive)
        -- Extract sentiment by field
        TD_Sentiment(REGEXP_SUBSTR(packed_review_text, 'review_body:([^|]+)', 1, 1, 'i', 1)) AS body_sentiment,
        TD_Sentiment(REGEXP_SUBSTR(packed_review_text, 'pros:([^|]+)', 1, 1, 'i', 1)) AS pros_sentiment,
        TD_Sentiment(REGEXP_SUBSTR(packed_review_text, 'cons:([^|]+)', 1, 1, 'i', 1)) AS cons_sentiment
    FROM reviews_packed
) WITH DATA;

-- Step 4: Identify sentiment-rating mismatches (suspicious reviews)
SELECT
    review_id,
    product_id,
    rating AS star_rating,
    sentiment_score,
    CASE
        WHEN rating >= 4 AND sentiment_score < -0.2 THEN 'Positive Rating, Negative Text'
        WHEN rating <= 2 AND sentiment_score > 0.2 THEN 'Negative Rating, Positive Text'
        ELSE 'Aligned'
    END AS sentiment_rating_match,
    packed_review_text
FROM review_sentiment
WHERE (rating >= 4 AND sentiment_score < -0.2)
   OR (rating <= 2 AND sentiment_score > 0.2)
ORDER BY ABS(sentiment_score - ((rating - 3) * 0.5)) DESC  -- Largest mismatches first
LIMIT 20;

-- Step 5: Topic extraction using packed text (prepare for NLP)
-- Extract common phrases from packed reviews for topic modeling
CREATE TABLE review_ngrams AS (
    SELECT
        product_id,
        ngram,
        COUNT(*) AS frequency
    FROM (
        SELECT
            product_id,
            TD_NGram(packed_review_text, 2) AS ngram  -- Hypothetical: Extract 2-word phrases
        FROM reviews_packed
    ) AS ngrams
    GROUP BY product_id, ngram
    HAVING COUNT(*) >= 10
) WITH DATA;

-- Top topics by product
SELECT
    product_id,
    ngram AS common_phrase,
    frequency,
    RANK() OVER (PARTITION BY product_id ORDER BY frequency DESC) AS phrase_rank
FROM review_ngrams
WHERE phrase_rank <= 10
ORDER BY product_id, phrase_rank;

-- Step 6: Product quality insights from packed reviews
SELECT
    product_id,
    COUNT(*) AS total_reviews,
    ROUND(AVG(rating), 2) AS avg_rating,
    ROUND(AVG(sentiment_score), 3) AS avg_sentiment,
    -- Categorize sentiment
    SUM(CASE WHEN sentiment_score >= 0.5 THEN 1 ELSE 0 END) AS very_positive_reviews,
    SUM(CASE WHEN sentiment_score BETWEEN 0.2 AND 0.5 THEN 1 ELSE 0 END) AS positive_reviews,
    SUM(CASE WHEN sentiment_score BETWEEN -0.2 AND 0.2 THEN 1 ELSE 0 END) AS neutral_reviews,
    SUM(CASE WHEN sentiment_score BETWEEN -0.5 AND -0.2 THEN 1 ELSE 0 END) AS negative_reviews,
    SUM(CASE WHEN sentiment_score < -0.5 THEN 1 ELSE 0 END) AS very_negative_reviews,
    -- Identify problem products
    CASE
        WHEN AVG(sentiment_score) < -0.3 THEN 'High Risk Product'
        WHEN AVG(sentiment_score) < 0 THEN 'Needs Improvement'
        WHEN AVG(sentiment_score) < 0.3 THEN 'Average'
        ELSE 'Excellent Product'
    END AS product_quality_category
FROM review_sentiment
GROUP BY product_id
HAVING COUNT(*) >= 20  -- Products with 20+ reviews
ORDER BY avg_sentiment ASC;
```

**Sample Output:**
```
-- Step 1: Packed reviews (sample)
review_id | product_id | rating | packed_review_text
----------+------------+--------+---------------------------------------------------------------------------------
1001      | 5001       | 5      | review_title:Amazing product!|review_body:This laptop exceeded my expectations. Fast, lightweight, great battery life.|pros:Speed, portability, battery|cons:|reviewer_comments:Highly recommend!
1002      | 5001       | 2      | review_title:Disappointed|review_body:Screen cracked after 2 months. Customer service unhelpful.|pros:Initial performance was good|cons:Poor build quality, bad support|reviewer_comments:Would not buy again.

-- Step 2: Text length distribution (top 10 products by review count)
product_id | review_count | avg_text_length | min_text_length | max_text_length | minimal_reviews | short_reviews | medium_reviews | detailed_reviews
-----------+--------------+-----------------+-----------------+-----------------+-----------------+---------------+----------------+------------------
5001       | 1,234        | 487             | 45              | 2,156           | 23              | 456           | 678            | 77
5002       | 892          | 523             | 67              | 1,989           | 12              | 298           | 512            | 70
(Most reviews are medium length 501-1500 chars - good detail for sentiment analysis)

-- Step 4: Sentiment-rating mismatches (suspicious reviews)
review_id | product_id | star_rating | sentiment_score | sentiment_rating_match        | packed_review_text
----------+------------+-------------+-----------------+-------------------------------+---------------------------------------------------
2345      | 5003       | 5           | -0.65           | Positive Rating, Negative Text| review_title:Love it!|review_body:Terrible quality, broke immediately...|pros:Nice packaging|cons:Everything else|...
3456      | 5004       | 1           | 0.78            | Negative Rating, Positive Text| review_title:One star|review_body:Great product, works perfectly. Very satisfied.|pros:Everything|cons:|...
(Suspicious: 5-star with very negative text, or 1-star with very positive text - possible fake reviews or rating errors)

-- Step 5: Top topics by product (sample: product 5001 - laptop)
product_id | common_phrase         | frequency | phrase_rank
-----------+-----------------------+-----------+-------------
5001       | "battery life"        | 234       | 1            ← Most mentioned
5001       | "fast performance"    | 198       | 2
5001       | "lightweight design"  | 176       | 3
5001       | "screen quality"      | 145       | 4
5001       | "keyboard feel"       | 123       | 5
5001       | "build quality"       | 112       | 6
5001       | "customer service"    | 89        | 7
5001       | "value money"         | 87        | 8
5001       | "highly recommend"    | 76        | 9
5001       | "would buy"           | 72        | 10

-- Step 6: Product quality insights
product_id | total_reviews | avg_rating | avg_sentiment | very_positive | positive | neutral | negative | very_negative | product_quality_category
-----------+---------------+------------+---------------+---------------+----------+---------+----------+---------------+-------------------------
5001       | 1,234         | 4.3        | 0.412         | 456           | 423      | 234     | 98       | 23            | Excellent Product
5002       | 892           | 3.8        | 0.198         | 234           | 312      | 267     | 67       | 12            | Average
5003       | 567           | 2.1        | -0.423        | 45            | 78       | 134     | 198      | 112           | Needs Improvement        ← Action needed!
5004       | 445           | 1.9        | -0.587        | 23            | 34       | 89      | 178      | 121           | High Risk Product        ← URGENT!
```

**Business Impact:**

**Text Analytics Efficiency:**
- **Single-Column NLP Input**: Packed 5 text columns → 1 column for sentiment analysis
  - Without Pack: Run sentiment analysis on 5 separate columns (5x processing time)
  - With Pack: Single TD_Sentiment call on packed_review_text (80% time savings)
  - Cost savings: $2,000/month reduced cloud NLP API costs

- **Field-Level Sentiment**: Column labels enable field-specific analysis
  - Extract review_body sentiment: REGEXP_SUBSTR(packed_review_text, 'review_body:([^|]+)')
  - Compare: Pros sentiment (+0.7) vs. Cons sentiment (-0.6) vs. Overall (0.2)
  - Insight: Customers have mixed feelings - strong positives, but also concerns

**Fake Review Detection:**
- **Sentiment-Rating Mismatches**: 156 suspicious reviews identified (0.65% of 24K reviews)
  - Pattern 1: 5-star rating with -0.65 sentiment ("Love it!" title but terrible text)
  - Pattern 2: 1-star rating with +0.78 sentiment (positive text but angry rating)
  - Likely: Fake reviews (competitors), rating mistakes, sarcasm

- **Business Action**:
  - Flag 156 reviews for manual moderation review
  - Remove confirmed fake reviews (improves review authenticity)
  - Contact reviewers with mismatches to verify intent

**Product Quality Insights:**
- **High Risk Product 5004**: avg_sentiment = -0.587, avg_rating = 1.9
  - 299 negative/very negative reviews (67% of 445 total)
  - Action: Immediate product investigation required
  - Potential: Design flaw, quality control issue, batch defect

- **Excellent Product 5001**: avg_sentiment = +0.412, avg_rating = 4.3
  - 879 positive/very positive reviews (71% of 1,234 total)
  - Action: Feature in marketing campaigns, analyze success factors

**Topic Modeling Results:**
- **Product 5001 (Laptop) Key Topics**:
  - Positive: "battery life" (234 mentions), "fast performance" (198), "lightweight design" (176)
  - Concerns: "customer service" (89 mentions), "build quality" (112)
  - Marketing Insight: Promote battery life and performance in ads
  - Product Improvement: Address customer service and build quality issues

**Customer Experience Improvements:**
1. **Targeted Product Improvements**:
   - Product 5004: Urgent quality investigation (high negative sentiment)
   - Product 5003: Design refresh needed (below-average sentiment)
   - Product 5001: Maintain quality, improve customer service

2. **Review Quality Enhancement**:
   - Remove 156 suspected fake reviews
   - Improves review credibility (customers trust authentic reviews)
   - Increases conversion rate: +2% estimated (from 12% to 14%)

3. **Personalized Recommendations**:
   - Use packed review text for collaborative filtering
   - "Customers who liked 'battery life' also liked Product 5007"
   - Increase average order value: +$15/order

**Financial Impact:**
- **Fake Review Removal**: +2% conversion rate × 500K monthly visitors × 12% base conversion × $200 AOV = +$240K monthly revenue
- **Product Quality Action**: Remove Product 5004 from catalog → prevent -$1.5M annual returns/refunds
- **NLP Cost Reduction**: Pack-based consolidation saves 80% processing time = -$2K monthly API costs
- **Total Annual Impact**: +$2.9M revenue improvement + $1.5M cost avoidance = **$4.4M total benefit**

**Next Steps:**
1. **Automated Sentiment Monitoring**: Daily sentiment tracking, alert if product drops below 0.0
2. **Real-Time Review Analysis**: Analyze reviews within 1 hour of submission for fake detection
3. **Multi-Language Support**: Pack and analyze reviews in Spanish, French, German
4. **Integration with CRM**: Flag customers with very negative reviews for proactive outreach

---

### Example 6: Data Archival and Historical Snapshots - Regulatory Compliance

**Business Context:**
A financial services firm must retain 7 years of customer transaction history per SOX (Sarbanes-Oxley) and SEC regulations. Storing full historical snapshots of 50-column transaction tables consumes massive storage (estimated 2TB annually). By packing infrequently-accessed historical columns into a single archive column, they reduce storage by 60% while maintaining full regulatory compliance and data accessibility.

**SQL Code:**
```sql
-- Current transaction table (hot data - frequent access)
CREATE TABLE transactions_current (
    transaction_id BIGINT,
    transaction_date DATE,
    account_id INTEGER,
    transaction_type VARCHAR(50),
    amount DECIMAL(15,2),
    currency VARCHAR(3),
    -- ... 44 additional columns (merchant details, location, device info, risk scores, etc.)
    status VARCHAR(20),
    processing_date DATE,
    settlement_date DATE
);

-- Step 1: Identify transactions to archive (older than 2 years, closed status)
CREATE TABLE transactions_to_archive AS (
    SELECT * FROM transactions_current
    WHERE transaction_date < ADD_MONTHS(CURRENT_DATE, -24)  -- Older than 2 years
      AND status IN ('SETTLED', 'COMPLETED', 'CANCELLED')   -- Closed transactions
) WITH DATA;

-- Step 2: Pack less-frequently-accessed columns for archival
-- Keep essential columns unpacked (transaction_id, date, account_id, amount) for reporting
-- Pack detailed columns (merchant info, device data, risk scores, etc.)
CREATE TABLE transactions_archived AS (
    SELECT * FROM Pack (
        ON transactions_to_archive AS InputTable
        USING
        TargetColumns(
            'merchant_name', 'merchant_category', 'merchant_city', 'merchant_state', 'merchant_country',
            'device_type', 'device_id', 'ip_address', 'user_agent', 'geolocation',
            'risk_score', 'fraud_indicators', 'authentication_method', 'mfa_used', 'mfa_type',
            'processor_response', 'processor_code', 'processor_timestamp', 'interchange_fee',
            'network_fee', 'processing_fee', 'total_fees', 'net_amount',
            'cardholder_name', 'card_last_four', 'card_type', 'card_brand', 'card_expiry',
            'billing_address', 'billing_city', 'billing_state', 'billing_zip', 'billing_country',
            'shipping_address', 'shipping_city', 'shipping_state', 'shipping_zip', 'shipping_country',
            'authorization_code', 'trace_id', 'batch_id', 'terminal_id', 'cashier_id'
        )  -- 40 columns packed
        Delimiter('||')                     -- Double-pipe delimiter (very unlikely in data)
        IncludeColumnName('true')           -- Keep column names for future unpacking
        OutputColumn('archived_details')
        Accumulate(
            'transaction_id', 'transaction_date', 'account_id', 'transaction_type',
            'amount', 'currency', 'status', 'processing_date', 'settlement_date'
        )  -- 9 essential columns remain unpacked
        ColCast('true')                     -- Optimize numeric column casting
    ) AS dt
) WITH DATA PRIMARY INDEX (transaction_id) PARTITION BY RANGE_N(
    transaction_date BETWEEN DATE '2017-01-01' AND DATE '2024-12-31' EACH INTERVAL '1' MONTH
);

-- Step 3: Verify storage reduction
SELECT
    'Original Table' AS table_type,
    COUNT(*) AS row_count,
    SUM(DataBlockSize) / 1024 / 1024 / 1024 AS storage_gb
FROM DBC.TableSize
WHERE DatabaseName = 'financial_db' AND TableName = 'transactions_current'

UNION ALL

SELECT
    'Archived Table' AS table_type,
    COUNT(*) AS row_count,
    SUM(DataBlockSize) / 1024 / 1024 / 1024 AS storage_gb
FROM DBC.TableSize
WHERE DatabaseName = 'financial_db' AND TableName = 'transactions_archived';

-- Step 4: Calculate compression ratio
WITH storage_stats AS (
    SELECT
        COUNT(*) AS archived_count,
        -- Estimate original unpacked size (50 columns × avg 30 bytes/column = 1500 bytes/row)
        COUNT(*) * 1500 AS estimated_unpacked_bytes,
        -- Actual packed size
        SUM(LENGTH(archived_details) + 200) AS actual_packed_bytes  -- +200 for unpacked columns
    FROM transactions_archived
)
SELECT
    archived_count AS transactions_archived,
    ROUND(estimated_unpacked_bytes / 1024.0 / 1024.0 / 1024.0, 2) AS estimated_unpacked_gb,
    ROUND(actual_packed_bytes / 1024.0 / 1024.0 / 1024.0, 2) AS actual_packed_gb,
    ROUND(100.0 * (estimated_unpacked_bytes - actual_packed_bytes) / estimated_unpacked_bytes, 1) AS storage_reduction_pct,
    ROUND((estimated_unpacked_bytes - actual_packed_bytes) / 1024.0 / 1024.0 / 1024.0, 2) AS storage_saved_gb
FROM storage_stats;

-- Step 5: Example query on archived data (reporting still works)
-- Monthly transaction volume by account (using unpacked columns only)
SELECT
    EXTRACT(YEAR FROM transaction_date) AS year,
    EXTRACT(MONTH FROM transaction_date) AS month,
    account_id,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount,
    AVG(amount) AS avg_amount
FROM transactions_archived
WHERE transaction_date BETWEEN DATE '2020-01-01' AND DATE '2020-12-31'
GROUP BY year, month, account_id
ORDER BY year, month, account_id;

-- Step 6: Unpack archived details when needed (rare access)
-- Example: Investigate specific transaction for audit
SELECT
    transaction_id,
    transaction_date,
    amount,
    -- Extract specific fields from packed data
    REGEXP_SUBSTR(archived_details, 'merchant_name:([^|]+)', 1, 1, 'i', 1) AS merchant_name,
    REGEXP_SUBSTR(archived_details, 'merchant_city:([^|]+)', 1, 1, 'i', 1) AS merchant_city,
    REGEXP_SUBSTR(archived_details, 'risk_score:([^|]+)', 1, 1, 'i', 1) AS risk_score,
    REGEXP_SUBSTR(archived_details, 'fraud_indicators:([^|]+)', 1, 1, 'i', 1) AS fraud_indicators,
    archived_details AS full_packed_record  -- Full details if needed
FROM transactions_archived
WHERE transaction_id = 123456789;

-- Step 7: Purge archived data from current table (free up hot storage)
DELETE FROM transactions_current
WHERE transaction_id IN (SELECT transaction_id FROM transactions_archived);

-- Step 8: Monitor archive access patterns (detect if unpacking is too frequent)
CREATE TABLE archive_access_log (
    access_date TIMESTAMP,
    transaction_id BIGINT,
    accessed_by VARCHAR(50),
    access_purpose VARCHAR(200)
);

-- If archive access > 100 queries/day → may need to adjust what's packed vs. unpacked
```

**Sample Output:**
```
-- Step 2: Sample archived transaction
transaction_id | transaction_date | account_id | amount   | currency | archived_details
---------------+------------------+------------+----------+----------+---------------------------------------------------------------------------------
123456789      | 2022-03-15       | 9876543    | 125.50   | USD      | merchant_name:Amazon.com||merchant_category:Online Retail||merchant_city:Seattle||...(40 packed columns)...||fraud_indicators:none||risk_score:low

-- Step 3: Storage comparison
table_type      | row_count   | storage_gb
----------------+-------------+------------
Original Table  | 25,000,000  | 450.5
Archived Table  | 20,000,000  | 180.2      ← 60% reduction!

-- Step 4: Compression ratio details
transactions_archived | estimated_unpacked_gb | actual_packed_gb | storage_reduction_pct | storage_saved_gb
----------------------+-----------------------+------------------+-----------------------+------------------
20,000,000            | 447.1                 | 178.8            | 60.0                  | 268.3            ← Saved 268GB!

-- Step 5: Monthly transaction volume (using unpacked columns - query still fast)
year | month | account_id | transaction_count | total_amount | avg_amount
-----+-------+------------+-------------------+--------------+------------
2020 | 1     | 1001       | 45                | 5,678.90     | 126.20
2020 | 1     | 1002       | 23                | 2,345.67     | 102.03
...(normal reporting queries work without unpacking)

-- Step 6: Detailed transaction investigation (unpack on demand)
transaction_id | transaction_date | amount  | merchant_name | merchant_city | risk_score | fraud_indicators | full_packed_record
---------------+------------------+---------+---------------+---------------+------------+------------------+--------------------
123456789      | 2022-03-15       | 125.50  | Amazon.com    | Seattle       | low        | none             | (full packed string available if needed)
```

**Business Impact:**

**Storage Cost Savings:**
- **Before Pack**: 20M archived transactions × 1,500 bytes/row = 447.1 GB
- **After Pack**: 20M archived transactions × 894 bytes/row (9 unpacked cols + 1 packed col) = 178.8 GB
- **Storage Reduction**: 60.0% (268.3 GB saved)
- **Annual Storage Cost**: $0.50/GB/month enterprise SSD storage
  - Before: 447.1 GB × $0.50 = $223/month = $2,676/year
  - After: 178.8 GB × $0.50 = $89/month = $1,068/year
  - **Savings**: $1,608/year per 20M transactions

- **7-Year Retention Requirement**: 140M total transactions (20M × 7 years)
  - Storage savings: 268.3 GB × 7 = 1,878 GB (1.83 TB)
  - **Total 7-year savings**: $1,608 × 7 = **$11,256**

**Regulatory Compliance (SOX/SEC):**
- **Full Data Retention**: All 50 columns preserved in archived_details
  - Auditors can unpack any transaction for investigation
  - No data loss or deletion (complies with SEC Rule 17a-4)

- **Rapid Audit Response**: Unpack specific transactions on demand
  - Query time: < 1 second to extract merchant_name, risk_score, etc.
  - Compliance: Meet 24-hour audit response requirement

- **Tamper-Evident**: Packed format prevents selective column modification
  - Changing any field requires unpacking, modifying, and repacking entire record
  - Audit trail: Log all unpack operations in archive_access_log
  - Regulatory benefit: Demonstrates data integrity

**Operational Performance:**
- **Query Performance**: Unpacked essential columns enable fast reporting
  - Common queries (monthly volume, account summaries): Use unpacked columns only
  - No performance degradation vs. original table
  - Example: Monthly volume query runs in 2.3 seconds (same as before archival)

- **Rare Detail Access**: < 0.01% of archived transactions unpacked
  - Typical: 100 unpack operations/month out of 20M archived = 0.0005%
  - Audit investigations, fraud reviews, customer disputes
  - Acceptable performance: < 1 second to unpack single transaction

**Data Lifecycle Management:**
- **Tier 1 (Hot - Current Table)**: Recent 2 years, full 50-column structure, SSD storage
- **Tier 2 (Warm - Archived Table)**: 2-7 years old, 9 essential + 1 packed column, SSD storage
- **Tier 3 (Cold - Tape Backup)**: 7+ years, full packed backup, tape storage (not shown)

**Scalability:**
- **Annual Transaction Growth**: 10M new transactions/year
  - Unpacked storage: 10M × 1,500 bytes = 223.9 GB/year
  - Packed storage: 10M × 894 bytes = 134.3 GB/year
  - Annual savings: 89.6 GB = $537/year

- **5-Year Projection**: 50M new transactions
  - Storage savings: 448 GB
  - Cost savings: $2,685 over 5 years

**IT Infrastructure Benefits:**
- **Backup/Recovery Speed**: 60% less data to backup
  - Before: 447.1 GB backup time = 4.5 hours
  - After: 178.8 GB backup time = 1.8 hours
  - Backup window reduction: 2.7 hours (60% faster)

- **Disaster Recovery**: Smaller storage footprint
  - Replication bandwidth: 60% reduction
  - DR site storage: 60% reduction
  - RPO/RTO: Improved recovery time objectives

**Next Steps:**
1. **Extend to 5-Year History**: Archive transactions from 2019-2020 (additional 30M records, 400GB savings)
2. **Automated Archival Pipeline**: Monthly job to pack and archive transactions > 2 years old
3. **Access Pattern Monitoring**: If unpack frequency > 0.1%, review what should remain unpacked
4. **Multi-Tier Strategy**: Move 7+ year archives to tape (Pack + compress + tape = 90% total savings)

---

## Common Use Cases

### Data Quality and Master Data Management
- **Duplicate detection**: Pack records for exact and fuzzy matching
- **Data profiling**: Analyze multi-column patterns in single packed view
- **Entity resolution**: Combine name, address, contact info for matching
- **Data standardization**: Identify inconsistent formatting across columns
- **Change detection**: Compare packed current vs. historical states

### Data Migration and Integration
- **ETL simplification**: Pack source columns before transmission
- **Legacy system integration**: Create single-column format for old systems
- **API payload creation**: Pack multiple fields for REST/SOAP requests
- **Data exchange**: Generate CSV/pipe-delimited export files
- **Cross-system matching**: Pack IDs and attributes for reconciliation

### Text Analytics and NLP
- **Sentiment analysis**: Consolidate review fields for unified analysis
- **Topic modeling**: Combine text columns for corpus creation
- **Document classification**: Pack document metadata and content
- **Customer feedback analysis**: Merge survey responses into single text
- **Search index preparation**: Create full-text searchable packed content

### Audit and Compliance
- **Change tracking**: Pack before/after states for audit trails
- **HIPAA compliance**: Track PHI modifications with packed snapshots
- **SOX compliance**: Maintain immutable packed historical records
- **Regulatory reporting**: Pack transaction details for audit submissions
- **Data lineage**: Track packed record provenance and transformations

### Storage Optimization
- **Archival**: Pack infrequently-accessed columns to reduce storage
- **Historical snapshots**: Maintain compact packed historical versions
- **Sparse data compression**: Pack tables with many NULL values
- **Wide table optimization**: Reduce column count via packing
- **Backup reduction**: Smaller packed archives mean faster backups

### Analytical Workflows
- **Hashing for deduplication**: MD5(packed_data) for fast exact match
- **Distance calculations**: Pack features for similarity metrics
- **Clustering preparation**: Create single feature for distance-based clustering
- **Dimension reduction**: Pack correlated columns into single dimension
- **Pattern mining**: Analyze frequent itemsets from packed multi-column data

## Best Practices

### Choosing What to Pack
1. **Pack together logically related columns**:
   - Address components: street, city, state, zip
   - Name components: first_name, middle_name, last_name, suffix
   - Contact info: phone, email, mobile, fax
   - Transaction details: merchant, location, amount, date

2. **Keep frequently-queried columns unpacked**:
   - ID columns (customer_id, transaction_id)
   - Date/timestamp columns for filtering
   - Numeric columns for aggregations (SUM, AVG, COUNT)
   - Status/category columns for grouping

3. **Consider access patterns**:
   - Pack columns accessed together (viewed as unit)
   - Leave unpacked columns accessed independently
   - Balance between storage savings and query performance

### Delimiter Selection
1. **Choose delimiter not in your data**:
   - **Pipe (|)**: Best choice for most use cases (rarely in text)
   - **Double-pipe (||)**: Even safer for complex data
   - **Tab (\t)**: Good for export formats
   - **Avoid comma**: Common in addresses, amounts, descriptions

2. **Test delimiter safety**:
```sql
-- Check if chosen delimiter appears in data
SELECT COUNT(*)
FROM source_table
WHERE column1 LIKE '%|%'
   OR column2 LIKE '%|%'
   OR column3 LIKE '%|%';
-- Result should be 0 (no conflicts)
```

3. **Document delimiter choice**:
   - Critical for unpacking operations
   - Include in data dictionary
   - Store as metadata with packed table

### IncludeColumnName Decision
**Use 'true' (include names) when:**
- Data exploration and profiling
- Audit trails (need to know what changed)
- Unpacking in future (column names guide extraction)
- Variable structure (not all records have same columns)
- Human readability important

**Use 'false' (exclude names) when:**
- Minimizing storage (names add 20-50% overhead)
- Fixed structure (always same columns in same order)
- Export to CSV/flat file (positional format)
- Performance critical (shorter strings)
- Integration with systems expecting positional data

### Performance Optimization
1. **Use ColCast('true') for numeric-heavy tables**:
   - Reduces query compilation time
   - 10-30% performance improvement
   - Especially beneficial with 10+ numeric columns

2. **Partition packed tables appropriately**:
   - Range partition by date for time-series data
   - Hash partition by ID for uniform distribution
   - Multi-level partitioning for very large tables

3. **Index unpacked columns**:
   - Create indexes on Accumulate columns (used in WHERE/JOIN)
   - No need to index packed column (rarely filtered directly)

4. **Batch packing operations**:
   - Pack in batches of 1M-10M rows
   - Use CTAS (CREATE TABLE AS) vs. INSERT for speed
   - Monitor spool space during large pack operations

### Data Quality Checks
**Before packing:**
```sql
-- Check for NULL values
SELECT
    COUNT(*) AS total_rows,
    SUM(CASE WHEN column1 IS NULL THEN 1 ELSE 0 END) AS null_column1,
    SUM(CASE WHEN column2 IS NULL THEN 1 ELSE 0 END) AS null_column2
FROM source_table;

-- Check for special characters that might interfere
SELECT *
FROM source_table
WHERE column1 LIKE '%|%'  -- If using pipe delimiter
LIMIT 10;
```

**After packing:**
```sql
-- Verify row count matches
SELECT COUNT(*) FROM source_table;        -- Original
SELECT COUNT(*) FROM packed_table;        -- Packed (should match)

-- Spot-check packed data
SELECT * FROM packed_table
ORDER BY RANDOM()
LIMIT 10;

-- Verify no unexpected NULLs in packed column
SELECT COUNT(*) FROM packed_table
WHERE packed_column IS NULL;  -- Should be 0 (unless source had all-NULL rows)
```

### Unpacking Preparation
1. **Document original data types**:
   - Pack converts all types to VARCHAR
   - Record original types for unpacking: INTEGER, DECIMAL(10,2), DATE, etc.
   - Store metadata: column names, types, positions

2. **Test unpacking before deployment**:
```sql
-- Test unpack on sample
SELECT
    packed_column,
    SPLIT_PART(packed_column, '|', 1) AS column1_extracted,
    SPLIT_PART(packed_column, '|', 2) AS column2_extracted,
    SPLIT_PART(packed_column, '|', 3) AS column3_extracted
FROM packed_table
LIMIT 5;

-- Verify extracted values match original
```

3. **Create unpacking views** for common access patterns:
```sql
CREATE VIEW customer_unpacked AS
SELECT
    customer_id,
    SPLIT_PART(packed_customer_data, '|', 1) AS first_name,
    SPLIT_PART(packed_customer_data, '|', 2) AS last_name,
    SPLIT_PART(packed_customer_data, '|', 3) AS email
FROM customer_packed;

-- Users query view instead of manually unpacking
```

### Monitoring and Maintenance
1. **Track packed table sizes**:
```sql
-- Monitor growth over time
SELECT
    CAST(CollectTimeStamp AS DATE) AS snapshot_date,
    TableName,
    SUM(CurrentPerm) / 1024 / 1024 / 1024 AS size_gb
FROM DBC.TableSize
WHERE TableName = 'packed_table'
GROUP BY snapshot_date, TableName
ORDER BY snapshot_date DESC;
```

2. **Monitor access patterns**:
   - Log queries accessing packed data
   - If unpacking operations > 10% of queries → reconsider what's packed
   - Adjust Accumulate columns based on actual access patterns

3. **Refresh packed data periodically**:
   - If source data changes, re-pack to reflect updates
   - Automated jobs for incremental packing
   - Version packed data (packed_data_v1, packed_data_v2)

## Related Functions

### Complementary Functions
- **Unpack**: Unpacks packed columns back to original multi-column format
- **StringSimilarity**: Compare packed records for fuzzy matching and deduplication
- **TD_NGram**: Extract n-grams from packed text for topic modeling
- **TD_Sentiment**: Analyze sentiment of packed review/feedback text
- **TD_TextParser**: Parse and tokenize packed text content

### Data Transformation
- **TD_ConvertTo**: Convert data types before packing
- **TD_ColumnTransformer**: Transform columns before packing
- **TD_Pivot**: Pivot data before packing (pack pivoted columns)
- **TD_Unpivot**: Unpivot before packing (create key-value packed format)

### String Functions
- **CONCAT**: Alternative for simple column concatenation (less flexible than Pack)
- **SPLIT_PART**: Extract values from packed column
- **REGEXP_SUBSTR**: Extract labeled values from packed column with IncludeColumnName('true')
- **HASHMD5**: Generate hash of packed column for exact duplicate detection

### Data Quality
- **TD_Analyze**: Profile data before deciding what to pack
- **TD_UnivariateStatistics**: Analyze column distributions before packing
- **TD_OutlierFilter**: Clean data before packing
- **TD_StringSimilarity**: Compare packed records for duplicates

## Notes and Limitations

### Function Constraints
- **Output is VARCHAR**: All data types converted to string representation
- **No multi-byte delimiter**: Delimiter must be single Unicode character (NFC normalized)
- **Column name requirements**: Special characters in column names require double-quote handling
- **VARCHAR length limit**: Packed column subject to VARCHAR maximum length (64KB in Teradata)

### Data Type Handling
1. **Numeric types**: Converted to string representation
   - INTEGER 123 → "123"
   - DECIMAL(10,2) 123.45 → "123.45"
   - Loss of type information (must track for unpacking)

2. **Date/Time types**: Converted to standard format
   - DATE → 'YYYY-MM-DD'
   - TIMESTAMP → 'YYYY-MM-DD HH:MI:SS'
   - May lose fractional seconds or timezone info

3. **NULL handling**: NULLs represented as empty strings
   - column:value1||column2:||column3:value3 (column2 is NULL)
   - Can be ambiguous: empty string vs. NULL
   - Document NULL handling convention

### Performance Considerations
1. **Packing overhead**: CPU cost to convert and concatenate columns
   - Negligible for small tables (<10K rows)
   - Noticeable for large tables (>10M rows) - budget 1-5 minutes per 1M rows

2. **Unpacking cost**: Extracting values from packed column slower than native column access
   - SPLIT_PART or REGEXP_SUBSTR required
   - 5-10x slower than accessing unpacked columns
   - Design for infrequent unpacking (archive use case)

3. **Query optimization**: Teradata optimizer can't push predicates into packed column
   - WHERE packed_column LIKE '%value%' → full table scan
   - Keep filterable columns unpacked (use Accumulate)

### Storage Considerations
1. **Storage savings vary**:
   - **Best case**: Sparse data, many NULLs → 70-80% reduction
   - **Typical case**: Normal data, including column names → 30-50% reduction
   - **Worst case**: Dense data, no column names → 10-20% reduction (delimiter overhead)

2. **VARCHAR compression**: Teradata compresses VARCHAR columns
   - Packed columns compress well (repetitive column name labels)
   - Actual storage savings less than estimated (compression overlap)

3. **Wide vs. narrow tables**:
   - Wide tables (50+ columns): High storage savings from packing
   - Narrow tables (5-10 columns): Marginal savings, may not justify complexity

### Functional Limitations
1. **No automatic unpacking**: Teradata doesn't auto-unpack for queries
   - Must manually extract with SPLIT_PART or REGEXP_SUBSTR
   - Consider creating views for common unpack patterns

2. **Loss of column metadata**:
   - Data types not preserved (everything becomes VARCHAR)
   - NULL vs. empty string ambiguity
   - Column order must be documented externally

3. **Not suitable for frequent access**:
   - Pack designed for archival, infrequent access
   - If unpacking frequently (>10% queries) → keep columns unpacked

### Business and Compliance Considerations
1. **Regulatory compliance**: Verify packed format acceptable
   - Some regulations require native column format
   - Document packing methodology for auditors
   - Demonstrate data integrity and recoverability

2. **Disaster recovery**: Ensure unpack process documented
   - Store column metadata separately (names, types, order)
   - Test unpack procedure regularly
   - Include in DR runbooks

3. **Data governance**: Update data dictionaries
   - Document which columns packed
   - Explain how to access packed data
   - Train analysts on unpacking techniques

### Recommendations
1. **Start with archival use cases**: Lowest risk, highest storage savings
2. **Test on sample data first**: Validate delimiter, check unpacking, measure storage
3. **Monitor access patterns**: Adjust Accumulate columns based on actual queries
4. **Version packed data**: Allow for schema evolution (packed_v1, packed_v2)
5. **Document thoroughly**: Critical for future unpacking and compliance

---

**Generated from Teradata Database Analytic Functions Version 17.20**
**Function Category**: Data Cleaning - Column Packing
**Last Updated**: November 29, 2025
