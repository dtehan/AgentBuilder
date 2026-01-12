# TD_RegressionEvaluator

## Function Name
**TD_RegressionEvaluator** (alias: **TD_REGRESSIONEVALUATOR**)

## Description
TD_RegressionEvaluator evaluates the performance of regression models by computing a comprehensive set of statistical metrics that measure prediction accuracy and model quality. The function compares predicted values against actual observed values to generate metrics including Mean Absolute Error (MAE), Mean Squared Error (MSE), Root Mean Squared Error (RMSE), R² (coefficient of determination), Adjusted R², and many others.

**Key Characteristics:**
- **Comprehensive Metrics**: Computes 13+ regression evaluation metrics in a single function call
- **Model Quality Assessment**: Provides both absolute error metrics (MAE, MSE, RMSE) and relative quality metrics (R², Adjusted R²)
- **Statistical Rigor**: Includes F-statistic for overall model significance testing
- **Flexible Metric Selection**: Choose specific metrics or compute all available metrics
- **Production Monitoring**: Ideal for tracking model performance degradation over time
- **Model Comparison**: Enables objective comparison of different regression approaches
- **Business Interpretability**: Metrics like MAPE and R² are easily explained to non-technical stakeholders

## When to Use

### Business Applications
1. **Sales Forecasting Validation**
   - Evaluate accuracy of revenue predictions
   - Measure forecast error in business-relevant terms (MAPE, MAE)
   - Compare forecasting models (time series vs. regression)
   - Monitor forecast accuracy degradation over time

2. **Pricing Model Assessment**
   - Validate dynamic pricing algorithms
   - Measure price prediction accuracy (RMSE, MAE)
   - Assess impact of pricing features on model quality (R², Adjusted R²)
   - A/B test different pricing strategies

3. **Demand Planning Evaluation**
   - Assess inventory forecasting models
   - Quantify prediction errors in units (MAE) and squared terms (MSE)
   - Compare demand models across product categories
   - Detect seasonal model degradation

4. **Financial Risk Modeling**
   - Evaluate credit score predictions
   - Assess loan default amount predictions
   - Validate portfolio value forecasts
   - Measure predictive power (R²) of risk factors

5. **Real Estate Valuation**
   - Validate property price prediction models
   - Compare appraisal methodologies
   - Assess feature importance via model comparison
   - Monitor market condition changes via R² trends

6. **Customer Lifetime Value (CLV)**
   - Evaluate CLV prediction accuracy
   - Measure revenue forecast errors
   - Compare CLV models (historical vs. predictive)
   - Track model performance across customer segments

7. **Supply Chain Optimization**
   - Validate lead time predictions
   - Assess delivery time forecasting accuracy
   - Evaluate demand variability models
   - Compare optimization algorithms

8. **Energy Load Forecasting**
   - Evaluate electricity demand predictions
   - Assess weather-based forecasting models
   - Compare forecasting approaches (statistical vs. ML)
   - Monitor seasonal model performance

### Analytical Use Cases
- **Model Development**: Select best-performing model during training phase
- **Model Validation**: Assess generalization on held-out test sets
- **Model Monitoring**: Track production model performance over time
- **Feature Engineering**: Compare models with different feature sets
- **Hyperparameter Tuning**: Evaluate model configurations
- **A/B Testing**: Compare champion vs. challenger models
- **Bias Detection**: Identify systematic prediction errors (ME, MPE)
- **Model Explanation**: Quantify predictive power for stakeholders

## Syntax

```sql
SELECT * FROM TD_RegressionEvaluator (
    ON { table | view | (query) } AS InputTable
    USING
    ObservationColumn ('observation_column')
    PredictionColumn ('prediction_column')
    [ Metrics ('metric_name' [,...]) ]
    [ NumOfIndependentVariables (num_features) ]
    [ NumSample (sample_count) ]
    [ Accumulate ('column_name' [,...]) ]
) AS alias;
```

## Required Elements

### InputTable
The table containing both observed (actual) and predicted values for regression evaluation.

**Required Columns:**
- Observation column: Actual target values (continuous numeric)
- Prediction column: Model-predicted values (continuous numeric)

**Optional Columns:**
- ID columns for tracking individual predictions
- Timestamp columns for temporal analysis
- Segment columns for stratified evaluation
- Model version columns for comparison

### ObservationColumn
**Required parameter** specifying the column containing actual observed values.
- **Type**: String (column name)
- **Values**: Continuous numeric values (FLOAT, DOUBLE PRECISION, NUMERIC, DECIMAL)
- **Constraints**: Cannot contain NULL values; must have matching rows with predictions

**Example:** `ObservationColumn('actual_revenue')`

### PredictionColumn
**Required parameter** specifying the column containing model-predicted values.
- **Type**: String (column name)
- **Values**: Continuous numeric values matching observation scale
- **Constraints**: Cannot contain NULL values; must have same cardinality as observations

**Example:** `PredictionColumn('predicted_revenue')`

## Optional Elements

### Metrics
Specifies which regression metrics to compute. If omitted, all available metrics are calculated.

**Available Metrics:**
- **MAE**: Mean Absolute Error = (1/n) × Σ|y_i - ŷ_i|
- **MSE**: Mean Squared Error = (1/n) × Σ(y_i - ŷ_i)²
- **RMSE**: Root Mean Squared Error = √MSE
- **R2**: R-squared (coefficient of determination) = 1 - (SS_res / SS_tot)
- **AdjustedR2**: Adjusted R² = 1 - [(1 - R²) × (n - 1) / (n - k - 1)]
- **MSLE**: Mean Squared Logarithmic Error = (1/n) × Σ(log(y_i + 1) - log(ŷ_i + 1))²
- **MAPE**: Mean Absolute Percentage Error = (1/n) × Σ|((y_i - ŷ_i) / y_i)| × 100
- **MPE**: Mean Percentage Error = (1/n) × Σ((y_i - ŷ_i) / y_i) × 100
- **RMSLE**: Root Mean Squared Logarithmic Error = √MSLE
- **EV**: Explained Variance = 1 - (Var(y - ŷ) / Var(y))
- **ME**: Mean Error (bias) = (1/n) × Σ(y_i - ŷ_i)
- **MPD**: Mean Percentage Deviation
- **MGD**: Mean Geometric Deviation
- **FSTAT**: F-statistic for overall model significance

**Syntax:** `Metrics('MAE', 'RMSE', 'R2', 'AdjustedR2')`

**Default:** All metrics computed if not specified

### NumOfIndependentVariables
Number of independent variables (features) used in the regression model. Required for computing Adjusted R² and F-statistic.

**Type:** Integer
**Range:** 1 to number of features in model
**Default:** NULL (Adjusted R² and F-statistic not computed)

**Example:** `NumOfIndependentVariables(15)` for a model with 15 features

### NumSample
Total number of samples used to train the model. Required for certain statistical calculations.

**Type:** Integer
**Range:** Must be ≥ number of rows being evaluated
**Default:** NULL (derived from input data if not specified)

**Example:** `NumSample(100000)` for a model trained on 100K records

### Accumulate
Columns to pass through from the InputTable to the output, useful for grouping or tracking.

**Type:** String (column names)
**Use Cases:**
- Model identifiers for comparing multiple models
- Time periods for temporal tracking
- Segments for stratified evaluation

**Example:** `Accumulate('model_name', 'evaluation_date', 'customer_segment')`

## Input Specification

### InputTable Schema
```sql
CREATE TABLE regression_predictions (
    prediction_id INTEGER,              -- Optional: Unique identifier
    actual_value FLOAT,                 -- Required: Observed values
    predicted_value FLOAT,              -- Required: Model predictions
    model_name VARCHAR(50),             -- Optional: For model comparison
    prediction_date DATE,               -- Optional: For temporal tracking
    segment VARCHAR(50),                -- Optional: For stratified analysis
    features_json VARCHAR(5000)         -- Optional: Feature values for debugging
);
```

**Requirements:**
- Must contain at least one row (minimum 2 rows recommended for meaningful statistics)
- Observation and prediction columns must be numeric and non-NULL
- Matching rows between observations and predictions
- All rows contribute equally to metric calculations (no weighting)

**Best Practices:**
- Include ID columns for traceability
- Add timestamp columns for temporal analysis
- Include model identifiers when comparing multiple models
- Ensure prediction scale matches observation scale

## Output Specification

### Output Table Schema
```sql
-- Output: Single row with all requested metrics
model_name          | VARCHAR  -- (if accumulated)
evaluation_date     | DATE     -- (if accumulated)
segment             | VARCHAR  -- (if accumulated)
MAE                 | FLOAT    -- Mean Absolute Error
MSE                 | FLOAT    -- Mean Squared Error
RMSE                | FLOAT    -- Root Mean Squared Error
R2                  | FLOAT    -- R-squared
AdjustedR2          | FLOAT    -- Adjusted R² (if NumOfIndependentVariables provided)
MSLE                | FLOAT    -- Mean Squared Logarithmic Error
MAPE                | FLOAT    -- Mean Absolute Percentage Error
MPE                 | FLOAT    -- Mean Percentage Error
RMSLE               | FLOAT    -- Root Mean Squared Logarithmic Error
EV                  | FLOAT    -- Explained Variance
ME                  | FLOAT    -- Mean Error (bias)
MPD                 | FLOAT    -- Mean Percentage Deviation
MGD                 | FLOAT    -- Mean Geometric Deviation
FSTAT               | FLOAT    -- F-statistic (if NumOfIndependentVariables provided)
```

**Metric Interpretations:**

**Absolute Error Metrics** (Lower is Better):
- **MAE**: Average absolute prediction error in original units. Robust to outliers.
- **MSE**: Average squared error. Penalizes large errors more heavily than MAE.
- **RMSE**: Square root of MSE, in original units. Most common regression metric.
- **MSLE/RMSLE**: Logarithmic error metrics for right-skewed targets (e.g., prices, counts).

**Relative Quality Metrics**:
- **R²**: Proportion of variance explained (0 to 1, higher is better). R² = 0.85 means model explains 85% of variance.
- **Adjusted R²**: R² adjusted for number of features. Penalizes overfitting.
- **EV**: Explained variance score. Similar to R² but uses different variance calculation.

**Bias Metrics**:
- **ME**: Average prediction error (can be positive or negative). ME ≠ 0 indicates systematic bias.
- **MPE**: Mean percentage error. Indicates direction of bias (over-prediction vs. under-prediction).

**Percentage Error Metrics** (Lower is Better):
- **MAPE**: Average absolute percentage error. Scale-independent, good for comparing models across different targets.
- **MPD**: Mean percentage deviation.
- **MGD**: Mean geometric deviation.

**Statistical Significance**:
- **F-statistic**: Tests if model explains significantly more variance than random. Higher is better.

**Output Characteristics:**
- Single row per evaluation (or per group if using Accumulate)
- All metrics returned unless specific Metrics parameter used
- NULL values for metrics requiring NumOfIndependentVariables if not provided
- Metrics computed on all non-NULL prediction/observation pairs

## Code Examples

### Example 1: Basic Regression Model Evaluation - Sales Forecasting

**Business Context:**
A retail company built a linear regression model to forecast monthly store revenue based on 8 features (store size, location demographics, marketing spend, seasonality, etc.). The data science team needs to evaluate the model's performance on the test set to determine if it's accurate enough for production deployment. Management requires forecasts within 10% error (MAPE < 10%) and strong explanatory power (R² > 0.75).

**SQL Code:**
```sql
-- Step 1: Generate predictions on test set (already completed, stored in revenue_predictions)
-- Assume model training used TD_GLM or TD_LinReg on training data

-- Step 2: Evaluate regression model performance
SELECT * FROM TD_RegressionEvaluator (
    ON revenue_predictions AS InputTable
    USING
    ObservationColumn('actual_monthly_revenue')
    PredictionColumn('predicted_monthly_revenue')
    Metrics('MAE', 'RMSE', 'R2', 'AdjustedR2', 'MAPE', 'ME')
    NumOfIndependentVariables(8)
    Accumulate('model_version')
) AS evaluation;

-- Step 3: Compare against baseline (previous year same month)
SELECT * FROM TD_RegressionEvaluator (
    ON revenue_predictions AS InputTable
    USING
    ObservationColumn('actual_monthly_revenue')
    PredictionColumn('previous_year_revenue')  -- Naive baseline
    Metrics('MAE', 'RMSE', 'MAPE')
) AS baseline_evaluation;
```

**Sample Output:**
```
model_version | MAE      | RMSE     | R2    | AdjustedR2 | MAPE  | ME
--------------+----------+----------+-------+------------+-------+--------
v2.1_linreg   | 12450.32 | 18234.67 | 0.823 | 0.816      | 7.82  | -234.56

-- Baseline comparison:
MAE      | RMSE     | MAPE
---------+----------+-------
23456.78 | 34567.89 | 18.45
```

**Business Impact:**
- **Model Performance**: R² = 0.823 indicates model explains 82.3% of revenue variance (exceeds 75% threshold)
- **Accuracy**: MAPE = 7.82% means average forecast is within 8% of actual (beats 10% requirement)
- **Bias**: ME = -234.56 shows slight under-prediction tendency (only 0.2% of average revenue)
- **Business Value**: Model improves over naive baseline by 46.9% (MAPE: 18.45% → 7.82%)
- **Deployment Decision**: Model approved for production with quarterly re-evaluation
- **Financial Impact**: More accurate forecasts enable optimized inventory ($1.2M savings annually) and staffing decisions

---

### Example 2: Comparing Multiple Regression Models - House Price Prediction

**Business Context:**
A real estate platform developed three different models to predict house sale prices: (1) Linear Regression with 12 features, (2) Random Forest with 25 features, and (3) XGBoost with 35 features. The analytics team needs to select the best model balancing accuracy, complexity, and interpretability. Key decision criteria: highest R², lowest RMSE, and reasonable Adjusted R² (to avoid overfitting).

**SQL Code:**
```sql
-- Step 1: Combine predictions from all three models
CREATE VOLATILE TABLE all_model_predictions AS (
    SELECT
        p.property_id,
        p.actual_sale_price,
        lr.predicted_price AS lr_prediction,
        rf.predicted_price AS rf_prediction,
        xgb.predicted_price AS xgb_prediction,
        p.property_type,
        p.location_tier
    FROM property_test_set p
    INNER JOIN linreg_predictions lr ON p.property_id = lr.property_id
    INNER JOIN randomforest_predictions rf ON p.property_id = rf.property_id
    INNER JOIN xgboost_predictions xgb ON p.property_id = xgb.property_id
) WITH DATA PRIMARY INDEX (property_id) ON COMMIT PRESERVE ROWS;

-- Step 2: Evaluate Linear Regression model
SELECT
    'Linear Regression' AS model_name,
    12 AS num_features,
    eval.*
FROM TD_RegressionEvaluator (
    ON all_model_predictions AS InputTable
    USING
    ObservationColumn('actual_sale_price')
    PredictionColumn('lr_prediction')
    Metrics('MAE', 'RMSE', 'R2', 'AdjustedR2', 'MAPE')
    NumOfIndependentVariables(12)
) AS eval

UNION ALL

-- Step 3: Evaluate Random Forest model
SELECT
    'Random Forest' AS model_name,
    25 AS num_features,
    eval.*
FROM TD_RegressionEvaluator (
    ON all_model_predictions AS InputTable
    USING
    ObservationColumn('actual_sale_price')
    PredictionColumn('rf_prediction')
    Metrics('MAE', 'RMSE', 'R2', 'AdjustedR2', 'MAPE')
    NumOfIndependentVariables(25)
) AS eval

UNION ALL

-- Step 4: Evaluate XGBoost model
SELECT
    'XGBoost' AS model_name,
    35 AS num_features,
    eval.*
FROM TD_RegressionEvaluator (
    ON all_model_predictions AS InputTable
    USING
    ObservationColumn('actual_sale_price')
    PredictionColumn('xgb_prediction')
    Metrics('MAE', 'RMSE', 'R2', 'AdjustedR2', 'MAPE')
    NumOfIndependentVariables(35)
) AS eval
ORDER BY R2 DESC;

-- Step 5: Segment analysis by property type
SELECT
    property_type,
    'XGBoost' AS model_name,
    eval.*
FROM TD_RegressionEvaluator (
    ON all_model_predictions AS InputTable
    PARTITION BY property_type
    USING
    ObservationColumn('actual_sale_price')
    PredictionColumn('xgb_prediction')
    Metrics('RMSE', 'R2', 'MAPE')
    NumOfIndependentVariables(35)
    Accumulate('property_type')
) AS eval
ORDER BY property_type, R2 DESC;
```

**Sample Output:**
```
model_name        | num_features | MAE      | RMSE     | R2    | AdjustedR2 | MAPE
------------------+--------------+----------+----------+-------+------------+-------
XGBoost           | 35           | 28450.23 | 42123.67 | 0.912 | 0.908      | 8.34
Random Forest     | 25           | 31234.56 | 45678.90 | 0.897 | 0.894      | 9.12
Linear Regression | 12           | 45678.12 | 67890.34 | 0.832 | 0.829      | 13.45

-- Segment analysis (XGBoost):
property_type | RMSE     | R2    | MAPE
--------------+----------+-------+-------
Single Family | 38234.56 | 0.923 | 7.45
Condo         | 29876.54 | 0.901 | 8.12
Townhouse     | 41234.78 | 0.887 | 9.67
```

**Business Impact:**
- **Model Selection**: XGBoost wins with R² = 0.912 (highest explanatory power) and RMSE = $42,124 (lowest error)
- **Complexity vs. Performance**: XGBoost's additional 23 features (vs. Linear Regression) improve R² by 9.6% and reduce RMSE by 38%
- **Adjusted R² Check**: Adjusted R² = 0.908 (only 0.004 lower than R²) indicates minimal overfitting despite 35 features
- **Percentage Accuracy**: MAPE = 8.34% means predictions typically within 8.34% of actual price (acceptable for pricing guidance)
- **Segment Insights**: Single Family homes have best predictions (R² = 0.923), Townhouses are hardest to predict (R² = 0.887)
- **Business Decision**: Deploy XGBoost for automated pricing with human review for Townhouse properties
- **Revenue Impact**: Improved pricing accuracy increases listing success rate by 12%, generating $3.2M additional commission annually

---

### Example 3: Time Series Forecasting Evaluation - Energy Demand Prediction

**Business Context:**
An electric utility company built a forecasting model to predict hourly energy demand (MW) for grid management. The model uses 20 features including weather data, time features, historical demand, and holiday indicators. Grid operators need to evaluate model accuracy across different time horizons (1-hour, 4-hour, 24-hour ahead) and detect any systematic bias that could lead to brownouts (under-prediction) or unnecessary generator activation (over-prediction).

**SQL Code:**
```sql
-- Step 1: Generate predictions for different forecast horizons
-- Assume forecasting model already trained and predictions stored

-- Step 2: Evaluate 1-hour ahead forecasts
SELECT
    '1-hour ahead' AS forecast_horizon,
    eval.*
FROM TD_RegressionEvaluator (
    ON demand_predictions_1h AS InputTable
    USING
    ObservationColumn('actual_demand_mw')
    PredictionColumn('predicted_demand_mw')
    Metrics('MAE', 'RMSE', 'R2', 'MAPE', 'ME', 'MPE')
    NumOfIndependentVariables(20)
    Accumulate('forecast_horizon')
) AS eval

UNION ALL

-- Step 3: Evaluate 4-hour ahead forecasts
SELECT
    '4-hour ahead' AS forecast_horizon,
    eval.*
FROM TD_RegressionEvaluator (
    ON demand_predictions_4h AS InputTable
    USING
    ObservationColumn('actual_demand_mw')
    PredictionColumn('predicted_demand_mw')
    Metrics('MAE', 'RMSE', 'R2', 'MAPE', 'ME', 'MPE')
    NumOfIndependentVariables(20)
    Accumulate('forecast_horizon')
) AS eval

UNION ALL

-- Step 4: Evaluate 24-hour ahead forecasts
SELECT
    '24-hour ahead' AS forecast_horizon,
    eval.*
FROM TD_RegressionEvaluator (
    ON demand_predictions_24h AS InputTable
    USING
    ObservationColumn('actual_demand_mw')
    PredictionColumn('predicted_demand_mw')
    Metrics('MAE', 'RMSE', 'R2', 'MAPE', 'ME', 'MPE')
    NumOfIndependentVariables(20)
    Accumulate('forecast_horizon')
) AS eval
ORDER BY forecast_horizon;

-- Step 5: Evaluate by time of day (peak vs. off-peak)
SELECT
    CASE
        WHEN EXTRACT(HOUR FROM prediction_timestamp) BETWEEN 7 AND 22 THEN 'Peak Hours'
        ELSE 'Off-Peak Hours'
    END AS period_type,
    eval.*
FROM TD_RegressionEvaluator (
    ON (
        SELECT
            *,
            CASE
                WHEN EXTRACT(HOUR FROM prediction_timestamp) BETWEEN 7 AND 22 THEN 'Peak Hours'
                ELSE 'Off-Peak Hours'
            END AS period_type
        FROM demand_predictions_1h
    ) AS InputTable
    PARTITION BY period_type
    USING
    ObservationColumn('actual_demand_mw')
    PredictionColumn('predicted_demand_mw')
    Metrics('MAE', 'RMSE', 'MAPE', 'ME')
    Accumulate('period_type')
) AS eval
ORDER BY period_type;

-- Step 6: Detect systematic bias by season
SELECT
    season,
    eval.*
FROM TD_RegressionEvaluator (
    ON demand_predictions_1h AS InputTable
    PARTITION BY season
    USING
    ObservationColumn('actual_demand_mw')
    PredictionColumn('predicted_demand_mw')
    Metrics('MAE', 'RMSE', 'ME', 'MPE')
    NumOfIndependentVariables(20)
    Accumulate('season')
) AS eval
ORDER BY season;
```

**Sample Output:**
```
forecast_horizon | MAE    | RMSE   | R2    | MAPE | ME      | MPE
-----------------+--------+--------+-------+------+---------+-------
1-hour ahead     | 124.56 | 178.34 | 0.945 | 3.45 | -12.34  | -0.34
4-hour ahead     | 234.67 | 345.78 | 0.887 | 6.78 | -45.67  | -1.23
24-hour ahead    | 456.89 | 678.90 | 0.812 | 11.2 | -123.45 | -3.45

-- Peak vs. Off-Peak analysis:
period_type     | MAE    | RMSE   | MAPE | ME
----------------+--------+--------+------+--------
Peak Hours      | 156.78 | 234.56 | 4.12 | -23.45
Off-Peak Hours  | 89.34  | 123.45 | 2.89 | -5.67

-- Seasonal bias analysis:
season | MAE    | RMSE   | ME       | MPE
-------+--------+--------+----------+------
Winter | 178.90 | 267.34 | -67.89   | -1.89
Spring | 112.34 | 156.78 | -23.45   | -0.67
Summer | 203.45 | 312.67 | -89.12   | -2.34
Fall   | 98.76  | 145.23 | -12.34   | -0.45
```

**Business Impact:**
- **Forecast Accuracy Degrades with Horizon**: 1-hour R² = 0.945 (excellent), 24-hour R² = 0.812 (acceptable)
- **1-Hour Forecasts**: MAPE = 3.45% enables tight grid management with minimal safety margins
- **Systematic Under-Prediction Bias**: ME consistently negative across all horizons (model under-predicts demand)
  - 1-hour: Under-predicts by 12.34 MW (0.34% MPE)
  - 24-hour: Under-predicts by 123.45 MW (3.45% MPE)
- **Bias Risk**: Under-prediction could lead to grid instability if reserves insufficient
- **Peak Hour Challenge**: Higher errors during peak hours (MAE = 156.78 vs. 89.34 off-peak) due to demand volatility
- **Seasonal Patterns**: Summer has worst performance (RMSE = 312.67 MW) due to air conditioning variability
- **Corrective Action**: Add +1.5% bias correction factor to all forecasts, prioritize summer re-training
- **Operational Impact**: Improved forecasts reduce unnecessary generator activations by $2.8M/year in fuel costs
- **Reliability Impact**: Better peak hour predictions prevent 4 potential brownout events annually

---

### Example 4: Feature Importance via Model Comparison - Customer Churn Prediction

**Business Context:**
A telecom company wants to predict monthly customer churn revenue ($ amount of monthly recurring revenue at risk). The data science team built multiple models with different feature sets to understand which features most impact prediction accuracy. By comparing R² and Adjusted R² across models, they can identify the most valuable features for churn prevention campaigns.

**SQL Code:**
```sql
-- Step 1: Train models with incrementally added feature groups
-- Model 1: Basic demographics only (5 features)
-- Model 2: Demographics + usage patterns (12 features)
-- Model 3: Demographics + usage + service history (20 features)
-- Model 4: Full feature set including satisfaction scores (28 features)

-- Step 2: Evaluate Model 1 - Demographics only
SELECT
    'Model 1: Demographics' AS model_name,
    5 AS num_features,
    'Age, Gender, Location, Income, Account_Age' AS feature_groups,
    eval.*
FROM TD_RegressionEvaluator (
    ON churn_revenue_predictions_model1 AS InputTable
    USING
    ObservationColumn('actual_churn_revenue')
    PredictionColumn('predicted_churn_revenue')
    Metrics('R2', 'AdjustedR2', 'RMSE', 'MAE', 'MAPE')
    NumOfIndependentVariables(5)
) AS eval

UNION ALL

-- Step 3: Evaluate Model 2 - Demographics + Usage
SELECT
    'Model 2: + Usage Patterns' AS model_name,
    12 AS num_features,
    '+ Call_Volume, Data_Usage, SMS_Count, Peak_Usage_Pct, International_Calls, Support_Contacts, Payment_Method' AS feature_groups,
    eval.*
FROM TD_RegressionEvaluator (
    ON churn_revenue_predictions_model2 AS InputTable
    USING
    ObservationColumn('actual_churn_revenue')
    PredictionColumn('predicted_churn_revenue')
    Metrics('R2', 'AdjustedR2', 'RMSE', 'MAE', 'MAPE')
    NumOfIndependentVariables(12)
) AS eval

UNION ALL

-- Step 4: Evaluate Model 3 - Demographics + Usage + Service History
SELECT
    'Model 3: + Service History' AS model_name,
    20 AS num_features,
    '+ Plan_Changes, Upgrades, Downgrades, Service_Outages, Billing_Issues, Contract_Type, Loyalty_Tier, Promotions_Used' AS feature_groups,
    eval.*
FROM TD_RegressionEvaluator (
    ON churn_revenue_predictions_model3 AS InputTable
    USING
    ObservationColumn('actual_churn_revenue')
    PredictionColumn('predicted_churn_revenue')
    Metrics('R2', 'AdjustedR2', 'RMSE', 'MAE', 'MAPE')
    NumOfIndependentVariables(20)
) AS eval

UNION ALL

-- Step 5: Evaluate Model 4 - Full feature set
SELECT
    'Model 4: + Satisfaction Scores' AS model_name,
    28 AS num_features,
    '+ NPS_Score, CSAT_Score, App_Rating, Network_Satisfaction, Support_Satisfaction, Billing_Satisfaction, Product_Satisfaction, Recommendation_Score' AS feature_groups,
    eval.*
FROM TD_RegressionEvaluator (
    ON churn_revenue_predictions_model4 AS InputTable
    USING
    ObservationColumn('actual_churn_revenue')
    PredictionColumn('predicted_churn_revenue')
    Metrics('R2', 'AdjustedR2', 'RMSE', 'MAE', 'MAPE')
    NumOfIndependentVariables(28)
) AS eval
ORDER BY R2 DESC;

-- Step 6: Calculate incremental R² improvement
SELECT
    model_name,
    num_features,
    R2,
    AdjustedR2,
    R2 - LAG(R2) OVER (ORDER BY num_features) AS r2_improvement,
    RMSE,
    RMSE / FIRST_VALUE(RMSE) OVER (ORDER BY num_features ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS rmse_vs_baseline
FROM model_comparison_results
ORDER BY num_features;
```

**Sample Output:**
```
model_name                    | num_features | R2    | AdjustedR2 | RMSE    | MAE     | MAPE
------------------------------+--------------+-------+------------+---------+---------+-------
Model 1: Demographics         | 5            | 0.412 | 0.408      | 234.56  | 178.90  | 18.34
Model 2: + Usage Patterns     | 12           | 0.678 | 0.672      | 178.34  | 134.56  | 13.78
Model 3: + Service History    | 20           | 0.812 | 0.804      | 134.67  | 98.76   | 10.12
Model 4: + Satisfaction Score | 28           | 0.889 | 0.878      | 103.45  | 76.89   | 7.89

-- Incremental analysis:
model_name                    | R2    | r2_improvement | RMSE    | rmse_vs_baseline
------------------------------+-------+----------------+---------+------------------
Model 1: Demographics         | 0.412 | NULL           | 234.56  | 1.000
Model 2: + Usage Patterns     | 0.678 | 0.266          | 178.34  | 0.760
Model 3: + Service History    | 0.812 | 0.134          | 134.67  | 0.574
Model 4: + Satisfaction Score | 0.889 | 0.077          | 103.45  | 0.441
```

**Business Impact:**
- **Feature Group Value Ranking**:
  1. **Usage Patterns**: Largest R² improvement (+0.266, from 0.412 to 0.678) - MOST VALUABLE
  2. **Service History**: Strong improvement (+0.134, from 0.678 to 0.812)
  3. **Satisfaction Scores**: Moderate improvement (+0.077, from 0.812 to 0.889)
  4. **Demographics**: Weak predictive power alone (R² = 0.412)

- **Model Selection**: Model 4 (full feature set) provides best performance with R² = 0.889 and MAPE = 7.89%
- **Adjusted R² Validation**: Adjusted R² = 0.878 (only 0.011 lower than R²) confirms features genuinely improve model vs. overfitting
- **Prediction Accuracy**: RMSE = $103.45 means typical error is $103 in predicting monthly churn revenue per customer
- **Improvement Over Baseline**: Full model reduces RMSE by 55.9% compared to demographics alone (0.441 vs. 1.000)

- **Business Insights**:
  - **Priority 1**: Focus churn prevention on customers with high call volume, data usage, and support contacts (usage patterns)
  - **Priority 2**: Proactively manage customers experiencing service outages and billing issues (service history)
  - **Priority 3**: Monitor NPS and CSAT scores for early churn warning signals (satisfaction scores)
  - Demographics alone are insufficient for targeting (R² = 0.412)

- **Campaign Optimization**:
  - Target top 10% predicted churn revenue (Model 4 identifies $2.3M at-risk MRR with 89% accuracy)
  - Retention offers focused on usage pattern and service history segments
  - Save $1.8M annually in prevented churn (78% retention rate on targeted campaigns)

- **Data Collection Priority**: Justify investment in NPS/CSAT surveys based on R² improvement (0.077 lift worth $450K annually in better targeting)

---

### Example 5: Production Model Monitoring Over Time - Loan Default Amount Prediction

**Business Context:**
A lending institution deployed a regression model 18 months ago to predict loan default amounts ($ loss per defaulted loan) for loss reserve calculations. The risk management team monitors model performance monthly to detect degradation that could lead to insufficient reserves and regulatory issues. They track R², RMSE, and bias (ME) over time, with alerts triggered if RMSE increases by >15% or |ME| exceeds $500.

**SQL Code:**
```sql
-- Step 1: Evaluate model performance for each month over past 18 months
SELECT
    evaluation_month,
    eval.*
FROM TD_RegressionEvaluator (
    ON monthly_default_predictions AS InputTable
    PARTITION BY evaluation_month
    USING
    ObservationColumn('actual_default_amount')
    PredictionColumn('predicted_default_amount')
    Metrics('R2', 'AdjustedR2', 'RMSE', 'MAE', 'MAPE', 'ME', 'MPE')
    NumOfIndependentVariables(18)
    Accumulate('evaluation_month')
) AS eval
ORDER BY evaluation_month;

-- Step 2: Calculate performance trends and degradation indicators
CREATE VOLATILE TABLE model_performance_trends AS (
    SELECT
        evaluation_month,
        R2,
        RMSE,
        ME,
        -- Compare to baseline (first 3 months average)
        RMSE / AVG(RMSE) OVER (ORDER BY evaluation_month ROWS BETWEEN 17 PRECEDING AND 15 PRECEDING) AS rmse_vs_baseline,
        ABS(ME) / AVG(ABS(ME)) OVER (ORDER BY evaluation_month ROWS BETWEEN 17 PRECEDING AND 15 PRECEDING) AS bias_vs_baseline,
        -- Trend indicators
        R2 - LAG(R2, 3) OVER (ORDER BY evaluation_month) AS r2_3month_change,
        RMSE - LAG(RMSE, 3) OVER (ORDER BY evaluation_month) AS rmse_3month_change,
        -- Alert flags
        CASE
            WHEN RMSE / AVG(RMSE) OVER (ORDER BY evaluation_month ROWS BETWEEN 17 PRECEDING AND 15 PRECEDING) > 1.15
            THEN 'ALERT: RMSE Degradation >15%'
            WHEN ABS(ME) > 500
            THEN 'ALERT: Bias Exceeds Threshold'
            WHEN R2 < 0.70
            THEN 'WARNING: R² Below Target'
            ELSE 'OK'
        END AS status_flag
    FROM monthly_model_performance
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 3: Summarize alert periods
SELECT
    evaluation_month,
    R2,
    RMSE,
    ME,
    ROUND(rmse_vs_baseline, 3) AS rmse_vs_baseline,
    ROUND(bias_vs_baseline, 3) AS bias_vs_baseline,
    status_flag
FROM model_performance_trends
WHERE status_flag != 'OK'
ORDER BY evaluation_month;

-- Step 4: Segment analysis for recent degradation period
-- Investigate performance by loan type for months with alerts
SELECT
    loan_type,
    evaluation_month,
    COUNT(*) AS num_predictions,
    eval.*
FROM TD_RegressionEvaluator (
    ON (
        SELECT * FROM monthly_default_predictions
        WHERE evaluation_month >= '2024-09-01'  -- Recent degradation period
    ) AS InputTable
    PARTITION BY loan_type, evaluation_month
    USING
    ObservationColumn('actual_default_amount')
    PredictionColumn('predicted_default_amount')
    Metrics('R2', 'RMSE', 'MAE', 'ME')
    Accumulate('loan_type', 'evaluation_month')
) AS eval
ORDER BY loan_type, evaluation_month;
```

**Sample Output:**
```
-- Monthly performance trends:
evaluation_month | R2    | RMSE     | ME       | MAPE  | status_flag
-----------------+-------+----------+----------+-------+---------------------------
2023-06-01       | 0.845 | 1234.56  | -123.45  | 8.34  | OK
2023-07-01       | 0.838 | 1289.67  | -145.67  | 8.67  | OK
...
2024-06-01       | 0.812 | 1456.78  | -234.56  | 9.89  | OK
2024-07-01       | 0.789 | 1567.89  | -345.67  | 11.23 | WARNING: R² Below Target
2024-08-01       | 0.763 | 1678.90  | -456.78  | 12.45 | WARNING: R² Below Target
2024-09-01       | 0.734 | 1789.12  | -567.89  | 13.78 | ALERT: RMSE Degradation >15%
2024-10-01       | 0.712 | 1856.34  | -623.45  | 14.56 | ALERT: Bias Exceeds Threshold
2024-11-01       | 0.698 | 1923.45  | -678.90  | 15.34 | ALERT: Multiple Issues

-- Alert summary:
evaluation_month | R2    | RMSE     | ME       | rmse_vs_baseline | bias_vs_baseline | status_flag
-----------------+-------+----------+----------+------------------+------------------+---------------------------
2024-07-01       | 0.789 | 1567.89  | -345.67  | 1.089            | 2.345            | WARNING: R² Below Target
2024-09-01       | 0.734 | 1789.12  | -567.89  | 1.234            | 3.678            | ALERT: RMSE Degradation >15%
2024-10-01       | 0.712 | 1856.34  | -623.45  | 1.287            | 4.234            | ALERT: Bias Exceeds Threshold
2024-11-01       | 0.698 | 1923.45  | -678.90  | 1.334            | 4.589            | ALERT: Multiple Issues

-- Segment analysis (recent months):
loan_type           | evaluation_month | num_predictions | R2    | RMSE     | MAE      | ME
--------------------+------------------+-----------------+-------+----------+----------+----------
Auto Loan           | 2024-09-01       | 1,234           | 0.812 | 1234.56  | 987.65   | -234.56
Auto Loan           | 2024-10-01       | 1,345           | 0.798 | 1289.67  | 1023.45  | -267.89
Auto Loan           | 2024-11-01       | 1,456           | 0.776 | 1345.78  | 1089.12  | -301.23
Personal Loan       | 2024-09-01       | 2,345           | 0.723 | 1987.65  | 1567.89  | -678.90
Personal Loan       | 2024-10-01       | 2,567           | 0.689 | 2134.56  | 1678.90  | -756.78
Personal Loan       | 2024-11-01       | 2,789           | 0.654 | 2289.67  | 1789.12  | -834.56  ← WORST
Mortgage            | 2024-09-01       | 3,456           | 0.856 | 1456.78  | 1123.45  | -345.67
Mortgage            | 2024-10-01       | 3,678           | 0.845 | 1489.12  | 1156.78  | -367.89
Mortgage            | 2024-11-01       | 3,890           | 0.834 | 1523.45  | 1189.12  | -389.23
```

**Business Impact:**
- **Model Degradation Detected**: Performance declining since July 2024
  - R² dropped from 0.845 (June 2023) to 0.698 (Nov 2024) - 17.4% decline
  - RMSE increased from $1,235 to $1,923 - 55.7% degradation (exceeds 15% alert threshold)
  - Bias increased from -$123 to -$679 (exceeds $500 alert threshold)

- **Under-Prediction Bias Growing**: ME increasingly negative indicates systematic under-prediction of default amounts
  - Current bias: -$679 means model under-predicts losses by $679 per default on average
  - Bias trend accelerating: 4.6x worse than baseline (bias_vs_baseline = 4.589)

- **Segment-Specific Issues**:
  - **Personal Loans**: Worst performance (R² = 0.654, RMSE = $2,290, ME = -$835) - PRIMARY PROBLEM
  - **Mortgages**: Stable performance (R² = 0.834, RMSE = $1,523) - performing well
  - **Auto Loans**: Moderate degradation (R² = 0.776, RMSE = $1,346) - acceptable but declining

- **Root Cause Hypothesis**: Personal loan market conditions changed (interest rates, borrower profiles, economic stress)

- **Financial Risk**:
  - Under-prediction of $679 per default × 2,789 personal loan defaults in Nov = $1.89M under-reserved
  - Over 18 months of degradation: Estimated $12-15M cumulative under-reserving
  - Regulatory risk: Insufficient loss reserves could trigger regulatory review

- **Immediate Actions**:
  1. **Urgent**: Adjust loss reserves upward by $2M for personal loan portfolio to cover under-prediction bias
  2. **Short-term**: Retrain model on recent 12 months of data (market conditions changed)
  3. **Medium-term**: Add macroeconomic features (unemployment rate, interest rates, inflation) to capture market shifts
  4. **Long-term**: Implement automated monthly retraining pipeline with performance alerts

- **Re-training Impact**: After retraining on recent data (executed Dec 2024):
  - Personal Loan R² improved from 0.654 to 0.812 (+24%)
  - Personal Loan RMSE reduced from $2,290 to $1,456 (-36%)
  - Bias reduced from -$835 to -$156 (within acceptable range)
  - Estimated savings: $8M annually in more accurate reserves (reduces over-reserving and under-reserving)

---

### Example 6: Model Selection with Business Cost Metrics - Demand Forecasting

**Business Context:**
A consumer goods manufacturer developed multiple models to forecast weekly product demand for production planning. While statistical metrics (RMSE, R²) are important, the business cares most about minimizing two costs: (1) under-forecasting leads to stockouts and lost sales ($50 per unit shortage), and (2) over-forecasting leads to excess inventory and waste ($10 per unit surplus). The analytics team needs to evaluate models not just on accuracy, but on business cost impact.

**SQL Code:**
```sql
-- Step 1: Evaluate three candidate models on statistical metrics
CREATE VOLATILE TABLE model_statistical_evaluation AS (
    SELECT
        'ARIMA' AS model_name,
        10 AS num_features,
        eval.*
    FROM TD_RegressionEvaluator (
        ON demand_predictions_arima AS InputTable
        USING
        ObservationColumn('actual_demand_units')
        PredictionColumn('predicted_demand_units')
        Metrics('MAE', 'RMSE', 'R2', 'MAPE', 'ME', 'MPE')
        NumOfIndependentVariables(10)
    ) AS eval

    UNION ALL

    SELECT
        'XGBoost' AS model_name,
        25 AS num_features,
        eval.*
    FROM TD_RegressionEvaluator (
        ON demand_predictions_xgboost AS InputTable
        USING
        ObservationColumn('actual_demand_units')
        PredictionColumn('predicted_demand_units')
        Metrics('MAE', 'RMSE', 'R2', 'MAPE', 'ME', 'MPE')
        NumOfIndependentVariables(25)
    ) AS eval

    UNION ALL

    SELECT
        'Prophet' AS model_name,
        15 AS num_features,
        eval.*
    FROM TD_RegressionEvaluator (
        ON demand_predictions_prophet AS InputTable
        USING
        ObservationColumn('actual_demand_units')
        PredictionColumn('predicted_demand_units')
        Metrics('MAE', 'RMSE', 'R2', 'MAPE', 'ME', 'MPE')
        NumOfIndependentVariables(15)
    ) AS eval
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 2: Calculate business cost impact for each model
CREATE VOLATILE TABLE model_business_cost_analysis AS (
    SELECT
        model_name,

        -- Statistical metrics
        MAE,
        RMSE,
        R2,
        ME AS avg_bias,

        -- Business cost calculations
        SUM(CASE
            WHEN actual_demand_units > predicted_demand_units
            THEN (actual_demand_units - predicted_demand_units) * 50  -- Stockout cost: $50/unit
            ELSE 0
        END) AS total_stockout_cost,

        SUM(CASE
            WHEN predicted_demand_units > actual_demand_units
            THEN (predicted_demand_units - actual_demand_units) * 10  -- Excess inventory cost: $10/unit
            ELSE 0
        END) AS total_excess_cost,

        SUM(CASE
            WHEN actual_demand_units > predicted_demand_units
            THEN (actual_demand_units - predicted_demand_units) * 50
            ELSE (predicted_demand_units - actual_demand_units) * 10
        END) AS total_business_cost,

        -- Frequency of errors
        COUNT(CASE WHEN actual_demand_units > predicted_demand_units THEN 1 END) AS num_stockouts,
        COUNT(CASE WHEN predicted_demand_units > actual_demand_units THEN 1 END) AS num_excess_inventory,
        COUNT(*) AS total_predictions,

        -- Average error sizes
        AVG(CASE
            WHEN actual_demand_units > predicted_demand_units
            THEN actual_demand_units - predicted_demand_units
        END) AS avg_stockout_units,
        AVG(CASE
            WHEN predicted_demand_units > actual_demand_units
            THEN predicted_demand_units - actual_demand_units
        END) AS avg_excess_units

    FROM (
        SELECT 'ARIMA' AS model_name, actual_demand_units, predicted_demand_units
        FROM demand_predictions_arima
        UNION ALL
        SELECT 'XGBoost' AS model_name, actual_demand_units, predicted_demand_units
        FROM demand_predictions_xgboost
        UNION ALL
        SELECT 'Prophet' AS model_name, actual_demand_units, predicted_demand_units
        FROM demand_predictions_prophet
    ) AS all_predictions
    GROUP BY model_name
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 3: Combine statistical and business metrics
SELECT
    s.model_name,
    s.num_features,
    s.MAE,
    s.RMSE,
    s.R2,
    s.ME AS statistical_bias,
    b.total_stockout_cost,
    b.total_excess_cost,
    b.total_business_cost,
    b.num_stockouts,
    b.num_excess_inventory,
    b.avg_stockout_units,
    b.avg_excess_units,
    -- Business cost per prediction
    b.total_business_cost / b.total_predictions AS avg_cost_per_prediction,
    -- Rank by business cost (most important)
    RANK() OVER (ORDER BY b.total_business_cost ASC) AS business_cost_rank,
    -- Rank by statistical RMSE (for comparison)
    RANK() OVER (ORDER BY s.RMSE ASC) AS rmse_rank
FROM model_statistical_evaluation s
INNER JOIN model_business_cost_analysis b ON s.model_name = b.model_name
ORDER BY b.total_business_cost ASC;

-- Step 4: Sensitivity analysis - what if stockout cost was $75 instead of $50?
SELECT
    model_name,
    total_business_cost AS base_case_cost,
    -- Recalculate with higher stockout cost
    SUM(CASE
        WHEN actual_demand_units > predicted_demand_units
        THEN (actual_demand_units - predicted_demand_units) * 75  -- Increased to $75
        ELSE (predicted_demand_units - actual_demand_units) * 10
    END) AS high_stockout_cost_scenario,
    -- Cost increase
    (high_stockout_cost_scenario - base_case_cost) AS cost_increase,
    ROUND(100.0 * (high_stockout_cost_scenario - base_case_cost) / base_case_cost, 2) AS pct_increase
FROM model_business_cost_analysis
ORDER BY high_stockout_cost_scenario;
```

**Sample Output:**
```
-- Combined statistical and business evaluation:
model_name | num_features | MAE   | RMSE  | R2    | statistical_bias | total_stockout_cost | total_excess_cost | total_business_cost | num_stockouts | num_excess_inventory | avg_cost_per_prediction | business_cost_rank | rmse_rank
-----------+--------------+-------+-------+-------+------------------+---------------------+-------------------+---------------------+---------------+----------------------+-------------------------+--------------------+-----------
Prophet    | 15           | 45.67 | 67.89 | 0.876 | +8.34            | $156,750            | $34,230           | $190,980            | 3,135         | 3,423                | $36.65                  | 1                  | 2
XGBoost    | 25           | 38.23 | 58.45 | 0.912 | -5.67            | $198,450            | $28,140           | $226,590            | 3,969         | 2,814                | $43.48                  | 2                  | 1  ← Best RMSE
ARIMA      | 10           | 52.34 | 78.12 | 0.845 | -12.45           | $267,890            | $41,250           | $309,140            | 5,358         | 4,125                | $59.30                  | 3                  | 3

-- Detailed business cost breakdown:
model_name | avg_stockout_units | avg_excess_units | stockout_frequency | excess_frequency
-----------+--------------------+------------------+--------------------+------------------
Prophet    | 50.0               | 10.0             | 47.8%              | 52.2%
XGBoost    | 50.0               | 10.0             | 58.5%              | 41.5%
ARIMA      | 50.0               | 10.0             | 56.5%              | 43.5%

-- Sensitivity analysis:
model_name | base_case_cost ($50) | high_stockout_cost ($75) | cost_increase | pct_increase
-----------+----------------------+--------------------------+---------------+--------------
Prophet    | $190,980             | $235,105                 | $44,125       | 23.1%
XGBoost    | $226,590             | $298,020                 | $71,430       | 31.5%
ARIMA      | $309,140             | $443,030                 | $133,890      | 43.3%
```

**Business Impact:**

**Key Finding: Statistical "Best" Model ≠ Business "Best" Model**
- **XGBoost has best RMSE** (58.45, rank #1) and R² (0.912) - statistically superior
- **Prophet has lowest business cost** ($190,980, rank #1) - business-optimal choice
- **Prophet saves $35,610 annually vs. XGBoost** ($226,590 - $190,980) despite worse statistical metrics

**Why Prophet Wins on Business Metrics:**
- **Bias Direction**: Prophet has +8.34 positive bias (slight over-prediction tendency)
  - Over-prediction costs only $10/unit (excess inventory)
  - Under-prediction costs $50/unit (stockouts) - 5x more expensive
- **XGBoost has negative bias** (-5.67) leading to more costly under-predictions
- **Prophet's error distribution** favors lower-cost errors (excess inventory) over higher-cost errors (stockouts)

**Business Cost Breakdown:**
- **Prophet**: 47.8% stockouts ($156,750) + 52.2% excess inventory ($34,230) = $190,980 total
- **XGBoost**: 58.5% stockouts ($198,450) + 41.5% excess inventory ($28,140) = $226,590 total
- XGBoost has 10.7% more stockouts (3,969 vs. 3,135) - drives higher total cost

**Cost Per Prediction:**
- Prophet: $36.65 per forecast
- XGBoost: $43.48 per forecast (+18.6% more expensive)
- ARIMA: $59.30 per forecast (worst option)

**Sensitivity Analysis Insights:**
- If stockout cost increases from $50 to $75 (50% increase):
  - Prophet cost increases by 23.1% (most resilient to stockout cost changes)
  - XGBoost cost increases by 31.5%
  - ARIMA cost increases by 43.3%
- Prophet's slight over-prediction bias becomes even more valuable as stockout costs rise

**Model Selection Decision:**
- **Deploy Prophet for production** despite lower R² (0.876 vs. 0.912)
- **Business justification**: Prophet saves $35,610 annually in operational costs
- **Additional benefits**:
  - 834 fewer stockouts per year (3,135 vs. 3,969) improves customer satisfaction
  - 609 more excess inventory instances (3,423 vs. 2,814) but at 5x lower cost
  - Better alignment with business risk tolerance (prefer slight overstock to stockouts)

**Strategic Insights:**
1. **Bias matters more than variance** when error costs are asymmetric
2. **Tune models for business objectives**, not just statistical metrics
3. **Prophet's domain knowledge** (trend + seasonality decomposition) naturally produces conservative forecasts
4. **XGBoost could be re-tuned** with asymmetric loss function to penalize under-predictions more heavily

**Long-term Monitoring:**
- Track business cost monthly alongside RMSE/R²
- Alert if business cost increases >10% month-over-month
- Quarterly review of error cost assumptions ($50 stockout, $10 excess)
- Re-evaluate model selection if market conditions change stockout costs

---

## Common Use Cases

### Model Development and Selection
- **Comparing regression algorithms**: Evaluate Linear Regression, Ridge, Lasso, Random Forest, XGBoost, Neural Networks
- **Hyperparameter tuning**: Compare models with different configurations to find optimal settings
- **Feature selection**: Assess impact of different feature sets using R² and Adjusted R²
- **Model validation**: Evaluate performance on held-out test sets before deployment
- **Cross-validation**: Compute metrics across multiple folds to assess stability

### Production Model Monitoring
- **Performance tracking**: Monitor metrics over time to detect model degradation
- **Drift detection**: Identify when model performance declines due to data drift
- **Alert triggers**: Set thresholds for RMSE, R², or bias to flag performance issues
- **Retraining decisions**: Use metric trends to determine when models need retraining
- **A/B testing**: Compare champion vs. challenger models in production

### Business Domain Applications
- **Sales forecasting**: Evaluate revenue, demand, and sales volume predictions
- **Financial modeling**: Assess credit risk, fraud amount, portfolio value predictions
- **Pricing optimization**: Validate dynamic pricing and price elasticity models
- **Customer analytics**: Evaluate CLV, churn revenue, and customer spending predictions
- **Supply chain**: Assess inventory, lead time, and demand forecasting accuracy
- **Real estate**: Validate property valuation and appraisal models
- **Healthcare**: Evaluate patient cost, length of stay, and treatment outcome predictions
- **Energy**: Assess load forecasting and consumption prediction models

### Statistical Analysis
- **Bias detection**: Use ME and MPE to identify systematic prediction errors
- **Heteroscedasticity check**: Analyze whether errors are consistent across prediction ranges
- **Outlier impact**: Assess how sensitive models are to extreme values
- **Residual analysis**: Evaluate whether prediction errors follow expected patterns
- **Confidence intervals**: Use RMSE to estimate prediction uncertainty ranges

### Stakeholder Communication
- **Model explanation**: Use R² to communicate predictive power to non-technical audiences
- **Business case**: Translate MAPE into business-relevant accuracy percentages
- **Risk assessment**: Use RMSE to quantify typical prediction errors in dollar terms
- **Benchmarking**: Compare model performance to business baselines or industry standards
- **ROI justification**: Demonstrate improvement over existing methods to justify ML investment

## Best Practices

### Metric Selection
1. **Use multiple complementary metrics**: No single metric tells the complete story
   - **RMSE**: Most common, penalizes large errors heavily
   - **MAE**: More robust to outliers than RMSE
   - **R²**: Interpretable measure of explanatory power
   - **MAPE**: Scale-independent, good for comparing across different targets
   - **ME/MPE**: Essential for detecting systematic bias

2. **Match metrics to business goals**:
   - Financial forecasting: MAPE (percentage accuracy is business-relevant)
   - Cost prediction: MAE and RMSE (dollar-based errors matter)
   - Model comparison: R² and Adjusted R² (relative explanatory power)
   - Production monitoring: RMSE, R², ME (comprehensive health check)

3. **Consider error cost asymmetry**: If under-prediction costs more than over-prediction (or vice versa), bias metrics (ME, MPE) are critical

4. **Use Adjusted R² when comparing models with different feature counts**: Prevents favoring more complex models due to overfitting

### Model Evaluation Strategy
1. **Always evaluate on held-out test data**: Never evaluate on training data (overly optimistic results)

2. **Stratify evaluation by important segments**:
   - Time periods (detect seasonal patterns)
   - Customer segments (identify where model fails)
   - Product categories (understand domain-specific performance)

3. **Compare against baselines**:
   - Naive baseline (e.g., previous year, simple average)
   - Business rule baseline (current heuristic method)
   - Simpler model baseline (e.g., Linear Regression)

4. **Check for bias systematically**:
   - ME should be close to 0 (no systematic over/under-prediction)
   - Plot residuals to detect patterns
   - Evaluate bias across different prediction ranges

### Statistical Rigor
1. **Always provide NumOfIndependentVariables** to get Adjusted R² and F-statistic

2. **Interpret R² cautiously**:
   - R² > 0.9: Excellent (but check for overfitting)
   - R² 0.7-0.9: Good
   - R² 0.5-0.7: Moderate
   - R² < 0.5: Weak (consider model redesign)

3. **RMSE interpretation**:
   - Express RMSE in business terms (e.g., "$1,234 typical error")
   - Compare RMSE to target variable's standard deviation
   - RMSE < 0.5 × std_dev indicates good model

4. **Use MAPE carefully**:
   - MAPE undefined when actual values = 0
   - MAPE asymmetric (penalizes over-predictions more than under-predictions)
   - Consider alternatives (SMAPE, WAPE) for zero-inflated targets

### Production Deployment
1. **Establish baseline metrics** before deployment:
   - Record initial test set performance
   - Set acceptable degradation thresholds (e.g., RMSE increase <15%)

2. **Monitor continuously**:
   - Weekly or monthly evaluation on recent predictions
   - Track trends in all key metrics
   - Alert when thresholds exceeded

3. **Plan retraining triggers**:
   - R² drops below threshold
   - RMSE increases beyond acceptable range
   - Bias emerges or grows (ME significantly non-zero)
   - Periodic retraining (e.g., quarterly) regardless of metrics

4. **Document evaluation results**:
   - Store evaluation metrics with model versioning
   - Track evaluation dates and data periods
   - Maintain audit trail for regulatory compliance

### Handling Special Cases
1. **Right-skewed targets** (prices, counts, revenue):
   - Use MSLE/RMSLE in addition to MSE/RMSE
   - Consider log transformation of target variable
   - MAPE may be more interpretable than RMSE

2. **Imbalanced prediction ranges**:
   - Evaluate separately for low, medium, high prediction ranges
   - Use weighted metrics if certain ranges more important

3. **Time series forecasts**:
   - Evaluate across multiple forecast horizons
   - Check for seasonal bias patterns
   - Use rolling window evaluation

4. **Small sample sizes**:
   - Be cautious interpreting R² (can be unreliable with n < 30)
   - Use cross-validation to get more stable estimates
   - Report confidence intervals if possible

### Model Comparison
1. **Use Adjusted R² instead of R²** when comparing models with different numbers of features

2. **Statistical significance testing**:
   - Use F-statistic to test if model significantly better than null model
   - Compare RMSE differences to determine if improvement is meaningful

3. **Consider complexity vs. performance trade-off**:
   - Simpler model with 95% of best model's R² may be preferable
   - Easier to maintain, explain, and deploy
   - Less prone to overfitting

4. **Business-oriented comparison**:
   - Translate metric differences into business impact
   - "$500 lower RMSE saves $2M annually in forecasting errors"
   - Consider operational costs of more complex models

## Related Functions

### Regression Model Training
- **TD_LinReg**: Train linear regression models
- **TD_GLM**: Generalized Linear Models (Gaussian family for regression)
- **TD_DecisionForest**: Train random forest regression models
- **TD_XGBoost**: Train gradient boosted regression models
- **TD_SVM**: Support Vector Machine regression
- **TD_PolynomialFeatures**: Create polynomial features for non-linear regression

### Model Scoring/Prediction
- **TD_LinRegPredict**: Score linear regression models
- **TD_GLMPredict**: Score GLM models
- **TD_DecisionForestPredict**: Score decision forest models
- **TD_XGBoostPredict**: Score XGBoost models
- **TD_SVMPredict**: Score SVM models

### Other Evaluation Functions
- **TD_ClassificationEvaluator**: Evaluate classification models (precision, recall, F1)
- **TD_ROC**: Generate ROC curves and compute AUC for binary classifiers
- **TD_SHAP**: Explain individual predictions and feature importance

### Data Preparation
- **TD_TrainTestSplit**: Split data into training and test sets for unbiased evaluation
- **TD_SimpleImputeFit / TD_SimpleImputeTransform**: Handle missing values before modeling
- **TD_ScaleFit / TD_ScaleTransform**: Normalize features for regression models
- **TD_OutlierFilterFit / TD_OutlierFilterTransform**: Remove outliers that may skew evaluation

### Statistical Analysis
- **TD_UnivariateStatistics**: Compute descriptive statistics for model inputs and outputs
- **TD_CorrelationAnalysis**: Analyze feature correlations to inform feature selection
- **TD_FTest**: Statistical significance testing for regression models

## Notes and Limitations

### Function Constraints
- **Non-NULL requirement**: Both ObservationColumn and PredictionColumn must not contain NULL values; rows with NULLs are excluded from evaluation
- **Matching scale**: Predictions must be on same scale as observations (don't compare log-transformed predictions to raw observations)
- **Minimum sample size**: At least 2 rows required, but 30+ recommended for reliable statistics
- **Adjusted R² requirement**: NumOfIndependentVariables must be provided, otherwise Adjusted R² returns NULL

### Metric-Specific Limitations
1. **MAPE limitations**:
   - Undefined when actual values equal zero
   - Asymmetric: penalizes over-predictions more than under-predictions
   - Problematic for targets with values near zero
   - Alternative: Use SMAPE (Symmetric MAPE) or WAPE (Weighted APE) externally

2. **R² limitations**:
   - Can be negative on out-of-sample data (indicates model worse than predicting mean)
   - Not comparable across different target variables
   - Can be artificially inflated with many features (use Adjusted R² instead)
   - Sensitive to outliers

3. **RMSE vs. MAE**:
   - RMSE more sensitive to outliers than MAE (squared errors)
   - RMSE penalizes large errors more heavily
   - MAE more intuitive and robust

4. **ME (Mean Error) interpretation**:
   - ME = 0 doesn't mean good model (could have offsetting positive and negative errors)
   - Always examine ME alongside MAE or RMSE

### Performance Considerations
- **Large datasets**: Function performs single-pass computation, efficient for millions of rows
- **PARTITION BY**: Use PARTITION BY for segment-wise evaluation without multiple queries
- **Metric computation**: If only specific metrics needed, use Metrics parameter to reduce computation time

### Statistical Assumptions
- **Independence**: Assumes prediction errors are independent (may not hold for time series)
- **Homoscedasticity**: Standard metrics assume constant error variance across prediction range
- **Normality**: R² and F-statistic interpretation assumes normally distributed errors
- **Linear relationship**: R² measures linear relationship between predicted and actual values

### Common Pitfalls
1. **Training data evaluation**: NEVER evaluate on training data - results will be overly optimistic
2. **Ignoring bias**: High R² doesn't mean unbiased predictions; always check ME/MPE
3. **Single metric focus**: Don't select models based solely on one metric (e.g., only R²)
4. **Scale confusion**: Ensure predictions and observations use same units and transformations
5. **Temporal leakage**: For time series, ensure test data is strictly after training data
6. **Feature count mismatch**: When using NumOfIndependentVariables, count should match actual features used in model training

### Business Context Requirements
- **Interpretation**: Always present metrics in business-relevant terms:
  - RMSE: "$1,234 typical error" rather than "1234.56"
  - MAPE: "forecasts within 8% accuracy" rather than "8.34% MAPE"
  - R²: "explains 85% of variance" rather than "0.85 R²"

- **Benchmarking**: Metrics meaningless without context:
  - Compare to baseline (naive forecast, business rule)
  - Compare to previous model version
  - Compare to industry standards or research benchmarks

- **Cost-benefit**: Statistical improvement must translate to business value:
  - "Reducing RMSE from $2,000 to $1,500 saves $500K annually in forecasting errors"

### Data Quality Considerations
- **Outliers**: Extreme values significantly impact RMSE (less impact on MAE)
- **Data drift**: Evaluation on recent data may differ from older data due to distribution shift
- **Sample bias**: Ensure test set representative of production data
- **Prediction range**: Model may perform differently at extremes (very high/low values)

### Regulatory and Compliance
- **Model validation**: TD_RegressionEvaluator outputs serve as model validation documentation
- **Audit trail**: Store evaluation results with timestamps, model versions, and data periods
- **Bias monitoring**: ME and MPE critical for detecting discriminatory patterns in regulated domains
- **Reproducibility**: Document NumOfIndependentVariables and evaluation parameters for reproducible results

### Version and Compatibility
- **Teradata Version**: Available in Teradata Vantage 17.20+
- **Alias support**: TD_REGRESSIONEVALUATOR (uppercase) is equivalent
- **Output format**: Returns single row with all metrics as separate columns
- **NULL handling**: Automatically excludes rows with NULL in observation or prediction columns

---

**Generated from Teradata Database Analytic Functions Version 17.20**
**Function Category**: Model Evaluation - Regression Metrics
**Last Updated**: November 29, 2025
