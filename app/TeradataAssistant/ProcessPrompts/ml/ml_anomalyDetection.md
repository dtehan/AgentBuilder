---
name: Anomaly Detection Workflow
allowed-tools:
description: Complete workflow for building anomaly detection models in Teradata
argument-hint: [database_name] [table_name] [contamination_rate]
---

# Anomaly Detection Workflow

## Overview
This workflow guides you through building, training, evaluating, and deploying anomaly detection models in Teradata. Anomaly detection identifies unusual patterns, outliers, or deviations from normal behavior in data.

## Variables
DATABASE_NAME: $1
TABLE_NAME: $2
CONTAMINATION_RATE: $3 (optional - expected % of anomalies, default 0.1 = 10%)

## Prerequisites
- **Data must be ML-ready**: Use @ml/ml_dataPreparation.md first
- All features should be numeric (scaled)
- No labeled anomalies required (unsupervised learning)
- Features should represent normal behavior patterns

## Anomaly Detection Use Cases

### Fraud Detection
- Credit card fraud
- Insurance claim fraud
- Identity theft detection
- Account takeover detection
- Payment fraud prevention

### Network Security
- Intrusion detection
- DDoS attack identification
- Unusual network traffic patterns
- Malware detection
- Unauthorized access attempts

### Quality Control and Manufacturing
- Defect detection
- Equipment malfunction prediction
- Process anomaly identification
- Product quality deviation
- Supply chain disruptions

### Healthcare and Medical
- Disease outbreak detection
- Abnormal patient vitals
- Medical billing anomalies
- Clinical trial outliers
- Prescription anomaly detection

### Business Operations
- Unusual transaction patterns
- Revenue anomalies
- Inventory irregularities
- Customer behavior anomalies
- System performance issues

### IoT and Sensor Data
- Sensor malfunction detection
- Equipment failure prediction
- Environmental anomaly detection
- Energy consumption anomalies
- Vehicle performance issues

## Workflow Stages

### Stage 0: Data Preparation Check

**Verify data is ML-ready:**
```sql
-- Check if data prep has been completed
SELECT COUNT(*) as total_rows,
       COUNT(DISTINCT dataset_split) as has_split
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready;

-- Check feature distributions for normal data
SELECT
    COUNT(*) as row_count,
    COUNT(DISTINCT row_id) as unique_ids
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN';
```

**Important Note:**
- Training data should contain primarily NORMAL examples
- Anomalies in training data will contaminate the model
- If labeled data exists, filter to normal examples only

**If data is not prepared:**
- Route to: @ml/ml_dataPreparation.md
- Arguments: ${DATABASE_NAME} ${TABLE_NAME}
- Special instruction: Filter to normal examples for training

### Stage 1: Problem Definition

**Define Anomaly Detection Problem:**

1. **Understand Expected Anomaly Rate:**
```sql
-- If labeled data exists, calculate actual anomaly rate
SELECT
    label,
    COUNT(*) as count,
    CAST(COUNT(*) AS FLOAT) / SUM(COUNT(*)) OVER () * 100 as percentage
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
GROUP BY label
ORDER BY count DESC;
```

**Contamination Rate Guidelines:**
- **Fraud Detection**: 0.5-2% (0.005-0.02)
- **Network Security**: 1-5% (0.01-0.05)
- **Quality Control**: 2-10% (0.02-0.10)
- **Business Operations**: 5-15% (0.05-0.15)
- **Unknown**: Start with 10% (0.10) and adjust

2. **Analyze Feature Distributions:**
```sql
-- Check for features with extreme values
SELECT
    'feature_1' as feature_name,
    MIN(feature_1) as min_val,
    PERCENTILE_CONT(0.01) WITHIN GROUP (ORDER BY feature_1) as p1,
    PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY feature_1) as p99,
    MAX(feature_1) as max_val,
    AVG(feature_1) as mean_val,
    STDDEV_POP(feature_1) as std_val
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN'

UNION ALL

SELECT
    'feature_2',
    MIN(feature_2), PERCENTILE_CONT(0.01) WITHIN GROUP (ORDER BY feature_2),
    PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY feature_2),
    MAX(feature_2), AVG(feature_2), STDDEV_POP(feature_2)
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN';
```

3. **Define Anomaly Characteristics:**
- What makes something anomalous in this context?
- Point anomalies (individual outliers) or contextual anomalies?
- Global anomalies or local anomalies?
- Real-time detection or batch analysis?

4. **Define Success Metrics:**
- **Precision**: % of detected anomalies that are true anomalies
- **Recall**: % of actual anomalies that are detected
- **F1-Score**: Balance between precision and recall
- **False Positive Rate**: % of normal cases flagged as anomalies

### Stage 2: Model Selection

**Decision Matrix: Which Anomaly Detection Algorithm?**

| Model | Best For | Pros | Cons | Teradata Function |
|-------|----------|------|------|-------------------|
| **OneClassSVM** | Complex boundaries | Handles non-linearity, robust | Slower, hyperparameter tuning needed | TD_OneClassSVM |
| **OutlierFilter** | Statistical outliers | Fast, simple, interpretable | Assumes normal distribution | TD_OutlierFilter |
| **Isolation Forest** | High-dimensional data | Fast, effective for many features | May miss local anomalies | TD_IsolationForest |
| **Local Outlier Factor** | Local anomalies | Detects density-based outliers | Computationally expensive | TD_LOF |

**Recommendation Engine:**

**Ask User:**
"What type of anomaly detection do you need?
1. **General purpose** (Recommended: OneClassSVM - handles complex patterns)
2. **Fast statistical** (OutlierFilter - simple outlier detection)
3. **High-dimensional** (IsolationForest - many features)
4. **Compare multiple** (Train and compare different methods)"

**User Response Handling:**
- **Option 1**: Proceed with TD_OneClassSVM
- **Option 2**: Use TD_OutlierFilter
- **Option 3**: Use TD_IsolationForest (if available)
- **Option 4**: Train multiple models and compare

### Stage 3: Model Training

#### Option A: Recommended Model (OneClassSVM)

```sql
-- Train One-Class SVM for anomaly detection
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_ocsvm_model AS
SELECT TD_OneClassSVM(
    Nu(${CONTAMINATION_RATE}),   -- Expected fraction of anomalies (e.g., 0.1 = 10%)
    KernelType('rbf'),            -- Radial basis function kernel
    Gamma('auto'),                -- Kernel coefficient (auto = 1/n_features)
    Tolerance(0.001),             -- Convergence tolerance
    MaxIterations(1000)           -- Maximum training iterations
)
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN'
WITH DATA;
```

**Hyperparameter Guidance:**
- **Nu**: Expected anomaly rate (0.01 to 0.5)
  - Lower = stricter (fewer anomalies)
  - Higher = more permissive (more anomalies)
- **KernelType**: 'rbf' (non-linear), 'linear' (linear boundaries)
- **Gamma**: 'auto' or 0.001-1.0
  - Lower = broader decision boundary
  - Higher = more complex boundary
- **Tolerance**: 0.001 (standard) to 0.0001 (precise)

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_oneclasssvm.md

#### Option B: Statistical Outlier Detection

```sql
-- Fit OutlierFilter model (statistical method)
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_outlier_model AS
SELECT TD_OutlierFilterFit(
    Method('iqr'),                -- Inter-Quartile Range method
    Multiplier(1.5),              -- IQR multiplier (1.5 = standard, 3.0 = strict)
    IncludeColumns('feature_1', 'feature_2', 'feature_3', 'feature_4')
)
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN'
WITH DATA;
```

**Method Options:**
- **'iqr'**: Inter-Quartile Range (IQR) method
  - Multiplier: 1.5 (permissive), 3.0 (strict)
- **'z-score'**: Standard deviation method
  - Threshold: 2.5 (permissive), 3.5 (strict)
- **'percentile'**: Percentile-based thresholds
  - Lower/Upper percentiles

**Function Reference**:
- FunctionalPrompts/Advanced_Analytics/td_outlierfilterfit.md
- FunctionalPrompts/Advanced_Analytics/td_outlierfiltertransform.md

#### Option C: Alternative Configurations

**Strict OneClassSVM (Low False Positives)**
```sql
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_ocsvm_strict AS
SELECT TD_OneClassSVM(
    Nu(0.05),                     -- Only 5% flagged as anomalies
    KernelType('rbf'),
    Gamma(0.001),                 -- Broader boundary
    Tolerance(0.001)
)
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN'
WITH DATA;
```

**Sensitive OneClassSVM (High Recall)**
```sql
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_ocsvm_sensitive AS
SELECT TD_OneClassSVM(
    Nu(0.20),                     -- Flag 20% as potential anomalies
    KernelType('rbf'),
    Gamma(0.1),                   -- Tighter boundary
    Tolerance(0.001)
)
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN'
WITH DATA;
```

**Linear OneClassSVM (Fast, Interpretable)**
```sql
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_ocsvm_linear AS
SELECT TD_OneClassSVM(
    Nu(${CONTAMINATION_RATE}),
    KernelType('linear'),         -- Linear decision boundary
    Tolerance(0.001)
)
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN'
WITH DATA;
```

### Stage 4: Anomaly Detection (Scoring)

#### OneClassSVM Predictions

```sql
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_anomaly_scores AS
SELECT
    t.*,
    p.prediction as is_anomaly,          -- 1 = normal, -1 = anomaly
    p.decision_value as anomaly_score,   -- Distance from decision boundary (more negative = more anomalous)
    ABS(p.decision_value) as anomaly_magnitude
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready t,
     TD_OneClassSVMPredict(
         ModelTable(${DATABASE_NAME}.${TABLE_NAME}_ocsvm_model)
     ) p
WHERE t.dataset_split = 'TEST'
WITH DATA;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_oneclasssvmpredict.md

**Score Interpretation:**
- **prediction = 1**: Normal instance
- **prediction = -1**: Anomaly detected
- **decision_value < 0**: Anomalous (more negative = more anomalous)
- **decision_value > 0**: Normal (more positive = more normal)

#### OutlierFilter Predictions

```sql
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_outlier_scores AS
SELECT
    t.*,
    p.is_outlier as is_anomaly,          -- 0 = normal, 1 = outlier
    p.outlier_features,                   -- Which features are anomalous
    p.outlier_score                       -- Magnitude of anomaly
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready t,
     TD_OutlierFilterTransform(
         ModelTable(${DATABASE_NAME}.${TABLE_NAME}_outlier_model)
     ) p
WHERE t.dataset_split = 'TEST'
WITH DATA;
```

#### Flag Top Anomalies

```sql
-- Identify most anomalous instances
SELECT
    row_id,
    is_anomaly,
    anomaly_score,
    anomaly_magnitude,
    RANK() OVER (ORDER BY anomaly_magnitude DESC) as anomaly_rank
FROM ${DATABASE_NAME}.${TABLE_NAME}_anomaly_scores
WHERE is_anomaly = -1
ORDER BY anomaly_magnitude DESC
LIMIT 100;
```

### Stage 5: Model Evaluation

#### Performance Metrics (If Labels Available)

```sql
-- Calculate precision, recall, F1 if true labels exist
WITH predictions AS (
    SELECT
        CASE WHEN true_label = 'anomaly' THEN 1 ELSE 0 END as actual_anomaly,
        CASE WHEN is_anomaly = -1 THEN 1 ELSE 0 END as predicted_anomaly
    FROM ${DATABASE_NAME}.${TABLE_NAME}_anomaly_scores
),
metrics AS (
    SELECT
        SUM(CASE WHEN actual_anomaly = 1 AND predicted_anomaly = 1 THEN 1 ELSE 0 END) as true_positive,
        SUM(CASE WHEN actual_anomaly = 0 AND predicted_anomaly = 1 THEN 1 ELSE 0 END) as false_positive,
        SUM(CASE WHEN actual_anomaly = 1 AND predicted_anomaly = 0 THEN 1 ELSE 0 END) as false_negative,
        SUM(CASE WHEN actual_anomaly = 0 AND predicted_anomaly = 0 THEN 1 ELSE 0 END) as true_negative
    FROM predictions
)
SELECT
    true_positive,
    false_positive,
    false_negative,
    true_negative,
    -- Precision: Of detected anomalies, how many are true?
    CAST(true_positive AS FLOAT) / NULLIFZERO(true_positive + false_positive) as precision,
    -- Recall: Of actual anomalies, how many did we detect?
    CAST(true_positive AS FLOAT) / NULLIFZERO(true_positive + false_negative) as recall,
    -- F1 Score: Harmonic mean of precision and recall
    2.0 * (CAST(true_positive AS FLOAT) / NULLIFZERO(true_positive + false_positive)) *
          (CAST(true_positive AS FLOAT) / NULLIFZERO(true_positive + false_negative)) /
          NULLIFZERO((CAST(true_positive AS FLOAT) / NULLIFZERO(true_positive + false_positive)) +
                     (CAST(true_positive AS FLOAT) / NULLIFZERO(true_positive + false_negative))) as f1_score,
    -- False Positive Rate
    CAST(false_positive AS FLOAT) / NULLIFZERO(false_positive + true_negative) as false_positive_rate,
    -- Accuracy
    CAST(true_positive + true_negative AS FLOAT) /
         NULLIFZERO(true_positive + true_negative + false_positive + false_negative) as accuracy
FROM metrics;
```

#### Metrics Interpretation Guide

| Metric | Formula | When to Prioritize | Target |
|--------|---------|---------------------|--------|
| **Precision** | TP/(TP+FP) | Minimize false alarms | >70% |
| **Recall** | TP/(TP+FN) | Catch all anomalies | >80% |
| **F1-Score** | 2PR/(P+R) | Balance both | >75% |
| **FPR** | FP/(FP+TN) | Reduce alert fatigue | <5% |

**Business Context:**
- **Fraud Detection**: Prioritize Recall (catch fraud) then filter FP
- **Quality Control**: Balance Precision/Recall
- **Security**: High Recall (catch intrusions), tolerate FP
- **Business Ops**: High Precision (avoid false alarms)

#### Anomaly Score Distribution

```sql
-- Analyze distribution of anomaly scores
SELECT
    CASE
        WHEN anomaly_score >= 0 THEN 'Normal (score >= 0)'
        WHEN anomaly_score >= -0.5 THEN 'Borderline (-0.5 to 0)'
        WHEN anomaly_score >= -1.0 THEN 'Mild Anomaly (-1.0 to -0.5)'
        WHEN anomaly_score >= -2.0 THEN 'Moderate Anomaly (-2.0 to -1.0)'
        ELSE 'Severe Anomaly (< -2.0)'
    END as anomaly_category,
    COUNT(*) as count,
    CAST(COUNT(*) AS FLOAT) / SUM(COUNT(*)) OVER () * 100 as percentage,
    AVG(anomaly_score) as avg_score,
    MIN(anomaly_score) as min_score,
    MAX(anomaly_score) as max_score
FROM ${DATABASE_NAME}.${TABLE_NAME}_anomaly_scores
GROUP BY 1
ORDER BY avg_score DESC;
```

#### Threshold Tuning

```sql
-- Evaluate different thresholds for anomaly classification
WITH threshold_analysis AS (
    SELECT
        threshold,
        SUM(CASE WHEN anomaly_score < threshold AND true_label = 'anomaly' THEN 1 ELSE 0 END) as tp,
        SUM(CASE WHEN anomaly_score < threshold AND true_label = 'normal' THEN 1 ELSE 0 END) as fp,
        SUM(CASE WHEN anomaly_score >= threshold AND true_label = 'anomaly' THEN 1 ELSE 0 END) as fn,
        SUM(CASE WHEN anomaly_score >= threshold AND true_label = 'normal' THEN 1 ELSE 0 END) as tn
    FROM ${DATABASE_NAME}.${TABLE_NAME}_anomaly_scores,
         (SELECT -0.1 as threshold UNION ALL
          SELECT -0.5 UNION ALL
          SELECT -1.0 UNION ALL
          SELECT -1.5 UNION ALL
          SELECT -2.0) thresholds
    GROUP BY threshold
)
SELECT
    threshold,
    tp, fp, fn, tn,
    CAST(tp AS FLOAT) / NULLIFZERO(tp + fp) as precision,
    CAST(tp AS FLOAT) / NULLIFZERO(tp + fn) as recall,
    CAST(fp AS FLOAT) / NULLIFZERO(fp + tn) as fpr
FROM threshold_analysis
ORDER BY threshold DESC;
```

#### Compare Multiple Models

```sql
-- Compare different anomaly detection approaches
SELECT
    'OneClassSVM' as model,
    COUNT(CASE WHEN is_anomaly = -1 THEN 1 END) as anomalies_detected,
    CAST(COUNT(CASE WHEN is_anomaly = -1 THEN 1 END) AS FLOAT) / COUNT(*) * 100 as detection_rate,
    AVG(CASE WHEN is_anomaly = -1 THEN anomaly_magnitude END) as avg_anomaly_score
FROM ${DATABASE_NAME}.${TABLE_NAME}_anomaly_scores

UNION ALL

SELECT
    'OutlierFilter' as model,
    COUNT(CASE WHEN is_anomaly = 1 THEN 1 END),
    CAST(COUNT(CASE WHEN is_anomaly = 1 THEN 1 END) AS FLOAT) / COUNT(*) * 100,
    AVG(CASE WHEN is_anomaly = 1 THEN outlier_score END)
FROM ${DATABASE_NAME}.${TABLE_NAME}_outlier_scores

ORDER BY detection_rate;
```

### Stage 6: Anomaly Interpretation and Root Cause Analysis

#### Feature Contribution to Anomalies

```sql
-- Analyze which features contribute most to anomalies
WITH feature_stats AS (
    SELECT
        'feature_1' as feature_name,
        AVG(CASE WHEN is_anomaly = -1 THEN feature_1 END) as avg_anomaly,
        AVG(CASE WHEN is_anomaly = 1 THEN feature_1 END) as avg_normal,
        STDDEV_POP(CASE WHEN is_anomaly = -1 THEN feature_1 END) as std_anomaly,
        STDDEV_POP(CASE WHEN is_anomaly = 1 THEN feature_1 END) as std_normal
    FROM ${DATABASE_NAME}.${TABLE_NAME}_anomaly_scores

    UNION ALL

    SELECT
        'feature_2',
        AVG(CASE WHEN is_anomaly = -1 THEN feature_2 END),
        AVG(CASE WHEN is_anomaly = 1 THEN feature_2 END),
        STDDEV_POP(CASE WHEN is_anomaly = -1 THEN feature_2 END),
        STDDEV_POP(CASE WHEN is_anomaly = 1 THEN feature_2 END)
    FROM ${DATABASE_NAME}.${TABLE_NAME}_anomaly_scores
)
SELECT
    feature_name,
    avg_anomaly,
    avg_normal,
    ABS(avg_anomaly - avg_normal) / NULLIFZERO(std_normal) as normalized_difference
FROM feature_stats
ORDER BY normalized_difference DESC;
```

#### Anomaly Clustering

```sql
-- Group similar anomalies together
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_anomaly_clusters AS
SELECT
    a.*,
    c.cluster_id as anomaly_type
FROM ${DATABASE_NAME}.${TABLE_NAME}_anomaly_scores a,
     TD_KMeans(
         K(5),                    -- 5 types of anomalies
         MaxIterations(100)
     ) c
WHERE a.is_anomaly = -1
WITH DATA;

-- Profile each anomaly type
SELECT
    anomaly_type,
    COUNT(*) as count,
    AVG(anomaly_magnitude) as avg_severity,
    AVG(feature_1) as avg_f1,
    AVG(feature_2) as avg_f2,
    AVG(feature_3) as avg_f3
FROM ${DATABASE_NAME}.${TABLE_NAME}_anomaly_clusters
GROUP BY anomaly_type
ORDER BY avg_severity DESC;
```

#### Individual Anomaly Explanation

```sql
-- Explain specific anomaly by comparing to normal distribution
WITH normal_stats AS (
    SELECT
        AVG(feature_1) as mean_f1, STDDEV_POP(feature_1) as std_f1,
        AVG(feature_2) as mean_f2, STDDEV_POP(feature_2) as std_f2,
        AVG(feature_3) as mean_f3, STDDEV_POP(feature_3) as std_f3
    FROM ${DATABASE_NAME}.${TABLE_NAME}_anomaly_scores
    WHERE is_anomaly = 1
)
SELECT
    a.row_id,
    a.anomaly_score,
    -- Feature deviations from normal
    (a.feature_1 - ns.mean_f1) / NULLIFZERO(ns.std_f1) as f1_z_score,
    (a.feature_2 - ns.mean_f2) / NULLIFZERO(ns.std_f2) as f2_z_score,
    (a.feature_3 - ns.mean_f3) / NULLIFZERO(ns.std_f3) as f3_z_score
FROM ${DATABASE_NAME}.${TABLE_NAME}_anomaly_scores a, normal_stats ns
WHERE a.row_id = 'specific_anomaly_id';
```

### Stage 7: Production Deployment

#### Create Anomaly Detection View

```sql
-- Production view for real-time anomaly detection
CREATE VIEW ${DATABASE_NAME}.${TABLE_NAME}_anomaly_detection AS
SELECT
    t.*,
    p.prediction as is_anomaly,
    p.decision_value as anomaly_score,
    ABS(p.decision_value) as anomaly_magnitude,
    CASE
        WHEN p.decision_value < -2.0 THEN 'Critical'
        WHEN p.decision_value < -1.0 THEN 'High'
        WHEN p.decision_value < -0.5 THEN 'Medium'
        WHEN p.decision_value < 0 THEN 'Low'
        ELSE 'Normal'
    END as anomaly_severity,
    CURRENT_TIMESTAMP as detection_timestamp
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready t,
     TD_OneClassSVMPredict(
         ModelTable(${DATABASE_NAME}.${TABLE_NAME}_ocsvm_model)
     ) p;
```

#### Batch Anomaly Detection

```sql
-- Score new data for anomalies
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_new_anomalies AS
SELECT
    new_data.*,
    p.prediction as is_anomaly,
    p.decision_value as anomaly_score,
    ABS(p.decision_value) as anomaly_magnitude,
    CASE
        WHEN p.decision_value < -2.0 THEN 'Critical'
        WHEN p.decision_value < -1.0 THEN 'High'
        ELSE 'Normal'
    END as severity,
    CURRENT_DATE as detection_date
FROM ${DATABASE_NAME}.${TABLE_NAME}_new_data new_data,
     TD_OneClassSVMPredict(
         ModelTable(${DATABASE_NAME}.${TABLE_NAME}_ocsvm_model)
     ) p
WITH DATA;
```

#### Anomaly Alerting

```sql
-- Identify critical anomalies for alerting
SELECT
    row_id,
    detection_timestamp,
    anomaly_score,
    anomaly_severity,
    feature_1,
    feature_2,
    feature_3
FROM ${DATABASE_NAME}.${TABLE_NAME}_new_anomalies
WHERE anomaly_severity IN ('Critical', 'High')
  AND detection_date = CURRENT_DATE
ORDER BY anomaly_magnitude DESC;
```

#### Monitor Anomaly Trends

```sql
-- Track anomaly rates over time
SELECT
    detection_date,
    COUNT(*) as total_cases,
    SUM(CASE WHEN is_anomaly = -1 THEN 1 ELSE 0 END) as anomaly_count,
    CAST(SUM(CASE WHEN is_anomaly = -1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 as anomaly_rate,
    AVG(CASE WHEN is_anomaly = -1 THEN anomaly_magnitude END) as avg_anomaly_severity
FROM ${DATABASE_NAME}.${TABLE_NAME}_new_anomalies
GROUP BY detection_date
ORDER BY detection_date;
```

#### Anomaly Investigation Workflow

```sql
-- Create investigation queue for detected anomalies
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_anomaly_investigations AS
SELECT
    row_id,
    detection_timestamp,
    anomaly_score,
    anomaly_severity,
    'PENDING' as investigation_status,
    NULL as investigation_notes,
    NULL as true_anomaly_flag,
    NULL as investigator,
    NULL as investigation_date
FROM ${DATABASE_NAME}.${TABLE_NAME}_new_anomalies
WHERE anomaly_severity IN ('Critical', 'High')
WITH DATA;
```

## Decision Guides

### When to Retrain Model

Retrain if:
- **Anomaly rate increases** significantly (>20% change)
- **False positive rate too high** (>10% of alerts are false)
- **New normal patterns emerge** (concept drift)
- **Business processes change** (new products, channels)
- **Model performance degrades** (precision/recall drop)
- **Time-based**: Every 3-6 months for most use cases

### Model Selection Summary

**Use OneClassSVM when:**
- Need to handle complex non-linear patterns
- Have sufficient training data (>1000 normal examples)
- Can tolerate slower training
- Want robust anomaly detection

**Use OutlierFilter when:**
- Need fast, interpretable results
- Data follows normal distribution
- Want to detect statistical outliers
- Need simple deployment

**Use IsolationForest when:**
- Have high-dimensional data (many features)
- Need fast training and scoring
- Want good performance with limited tuning

**Use Local Outlier Factor when:**
- Anomalies are contextual (local patterns)
- Have varying density regions
- Need density-based detection

### Choosing Contamination Rate (Nu)

**Conservative (Low False Positives):**
- Nu = 0.01-0.05 (1-5%)
- Use for critical applications (security, safety)
- Accept some missed anomalies to reduce false alarms

**Balanced:**
- Nu = 0.05-0.15 (5-15%)
- Use for general purpose anomaly detection
- Balance between detection and false positives

**Sensitive (High Recall):**
- Nu = 0.15-0.30 (15-30%)
- Use for exploratory analysis
- Accept more false positives to catch more anomalies

### Threshold Tuning Strategy

1. **Start with model default** (Nu parameter)
2. **Evaluate precision and recall** on validation set
3. **If too many false positives**: Decrease Nu or lower threshold
4. **If missing anomalies**: Increase Nu or raise threshold
5. **Use business cost** to optimize threshold

## Output Artifacts

This workflow produces:
1. `${TABLE_NAME}_ocsvm_model` - Trained One-Class SVM model
2. `${TABLE_NAME}_anomaly_scores` - Test set with anomaly scores
3. `${TABLE_NAME}_anomaly_detection` - Production view
4. `${TABLE_NAME}_anomaly_clusters` - Grouped anomaly types
5. `${TABLE_NAME}_anomaly_investigations` - Investigation queue
6. Performance metrics (precision, recall, F1, FPR)
7. Anomaly score distributions
8. Feature contribution analysis

## Best Practices

1. **Train on normal data only** - Filter out known anomalies
2. **Scale features properly** - Essential for distance-based methods
3. **Set appropriate contamination rate** - Based on domain knowledge
4. **Monitor false positive rate** - Avoid alert fatigue
5. **Investigate anomalies** - Build feedback loop
6. **Profile anomaly types** - Understand patterns
7. **Set severity levels** - Prioritize critical anomalies
8. **Track performance over time** - Detect concept drift
9. **Document investigation results** - Improve model over time
10. **Retrain regularly** - Adapt to changing patterns

## Common Issues and Solutions

### Issue: Too Many False Positives
**Cause:** Contamination rate too high or model too sensitive
**Solutions:**
- Decrease Nu parameter (make stricter)
- Adjust decision threshold
- Remove outliers from training data
- Add more normal examples to training
- Review feature engineering

### Issue: Missing Known Anomalies
**Cause:** Contamination rate too low or model too strict
**Solutions:**
- Increase Nu parameter
- Adjust decision threshold
- Check if training data is truly normal
- Add more relevant features
- Try different kernel (linear vs. RBF)

### Issue: High Anomaly Rate (>20%)
**Cause:** Model not learning normal behavior or concept drift
**Solutions:**
- Verify training data quality
- Check for data distribution shifts
- Retrain with more recent data
- Review feature selection
- Adjust Nu parameter

### Issue: Inconsistent Results
**Cause:** Non-deterministic training or unstable model
**Solutions:**
- Set random seed for reproducibility
- Increase training data size
- Ensure feature scaling consistency
- Check for data quality issues
- Use more stable algorithm (OutlierFilter)

### Issue: Slow Scoring Performance
**Cause:** Complex model or large dataset
**Solutions:**
- Use linear kernel instead of RBF
- Consider OutlierFilter for simpler cases
- Optimize feature count
- Use batch scoring instead of row-by-row
- Consider model simplification

### Issue: Cannot Interpret Anomalies
**Cause:** Complex model or unclear feature contributions
**Solutions:**
- Use OutlierFilter for interpretability
- Calculate feature deviations from normal
- Cluster anomalies into types
- Add domain-specific features
- Create anomaly profiles

## Function Reference Summary

### Model Training
- FunctionalPrompts/Advanced_Analytics/td_oneclasssvm.md
- FunctionalPrompts/Advanced_Analytics/td_outlierfilterfit.md

### Anomaly Detection
- FunctionalPrompts/Advanced_Analytics/td_oneclasssvmpredict.md
- FunctionalPrompts/Advanced_Analytics/td_outlierfiltertransform.md

### Supporting Functions
- FunctionalPrompts/Advanced_Analytics/td_kmeans.md (for anomaly clustering)

### Data Preparation
- ProcessPrompts/ml/ml_dataPreparation.md

---

**File Created**: 2025-11-28
**Version**: 1.0
**Workflow Type**: Anomaly Detection
**Parent Persona**: persona_data_scientist.md
