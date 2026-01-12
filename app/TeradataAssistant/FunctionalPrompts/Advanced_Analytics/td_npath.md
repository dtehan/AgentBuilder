# TD_nPath

## Function Name
- **TD_nPath**: Pattern Matching for Path Analysis - Finds complex patterns in sequential event data

## Description
TD_nPath scans a set of rows looking for patterns that you specify using a flexible pattern language. For each set of input rows that matches the pattern, nPath produces a single output row. The function provides powerful pattern-matching capabilities that let you specify complex patterns in sequences of events and define what values to output for each matched sequence.

TD_nPath is essential when your goal is to identify specific paths or patterns that lead to outcomes. Unlike simple aggregations or filtering, nPath can find complex sequential patterns like "home page followed by one or more product views, then checkout" or "three failed login attempts followed by successful login."

### Characteristics
- Powerful pattern matching with regular expression-like syntax
- Supports overlapping and non-overlapping pattern matches
- Flexible symbol definitions using SQL predicates
- Multiple aggregate functions for extracting insights from matched patterns
- Handles multiple input tables (including DIMENSION tables)
- LAG and LEAD expressions for comparing current row to previous/next rows
- Greedy pattern matching for longest available matches

### Limitations
- Pattern and symbol syntax does not support UNICODE characters
- ACCUMULATE function does not support UNICODE input/output data
- Does not support Pass Through Characters (PTCs)
- Does not support KanjiSJIS or Graphic data types
- ORDER BY clause supports only ASCII collation
- PARTITION BY assumes column names in Normalization Form C (NFC)
- Complex patterns require careful syntax construction
- Nondeterministic if input is nondeterministic

## When to Use TD_nPath

TD_nPath is essential for discovering sequential patterns and paths in event data:

### Website and App User Journey Analysis
- **Conversion paths**: Find sequences of pages that lead to purchases
- **Drop-off analysis**: Identify where users abandon in checkout flow
- **Feature adoption**: Track how users discover and adopt features
- **Navigation patterns**: Understand common browsing paths
- **Content engagement**: Find reading/viewing sequences

### Customer Behavior Analysis
- **Purchase patterns**: Identify sequences leading to repeat purchases
- **Churn indicators**: Find event patterns that precede customer churn
- **Upsell opportunities**: Detect patterns indicating readiness to upgrade
- **Cross-sell patterns**: Sequences indicating complementary needs
- **Loyalty progression**: Paths from new customer to loyal advocate

### Fraud and Security Detection
- **Attack patterns**: Identify sequences of suspicious activities
- **Login anomalies**: Detect unusual authentication patterns
- **Transaction fraud**: Find suspicious transaction sequences
- **Account takeover**: Patterns indicating compromised accounts
- **Bot detection**: Sequential patterns characteristic of automation

### Healthcare and Clinical
- **Patient pathways**: Clinical event sequences and outcomes
- **Treatment patterns**: Successful treatment progressions
- **Adverse events**: Sequences leading to complications
- **Diagnostic paths**: Common diagnostic workup sequences
- **Medication adherence**: Prescription fill and refill patterns

### Industrial and IoT
- **Equipment failure**: Sensor reading patterns before failures
- **Quality issues**: Process sequences leading to defects
- **Maintenance patterns**: Optimal maintenance timing sequences
- **Performance optimization**: Configurations yielding best results
- **Anomaly detection**: Unusual operational sequences

## Syntax

```sql
nPath (
    ON { table | view | (query) }
    PARTITION BY partition_column
    ORDER BY order_column [ ASC | DESC ] [...]
    [ ON { table | view | (query) }
      [ PARTITION BY partition_column | DIMENSION ]
      ORDER BY order_column [ ASC | DESC ]
    ] [...]
    USING
    Mode ({ OVERLAPPING | NONOVERLAPPING })
    Pattern ('pattern')
    Symbols ({ col_expr = symbol_predicate AS symbol } [,...])
    [ Filter (filter_expression [,...]) ]
    Result ({ aggregate_function (expression OF [ANY] symbol [,...]) AS alias } [,...])
)
```

**Note:** You can call this function from:
- The FROM clause of a SELECT statement
- As part of a CREATE TABLE statement
- As part of a CREATE VIEW statement

## Required Syntax Elements

### ON Clause
Specifies input tables. Requires at least one partitioned input table. Can have additional input tables that are partitioned or DIMENSION tables.

**Important**: If input table has CLOB columns, it cannot be a DIMENSION table.

### PARTITION BY
Specifies how to partition input data. Each partition typically represents one entity (user, customer, device, session).

### ORDER BY
Specifies order of rows within each partition. Critical for pattern matching as patterns are matched in this order.

### Mode
Specify the pattern-matching mode:

| Mode | Description |
|------|-------------|
| **OVERLAPPING** | Find every occurrence of pattern, even if part of previous match. One row can match multiple symbols in a pattern. |
| **NONOVERLAPPING** | Start next pattern search at row following last match. Each row matched at most once. |

**Example**: Pattern 'A.A' on sequence [A, A, A, A]
- OVERLAPPING: Finds 3 matches: (A₁,A₂), (A₂,A₃), (A₃,A₄)
- NONOVERLAPPING: Finds 2 matches: (A₁,A₂), (A₃,A₄)

### Pattern
Specify the pattern for which the function searches. Composed using symbols (defined in Symbols element), operators, and parentheses.

**Pattern Operators** (in order of precedence):

| Operator | Description | Example |
|----------|-------------|---------|
| A | Matches one row satisfying symbol A | 'A' |
| A? | Matches 0 or 1 rows satisfying A | 'A?' |
| A* | Matches 0 or more rows satisfying A (greedy) | 'A*' |
| A+ | Matches 1 or more rows satisfying A (greedy) | 'A+' |
| A.B | A followed by B | 'A.B' |
| A\|B | Either A or B | 'A\|B' |
| ^A | Pattern must start with A | '^A.B*' |
| A$ | Pattern must end with A | 'B*.A$' |
| (X){n} | Exactly n occurrences of pattern X | '(A.B){3}' |
| (X){n,} | At least n occurrences | '(A.B){2,}' |
| (X){n,m} | Between n and m occurrences | '(A.B){2,5}' |

**Pattern Examples**:
- `'A.B.C'` - Exactly A, then B, then C
- `'A+.B*.C'` - One or more A's, followed by zero or more B's, then C
- `'^H.(B|C)+.D?.X*.A$'` - Starts with H, has one or more B or C, optional D, any number of X, ends with A
- `'(A.B){2,4}'` - The sequence A followed by B, repeated 2 to 4 times

### Symbols
Defines symbols used in Pattern and Result elements. Each symbol represents rows matching a specific condition.

**Syntax**: `col_expr = symbol_predicate AS symbol`

**Symbol Naming**:
- Can be any valid identifier
- Case-insensitive (A and a are same symbol)
- Typically 1-2 uppercase letters for readability
- TRUE AS X matches all rows

**Examples**:
```sql
Symbols (
    pagetype = 'home' AS H,
    pagetype = 'checkout' AS CO,
    pagetype <> 'home' AND pagetype <> 'checkout' AS PP,
    productprice > 100 AS EXPENSIVE,
    TRUE AS ANY_ROW
)
```

**NULL Handling**: Rows with NULL values in symbol predicates do not match any symbol.

### Result
Defines output columns using aggregate functions applied to matched rows.

**Aggregate Functions**:

| Function | Description |
|----------|-------------|
| COUNT(* OF symbol_list) | Count of matched rows |
| COUNT(col_expr OF symbol_list) | Count of non-NULL col_expr values |
| FIRST(col_expr OF symbol_list) | Value from first matched row |
| LAST(col_expr OF symbol_list) | Value from last matched row |
| NTH(col_expr, n OF symbol_list) | Value from nth matched row (n>0: from start, n<0: from end) |
| FIRST_NOTNULL(col_expr OF symbol_list) | First non-NULL value |
| LAST_NOTNULL(col_expr OF symbol_list) | Last non-NULL value |
| MAX_CHOOSE(quantify_col, describe_col OF symbol_list) | describe_col value from row with max quantify_col |
| MIN_CHOOSE(quantify_col, describe_col OF symbol_list) | describe_col value from row with min quantify_col |
| DUPCOUNT(col_expr OF symbol_list) | Duplicate count for current value |
| DUPCOUNTCUM(col_expr OF symbol_list) | Cumulative duplicate count |
| ACCUMULATE(col_expr OF symbol_list DELIMITER 'delim') | Concatenated values with delimiter |

**Symbol Lists**:
- Single symbol: `OF A`
- Multiple symbols: `OF ANY(A, B, C)`
- ANY keyword allows combining multiple symbols

## Optional Syntax Elements

### Filter
Specify filters to impose on matched rows. Multiple filter expressions combined with AND.

**Filter Syntax**:
```sql
Filter (
    FIRST(col1 OF A) > LAST(col2 OF B),
    FIRST(timestamp OF ANY(A,B)) + INTERVAL '10' MINUTE > LAST(timestamp OF C)
)
```

**Use Case**: When you can't express constraint with LAG/LEAD in symbols.

## LAG and LEAD Expressions

Compare current row to previous or subsequent rows within symbol predicates.

**LAG Syntax**:
```sql
current_expr operator LAG(previous_expr, lag_rows [, default])
```

**LEAD Syntax**:
```sql
current_expr operator LEAD(next_expr, lead_rows [, default])
```

**Rules**:
- lag_rows/lead_rows: Number of rows backward/forward
- default: Value when no such row exists
- Symbol with LAG/LEAD cannot have OR operator
- If input is query (not table), must create alias

**Example**:
```sql
Symbols (
    TRUE AS A,
    page = LAG(page, 1) AS DUP,
    price > LAG(price, 1, 0) AS PRICE_INCREASE
)
```

## Code Examples

### Example 1: Basic Web Clickstream - Pages Leading to Checkout

Find sessions where users went from home to products to checkout:

```sql
-- Find conversion paths
CREATE TABLE conversion_paths AS (
    SELECT * FROM nPath(
        ON web_clicks
        PARTITION BY session_id
        ORDER BY click_time
        USING
        Mode(NONOVERLAPPING)
        Pattern('^H.P+.CO')
        Symbols(
            pagetype = 'home' AS H,
            pagetype = 'product' AS P,
            pagetype = 'checkout' AS CO
        )
        Result(
            FIRST(session_id OF ANY(H,P,CO)) AS session_id,
            FIRST(user_id OF H) AS user_id,
            COUNT(* OF P) AS product_views,
            ACCUMULATE(product_name OF P DELIMITER ' -> ') AS products_viewed,
            FIRST(click_time OF H) AS journey_start,
            LAST(click_time OF CO) AS checkout_time,
            CAST((LAST(click_time OF CO) - FIRST(click_time OF H)) AS INTERVAL SECOND)
                AS time_to_checkout
        )
    )
) WITH DATA;

-- Analyze conversion patterns
SELECT
    product_views,
    COUNT(*) AS path_count,
    ROUND(AVG(EXTRACT(SECOND FROM time_to_checkout)), 0) AS avg_seconds_to_checkout,
    products_viewed
FROM conversion_paths
GROUP BY product_views, products_viewed
ORDER BY path_count DESC
LIMIT 20;
```

**Business Insights**:
- Identify most common paths to checkout
- Understand optimal number of product views before purchase
- Find fastest conversion paths

### Example 2: Detecting Abandoned Carts

Find patterns where users add to cart but don't complete purchase:

```sql
-- Find cart abandonment patterns
CREATE TABLE cart_abandonments AS (
    SELECT * FROM nPath(
        ON ecommerce_events
        PARTITION BY user_id
        ORDER BY event_time
        USING
        Mode(NONOVERLAPPING)
        Pattern('ADD+.VIEW*.^CO')  -- Add to cart, maybe view more, but NO checkout
        Symbols(
            event_type = 'add_to_cart' AS ADD,
            event_type = 'view_product' AS VIEW,
            event_type = 'checkout' AS CO
        )
        Result(
            FIRST(user_id OF ANY(ADD,VIEW)) AS user_id,
            FIRST(session_id OF ADD) AS session_id,
            COUNT(* OF ADD) AS items_added,
            ACCUMULATE(product_id OF ADD DELIMITER ',') AS abandoned_products,
            FIRST(event_time OF ADD) AS first_add_time,
            LAST(event_time OF ANY(ADD,VIEW)) AS last_activity_time,
            MAX_CHOOSE(product_price, product_name OF ADD) AS highest_value_item,
            SUM(product_price OF ADD) AS total_cart_value
        )
    )
) WITH DATA;

-- Analyze abandonment by cart value
SELECT
    CASE
        WHEN total_cart_value < 50 THEN 'Low (<$50)'
        WHEN total_cart_value < 100 THEN 'Medium ($50-$100)'
        WHEN total_cart_value < 200 THEN 'High ($100-$200)'
        ELSE 'Very High ($200+)'
    END AS cart_value_tier,
    COUNT(*) AS abandonment_count,
    ROUND(AVG(items_added), 1) AS avg_items_abandoned,
    ROUND(AVG(total_cart_value), 2) AS avg_cart_value,
    ROUND(SUM(total_cart_value), 0) AS total_abandoned_revenue
FROM cart_abandonments
GROUP BY cart_value_tier
ORDER BY MIN(total_cart_value);
```

**Recovery Strategy**: Target high-value abandonments with personalized recovery emails.

### Example 3: Finding Repeat Patterns with Range Matching

Identify users who view the same product multiple times:

```sql
-- Find repeated product views
CREATE TABLE repeat_viewers AS (
    SELECT * FROM nPath(
        ON product_views
        PARTITION BY user_id
        ORDER BY view_time
        USING
        Mode(OVERLAPPING)
        Pattern('V{3,}')  -- At least 3 views of same product
        Symbols(
            product_id = LAG(product_id, 1) AS V
        )
        Result(
            FIRST(user_id OF V) AS user_id,
            FIRST(product_id OF V) AS repeatedly_viewed_product,
            COUNT(* OF V) + 1 AS total_views,  -- +1 because LAG starts at second occurrence
            FIRST(view_time OF V) AS first_view,
            LAST(view_time OF V) AS last_view,
            CAST((LAST(view_time OF V) - FIRST(view_time OF V)) AS INTERVAL DAY)
                AS viewing_period
        )
    )
) WITH DATA;

-- Identify high-intent prospects
SELECT
    user_id,
    repeatedly_viewed_product,
    total_views,
    EXTRACT(DAY FROM viewing_period) AS days_viewing,
    CASE
        WHEN total_views >= 5 AND EXTRACT(DAY FROM viewing_period) <= 7
            THEN 'High Intent - Follow up immediately'
        WHEN total_views >= 3 AND EXTRACT(DAY FROM viewing_period) <= 14
            THEN 'Medium Intent - Send offer'
        ELSE 'Low Intent - Add to nurture campaign'
    END AS recommendation
FROM repeat_viewers
WHERE total_views >= 3
ORDER BY total_views DESC, days_viewing;
```

**Sales Action**: Proactively reach out to high-intent prospects with personalized offers.

### Example 4: Sequential Feature Adoption Analysis

Track how users adopt features in your product:

```sql
-- Find feature adoption sequences
CREATE TABLE feature_adoption_paths AS (
    SELECT * FROM nPath(
        ON app_events
        PARTITION BY user_id
        ORDER BY event_timestamp
        USING
        Mode(NONOVERLAPPING)
        Pattern('^ONBOARD.(BASIC|FEATURE)*.(ADVANCED)+')
        Symbols(
            event_name = 'onboarding_complete' AS ONBOARD,
            event_name IN ('basic_feature_1', 'basic_feature_2') AS BASIC,
            event_name IN ('profile_setup', 'settings_config') AS FEATURE,
            event_name IN ('advanced_report', 'export_data', 'api_integration') AS ADVANCED
        )
        Result(
            FIRST(user_id OF ONBOARD) AS user_id,
            FIRST(event_timestamp OF ONBOARD) AS onboarding_date,
            FIRST(event_timestamp OF ADVANCED) AS first_advanced_feature,
            CAST((FIRST(event_timestamp OF ADVANCED) - FIRST(event_timestamp OF ONBOARD))
                AS INTERVAL DAY) AS days_to_power_user,
            ACCUMULATE(event_name OF ANY(BASIC, FEATURE, ADVANCED) DELIMITER ' > ')
                AS adoption_path,
            COUNT(DISTINCT event_name OF BASIC) AS basic_features_used,
            COUNT(DISTINCT event_name OF ADVANCED) AS advanced_features_used
        )
    )
) WITH DATA;

-- Analyze paths to power user status
SELECT
    EXTRACT(DAY FROM days_to_power_user) AS days_bucket,
    COUNT(*) AS user_count,
    ROUND(AVG(basic_features_used), 1) AS avg_basic_features,
    ROUND(AVG(advanced_features_used), 1) AS avg_advanced_features,
    adoption_path
FROM feature_adoption_paths
WHERE EXTRACT(DAY FROM days_to_power_user) <= 90
GROUP BY days_bucket, adoption_path
ORDER BY user_count DESC
LIMIT 20;
```

**Product Insights**: Identify fastest paths to power user status and optimize onboarding.

### Example 5: Fraud Detection - Suspicious Login Patterns

Detect accounts with multiple failed logins followed by success:

```sql
-- Detect suspicious authentication patterns
CREATE TABLE suspicious_logins AS (
    SELECT * FROM nPath(
        ON auth_logs
        PARTITION BY user_id
        ORDER BY attempt_time
        USING
        Mode(OVERLAPPING)
        Pattern('FAIL{3,}.SUCCESS')  -- 3+ failures then success
        Symbols(
            login_status = 'failed' AS FAIL,
            login_status = 'success' AS SUCCESS
        )
        Result(
            FIRST(user_id OF FAIL) AS user_id,
            FIRST(attempt_time OF FAIL) AS first_failure,
            LAST(attempt_time OF SUCCESS) AS successful_login,
            COUNT(* OF FAIL) AS consecutive_failures,
            CAST((LAST(attempt_time OF SUCCESS) - FIRST(attempt_time OF FAIL))
                AS INTERVAL SECOND) AS attack_duration,
            ACCUMULATE(ip_address OF ANY(FAIL, SUCCESS) DELIMITER ' | ') AS ip_addresses,
            COUNT(DISTINCT ip_address OF ANY(FAIL, SUCCESS)) AS distinct_ips,
            FIRST(user_agent OF SUCCESS) AS successful_user_agent
        )
    )
) WITH DATA;

-- Flag high-risk accounts
SELECT
    user_id,
    consecutive_failures,
    EXTRACT(SECOND FROM attack_duration) AS duration_seconds,
    distinct_ips,
    ip_addresses,
    CASE
        WHEN consecutive_failures >= 10 THEN 'Critical - Likely brute force attack'
        WHEN consecutive_failures >= 5 AND distinct_ips > 1 THEN 'High Risk - Distributed attack'
        WHEN consecutive_failures >= 3 AND EXTRACT(SECOND FROM attack_duration) < 60
            THEN 'High Risk - Rapid attempts'
        ELSE 'Medium Risk - Monitor account'
    END AS risk_level,
    'Consider: Password reset, 2FA enforcement, temporary lock' AS recommended_action
FROM suspicious_logins
WHERE consecutive_failures >= 3
ORDER BY consecutive_failures DESC, duration_seconds;
```

**Security Action**: Automatically trigger additional authentication for flagged accounts.

### Example 6: IoT Sensor Pattern - Equipment Failure Prediction

Identify sensor reading patterns that precede equipment failures:

```sql
-- Find sensor patterns before failures
CREATE TABLE failure_precursors AS (
    SELECT * FROM nPath(
        ON sensor_readings
        PARTITION BY equipment_id
        ORDER BY reading_time
        USING
        Mode(NONOVERLAPPING)
        Pattern('NORMAL+.WARNING{2,}.CRITICAL+.FAILURE')
        Symbols(
            temperature < 80 AND vibration < 50 AS NORMAL,
            (temperature BETWEEN 80 AND 95) OR (vibration BETWEEN 50 AND 70) AS WARNING,
            temperature > 95 OR vibration > 70 AS CRITICAL,
            status = 'failure' AS FAILURE
        )
        Result(
            FIRST(equipment_id OF NORMAL) AS equipment_id,
            FIRST(reading_time OF WARNING) AS first_warning_time,
            FIRST(reading_time OF FAILURE) AS failure_time,
            CAST((FIRST(reading_time OF FAILURE) - FIRST(reading_time OF WARNING))
                AS INTERVAL HOUR) AS warning_window,
            COUNT(* OF WARNING) AS warning_readings,
            COUNT(* OF CRITICAL) AS critical_readings,
            MAX(temperature OF CRITICAL) AS max_temp_before_failure,
            MAX(vibration OF CRITICAL) AS max_vibration_before_failure,
            AVG(temperature OF WARNING) AS avg_temp_warning_phase,
            AVG(vibration OF WARNING) AS avg_vibration_warning_phase
        )
    )
) WITH DATA;

-- Develop predictive maintenance rules
SELECT
    EXTRACT(HOUR FROM warning_window) AS hours_warning_window,
    COUNT(*) AS failure_count,
    ROUND(AVG(warning_readings), 1) AS avg_warning_readings,
    ROUND(AVG(max_temp_before_failure), 1) AS avg_peak_temp,
    ROUND(AVG(max_vibration_before_failure), 1) AS avg_peak_vibration,
    CASE
        WHEN EXTRACT(HOUR FROM warning_window) <= 2
            THEN 'Rapid deterioration - Immediate inspection needed'
        WHEN EXTRACT(HOUR FROM warning_window) <= 12
            THEN 'Schedule maintenance within 24 hours'
        ELSE 'Normal wear - Schedule routine maintenance'
    END AS maintenance_protocol
FROM failure_precursors
GROUP BY hours_warning_window
ORDER BY hours_warning_window;
```

**Predictive Maintenance**: Automatically alert technicians when warning pattern detected.

## Common Use Cases

### 1. Session Conversion Analysis

```sql
-- Find all paths from entry to conversion
Pattern('^ENTRY.(BROWSE|SEARCH)*.(ADD_CART).CHECKOUT.PURCHASE')
```

### 2. Content Engagement Sequences

```sql
-- Users who read multiple articles in sequence
Pattern('ARTICLE{3,}')
WHERE article_id = LAG(article_id, 1)  -- Same article
```

### 3. Churn Warning Signs

```sql
-- Declining engagement before churn
Pattern('ACTIVE+.DECLINING{2,}.INACTIVE+.CHURN')
```

### 4. Upsell Opportunity Detection

```sql
-- Users exploring premium features
Pattern('FREE_FEATURE+.PREMIUM_VIEW{2,}')
```

### 5. Multi-Touch Attribution Paths

```sql
-- All touchpoints before conversion
Pattern('(IMPRESSION|CLICK|EMAIL|SOCIAL)+.CONVERSION')
```

## Best Practices

1. **Start Simple, Then Refine**:
   - Begin with basic patterns like 'A.B.C'
   - Add complexity incrementally (*, +, |)
   - Test pattern on small data sample first
   - Validate results before scaling

2. **Choose Appropriate Mode**:
   - **NONOVERLAPPING**: When analyzing distinct sequences (most common)
   - **OVERLAPPING**: When need all possible matches (less common)
   - OVERLAPPING generates more output rows

3. **Define Symbols Clearly**:
   - Use descriptive symbol names (HOME not H if unclear)
   - Ensure symbols are mutually exclusive when possible
   - Use TRUE AS X for wildcard/any-row symbol
   - Document complex symbol predicates

4. **Use Greedy Operators Wisely**:
   - Remember * and + are greedy (find longest match)
   - May match more rows than expected
   - Use {n,m} for bounded matching when needed

5. **Optimize Performance**:
   - Partition data appropriately (by user, session, device)
   - Order by timestamp for sequential analysis
   - Filter input data before nPath when possible
   - Use indexes on partition and order columns

6. **Leverage Result Functions**:
   - ACCUMULATE for visualizing paths
   - MAX_CHOOSE/MIN_CHOOSE for finding extremes
   - FIRST/LAST for boundary values
   - COUNT for pattern frequency

7. **Test Pattern Logic**:
   - Verify pattern matches expected sequences
   - Check edge cases (empty sequences, single rows)
   - Validate with known data
   - Compare OVERLAPPING vs NONOVERLAPPING results

## Related Functions

- **TD_Sessionize**: Group events into sessions before nPath analysis
- **TD_Attribution**: Assign credit after finding paths with nPath
- **TD_CFilter**: Find items that co-occur in sequences
- **LAG/LEAD Window Functions**: Simple sequential comparisons

## Notes and Limitations

1. **Unicode Support**:
   - Pattern and Symbols syntax do not support UNICODE characters
   - ACCUMULATE does not support UNICODE input/output
   - Use UTF8 client character set for data

2. **Greedy Matching**:
   - * and + operators find longest match
   - May not match shortest pattern expected
   - Consider using bounded quantifiers {n,m}

3. **Performance Considerations**:
   - Complex patterns increase computation time
   - Large partitions consume more memory
   - OVERLAPPING mode generates more output
   - Consider sampling for pattern discovery

4. **Pattern Complexity**:
   - Very complex patterns difficult to debug
   - Break into multiple simpler nPath calls
   - Test incrementally as you build pattern
   - Document pattern logic for maintenance

5. **NULL Handling**:
   - Rows with NULL in symbol predicates don't match any symbol
   - Can cause gaps in expected matches
   - Filter NULLs before nPath or handle in symbols

6. **Determinism**:
   - Output is nondeterministic if input is nondeterministic
   - Ensure ORDER BY provides total ordering
   - Add tie-breaker columns if needed

7. **LAG/LEAD Restrictions**:
   - Symbol with LAG/LEAD cannot have OR operator
   - Requires input alias if using query instead of table
   - Default value important for edge cases

8. **CLOB Columns**:
   - Input tables with CLOB cannot be DIMENSION tables
   - ACCUMULATE can output CLOB if size > 64000
   - Specify size parameter for large accumulated strings

## Version Information

- **Function Version**: Based on Teradata Database Analytic Functions Version 17.20
- **Generated**: November 28, 2025
- **Category**: Path and Pattern Analysis / Sequential Pattern Matching
