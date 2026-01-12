# TD_ClassificationEvaluator

## Function Name
**TD_ClassificationEvaluator**

## Description
TD_ClassificationEvaluator computes comprehensive evaluation metrics for classification models, enabling comparison of multiple models and assessment of prediction accuracy. The function analyzes actual vs. predicted class labels to calculate precision, recall, F1-score, and accuracy metrics at both class-level and aggregate levels (micro, macro, and weighted averages).

**Key Characteristics:**
- **Multi-Class Support**: Works with binary and multi-class classification
- **Comprehensive Metrics**: Calculates accuracy, precision, recall, F1-score
- **Multiple Aggregation Methods**: Micro, macro, and weighted averaging
- **Confusion Matrix Basis**: Generates class-level performance breakdown
- **Dual Output Tables**: Primary (class-level) and secondary (aggregate) metrics
- **Model Comparison**: Enables direct comparison of multiple classification models

The function generates two output tables:
- **Primary Output**: Class-level metrics including precision, recall, F1-score, and support
- **Secondary Output**: Overall metrics with micro, macro, and weighted averages

## When to Use

### Business Applications

**Model Evaluation and Selection:**
- Compare multiple classification algorithms (logistic regression, decision trees, XGBoost, etc.)
- Evaluate model performance before production deployment
- Select best model based on business-critical metrics
- Validate model performance across different classes
- Assess model generalization on test data

**Credit Risk and Fraud Detection:**
- Evaluate fraud detection model accuracy
- Balance false positives vs. false negatives in credit decisions
- Assess risk classification precision
- Monitor fraud detection model performance
- Optimize decision thresholds for business goals

**Customer Analytics:**
- Evaluate churn prediction model accuracy
- Assess customer segment classification quality
- Validate propensity-to-buy models
- Monitor recommendation system precision
- Measure targeting model effectiveness

**Healthcare and Diagnostics:**
- Evaluate disease diagnosis model accuracy
- Assess patient risk stratification quality
- Validate treatment response predictions
- Monitor clinical decision support systems
- Balance sensitivity and specificity for diagnostics

**Marketing and Lead Scoring:**
- Evaluate lead quality classification models
- Assess campaign response prediction accuracy
- Validate customer lifetime value tier classification
- Monitor A/B test prediction quality
- Measure conversion prediction precision

**Quality Control and Manufacturing:**
- Evaluate defect detection model accuracy
- Assess product quality classification
- Validate equipment failure prediction
- Monitor predictive maintenance models
- Measure inspection automation accuracy

## Syntax

```sql
SELECT * FROM TD_ClassificationEvaluator (
    ON { table | view | (query) } AS InputTable
    [ OUT TABLE OutputTable (output_table_name) ]
    USING
    ObservationColumn ('observation_column')
    PredictionColumn ('prediction_column')
    { NumLabels (label_count) | Labels ('label1' [,...]) }
) AS alias;
```

## Required and Optional Elements

### Required Elements

**ObservationColumn:**
- Specifies the column containing actual/observed class labels
- Ground truth values for model evaluation
- Can be INTEGER or VARCHAR/CHAR data types
- Must match data type of PredictionColumn
- Format: `ObservationColumn('actual_class')`

**PredictionColumn:**
- Specifies the column containing predicted class labels from model
- Model output values for evaluation
- Can be INTEGER or VARCHAR/CHAR data types
- Must match data type of ObservationColumn
- Format: `PredictionColumn('predicted_class')`

**NumLabels OR Labels:**
- **NumLabels**: Specifies total count of class labels
  - Format: `NumLabels(3)` for 3-class problem
  - Use when labels are integers 0, 1, 2, ...
- **Labels**: Explicitly lists all class label values
  - Format: `Labels('0', '1', '2')` or `Labels('setosa', 'versicolor', 'virginica')`
  - Use when labels are strings or non-sequential integers
- **Must provide one** of NumLabels or Labels

### Optional Elements

**OUT TABLE OutputTable:**
- Specifies name for secondary output table containing aggregate metrics
- Format: `OUT TABLE OutputTable(aggregate_metrics)`
- **If not specified**: Only primary output returned (class-level metrics)
- **If specified**: Both primary and secondary outputs created
- Can specify PERMANENT or VOLATILE table type

## Input Specifications

### InputTable Schema

| Column | Data Type | Description | Required |
|--------|-----------|-------------|----------|
| ObservationColumn | INTEGER or VARCHAR/CHAR | Actual class labels (ground truth) | Yes |
| PredictionColumn | INTEGER or VARCHAR/CHAR | Predicted class labels from model | Yes |
| Other columns | Any type | Additional columns (not used by function) | No |

### Data Requirements

- **Matching data types**: ObservationColumn and PredictionColumn must have same data type
- **Complete labels**: All labels specified in Labels or NumLabels should appear in data
- **No NULL values**: NULL predictions or observations may cause errors
- **Consistent encoding**: Use same encoding for observations and predictions

## Output Specifications

### Primary Output Table Schema (Class-Level Metrics)

| Column | Data Type | Description |
|--------|-----------|-------------|
| SeqNum | INTEGER | Sequence number of the row |
| Prediction | VARCHAR | Column name containing predicted labels |
| Mapping | VARCHAR | Mapping used for the label (CLASS_N format) |
| Class_1, Class_2, ... | BIGINT | Confusion matrix columns - count of predictions per actual class |
| Precision | REAL | Positive predictive value: TP / (TP + FP) |
| Recall | REAL | Sensitivity or true positive rate: TP / (TP + FN) |
| F1 | REAL | Harmonic mean of precision and recall: 2 * (Precision * Recall) / (Precision + Recall) |
| Support | BIGINT | Number of occurrences of this class in ObservationColumn |

### Secondary Output Table Schema (Aggregate Metrics)

| Column | Data Type | Description |
|--------|-----------|-------------|
| SeqNum | INTEGER | Sequence number of the row |
| Metric | VARCHAR | Name of the metric |
| MetricValue | REAL | Value for the corresponding metric |

**Metrics in Secondary Output:**
- **Accuracy**: Overall classification accuracy (TP + TN) / Total
- **Micro-Precision**: Global precision calculated from total TP and FP across all classes
- **Micro-Recall**: Global recall calculated from total TP and FN across all classes
- **Micro-F1**: F1 score calculated from micro-precision and micro-recall
- **Macro-Precision**: Unweighted average of precision across all classes
- **Macro-Recall**: Unweighted average of recall across all classes
- **Macro-F1**: Unweighted average of F1 scores across all classes
- **Weighted-Precision**: Support-weighted average precision
- **Weighted-Recall**: Support-weighted average recall
- **Weighted-F1**: Support-weighted average F1 score

### Metric Interpretations

**Precision (Positive Predictive Value):**
- Answers: "Of all instances predicted as positive, how many were actually positive?"
- Formula: TP / (TP + FP)
- High precision = Low false positive rate
- Important when false positives are costly

**Recall (Sensitivity, True Positive Rate):**
- Answers: "Of all actual positive instances, how many did we correctly identify?"
- Formula: TP / (TP + FN)
- High recall = Low false negative rate
- Important when false negatives are costly

**F1 Score:**
- Harmonic mean balancing precision and recall
- Formula: 2 * (Precision * Recall) / (Precision + Recall)
- Useful when you need balance between precision and recall
- Range: 0 to 1, higher is better

**Support:**
- Number of actual occurrences of the class in dataset
- Used for weighted averaging
- Important for understanding class imbalance

## Code Examples

### Example 1: Binary Classification Model Evaluation (Fraud Detection)
**Business Context:** Financial services company evaluating fraud detection model performance.

```sql
-- Step 1: Evaluate fraud detection model
CREATE TABLE fraud_model_performance (
    SELECT * FROM TD_ClassificationEvaluator (
        ON fraud_predictions AS InputTable
        OUT TABLE OutputTable(fraud_aggregate_metrics)
        USING
        ObservationColumn('actual_fraud')
        PredictionColumn('predicted_fraud')
        Labels('0', '1')  -- 0=legitimate, 1=fraud
    ) AS dt
    ORDER BY SeqNum
) WITH DATA;

-- Step 2: Review class-level performance
SELECT
    Prediction,
    Mapping,
    CLASS_1 as predicted_legitimate,
    CLASS_2 as predicted_fraud,
    Precision,
    Recall,
    F1,
    Support,
    CASE
        WHEN Mapping = 'CLASS_1' THEN 'Legitimate Transactions'
        WHEN Mapping = 'CLASS_2' THEN 'Fraudulent Transactions'
    END as class_description
FROM fraud_model_performance;

-- Step 3: Review aggregate metrics
SELECT
    Metric,
    MetricValue,
    CASE
        WHEN Metric = 'Accuracy' THEN 'Overall correctness of predictions'
        WHEN Metric LIKE '%Precision' THEN 'Accuracy of positive predictions'
        WHEN Metric LIKE '%Recall' THEN 'Coverage of actual positives'
        WHEN Metric LIKE '%F1' THEN 'Balance between precision and recall'
    END as metric_description
FROM fraud_aggregate_metrics
ORDER BY SeqNum;

-- Step 4: Calculate business impact metrics
SELECT
    'Fraud Detection Performance' as analysis,
    (SELECT MetricValue FROM fraud_aggregate_metrics WHERE Metric = 'Accuracy') as overall_accuracy,
    (SELECT Recall FROM fraud_model_performance WHERE Mapping = 'CLASS_2') as fraud_recall,
    (SELECT Precision FROM fraud_model_performance WHERE Mapping = 'CLASS_2') as fraud_precision,
    (SELECT Support FROM fraud_model_performance WHERE Mapping = 'CLASS_2') as total_fraud_cases,
    -- Calculate missed fraud (false negatives)
    (SELECT Support FROM fraud_model_performance WHERE Mapping = 'CLASS_2') *
    (1 - (SELECT Recall FROM fraud_model_performance WHERE Mapping = 'CLASS_2')) as missed_fraud_count,
    -- Calculate false alarms (false positives)
    (SELECT Support FROM fraud_model_performance WHERE Mapping = 'CLASS_1') *
    (1 - (SELECT Precision FROM fraud_model_performance WHERE Mapping = 'CLASS_1')) as false_alarm_count;
```

**Sample Output:**
```
Prediction      | Mapping | predicted_legitimate | predicted_fraud | Precision | Recall | F1    | Support | class_description
----------------|---------|----------------------|-----------------|-----------|--------|-------|---------|----------------------
predicted_fraud | CLASS_1 |               48,756 |           1,244 |  0.975000 | 0.975  | 0.975 |  50,000 | Legitimate Transactions
predicted_fraud | CLASS_2 |                  345 |           4,655 |  0.789000 | 0.931  | 0.854 |   5,000 | Fraudulent Transactions

Metric            | MetricValue | metric_description
------------------|-------------|-------------------------------------------
Accuracy          |    0.971091 | Overall correctness of predictions
Micro-Precision   |    0.971091 | Accuracy of positive predictions
Micro-Recall      |    0.971091 | Coverage of actual positives
Micro-F1          |    0.971091 | Balance between precision and recall
Macro-Precision   |    0.882000 | Accuracy of positive predictions
Macro-Recall      |    0.953000 | Coverage of actual positives
Macro-F1          |    0.914500 | Balance between precision and recall
Weighted-Precision|    0.960318 | Accuracy of positive predictions
Weighted-Recall   |    0.971091 | Coverage of actual positives
Weighted-F1       |    0.965273 | Balance between precision and recall

analysis                      | overall_accuracy | fraud_recall | fraud_precision | total_fraud_cases | missed_fraud_count | false_alarm_count
------------------------------|------------------|--------------|-----------------|-------------------|--------------------|-----------------
Fraud Detection Performance   |         0.971091 |        0.931 |           0.789 |             5,000 |                345 |             1,244
```

**Business Impact:** Model achieves 97.1% overall accuracy with 93.1% fraud recall (catches 4,655 of 5,000 frauds) and 78.9% fraud precision. Misses 345 fraudulent transactions (6.9% false negative rate) while generating 1,244 false alarms (2.5% false positive rate). Trade-off analysis: Catching additional 345 frauds would increase false alarms, requiring cost-benefit analysis of investigation resources vs. fraud losses.

---

### Example 2: Multi-Class Customer Segment Classification
**Business Context:** E-commerce company evaluating customer segment prediction model for targeted marketing.

```sql
-- Step 1: Evaluate customer segment classification model
CREATE TABLE segment_model_performance (
    SELECT * FROM TD_ClassificationEvaluator (
        ON customer_segment_predictions AS InputTable
        OUT TABLE OutputTable(segment_aggregate_metrics)
        USING
        ObservationColumn('actual_segment')
        PredictionColumn('predicted_segment')
        Labels('High_Value', 'Medium_Value', 'Low_Value', 'At_Risk')
    ) AS dt
    ORDER BY SeqNum
) WITH DATA;

-- Step 2: Analyze per-segment performance
SELECT
    CASE Mapping
        WHEN 'CLASS_1' THEN 'High_Value'
        WHEN 'CLASS_2' THEN 'Medium_Value'
        WHEN 'CLASS_3' THEN 'Low_Value'
        WHEN 'CLASS_4' THEN 'At_Risk'
    END as segment_name,
    Support as actual_count,
    Precision,
    Recall,
    F1,
    -- Performance rating
    CASE
        WHEN F1 >= 0.80 THEN 'EXCELLENT'
        WHEN F1 >= 0.70 THEN 'GOOD'
        WHEN F1 >= 0.60 THEN 'ACCEPTABLE'
        ELSE 'NEEDS_IMPROVEMENT'
    END as performance_rating,
    -- Business priority
    CASE
        WHEN Mapping IN ('CLASS_1', 'CLASS_4') THEN 'HIGH_PRIORITY'
        ELSE 'STANDARD'
    END as business_priority
FROM segment_model_performance
ORDER BY F1 DESC;

-- Step 3: Identify misclassification patterns
SELECT
    'High_Value misclassified as Medium_Value' as misclassification_type,
    CLASS_2 as misclassification_count,
    CAST(CLASS_2 AS FLOAT) / Support * 100 as pct_of_actual
FROM segment_model_performance
WHERE Mapping = 'CLASS_1'

UNION ALL

SELECT
    'At_Risk misclassified as Low_Value' as misclassification_type,
    CLASS_3 as misclassification_count,
    CAST(CLASS_3 AS FLOAT) / Support * 100 as pct_of_actual
FROM segment_model_performance
WHERE Mapping = 'CLASS_4'

ORDER BY misclassification_count DESC;

-- Step 4: Compare averaging methods
SELECT
    SUBSTR(Metric, 1, POSITION('-' IN Metric) - 1) as metric_type,
    MAX(CASE WHEN Metric LIKE 'Micro-%' THEN MetricValue END) as micro_avg,
    MAX(CASE WHEN Metric LIKE 'Macro-%' THEN MetricValue END) as macro_avg,
    MAX(CASE WHEN Metric LIKE 'Weighted-%' THEN MetricValue END) as weighted_avg,
    -- Interpretation
    CASE
        WHEN ABS(MAX(CASE WHEN Metric LIKE 'Macro-%' THEN MetricValue END) -
                 MAX(CASE WHEN Metric LIKE 'Weighted-%' THEN MetricValue END)) > 0.05
        THEN 'CLASS_IMBALANCE_DETECTED'
        ELSE 'BALANCED_PERFORMANCE'
    END as balance_assessment
FROM segment_aggregate_metrics
WHERE Metric NOT IN ('Accuracy')
GROUP BY metric_type
ORDER BY metric_type;

-- Step 5: Revenue impact analysis
SELECT
    seg.segment_name,
    seg.actual_count,
    seg.Recall as correct_identification_rate,
    seg.actual_count * (1 - seg.Recall) as missed_customers,
    rev.avg_segment_revenue,
    seg.actual_count * (1 - seg.Recall) * rev.avg_segment_revenue as potential_lost_revenue
FROM (
    SELECT
        CASE Mapping
            WHEN 'CLASS_1' THEN 'High_Value'
            WHEN 'CLASS_2' THEN 'Medium_Value'
            WHEN 'CLASS_3' THEN 'Low_Value'
            WHEN 'CLASS_4' THEN 'At_Risk'
        END as segment_name,
        Support as actual_count,
        Recall
    FROM segment_model_performance
) seg
INNER JOIN segment_revenue_benchmarks rev
    ON seg.segment_name = rev.segment
ORDER BY potential_lost_revenue DESC;
```

**Sample Output:**
```
segment_name   | actual_count | Precision | Recall | F1    | performance_rating | business_priority
---------------|--------------|-----------|--------|-------|--------------------|-----------------
High_Value     |        8,234 |  0.867000 | 0.923  | 0.894 | EXCELLENT          | HIGH_PRIORITY
At_Risk        |        5,678 |  0.812000 | 0.856  | 0.833 | EXCELLENT          | HIGH_PRIORITY
Medium_Value   |       23,456 |  0.789000 | 0.812  | 0.800 | GOOD               | STANDARD
Low_Value      |       12,632 |  0.745000 | 0.778  | 0.761 | GOOD               | STANDARD

misclassification_type                         | misclassification_count | pct_of_actual
-----------------------------------------------|-------------------------|---------------
High_Value misclassified as Medium_Value       |                     634 |          7.70
At_Risk misclassified as Low_Value             |                     818 |         14.41
Medium_Value misclassified as Low_Value        |                   2,456 |         10.47

metric_type | micro_avg | macro_avg | weighted_avg | balance_assessment
------------|-----------|-----------|--------------|----------------------
F1          |  0.801234 |  0.822000 |     0.807891 | BALANCED_PERFORMANCE
Precision   |  0.801234 |  0.803250 |     0.794562 | BALANCED_PERFORMANCE
Recall      |  0.801234 |  0.842250 |     0.801234 | BALANCED_PERFORMANCE

segment_name   | actual_count | correct_identification_rate | missed_customers | avg_segment_revenue | potential_lost_revenue
---------------|--------------|----------------------------|------------------|---------------------|----------------------
High_Value     |        8,234 |                      0.923 |              634 |            5,678.90 |            3,600,461
At_Risk        |        5,678 |                      0.856 |              818 |            1,234.56 |            1,009,870
Medium_Value   |       23,456 |                      0.812 |            4,410 |              567.89 |            2,504,395
Low_Value      |       12,632 |                      0.778 |            2,804 |              123.45 |              346,158
```

**Business Impact:** Overall 80.1% accuracy across 4 customer segments with strong performance on high-priority segments (High_Value: 89.4% F1, At_Risk: 83.3% F1). Model misclassifies 7.7% of High_Value customers (634 customers, $3.6M potential lost revenue) and 14.4% of At_Risk customers (818 customers, $1.0M churn risk). Balanced performance across segments (macro vs. weighted F1 difference < 5%) indicates no major class imbalance issues. Recommended improvement focus on High_Value segment to capture additional $3.6M revenue opportunity.

---

### Example 3: Comparing Multiple Classification Models
**Business Context:** Insurance company comparing 3 different models for insurance claim approval prediction.

```sql
-- Model 1: Logistic Regression
CREATE TABLE logistic_performance (
    SELECT 'Logistic_Regression' as model_name, dt.*
    FROM TD_ClassificationEvaluator (
        ON logistic_predictions AS InputTable
        OUT TABLE OutputTable(logistic_aggregate)
        USING
        ObservationColumn('actual_decision')
        PredictionColumn('predicted_decision')
        Labels('Approve', 'Deny', 'Review')
    ) AS dt
) WITH DATA;

-- Model 2: Decision Tree
CREATE TABLE tree_performance (
    SELECT 'Decision_Tree' as model_name, dt.*
    FROM TD_ClassificationEvaluator (
        ON tree_predictions AS InputTable
        OUT TABLE OutputTable(tree_aggregate)
        USING
        ObservationColumn('actual_decision')
        PredictionColumn('predicted_decision')
        Labels('Approve', 'Deny', 'Review')
    ) AS dt
) WITH DATA;

-- Model 3: XGBoost
CREATE TABLE xgboost_performance (
    SELECT 'XGBoost' as model_name, dt.*
    FROM TD_ClassificationEvaluator (
        ON xgboost_predictions AS InputTable
        OUT TABLE OutputTable(xgboost_aggregate)
        USING
        ObservationColumn('actual_decision')
        PredictionColumn('predicted_decision')
        Labels('Approve', 'Deny', 'Review')
    ) AS dt
) WITH DATA;

-- Compare overall accuracy
SELECT
    model_name,
    MetricValue as accuracy,
    RANK() OVER (ORDER BY MetricValue DESC) as accuracy_rank
FROM (
    SELECT 'Logistic_Regression' as model_name, MetricValue FROM logistic_aggregate WHERE Metric = 'Accuracy'
    UNION ALL
    SELECT 'Decision_Tree', MetricValue FROM tree_aggregate WHERE Metric = 'Accuracy'
    UNION ALL
    SELECT 'XGBoost', MetricValue FROM xgboost_aggregate WHERE Metric = 'Accuracy'
) combined
ORDER BY accuracy DESC;

-- Compare per-class F1 scores
SELECT
    CASE Mapping
        WHEN 'CLASS_1' THEN 'Approve'
        WHEN 'CLASS_2' THEN 'Deny'
        WHEN 'CLASS_3' THEN 'Review'
    END as decision_class,
    MAX(CASE WHEN model_name = 'Logistic_Regression' THEN F1 END) as logistic_f1,
    MAX(CASE WHEN model_name = 'Decision_Tree' THEN F1 END) as tree_f1,
    MAX(CASE WHEN model_name = 'XGBoost' THEN F1 END) as xgboost_f1,
    -- Identify best model per class
    CASE
        WHEN MAX(CASE WHEN model_name = 'XGBoost' THEN F1 END) >= MAX(CASE WHEN model_name = 'Logistic_Regression' THEN F1 END)
         AND MAX(CASE WHEN model_name = 'XGBoost' THEN F1 END) >= MAX(CASE WHEN model_name = 'Decision_Tree' THEN F1 END)
        THEN 'XGBoost'
        WHEN MAX(CASE WHEN model_name = 'Decision_Tree' THEN F1 END) >= MAX(CASE WHEN model_name = 'Logistic_Regression' THEN F1 END)
        THEN 'Decision_Tree'
        ELSE 'Logistic_Regression'
    END as best_model_for_class
FROM (
    SELECT * FROM logistic_performance
    UNION ALL
    SELECT * FROM tree_performance
    UNION ALL
    SELECT * FROM xgboost_performance
) combined
GROUP BY Mapping
ORDER BY Mapping;

-- Compare macro and weighted averages
SELECT
    model_name,
    MAX(CASE WHEN Metric = 'Macro-F1' THEN MetricValue END) as macro_f1,
    MAX(CASE WHEN Metric = 'Weighted-F1' THEN MetricValue END) as weighted_f1,
    MAX(CASE WHEN Metric = 'Macro-Precision' THEN MetricValue END) as macro_precision,
    MAX(CASE WHEN Metric = 'Weighted-Precision' THEN MetricValue END) as weighted_precision,
    MAX(CASE WHEN Metric = 'Macro-Recall' THEN MetricValue END) as macro_recall,
    MAX(CASE WHEN Metric = 'Weighted-Recall' THEN MetricValue END) as weighted_recall
FROM (
    SELECT 'Logistic_Regression' as model_name, Metric, MetricValue FROM logistic_aggregate
    UNION ALL
    SELECT 'Decision_Tree', Metric, MetricValue FROM tree_aggregate
    UNION ALL
    SELECT 'XGBoost', Metric, MetricValue FROM xgboost_aggregate
) combined
GROUP BY model_name
ORDER BY weighted_f1 DESC;

-- Final recommendation
SELECT
    model_name,
    accuracy,
    weighted_f1,
    macro_f1,
    (accuracy + weighted_f1 + macro_f1) / 3 as composite_score,
    RANK() OVER (ORDER BY (accuracy + weighted_f1 + macro_f1) / 3 DESC) as overall_rank,
    CASE
        WHEN RANK() OVER (ORDER BY (accuracy + weighted_f1 + macro_f1) / 3 DESC) = 1 THEN 'RECOMMENDED_FOR_PRODUCTION'
        ELSE 'NOT_RECOMMENDED'
    END as recommendation
FROM (
    SELECT
        model_name,
        MAX(CASE WHEN Metric = 'Accuracy' THEN MetricValue END) as accuracy,
        MAX(CASE WHEN Metric = 'Weighted-F1' THEN MetricValue END) as weighted_f1,
        MAX(CASE WHEN Metric = 'Macro-F1' THEN MetricValue END) as macro_f1
    FROM (
        SELECT 'Logistic_Regression' as model_name, Metric, MetricValue FROM logistic_aggregate
        UNION ALL
        SELECT 'Decision_Tree', Metric, MetricValue FROM tree_aggregate
        UNION ALL
        SELECT 'XGBoost', Metric, MetricValue FROM xgboost_aggregate
    ) combined
    GROUP BY model_name
) scored
ORDER BY composite_score DESC;
```

**Sample Output:**
```
model_name           | accuracy  | accuracy_rank
---------------------|-----------|---------------
XGBoost              | 0.892345  |             1
Decision_Tree        | 0.867891  |             2
Logistic_Regression  | 0.845678  |             3

decision_class | logistic_f1 | tree_f1   | xgboost_f1 | best_model_for_class
---------------|-------------|-----------|------------|---------------------
Approve        |    0.878901 |  0.889012 |   0.912345 | XGBoost
Deny           |    0.823456 |  0.856789 |   0.878901 | XGBoost
Review         |    0.789012 |  0.812345 |   0.867890 | XGBoost

model_name           | macro_f1  | weighted_f1 | macro_precision | weighted_precision | macro_recall | weighted_recall
---------------------|-----------|-------------|-----------------|--------------------|--------------|-----------------
XGBoost              | 0.886379  |    0.892123 |        0.879012 |           0.885678 |     0.893456 |        0.892345
Decision_Tree        | 0.852715  |    0.861234 |        0.845678 |           0.854321 |     0.859876 |        0.867891
Logistic_Regression  | 0.830456  |    0.838901 |        0.823456 |           0.831234 |     0.837654 |        0.845678

model_name           | accuracy  | weighted_f1 | macro_f1  | composite_score | overall_rank | recommendation
---------------------|-----------|-------------|-----------|-----------------|--------------|-------------------------
XGBoost              | 0.892345  |    0.892123 |  0.886379 |        0.890282 |            1 | RECOMMENDED_FOR_PRODUCTION
Decision_Tree        | 0.867891  |    0.861234 |  0.852715 |        0.860613 |            2 | NOT_RECOMMENDED
Logistic_Regression  | 0.845678  |    0.838901 |  0.830456 |        0.838345 |            3 | NOT_RECOMMENDED
```

**Business Impact:** XGBoost outperforms both alternatives across all metrics with 89.2% accuracy and 89.2% weighted F1 score, representing 4.7% improvement over best alternative (Decision Tree). XGBoost achieves best performance in all 3 decision classes, particularly strong in "Approve" decisions (91.2% F1) which represent 60% of volume. Composite score analysis (averaging accuracy, weighted F1, and macro F1) confirms XGBoost as clear winner with 3.5% advantage. Recommended for production deployment with projected 25% reduction in manual review cases while maintaining decision quality.

---

### Example 4: Imbalanced Classes - Medical Diagnosis
**Business Context:** Hospital evaluating rare disease diagnosis model with severe class imbalance.

```sql
-- Evaluate diagnosis model with imbalanced classes
CREATE TABLE diagnosis_performance (
    SELECT * FROM TD_ClassificationEvaluator (
        ON diagnosis_predictions AS InputTable
        OUT TABLE OutputTable(diagnosis_aggregate)
        USING
        ObservationColumn('actual_diagnosis')
        PredictionColumn('predicted_diagnosis')
        Labels('Negative', 'Positive')  -- Positive = rare disease (2% prevalence)
    ) AS dt
    ORDER BY SeqNum
) WITH DATA;

-- Analyze class imbalance impact
SELECT
    CASE Mapping
        WHEN 'CLASS_1' THEN 'Negative (Healthy)'
        WHEN 'CLASS_2' THEN 'Positive (Disease)'
    END as diagnosis,
    Support as actual_cases,
    CAST(Support AS FLOAT) / (SELECT SUM(Support) FROM diagnosis_performance) * 100 as pct_of_total,
    Precision,
    Recall,
    F1,
    -- Clinical interpretation
    CASE
        WHEN Mapping = 'CLASS_2' THEN CAST(Support * (1 - Recall) AS INTEGER)
    END as missed_diagnoses,
    CASE
        WHEN Mapping = 'CLASS_1' THEN CAST(Support * (1 - Precision) AS INTEGER)
    END as false_alarms
FROM diagnosis_performance;

-- Compare averaging methods for imbalanced data
SELECT
    Metric,
    MetricValue,
    CASE
        WHEN Metric LIKE 'Micro-%' THEN 'Dominated by majority class (Negative)'
        WHEN Metric LIKE 'Macro-%' THEN 'Equal weight to both classes'
        WHEN Metric LIKE 'Weighted-%' THEN 'Weighted by class frequency'
    END as interpretation,
    CASE
        WHEN Metric IN ('Macro-Precision', 'Macro-Recall', 'Macro-F1') THEN 'MOST_RELEVANT'
        ELSE 'REFERENCE_ONLY'
    END as relevance_for_imbalanced
FROM diagnosis_aggregate
WHERE Metric NOT IN ('Accuracy')
ORDER BY
    CASE
        WHEN Metric LIKE 'Macro-%' THEN 1
        WHEN Metric LIKE 'Weighted-%' THEN 2
        ELSE 3
    END,
    Metric;

-- Cost-benefit analysis
SELECT
    'Disease Detection Performance' as analysis,
    (SELECT Recall FROM diagnosis_performance WHERE Mapping = 'CLASS_2') as disease_detection_rate,
    (SELECT Precision FROM diagnosis_performance WHERE Mapping = 'CLASS_2') as positive_pred_accuracy,
    (SELECT Support FROM diagnosis_performance WHERE Mapping = 'CLASS_2') as total_disease_cases,
    (SELECT Support FROM diagnosis_performance WHERE Mapping = 'CLASS_2') *
        (1 - (SELECT Recall FROM diagnosis_performance WHERE Mapping = 'CLASS_2')) as missed_disease_cases,
    (SELECT CLASS_2 FROM diagnosis_performance WHERE Mapping = 'CLASS_1') as false_positive_count,
    -- Costs (example values)
    (SELECT Support FROM diagnosis_performance WHERE Mapping = 'CLASS_2') *
        (1 - (SELECT Recall FROM diagnosis_performance WHERE Mapping = 'CLASS_2')) * 50000 as cost_of_missed_diagnoses,
    (SELECT CLASS_2 FROM diagnosis_performance WHERE Mapping = 'CLASS_1') * 500 as cost_of_false_positives;
```

**Sample Output:**
```
diagnosis           | actual_cases | pct_of_total | Precision | Recall | F1    | missed_diagnoses | false_alarms
--------------------|--------------|--------------|-----------|--------|-------|------------------|-------------
Negative (Healthy)  |       49,000 |        98.00 |  0.994898 | 0.989  | 0.992 |             NULL |          539
Positive (Disease)  |        1,000 |         2.00 |  0.649675 | 0.900  | 0.755 |              100 |         NULL

Metric              | MetricValue | interpretation                          | relevance_for_imbalanced
--------------------|-------------|-----------------------------------------|-------------------------
Macro-F1            |    0.873500 | Equal weight to both classes            | MOST_RELEVANT
Macro-Precision     |    0.822287 | Equal weight to both classes            | MOST_RELEVANT
Macro-Recall        |    0.944500 | Equal weight to both classes            | MOST_RELEVANT
Weighted-F1         |    0.987073 | Weighted by class frequency             | REFERENCE_ONLY
Weighted-Precision  |    0.987851 | Weighted by class frequency             | REFERENCE_ONLY
Weighted-Recall     |    0.989000 | Weighted by class frequency             | REFERENCE_ONLY
Micro-F1            |    0.989000 | Dominated by majority class (Negative)  | REFERENCE_ONLY
Micro-Precision     |    0.989000 | Dominated by majority class (Negative)  | REFERENCE_ONLY
Micro-Recall        |    0.989000 | Dominated by majority class (Negative)  | REFERENCE_ONLY

analysis                        | disease_detection_rate | positive_pred_accuracy | total_disease_cases | missed_disease_cases | false_positive_count | cost_of_missed_diagnoses | cost_of_false_positives
--------------------------------|------------------------|------------------------|---------------------|----------------------|----------------------|--------------------------|------------------------
Disease Detection Performance   |               0.900000 |               0.649675 |               1,000 |                  100 |                  539 |            5,000,000.00  |              269,500.00
```

**Business Impact:** Model achieves 90% recall for rare disease (detects 900 of 1,000 cases), critical for clinical application, but generates 539 false positives (64.9% positive predictive value). Macro-F1 (87.4%) more relevant than micro-F1 (98.9%) for imbalanced data, accounting for rare class performance. Cost analysis: Missing 100 disease cases costs $5M (treatment delay), while 539 false positives cost $269.5K (unnecessary tests), net benefit of $4.73M. Trade-off acceptable given high cost of missed diagnoses. Recommended threshold adjustment to increase recall to 95% even if precision drops further.

---

### Example 5: Production Model Monitoring Over Time
**Business Context:** SaaS company monitoring churn prediction model performance monthly.

```sql
-- Calculate monthly model performance
CREATE TABLE churn_model_monitoring AS (
    SELECT
        evaluation_month,
        dt.*
    FROM (
        SELECT DISTINCT DATE_TRUNC('month', prediction_date) as evaluation_month
        FROM churn_predictions_history
    ) months
    CROSS JOIN LATERAL (
        SELECT * FROM TD_ClassificationEvaluator (
            ON (
                SELECT actual_churn, predicted_churn
                FROM churn_predictions_history
                WHERE DATE_TRUNC('month', prediction_date) = months.evaluation_month
            ) AS InputTable
            OUT TABLE OutputTable(churn_aggregate_temp)
            USING
            ObservationColumn('actual_churn')
            PredictionColumn('predicted_churn')
            Labels('0', '1')  -- 0=retained, 1=churned
        ) AS dt
    )
) WITH DATA;

-- Track performance trends
SELECT
    evaluation_month,
    CASE Mapping
        WHEN 'CLASS_1' THEN 'Retained'
        WHEN 'CLASS_2' THEN 'Churned'
    END as customer_status,
    Support as actual_count,
    Recall,
    Precision,
    F1,
    -- Calculate month-over-month changes
    LAG(Recall) OVER (PARTITION BY Mapping ORDER BY evaluation_month) as prev_month_recall,
    Recall - LAG(Recall) OVER (PARTITION BY Mapping ORDER BY evaluation_month) as recall_change,
    LAG(F1) OVER (PARTITION BY Mapping ORDER BY evaluation_month) as prev_month_f1,
    F1 - LAG(F1) OVER (PARTITION BY Mapping ORDER BY evaluation_month) as f1_change
FROM churn_model_monitoring
WHERE Mapping = 'CLASS_2'  -- Focus on churn class
ORDER BY evaluation_month DESC;

-- Detect model degradation
SELECT
    evaluation_month,
    f1_current_month,
    f1_baseline,
    f1_current_month - f1_baseline as degradation,
    CASE
        WHEN f1_current_month < f1_baseline - 0.10 THEN 'CRITICAL_RETRAIN_REQUIRED'
        WHEN f1_current_month < f1_baseline - 0.05 THEN 'WARNING_MONITOR_CLOSELY'
        ELSE 'ACCEPTABLE'
    END as model_health_status
FROM (
    SELECT
        evaluation_month,
        F1 as f1_current_month,
        FIRST_VALUE(F1) OVER (ORDER BY evaluation_month) as f1_baseline
    FROM churn_model_monitoring
    WHERE Mapping = 'CLASS_2'
) degradation_analysis
ORDER BY evaluation_month DESC;

-- Alert on significant changes
SELECT
    evaluation_month,
    metric_name,
    current_value,
    previous_value,
    pct_change,
    alert_level
FROM (
    SELECT
        evaluation_month,
        'Churn_Recall' as metric_name,
        Recall as current_value,
        LAG(Recall) OVER (ORDER BY evaluation_month) as previous_value,
        (Recall - LAG(Recall) OVER (ORDER BY evaluation_month)) / NULLIF(LAG(Recall) OVER (ORDER BY evaluation_month), 0) * 100 as pct_change,
        CASE
            WHEN ABS((Recall - LAG(Recall) OVER (ORDER BY evaluation_month)) / NULLIF(LAG(Recall) OVER (ORDER BY evaluation_month), 0) * 100) > 10 THEN 'HIGH'
            WHEN ABS((Recall - LAG(Recall) OVER (ORDER BY evaluation_month)) / NULLIF(LAG(Recall) OVER (ORDER BY evaluation_month), 0) * 100) > 5 THEN 'MEDIUM'
            ELSE 'LOW'
        END as alert_level
    FROM churn_model_monitoring
    WHERE Mapping = 'CLASS_2'
) alerts
WHERE alert_level IN ('HIGH', 'MEDIUM')
ORDER BY evaluation_month DESC, alert_level;
```

**Sample Output:**
```
evaluation_month | customer_status | actual_count | Recall | Precision | F1    | prev_month_recall | recall_change | prev_month_f1 | f1_change
-----------------|-----------------|--------------|--------|-----------|-------|-------------------|---------------|---------------|----------
    2024-11-01   | Churned         |        1,234 | 0.7890 |  0.8123   | 0.800 |            0.8234 |       -0.0344 |        0.8345 |   -0.0345
    2024-10-01   | Churned         |        1,189 | 0.8234 |  0.8456   | 0.8345|            0.8345 |       -0.0111 |        0.8456 |   -0.0111
    2024-09-01   | Churned         |        1,145 | 0.8345 |  0.8567   | 0.8456|            0.8423 |       -0.0078 |        0.8512 |   -0.0056
    2024-08-01   | Churned         |        1,098 | 0.8423 |  0.8601   | 0.8512|            0.8456 |       -0.0033 |        0.8534 |   -0.0022

evaluation_month | f1_current_month | f1_baseline | degradation | model_health_status
-----------------|------------------|-------------|-------------|------------------------
    2024-11-01   |           0.8000 |      0.8512 |     -0.0512 | WARNING_MONITOR_CLOSELY
    2024-10-01   |           0.8345 |      0.8512 |     -0.0167 | ACCEPTABLE
    2024-09-01   |           0.8456 |      0.8512 |     -0.0056 | ACCEPTABLE
    2024-08-01   |           0.8512 |      0.8512 |      0.0000 | ACCEPTABLE

evaluation_month | metric_name   | current_value | previous_value | pct_change | alert_level
-----------------|---------------|---------------|----------------|------------|------------
    2024-11-01   | Churn_Recall  |        0.7890 |         0.8234 |      -4.18 | MEDIUM
```

**Business Impact:** Churn prediction model showing performance degradation: F1 score declined 5.1% from baseline (0.851 to 0.800) over 4 months, triggering "WARNING_MONITOR_CLOSELY" alert. Churn recall dropped 3.4% month-over-month in November (from 82.3% to 78.9%), indicating model is missing more churners. Potential cause: customer behavior shifts or feature drift. Recommended immediate model retraining with recent data. Estimated impact: Additional 3.4% missed churners represents ~42 customers ($50K annual revenue at risk).

---

### Example 6: Threshold Optimization Using Evaluation Metrics
**Business Context:** Credit card company optimizing approval threshold based on business costs.

```sql
-- Test multiple threshold values
CREATE TABLE threshold_evaluation AS (
    SELECT
        threshold_value,
        dt.*
    FROM (
        SELECT 0.30 as threshold_value UNION ALL
        SELECT 0.40 UNION ALL
        SELECT 0.50 UNION ALL
        SELECT 0.60 UNION ALL
        SELECT 0.70
    ) thresholds
    CROSS JOIN LATERAL (
        SELECT * FROM TD_ClassificationEvaluator (
            ON (
                SELECT
                    actual_approval,
                    CASE
                        WHEN approval_probability >= thresholds.threshold_value THEN 'Approve'
                        ELSE 'Deny'
                    END as predicted_approval
                FROM credit_applications_scored
            ) AS InputTable
            OUT TABLE OutputTable(threshold_aggregate_temp)
            USING
            ObservationColumn('actual_approval')
            PredictionColumn('predicted_approval')
            Labels('Approve', 'Deny')
        ) AS dt
    )
) WITH DATA;

-- Analyze threshold impact
SELECT
    threshold_value,
    CASE Mapping
        WHEN 'CLASS_1' THEN 'Approve'
        WHEN 'CLASS_2' THEN 'Deny'
    END as decision,
    Precision as approval_accuracy,
    Recall as approval_coverage,
    F1 as approval_f1,
    Support as actual_count
FROM threshold_evaluation
WHERE Mapping = 'CLASS_1'  -- Focus on approval performance
ORDER BY threshold_value;

-- Calculate business metrics per threshold
SELECT
    threshold_value,
    MAX(CASE WHEN Mapping = 'CLASS_1' THEN Recall END) as approval_rate,
    MAX(CASE WHEN Mapping = 'CLASS_1' THEN Precision END) as good_customer_precision,
    MAX(CASE WHEN Mapping = 'CLASS_1' THEN Support END) as actual_good_customers,
    -- Calculate revenue and costs
    MAX(CASE WHEN Mapping = 'CLASS_1' THEN Support * Recall END) * 1000 as approved_good_customers_revenue,
    MAX(CASE WHEN Mapping = 'CLASS_1' THEN Support * (1 - Precision) * Recall END) * 5000 as bad_debt_cost,
    MAX(CASE WHEN Mapping = 'CLASS_1' THEN Support * Recall END) * 1000 -
        MAX(CASE WHEN Mapping = 'CLASS_1' THEN Support * (1 - Precision) * Recall END) * 5000 as net_profit,
    RANK() OVER (ORDER BY
        MAX(CASE WHEN Mapping = 'CLASS_1' THEN Support * Recall END) * 1000 -
        MAX(CASE WHEN Mapping = 'CLASS_1' THEN Support * (1 - Precision) * Recall END) * 5000 DESC
    ) as profitability_rank
FROM threshold_evaluation
GROUP BY threshold_value
ORDER BY net_profit DESC;
```

**Sample Output:**
```
threshold_value | decision | approval_accuracy | approval_coverage | approval_f1 | actual_count
----------------|----------|-------------------|-------------------|-------------|-------------
           0.30 | Approve  |          0.876543 |          0.956789 |    0.915012 |       10,000
           0.40 | Approve  |          0.912345 |          0.923456 |    0.917890 |       10,000
           0.50 | Approve  |          0.934567 |          0.889012 |    0.911234 |       10,000
           0.60 | Approve  |          0.956789 |          0.834567 |    0.891234 |       10,000
           0.70 | Approve  |          0.978901 |          0.767890 |    0.861234 |       10,000

threshold_value | approval_rate | good_customer_precision | actual_good_customers | approved_good_customers_revenue | bad_debt_cost | net_profit   | profitability_rank
----------------|---------------|------------------------|----------------------|--------------------------------|---------------|--------------|-------------------
           0.50 |      0.889012 |               0.934567 |               10,000 |                    8,890,120.00|    581,234.00 | 8,308,886.00 |                  1
           0.40 |      0.923456 |               0.912345 |               10,000 |                    9,234,560.00|  1,012,345.00 | 8,222,215.00 |                  2
           0.60 |      0.834567 |               0.956789 |               10,000 |                    8,345,670.00|    451,234.00 | 7,894,436.00 |                  3
           0.30 |      0.956789 |               0.876543 |               10,000 |                    9,567,890.00|  1,478,901.00 | 8,088,989.00 |                  4
           0.70 |      0.767890 |               0.978901 |               10,000 |                    7,678,900.00|    201,234.00 | 7,477,666.00 |                  5
```

**Business Impact:** Threshold optimization analysis across 5 values (0.30-0.70) identifies 0.50 as optimal for maximizing net profit ($8.31M). At 0.50 threshold: 88.9% approval rate, 93.5% precision (capturing good customers while minimizing bad debt). Lower threshold (0.30) approves more customers (95.7% rate) but increases bad debt cost by $897K. Higher threshold (0.70) reduces bad debt by $380K but sacrifices $831K in revenue from rejected good customers. Recommended deployment at 0.50 threshold balancing revenue capture and risk management.

---

## Common Use Cases

### By Industry

**Financial Services:**
- Fraud detection model evaluation
- Credit risk classification assessment
- Loan approval model comparison
- Anti-money laundering model validation
- Trading signal classification evaluation

**Healthcare:**
- Disease diagnosis model validation
- Patient risk stratification evaluation
- Treatment response prediction assessment
- Medical imaging classification evaluation
- Clinical decision support model validation

**E-commerce & Retail:**
- Customer churn prediction evaluation
- Product recommendation quality assessment
- Customer segment classification validation
- Purchase propensity model comparison
- Fraud detection in transactions

**Marketing & Advertising:**
- Lead scoring model evaluation
- Campaign response prediction assessment
- Customer lifetime value classification
- Email engagement prediction validation
- Ad click prediction model comparison

**Manufacturing:**
- Defect detection model validation
- Equipment failure prediction evaluation
- Quality control classification assessment
- Predictive maintenance model comparison
- Product categorization validation

**Telecommunications:**
- Network anomaly detection evaluation
- Customer churn prediction assessment
- Service quality classification
- Call routing optimization validation
- Device failure prediction evaluation

### By Analytics Task

**Model Development:**
- Compare multiple algorithms
- Validate model before deployment
- Select best features
- Optimize hyperparameters
- Assess generalization

**Production Monitoring:**
- Track model performance over time
- Detect model degradation
- Identify performance drift
- Compare model versions
- Monitor class-specific performance

**Business Optimization:**
- Optimize decision thresholds
- Balance precision vs. recall
- Calculate ROI of predictions
- Assess cost-benefit trade-offs
- Prioritize model improvements

**Compliance and Reporting:**
- Document model performance
- Validate fairness across segments
- Report to stakeholders
- Audit model decisions
- Demonstrate model quality

## Best Practices

### Metric Selection and Interpretation

**1. Choose Appropriate Metrics for Business Context:**

**High Cost of False Positives (e.g., spam filtering, marketing campaigns):**
- Prioritize **Precision**
- Accept lower recall to minimize false alarms
- Example: Email spam filter (false positives annoy users)

**High Cost of False Negatives (e.g., fraud detection, medical diagnosis):**
- Prioritize **Recall**
- Accept lower precision to catch all critical cases
- Example: Cancer screening (missing disease is costly)

**Balanced Importance:**
- Use **F1 Score**
- Balances precision and recall
- Example: Customer churn prediction

**2. Understand Aggregation Methods:**

**Micro-Average:**
- Calculates metrics globally from total TP, FP, FN
- Dominated by frequent classes
- Use when all instances equally important

**Macro-Average:**
- Unweighted mean of per-class metrics
- Treats all classes equally regardless of frequency
- Use when all classes equally important (rare disease detection)

**Weighted-Average:**
- Mean weighted by class frequency (support)
- Balances class importance by frequency
- Use for general model assessment with imbalanced classes

**3. Handle Class Imbalance:**
```sql
-- Check class distribution
SELECT
    actual_class,
    COUNT(*) as count,
    CAST(COUNT(*) AS FLOAT) / SUM(COUNT(*) OVER ()) * 100 as pct
FROM predictions
GROUP BY actual_class
ORDER BY count DESC;

-- Focus on macro metrics for imbalanced data
SELECT Metric, MetricValue
FROM aggregate_metrics
WHERE Metric LIKE 'Macro-%';
```

### Model Comparison

**1. Systematic Comparison Framework:**
```sql
-- Compare models across multiple dimensions
CREATE TABLE model_comparison_scorecard AS (
    SELECT
        model_name,
        accuracy,
        weighted_f1,
        macro_f1,
        minority_class_recall,
        -- Composite score (customize weights for business)
        (accuracy * 0.3 + weighted_f1 * 0.4 + macro_f1 * 0.3) as composite_score
    FROM model_metrics
);
```

**2. Consider Multiple Criteria:**
- Accuracy (overall correctness)
- Class-specific performance (critical classes)
- Consistency across classes (macro metrics)
- Training time and complexity
- Interpretability requirements
- Production inference speed

**3. Statistical Significance:**
- Test multiple random seeds
- Use cross-validation
- Calculate confidence intervals
- Ensure differences are meaningful, not random

### Production Implementation

**1. Establish Baselines and Thresholds:**
```sql
-- Set minimum acceptable thresholds
CREATE TABLE model_quality_gates AS (
    SELECT
        'Minimum_Accuracy' as gate_name,
        0.85 as threshold_value
    UNION ALL
    SELECT 'Minimum_Weighted_F1', 0.80
    UNION ALL
    SELECT 'Minimum_Macro_F1', 0.75
    UNION ALL
    SELECT 'Maximum_Class_F1_Variance', 0.15
);

-- Validate against gates
SELECT
    gate_name,
    threshold_value,
    actual_value,
    CASE
        WHEN actual_value >= threshold_value THEN 'PASS'
        ELSE 'FAIL'
    END as gate_status
FROM model_quality_gates
INNER JOIN current_model_metrics;
```

**2. Monitor Performance Over Time:**
- Calculate metrics monthly/quarterly
- Track trends and detect degradation
- Set alerts for significant drops (>5%)
- Document and investigate changes

**3. Version Control and Documentation:**
- Tag models with version numbers
- Store evaluation results with models
- Document metric thresholds and rationale
- Maintain change log for model updates

**4. A/B Testing in Production:**
- Compare new model to baseline
- Use statistical tests for significance
- Monitor business metrics alongside model metrics
- Gradual rollout with performance monitoring

### Handling Special Cases

**1. Multi-Label Classification:**
- Evaluate each label independently
- Calculate micro/macro/weighted across all labels
- Consider label frequency and importance
- Use appropriate aggregation methods

**2. Extremely Imbalanced Classes:**
- Focus on minority class metrics (recall, precision)
- Use macro-averaging over micro-averaging
- Consider resampling techniques before evaluation
- Evaluate cost-benefit analysis explicitly

**3. Changing Class Distributions:**
- Monitor support (class frequency) over time
- Retrain if distribution shifts significantly
- Use weighted metrics that account for distribution
- Document expected class distributions

**4. Threshold Optimization:**
- Evaluate multiple thresholds systematically
- Calculate business metrics (revenue, cost) per threshold
- Consider operational constraints
- Document threshold selection rationale

## Related Functions

### Model Evaluation Functions
- **TD_RegressionEvaluator**: Evaluate regression model performance
- **TD_ROC**: ROC curves and AUC for binary classification
- **TD_Silhouette**: Clustering quality evaluation
- **TD_TrainTestSplit**: Split data for model validation

### Classification Functions
- **TD_DecisionForest / TD_DecisionForestPredict**: Random forest classification
- **TD_XGBoost / TD_XGBoostPredict**: Gradient boosting classification
- **TD_NaiveBayes / TD_NaiveBayesPredict**: Naive Bayes classification
- **TD_SVM / TD_SVMPredict**: Support vector machine classification
- **TD_GLM / TD_GLMPredict**: Logistic regression

### Data Preparation
- **TD_TrainTestSplit**: Create train/test splits
- **TD_SimpleImputeFit / TD_SimpleImputeTransform**: Handle missing values
- **TD_ScaleFit / TD_ScaleTransform**: Normalize features
- **TD_OneHotEncodingFit**: Encode categorical variables

## Notes and Limitations

### Important Considerations

**1. Requires Actual and Predicted Labels:**
- Function needs both ground truth and predictions
- Cannot evaluate without holdout test set
- Predictions must be final class labels (not probabilities)
- Use TD_ROC for probability-based evaluation

**2. Label Matching Requirements:**
- ObservationColumn and PredictionColumn must have same data type
- All labels in Labels parameter should appear in data
- Missing labels may cause incomplete evaluation
- Consistent encoding required (e.g., all "0"/"1" not mixed with 0/1)

**3. Class Imbalance Impact:**
- Accuracy can be misleading with imbalanced classes
- Micro-averages dominated by frequent classes
- Macro-averages treat all classes equally
- Use appropriate metric for business context

**4. No Probability Scores:**
- Function works with class labels only
- Cannot optimize thresholds directly
- Use TD_ROC for threshold optimization with probabilities
- Convert probabilities to labels before evaluation

**5. Multi-Class Confusion Matrix:**
- Primary output includes confusion matrix as CLASS_N columns
- Number of columns equals number of classes
- Can become wide with many classes (20+ classes)
- May need post-processing for visualization

**6. Output Table Management:**
- Secondary output requires explicit OUT TABLE specification
- VOLATILE tables disappear at session end
- PERMANENT tables require explicit cleanup
- Consider naming conventions for multiple evaluations

### Technical Constraints

**1. Data Type Limitations:**
- ObservationColumn: BYTEINT, SHORTINT, INTEGER, CHAR, VARCHAR
- PredictionColumn: BYTEINT, SHORTINT, INTEGER, CHAR, VARCHAR
- Both must match exactly
- No support for FLOAT/DOUBLE class labels

**2. Label Specification:**
- NumLabels: Assumes integer labels 0, 1, 2, ..., N-1
- Labels: Must explicitly list all possible labels
- Cannot mix NumLabels and Labels parameters
- Labels parameter is case-sensitive for VARCHAR

**3. NULL Handling:**
- NULL predictions or observations may cause errors
- Filter NULLs before evaluation
- Document NULL handling approach
- Consider implications of excluding NULL predictions

**4. Performance Considerations:**
- Large confusion matrices (100+ classes) may be slow
- Wide output tables with many classes
- Consider aggregating rare classes
- Use appropriate sampling for very large datasets

### Best Practices Summary

1. **Choose metrics appropriate** for business context (precision vs. recall trade-off)
2. **Use macro-averaging** for imbalanced classes when all classes equally important
3. **Calculate class-specific metrics** for critical classes (fraud, disease, high-value customers)
4. **Compare multiple models** systematically using consistent evaluation data
5. **Monitor performance over time** to detect model degradation
6. **Set quality gate thresholds** for production deployment
7. **Document metric selection** rationale and business requirements
8. **Handle NULL predictions** explicitly before evaluation
9. **Consider cost-benefit analysis** beyond just accuracy metrics
10. **Use both primary and secondary outputs** for comprehensive evaluation

## Version Information

- **Teradata Vantage Version**: 17.20
- **Function Category**: Model Evaluation
- **Documentation Generated**: November 2024
- **Output**: Dual tables (class-level and aggregate metrics)
