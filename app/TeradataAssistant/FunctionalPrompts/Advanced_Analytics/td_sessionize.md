# TD_Sessionize

## Function Name
- **TD_Sessionize**: Session Identification - Groups clicks into browsing sessions and detects bot activity

## Description
TD_Sessionize maps each click in a clickstream to a unique session identifier. A session is defined as a sequence of clicks by one user that are separated by at most a specified timeout period (n seconds). If more than n seconds elapse between clicks, the function starts a new session.

The function is useful for both sessionization (grouping user interactions into meaningful sessions) and detecting web crawler or bot activity (identifying automated traffic based on unrealistically short time intervals between clicks). Understanding user sessions is critical for analyzing browsing behavior, conversion funnels, and user engagement on websites and applications.

### Characteristics
- Assigns unique session IDs to sequences of clicks
- Configurable timeout threshold for session boundaries
- Bot detection via minimum click lag parameter
- Handles NULL values in time columns
- Outputs session ID and bot detection flag for each row
- Preserves all input columns in output

### Limitations
- Cannot use column names 'sessionid' or 'clicklag' in input (reserved for output)
- Requires consistent timestamp format
- Simple timeout-based logic (no semantic session boundaries)
- Bot detection based only on click frequency
- Does not handle cross-device sessions

## When to Use TD_Sessionize

TD_Sessionize is essential for analyzing user behavior and detecting automated traffic:

### Web Analytics and User Behavior
- **Session analysis**: Group user actions into meaningful browsing sessions
- **Funnel analysis**: Track conversion funnels within sessions
- **Engagement metrics**: Calculate session duration, pages per session
- **Bounce rate**: Identify single-page sessions
- **User journey mapping**: Understand paths users take within sessions

### Conversion Rate Optimization
- **Session-level conversion**: Analyze which sessions lead to conversions
- **Path to purchase**: Examine typical session flows before purchase
- **Cart abandonment**: Identify sessions that add to cart but don't convert
- **Exit page analysis**: Find where users leave within sessions
- **A/B testing**: Compare session behavior across test variants

### Bot and Fraud Detection
- **Web crawler detection**: Identify automated bots by click frequency
- **Traffic quality**: Filter bot traffic from analytics
- **Security monitoring**: Detect suspicious automated activity
- **Scraping prevention**: Identify and block content scrapers
- **Ad fraud detection**: Find click fraud and invalid traffic

### Content Effectiveness
- **Content engagement**: Measure how content keeps users in session
- **Navigation analysis**: Understand how users move through site
- **Search behavior**: Analyze search patterns within sessions
- **Video engagement**: Track video viewing within sessions
- **Document downloads**: Identify document access patterns

### Mobile App Analytics
- **App session tracking**: Group app interactions into sessions
- **Feature usage**: Analyze which features are used together
- **Crash analysis**: Identify session context around crashes
- **Performance monitoring**: Track session-level app performance
- **User retention**: Measure session frequency and recency

## Syntax

```sql
SESSIONIZE (
    ON { table | view | (query) }
    PARTITION BY expression [,...]
    ORDER BY order_column [,...]
    USING
    TimeColumn ('time_column')
    TimeOut (session_timeout)
    [ ClickLag (min_click_lag) ]
    [ EmitNull ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
)
```

**Note:** You can call this function from:
- The FROM clause of a SELECT statement
- As part of a CREATE TABLE statement
- As part of a CREATE VIEW statement

## Required Syntax Elements

### ON Clause
Accepts the clickstream input table containing user interactions.

### PARTITION BY
Specifies how to partition the input data. Each partition should contain all rows for one entity (typically user or device).

**Common Partitions**:
- `PARTITION BY user_id`: Sessionize by user
- `PARTITION BY device_id`: Sessionize by device
- `PARTITION BY user_id, device_type`: Sessionize by user and device type
- `PARTITION BY ip_address`: Sessionize by IP (when no user ID available)

### ORDER BY
Specifies how to order rows within each partition. Must include time_column.

**Examples**:
- `ORDER BY clicktime`: Order by timestamp ascending
- `ORDER BY clicktime DESC`: Reverse chronological
- `ORDER BY clicktime, sequence_number`: Secondary sort key

### TimeColumn
**Required**: Specify the name of the input column that contains the click times.
- **Data Type**: TIME, TIMESTAMP, INTEGER, BIGINT, SMALLINT, or DATE
- **Description**: Timestamp of each click or interaction
- **Integer Types**: Interpreted as milliseconds since epoch
- **Must be**: Included in ORDER BY clause

### TimeOut
**Required**: Specify the number of seconds that the session times out.
- **Data Type**: DOUBLE PRECISION
- **Description**: Maximum time gap between clicks in same session
- **Logic**: If timeout seconds elapse after a click, next click starts new session
- **Common Values**:
  - 1800 (30 minutes): Standard web session timeout
  - 900 (15 minutes): Shorter timeout for high-engagement sites
  - 3600 (1 hour): Longer timeout for research/comparison sites
  - 300 (5 minutes): Mobile app sessions

## Optional Syntax Elements

### ClickLag
Specify the minimum number of seconds (lag) between clicks for the session user to be considered human.
- **Data Type**: DOUBLE PRECISION
- **Description**: Minimum time between clicks that indicates human behavior
- **Constraint**: Must be less than timeout threshold
- **Default**: No filtering (all sessions retained regardless of click frequency)
- **Bot Detection**: If time between clicks < min_click_lag, session marked as bot
- **Common Values**:
  - 0.2 (200 milliseconds): Very fast but possible for humans
  - 0.5 (500 milliseconds): More conservative bot threshold
  - 1.0 (1 second): Very conservative threshold

**Example**: `ClickLag(0.2)` marks sessions as bots if any two consecutive clicks are less than 0.2 seconds apart.

### EmitNull
Specify whether to output rows that have NULL values in time_column.
- **Data Type**: Boolean string
- **Default**: 'false'
- **Values**: 'true', 't', 'yes', 'y', '1' (true) or 'false', 'f', 'no', 'n', '0' (false)
- **Behavior**:
  - 'false': Rows with NULL time_column are omitted from output
  - 'true': Rows with NULL time_column included with NULL sessionid and clicklag

## Input Schema

### Input Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| time_column | TIME, TIMESTAMP, INTEGER, BIGINT, SMALLINT, or DATE | Click times (milliseconds if INTEGER type) |
| partition_column | ANY | Column that partitions input (user_id, device_id, etc.) |
| order_column | ANY | Column by which data is ordered (usually time_column) |
| other_columns | ANY | Additional columns to preserve in output |

**Important Restrictions**:
- No input column can be named 'sessionid' (reserved for output)
- No input column can be named 'clicklag' (reserved for output)

**Creating Timestamp from Separate Columns**:
```sql
-- Combine date and time columns into timestamp
SELECT (date_column || ' ' || time_column)::timestamp AS event_timestamp
FROM input_table;
```

## Output Schema

### Output Table Schema

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| input_column | Same as input | All columns from input table are copied to output |
| sessionid | INTEGER or BIGINT | Unique session identifier assigned by function (starts at 0 for each partition) |
| clicklag | BYTEINT | Bot detection indicator:<br/>• 0 or 'f': Human behavior (meets minimum click lag)<br/>• 1 or 't': Bot suspected (click lag below threshold) |

**Session ID Assignment**:
- Starts at 0 for first session in each partition
- Increments by 1 for each new session
- Unique within partition, not globally unique

## Code Examples

### Example 1: Basic Website Sessionization

Group website clicks into 30-minute sessions:

```sql
-- Create sessionized clickstream
CREATE TABLE web_sessions AS (
    SELECT * FROM SESSIONIZE(
        ON website_clicks
        PARTITION BY user_id
        ORDER BY click_time
        USING
        TimeColumn('click_time')
        TimeOut(1800)  -- 30 minutes
    )
) WITH DATA ORDER BY user_id, click_time;

-- View session summary
SELECT
    user_id,
    sessionid,
    COUNT(*) as clicks_in_session,
    MIN(click_time) as session_start,
    MAX(click_time) as session_end,
    EXTRACT(EPOCH FROM (MAX(click_time) - MIN(click_time))) as session_duration_seconds,
    SUM(CASE WHEN page_type = 'product' THEN 1 ELSE 0 END) as product_views,
    SUM(CASE WHEN page_type = 'checkout' THEN 1 ELSE 0 END) as checkout_pages,
    MAX(CASE WHEN page_type = 'purchase' THEN 1 ELSE 0 END) as converted
FROM web_sessions
GROUP BY user_id, sessionid
ORDER BY user_id, sessionid;
```

**Analytics Use**:
- Calculate pages per session
- Identify session duration distribution
- Track conversion rate by session

### Example 2: Bot Detection with ClickLag

Identify and filter bot traffic:

```sql
-- Sessionize with bot detection
CREATE TABLE sessions_with_bots AS (
    SELECT * FROM SESSIONIZE(
        ON web_traffic
        PARTITION BY ip_address
        ORDER BY request_time
        USING
        TimeColumn('request_time')
        TimeOut(900)     -- 15 minutes
        ClickLag(0.2)    -- 200ms minimum between clicks
    )
) WITH DATA;

-- Analyze bot vs human traffic
SELECT
    clicklag as is_bot,
    COUNT(DISTINCT ip_address) as unique_visitors,
    COUNT(DISTINCT sessionid) as total_sessions,
    COUNT(*) as total_clicks,
    ROUND(AVG(EXTRACT(EPOCH FROM (MAX(request_time) - MIN(request_time)))), 1)
        as avg_session_duration,
    CASE clicklag
        WHEN 't' THEN 'Bot Traffic (exclude from analytics)'
        ELSE 'Human Traffic (include in analytics)'
    END as traffic_classification
FROM sessions_with_bots
GROUP BY clicklag, traffic_classification;

-- Filter to human sessions only
CREATE VIEW human_sessions AS
SELECT *
FROM sessions_with_bots
WHERE clicklag = 'f';  -- Only human traffic

-- Session metrics for humans only
SELECT
    COUNT(DISTINCT sessionid) as human_sessions,
    ROUND(AVG(clicks_per_session), 1) as avg_clicks_per_session,
    ROUND(AVG(session_duration_minutes), 1) as avg_session_duration_min
FROM (
    SELECT
        sessionid,
        COUNT(*) as clicks_per_session,
        EXTRACT(EPOCH FROM (MAX(request_time) - MIN(request_time))) / 60.0
            as session_duration_minutes
    FROM human_sessions
    GROUP BY sessionid
) session_stats;
```

**Bot Detection Value**:
- Exclude bot traffic from user analytics
- Identify scraping attempts
- Clean data for accurate metrics

### Example 3: E-Commerce Session Funnel Analysis

Analyze conversion funnel within sessions:

```sql
-- Sessionize e-commerce clickstream
CREATE TABLE ecommerce_sessions AS (
    SELECT * FROM SESSIONIZE(
        ON ecommerce_clicks
        PARTITION BY customer_id
        ORDER BY event_timestamp
        USING
        TimeColumn('event_timestamp')
        TimeOut(1800)  -- 30 minutes
        ClickLag(0.3)
    )
) WITH DATA;

-- Session-level funnel analysis
WITH session_funnel AS (
    SELECT
        sessionid,
        customer_id,
        MAX(CASE WHEN page_type = 'home' THEN 1 ELSE 0 END) as visited_home,
        MAX(CASE WHEN page_type = 'product' THEN 1 ELSE 0 END) as viewed_product,
        MAX(CASE WHEN page_type = 'cart' THEN 1 ELSE 0 END) as added_to_cart,
        MAX(CASE WHEN page_type = 'checkout' THEN 1 ELSE 0 END) as started_checkout,
        MAX(CASE WHEN page_type = 'purchase' THEN 1 ELSE 0 END) as completed_purchase,
        clicklag
    FROM ecommerce_sessions
    WHERE clicklag = 'f'  -- Human traffic only
    GROUP BY sessionid, customer_id, clicklag
)
SELECT
    'Total Sessions' as funnel_stage,
    COUNT(*) as session_count,
    100.0 as pct_of_previous_stage,
    100.0 as pct_of_total
FROM session_funnel

UNION ALL

SELECT
    'Viewed Product' as funnel_stage,
    SUM(viewed_product) as session_count,
    ROUND(SUM(viewed_product) * 100.0 / COUNT(*), 1) as pct_of_previous_stage,
    ROUND(SUM(viewed_product) * 100.0 / COUNT(*), 1) as pct_of_total
FROM session_funnel

UNION ALL

SELECT
    'Added to Cart' as funnel_stage,
    SUM(added_to_cart) as session_count,
    ROUND(SUM(added_to_cart) * 100.0 / NULLIFZERO(SUM(viewed_product)), 1)
        as pct_of_previous_stage,
    ROUND(SUM(added_to_cart) * 100.0 / COUNT(*), 1) as pct_of_total
FROM session_funnel

UNION ALL

SELECT
    'Started Checkout' as funnel_stage,
    SUM(started_checkout) as session_count,
    ROUND(SUM(started_checkout) * 100.0 / NULLIFZERO(SUM(added_to_cart)), 1)
        as pct_of_previous_stage,
    ROUND(SUM(started_checkout) * 100.0 / COUNT(*), 1) as pct_of_total
FROM session_funnel

UNION ALL

SELECT
    'Completed Purchase' as funnel_stage,
    SUM(completed_purchase) as session_count,
    ROUND(SUM(completed_purchase) * 100.0 / NULLIFZERO(SUM(started_checkout)), 1)
        as pct_of_previous_stage,
    ROUND(SUM(completed_purchase) * 100.0 / COUNT(*), 1) as pct_of_total
FROM session_funnel

ORDER BY session_count DESC;
```

**Funnel Insights**:
- Identify drop-off points in conversion journey
- Calculate session-level conversion rates
- Compare funnel performance across segments

### Example 4: Mobile App Session Analysis

Analyze mobile app usage patterns:

```sql
-- Sessionize app events
CREATE TABLE app_sessions AS (
    SELECT * FROM SESSIONIZE(
        ON mobile_app_events
        PARTITION BY device_id, user_id
        ORDER BY event_time
        USING
        TimeColumn('event_time')
        TimeOut(300)    -- 5 minutes for mobile apps
        ClickLag(0.1)   -- Very fast clicks possible on mobile
    )
) WITH DATA;

-- App engagement metrics by session
WITH session_metrics AS (
    SELECT
        user_id,
        sessionid,
        COUNT(*) as events_in_session,
        COUNT(DISTINCT feature_name) as features_used,
        MIN(event_time) as session_start,
        MAX(event_time) as session_end,
        EXTRACT(EPOCH FROM (MAX(event_time) - MIN(event_time))) as duration_seconds,
        SUM(CASE WHEN event_type = 'error' THEN 1 ELSE 0 END) as error_count
    FROM app_sessions
    WHERE clicklag = 'f'
    GROUP BY user_id, sessionid
)
SELECT
    CASE
        WHEN duration_seconds < 60 THEN '< 1 minute'
        WHEN duration_seconds < 300 THEN '1-5 minutes'
        WHEN duration_seconds < 900 THEN '5-15 minutes'
        ELSE '15+ minutes'
    END as session_length,
    COUNT(*) as num_sessions,
    ROUND(AVG(events_in_session), 1) as avg_events,
    ROUND(AVG(features_used), 1) as avg_features_used,
    ROUND(SUM(CASE WHEN error_count > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1)
        as pct_sessions_with_errors
FROM session_metrics
GROUP BY session_length
ORDER BY
    CASE session_length
        WHEN '< 1 minute' THEN 1
        WHEN '1-5 minutes' THEN 2
        WHEN '5-15 minutes' THEN 3
        ELSE 4
    END;
```

**Mobile App Insights**:
- Understand typical session lengths
- Identify feature adoption within sessions
- Track session quality (errors)

### Example 5: Cross-Session User Journey Analysis

Track users across multiple sessions:

```sql
-- Sessionize with user history
CREATE TABLE user_sessions AS (
    SELECT * FROM SESSIONIZE(
        ON user_activity
        PARTITION BY user_id
        ORDER BY activity_timestamp
        USING
        TimeColumn('activity_timestamp')
        TimeOut(1800)
    )
) WITH DATA;

-- Analyze user behavior across sessions
WITH user_session_summary AS (
    SELECT
        user_id,
        COUNT(DISTINCT sessionid) as total_sessions,
        MIN(activity_timestamp) as first_visit,
        MAX(activity_timestamp) as last_visit,
        EXTRACT(EPOCH FROM (MAX(activity_timestamp) - MIN(activity_timestamp))) / 86400.0
            as days_active,
        SUM(CASE WHEN action = 'purchase' THEN 1 ELSE 0 END) as total_purchases,
        COUNT(DISTINCT CASE WHEN action = 'purchase' THEN sessionid END)
            as sessions_with_purchase
    FROM user_sessions
    GROUP BY user_id
)
SELECT
    CASE
        WHEN total_sessions = 1 THEN 'Single Session'
        WHEN total_sessions <= 5 THEN '2-5 Sessions'
        WHEN total_sessions <= 10 THEN '6-10 Sessions'
        ELSE '11+ Sessions'
    END as session_frequency,
    COUNT(*) as num_users,
    ROUND(AVG(total_purchases), 2) as avg_purchases_per_user,
    ROUND(AVG(sessions_with_purchase * 100.0 / total_sessions), 1)
        as avg_conversion_rate,
    ROUND(AVG(days_active), 1) as avg_days_active
FROM user_session_summary
GROUP BY session_frequency
ORDER BY
    CASE session_frequency
        WHEN 'Single Session' THEN 1
        WHEN '2-5 Sessions' THEN 2
        WHEN '6-10 Sessions' THEN 3
        ELSE 4
    END;
```

**User Retention Insights**:
- Segment users by session frequency
- Calculate lifetime conversion rates
- Identify most engaged user segments

### Example 6: Real-Time Session Monitoring

Monitor active sessions and detect anomalies:

```sql
-- Sessionize recent activity (last 24 hours)
CREATE TABLE active_sessions AS (
    SELECT * FROM SESSIONIZE(
        ON recent_clickstream
        PARTITION BY user_id
        ORDER BY click_timestamp
        USING
        TimeColumn('click_timestamp')
        TimeOut(1800)
        ClickLag(0.2)
    )
    WHERE click_timestamp >= CURRENT_TIMESTAMP - INTERVAL '24' HOUR
) WITH DATA;

-- Real-time session monitoring dashboard
WITH current_sessions AS (
    SELECT
        user_id,
        sessionid,
        COUNT(*) as clicks,
        MIN(click_timestamp) as session_start,
        MAX(click_timestamp) as last_activity,
        EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - MAX(click_timestamp))) as idle_seconds,
        clicklag as is_bot
    FROM active_sessions
    GROUP BY user_id, sessionid, clicklag
    HAVING MAX(click_timestamp) >= CURRENT_TIMESTAMP - INTERVAL '30' MINUTE
)
SELECT
    COUNT(*) as active_sessions,
    SUM(CASE WHEN is_bot = 't' THEN 1 ELSE 0 END) as suspected_bots,
    SUM(CASE WHEN idle_seconds < 60 THEN 1 ELSE 0 END) as very_active,
    SUM(CASE WHEN idle_seconds BETWEEN 60 AND 600 THEN 1 ELSE 0 END) as moderately_active,
    SUM(CASE WHEN idle_seconds > 600 THEN 1 ELSE 0 END) as likely_abandoned,
    ROUND(AVG(clicks), 1) as avg_clicks_per_session,
    MAX(clicks) as max_clicks_in_session
FROM current_sessions;

-- Alert on suspicious activity
SELECT
    user_id,
    sessionid,
    clicks,
    session_start,
    last_activity,
    idle_seconds,
    'ALERT: Potential bot or scraper' as alert_type
FROM current_sessions
WHERE is_bot = 't'
   OR clicks > 100  -- Unusually high clicks
ORDER BY clicks DESC;
```

**Real-Time Monitoring**:
- Track currently active sessions
- Identify and block bots in real-time
- Detect unusual activity patterns

## Common Use Cases

### 1. Bounce Rate Calculation

```sql
-- Identify single-page sessions (bounces)
WITH session_stats AS (
    SELECT
        sessionid,
        COUNT(*) as page_views
    FROM web_sessions
    WHERE clicklag = 'f'
    GROUP BY sessionid
)
SELECT
    SUM(CASE WHEN page_views = 1 THEN 1 ELSE 0 END) as bounced_sessions,
    COUNT(*) as total_sessions,
    ROUND(SUM(CASE WHEN page_views = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2)
        as bounce_rate_pct
FROM session_stats;
```

### 2. Session Duration Distribution

```sql
-- Analyze session length patterns
WITH session_duration AS (
    SELECT
        sessionid,
        EXTRACT(EPOCH FROM (MAX(timestamp) - MIN(timestamp))) as duration_seconds
    FROM web_sessions
    GROUP BY sessionid
)
SELECT
    CASE
        WHEN duration_seconds = 0 THEN '0s (Single Click)'
        WHEN duration_seconds < 30 THEN '1-30s'
        WHEN duration_seconds < 60 THEN '30-60s'
        WHEN duration_seconds < 300 THEN '1-5 min'
        WHEN duration_seconds < 600 THEN '5-10 min'
        WHEN duration_seconds < 1800 THEN '10-30 min'
        ELSE '30+ min'
    END as duration_bucket,
    COUNT(*) as session_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) as pct_of_sessions
FROM session_duration
GROUP BY duration_bucket
ORDER BY MIN(duration_seconds);
```

### 3. Time Between Sessions (Return Frequency)

```sql
-- Calculate time between user sessions
WITH session_times AS (
    SELECT
        user_id,
        sessionid,
        MIN(click_time) as session_start
    FROM web_sessions
    GROUP BY user_id, sessionid
),
session_gaps AS (
    SELECT
        user_id,
        sessionid,
        session_start,
        LAG(session_start) OVER (PARTITION BY user_id ORDER BY sessionid) as prev_session_start,
        EXTRACT(EPOCH FROM (
            session_start - LAG(session_start) OVER (PARTITION BY user_id ORDER BY sessionid)
        )) / 3600.0 as hours_since_last_session
    FROM session_times
)
SELECT
    CASE
        WHEN hours_since_last_session < 1 THEN '< 1 hour'
        WHEN hours_since_last_session < 24 THEN '1-24 hours'
        WHEN hours_since_last_session < 168 THEN '1-7 days'
        WHEN hours_since_last_session < 720 THEN '1-4 weeks'
        ELSE '1+ months'
    END as return_frequency,
    COUNT(*) as num_return_sessions
FROM session_gaps
WHERE prev_session_start IS NOT NULL
GROUP BY return_frequency
ORDER BY MIN(hours_since_last_session);
```

## Best Practices

1. **Choose Appropriate Timeout**:
   - **Web browsing**: 30 minutes (1800 seconds) standard
   - **Mobile apps**: 5-10 minutes (300-600 seconds)
   - **Research sites**: 1 hour (3600 seconds) for longer reading
   - **Transaction sites**: 15 minutes (900 seconds) for checkout flows
   - **Video streaming**: Consider no timeout or very long (watching full video)

2. **Set Realistic ClickLag for Bot Detection**:
   - **0.1-0.2 seconds**: Very aggressive (may catch fast human users)
   - **0.3-0.5 seconds**: Balanced approach
   - **1.0+ seconds**: Very conservative (only catches obvious bots)
   - Test with real traffic before filtering

3. **Partition Appropriately**:
   - **Logged-in users**: Partition by user_id
   - **Anonymous traffic**: Partition by device_id or cookie_id
   - **No identifiers**: Partition by IP address (less accurate)
   - **Cross-device**: Requires identity resolution first

4. **Handle NULL Timestamps**:
   - Use EmitNull('false') to exclude incomplete data
   - Or EmitNull('true') and filter NULL sessions in analysis
   - Investigate why NULLs occur (data quality issue?)

5. **Combine with Other Analysis**:
   - Use sessionize before running nPath for pattern analysis
   - Feed sessions into attribution models
   - Join with user demographics for segmentation
   - Combine with CFilter for in-session item associations

6. **Monitor Bot Traffic**:
   - Regularly review clicklag = 't' traffic
   - Validate bot detection with manual inspection
   - Update ClickLag threshold based on findings
   - Block detected bots at application layer

7. **Performance Optimization**:
   - Partition by columns that distribute data evenly
   - Index on partition and order columns
   - Consider incremental processing for large datasets
   - Archive old sessions to separate tables

## Related Functions

- **TD_nPath**: Analyze patterns within sessions
- **TD_Attribution**: Assign conversion credit to session touchpoints
- **TD_CFilter**: Find items purchased together in same session
- **LAG/LEAD**: Analyze time between clicks within sessions

## Notes and Limitations

1. **Reserved Column Names**:
   - Cannot use 'sessionid' as input column name
   - Cannot use 'clicklag' as input column name
   - Function will error if these columns exist in input

2. **Simple Timeout Logic**:
   - Only uses time threshold for session boundaries
   - Does not consider semantic events (logout, session end markers)
   - Cannot detect session from URL parameters or cookies
   - Manual session boundaries require pre-processing

3. **Bot Detection Limitations**:
   - Only detects bots by click frequency
   - Does not use user-agent, IP patterns, or behavior
   - Fast human users may be flagged incorrectly
   - Sophisticated bots can mimic human timing

4. **Session ID Scope**:
   - Session IDs unique within partition only
   - Not globally unique across all users
   - Starts at 0 for each partition
   - Combine with partition key for unique identifier

5. **Timestamp Handling**:
   - Integer timestamps interpreted as milliseconds
   - Ensure consistent time zones across data
   - Be aware of daylight saving time changes
   - NULL timestamps require EmitNull parameter

6. **Cross-Device Sessions**:
   - Function cannot track sessions across devices
   - Requires pre-processing with identity resolution
   - Consider using session cookies or device fingerprinting
   - May need custom logic for cross-device journeys

7. **Memory and Performance**:
   - Large partitions may consume significant memory
   - Very long sessions increase computation time
   - Consider breaking analysis into time windows
   - Use appropriate ORDER BY for efficient processing

8. **Business Logic**:
   - 30-minute timeout is convention, not universal truth
   - Validate timeout choice against actual user behavior
   - Different site types may need different timeouts
   - Consider making timeout configurable per user segment

## Version Information

- **Function Version**: Based on Teradata Database Analytic Functions Version 17.20
- **Generated**: November 28, 2025
- **Category**: Path and Pattern Analysis / Session Analysis / Web Analytics
