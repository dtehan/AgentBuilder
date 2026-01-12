# TD_Silhouette

## Function Name
**TD_Silhouette**

## Description
TD_Silhouette calculates silhouette coefficients to measure clustering quality and validate how well data points are assigned to their clusters. The silhouette coefficient evaluates cluster cohesion (similarity within a cluster) and separation (dissimilarity from other clusters), providing a quantitative metric to optimize cluster count and compare clustering algorithms.

**Key Characteristics:**
- **Cluster Validation**: Measures how appropriately data is clustered
- **Cohesion vs. Separation**: Balances within-cluster similarity and between-cluster dissimilarity
- **Score Range**: Values from -1 (poorly clustered) to +1 (well clustered), 0 indicates border cases
- **Multiple Output Modes**: Overall score, per-sample scores, or per-cluster scores
- **Algorithm Agnostic**: Works with any clustering algorithm (K-Means, Hierarchical, DBSCAN, etc.)
- **Optimization Tool**: Helps identify optimal number of clusters

The silhouette coefficient ranges from -1 to 1:
- **+1**: Data point is very well matched to its cluster and poorly matched to neighboring clusters
- **0**: Data point is on the border between two clusters
- **-1**: Data point may be assigned to the wrong cluster

**Important Note:** The algorithm is O(N²) complexity, where N is the number of rows. Performance degrades significantly with large datasets.

## When to Use

### Business Applications

**Cluster Validation and Optimization:**
- Determine optimal number of clusters (K) for K-Means
- Validate clustering quality before deployment
- Compare performance of different clustering algorithms
- Identify poorly clustered data points for review
- Assess cluster stability over time

**Customer Segmentation:**
- Validate customer segment definitions
- Optimize number of customer personas
- Identify customers on segment boundaries (cross-sell opportunities)
- Compare segmentation approaches (demographic vs. behavioral)
- Monitor segment quality as customer base evolves

**Market Research:**
- Validate survey response clusters
- Optimize product positioning segments
- Identify niche market opportunities (border clusters)
- Compare segmentation methods
- Assess brand perception clustering

**Anomaly Detection:**
- Validate outlier cluster separation
- Identify ambiguous anomaly cases (score near 0)
- Optimize anomaly detection thresholds
- Compare anomaly detection methods
- Monitor detection quality over time

**Image and Document Clustering:**
- Validate image similarity clusters
- Optimize document topic modeling
- Identify ambiguous category assignments
- Compare clustering algorithms for media
- Assess content organization quality

**Healthcare and Genomics:**
- Validate patient cohort definitions
- Optimize disease subtype clustering
- Identify patients with mixed characteristics
- Compare clinical grouping methods
- Assess treatment response clustering

## Syntax

```sql
SELECT * FROM TD_Silhouette (
    ON { table | view | (query) } AS InputTable
    USING
    IdColumn ('id_column')
    ClusterIdColumn ('clusterid_column')
    TargetColumns ('column_name' [,...])
    [ OutputType ({ 'SCORE' | 'CLUSTER_SCORES' | 'SAMPLE_SCORES' }) ]
    [ Accumulate ('column_name' [,...]) ]
) AS alias;
```

## Required and Optional Elements

### Required Elements

**IdColumn:**
- Specifies the column containing unique row identifiers
- Must contain unique values for each data point
- Can be any data type (INTEGER, VARCHAR, etc.)
- Used to join silhouette scores back to original data
- Format: `IdColumn('customer_id')`

**ClusterIdColumn:**
- Specifies the column containing assigned cluster IDs
- Must be integer type (BYTEINT, SMALLINT, INTEGER, BIGINT)
- Contains the cluster assignment from clustering algorithm
- Used to group data points for cohesion calculation
- Format: `ClusterIdColumn('cluster_id')`

**TargetColumns:**
- Specifies the feature columns used for clustering
- Must be numeric types (INTEGER, DECIMAL, FLOAT, DOUBLE)
- Should match the features used in original clustering
- Can specify individual columns or ranges
- Format: `TargetColumns('age', 'income', 'score')` or `TargetColumns('[2:5]')`

### Optional Elements

**OutputType:**
- Controls the level of detail in output
- **Values:**
  - `'SCORE'`: Returns single overall average silhouette coefficient (default)
  - `'SAMPLE_SCORES'`: Returns silhouette score for each individual data point
  - `'CLUSTER_SCORES'`: Returns average silhouette score for each cluster
- **Default**: 'SCORE'
- **Use cases:**
  - SCORE: Quick overall clustering quality assessment
  - SAMPLE_SCORES: Identify specific poorly clustered points
  - CLUSTER_SCORES: Compare quality across clusters

**Accumulate:**
- Specifies columns to copy from input to output
- Only applicable when `OutputType='SAMPLE_SCORES'`
- Useful for preserving descriptive attributes
- Format: `Accumulate('customer_name', 'segment', 'date')`

## Input Specifications

### InputTable Schema

| Column | Data Type | Description | Required |
|--------|-----------|-------------|----------|
| IdColumn | Any type | Unique identifier for each data point | Yes |
| ClusterIdColumn | INTEGER types | Assigned cluster ID for each data point | Yes |
| TargetColumns | NUMERIC types | Feature columns used for distance calculations | Yes |
| Other columns | Any type | Additional columns (accumulated if specified) | No |

### Data Requirements

- **Unique identifiers**: IdColumn must contain unique values
- **Valid cluster IDs**: ClusterIdColumn must contain valid integer cluster assignments
- **No NULL values**: Target columns should not contain NULL values (may cause errors)
- **Minimum clusters**: At least 2 clusters required for meaningful silhouette scores
- **Minimum points per cluster**: Each cluster should contain at least 2 data points

## Output Specifications

### Output Schema: SCORE Mode

| Column | Data Type | Description |
|--------|-----------|-------------|
| Silhouette_Score | REAL | Overall average silhouette coefficient for entire dataset |

### Output Schema: SAMPLE_SCORES Mode

| Column | Data Type | Description |
|--------|-----------|-------------|
| [IdColumn] | Same as input | Unique identifier copied from input |
| [ClusterIdColumn] | INTEGER | Cluster ID copied from input |
| A_i | REAL | Average distance to points in same cluster (cohesion) |
| B_i | REAL | Minimum average distance to points in nearest neighbor cluster |
| Silhouette_Score | REAL | Silhouette coefficient for this data point: (B_i - A_i) / max(A_i, B_i) |
| [Accumulated columns] | Same as input | Columns specified in Accumulate clause |

### Output Schema: CLUSTER_SCORES Mode

| Column | Data Type | Description |
|--------|-----------|-------------|
| [ClusterIdColumn] | INTEGER | Cluster identifier |
| Silhouette_Score | REAL | Average silhouette coefficient for all points in this cluster |

### Interpretation of Silhouette Scores

**Score Ranges:**
- **0.71 - 1.0**: Strong, well-separated clusters
- **0.51 - 0.70**: Reasonable clustering structure
- **0.26 - 0.50**: Weak clustering structure, consider alternative K
- **< 0.25**: No substantial clustering structure found
- **Negative scores**: Data points likely assigned to wrong cluster

## Code Examples

### Example 1: Basic Clustering Validation and K Optimization
**Business Context:** E-commerce company determining optimal number of customer segments for marketing.

```sql
-- Step 1: Test different K values (2 through 10 clusters)
CREATE VOLATILE TABLE cluster_quality_comparison (
    k_value INTEGER,
    silhouette_score REAL
) ON COMMIT PRESERVE ROWS;

-- Run K-Means for K=2
CREATE TABLE customer_clusters_k2 AS (
    SELECT * FROM TD_KMeans (
        ON customer_features AS InputTable
        USING
        TargetColumns('recency_days', 'frequency', 'monetary_value', 'avg_order_value')
        K(2)
        MaxIterations(100)
        Seed(42)
    ) AS dt
) WITH DATA;

-- Calculate silhouette score for K=2
INSERT INTO cluster_quality_comparison
SELECT 2 as k_value, Silhouette_Score
FROM TD_Silhouette (
    ON customer_clusters_k2 AS InputTable
    USING
    IdColumn('customer_id')
    ClusterIdColumn('cluster_id')
    TargetColumns('recency_days', 'frequency', 'monetary_value', 'avg_order_value')
    OutputType('SCORE')
) AS dt;

-- Repeat for K=3 through K=10 (similar pattern)
-- ... [K=3, K=4, ..., K=10 clustering and scoring] ...

-- Step 2: Find optimal K
SELECT
    k_value,
    silhouette_score,
    RANK() OVER (ORDER BY silhouette_score DESC) as quality_rank
FROM cluster_quality_comparison
ORDER BY silhouette_score DESC;

-- Step 3: Analyze elbow point
SELECT
    k_value,
    silhouette_score,
    LAG(silhouette_score) OVER (ORDER BY k_value) as previous_score,
    silhouette_score - LAG(silhouette_score) OVER (ORDER BY k_value) as score_improvement,
    CASE
        WHEN ABS(silhouette_score - LAG(silhouette_score) OVER (ORDER BY k_value)) < 0.05
        THEN 'DIMINISHING_RETURNS'
        ELSE 'KEEP_INCREASING'
    END as recommendation
FROM cluster_quality_comparison
ORDER BY k_value;
```

**Sample Output:**
```
k_value | silhouette_score | quality_rank
--------|------------------|-------------
      4 |         0.623451 |            1
      3 |         0.598234 |            2
      5 |         0.567891 |            3
      2 |         0.534567 |            4
      6 |         0.489012 |            5
      7 |         0.445678 |            6
      8 |         0.412345 |            7
      9 |         0.389012 |            8
     10 |         0.367890 |            9

k_value | silhouette_score | previous_score | score_improvement | recommendation
--------|------------------|----------------|-------------------|------------------
      2 |         0.534567 |           NULL |              NULL | KEEP_INCREASING
      3 |         0.598234 |       0.534567 |          0.063667 | KEEP_INCREASING
      4 |         0.623451 |       0.598234 |          0.025217 | DIMINISHING_RETURNS
      5 |         0.567891 |       0.623451 |         -0.055560 | DIMINISHING_RETURNS
      6 |         0.489012 |       0.567891 |         -0.078879 | DIMINISHING_RETURNS
```

**Business Impact:** Identified K=4 as optimal number of customer segments with silhouette score of 0.62 (reasonable structure), indicating distinct customer personas. Analysis shows diminishing returns beyond K=4, with scores declining after peak. Recommended 4-segment strategy for marketing campaigns balancing segment differentiation and operational complexity.

---

### Example 2: Identifying Poorly Clustered Customers for Review
**Business Context:** Retail company identifying customers on segment boundaries for personalized marketing.

```sql
-- Step 1: Calculate per-customer silhouette scores
CREATE TABLE customer_segment_quality AS (
    SELECT * FROM TD_Silhouette (
        ON customer_segments AS InputTable
        USING
        IdColumn('customer_id')
        ClusterIdColumn('segment_id')
        TargetColumns('recency_days', 'frequency', 'monetary_value', 'avg_order_value', 'product_diversity')
        OutputType('SAMPLE_SCORES')
        Accumulate('customer_name', 'email', 'signup_date', 'lifetime_value')
    ) AS dt
) WITH DATA;

-- Step 2: Categorize customers by clustering quality
SELECT
    segment_id,
    CASE
        WHEN Silhouette_Score >= 0.70 THEN 'STRONG_FIT'
        WHEN Silhouette_Score >= 0.50 THEN 'GOOD_FIT'
        WHEN Silhouette_Score >= 0.25 THEN 'WEAK_FIT'
        WHEN Silhouette_Score >= 0 THEN 'BORDER_CASE'
        ELSE 'LIKELY_MISASSIGNED'
    END as fit_category,
    COUNT(*) as customer_count,
    AVG(Silhouette_Score) as avg_silhouette,
    AVG(lifetime_value) as avg_ltv
FROM customer_segment_quality
GROUP BY segment_id, fit_category
ORDER BY segment_id, fit_category;

-- Step 3: Identify border customers (potential cross-sell)
SELECT
    customer_id,
    customer_name,
    email,
    segment_id,
    Silhouette_Score,
    A_i as cohesion_distance,
    B_i as separation_distance,
    lifetime_value,
    CASE
        WHEN Silhouette_Score BETWEEN -0.1 AND 0.1 THEN 'HIGH_PRIORITY_REVIEW'
        WHEN Silhouette_Score BETWEEN 0.1 AND 0.25 THEN 'MEDIUM_PRIORITY_REVIEW'
        ELSE 'LOW_PRIORITY'
    END as review_priority
FROM customer_segment_quality
WHERE Silhouette_Score < 0.25
ORDER BY ABS(Silhouette_Score), lifetime_value DESC;

-- Step 4: Analyze misassigned high-value customers
SELECT
    cq.customer_id,
    cq.customer_name,
    cq.segment_id as assigned_segment,
    cq.Silhouette_Score,
    cq.lifetime_value,
    -- Find which cluster this customer is closest to
    (SELECT cs2.segment_id
     FROM customer_segments cs2
     WHERE cs2.customer_id != cq.customer_id
     ORDER BY SQRT(
         POWER(cs2.recency_days - cs.recency_days, 2) +
         POWER(cs2.frequency - cs.frequency, 2) +
         POWER(cs2.monetary_value - cs.monetary_value, 2)
     )
     LIMIT 1) as nearest_neighbor_segment
FROM customer_segment_quality cq
INNER JOIN customer_segments cs ON cq.customer_id = cs.customer_id
WHERE cq.Silhouette_Score < 0
    AND cq.lifetime_value > 5000
ORDER BY cq.Silhouette_Score, cq.lifetime_value DESC;
```

**Sample Output:**
```
segment_id | fit_category       | customer_count | avg_silhouette | avg_ltv
-----------|--------------------|--------------|--------------|---------
         1 | STRONG_FIT         |        3,456 |        0.823 | 4,567.89
         1 | GOOD_FIT           |        1,234 |        0.587 | 3,890.12
         1 | WEAK_FIT           |          456 |        0.342 | 3,234.56
         1 | BORDER_CASE        |          123 |        0.089 | 2,987.65
         1 | LIKELY_MISASSIGNED |           34 |       -0.234 | 5,123.45
         2 | STRONG_FIT         |        2,890 |        0.798 | 8,234.56
         2 | GOOD_FIT           |          987 |        0.612 | 7,456.78

customer_id | customer_name    | email                  | segment_id | Silhouette_Score | cohesion_distance | separation_distance | lifetime_value | review_priority
------------|------------------|------------------------|------------|------------------|-------------------|---------------------|----------------|--------------------
CUST-45678  | John Smith       | john.smith@email.com   |          2 |           0.034 |           234.56 |              245.67 |       12,345.67| HIGH_PRIORITY_REVIEW
CUST-45679  | Jane Doe         | jane.doe@email.com     |          1 |          -0.067 |           456.78 |              423.45 |        9,876.54| HIGH_PRIORITY_REVIEW
CUST-45680  | Bob Johnson      | bob.j@email.com        |          3 |           0.123 |           345.67 |              389.01 |        7,654.32| MEDIUM_PRIORITY_REVIEW

customer_id | customer_name    | assigned_segment | Silhouette_Score | lifetime_value | nearest_neighbor_segment
------------|------------------|------------------|------------------|----------------|-------------------------
CUST-45679  | Jane Doe         |                1 |           -0.234 |        9,876.54|                        3
CUST-45681  | Alice Williams   |                2 |           -0.189 |        8,234.56|                        4
CUST-45682  | Charlie Brown    |                1 |           -0.156 |        6,543.21|                        2
```

**Business Impact:** Identified 157 customers with weak cluster fit (silhouette < 0.25), including 34 high-value customers (LTV > $5K) likely misassigned to wrong segments. Flagged 45 "border case" customers (score near 0) as cross-sell opportunities exhibiting characteristics of multiple segments. Prioritized manual review of 12 high-value customers with negative scores for segment reassignment, potentially improving targeting accuracy for $115K in combined lifetime value.

---

### Example 3: Comparing Clustering Algorithms
**Business Context:** Marketing analytics team comparing K-Means vs. Hierarchical clustering for customer segmentation.

```sql
-- Step 1: Run K-Means clustering (K=5)
CREATE TABLE customers_kmeans AS (
    SELECT
        customer_id,
        cluster_id as segment_kmeans
    FROM TD_KMeans (
        ON customer_features AS InputTable
        USING
        TargetColumns('age', 'income', 'recency', 'frequency', 'monetary')
        K(5)
        MaxIterations(100)
        Seed(42)
    ) AS dt
) WITH DATA;

-- Step 2: Run Hierarchical clustering (alternative method - simulated for example)
CREATE TABLE customers_hierarchical AS (
    SELECT
        customer_id,
        hierarchical_cluster_id as segment_hierarchical
    FROM hierarchical_clustering_output  -- Assume pre-computed
) WITH DATA;

-- Step 3: Calculate silhouette scores for K-Means
CREATE TABLE kmeans_silhouette AS (
    SELECT
        'K-Means' as algorithm,
        cluster_id as segment_id,
        Silhouette_Score
    FROM TD_Silhouette (
        ON customers_kmeans
        INNER JOIN customer_features USING (customer_id)
        AS InputTable
        USING
        IdColumn('customer_id')
        ClusterIdColumn('segment_kmeans')
        TargetColumns('age', 'income', 'recency', 'frequency', 'monetary')
        OutputType('CLUSTER_SCORES')
    ) AS dt
) WITH DATA;

-- Step 4: Calculate silhouette scores for Hierarchical
CREATE TABLE hierarchical_silhouette AS (
    SELECT
        'Hierarchical' as algorithm,
        cluster_id as segment_id,
        Silhouette_Score
    FROM TD_Silhouette (
        ON customers_hierarchical
        INNER JOIN customer_features USING (customer_id)
        AS InputTable
        USING
        IdColumn('customer_id')
        ClusterIdColumn('segment_hierarchical')
        TargetColumns('age', 'income', 'recency', 'frequency', 'monetary')
        OutputType('CLUSTER_SCORES')
    ) AS dt
) WITH DATA;

-- Step 5: Compare overall performance
SELECT
    algorithm,
    COUNT(*) as cluster_count,
    AVG(Silhouette_Score) as overall_silhouette,
    MIN(Silhouette_Score) as worst_cluster,
    MAX(Silhouette_Score) as best_cluster,
    STDDEV_SAMP(Silhouette_Score) as score_variability
FROM (
    SELECT * FROM kmeans_silhouette
    UNION ALL
    SELECT * FROM hierarchical_silhouette
) combined
GROUP BY algorithm
ORDER BY overall_silhouette DESC;

-- Step 6: Side-by-side cluster quality comparison
SELECT
    km.segment_id,
    km.Silhouette_Score as kmeans_score,
    h.Silhouette_Score as hierarchical_score,
    km.Silhouette_Score - h.Silhouette_Score as score_difference,
    CASE
        WHEN ABS(km.Silhouette_Score - h.Silhouette_Score) < 0.05 THEN 'SIMILAR'
        WHEN km.Silhouette_Score > h.Silhouette_Score THEN 'KMEANS_BETTER'
        ELSE 'HIERARCHICAL_BETTER'
    END as winner
FROM kmeans_silhouette km
LEFT JOIN hierarchical_silhouette h
    ON km.segment_id = h.segment_id
ORDER BY score_difference DESC;
```

**Sample Output:**
```
algorithm     | cluster_count | overall_silhouette | worst_cluster | best_cluster | score_variability
--------------|---------------|--------------------|---------------|--------------|------------------
K-Means       |             5 |           0.612345 |      0.489012 |     0.756789 |          0.098234
Hierarchical  |             5 |           0.578901 |      0.412345 |     0.723456 |          0.112345

segment_id | kmeans_score | hierarchical_score | score_difference | winner
-----------|--------------|--------------------|-----------------|-----------------
         1 |     0.756789 |           0.598234 |         0.158555 | KMEANS_BETTER
         2 |     0.678901 |           0.656789 |         0.022112 | SIMILAR
         3 |     0.612345 |           0.723456 |        -0.111111 | HIERARCHICAL_BETTER
         4 |     0.545678 |           0.512345 |         0.033333 | SIMILAR
         5 |     0.489012 |           0.412345 |         0.076667 | KMEANS_BETTER
```

**Business Impact:** K-Means outperformed Hierarchical clustering with overall silhouette of 0.61 vs. 0.58, indicating better-defined customer segments. K-Means produced more consistent cluster quality (lower variability: 0.098 vs. 0.112) and performed better in 3 of 5 segments. Recommended K-Means for production segmentation, projected to improve campaign targeting precision by 12% based on stronger cluster separation.

---

### Example 4: Monitoring Cluster Quality Over Time
**Business Context:** SaaS company tracking customer segment stability as product features and customer base evolve.

```sql
-- Step 1: Calculate monthly silhouette scores
CREATE TABLE segment_quality_history AS (
    SELECT
        snapshot_month,
        'OVERALL' as metric_type,
        NULL as segment_id,
        Silhouette_Score
    FROM TD_Silhouette (
        ON customer_segments_monthly AS InputTable
        USING
        IdColumn('customer_id')
        ClusterIdColumn('segment_id')
        TargetColumns('feature_usage_score', 'support_tickets', 'monthly_spend', 'user_count')
        OutputType('SCORE')
    ) AS dt
    CROSS JOIN (SELECT DISTINCT snapshot_month FROM customer_segments_monthly) months

    UNION ALL

    SELECT
        snapshot_month,
        'PER_CLUSTER' as metric_type,
        cluster_id as segment_id,
        Silhouette_Score
    FROM TD_Silhouette (
        ON customer_segments_monthly AS InputTable
        USING
        IdColumn('customer_id')
        ClusterIdColumn('segment_id')
        TargetColumns('feature_usage_score', 'support_tickets', 'monthly_spend', 'user_count')
        OutputType('CLUSTER_SCORES')
    ) AS dt
    INNER JOIN customer_segments_monthly USING (segment_id)
) WITH DATA;

-- Step 2: Track overall quality trends
SELECT
    snapshot_month,
    Silhouette_Score as current_score,
    LAG(Silhouette_Score) OVER (ORDER BY snapshot_month) as previous_score,
    Silhouette_Score - LAG(Silhouette_Score) OVER (ORDER BY snapshot_month) as month_over_month_change,
    AVG(Silhouette_Score) OVER (ORDER BY snapshot_month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as rolling_3month_avg,
    CASE
        WHEN Silhouette_Score - LAG(Silhouette_Score) OVER (ORDER BY snapshot_month) < -0.05 THEN 'DEGRADING'
        WHEN Silhouette_Score - LAG(Silhouette_Score) OVER (ORDER BY snapshot_month) > 0.05 THEN 'IMPROVING'
        ELSE 'STABLE'
    END as trend
FROM segment_quality_history
WHERE metric_type = 'OVERALL'
ORDER BY snapshot_month DESC;

-- Step 3: Identify problematic segments
SELECT
    segment_id,
    MIN(Silhouette_Score) as worst_month_score,
    MAX(Silhouette_Score) as best_month_score,
    MAX(Silhouette_Score) - MIN(Silhouette_Score) as score_volatility,
    AVG(Silhouette_Score) as avg_score,
    CASE
        WHEN AVG(Silhouette_Score) < 0.40 THEN 'REQUIRES_RETRAINING'
        WHEN MAX(Silhouette_Score) - MIN(Silhouette_Score) > 0.20 THEN 'UNSTABLE_SEGMENT'
        ELSE 'HEALTHY'
    END as segment_health
FROM segment_quality_history
WHERE metric_type = 'PER_CLUSTER'
    AND snapshot_month >= ADD_MONTHS(CURRENT_DATE, -6)
GROUP BY segment_id
ORDER BY segment_health, avg_score;

-- Step 4: Alert on quality degradation
SELECT
    snapshot_month,
    segment_id,
    Silhouette_Score as current_score,
    AVG(Silhouette_Score) OVER (PARTITION BY segment_id ORDER BY snapshot_month ROWS BETWEEN 5 PRECEDING AND 1 PRECEDING) as historical_avg,
    Silhouette_Score - AVG(Silhouette_Score) OVER (PARTITION BY segment_id ORDER BY snapshot_month ROWS BETWEEN 5 PRECEDING AND 1 PRECEDING) as deviation_from_baseline,
    CASE
        WHEN Silhouette_Score < 0.30 THEN 'CRITICAL_ALERT'
        WHEN Silhouette_Score - AVG(Silhouette_Score) OVER (PARTITION BY segment_id ORDER BY snapshot_month ROWS BETWEEN 5 PRECEDING AND 1 PRECEDING) < -0.10 THEN 'WARNING_ALERT'
        ELSE 'NO_ALERT'
    END as alert_level
FROM segment_quality_history
WHERE metric_type = 'PER_CLUSTER'
    AND snapshot_month = (SELECT MAX(snapshot_month) FROM segment_quality_history)
    AND (
        Silhouette_Score < 0.30
        OR Silhouette_Score - AVG(Silhouette_Score) OVER (PARTITION BY segment_id ORDER BY snapshot_month ROWS BETWEEN 5 PRECEDING AND 1 PRECEDING) < -0.10
    )
ORDER BY alert_level, Silhouette_Score;
```

**Sample Output:**
```
snapshot_month | current_score | previous_score | month_over_month_change | rolling_3month_avg | trend
---------------|---------------|----------------|-------------------------|--------------------|-----------
    2024-11-01 |      0.598234 |       0.623451 |               -0.025217 |           0.607893 | STABLE
    2024-10-01 |      0.623451 |       0.612345 |                0.011106 |           0.615678 | STABLE
    2024-09-01 |      0.612345 |       0.656789 |               -0.044444 |           0.631528 | STABLE
    2024-08-01 |      0.656789 |       0.678901 |               -0.022112 |           0.662678 | STABLE
    2024-07-01 |      0.678901 |       0.689012 |               -0.010111 |           0.674901 | STABLE
    2024-06-01 |      0.689012 |       0.701234 |               -0.012222 |           0.689716 | STABLE

segment_id | worst_month_score | best_month_score | score_volatility | avg_score | segment_health
-----------|-------------------|------------------|------------------|-----------|-------------------
         3 |          0.289012 |         0.512345 |         0.223333 |  0.387654 | REQUIRES_RETRAINING
         5 |          0.412345 |         0.656789 |         0.244444 |  0.523456 | UNSTABLE_SEGMENT
         1 |          0.598234 |         0.756789 |         0.158555 |  0.678901 | HEALTHY
         2 |          0.545678 |         0.689012 |         0.143334 |  0.623451 | HEALTHY
         4 |          0.512345 |         0.634567 |         0.122222 |  0.578901 | HEALTHY

snapshot_month | segment_id | current_score | historical_avg | deviation_from_baseline | alert_level
---------------|------------|---------------|----------------|------------------------|----------------
    2024-11-01 |          3 |      0.289012 |       0.456789 |               -0.167777 | CRITICAL_ALERT
    2024-11-01 |          5 |      0.412345 |       0.534567 |               -0.122222 | WARNING_ALERT
```

**Business Impact:** Detected 8% degradation in overall segment quality over 6 months (from 0.70 to 0.60 silhouette score), indicating customer behavior evolution. Identified Segment 3 with critical quality drop to 0.29 (below 0.30 threshold), requiring immediate re-segmentation. Segment 5 showing high volatility (0.24 range) flagged as unstable, suggesting need for different feature selection. Recommended quarterly model retraining to maintain segment quality above 0.60 target.

---

### Example 5: Medical Patient Cohort Validation
**Business Context:** Hospital validating disease subtype clustering for personalized treatment protocols.

```sql
-- Step 1: Calculate per-patient silhouette scores for cohort validation
CREATE TABLE patient_cohort_quality AS (
    SELECT * FROM TD_Silhouette (
        ON patient_clusters AS InputTable
        USING
        IdColumn('patient_mrn')
        ClusterIdColumn('cohort_id')
        TargetColumns('age', 'bmi', 'blood_pressure_sys', 'blood_pressure_dia', 'glucose_level', 'cholesterol', 'symptom_severity_score')
        OutputType('SAMPLE_SCORES')
        Accumulate('patient_name', 'primary_diagnosis', 'comorbidity_count', 'treatment_history')
    ) AS dt
) WITH DATA;

-- Step 2: Cohort quality summary for clinical review
SELECT
    cohort_id,
    COUNT(*) as patient_count,
    AVG(Silhouette_Score) as avg_silhouette,
    MIN(Silhouette_Score) as min_silhouette,
    MAX(Silhouette_Score) as max_silhouette,
    STDDEV_SAMP(Silhouette_Score) as score_std_dev,
    SUM(CASE WHEN Silhouette_Score < 0 THEN 1 ELSE 0 END) as misassigned_patients,
    SUM(CASE WHEN Silhouette_Score BETWEEN 0 AND 0.25 THEN 1 ELSE 0 END) as borderline_patients,
    CASE
        WHEN AVG(Silhouette_Score) >= 0.60 THEN 'HIGH_CONFIDENCE'
        WHEN AVG(Silhouette_Score) >= 0.40 THEN 'MODERATE_CONFIDENCE'
        ELSE 'LOW_CONFIDENCE_REVIEW_REQUIRED'
    END as clinical_confidence
FROM patient_cohort_quality
GROUP BY cohort_id
ORDER BY avg_silhouette DESC;

-- Step 3: Identify patients requiring clinical review
SELECT
    patient_mrn,
    patient_name,
    cohort_id,
    primary_diagnosis,
    comorbidity_count,
    Silhouette_Score,
    A_i as cohort_similarity,
    B_i as nearest_cohort_distance,
    CASE
        WHEN Silhouette_Score < -0.10 THEN 'URGENT_REVIEW'
        WHEN Silhouette_Score BETWEEN -0.10 AND 0.10 THEN 'CLINICAL_REVIEW'
        WHEN Silhouette_Score BETWEEN 0.10 AND 0.30 THEN 'BORDERLINE_MONITOR'
        ELSE 'WELL_ASSIGNED'
    END as review_priority,
    CASE
        WHEN Silhouette_Score < 0 THEN 'Consider reassigning to nearest cohort based on clinical assessment'
        WHEN Silhouette_Score BETWEEN 0 AND 0.25 THEN 'Patient exhibits characteristics of multiple cohorts - personalize treatment'
        ELSE 'Standard cohort-based treatment protocol appropriate'
    END as clinical_recommendation
FROM patient_cohort_quality
WHERE Silhouette_Score < 0.30
ORDER BY Silhouette_Score, comorbidity_count DESC;

-- Step 4: Treatment outcome correlation with cluster quality
SELECT
    pcq.cohort_id,
    AVG(pcq.Silhouette_Score) as avg_silhouette,
    COUNT(*) as patient_count,
    AVG(to.treatment_effectiveness_score) as avg_treatment_effectiveness,
    AVG(to.readmission_rate_30day) as avg_readmission_rate,
    AVG(to.days_to_improvement) as avg_days_to_improvement,
    CORR(pcq.Silhouette_Score, to.treatment_effectiveness_score) as correlation_effectiveness,
    CASE
        WHEN AVG(pcq.Silhouette_Score) >= 0.60 AND AVG(to.treatment_effectiveness_score) >= 0.75 THEN 'OPTIMAL_COHORT'
        WHEN AVG(pcq.Silhouette_Score) < 0.40 THEN 'REFINE_COHORT_DEFINITION'
        ELSE 'ACCEPTABLE'
    END as cohort_status
FROM patient_cohort_quality pcq
INNER JOIN treatment_outcomes to ON pcq.patient_mrn = to.patient_mrn
GROUP BY pcq.cohort_id
ORDER BY avg_silhouette DESC, avg_treatment_effectiveness DESC;

-- Step 5: Feature importance for cohort separation
SELECT
    'age' as feature,
    STDDEV_SAMP(age) as within_cluster_std,
    AVG(CASE WHEN Silhouette_Score > 0.60 THEN age END) - AVG(CASE WHEN Silhouette_Score < 0.30 THEN age END) as separation_strength
FROM patient_cohort_quality
INNER JOIN patient_clusters USING (patient_mrn)
UNION ALL
SELECT
    'bmi' as feature,
    STDDEV_SAMP(bmi),
    AVG(CASE WHEN Silhouette_Score > 0.60 THEN bmi END) - AVG(CASE WHEN Silhouette_Score < 0.30 THEN bmi END)
FROM patient_cohort_quality
INNER JOIN patient_clusters USING (patient_mrn)
-- ... repeat for other features ...
ORDER BY ABS(separation_strength) DESC;
```

**Sample Output:**
```
cohort_id | patient_count | avg_silhouette | min_silhouette | max_silhouette | score_std_dev | misassigned_patients | borderline_patients | clinical_confidence
----------|---------------|----------------|----------------|----------------|---------------|----------------------|---------------------|------------------------
        1 |           234 |       0.687654 |       0.289012 |       0.876543 |      0.123456 |                    3 |                  12 | HIGH_CONFIDENCE
        2 |           189 |       0.623451 |       0.198765 |       0.823456 |      0.145678 |                    5 |                  18 | HIGH_CONFIDENCE
        3 |           156 |       0.545678 |       0.112345 |       0.756789 |      0.167890 |                    8 |                  23 | MODERATE_CONFIDENCE
        4 |           123 |       0.389012 |      -0.123456 |       0.689012 |      0.198765 |                   15 |                  34 | LOW_CONFIDENCE_REVIEW_REQUIRED

patient_mrn | patient_name     | cohort_id | primary_diagnosis           | comorbidity_count | Silhouette_Score | cohort_similarity | nearest_cohort_distance | review_priority | clinical_recommendation
------------|------------------|-----------|----------------------------|-------------------|------------------|-------------------|------------------------|-----------------|--------------------------------
MRN-123456  | John Doe         |         4 | Type 2 Diabetes            |                 5 |        -0.234567 |          456.789 |                 398.123 | URGENT_REVIEW   | Consider reassigning to nearest cohort...
MRN-123457  | Jane Smith       |         3 | Hypertension               |                 4 |        -0.156789 |          378.901 |                 345.678 | URGENT_REVIEW   | Consider reassigning to nearest cohort...
MRN-123458  | Bob Johnson      |         4 | Metabolic Syndrome         |                 6 |         0.067891 |          289.012 |                 298.765 | CLINICAL_REVIEW | Patient exhibits characteristics...
MRN-123459  | Alice Williams   |         2 | Cardiovascular Disease     |                 3 |         0.123456 |          234.567 |                 267.890 | BORDERLINE_MONITOR | Patient exhibits characteristics...

cohort_id | avg_silhouette | patient_count | avg_treatment_effectiveness | avg_readmission_rate | avg_days_to_improvement | correlation_effectiveness | cohort_status
----------|----------------|---------------|----------------------------|---------------------|------------------------|--------------------------|------------------
        1 |       0.687654 |           234 |                   0.834567 |                0.089 |                   12.34 |                 0.678901 | OPTIMAL_COHORT
        2 |       0.623451 |           189 |                   0.789012 |                0.123 |                   15.67 |                 0.623451 | OPTIMAL_COHORT
        3 |       0.545678 |           156 |                   0.723456 |                0.156 |                   18.90 |                 0.545678 | ACCEPTABLE
        4 |       0.389012 |           123 |                   0.612345 |                0.234 |                   24.56 |                 0.412345 | REFINE_COHORT_DEFINITION

feature                 | within_cluster_std | separation_strength
------------------------|--------------------|-----------------------
symptom_severity_score  |           12.34567 |             45.678901
glucose_level           |           23.45678 |             38.901234
bmi                     |            5.67890 |             12.345678
age                     |            8.90123 |              8.901234
```

**Business Impact:** Validated 4 patient cohorts with average silhouette of 0.56 (moderate confidence), identifying Cohort 4 requiring refinement (0.39 score, 15 misassigned patients). Strong correlation (0.68) between silhouette score and treatment effectiveness confirms clustering clinical relevance. Flagged 23 patients for urgent clinical review with negative scores, potentially improving treatment outcomes by reassigning to better-matched cohorts. Identified symptom severity and glucose as strongest discriminating features for cohort separation.

---

### Example 6: Product Recommendation Cluster Validation
**Business Context:** E-commerce platform validating product similarity clusters for recommendation engine.

```sql
-- Step 1: Calculate product cluster quality scores
CREATE TABLE product_cluster_validation AS (
    SELECT * FROM TD_Silhouette (
        ON product_embeddings_clustered AS InputTable
        USING
        IdColumn('product_sku')
        ClusterIdColumn('similarity_cluster_id')
        TargetColumns('[2:51]')  -- 50 embedding dimensions
        OutputType('SAMPLE_SCORES')
        Accumulate('product_name', 'category', 'subcategory', 'price', 'avg_rating')
    ) AS dt
) WITH DATA;

-- Step 2: Cluster quality by product category
SELECT
    category,
    COUNT(DISTINCT similarity_cluster_id) as cluster_count,
    COUNT(*) as product_count,
    AVG(Silhouette_Score) as avg_silhouette,
    MIN(Silhouette_Score) as worst_product,
    SUM(CASE WHEN Silhouette_Score < 0.30 THEN 1 ELSE 0 END) as poorly_clustered_products,
    CAST(SUM(CASE WHEN Silhouette_Score < 0.30 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 as pct_poorly_clustered
FROM product_cluster_validation
GROUP BY category
ORDER BY avg_silhouette DESC;

-- Step 3: Identify cross-category recommendation opportunities
SELECT
    pcv.product_sku,
    pcv.product_name,
    pcv.category as product_category,
    pcv.similarity_cluster_id,
    pcv.Silhouette_Score,
    pcv.price,
    -- Find dominant category in this cluster
    (SELECT category
     FROM product_cluster_validation pcv2
     WHERE pcv2.similarity_cluster_id = pcv.similarity_cluster_id
     GROUP BY category
     ORDER BY COUNT(*) DESC
     LIMIT 1) as cluster_dominant_category,
    CASE
        WHEN Silhouette_Score BETWEEN 0 AND 0.25 THEN 'CROSS_SELL_OPPORTUNITY'
        WHEN Silhouette_Score < 0 THEN 'RECONSIDER_CLUSTER'
        ELSE 'STANDARD_RECOMMENDATION'
    END as recommendation_strategy
FROM product_cluster_validation pcv
WHERE Silhouette_Score < 0.40
ORDER BY Silhouette_Score, price DESC;

-- Step 4: A/B test cluster-based recommendations
SELECT
    test_variant,
    COUNT(DISTINCT user_id) as users,
    AVG(click_through_rate) as avg_ctr,
    AVG(conversion_rate) as avg_conversion,
    AVG(avg_order_value) as avg_aov
FROM (
    SELECT
        'CONTROL_NO_CLUSTERING' as test_variant,
        user_id,
        click_through_rate,
        conversion_rate,
        avg_order_value
    FROM recommendation_performance_control

    UNION ALL

    SELECT
        'TREATMENT_SILHOUETTE_FILTERED' as test_variant,
        user_id,
        click_through_rate,
        conversion_rate,
        avg_order_value
    FROM recommendation_performance_treatment
    WHERE product_sku IN (
        SELECT product_sku
        FROM product_cluster_validation
        WHERE Silhouette_Score >= 0.50  -- Only recommend well-clustered products
    )
) combined
GROUP BY test_variant
ORDER BY avg_conversion DESC;

-- Step 5: Cluster coherence analysis
SELECT
    similarity_cluster_id,
    COUNT(*) as product_count,
    AVG(Silhouette_Score) as avg_cluster_silhouette,
    AVG(price) as avg_price,
    STDDEV_SAMP(price) as price_std_dev,
    AVG(avg_rating) as avg_rating,
    COUNT(DISTINCT category) as category_diversity,
    STRING_AGG(DISTINCT category, ', ' ORDER BY category) as categories_in_cluster,
    CASE
        WHEN AVG(Silhouette_Score) >= 0.60 AND COUNT(DISTINCT category) = 1 THEN 'HIGHLY_COHERENT'
        WHEN AVG(Silhouette_Score) >= 0.40 AND COUNT(DISTINCT category) <= 2 THEN 'COHERENT'
        WHEN COUNT(DISTINCT category) >= 4 THEN 'DIVERSE_CLUSTER'
        ELSE 'NEEDS_REFINEMENT'
    END as cluster_quality
FROM product_cluster_validation
GROUP BY similarity_cluster_id
HAVING COUNT(*) >= 10  -- Minimum cluster size
ORDER BY avg_cluster_silhouette DESC;
```

**Sample Output:**
```
category       | cluster_count | product_count | avg_silhouette | worst_product | poorly_clustered_products | pct_poorly_clustered
---------------|---------------|---------------|----------------|---------------|--------------------------|--------------------
Electronics    |            23 |         4,567 |       0.678901 |      0.123456 |                      234 |                5.12
Home & Garden  |            18 |         3,456 |       0.623451 |      0.089012 |                      189 |                5.47
Sports         |            15 |         2,890 |       0.598234 |      0.045678 |                      156 |                5.40
Clothing       |            28 |         5,678 |       0.545678 |     -0.023456 |                      456 |                8.03

product_sku | product_name              | product_category | similarity_cluster_id | Silhouette_Score | price  | cluster_dominant_category | recommendation_strategy
------------|---------------------------|------------------|----------------------|------------------|--------|--------------------------|-------------------------
PROD-12345  | Wireless Earbuds          | Electronics      |                   12 |         0.089012 | 129.99 | Electronics              | CROSS_SELL_OPPORTUNITY
PROD-12346  | Yoga Mat                  | Sports           |                    7 |         0.156789 |  39.99 | Home & Garden            | CROSS_SELL_OPPORTUNITY
PROD-12347  | Kitchen Scale             | Home & Garden    |                   15 |        -0.023456 |  24.99 | Electronics              | RECONSIDER_CLUSTER

test_variant                    | users  | avg_ctr  | avg_conversion | avg_aov
--------------------------------|--------|----------|----------------|----------
TREATMENT_SILHOUETTE_FILTERED   | 25,678 | 0.089012 |       0.034567 |   89.99
CONTROL_NO_CLUSTERING           | 25,890 | 0.067890 |       0.028901 |   82.34

similarity_cluster_id | product_count | avg_cluster_silhouette | avg_price | price_std_dev | avg_rating | category_diversity | categories_in_cluster              | cluster_quality
----------------------|---------------|------------------------|-----------|---------------|------------|-------------------|-----------------------------------|------------------
                   12 |           234 |               0.756789 |    149.99 |         23.45 |       4.56 |                  1 | Electronics                       | HIGHLY_COHERENT
                    7 |           189 |               0.689012 |     89.99 |         45.67 |       4.34 |                  2 | Home & Garden, Sports             | COHERENT
                   15 |           156 |               0.623451 |    129.99 |         67.89 |       4.23 |                  2 | Electronics, Home & Garden        | COHERENT
                   23 |            98 |               0.412345 |    199.99 |         89.01 |       4.12 |                  4 | Clothing, Electronics, Home, Sports| NEEDS_REFINEMENT
```

**Business Impact:** Validated 84 product similarity clusters with average silhouette of 0.61 (reasonable structure), enabling accurate product recommendations. A/B test showed recommendations filtered by silhouette (>0.50) increased CTR by 31% (0.089 vs. 0.068) and conversion by 20% (0.035 vs. 0.029). Identified 456 poorly clustered products (8% of catalog) for manual review and re-embedding. Flagged Cluster 23 with low coherence (0.41 score, 4 categories) for refinement, while 12 "highly coherent" clusters drive 65% of successful recommendations with silhouette >0.75.

---

## Common Use Cases

### By Industry

**Retail & E-commerce:**
- Customer segmentation validation
- Product similarity cluster quality
- Market basket analysis optimization
- Store clustering for merchandising
- Pricing tier validation

**Financial Services:**
- Customer risk segmentation
- Fraud pattern clustering validation
- Credit scoring group optimization
- Trading strategy cluster quality
- Portfolio diversification validation

**Healthcare:**
- Patient cohort validation
- Disease subtype clustering
- Treatment response group quality
- Clinical trial stratification
- Medical imaging cluster validation

**Marketing & Advertising:**
- Audience segment optimization
- Campaign targeting cluster quality
- Persona definition validation
- Channel affinity clustering
- Content recommendation cluster validation

**Telecommunications:**
- Customer churn segment validation
- Network usage pattern clustering
- Service package optimization
- Geographic coverage clustering
- Device affinity group quality

**Manufacturing:**
- Product defect pattern validation
- Equipment failure mode clustering
- Supply chain network optimization
- Quality control tier validation
- Maintenance strategy clustering

### By Analytics Task

**Clustering Optimization:**
- Determine optimal K for K-Means
- Compare clustering algorithms
- Validate hierarchical cut-off points
- Assess DBSCAN epsilon parameter
- Optimize spectral clustering parameters

**Model Validation:**
- Validate unsupervised learning results
- Assess clustering stability
- Identify outlier clusters
- Compare feature engineering approaches
- Monitor clustering quality over time

**Business Strategy:**
- Validate market segmentation
- Assess customer persona definitions
- Optimize resource allocation by segment
- Identify cross-sell opportunities
- Prioritize segment-specific strategies

**Data Quality:**
- Identify mislabeled data
- Detect data collection issues
- Validate data preprocessing
- Assess feature importance
- Monitor data drift

## Best Practices

### Cluster Quality Assessment

**1. Interpret Silhouette Scores Correctly:**

**Score Ranges:**
- **0.71 - 1.0**: Strong, well-separated clusters - ideal for production
- **0.51 - 0.70**: Reasonable clustering structure - acceptable for most applications
- **0.26 - 0.50**: Weak structure - consider alternative K or features
- **0.00 - 0.25**: Minimal structure - re-evaluate approach
- **Negative**: Likely misassigned - critical review needed

**2. Use Multiple Output Modes:**
```sql
-- Overall assessment
SELECT Silhouette_Score FROM TD_Silhouette(...) OutputType('SCORE');

-- Per-cluster comparison
SELECT cluster_id, Silhouette_Score FROM TD_Silhouette(...) OutputType('CLUSTER_SCORES');

-- Identify specific problem points
SELECT id, Silhouette_Score FROM TD_Silhouette(...) OutputType('SAMPLE_SCORES') WHERE Silhouette_Score < 0.25;
```

**3. Compare Across K Values:**
- Test K from 2 to 10 (or higher)
- Plot silhouette scores vs. K
- Look for "elbow" where improvement diminishes
- Balance score with interpretability

**4. Consider Domain Knowledge:**
- Silhouette scores are quantitative, not definitive
- Integrate business context and domain expertise
- Lower scores may be acceptable if clusters are interpretable
- Higher scores don't guarantee business value

### Performance Optimization

**1. Manage O(N²) Complexity:**
```sql
-- Sample large datasets
CREATE TABLE customer_sample AS (
    SELECT * FROM customers
    SAMPLE 10000  -- Limit to manageable size
) WITH DATA;

-- Calculate silhouette on sample
SELECT * FROM TD_Silhouette (
    ON customer_sample AS InputTable
    ...
) AS dt;
```

**2. Performance Guidelines:**
- **< 10K rows**: Fast execution, full dataset recommended
- **10K - 50K rows**: Moderate execution time, consider sampling
- **50K - 100K rows**: Slow execution, sampling recommended
- **> 100K rows**: Very slow, definitely sample or use CLUSTER_SCORES mode only

**3. Use Appropriate Output Mode:**
- `SCORE`: Fastest, single metric
- `CLUSTER_SCORES`: Moderate, per-cluster metrics
- `SAMPLE_SCORES`: Slowest, per-point metrics (avoid for large datasets)

**4. Optimize for Repeated Analysis:**
```sql
-- Pre-compute and store per-sample scores once
CREATE TABLE silhouette_cache AS (
    SELECT * FROM TD_Silhouette (
        ON clusters AS InputTable
        USING
        IdColumn('id')
        ClusterIdColumn('cluster_id')
        TargetColumns('f1', 'f2', 'f3')
        OutputType('SAMPLE_SCORES')
    ) AS dt
) WITH DATA;

-- Then query cached scores repeatedly
SELECT AVG(Silhouette_Score) FROM silhouette_cache WHERE cluster_id = 1;
```

### Validation and Monitoring

**1. Validate Results:**
```sql
-- Check for data quality issues
SELECT
    COUNT(*) as total_points,
    COUNT(DISTINCT cluster_id) as cluster_count,
    MIN(cluster_id) as min_cluster,
    MAX(cluster_id) as max_cluster,
    SUM(CASE WHEN cluster_id IS NULL THEN 1 ELSE 0 END) as null_clusters
FROM clusters;

-- Verify minimum cluster sizes
SELECT
    cluster_id,
    COUNT(*) as cluster_size
FROM clusters
GROUP BY cluster_id
HAVING COUNT(*) < 2;  -- Flag singleton clusters
```

**2. Track Over Time:**
- Calculate silhouette scores monthly/quarterly
- Monitor for degradation (score drops > 0.05)
- Set alerts for scores below thresholds
- Document and investigate sudden changes

**3. Cross-Validate with Business Metrics:**
```sql
-- Correlate silhouette with business outcomes
SELECT
    cluster_id,
    AVG(silhouette_score) as avg_silhouette,
    AVG(customer_lifetime_value) as avg_ltv,
    AVG(conversion_rate) as avg_conversion,
    CORR(silhouette_score, customer_lifetime_value) as correlation
FROM silhouette_scores
INNER JOIN business_metrics USING (customer_id)
GROUP BY cluster_id;
```

**4. Document Decisions:**
- Record K selection rationale
- Document silhouette score thresholds
- Maintain change log for model updates
- Include silhouette scores in model cards

### Production Implementation

**1. Automate Cluster Validation:**
```sql
-- Create validation pipeline
CREATE PROCEDURE validate_clustering()
BEGIN
    -- Calculate current silhouette
    CREATE VOLATILE TABLE current_silhouette AS (
        SELECT * FROM TD_Silhouette (...)
    ) WITH DATA;

    -- Compare to baseline
    SELECT
        CASE
            WHEN cs.silhouette_score < bl.silhouette_score - 0.10 THEN 'RETRAIN_REQUIRED'
            WHEN cs.silhouette_score < bl.silhouette_score - 0.05 THEN 'MONITOR_CLOSELY'
            ELSE 'ACCEPTABLE'
        END as status
    FROM current_silhouette cs
    CROSS JOIN baseline_silhouette bl;
END;
```

**2. Set Quality Gates:**
- Minimum silhouette score for deployment (e.g., 0.40)
- Maximum percentage of negative scores (e.g., < 5%)
- Minimum average cluster score (e.g., 0.50)
- Alert thresholds for monitoring

**3. Handle Edge Cases:**
- Singleton clusters (only 1 member): silhouette = 0
- Two-cluster solutions: may show artificially high scores
- Very large K: scores may decrease even if structure improves
- Imbalanced cluster sizes: weight scores by cluster size

**4. Integrate with MLOps:**
- Include silhouette in model evaluation
- Track as model quality metric
- Use in A/B testing comparisons
- Report in model performance dashboards

## Related Functions

### Clustering Functions
- **TD_KMeans**: K-Means clustering algorithm
- **TD_KMeansPredict**: Apply trained K-Means model
- Additional clustering algorithms (external to Teradata)

### Model Evaluation
- **TD_ClassificationEvaluator**: Classification model metrics
- **TD_RegressionEvaluator**: Regression model metrics
- **TD_ROC**: ROC curves for binary classification
- **TD_TrainTestSplit**: Split data for validation

### Data Exploration
- **TD_UnivariateStatistics**: Calculate feature statistics
- **TD_ColumnSummary**: Summarize data distributions
- **TD_Histogram**: Visualize data distributions

### Data Preparation
- **TD_ScaleFit / TD_ScaleTransform**: Normalize features before clustering
- **TD_OutlierFilterFit / TD_OutlierFilterTransform**: Handle outliers
- **TD_SimpleImputeFit / TD_SimpleImputeTransform**: Handle missing values

## Notes and Limitations

### Important Considerations

**1. Computational Complexity:**
- Algorithm is O(N²) where N is number of data points
- Performance degrades significantly with large datasets
- 100K rows may take hours to process
- Strongly recommend sampling for > 50K rows
- Consider CLUSTER_SCORES mode for large datasets (faster than SAMPLE_SCORES)

**2. Distance Metric:**
- Uses Euclidean distance for calculations
- Sensitive to feature scaling (normalize features first)
- May not be appropriate for categorical features
- Consider feature engineering for mixed data types

**3. Cluster Size Requirements:**
- Each cluster must have at least 2 data points
- Singleton clusters produce silhouette = 0
- Very small clusters may show inflated scores
- Imbalanced cluster sizes affect interpretation

**4. Score Interpretation:**
- High score doesn't guarantee business value
- Domain knowledge essential for validation
- Compare across multiple clustering solutions
- Consider interpretability alongside scores

**5. Sensitivity to Outliers:**
- Outliers can significantly affect scores
- Consider outlier removal before clustering
- Outlier clusters may show artificially low scores
- Use in combination with other validation methods

**6. Feature Selection Impact:**
- Silhouette scores depend on chosen features
- Different feature sets produce different scores
- Test multiple feature combinations
- Document feature selection rationale

### Technical Constraints

**1. Data Type Requirements:**
- IdColumn: Any data type
- ClusterIdColumn: Integer types only (BYTEINT, SMALLINT, INTEGER, BIGINT)
- TargetColumns: Numeric types only (INTEGER, DECIMAL, FLOAT, DOUBLE)
- No support for categorical clustering features

**2. NULL Handling:**
- NULL values in TargetColumns may cause errors
- NULL cluster IDs will be excluded from analysis
- Impute or remove NULLs before calculation
- Document NULL handling approach

**3. Memory and Resource Usage:**
- Distance matrix stored in memory: O(N²) space
- Large datasets may exhaust memory
- Consider batch processing for very large datasets
- Monitor spool space usage

**4. Output Modes:**
- SCORE: Single row output (fastest)
- CLUSTER_SCORES: One row per cluster (moderate)
- SAMPLE_SCORES: One row per input row (slowest)
- Accumulate only works with SAMPLE_SCORES mode

### Best Practices Summary

1. **Sample large datasets** (> 50K rows) to manage O(N²) complexity
2. **Normalize features** before clustering to ensure fair distance calculations
3. **Test multiple K values** (2-10+) to find optimal cluster count
4. **Use CLUSTER_SCORES mode** for large datasets instead of SAMPLE_SCORES
5. **Interpret scores with domain knowledge**, not in isolation
6. **Compare across algorithms** to find best clustering approach
7. **Monitor scores over time** to detect clustering quality degradation
8. **Set quality thresholds** for production deployment (e.g., > 0.40)
9. **Handle edge cases** like singleton clusters and imbalanced sizes
10. **Integrate with business metrics** to validate clustering value

## Version Information

- **Teradata Vantage Version**: 17.20
- **Function Category**: Model Evaluation
- **Documentation Generated**: November 2024
- **Complexity**: O(N²) - Performance sensitive to dataset size
