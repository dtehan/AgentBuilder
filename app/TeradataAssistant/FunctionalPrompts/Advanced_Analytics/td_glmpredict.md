# TD_GLMPredict

## Function Name
**TD_GLMPredict** - Generalized Linear Model Prediction

**Aliases:** GLMPredict

## Description

TD_GLMPredict applies a trained Generalized Linear Model (GLM) to new data for prediction. GLM is a flexible framework that extends ordinary linear regression to response variables with non-normal error distributions through link functions. This function supports both classification (logistic regression, probit, complementary log-log) and regression (identity, log, inverse) tasks with multiple distribution families.

**Key Characteristics:**
- **Classification & Regression**: Supports binary classification, multi-class classification, and continuous regression
- **Multiple Link Functions**: Identity, log, inverse, logit, probit, complementary log-log (cloglog)
- **Distribution Families**: Gaussian, binomial, Poisson, gamma, inverse Gaussian
- **Probability Output**: Returns predicted probabilities for classification tasks
- **Linear Interpretability**: Model coefficients provide direct interpretation of feature importance
- **Production-Ready**: Optimized for batch scoring large datasets in-database

The function takes a trained GLM model (from TD_GLM) and applies it to test data, returning predictions based on the learned coefficients and intercept.

## When to Use TD_GLMPredict

**Business Applications:**
- **Credit Risk Scoring**: Predict loan default probability using logistic regression
- **Insurance Claim Prediction**: Estimate claim amounts using gamma regression
- **Customer Conversion**: Score leads for likelihood of conversion
- **Fraud Detection**: Calculate fraud probability based on transaction features
- **Sales Forecasting**: Predict sales volume using Poisson regression for count data
- **Healthcare Risk**: Predict patient readmission probability
- **Pricing Optimization**: Model price elasticity with log-link functions
- **Marketing Response**: Score customers for campaign response likelihood

**Use TD_GLMPredict When You Need To:**
- Apply a trained GLM model to new data
- Score test sets for model evaluation
- Perform batch predictions in production
- Generate probability scores for classification
- Obtain linear model predictions with interpretable coefficients
- Compare predictions across different link functions or families

**Analytical Use Cases:**
- Model validation on hold-out test sets
- A/B testing with propensity scores
- Risk stratification and segmentation
- Real-time or batch scoring pipelines
- Model monitoring and performance tracking

## Syntax

```sql
SELECT * FROM TD_GLMPredict (
    ON { table | view | (query) } AS InputTable PARTITION BY ANY
    ON { table | view | (query) } AS ModelTable DIMENSION
    USING
    IDColumn ('id_column')
    [ Accumulate ('column' [,...]) ]
    [ OutputProb ({ 'true' | 'false' }) ]
    [ Responses ('response_value' [,...]) ]
) AS dt;
```

## Required Elements

### InputTable (PARTITION BY ANY)
The table containing data to score. Must include:
- All predictor columns used during model training (same names and types)
- ID column for row identification

### ModelTable (DIMENSION)
The trained GLM model table produced by TD_GLM function. Contains:
- Model coefficients for each predictor
- Intercept term
- Link function and family information
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
Accumulate('customer_id', 'account_type', 'credit_score')
```

### OutputProb
**For Classification Only**: Whether to output predicted probabilities for each class.

**Values:**
- `'true'`: Include probability columns (prob_0, prob_1, etc.)
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
Responses('0', '1')  -- For binary classification
Responses('low', 'medium', 'high')  -- For multi-class
```

## Input Schema

### InputTable
| Column | Data Type | Description |
|--------|-----------|-------------|
| id_column | INTEGER, VARCHAR | Unique identifier for each row |
| predictor_1 | NUMERIC | First predictor variable (same as training) |
| predictor_2 | NUMERIC | Second predictor variable (same as training) |
| ... | NUMERIC | Additional predictors (must match training data) |
| accumulate_cols | ANY | Optional columns to pass through |

**Requirements:**
- All predictor columns from training must be present
- Column names must match training data exactly
- Numeric data types for predictors
- No NULL values in predictors (handle missing values before prediction)

### ModelTable
Standard output from TD_GLM function containing:
- Model coefficients
- Intercept
- Link function specification
- Distribution family
- Convergence information

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
| prob_0 | DOUBLE PRECISION | Probability of first response class |
| prob_1 | DOUBLE PRECISION | Probability of second response class |
| ... | DOUBLE PRECISION | Additional probabilities for multi-class |
| accumulate_cols | Same as input | Pass-through columns if specified |

### Regression Output
| Column | Data Type | Description |
|--------|-----------|-------------|
| id_column | Same as input | Row identifier from InputTable |
| prediction | DOUBLE PRECISION | Predicted continuous value |
| accumulate_cols | Same as input | Pass-through columns if specified |

**Notes:**
- For classification, probabilities sum to 1.0 across all classes
- Regression predictions are in the scale of the response variable (after inverse link transformation)
- Column order: ID, prediction, probabilities (if requested), accumulated columns

## Code Examples

### Example 1: Binary Classification - Credit Default Prediction (Basic)

**Business Context:** A bank has trained a logistic regression model to predict loan defaults. Score new loan applications to assess risk.

```sql
-- Train logistic regression model on historical data
CREATE TABLE credit_glm_model AS (
    SELECT * FROM TD_GLM (
        ON credit_training AS InputTable
        USING
        InputColumns ('income', 'debt_ratio', 'credit_score', 'age', 'employment_years')
        ResponseColumn ('default_flag')
        Family ('binomial')
        LinkFunction ('logit')
        Intercept ('true')
        MaxIterNum (100)
    ) AS dt
) WITH DATA;

-- Predict default probability on new applications
SELECT * FROM TD_GLMPredict (
    ON credit_test AS InputTable PARTITION BY ANY
    ON credit_glm_model AS ModelTable DIMENSION
    USING
    IDColumn ('application_id')
    Accumulate ('applicant_name', 'loan_amount', 'credit_score')
) AS dt
ORDER BY application_id;

/*
Sample Output:
application_id | prediction | applicant_name     | loan_amount | credit_score
---------------|------------|--------------------|-------------|-------------
10001          | 0          | John Smith         | 250000      | 720
10002          | 1          | Jane Doe           | 180000      | 580
10003          | 0          | Robert Johnson     | 320000      | 780
10004          | 1          | Maria Garcia       | 150000      | 610

Interpretation:
- application_id 10001, 10003: Predicted non-default (0) - approve loan
- application_id 10002, 10004: Predicted default (1) - reject or require additional review
- Accumulate columns provide business context for decision-making
*/

-- Business Impact:
-- Automated credit scoring reduces manual review time by 70%
-- Consistent risk assessment across all applications
```

### Example 2: Binary Classification with Probabilities - Fraud Detection

**Business Context:** Score transactions for fraud probability, enabling risk-based authentication thresholds.

```sql
-- Train fraud detection model
CREATE TABLE fraud_glm_model AS (
    SELECT * FROM TD_GLM (
        ON transaction_training AS InputTable
        USING
        InputColumns ('amount', 'merchant_category', 'distance_from_home',
                      'hour_of_day', 'card_age_days', 'transaction_velocity')
        ResponseColumn ('is_fraud')
        Family ('binomial')
        LinkFunction ('logit')
        Intercept ('true')
    ) AS dt
) WITH DATA;

-- Score new transactions with fraud probability
SELECT * FROM TD_GLMPredict (
    ON transaction_stream AS InputTable PARTITION BY ANY
    ON fraud_glm_model AS ModelTable DIMENSION
    USING
    IDColumn ('transaction_id')
    OutputProb ('true')
    Responses ('0', '1')
    Accumulate ('customer_id', 'amount', 'merchant_name', 'transaction_time')
) AS dt
ORDER BY prob_1 DESC;  -- Highest fraud probability first

/*
Sample Output:
transaction_id | prediction | prob_0 | prob_1 | customer_id | amount  | merchant_name    | transaction_time
---------------|------------|--------|--------|-------------|---------|------------------|------------------
TXN9945        | 1          | 0.08   | 0.92   | C12890      | 2850.00 | Electronics Hub  | 2024-01-15 03:22
TXN9823        | 1          | 0.15   | 0.85   | C45612      | 1980.00 | Online Retailer  | 2024-01-15 02:45
TXN9901        | 0          | 0.72   | 0.28   | C78234      | 156.50  | Local Grocery    | 2024-01-15 10:15
TXN9887        | 0          | 0.95   | 0.05   | C23456      | 42.30   | Coffee Shop      | 2024-01-15 08:30

Interpretation:
- TXN9945: 92% fraud probability → Block transaction, call customer
- TXN9823: 85% fraud probability → Flag for manual review
- TXN9901: 28% fraud probability → Allow with additional verification (e.g., SMS code)
- TXN9887: 5% fraud probability → Approve automatically
*/

-- Create risk-based routing
CREATE TABLE fraud_routing AS (
    SELECT
        transaction_id,
        customer_id,
        amount,
        prob_1 AS fraud_probability,
        CASE
            WHEN prob_1 >= 0.80 THEN 'BLOCK_AND_CALL'
            WHEN prob_1 >= 0.50 THEN 'MANUAL_REVIEW'
            WHEN prob_1 >= 0.20 THEN 'ADDITIONAL_AUTH'
            ELSE 'AUTO_APPROVE'
        END AS action
    FROM TD_GLMPredict (
        ON transaction_stream AS InputTable PARTITION BY ANY
        ON fraud_glm_model AS ModelTable DIMENSION
        USING
        IDColumn ('transaction_id')
        OutputProb ('true')
        Responses ('0', '1')
        Accumulate ('customer_id', 'amount')
    ) AS dt
) WITH DATA;

-- Business Impact:
-- Reduced fraud losses by $2.3M annually
-- False positive rate decreased by 40% compared to rule-based system
-- Customer friction reduced with risk-appropriate authentication
```

### Example 3: Regression - Insurance Claim Amount Prediction

**Business Context:** Predict expected claim amounts for reserving and pricing using gamma regression with log link (appropriate for positive, right-skewed data).

```sql
-- Train gamma regression model for claim amounts
CREATE TABLE claim_glm_model AS (
    SELECT * FROM TD_GLM (
        ON insurance_claims_training AS InputTable
        USING
        InputColumns ('age', 'vehicle_age', 'vehicle_value', 'area_risk_score',
                      'driver_experience_years', 'claims_last_3years')
        ResponseColumn ('claim_amount')
        Family ('gamma')
        LinkFunction ('log')
        Intercept ('true')
        MaxIterNum (150)
    ) AS dt
) WITH DATA;

-- Predict claim amounts for new policies
SELECT * FROM TD_GLMPredict (
    ON new_policies AS InputTable PARTITION BY ANY
    ON claim_glm_model AS ModelTable DIMENSION
    USING
    IDColumn ('policy_id')
    Accumulate ('customer_name', 'vehicle_make', 'vehicle_model', 'premium_amount')
) AS dt
ORDER BY prediction DESC;

/*
Sample Output:
policy_id | prediction | customer_name     | vehicle_make | vehicle_model | premium_amount
----------|------------|-------------------|--------------|---------------|---------------
POL8821   | 8750.50    | James Wilson      | BMW          | X5            | 2400.00
POL8834   | 6230.25    | Sarah Chen        | Mercedes     | E-Class       | 2100.00
POL8792   | 3420.80    | Michael Brown     | Toyota       | Camry         | 1200.00
POL8856   | 2180.40    | Emily Davis       | Honda        | Civic         | 950.00

Interpretation:
- POL8821: Expected claim amount $8,750 → High-risk policy, ensure adequate reserves
- POL8792: Expected claim amount $3,420 → Moderate risk, standard pricing
- POL8856: Expected claim amount $2,180 → Low risk, competitive pricing opportunity
*/

-- Calculate loss ratio and reserve requirements
CREATE TABLE policy_risk_analysis AS (
    SELECT
        policy_id,
        customer_name,
        premium_amount,
        prediction AS expected_claim_amount,
        ROUND(prediction / NULLIF(premium_amount, 0), 2) AS expected_loss_ratio,
        CASE
            WHEN prediction / NULLIF(premium_amount, 0) > 0.80 THEN 'HIGH_RISK'
            WHEN prediction / NULLIF(premium_amount, 0) > 0.60 THEN 'MEDIUM_RISK'
            ELSE 'LOW_RISK'
        END AS risk_category,
        ROUND(prediction * 1.15, 2) AS reserve_amount  -- 15% safety margin
    FROM TD_GLMPredict (
        ON new_policies AS InputTable PARTITION BY ANY
        ON claim_glm_model AS ModelTable DIMENSION
        USING
        IDColumn ('policy_id')
        Accumulate ('customer_name', 'premium_amount')
    ) AS dt
) WITH DATA;

-- Business Impact:
-- Improved reserve accuracy by 28%, reducing capital requirements
-- Identified underpriced policies with loss ratios > 0.80
-- Dynamic pricing based on expected claim amounts
```

### Example 4: Poisson Regression - Call Center Volume Prediction

**Business Context:** Predict daily call volumes for staffing optimization using Poisson regression (ideal for count data).

```sql
-- Train Poisson regression for call volume
CREATE TABLE call_volume_glm_model AS (
    SELECT * FROM TD_GLM (
        ON call_center_history AS InputTable
        USING
        InputColumns ('day_of_week', 'is_holiday', 'month', 'temperature',
                      'marketing_campaign_active', 'website_visitors')
        ResponseColumn ('call_count')
        Family ('poisson')
        LinkFunction ('log')
        Intercept ('true')
    ) AS dt
) WITH DATA;

-- Predict call volumes for next 30 days
SELECT * FROM TD_GLMPredict (
    ON call_center_forecast_features AS InputTable PARTITION BY ANY
    ON call_volume_glm_model AS ModelTable DIMENSION
    USING
    IDColumn ('forecast_date')
    Accumulate ('day_name', 'is_holiday', 'marketing_campaign_active')
) AS dt
ORDER BY forecast_date;

/*
Sample Output:
forecast_date | prediction | day_name  | is_holiday | marketing_campaign_active
--------------|------------|-----------|------------|---------------------------
2024-02-01    | 1847       | Thursday  | 0          | 1
2024-02-02    | 1923       | Friday    | 0          | 1
2024-02-03    | 1245       | Saturday  | 0          | 0
2024-02-04    | 1108       | Sunday    | 0          | 0
2024-02-05    | 2156       | Monday    | 0          | 1

Interpretation:
- 2024-02-01: 1,847 predicted calls → Schedule 28 agents (65 calls/agent)
- 2024-02-05: 2,156 predicted calls → Schedule 33 agents (Monday + campaign surge)
- Weekend: ~1,200 calls → Reduce weekend staffing
*/

-- Create staffing recommendations
CREATE TABLE staffing_plan AS (
    SELECT
        forecast_date,
        day_name,
        prediction AS predicted_calls,
        CEIL(prediction / 65.0) AS agents_needed,  -- 65 calls per agent target
        CEIL(prediction / 65.0) * 8 AS agent_hours,  -- 8-hour shifts
        CASE
            WHEN CEIL(prediction / 65.0) > 30 THEN 'ADD_OVERTIME'
            WHEN CEIL(prediction / 65.0) < 15 THEN 'REDUCE_SHIFTS'
            ELSE 'STANDARD_STAFFING'
        END AS staffing_action
    FROM TD_GLMPredict (
        ON call_center_forecast_features AS InputTable PARTITION BY ANY
        ON call_volume_glm_model AS ModelTable DIMENSION
        USING
        IDColumn ('forecast_date')
        Accumulate ('day_name', 'is_holiday')
    ) AS dt
) WITH DATA;

-- Business Impact:
-- Optimized staffing reduced labor costs by $450K annually
-- Service level (80% answered in 30 sec) improved from 72% to 88%
-- Eliminated overstaffing on low-volume days
```

### Example 5: Multi-Class Classification - Patient Risk Stratification

**Business Context:** Classify patients into low, medium, or high readmission risk categories for care management prioritization.

```sql
-- Train multi-class logistic regression
CREATE TABLE readmission_glm_model AS (
    SELECT * FROM TD_GLM (
        ON patient_history AS InputTable
        USING
        InputColumns ('age', 'num_chronic_conditions', 'num_medications',
                      'prior_admissions_12mo', 'length_of_stay', 'comorbidity_score')
        ResponseColumn ('risk_category')
        Family ('binomial')  -- Extends to multinomial for multi-class
        LinkFunction ('logit')
        Intercept ('true')
    ) AS dt
) WITH DATA;

-- Score discharged patients
SELECT * FROM TD_GLMPredict (
    ON discharged_patients AS InputTable PARTITION BY ANY
    ON readmission_glm_model AS ModelTable DIMENSION
    USING
    IDColumn ('patient_id')
    OutputProb ('true')
    Responses ('low', 'medium', 'high')
    Accumulate ('patient_name', 'discharge_date', 'primary_diagnosis')
) AS dt
ORDER BY prob_high DESC;

/*
Sample Output:
patient_id | prediction | prob_low | prob_medium | prob_high | patient_name   | discharge_date | primary_diagnosis
-----------|------------|----------|-------------|-----------|----------------|----------------|-------------------
PT4521     | high       | 0.05     | 0.22        | 0.73      | John Anderson  | 2024-01-10     | CHF
PT4598     | high       | 0.08     | 0.28        | 0.64      | Mary Thompson  | 2024-01-11     | COPD
PT4502     | medium     | 0.15     | 0.58        | 0.27      | David Lee      | 2024-01-10     | Pneumonia
PT4556     | low        | 0.82     | 0.14        | 0.04      | Sarah Kim      | 2024-01-11     | Minor Surgery

Interpretation:
- PT4521: 73% high-risk probability → Assign care manager, schedule 48-hour follow-up call
- PT4598: 64% high-risk probability → Home health visit within 7 days
- PT4502: 58% medium-risk probability → Telehealth check-in, medication review
- PT4556: 82% low-risk probability → Standard discharge instructions, no intervention
*/

-- Create care management assignments
CREATE TABLE care_management_queue AS (
    SELECT
        patient_id,
        patient_name,
        discharge_date,
        prediction AS risk_category,
        prob_high AS risk_score,
        CASE
            WHEN prob_high >= 0.60 THEN 'INTENSIVE_CASE_MANAGEMENT'
            WHEN prob_high >= 0.40 OR prob_medium >= 0.50 THEN 'STANDARD_FOLLOW_UP'
            ELSE 'AUTOMATED_OUTREACH'
        END AS care_program,
        CASE
            WHEN prob_high >= 0.60 THEN discharge_date + INTERVAL '2' DAY
            WHEN prob_high >= 0.40 THEN discharge_date + INTERVAL '5' DAY
            ELSE discharge_date + INTERVAL '10' DAY
        END AS contact_by_date
    FROM TD_GLMPredict (
        ON discharged_patients AS InputTable PARTITION BY ANY
        ON readmission_glm_model AS ModelTable DIMENSION
        USING
        IDColumn ('patient_id')
        OutputProb ('true')
        Responses ('low', 'medium', 'high')
        Accumulate ('patient_name', 'discharge_date', 'primary_diagnosis')
    ) AS dt
    WHERE prob_high >= 0.20  -- Focus resources on medium and high risk
) WITH DATA;

-- Business Impact:
-- 30-day readmission rate reduced from 18.5% to 13.2%
-- Care management resources focused on highest-risk patients
-- $1.8M annual savings from avoided readmission penalties
```

### Example 6: Probit Link - Market Research Analysis

**Business Context:** Model purchase probability using probit link (assumes normally distributed latent variable, common in econometrics).

```sql
-- Train probit model for purchase probability
CREATE TABLE purchase_glm_model AS (
    SELECT * FROM TD_GLM (
        ON customer_survey_training AS InputTable
        USING
        InputColumns ('price_sensitivity', 'brand_awareness', 'product_rating',
                      'competitor_usage', 'income_level', 'household_size')
        ResponseColumn ('purchased')
        Family ('binomial')
        LinkFunction ('probit')  -- Probit link assumes normal distribution
        Intercept ('true')
        MaxIterNum (100)
    ) AS dt
) WITH DATA;

-- Score market research respondents
SELECT * FROM TD_GLMPredict (
    ON market_research_respondents AS InputTable PARTITION BY ANY
    ON purchase_glm_model AS ModelTable DIMENSION
    USING
    IDColumn ('respondent_id')
    OutputProb ('true')
    Responses ('0', '1')
    Accumulate ('age_group', 'income_bracket', 'region')
) AS dt
ORDER BY respondent_id;

/*
Sample Output:
respondent_id | prediction | prob_0 | prob_1 | age_group | income_bracket | region
--------------|------------|--------|--------|-----------|----------------|----------
RESP1001      | 1          | 0.22   | 0.78   | 35-44     | $75K-$100K     | Northeast
RESP1002      | 0          | 0.68   | 0.32   | 25-34     | $50K-$75K      | South
RESP1003      | 1          | 0.38   | 0.62   | 45-54     | $100K+         | West

Interpretation:
- RESP1001: 78% purchase probability → High-value target for marketing
- RESP1002: 32% purchase probability → Requires promotional incentive
- Probit model provides marginal effects for pricing strategy analysis
*/

-- Segment market by purchase propensity
CREATE TABLE market_segments AS (
    SELECT
        age_group,
        income_bracket,
        region,
        COUNT(*) AS segment_size,
        AVG(prob_1) AS avg_purchase_probability,
        SUM(CASE WHEN prob_1 >= 0.60 THEN 1 ELSE 0 END) AS high_propensity_count,
        ROUND(AVG(prob_1) * COUNT(*), 0) AS expected_conversions
    FROM TD_GLMPredict (
        ON market_research_respondents AS InputTable PARTITION BY ANY
        ON purchase_glm_model AS ModelTable DIMENSION
        USING
        IDColumn ('respondent_id')
        OutputProb ('true')
        Responses ('0', '1')
        Accumulate ('age_group', 'income_bracket', 'region')
    ) AS dt
    GROUP BY age_group, income_bracket, region
) WITH DATA
ORDER BY expected_conversions DESC;

-- Business Impact:
-- Targeted marketing to high-propensity segments improved ROI by 45%
-- Price sensitivity analysis informed premium product launch strategy
-- Identified underserved geographic markets with low brand awareness
```

## Common Use Cases

### Credit Risk and Financial Services
- **Loan Default Prediction**: Binary classification with logistic regression
- **Credit Scoring**: Probability-based risk assessment for lending decisions
- **Fraud Detection**: Real-time transaction scoring with probability thresholds
- **Customer Lifetime Value**: Gamma regression for revenue prediction

### Healthcare and Life Sciences
- **Patient Risk Stratification**: Multi-class classification for care prioritization
- **Readmission Prediction**: Binary classification for care management
- **Length of Stay Prediction**: Gamma or inverse Gaussian regression
- **Disease Progression**: Ordinal regression for stage prediction

### Insurance
- **Claim Amount Prediction**: Gamma regression with log link for positive, skewed data
- **Claim Frequency**: Poisson regression for count data
- **Policy Lapse Prediction**: Logistic regression for retention analysis
- **Risk Classification**: Multi-class models for underwriting

### Retail and E-commerce
- **Customer Churn**: Binary classification with probability scores
- **Purchase Propensity**: Logistic or probit regression for targeting
- **Product Demand Forecasting**: Poisson regression for count data
- **Price Sensitivity**: Linear regression with log link

### Operations and Supply Chain
- **Call Volume Forecasting**: Poisson regression for staffing optimization
- **Defect Rate Prediction**: Binomial regression for quality control
- **Delivery Time Estimation**: Gamma regression for logistics
- **Inventory Optimization**: Multiple regression for demand prediction

## Best Practices

### Model Application
1. **Feature Consistency**: Ensure test data has identical predictor columns as training data
2. **Missing Value Handling**: Impute or remove missing values before prediction
3. **Feature Scaling**: Apply same scaling/transformations used during training
4. **Probability Calibration**: For classification, verify probabilities are well-calibrated on validation set

### Performance Optimization
1. **Batch Scoring**: Score data in batches using PARTITION BY ANY for parallel processing
2. **Index ID Column**: Create index on IDColumn for faster joins with business tables
3. **Accumulate Wisely**: Only accumulate columns needed downstream to reduce data transfer
4. **Partition Large Tables**: Use temporal or geographic partitioning for very large scoring datasets

### Production Deployment
1. **Model Versioning**: Include model version in table names (credit_glm_model_v2)
2. **Threshold Tuning**: Adjust probability thresholds based on business costs (false positive vs false negative)
3. **Monitoring**: Track prediction distribution over time to detect data drift
4. **A/B Testing**: Compare model versions side-by-side before full deployment

### Interpretation
1. **Link Function Awareness**: Remember predictions are transformed through inverse link function
2. **Probability Interpretation**: Use OutputProb for classification to enable threshold optimization
3. **Confidence Intervals**: For regression, calculate confidence intervals from model standard errors
4. **Business Context**: Accumulate business-relevant columns for decision-making

### Data Quality
1. **Outlier Detection**: Check for extreme values that may produce unrealistic predictions
2. **Data Type Validation**: Ensure numeric predictors are not inadvertently character type
3. **Range Checks**: Validate predictions fall within expected business ranges
4. **NULL Handling**: Models cannot predict with NULL predictors - handle upstream

## Related Functions

### Model Training
- **TD_GLM**: Train Generalized Linear Models (produces ModelTable input)
- **TD_DecisionForest**: Alternative non-linear classification/regression
- **TD_XGBoost**: Gradient boosting alternative for complex patterns
- **TD_NaiveBayes**: Probabilistic classification alternative

### Model Evaluation
- **TD_ClassificationEvaluator**: Evaluate classification model performance with confusion matrix
- **TD_RegressionEvaluator**: Evaluate regression model metrics (RMSE, MAE, R²)
- **TD_ROC**: Generate ROC curves and calculate AUC for binary classification

### Data Preparation
- **TD_SimpleImputeFit/Transform**: Handle missing values before prediction
- **TD_ScaleFit/Transform**: Standardize features to improve model performance
- **TD_OneHotEncodingFit/Transform**: Convert categorical variables for GLM input

### Feature Engineering
- **TD_PolynomialFeaturesFit/Transform**: Create polynomial and interaction terms
- **TD_BincodeFit/Transform**: Bin continuous variables for non-linear effects
- **TD_ColumnTransformer**: Apply multiple transformations in pipeline

## Notes and Limitations

### General Limitations
1. **Linear Assumptions**: GLM assumes linear relationship between predictors and link-transformed response
2. **Feature Matching**: All predictor columns from training must be present in test data
3. **No Automatic Imputation**: Function does not handle missing values - preprocess data first
4. **No Feature Engineering**: Apply same transformations (scaling, encoding) used during training

### Distribution and Link Function
1. **Family Selection**: Distribution family must match response variable characteristics
   - Gaussian: Continuous, normally distributed
   - Binomial: Binary (0/1) classification
   - Poisson: Count data (non-negative integers)
   - Gamma: Positive, right-skewed continuous data
   - Inverse Gaussian: Positive continuous with long right tail
2. **Link Function**: Must match link function used in training model
3. **Prediction Scale**: Predictions are in original response scale (inverse link applied automatically)

### Classification Specifics
1. **Multi-Class**: Some implementations support multi-class through multinomial extension
2. **Class Ordering**: Response class order must match training for probability interpretation
3. **Threshold Selection**: Default 0.5 threshold may not be optimal - use OutputProb to tune
4. **Imbalanced Classes**: GLM can struggle with severe imbalance - consider class weights or sampling

### Performance Considerations
1. **Large Models**: Models with many predictors may have slower prediction time
2. **Numerical Stability**: Extreme predictor values can cause overflow in exponential link functions
3. **Memory**: Very large test datasets may require chunking into smaller batches

### Best Use Cases
- **When to Use GLM**: Interpretability important, linear relationships expected, need probability calibration
- **When to Avoid GLM**: Complex non-linear patterns, many interaction effects, high-dimensional feature spaces
- **Alternatives**: Consider TD_XGBoost or TD_DecisionForest for non-linear patterns

### Teradata-Specific Notes
1. **UTF8 Support**: ModelTable and InputTable support UTF8 character sets
2. **PARTITION BY ANY**: Enables parallel processing across AMPs
3. **DIMENSION Tables**: ModelTable must be DIMENSION for broadcast to all AMPs
4. **Deterministic**: Same input always produces same output (no randomness)

## Version Information

**Documentation Generated:** November 29, 2025
**Based on:** Teradata Database Analytic Functions Version 17.20
**Function Category:** Machine Learning - Model Scoring
**Last Updated:** 2025-11-29
