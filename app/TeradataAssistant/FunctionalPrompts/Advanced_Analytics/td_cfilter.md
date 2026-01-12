# TD_CFilter

## Function Name
- **TD_CFilter**: Collaborative Filtering for Association Analysis - Identifies item co-occurrence patterns and likelihood of items being purchased together

## Description
TD_CFilter calculates several statistical measures of how likely each pair of items is to be purchased together. The function analyzes transactional data (such as market basket data) to discover associations between items based on their co-occurrence patterns within transactions or customer sessions.

A typical input for TD_CFilter is a set of sales transactions with a column of purchased items and a column that groups the purchased items together (such as transaction ID or customer ID). The function computes multiple association metrics including support, confidence, lift, and z-score to quantify the strength and significance of item relationships.

### Characteristics
- Identifies item pairs that frequently appear together in transactions
- Calculates multiple association metrics (score, support, confidence, lift, z-score)
- Supports partitioning to analyze associations within specific segments
- Handles large-scale transactional data efficiently
- Useful for market basket analysis and recommendation systems
- Provides both frequency-based and statistical significance measures

### Limitations
- Only analyzes pairwise associations (not 3+ item combinations)
- Requires UTF8 client character set for UNICODE data
- Does not support Pass Through Characters (PTCs)
- Does not support KanjiSJIS or Graphic data types
- MaxDistinctItems parameter limits scalability for very large item sets
- Z-score cannot be calculated if all co-occurrence counts are equal

## When to Use TD_CFilter

TD_CFilter is essential for discovering item associations and patterns in various business scenarios:

### Retail and E-Commerce
- **Market basket analysis**: Identify products frequently bought together
- **Product bundling**: Create bundles based on purchase patterns
- **Cross-selling recommendations**: Suggest complementary products
- **Store layout optimization**: Place related items near each other
- **Promotional strategies**: Bundle products with high lift values
- **Inventory management**: Stock complementary items together

### Recommendation Systems
- **Product recommendations**: "Customers who bought X also bought Y"
- **Content recommendations**: Articles, videos, or music that go together
- **Collaborative filtering**: User-item affinity based on co-occurrence
- **Next-best-offer**: Predict what customer will buy next
- **Personalization**: Tailor recommendations based on current basket

### Customer Behavior Analysis
- **Purchase pattern discovery**: Understand how customers shop
- **Customer segmentation**: Group customers by purchase patterns
- **Channel analysis**: Compare associations across different channels
- **Seasonal analysis**: Identify seasonal co-purchase patterns
- **Regional differences**: Compare associations across regions

### Healthcare and Clinical Research
- **Comorbidity analysis**: Diseases that frequently occur together
- **Treatment combinations**: Therapies commonly prescribed together
- **Medication interactions**: Drugs frequently prescribed concurrently
- **Diagnostic patterns**: Symptoms that appear together
- **Patient pathway analysis**: Common sequences of medical events

### Content and Media
- **Content bundling**: Movies, songs, or articles consumed together
- **Genre associations**: Content categories with high affinity
- **Playlist generation**: Songs that are listened to in sequence
- **Reading lists**: Books commonly read by same audience
- **Viewing patterns**: TV shows or videos watched together

## Syntax

```sql
TD_CFilter (
    ON { table | view | (query) } AS InputTable
    USING
    TargetColumn ('target_column')
    TransactionIDColumns ('transaction_id_column' [,...])
    [ PartitionColumns ('partition_column' [,...]) ]
    [ MaxDistinctItems (max_distinct_items) ]
)
```

**Note:** You can call this function from:
- The FROM clause of a SELECT statement
- As part of a CREATE TABLE statement
- As part of a CREATE VIEW statement

## Required Elements

### ON Clause
Accepts the InputTable clause. Specifies the table containing transactional or co-occurrence data.

### TargetColumn
**Required**: Specify the name of the InputTable column that contains the data to filter (the items).
- **Data Type**: CHAR or VARCHAR
- **Description**: Column containing item names, product IDs, SKUs, or other identifiers
- **Constraint**: Maximum 1 column allowed
- **Examples**: product_name, item_id, sku, category, content_id

### TransactionIDColumns
**Required**: Specify the names of InputTable columns that contain the transaction ID which groups items purchased together.
- **Data Type**: Any data type allowed by PARTITION BY clause
- **Description**: One or more columns that identify transactions, baskets, or sessions
- **Constraint**: Maximum 2047 columns allowed
- **Examples**:
  - Single column: transaction_id, order_id, session_id, customer_id
  - Multiple columns: customer_id, purchase_date (for analyzing by customer)
  - Hierarchical: store_id, date, transaction_id

## Optional Elements

### PartitionColumns
Specify the names of input columns to copy to the output table. The function partitions the input data and output table on these columns.
- **Default**: No partitioning (analyze all data together)
- **Data Type**: Any data type allowed by PARTITION BY clause
- **Constraint**: Maximum 10 columns allowed
- **Use Cases**:
  - **Store-level analysis**: Partition by store_id to find associations per store
  - **Regional analysis**: Partition by region to compare association patterns
  - **Temporal analysis**: Partition by time period (month, quarter, year)
  - **Customer segment**: Partition by customer_segment to find segment-specific patterns

**Important**: PartitionColumns makes TD_CFilter output nondeterministic unless each partition_column is unique in the group defined by TransactionIDColumns.

### MaxDistinctItems
Specify the maximum size of the item set (maximum number of distinct items to analyze).
- **Default**: 100
- **Data Type**: INTEGER
- **Constraint**: Must be positive
- **Performance Consideration**: Higher values allow analysis of more items but increase memory and computation requirements

## Input Schema

### Input Table Schema
The input table contains transactional data with one row per item per transaction.

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | CHAR/VARCHAR | Item identifier (product name, SKU, item ID, etc.) |
| transaction_id_column | ANY (allowed by PARTITION BY) | Transaction, order, or session identifier |
| partition_column | ANY (allowed by PARTITION BY) | Optional column(s) to partition analysis (store, region, period) |

**Data Structure Example**:
```
transaction_id | product_name
--------------+-------------
1001          | milk
1001          | bread
1001          | eggs
1002          | milk
1002          | butter
1002          | eggs
```

## Output Schema

### Output Table Schema
The output table contains one row for each significant item pair, with association metrics.

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| partition_column | ANY | Copied from input if PartitionColumns specified |
| TD_item1 | VARCHAR | Name of first item in the pair |
| TD_item2 | VARCHAR | Name of second item in the pair |
| cntb | INTEGER | Count of co-occurrence of both items in partition (both appear in same transaction) |
| cnt1 | INTEGER | Count of occurrence of item1 in partition (item1 appears in any transaction) |
| cnt2 | INTEGER | Count of occurrence of item2 in partition (item2 appears in any transaction) |
| score | REAL | Product of two conditional probabilities: P({item2\|item1}) × P({item1\|item2}) = (cntb × cntb) / (cnt1 × cnt2) |
| support | REAL | Percentage of transactions where both items co-occur: cntb / tran_cnt |
| confidence | REAL | Percentage of item1 transactions where item2 also occurs: cntb / cnt1 |
| lift | REAL | Ratio of observed to expected support if independent: (cntb/tran_cnt) / [(cnt1/tran_cnt) × (cnt2/tran_cnt)]<br/>• lift > 1: Positive association (items occur together more than expected)<br/>• lift = 1: No association (items are independent)<br/>• lift < 1: Negative association (items occur together less than expected) |
| z_score | REAL | Significance of co-occurrence assuming normal distribution: (cntb - mean(cntb)) / sd(cntb)<br/>• If all cntb values equal, sd(cntb) = 0 and z_score is not calculated |

## Code Examples

### Example 1: Basic Market Basket Analysis - Grocery Store

Analyze which grocery items are frequently purchased together:

```sql
-- Create grocery transaction data
CREATE TABLE grocery_transactions (
    transaction_id INTEGER,
    customer_id INTEGER,
    item_name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2),
    purchase_date DATE
);

-- Analyze item associations
CREATE TABLE grocery_associations AS (
    SELECT * FROM TD_CFilter(
        ON grocery_transactions AS InputTable
        USING
        TargetColumn('item_name')
        TransactionIDColumns('transaction_id')
        MaxDistinctItems(200)
    )
) WITH DATA;

-- View strongest associations (high lift and confidence)
SELECT
    TD_item1,
    TD_item2,
    cntb as co_purchases,
    ROUND(support, 3) as support_pct,
    ROUND(confidence, 3) as confidence_pct,
    ROUND(lift, 2) as lift_ratio,
    CASE
        WHEN lift > 2.0 THEN 'Very Strong'
        WHEN lift > 1.5 THEN 'Strong'
        WHEN lift > 1.2 THEN 'Moderate'
        WHEN lift > 1.0 THEN 'Weak'
        ELSE 'Negative'
    END as association_strength
FROM grocery_associations
WHERE confidence > 0.3  -- At least 30% of item1 purchases include item2
  AND lift > 1.0        -- Positive association only
ORDER BY lift DESC, confidence DESC
LIMIT 20;
```

**Business Application**:
- **Cross-sell**: Recommend item2 when customer adds item1 to cart
- **Bundling**: Create promotional bundles for strongly associated items
- **Store layout**: Place associated items near each other

### Example 2: Store-Level Association Analysis

Compare item associations across different stores:

```sql
-- Analyze associations by store
CREATE TABLE store_associations AS (
    SELECT * FROM TD_CFilter(
        ON grocery_transactions AS InputTable
        USING
        TargetColumn('item_name')
        TransactionIDColumns('transaction_id')
        PartitionColumns('store_id')
        MaxDistinctItems(150)
    )
) WITH DATA;

-- Find associations that vary significantly across stores
WITH store_comparison AS (
    SELECT
        TD_item1,
        TD_item2,
        store_id,
        lift,
        confidence,
        RANK() OVER (PARTITION BY TD_item1, TD_item2 ORDER BY lift DESC) as lift_rank
    FROM store_associations
    WHERE confidence > 0.2
)
SELECT
    TD_item1,
    TD_item2,
    MAX(CASE WHEN lift_rank = 1 THEN store_id END) as strongest_store,
    MAX(CASE WHEN lift_rank = 1 THEN lift END) as max_lift,
    MIN(lift) as min_lift,
    MAX(lift) - MIN(lift) as lift_variance,
    CASE
        WHEN MAX(lift) - MIN(lift) > 1.0 THEN 'High variance across stores'
        WHEN MAX(lift) - MIN(lift) > 0.5 THEN 'Moderate variance'
        ELSE 'Consistent across stores'
    END as geographic_pattern
FROM store_comparison
GROUP BY TD_item1, TD_item2
HAVING COUNT(DISTINCT store_id) >= 3  -- Present in at least 3 stores
  AND MAX(lift) - MIN(lift) > 0.5     -- Significant variance
ORDER BY lift_variance DESC;
```

**Strategic Insights**:
- Customize promotions by store based on local associations
- Identify regional preferences
- Optimize inventory mix by location

### Example 3: Product Recommendation System

Generate "Customers also bought" recommendations:

```sql
-- Create recommendations for specific product
CREATE TABLE product_recommendations AS (
    WITH associations AS (
        SELECT * FROM TD_CFilter(
            ON purchase_history AS InputTable
            USING
            TargetColumn('product_id')
            TransactionIDColumns('order_id')
            MaxDistinctItems(500)
        )
    ),
    -- Rank recommendations by multiple criteria
    ranked_recommendations AS (
        SELECT
            TD_item1 as source_product,
            TD_item2 as recommended_product,
            lift,
            confidence,
            support,
            z_score,
            -- Composite score: combine lift and confidence
            (lift * confidence) as recommendation_score,
            ROW_NUMBER() OVER (
                PARTITION BY TD_item1
                ORDER BY (lift * confidence) DESC, support DESC
            ) as recommendation_rank
        FROM associations
        WHERE lift > 1.0          -- Positive association only
          AND confidence > 0.1    -- Minimum 10% confidence
          AND support > 0.01      -- Appears in at least 1% of transactions
    )
    SELECT
        source_product,
        recommended_product,
        recommendation_rank,
        ROUND(lift, 2) as lift,
        ROUND(confidence, 3) as confidence_pct,
        ROUND(recommendation_score, 3) as score
    FROM ranked_recommendations
    WHERE recommendation_rank <= 10  -- Top 10 recommendations per product
) WITH DATA;

-- Use in application
SELECT
    recommended_product,
    lift,
    confidence_pct,
    CASE
        WHEN recommendation_rank = 1 THEN 'Most recommended'
        WHEN recommendation_rank <= 3 THEN 'Highly recommended'
        ELSE 'Also recommended'
    END as recommendation_tier
FROM product_recommendations
WHERE source_product = 'PRODUCT_XYZ'
ORDER BY recommendation_rank;
```

**E-Commerce Application**:
- Display recommendations on product pages
- Include in shopping cart suggestions
- Power email marketing campaigns

### Example 4: Seasonal Association Analysis

Compare associations across different time periods:

```sql
-- Analyze associations by season
CREATE TABLE seasonal_associations AS (
    WITH transactions_with_season AS (
        SELECT
            transaction_id,
            product_name,
            CASE
                WHEN EXTRACT(MONTH FROM purchase_date) IN (12, 1, 2) THEN 'Winter'
                WHEN EXTRACT(MONTH FROM purchase_date) IN (3, 4, 5) THEN 'Spring'
                WHEN EXTRACT(MONTH FROM purchase_date) IN (6, 7, 8) THEN 'Summer'
                ELSE 'Fall'
            END as season
        FROM retail_transactions
    )
    SELECT * FROM TD_CFilter(
        ON transactions_with_season AS InputTable
        USING
        TargetColumn('product_name')
        TransactionIDColumns('transaction_id')
        PartitionColumns('season')
        MaxDistinctItems(300)
    )
) WITH DATA;

-- Find seasonal-specific associations
WITH season_comparison AS (
    SELECT
        TD_item1,
        TD_item2,
        season,
        lift,
        confidence,
        CASE
            WHEN season = 'Winter' THEN lift
            ELSE NULL
        END as winter_lift,
        CASE
            WHEN season = 'Summer' THEN lift
            ELSE NULL
        END as summer_lift
    FROM seasonal_associations
    WHERE confidence > 0.2
)
SELECT
    TD_item1,
    TD_item2,
    MAX(winter_lift) as winter_lift,
    MAX(summer_lift) as summer_lift,
    ABS(COALESCE(MAX(winter_lift), 0) - COALESCE(MAX(summer_lift), 0)) as seasonal_variance,
    CASE
        WHEN MAX(winter_lift) > MAX(summer_lift) * 1.5 THEN 'Winter association'
        WHEN MAX(summer_lift) > MAX(winter_lift) * 1.5 THEN 'Summer association'
        ELSE 'Year-round association'
    END as seasonality_pattern
FROM season_comparison
GROUP BY TD_item1, TD_item2
HAVING MAX(winter_lift) IS NOT NULL
   AND MAX(summer_lift) IS NOT NULL
   AND ABS(COALESCE(MAX(winter_lift), 0) - COALESCE(MAX(summer_lift), 0)) > 0.5
ORDER BY seasonal_variance DESC;
```

**Merchandising Strategy**:
- Adjust promotions and bundles by season
- Plan inventory for seasonal co-purchase patterns
- Time cross-sell campaigns to seasonal demand

### Example 5: Negative Association Detection

Identify substitute products (items that don't sell together):

```sql
-- Find negative associations (substitutes)
CREATE TABLE product_substitutes AS (
    WITH all_associations AS (
        SELECT * FROM TD_CFilter(
            ON purchase_data AS InputTable
            USING
            TargetColumn('product_id')
            TransactionIDColumns('customer_id', 'purchase_date')
            MaxDistinctItems(400)
        )
    )
    SELECT
        TD_item1 as product_1,
        TD_item2 as product_2,
        cnt1 as product_1_purchases,
        cnt2 as product_2_purchases,
        cntb as co_purchases,
        ROUND(lift, 3) as lift_ratio,
        ROUND(support, 4) as support_pct,
        ROUND(confidence, 4) as confidence_pct,
        CASE
            WHEN lift < 0.5 THEN 'Strong substitute (rarely bought together)'
            WHEN lift < 0.8 THEN 'Moderate substitute'
            WHEN lift < 1.0 THEN 'Weak substitute'
            ELSE 'Not a substitute'
        END as substitution_pattern,
        -- Calculate expected co-purchases if independent
        ROUND((cnt1 * cnt2) / (SELECT COUNT(DISTINCT transaction_id) FROM purchase_data), 1)
            as expected_co_purchases
    FROM all_associations
    WHERE lift < 1.0  -- Negative association
      AND cnt1 >= 10  -- Each product has at least 10 purchases
      AND cnt2 >= 10
) WITH DATA;

-- Identify strongest substitutes within categories
SELECT
    p1.category,
    s.product_1,
    s.product_2,
    s.lift_ratio,
    s.product_1_purchases,
    s.product_2_purchases,
    s.co_purchases,
    s.expected_co_purchases,
    (s.expected_co_purchases - s.co_purchases) as purchase_displacement
FROM product_substitutes s
JOIN product_catalog p1 ON s.product_1 = p1.product_id
JOIN product_catalog p2 ON s.product_2 = p2.product_id
WHERE p1.category = p2.category  -- Same category
  AND s.lift_ratio < 0.7         -- Strong negative association
ORDER BY s.lift_ratio, purchase_displacement DESC
LIMIT 50;
```

**Business Decisions**:
- Understand competitive dynamics within categories
- Avoid bundling substitutes
- Price competing products strategically
- Optimize assortment to reduce cannibalization

### Example 6: Healthcare Comorbidity Analysis

Analyze diseases or conditions that commonly occur together:

```sql
-- Analyze disease co-occurrence
CREATE TABLE disease_comorbidity AS (
    SELECT * FROM TD_CFilter(
        ON patient_diagnoses AS InputTable
        USING
        TargetColumn('diagnosis_code')
        TransactionIDColumns('patient_id')
        MaxDistinctItems(500)
    )
) WITH DATA;

-- Identify significant comorbidities
WITH comorbidity_analysis AS (
    SELECT
        d1.diagnosis_name as primary_condition,
        d2.diagnosis_name as comorbid_condition,
        c.cntb as co_occurrence_count,
        c.cnt1 as primary_condition_patients,
        c.cnt2 as comorbid_condition_patients,
        ROUND(c.confidence, 3) as comorbidity_rate,
        ROUND(c.lift, 2) as lift_ratio,
        c.z_score,
        CASE
            WHEN c.z_score > 2.58 THEN 'Highly significant (p < 0.01)'
            WHEN c.z_score > 1.96 THEN 'Significant (p < 0.05)'
            WHEN c.z_score > 1.645 THEN 'Marginally significant (p < 0.10)'
            ELSE 'Not significant'
        END as statistical_significance
    FROM disease_comorbidity c
    JOIN diagnosis_lookup d1 ON c.TD_item1 = d1.diagnosis_code
    JOIN diagnosis_lookup d2 ON c.TD_item2 = d2.diagnosis_code
    WHERE c.confidence > 0.1  -- At least 10% comorbidity rate
      AND c.z_score > 1.96    -- Statistically significant
)
SELECT
    primary_condition,
    comorbid_condition,
    co_occurrence_count,
    comorbidity_rate,
    lift_ratio,
    statistical_significance,
    CASE
        WHEN lift_ratio > 3.0 THEN 'Very high comorbidity risk'
        WHEN lift_ratio > 2.0 THEN 'High comorbidity risk'
        WHEN lift_ratio > 1.5 THEN 'Moderate comorbidity risk'
        ELSE 'Elevated comorbidity risk'
    END as clinical_risk_level
FROM comorbidity_analysis
ORDER BY lift_ratio DESC, comorbidity_rate DESC
LIMIT 100;
```

**Clinical Applications**:
- Identify patients at risk for multiple conditions
- Develop screening protocols for comorbidities
- Inform treatment planning and care coordination
- Support population health management

## Common Use Cases

### 1. Dynamic Bundle Creation

```sql
-- Create product bundles based on associations
WITH top_associations AS (
    SELECT
        TD_item1 as anchor_product,
        TD_item2 as bundle_product,
        lift,
        confidence,
        ROW_NUMBER() OVER (PARTITION BY TD_item1 ORDER BY lift DESC) as rank
    FROM product_associations
    WHERE lift > 1.5 AND confidence > 0.25
)
SELECT
    anchor_product,
    STRING_AGG(bundle_product, ', ') as recommended_bundle,
    AVG(lift) as avg_bundle_lift
FROM top_associations
WHERE rank <= 3  -- 3-item bundles
GROUP BY anchor_product
HAVING COUNT(*) = 3;
```

### 2. Category Affinity Analysis

```sql
-- Analyze which product categories are purchased together
WITH category_transactions AS (
    SELECT
        t.transaction_id,
        p.category
    FROM transactions t
    JOIN products p ON t.product_id = p.product_id
)
SELECT * FROM TD_CFilter(
    ON category_transactions AS InputTable
    USING
    TargetColumn('category')
    TransactionIDColumns('transaction_id')
)
WHERE lift > 1.0
ORDER BY lift DESC;
```

### 3. Customer Segment Association Patterns

```sql
-- Compare associations across customer segments
CREATE TABLE segment_associations AS (
    WITH customer_transactions AS (
        SELECT
            t.transaction_id,
            t.product_name,
            c.customer_segment
        FROM transactions t
        JOIN customers c ON t.customer_id = c.customer_id
    )
    SELECT * FROM TD_CFilter(
        ON customer_transactions AS InputTable
        USING
        TargetColumn('product_name')
        TransactionIDColumns('transaction_id')
        PartitionColumns('customer_segment')
        MaxDistinctItems(250)
    )
) WITH DATA;

-- Find segment-specific associations
SELECT
    customer_segment,
    TD_item1,
    TD_item2,
    lift,
    confidence
FROM segment_associations
WHERE lift > 2.0
ORDER BY customer_segment, lift DESC;
```

## Best Practices

1. **Choose Appropriate Transaction ID**:
   - Use actual transaction/order ID for point-in-time purchases
   - Use customer_id for customer-level affinity analysis
   - Combine customer_id + date for repeat purchase patterns
   - Consider session_id for online behavior analysis

2. **Set Meaningful MaxDistinctItems**:
   - Balance between coverage and performance
   - Start with 100-200 for initial analysis
   - Increase to 500-1000 for comprehensive analysis
   - Monitor memory usage with larger values

3. **Use Partitioning Strategically**:
   - Partition by store, region, or channel to find local patterns
   - Partition by time period to track changing associations
   - Partition by customer segment for targeted insights
   - Be aware that partitioning affects output determinism

4. **Filter Results Appropriately**:
   - Set minimum thresholds for support (e.g., > 0.01 or 1%)
   - Set minimum confidence (e.g., > 0.1 or 10%)
   - Focus on lift > 1.0 for positive associations
   - Use z-score > 1.96 for statistical significance

5. **Interpret Metrics Holistically**:
   - **High lift, low support**: Strong but rare association
   - **Low lift, high support**: Common but not special
   - **High confidence**: Item2 almost always appears with item1
   - **High lift and confidence**: Best candidates for cross-sell

6. **Handle Cold Start Problem**:
   - New items won't have associations yet
   - Use category-level associations as fallback
   - Apply collaborative filtering at different levels
   - Consider content-based recommendations initially

7. **Validate Business Logic**:
   - Exclude unlikely pairs (e.g., competing products in same category)
   - Verify that associations make business sense
   - Test recommendations with real users
   - Monitor click-through and conversion rates

## Related Functions

- **TD_Attribution**: Assign credit to touchpoints leading to conversion
- **TD_nPath**: Pattern matching for sequential event analysis
- **TD_Sessionize**: Group clicks into sessions for behavioral analysis
- **TD_FrequentItemSets**: Find frequent item sets (3+ items)
- **TD_AssociationRules**: Generate association rules with configurable metrics

## Notes and Limitations

1. **Pairwise Analysis Only**:
   - TD_CFilter only analyzes pairs of items
   - For 3+ item associations, use TD_FrequentItemSets
   - Cannot capture complex multi-item patterns
   - Consider sequential analysis with nPath for order-dependent patterns

2. **Character Set Requirements**:
   - Requires UTF8 client character set for UNICODE data
   - Does not support Pass Through Characters (PTCs)
   - Does not support KanjiSJIS or Graphic data types
   - Ensure consistent encoding across input data

3. **Scalability Considerations**:
   - MaxDistinctItems limits number of unique items analyzed
   - Output size grows quadratically with number of items
   - Very high item counts may require significant memory
   - Consider pre-filtering to top-selling items

4. **Statistical Considerations**:
   - Z-score assumes normal distribution of co-occurrences
   - Cannot calculate z-score if all co-occurrence counts are equal
   - Low transaction counts reduce statistical reliability
   - Spurious correlations possible with rare items

5. **Partition Effects**:
   - PartitionColumns makes output nondeterministic unless partition columns are unique within transaction groups
   - Smaller partitions have less statistical power
   - Associations may not generalize across partitions
   - Consider partition size when interpreting results

6. **Directional Interpretation**:
   - TD_CFilter identifies associations, not causation
   - Confidence is directional (item1 → item2)
   - Both (item1, item2) and (item2, item1) appear in output
   - Lift is symmetric: lift(item1, item2) = lift(item2, item1)

7. **Performance Optimization**:
   - Pre-filter transactions to relevant time periods
   - Exclude very rare items (appear in < 5 transactions)
   - Use appropriate MaxDistinctItems value
   - Consider sampling for exploratory analysis

8. **Business Context Required**:
   - High lift doesn't always mean actionable insight
   - Consider profit margins when creating bundles
   - Account for inventory constraints
   - Validate with A/B testing before large-scale deployment

## Version Information

- **Function Version**: Based on Teradata Database Analytic Functions Version 17.20
- **Generated**: November 28, 2025
- **Category**: Path and Pattern Analysis / Association Analysis / Market Basket Analysis
