---
name: Clustering Model Workflow
allowed-tools:
description: Complete workflow for building clustering models in Teradata
argument-hint: [database_name] [table_name] [num_clusters]
---

# Clustering Model Workflow

## Overview
This workflow guides you through building, training, evaluating, and deploying clustering models in Teradata. Clustering is an unsupervised learning technique used to discover natural groupings in data without predefined labels.

## Variables
DATABASE_NAME: $1
TABLE_NAME: $2
NUM_CLUSTERS: $3 (optional - will be determined if not provided)

## Prerequisites
- **Data must be ML-ready**: Use @ml/ml_dataPreparation.md first
- All features should be numeric (scaled)
- No target column required (unsupervised learning)
- Features should be normalized for distance-based clustering

## Clustering Use Cases

### Customer Segmentation
- Customer behavior groups
- Purchase pattern clustering
- Customer lifetime value segments
- Product preference groups
- Channel preference clustering

### Market Segmentation
- Geographic market segments
- Demographic grouping
- Psychographic segmentation
- Product market segments
- Pricing tier optimization

### Anomaly Detection via Clustering
- Identify outlier data points
- Detect unusual patterns
- Find rare customer behaviors
- Network traffic anomalies

### Pattern Discovery
- Transaction pattern grouping
- Usage pattern identification
- Operational efficiency clusters
- Resource utilization patterns
- Time-series pattern detection

### Data Exploration and Analysis
- Understand data structure
- Feature relationship discovery
- Dimensionality reduction preparation
- Data preprocessing for supervised learning

## Workflow Stages

### Stage 0: Data Preparation Check

**Verify data is ML-ready:**
```sql
-- Check if data prep has been completed
SELECT COUNT(*) as total_rows,
       COUNT(DISTINCT dataset_split) as has_split,
       COUNT(*) as feature_count
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready;

-- Check feature distributions
SELECT
    COUNT(*) as row_count,
    COUNT(DISTINCT row_id) as unique_ids
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN';
```

**If data is not prepared:**
- Route to: @ml/ml_dataPreparation.md
- Arguments: ${DATABASE_NAME} ${TABLE_NAME}
- Note: No target column needed for clustering

### Stage 1: Problem Definition

**Define Clustering Problem:**

1. **Determine Number of Features:**
```sql
-- Count and list features for clustering
SELECT COUNT(*) as feature_count
FROM information_schema.columns
WHERE table_schema = '${DATABASE_NAME}'
  AND table_name = '${TABLE_NAME}_ml_ready'
  AND column_name NOT IN ('row_id', 'dataset_split');
```

2. **Analyze Feature Scales:**
```sql
-- Check if features are properly scaled (important for K-Means)
SELECT
    MIN(feature_1) as min_f1, MAX(feature_1) as max_f1, STDDEV_POP(feature_1) as std_f1,
    MIN(feature_2) as min_f2, MAX(feature_2) as max_f2, STDDEV_POP(feature_2) as std_f2,
    MIN(feature_3) as min_f3, MAX(feature_3) as max_f3, STDDEV_POP(feature_3) as std_f3
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN';
```

**Scaling Requirement:**
- All features should have similar scales (mean ~0, std ~1)
- If not scaled, return to data preparation for standardization
- K-Means is sensitive to feature scales

3. **Define Business Objective:**
- How many segments are needed? (if known)
- What is the business goal? (targeting, personalization, analysis)
- Are cluster characteristics interpretable?
- Will clusters be used for downstream modeling?

### Stage 2: Determining Optimal Number of Clusters

**Decision: Is K (number of clusters) known?**

**Ask User:**
"Do you know how many clusters you need?
1. **Yes** - I know the number of clusters (${NUM_CLUSTERS})
2. **No** - Help me find the optimal number using Elbow Method
3. **Explore** - Test multiple values and compare"

**User Response Handling:**
- **Option 1**: Proceed with ${NUM_CLUSTERS}
- **Option 2**: Use Elbow Method to find optimal K
- **Option 3**: Train multiple models with different K values

#### Option A: Elbow Method (Find Optimal K)

```sql
-- Test K values from 2 to 10
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_elbow_analysis AS
WITH k_values AS (
    SELECT k_value
    FROM (
        SELECT 2 as k_value UNION ALL
        SELECT 3 UNION ALL
        SELECT 4 UNION ALL
        SELECT 5 UNION ALL
        SELECT 6 UNION ALL
        SELECT 7 UNION ALL
        SELECT 8 UNION ALL
        SELECT 9 UNION ALL
        SELECT 10
    ) k
)
SELECT
    k_value,
    within_ss,
    between_ss,
    total_ss,
    within_ss / total_ss as variance_ratio
FROM (
    SELECT
        kv.k_value,
        kmeans.within_cluster_sum_squares as within_ss,
        kmeans.between_cluster_sum_squares as between_ss,
        kmeans.total_sum_squares as total_ss
    FROM k_values kv,
         LATERAL (
             SELECT TD_KMeans(
                 K(kv.k_value),
                 MaxIterations(100),
                 Seed(42)
             )
             FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
             WHERE dataset_split = 'TRAIN'
         ) kmeans
)
ORDER BY k_value
WITH DATA;

-- Analyze elbow curve
SELECT
    k_value,
    within_ss,
    variance_ratio,
    LAG(variance_ratio) OVER (ORDER BY k_value) - variance_ratio as improvement
FROM ${DATABASE_NAME}.${TABLE_NAME}_elbow_analysis
ORDER BY k_value;
```

**Elbow Method Interpretation:**
- Plot K vs. Within-Cluster Sum of Squares
- Look for "elbow" point where improvement diminishes
- Optimal K is where curve bends (marginal improvement decreases)
- Balance between cluster count and explained variance

**Decision Rule:**
- Choose K where improvement drops below 10-15%
- Consider business constraints (too many/few clusters)
- Validate with Silhouette Score

### Stage 3: Model Training

#### Train K-Means Clustering Model

```sql
-- Train K-Means with optimal K
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_kmeans_model AS
SELECT TD_KMeans(
    K(${NUM_CLUSTERS}),          -- Number of clusters
    MaxIterations(100),           -- Maximum iterations for convergence
    Tolerance(0.001),             -- Convergence threshold
    Seed(42),                     -- Random seed for reproducibility
    InitMethod('kmeans++')        -- Initialization method (kmeans++ is best)
)
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN'
WITH DATA;
```

**Hyperparameter Guidance:**
- **K**: 2-20 (determined by elbow method or business need)
- **MaxIterations**: 100-300 (ensure convergence)
- **InitMethod**: 'kmeans++' (better than 'random')
- **Tolerance**: 0.001-0.0001 (convergence precision)
- **Seed**: Fixed number for reproducibility

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_kmeans.md

#### Alternative: Try Multiple K Values

```sql
-- Train models with K=3, 4, 5
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_kmeans_k3 AS
SELECT TD_KMeans(K(3), MaxIterations(100), Seed(42))
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN'
WITH DATA;

CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_kmeans_k4 AS
SELECT TD_KMeans(K(4), MaxIterations(100), Seed(42))
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN'
WITH DATA;

CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_kmeans_k5 AS
SELECT TD_KMeans(K(5), MaxIterations(100), Seed(42))
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN'
WITH DATA;
```

### Stage 4: Cluster Assignment (Predictions)

#### Assign Clusters to Data Points

```sql
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_clustered AS
SELECT
    t.*,
    p.cluster_id,
    p.distance as distance_to_centroid
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready t,
     TD_KMeansPredict(
         ModelTable(${DATABASE_NAME}.${TABLE_NAME}_kmeans_model)
     ) p
WHERE t.dataset_split = 'TRAIN'
WITH DATA;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_kmeanspredict.md

#### Assign Test Data to Clusters

```sql
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_test_clustered AS
SELECT
    t.*,
    p.cluster_id,
    p.distance as distance_to_centroid
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready t,
     TD_KMeansPredict(
         ModelTable(${DATABASE_NAME}.${TABLE_NAME}_kmeans_model)
     ) p
WHERE t.dataset_split = 'TEST'
WITH DATA;
```

### Stage 5: Model Evaluation

#### Silhouette Score (Cluster Quality)

```sql
-- Calculate Silhouette Score to evaluate clustering quality
SELECT
    'K=${NUM_CLUSTERS}' as model,
    metrics.*
FROM TD_Silhouette(
    ClusterColumn('cluster_id'),
    Metric('euclidean')
) metrics,
${DATABASE_NAME}.${TABLE_NAME}_clustered;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_silhouette.md

**Silhouette Score Interpretation:**
- **0.71 - 1.0**: Strong structure - excellent clustering
- **0.51 - 0.70**: Reasonable structure - good clustering
- **0.26 - 0.50**: Weak structure - some clustering
- **< 0.25**: No substantial structure - poor clustering

#### Per-Cluster Silhouette Analysis

```sql
-- Analyze silhouette score by cluster
SELECT
    cluster_id,
    COUNT(*) as cluster_size,
    AVG(silhouette_score) as avg_silhouette,
    MIN(silhouette_score) as min_silhouette,
    MAX(silhouette_score) as max_silhouette
FROM ${DATABASE_NAME}.${TABLE_NAME}_clustered c,
     TD_Silhouette(
         ClusterColumn('cluster_id'),
         Metric('euclidean')
     ) s
GROUP BY cluster_id
ORDER BY cluster_id;
```

**Interpretation:**
- Clusters with low avg silhouette may need refinement
- High variation in silhouette suggests heterogeneous clusters
- Negative silhouette scores indicate misassigned points

#### Cluster Size Distribution

```sql
-- Analyze cluster sizes
SELECT
    cluster_id,
    COUNT(*) as cluster_size,
    CAST(COUNT(*) AS FLOAT) / SUM(COUNT(*)) OVER () * 100 as percentage,
    AVG(distance_to_centroid) as avg_distance,
    MAX(distance_to_centroid) as max_distance
FROM ${DATABASE_NAME}.${TABLE_NAME}_clustered
GROUP BY cluster_id
ORDER BY cluster_size DESC;
```

**Look For:**
- Relatively balanced cluster sizes (unless expected)
- Very small clusters (<5%) may be outliers
- Very large clusters (>50%) may need more segments

#### Within-Cluster Sum of Squares

```sql
-- Extract clustering metrics from model
SELECT
    'K=${NUM_CLUSTERS}' as configuration,
    total_sum_squares,
    within_cluster_sum_squares,
    between_cluster_sum_squares,
    within_cluster_sum_squares / total_sum_squares as variance_ratio,
    between_cluster_sum_squares / total_sum_squares as explained_variance
FROM ${DATABASE_NAME}.${TABLE_NAME}_kmeans_model;
```

**Metrics Interpretation:**
- **Variance Ratio**: Lower is better (compact clusters)
- **Explained Variance**: Higher is better (well-separated clusters)
- Target: Variance ratio < 0.3, Explained variance > 0.7

#### Compare Multiple K Values

```sql
-- Compare different K configurations
SELECT
    'K=3' as model,
    between_cluster_sum_squares / total_sum_squares as explained_variance
FROM ${DATABASE_NAME}.${TABLE_NAME}_kmeans_k3

UNION ALL

SELECT
    'K=4' as model,
    between_cluster_sum_squares / total_sum_squares as explained_variance
FROM ${DATABASE_NAME}.${TABLE_NAME}_kmeans_k4

UNION ALL

SELECT
    'K=5' as model,
    between_cluster_sum_squares / total_sum_squares as explained_variance
FROM ${DATABASE_NAME}.${TABLE_NAME}_kmeans_k5

ORDER BY explained_variance DESC;
```

### Stage 6: Cluster Interpretation and Profiling

#### Cluster Centroids Analysis

```sql
-- Extract and analyze cluster centroids
SELECT
    cluster_id,
    feature_name,
    centroid_value
FROM ${DATABASE_NAME}.${TABLE_NAME}_kmeans_model
ORDER BY cluster_id, feature_name;
```

#### Cluster Characteristics

```sql
-- Profile each cluster by feature averages
SELECT
    cluster_id,
    COUNT(*) as cluster_size,
    AVG(feature_1) as avg_feature_1,
    AVG(feature_2) as avg_feature_2,
    AVG(feature_3) as avg_feature_3,
    AVG(feature_4) as avg_feature_4,
    AVG(feature_5) as avg_feature_5,
    STDDEV_POP(feature_1) as std_feature_1,
    STDDEV_POP(feature_2) as std_feature_2
FROM ${DATABASE_NAME}.${TABLE_NAME}_clustered
GROUP BY cluster_id
ORDER BY cluster_id;
```

#### Cluster Naming and Business Interpretation

```sql
-- Create business-friendly cluster names based on characteristics
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_cluster_profiles AS
SELECT
    cluster_id,
    CASE
        WHEN cluster_id = 0 AND avg_spend > 1000 THEN 'High Value Customers'
        WHEN cluster_id = 1 AND avg_frequency < 5 THEN 'Occasional Buyers'
        WHEN cluster_id = 2 THEN 'Regular Customers'
        -- Add more business logic based on your features
        ELSE 'Cluster_' || CAST(cluster_id AS VARCHAR(10))
    END as cluster_name,
    cluster_description,
    COUNT(*) as size
FROM (
    SELECT
        cluster_id,
        AVG(spend_amount) as avg_spend,
        AVG(purchase_frequency) as avg_frequency,
        'Description based on characteristics' as cluster_description
    FROM ${DATABASE_NAME}.${TABLE_NAME}_clustered
    GROUP BY cluster_id
)
GROUP BY cluster_id, cluster_name, cluster_description
ORDER BY cluster_id
WITH DATA;
```

#### Compare Clusters Across Key Dimensions

```sql
-- Comparative analysis across clusters
WITH cluster_stats AS (
    SELECT
        cluster_id,
        AVG(revenue) as avg_revenue,
        AVG(recency) as avg_recency,
        AVG(frequency) as avg_frequency,
        AVG(tenure) as avg_tenure
    FROM ${DATABASE_NAME}.${TABLE_NAME}_clustered
    GROUP BY cluster_id
),
overall_stats AS (
    SELECT
        AVG(revenue) as overall_avg_revenue,
        AVG(recency) as overall_avg_recency,
        AVG(frequency) as overall_avg_frequency,
        AVG(tenure) as overall_avg_tenure
    FROM ${DATABASE_NAME}.${TABLE_NAME}_clustered
)
SELECT
    c.cluster_id,
    c.avg_revenue,
    (c.avg_revenue - o.overall_avg_revenue) / o.overall_avg_revenue * 100 as revenue_vs_avg_pct,
    c.avg_frequency,
    (c.avg_frequency - o.overall_avg_frequency) / o.overall_avg_frequency * 100 as frequency_vs_avg_pct
FROM cluster_stats c, overall_stats o
ORDER BY c.cluster_id;
```

#### Identify Cluster Outliers

```sql
-- Find data points far from their cluster centroid (potential outliers)
SELECT
    cluster_id,
    row_id,
    distance_to_centroid,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY distance_to_centroid) OVER (PARTITION BY cluster_id) as p95_distance
FROM ${DATABASE_NAME}.${TABLE_NAME}_clustered
QUALIFY distance_to_centroid > p95_distance
ORDER BY distance_to_centroid DESC;
```

### Stage 7: Production Deployment

#### Create Cluster Assignment View

```sql
-- Production view for cluster assignment
CREATE VIEW ${DATABASE_NAME}.${TABLE_NAME}_cluster_assigned AS
SELECT
    t.*,
    p.cluster_id,
    p.distance as distance_to_centroid,
    cp.cluster_name,
    cp.cluster_description,
    CURRENT_TIMESTAMP as assignment_timestamp
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready t,
     TD_KMeansPredict(
         ModelTable(${DATABASE_NAME}.${TABLE_NAME}_kmeans_model)
     ) p,
     ${DATABASE_NAME}.${TABLE_NAME}_cluster_profiles cp
WHERE p.cluster_id = cp.cluster_id;
```

#### Batch Cluster Assignment

```sql
-- Assign new data to existing clusters
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_new_assignments AS
SELECT
    new_data.*,
    p.cluster_id,
    p.distance as distance_to_centroid,
    cp.cluster_name,
    CURRENT_DATE as assignment_date
FROM ${DATABASE_NAME}.${TABLE_NAME}_new_data new_data,
     TD_KMeansPredict(
         ModelTable(${DATABASE_NAME}.${TABLE_NAME}_kmeans_model)
     ) p,
     ${DATABASE_NAME}.${TABLE_NAME}_cluster_profiles cp
WHERE p.cluster_id = cp.cluster_id
WITH DATA;
```

#### Monitor Cluster Stability

```sql
-- Track cluster distribution over time
SELECT
    assignment_date,
    cluster_id,
    cluster_name,
    COUNT(*) as assignment_count,
    AVG(distance_to_centroid) as avg_distance
FROM ${DATABASE_NAME}.${TABLE_NAME}_new_assignments
GROUP BY assignment_date, cluster_id, cluster_name
ORDER BY assignment_date, cluster_id;
```

#### Cluster Migration Analysis

```sql
-- Track how entities move between clusters over time
WITH current_assignments AS (
    SELECT entity_id, cluster_id as current_cluster
    FROM ${DATABASE_NAME}.${TABLE_NAME}_new_assignments
    WHERE assignment_date = CURRENT_DATE
),
previous_assignments AS (
    SELECT entity_id, cluster_id as previous_cluster
    FROM ${DATABASE_NAME}.${TABLE_NAME}_new_assignments
    WHERE assignment_date = CURRENT_DATE - 30
)
SELECT
    c.current_cluster,
    p.previous_cluster,
    COUNT(*) as migration_count,
    CAST(COUNT(*) AS FLOAT) / SUM(COUNT(*)) OVER () * 100 as percentage
FROM current_assignments c
LEFT JOIN previous_assignments p ON c.entity_id = p.entity_id
GROUP BY c.current_cluster, p.previous_cluster
ORDER BY migration_count DESC;
```

#### Alerting on Cluster Drift

```sql
-- Alert if cluster distributions change significantly
WITH recent_distribution AS (
    SELECT
        cluster_id,
        COUNT(*) as recent_count,
        CAST(COUNT(*) AS FLOAT) / SUM(COUNT(*)) OVER () as recent_pct
    FROM ${DATABASE_NAME}.${TABLE_NAME}_new_assignments
    WHERE assignment_date >= CURRENT_DATE - 7
    GROUP BY cluster_id
),
baseline_distribution AS (
    SELECT
        cluster_id,
        COUNT(*) as baseline_count,
        CAST(COUNT(*) AS FLOAT) / SUM(COUNT(*)) OVER () as baseline_pct
    FROM ${DATABASE_NAME}.${TABLE_NAME}_clustered
    GROUP BY cluster_id
)
SELECT
    r.cluster_id,
    r.recent_pct,
    b.baseline_pct,
    ABS(r.recent_pct - b.baseline_pct) as distribution_change,
    CASE WHEN ABS(r.recent_pct - b.baseline_pct) > 0.10
         THEN 'ALERT: Significant Drift'
         ELSE 'Normal' END as status
FROM recent_distribution r
JOIN baseline_distribution b ON r.cluster_id = b.cluster_id
ORDER BY distribution_change DESC;
```

## Decision Guides

### When to Retrain Model

Retrain if:
- **Cluster distribution shifts** >10% from baseline
- **Average distance to centroids increases** significantly
- **New feature patterns emerge** in the data
- **Business segments change** (new products, markets)
- **Silhouette score drops** below acceptable threshold
- **Time-based**: Every 6-12 months for most use cases

### Choosing Number of Clusters (K)

**Use Elbow Method when:**
- No business constraint on number of segments
- Exploratory analysis phase
- Want data-driven decision

**Use Business-Driven K when:**
- Existing segment structure
- Marketing campaign tiers
- Operational constraints (e.g., 3 service tiers)
- Resource allocation limits

**Use Multiple K Comparison when:**
- Uncertain about optimal number
- Want to evaluate trade-offs
- Need stakeholder buy-in

### Interpreting Cluster Quality

**Silhouette Score > 0.7:**
- Excellent clustering
- Proceed with confidence
- Clusters are well-separated and compact

**Silhouette Score 0.5-0.7:**
- Good clustering
- Acceptable for most use cases
- Validate business interpretability

**Silhouette Score 0.25-0.5:**
- Weak clustering
- Consider different K value
- May need feature engineering
- Evaluate business value

**Silhouette Score < 0.25:**
- Poor clustering
- Data may not have natural clusters
- Try different features or algorithms
- Consider hierarchical clustering

### Feature Selection for Clustering

**Include features that:**
- Represent business-relevant dimensions
- Have meaningful variation across entities
- Are scaled to similar ranges
- Are not highly correlated (multicollinearity)

**Exclude features that:**
- Are identifiers (IDs, keys)
- Have no variance (constant values)
- Are derived from other included features
- Represent time periods (unless doing temporal clustering)

## Output Artifacts

This workflow produces:
1. `${TABLE_NAME}_kmeans_model` - Trained K-Means clustering model
2. `${TABLE_NAME}_clustered` - Training data with cluster assignments
3. `${TABLE_NAME}_test_clustered` - Test data with cluster assignments
4. `${TABLE_NAME}_cluster_profiles` - Business interpretation of each cluster
5. `${TABLE_NAME}_cluster_assigned` - Production view for cluster assignment
6. Elbow analysis results (if performed)
7. Silhouette scores for cluster quality
8. Cluster centroids and characteristics
9. Cluster size distributions

## Best Practices

1. **Always scale features** - K-Means is sensitive to feature scales
2. **Use Elbow Method** - Don't guess the number of clusters
3. **Validate with Silhouette** - Ensure clusters are meaningful
4. **Profile clusters** - Give business-friendly names and descriptions
5. **Monitor stability** - Track cluster distributions over time
6. **Handle outliers** - Consider removing extreme outliers before clustering
7. **Document segments** - Record cluster characteristics and use cases
8. **Set random seed** - Ensure reproducible results
9. **Use kmeans++** - Better initialization than random
10. **Test multiple K values** - Compare quality metrics

## Common Issues and Solutions

### Issue: Poor Silhouette Score
**Cause:** Data doesn't have natural clusters or wrong K
**Solutions:**
- Try different K values (elbow method)
- Improve feature engineering
- Remove outliers
- Check if data has inherent structure
- Consider hierarchical clustering

### Issue: Unbalanced Cluster Sizes
**Cause:** Natural data distribution or outliers
**Solutions:**
- Verify with business context (may be expected)
- Check for outliers pulling centroids
- Try different K values
- Consider density-based clustering (DBSCAN)

### Issue: Clusters Not Business-Interpretable
**Cause:** Wrong features or too many/few clusters
**Solutions:**
- Review feature selection
- Add domain-relevant features
- Try different K values
- Profile clusters more deeply
- Consult domain experts

### Issue: High Distance to Centroids
**Cause:** Diffuse clusters or outliers
**Solutions:**
- Check for outliers in data
- Verify feature scaling
- Try different K values (more clusters)
- Consider removing outliers
- Evaluate if clustering is appropriate

### Issue: Cluster Drift in Production
**Cause:** Population changes or concept drift
**Solutions:**
- Schedule regular retraining
- Monitor cluster stability metrics
- Investigate population changes
- Update features to reflect new patterns
- Consider online clustering methods

### Issue: Slow Convergence
**Cause:** Too many features or poor initialization
**Solutions:**
- Increase MaxIterations
- Use kmeans++ initialization
- Reduce dimensionality (PCA)
- Check for highly correlated features
- Ensure proper feature scaling

## Function Reference Summary

### Model Training
- FunctionalPrompts/Advanced_Analytics/td_kmeans.md

### Cluster Assignment
- FunctionalPrompts/Advanced_Analytics/td_kmeanspredict.md

### Model Evaluation
- FunctionalPrompts/Advanced_Analytics/td_silhouette.md

### Data Preparation
- ProcessPrompts/ml/ml_dataPreparation.md

---

**File Created**: 2025-11-28
**Version**: 1.0
**Workflow Type**: Clustering
**Parent Persona**: persona_data_scientist.md
