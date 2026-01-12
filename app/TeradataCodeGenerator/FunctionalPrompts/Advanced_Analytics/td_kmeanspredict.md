# TD_KMeansPredict

## Function Name
**TD_KMeansPredict** - K-Means Clustering Prediction

**Aliases:** KMeansPredict

## Description

TD_KMeansPredict assigns new data points to clusters based on a trained K-means clustering model. K-means is an unsupervised learning algorithm that partitions data into K distinct groups based on feature similarity, where each data point belongs to the cluster with the nearest centroid. This function is essential for applying trained clustering models to new observations for segmentation, pattern recognition, and anomaly detection.

**Key Characteristics:**
- **Unsupervised Learning**: Assigns cluster membership without labeled training data
- **Distance-Based Assignment**: Uses Euclidean or other distance metrics to find nearest centroid
- **Fast Prediction**: Efficient assignment by calculating distances to K centroids
- **Cluster Centers**: Works with centroids learned from TD_KMeans training
- **Multi-Dimensional**: Handles high-dimensional feature spaces
- **Production-Ready**: Optimized for scoring large datasets in real-time or batch mode

The function takes a trained K-means model (cluster centroids from TD_KMeans) and assigns each new data point to the nearest cluster.

## When to Use TD_KMeansPredict

**Business Applications:**
- **Customer Segmentation**: Assign new customers to behavioral segments for personalized marketing
- **Product Recommendations**: Group products into categories for recommendation engines
- **Anomaly Detection**: Identify observations far from any cluster center (outliers)
- **Image Compression**: Assign pixels to color clusters for compression
- **Network Security**: Classify network traffic patterns into normal/anomalous groups
- **Inventory Optimization**: Segment products by demand patterns for stocking strategies
- **Credit Risk**: Group loan applicants into risk tiers based on financial profiles
- **Healthcare**: Stratify patients into care pathways based on clinical features

**Use TD_KMeansPredict When You Need To:**
- Assign new observations to pre-defined clusters
- Score test data after model training
- Deploy clustering models in production pipelines
- Segment incoming data streams in real-time
- Apply consistent segmentation logic across time periods
- Identify which cluster a new customer/product/transaction belongs to

**Analytical Use Cases:**
- Customer profiling and targeting
- Market basket analysis
- Fraud detection (outliers)
- Content recommendation
- Sensor data classification
- Geographic segmentation
- A/B test group assignment

## Syntax

```sql
SELECT * FROM TD_KMeansPredict (
    ON { table | view | (query) } AS InputTable PARTITION BY ANY
    ON { table | view | (query) } AS ModelTable DIMENSION
    USING
    IDColumn ('id_column')
    [ Accumulate ('column' [,...]) ]
    [ OutputDistance ({ 'true' | 'false' }) ]
) AS dt;
```

## Required Elements

### InputTable (PARTITION BY ANY)
The table containing data to score. Must include:
- All feature columns used during model training (same names and types)
- ID column for row identification
- Numeric features (K-means operates on continuous variables)

### ModelTable (DIMENSION)
The trained K-means model table produced by TD_KMeans function. Contains:
- Cluster centroids (K rows, one per cluster)
- Feature means for each cluster
- Cluster identifiers
- Model metadata

### IDColumn
Specifies the column that uniquely identifies each row in InputTable.

**Syntax:** `IDColumn('column_name')`

**Example:**
```sql
IDColumn('customer_id')
```

## Optional Elements

### Accumulate
Specifies columns from InputTable to include in output (pass-through columns).

**Syntax:** `Accumulate('column1', 'column2', ...)`

**Example:**
```sql
Accumulate('customer_id', 'customer_name', 'segment_date')
```

**Note:** Accumulate categorical or descriptive columns for business context, not features used in distance calculation.

### OutputDistance
Whether to output the Euclidean distance from each data point to its assigned cluster centroid.

**Values:**
- `'true'`: Include distance column showing proximity to cluster center
- `'false'`: Output only cluster assignment (default)

**Syntax:** `OutputDistance('true')`

**Use Cases for OutputDistance:**
- **Anomaly Detection**: Large distances indicate outliers or atypical observations
- **Cluster Confidence**: Small distances indicate strong cluster membership
- **Quality Assessment**: Monitor average distances to detect model degradation

## Input Schema

### InputTable
| Column | Data Type | Description |
|--------|-----------|-------------|
| id_column | INTEGER, VARCHAR | Unique identifier for each row |
| feature_1 | NUMERIC | First feature (same as training) |
| feature_2 | NUMERIC | Second feature (same as training) |
| ... | NUMERIC | Additional features (must match training data) |
| accumulate_cols | ANY | Optional columns to pass through |

**Requirements:**
- All feature columns from training must be present
- Column names must match training data exactly
- Numeric data types for features
- No NULL values in features (handle missing values before prediction)
- Features should be scaled if scaling was applied during training

### ModelTable
Standard output from TD_KMeans function containing:
- Cluster centroids (one row per cluster)
- Feature means for each cluster
- Cluster IDs (typically 0 to K-1)

## Output Schema

### Standard Output (OutputDistance = 'false')
| Column | Data Type | Description |
|--------|-----------|-------------|
| id_column | Same as input | Row identifier from InputTable |
| cluster_id | INTEGER | Assigned cluster (0 to K-1) |
| accumulate_cols | Same as input | Pass-through columns if specified |

### Output with Distance (OutputDistance = 'true')
| Column | Data Type | Description |
|--------|-----------|-------------|
| id_column | Same as input | Row identifier from InputTable |
| cluster_id | INTEGER | Assigned cluster (0 to K-1) |
| distance | DOUBLE PRECISION | Euclidean distance to cluster centroid |
| accumulate_cols | Same as input | Pass-through columns if specified |

**Notes:**
- cluster_id is the cluster with minimum distance to the data point
- distance is the Euclidean distance: sqrt(sum((x_i - centroid_i)^2))
- Lower distance indicates stronger cluster membership
- Very high distances may indicate outliers

## Code Examples

### Example 1: Customer Segmentation - Basic Cluster Assignment

**Business Context:** A retailer has trained a 4-cluster model on historical customer purchase behavior. Assign new customers to segments for targeted marketing.

```sql
-- Train K-means model on historical customer data
CREATE TABLE customer_kmeans_model AS (
    SELECT * FROM TD_KMeans (
        ON customer_features_training AS InputTable
        USING
        InputColumns ('annual_spend', 'purchase_frequency', 'avg_order_value',
                      'recency_days', 'product_diversity')
        NumClusters (4)
        MaxIterNum (50)
        StopThreshold (0.01)
    ) AS dt
) WITH DATA;

-- Assign new customers to segments
SELECT * FROM TD_KMeansPredict (
    ON new_customers AS InputTable PARTITION BY ANY
    ON customer_kmeans_model AS ModelTable DIMENSION
    USING
    IDColumn ('customer_id')
    Accumulate ('customer_name', 'signup_date', 'email')
) AS dt
ORDER BY cluster_id, customer_id;

/*
Sample Output:
customer_id | cluster_id | customer_name      | signup_date | email
------------|------------|--------------------|-------------|------------------------
12001       | 0          | John Smith         | 2024-01-15  | john.smith@email.com
12005       | 0          | Sarah Johnson      | 2024-01-16  | sarah.j@email.com
12002       | 1          | Maria Garcia       | 2024-01-15  | maria.g@email.com
12004       | 2          | David Lee          | 2024-01-16  | david.lee@email.com
12003       | 3          | Emily Chen         | 2024-01-15  | emily.c@email.com

Interpretation (based on cluster profiling):
- Cluster 0: High-value, frequent buyers → Premium offers, loyalty rewards
- Cluster 1: Moderate spenders, price-sensitive → Discount campaigns
- Cluster 2: Low engagement, at-risk → Re-engagement campaigns
- Cluster 3: New, high-potential → Onboarding sequence, cross-sell
*/

-- Business Impact:
-- Automated segmentation reduces manual customer classification time by 90%
-- Enables real-time personalization at scale
```

### Example 2: Anomaly Detection with Distance Thresholds

**Business Context:** Detect fraudulent transactions by identifying purchases that don't fit any normal spending pattern (outliers).

```sql
-- Train K-means on normal transaction patterns
CREATE TABLE transaction_kmeans_model AS (
    SELECT * FROM TD_KMeans (
        ON normal_transactions_training AS InputTable
        USING
        InputColumns ('amount', 'merchant_category_code', 'distance_from_home',
                      'transaction_hour', 'days_since_last_purchase')
        NumClusters (6)
        MaxIterNum (100)
    ) AS dt
) WITH DATA;

-- Score new transactions with distance to nearest cluster
SELECT * FROM TD_KMeansPredict (
    ON incoming_transactions AS InputTable PARTITION BY ANY
    ON transaction_kmeans_model AS ModelTable DIMENSION
    USING
    IDColumn ('transaction_id')
    OutputDistance ('true')
    Accumulate ('customer_id', 'amount', 'merchant_name', 'transaction_time')
) AS dt
ORDER BY distance DESC;  -- Largest distances first (potential fraud)

/*
Sample Output:
transaction_id | cluster_id | distance | customer_id | amount  | merchant_name       | transaction_time
---------------|------------|----------|-------------|---------|---------------------|------------------
TXN50012       | 3          | 8.42     | C78901      | 2850.50 | Electronics Store   | 2024-01-15 03:22
TXN50089       | 2          | 7.15     | C45612      | 1980.00 | Online Retailer     | 2024-01-15 02:15
TXN50045       | 1          | 2.31     | C12345      | 156.50  | Local Grocery       | 2024-01-15 10:30
TXN50023       | 0          | 0.87     | C23456      | 42.30   | Coffee Shop         | 2024-01-15 08:15

Interpretation:
- TXN50012: Distance 8.42 → Highly anomalous, flag for fraud review
- TXN50089: Distance 7.15 → Somewhat unusual, require additional verification
- TXN50045: Distance 2.31 → Normal variation, approve
- TXN50023: Distance 0.87 → Typical transaction, auto-approve
*/

-- Create fraud alert system
CREATE TABLE fraud_alerts AS (
    SELECT
        transaction_id,
        customer_id,
        amount,
        merchant_name,
        cluster_id,
        distance,
        CASE
            WHEN distance >= 7.0 THEN 'HIGH_RISK_BLOCK'
            WHEN distance >= 4.0 THEN 'MEDIUM_RISK_REVIEW'
            WHEN distance >= 2.5 THEN 'LOW_RISK_MONITOR'
            ELSE 'NORMAL'
        END AS fraud_risk_level
    FROM TD_KMeansPredict (
        ON incoming_transactions AS InputTable PARTITION BY ANY
        ON transaction_kmeans_model AS ModelTable DIMENSION
        USING
        IDColumn ('transaction_id')
        OutputDistance ('true')
        Accumulate ('customer_id', 'amount', 'merchant_name')
    ) AS dt
    WHERE distance >= 2.5  -- Only flag unusual transactions
) WITH DATA;

-- Business Impact:
-- Detected 47% more fraud cases compared to rule-based system
-- Reduced false positives by 35%
-- Average fraud detection time reduced from 3 days to real-time
```

### Example 3: Product Categorization for Recommendations

**Business Context:** Assign new products to categories based on sales patterns to power recommendation engine.

```sql
-- Train K-means on product sales features
CREATE TABLE product_kmeans_model AS (
    SELECT * FROM TD_KMeans (
        ON product_sales_history AS InputTable
        USING
        InputColumns ('avg_daily_units', 'price_point', 'seasonality_index',
                      'customer_age_median', 'online_vs_store_ratio')
        NumClusters (8)
        MaxIterNum (75)
        Seed (12345)  -- Reproducible results
    ) AS dt
) WITH DATA;

-- Assign new products to clusters
SELECT * FROM TD_KMeansPredict (
    ON new_product_catalog AS InputTable PARTITION BY ANY
    ON product_kmeans_model AS ModelTable DIMENSION
    USING
    IDColumn ('product_id')
    Accumulate ('product_name', 'category', 'launch_date')
) AS dt
ORDER BY product_id;

/*
Sample Output:
product_id | cluster_id | product_name           | category        | launch_date
-----------|------------|------------------------|-----------------|------------
PRD8801    | 2          | Wireless Headphones    | Electronics     | 2024-02-01
PRD8802    | 2          | Bluetooth Speaker      | Electronics     | 2024-02-01
PRD8803    | 5          | Winter Jacket          | Apparel         | 2024-02-01
PRD8804    | 1          | Kitchen Blender        | Home & Kitchen  | 2024-02-01

Interpretation:
- Cluster 2: High-tech accessories, young demographic → Recommend with smartphones
- Cluster 5: Seasonal apparel, moderate price → Recommend seasonal bundles
- Cluster 1: Home appliances, family demographic → Cross-sell related kitchen items
*/

-- Build recommendation rules based on clusters
CREATE TABLE product_recommendations AS (
    SELECT
        p1.product_id AS source_product,
        p2.product_id AS recommended_product,
        p1.cluster_id,
        'SAME_CLUSTER' AS recommendation_reason
    FROM TD_KMeansPredict (
        ON new_product_catalog AS InputTable PARTITION BY ANY
        ON product_kmeans_model AS ModelTable DIMENSION
        USING IDColumn ('product_id')
        Accumulate ('product_name')
    ) AS p1
    JOIN TD_KMeansPredict (
        ON new_product_catalog AS InputTable PARTITION BY ANY
        ON product_kmeans_model AS ModelTable DIMENSION
        USING IDColumn ('product_id')
        Accumulate ('product_name')
    ) AS p2
    ON p1.cluster_id = p2.cluster_id
    WHERE p1.product_id <> p2.product_id
) WITH DATA;

-- Business Impact:
-- Recommendation click-through rate improved by 28%
-- Cross-sell conversion increased by 18%
-- Reduced manual product categorization effort by 85%
```

### Example 4: Customer Lifetime Value Segmentation with Profiling

**Business Context:** Segment customers into value tiers and profile each segment to optimize resource allocation.

```sql
-- Train K-means on customer value metrics
CREATE TABLE clv_kmeans_model AS (
    SELECT * FROM TD_KMeans (
        ON customer_value_features AS InputTable
        USING
        InputColumns ('total_revenue', 'purchase_frequency', 'avg_margin',
                      'customer_tenure_months', 'support_tickets_per_year')
        NumClusters (5)
        MaxIterNum (100)
    ) AS dt
) WITH DATA;

-- Assign all customers to value segments
CREATE TABLE customer_segments AS (
    SELECT * FROM TD_KMeansPredict (
        ON all_customers AS InputTable PARTITION BY ANY
        ON clv_kmeans_model AS ModelTable DIMENSION
        USING
        IDColumn ('customer_id')
        OutputDistance ('true')
        Accumulate ('customer_name', 'industry', 'account_manager', 'total_revenue')
    ) AS dt
) WITH DATA;

-- Profile each segment
SELECT
    cluster_id AS segment_id,
    COUNT(*) AS customer_count,
    AVG(total_revenue) AS avg_revenue,
    AVG(distance) AS avg_cluster_tightness,
    CASE
        WHEN cluster_id = 0 THEN 'PLATINUM - High Value'
        WHEN cluster_id = 1 THEN 'GOLD - Growth Potential'
        WHEN cluster_id = 2 THEN 'SILVER - Stable'
        WHEN cluster_id = 3 THEN 'BRONZE - Occasional'
        WHEN cluster_id = 4 THEN 'AT RISK - Declining'
    END AS segment_label
FROM customer_segments
GROUP BY cluster_id
ORDER BY avg_revenue DESC;

/*
Sample Output:
segment_id | customer_count | avg_revenue | avg_cluster_tightness | segment_label
-----------|----------------|-------------|----------------------|----------------------
0          | 450            | 125000.00   | 1.45                 | PLATINUM - High Value
1          | 1200           | 48000.00    | 1.82                 | GOLD - Growth Potential
2          | 3500           | 18000.00    | 1.53                 | SILVER - Stable
3          | 5200           | 6500.00     | 2.11                 | BRONZE - Occasional
4          | 850            | 4200.00     | 2.87                 | AT RISK - Declining

Interpretation:
- Segment 0: Top 450 customers drive 28% of revenue → Dedicate account managers
- Segment 1: High growth potential → Upsell campaigns, quarterly business reviews
- Segment 2: Largest group, stable → Automated nurture campaigns
- Segment 3: Low engagement → Self-service portal, occasional promotions
- Segment 4: High distance (2.87) indicates heterogeneous group → Investigate churn risk
*/

-- Assign treatment strategy per segment
CREATE TABLE segment_strategies AS (
    SELECT
        customer_id,
        customer_name,
        cluster_id AS segment_id,
        total_revenue,
        distance,
        CASE
            WHEN cluster_id = 0 THEN 'DEDICATED_MANAGER'
            WHEN cluster_id = 1 THEN 'GROWTH_PROGRAM'
            WHEN cluster_id = 2 THEN 'AUTOMATED_NURTURE'
            WHEN cluster_id = 3 THEN 'SELF_SERVICE'
            WHEN cluster_id = 4 AND distance > 3.5 THEN 'CHURN_PREVENTION'
            WHEN cluster_id = 4 THEN 'WIN_BACK'
        END AS engagement_strategy,
        CASE
            WHEN cluster_id IN (0, 1) THEN 'HIGH'
            WHEN cluster_id = 2 THEN 'MEDIUM'
            ELSE 'LOW'
        END AS priority
    FROM customer_segments
) WITH DATA;

-- Business Impact:
-- Resource allocation optimized: Focus 80% of effort on segments 0 and 1
-- Customer retention improved by 22% through targeted interventions
-- Marketing ROI increased 3.2x by eliminating mass campaigns
```

### Example 5: Geographic Market Segmentation

**Business Context:** Segment retail store locations into performance tiers for inventory allocation and staffing decisions.

```sql
-- Train K-means on store performance metrics
CREATE TABLE store_kmeans_model AS (
    SELECT * FROM TD_KMeans (
        ON store_performance AS InputTable
        USING
        InputColumns ('weekly_revenue', 'foot_traffic', 'avg_basket_size',
                      'inventory_turnover', 'employee_productivity')
        NumClusters (3)  -- High, Medium, Low performance
        MaxIterNum (50)
    ) AS dt
) WITH DATA;

-- Segment all stores
CREATE TABLE store_segments AS (
    SELECT * FROM TD_KMeansPredict (
        ON all_stores AS InputTable PARTITION BY ANY
        ON store_kmeans_model AS ModelTable DIMENSION
        USING
        IDColumn ('store_id')
        OutputDistance ('true')
        Accumulate ('store_name', 'city', 'state', 'square_footage', 'employee_count')
    ) AS dt
) WITH DATA;

-- Profile store segments and create action plans
SELECT
    cluster_id,
    COUNT(*) AS store_count,
    AVG(square_footage) AS avg_size,
    AVG(employee_count) AS avg_employees,
    CASE
        WHEN cluster_id = 0 THEN 'FLAGSHIP STORES'
        WHEN cluster_id = 1 THEN 'STANDARD STORES'
        WHEN cluster_id = 2 THEN 'UNDERPERFORMING'
    END AS segment_name,
    CASE
        WHEN cluster_id = 0 THEN 'Premium inventory, extended hours, events'
        WHEN cluster_id = 1 THEN 'Standard assortment, regular hours'
        WHEN cluster_id = 2 THEN 'Reduce inventory, audit operations, consider closure'
    END AS action_plan
FROM store_segments
GROUP BY cluster_id;

/*
Sample Output:
cluster_id | store_count | avg_size | avg_employees | segment_name       | action_plan
-----------|-------------|----------|---------------|--------------------|--------------------------------
0          | 25          | 45000    | 85            | FLAGSHIP STORES    | Premium inventory, events
1          | 150         | 28000    | 45            | STANDARD STORES    | Standard assortment
2          | 18          | 22000    | 32            | UNDERPERFORMING    | Reduce inventory, audit ops

Interpretation:
- Cluster 0: Top 25 stores → Increase inventory depth, host promotional events
- Cluster 1: 150 standard stores → Maintain current strategy
- Cluster 2: 18 underperforming stores → Root cause analysis, potential closure
*/

-- Flag outlier stores within each segment
SELECT
    store_id,
    store_name,
    city,
    state,
    cluster_id AS performance_segment,
    distance,
    CASE
        WHEN distance > 4.0 THEN 'INVESTIGATE - Unusual metrics for segment'
        ELSE 'NORMAL'
    END AS outlier_flag
FROM store_segments
WHERE distance > 4.0
ORDER BY distance DESC;

-- Business Impact:
-- Inventory allocation optimized, reducing waste by $2.1M annually
-- Identified 5 stores for closure, saving $800K/year in operating costs
-- Flagship stores received additional investment, increasing revenue by 15%
```

### Example 6: Real-Time Content Recommendation

**Business Context:** Assign articles/videos to content clusters for real-time personalized recommendations.

```sql
-- Train K-means on content engagement features
CREATE TABLE content_kmeans_model AS (
    SELECT * FROM TD_KMeans (
        ON content_engagement_history AS InputTable
        USING
        InputColumns ('avg_view_duration', 'completion_rate', 'share_rate',
                      'comment_count_normalized', 'click_through_rate')
        NumClusters (6)
        MaxIterNum (80)
    ) AS dt
) WITH DATA;

-- Assign new content to clusters in real-time
SELECT * FROM TD_KMeansPredict (
    ON new_content_published AS InputTable PARTITION BY ANY
    ON content_kmeans_model AS ModelTable DIMENSION
    USING
    IDColumn ('content_id')
    Accumulate ('title', 'author', 'publish_date', 'topic')
) AS dt
ORDER BY content_id;

/*
Sample Output:
content_id | cluster_id | title                          | author         | publish_date | topic
-----------|------------|--------------------------------|----------------|--------------|-------------
ART9001    | 2          | 10 Ways to Boost Productivity  | Sarah Johnson  | 2024-01-15   | Business
ART9002    | 4          | Breaking News: Tech Merger     | John Smith     | 2024-01-15   | Technology
ART9003    | 2          | Remote Work Best Practices     | Emily Chen     | 2024-01-15   | Business
ART9004    | 1          | Celebrity Interview Exclusive  | Maria Garcia   | 2024-01-15   | Entertainment

Interpretation:
- Cluster 2: High-engagement business content → Recommend to professional users
- Cluster 4: Breaking news, high virality → Push notifications, homepage feature
- Cluster 1: Entertainment, casual consumption → Recommend during off-peak hours
*/

-- Build user-to-content recommendation logic
CREATE TABLE user_content_recommendations AS (
    SELECT
        u.user_id,
        c.content_id,
        c.title,
        c.cluster_id AS content_cluster,
        u.preferred_cluster,
        CASE
            WHEN c.cluster_id = u.preferred_cluster THEN 1.0
            ELSE 0.3
        END AS recommendation_score
    FROM (
        -- User's preferred cluster based on past engagement
        SELECT user_id, MODE(cluster_id) AS preferred_cluster
        FROM user_content_history
        GROUP BY user_id
    ) u
    CROSS JOIN TD_KMeansPredict (
        ON new_content_published AS InputTable PARTITION BY ANY
        ON content_kmeans_model AS ModelTable DIMENSION
        USING
        IDColumn ('content_id')
        Accumulate ('title')
    ) c
    WHERE recommendation_score > 0.5
) WITH DATA;

-- Business Impact:
-- Content engagement increased by 32%
-- Time on site improved by 18 minutes per session
-- Real-time personalization at scale (10M+ users)
```

## Common Use Cases

### Customer Analytics
- **Behavioral Segmentation**: Group customers by purchase patterns, engagement, or demographics
- **Churn Prediction**: Identify at-risk segment based on declining engagement
- **Lifetime Value**: Segment by revenue potential for resource allocation
- **Personalization**: Assign users to preference clusters for content/product recommendations

### Fraud and Anomaly Detection
- **Transaction Monitoring**: Flag purchases far from normal behavior patterns
- **Network Security**: Detect unusual network traffic patterns
- **Quality Control**: Identify defective products that don't fit normal specifications
- **Healthcare**: Flag abnormal patient vitals or test results

### Product and Inventory Management
- **Product Categorization**: Auto-assign products to performance or preference clusters
- **Demand Forecasting**: Group SKUs by demand patterns for inventory optimization
- **Price Optimization**: Segment products for dynamic pricing strategies
- **Assortment Planning**: Allocate products to stores based on cluster affinity

### Operations and Logistics
- **Store Performance**: Segment locations for resource allocation
- **Route Optimization**: Cluster delivery addresses for efficient routing
- **Workforce Segmentation**: Group employees by performance for targeted development
- **Sensor Data**: Cluster IoT sensor readings for predictive maintenance

### Marketing and Content
- **Campaign Targeting**: Assign prospects to segments for personalized messaging
- **Content Recommendation**: Match users to content clusters
- **A/B Test Assignment**: Allocate users to test groups based on behavior clusters
- **Lead Scoring**: Segment leads by conversion propensity

## Best Practices

### Data Preparation
1. **Feature Scaling**: Apply same scaling (StandardScaler, MinMaxScaler) used during training
2. **Missing Values**: Impute or remove missing values before prediction (K-means requires complete data)
3. **Feature Consistency**: Ensure test data has identical feature columns as training
4. **Outlier Handling**: Consider capping extreme values to avoid skewing distance calculations

### Model Application
1. **Distance Monitoring**: Use OutputDistance to detect data drift or model degradation
2. **Cluster Interpretation**: Profile clusters on training data before applying to new data
3. **Periodic Retraining**: Retrain K-means periodically (e.g., quarterly) as patterns evolve
4. **Anomaly Thresholds**: Define distance thresholds for outlier detection based on validation data

### Performance Optimization
1. **Batch Scoring**: Use PARTITION BY ANY for parallel processing of large datasets
2. **Index ID Column**: Create index on IDColumn for faster joins
3. **Accumulate Wisely**: Only include necessary pass-through columns
4. **Small Model Table**: K-means models are compact (K rows) → fast broadcast to all AMPs

### Production Deployment
1. **Model Versioning**: Include version/date in model table names (kmeans_model_2024_Q1)
2. **A/B Testing**: Run old and new cluster models side-by-side before full cutover
3. **Monitoring**: Track cluster distribution and average distances over time
4. **Documentation**: Maintain cluster interpretation guide (what each cluster represents)

### Business Integration
1. **Cluster Profiling**: Analyze cluster characteristics on training data for actionable insights
2. **Treatment Strategies**: Define business rules for each cluster (e.g., marketing offers, pricing)
3. **Threshold Tuning**: Adjust distance thresholds for anomaly detection based on business costs
4. **Feedback Loop**: Monitor business outcomes by cluster to validate model effectiveness

## Related Functions

### Model Training
- **TD_KMeans**: Train K-means clustering models (produces ModelTable input)
- **TD_Silhouette**: Evaluate clustering quality and optimal K selection
- **TD_KMeansPlot**: Visualize cluster centroids and data distribution

### Alternative Clustering
- **TD_DBSCAN**: Density-based clustering for non-spherical clusters
- **TD_HierarchicalClustering**: Build cluster hierarchies for nested segmentation

### Model Evaluation
- **TD_Silhouette**: Calculate silhouette scores to assess cluster quality
- **TD_UnivariateStatistics**: Profile cluster characteristics
- **TD_TextAnalyzer**: Analyze text features within clusters (for content clustering)

### Data Preparation
- **TD_ScaleFit/Transform**: Standardize features for improved clustering
- **TD_SimpleImputeFit/Transform**: Handle missing values before clustering
- **TD_OutlierFilterFit/Transform**: Remove outliers before training

### Feature Engineering
- **TD_PolynomialFeaturesFit/Transform**: Create interaction terms for richer clustering
- **TD_OneHotEncodingFit/Transform**: Convert categorical variables for clustering
- **TD_PCA**: Reduce dimensionality before clustering high-dimensional data

## Notes and Limitations

### General Limitations
1. **Feature Matching**: All feature columns from training must be present in test data
2. **No Missing Values**: K-means cannot handle NULLs - preprocess data first
3. **Distance Metric**: Uses Euclidean distance (assumes spherical clusters)
4. **Feature Scale Sensitivity**: Distance calculation sensitive to feature scales - standardize features

### Clustering Characteristics
1. **K Fixed**: Number of clusters (K) is fixed from training - cannot change during prediction
2. **Hard Assignment**: Each point assigned to exactly one cluster (no fuzzy membership)
3. **Convex Clusters**: K-means assumes convex, roughly spherical clusters
4. **Centroid-Based**: Clusters defined by centroids, not by density or connectivity

### Distance and Outliers
1. **Outlier Detection**: Very large distances indicate points far from all clusters
2. **No "Unknown" Cluster**: Every point assigned to some cluster, even if poor fit
3. **Distance Threshold**: Define business-specific thresholds for outlier flagging
4. **Cluster Imbalance**: Some clusters may be much larger or smaller than others

### Performance Considerations
1. **Scalability**: Very fast prediction (linear in K, which is typically small)
2. **High Dimensions**: Performance degrades in very high-dimensional spaces (curse of dimensionality)
3. **Model Size**: Model table is small (K rows), enabling fast broadcast

### Best Use Cases
- **When to Use K-Means**: Clear cluster structure expected, spherical clusters, need interpretability
- **When to Avoid K-Means**: Non-convex clusters, varying cluster densities, unknown K
- **Alternatives**: Consider DBSCAN for density-based clustering or hierarchical clustering for nested structures

### Teradata-Specific Notes
1. **UTF8 Support**: ModelTable and InputTable support UTF8 character sets
2. **PARTITION BY ANY**: Enables parallel processing across AMPs
3. **DIMENSION Tables**: ModelTable must be DIMENSION for broadcast to all AMPs
4. **Deterministic**: Same input always produces same output (no randomness in prediction)

## Version Information

**Documentation Generated:** November 29, 2025
**Based on:** Teradata Database Analytic Functions Version 17.20
**Function Category:** Machine Learning - Model Scoring (Unsupervised Learning)
**Last Updated:** 2025-11-29
