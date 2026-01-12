# UNPACK

## Function Name
**UNPACK** | **TD_Unpack**

## Description
UNPACK transforms packed or delimited string data into separate rows or columns, converting a single row containing multiple values into multiple rows (vertical unpacking) or multiple columns (horizontal unpacking). This function is commonly used to normalize denormalized data, parse delimited strings, and convert array-like structures into relational format.

**Key Characteristics:**
- **String Parsing**: Splits delimited strings into individual values
- **Flexible Output**: Creates either multiple rows (UNPACK) or columns (horizontal)
- **Multiple Delimiters**: Supports various delimiter types (comma, pipe, semicolon, etc.)
- **Data Normalization**: Converts denormalized data to normalized form
- **Array Expansion**: Expands array-like strings into relational structure
- **Null Handling**: Configurable handling of empty delimited values

The function is essential for ETL processes, data cleaning, and preparing denormalized data for relational analysis.

## When to Use

### Business Applications

**Data Import and ETL:**
- Parse comma-separated values from flat files
- Split delimited strings from external systems
- Normalize denormalized data imports
- Convert packed data structures to relational format
- Prepare data for database loading

**E-commerce and Product Catalogs:**
- Expand multi-value product attributes (colors, sizes, categories)
- Parse product tag lists into individual tags
- Split category hierarchies into separate rows
- Normalize variant SKUs and options
- Expand customer interest lists

**Marketing and Analytics:**
- Split multi-select survey responses
- Expand email recipient lists
- Parse marketing channel attribution chains
- Normalize customer interest categories
- Split UTM parameter strings

**Healthcare and Life Sciences:**
- Parse diagnosis code lists (ICD-10 multi-codes)
- Split medication lists into individual medications
- Expand procedure code combinations
- Normalize patient allergy lists
- Parse lab test panel results

**Financial Services:**
- Split transaction category codes
- Expand account holder lists
- Parse beneficiary designations
- Normalize investment portfolio holdings
- Split account access permission lists

**Social Media and Text Analysis:**
- Parse hashtag lists
- Split mention strings
- Expand topic category assignments
- Normalize user interest tags
- Parse emoji sequences

## Syntax

```sql
-- Basic vertical unpacking (creates multiple rows)
SELECT * FROM UNPACK (
    ON { table_name | view_name | query }
    USING
    TextColumn ('column_name')
    Delimiter ('delimiter_string')
    [ ColumnToUnpack ('column_name') ]
    [ OutputColumn ('output_column_name') ]
    [ Regex ('pattern') ]
    [ IgnoreInvalid ('true' | 'false') ]
    [ Accumulate ('column_name' [,...]) ]
) AS alias;
```

## Required and Optional Elements

### Required Elements

**TextColumn:**
- Specifies the column containing delimited string data to unpack
- Must be VARCHAR or CHAR data type
- Contains the packed values separated by delimiters
- Format: `TextColumn('column_name')`

**Delimiter:**
- Specifies the delimiter character(s) separating values in the packed string
- Common delimiters: comma ',', pipe '|', semicolon ';', tab '\t'
- Can be multi-character string
- Format: `Delimiter(',')`  or  `Delimiter('|')`
- **Special delimiters:**
  - `','` - Comma (most common)
  - `'|'` - Pipe
  - `';'` - Semicolon
  - `'\t'` - Tab character
  - `' '` - Space
  - Custom multi-character strings

### Optional Elements

**ColumnToUnpack:**
- Alternative to TextColumn for specifying the column to unpack
- Use when column name needs special handling
- Format: `ColumnToUnpack('column_name')`

**OutputColumn:**
- Specifies name for the output column containing unpacked values
- Default name is derived from input column name
- Format: `OutputColumn('unpacked_value')`
- Useful for consistent naming across transformations

**Regex:**
- Uses regular expression pattern instead of fixed delimiter
- More flexible for complex parsing scenarios
- Format: `Regex('pattern')`
- Example: `Regex('[,;|]')` matches comma, semicolon, or pipe
- Example: `Regex('\\s+')` matches one or more whitespace characters

**IgnoreInvalid:**
- Controls handling of malformed or invalid input strings
- **Values:**
  - `'true'`: Skip rows with parsing errors (default)
  - `'false'`: Fail on parsing errors
- Format: `IgnoreInvalid('true')`

**Accumulate:**
- Specifies columns to copy from input to each output row
- Essential for preserving identifiers and context
- Format: `Accumulate('id', 'name', 'date')`
- **Common columns to accumulate:**
  - Primary keys and identifiers
  - Timestamps and dates
  - Grouping columns
  - Descriptive attributes

## Input Specifications

### InputTable Schema

| Column | Data Type | Description | Required |
|--------|-----------|-------------|----------|
| TextColumn | VARCHAR/CHAR | Column containing delimited string to unpack | Yes |
| Accumulate columns | Any type | Columns to preserve in output | No |
| Other columns | Any type | Additional columns (not included in output unless accumulated) | No |

### Data Requirements

- **TextColumn format**: String with consistent delimiter separating values
- **Delimiter consistency**: Same delimiter used throughout each string
- **Null handling**: NULL values in TextColumn result in no output rows
- **Empty strings**: Empty string results in single empty value or no rows (configurable)
- **Trailing delimiters**: Handled based on IgnoreInvalid setting

## Output Specifications

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| [OutputColumn] | VARCHAR | Unpacked individual value from delimited string |
| [Accumulated columns] | Same as input | Columns specified in Accumulate clause |
| token_count | INTEGER | Position/index of unpacked value in original string |

### Output Behavior

**Single Row Input → Multiple Row Output:**
- Input: `product_id=123, tags='electronics,laptop,portable'`
- Output after unpacking tags by delimiter ',':
  ```
  product_id | tag         | token_count
  -----------|-------------|------------
  123        | electronics |           1
  123        | laptop      |           2
  123        | portable    |           3
  ```

**Delimiter Handling:**
- Leading/trailing spaces preserved unless trimmed in pre-processing
- Empty tokens (consecutive delimiters) may create empty strings
- NULL input values produce no output rows

**Token Count:**
- 1-indexed position of value in original delimited string
- Useful for preserving order and identifying first/last values
- Can be used to filter (e.g., only first tag) or aggregate

## Code Examples

### Example 1: Basic Product Tag Expansion
**Business Context:** E-commerce company expanding product tag lists for search and recommendation analysis.

```sql
-- Step 1: Examine packed tag data
SELECT
    product_id,
    product_name,
    product_tags,
    LENGTH(product_tags) - LENGTH(REPLACE(product_tags, ',', '')) + 1 as tag_count
FROM product_catalog
WHERE product_tags IS NOT NULL
SAMPLE 10;

-- Step 2: Unpack product tags into individual rows
CREATE TABLE product_tags_normalized AS (
    SELECT * FROM UNPACK (
        ON product_catalog
        USING
        TextColumn('product_tags')
        Delimiter(',')
        OutputColumn('tag')
        Accumulate('product_id', 'product_name', 'category', 'price')
    ) AS dt
) WITH DATA;

-- Step 3: Analyze tag frequency and co-occurrence
SELECT
    tag,
    COUNT(DISTINCT product_id) as product_count,
    AVG(price) as avg_price_for_tag,
    COUNT(*) as total_occurrences
FROM product_tags_normalized
GROUP BY tag
ORDER BY product_count DESC;

-- Step 4: Find products with multiple specific tags
SELECT
    product_id,
    product_name,
    COUNT(DISTINCT tag) as matching_tags,
    STRING_AGG(tag, ', ') as matched_tag_list
FROM product_tags_normalized
WHERE tag IN ('wireless', 'bluetooth', 'portable', 'rechargeable')
GROUP BY product_id, product_name
HAVING COUNT(DISTINCT tag) >= 3
ORDER BY matching_tags DESC, product_name;
```

**Sample Output:**
```
product_id | product_name           | product_tags                          | tag_count
-----------|------------------------|---------------------------------------|----------
PROD-1001  | Wireless Headphones    | electronics,audio,wireless,bluetooth  |         4
PROD-1002  | Laptop Stand           | office,ergonomic,portable,aluminum    |         4
PROD-1003  | USB Cable              | electronics,cable,usb-c,charging      |         4

tag          | product_count | avg_price_for_tag | total_occurrences
-------------|---------------|-------------------|------------------
electronics  |        12,345 |            234.56 |            12,345
wireless     |         4,567 |            189.90 |             4,567
portable     |         3,890 |            156.78 |             3,890
bluetooth    |         3,456 |            198.45 |             3,456
rechargeable |         2,345 |            145.67 |             2,345

product_id | product_name                | matching_tags | matched_tag_list
-----------|----------------------------|---------------|--------------------------------
PROD-2345  | Bluetooth Speaker          |             4 | wireless, bluetooth, portable, rechargeable
PROD-3456  | Wireless Earbuds           |             3 | wireless, bluetooth, portable
PROD-4567  | Portable Charger           |             3 | portable, rechargeable, wireless
```

**Business Impact:** Normalized 45K+ products with 8.7 tags per product on average, enabling tag-based search and filtering, identified 234 products with 3+ matching feature tags for targeted marketing, and calculated category-specific pricing insights by tag.

---

### Example 2: Multi-Select Survey Response Analysis
**Business Context:** Market research firm analyzing multi-select survey questions where respondents selected multiple options.

```sql
-- Step 1: Unpack multi-select responses
CREATE TABLE survey_responses_unpacked AS (
    SELECT * FROM UNPACK (
        ON survey_responses
        USING
        TextColumn('preferred_features')  -- "feature1|feature2|feature3"
        Delimiter('|')
        OutputColumn('selected_feature')
        Accumulate('response_id', 'respondent_id', 'customer_segment', 'survey_date', 'satisfaction_score')
    ) AS dt
) WITH DATA;

-- Step 2: Feature popularity by customer segment
SELECT
    customer_segment,
    selected_feature,
    COUNT(DISTINCT respondent_id) as respondent_count,
    COUNT(*) as selection_count,
    CAST(COUNT(DISTINCT respondent_id) AS FLOAT) /
        (SELECT COUNT(DISTINCT respondent_id) FROM survey_responses WHERE customer_segment = sr.customer_segment) * 100 as pct_respondents,
    AVG(satisfaction_score) as avg_satisfaction_for_feature
FROM survey_responses_unpacked sr
GROUP BY customer_segment, selected_feature
HAVING COUNT(DISTINCT respondent_id) >= 10
ORDER BY customer_segment, pct_respondents DESC;

-- Step 3: Feature combination analysis
SELECT
    r1.selected_feature as feature1,
    r2.selected_feature as feature2,
    COUNT(DISTINCT r1.respondent_id) as co_occurrence_count,
    CAST(COUNT(DISTINCT r1.respondent_id) AS FLOAT) /
        (SELECT COUNT(DISTINCT respondent_id) FROM survey_responses) * 100 as pct_respondents_with_both
FROM survey_responses_unpacked r1
INNER JOIN survey_responses_unpacked r2
    ON r1.respondent_id = r2.respondent_id
    AND r1.selected_feature < r2.selected_feature  -- Avoid duplicates
GROUP BY feature1, feature2
HAVING COUNT(DISTINCT r1.respondent_id) >= 100
ORDER BY co_occurrence_count DESC;

-- Step 4: Respondent segmentation by feature selection count
SELECT
    customer_segment,
    feature_selection_count,
    COUNT(*) as respondent_count,
    AVG(avg_satisfaction) as avg_satisfaction_score
FROM (
    SELECT
        respondent_id,
        customer_segment,
        COUNT(DISTINCT selected_feature) as feature_selection_count,
        AVG(satisfaction_score) as avg_satisfaction
    FROM survey_responses_unpacked
    GROUP BY respondent_id, customer_segment
) subq
GROUP BY customer_segment, feature_selection_count
ORDER BY customer_segment, feature_selection_count;
```

**Sample Output:**
```
customer_segment | selected_feature      | respondent_count | selection_count | pct_respondents | avg_satisfaction_for_feature
-----------------|----------------------|------------------|-----------------|-----------------|-----------------------------
Premium          | Advanced Analytics    |            2,345 |           2,345 |           65.43 |                        8.90
Premium          | Custom Integrations   |            1,890 |           1,890 |           52.73 |                        8.75
Premium          | Priority Support      |            1,678 |           1,678 |           46.82 |                        9.10
Standard         | Ease of Use           |            4,567 |           4,567 |           78.90 |                        7.85
Standard         | Mobile App            |            3,456 |           3,456 |           59.67 |                        7.60
Standard         | Affordable Pricing    |            3,234 |           3,234 |           55.84 |                        8.20

feature1            | feature2               | co_occurrence_count | pct_respondents_with_both
--------------------|------------------------|---------------------|---------------------------
Ease of Use         | Mobile App             |               3,890 |                     42.35
Advanced Analytics  | Custom Integrations    |               1,678 |                     18.26
Mobile App          | Affordable Pricing     |               2,345 |                     25.52
Priority Support    | Advanced Analytics     |               1,234 |                     13.43

customer_segment | feature_selection_count | respondent_count | avg_satisfaction_score
-----------------|------------------------|------------------|------------------------
Premium          |                       1 |              234 |                   7.20
Premium          |                       2 |              890 |                   8.45
Premium          |                       3 |            1,234 |                   8.90
Premium          |                       4 |              890 |                   9.10
Premium          |                       5 |              334 |                   9.35
Standard         |                       1 |            1,456 |                   6.85
Standard         |                       2 |            2,678 |                   7.60
Standard         |                       3 |            1,456 |                   8.10
```

**Business Impact:** Analyzed 9,200 multi-select survey responses unpacked into 28,450 individual feature selections, identified top features by segment (Premium: Analytics 65%, Standard: Ease of Use 79%), discovered strong feature pairs (Ease of Use + Mobile App: 42% co-occurrence), and found correlation between feature selection count and satisfaction (5 features: 9.35 score vs. 1 feature: 7.20 score).

---

### Example 3: Healthcare Diagnosis Code Expansion
**Business Context:** Hospital expanding multi-diagnosis code strings (ICD-10) for clinical analytics and billing.

```sql
-- Step 1: Unpack diagnosis codes from encounter records
CREATE TABLE patient_diagnoses_normalized AS (
    SELECT * FROM UNPACK (
        ON patient_encounters
        USING
        TextColumn('diagnosis_codes')  -- "E11.9;I10;Z79.4"
        Delimiter(';')
        OutputColumn('diagnosis_code')
        Accumulate('encounter_id', 'patient_mrn', 'patient_id', 'encounter_date', 'provider_id', 'facility', 'primary_diagnosis')
    ) AS dt
) WITH DATA;

-- Step 2: Diagnosis frequency and comorbidity analysis
SELECT
    diagnosis_code,
    dc.diagnosis_name,
    dc.diagnosis_category,
    COUNT(DISTINCT patient_id) as patient_count,
    COUNT(DISTINCT encounter_id) as encounter_count,
    AVG(token_count) as avg_position_in_list
FROM patient_diagnoses_normalized pdn
INNER JOIN diagnosis_code_lookup dc
    ON pdn.diagnosis_code = dc.icd10_code
GROUP BY diagnosis_code, dc.diagnosis_name, dc.diagnosis_category
ORDER BY patient_count DESC;

-- Step 3: Common diagnosis combinations (comorbidities)
SELECT
    d1.diagnosis_code as diagnosis1,
    d1.diagnosis_name as name1,
    d2.diagnosis_code as diagnosis2,
    d2.diagnosis_name as name2,
    COUNT(DISTINCT p1.patient_id) as patient_count,
    CAST(COUNT(DISTINCT p1.patient_id) AS FLOAT) /
        (SELECT COUNT(DISTINCT patient_id) FROM patient_encounters) * 100 as prevalence_pct
FROM patient_diagnoses_normalized p1
INNER JOIN patient_diagnoses_normalized p2
    ON p1.patient_id = p2.patient_id
    AND p1.diagnosis_code < p2.diagnosis_code
INNER JOIN diagnosis_code_lookup d1 ON p1.diagnosis_code = d1.icd10_code
INNER JOIN diagnosis_code_lookup d2 ON p2.diagnosis_code = d2.icd10_code
GROUP BY d1.diagnosis_code, d1.diagnosis_name, d2.diagnosis_code, d2.diagnosis_name
HAVING COUNT(DISTINCT p1.patient_id) >= 50
ORDER BY patient_count DESC;

-- Step 4: Patient complexity scoring based on diagnosis count
SELECT
    patient_id,
    patient_mrn,
    diagnosis_count,
    encounter_count,
    CASE
        WHEN diagnosis_count >= 10 THEN 'HIGH_COMPLEXITY'
        WHEN diagnosis_count >= 5 THEN 'MEDIUM_COMPLEXITY'
        ELSE 'LOW_COMPLEXITY'
    END as complexity_category,
    primary_diagnosis_list
FROM (
    SELECT
        patient_id,
        patient_mrn,
        COUNT(DISTINCT diagnosis_code) as diagnosis_count,
        COUNT(DISTINCT encounter_id) as encounter_count,
        STRING_AGG(DISTINCT diagnosis_code, ', ' ORDER BY diagnosis_code) as primary_diagnosis_list
    FROM patient_diagnoses_normalized
    GROUP BY patient_id, patient_mrn
) subq
ORDER BY diagnosis_count DESC, encounter_count DESC;
```

**Sample Output:**
```
diagnosis_code | diagnosis_name                  | diagnosis_category | patient_count | encounter_count | avg_position_in_list
---------------|--------------------------------|-------------------|---------------|-----------------|---------------------
I10            | Essential Hypertension          | Cardiovascular    |        12,345 |          18,456 |                 2.34
E11.9          | Type 2 Diabetes without comp.   | Endocrine         |        10,234 |          15,678 |                 1.89
Z79.4          | Long-term insulin use           | Medications       |         8,901 |          12,345 |                 3.45
J44.9          | COPD, unspecified               | Respiratory       |         6,789 |           9,876 |                 2.78
N18.3          | Chronic kidney disease, stage 3 | Renal             |         5,678 |           8,234 |                 3.12

diagnosis1 | name1                            | diagnosis2 | name2                             | patient_count | prevalence_pct
-----------|----------------------------------|-----------|-----------------------------------|---------------|---------------
I10        | Essential Hypertension           | E11.9     | Type 2 Diabetes without comp.     |         4,567 |          22.35
E11.9      | Type 2 Diabetes without comp.    | Z79.4     | Long-term insulin use             |         3,890 |          19.03
I10        | Essential Hypertension           | J44.9     | COPD, unspecified                 |         2,345 |          11.47
E11.9      | Type 2 Diabetes without comp.    | N18.3     | Chronic kidney disease, stage 3   |         1,890 |           9.25

patient_mrn | patient_id | diagnosis_count | encounter_count | complexity_category | primary_diagnosis_list
------------|------------|-----------------|-----------------|---------------------|------------------------------------------
MRN-123456  | PAT-98765  |              15 |              23 | HIGH_COMPLEXITY     | E11.9, I10, J44.9, N18.3, Z79.4, ...
MRN-123457  | PAT-98766  |              12 |              18 | HIGH_COMPLEXITY     | E11.9, I10, I25.10, J44.9, Z79.4, ...
MRN-123458  | PAT-98767  |               8 |              12 | MEDIUM_COMPLEXITY   | E11.9, I10, J44.9, Z79.4
MRN-123459  | PAT-98768  |               3 |               5 | LOW_COMPLEXITY      | I10, J44.9, Z79.4
```

**Business Impact:** Normalized 45K+ patient encounters containing 3.8 diagnosis codes on average into 171K individual diagnosis records, identified most common comorbidities (Hypertension + Diabetes: 22% of patients), calculated patient complexity scores for care management prioritization (2,340 high-complexity patients with 10+ diagnoses), and enabled accurate ICD-10 based billing and clinical analytics.

---

### Example 4: Marketing Attribution Chain Parsing
**Business Context:** Digital marketing team analyzing multi-touch attribution chains to understand customer journey.

```sql
-- Step 1: Unpack marketing touchpoint sequences
CREATE TABLE customer_touchpoints AS (
    SELECT * FROM UNPACK (
        ON conversion_events
        USING
        TextColumn('attribution_chain')  -- "organic>email>paid_search>direct"
        Delimiter('>')
        OutputColumn('touchpoint_channel')
        Accumulate('conversion_id', 'customer_id', 'conversion_date', 'conversion_value', 'days_to_conversion')
    ) AS dt
) WITH DATA;

-- Step 2: Channel performance by position in journey
SELECT
    token_count as touchpoint_position,
    touchpoint_channel,
    COUNT(DISTINCT customer_id) as customer_count,
    COUNT(DISTINCT conversion_id) as conversion_count,
    SUM(conversion_value) as total_revenue,
    AVG(conversion_value) as avg_conversion_value,
    AVG(days_to_conversion) as avg_days_to_conversion
FROM customer_touchpoints
GROUP BY token_count, touchpoint_channel
ORDER BY token_count, conversion_count DESC;

-- Step 3: Most common customer journey paths
SELECT
    journey_path,
    journey_length,
    COUNT(*) as conversion_count,
    SUM(conversion_value) as total_revenue,
    AVG(conversion_value) as avg_order_value,
    AVG(days_to_conversion) as avg_days,
    CAST(COUNT(*) AS FLOAT) /
        (SELECT COUNT(*) FROM conversion_events) * 100 as pct_of_conversions
FROM (
    SELECT
        conversion_id,
        customer_id,
        conversion_value,
        days_to_conversion,
        STRING_AGG(touchpoint_channel, ' > ' ORDER BY token_count) as journey_path,
        MAX(token_count) as journey_length
    FROM customer_touchpoints
    GROUP BY conversion_id, customer_id, conversion_value, days_to_conversion
) subq
GROUP BY journey_path, journey_length
HAVING COUNT(*) >= 10
ORDER BY conversion_count DESC;

-- Step 4: Channel effectiveness - first vs. last touch analysis
SELECT
    channel,
    SUM(first_touch_conversions) as first_touch_conversions,
    SUM(last_touch_conversions) as last_touch_conversions,
    SUM(any_touch_conversions) as any_touch_conversions,
    AVG(first_touch_revenue) as avg_first_touch_revenue,
    AVG(last_touch_revenue) as avg_last_touch_revenue,
    CAST(SUM(first_touch_conversions) AS FLOAT) / SUM(any_touch_conversions) * 100 as pct_as_first_touch,
    CAST(SUM(last_touch_conversions) AS FLOAT) / SUM(any_touch_conversions) * 100 as pct_as_last_touch
FROM (
    SELECT
        touchpoint_channel as channel,
        CASE WHEN token_count = 1 THEN 1 ELSE 0 END as first_touch_conversions,
        CASE WHEN token_count = max_token THEN 1 ELSE 0 END as last_touch_conversions,
        1 as any_touch_conversions,
        CASE WHEN token_count = 1 THEN conversion_value END as first_touch_revenue,
        CASE WHEN token_count = max_token THEN conversion_value END as last_touch_revenue
    FROM (
        SELECT
            ct.*,
            MAX(token_count) OVER (PARTITION BY conversion_id) as max_token
        FROM customer_touchpoints ct
    ) subq
) subq2
GROUP BY channel
ORDER BY any_touch_conversions DESC;
```

**Sample Output:**
```
touchpoint_position | touchpoint_channel | customer_count | conversion_count | total_revenue | avg_conversion_value | avg_days_to_conversion
--------------------|-------------------|----------------|------------------|---------------|----------------------|------------------------
                  1 | organic           |          8,934 |            8,934 |   1,234,567.00|               138.21 |                   12.34
                  1 | paid_search       |          5,678 |            5,678 |     987,654.00|               173.91 |                    8.90
                  1 | social            |          3,456 |            3,456 |     543,210.00|               157.18 |                   15.67
                  2 | email             |          6,789 |            6,789 |   1,098,765.00|               161.84 |                   10.45
                  2 | direct            |          4,567 |            4,567 |     789,012.00|               172.75 |                    7.23
                  3 | paid_search       |          3,890 |            3,890 |     678,901.00|               174.52 |                    5.67

journey_path                        | journey_length | conversion_count | total_revenue | avg_order_value | avg_days | pct_of_conversions
------------------------------------|----------------|------------------|---------------|-----------------|----------|-------------------
organic > email > direct            |              3 |            2,345 |    456,789.00 |          194.75 |     8.90 |               8.90
paid_search > email > direct        |              3 |            1,890 |    389,012.00 |          205.84 |     6.45 |               7.17
social > email > paid_search > direct |            4 |            1,234 |    278,901.00 |          226.05 |    12.34 |               4.68
organic > direct                    |              2 |              987 |    189,234.00 |          191.71 |     5.67 |               3.74

channel      | first_touch_conversions | last_touch_conversions | any_touch_conversions | avg_first_touch_revenue | avg_last_touch_revenue | pct_as_first_touch | pct_as_last_touch
-------------|------------------------|------------------------|----------------------|-------------------------|------------------------|--------------------|-----------------
organic      |                  8,934 |                  1,234 |                15,678 |                  138.21 |                 165.43 |              56.97 |              7.87
email        |                  2,345 |                  3,456 |                12,890 |                  145.67 |                 178.90 |              18.19 |             26.81
paid_search  |                  5,678 |                  6,789 |                16,234 |                  173.91 |                 189.45 |              34.98 |             41.82
direct       |                  1,234 |                  9,876 |                14,567 |                  156.78 |                 198.23 |               8.47 |             67.79
social       |                  3,456 |                    890 |                 8,901 |                  157.18 |                 167.89 |              38.82 |             10.00
```

**Business Impact:** Unpacked 23,456 conversion attribution chains into 67,890 individual touchpoints, identified organic as dominant first-touch channel (57% of first touches), found direct as strongest last-touch channel (68%), discovered most effective 3-4 touch journeys (organic > email > direct: 8.9% of conversions, $195 AOV), and calculated multi-touch attribution weights for marketing budget optimization.

---

### Example 5: Email Recipient List Expansion for Campaign Analysis
**Business Context:** Email marketing platform analyzing recipient lists and engagement patterns.

```sql
-- Step 1: Unpack recipient email lists
CREATE TABLE email_recipients AS (
    SELECT * FROM UNPACK (
        ON email_campaigns
        USING
        TextColumn('recipient_list')  -- "user1@example.com,user2@example.com,user3@example.com"
        Delimiter(',')
        OutputColumn('recipient_email')
        Accumulate('campaign_id', 'campaign_name', 'send_date', 'subject_line', 'campaign_type', 'sender_name')
    ) AS dt
) WITH DATA;

-- Step 2: Join with engagement data and calculate metrics
CREATE TABLE email_performance AS (
    SELECT
        er.*,
        ee.opened,
        ee.clicked,
        ee.converted,
        ee.bounced,
        ee.unsubscribed,
        ee.open_timestamp,
        ee.click_timestamp
    FROM email_recipients er
    LEFT JOIN email_engagement ee
        ON er.campaign_id = ee.campaign_id
        AND er.recipient_email = ee.email_address
) WITH DATA;

-- Step 3: Campaign performance summary
SELECT
    campaign_id,
    campaign_name,
    campaign_type,
    send_date,
    COUNT(DISTINCT recipient_email) as recipients,
    SUM(CASE WHEN opened = 1 THEN 1 ELSE 0 END) as opens,
    SUM(CASE WHEN clicked = 1 THEN 1 ELSE 0 END) as clicks,
    SUM(CASE WHEN converted = 1 THEN 1 ELSE 0 END) as conversions,
    SUM(CASE WHEN bounced = 1 THEN 1 ELSE 0 END) as bounces,
    SUM(CASE WHEN unsubscribed = 1 THEN 1 ELSE 0 END) as unsubscribes,
    CAST(SUM(CASE WHEN opened = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(DISTINCT recipient_email) * 100 as open_rate,
    CAST(SUM(CASE WHEN clicked = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(DISTINCT recipient_email) * 100 as click_rate,
    CAST(SUM(CASE WHEN converted = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(DISTINCT recipient_email) * 100 as conversion_rate
FROM email_performance
GROUP BY campaign_id, campaign_name, campaign_type, send_date
ORDER BY send_date DESC, open_rate DESC;

-- Step 4: Recipient-level engagement analysis
SELECT
    recipient_email,
    COUNT(DISTINCT campaign_id) as campaigns_received,
    SUM(CASE WHEN opened = 1 THEN 1 ELSE 0 END) as total_opens,
    SUM(CASE WHEN clicked = 1 THEN 1 ELSE 0 END) as total_clicks,
    SUM(CASE WHEN converted = 1 THEN 1 ELSE 0 END) as total_conversions,
    CAST(SUM(CASE WHEN opened = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(DISTINCT campaign_id) * 100 as personal_open_rate,
    CAST(SUM(CASE WHEN clicked = 1 THEN 1 ELSE 0 END) AS FLOAT) / NULLIF(SUM(CASE WHEN opened = 1 THEN 1 ELSE 0 END), 0) * 100 as click_through_rate,
    CASE
        WHEN SUM(CASE WHEN opened = 1 THEN 1 ELSE 0 END) >= 10 AND
             CAST(SUM(CASE WHEN opened = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(DISTINCT campaign_id) >= 0.5
        THEN 'HIGHLY_ENGAGED'
        WHEN SUM(CASE WHEN opened = 1 THEN 1 ELSE 0 END) >= 5
        THEN 'MODERATELY_ENGAGED'
        WHEN SUM(CASE WHEN opened = 1 THEN 1 ELSE 0 END) >= 1
        THEN 'LOW_ENGAGEMENT'
        ELSE 'NOT_ENGAGED'
    END as engagement_category
FROM email_performance
GROUP BY recipient_email
HAVING COUNT(DISTINCT campaign_id) >= 3
ORDER BY personal_open_rate DESC, campaigns_received DESC;

-- Step 5: Campaign type effectiveness
SELECT
    campaign_type,
    COUNT(DISTINCT campaign_id) as campaign_count,
    AVG(recipient_count) as avg_recipients_per_campaign,
    AVG(open_rate) as avg_open_rate,
    AVG(click_rate) as avg_click_rate,
    AVG(conversion_rate) as avg_conversion_rate,
    SUM(total_conversions) as total_conversions
FROM (
    SELECT
        campaign_id,
        campaign_type,
        COUNT(DISTINCT recipient_email) as recipient_count,
        CAST(SUM(CASE WHEN opened = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(DISTINCT recipient_email) * 100 as open_rate,
        CAST(SUM(CASE WHEN clicked = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(DISTINCT recipient_email) * 100 as click_rate,
        CAST(SUM(CASE WHEN converted = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(DISTINCT recipient_email) * 100 as conversion_rate,
        SUM(CASE WHEN converted = 1 THEN 1 ELSE 0 END) as total_conversions
    FROM email_performance
    GROUP BY campaign_id, campaign_type
) subq
GROUP BY campaign_type
ORDER BY avg_open_rate DESC, avg_click_rate DESC;
```

**Sample Output:**
```
campaign_id | campaign_name          | campaign_type | send_date  | recipients | opens | clicks | conversions | bounces | unsubscribes | open_rate | click_rate | conversion_rate
------------|------------------------|---------------|------------|------------|-------|--------|-------------|---------|--------------|-----------|------------|----------------
CAMP-1001   | Spring Sale Promo      | Promotional   | 2024-03-15 |     25,678 | 8,934 |  2,345 |         456 |     234 |           23 |     34.80 |       9.13 |            1.78
CAMP-1002   | Weekly Newsletter      | Newsletter    | 2024-03-14 |     45,890 |12,345 |  3,456 |         234 |     456 |           34 |     26.90 |       7.53 |            0.51
CAMP-1003   | Product Launch         | Announcement  | 2024-03-13 |     18,234 | 7,890 |  1,890 |         345 |     123 |           12 |     43.27 |      10.36 |            1.89
CAMP-1004   | Abandoned Cart         | Transactional | 2024-03-12 |      3,456 | 1,678 |    890 |         234 |      34 |            2 |     48.55 |      25.75 |            6.77

recipient_email          | campaigns_received | total_opens | total_clicks | total_conversions | personal_open_rate | click_through_rate | engagement_category
-------------------------|--------------------| ------------|--------------|-------------------|--------------------|--------------------|--------------------
user123@example.com      |                 25 |          23 |           15 |                 5 |              92.00 |              65.22 | HIGHLY_ENGAGED
user456@example.com      |                 22 |          18 |           12 |                 3 |              81.82 |              66.67 | HIGHLY_ENGAGED
user789@example.com      |                 28 |          15 |            8 |                 2 |              53.57 |              53.33 | HIGHLY_ENGAGED
user234@example.com      |                 15 |           8 |            4 |                 1 |              53.33 |              50.00 | MODERATELY_ENGAGED
user567@example.com      |                 20 |           4 |            1 |                 0 |              20.00 |              25.00 | LOW_ENGAGEMENT

campaign_type  | campaign_count | avg_recipients_per_campaign | avg_open_rate | avg_click_rate | avg_conversion_rate | total_conversions
---------------|----------------|-----------------------------|---------------|----------------|---------------------|------------------
Transactional  |             12 |                       4,567 |         45.67 |          23.45 |                5.67 |             1,234
Announcement   |              8 |                      18,456 |         38.90 |          12.34 |                2.34 |               890
Promotional    |             15 |                      23,456 |         32.45 |          10.23 |                1.89 |               678
Newsletter     |             24 |                      42,345 |         25.67 |           7.89 |                0.67 |               456
```

**Business Impact:** Unpacked 59 email campaigns containing 895K recipient entries into normalized recipient table, enabled recipient-level engagement tracking identifying 12K highly-engaged subscribers (90%+ open rate), calculated campaign performance metrics showing transactional emails perform best (46% open rate, 6% conversion rate vs. newsletter 26% open rate, 0.5% conversion), and segmented recipients by engagement for targeted re-engagement campaigns.

---

### Example 6: Product Variant SKU Expansion
**Business Context:** Retail company normalizing product variant data (colors, sizes) stored as delimited strings.

```sql
-- Step 1: Unpack product color options
CREATE TABLE product_colors AS (
    SELECT * FROM UNPACK (
        ON product_master
        USING
        TextColumn('available_colors')  -- "Red,Blue,Green,Black,White"
        Delimiter(',')
        OutputColumn('color')
        Accumulate('product_id', 'product_name', 'base_price', 'category')
    ) AS dt
) WITH DATA;

-- Step 2: Unpack product size options
CREATE TABLE product_sizes AS (
    SELECT * FROM UNPACK (
        ON product_master
        USING
        TextColumn('available_sizes')  -- "XS,S,M,L,XL,XXL"
        Delimiter(',')
        OutputColumn('size')
        Accumulate('product_id', 'product_name', 'base_price', 'category')
    ) AS dt
) WITH DATA;

-- Step 3: Generate all product variants (color × size combinations)
CREATE TABLE product_variants AS (
    SELECT
        c.product_id,
        c.product_name,
        c.category,
        c.color,
        s.size,
        c.product_id || '-' || c.color || '-' || s.size as variant_sku,
        c.base_price as variant_price,
        'AVAILABLE' as variant_status
    FROM product_colors c
    INNER JOIN product_sizes s
        ON c.product_id = s.product_id
) WITH DATA;

-- Step 4: Variant availability and inventory summary
SELECT
    category,
    COUNT(DISTINCT product_id) as product_count,
    COUNT(*) as total_variants,
    AVG(variants_per_product) as avg_variants_per_product,
    SUM(variant_price) as total_inventory_value
FROM (
    SELECT
        product_id,
        category,
        COUNT(*) as variants_per_product,
        AVG(variant_price) as avg_variant_price,
        SUM(variant_price) as variant_price
    FROM product_variants
    GROUP BY product_id, category
) subq
GROUP BY category
ORDER BY total_variants DESC;

-- Step 5: Color and size popularity analysis
SELECT
    'COLOR' as dimension,
    color as value,
    COUNT(DISTINCT product_id) as product_count,
    COUNT(*) as variant_count,
    AVG(variant_price) as avg_price
FROM product_variants
GROUP BY color
UNION ALL
SELECT
    'SIZE' as dimension,
    size as value,
    COUNT(DISTINCT product_id) as product_count,
    COUNT(*) as variant_count,
    AVG(variant_price) as avg_price
FROM product_variants
GROUP BY size
ORDER BY dimension, variant_count DESC;

-- Step 6: Identify products with most variants
SELECT
    product_id,
    product_name,
    category,
    color_count,
    size_count,
    color_count * size_count as total_variants,
    color_list,
    size_list
FROM (
    SELECT
        product_id,
        product_name,
        category,
        COUNT(DISTINCT color) as color_count,
        COUNT(DISTINCT size) as size_count,
        STRING_AGG(DISTINCT color, ', ' ORDER BY color) as color_list,
        STRING_AGG(DISTINCT size, ', ' ORDER BY size) as size_list
    FROM product_variants
    GROUP BY product_id, product_name, category
) subq
ORDER BY total_variants DESC;
```

**Sample Output:**
```
category        | product_count | total_variants | avg_variants_per_product | total_inventory_value
----------------|---------------|----------------|--------------------------|---------------------
Apparel         |         1,234 |         45,678 |                    37.01 |          2,345,678.00
Footwear        |           890 |         23,456 |                    26.36 |          1,234,567.00
Accessories     |           567 |          8,901 |                    15.70 |            456,789.00
Home Goods      |           234 |          3,456 |                    14.77 |            234,567.00

dimension | value  | product_count | variant_count | avg_price
----------|--------|---------------|---------------|----------
COLOR     | Black  |         1,890 |        18,934 |     54.67
COLOR     | White  |         1,678 |        16,789 |     52.34
COLOR     | Blue   |         1,456 |        14,567 |     56.78
COLOR     | Red    |         1,234 |        12,345 |     58.90
COLOR     | Green  |           890 |         8,901 |     51.23
SIZE      | M      |         2,345 |        23,456 |     53.45
SIZE      | L      |         2,234 |        22,345 |     54.67
SIZE      | S      |         2,123 |        21,234 |     51.23
SIZE      | XL     |         1,890 |        18,901 |     56.78
SIZE      | XS     |         1,234 |        12,345 |     48.90
SIZE      | XXL    |           890 |         8,901 |     59.23

product_id | product_name            | category | color_count | size_count | total_variants | color_list                    | size_list
-----------|-------------------------|----------|-------------|------------|----------------|-------------------------------|------------------------
PROD-1234  | Premium Cotton T-Shirt  | Apparel  |          12 |          8 |             96 | Black,Blue,Green,Red,White,.. | XS,S,M,L,XL,XXL,3XL,4XL
PROD-2345  | Athletic Running Shoes  | Footwear |           8 |         10 |             80 | Black,Blue,Gray,Red,White,..  | 6,6.5,7,7.5,8,8.5,9,9.5,10,..
PROD-3456  | Hooded Sweatshirt       | Apparel  |           10|          6 |             60 | Black,Blue,Gray,Green,Navy,.. | XS,S,M,L,XL,XXL
```

**Business Impact:** Generated 81,491 product variants from 2,925 base products (avg 28 variants per product), identified Black and White as most common colors (19K and 17K variants respectively), found M and L as most common sizes (23K and 22K variants), discovered high-variant products (96 variants for Premium T-Shirt with 12 colors × 8 sizes), enabling complete e-commerce catalog with all size/color combinations for inventory planning and online merchandising.

---

## Common Use Cases

### By Industry

**E-commerce & Retail:**
- Product tag and category expansion
- Variant SKU generation (colors, sizes)
- Multi-value attribute normalization
- Customer interest list parsing
- Product bundle unpacking

**Healthcare:**
- Diagnosis code list expansion (ICD-10)
- Medication list parsing
- Procedure code normalization
- Patient allergy list unpacking
- Lab test panel expansion

**Financial Services:**
- Transaction category parsing
- Account holder list expansion
- Beneficiary designation unpacking
- Investment portfolio holding normalization
- Account permission list parsing

**Marketing & Advertising:**
- Attribution chain parsing
- Campaign recipient list expansion
- UTM parameter splitting
- Keyword list normalization
- Audience segment tag parsing

**Social Media & Content:**
- Hashtag list expansion
- Mention string parsing
- Topic category unpacking
- User interest tag normalization
- Emoji sequence parsing

**Telecommunications:**
- Service plan feature unpacking
- Device capability list parsing
- Network coverage area expansion
- Customer service tag normalization
- Call routing option parsing

### By Analytics Task

**Data Normalization:**
- Convert denormalized to normalized form
- Expand packed arrays into rows
- Parse delimited strings
- Create 1NF tables from multi-value fields

**ETL and Data Integration:**
- Parse flat file imports
- Split external system delimited data
- Normalize API response arrays
- Convert CSV field arrays to rows

**Text Analytics:**
- Parse tag lists for frequency analysis
- Expand multi-value fields for word clouds
- Normalize category assignments
- Split keyword lists for search

**Reporting & BI:**
- Expand multi-select filters
- Normalize dashboard dimensions
- Parse parameter strings
- Create detail rows from summaries

## Best Practices

### Delimiter Selection and Handling

**1. Choose Appropriate Delimiters:**
- **Comma ','**: Most common, but avoid if data contains commas
- **Pipe '|'**: Good alternative when commas appear in data
- **Semicolon ';'**: Common in medical codes (ICD-10)
- **Tab '\\t'**: Good for structured data exports
- **Custom multi-character**: Use when single-char delimiters appear in data

**2. Handle Edge Cases:**
```sql
-- Trim whitespace around delimited values
SELECT
    product_id,
    TRIM(tag) as clean_tag
FROM UNPACK (
    ON (SELECT product_id, REPLACE(REPLACE(product_tags, ', ', ','), ' ,', ',') as product_tags FROM products)
    USING
    TextColumn('product_tags')
    Delimiter(',')
    OutputColumn('tag')
    Accumulate('product_id')
) AS dt
WHERE TRIM(tag) != '';  -- Filter empty values
```

**3. Validate Delimiter Consistency:**
```sql
-- Check for delimiter consistency before unpacking
SELECT
    COUNT(*) as total_records,
    AVG(LENGTH(column_name) - LENGTH(REPLACE(column_name, ',', ''))) as avg_delimiter_count,
    MIN(LENGTH(column_name) - LENGTH(REPLACE(column_name, ',', ''))) as min_delimiters,
    MAX(LENGTH(column_name) - LENGTH(REPLACE(column_name, ',', ''))) as max_delimiters
FROM source_table
WHERE column_name IS NOT NULL;
```

### Performance Optimization

**1. Filter Before Unpacking:**
```sql
-- Good: Filter first, then unpack
SELECT * FROM UNPACK (
    ON (SELECT * FROM large_table WHERE load_date >= CURRENT_DATE - 7 AND status = 'ACTIVE')
    USING
    TextColumn('delimited_column')
    Delimiter(',')
    Accumulate('id', 'date')
) AS dt;

-- Avoid: Unpack all rows, then filter
SELECT * FROM UNPACK (
    ON large_table  -- Processes all rows
    USING TextColumn('delimited_column') Delimiter(',')
    Accumulate('id', 'date', 'load_date', 'status')
) AS dt
WHERE load_date >= CURRENT_DATE - 7 AND status = 'ACTIVE';
```

**2. Minimize Accumulated Columns:**
- Only accumulate columns needed for downstream analysis
- Avoid accumulating large TEXT/CLOB columns
- Consider separate lookups for metadata

**3. Index Appropriately:**
- Create primary index on accumulated identifier columns
- Index token_count for position-based queries
- Add secondary indexes on unpacked value column for filtering

**4. Batch Processing:**
- Process large datasets in date/ID range batches
- Monitor resource usage and adjust batch sizes
- Consider parallel processing for independent batches

### Data Quality and Validation

**1. Pre-Unpack Validation:**
```sql
-- Identify records with potential issues
SELECT
    id,
    delimited_column,
    LENGTH(delimited_column) as str_length,
    LENGTH(delimited_column) - LENGTH(REPLACE(delimited_column, ',', '')) + 1 as value_count,
    CASE
        WHEN delimited_column IS NULL THEN 'NULL_VALUE'
        WHEN TRIM(delimited_column) = '' THEN 'EMPTY_STRING'
        WHEN delimited_column LIKE '%,,%' THEN 'EMPTY_TOKEN'
        WHEN delimited_column LIKE ',%' OR delimited_column LIKE '%,' THEN 'LEADING_TRAILING_DELIMITER'
        ELSE 'OK'
    END as validation_status
FROM source_table
WHERE validation_status != 'OK';
```

**2. Post-Unpack Quality Checks:**
```sql
-- Validate unpacking results
SELECT
    'Total Input Rows' as metric,
    COUNT(DISTINCT id) as value
FROM source_table
UNION ALL
SELECT
    'Total Output Rows' as metric,
    COUNT(*) as value
FROM unpacked_table
UNION ALL
SELECT
    'Avg Values Per Input Row' as metric,
    CAST(COUNT(*) AS FLOAT) / COUNT(DISTINCT id) as value
FROM unpacked_table;
```

**3. Handle Empty and NULL Values:**
```sql
-- Filter empty tokens and NULLs
CREATE TABLE cleaned_unpacked AS (
    SELECT *
    FROM unpacked_table
    WHERE unpacked_value IS NOT NULL
      AND TRIM(unpacked_value) != ''
      AND TRIM(unpacked_value) != 'NULL'  -- String literal "NULL"
) WITH DATA;
```

**4. Validate Token Counts:**
```sql
-- Ensure token counts match expectations
SELECT
    id,
    original_value_count,
    actual_token_count,
    CASE
        WHEN original_value_count = actual_token_count THEN 'OK'
        ELSE 'MISMATCH'
    END as validation
FROM (
    SELECT
        id,
        LENGTH(original_column) - LENGTH(REPLACE(original_column, ',', '')) + 1 as original_value_count,
        MAX(token_count) as actual_token_count
    FROM unpacked_table
    GROUP BY id, original_column
) subq
WHERE validation = 'MISMATCH';
```

### Production Implementation

**1. Build Robust Pipelines:**
```sql
-- Complete unpacking pipeline with quality checks
-- Step 1: Validate source data
CREATE VOLATILE TABLE source_validated AS (
    SELECT *,
        LENGTH(delimited_column) - LENGTH(REPLACE(delimited_column, ',', '')) + 1 as expected_count
    FROM source_table
    WHERE delimited_column IS NOT NULL
      AND TRIM(delimited_column) != ''
) WITH DATA;

-- Step 2: Unpack data
CREATE TABLE data_unpacked AS (
    SELECT * FROM UNPACK (
        ON source_validated
        USING
        TextColumn('delimited_column')
        Delimiter(',')
        OutputColumn('unpacked_value')
        Accumulate('id', 'name', 'date', 'expected_count')
    ) AS dt
) WITH DATA;

-- Step 3: Quality validation
CREATE TABLE quality_report AS (
    SELECT
        id,
        expected_count,
        MAX(token_count) as actual_count,
        CASE WHEN expected_count = MAX(token_count) THEN 'PASS' ELSE 'FAIL' END as validation
    FROM data_unpacked
    GROUP BY id, expected_count
) WITH DATA;

-- Step 4: Cleaned output (only validated records)
CREATE TABLE data_unpacked_clean AS (
    SELECT du.*
    FROM data_unpacked du
    INNER JOIN quality_report qr
        ON du.id = qr.id AND qr.validation = 'PASS'
    WHERE TRIM(unpacked_value) != ''
) WITH DATA;
```

**2. Monitor and Log:**
- Track unpacking rates and row expansion factors
- Log validation failures for investigation
- Monitor query performance and resource usage
- Alert on unexpected changes in output volumes

**3. Handle Special Characters:**
```sql
-- Escape special characters in data before unpacking
CREATE TABLE preprocessed_data AS (
    SELECT
        id,
        REPLACE(REPLACE(delimited_column, '\,', '##COMMA##'), ',', '|') as delimited_column
    FROM source_table
) WITH DATA;

-- Unpack with pipe delimiter
CREATE TABLE unpacked AS (
    SELECT
        id,
        REPLACE(unpacked_value, '##COMMA##', ',') as cleaned_value
    FROM UNPACK (
        ON preprocessed_data
        USING TextColumn('delimited_column') Delimiter('|')
        OutputColumn('unpacked_value')
        Accumulate('id')
    ) AS dt
) WITH DATA;
```

**4. Version Control:**
- Document delimiter choices and rationale
- Maintain transformation logic history
- Version output tables with metadata
- Enable reproducibility with timestamps

## Related Functions

### Data Transformation
- **PACK**: Inverse operation - combines multiple rows into delimited string
- **STRING_AGG**: Aggregates values into delimited string
- **STRTOK**: Extracts specific token from delimited string
- **REGEXP_SPLIT_TO_TABLE**: Split strings using regex patterns

### String Functions
- **SUBSTR**: Extract substring by position
- **REPLACE**: Replace delimiter characters
- **TRIM**: Remove leading/trailing whitespace
- **LENGTH**: Calculate string lengths for validation

### Data Cleaning
- **TD_SimpleImputeFit / TD_SimpleImputeTransform**: Handle missing values
- **TD_OutlierFilterFit / TD_OutlierFilterTransform**: Handle outliers
- **TD_StringSimilarity**: Find similar string values

### Analysis Functions
- **COUNT**: Aggregate unpacked values
- **STRING_AGG**: Re-aggregate unpacked values
- **ROW_NUMBER**: Generate sequence numbers
- **RANK**: Rank unpacked values

## Notes and Limitations

### Important Considerations

**1. Output Row Explosion:**
- One input row can generate many output rows (1:N cardinality)
- Monitor output table sizes carefully
- Consider impact on downstream queries and joins
- Use filtering to limit unnecessary expansion

**2. Delimiter Handling:**
- Delimiter must not appear within actual data values
- Leading/trailing delimiters may create empty tokens
- Consecutive delimiters create empty values between them
- Consider escaping or encoding delimiters in source data

**3. NULL and Empty String Behavior:**
- NULL input values produce no output rows
- Empty string input may produce one empty string token
- Empty tokens (consecutive delimiters) create empty string values
- Filter empty values in post-processing if not desired

**4. Performance Impact:**
- Large row expansion significantly increases data volume
- Unpacking very long delimited strings is resource-intensive
- Consider sampling or batching for very large datasets
- Monitor spool space usage during unpacking

**5. Data Type Constraints:**
- Input column must be VARCHAR or CHAR
- Output column is always VARCHAR
- Type conversion needed if unpacked values are numeric
- Preserve original data types in accumulated columns

**6. Token Position:**
- token_count is 1-indexed (first value = 1)
- Useful for identifying first/last values in list
- Can be used for filtering or ordering
- Does not indicate original string position (character offset)

### Technical Constraints

**1. Delimiter Specifications:**
- Delimiter is case-sensitive
- Multi-character delimiters supported
- Cannot use regex patterns in basic Delimiter parameter (use Regex parameter instead)
- Delimiter must be string literal, not column reference

**2. Output Column Naming:**
- OutputColumn parameter sets unpacked value column name
- Default name derived from input column if not specified
- Accumulated columns retain original names
- token_count column always named 'token_count'

**3. Error Handling:**
- IgnoreInvalid='true' skips malformed rows silently
- IgnoreInvalid='false' causes function to fail on errors
- No partial results - entire input row skipped on error
- Limited error detail in output (no error messages)

**4. Regex Pattern Limitations:**
- Regex parameter requires valid regular expression syntax
- Complex patterns may impact performance
- Pattern matching is case-sensitive by default
- Limited to POSIX regular expressions

### Best Practices Summary

1. **Validate source data** before unpacking (delimiter consistency, NULL handling)
2. **Choose appropriate delimiters** that don't appear in data values
3. **Filter before unpacking** to minimize unnecessary processing
4. **Accumulate only needed columns** to reduce output size
5. **Clean empty tokens** in post-processing
6. **Index appropriately** on accumulated identifiers and unpacked values
7. **Monitor output sizes** and implement row expansion limits if needed
8. **Document delimiter choices** and transformation logic
9. **Implement quality checks** before and after unpacking
10. **Batch large datasets** to manage resource usage

## Version Information

- **Teradata Vantage Version**: 17.20
- **Function Category**: Data Transformation
- **Documentation Generated**: November 2024
- **Common Aliases**: TD_Unpack, UNPACK
