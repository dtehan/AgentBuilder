# TD_Attribution

## Function Name
- **TD_Attribution**: Marketing Attribution Analysis - Assigns credit to touchpoints that contribute to conversion events

## Description
TD_Attribution assigns weights or credits to different events and marketing channels based on their contribution to conversion outcomes. The function analyzes customer journeys and the various touchpoints customers encounter before making a purchase or completing a desired action. It uses configurable attribution models to distribute conversion credit across the sequence of events leading up to the conversion.

Attribution analysis helps organizations understand which marketing channels, campaigns, and touchpoints are most effective at driving conversions. By assigning appropriate weights using probabilistic models or rule-based methods, businesses can optimize their marketing spend and strategy to focus on the most impactful channels.

### Characteristics
- Supports multiple attribution models (first-click, last-click, uniform, exponential, weighted)
- Analyzes up to 5 input tables simultaneously
- Configurable time windows for attribution (by rows or seconds)
- Distinguishes between conversion events, excluded events, and optional events
- Provides flexible model specification for event-level or segment-level attribution
- Calculates time-to-conversion for each attributed event

### Limitations
- Limited to 5 input tables maximum
- Does not support Unicode characters in some contexts
- Requires careful model specification
- Window size must be appropriate for business context
- Attribution credit always sums to 1.0 per conversion
- Cannot attribute conversions that occur without preceding events in window

## When to Use TD_Attribution

TD_Attribution is essential for understanding marketing effectiveness and customer journeys:

### Digital Marketing Optimization
- **Multi-channel attribution**: Assign credit across email, social, search, display ads
- **Campaign effectiveness**: Measure which campaigns contribute most to conversions
- **Marketing mix modeling**: Understand channel interactions and synergies
- **Budget allocation**: Invest in channels that truly drive conversions
- **ROI measurement**: Calculate true return on investment by channel

### Customer Journey Analysis
- **Touchpoint importance**: Identify critical moments in customer journey
- **Path to purchase**: Understand typical sequences leading to conversion
- **Cross-channel behavior**: Track customers across multiple touchpoints
- **Influence vs direct**: Distinguish assisted conversions from last-click
- **Journey optimization**: Remove friction points, enhance key touchpoints

### E-Commerce and Retail
- **Product discovery paths**: How customers find and buy products
- **Content effectiveness**: Which pages/content drive purchases
- **Promotion impact**: Measure promotional touchpoint contribution
- **Referral value**: Credit referral sources appropriately
- **Cart abandonment**: Understand touchpoints before/after abandonment

### B2B Marketing
- **Lead nurturing**: Track touchpoints in long B2B sales cycles
- **Content marketing**: Measure impact of whitepapers, webinars, demos
- **Account-based marketing**: Attribute across multiple stakeholders
- **Sales enablement**: Identify which materials drive deals
- **Pipeline attribution**: Credit touchpoints throughout sales funnel

### Media and Advertising
- **Ad effectiveness**: Measure impact of different ad formats and placements
- **Sequential messaging**: Understand how message sequence affects conversion
- **Frequency analysis**: Determine optimal exposure frequency
- **Creative performance**: Compare creative variants' contribution
- **Publisher value**: Attribute credit to different media publishers

## Syntax

```sql
ATTRIBUTION (
    ON { table | view | (query) } [ AS InputTable1 ]
    PARTITION BY user_id
    ORDER BY time_column
    [ ON { table | view | (query) } [ AS InputTable2 ]
      PARTITION BY user_id
      ORDER BY time_column [,...] ]
    ON conversion_event_table AS ConversionEventTable DIMENSION
    [ ON excluding_event_table AS ExcludedEventTable DIMENSION ]
    [ ON optional_event_table AS OptionalEventTable DIMENSION ]
    ON model1_table AS FirstModelTable DIMENSION
    [ ON model2_table AS SecondModelTable DIMENSION ]
    USING
    EventColumn ('event_column')
    TimeColumn ('time_column')
    WindowSize ({'rows:K' | 'seconds:K' | 'rows:K&seconds:K2'})
) ORDER BY user_id, time_stamp;
```

**Note:** You can call this function from:
- The FROM clause of a SELECT statement
- As part of a CREATE TABLE statement
- As part of a CREATE VIEW statement

## Required Input Tables

### Input Tables (1-5 tables)
Contains clickstream data for computing attributions. Each table must be:
- **Partitioned by**: user_id (or customer identifier)
- **Ordered by**: time_column
- **Contains**: Clickstream events with timestamps

### ConversionEventTable (DIMENSION)
Specifies which events are conversion events.
- **Schema**: Single column named `conversion_event` (VARCHAR)
- **Content**: List of event values that represent conversions
- **Examples**: 'PaidSearch', 'SocialNetwork', 'Purchase', 'Signup'

### FirstModelTable (DIMENSION)
Defines the type and distribution of the first attribution model.
- **Schema**:
  - `id` (INTEGER): Row identifier (0, 1, 2, ...)
  - `model` (VARCHAR): Model type and parameters
- **Row 0**: Model type specification
- **Rows 1+**: Distribution model definitions

## Optional Input Tables

### ExcludedEventTable (DIMENSION)
Lists events to exclude from attribution.
- **Schema**: Single column named `excluding_event` (VARCHAR)
- **Content**: Events that should not receive attribution credit
- **Cannot include**: Conversion events
- **Example**: 'Email' (if treating email as not attributable)

### OptionalEventTable (DIMENSION)
Lists optional events that receive attribution only if regular events are unavailable.
- **Schema**: Single column named `optional_event` (VARCHAR)
- **Content**: Events like 'Direct', 'Referral', 'OrganicSearch'
- **Cannot include**: Conversion or excluded events
- **Use case**: Attribute to direct traffic only if no other channel available

### SecondModelTable (DIMENSION)
Defines a second attribution model for more complex scenarios.
- Same schema as FirstModelTable
- Used in combination with FirstModelTable
- See Model Specification for allowed combinations

## Required Syntax Elements

### EventColumn
Specify the name of the input column that contains the clickstream events.
- **Data Type**: VARCHAR or INTEGER
- **Description**: Event names, types, or channel identifiers
- **Examples**: 'impression', 'SocialNetwork', 'PaidSearch', 'Email'

### TimeColumn
Specify the name of the input column that contains the timestamps of the clickstream events.
- **Data Type**: INTEGER, SMALLINT, BIGINT, TIMESTAMP, or TIME
- **Description**: Event timestamps for ordering and window calculations
- **Must be**: Also used in ORDER BY clause

### WindowSize
Specify how to determine the maximum window size for attribution calculation:

| Option | Description |
|--------|-------------|
| 'rows:K' | Assign attributions to at most K events before conversion event (excluding excluded events) |
| 'seconds:K' | Assign attributions only to events within K seconds before conversion |
| 'rows:K&seconds:K2' | Apply both constraints and use stricter one |

**Examples**:
- `WindowSize('rows:10')`: Look at most recent 10 attributable events
- `WindowSize('seconds:1800')`: Look at events in last 30 minutes
- `WindowSize('rows:5&seconds:3600')`: At most 5 events within last hour

## Model Specification

### Model Types

| Model Type | Description | Additional Model Tables |
|------------|-------------|------------------------|
| **SIMPLE** | Single distribution model for all events | None allowed |
| **EVENT_REGULAR** | Distribution model per regular event | Can add EVENT_OPTIONAL |
| **EVENT_OPTIONAL** | Distribution model for optional events | Requires EVENT_REGULAR |
| **SEGMENT_ROWS** | Distribution by row segments | Can add SEGMENT_SECONDS |
| **SEGMENT_SECONDS** | Distribution by time segments | None allowed |

### Distribution Models

| Model | Parameters | Description |
|-------|------------|-------------|
| **LAST_CLICK** | 'NA' | 100% credit to most recent attributable event |
| **FIRST_CLICK** | 'NA' | 100% credit to first attributable event |
| **UNIFORM** | 'NA' | Equal credit to all attributable events |
| **EXPONENTIAL** | 'alpha,type' | Exponential decay (more recent = higher credit)<br/>• alpha: decay factor (0-1), smaller = slower decay<br/>• type: ROW, MILLISECOND, SECOND, MINUTE, HOUR, DAY, MONTH, YEAR<br/>• Formula: weight = exp(-alpha × distance)<br/>• Example: '0.5,SECOND' means weight halves each second |
| **WEIGHTED** | 'w1,w2,w3,...' | Custom weights for position-based attribution<br/>• w1: weight for most recent event (closest to conversion)<br/>• w2: weight for second most recent event<br/>• w3: weight for third most recent, etc.<br/>• Weights automatically normalized to sum to 1.0<br/>• Example: '0.5,0.3,0.2' = 50% recent, 30% middle, 20% oldest<br/>• Number of weights can be less than events (remaining events get 0) |

### SIMPLE Model Example

```sql
-- Model Table
id | model
---+------------------------
0  | SIMPLE:UNIFORM:NA
```
Applies uniform distribution to all events.

### EVENT_REGULAR Model Example

```sql
-- Model Table
id | model
---+----------------------------------------
0  | EVENT_REGULAR
1  | email:0.19:LAST_CLICK:NA
2  | impression:0.81:UNIFORM:NA
```
Within window, 19% of credit to last email event, 81% distributed uniformly across impression events.

### SEGMENT_ROWS Model Example

```sql
-- Model Table (with WindowSize('rows:10'))
id | model
---+-------------------------------
0  | SEGMENT_ROWS
1  | 3:0.5:UNIFORM:NA
2  | 4:0.3:LAST_CLICK:NA
3  | 3:0.2:FIRST_CLICK:NA
```
Of 10 rows before conversion:
- Rows 10-8 (most recent 3): 50% credit distributed uniformly
- Rows 7-4: 30% credit to last click in this segment
- Rows 3-1: 20% credit to first click in this segment

### SEGMENT_SECONDS Model Example

```sql
-- Model Table (with WindowSize('seconds:20'))
id | model
---+--------------------------------
0  | SEGMENT_SECONDS
1  | 6:0.5:UNIFORM:NA
2  | 8:0.3:LAST_CLICK:NA
3  | 6:0.2:FIRST_CLICK:NA
```
Of 20 seconds before conversion:
- Last 6 seconds: 50% credit distributed uniformly
- Previous 8 seconds: 30% credit to last click
- Oldest 6 seconds: 20% credit to first click

## Output Schema

### Output Table Schema

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| user_id | INTEGER or VARCHAR | User identifier from input table |
| event | VARCHAR | Clickstream event from input table |
| time_stamp | TIMESTAMP | Event timestamp from input table |
| attribution | DOUBLE PRECISION | Fraction of conversion attributed to this event (0.0 to 1.0) |
| time_to_conversion | INTEGER | Elapsed time (seconds) between this event and conversion event |

**Note**: For each conversion event, the sum of attribution values across all attributed events equals 1.0.

## Code Examples

### Example 1: Basic Last-Click Attribution

Simple last-click attribution model:

```sql
-- Create conversion events table
CREATE TABLE conversion_events (conversion_event VARCHAR(50));
INSERT INTO conversion_events VALUES ('Purchase');
INSERT INTO conversion_events VALUES ('Signup');

-- Create simple model (last-click)
CREATE TABLE lastclick_model (id INTEGER, model VARCHAR(200));
INSERT INTO lastclick_model VALUES (0, 'SIMPLE:LAST_CLICK:NA');

-- Run attribution
CREATE TABLE lastclick_attribution AS (
    SELECT * FROM ATTRIBUTION(
        ON clickstream_data AS InputTable1
        PARTITION BY user_id ORDER BY event_time
        ON conversion_events AS ConversionEventTable DIMENSION
        ON lastclick_model AS FirstModelTable DIMENSION
        USING
        EventColumn('event_type')
        TimeColumn('event_time')
        WindowSize('rows:10')
    )
) WITH DATA ORDER BY user_id, event_time;

-- View results
SELECT
    user_id,
    event,
    time_stamp,
    ROUND(attribution, 4) as attribution_credit,
    time_to_conversion,
    CASE
        WHEN attribution = 1.0 THEN 'Full credit (last-click)'
        WHEN attribution = 0 THEN 'No credit'
        ELSE 'Partial credit'
    END as credit_type
FROM lastclick_attribution
WHERE attribution > 0
ORDER BY user_id, time_stamp;
```

**Use Case**: Simple attribution where only the last touchpoint before conversion gets credit.

### Example 2: Multi-Channel Attribution with Event-Specific Models

Assign different weights to different channels:

```sql
-- Define conversion events
CREATE TABLE conversions (conversion_event VARCHAR(50));
INSERT INTO conversions VALUES ('PaidSearch');
INSERT INTO conversions VALUES ('SocialNetwork');

-- Define excluded events (don't attribute to email)
CREATE TABLE excluded (excluding_event VARCHAR(50));
INSERT INTO excluded VALUES ('Email');

-- Define event-specific model
CREATE TABLE event_model (id INTEGER, model VARCHAR(200));
INSERT INTO event_model VALUES (0, 'EVENT_REGULAR');
INSERT INTO event_model VALUES (1, 'impression:0.30:UNIFORM:NA');
INSERT INTO event_model VALUES (2, 'SocialNetwork:0.40:LAST_CLICK:NA');
INSERT INTO event_model VALUES (3, 'PaidSearch:0.30:LAST_CLICK:NA');

-- Run attribution
CREATE TABLE channel_attribution AS (
    SELECT * FROM ATTRIBUTION(
        ON web_clickstream AS InputTable1
        PARTITION BY user_id ORDER BY timestamp
        ON conversions AS ConversionEventTable DIMENSION
        ON excluded AS ExcludedEventTable DIMENSION
        ON event_model AS FirstModelTable DIMENSION
        USING
        EventColumn('channel')
        TimeColumn('timestamp')
        WindowSize('seconds:1800')  -- 30 minute window
    )
) WITH DATA ORDER BY user_id, timestamp;

-- Analyze channel contribution
SELECT
    event as channel,
    COUNT(*) as attribution_count,
    SUM(attribution) as total_attribution,
    ROUND(AVG(attribution), 4) as avg_attribution_per_touch,
    ROUND(SUM(attribution) / COUNT(DISTINCT user_id), 2) as attribution_per_user
FROM channel_attribution
WHERE attribution > 0
GROUP BY event
ORDER BY total_attribution DESC;
```

**Strategic Insights**:
- 30% credit distributed among impressions (awareness)
- 40% credit to last social network click (engagement)
- 30% credit to last paid search click (intent)

### Example 3: Time-Decay Attribution

Recent touchpoints get more credit:

```sql
-- Create exponential decay model
CREATE TABLE decay_model (id INTEGER, model VARCHAR(200));
INSERT INTO decay_model VALUES (0, 'SIMPLE:EXPONENTIAL:0.5,SECOND');

-- Run attribution
CREATE TABLE time_decay_attribution AS (
    SELECT * FROM ATTRIBUTION(
        ON customer_journey AS InputTable1
        PARTITION BY customer_id ORDER BY interaction_time
        ON conversion_list AS ConversionEventTable DIMENSION
        ON decay_model AS FirstModelTable DIMENSION
        USING
        EventColumn('touchpoint')
        TimeColumn('interaction_time')
        WindowSize('seconds:604800')  -- 7 day window
    )
) WITH DATA;

-- Compare attribution by recency
WITH attribution_by_recency AS (
    SELECT
        touchpoint,
        CASE
            WHEN time_to_conversion <= 86400 THEN '< 1 day'
            WHEN time_to_conversion <= 259200 THEN '1-3 days'
            WHEN time_to_conversion <= 432000 THEN '3-5 days'
            ELSE '5-7 days'
        END as recency_bucket,
        attribution
    FROM time_decay_attribution
    WHERE attribution > 0
)
SELECT
    touchpoint,
    recency_bucket,
    COUNT(*) as touch_count,
    ROUND(AVG(attribution), 4) as avg_attribution,
    ROUND(SUM(attribution), 2) as total_attribution
FROM attribution_by_recency
GROUP BY touchpoint, recency_bucket
ORDER BY touchpoint, recency_bucket;
```

**Decay Model**: With alpha=0.5, each additional second cuts attribution weight in half. More recent touchpoints receive exponentially more credit.

### Example 4: Segment-Based Attribution (Position-Based)

40% to first, 40% to last, 20% to middle:

```sql
-- Create position-based model (U-shaped)
CREATE TABLE position_model (id INTEGER, model VARCHAR(200));
INSERT INTO position_model VALUES (0, 'SEGMENT_ROWS');
INSERT INTO position_model VALUES (1, '1:0.40:FIRST_CLICK:NA');   -- First touchpoint: 40%
INSERT INTO position_model VALUES (2, '8:0.20:UNIFORM:NA');        -- Middle 8: 20% distributed
INSERT INTO position_model VALUES (3, '1:0.40:LAST_CLICK:NA');     -- Last touchpoint: 40%

-- Run attribution
CREATE TABLE position_attribution AS (
    SELECT * FROM ATTRIBUTION(
        ON marketing_touchpoints AS InputTable1
        PARTITION BY customer_id ORDER BY touchpoint_time
        ON conversion_table AS ConversionEventTable DIMENSION
        ON position_model AS FirstModelTable DIMENSION
        USING
        EventColumn('channel')
        TimeColumn('touchpoint_time')
        WindowSize('rows:10')
    )
) WITH DATA;

-- Analyze first-touch vs last-touch channels
WITH channel_position AS (
    SELECT
        channel,
        CASE
            WHEN time_to_conversion = (
                SELECT MAX(time_to_conversion)
                FROM position_attribution pa2
                WHERE pa2.user_id = pa1.user_id
            ) THEN 'First Touch'
            WHEN time_to_conversion = 0 THEN 'Last Touch'
            ELSE 'Middle Touch'
        END as position,
        attribution
    FROM position_attribution pa1
    WHERE attribution > 0
)
SELECT
    channel,
    position,
    COUNT(*) as occurrences,
    ROUND(AVG(attribution), 4) as avg_attribution,
    ROUND(SUM(attribution), 2) as total_attribution
FROM channel_position
GROUP BY channel, position
ORDER BY channel, position;
```

**U-Shaped Model**: Emphasizes introduction (first touch) and closing (last touch) while still crediting middle touchpoints.

### Example 5: Multi-Table Attribution with Optional Events

Combine online and TV advertising attribution:

```sql
-- Create optional events table (direct, referral only get credit if no other events)
CREATE TABLE optional_events (optional_event VARCHAR(50));
INSERT INTO optional_events VALUES ('Direct');
INSERT INTO optional_events VALUES ('Referral');
INSERT INTO optional_events VALUES ('OrganicSearch');

-- Create event model with optional events
CREATE TABLE multi_event_model (id INTEGER, model VARCHAR(200));
INSERT INTO multi_event_model VALUES (0, 'EVENT_REGULAR');
INSERT INTO multi_event_model VALUES (1, 'impression:0.30:UNIFORM:NA');
INSERT INTO multi_event_model VALUES (2, 'SocialNetwork:0.35:LAST_CLICK:NA');
INSERT INTO multi_event_model VALUES (3, 'PaidSearch:0.35:LAST_CLICK:NA');

CREATE TABLE optional_model (id INTEGER, model VARCHAR(200));
INSERT INTO optional_model VALUES (0, 'EVENT_OPTIONAL');
INSERT INTO optional_model VALUES (1, 'Direct:0.40:LAST_CLICK:NA');
INSERT INTO optional_model VALUES (2, 'Referral:0.30:LAST_CLICK:NA');
INSERT INTO optional_model VALUES (3, 'OrganicSearch:0.30:UNIFORM:NA');

-- Run attribution with multiple inputs
CREATE TABLE comprehensive_attribution AS (
    SELECT * FROM ATTRIBUTION(
        ON web_events AS InputTable1
        PARTITION BY user_id ORDER BY event_time
        ON tv_spots AS InputTable2 DIMENSION ORDER BY air_time
        ON conversions AS ConversionEventTable DIMENSION
        ON optional_events AS OptionalEventTable DIMENSION
        ON multi_event_model AS FirstModelTable DIMENSION
        ON optional_model AS SecondModelTable DIMENSION
        USING
        EventColumn('event')
        TimeColumn('event_time')
        WindowSize('rows:15&seconds:2592000')  -- 15 events or 30 days
    )
) WITH DATA;

-- Analyze regular vs optional attribution
SELECT
    event,
    CASE
        WHEN event IN (SELECT optional_event FROM optional_events) THEN 'Optional'
        ELSE 'Regular'
    END as event_category,
    COUNT(DISTINCT user_id) as users_attributed,
    ROUND(SUM(attribution), 2) as total_attribution,
    ROUND(AVG(attribution), 4) as avg_attribution,
    ROUND(AVG(time_to_conversion) / 86400.0, 1) as avg_days_to_conversion
FROM comprehensive_attribution
WHERE attribution > 0
GROUP BY event, event_category
ORDER BY total_attribution DESC;
```

**Optional Events Logic**: Direct, Referral, and Organic get credit only when no regular paid channels are available in the attribution window.

### Example 6: ROI Calculation with Attribution

Calculate true ROI by channel using attribution:

```sql
-- First, run attribution
CREATE TABLE campaign_attribution AS (
    SELECT * FROM ATTRIBUTION(
        ON campaign_clicks AS InputTable1
        PARTITION BY user_id ORDER BY click_time
        ON purchases AS ConversionEventTable DIMENSION
        ON attribution_model AS FirstModelTable DIMENSION
        USING
        EventColumn('campaign_channel')
        TimeColumn('click_time')
        WindowSize('seconds:2592000')  -- 30 days
    )
) WITH DATA;

-- Join with cost and revenue data to calculate ROI
WITH attributed_revenue AS (
    SELECT
        a.event as campaign_channel,
        a.user_id,
        a.attribution as attribution_weight,
        p.order_value,
        p.order_value * a.attribution as attributed_revenue
    FROM campaign_attribution a
    JOIN purchases p
        ON a.user_id = p.user_id
        AND a.time_stamp <= p.purchase_time
    WHERE a.attribution > 0
),
channel_performance AS (
    SELECT
        campaign_channel,
        COUNT(DISTINCT user_id) as attributed_customers,
        SUM(attributed_revenue) as total_attributed_revenue,
        AVG(attributed_revenue) as avg_attributed_revenue_per_touch
    FROM attributed_revenue
    GROUP BY campaign_channel
),
channel_costs AS (
    SELECT
        channel,
        SUM(spend) as total_spend
    FROM campaign_budget
    GROUP BY channel
)
SELECT
    p.campaign_channel,
    p.attributed_customers,
    ROUND(p.total_attributed_revenue, 2) as attributed_revenue,
    ROUND(c.total_spend, 2) as channel_spend,
    ROUND((p.total_attributed_revenue - c.total_spend) / c.total_spend * 100, 1)
        as roi_percentage,
    ROUND(p.total_attributed_revenue / c.total_spend, 2) as revenue_per_dollar_spent,
    ROUND(p.avg_attributed_revenue_per_touch, 2) as avg_revenue_per_touchpoint,
    CASE
        WHEN (p.total_attributed_revenue / c.total_spend) > 5.0 THEN 'Excellent ROI - Increase spend'
        WHEN (p.total_attributed_revenue / c.total_spend) > 3.0 THEN 'Good ROI - Maintain'
        WHEN (p.total_attributed_revenue / c.total_spend) > 1.5 THEN 'Acceptable ROI'
        WHEN (p.total_attributed_revenue / c.total_spend) > 1.0 THEN 'Marginal ROI - Optimize'
        ELSE 'Negative ROI - Reconsider channel'
    END as roi_recommendation
FROM channel_performance p
JOIN channel_costs c ON p.campaign_channel = c.channel
ORDER BY roi_percentage DESC;
```

**Business Impact**: True multi-touch attribution reveals actual channel performance, enabling data-driven budget allocation.

### Example 7: Complete Multi-Table Attribution with Combined Segment Models

Comprehensive example using both SEGMENT_ROWS and SEGMENT_SECONDS models together:

```sql
-- Create first input table: clickstream data (Table 1)
CREATE TABLE attribution_sample_table1 (
    user_id INTEGER,
    event VARCHAR(50),
    timestamp_value INTEGER
);

INSERT INTO attribution_sample_table1 VALUES
(1, 'impression', 100),
(1, 'impression', 200),
(1, 'impression', 400),
(1, 'email', 500),
(1, 'impression', 600),
(1, 'impression', 700),
(1, 'impression', 900),
(1, 'impression', 1000),
(1, 'impression', 1200),
(1, 'impression', 1300),
(1, 'impression', 1500);

-- Create second input table: social and paid search data (Table 2)
CREATE TABLE attribution_sample_table2 (
    user_id INTEGER,
    event VARCHAR(50),
    timestamp_value INTEGER
);

INSERT INTO attribution_sample_table2 VALUES
(1, 'impression', 300),
(1, 'impression', 800),
(1, 'impression', 1100),
(1, 'impression', 1400),
(1, 'SocialNetwork', 1600),  -- Conversion event
(1, 'PaidSearch', 2100);      -- Conversion event

-- Define conversion events
CREATE TABLE conversion_event_table (conversion_event VARCHAR(50));
INSERT INTO conversion_event_table VALUES ('SocialNetwork');
INSERT INTO conversion_event_table VALUES ('PaidSearch');

-- Define excluded events (email should not receive attribution)
CREATE TABLE excluding_event_table (excluding_event VARCHAR(50));
INSERT INTO excluding_event_table VALUES ('email');

-- Define optional events (direct traffic only gets credit if no regular events)
CREATE TABLE optional_event_table (optional_event VARCHAR(50));
INSERT INTO optional_event_table VALUES ('Direct');

-- Create First Model: SEGMENT_ROWS
-- Distributes attribution based on position in event sequence
CREATE TABLE model1_table (id INTEGER, model VARCHAR(200));
INSERT INTO model1_table VALUES (0, 'SEGMENT_ROWS');
INSERT INTO model1_table VALUES (1, '3:0.5:UNIFORM:NA');       -- Most recent 3 rows: 50% uniform
INSERT INTO model1_table VALUES (2, '4:0.3:LAST_CLICK:NA');    -- Next 4 rows: 30% last click
INSERT INTO model1_table VALUES (3, '3:0.2:FIRST_CLICK:NA');   -- Oldest 3 rows: 20% first click

-- Create Second Model: SEGMENT_SECONDS
-- Distributes attribution based on time proximity to conversion
CREATE TABLE model2_table (id INTEGER, model VARCHAR(200));
INSERT INTO model2_table VALUES (0, 'SEGMENT_SECONDS');
INSERT INTO model2_table VALUES (1, '6:0.5:UNIFORM:NA');       -- Last 6 seconds: 50% uniform
INSERT INTO model2_table VALUES (2, '8:0.3:LAST_CLICK:NA');    -- Previous 8 seconds: 30% last click
INSERT INTO model2_table VALUES (3, '6:0.2:FIRST_CLICK:NA');   -- Oldest 6 seconds: 20% first click

-- Run attribution with both segment models
CREATE TABLE complete_attribution AS (
    SELECT * FROM ATTRIBUTION(
        ON attribution_sample_table1 AS InputTable1
        PARTITION BY user_id ORDER BY timestamp_value
        ON attribution_sample_table2 AS InputTable2
        PARTITION BY user_id ORDER BY timestamp_value
        ON conversion_event_table AS ConversionEventTable DIMENSION
        ON excluding_event_table AS ExcludedEventTable DIMENSION
        ON optional_event_table AS OptionalEventTable DIMENSION
        ON model1_table AS FirstModelTable DIMENSION
        ON model2_table AS SecondModelTable DIMENSION
        USING
        EventColumn('event')
        TimeColumn('timestamp_value')
        WindowSize('rows:10&seconds:20')  -- Apply both row and time constraints
    )
) WITH DATA ORDER BY user_id, timestamp_value;

-- View results for first conversion (SocialNetwork at timestamp 1600)
SELECT
    user_id,
    event,
    time_stamp,
    ROUND(attribution, 6) as attribution_value,
    time_to_conversion,
    CASE
        WHEN time_stamp = 1500 THEN 'Most recent impression (3-row segment)'
        WHEN time_stamp = 1400 THEN 'Second most recent (3-row segment)'
        WHEN time_stamp = 1300 THEN 'Third most recent (3-row segment)'
        WHEN time_stamp = 1200 THEN 'In 4-row middle segment'
        WHEN time_stamp = 1100 THEN 'In 4-row middle segment'
        ELSE 'Older impressions'
    END as segment_explanation
FROM complete_attribution
WHERE time_stamp <= 1600
ORDER BY user_id, time_stamp;

/*
Expected Output for SocialNetwork conversion (timestamp 1600):

user_id | event      | time_stamp | attribution_value | time_to_conversion | segment_explanation
--------|------------|------------|-------------------|--------------------|--------------------------
1       | impression | 1100       | 0.142857          | 500                | In 4-row middle segment
1       | impression | 1200       | 0.142857          | 400                | In 4-row middle segment
1       | impression | 1300       | 0.142857          | 300                | Third most recent
1       | impression | 1400       | 0.142857          | 200                | Second most recent
1       | impression | 1500       | 0.142857          | 100                | Most recent impression
1       | impression | 300        | 0.285714          | 1300               | Combined attribution
1       | SocialNetwork | 1600    | 1.000000          | 0                  | Conversion event

Explanation of Attribution Values:
- WindowSize('rows:10&seconds:20'): At most 10 events within 20 seconds of conversion
- For SocialNetwork conversion at t=1600:
  * Events within 20 seconds: 1400 (t-200), 1500 (t-100)
  * But need to include up to 10 events, so goes back to earlier events
- SEGMENT_ROWS model (50% weight):
  * Last 3 rows get 0.5 * (1/3) each = 0.166667
  * Next 4 rows would get 0.3 distributed
  * Oldest 3 rows would get 0.2 distributed
- SEGMENT_SECONDS model (50% weight):
  * Last 6 seconds (1400-1600): 0.5 uniform distribution
  * Previous 8 seconds: 0.3 last click
  * Oldest 6 seconds: 0.2 first click
- Combined: Average of both models' attributions
*/

-- Analyze attribution by model contribution
WITH model_analysis AS (
    SELECT
        event,
        time_stamp,
        attribution,
        time_to_conversion,
        CASE
            WHEN time_to_conversion <= 100 THEN 'Very recent (0-100s)'
            WHEN time_to_conversion <= 400 THEN 'Recent (100-400s)'
            WHEN time_to_conversion <= 800 THEN 'Mid-range (400-800s)'
            ELSE 'Distant (>800s)'
        END as time_bucket
    FROM complete_attribution
    WHERE attribution > 0
)
SELECT
    time_bucket,
    COUNT(*) as event_count,
    ROUND(SUM(attribution), 4) as total_attribution,
    ROUND(AVG(attribution), 6) as avg_attribution,
    ROUND(MIN(time_to_conversion), 0) as min_seconds,
    ROUND(MAX(time_to_conversion), 0) as max_seconds
FROM model_analysis
GROUP BY time_bucket
ORDER BY min_seconds;

-- Compare conversion attribution patterns
SELECT
    'SocialNetwork' as conversion_type,
    COUNT(DISTINCT event) as unique_touchpoints,
    SUM(CASE WHEN attribution > 0 THEN 1 ELSE 0 END) as attributed_events,
    ROUND(SUM(attribution), 2) as total_attribution_sum,
    ROUND(AVG(CASE WHEN attribution > 0 THEN attribution END), 6) as avg_nonzero_attribution
FROM complete_attribution
WHERE time_stamp <= 1600

UNION ALL

SELECT
    'PaidSearch' as conversion_type,
    COUNT(DISTINCT event) as unique_touchpoints,
    SUM(CASE WHEN attribution > 0 THEN 1 ELSE 0 END) as attributed_events,
    ROUND(SUM(attribution), 2) as total_attribution_sum,
    ROUND(AVG(CASE WHEN attribution > 0 THEN attribution END), 6) as avg_nonzero_attribution
FROM complete_attribution
WHERE time_stamp > 1600 AND time_stamp <= 2100;
```

**Key Insights from Combined Segment Models**:

1. **Dual Constraint Window** (`rows:10&seconds:20`):
   - Uses the stricter of two constraints
   - Ensures attribution considers both recency and sequence position
   - Prevents distant events from receiving credit even if within row window

2. **SEGMENT_ROWS Model** (First Model):
   - Divides the 10-event window into 3 segments by position
   - Most recent 3 events: 50% credit distributed uniformly
   - Middle 4 events: 30% credit to last click in segment
   - Oldest 3 events: 20% credit to first click in segment

3. **SEGMENT_SECONDS Model** (Second Model):
   - Divides the 20-second window into 3 time segments
   - Last 6 seconds: 50% credit distributed uniformly
   - Previous 8 seconds: 30% credit to last click
   - Oldest 6 seconds: 20% credit to first click

4. **Model Combination**:
   - Both models evaluate independently
   - Final attribution is average of both models
   - Balances position-based and time-based attribution
   - More robust than single-model approach

5. **Excluded Events Impact**:
   - 'email' events at timestamp 500 receive zero attribution
   - Not counted toward the 10-row window
   - Removed before attribution calculation

6. **Multiple Conversions**:
   - Each conversion (SocialNetwork, PaidSearch) gets independent attribution
   - Attribution sums to 1.0 for each conversion event
   - Different touchpoints may contribute to different conversions

**Business Application**:
This comprehensive model is ideal for scenarios where both the sequence of touchpoints AND their timing relative to conversion are important. For example:
- E-commerce where recent browsing matters but also the discovery sequence
- B2B sales where both touchpoint order and time decay are relevant
- Mobile app engagement where session position and time-since-event both matter

## Common Use Cases

### 1. Compare Attribution Models

```sql
-- Run multiple models and compare
-- Last-click
SELECT 'Last-Click' as model, event, SUM(attribution) as total_credit
FROM lastclick_attribution GROUP BY event

UNION ALL

-- Linear (uniform)
SELECT 'Linear' as model, event, SUM(attribution) as total_credit
FROM linear_attribution GROUP BY event

UNION ALL

-- Time-decay
SELECT 'Time-Decay' as model, event, SUM(attribution) as total_credit
FROM decay_attribution GROUP BY event

ORDER BY model, total_credit DESC;
```

### 2. Journey Path Attribution

```sql
-- Identify most valuable customer journeys
WITH journey_paths AS (
    SELECT
        user_id,
        STRING_AGG(event, ' > ' ORDER BY time_stamp) as journey,
        SUM(attribution) as total_attribution
    FROM attribution_results
    WHERE attribution > 0
    GROUP BY user_id
)
SELECT
    journey,
    COUNT(*) as occurrence_count,
    ROUND(AVG(total_attribution), 4) as avg_attribution
FROM journey_paths
GROUP BY journey
HAVING COUNT(*) >= 5  -- Journeys that occurred at least 5 times
ORDER BY occurrence_count DESC, avg_attribution DESC
LIMIT 20;
```

### 3. Assisted Conversion Analysis

```sql
-- Identify assist vs direct conversions
WITH conversion_analysis AS (
    SELECT
        user_id,
        event,
        attribution,
        time_to_conversion,
        CASE
            WHEN time_to_conversion = 0 THEN 'Direct Conversion'
            ELSE 'Assisted Conversion'
        END as conversion_role
    FROM attribution_results
    WHERE attribution > 0
)
SELECT
    event,
    conversion_role,
    COUNT(*) as touch_count,
    ROUND(SUM(attribution), 2) as total_attribution,
    ROUND(AVG(attribution), 4) as avg_attribution
FROM conversion_analysis
GROUP BY event, conversion_role
ORDER BY event, conversion_role;
```

## Best Practices

1. **Choose Appropriate Window Size**:
   - E-commerce: 30 days typical consideration period
   - B2B: 90-180 days for longer sales cycles
   - Impulse purchases: 1-7 days
   - Consider both rows and seconds constraints

2. **Select Right Attribution Model**:
   - **Last-click**: Simple, biased toward closing touchpoints
   - **First-click**: Emphasizes awareness and discovery
   - **Linear**: Fair but may overvalue minor touchpoints
   - **Time-decay**: Balances recency with full journey
   - **Position-based**: Emphasizes first and last (U-shaped)
   - **Data-driven**: Use historical data to optimize weights

3. **Define Events Carefully**:
   - **Conversion events**: Clear, measurable actions
   - **Excluded events**: Internal or non-attributable touchpoints
   - **Optional events**: Direct traffic, organic (use as fallback)

4. **Validate Attribution Results**:
   - Total attribution should sum to 1.0 per conversion
   - Check for missing conversions in output
   - Verify time windows make business sense
   - Compare multiple models before deciding

5. **Handle Multi-Device Journeys**:
   - Use cross-device identity resolution first
   - Ensure user_id is consistent across devices
   - Consider device as additional partition dimension

6. **Monitor Model Performance**:
   - Track how attribution affects budget allocation
   - Measure actual ROI changes after optimization
   - Periodically re-evaluate model choice
   - A/B test budget changes based on attribution

7. **Communicate Results Effectively**:
   - Show assist vs direct contribution
   - Visualize customer journey flows
   - Calculate incremental lift by channel
   - Present ROI with confidence intervals

## Related Functions

- **TD_nPath**: Pattern matching for complex journey analysis
- **TD_Sessionize**: Group clicks into sessions before attribution
- **TD_CFilter**: Analyze which touchpoints co-occur
- **Window functions**: LEAD/LAG for analyzing touchpoint sequences

## Notes and Limitations

1. **Input Table Limit**:
   - Maximum 5 input tables (partitioned)
   - Unlimited DIMENSION tables
   - All partitioned tables must use same user_id partition key

2. **Unicode Support**:
   - Does not support UNICODE for ACCUMULATE function results
   - Does not support UNICODE in Pattern syntax elements
   - Supports UNICODE data in input tables with UTF8 client

3. **Model Complexity**:
   - Complex models require careful specification
   - Weights must sum to 1.0 in EVENT models
   - Segment sizes must match WindowSize constraints
   - Model validation is critical

4. **Attribution Sum**:
   - For each conversion, attribution always sums to exactly 1.0
   - Multiple conversions per user treated independently
   - No attribution if no events in window before conversion

5. **Time Handling**:
   - Time calculations depend on TimeColumn data type
   - Ensure consistent time zones across inputs
   - WindowSize seconds uses actual elapsed time
   - Consider clock changes (daylight saving time)

6. **Performance Considerations**:
   - Large windows increase computation
   - Multiple input tables add complexity
   - Consider sampling for exploratory analysis
   - Partition by user_id required for parallel processing

7. **Business Logic**:
   - Attribution models are assumptions, not truth
   - No single "correct" model
   - Test multiple approaches
   - Combine with experimentation (A/B tests)

8. **Causation vs Correlation**:
   - Attribution identifies association, not causation
   - High attribution ≠ high incremental value
   - Use incrementality testing to validate
   - Consider confounding factors

## Version Information

- **Function Version**: Based on Teradata Database Analytic Functions Version 17.20
- **Generated**: November 28, 2025
- **Category**: Path and Pattern Analysis / Marketing Attribution / Customer Journey Analysis
