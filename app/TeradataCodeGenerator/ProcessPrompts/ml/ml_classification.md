---
name: Classification Model Workflow
allowed-tools:
description: Complete workflow for building classification models in Teradata
argument-hint: [database_name] [table_name] [target_column]
---

# Classification Model Workflow

## Overview
This workflow guides you through building, training, evaluating, and deploying classification models in Teradata. Classification is used to predict categorical outcomes (binary or multiclass).

## Variables
DATABASE_NAME: $1
TABLE_NAME: $2
TARGET_COLUMN: $3

## Prerequisites
- **Data must be ML-ready**: Use @ml/ml_dataPreparation.md first
- Source table should have train/test split
- Target column should be categorical
- All features should be numeric (encoded)

## Classification Use Cases

### Binary Classification (2 classes)
- Customer churn prediction (churn/no churn)
- Fraud detection (fraud/legitimate)
- Credit risk (default/no default)
- Email classification (spam/not spam)
- Disease diagnosis (positive/negative)

### Multiclass Classification (3+ classes)
- Product category prediction
- Customer segment classification
- Priority level assignment (low/medium/high)
- Sentiment classification (positive/neutral/negative)
- Transaction type classification

## Workflow Stages

### Stage 0: Data Preparation Check

**Verify data is ML-ready:**
```sql
-- Check if data prep has been completed
SELECT COUNT(*) as total_rows,
       COUNT(DISTINCT dataset_split) as has_split,
       COUNT(${TARGET_COLUMN}) as target_non_null
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready;

-- Verify train/test split exists
SELECT dataset_split, COUNT(*) as row_count
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
GROUP BY dataset_split;
```

**If data is not prepared:**
- Route to: @ml/ml_dataPreparation.md
- Arguments: ${DATABASE_NAME} ${TABLE_NAME} ${TARGET_COLUMN}

### Stage 1: Problem Definition

**Define Classification Problem:**

1. **Binary or Multiclass?**
```sql
-- Check number of classes
SELECT ${TARGET_COLUMN}, COUNT(*) as class_count
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
GROUP BY ${TARGET_COLUMN}
ORDER BY class_count DESC;
```

2. **Check Class Balance:**
```sql
-- Assess class imbalance
SELECT
    ${TARGET_COLUMN},
    COUNT(*) as count,
    CAST(COUNT(*) AS FLOAT) / SUM(COUNT(*)) OVER () * 100 as percentage
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN'
GROUP BY ${TARGET_COLUMN}
ORDER BY count DESC;
```

**Imbalance Handling:**
- <10% minority class: Consider class weights or oversampling
- 10-40% minority class: Standard training should work
- >40% minority class: Well-balanced, proceed normally

3. **Define Success Metrics:**
- **Balanced classes**: Accuracy, F1-Score
- **Imbalanced classes**: Precision, Recall, AUC-ROC
- **Cost-sensitive**: Custom metric based on business impact

### Stage 2: Model Selection

**Decision Matrix: Which Classification Algorithm?**

| Model | Best For | Pros | Cons | Teradata Function |
|-------|----------|------|------|-------------------|
| **XGBoost** | Best overall performance | Highest accuracy, handles complex patterns | Slower training, less interpretable | TD_XGBoost |
| **DecisionForest** | Need interpretability | Good accuracy, feature importance, fast | May overfit on noisy data | TD_DecisionForest |
| **GLM (Logistic)** | Linear relationships | Fast, interpretable, probabilistic | Poor on non-linear data | TD_GLM |
| **SVM** | Complex boundaries | Excellent for high-dimensional data | Slow on large datasets | TD_SVM |
| **NaiveBayes** | Baseline/fast results | Very fast, works with small data | Assumes feature independence | TD_NaiveBayes |
| **KNN** | Similar examples important | Simple, no training time | Slow prediction, memory intensive | TD_KNN |

**Recommendation Engine:**

**Ask User:**
"Would you like to:
1. Use the **recommended model** (TD_XGBoost - best performance)
2. **Compare multiple models** (XGBoost, DecisionForest, GLM)
3. **Select a specific model** based on requirements"

**User Response Handling:**
- **Option 1**: Proceed with TD_XGBoost only
- **Option 2**: Train XGBoost, DecisionForest, and GLM; compare results
- **Option 3**: Use model selection matrix above

### Stage 3: Model Training

#### Option A: Recommended Model (TD_XGBoost)

```sql
-- Train XGBoost Classification Model
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_xgboost_model AS
SELECT TD_XGBoost(
    ModelType('classification'),
    TargetColumn('${TARGET_COLUMN}'),
    NumTrees(100),              -- Good default
    MaxDepth(6),                -- Prevents overfitting
    LearningRate(0.1),          -- Standard rate
    MinChildWeight(1),
    Subsample(0.8),             -- Use 80% of data per tree
    ColSampleByTree(0.8)        -- Use 80% of features per tree
)
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN'
WITH DATA;
```

**Hyperparameter Guidance:**
- **NumTrees**: 50-200 (more = better, but slower)
- **MaxDepth**: 3-10 (lower = less overfitting)
- **LearningRate**: 0.01-0.3 (lower = slower but more accurate)
- **Subsample**: 0.6-0.9 (prevents overfitting)

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_xgboost.md

#### Option B: Multiple Model Comparison

**Model 1: XGBoost**
```sql
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_xgboost_model AS
SELECT TD_XGBoost(
    ModelType('classification'),
    TargetColumn('${TARGET_COLUMN}'),
    NumTrees(100),
    MaxDepth(6),
    LearningRate(0.1)
)
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN'
WITH DATA;
```

**Model 2: DecisionForest (Random Forest)**
```sql
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_rf_model AS
SELECT TD_DecisionForest(
    ModelType('classification'),
    TargetColumn('${TARGET_COLUMN}'),
    NumTrees(100),
    MaxDepth(10),
    MinNodeSize(10),
    SampleSize(0.8)
)
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN'
WITH DATA;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_decisionforest.md

**Model 3: Logistic Regression (GLM)**
```sql
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_glm_model AS
SELECT TD_GLM(
    Family('binomial'),          -- For binary classification
    LinkFunction('logit'),
    TargetColumn('${TARGET_COLUMN}'),
    MaxIterations(100),
    Tolerance(0.0001)
)
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN'
WITH DATA;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_glm.md

#### Option C: Specialized Models

**Support Vector Machine (Complex Boundaries)**
```sql
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_svm_model AS
SELECT TD_SVM(
    ModelType('classification'),
    TargetColumn('${TARGET_COLUMN}'),
    KernelType('rbf'),           -- radial basis function
    Cost(1.0),
    Gamma(0.1)
)
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN'
WITH DATA;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_svm.md

**Naive Bayes (Fast Baseline)**
```sql
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_nb_model AS
SELECT TD_NaiveBayes(
    TargetColumn('${TARGET_COLUMN}'),
    ModelType('multinomial')     -- or 'gaussian' for continuous features
)
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN'
WITH DATA;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_naivebayes.md

**K-Nearest Neighbors (Instance-Based)**
```sql
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_knn_model AS
SELECT TD_KNN(
    TargetColumn('${TARGET_COLUMN}'),
    K(5),                        -- Number of neighbors
    DistanceMetric('euclidean')
)
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN'
WITH DATA;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_knn.md

### Stage 4: Model Scoring (Predictions)

#### XGBoost Predictions
```sql
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_xgboost_predictions AS
SELECT
    t.*,
    p.prediction as predicted_class,
    p.probability as prediction_probability
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready t,
     TD_XGBoostPredict(
         ModelTable(${DATABASE_NAME}.${TABLE_NAME}_xgboost_model),
         OutputProb(1)           -- Output probability scores
     ) p
WHERE t.dataset_split = 'TEST'
WITH DATA;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_xgboostpredict.md

#### DecisionForest Predictions
```sql
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_rf_predictions AS
SELECT
    t.*,
    p.prediction as predicted_class,
    p.probability as prediction_probability
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready t,
     TD_DecisionForestPredict(
         ModelTable(${DATABASE_NAME}.${TABLE_NAME}_rf_model),
         OutputProb(1)
     ) p
WHERE t.dataset_split = 'TEST'
WITH DATA;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_decisionforestpredict.md

#### GLM Predictions
```sql
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_glm_predictions AS
SELECT
    t.*,
    p.prediction as predicted_class,
    p.fitted_value as prediction_probability
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready t,
     TD_GLMPredict(
         ModelTable(${DATABASE_NAME}.${TABLE_NAME}_glm_model)
     ) p
WHERE t.dataset_split = 'TEST'
WITH DATA;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_glmpredict.md

### Stage 5: Model Evaluation

#### Comprehensive Classification Metrics

```sql
-- Evaluate XGBoost Model
SELECT
    'XGBoost' as model_name,
    metrics.*
FROM TD_ClassificationEvaluator(
    ObservationColumn('${TARGET_COLUMN}'),
    PredictionColumn('predicted_class'),
    Metrics('Accuracy', 'Precision', 'Recall', 'F1', 'AUC')
) metrics,
${DATABASE_NAME}.${TABLE_NAME}_xgboost_predictions;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_classificationevaluator.md

#### Metrics Interpretation Guide

| Metric | Formula | When to Use | Good Score |
|--------|---------|-------------|------------|
| **Accuracy** | (TP+TN)/(TP+TN+FP+FN) | Balanced classes | >85% |
| **Precision** | TP/(TP+FP) | Minimize false positives | >80% |
| **Recall** | TP/(TP+FN) | Minimize false negatives | >80% |
| **F1-Score** | 2*(P*R)/(P+R) | Balance precision & recall | >80% |
| **AUC-ROC** | Area under ROC curve | Overall performance | >0.85 |

**Business Context:**
- **Fraud Detection**: Prioritize Recall (catch all fraud)
- **Spam Filter**: Prioritize Precision (avoid false positives)
- **Medical Diagnosis**: High Recall (catch all diseases)
- **Marketing Campaign**: Balance F1-Score

#### ROC Curve Analysis

```sql
-- Generate ROC Curve
SELECT TD_ROC(
    ObservationColumn('${TARGET_COLUMN}'),
    ProbabilityColumn('prediction_probability'),
    PositiveClass(1),
    NumThresholds(100)
)
FROM ${DATABASE_NAME}.${TABLE_NAME}_xgboost_predictions;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_roc.md

#### Confusion Matrix

```sql
-- Detailed Confusion Matrix
SELECT
    ${TARGET_COLUMN} as actual_class,
    predicted_class,
    COUNT(*) as count
FROM ${DATABASE_NAME}.${TABLE_NAME}_xgboost_predictions
GROUP BY ${TARGET_COLUMN}, predicted_class
ORDER BY ${TARGET_COLUMN}, predicted_class;
```

#### Compare Multiple Models

```sql
-- Model Comparison
SELECT
    'XGBoost' as model,
    AVG(CASE WHEN ${TARGET_COLUMN} = predicted_class THEN 1.0 ELSE 0.0 END) as accuracy
FROM ${DATABASE_NAME}.${TABLE_NAME}_xgboost_predictions

UNION ALL

SELECT
    'RandomForest' as model,
    AVG(CASE WHEN ${TARGET_COLUMN} = predicted_class THEN 1.0 ELSE 0.0 END) as accuracy
FROM ${DATABASE_NAME}.${TABLE_NAME}_rf_predictions

UNION ALL

SELECT
    'GLM' as model,
    AVG(CASE WHEN ${TARGET_COLUMN} = predicted_class THEN 1.0 ELSE 0.0 END) as accuracy
FROM ${DATABASE_NAME}.${TABLE_NAME}_glm_predictions

ORDER BY accuracy DESC;
```

### Stage 6: Model Interpretation

#### Feature Importance (SHAP Values)

```sql
-- Calculate SHAP values for feature importance
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_shap_values AS
SELECT TD_SHAP(
    ModelTable(${DATABASE_NAME}.${TABLE_NAME}_xgboost_model),
    InputTable(${DATABASE_NAME}.${TABLE_NAME}_ml_ready),
    MaxSamples(1000)            -- Sample for faster computation
)
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TEST'
WITH DATA;

-- Summarize feature importance
SELECT
    feature_name,
    AVG(ABS(shap_value)) as importance
FROM ${DATABASE_NAME}.${TABLE_NAME}_shap_values
GROUP BY feature_name
ORDER BY importance DESC
LIMIT 20;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_shap.md

#### Model Explainability

```sql
-- Top features driving predictions for a specific instance
SELECT
    feature_name,
    shap_value,
    CASE WHEN shap_value > 0 THEN 'Increases probability'
         ELSE 'Decreases probability' END as impact
FROM ${DATABASE_NAME}.${TABLE_NAME}_shap_values
WHERE row_id = 'specific_customer_id'
ORDER BY ABS(shap_value) DESC
LIMIT 10;
```

### Stage 7: Production Deployment

#### Create Scoring View

```sql
-- Production scoring view (no test split filter)
CREATE VIEW ${DATABASE_NAME}.${TABLE_NAME}_scored AS
SELECT
    t.*,
    p.prediction as predicted_${TARGET_COLUMN},
    p.probability as prediction_confidence,
    CURRENT_TIMESTAMP as score_timestamp
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready t,
     TD_XGBoostPredict(
         ModelTable(${DATABASE_NAME}.${TABLE_NAME}_xgboost_model),
         OutputProb(1)
     ) p;
```

#### Batch Scoring Script

```sql
-- Score new data using trained model
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_new_predictions AS
SELECT
    new_data.*,
    p.prediction as predicted_class,
    p.probability as confidence_score,
    CURRENT_DATE as prediction_date
FROM ${DATABASE_NAME}.${TABLE_NAME}_new_data new_data,
     TD_XGBoostPredict(
         ModelTable(${DATABASE_NAME}.${TABLE_NAME}_xgboost_model),
         OutputProb(1)
     ) p
WITH DATA;
```

#### Monitor Model Performance

```sql
-- Track prediction distribution over time
SELECT
    prediction_date,
    predicted_class,
    COUNT(*) as prediction_count,
    AVG(confidence_score) as avg_confidence
FROM ${DATABASE_NAME}.${TABLE_NAME}_new_predictions
GROUP BY prediction_date, predicted_class
ORDER BY prediction_date, predicted_class;
```

## Decision Guides

### When to Retrain Model

Retrain if:
- **Accuracy drops >5%** on new data
- **Prediction distribution changes** significantly
- **New features** are available
- **Business rules change**
- **Time-based**: Every 3-6 months for most use cases

### Model Selection Summary

**Use XGBoost when:**
- Need best possible accuracy
- Have sufficient training data (>1000 rows)
- Can tolerate longer training time

**Use DecisionForest when:**
- Need interpretability
- Want feature importance
- Have categorical features

**Use GLM when:**
- Need fast training
- Linear relationships exist
- Want simple interpretation
- Require probability calibration

**Use SVM when:**
- Have high-dimensional data
- Non-linear boundaries
- Small to medium datasets

**Use NaiveBayes when:**
- Need very fast training
- Have limited data
- Features are independent
- Need a quick baseline

**Use KNN when:**
- Similar examples are important
- Have well-distributed data
- Can tolerate slow predictions

## Output Artifacts

This workflow produces:
1. `${TABLE_NAME}_xgboost_model` - Trained XGBoost model
2. `${TABLE_NAME}_xgboost_predictions` - Test set predictions
3. `${TABLE_NAME}_shap_values` - Feature importance scores
4. `${TABLE_NAME}_scored` - Production scoring view
5. Model evaluation metrics (accuracy, precision, recall, F1, AUC)
6. ROC curve data
7. Confusion matrix

## Best Practices

1. **Always use train/test split** - Never evaluate on training data
2. **Check class balance** - Handle imbalanced classes appropriately
3. **Validate assumptions** - Ensure features are properly scaled/encoded
4. **Monitor in production** - Track prediction distributions and accuracy
5. **Version models** - Keep track of model versions and performance
6. **Document decisions** - Record why specific models/parameters were chosen
7. **Test edge cases** - Validate model on edge cases before production

## Common Issues and Solutions

### Issue: Poor Model Performance
**Solutions:**
- Check if data prep was done correctly
- Try different models
- Adjust hyperparameters
- Add more relevant features
- Check for data leakage

### Issue: Overfitting (high train, low test accuracy)
**Solutions:**
- Reduce model complexity (MaxDepth, NumTrees)
- Increase regularization
- Use more training data
- Remove correlated features

### Issue: Class Imbalance
**Solutions:**
- Use class weights in model training
- Oversample minority class
- Undersample majority class
- Focus on precision/recall instead of accuracy

## Function Reference Summary

### Model Training
- FunctionalPrompts/Advanced_Analytics/td_xgboost.md
- FunctionalPrompts/Advanced_Analytics/td_decisionforest.md
- FunctionalPrompts/Advanced_Analytics/td_glm.md
- FunctionalPrompts/Advanced_Analytics/td_svm.md
- FunctionalPrompts/Advanced_Analytics/td_naivebayes.md
- FunctionalPrompts/Advanced_Analytics/td_knn.md

### Model Scoring
- FunctionalPrompts/Advanced_Analytics/td_xgboostpredict.md
- FunctionalPrompts/Advanced_Analytics/td_decisionforestpredict.md
- FunctionalPrompts/Advanced_Analytics/td_glmpredict.md
- FunctionalPrompts/Advanced_Analytics/td_svmpredict.md
- FunctionalPrompts/Advanced_Analytics/td_naivebayespredict.md

### Model Evaluation
- FunctionalPrompts/Advanced_Analytics/td_classificationevaluator.md
- FunctionalPrompts/Advanced_Analytics/td_roc.md
- FunctionalPrompts/Advanced_Analytics/td_shap.md

### Data Preparation
- ProcessPrompts/ml/ml_dataPreparation.md

---

**File Created**: 2025-11-28
**Version**: 1.0
**Workflow Type**: Classification
**Parent Persona**: persona_data_scientist.md
