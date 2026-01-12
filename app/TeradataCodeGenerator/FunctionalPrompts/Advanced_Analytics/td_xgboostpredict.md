# TD_XGBoostPredict

## Function Name
**TD_XGBoostPredict** - XGBoost Gradient Boosting Prediction

**Aliases:** XGBoostPredict

## Description

TD_XGBoostPredict applies a trained XGBoost model to new data for classification or regression. XGBoost (eXtreme Gradient Boosting) is a highly optimized implementation of gradient boosted decision trees that has become the go-to algorithm for structured/tabular data in machine learning competitions and production systems. It builds an ensemble of decision trees sequentially, where each tree corrects errors made by previous trees, resulting in exceptional predictive accuracy.

**Key Characteristics:**
- **State-of-the-Art Accuracy**: Consistently wins Kaggle competitions and achieves top performance on tabular data
- **Classification & Regression**: Handles both classification (binary, multi-class) and regression tasks
- **Gradient Boosting**: Sequential ensemble learning where each tree improves on previous errors
- **Built-in Regularization**: L1 (Lasso) and L2 (Ridge) regularization prevent overfitting
- **Feature Importance**: Provides interpretable feature importance scores
- **Missing Value Handling**: Native support for missing data (learns optimal handling)
- **Production-Ready**: Fast prediction, handles large-scale datasets efficiently

The function takes a trained XGBoost model (from TD_XGBoost) and generates predictions for new observations with optional probability estimates.

## When to Use TD_XGBoostPredict

**Business Applications:**
- **Credit Scoring**: Predict loan default with highest accuracy
- **Customer Churn Prediction**: Identify at-risk customers for retention
- **Fraud Detection**: Classify fraudulent transactions with low false positives
- **Demand Forecasting**: Predict product demand for inventory optimization
- **Click-Through Rate (CTR) Prediction**: Ad targeting and bidding optimization
- **Medical Diagnosis**: Disease prediction from clinical and lab data
- **Price Optimization**: Predict optimal pricing for maximum revenue
- **Predictive Maintenance**: Forecast equipment failure with lead time

**Use TD_XGBoostPredict When You Need To:**
- Apply a trained XGBoost model to new observations
- Score test data for model evaluation
- Deploy highest-accuracy predictions in production
- Handle complex non-linear relationships and interactions
- Work with mixed data types (numeric, categorical, missing values)
- Obtain feature importance for interpretability

**Analytical Use Cases:**
- Model validation on hold-out test sets
- Real-time scoring in production pipelines
- A/B testing for model comparison
- Risk scoring and stratification
- Personalized recommendations

## Syntax

```sql
SELECT * FROM TD_XGBoostPredict (
    ON { table | view | (query) } AS InputTable PARTITION BY ANY
    ON { table | view | (query) } AS ModelTable DIMENSION
    USING
    IDColumn ('id_column')
    [ Accumulate ('column' [,...]) ]
    [ OutputProb ({ 'true' | 'false' }) ]
    [ Responses ('response_value' [,...]) ]
    [ Detailed ({ 'true' | 'false' }) ]
) AS dt;
```

## Required Elements

### InputTable (PARTITION BY ANY)
The table containing data to score. Must include:
- All feature columns used during model training (same names and types)
- ID column for row identification
- Numeric and/or categorical features

### ModelTable (DIMENSION)
The trained XGBoost model table produced by TD_XGBoost function. Contains:
- Ensemble of boosted decision trees
- Tree structures (splits, thresholds)
- Model hyperparameters (learning rate, max depth, etc.)
- Feature metadata

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
Accumulate('customer_id', 'customer_name', 'transaction_date')
```

### OutputProb
**For Classification Only**: Whether to output predicted probabilities for each class.

**Values:**
- `'true'`: Include probability columns (prob_class1, prob_class2, etc.)
- `'false'`: Output only predicted class (default)

**Syntax:** `OutputProb('true')`

**Example:**
```sql
OutputProb('true')
```

### Responses
**For Classification Only**: Specifies the class labels in the order corresponding to probability columns when OutputProb is true.

**Syntax:** `Responses('class1', 'class2', ...)`

**Example:**
```sql
Responses('no_churn', 'churn')  -- For binary classification
Responses('low', 'medium', 'high')  -- For multi-class
```

### Detailed
**For Regression Only**: Whether to output detailed prediction information including variance estimates.

**Values:**
- `'true'`: Include detailed prediction metrics
- `'false'`: Output only predicted value (default)

**Syntax:** `Detailed('true')`

**Example:**
```sql
Detailed('true')
```

## Input Schema

### InputTable
| Column | Data Type | Description |
|--------|-----------|-------------|
| id_column | INTEGER, VARCHAR | Unique identifier for each row |
| feature_1 | NUMERIC/CATEGORICAL | First feature (same as training) |
| feature_2 | NUMERIC/CATEGORICAL | Second feature (same as training) |
| ... | NUMERIC/CATEGORICAL | Additional features (must match training) |
| accumulate_cols | ANY | Optional columns to pass through |

**Requirements:**
- All feature columns from training must be present
- Column names must match training data exactly
- Can include both numeric and categorical features
- NULL values are handled automatically (XGBoost learns optimal imputation)

### ModelTable
Standard output from TD_XGBoost function containing:
- Boosted tree ensemble
- Tree splits and thresholds
- Leaf values
- Hyperparameters (learning rate, max_depth, etc.)
- Feature metadata

## Output Schema

### Classification Output (OutputProb = 'false')
| Column | Data Type | Description |
|--------|-----------|-------------|
| id_column | Same as input | Row identifier from InputTable |
| prediction | VARCHAR/INTEGER | Predicted class label |
| accumulate_cols | Same as input | Pass-through columns if specified |

### Classification Output (OutputProb = 'true')
| Column | Data Type | Description |
|--------|-----------|-------------|
| id_column | Same as input | Row identifier from InputTable |
| prediction | VARCHAR/INTEGER | Predicted class label |
| prob_class1 | DOUBLE PRECISION | Probability of first class |
| prob_class2 | DOUBLE PRECISION | Probability of second class |
| ... | DOUBLE PRECISION | Additional probabilities (multi-class) |
| accumulate_cols | Same as input | Pass-through columns if specified |

### Regression Output
| Column | Data Type | Description |
|--------|-----------|-------------|
| id_column | Same as input | Row identifier from InputTable |
| prediction | DOUBLE PRECISION | Predicted continuous value |
| accumulate_cols | Same as input | Pass-through columns if specified |

**Notes:**
- For classification, probabilities sum to 1.0 across all classes
- Prediction is class with maximum probability for classification
- Regression predictions are continuous numeric values

## Code Examples

### Example 1: Customer Churn Prediction - Basic Binary Classification

**Business Context:** A subscription service has trained an XGBoost model to predict customer churn. Score active customers to identify retention targets.

```sql
-- Train XGBoost churn model
CREATE TABLE churn_xgb_model AS (
    SELECT * FROM TD_XGBoost (
        ON customer_training AS InputTable
        USING
        InputColumns ('months_subscribed', 'support_tickets', 'usage_last_30days',
                      'payment_failures', 'feature_usage_score', 'competitor_views')
        ResponseColumn ('churned')
        LearningRate (0.1)
        MaxDepth (6)
        NumTrees (100)
        Objective ('binary:logistic')
    ) AS dt
) WITH DATA;

-- Score active customers
SELECT * FROM TD_XGBoostPredict (
    ON active_customers AS InputTable PARTITION BY ANY
    ON churn_xgb_model AS ModelTable DIMENSION
    USING
    IDColumn ('customer_id')
    Accumulate ('customer_name', 'subscription_value', 'tenure_months')
) AS dt
ORDER BY customer_id;

/*
Sample Output:
customer_id | prediction | customer_name      | subscription_value | tenure_months
------------|------------|--------------------|--------------------|--------------
C10001      | no_churn   | John Smith         | 1200.00            | 24
C10002      | churn      | Jane Doe           | 850.00             | 8
C10003      | no_churn   | Robert Johnson     | 2400.00            | 36
C10004      | churn      | Maria Garcia       | 480.00             | 6

Interpretation:
- C10001, C10003: No churn predicted → Standard nurture campaign
- C10002, C10004: Churn predicted → Immediate retention intervention
*/

-- Business Impact:
-- Churn prediction accuracy: 94% (vs 87% with logistic regression)
-- Early identification enables proactive retention
```

### Example 2: Churn with Probability Scores for Targeted Retention

**Business Context:** Use churn probabilities to create tiered retention campaigns based on risk and customer value.

```sql
-- Score customers with churn probabilities
SELECT * FROM TD_XGBoostPredict (
    ON active_customers AS InputTable PARTITION BY ANY
    ON churn_xgb_model AS ModelTable DIMENSION
    USING
    IDColumn ('customer_id')
    OutputProb ('true')
    Responses ('no_churn', 'churn')
    Accumulate ('customer_name', 'subscription_value', 'tenure_months')
) AS dt
ORDER BY prob_churn DESC;  -- Highest risk first

/*
Sample Output:
customer_id | prediction | prob_no_churn | prob_churn | customer_name      | subscription_value | tenure_months
------------|------------|---------------|------------|--------------------|--------------------|--------------
C78901      | churn      | 0.08          | 0.92       | John Anderson      | 3600.00            | 18
C45612      | churn      | 0.18          | 0.82       | Mary Johnson       | 2400.00            | 12
C12345      | churn      | 0.48          | 0.52       | David Lee          | 1200.00            | 9
C23456      | no_churn   | 0.85          | 0.15       | Sarah Kim          | 1800.00            | 36

Interpretation:
- C78901: 92% churn risk, high value → CEO call, custom retention package
- C45612: 82% churn risk, high value → Account manager intervention
- C12345: 52% churn risk, moderate value → Automated discount offer
- C23456: 15% churn risk → Standard customer journey
*/

-- Create value-weighted retention campaigns
CREATE TABLE retention_strategy AS (
    SELECT
        customer_id,
        customer_name,
        subscription_value,
        prob_churn,
        subscription_value * prob_churn AS risk_weighted_value,
        CASE
            WHEN prob_churn >= 0.80 AND subscription_value >= 2000 THEN 'VIP_INTERVENTION'
            WHEN prob_churn >= 0.70 THEN 'HIGH_TOUCH_RETENTION'
            WHEN prob_churn >= 0.50 THEN 'AUTOMATED_DISCOUNT'
            WHEN prob_churn >= 0.30 THEN 'ENGAGEMENT_CAMPAIGN'
            ELSE 'STANDARD_NURTURE'
        END AS campaign_type,
        CASE
            WHEN prob_churn >= 0.80 AND subscription_value >= 2000 THEN subscription_value * 0.20
            WHEN prob_churn >= 0.70 THEN subscription_value * 0.15
            WHEN prob_churn >= 0.50 THEN subscription_value * 0.10
            ELSE 0
        END AS max_retention_spend
    FROM TD_XGBoostPredict (
        ON active_customers AS InputTable PARTITION BY ANY
        ON churn_xgb_model AS ModelTable DIMENSION
        USING
        IDColumn ('customer_id')
        OutputProb ('true')
        Responses ('no_churn', 'churn')
        Accumulate ('customer_name', 'subscription_value')
    ) AS dt
) WITH DATA
ORDER BY risk_weighted_value DESC;

-- Business Impact:
-- Churn rate reduced from 22% to 14% through targeted retention
-- Retention campaign ROI: 5.8x (saved $4.2M annual recurring revenue)
-- Focused budget on high-value at-risk customers
```

### Example 3: Credit Default Prediction with Multi-Class Risk Tiers

**Business Context:** Classify loan applicants into risk tiers (low, medium, high) for differentiated pricing and terms.

```sql
-- Train multi-class risk model
CREATE TABLE credit_risk_xgb_model AS (
    SELECT * FROM TD_XGBoost (
        ON loan_applications AS InputTable
        USING
        InputColumns ('income', 'debt_to_income', 'credit_score', 'employment_years',
                      'age', 'num_credit_accounts', 'prior_defaults')
        ResponseColumn ('risk_tier')
        LearningRate (0.05)
        MaxDepth (5)
        NumTrees (150)
        Objective ('multi:softprob')  -- Multi-class classification
    ) AS dt
) WITH DATA;

-- Classify new applicants
SELECT * FROM TD_XGBoostPredict (
    ON new_applicants AS InputTable PARTITION BY ANY
    ON credit_risk_xgb_model AS ModelTable DIMENSION
    USING
    IDColumn ('application_id')
    OutputProb ('true')
    Responses ('low_risk', 'medium_risk', 'high_risk')
    Accumulate ('applicant_name', 'requested_amount', 'credit_score')
) AS dt
ORDER BY application_id;

/*
Sample Output:
application_id | prediction   | prob_low | prob_medium | prob_high | applicant_name  | requested_amount | credit_score
---------------|--------------|----------|-------------|-----------|-----------------|------------------|-------------
APP10001       | low_risk     | 0.78     | 0.18        | 0.04      | John Smith      | 250000           | 780
APP10002       | high_risk    | 0.12     | 0.25        | 0.63      | Jane Doe        | 180000           | 580
APP10003       | low_risk     | 0.82     | 0.15        | 0.03      | Robert Johnson  | 320000           | 820
APP10004       | medium_risk  | 0.28     | 0.58        | 0.14      | Maria Garcia    | 150000           | 650

Interpretation:
- APP10001, APP10003: Low risk → Prime rate, standard terms
- APP10004: Medium risk → Standard rate + 1.5%, require MI if LTV > 80%
- APP10002: High risk → Decline or subprime rate + 4%, low LTV required
*/

-- Create pricing and terms based on risk
CREATE TABLE loan_offers AS (
    SELECT
        application_id,
        applicant_name,
        requested_amount,
        prediction AS risk_tier,
        CASE
            WHEN prediction = 'low_risk' THEN 4.25
            WHEN prediction = 'medium_risk' THEN 5.75
            WHEN prediction = 'high_risk' THEN 8.50
        END AS interest_rate,
        CASE
            WHEN prediction = 'low_risk' THEN 0.95
            WHEN prediction = 'medium_risk' THEN 0.85
            WHEN prediction = 'high_risk' THEN 0.70
        END AS max_ltv,
        CASE
            WHEN prediction = 'low_risk' THEN 'Approved - Prime Terms'
            WHEN prediction = 'medium_risk' THEN 'Approved - Standard Terms'
            WHEN prediction = 'high_risk' AND prob_high < 0.75 THEN 'Conditional Approval'
            ELSE 'Declined'
        END AS decision
    FROM TD_XGBoostPredict (
        ON new_applicants AS InputTable PARTITION BY ANY
        ON credit_risk_xgb_model AS ModelTable DIMENSION
        USING
        IDColumn ('application_id')
        OutputProb ('true')
        Responses ('low_risk', 'medium_risk', 'high_risk')
        Accumulate ('applicant_name', 'requested_amount')
    ) AS dt
) WITH DATA;

-- Business Impact:
-- Default rate reduced by 38% compared to rule-based underwriting
-- Approval rate for low-risk borrowers increased 15%
-- Risk-based pricing optimized for profitability
```

### Example 4: Demand Forecasting (Regression)

**Business Context:** Predict product demand for inventory optimization using XGBoost regression.

```sql
-- Train demand forecasting model
CREATE TABLE demand_xgb_model AS (
    SELECT * FROM TD_XGBoost (
        ON product_demand_history AS InputTable
        USING
        InputColumns ('day_of_week', 'month', 'is_holiday', 'temperature',
                      'promotion_active', 'price', 'competitor_price_diff',
                      'lag_7_day_sales', 'lag_30_day_avg')
        ResponseColumn ('daily_units_sold')
        LearningRate (0.05)
        MaxDepth (6)
        NumTrees (200)
        Objective ('reg:squarederror')  -- Regression
    ) AS dt
) WITH DATA;

-- Forecast demand for next 30 days
SELECT * FROM TD_XGBoostPredict (
    ON forecast_features AS InputTable PARTITION BY ANY
    ON demand_xgb_model AS ModelTable DIMENSION
    USING
    IDColumn ('forecast_date')
    Accumulate ('product_name', 'promotion_planned', 'current_inventory')
) AS dt
ORDER BY forecast_date;

/*
Sample Output:
forecast_date | prediction | product_name          | promotion_planned | current_inventory
--------------|------------|-----------------------|-------------------|------------------
2024-02-01    | 1847       | Widget A              | Yes               | 3500
2024-02-02    | 2156       | Widget A              | Yes               | 3500
2024-02-03    | 1245       | Widget A              | No                | 1653
2024-02-04    | 1108       | Widget A              | No                | 408

Interpretation:
- 2024-02-01-02: High demand (promotion) → Inventory sufficient for 1.5 days
- 2024-02-03-04: Normal demand → Reorder needed before 2024-02-04
*/

-- Create inventory recommendations
CREATE TABLE inventory_plan AS (
    SELECT
        forecast_date,
        product_name,
        current_inventory,
        prediction AS forecasted_demand,
        current_inventory - SUM(prediction) OVER (
            PARTITION BY product_name
            ORDER BY forecast_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS projected_inventory,
        CASE
            WHEN current_inventory - SUM(prediction) OVER (
                PARTITION BY product_name
                ORDER BY forecast_date
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) < prediction * 2 THEN 'REORDER_NOW'
            WHEN current_inventory - SUM(prediction) OVER (
                PARTITION BY product_name
                ORDER BY forecast_date
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) < prediction * 5 THEN 'SCHEDULE_REORDER'
            ELSE 'STOCK_ADEQUATE'
        END AS inventory_action
    FROM TD_XGBoostPredict (
        ON forecast_features AS InputTable PARTITION BY ANY
        ON demand_xgb_model AS ModelTable DIMENSION
        USING
        IDColumn ('forecast_date')
        Accumulate ('product_name', 'current_inventory')
    ) AS dt
) WITH DATA;

-- Business Impact:
-- Forecast accuracy improved to 96% (MAPE: 4%)
-- Stockouts reduced by 68%
-- Inventory carrying costs reduced by $1.2M annually
```

### Example 5: Click-Through Rate Prediction for Ad Targeting

**Business Context:** Predict ad CTR for real-time bidding and targeting optimization.

```sql
-- Train CTR prediction model
CREATE TABLE ctr_xgb_model AS (
    SELECT * FROM TD_XGBoost (
        ON ad_impressions_training AS InputTable
        USING
        InputColumns ('user_age_group', 'user_gender', 'device_type', 'hour_of_day',
                      'ad_position', 'ad_format', 'site_category', 'historical_ctr')
        ResponseColumn ('clicked')
        LearningRate (0.1)
        MaxDepth (4)
        NumTrees (100)
        Objective ('binary:logistic')
    ) AS dt
) WITH DATA;

-- Score ad opportunities in real-time
SELECT * FROM TD_XGBoostPredict (
    ON ad_opportunities AS InputTable PARTITION BY ANY
    ON ctr_xgb_model AS ModelTable DIMENSION
    USING
    IDColumn ('opportunity_id')
    OutputProb ('true')
    Responses ('no_click', 'click')
    Accumulate ('user_id', 'ad_id', 'max_bid', 'timestamp')
) AS dt
ORDER BY prob_click DESC;

/*
Sample Output:
opportunity_id | prediction | prob_no_click | prob_click | user_id | ad_id  | max_bid | timestamp
---------------|------------|---------------|------------|---------|--------|---------|------------------
OPP5012        | click      | 0.22          | 0.78       | U78901  | AD4521 | 2.50    | 2024-01-15 14:22
OPP5089        | click      | 0.35          | 0.65       | U45612  | AD1234 | 1.80    | 2024-01-15 14:22
OPP5045        | no_click   | 0.72          | 0.28       | U12345  | AD9876 | 1.20    | 2024-01-15 14:22
OPP5101        | no_click   | 0.88          | 0.12       | U23456  | AD5678 | 0.80    | 2024-01-15 14:22

Interpretation:
- OPP5012: 78% CTR → Bid aggressively (up to $2.50)
- OPP5089: 65% CTR → Standard bid ($1.80)
- OPP5045: 28% CTR → Low bid ($0.40)
- OPP5101: 12% CTR → Pass on opportunity
*/

-- Create dynamic bidding strategy
CREATE TABLE ad_bids AS (
    SELECT
        opportunity_id,
        user_id,
        ad_id,
        prob_click AS predicted_ctr,
        max_bid,
        CASE
            WHEN prob_click >= 0.70 THEN max_bid * 1.0
            WHEN prob_click >= 0.50 THEN max_bid * 0.75
            WHEN prob_click >= 0.30 THEN max_bid * 0.40
            WHEN prob_click >= 0.15 THEN max_bid * 0.20
            ELSE 0
        END AS calculated_bid,
        prob_click * 5.00 AS expected_revenue,  -- $5 conversion value
        prob_click * 5.00 - (max_bid * 0.75) AS expected_profit
    FROM TD_XGBoostPredict (
        ON ad_opportunities AS InputTable PARTITION BY ANY
        ON ctr_xgb_model AS ModelTable DIMENSION
        USING
        IDColumn ('opportunity_id')
        OutputProb ('true')
        Responses ('no_click', 'click')
        Accumulate ('user_id', 'ad_id', 'max_bid')
    ) AS dt
    WHERE prob_click * 5.00 > (max_bid * 0.75)  -- Only bid if profitable
) WITH DATA;

-- Business Impact:
-- CTR prediction accuracy: 89%
-- Ad spend ROI improved by 3.4x through better targeting
-- Cost per acquisition reduced by 42%
```

### Example 6: Medical Diagnosis with Feature Importance

**Business Context:** Predict disease presence and understand which clinical features drive the prediction.

```sql
-- Train diagnostic model
CREATE TABLE diagnosis_xgb_model AS (
    SELECT * FROM TD_XGBoost (
        ON patient_training AS InputTable
        USING
        InputColumns ('age', 'bmi', 'blood_pressure', 'glucose', 'cholesterol',
                      'family_history', 'smoking', 'exercise_frequency')
        ResponseColumn ('disease_present')
        LearningRate (0.05)
        MaxDepth (4)
        NumTrees (150)
        Objective ('binary:logistic')
        FeatureImportance ('true')  -- Calculate feature importance
    ) AS dt
) WITH DATA;

-- Classify new patients
SELECT * FROM TD_XGBoostPredict (
    ON new_patients AS InputTable PARTITION BY ANY
    ON diagnosis_xgb_model AS ModelTable DIMENSION
    USING
    IDColumn ('patient_id')
    OutputProb ('true')
    Responses ('healthy', 'disease')
    Accumulate ('patient_name', 'age', 'primary_care_physician')
) AS dt
ORDER BY prob_disease DESC;

/*
Sample Output:
patient_id | prediction | prob_healthy | prob_disease | patient_name    | age | primary_care_physician
-----------|------------|--------------|--------------|-----------------|-----|----------------------
PT5012     | disease    | 0.12         | 0.88         | John Anderson   | 58  | Dr. Smith
PT5089     | disease    | 0.28         | 0.72         | Mary Johnson    | 62  | Dr. Chen
PT5045     | healthy    | 0.78         | 0.22         | David Lee       | 45  | Dr. Garcia
PT5101     | healthy    | 0.92         | 0.08         | Sarah Kim       | 38  | Dr. Brown

Interpretation:
- PT5012: 88% disease probability → Urgent diagnostic workup
- PT5089: 72% disease probability → Schedule specialized testing
- PT5045: 22% disease probability → Lifestyle counseling, 6-month follow-up
- PT5101: 8% disease probability → Annual screening
*/

-- Create clinical action plan
CREATE TABLE clinical_pathways AS (
    SELECT
        patient_id,
        patient_name,
        age,
        prob_disease,
        CASE
            WHEN prob_disease >= 0.80 THEN 'IMMEDIATE_SPECIALIST_REFERRAL'
            WHEN prob_disease >= 0.60 THEN 'DIAGNOSTIC_WORKUP'
            WHEN prob_disease >= 0.40 THEN 'ENHANCED_MONITORING'
            WHEN prob_disease >= 0.20 THEN 'LIFESTYLE_INTERVENTION'
            ELSE 'ROUTINE_SCREENING'
        END AS clinical_pathway,
        CASE
            WHEN prob_disease >= 0.80 THEN 'Within 1 week'
            WHEN prob_disease >= 0.60 THEN 'Within 1 month'
            WHEN prob_disease >= 0.40 THEN 'Within 3 months'
            WHEN prob_disease >= 0.20 THEN 'Within 6 months'
            ELSE 'Annual visit'
        END AS follow_up_timeline
    FROM TD_XGBoostPredict (
        ON new_patients AS InputTable PARTITION BY ANY
        ON diagnosis_xgb_model AS ModelTable DIMENSION
        USING
        IDColumn ('patient_id')
        OutputProb ('true')
        Responses ('healthy', 'disease')
        Accumulate ('patient_name', 'age')
    ) AS dt
) WITH DATA;

-- Business Impact:
-- Early disease detection rate improved by 41%
-- Diagnostic accuracy: 93% (vs. 85% with logistic regression)
-- IMPORTANT: Model assists physicians, does not replace clinical judgment
```

## Common Use Cases

### Customer Analytics
- **Churn Prediction**: Identify at-risk customers for retention (highest accuracy)
- **Customer Lifetime Value**: Predict future value for resource allocation
- **Purchase Propensity**: Score leads for likelihood of purchase
- **Next Best Action**: Predict optimal product/offer for each customer

### Credit Risk and Financial Services
- **Default Prediction**: Loan default classification
- **Credit Scoring**: Risk-based pricing and approval
- **Fraud Detection**: Transaction fraud classification
- **Financial Forecasting**: Revenue, cash flow predictions

### Healthcare and Life Sciences
- **Disease Diagnosis**: Patient risk stratification
- **Readmission Prediction**: Hospital readmission forecasting
- **Treatment Response**: Predict which patients will respond to treatment
- **Drug Discovery**: Predict compound efficacy

### E-commerce and Retail
- **Demand Forecasting**: Inventory optimization
- **Price Optimization**: Revenue maximization
- **Product Recommendations**: Personalized recommendations
- **Click-Through Rate**: Ad targeting and bidding

### Manufacturing and Operations
- **Predictive Maintenance**: Equipment failure prediction
- **Quality Prediction**: Defect detection before inspection
- **Process Optimization**: Yield optimization
- **Supply Chain**: Delivery time and logistics optimization

## Best Practices

### Model Training and Selection
1. **Hyperparameter Tuning**: Use grid search or Bayesian optimization for learning_rate, max_depth, num_trees
2. **Early Stopping**: Monitor validation loss to prevent overfitting
3. **Regularization**: Use L1/L2 regularization (alpha, lambda) for complex models
4. **Feature Engineering**: XGBoost benefits from engineered features (interactions, polynomials)

### Prediction
1. **Feature Consistency**: Ensure test data has identical features as training
2. **Missing Values**: XGBoost handles NULLs automatically, no imputation needed
3. **Categorical Encoding**: Use label encoding or one-hot encoding (XGBoost handles both)
4. **Probability Calibration**: XGBoost probabilities are generally well-calibrated

### Performance Optimization
1. **Batch Scoring**: Use PARTITION BY ANY for parallel processing
2. **Model Pruning**: Remove low-importance features to reduce model size
3. **Tree Depth**: Limit max_depth to reduce prediction time
4. **Early Stopping**: Fewer trees = faster prediction

### Production Deployment
1. **Model Versioning**: Track model versions with hyperparameters and training date
2. **A/B Testing**: Compare XGBoost vs existing models before full deployment
3. **Monitoring**: Track prediction distribution, feature drift, and business metrics
4. **Retraining Schedule**: Retrain monthly or quarterly as patterns evolve

### Interpretability
1. **Feature Importance**: Use built-in feature importance for model interpretation
2. **SHAP Values**: Calculate SHAP for individual prediction explanations
3. **Partial Dependence**: Understand feature effects on predictions
4. **Tree Visualization**: Inspect individual trees for transparency

## Related Functions

### Model Training
- **TD_XGBoost**: Train XGBoost models (produces ModelTable input)
- **TD_XGBoostCV**: Cross-validation for hyperparameter tuning

### Alternative Algorithms
- **TD_DecisionForest**: Random forests for interpretability
- **TD_GLM**: Logistic/linear regression for speed and simplicity
- **TD_SVM**: Support vector machines for small to medium datasets
- **TD_NaiveBayes**: Fast probabilistic classifier for text/categorical data

### Model Evaluation
- **TD_ClassificationEvaluator**: Evaluate classification performance with confusion matrix
- **TD_RegressionEvaluator**: Evaluate regression metrics (RMSE, MAE, R²)
- **TD_ROC**: Generate ROC curves and calculate AUC
- **TD_SHAP**: Calculate SHAP values for feature importance and interpretability

### Data Preparation
- **TD_SimpleImputeFit/Transform**: Handle missing values (though XGBoost handles internally)
- **TD_ScaleFit/Transform**: Standardize features (optional for XGBoost)
- **TD_OneHotEncodingFit/Transform**: Encode categorical variables

### Feature Engineering
- **TD_PolynomialFeaturesFit/Transform**: Create interaction terms
- **TD_BincodeFit/Transform**: Bin continuous variables
- **TD_TargetEncodingFit/Transform**: Encode categorical variables based on target

## Notes and Limitations

### General Limitations
1. **Feature Matching**: All feature columns from training must be present in test data
2. **Black Box**: Less interpretable than linear models (use SHAP for explanations)
3. **Training Time**: Can be slow for very large datasets (though parallelizable)
4. **Overfitting Risk**: Requires careful tuning of learning_rate, max_depth, num_trees

### Model Characteristics
1. **Gradient Boosting**: Sequential ensemble where each tree corrects previous errors
2. **Tree-Based**: Naturally handles non-linear relationships and interactions
3. **Regularization**: Built-in L1/L2 regularization prevents overfitting
4. **Missing Values**: Native support (learns optimal direction at splits)

### Performance Considerations
1. **Training Time**: Longer than single models but faster than deep learning
2. **Prediction Speed**: Very fast (milliseconds per prediction)
3. **Memory**: Model size grows with num_trees and max_depth
4. **Scalability**: Efficient parallelization across AMPs

### Best Use Cases
- **When to Use XGBoost**: Need highest accuracy, tabular/structured data, moderate-to-large datasets, can afford training time
- **When to Avoid XGBoost**: Need real-time training, need full interpretability, very small datasets (<100 rows)
- **Alternatives**: Consider TD_DecisionForest for interpretability, TD_GLM for speed and simplicity

### Teradata-Specific Notes
1. **UTF8 Support**: ModelTable and InputTable support UTF8 character sets
2. **PARTITION BY ANY**: Enables parallel processing across AMPs
3. **DIMENSION Tables**: ModelTable must be DIMENSION for broadcast to all AMPs
4. **Deterministic**: Same input and model always produce same output

## Version Information

**Documentation Generated:** November 29, 2025
**Based on:** Teradata Database Analytic Functions Version 17.20
**Function Category:** Machine Learning - Model Scoring (Classification & Regression)
**Last Updated:** 2025-11-29
