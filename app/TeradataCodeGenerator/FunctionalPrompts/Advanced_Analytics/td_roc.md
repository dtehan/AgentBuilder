# TD_ROC

## Function Name
**TD_ROC** (alias: **TD_ROC_AUC**, **ROC**)

## Description
TD_ROC (Receiver Operating Characteristic) generates ROC curves and computes the Area Under the Curve (AUC) for evaluating binary classification models. The function analyzes the trade-off between True Positive Rate (TPR/Sensitivity/Recall) and False Positive Rate (FPR) across all possible classification thresholds, providing a comprehensive view of model discrimination ability independent of any specific threshold choice.

**Key Characteristics:**
- **Threshold-Independent Evaluation**: Assesses model performance across all possible classification thresholds
- **AUC Metric**: Single scalar metric (0 to 1) summarizing overall model discrimination ability
- **ROC Curve Generation**: Produces coordinate pairs (FPR, TPR) for plotting ROC curves
- **Probability Score Input**: Works with predicted probabilities rather than hard class predictions
- **Imbalanced Class Support**: Performance metric unaffected by class imbalance (unlike accuracy)
- **Model Comparison**: Enables objective comparison of different classification algorithms
- **Optimal Threshold Selection**: Helps identify best threshold for specific business objectives
- **Industry Standard**: Most widely used metric for binary classification evaluation

## When to Use

### Business Applications
1. **Fraud Detection Models**
   - Evaluate fraud probability prediction models
   - Balance fraud detection rate (TPR) vs. false alarm rate (FPR)
   - Find optimal threshold balancing fraud losses and investigation costs
   - Compare fraud detection algorithms (Logistic Regression vs. XGBoost vs. Neural Networks)
   - AUC = 0.95+ indicates excellent fraud discrimination

2. **Credit Risk Scoring**
   - Assess loan default probability models
   - Balance approval rate (accepting good customers) vs. default rate (rejecting bad risks)
   - Determine optimal credit score cutoff for different risk appetites
   - Compare credit scoring methodologies
   - Regulatory compliance (Basel II/III requires model discrimination validation)

3. **Medical Diagnosis Models**
   - Evaluate disease probability prediction models
   - Balance sensitivity (catching true cases) vs. specificity (avoiding false alarms)
   - Find optimal diagnostic threshold for different screening contexts
   - Compare diagnostic algorithms or biomarker panels
   - AUC interpretation: 0.9-1.0 (Excellent), 0.8-0.9 (Good), 0.7-0.8 (Fair), 0.5-0.7 (Poor)

4. **Customer Churn Prediction**
   - Assess churn probability models
   - Balance retention campaign reach (how many customers to target) vs. precision
   - Find threshold maximizing retention ROI
   - Compare churn prediction approaches
   - Optimize for business metrics (revenue saved vs. campaign cost)

5. **Marketing Response Models**
   - Evaluate campaign response probability predictions
   - Balance campaign reach vs. response rate
   - Determine optimal targeting threshold for different campaign economics
   - Compare propensity models
   - Maximize marketing ROI through optimal targeting

6. **Quality Control and Defect Detection**
   - Assess manufacturing defect probability models
   - Balance defect detection rate vs. false rejection rate
   - Find optimal inspection threshold for different cost structures
   - Compare defect detection algorithms
   - Minimize total cost (defect escape cost + false rejection cost)

7. **Cybersecurity Threat Detection**
   - Evaluate security threat probability models
   - Balance threat detection rate vs. false positive rate (alert fatigue)
   - Find optimal alerting threshold
   - Compare threat detection algorithms
   - Optimize SOC (Security Operations Center) efficiency

8. **Conversion Prediction (E-commerce)**
   - Assess purchase probability models
   - Balance targeting breadth vs. conversion rate
   - Optimize ad spend by targeting high-probability converters
   - Compare conversion prediction models
   - Maximize revenue per marketing dollar

### Analytical Use Cases
- **Model Comparison**: Compare AUC across different algorithms to select best model
- **Threshold Selection**: Identify optimal classification threshold for specific business objectives
- **Feature Engineering Validation**: Compare ROC/AUC before and after adding new features
- **Model Monitoring**: Track AUC over time to detect model degradation
- **Calibration Check**: Assess if predicted probabilities reflect true likelihood (complement to Brier score)
- **Imbalanced Classes**: Evaluate models on imbalanced datasets where accuracy is misleading
- **Cost-Sensitive Classification**: Find threshold minimizing total business cost
- **A/B Testing**: Compare champion vs. challenger models using AUC

## Syntax

```sql
SELECT * FROM TD_ROC (
    ON { table | view | (query) } AS InputTable
    [ OUT TABLE OutputTable (output_table_name) ]
    USING
    ObservationColumn ('observation_column')
    ProbabilityColumn ('probability_column')
    [ PositiveLabel ('positive_class_label') ]
    [ NumThresholds (num_thresholds) ]
    [ Accumulate ('column_name' [,...]) ]
) AS alias;
```

## Required Elements

### InputTable
The table containing both observed class labels and predicted probabilities for binary classification evaluation.

**Required Columns:**
- Observation column: Actual class labels (binary: 0/1, TRUE/FALSE, Positive/Negative, Yes/No, etc.)
- Probability column: Predicted probabilities for the positive class (values between 0 and 1)

**Optional Columns:**
- ID columns for tracking individual predictions
- Timestamp columns for temporal analysis
- Model version columns for comparison
- Segment columns for stratified evaluation

### ObservationColumn
**Required parameter** specifying the column containing actual observed class labels.
- **Type**: String (column name)
- **Values**: Binary class labels (numeric 0/1, boolean TRUE/FALSE, or categorical strings)
- **Constraints**: Must contain exactly 2 distinct values; NULL values excluded from analysis

**Example:** `ObservationColumn('actual_churn_flag')`

### ProbabilityColumn
**Required parameter** specifying the column containing predicted probabilities for the positive class.
- **Type**: String (column name)
- **Values**: Continuous numeric probabilities between 0 and 1
- **Constraints**: Should represent P(Positive Class | Features); values outside [0, 1] may be clipped
- **Note**: Most classification models output probabilities via predict_proba() or similar methods

**Example:** `ProbabilityColumn('churn_probability')`

## Optional Elements

### PositiveLabel
Specifies which class label should be treated as the "positive" class (the class of interest).

**Type:** String or Numeric
**Default:** If not specified, function determines positive class automatically (typically the minority class or the higher value)
**Use Cases:**
- Explicitly define positive class when class labels are ambiguous
- Ensure consistent interpretation across multiple evaluations
- Required when class labels are non-standard strings

**Examples:**
- `PositiveLabel('1')` - Class '1' is positive (fraud, churn, disease, etc.)
- `PositiveLabel('TRUE')` - Boolean TRUE is positive class
- `PositiveLabel('Fraud')` - String 'Fraud' is positive class
- `PositiveLabel('Yes')` - String 'Yes' is positive class

**Important:** The probability column should contain P(PositiveLabel | Features)

### NumThresholds
Number of threshold points to generate for ROC curve construction.

**Type:** Integer
**Range:** 10 to 10,000
**Default:** 100 (provides smooth ROC curve for visualization)
**Trade-offs:**
- **Lower values** (10-50): Faster computation, coarser ROC curve, sufficient for AUC calculation
- **Higher values** (500-1,000): Smoother ROC curve for publication-quality plots, slower computation
- **Very high values** (5,000-10,000): Maximum precision for optimal threshold identification

**Example:** `NumThresholds(500)` for high-resolution ROC curve

**Note:** AUC is computed via trapezoidal rule; more thresholds = more accurate AUC (but diminishing returns above ~200)

### Accumulate
Columns to pass through from the InputTable to the output, useful for grouping or tracking.

**Type:** String (column names)
**Use Cases:**
- Model identifiers for comparing multiple models
- Time periods for temporal tracking
- Segments for stratified evaluation
- Data partitions (train/validation/test identification)

**Example:** `Accumulate('model_name', 'evaluation_date', 'customer_segment')`

## Input Specification

### InputTable Schema
```sql
CREATE TABLE classification_predictions (
    prediction_id INTEGER,              -- Optional: Unique identifier
    actual_class VARCHAR(10),           -- Required: Observed class labels (0/1, TRUE/FALSE, etc.)
    predicted_probability FLOAT,        -- Required: Predicted P(Positive Class)
    model_name VARCHAR(50),             -- Optional: For model comparison
    prediction_date DATE,               -- Optional: For temporal tracking
    segment VARCHAR(50),                -- Optional: For stratified analysis
    customer_id INTEGER                 -- Optional: For traceability
);
```

**Requirements:**
- Must contain at least one instance of each class (positive and negative)
- Probability column should contain values between 0 and 1 (though function may handle out-of-range values)
- Observation column must be binary (exactly 2 distinct values)
- Sufficient sample size for reliable ROC curve (minimum 100+ instances, 1000+ recommended)

**Best Practices:**
- Include diverse probability scores (not all near 0 or 1) for meaningful ROC curve
- Ensure probability scores are well-calibrated (P(Y=1) should reflect true probability)
- Maintain balanced or known class distribution for interpretable results
- Include model identifiers when comparing multiple models

## Output Specification

### Primary Output Table Schema
```sql
-- ROC Curve Coordinates (one row per threshold)
threshold           | FLOAT    -- Classification threshold value (0 to 1)
false_positive_rate | FLOAT    -- FPR = FP / (FP + TN) - X-axis of ROC curve
true_positive_rate  | FLOAT    -- TPR = TP / (TP + FN) - Y-axis of ROC curve (Sensitivity/Recall)
false_negatives     | INTEGER  -- Count of false negatives at this threshold
false_positives     | INTEGER  -- Count of false positives at this threshold
true_negatives      | INTEGER  -- Count of true negatives at this threshold
true_positives      | INTEGER  -- Count of true positives at this threshold
-- Accumulated columns (if specified)
model_name          | VARCHAR  -- (if accumulated)
evaluation_date     | DATE     -- (if accumulated)
```

### Secondary Output Table (via OUT TABLE)
```sql
-- Summary Statistics (single row)
AUC                 | FLOAT    -- Area Under the ROC Curve (0 to 1)
num_thresholds      | INTEGER  -- Number of threshold points evaluated
positive_count      | INTEGER  -- Total number of positive class instances
negative_count      | INTEGER  -- Total number of negative class instances
-- Accumulated columns (if specified)
model_name          | VARCHAR  -- (if accumulated)
evaluation_date     | DATE     -- (if accumulated)
```

**Output Characteristics:**

**ROC Curve Coordinates (Primary Output):**
- One row per threshold value
- Thresholds range from 0 (classify all as positive) to 1 (classify all as negative)
- Ordered by threshold ascending
- (FPR, TPR) pairs define the ROC curve for plotting

**Key Points on ROC Curve:**
- **(0, 0)**: Threshold = 1.0, classify nothing as positive (no predictions)
- **(1, 1)**: Threshold = 0.0, classify everything as positive (predict all positive)
- **(0, 1)**: Perfect classifier at optimal threshold (all positives correct, no false positives)
- **Diagonal (0,0) to (1,1)**: Random classifier (AUC = 0.5)

**AUC Interpretation:**
- **AUC = 1.0**: Perfect discrimination (model perfectly separates positive and negative classes)
- **AUC = 0.9 - 1.0**: Excellent discrimination (model nearly perfect)
- **AUC = 0.8 - 0.9**: Good discrimination (model performs well)
- **AUC = 0.7 - 0.8**: Fair discrimination (model has some predictive power)
- **AUC = 0.6 - 0.7**: Poor discrimination (model marginally better than random)
- **AUC = 0.5**: No discrimination (random guessing)
- **AUC < 0.5**: Inverse discrimination (predictions inverted; flip predicted classes to get AUC > 0.5)

**Confusion Matrix Elements at Each Threshold:**
- **True Positives (TP)**: Correctly predicted positive cases
- **False Positives (FP)**: Incorrectly predicted positive (actually negative)
- **True Negatives (TN)**: Correctly predicted negative cases
- **False Negatives (FN)**: Incorrectly predicted negative (actually positive)

**Derived Metrics (can be calculated from output):**
- **TPR (Sensitivity/Recall)**: TP / (TP + FN) - Y-axis of ROC
- **FPR**: FP / (FP + TN) - X-axis of ROC
- **Specificity**: TN / (TN + FP) = 1 - FPR
- **Precision**: TP / (TP + FP)
- **F1 Score**: 2 × (Precision × Recall) / (Precision + Recall)
- **Youden's Index**: TPR - FPR (optimal threshold often chosen as max Youden's Index)

## Code Examples

### Example 1: Basic ROC/AUC Evaluation - Fraud Detection Model

**Business Context:**
A payment processing company built a logistic regression model to predict transaction fraud probability. The fraud detection team needs to evaluate the model's discrimination ability before deployment. They want to understand: (1) Overall model quality (AUC), (2) Trade-off between fraud detection rate (TPR) and false positive rate (FPR), (3) Optimal threshold balancing fraud losses ($500 per fraud) and investigation costs ($50 per false positive).

**SQL Code:**
```sql
-- Step 1: Generate ROC curve and compute AUC
SELECT * FROM TD_ROC (
    ON fraud_predictions AS InputTable
    OUT TABLE fraud_model_auc_summary
    USING
    ObservationColumn('actual_fraud_flag')
    ProbabilityColumn('fraud_probability')
    PositiveLabel('1')  -- '1' indicates fraud
    NumThresholds(100)  -- 100 threshold points for smooth curve
    Accumulate('model_version')
) AS roc_curve
ORDER BY threshold;

-- Step 2: Retrieve AUC summary
SELECT * FROM fraud_model_auc_summary;

-- Step 3: Find optimal threshold using Youden's Index (TPR - FPR)
SELECT
    threshold,
    true_positive_rate AS tpr,
    false_positive_rate AS fpr,
    (true_positive_rate - false_positive_rate) AS youden_index,
    true_positives,
    false_positives,
    false_negatives,
    true_negatives,
    -- Business cost calculation
    (false_negatives * 500) + (false_positives * 50) AS total_cost
FROM fraud_model_roc_curve
ORDER BY youden_index DESC
LIMIT 5;

-- Step 4: Find threshold minimizing total business cost
SELECT
    threshold,
    true_positive_rate AS tpr,
    false_positive_rate AS fpr,
    true_positives,
    false_positives,
    false_negatives,
    -- Business metrics
    (false_negatives * 500) AS fraud_loss,
    (false_positives * 50) AS investigation_cost,
    (false_negatives * 500) + (false_positives * 50) AS total_cost,
    -- Operational metrics
    true_positives + false_positives AS transactions_flagged,
    ROUND(100.0 * true_positives / (true_positives + false_positives), 2) AS precision_pct
FROM fraud_model_roc_curve
ORDER BY total_cost ASC
LIMIT 1;
```

**Sample Output:**
```
-- AUC Summary:
model_version | AUC    | num_thresholds | positive_count | negative_count
--------------+--------+----------------+----------------+----------------
v3.2_logreg   | 0.9234 | 100            | 2,456          | 97,544

-- ROC Curve (first 10 rows):
threshold | fpr    | tpr    | false_positives | false_negatives | true_negatives | true_positives
----------+--------+--------+-----------------+-----------------+----------------+----------------
0.01      | 0.8923 | 0.9878 | 87,023          | 30              | 10,521         | 2,426
0.05      | 0.4567 | 0.9756 | 44,543          | 60              | 53,001         | 2,396
0.10      | 0.2345 | 0.9512 | 22,878          | 120             | 74,666         | 2,336
0.15      | 0.1234 | 0.9187 | 12,037          | 200             | 85,507         | 2,256
0.20      | 0.0678 | 0.8756 | 6,613           | 306             | 90,931         | 2,150
0.25      | 0.0456 | 0.8234 | 4,448           | 434             | 93,096         | 2,022
0.30      | 0.0312 | 0.7612 | 3,043           | 587             | 94,501         | 1,869
0.50      | 0.0123 | 0.5234 | 1,200           | 1,171           | 96,344         | 1,285
0.75      | 0.0034 | 0.2345 | 332             | 1,880           | 97,212         | 576
0.90      | 0.0008 | 0.0912 | 78              | 2,232           | 97,466         | 224

-- Optimal threshold by Youden's Index:
threshold | tpr    | fpr    | youden_index | true_positives | false_positives | false_negatives | true_negatives | total_cost
----------+--------+--------+--------------+----------------+-----------------+-----------------+----------------+------------
0.18      | 0.8921 | 0.0589 | 0.8332       | 2,191          | 5,746           | 265             | 91,798         | $419,800

-- Optimal threshold by total business cost:
threshold | tpr    | fpr    | true_positives | false_positives | false_negatives | fraud_loss | investigation_cost | total_cost | transactions_flagged | precision_pct
----------+--------+--------+----------------+-----------------+-----------------+------------+--------------------+------------+----------------------+---------------
0.22      | 0.8645 | 0.0523 | 2,123          | 5,101           | 333             | $166,500   | $255,050           | $421,550   | 7,224                | 29.38
```

**Business Impact:**
- **Model Quality**: AUC = 0.9234 indicates excellent discrimination ability (>0.9 = excellent)
- **Interpretation**: Model correctly ranks a random fraud transaction higher than a random legitimate transaction 92.34% of the time
- **Deployment Confidence**: AUC > 0.9 provides strong confidence for production deployment

**Threshold Selection Analysis:**
- **Youden's Index Optimal** (Threshold = 0.18):
  - TPR = 89.21% (catches 89.21% of fraud)
  - FPR = 5.89% (5.89% of legitimate transactions flagged)
  - Detects 2,191 of 2,456 frauds (misses 265)
  - Flags 5,746 legitimate transactions for review
  - Total cost: $419,800 (265 × $500 fraud + 5,746 × $50 investigation)

- **Business Cost Optimal** (Threshold = 0.22):
  - TPR = 86.45% (catches 86.45% of fraud)
  - FPR = 5.23% (slightly fewer false positives)
  - Detects 2,123 of 2,456 frauds (misses 333)
  - Flags 5,101 legitimate transactions for review
  - Total cost: $421,550 (333 × $500 fraud + 5,101 × $50 investigation)
  - Precision: 29.38% of flagged transactions are actually fraud

**Operational Decision:**
- **Deploy with threshold = 0.22** (business cost optimized)
- **Flag 7,224 transactions per 100,000** for manual review
- **Catch 86.45% of fraud** (acceptable detection rate)
- **Precision = 29.38%**: Fraud analysts review ~3.4 transactions per confirmed fraud (acceptable workload)
- **Expected savings**: Prevent $1.06M in fraud losses annually (2,123 frauds × $500), invest $255K in investigation
- **Net benefit**: $805K annually vs. no fraud detection

**Alternative Threshold Scenarios:**
- **High sensitivity** (threshold = 0.10): Catch 95.12% of fraud but 23.45% FPR (high investigation cost)
- **High specificity** (threshold = 0.50): Only 1.23% FPR but miss ~48% of fraud (unacceptable)

---

### Example 2: Comparing Multiple Classification Models - Customer Churn Prediction

**Business Context:**
A telecom company developed four different models to predict customer churn probability: (1) Logistic Regression, (2) Random Forest, (3) XGBoost, and (4) Neural Network. The analytics team needs to compare models using AUC to select the best performer. Additionally, they want to visualize ROC curves to understand trade-offs and ensure the winning model performs well across all operating points (thresholds).

**SQL Code:**
```sql
-- Step 1: Combine predictions from all four models
CREATE VOLATILE TABLE all_model_predictions AS (
    SELECT
        c.customer_id,
        c.actual_churn,
        lr.churn_probability AS lr_probability,
        rf.churn_probability AS rf_probability,
        xgb.churn_probability AS xgb_probability,
        nn.churn_probability AS nn_probability,
        c.customer_segment,
        c.evaluation_month
    FROM customer_test_set c
    INNER JOIN logreg_predictions lr ON c.customer_id = lr.customer_id
    INNER JOIN randomforest_predictions rf ON c.customer_id = rf.customer_id
    INNER JOIN xgboost_predictions xgb ON c.customer_id = xgb.customer_id
    INNER JOIN neuralnet_predictions nn ON c.customer_id = nn.customer_id
) WITH DATA PRIMARY INDEX (customer_id) ON COMMIT PRESERVE ROWS;

-- Step 2: Generate ROC curves and AUC for all models in parallel
-- Logistic Regression
SELECT
    'Logistic Regression' AS model_name,
    roc.*
FROM TD_ROC (
    ON all_model_predictions AS InputTable
    OUT TABLE logreg_auc_summary
    USING
    ObservationColumn('actual_churn')
    ProbabilityColumn('lr_probability')
    PositiveLabel('1')
    NumThresholds(200)
) AS roc

UNION ALL

-- Random Forest
SELECT
    'Random Forest' AS model_name,
    roc.*
FROM TD_ROC (
    ON all_model_predictions AS InputTable
    OUT TABLE rf_auc_summary
    USING
    ObservationColumn('actual_churn')
    ProbabilityColumn('rf_probability')
    PositiveLabel('1')
    NumThresholds(200)
) AS roc

UNION ALL

-- XGBoost
SELECT
    'XGBoost' AS model_name,
    roc.*
FROM TD_ROC (
    ON all_model_predictions AS InputTable
    OUT TABLE xgb_auc_summary
    USING
    ObservationColumn('actual_churn')
    ProbabilityColumn('xgb_probability')
    PositiveLabel('1')
    NumThresholds(200)
) AS roc

UNION ALL

-- Neural Network
SELECT
    'Neural Network' AS model_name,
    roc.*
FROM TD_ROC (
    ON all_model_predictions AS InputTable
    OUT TABLE nn_auc_summary
    USING
    ObservationColumn('actual_churn')
    ProbabilityColumn('nn_probability')
    PositiveLabel('1')
    NumThresholds(200)
) AS roc
ORDER BY model_name, threshold;

-- Step 3: Compare AUC across models
SELECT
    'Logistic Regression' AS model_name, AUC, positive_count, negative_count
FROM logreg_auc_summary
UNION ALL
SELECT 'Random Forest' AS model_name, AUC, positive_count, negative_count
FROM rf_auc_summary
UNION ALL
SELECT 'XGBoost' AS model_name, AUC, positive_count, negative_count
FROM xgb_auc_summary
UNION ALL
SELECT 'Neural Network' AS model_name, AUC, positive_count, negative_count
FROM nn_auc_summary
ORDER BY AUC DESC;

-- Step 4: Compare models at specific operating points (TPR targets)
-- Business requirement: Must achieve 80% churn detection rate (TPR = 0.80)
SELECT
    model_name,
    MIN(false_positive_rate) AS fpr_at_80pct_tpr,
    MIN(threshold) AS threshold_for_80pct_tpr,
    MIN(false_positives) AS false_positives_at_80pct_tpr
FROM (
    SELECT 'Logistic Regression' AS model_name, * FROM logreg_roc_curve WHERE true_positive_rate >= 0.80
    UNION ALL
    SELECT 'Random Forest' AS model_name, * FROM rf_roc_curve WHERE true_positive_rate >= 0.80
    UNION ALL
    SELECT 'XGBoost' AS model_name, * FROM xgb_roc_curve WHERE true_positive_rate >= 0.80
    UNION ALL
    SELECT 'Neural Network' AS model_name, * FROM nn_roc_curve WHERE true_positive_rate >= 0.80
) AS models_80tpr
GROUP BY model_name
ORDER BY fpr_at_80pct_tpr ASC;

-- Step 5: Segment-level AUC comparison (best model only - XGBoost)
SELECT
    customer_segment,
    auc_stats.*
FROM TD_ROC (
    ON all_model_predictions AS InputTable
    PARTITION BY customer_segment
    OUT TABLE xgb_segment_auc
    USING
    ObservationColumn('actual_churn')
    ProbabilityColumn('xgb_probability')
    PositiveLabel('1')
    NumThresholds(100)
    Accumulate('customer_segment')
) AS roc_curve
-- Only retrieve AUC summary
WHERE FALSE
UNION ALL
SELECT customer_segment, AUC, positive_count, negative_count
FROM xgb_segment_auc
ORDER BY customer_segment;
```

**Sample Output:**
```
-- AUC Comparison:
model_name           | AUC    | positive_count | negative_count
---------------------+--------+----------------+----------------
XGBoost              | 0.8876 | 4,532          | 45,468
Neural Network       | 0.8734 | 4,532          | 45,468
Random Forest        | 0.8621 | 4,532          | 45,468
Logistic Regression  | 0.8234 | 4,532          | 45,468

-- Performance at 80% TPR Operating Point:
model_name           | fpr_at_80pct_tpr | threshold_for_80pct_tpr | false_positives_at_80pct_tpr
---------------------+------------------+-------------------------+------------------------------
XGBoost              | 0.1234           | 0.32                    | 5,611
Neural Network       | 0.1456           | 0.28                    | 6,620
Random Forest        | 0.1678           | 0.35                    | 7,629
Logistic Regression  | 0.2123           | 0.41                    | 9,651

-- Segment-level AUC (XGBoost):
customer_segment | AUC    | positive_count | negative_count
-----------------+--------+----------------+----------------
High Value       | 0.9123 | 1,234          | 8,766
Medium Value     | 0.8845 | 2,345          | 22,655
Low Value        | 0.8567 | 953            | 14,047
```

**Business Impact:**

**Model Selection - XGBoost Wins:**
- **AUC = 0.8876**: Best discrimination ability (+1.42% vs. Neural Network, +7.8% vs. Logistic Regression)
- **AUC Improvement**: XGBoost provides 0.0642 AUC improvement over Logistic Regression (7.8% relative improvement)
- **Statistical Significance**: 0.0142 AUC difference vs. Neural Network is material for 50K customer base

**Operating Point Analysis (80% TPR Target):**
Business requirement: Retention campaigns must reach 80% of churners (TPR = 0.80)

- **XGBoost**: Achieves 80% TPR with only 12.34% FPR (5,611 false positives)
  - Target 9,237 customers (3,626 actual churners + 5,611 non-churners)
  - Precision = 39.3% (3,626 / 9,237)
  - Campaign cost: 9,237 × $50 retention offer = $461,850

- **Neural Network**: Achieves 80% TPR with 14.56% FPR (6,620 false positives)
  - Target 10,246 customers
  - Precision = 35.4%
  - Campaign cost: $512,300
  - **$50,450 more expensive than XGBoost** for same churn detection rate

- **Logistic Regression**: Achieves 80% TPR with 21.23% FPR (9,651 false positives)
  - Target 13,277 customers
  - Precision = 27.3%
  - Campaign cost: $663,850
  - **$202,000 more expensive than XGBoost** for same detection rate

**Segment Performance (XGBoost):**
- **High Value Customers**: AUC = 0.9123 (excellent) - Most predictable churn behavior
- **Medium Value Customers**: AUC = 0.8845 (good) - Slightly less predictable
- **Low Value Customers**: AUC = 0.8567 (good) - Least predictable but still strong

**ROI Analysis:**
- **Churn Prevention Value**: $2,000 avg lifetime value × 3,626 churners saved × 70% retention success rate = $5.08M
- **Campaign Cost**: $461,850 (targeting 9,237 customers)
- **Net ROI**: $4.62M annual benefit (10:1 return on investment)
- **XGBoost vs. Logistic Regression**: Additional $202K savings on campaign costs + better targeting precision

**Deployment Decision:**
- **Deploy XGBoost model** with threshold = 0.32 for production churn prevention
- **Monthly targeting**: Top ~9,200 customers by churn probability
- **Segment-specific thresholds**: Consider lower threshold for High Value segment (higher AUC allows tighter targeting)
- **A/B Test**: Run XGBoost vs. Neural Network A/B test to validate 1.42% AUC difference translates to business impact

**Visualization Insight:**
- XGBoost ROC curve dominates others across most operating points (consistently higher TPR for same FPR)
- All models show similar performance at extreme thresholds (very high TPR/FPR or very low TPR/FPR)
- XGBoost advantage most pronounced in business-relevant range (60-90% TPR, 10-25% FPR)

---

### Example 3: Optimal Threshold Selection for Cost-Sensitive Classification - Medical Diagnosis

**Business Context:**
A healthcare provider developed a model to predict diabetes risk from patient screening data. The model outputs a probability score (0-1) indicating diabetes likelihood. The clinical team needs to select an optimal classification threshold balancing two objectives: (1) High sensitivity (catch as many true diabetes cases as possible - minimize false negatives), and (2) Reasonable specificity (avoid unnecessary follow-up tests - minimize false positives). False negatives cost $10,000 (delayed treatment), while false positives cost $500 (unnecessary confirmatory tests).

**SQL Code:**
```sql
-- Step 1: Generate ROC curve with high resolution for precise threshold selection
SELECT * FROM TD_ROC (
    ON diabetes_risk_predictions AS InputTable
    OUT TABLE diabetes_model_auc
    USING
    ObservationColumn('actual_diabetes_diagnosis')
    ProbabilityColumn('diabetes_risk_probability')
    PositiveLabel('1')  -- '1' = Diabetes
    NumThresholds(1000)  -- High resolution for precise threshold selection
) AS roc_curve
ORDER BY threshold;

-- Step 2: Calculate business metrics for each threshold
CREATE VOLATILE TABLE threshold_business_analysis AS (
    SELECT
        threshold,
        true_positive_rate AS sensitivity,
        1 - false_positive_rate AS specificity,
        false_positive_rate,
        true_positives,
        false_positives,
        true_negatives,
        false_negatives,

        -- Clinical metrics
        ROUND(100.0 * true_positives / (true_positives + false_negatives), 2) AS detection_rate_pct,
        ROUND(100.0 * true_positives / (true_positives + false_positives), 2) AS positive_predictive_value_pct,

        -- Youden's Index (common optimal threshold metric)
        true_positive_rate + (1 - false_positive_rate) - 1 AS youden_index,

        -- Business costs
        (false_negatives * 10000) AS missed_diagnosis_cost,
        (false_positives * 500) AS unnecessary_test_cost,
        (false_negatives * 10000) + (false_positives * 500) AS total_cost,

        -- Patients affected
        true_positives + false_positives AS patients_flagged_for_followup,
        false_negatives AS missed_diabetes_cases

    FROM diabetes_roc_curve
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 3: Find threshold minimizing total business cost
SELECT
    threshold,
    sensitivity,
    specificity,
    detection_rate_pct,
    positive_predictive_value_pct,
    missed_diabetes_cases,
    patients_flagged_for_followup,
    missed_diagnosis_cost,
    unnecessary_test_cost,
    total_cost,
    youden_index
FROM threshold_business_analysis
ORDER BY total_cost ASC
LIMIT 1;

-- Step 4: Compare multiple threshold strategies
SELECT
    strategy_name,
    threshold,
    sensitivity,
    specificity,
    detection_rate_pct,
    missed_diabetes_cases,
    patients_flagged_for_followup,
    total_cost
FROM (
    -- Strategy 1: Minimize total business cost
    SELECT
        'Min Total Cost' AS strategy_name,
        *
    FROM threshold_business_analysis
    ORDER BY total_cost ASC
    LIMIT 1

    UNION ALL

    -- Strategy 2: Maximize Youden's Index (balanced sensitivity/specificity)
    SELECT
        'Max Youden Index' AS strategy_name,
        *
    FROM threshold_business_analysis
    ORDER BY youden_index DESC
    LIMIT 1

    UNION ALL

    -- Strategy 3: Target 95% sensitivity (clinical guideline)
    SELECT
        '95% Sensitivity Target' AS strategy_name,
        *
    FROM threshold_business_analysis
    WHERE sensitivity >= 0.95
    ORDER BY specificity DESC
    LIMIT 1

    UNION ALL

    -- Strategy 4: Target 90% specificity (reduce false alarms)
    SELECT
        '90% Specificity Target' AS strategy_name,
        *
    FROM threshold_business_analysis
    WHERE specificity >= 0.90
    ORDER BY sensitivity DESC
    LIMIT 1

    UNION ALL

    -- Strategy 5: Maximize F1 score (harmonic mean of precision and recall)
    SELECT
        'Max F1 Score' AS strategy_name,
        *
    FROM (
        SELECT
            *,
            2.0 * (positive_predictive_value_pct / 100.0) * sensitivity /
                ((positive_predictive_value_pct / 100.0) + sensitivity) AS f1_score
        FROM threshold_business_analysis
    ) WITH_F1
    ORDER BY f1_score DESC
    LIMIT 1
) AS strategies
ORDER BY total_cost ASC;

-- Step 5: Sensitivity analysis - how does total cost change around optimal threshold?
SELECT
    threshold,
    sensitivity,
    specificity,
    total_cost,
    total_cost - MIN(total_cost) OVER () AS cost_vs_optimal,
    ROUND(100.0 * (total_cost - MIN(total_cost) OVER ()) / MIN(total_cost) OVER (), 2) AS pct_cost_increase
FROM threshold_business_analysis
WHERE threshold BETWEEN
    (SELECT threshold FROM threshold_business_analysis ORDER BY total_cost ASC LIMIT 1) - 0.05
    AND
    (SELECT threshold FROM threshold_business_analysis ORDER BY total_cost ASC LIMIT 1) + 0.05
ORDER BY threshold;

-- Step 6: Retrieve overall model quality (AUC)
SELECT * FROM diabetes_model_auc;
```

**Sample Output:**
```
-- Overall Model Quality:
AUC    | num_thresholds | positive_count | negative_count
-------+----------------+----------------+----------------
0.8945 | 1000           | 2,345          | 47,655

-- Optimal Threshold (Minimum Total Cost):
threshold | sensitivity | specificity | detection_rate_pct | positive_predictive_value_pct | missed_diabetes_cases | patients_flagged_for_followup | missed_diagnosis_cost | unnecessary_test_cost | total_cost | youden_index
----------+-------------+-------------+--------------------+-------------------------------+-----------------------+-------------------------------+-----------------------+-----------------------+------------+--------------
0.276     | 0.8923      | 0.8234      | 89.23              | 24.87                         | 252                   | 8,438                         | $2,520,000            | $4,219,000            | $6,739,000 | 0.7157

-- Threshold Strategy Comparison:
strategy_name            | threshold | sensitivity | specificity | detection_rate_pct | missed_diabetes_cases | patients_flagged_for_followup | total_cost
-------------------------+-----------+-------------+-------------+--------------------+-----------------------+-------------------------------+------------
Min Total Cost           | 0.276     | 0.8923      | 0.8234      | 89.23              | 252                   | 8,438                         | $6,739,000
Max F1 Score             | 0.312     | 0.8645      | 0.8567      | 86.45              | 318                   | 7,189                         | $6,774,450
Max Youden Index         | 0.298     | 0.8789      | 0.8412      | 87.89              | 284                   | 7,845                         | $6,762,250
90% Specificity Target   | 0.445     | 0.7234      | 0.9012      | 72.34              | 649                   | 5,411                         | $9,195,500
95% Sensitivity Target   | 0.198     | 0.9512      | 0.7123      | 95.12              | 114                   | 15,952                        | $9,116,000

-- Sensitivity Analysis (±0.05 around optimal):
threshold | sensitivity | specificity | total_cost | cost_vs_optimal | pct_cost_increase
----------+-------------+-------------+------------+-----------------+-------------------
0.226     | 0.9234      | 0.7645      | $7,456,750 | $717,750        | 10.65%
0.240     | 0.9123      | 0.7867      | $7,012,350 | $273,350        | 4.06%
0.255     | 0.9012      | 0.8023      | $6,823,450 | $84,450         | 1.25%
0.276     | 0.8923      | 0.8234      | $6,739,000 | $0              | 0.00%   ← OPTIMAL
0.290     | 0.8834      | 0.8345      | $6,771,500 | $32,500         | 0.48%
0.310     | 0.8678      | 0.8534      | $6,829,000 | $90,000         | 1.34%
0.326     | 0.8545      | 0.8698      | $6,932,750 | $193,750        | 2.87%
```

**Business Impact:**

**Model Quality:**
- **AUC = 0.8945**: Excellent discrimination (close to 0.9 threshold)
- Model effectively separates diabetes patients from non-diabetes patients
- Strong confidence for clinical deployment

**Optimal Threshold Selection (Minimize Total Cost):**
- **Threshold = 0.276**: Flag patients with ≥27.6% diabetes risk
- **Sensitivity = 89.23%**: Detect 89.23% of diabetes cases (2,093 of 2,345)
- **Specificity = 82.34%**: Correctly identify 82.34% of non-diabetes patients
- **Missed Cases**: 252 diabetes patients not detected (false negatives)
- **Unnecessary Tests**: 8,438 false positives (non-diabetes patients flagged)

**Cost Analysis:**
- **Missed Diagnosis Cost**: 252 × $10,000 = $2,520,000 (delayed treatment complications)
- **Unnecessary Test Cost**: 8,438 × $500 = $4,219,000 (confirmatory tests for non-diabetes)
- **Total Cost**: $6,739,000 annually
- **Patients Flagged**: 8,438 patients for follow-up confirmatory testing
- **Positive Predictive Value**: 24.87% of flagged patients actually have diabetes

**Strategy Comparison:**

1. **Min Total Cost (threshold = 0.276)**: $6,739,000 ← OPTIMAL
   - Balanced approach considering both error types
   - 89% sensitivity acceptable for screening program

2. **Max Youden Index (threshold = 0.298)**: $6,762,250 (+$23,250 vs. optimal)
   - Slightly lower sensitivity (87.89%), higher specificity (84.12%)
   - Traditional statistical optimal point (maximizes TPR + TNR - 1)
   - Nearly equivalent to business optimal

3. **Max F1 Score (threshold = 0.312)**: $6,774,450 (+$35,450 vs. optimal)
   - Balances precision and recall
   - Fewer false positives (7,189) but more missed cases (318)

4. **95% Sensitivity Target (threshold = 0.198)**: $9,116,000 (+$2,377,000 vs. optimal)
   - Catches 95.12% of diabetes cases (only 114 missed)
   - But flags 15,952 patients (89% more than optimal)
   - Overwhelms clinical capacity with false positives
   - **35% more expensive** than optimal

5. **90% Specificity Target (threshold = 0.445)**: $9,195,500 (+$2,456,500 vs. optimal)
   - Reduces false positives to 5,411 (36% fewer)
   - But misses 649 diabetes cases (158% more than optimal)
   - High cost of missed diagnoses outweighs savings on unnecessary tests
   - **36% more expensive** than optimal

**Sensitivity Analysis:**
- **Robust Optimal Region**: Cost increases only 1.25% if threshold varies by ±0.02 (0.255 to 0.290)
- **Sharp Cost Increase Outside Range**: 10.65% cost increase if threshold drops to 0.226 (too many false positives)
- **Recommendation**: Set threshold = 0.28 with ±0.02 tolerance band for operational flexibility

**Clinical Decision:**
- **Deploy with threshold = 0.276** (27.6% risk)
- **Screening Protocol**: Flag ~8,400 patients annually for confirmatory HbA1c test
- **Detection Rate**: Catch 89% of diabetes cases in screening population
- **Clinical Workflow**: Manageable false positive rate (82% specificity)
- **Cost-Benefit**: Optimal balance given $10K missed diagnosis cost vs. $500 false positive cost

**Alternative Scenarios:**
- **If false negative cost increases to $15K**: Optimal threshold shifts to ~0.24 (higher sensitivity priority)
- **If confirmatory test cost drops to $200**: Optimal threshold shifts to ~0.20 (lower cost of false positives)
- **Population-specific**: Consider different thresholds for high-risk populations (family history, obesity, age >45)

---

### Example 4: Production Model Monitoring - Tracking AUC Over Time

**Business Context:**
A credit card company deployed a fraud detection model 24 months ago. The risk management team monitors model AUC monthly to detect performance degradation that could result from fraud pattern evolution (concept drift) or data quality issues. They have established alert thresholds: AUC drop >5% triggers investigation, AUC drop >10% triggers immediate retraining.

**SQL Code:**
```sql
-- Step 1: Compute monthly AUC for the past 24 months
SELECT
    evaluation_month,
    auc_stats.*
FROM TD_ROC (
    ON monthly_fraud_predictions AS InputTable
    PARTITION BY evaluation_month
    OUT TABLE monthly_auc_summary
    USING
    ObservationColumn('actual_fraud')
    ProbabilityColumn('fraud_probability')
    PositiveLabel('1')
    NumThresholds(100)
    Accumulate('evaluation_month')
) AS roc_curve
-- Don't retrieve full ROC curve, just interested in AUC summary
WHERE FALSE;

-- Step 2: Retrieve monthly AUC summary with trend analysis
SELECT
    evaluation_month,
    AUC AS current_auc,
    positive_count AS fraud_count,
    negative_count AS legitimate_count,
    -- Calculate baseline (first 3 months average)
    AVG(AUC) OVER (ORDER BY evaluation_month ROWS BETWEEN 23 PRECEDING AND 21 PRECEDING) AS baseline_auc,
    -- Calculate trends
    AUC - LAG(AUC, 1) OVER (ORDER BY evaluation_month) AS mom_auc_change,
    AUC - LAG(AUC, 3) OVER (ORDER BY evaluation_month) AS qoq_auc_change,
    AUC - AVG(AUC) OVER (ORDER BY evaluation_month ROWS BETWEEN 23 PRECEDING AND 21 PRECEDING) AS auc_vs_baseline,
    ROUND(100.0 * (AUC - AVG(AUC) OVER (ORDER BY evaluation_month ROWS BETWEEN 23 PRECEDING AND 21 PRECEDING)) /
        AVG(AUC) OVER (ORDER BY evaluation_month ROWS BETWEEN 23 PRECEDING AND 21 PRECEDING), 2) AS pct_change_vs_baseline,
    -- Alert flags
    CASE
        WHEN AUC - AVG(AUC) OVER (ORDER BY evaluation_month ROWS BETWEEN 23 PRECEDING AND 21 PRECEDING) < -0.10
        THEN 'CRITICAL: AUC Drop >10%'
        WHEN AUC - AVG(AUC) OVER (ORDER BY evaluation_month ROWS BETWEEN 23 PRECEDING AND 21 PRECEDING) < -0.05
        THEN 'WARNING: AUC Drop >5%'
        WHEN AUC < 0.85
        THEN 'WARNING: AUC Below Target'
        ELSE 'OK'
    END AS status_flag
FROM monthly_auc_summary
ORDER BY evaluation_month;

-- Step 3: Identify alert periods
SELECT
    evaluation_month,
    current_auc,
    baseline_auc,
    auc_vs_baseline,
    pct_change_vs_baseline,
    fraud_count,
    status_flag
FROM monthly_auc_trend_analysis
WHERE status_flag != 'OK'
ORDER BY evaluation_month;

-- Step 4: Investigate degraded periods by fraud type
SELECT
    fraud_type,
    evaluation_month,
    auc_stats.*
FROM TD_ROC (
    ON (
        SELECT * FROM monthly_fraud_predictions
        WHERE evaluation_month >= '2024-06-01'  -- Recent degradation period
    ) AS InputTable
    PARTITION BY fraud_type, evaluation_month
    OUT TABLE fraud_type_auc
    USING
    ObservationColumn('actual_fraud')
    ProbabilityColumn('fraud_probability')
    PositiveLabel('1')
    NumThresholds(100)
    Accumulate('fraud_type', 'evaluation_month')
) AS roc_curve
WHERE FALSE;

SELECT * FROM fraud_type_auc
ORDER BY fraud_type, evaluation_month;

-- Step 5: Compare current model to retrained challenger model
SELECT
    'Champion (Current)' AS model_type,
    auc.*
FROM TD_ROC (
    ON fraud_predictions_champion AS InputTable
    OUT TABLE champion_auc
    USING
    ObservationColumn('actual_fraud')
    ProbabilityColumn('fraud_probability')
    PositiveLabel('1')
    NumThresholds(200)
) AS roc

UNION ALL

SELECT
    'Challenger (Retrained)' AS model_type,
    auc.*
FROM TD_ROC (
    ON fraud_predictions_challenger AS InputTable
    OUT TABLE challenger_auc
    USING
    ObservationColumn('actual_fraud')
    ProbabilityColumn('fraud_probability')
    PositiveLabel('1')
    NumThresholds(200)
) AS roc;

SELECT model_type, AUC, positive_count, negative_count
FROM (
    SELECT 'Champion' AS model_type, * FROM champion_auc
    UNION ALL
    SELECT 'Challenger' AS model_type, * FROM challenger_auc
) ORDER BY AUC DESC;
```

**Sample Output:**
```
-- Monthly AUC Trend (24 months):
evaluation_month | current_auc | fraud_count | legitimate_count | baseline_auc | mom_auc_change | qoq_auc_change | auc_vs_baseline | pct_change_vs_baseline | status_flag
-----------------+-------------+-------------+------------------+--------------+----------------+----------------+-----------------+------------------------+---------------------------
2023-01-01       | 0.9234      | 1,234       | 123,456          | NULL         | NULL           | NULL           | NULL            | NULL                   | OK
2023-02-01       | 0.9245      | 1,189       | 124,567          | NULL         | +0.0011        | NULL           | NULL            | NULL                   | OK
2023-03-01       | 0.9256      | 1,302       | 125,234          | NULL         | +0.0011        | NULL           | NULL            | NULL                   | OK
2023-04-01       | 0.9241      | 1,267       | 126,012          | 0.9245       | -0.0015        | NULL           | -0.0004         | -0.04                  | OK
...
2024-06-01       | 0.8923      | 1,456       | 145,678          | 0.9245       | -0.0123        | -0.0234        | -0.0322         | -3.48                  | OK
2024-07-01       | 0.8812      | 1,523       | 147,890          | 0.9245       | -0.0111        | -0.0289        | -0.0433         | -4.68                  | WARNING: AUC Below Target
2024-08-01       | 0.8734      | 1,601       | 149,234          | 0.9245       | -0.0078        | -0.0345        | -0.0511         | -5.53                  | WARNING: AUC Drop >5%
2024-09-01       | 0.8645      | 1,689       | 151,023          | 0.9245       | -0.0089        | -0.0398        | -0.0600         | -6.49                  | WARNING: AUC Drop >5%
2024-10-01       | 0.8534      | 1,756       | 153,456          | 0.9245       | -0.0111        | -0.0478        | -0.0711         | -7.69                  | WARNING: AUC Drop >5%
2024-11-01       | 0.8412      | 1,834       | 155,892          | 0.9245       | -0.0122        | -0.0533        | -0.0833         | -9.01                  | CRITICAL: AUC Drop >10%

-- Alert periods summary:
evaluation_month | current_auc | baseline_auc | auc_vs_baseline | pct_change_vs_baseline | fraud_count | status_flag
-----------------+-------------+--------------+-----------------+------------------------+-------------+---------------------------
2024-07-01       | 0.8812      | 0.9245       | -0.0433         | -4.68                  | 1,523       | WARNING: AUC Below Target
2024-08-01       | 0.8734      | 0.9245       | -0.0511         | -5.53                  | 1,601       | WARNING: AUC Drop >5%
2024-09-01       | 0.8645      | 0.9245       | -0.0600         | -6.49                  | 1,689       | WARNING: AUC Drop >5%
2024-10-01       | 0.8534      | 0.9245       | -0.0711         | -7.69                  | 1,756       | WARNING: AUC Drop >5%
2024-11-01       | 0.8412      | 0.9245       | -0.0833         | -9.01                  | 1,834       | CRITICAL: AUC Drop >10%

-- Fraud type analysis (recent period):
fraud_type               | evaluation_month | AUC    | positive_count | negative_count
-------------------------+------------------+--------+----------------+----------------
Account Takeover         | 2024-06-01       | 0.9123 | 234            | 145,444
Account Takeover         | 2024-07-01       | 0.9087 | 256            | 147,634
Account Takeover         | 2024-08-01       | 0.9045 | 278            | 148,956
Synthetic Identity       | 2024-06-01       | 0.8923 | 123            | 145,555
Synthetic Identity       | 2024-07-01       | 0.8812 | 145            | 147,745
Synthetic Identity       | 2024-08-01       | 0.8734 | 167            | 149,067
Card Not Present (CNP)   | 2024-06-01       | 0.7823 | 567            | 144,911
Card Not Present (CNP)   | 2024-07-01       | 0.7234 | 623            | 147,267  ← DEGRADING
Card Not Present (CNP)   | 2024-08-01       | 0.6845 | 689            | 148,545  ← CRITICAL
Application Fraud        | 2024-06-01       | 0.9045 | 298            | 145,380
Application Fraud        | 2024-07-01       | 0.8987 | 312            | 147,578
Application Fraud        | 2024-08-01       | 0.8923 | 327            | 148,907

-- Champion vs. Challenger comparison:
model_type              | AUC    | positive_count | negative_count
------------------------+--------+----------------+----------------
Challenger (Retrained)  | 0.9012 | 3,456          | 296,544
Champion (Current)      | 0.8412 | 3,456          | 296,544
```

**Business Impact:**

**Model Degradation Detected:**
- **Baseline AUC**: 0.9245 (average of first 3 months: Jan-Mar 2023)
- **Current AUC**: 0.8412 (Nov 2024)
- **Degradation**: -0.0833 AUC (-9.01% decline)
- **Status**: CRITICAL alert triggered (>10% drop threshold breached - actually 9.01% but trending toward 10%)
- **Trend**: Consistent decline over 5 months (June - Nov 2024)

**Month-over-Month Degradation:**
- June 2024: AUC = 0.8923 (first warning sign)
- July 2024: AUC = 0.8812 (-1.11% MoM, breach of 0.85 minimum threshold)
- August 2024: AUC = 0.8734 (-0.78% MoM, cumulative -5.53% vs. baseline)
- September 2024: AUC = 0.8645 (-0.89% MoM, cumulative -6.49% vs. baseline)
- October 2024: AUC = 0.8534 (-1.11% MoM, cumulative -7.69% vs. baseline)
- November 2024: AUC = 0.8412 (-1.22% MoM, cumulative -9.01% vs. baseline - **CRITICAL**)

**Root Cause Analysis - Fraud Type Breakdown:**
- **Card Not Present (CNP) Fraud**: PRIMARY ISSUE
  - AUC degraded from 0.7823 (June) to 0.6845 (August) - **12.5% decline**
  - AUC = 0.6845 is POOR (barely better than random guessing at 0.5)
  - CNP fraud volume increasing: 567 → 689 cases (+21.5%)
  - Hypothesis: E-commerce fraud patterns evolved (new fraud techniques not in training data)

- **Account Takeover**: Stable performance
  - AUC remains strong: 0.9123 → 0.9045 (only -0.78% decline)
  - Model still effective for this fraud type

- **Synthetic Identity**: Moderate degradation
  - AUC: 0.8923 → 0.8734 (-2.12% decline)
  - Acceptable performance but trending down

- **Application Fraud**: Stable performance
  - AUC: 0.9045 → 0.8923 (-1.35% decline)
  - Within acceptable variation

**Fraud Volume Trends:**
- Overall fraud count increasing: 1,456 (June) → 1,834 (Nov) +26%
- Fraudsters adapting faster than model can keep up
- CNP fraud driving both volume increase and model degradation

**Champion vs. Challenger Analysis:**
- **Challenger Model** (retrained on recent 12 months): AUC = 0.9012
- **Champion Model** (current production, trained 24 months ago): AUC = 0.8412
- **Improvement**: +0.0600 AUC (+7.1% relative improvement)
- **Retrained model recovers nearly all degradation** (vs. baseline 0.9245)

**Financial Impact of Degradation:**
- **At baseline AUC (0.9245)**: Detect 92% of fraud at 5% FPR (estimated from typical ROC curve)
- **At degraded AUC (0.8412)**: Detect only 82% of fraud at same 5% FPR (10% fewer frauds caught)
- **Missed fraud**: 10% of 1,834 monthly frauds = 183 additional fraud losses
- **Average fraud amount**: $2,500
- **Monthly cost of degradation**: 183 × $2,500 = $457,500
- **6-month cost** (June - Nov 2024): Estimated $2.1M - $2.7M in additional fraud losses
- **Annual cost if not addressed**: $5.5M+ in preventable fraud

**Immediate Actions:**

1. **URGENT - Deploy Challenger Model**:
   - Retrained model AUC = 0.9012 (recovers 7.1% performance)
   - Expected fraud reduction: ~150 fewer fraud cases per month
   - Estimated savings: $375K monthly ($4.5M annually)

2. **CNP-Specific Model Enhancement**:
   - Build specialized CNP fraud sub-model or feature engineering
   - Add new CNP fraud indicators (device fingerprinting, behavioral analytics)
   - Target AUC > 0.85 for CNP fraud type

3. **Automated Retraining Pipeline**:
   - Implement quarterly model retraining (vs. current ad-hoc approach)
   - Automated AUC monitoring with Slack/email alerts
   - Trigger retraining if AUC drops >3% or fraud patterns shift

4. **Feature Engineering Investigation**:
   - Hypothesis: CNP fraud patterns evolved (new ecommerce fraud tactics)
   - Add features: merchant category analysis, shipping address validation, velocity checks
   - Investigate recent CNP fraud cases for new patterns

**Long-Term Strategy:**
- **Continuous learning**: Implement online learning or weekly model updates for CNP fraud
- **Ensemble approach**: Combine general fraud model + CNP-specific model
- **Fraud intelligence integration**: Incorporate external fraud intelligence feeds
- **A/B testing framework**: Continuously test challenger models in production (10% traffic)

**Regulatory Considerations:**
- Model degradation impacts regulatory capital requirements (Basel III)
- Document root cause analysis and remediation plan for auditors
- Update model risk management documentation with new retraining schedule

---

### Example 5: Imbalanced Classification - Rare Event Detection

**Business Context:**
A pharmaceutical company developed a model to predict serious adverse drug events (SADEs) from patient monitoring data. SADEs are rare (0.3% prevalence) but critical to detect. Accuracy is a misleading metric due to extreme class imbalance (99.7% non-SADE). AUC and ROC curve provide proper evaluation, as they're unaffected by class imbalance. The clinical team needs to select a threshold achieving 90% SADE detection (sensitivity) while minimizing false alarms (low FPR).

**SQL Code:**
```sql
-- Step 1: Generate ROC curve for rare event model
SELECT * FROM TD_ROC (
    ON adverse_event_predictions AS InputTable
    OUT TABLE sade_model_auc
    USING
    ObservationColumn('actual_sade')
    ProbabilityColumn('sade_probability')
    PositiveLabel('1')  -- '1' = Serious Adverse Drug Event
    NumThresholds(500)  -- High resolution for rare event
) AS roc_curve
ORDER BY threshold;

-- Step 2: Check model quality (AUC)
SELECT
    AUC,
    positive_count AS sade_count,
    negative_count AS non_sade_count,
    ROUND(100.0 * positive_count / (positive_count + negative_count), 3) AS sade_prevalence_pct
FROM sade_model_auc;

-- Step 3: Find threshold achieving 90% sensitivity target
SELECT
    threshold,
    true_positive_rate AS sensitivity,
    false_positive_rate AS fpr,
    1 - false_positive_rate AS specificity,
    true_positives AS sade_detected,
    false_negatives AS sade_missed,
    false_positives AS false_alarms,
    true_negatives,
    -- Clinical metrics
    ROUND(100.0 * true_positives / (true_positives + false_positives), 2) AS positive_predictive_value_pct,
    ROUND(100.0 * true_negatives / (true_negatives + false_negatives), 2) AS negative_predictive_value_pct,
    -- Operational metrics
    true_positives + false_positives AS patients_flagged,
    ROUND(100.0 * (true_positives + false_positives) / (true_positives + false_positives + true_negatives + false_negatives), 2) AS pct_patients_flagged
FROM sade_roc_curve
WHERE true_positive_rate >= 0.90
ORDER BY false_positive_rate ASC
LIMIT 5;

-- Step 4: Compare performance at different sensitivity targets
SELECT
    sensitivity_target,
    threshold,
    sensitivity,
    specificity,
    fpr,
    sade_detected,
    sade_missed,
    false_alarms,
    patients_flagged,
    positive_predictive_value_pct
FROM (
    -- 80% sensitivity
    SELECT
        '80% Sensitivity' AS sensitivity_target,
        threshold,
        true_positive_rate AS sensitivity,
        1 - false_positive_rate AS specificity,
        false_positive_rate AS fpr,
        true_positives AS sade_detected,
        false_negatives AS sade_missed,
        false_positives AS false_alarms,
        true_positives + false_positives AS patients_flagged,
        ROUND(100.0 * true_positives / (true_positives + false_positives), 2) AS positive_predictive_value_pct
    FROM sade_roc_curve
    WHERE true_positive_rate >= 0.80
    ORDER BY false_positive_rate ASC
    LIMIT 1

    UNION ALL

    -- 90% sensitivity
    SELECT
        '90% Sensitivity' AS sensitivity_target,
        threshold,
        true_positive_rate AS sensitivity,
        1 - false_positive_rate AS specificity,
        false_positive_rate AS fpr,
        true_positives AS sade_detected,
        false_negatives AS sade_missed,
        false_positives AS false_alarms,
        true_positives + false_positives AS patients_flagged,
        ROUND(100.0 * true_positives / (true_positives + false_positives), 2) AS positive_predictive_value_pct
    FROM sade_roc_curve
    WHERE true_positive_rate >= 0.90
    ORDER BY false_positive_rate ASC
    LIMIT 1

    UNION ALL

    -- 95% sensitivity
    SELECT
        '95% Sensitivity' AS sensitivity_target,
        threshold,
        true_positive_rate AS sensitivity,
        1 - false_positive_rate AS specificity,
        false_positive_rate AS fpr,
        true_positives AS sade_detected,
        false_negatives AS sade_missed,
        false_positives AS false_alarms,
        true_positives + false_positives AS patients_flagged,
        ROUND(100.0 * true_positives / (true_positives + false_positives), 2) AS positive_predictive_value_pct
    FROM sade_roc_curve
    WHERE true_positive_rate >= 0.95
    ORDER BY false_positive_rate ASC
    LIMIT 1

    UNION ALL

    -- 99% sensitivity
    SELECT
        '99% Sensitivity' AS sensitivity_target,
        threshold,
        true_positive_rate AS sensitivity,
        1 - false_positive_rate AS specificity,
        false_positive_rate AS fpr,
        true_positives AS sade_detected,
        false_negatives AS sade_missed,
        false_positives AS false_alarms,
        true_positives + false_positives AS patients_flagged,
        ROUND(100.0 * true_positives / (true_positives + false_positives), 2) AS positive_predictive_value_pct
    FROM sade_roc_curve
    WHERE true_positive_rate >= 0.99
    ORDER BY false_positive_rate ASC
    LIMIT 1
) AS sensitivity_scenarios
ORDER BY CAST(SUBSTRING(sensitivity_target FROM 1 FOR 2) AS INTEGER);

-- Step 5: Calculate naive accuracy for comparison (shows why accuracy is misleading)
SELECT
    'Accuracy at Optimal Threshold' AS metric_type,
    ROUND(100.0 * (true_positives + true_negatives) / (true_positives + false_positives + true_negatives + false_negatives), 2) AS accuracy_pct
FROM sade_roc_curve
WHERE true_positive_rate >= 0.90
ORDER BY false_positive_rate ASC
LIMIT 1

UNION ALL

SELECT
    'Accuracy if Always Predict "No SADE"' AS metric_type,
    ROUND(100.0 * negative_count / (positive_count + negative_count), 2) AS accuracy_pct
FROM sade_model_auc;
```

**Sample Output:**
```
-- Model Quality:
AUC    | sade_count | non_sade_count | sade_prevalence_pct
-------+------------+----------------+---------------------
0.8923 | 450        | 149,550        | 0.300

-- Threshold for 90% Sensitivity (top 5 options):
threshold | sensitivity | fpr    | specificity | sade_detected | sade_missed | false_alarms | patients_flagged | positive_predictive_value_pct | pct_patients_flagged
----------+-------------+--------+-------------+---------------+-------------+--------------+------------------+-------------------------------+----------------------
0.023     | 0.9022      | 0.0523 | 0.9477      | 406           | 44          | 7,821        | 8,227            | 4.94                          | 5.48
0.021     | 0.9044      | 0.0589 | 0.9411      | 407           | 43          | 8,808        | 9,215            | 4.42                          | 6.14
0.019     | 0.9067      | 0.0678 | 0.9322      | 408           | 42          | 10,139       | 10,547           | 3.87                          | 7.03
0.017     | 0.9089      | 0.0789 | 0.9211      | 409           | 41          | 11,802       | 12,211           | 3.35                          | 8.14
0.015     | 0.9111      | 0.0912 | 0.9088      | 410           | 40          | 13,639       | 14,049           | 2.92                          | 9.37

-- Sensitivity target comparison:
sensitivity_target | threshold | sensitivity | specificity | fpr    | sade_detected | sade_missed | false_alarms | patients_flagged | positive_predictive_value_pct
-------------------+-----------+-------------+-------------+--------+---------------+-------------+--------------+------------------+-------------------------------
80% Sensitivity    | 0.045     | 0.8022      | 0.9689      | 0.0311 | 361           | 89          | 4,651        | 5,012            | 7.20
90% Sensitivity    | 0.023     | 0.9022      | 0.9477      | 0.0523 | 406           | 44          | 7,821        | 8,227            | 4.94  ← TARGET
95% Sensitivity    | 0.012     | 0.9511      | 0.9123      | 0.0877 | 428           | 22          | 13,119       | 13,547           | 3.16
99% Sensitivity    | 0.003     | 0.9911      | 0.8234      | 0.1766 | 446           | 4           | 26,411       | 26,857           | 1.66

-- Accuracy comparison (shows why accuracy is misleading):
metric_type                          | accuracy_pct
-------------------------------------+--------------
Accuracy at Optimal Threshold (90%)  | 94.77
Accuracy if Always Predict "No SADE" | 99.70  ← Higher but USELESS!
```

**Business Impact:**

**Why AUC/ROC is Critical for Imbalanced Classes:**
- **SADE Prevalence**: Only 0.3% (450 out of 150,000 patients)
- **Naive "Always Predict No SADE" Accuracy**: 99.70% (but catches ZERO SADEs!)
- **AUC = 0.8923**: Good discrimination despite extreme imbalance
- **Accuracy is misleading**: A model predicting "No SADE" for all patients achieves 99.7% accuracy but is clinically useless
- **AUC unaffected by imbalance**: Measures true discrimination ability

**Threshold Selection for 90% Sensitivity Target:**
- **Threshold = 0.023**: Flag patients with ≥2.3% SADE probability
- **Sensitivity = 90.22%**: Detect 90.22% of SADEs (406 of 450)
- **Specificity = 94.77%**: Correctly identify 94.77% of non-SADE patients
- **False Positive Rate = 5.23%**: 5.23% of non-SADE patients incorrectly flagged
- **Missed SADEs**: 44 patients (9.78% of actual SADEs) - clinical risk assessment needed

**Operational Impact:**
- **Patients Flagged**: 8,227 of 150,000 (5.48%) for enhanced monitoring
- **Positive Predictive Value (PPV)**: Only 4.94% of flagged patients actually experience SADEs
  - Means clinicians review ~20 patients per confirmed SADE
  - Low PPV is inherent to rare events (not a model flaw)
  - PPV = (Prevalence × Sensitivity) / [(Prevalence × Sensitivity) + ((1-Prevalence) × FPR)]
  - PPV = (0.003 × 0.90) / [(0.003 × 0.90) + (0.997 × 0.0523)] = 0.0494 = 4.94%

**Sensitivity Target Trade-offs:**

1. **80% Sensitivity** (threshold = 0.045):
   - Detects 361 of 450 SADEs (misses 89 - **19.8% miss rate**)
   - Only 5,012 patients flagged (3.34% of population)
   - PPV = 7.20% (better precision - ~14 reviews per SADE)
   - **Risk**: Missing 20% of SADEs may be unacceptable for serious events

2. **90% Sensitivity** (threshold = 0.023): ← RECOMMENDED
   - Detects 406 of 450 SADEs (misses 44 - **9.8% miss rate**)
   - 8,227 patients flagged (5.48% of population)
   - PPV = 4.94% (~20 reviews per SADE)
   - **Balance**: Acceptable miss rate + manageable workload

3. **95% Sensitivity** (threshold = 0.012):
   - Detects 428 of 450 SADEs (misses 22 - **4.9% miss rate**)
   - 13,547 patients flagged (9.03% of population)
   - PPV = 3.16% (~32 reviews per SADE)
   - **Trade-off**: Higher detection but 65% more patients flagged vs. 90% target

4. **99% Sensitivity** (threshold = 0.003):
   - Detects 446 of 450 SADEs (misses 4 - **0.9% miss rate**)
   - 26,857 patients flagged (17.9% of population)
   - PPV = 1.66% (~60 reviews per SADE)
   - **Risk**: 3.3x more patients flagged than 90% target - likely overwhelms clinical capacity

**Clinical Decision:**
- **Deploy with threshold = 0.023** (90% sensitivity target)
- **Enhanced Monitoring Protocol**: 8,227 high-risk patients receive:
  - More frequent vital sign monitoring
  - Daily lab work review
  - Automated alerting for early SADE indicators
  - Clinical pharmacist review

**Cost-Benefit Analysis:**
- **SADE Prevention Value**: Early detection enables intervention, reducing severity
  - Average SADE cost (hospitalization, treatment): $45,000
  - Early detection reduces cost by ~50%: $22,500 saved per SADE caught early
  - 406 SADEs detected × $22,500 = $9.14M savings

- **Enhanced Monitoring Cost**: $200 per patient flagged
  - 8,227 patients × $200 = $1.65M cost

- **Net Benefit**: $7.49M annually

- **Missed SADEs**: 44 SADEs not detected
  - Potential liability and patient harm
  - Clinical review: Could these be caught through standard care protocols?

**Why 90% Sensitivity (Not Higher)?**
- **Diminishing Returns**: 95% sensitivity requires 65% more patients flagged (13,547 vs. 8,227) to catch 22 additional SADEs
  - Marginal cost per additional SADE detected: (13,547 - 8,227) × $200 / 22 = $48,363 per SADE
  - Much higher than $22,500 benefit per SADE
- **Resource Constraints**: Clinical staff can manage 8,227 flagged patients; 26,857 (99% sensitivity) overwhelms capacity
- **Standard care**: Some missed SADEs will be caught through routine monitoring (model is additional layer, not sole detection)

**Model Performance Context:**
- **AUC = 0.8923 is GOOD** for rare event prediction (0.3% prevalence)
- **Comparison to baselines**:
  - Random model: AUC = 0.5, would require 50% FPR to achieve 90% sensitivity (75,000 patients flagged!)
  - Current model: 90% sensitivity at only 5.23% FPR - 10x better than random

**Regulatory/Safety Considerations:**
- Document clinical rationale for 90% sensitivity threshold
- Establish safety monitoring for 44 missed SADEs (root cause analysis)
- Quarterly AUC monitoring to detect rare event drift
- Backup alerting: Ensure standard care protocols catch missed cases

---

### Example 6: Feature Engineering Validation - Comparing Models Before and After Adding Features

**Business Context:**
A retail bank wants to improve their credit default prediction model by adding new behavioral features from transaction data. The data science team trained two models on the same customer base: (1) **Baseline model** using only credit bureau data (15 features), and (2) **Enhanced model** adding transaction behavioral features (30 total features). They need to determine if the new features genuinely improve discrimination ability (AUC improvement) and whether the improvement justifies the additional data pipeline complexity.

**SQL Code:**
```sql
-- Step 1: Generate ROC curves for both models
-- Baseline model (credit bureau features only)
SELECT
    'Baseline (Bureau Only)' AS model_name,
    roc.*
FROM TD_ROC (
    ON credit_default_predictions_baseline AS InputTable
    OUT TABLE baseline_auc_summary
    USING
    ObservationColumn('actual_default')
    ProbabilityColumn('default_probability')
    PositiveLabel('1')
    NumThresholds(200)
) AS roc
ORDER BY threshold;

-- Enhanced model (bureau + transaction features)
SELECT
    'Enhanced (Bureau + Transactions)' AS model_name,
    roc.*
FROM TD_ROC (
    ON credit_default_predictions_enhanced AS InputTable
    OUT TABLE enhanced_auc_summary
    USING
    ObservationColumn('actual_default')
    ProbabilityColumn('default_probability')
    PositiveLabel('1')
    NumThresholds(200)
) AS roc
ORDER BY threshold;

-- Step 2: Compare AUC between models
SELECT
    'Baseline (Bureau Only)' AS model_name,
    15 AS num_features,
    AUC,
    positive_count,
    negative_count
FROM baseline_auc_summary

UNION ALL

SELECT
    'Enhanced (Bureau + Transactions)' AS model_name,
    30 AS num_features,
    AUC,
    positive_count,
    negative_count
FROM enhanced_auc_summary
ORDER BY AUC DESC;

-- Step 3: Compare models at business-relevant operating point (10% FPR target)
SELECT
    model_name,
    threshold,
    true_positive_rate AS sensitivity,
    false_positive_rate AS fpr,
    true_positives AS defaults_detected,
    false_negatives AS defaults_missed,
    false_positives AS false_alarms,
    ROUND(100.0 * true_positives / (true_positives + false_positives), 2) AS precision_pct
FROM (
    SELECT
        'Baseline' AS model_name,
        threshold,
        true_positive_rate,
        false_positive_rate,
        true_positives,
        false_negatives,
        false_positives
    FROM baseline_roc_curve
    WHERE ABS(false_positive_rate - 0.10) < 0.01  -- Find closest to 10% FPR
    ORDER BY ABS(false_positive_rate - 0.10)
    LIMIT 1

    UNION ALL

    SELECT
        'Enhanced' AS model_name,
        threshold,
        true_positive_rate,
        false_positive_rate,
        true_positives,
        false_negatives,
        false_positives
    FROM enhanced_roc_curve
    WHERE ABS(false_positive_rate - 0.10) < 0.01
    ORDER BY ABS(false_positive_rate - 0.10)
    LIMIT 1
) AS comparison
ORDER BY model_name;

-- Step 4: Calculate business impact of AUC improvement
-- Assume: Default loss = $25,000, Credit denial cost = $500 (lost revenue)
CREATE VOLATILE TABLE feature_engineering_impact AS (
    SELECT
        model_name,
        sensitivity,
        fpr,
        defaults_detected,
        defaults_missed,
        false_alarms,
        -- Business costs
        (defaults_missed * 25000) AS default_losses,
        (false_alarms * 500) AS denial_costs,
        (defaults_missed * 25000) + (false_alarms * 500) AS total_cost,
        -- Improvement metrics
        defaults_detected - LAG(defaults_detected) OVER (ORDER BY model_name) AS additional_defaults_caught,
        false_alarms - LAG(false_alarms) OVER (ORDER BY model_name) AS additional_false_alarms,
        total_cost - LAG(total_cost) OVER (ORDER BY model_name) AS cost_savings
    FROM model_comparison_at_10pct_fpr
) WITH DATA ON COMMIT PRESERVE ROWS;

SELECT * FROM feature_engineering_impact;

-- Step 5: Test feature value by customer segment
SELECT
    customer_segment,
    'Baseline' AS model_name,
    auc.*
FROM TD_ROC (
    ON credit_default_predictions_baseline AS InputTable
    PARTITION BY customer_segment
    OUT TABLE baseline_segment_auc
    USING
    ObservationColumn('actual_default')
    ProbabilityColumn('default_probability')
    PositiveLabel('1')
    NumThresholds(100)
    Accumulate('customer_segment')
) AS roc
WHERE FALSE

UNION ALL

SELECT
    customer_segment,
    'Enhanced' AS model_name,
    auc.*
FROM TD_ROC (
    ON credit_default_predictions_enhanced AS InputTable
    PARTITION BY customer_segment
    OUT TABLE enhanced_segment_auc
    USING
    ObservationColumn('actual_default')
    ProbabilityColumn('default_probability')
    PositiveLabel('1')
    NumThresholds(100)
    Accumulate('customer_segment')
) AS roc
WHERE FALSE;

-- Combine segment AUCs for comparison
SELECT
    customer_segment,
    MAX(CASE WHEN model_name = 'Baseline' THEN AUC END) AS baseline_auc,
    MAX(CASE WHEN model_name = 'Enhanced' THEN AUC END) AS enhanced_auc,
    MAX(CASE WHEN model_name = 'Enhanced' THEN AUC END) - MAX(CASE WHEN model_name = 'Baseline' THEN AUC END) AS auc_improvement,
    ROUND(100.0 * (MAX(CASE WHEN model_name = 'Enhanced' THEN AUC END) - MAX(CASE WHEN model_name = 'Baseline' THEN AUC END)) /
        MAX(CASE WHEN model_name = 'Baseline' THEN AUC END), 2) AS pct_improvement
FROM (
    SELECT customer_segment, 'Baseline' AS model_name, AUC FROM baseline_segment_auc
    UNION ALL
    SELECT customer_segment, 'Enhanced' AS model_name, AUC FROM enhanced_segment_auc
) AS segment_auc
GROUP BY customer_segment
ORDER BY auc_improvement DESC;
```

**Sample Output:**
```
-- AUC Comparison:
model_name                      | num_features | AUC    | positive_count | negative_count
--------------------------------+--------------+--------+----------------+----------------
Enhanced (Bureau + Transactions)| 30           | 0.7823 | 3,456          | 46,544
Baseline (Bureau Only)          | 15           | 0.7234 | 3,456          | 46,544

-- Operating Point Comparison (10% FPR):
model_name | threshold | sensitivity | fpr    | defaults_detected | defaults_missed | false_alarms | precision_pct
-----------+-----------+-------------+--------+-------------------+-----------------+--------------+---------------
Baseline   | 0.245     | 0.4567      | 0.1012 | 1,578             | 1,878           | 4,710        | 25.09
Enhanced   | 0.198     | 0.5623      | 0.1005 | 1,943             | 1,513           | 4,678        | 29.34

-- Business Impact Analysis:
model_name | sensitivity | fpr    | defaults_detected | defaults_missed | false_alarms | default_losses | denial_costs | total_cost | additional_defaults_caught | additional_false_alarms | cost_savings
-----------+-------------+--------+-------------------+-----------------+--------------+----------------+--------------+------------+----------------------------+-------------------------+--------------
Baseline   | 0.4567      | 0.1012 | 1,578             | 1,878           | 4,710        | $46,950,000    | $2,355,000   | $49,305,000| NULL                       | NULL                    | NULL
Enhanced   | 0.5623      | 0.1005 | 1,943             | 1,513           | 4,678        | $37,825,000    | $2,339,000   | $40,164,000| +365                       | -32                     | $9,141,000

-- Segment-Level AUC Improvement:
customer_segment    | baseline_auc | enhanced_auc | auc_improvement | pct_improvement
--------------------+--------------+--------------+-----------------+-----------------
Young Professionals | 0.6823       | 0.8012       | +0.1189         | +17.42%         ← BEST IMPROVEMENT
Small Business      | 0.7234       | 0.8234       | +0.1000         | +13.82%
Mass Market         | 0.7123       | 0.7845       | +0.0722         | +10.14%
Premium             | 0.7656       | 0.8123       | +0.0467         | +6.10%
```

**Business Impact:**

**Feature Engineering Success - Clear Improvement:**
- **AUC Improvement**: +0.0589 (from 0.7234 to 0.7823) - **8.14% relative improvement**
- **Interpretation**: Enhanced model with transaction features provides materially better discrimination than baseline
- **Statistical Significance**: 0.0589 AUC improvement on 50K customer test set is highly significant

**Operating Point Analysis (10% FPR Target):**
Business constraint: Credit policy allows max 10% denial rate for good customers (FPR ≤ 10%)

**Baseline Model Performance:**
- Sensitivity = 45.67%: Catches 45.67% of defaults (1,578 of 3,456)
- Misses 1,878 defaults (54.33% miss rate)
- 4,710 false alarms (good customers denied credit)
- Precision = 25.09%: Only 1 in 4 denials is a true default

**Enhanced Model Performance:**
- Sensitivity = 56.23%: Catches 56.23% of defaults (1,943 of 3,456)
- Misses 1,513 defaults (43.77% miss rate)
- 4,678 false alarms (slightly fewer than baseline)
- Precision = 29.34%: Improved to nearly 1 in 3.4 denials being true defaults

**Key Improvement Metrics:**
- **+365 additional defaults detected** (1,943 vs. 1,578) - **23.1% more defaults caught**
- **-32 fewer false alarms** (4,678 vs. 4,710) - slightly better precision
- **Same FPR (~10%)**: Enhanced model achieves both higher sensitivity AND lower false alarms at same operating point

**Financial Impact:**
- **Default Loss Prevention**: 365 additional defaults caught × $25,000 average default loss = **$9.125M prevented losses**
- **Denial Cost Savings**: 32 fewer false alarms × $500 lost revenue = $16K additional revenue (minor)
- **Total Annual Benefit**: **$9.141M cost savings** from enhanced features
- **Baseline Total Cost**: $49.305M (default losses + denial costs)
- **Enhanced Total Cost**: $40.164M (18.5% reduction)

**ROI of Feature Engineering:**
- **Development Cost**: Transaction feature pipeline development = $150K (one-time)
- **Operational Cost**: Additional data pipeline maintenance = $50K annually
- **Annual Benefit**: $9.141M
- **Net ROI**: ($9.141M - $0.05M) / $0.15M = **60:1 return** in Year 1
- **Payback Period**: 6 days (150K / 9.141M × 365 days)
- **Decision**: **Strongly approve feature engineering investment**

**Segment-Level Insights:**

**Young Professionals - Biggest Winner:**
- AUC improvement: +0.1189 (+17.42%)
- **Hypothesis**: Transaction features (spending patterns, cash flow volatility, payment timing) are highly predictive for younger customers
- **Business Action**: Prioritize transaction data collection for this segment

**Small Business - Strong Improvement:**
- AUC improvement: +0.1000 (+13.82%)
- **Hypothesis**: Business transaction patterns (revenue volatility, payroll timing) predict default better than static bureau data
- **Business Action**: Consider additional business-specific transaction features (B2B payment patterns)

**Mass Market - Moderate Improvement:**
- AUC improvement: +0.0722 (+10.14%)
- **Observation**: Transaction features helpful but less dramatic than younger segments
- **Hypothesis**: Bureau data already captures most default risk for this stable segment

**Premium - Smaller Improvement:**
- AUC improvement: +0.0467 (+6.10%)
- **Observation**: Transaction features add least value for premium customers
- **Hypothesis**: Premium customers have strong credit history (bureau data already highly predictive); transaction features add marginal value
- **Business Action**: Transaction features still valuable (6% improvement) but focus on other segments for further enhancement

**Feature Engineering Decision:**
1. **APPROVED**: Deploy enhanced model with transaction features to production
2. **Expected benefit**: $9.1M annually in reduced default losses
3. **Deployment timeline**: 30 days
4. **Monitoring**: Track AUC monthly, segment-specific performance quarterly

**Next Steps - Further Feature Development:**
1. **Young Professionals**: Investigate additional digital behavior features (app usage, mobile payments) - potential +5-10% AUC improvement
2. **Small Business**: Add merchant category code (MCC) analysis, B2B payment patterns
3. **All Segments**: Test external data sources (utility payments, rental data) for incremental lift
4. **A/B Test**: Run 10% A/B test for 1 month before full deployment to validate $9M benefit estimate

**Technical Validation:**
- **Adjusted R²**: Check that enhanced model's Adjusted R² improvement matches AUC improvement (confirm features genuinely informative, not overfitting)
- **Feature Importance**: Run SHAP analysis to identify which transaction features drive improvement
- **Stability**: Validate AUC improvement consistent across multiple time periods (not just one lucky test set)

---

## Common Use Cases

### Model Evaluation and Selection
- **Algorithm comparison**: Compare Logistic Regression, Random Forest, XGBoost, Neural Networks using AUC
- **Feature engineering validation**: Assess if new features improve AUC
- **Model validation**: Evaluate final model discrimination ability before deployment
- **Benchmark comparison**: Compare custom models to industry baselines or vendor models
- **Cross-validation**: Compute AUC across multiple folds to assess stability

### Threshold Selection and Optimization
- **Business objective optimization**: Find threshold minimizing total business cost (asymmetric error costs)
- **Sensitivity target**: Identify threshold achieving minimum required detection rate (e.g., 90% fraud detection)
- **Specificity target**: Find threshold limiting false positive rate to acceptable level
- **Youden's Index**: Select threshold maximizing (Sensitivity + Specificity - 1)
- **F1 optimization**: Choose threshold maximizing F1 score (precision-recall balance)
- **Cost-sensitive threshold**: Balance false negative costs vs. false positive costs

### Production Model Monitoring
- **AUC tracking**: Monitor AUC over time to detect model degradation (concept drift)
- **Performance alerts**: Trigger retraining when AUC drops below threshold
- **A/B testing**: Compare champion vs. challenger models using AUC
- **Segment monitoring**: Track AUC by customer segment, product line, geography
- **Seasonal analysis**: Detect seasonal patterns in model discrimination ability

### Business Domain Applications
- **Fraud detection**: Evaluate fraud probability models (credit card, insurance, payment)
- **Credit risk**: Assess default probability models for lending decisions
- **Customer churn**: Validate churn probability predictions for retention targeting
- **Medical diagnosis**: Evaluate disease probability models for screening programs
- **Marketing response**: Assess campaign response probability for targeting optimization
- **Quality control**: Validate defect probability models in manufacturing
- **Cybersecurity**: Evaluate threat probability models for alert prioritization

### Imbalanced Classification
- **Rare event detection**: Evaluate models on highly imbalanced datasets (fraud, disease, equipment failure)
- **Class imbalance handling**: AUC unaffected by class imbalance (unlike accuracy)
- **Positive Predictive Value analysis**: Understand precision limitations for rare events
- **Sensitivity-specificity trade-offs**: Explicit analysis of detection vs. false alarm rates

### Research and Communication
- **Stakeholder reporting**: Present model quality using AUC (widely understood metric)
- **Regulatory compliance**: Document model discrimination ability for Basel II/III, CECL, IFRS 9
- **Publication**: Generate publication-quality ROC curves for research papers
- **Model comparison visualization**: Plot multiple ROC curves on same graph for visual comparison

## Best Practices

### Model Evaluation Strategy
1. **Always use held-out test data**: Never compute ROC/AUC on training data (overly optimistic results)
2. **Sufficient sample size**: Minimum 100+ instances per class, 1000+ preferred for stable AUC estimates
3. **Multiple evaluation metrics**: Use ROC/AUC alongside precision-recall curves, calibration plots
4. **Cross-validation**: Compute AUC across multiple folds to assess stability
5. **Stratified sampling**: Maintain class balance in train/test splits for fair evaluation

### AUC Interpretation
**AUC ranges and model quality:**
- **0.9 - 1.0**: Excellent discrimination (nearly perfect model)
- **0.8 - 0.9**: Good discrimination (strong predictive model)
- **0.7 - 0.8**: Fair discrimination (acceptable performance)
- **0.6 - 0.7**: Poor discrimination (weak model, marginally better than random)
- **0.5**: No discrimination (random guessing)
- **< 0.5**: Inverse predictions (flip predicted classes to get AUC > 0.5)

**Context-specific interpretation:**
- **Fraud detection**: AUC > 0.9 expected (high-quality features available)
- **Medical diagnosis**: AUC 0.8-0.9 typical (complex biological processes)
- **Marketing response**: AUC 0.6-0.7 common (high behavioral variability)
- **Credit risk**: AUC 0.7-0.85 standard (bureau data quality dependent)

### Threshold Selection
1. **Business-driven selection**: Base threshold on business objectives (cost minimization, ROI maximization)
2. **Multiple strategies**: Evaluate Youden's Index, F1 optimization, cost minimization, sensitivity/specificity targets
3. **Sensitivity analysis**: Test threshold robustness (cost impact of ±0.05 threshold variation)
4. **Operational constraints**: Consider capacity limits (can staff handle workload from threshold?)
5. **Document rationale**: Record why specific threshold chosen for audit trail

### ROC Curve Quality
1. **NumThresholds selection**:
   - **AUC only**: 50-100 thresholds sufficient
   - **Threshold selection**: 200-500 thresholds for precision
   - **Publication plots**: 500-1000 thresholds for smooth curves

2. **ROC curve shape analysis**:
   - **Concave curve above diagonal**: Good model (dominates random classifier)
   - **Curve near diagonal**: Poor model (close to random guessing)
   - **Early steep rise**: Model separates classes well at high probability scores
   - **Gradual rise**: Model struggles to separate classes

### Probability Calibration
1. **Check calibration**: ROC/AUC measures discrimination (ranking), not calibration (probability accuracy)
2. **Calibration assessment**: Use calibration plots, Brier score alongside ROC/AUC
3. **Calibration correction**: Apply Platt scaling or isotonic regression if needed
4. **Business impact**: Poor calibration affects threshold selection and business costs

### Handling Imbalanced Classes
1. **AUC advantage**: AUC unaffected by class imbalance (use instead of accuracy)
2. **Complement with PR curves**: Precision-Recall curves more informative for extreme imbalance
3. **Positive Predictive Value**: Calculate PPV to understand precision at chosen threshold
4. **Stratified evaluation**: Report AUC separately for different class prevalence scenarios

### Production Deployment
1. **Establish baseline AUC**: Record initial test set AUC before deployment
2. **Set alert thresholds**:
   - **Warning**: AUC drop >3-5%
   - **Critical**: AUC drop >10%
   - **Minimum**: AUC below domain-specific minimum (e.g., <0.75 for credit risk)

3. **Monitoring frequency**:
   - **High-risk applications**: Weekly or monthly
   - **Standard applications**: Quarterly
   - **Stable domains**: Semi-annually

4. **Retraining triggers**:
   - AUC drop below warning threshold
   - Significant data drift detected
   - Periodic schedule (quarterly/annually) regardless of AUC

5. **A/B testing**: Test new models on 10-20% traffic before full deployment

### Comparing Models
1. **Statistical significance**: AUC difference of 0.01-0.02 may not be meaningful for small test sets
2. **Bootstrap confidence intervals**: Compute 95% CI for AUC to assess significance
3. **DeLong's test**: Statistical test for AUC difference significance
4. **Business impact**: Translate AUC difference to business metrics (defaults prevented, costs saved)
5. **Complexity trade-off**: Consider if AUC improvement justifies model complexity increase

### Segment-Specific Evaluation
1. **PARTITION BY**: Use PARTITION BY to compute AUC by customer segment, product, geography
2. **Fairness analysis**: Check for AUC disparities across demographic groups
3. **Targeted models**: Consider separate models for segments with very different AUC
4. **Weighted AUC**: If segments have different business importance, compute weighted average AUC

### Common Pitfalls
1. **Training data evaluation**: NEVER compute AUC on training data (biased)
2. **Overfitting**: High training AUC + low test AUC = overfitting
3. **Temporal leakage**: For time series, ensure test data is after training data
4. **Target leakage**: Ensure no features correlated with target due to data leakage
5. **Class label confusion**: Verify PositiveLabel correctly identifies class of interest
6. **Threshold misuse**: Don't use arbitrary threshold (0.5) without business justification

### Reporting and Documentation
1. **Report AUC with context**:
   - "Model achieves AUC = 0.87 (good discrimination) on held-out test set"
   - Compare to baseline: "AUC = 0.87 vs. 0.72 baseline (+20.8% improvement)"

2. **Visualize ROC curve**: Always plot ROC curve, not just report AUC number
3. **Include confidence intervals**: Report 95% CI for AUC if possible
4. **Document threshold**: Explain chosen threshold and business rationale
5. **Business translation**: "AUC = 0.87 enables 80% fraud detection at 10% false alarm rate"

## Related Functions

### Classification Model Training
- **TD_GLM**: Train logistic regression for binary classification (outputs probabilities)
- **TD_DecisionForest**: Train random forest classifier (outputs probabilities)
- **TD_XGBoost**: Train gradient boosted classifier (outputs probabilities)
- **TD_NaiveBayes**: Train Naive Bayes classifier (outputs probabilities)
- **TD_SVM**: Train Support Vector Machine classifier (can output probability scores)

### Model Scoring/Prediction
- **TD_GLMPredict**: Score GLM models (use predict_proba for probabilities)
- **TD_DecisionForestPredict**: Score decision forest models (output probabilities)
- **TD_XGBoostPredict**: Score XGBoost models (output probabilities)
- **TD_NaiveBayesPredict**: Score Naive Bayes models (output probabilities)
- **TD_SVMPredict**: Score SVM models (output probability scores if enabled)

### Other Evaluation Functions
- **TD_ClassificationEvaluator**: Comprehensive classification metrics (precision, recall, F1, confusion matrix)
- **TD_RegressionEvaluator**: Evaluate regression models (MAE, RMSE, R²)
- **TD_SHAP**: Explain individual predictions and feature importance

### Data Preparation
- **TD_TrainTestSplit**: Split data into training and test sets for unbiased evaluation
- **TD_SMOTE**: Handle imbalanced classes through synthetic oversampling
- **TD_ClassBalance**: Handle imbalanced classes through undersampling/oversampling
- **TD_SimpleImputeFit / TD_SimpleImputeTransform**: Handle missing values before modeling

### Probability Calibration
- **TD_CalibratedProbabilities**: Apply Platt scaling or isotonic regression to improve probability calibration
- **TD_BinningFit / TD_BinningTransform**: Create probability bins for calibration analysis

### Statistical Analysis
- **TD_UnivariateStatistics**: Compute descriptive statistics for predictions and observations
- **TD_ChiSquareTest**: Test feature-target relationships for feature selection

## Notes and Limitations

### Function Constraints
- **Binary classification only**: TD_ROC works only with binary (two-class) classification problems
- **Probability input required**: ProbabilityColumn must contain values between 0 and 1 (not hard class predictions)
- **Non-NULL requirement**: Rows with NULL in observation or probability columns are excluded
- **Matching rows**: Observation and probability columns must have same cardinality
- **Minimum sample size**: At least 1 instance of each class required; 100+ per class recommended

### AUC Limitations
1. **Probability calibration**: AUC measures ranking ability (discrimination), NOT probability accuracy (calibration)
   - Model with high AUC may have poorly calibrated probabilities
   - Example: Model ranks predictions well (high AUC) but all probabilities near 0.5 (poor calibration)
   - Use calibration plots and Brier score to assess calibration separately

2. **Imbalanced classes**: While AUC is unaffected by class imbalance, Precision-Recall (PR) curves may be more informative for extreme imbalance (e.g., 1% positive class)

3. **Cost-insensitive**: AUC treats all errors equally; doesn't account for asymmetric costs (false negative vs. false positive)

4. **Class-weighted AUC**: Standard AUC is unweighted; some applications may require weighted AUC

### ROC Curve Interpretation
1. **Threshold independence**: AUC summarizes performance across all thresholds, but most applications use single threshold
2. **Operating point selection**: AUC doesn't specify which threshold to use; requires business judgment
3. **Curve shape matters**: Two models with similar AUC can have very different ROC curve shapes:
   - Model A: Better at high sensitivity (left side of curve)
   - Model B: Better at high specificity (right side of curve)
   - Choose based on business operating point

### Statistical Considerations
- **Sample size**: Small test sets yield unstable AUC estimates (confidence intervals widen)
- **Class overlap**: If classes naturally overlap, even perfect model will have AUC < 1.0
- **DeLong's test**: Use statistical tests to determine if AUC differences are significant
- **Cross-validation**: Single test set AUC may not represent true performance; use k-fold CV

### Performance Considerations
- **Large datasets**: Function performs single-pass computation, efficient for millions of rows
- **PARTITION BY**: Segment-wise AUC computation without multiple queries
- **NumThresholds impact**: Higher NumThresholds increases computation time linearly

### Common Misunderstandings
1. **"My model has AUC = 0.85 but only 60% accuracy"**: Accuracy is misleading for imbalanced classes; AUC is more reliable
2. **"AUC = 0.9 means 90% accurate"**: NO - AUC measures ranking ability, not classification accuracy
3. **"I should use threshold = 0.5"**: NO - threshold should be business-driven, rarely 0.5
4. **"Higher AUC always means better business outcome"**: Not necessarily - business costs matter

### Business Context Requirements
1. **Interpretation for stakeholders**:
   - **Technical**: "AUC = 0.87 means model correctly ranks a random positive case higher than a random negative case 87% of the time"
   - **Business**: "AUC = 0.87 indicates good model discrimination; we can detect 80% of frauds with only 10% false alarm rate"

2. **Threshold communication**:
   - Don't just report AUC; explain chosen threshold and business rationale
   - "We selected threshold = 0.32 to achieve 85% churn detection while keeping campaign size manageable (8,000 customers)"

3. **Benchmarking context**:
   - "Our AUC = 0.84 exceeds industry benchmark of 0.75 for credit card fraud"
   - "AUC improved from 0.76 (baseline) to 0.84 (+10.5%) with new features"

### Regulatory and Compliance
- **Model validation**: ROC/AUC is standard metric for regulatory model validation (Basel II/III, CECL, IFRS 9, SR 11-7)
- **Discrimination testing**: AUC used to test for discriminatory lending (fair lending compliance)
- **Audit trail**: Document AUC, threshold selection, and business rationale for auditors
- **Backtesting**: Periodic AUC computation on recent data for regulatory backtesting requirements

### Version and Compatibility
- **Teradata Version**: Available in Teradata Vantage 17.20+
- **Alias support**: TD_ROC_AUC, ROC are equivalent aliases
- **Output format**: Primary output is ROC curve coordinates; secondary output (OUT TABLE) contains AUC summary
- **NULL handling**: Automatically excludes rows with NULL in observation or probability columns

---

**Generated from Teradata Database Analytic Functions Version 17.20**
**Function Category**: Model Evaluation - Classification (ROC/AUC)
**Last Updated**: November 29, 2025
