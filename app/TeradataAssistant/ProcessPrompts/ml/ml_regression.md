---
name: Regression Model Workflow
allowed-tools:
description: Complete workflow for building regression models in Teradata
argument-hint: [database_name] [table_name] [target_column]
---

# Regression Model Workflow

## Overview
This workflow guides you through building, training, evaluating, and deploying regression models in Teradata. Regression is used to predict continuous numeric outcomes.

## Variables
DATABASE_NAME: $1
TABLE_NAME: $2
TARGET_COLUMN: $3

## Prerequisites
- **Data must be ML-ready**: Use @ml/ml_dataPreparation.md first
- Source table should have train/test split
- Target column should be numeric (continuous)
- All features should be numeric (scaled)

## Regression Use Cases

### Sales and Revenue Prediction
- Sales forecasting by region/product
- Revenue projection
- Demand estimation
- Inventory level optimization

### Pricing and Valuation
- House price prediction
- Product pricing optimization
- Stock price forecasting
- Asset valuation

### Time Series and Trends
- Energy consumption forecasting
- Traffic volume prediction
- Resource utilization prediction
- Weather forecasting

### Risk and Finance
- Insurance claim amount prediction
- Loan amount estimation
- Credit limit determination
- Investment return prediction

### Operational Metrics
- Delivery time estimation
- Processing time prediction
- Resource consumption forecasting
- Performance metric prediction

## Workflow Stages

### Stage 0: Data Preparation Check

**Verify data is ML-ready:**
```sql
-- Check if data prep has been completed
SELECT COUNT(*) as total_rows,
       COUNT(DISTINCT dataset_split) as has_split,
       COUNT(${TARGET_COLUMN}) as target_non_null,
       AVG(${TARGET_COLUMN}) as target_mean,
       STDDEV_POP(${TARGET_COLUMN}) as target_stddev
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready;

-- Verify train/test split exists
SELECT dataset_split,
       COUNT(*) as row_count,
       AVG(${TARGET_COLUMN}) as avg_target,
       MIN(${TARGET_COLUMN}) as min_target,
       MAX(${TARGET_COLUMN}) as max_target
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
GROUP BY dataset_split;
```

**If data is not prepared:**
- Route to: @ml/ml_dataPreparation.md
- Arguments: ${DATABASE_NAME} ${TABLE_NAME} ${TARGET_COLUMN}

### Stage 1: Problem Definition

**Define Regression Problem:**

1. **Understand Target Distribution:**
```sql
-- Analyze target variable distribution
SELECT
    MIN(${TARGET_COLUMN}) as min_value,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY ${TARGET_COLUMN}) as q1,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY ${TARGET_COLUMN}) as median,
    AVG(${TARGET_COLUMN}) as mean,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY ${TARGET_COLUMN}) as q3,
    MAX(${TARGET_COLUMN}) as max_value,
    STDDEV_POP(${TARGET_COLUMN}) as std_dev,
    COUNT(*) as total_count
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN';
```

2. **Check for Outliers:**
```sql
-- Identify potential outliers using IQR method
WITH stats AS (
    SELECT
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY ${TARGET_COLUMN}) as q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY ${TARGET_COLUMN}) as q3
    FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
    WHERE dataset_split = 'TRAIN'
)
SELECT
    COUNT(*) as outlier_count,
    COUNT(*) * 100.0 / (SELECT COUNT(*) FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready WHERE dataset_split = 'TRAIN') as outlier_percentage
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready, stats
WHERE dataset_split = 'TRAIN'
  AND (${TARGET_COLUMN} < q1 - 1.5 * (q3 - q1)
   OR ${TARGET_COLUMN} > q3 + 1.5 * (q3 - q1));
```

**Outlier Handling:**
- <1% outliers: Proceed normally
- 1-5% outliers: Consider robust models or outlier treatment
- >5% outliers: Investigate data quality or use robust regression

3. **Define Success Metrics:**
- **RMSE (Root Mean Squared Error)**: Penalizes large errors
- **MAE (Mean Absolute Error)**: Robust to outliers
- **R² (R-Squared)**: Proportion of variance explained
- **MAPE (Mean Absolute Percentage Error)**: Relative error measure

### Stage 2: Model Selection

**Decision Matrix: Which Regression Algorithm?**

| Model | Best For | Pros | Cons | Teradata Function |
|-------|----------|------|------|-------------------|
| **XGBoost** | Best overall performance | Highest accuracy, handles non-linearity | Slower training, less interpretable | TD_XGBoost |
| **DecisionForest** | Non-linear relationships | Good accuracy, feature importance | May overfit, less smooth predictions | TD_DecisionForest |
| **GLM (Linear)** | Linear relationships | Fast, interpretable, coefficients | Poor on non-linear data | TD_GLM |
| **GLM (Polynomial)** | Polynomial patterns | Captures curves, still interpretable | Can overfit, requires degree selection | TD_GLM |

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
-- Train XGBoost Regression Model
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_xgboost_model AS
SELECT TD_XGBoost(
    ModelType('regression'),
    TargetColumn('${TARGET_COLUMN}'),
    NumTrees(100),              -- Good default
    MaxDepth(6),                -- Prevents overfitting
    LearningRate(0.1),          -- Standard rate
    MinChildWeight(1),
    Subsample(0.8),             -- Use 80% of data per tree
    ColSampleByTree(0.8),       -- Use 80% of features per tree
    Objective('reg:squarederror') -- Standard for regression
)
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN'
WITH DATA;
```

**Hyperparameter Guidance:**
- **NumTrees**: 50-200 (more trees = better but slower)
- **MaxDepth**: 3-10 (lower depth = less overfitting)
- **LearningRate**: 0.01-0.3 (lower = slower convergence but more accurate)
- **MinChildWeight**: 1-10 (higher = more conservative)
- **Subsample**: 0.6-0.9 (prevents overfitting)
- **Objective**: 'reg:squarederror', 'reg:squaredlogerror', 'reg:pseudohubererror'

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_xgboost.md

#### Option B: Multiple Model Comparison

**Model 1: XGBoost**
```sql
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_xgboost_model AS
SELECT TD_XGBoost(
    ModelType('regression'),
    TargetColumn('${TARGET_COLUMN}'),
    NumTrees(100),
    MaxDepth(6),
    LearningRate(0.1),
    Objective('reg:squarederror')
)
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN'
WITH DATA;
```

**Model 2: DecisionForest (Random Forest)**
```sql
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_rf_model AS
SELECT TD_DecisionForest(
    ModelType('regression'),
    TargetColumn('${TARGET_COLUMN}'),
    NumTrees(100),
    MaxDepth(15),
    MinNodeSize(5),
    SampleSize(0.8)
)
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN'
WITH DATA;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_decisionforest.md

**Model 3: Linear Regression (GLM)**
```sql
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_glm_model AS
SELECT TD_GLM(
    Family('gaussian'),          -- For continuous outcomes
    LinkFunction('identity'),    -- Linear relationship
    TargetColumn('${TARGET_COLUMN}'),
    MaxIterations(100),
    Tolerance(0.0001)
)
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN'
WITH DATA;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_glm.md

#### Option C: Advanced GLM Configurations

**Ridge Regression (L2 Regularization)**
```sql
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_ridge_model AS
SELECT TD_GLM(
    Family('gaussian'),
    LinkFunction('identity'),
    TargetColumn('${TARGET_COLUMN}'),
    Alpha(0),                    -- 0 = Ridge (L2 only)
    Lambda(0.1),                 -- Regularization strength
    MaxIterations(100)
)
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN'
WITH DATA;
```

**Lasso Regression (L1 Regularization)**
```sql
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_lasso_model AS
SELECT TD_GLM(
    Family('gaussian'),
    LinkFunction('identity'),
    TargetColumn('${TARGET_COLUMN}'),
    Alpha(1),                    -- 1 = Lasso (L1 only)
    Lambda(0.1),                 -- Regularization strength
    MaxIterations(100)
)
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN'
WITH DATA;
```

**Elastic Net (L1 + L2)**
```sql
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_elasticnet_model AS
SELECT TD_GLM(
    Family('gaussian'),
    LinkFunction('identity'),
    TargetColumn('${TARGET_COLUMN}'),
    Alpha(0.5),                  -- 0.5 = Mix of L1 and L2
    Lambda(0.1),
    MaxIterations(100)
)
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
WHERE dataset_split = 'TRAIN'
WITH DATA;
```

### Stage 4: Model Scoring (Predictions)

#### XGBoost Predictions
```sql
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_xgboost_predictions AS
SELECT
    t.*,
    p.prediction as predicted_${TARGET_COLUMN},
    t.${TARGET_COLUMN} as actual_${TARGET_COLUMN},
    t.${TARGET_COLUMN} - p.prediction as residual,
    ABS(t.${TARGET_COLUMN} - p.prediction) as absolute_error,
    POWER(t.${TARGET_COLUMN} - p.prediction, 2) as squared_error
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready t,
     TD_XGBoostPredict(
         ModelTable(${DATABASE_NAME}.${TABLE_NAME}_xgboost_model)
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
    p.prediction as predicted_${TARGET_COLUMN},
    t.${TARGET_COLUMN} as actual_${TARGET_COLUMN},
    t.${TARGET_COLUMN} - p.prediction as residual,
    ABS(t.${TARGET_COLUMN} - p.prediction) as absolute_error,
    POWER(t.${TARGET_COLUMN} - p.prediction, 2) as squared_error
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready t,
     TD_DecisionForestPredict(
         ModelTable(${DATABASE_NAME}.${TABLE_NAME}_rf_model)
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
    p.prediction as predicted_${TARGET_COLUMN},
    t.${TARGET_COLUMN} as actual_${TARGET_COLUMN},
    t.${TARGET_COLUMN} - p.prediction as residual,
    ABS(t.${TARGET_COLUMN} - p.prediction) as absolute_error,
    POWER(t.${TARGET_COLUMN} - p.prediction, 2) as squared_error
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready t,
     TD_GLMPredict(
         ModelTable(${DATABASE_NAME}.${TABLE_NAME}_glm_model)
     ) p
WHERE t.dataset_split = 'TEST'
WITH DATA;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_glmpredict.md

### Stage 5: Model Evaluation

#### Comprehensive Regression Metrics

```sql
-- Evaluate XGBoost Model using TD_RegressionEvaluator
SELECT
    'XGBoost' as model_name,
    metrics.*
FROM TD_RegressionEvaluator(
    ObservationColumn('actual_${TARGET_COLUMN}'),
    PredictionColumn('predicted_${TARGET_COLUMN}'),
    Metrics('RMSE', 'MAE', 'R2', 'MAPE')
) metrics,
${DATABASE_NAME}.${TABLE_NAME}_xgboost_predictions;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_regressionevaluator.md

#### Manual Metric Calculations

```sql
-- Calculate all regression metrics manually
SELECT
    'XGBoost' as model_name,
    -- Root Mean Squared Error
    SQRT(AVG(squared_error)) as RMSE,
    -- Mean Absolute Error
    AVG(absolute_error) as MAE,
    -- R-Squared
    1 - (SUM(squared_error) /
         SUM(POWER(actual_${TARGET_COLUMN} - (SELECT AVG(${TARGET_COLUMN})
                                               FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready
                                               WHERE dataset_split = 'TEST'), 2))) as R2,
    -- Mean Absolute Percentage Error
    AVG(ABS(residual) / NULLIFZERO(ABS(actual_${TARGET_COLUMN}))) * 100 as MAPE,
    -- Additional metrics
    COUNT(*) as prediction_count,
    AVG(actual_${TARGET_COLUMN}) as actual_mean,
    AVG(predicted_${TARGET_COLUMN}) as predicted_mean
FROM ${DATABASE_NAME}.${TABLE_NAME}_xgboost_predictions;
```

#### Metrics Interpretation Guide

| Metric | Formula | Interpretation | Good Score |
|--------|---------|----------------|------------|
| **RMSE** | sqrt(mean(errors²)) | Average prediction error (same units as target) | Lower is better |
| **MAE** | mean(abs(errors)) | Average absolute error (robust to outliers) | Lower is better |
| **R²** | 1 - (SS_res/SS_tot) | % of variance explained (0-1 scale) | >0.80 |
| **MAPE** | mean(abs(errors/actual)) × 100 | Average % error | <10% |

**Business Context:**
- **RMSE**: Penalizes large errors heavily (use when large errors are costly)
- **MAE**: Treats all errors equally (use when all errors have similar cost)
- **R²**: Overall model fit (use for model comparison)
- **MAPE**: Relative accuracy (use when scale matters)

#### Residual Analysis

```sql
-- Analyze residuals for model diagnostics
SELECT
    CASE
        WHEN residual BETWEEN -10 AND 0 THEN '[-10, 0)'
        WHEN residual BETWEEN 0 AND 10 THEN '[0, 10)'
        WHEN residual BETWEEN 10 AND 20 THEN '[10, 20)'
        WHEN residual BETWEEN 20 AND 50 THEN '[20, 50)'
        WHEN residual < -10 THEN '< -10'
        ELSE '> 50'
    END as residual_range,
    COUNT(*) as count,
    AVG(residual) as avg_residual,
    STDDEV_POP(residual) as stddev_residual
FROM ${DATABASE_NAME}.${TABLE_NAME}_xgboost_predictions
GROUP BY 1
ORDER BY 1;
```

#### Prediction vs Actual Analysis

```sql
-- Analyze predictions across target value ranges
WITH ranges AS (
    SELECT
        CASE
            WHEN actual_${TARGET_COLUMN} < (SELECT PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY ${TARGET_COLUMN}) FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready WHERE dataset_split = 'TEST') THEN 'Low'
            WHEN actual_${TARGET_COLUMN} < (SELECT PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY ${TARGET_COLUMN}) FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready WHERE dataset_split = 'TEST') THEN 'Medium'
            ELSE 'High'
        END as value_range,
        actual_${TARGET_COLUMN},
        predicted_${TARGET_COLUMN},
        absolute_error
    FROM ${DATABASE_NAME}.${TABLE_NAME}_xgboost_predictions
)
SELECT
    value_range,
    COUNT(*) as count,
    AVG(actual_${TARGET_COLUMN}) as avg_actual,
    AVG(predicted_${TARGET_COLUMN}) as avg_predicted,
    AVG(absolute_error) as avg_error,
    SQRT(AVG(POWER(actual_${TARGET_COLUMN} - predicted_${TARGET_COLUMN}, 2))) as rmse
FROM ranges
GROUP BY value_range
ORDER BY value_range;
```

#### Compare Multiple Models

```sql
-- Model Comparison Dashboard
WITH xgb AS (
    SELECT 'XGBoost' as model,
           SQRT(AVG(squared_error)) as rmse,
           AVG(absolute_error) as mae,
           1 - (SUM(squared_error) / SUM(POWER(actual_${TARGET_COLUMN} - (SELECT AVG(actual_${TARGET_COLUMN}) FROM ${DATABASE_NAME}.${TABLE_NAME}_xgboost_predictions), 2))) as r2
    FROM ${DATABASE_NAME}.${TABLE_NAME}_xgboost_predictions
),
rf AS (
    SELECT 'RandomForest' as model,
           SQRT(AVG(squared_error)) as rmse,
           AVG(absolute_error) as mae,
           1 - (SUM(squared_error) / SUM(POWER(actual_${TARGET_COLUMN} - (SELECT AVG(actual_${TARGET_COLUMN}) FROM ${DATABASE_NAME}.${TABLE_NAME}_rf_predictions), 2))) as r2
    FROM ${DATABASE_NAME}.${TABLE_NAME}_rf_predictions
),
glm AS (
    SELECT 'GLM' as model,
           SQRT(AVG(squared_error)) as rmse,
           AVG(absolute_error) as mae,
           1 - (SUM(squared_error) / SUM(POWER(actual_${TARGET_COLUMN} - (SELECT AVG(actual_${TARGET_COLUMN}) FROM ${DATABASE_NAME}.${TABLE_NAME}_glm_predictions), 2))) as r2
    FROM ${DATABASE_NAME}.${TABLE_NAME}_glm_predictions
)
SELECT * FROM xgb
UNION ALL
SELECT * FROM rf
UNION ALL
SELECT * FROM glm
ORDER BY r2 DESC, rmse ASC;
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
    AVG(ABS(shap_value)) as importance_score,
    AVG(shap_value) as avg_impact,
    MIN(shap_value) as min_impact,
    MAX(shap_value) as max_impact
FROM ${DATABASE_NAME}.${TABLE_NAME}_shap_values
GROUP BY feature_name
ORDER BY importance_score DESC
LIMIT 20;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_shap.md

#### GLM Coefficient Analysis

```sql
-- Extract GLM coefficients for linear model interpretation
SELECT
    feature_name,
    coefficient,
    std_error,
    z_score,
    p_value,
    CASE WHEN p_value < 0.05 THEN 'Significant'
         ELSE 'Not Significant' END as significance
FROM ${DATABASE_NAME}.${TABLE_NAME}_glm_model
ORDER BY ABS(coefficient) DESC;
```

**Interpretation:**
- **Positive coefficient**: Feature increase leads to target increase
- **Negative coefficient**: Feature increase leads to target decrease
- **Magnitude**: Strength of relationship
- **p-value < 0.05**: Statistically significant relationship

#### Prediction Explanation for Specific Instance

```sql
-- Top features driving prediction for a specific case
SELECT
    feature_name,
    shap_value,
    CASE WHEN shap_value > 0 THEN 'Increases prediction'
         ELSE 'Decreases prediction' END as impact_direction,
    ABS(shap_value) as impact_magnitude
FROM ${DATABASE_NAME}.${TABLE_NAME}_shap_values
WHERE row_id = 'specific_instance_id'
ORDER BY impact_magnitude DESC
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
    CURRENT_TIMESTAMP as score_timestamp
FROM ${DATABASE_NAME}.${TABLE_NAME}_ml_ready t,
     TD_XGBoostPredict(
         ModelTable(${DATABASE_NAME}.${TABLE_NAME}_xgboost_model)
     ) p;
```

#### Batch Scoring Script

```sql
-- Score new data using trained model
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_new_predictions AS
SELECT
    new_data.*,
    p.prediction as predicted_${TARGET_COLUMN},
    CURRENT_DATE as prediction_date
FROM ${DATABASE_NAME}.${TABLE_NAME}_new_data new_data,
     TD_XGBoostPredict(
         ModelTable(${DATABASE_NAME}.${TABLE_NAME}_xgboost_model)
     ) p
WITH DATA;
```

#### Monitor Model Performance

```sql
-- Track prediction distribution over time
SELECT
    prediction_date,
    COUNT(*) as prediction_count,
    AVG(predicted_${TARGET_COLUMN}) as avg_prediction,
    MIN(predicted_${TARGET_COLUMN}) as min_prediction,
    MAX(predicted_${TARGET_COLUMN}) as max_prediction,
    STDDEV_POP(predicted_${TARGET_COLUMN}) as prediction_stddev
FROM ${DATABASE_NAME}.${TABLE_NAME}_new_predictions
GROUP BY prediction_date
ORDER BY prediction_date;
```

#### Model Performance Tracking

```sql
-- Compare predictions to actuals when labels become available
SELECT
    prediction_date,
    COUNT(*) as count,
    SQRT(AVG(POWER(actual_value - predicted_${TARGET_COLUMN}, 2))) as rmse,
    AVG(ABS(actual_value - predicted_${TARGET_COLUMN})) as mae,
    CORR(actual_value, predicted_${TARGET_COLUMN}) as correlation
FROM ${DATABASE_NAME}.${TABLE_NAME}_new_predictions
WHERE actual_value IS NOT NULL
GROUP BY prediction_date
ORDER BY prediction_date;
```

## Decision Guides

### When to Retrain Model

Retrain if:
- **RMSE increases >10%** on new data
- **Prediction distribution shifts** significantly
- **R² drops below 0.7** (if previously higher)
- **New features** are available
- **Seasonality changes** (for time-series)
- **Time-based**: Every 3-6 months for most use cases

### Model Selection Summary

**Use XGBoost when:**
- Need best possible accuracy
- Have sufficient training data (>1000 rows)
- Non-linear relationships exist
- Can tolerate longer training time

**Use DecisionForest when:**
- Need feature importance insights
- Have categorical features
- Want robust performance
- Non-linear patterns exist

**Use GLM (Linear) when:**
- Linear relationships exist
- Need fast training and scoring
- Want interpretable coefficients
- Need statistical inference (p-values)

**Use Ridge/Lasso/ElasticNet when:**
- Have many correlated features
- Risk of overfitting
- Need feature selection (Lasso)
- Want to prevent multicollinearity

### Choosing Evaluation Metric

**Use RMSE when:**
- Large errors are particularly costly
- Need to penalize outliers
- Comparing models on same scale

**Use MAE when:**
- All errors have similar cost
- Want robustness to outliers
- Need intuitive interpretation

**Use R² when:**
- Comparing different models
- Communicating overall fit
- Variance explanation matters

**Use MAPE when:**
- Relative accuracy matters
- Comparing across different scales
- Need percentage-based metric

## Output Artifacts

This workflow produces:
1. `${TABLE_NAME}_xgboost_model` - Trained XGBoost regression model
2. `${TABLE_NAME}_xgboost_predictions` - Test set predictions with residuals
3. `${TABLE_NAME}_shap_values` - Feature importance scores
4. `${TABLE_NAME}_scored` - Production scoring view
5. Model evaluation metrics (RMSE, MAE, R², MAPE)
6. Residual analysis results
7. Feature importance rankings
8. Model coefficients (for GLM)

## Best Practices

1. **Always use train/test split** - Never evaluate on training data
2. **Check residual distribution** - Should be normally distributed around zero
3. **Validate assumptions** - Ensure features are properly scaled
4. **Monitor prediction ranges** - Ensure predictions stay within reasonable bounds
5. **Track performance over time** - Monitor RMSE/MAE on new data
6. **Version models** - Keep track of model versions and performance
7. **Document feature engineering** - Record transformations applied
8. **Test edge cases** - Validate on extreme values
9. **Check for data leakage** - Ensure no future information in features
10. **Consider business constraints** - Some predictions may need bounds

## Common Issues and Solutions

### Issue: High RMSE but Good R²
**Cause:** Model fits pattern well but scale is off
**Solutions:**
- Check target variable scaling
- Review feature engineering
- Verify data quality
- Consider log transformation of target

### Issue: Poor Performance on Extreme Values
**Cause:** Limited training data at extremes
**Solutions:**
- Collect more data at extremes
- Use robust loss functions
- Consider quantile regression
- Apply winsorization

### Issue: Residuals Not Normally Distributed
**Cause:** Model assumptions violated or missing patterns
**Solutions:**
- Try non-linear models (XGBoost, RF)
- Add polynomial features
- Transform target variable (log, sqrt)
- Check for missing features

### Issue: Overfitting (Low Train Error, High Test Error)
**Solutions:**
- Reduce model complexity (MaxDepth, NumTrees)
- Increase regularization (Lambda)
- Use more training data
- Remove irrelevant features
- Apply feature selection

### Issue: Underfitting (High Train and Test Error)
**Solutions:**
- Add more relevant features
- Try more complex models
- Reduce regularization
- Increase model capacity (MaxDepth, NumTrees)
- Check for data quality issues

### Issue: Predictions Outside Valid Range
**Solutions:**
- Apply post-prediction clipping
- Use appropriate link functions (GLM)
- Review feature engineering
- Check for data leakage

## Function Reference Summary

### Model Training
- FunctionalPrompts/Advanced_Analytics/td_xgboost.md
- FunctionalPrompts/Advanced_Analytics/td_decisionforest.md
- FunctionalPrompts/Advanced_Analytics/td_glm.md

### Model Scoring
- FunctionalPrompts/Advanced_Analytics/td_xgboostpredict.md
- FunctionalPrompts/Advanced_Analytics/td_decisionforestpredict.md
- FunctionalPrompts/Advanced_Analytics/td_glmpredict.md

### Model Evaluation
- FunctionalPrompts/Advanced_Analytics/td_regressionevaluator.md
- FunctionalPrompts/Advanced_Analytics/td_shap.md

### Data Preparation
- ProcessPrompts/ml/ml_dataPreparation.md

---

**File Created**: 2025-11-28
**Version**: 1.0
**Workflow Type**: Regression
**Parent Persona**: persona_data_scientist.md
