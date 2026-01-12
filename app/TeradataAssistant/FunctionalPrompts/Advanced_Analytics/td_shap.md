# TD_SHAP

### Function Name
**TD_SHAP** (SHapley Additive exPlanations)

### Description
TD_SHAP computes SHAP (SHapley Additive exPlanations) values to explain individual predictions by quantifying each feature's contribution to the model's output, based on cooperative game theory principles. This model-agnostic explainability method calculates the marginal contribution of each feature value across all possible feature coalitions, providing both local explanations (per-prediction feature attributions) and global explanations (overall feature importance across all predictions). By treating features as "players" in a cooperative game where the "payout" is the prediction, SHAP values offer theoretically sound, consistent, and interpretable explanations that satisfy desirable properties including local accuracy, missingness, and consistency.

The algorithm computes Shapley values by considering all possible subsets of features and measuring how much each feature contributes when added to different feature combinations. For each prediction, TD_SHAP outputs SHAP values for every input feature, where positive values indicate the feature pushed the prediction higher, negative values indicate it pushed the prediction lower, and the magnitude represents the strength of influence. The sum of all SHAP values plus the base prediction equals the final model prediction, ensuring complete attribution of the prediction to individual features. The secondary output provides mean absolute SHAP values across all samples, serving as a global measure of feature importance that ranks features by their average impact on predictions across the dataset.

TD_SHAP supports three major model types: TD_GLM (Generalized Linear Models), TD_DecisionForest (Random Forests), and TD_XGBoost (Gradient Boosted Trees), enabling explainability for both linear and complex non-linear models. For linear models, SHAP computation is fast and exact, directly calculating feature contributions from coefficients. For tree-based models, TD_SHAP uses TreeSHAP, an efficient algorithm that computes exact SHAP values by traversing decision trees and aggregating contributions across all trees in the ensemble. However, TreeSHAP is computationally intensive with complexity proportional to tree depth, number of trees, and dataset size - for large tree ensembles, users should run TD_SHAP on a representative subset of test data. The Detailed parameter enables per-tree SHAP values for fine-grained analysis, while the standard output provides aggregated SHAP values suitable for most explainability use cases.

### When the Function Would Be Used
- **Model Interpretability**: Explain why a model made specific predictions for individual samples
- **Feature Importance Analysis**: Identify which features drive model decisions globally
- **Regulatory Compliance**: Provide explainability for models in regulated industries (finance, healthcare)
- **Model Debugging**: Diagnose unexpected predictions by examining feature contributions
- **Trust Building**: Increase stakeholder confidence by making black-box models transparent
- **Fairness Auditing**: Detect if sensitive attributes inappropriately influence predictions
- **Clinical Decision Support**: Explain medical diagnoses or treatment recommendations
- **Credit Decisioning**: Provide reasons for loan approvals or rejections (FCRA compliance)
- **Fraud Investigation**: Understand which features flagged a transaction as fraudulent
- **Customer Churn Analysis**: Identify factors driving individual customer churn predictions
- **Model Comparison**: Compare feature importance across different model architectures
- **Feature Engineering Validation**: Verify that engineered features contribute as expected
- **Anomaly Explanation**: Explain why specific instances were flagged as anomalous
- **Risk Assessment**: Decompose risk scores into individual risk factor contributions
- **Predictive Maintenance**: Identify which sensor readings predict equipment failure
- **Marketing Attribution**: Understand which customer attributes predict conversion
- **Quality Control**: Explain why products were classified as defective
- **Scientific Research**: Interpret ML models in biology, chemistry, physics research
- **Business Insights**: Generate actionable insights from model feature contributions
- **Model Validation**: Confirm models use domain-appropriate features for decisions
- **Sensitivity Analysis**: Understand how prediction changes with feature perturbations
- **Documentation**: Create audit trails for model decisions and predictions
- **Education**: Teach stakeholders how ML models make decisions
- **Algorithm Selection**: Choose models based on interpretability requirements

### Syntax

```sql
TD_SHAP (
    ON { table | view | (query) } AS InputTable
    ON { table | view | (query) } AS ModelTable DIMENSION
    OUT [PERMANENT | VOLATILE] TABLE GlobalExplanation (global_explanation_table)
    USING
    IDColumn ('id_column')
    TrainingFunction ({'td_glm' | 'td_decisionforest' | 'td_xgboost'})
    InputColumns ({ 'input_column' | input_column_range }[,...])
    [ ModelType ({'regression' | 'classification'}) ]
    [ Detailed ({'true' | 't' | 'yes' | 'y' | '1' | 'false' | 'f' | 'no' | 'n' | '0'}) ]
    [ Accumulate ({ 'column' | column_range }[,...]) ]
    [ NumParallelTrees (number_of_trees) ]
    [ NumBoostRounds (iteration_number) ]
) AS alias
```

### Required Syntax Elements for TD_SHAP

**ON clause (InputTable)**
- Test/prediction data for which to compute SHAP explanations
- Should be a representative sample (small subset for tree models)
- Contains feature values and identifier column

**ON clause (ModelTable DIMENSION)**
- Trained model table from TD_GLM, TD_DecisionForest, or TD_XGBoost
- DIMENSION: model replicated to all AMPs for SHAP computation
- Model structure determines SHAP computation method

**OUT TABLE GlobalExplanation**
- Secondary output table for global feature importance
- Contains mean absolute SHAP values per feature
- Provides overall feature ranking across all predictions
- Can be PERMANENT or VOLATILE

**IDColumn**
- Column uniquely identifying each input sample
- Used to match SHAP values to original predictions
- Any data type (INTEGER, VARCHAR, etc.)

**TrainingFunction**
- Specifies which model type created the model
- **'td_glm'**: Linear/logistic regression models
  - Fast SHAP computation (closed-form solution)
  - Exact SHAP values
- **'td_decisionforest'**: Decision forest/random forest models
  - TreeSHAP algorithm for exact SHAP values
  - Computationally intensive for large ensembles
- **'td_xgboost'**: Gradient boosted tree models
  - TreeSHAP algorithm
  - Most computationally intensive due to many trees
- Must match the actual training function used

**InputColumns**
- Feature columns for which to compute SHAP values
- Must exactly match columns used to train the model
- Column names and case must be identical to training
- Supports column range notation ('[1:10]')

### Optional Syntax Elements for TD_SHAP

**ModelType**
- Type of model task
- **'regression'**: Continuous predictions (SHAP values in prediction units)
- **'classification'**: Categorical predictions (SHAP values per class)
- Default: 'regression'

**Detailed**
- Whether to output per-tree SHAP values (tree-based models only)
- **'true'**: Output SHAP contribution from each individual tree
  - Enables fine-grained analysis of tree contributions
  - Output includes tree_num and iter_num columns
  - Final aggregated SHAP has tree_num = "FINAL"
  - Dramatically increases output size
- **'false'**: Output only aggregated SHAP values
  - Standard output for most use cases
  - One row per sample per class (classification) or per sample (regression)
- Default: 'false'
- Only applicable for TD_DecisionForest and TD_XGBoost

**Accumulate**
- Columns from InputTable to copy to output unchanged
- Useful for preserving labels, metadata, timestamps
- Enables joining SHAP values back to original data

**NumParallelTrees**
- Number of boosted trees to use for SHAP computation
- Only applicable for TD_XGBoost models
- Limits trees evaluated to control computation time
- Range: [1, total_trees_in_model]
- Default: 1000

**NumBoostRounds**
- Number of boosting iterations to use
- Only applicable for TD_XGBoost models
- Range: [1, 100000]
- Default: 3

### Input Table Schemas

**InputTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| id_column | ANY | Unique identifier for each sample |
| input_column | NUMERIC (INTEGER, BIGINT, SMALLINT, BYTEINT, FLOAT, DECIMAL, NUMBER) | Feature columns (must match model training columns exactly) |
| accumulate_column | ANY | [Optional] Columns to preserve in output |

**Important:** Column names must exactly match (including case) the columns used during model training.

**ModelTable Schema:**
- Same as output from TD_GLM, TD_DecisionForest, or TD_XGBoost
- See respective function documentation for model table structure

### Output Table Schemas

**Primary OutputTable Schema (Local Explanations):**

| Column | Data Type | Description |
|--------|-----------|-------------|
| id | INTEGER | Unique identifier from InputTable |
| accumulate_column | ANY | Columns copied from InputTable |
| input_column_shap | DOUBLE PRECISION | SHAP value for each input feature (one column per feature) |
| label | INTEGER | Class label (classification models only) |
| tree_num | VARCHAR | Tree identifier (only when Detailed='true' for tree models) |
| iter_num | INTEGER | Iteration number (only when Detailed='true' for XGBoost) |

**SHAP Value Interpretation:**
- Positive SHAP value: Feature increases prediction
- Negative SHAP value: Feature decreases prediction
- Magnitude: Strength of feature's influence
- Sum of all SHAP values + base value = final prediction

**Secondary OutputTable Schema (Global Explanations):**

| Column | Data Type | Description |
|--------|-----------|-------------|
| input_column | DOUBLE PRECISION | Mean absolute SHAP value for each feature |
| label | INTEGER | Class label (only for TD_DecisionForest and TD_XGBoost classification) |

**Global Importance:** Features ranked by mean absolute SHAP value indicate overall feature importance across all predictions.

### Code Examples

**Example 1: Basic SHAP Explanation for GLM Regression**
```sql
-- Step 1: Train GLM regression model
CREATE VOLATILE TABLE regression_model AS (
    SELECT * FROM TD_GLM (
        ON housing_train AS InputTable PARTITION BY ANY
        USING
        InputColumns('sqft', 'bedrooms', 'age', 'location_score')
        ResponseColumn('price')
        Family('Gaussian')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 2: Compute SHAP values on test set
CREATE VOLATILE TABLE shap_output AS (
    SELECT * FROM TD_SHAP (
        ON housing_test AS InputTable
        ON regression_model AS ModelTable DIMENSION
        OUT VOLATILE TABLE GlobalExplanation(global_importance)
        USING
        IDColumn('house_id')
        TrainingFunction('td_glm')
        InputColumns('sqft', 'bedrooms', 'age', 'location_score')
        ModelType('regression')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- View local explanations (per-house SHAP values)
SELECT
    id AS house_id,
    td_sqft_shap AS sqft_contribution,
    td_bedrooms_shap AS bedrooms_contribution,
    td_age_shap AS age_contribution,
    td_location_score_shap AS location_contribution
FROM shap_output
ORDER BY id
LIMIT 10;

-- View global feature importance
SELECT * FROM global_importance
ORDER BY sqft DESC;  -- Ranking by absolute importance
```

**Example 2: SHAP for Binary Classification (Churn Prediction)**
```sql
-- Train XGBoost binary classifier
CREATE VOLATILE TABLE churn_model AS (
    SELECT * FROM TD_XGBoost (
        ON customer_train AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('churned')
        InputColumns('tenure', 'monthly_charges', 'support_calls', 'contract_type')
        NumBoostRounds(50)
        MaxDepth(5)
        Objective('BINARY')
        Seed(42)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Compute SHAP values for test customers
CREATE VOLATILE TABLE churn_shap AS (
    SELECT * FROM TD_SHAP (
        ON customer_test_sample AS InputTable  -- Small sample for tree models
        ON churn_model AS ModelTable DIMENSION
        OUT VOLATILE TABLE GlobalExplanation(churn_global_shap)
        USING
        IDColumn('customer_id')
        TrainingFunction('td_xgboost')
        InputColumns('tenure', 'monthly_charges', 'support_calls', 'contract_type')
        ModelType('classification')
        NumBoostRounds(50)
        Accumulate('customer_name', 'actual_churned')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Analyze why specific customers predicted to churn
SELECT
    customer_id,
    customer_name,
    td_tenure_shap,
    td_monthly_charges_shap,
    td_support_calls_shap,
    td_contract_type_shap
FROM churn_shap
WHERE label = 1  -- Churn class
  AND actual_churned = 1  -- Actually churned
ORDER BY ABS(td_support_calls_shap) DESC
LIMIT 10;

-- Global feature importance for churn
SELECT * FROM churn_global_shap
WHERE label = 1
ORDER BY tenure DESC;  -- Most important features for churn
```

**Example 3: Multi-Class Classification with Decision Forest**
```sql
-- Train decision forest for iris classification
CREATE VOLATILE TABLE iris_model AS (
    SELECT * FROM TD_DecisionForest (
        ON iris_train AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('species')  -- 3 classes: setosa, versicolor, virginica
        InputColumns('sepal_length', 'sepal_width', 'petal_length', 'petal_width')
        NumTrees(100)
        MaxDepth(10)
        Seed(42)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Compute SHAP for small test subset
CREATE VOLATILE TABLE iris_shap AS (
    SELECT * FROM TD_SHAP (
        ON iris_test_small AS InputTable  -- Use small sample (10-50 rows)
        ON iris_model AS ModelTable DIMENSION
        OUT VOLATILE TABLE GlobalExplanation(iris_feature_importance)
        USING
        IDColumn('id')
        TrainingFunction('td_decisionforest')
        InputColumns('sepal_length', 'sepal_width', 'petal_length', 'petal_width')
        ModelType('classification')
        Accumulate('species')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Analyze SHAP values for each class
SELECT
    id,
    label,  -- Class: 0=setosa, 1=versicolor, 2=virginica
    species,
    td_petal_length_shap AS petal_length_impact,
    td_petal_width_shap AS petal_width_impact,
    td_sepal_length_shap AS sepal_length_impact,
    td_sepal_width_shap AS sepal_width_impact
FROM iris_shap
WHERE id = 5  -- Analyze one specific prediction across all classes
ORDER BY label;

-- Global feature importance per class
SELECT * FROM iris_feature_importance
ORDER BY label, petal_length DESC;
```

**Example 4: Detailed Tree-Level SHAP Analysis**
```sql
-- Compute detailed SHAP showing contribution from each tree
CREATE VOLATILE TABLE detailed_shap AS (
    SELECT * FROM TD_SHAP (
        ON fraud_test_sample AS InputTable
        ON fraud_xgboost_model AS ModelTable DIMENSION
        OUT VOLATILE TABLE GlobalExplanation(fraud_global)
        USING
        IDColumn('transaction_id')
        TrainingFunction('td_xgboost')
        InputColumns('amount', 'merchant_category', 'time_of_day', 'location')
        ModelType('classification')
        NumBoostRounds(10)
        Detailed('true')  -- Per-tree SHAP values
        Accumulate('is_fraud')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- View SHAP contribution from each tree
SELECT
    id,
    tree_num,  -- Individual tree identifier
    iter_num,  -- Boosting iteration
    label,     -- Class
    td_amount_shap
FROM detailed_shap
WHERE id = 12345  -- Specific transaction
  AND label = 1   -- Fraud class
ORDER BY tree_num;

-- View final aggregated SHAP (tree_num = 'FINAL')
SELECT
    id,
    td_amount_shap AS amount_contribution,
    td_merchant_category_shap AS merchant_contribution,
    td_time_of_day_shap AS time_contribution,
    td_location_shap AS location_contribution
FROM detailed_shap
WHERE tree_num = 'FINAL'
  AND label = 1
ORDER BY id;
```

**Example 5: Credit Scoring Explainability**
```sql
-- Train GLM for credit approval
CREATE VOLATILE TABLE credit_model AS (
    SELECT * FROM TD_GLM (
        ON credit_applications AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('approved')
        InputColumns('income', 'credit_score', 'debt_ratio', 'employment_years')
        Family('Binomial')
        RegularizationLambda(0.01)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Compute SHAP for rejected applications (explainability requirement)
CREATE VOLATILE TABLE rejection_explanations AS (
    SELECT * FROM TD_SHAP (
        ON rejected_applications AS InputTable
        ON credit_model AS ModelTable DIMENSION
        OUT VOLATILE TABLE GlobalExplanation(credit_feature_importance)
        USING
        IDColumn('application_id')
        TrainingFunction('td_glm')
        InputColumns('income', 'credit_score', 'debt_ratio', 'employment_years')
        ModelType('classification')
        Accumulate('applicant_name', 'approved')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Generate adverse action notices (FCRA compliance)
SELECT
    application_id,
    applicant_name,
    CASE
        WHEN td_credit_score_shap < 0 THEN 'Low credit score negatively impacted decision'
        WHEN td_debt_ratio_shap < 0 THEN 'High debt-to-income ratio negatively impacted decision'
        WHEN td_income_shap < 0 THEN 'Income level negatively impacted decision'
        WHEN td_employment_years_shap < 0 THEN 'Short employment history negatively impacted decision'
    END AS primary_reason_for_rejection,
    td_credit_score_shap,
    td_debt_ratio_shap,
    td_income_shap,
    td_employment_years_shap
FROM rejection_explanations
WHERE label = 0  -- Rejection class
ORDER BY application_id;
```

**Example 6: Model Debugging with SHAP**
```sql
-- Identify unexpected predictions using SHAP
WITH predictions AS (
    SELECT * FROM TD_XGBoostPredict (
        ON test_data AS InputTable PARTITION BY ANY
        ON quality_model AS ModelTable DIMENSION
        USING
        IDColumn('product_id')
        Accumulate('actual_quality', 'expected_quality')
    ) AS dt
),
unexpected AS (
    SELECT product_id
    FROM predictions
    WHERE prediction != expected_quality  -- Unexpected predictions
)
-- Explain unexpected predictions
SELECT
    s.id AS product_id,
    s.label AS predicted_class,
    s.td_dimension1_shap,
    s.td_dimension2_shap,
    s.td_dimension3_shap,
    s.td_weight_shap,
    s.td_hardness_shap
FROM TD_SHAP (
    ON test_data AS InputTable
    ON quality_model AS ModelTable DIMENSION
    OUT VOLATILE TABLE GlobalExplanation(quality_global)
    USING
    IDColumn('product_id')
    TrainingFunction('td_xgboost')
    InputColumns('dimension1', 'dimension2', 'dimension3', 'weight', 'hardness')
    ModelType('classification')
    NumBoostRounds(50)
) AS s
INNER JOIN unexpected u ON s.id = u.product_id
ORDER BY s.id, s.label;

-- Debug: Which features drive unexpected predictions?
```

**Example 7: Fairness Auditing with SHAP**
```sql
-- Check if sensitive attributes (e.g., gender, race) inappropriately influence predictions
CREATE VOLATILE TABLE hiring_shap AS (
    SELECT * FROM TD_SHAP (
        ON hiring_test AS InputTable
        ON hiring_model AS ModelTable DIMENSION
        OUT VOLATILE TABLE GlobalExplanation(hiring_global)
        USING
        IDColumn('candidate_id')
        TrainingFunction('td_decisionforest')
        InputColumns('experience_years', 'education_level', 'skills_score',
                     'gender_code', 'race_code')  -- Include sensitive attributes
        ModelType('classification')
        Accumulate('gender', 'race', 'hired')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Audit: Check if sensitive attributes have large SHAP values
SELECT
    AVG(ABS(td_gender_code_shap)) AS avg_gender_impact,
    AVG(ABS(td_race_code_shap)) AS avg_race_impact,
    AVG(ABS(td_experience_years_shap)) AS avg_experience_impact,
    AVG(ABS(td_skills_score_shap)) AS avg_skills_impact
FROM hiring_shap
WHERE label = 1;  -- Hired class

-- Flag if sensitive attributes have high impact
-- If avg_gender_impact or avg_race_impact is high, model may be discriminatory
```

**Example 8: Comparing Models with SHAP**
```sql
-- Compare feature importance between two models
-- Model 1: Decision Forest
CREATE VOLATILE TABLE model1_shap AS (
    SELECT * FROM TD_SHAP (
        ON validation_sample AS InputTable
        ON decisionforest_model AS ModelTable DIMENSION
        OUT VOLATILE TABLE GlobalExplanation(df_global_shap)
        USING
        IDColumn('id')
        TrainingFunction('td_decisionforest')
        InputColumns('feature1', 'feature2', 'feature3', 'feature4')
        ModelType('regression')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Model 2: XGBoost
CREATE VOLATILE TABLE model2_shap AS (
    SELECT * FROM TD_SHAP (
        ON validation_sample AS InputTable
        ON xgboost_model AS ModelTable DIMENSION
        OUT VOLATILE TABLE GlobalExplanation(xgb_global_shap)
        USING
        IDColumn('id')
        TrainingFunction('td_xgboost')
        InputColumns('feature1', 'feature2', 'feature3', 'feature4')
        ModelType('regression')
        NumBoostRounds(50)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Compare global feature importance
SELECT
    'DecisionForest' AS model,
    feature1 AS feature1_importance,
    feature2 AS feature2_importance,
    feature3 AS feature3_importance,
    feature4 AS feature4_importance
FROM df_global_shap
UNION ALL
SELECT
    'XGBoost' AS model,
    feature1,
    feature2,
    feature3,
    feature4
FROM xgb_global_shap;

-- Identifies if models rely on different features for predictions
```

**Example 9: Medical Diagnosis Explanation**
```sql
-- Explain disease diagnosis predictions
CREATE VOLATILE TABLE diagnosis_shap AS (
    SELECT * FROM TD_SHAP (
        ON patient_test_data AS InputTable
        ON diagnosis_model AS ModelTable DIMENSION
        OUT VOLATILE TABLE GlobalExplanation(diagnosis_feature_importance)
        USING
        IDColumn('patient_id')
        TrainingFunction('td_decisionforest')
        InputColumns('temperature', 'blood_pressure', 'heart_rate', 'glucose',
                     'cholesterol', 'age', 'bmi')
        ModelType('classification')
        Accumulate('patient_name', 'diagnosis')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Generate patient-specific diagnosis explanation
SELECT
    patient_id,
    patient_name,
    CASE label
        WHEN 0 THEN 'Healthy'
        WHEN 1 THEN 'Type 1 Diabetes'
        WHEN 2 THEN 'Type 2 Diabetes'
    END AS predicted_diagnosis,
    diagnosis AS actual_diagnosis,
    td_glucose_shap AS glucose_contribution,
    td_bmi_shap AS bmi_contribution,
    td_age_shap AS age_contribution,
    td_blood_pressure_shap AS bp_contribution
FROM diagnosis_shap
WHERE patient_id = 12345
ORDER BY label;

-- Clinician can understand which biomarkers drove the diagnosis
```

**Example 10: Feature Engineering Validation**
```sql
-- Validate that engineered features contribute as expected
-- Step 1: Train model with original + engineered features
CREATE VOLATILE TABLE model_with_features AS (
    SELECT * FROM TD_XGBoost (
        ON data_with_features AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('target')
        InputColumns('original_f1', 'original_f2', 'original_f3',
                     'engineered_interaction', 'engineered_polynomial')
        NumBoostRounds(30)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 2: Compute SHAP to check engineered feature contributions
CREATE VOLATILE TABLE feature_shap AS (
    SELECT * FROM TD_SHAP (
        ON test_sample AS InputTable
        ON model_with_features AS ModelTable DIMENSION
        OUT VOLATILE TABLE GlobalExplanation(feature_global_shap)
        USING
        IDColumn('id')
        TrainingFunction('td_xgboost')
        InputColumns('original_f1', 'original_f2', 'original_f3',
                     'engineered_interaction', 'engineered_polynomial')
        ModelType('regression')
        NumBoostRounds(30)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Check if engineered features are important
SELECT * FROM feature_global_shap
ORDER BY engineered_interaction DESC;

-- If engineered features have low importance, consider removing them
```

### Algorithm Details

**SHAP (Shapley Values) Mathematical Foundation:**

SHAP values are based on Shapley values from cooperative game theory. For feature i and prediction f(x):

```
φᵢ = Σ (|S|! × (M - |S| - 1)!) / M! × [f(S ∪ {i}) - f(S)]
     S⊆F\{i}

Where:
- φᵢ: SHAP value for feature i
- F: Set of all features
- S: Subset of features not including i
- M: Total number of features
- f(S): Model prediction using only features in S
- f(S ∪ {i}): Prediction when feature i is added to S
```

**Interpretation:**
- φᵢ: Average marginal contribution of feature i across all possible feature coalitions
- Positive φᵢ: Feature increases prediction above base value
- Negative φᵢ: Feature decreases prediction below base value
- |φᵢ|: Magnitude of feature's influence

**SHAP Properties:**

1. **Local Accuracy (Additivity):**
   ```
   f(x) = φ₀ + Σᵢ φᵢ

   Where φ₀ is the base value (average prediction)
   Sum of all SHAP values equals prediction deviation from base
   ```

2. **Missingness:**
   ```
   If feature i is missing: φᵢ = 0
   ```

3. **Consistency:**
   ```
   If f'(S ∪ {i}) - f'(S) ≥ f(S ∪ {i}) - f(S) for all S,
   then φᵢ(f') ≥ φᵢ(f)

   If a feature contributes more, its SHAP value increases
   ```

**SHAP for Linear Models (TD_GLM):**

For linear model f(x) = β₀ + Σᵢ βᵢxᵢ:

```
φᵢ = βᵢ × (xᵢ - E[xᵢ])

Where:
- βᵢ: Model coefficient for feature i
- xᵢ: Feature value
- E[xᵢ]: Expected value (mean) of feature i in training data

Base value: φ₀ = β₀ + Σᵢ βᵢ × E[xᵢ]
```

**Linear SHAP is exact and computationally efficient (O(M) complexity).**

**TreeSHAP for Tree-Based Models:**

For decision trees and ensembles (TD_DecisionForest, TD_XGBoost):

```
Algorithm TreeSHAP:
1. For each tree in ensemble:
   a. Traverse all paths from root to leaves
   b. For each feature split:
      - Compute cover (samples reaching split)
      - Compute contribution to prediction change
   c. Aggregate contributions across all paths
2. Sum SHAP values across all trees

Complexity: O(T × L × D²)
Where:
- T: Number of trees
- L: Number of leaves per tree
- D: Tree depth
```

**TreeSHAP efficiently computes exact SHAP values for trees without enumerating all 2^M feature coalitions.**

**Global Feature Importance:**

```
Mean Absolute SHAP Value for feature i:
SHAP_importance_i = (1/N) × Σⱼ |φᵢ(xⱼ)|

Where:
- N: Number of samples
- xⱼ: Sample j
- φᵢ(xⱼ): SHAP value for feature i on sample j

Features ranked by mean absolute SHAP → global feature importance
```

**Computational Complexity:**

```
TD_GLM (Linear):
- Time: O(N × M) where N=samples, M=features
- Space: O(N × M)
- Fast, scales to large datasets

TD_DecisionForest / TD_XGBoost (Trees):
- Time: O(N × T × L × D²)
- Space: O(N × M × T)
- Intensive, use small sample (100-1000 rows)

Where:
- T: Number of trees (hundreds to thousands)
- L: Average number of leaves per tree
- D: Average tree depth
```

### Use Cases and Applications

**1. Regulatory Compliance and Audit**
- Fair Credit Reporting Act (FCRA) adverse action notices
- Equal Credit Opportunity Act (ECOA) compliance
- General Data Protection Regulation (GDPR) "right to explanation"
- Model Risk Management (MRM) documentation
- Sarbanes-Oxley (SOX) audit trails

**2. Healthcare and Medical AI**
- Explain clinical decision support system recommendations
- Justify diagnosis predictions to physicians
- Identify biomarkers driving disease predictions
- Validate medical AI models with domain experts
- Support personalized treatment decisions

**3. Financial Services**
- Credit decisioning explanations
- Loan approval/rejection reasons
- Fraud detection justifications
- Risk score decomposition
- Algorithmic trading strategy analysis

**4. Model Development and Debugging**
- Identify unexpected feature contributions
- Debug poor predictions
- Validate model behavior matches domain knowledge
- Compare feature importance across model iterations
- Diagnose data leakage or spurious correlations

**5. Fairness and Bias Detection**
- Audit for discriminatory patterns
- Detect if sensitive attributes drive predictions
- Compare SHAP values across demographic groups
- Identify proxy variables for protected attributes
- Support algorithmic fairness improvements

**6. Business Insights and Decision Support**
- Understand customer churn drivers
- Identify factors influencing conversions
- Analyze pricing sensitivity
- Decompose customer lifetime value predictions
- Generate actionable insights from predictions

**7. Scientific Research**
- Interpret ML models in biology, chemistry, physics
- Identify important variables in scientific phenomena
- Validate hypotheses with feature importance
- Explain predictions to peer reviewers
- Generate new research directions from feature contributions

**8. Customer-Facing Explanations**
- Personalized product recommendations with reasons
- Dynamic pricing explanations
- Insurance premium justifications
- Content recommendation reasons
- Search result ranking explanations

**9. Marketing and Sales**
- Lead scoring explanations
- Customer segmentation insights
- Campaign response factor analysis
- Product recommendation reasons
- Churn risk factor identification

**10. Quality Control and Manufacturing**
- Explain product defect predictions
- Identify root causes of quality issues
- Understand process parameter influences
- Justify predictive maintenance alerts
- Optimize manufacturing processes

### Important Notes

**Computational Intensity for Tree Models:**
- TreeSHAP complexity: O(N × T × L × D²)
- For large forests (T > 100 trees), computation is **extremely slow**
- **CRITICAL: Use small sample** (10-1000 rows) for tree-based models
- For XGBoost with 100 rounds, expect minutes to hours per sample
- Consider subsetting test data before SHAP computation

**Column Name Matching:**
- InputColumns must **exactly match** training column names (case-sensitive)
- Mismatched names cause errors or incorrect SHAP values
- Verify column names before running TD_SHAP
- Use same feature order as training for consistency

**Model Type Selection:**
- Must match actual model task (regression vs classification)
- Incorrect ModelType produces nonsensical SHAP values
- Classification models output SHAP values per class
- Regression models output single SHAP value per sample

**Memory Considerations:**
- ModelTable DIMENSION: entire model copied to each AMP
- Large tree ensembles (>1000 trees) may cause memory issues
- Detailed='true' dramatically increases output size
- Use VOLATILE tables to avoid permanent storage of large outputs
- Monitor spool space usage for large SHAP computations

**SHAP Value Interpretation:**
- SHAP values are in **same units as model predictions**
  - Regression: SHAP in target variable units (e.g., dollars, years)
  - Classification: SHAP in log-odds or probability space
- Positive SHAP: Feature pushes prediction higher
- Negative SHAP: Feature pushes prediction lower
- Sum(SHAP values) + base value = final prediction

**Global vs Local Explanations:**
- **Local**: Per-sample SHAP values (primary output)
  - Explains individual predictions
  - Different SHAP values for each sample
- **Global**: Mean absolute SHAP (secondary output)
  - Overall feature importance
  - Averaged across all samples
  - Does not capture feature interactions

**Feature Interactions:**
- SHAP values capture main effects but not interactions explicitly
- High SHAP value may result from interaction with other features
- Use SHAP interaction values (not in TD_SHAP) for explicit interactions
- Detailed analysis requires examining SHAP values across multiple samples

**Base Value and Expected Value:**
- Base value = average prediction on training data
- SHAP values are deviations from this base
- Final prediction = base value + sum(SHAP values)
- Base value not explicitly returned by TD_SHAP

**Limitations:**
- Does not explain **why** feature has certain value (only contribution given value)
- Assumes features are independent (may not reflect real dependencies)
- Computationally expensive for tree models
- Requires trained model (cannot explain model-free decisions)
- SHAP values are approximations for some model types (exact for GLM and trees)

**NumParallelTrees and NumBoostRounds:**
- Only for TD_XGBoost models
- Must match or be ≤ values used during training
- Reducing trees speeds computation but may reduce accuracy
- Use full model (all trees) for production explanations

### Best Practices

**1. Use Representative Sample for Tree Models**
- TreeSHAP is O(N × T × L × D²) - very expensive
- Sample 100-1000 rows from test set for SHAP computation
- Use stratified sampling to maintain class distribution
- Avoid SHAP on entire test set for large forests
- Profile computation time on small subset first

**2. Verify Column Names Match Training**
- Use exact column names (case-sensitive) from model training
- Query model metadata to confirm feature names
- Document feature names in model training code
- Use same column ordering as training for clarity
- Test SHAP on single sample before full computation

**3. Start with Detailed='false'**
- Detailed output is massive and rarely needed
- Use Detailed='true' only for debugging or research
- Aggregate SHAP (Detailed='false') sufficient for most use cases
- Per-tree SHAP useful for understanding ensemble contributions
- Save storage space with standard output

**4. Leverage Global Explanations**
- Always use OUT TABLE GlobalExplanation
- Provides overall feature importance ranking
- Cheaper to compute than local explanations
- Use for feature selection and model simplification
- Compare global importance across models

**5. Validate SHAP Values Make Sense**
- Check if SHAP values match domain expectations
- Verify sum(SHAP) + base ≈ prediction (additivity property)
- Inspect SHAP values for known samples
- Compare SHAP with other feature importance methods
- Flag suspicious SHAP patterns for investigation

**6. Use VOLATILE Tables for SHAP Output**
- SHAP output can be very large (especially Detailed='true')
- VOLATILE tables automatically cleaned up
- Reduces permanent storage usage
- Export only summary statistics permanently
- Process SHAP output in same session

**7. Combine SHAP with Domain Knowledge**
- SHAP is data-driven but not omniscient
- Validate feature contributions with domain experts
- Use SHAP to confirm or challenge assumptions
- Identify counterintuitive patterns for investigation
- Don't blindly trust SHAP without domain validation

**8. Document and Archive SHAP Results**
- Save SHAP explanations for audit trails
- Document when SHAP was computed and on which data
- Store representative SHAP examples for model documentation
- Include SHAP in model cards and documentation
- Maintain version control for SHAP outputs

**9. Monitor SHAP Over Time**
- Periodically recompute SHAP on new data
- Check if feature importance shifts (concept drift)
- Flag significant changes in SHAP patterns
- Update stakeholder communications if importance changes
- Retrain model if SHAP reveals issues

**10. Production Deployment Strategy**
- Precompute SHAP for common scenarios
- Cache SHAP values for frequently accessed samples
- Use GLM when real-time explanations needed (fast SHAP)
- For tree models, compute SHAP offline in batches
- Provide approximate explanations for real-time systems
- Balance explanation accuracy vs latency requirements

### Related Functions

**Model Training (Models Supported by TD_SHAP):**
- **TD_GLM** - Generalized Linear Models (fast exact SHAP)
- **TD_DecisionForest** - Random Forest (TreeSHAP)
- **TD_XGBoost** - Gradient Boosting (TreeSHAP)

**Model Evaluation:**
- **TD_ClassificationEvaluator** - Classification metrics (accuracy, precision, recall, F1)
- **TD_RegressionEvaluator** - Regression metrics (MSE, MAE, R²)
- **TD_ROC** - ROC curves and AUC for binary classification
- **TD_Silhouette** - Clustering quality evaluation

**Model Scoring (Generate Predictions for SHAP):**
- **TD_GLMPredict** - Predictions from TD_GLM models
- **TD_DecisionForestPredict** - Predictions from forest models
- **TD_XGBoostPredict** - Predictions from XGBoost models

**Data Preparation:**
- **TD_TrainTestSplit** - Split data for model training and SHAP evaluation
- **TD_ScaleFit** - Standardize features before model training
- **TD_SimpleImputeFit** - Handle missing values

**Feature Engineering:**
- **TD_OneHotEncodingFit** - Encode categorical features for models
- **TD_Bin** - Discretize continuous features for interpretability
- **TD_PolynomialFeatures** - Create interaction features

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf
- [SHAP (SHapley Additive exPlanations) - GitHub](https://github.com/slundberg/shap)
- [Lundberg & Lee (2017) - A Unified Approach to Interpreting Model Predictions](https://arxiv.org/abs/1705.07874)
- [Interpretable Machine Learning Book - Christoph Molnar](https://christophm.github.io/interpretable-ml-book/shap.html)
- [TreeSHAP Algorithm Paper](https://arxiv.org/abs/1802.03888)

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Model Evaluation Functions (Explainable AI)
