# TD_DecisionForestPredict

## Function Name
- **TD_DecisionForestPredict**: Random Forest Prediction Function - Scores test data using a trained decision forest model

## Description
TD_DecisionForestPredict uses the model output by TD_DecisionForest to analyze input data and make predictions. This function outputs the probability that each observation belongs to the predicted class (for classification) or the predicted value with confidence interval (for regression).

The function applies ensemble learning by aggregating predictions from multiple decision trees trained on different subsets of data and features. Each tree votes on the prediction, and the final output is determined by majority vote (classification) or average (regression).

### Characteristics
- Processes test data using trained random forest model
- Supports both classification and regression
- Outputs prediction probabilities for classification tasks
- Provides confidence intervals for regression tasks
- Can output detailed tree-level information
- Handles models with hundreds or thousands of trees
- Trees cached in local spool when exceeding memory

### Processing Notes
- Processing time controlled by number of trees in model
- When trees exceed available memory, cached in local spool
- Can specify which response classes to output probabilities for
- Optional detailed output shows which tree made each prediction

## When to Use TD_DecisionForestPredict

TD_DecisionForestPredict is essential for applying trained random forest models:

### Production Scoring
- **Batch predictions**: Score large datasets with trained models
- **Real-time scoring**: Apply models to new observations
- **Scheduled scoring**: Regular scoring runs (daily, weekly)
- **A/B testing**: Compare predictions from different model versions
- **Model monitoring**: Track prediction distributions over time

### Model Validation and Testing
- **Test set evaluation**: Score holdout test data to assess performance
- **Cross-validation**: Score validation folds during model selection
- **Model comparison**: Compare predictions from multiple algorithms
- **Threshold optimization**: Analyze probabilities to set optimal cutoffs
- **Confidence analysis**: Examine prediction confidence intervals

### Business Applications
- **Customer churn prediction**: Identify customers likely to leave
- **Credit risk scoring**: Assess loan default probability
- **Fraud detection**: Flag suspicious transactions
- **Product recommendations**: Predict product preferences
- **Demand forecasting**: Predict future sales or demand
- **Medical diagnosis**: Predict disease presence or outcomes
- **Predictive maintenance**: Forecast equipment failures

### Use Cases by Industry
- **Retail**: Customer lifetime value prediction, basket analysis
- **Finance**: Credit scoring, fraud detection, risk assessment
- **Healthcare**: Disease diagnosis, readmission prediction, treatment outcomes
- **Manufacturing**: Quality control, predictive maintenance, yield prediction
- **Telecommunications**: Churn prediction, network optimization
- **Insurance**: Claims prediction, risk assessment, pricing
- **Marketing**: Response prediction, customer segmentation, targeting

## Syntax

```sql
TD_DecisionForestPredict (
    ON { table | view | (query) } AS InputTable PARTITION BY ANY
    ON { table | view | (query) } AS ModelTable DIMENSION
    USING
    IDColumn ('id_column')
    [ Detailed ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
    [ OutputProb ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
    [ Responses ('response'[,...]) ]
    [ Accumulate ({'accumulate_column'|accumulate_column_range}[,...]) ]
)
```

**Note:** You can call this function from:
- The FROM clause of a SELECT statement
- As part of a CREATE TABLE statement
- As part of a CREATE VIEW statement

## Required Syntax Elements

### ON Clause
Specifies the table name, view name, or query as InputTable and ModelTable.
- **InputTable**: Test data for which to predict outcomes
- **PARTITION BY ANY**: Required partitioning clause
- **ModelTable**: Trained model from TD_DecisionForest (DIMENSION table)

### IDColumn
Column with a unique identifier for each test point in the test set.
- **Data Type**: Any
- **Purpose**: Identifies each prediction in output
- **Requirement**: Cannot be NULL
- **Example**: `IDColumn('customer_id')`

## Optional Syntax Elements

### Detailed
Indicator to output detailed information about decision trees.
- **Values**: true/false (or t/f, yes/no, y/n, 1/0)
- **Default**: false
- **Output**: When true, shows task index and tree index for each tree
- **Purpose**: Debug predictions, understand tree-level contributions
- **Use case**: Identify which trees drive specific predictions

### OutputProb
Indicator to output the probability for each response.
- **Values**: true/false (or t/f, yes/no, y/n, 1/0)
- **Default**: false
- **Applies to**: Classification models only
- **Without Responses**: Outputs probability of predicted class only
- **With Responses**: Outputs probability for each specified response
- **Note**: Must be true when using Responses parameter

### Responses
Classes to output the probabilities.
- **Format**: Comma-separated list of class labels
- **Applies to**: Classification models only
- **Requires**: OutputProb must be true
- **Default**: Output only probability of predicted class
- **Example**: `Responses('0', '1')` or `Responses('Churned', 'Retained')`
- **Use case**: Multi-class problems where you want all class probabilities

### Accumulate
Names of input columns to copy to the output table.
- **Format**: Column names or column ranges
- **Purpose**: Include additional context in output
- **Example**: `Accumulate('customer_name', 'signup_date', 'segment')`
- **Use case**: Join predictions back to original data

## Input

### InputTable Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| ID_Column | Varies | Unique test point identifier (cannot be NULL) |
| target_columns | INTEGER, BIGINT, SMALLINT, BYTEINT, FLOAT, DECIMAL, NUMBER | Predictor variables (one column per feature, cannot be NULL) |
| accumulate_columns | Varies | Columns to copy to output table |

**Requirements**:
- Input features must match those used in TD_DecisionForest training
- Feature columns cannot contain NULLs
- Column names and data types must match training data

### ModelTable Schema

Output from TD_DecisionForest function.

**For Classification**:

| Column | Data Type | Description |
|--------|-----------|-------------|
| task_index | SMALLINT | Identifier of AMP that produced decision tree |
| tree_num | INTEGER | Decision tree identifier |
| tree_order | INTEGER | Sequence of substring of tree |
| classification_tree | VARCHAR(16000) | JSON representation of decision tree |

**For Regression**:

| Column | Data Type | Description |
|--------|-----------|-------------|
| task_index | SMALLINT | Identifier of AMP that produced decision tree |
| tree_num | INTEGER | Decision tree identifier |
| tree_order | INTEGER | Sequence of substring of tree |
| regression_tree | VARCHAR(16000) | JSON representation of decision tree |

## Output

### Output Table Schema

The table contains a set of predictions for each test point.

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| id_column | Same as input | Column copied from input table (unique row identifier) |
| prediction | Integer (classification) or FLOAT (regression) | Predicted test point value or predicted class |
| confidence_lower | FLOAT | [OutputProb is false] Lower bound of confidence interval. For classification, equals confidence_upper (probability of predicted class) |
| confidence_upper | FLOAT | [OutputProb is false] Upper bound of confidence interval. For classification, equals confidence_upper (probability of predicted class) |
| prob | FLOAT | [OutputProb is true, no Responses] Probability that observation belongs to class prediction |
| prob_response | FLOAT | [OutputProb is true with Responses] Probability that observation belongs to category response (one column per response) |
| tree_num | VARCHAR(30) | [Detailed is true] Concatenation of task_index and tree_num showing which tree created prediction, or "Final" for overall prediction |
| accumulate_column | Same as input | Columns copied from input table |

## Code Examples

### Example 1: Basic Classification Prediction (Home Style Classification)

Predict home architectural styles using trained random forest model:

```sql
-- Input: Test data for home style classification
CREATE TABLE homes_test (
    SN INTEGER,
    Price DECIMAL(10,2),
    LotSize INTEGER,
    Bedrooms INTEGER,
    Bathrooms INTEGER,
    Stories INTEGER,
    Driveways INTEGER,
    Recroom INTEGER,
    FullBase INTEGER,
    GasHW INTEGER,
    AirCo INTEGER,
    HomeStyle VARCHAR(20)  -- Actual style (for validation)
);

INSERT INTO homes_test VALUES
(1, 42000, 4960, 2, 1, 1, 1, 0, 0, 0, 0, '1'),
(2, 130000, 6000, 4, 1, 2, 1, 0, 1, 0, 0, '3'),
(3, 60000, 2953, 3, 1, 2, 1, 0, 1, 0, 1, '2'),
(4, 43000, 3750, 3, 1, 2, 1, 0, 0, 0, 0, '1'),
(5, 86900, 4300, 6, 2, 2, 1, 0, 0, 0, 0, '2'),
(6, 141000, 8100, 4, 1, 2, 1, 1, 1, 0, 1, '3');

-- Basic prediction without probabilities
SELECT * FROM TD_DecisionForestPredict (
    ON homes_test AS InputTable PARTITION BY ANY
    ON home_style_model AS ModelTable DIMENSION
    USING
    IDColumn ('SN')
    Accumulate('HomeStyle', 'Price')
    Detailed('false')
) AS dt
ORDER BY SN;

/*
Output:
SN | Prediction | Confidence_Lower | Confidence_Upper | HomeStyle | Price
---|------------|------------------|------------------|-----------|--------
1  | 1          | 0.7143          | 0.7143           | 1         | 42000
2  | 3          | 0.5714          | 0.5714           | 3         | 130000
3  | 2          | 0.7143          | 0.7143           | 2         | 60000
4  | 1          | 0.7143          | 0.7143           | 1         | 43000
5  | 2          | 0.8571          | 0.8571           | 2         | 86900
6  | 3          | 0.5714          | 0.5714           | 3         | 141000

Interpretation:
- SN 1: Predicted style 1 with 71.43% confidence (correct)
- SN 2: Predicted style 3 with 57.14% confidence (correct)
- SN 3: Predicted style 2 with 71.43% confidence (correct)
- Lower confidence_lower/upper values indicate less certain predictions
- For classification, both confidence values are equal (represent probability)
*/

-- Validate predictions
SELECT
    COUNT(*) as total_predictions,
    SUM(CASE WHEN prediction = CAST(HomeStyle AS INTEGER) THEN 1 ELSE 0 END) as correct_predictions,
    ROUND(SUM(CASE WHEN prediction = CAST(HomeStyle AS INTEGER) THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as accuracy_pct
FROM TD_DecisionForestPredict (
    ON homes_test AS InputTable PARTITION BY ANY
    ON home_style_model AS ModelTable DIMENSION
    USING
    IDColumn ('SN')
    Accumulate('HomeStyle')
) AS dt;

/*
Output:
total_predictions | correct_predictions | accuracy_pct
------------------|--------------------|--------------
6                 | 6                  | 100.00

Perfect accuracy on this test set!
*/
```

**Use Case**: Predict residential architectural style based on home features.

### Example 2: Classification with Probability Output

Output probabilities for all classes to understand prediction confidence:

```sql
-- Predict with full probability distribution across classes
SELECT * FROM TD_DecisionForestPredict (
    ON homes_test AS InputTable PARTITION BY ANY
    ON home_style_model AS ModelTable DIMENSION
    USING
    IDColumn ('SN')
    OutputProb('true')
    Responses('1', '2', '3')  -- Three home style classes
    Accumulate('HomeStyle', 'Price')
) AS dt
ORDER BY SN;

/*
Output:
SN | Prediction | prob_1  | prob_2  | prob_3  | HomeStyle | Price
---|------------|---------|---------|---------|-----------|--------
1  | 1          | 0.7143  | 0.2143  | 0.0714  | 1         | 42000
2  | 3          | 0.1429  | 0.2857  | 0.5714  | 3         | 130000
3  | 2          | 0.1429  | 0.7143  | 0.1429  | 2         | 60000
4  | 1          | 0.7143  | 0.2143  | 0.0714  | 1         | 43000
5  | 2          | 0.0714  | 0.8571  | 0.0714  | 2         | 86900
6  | 3          | 0.1429  | 0.2857  | 0.5714  | 3         | 141000

Interpretation:
- SN 1: 71% style 1, 21% style 2, 7% style 3 → Clear prediction
- SN 2: 57% style 3, 29% style 2, 14% style 1 → Less confident
- SN 5: 86% style 2, 7% styles 1&3 → Very confident prediction
- Probabilities sum to 1.0 for each row
*/

-- Analyze prediction confidence
WITH predictions AS (
    SELECT
        SN,
        prediction,
        prob_1,
        prob_2,
        prob_3,
        GREATEST(prob_1, prob_2, prob_3) as max_probability,
        HomeStyle
    FROM TD_DecisionForestPredict (
        ON homes_test AS InputTable PARTITION BY ANY
        ON home_style_model AS ModelTable DIMENSION
        USING
        IDColumn ('SN')
        OutputProb('true')
        Responses('1', '2', '3')
        Accumulate('HomeStyle')
    ) AS dt
)
SELECT
    SN,
    prediction,
    CAST(HomeStyle AS INTEGER) as actual,
    ROUND(max_probability, 4) as confidence,
    CASE
        WHEN max_probability >= 0.8 THEN 'High Confidence'
        WHEN max_probability >= 0.6 THEN 'Medium Confidence'
        ELSE 'Low Confidence'
    END as confidence_category,
    CASE WHEN prediction = CAST(HomeStyle AS INTEGER) THEN 'Correct' ELSE 'Incorrect' END as result
FROM predictions
ORDER BY max_probability DESC;
```

**Business Value**: Understand prediction certainty to prioritize actions or flag uncertain predictions for review.

### Example 3: Customer Churn Prediction with Detailed Tree Analysis

Use detailed output to understand which trees contribute to predictions:

```sql
-- Customer churn prediction dataset
CREATE TABLE customers_test AS (
    SELECT
        customer_id,
        tenure_months,
        monthly_charges,
        total_charges,
        num_products,
        has_phone_service,
        has_internet_service,
        contract_type,
        churned  -- Actual outcome (0=retained, 1=churned)
    FROM customer_churn_test
) WITH DATA;

-- Predict with detailed tree information
SELECT * FROM TD_DecisionForestPredict (
    ON customers_test AS InputTable PARTITION BY ANY
    ON churn_forest_model AS ModelTable DIMENSION
    USING
    IDColumn ('customer_id')
    Detailed('true')
    OutputProb('false')
    Accumulate('churned', 'tenure_months', 'monthly_charges')
) AS dt
WHERE customer_id IN (1001, 1002)
ORDER BY customer_id, tree_num;

/*
Output (sample):
customer_id | prediction | confidence_lower | confidence_upper | tree_num  | churned | tenure_months | monthly_charges
------------|------------|------------------|------------------|-----------|---------|---------------|----------------
1001        | 0          | 0.00             | 0.00             | 0_1       | 0       | 48            | 65.50
1001        | 0          | 0.00             | 0.00             | 0_2       | 0       | 48            | 65.50
1001        | 0          | 0.00             | 0.00             | 1_1       | 0       | 48            | 65.50
1001        | 0          | 0.00             | 0.00             | 1_2       | 0       | 48            | 65.50
1001        | 0          | 0.00             | 0.00             | Final     | 0       | 48            | 65.50
1002        | 1          | 1.00             | 1.00             | 0_1       | 1       | 6             | 95.00
1002        | 1          | 1.00             | 1.00             | 0_2       | 1       | 6             | 95.00
1002        | 0          | 0.00             | 0.00             | 1_1       | 1       | 6             | 95.00
1002        | 1          | 1.00             | 1.00             | 1_2       | 1       | 6             | 95.00
1002        | 1          | 1.00             | 1.00             | Final     | 1       | 6             | 95.00

Interpretation:
- customer_id 1001: All trees predict 0 (retained) → Unanimous prediction
- customer_id 1002: Most trees predict 1 (churned), one predicts 0 → Majority vote for churned
- tree_num format: "task_index_tree_num" identifies specific tree
- "Final" row shows ensemble prediction from all trees
*/

-- Analyze tree-level predictions to understand consensus
WITH tree_votes AS (
    SELECT
        customer_id,
        tree_num,
        prediction
    FROM TD_DecisionForestPredict (
        ON customers_test AS InputTable PARTITION BY ANY
        ON churn_forest_model AS ModelTable DIMENSION
        USING
        IDColumn ('customer_id')
        Detailed('true')
        Accumulate('churned')
    ) AS dt
    WHERE tree_num != 'Final'  -- Exclude final prediction
)
SELECT
    customer_id,
    SUM(CASE WHEN prediction = 0 THEN 1 ELSE 0 END) as trees_predict_retained,
    SUM(CASE WHEN prediction = 1 THEN 1 ELSE 0 END) as trees_predict_churned,
    COUNT(*) as total_trees,
    ROUND(SUM(CASE WHEN prediction = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as pct_trees_churn
FROM tree_votes
GROUP BY customer_id
ORDER BY pct_trees_churn DESC
LIMIT 10;

/*
Output:
customer_id | trees_predict_retained | trees_predict_churned | total_trees | pct_trees_churn
------------|------------------------|----------------------|-------------|------------------
1002        | 1                      | 4                    | 5           | 80.00
1005        | 2                      | 3                    | 5           | 60.00
1003        | 3                      | 2                    | 5           | 40.00
1001        | 5                      | 0                    | 5           | 0.00

High percentage = strong churn signal across trees
Low percentage = weak churn signal
*/
```

**Strategic Insight**: Tree-level detail reveals prediction strength and helps identify borderline cases.

### Example 4: Regression with Confidence Intervals

Predict continuous values with confidence intervals:

```sql
-- Housing price prediction
CREATE TABLE houses_test (
    house_id INTEGER,
    sqft INTEGER,
    bedrooms INTEGER,
    bathrooms DECIMAL(3,1),
    lot_size INTEGER,
    year_built INTEGER,
    actual_price DECIMAL(12,2)
);

-- Predict house prices with confidence intervals
SELECT
    house_id,
    prediction as predicted_price,
    confidence_lower as price_lower_bound,
    confidence_upper as price_upper_bound,
    (confidence_upper - confidence_lower) as confidence_width,
    actual_price,
    ABS(prediction - actual_price) as prediction_error,
    ROUND(ABS(prediction - actual_price) * 100.0 / actual_price, 2) as pct_error
FROM TD_DecisionForestPredict (
    ON houses_test AS InputTable PARTITION BY ANY
    ON housing_forest_model AS ModelTable DIMENSION
    USING
    IDColumn ('house_id')
    Accumulate('actual_price')
) AS dt
ORDER BY pct_error;

/*
Output:
house_id | predicted_price | price_lower_bound | price_upper_bound | confidence_width | actual_price | prediction_error | pct_error
---------|-----------------|-------------------|-------------------|------------------|--------------|------------------|----------
101      | 425000          | 410000            | 440000            | 30000            | 430000       | 5000             | 1.16
102      | 680000          | 650000            | 710000            | 60000            | 675000       | 5000             | 0.74
103      | 295000          | 280000            | 310000            | 30000            | 320000       | 25000            | 7.81

Interpretation:
- Confidence intervals show prediction uncertainty
- Wider intervals = less certain predictions
- Actual prices should fall within intervals ~95% of time (depends on model)
- Lower percent error = better predictions
*/

-- Summarize prediction quality
SELECT
    COUNT(*) as total_houses,
    ROUND(AVG(prediction), 0) as avg_predicted_price,
    ROUND(AVG(actual_price), 0) as avg_actual_price,
    ROUND(AVG(ABS(prediction - actual_price)), 0) as mae,
    ROUND(SQRT(AVG(POWER(prediction - actual_price, 2))), 0) as rmse,
    ROUND(AVG(confidence_upper - confidence_lower), 0) as avg_confidence_width
FROM TD_DecisionForestPredict (
    ON houses_test AS InputTable PARTITION BY ANY
    ON housing_forest_model AS ModelTable DIMENSION
    USING
    IDColumn ('house_id')
    Accumulate('actual_price')
) AS dt;
```

**Use Case**: Real estate valuation with uncertainty quantification.

### Example 5: Batch Scoring for Production

Score large dataset for production use:

```sql
-- Production batch scoring
CREATE TABLE customer_churn_scores_2024Q1 AS (
    SELECT
        customer_id,
        score_date,
        prediction as predicted_churn,
        CASE WHEN prediction = 1 THEN 'At Risk' ELSE 'Stable' END as risk_category,
        confidence_lower as churn_probability,
        CASE
            WHEN confidence_lower >= 0.8 THEN 'Very High Risk'
            WHEN confidence_lower >= 0.6 THEN 'High Risk'
            WHEN confidence_lower >= 0.4 THEN 'Medium Risk'
            WHEN confidence_lower >= 0.2 THEN 'Low Risk'
            ELSE 'Very Low Risk'
        END as risk_level,
        -- Accumulated customer features for context
        tenure_months,
        monthly_charges,
        contract_type,
        customer_segment
    FROM TD_DecisionForestPredict (
        ON (
            SELECT
                CURRENT_DATE as score_date,
                *
            FROM active_customers_features
            WHERE as_of_date = CURRENT_DATE
        ) AS InputTable PARTITION BY ANY
        ON churn_forest_model_v2 AS ModelTable DIMENSION
        USING
        IDColumn ('customer_id')
        Accumulate('tenure_months', 'monthly_charges', 'contract_type', 'customer_segment')
    ) AS dt
) WITH DATA;

-- Create retention campaign target list
CREATE TABLE retention_campaign_targets AS (
    SELECT
        customer_id,
        risk_level,
        churn_probability,
        tenure_months,
        monthly_charges,
        CASE
            WHEN churn_probability >= 0.7 AND monthly_charges > 100 THEN 'Tier 1: High Value, High Risk'
            WHEN churn_probability >= 0.6 AND monthly_charges > 50 THEN 'Tier 2: Medium Value, High Risk'
            WHEN churn_probability >= 0.4 THEN 'Tier 3: Medium Risk'
            ELSE 'Tier 4: Low Risk - Monitor Only'
        END as campaign_tier
    FROM customer_churn_scores_2024Q1
    WHERE predicted_churn = 1
) WITH DATA;

-- Analyze campaign targeting
SELECT
    campaign_tier,
    COUNT(*) as customer_count,
    ROUND(AVG(churn_probability), 4) as avg_churn_prob,
    ROUND(AVG(monthly_charges), 2) as avg_monthly_revenue,
    ROUND(SUM(monthly_charges * 12), 0) as annual_revenue_at_risk
FROM retention_campaign_targets
GROUP BY campaign_tier
ORDER BY campaign_tier;

/*
Output:
campaign_tier                        | customer_count | avg_churn_prob | avg_monthly_revenue | annual_revenue_at_risk
-------------------------------------|----------------|----------------|---------------------|------------------------
Tier 1: High Value, High Risk       | 450            | 0.7845         | 145.50              | 785700
Tier 2: Medium Value, High Risk     | 1200           | 0.6521         | 75.25               | 1083600
Tier 3: Medium Risk                 | 2800           | 0.5134         | 62.10               | 2086560
Tier 4: Low Risk - Monitor Only     | 1550           | 0.3245         | 55.80               | 1037640

Business Action:
- Tier 1: Immediate outreach with premium retention offers
- Tier 2: Proactive retention campaigns
- Tier 3: Automated engagement programs
- Tier 4: Standard customer success check-ins
*/
```

**Production Pattern**: Score all customers, segment by risk, prioritize retention efforts.

### Example 6: Compare Multiple Model Versions

Compare predictions from different model versions:

```sql
-- Score with Model V1
CREATE TABLE predictions_v1 AS (
    SELECT
        customer_id,
        'Model V1' as model_version,
        prediction as predicted_churn,
        confidence_lower as churn_probability
    FROM TD_DecisionForestPredict (
        ON customers_test AS InputTable PARTITION BY ANY
        ON churn_model_v1 AS ModelTable DIMENSION
        USING IDColumn ('customer_id')
    ) AS dt
) WITH DATA;

-- Score with Model V2 (retrained with recent data)
CREATE TABLE predictions_v2 AS (
    SELECT
        customer_id,
        'Model V2' as model_version,
        prediction as predicted_churn,
        confidence_lower as churn_probability
    FROM TD_DecisionForestPredict (
        ON customers_test AS InputTable PARTITION BY ANY
        ON churn_model_v2 AS ModelTable DIMENSION
        USING IDColumn ('customer_id')
    ) AS dt
) WITH DATA;

-- Compare model predictions
SELECT
    COALESCE(v1.customer_id, v2.customer_id) as customer_id,
    v1.predicted_churn as v1_prediction,
    v2.predicted_churn as v2_prediction,
    v1.churn_probability as v1_probability,
    v2.churn_probability as v2_probability,
    ABS(v1.churn_probability - v2.churn_probability) as probability_diff,
    CASE
        WHEN v1.predicted_churn = v2.predicted_churn THEN 'Agreement'
        ELSE 'Disagreement'
    END as model_agreement
FROM predictions_v1 v1
FULL OUTER JOIN predictions_v2 v2 USING (customer_id)
ORDER BY probability_diff DESC
LIMIT 20;

/*
Customers where models disagree most:
customer_id | v1_prediction | v2_prediction | v1_probability | v2_probability | probability_diff | model_agreement
------------|---------------|---------------|----------------|----------------|------------------|------------------
1523        | 0             | 1             | 0.45           | 0.85           | 0.40             | Disagreement
1789        | 1             | 0             | 0.75           | 0.35           | 0.40             | Disagreement
2041        | 0             | 1             | 0.40           | 0.78           | 0.38             | Disagreement

Analysis: Large differences suggest:
- V2 model learned new patterns from recent data
- Customer behavior may have shifted
- Review these customers for model validation
*/
```

**Model Management**: Track model version changes and validate improvements.

## Common Use Cases

### 1. Probability-Based Ranking

```sql
-- Rank customers by churn probability
SELECT
    customer_id,
    confidence_lower as churn_probability,
    ROW_NUMBER() OVER (ORDER BY confidence_lower DESC) as churn_risk_rank
FROM TD_DecisionForestPredict (
    ON customers AS InputTable PARTITION BY ANY
    ON churn_model AS ModelTable DIMENSION
    USING IDColumn ('customer_id')
)
WHERE prediction = 1
ORDER BY churn_probability DESC
LIMIT 100;
```

### 2. A/B Test Analysis

```sql
-- Compare treated vs control groups
SELECT
    treatment_group,
    COUNT(*) as customers,
    SUM(prediction) as predicted_conversions,
    ROUND(AVG(confidence_lower), 4) as avg_conversion_prob
FROM TD_DecisionForestPredict (
    ON ab_test_cohort AS InputTable PARTITION BY ANY
    ON conversion_model AS ModelTable DIMENSION
    USING IDColumn ('customer_id') Accumulate('treatment_group')
) AS dt
GROUP BY treatment_group;
```

### 3. Forecast Validation

```sql
-- Compare predictions to actuals over time
SELECT
    forecast_date,
    SUM(prediction) as predicted_sales,
    SUM(actual_sales) as actual_sales,
    SUM(prediction) - SUM(actual_sales) as forecast_error,
    ROUND((SUM(prediction) - SUM(actual_sales)) * 100.0 / SUM(actual_sales), 2) as pct_error
FROM TD_DecisionForestPredict (
    ON sales_history AS InputTable PARTITION BY ANY
    ON demand_model AS ModelTable DIMENSION
    USING IDColumn ('transaction_id') Accumulate('forecast_date', 'actual_sales')
) AS dt
GROUP BY forecast_date
ORDER BY forecast_date;
```

## Best Practices

1. **Match Training and Test Data**:
   - Ensure test data has same features as training data
   - Use same feature engineering pipeline
   - Check for data type consistency
   - Handle missing values before scoring

2. **Interpret Probabilities Correctly**:
   - Classification: confidence_lower/upper = probability
   - Regression: confidence_lower/upper = prediction interval
   - Higher probabilities = more confident predictions
   - Use probability thresholds for decision-making

3. **Use Detailed Output for Debugging**:
   - Enable when predictions seem incorrect
   - Identify if specific trees are problematic
   - Understand consensus across trees
   - Disable for production (performance impact)

4. **Handle Large Models**:
   - Models with many trees may exceed memory
   - Trees cached in spool when necessary
   - Monitor performance with large forests
   - Consider model pruning if too slow

5. **Monitor Prediction Quality**:
   - Track prediction distributions over time
   - Compare to historical baselines
   - Alert on significant distribution shifts
   - Retrain when performance degrades

6. **Batch Scoring Optimization**:
   - Score in batches rather than row-by-row
   - Partition by appropriate keys
   - Index on IDColumn for joins
   - Archive old predictions

7. **Business Rule Integration**:
   - Combine predictions with business rules
   - Use probabilities to prioritize actions
   - Set thresholds based on business costs
   - Create tiered intervention strategies

8. **Version Control**:
   - Track model versions used for scoring
   - Document when models are retrained
   - Compare predictions across versions
   - Maintain model lineage

## Related Functions

- **TD_DecisionForest**: Train random forest models for classification and regression
- **TD_ClassificationEvaluator**: Evaluate classification predictions
- **TD_RegressionEvaluator**: Evaluate regression predictions
- **TD_ROC**: Generate ROC curves for binary classification
- **TD_FeatureImportance**: Understand which features drive predictions
- **TD_GLMPredict**: Alternative prediction using generalized linear models
- **TD_XGBoostPredict**: Alternative using gradient boosting

## Notes and Limitations

1. **Model Requirements**:
   - ModelTable must be from TD_DecisionForest
   - Model must be DIMENSION table
   - Cannot use models from other functions

2. **Feature Consistency**:
   - Test data must have exact same features as training
   - Feature names must match exactly (case-sensitive)
   - Data types must match
   - NULL values will cause errors

3. **Memory and Performance**:
   - Large models (many trees) may exceed memory
   - Trees cached in local spool when needed
   - Detailed output increases processing time
   - Performance depends on number of trees

4. **OutputProb Limitations**:
   - Only works with classification models
   - Regression models don't have OutputProb option
   - Must specify Responses if want all class probabilities
   - Probabilities based on tree votes (may differ from calibrated probabilities)

5. **Confidence Intervals**:
   - For classification: Both bounds equal probability
   - For regression: Bounds form prediction interval
   - Interval width indicates uncertainty
   - Not Bayesian credible intervals

6. **ID Column**:
   - Must be unique for each row
   - Cannot contain NULLs
   - Used to join predictions back to source data
   - Any data type acceptable

7. **Detailed Output**:
   - Generates multiple rows per observation
   - One row per tree + one final row
   - Can significantly increase output size
   - Use only for debugging/analysis

8. **Responses Parameter**:
   - Requires OutputProb to be true
   - Can specify subset of classes
   - Order doesn't matter
   - Creates one prob_ column per response

## Version Information

- **Function Version**: Based on Teradata Database Analytic Functions Version 17.20
- **Generated**: November 29, 2025
- **Category**: Model Scoring Functions / Random Forest / Ensemble Learning
