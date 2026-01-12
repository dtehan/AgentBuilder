# TD_SVMPredict

## Function Name
**TD_SVMPredict** - Support Vector Machine Prediction

**Aliases:** SVMPredict

## Description

TD_SVMPredict applies a trained Support Vector Machine (SVM) model to new data for classification. SVM is a powerful supervised learning algorithm that finds an optimal hyperplane to separate classes in high-dimensional feature space. Using the "kernel trick," SVM can efficiently handle non-linear decision boundaries, making it effective for complex classification problems where classes are not linearly separable.

**Key Characteristics:**
- **Binary & Multi-Class Classification**: Supports both two-class and multi-class problems
- **Non-Linear Decision Boundaries**: Kernel methods (RBF, polynomial) enable complex separations
- **Maximum Margin Classification**: Finds decision boundary that maximizes separation between classes
- **Robust to High Dimensions**: Performs well even when features >> samples
- **Support Vector-Based**: Model defined by critical examples (support vectors) on class boundaries
- **Production-Ready**: Optimized for batch scoring large datasets

The function takes a trained SVM model (from TD_SVM) and predicts class labels for new observations based on learned decision boundaries.

## When to Use TD_SVMPredict

**Business Applications:**
- **Credit Risk Classification**: Approve/reject loan applications based on applicant features
- **Image Classification**: Categorize images (handwritten digits, medical scans, product photos)
- **Medical Diagnosis**: Classify patients as healthy/diseased based on clinical variables
- **Customer Churn**: Predict which customers will churn based on behavior patterns
- **Fraud Detection**: Classify transactions as fraudulent or legitimate
- **Text Classification**: Document categorization, spam filtering (with text features)
- **Quality Control**: Classify products as pass/fail based on inspection measurements
- **Marketing Response**: Predict customer response to campaigns

**Use TD_SVMPredict When You Need To:**
- Apply a trained SVM model to new observations
- Score test data for model evaluation
- Perform production classification with high accuracy
- Handle non-linearly separable classes
- Work with high-dimensional feature spaces
- Obtain robust predictions with limited training data

**Analytical Use Cases:**
- Model validation on hold-out test sets
- Real-time classification in production pipelines
- A/B testing with propensity scores
- Customer segmentation and targeting
- Risk scoring and stratification

## Syntax

```sql
SELECT * FROM TD_SVMPredict (
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
- All feature columns used during model training (same names and types)
- ID column for row identification
- Numeric features (SVM operates on continuous variables)

### ModelTable (DIMENSION)
The trained SVM model table produced by TD_SVM function. Contains:
- Support vectors (training examples on decision boundary)
- Dual coefficients for each support vector
- Kernel specification and parameters (type, gamma, degree, coef0)
- Intercept term
- Class labels

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
Accumulate('customer_id', 'customer_name', 'application_date')
```

### OutputProb
**For Binary Classification**: Whether to output predicted probabilities for each class.

**Values:**
- `'true'`: Include probability columns (prob_class0, prob_class1)
- `'false'`: Output only predicted class (default)

**Syntax:** `OutputProb('true')`

**Note:** For SVM, probabilities are estimated using Platt scaling or decision function distances.

**Example:**
```sql
OutputProb('true')
```

### Responses
Specifies the class labels in the order corresponding to probability columns when OutputProb is true.

**Syntax:** `Responses('class1', 'class2', ...)`

**Example:**
```sql
Responses('approve', 'reject')  -- For binary classification
Responses('low', 'medium', 'high')  -- For multi-class
```

## Input Schema

### InputTable
| Column | Data Type | Description |
|--------|-----------|-------------|
| id_column | INTEGER, VARCHAR | Unique identifier for each row |
| feature_1 | NUMERIC | First predictor variable (same as training) |
| feature_2 | NUMERIC | Second predictor variable (same as training) |
| ... | NUMERIC | Additional predictors (must match training data) |
| accumulate_cols | ANY | Optional columns to pass through |

**Requirements:**
- All feature columns from training must be present
- Column names must match training data exactly
- Numeric data types for features
- No NULL values in features (handle missing values before prediction)
- Features should be scaled if scaling was applied during training

### ModelTable
Standard output from TD_SVM function containing:
- Support vectors
- Dual coefficients (alpha values)
- Kernel specification (RBF, linear, polynomial, sigmoid)
- Kernel parameters (gamma, degree, coef0)
- Intercept (bias term)
- Class labels

## Output Schema

### Standard Output (OutputProb = 'false')
| Column | Data Type | Description |
|--------|-----------|-------------|
| id_column | Same as input | Row identifier from InputTable |
| prediction | VARCHAR/INTEGER | Predicted class label |
| accumulate_cols | Same as input | Pass-through columns if specified |

### Output with Probabilities (OutputProb = 'true')
| Column | Data Type | Description |
|--------|-----------|-------------|
| id_column | Same as input | Row identifier from InputTable |
| prediction | VARCHAR/INTEGER | Predicted class label |
| prob_class1 | DOUBLE PRECISION | Probability of first class |
| prob_class2 | DOUBLE PRECISION | Probability of second class |
| ... | DOUBLE PRECISION | Additional probabilities (multi-class) |
| accumulate_cols | Same as input | Pass-through columns if specified |

**Notes:**
- For binary classification, probabilities sum to 1.0
- Multi-class: One-vs-one or one-vs-all strategy used
- Prediction is class with maximum decision function value

## Code Examples

### Example 1: Credit Approval - Basic Binary Classification

**Business Context:** A bank has trained an SVM model to classify loan applications as approve or reject based on applicant characteristics.

```sql
-- Train SVM model on historical loan data
CREATE TABLE loan_svm_model AS (
    SELECT * FROM TD_SVM (
        ON loan_training AS InputTable
        USING
        InputColumns ('income', 'debt_ratio', 'credit_score', 'employment_years', 'age')
        ResponseColumn ('approval_status')
        Kernel ('rbf')
        Gamma (0.1)
        C (1.0)  -- Regularization parameter
    ) AS dt
) WITH DATA;

-- Classify new loan applications
SELECT * FROM TD_SVMPredict (
    ON new_applications AS InputTable PARTITION BY ANY
    ON loan_svm_model AS ModelTable DIMENSION
    USING
    IDColumn ('application_id')
    Accumulate ('applicant_name', 'requested_amount', 'credit_score')
) AS dt
ORDER BY application_id;

/*
Sample Output:
application_id | prediction | applicant_name     | requested_amount | credit_score
---------------|------------|--------------------|------------------|-------------
APP10001       | approve    | John Smith         | 250000           | 720
APP10002       | reject     | Jane Doe           | 180000           | 580
APP10003       | approve    | Robert Johnson     | 320000           | 780
APP10004       | reject     | Maria Garcia       | 150000           | 610

Interpretation:
- APP10001, APP10003: Approved → Process loan
- APP10002, APP10004: Rejected → Deny application or request more documentation
*/

-- Business Impact:
-- Consistent credit decisions reduced manual review time by 65%
-- Approval accuracy improved by 12% compared to rule-based system
```

### Example 2: Customer Churn with Probability Scores

**Business Context:** Predict which customers are likely to churn, using probability scores to prioritize retention efforts.

```sql
-- Train churn prediction model
CREATE TABLE churn_svm_model AS (
    SELECT * FROM TD_SVM (
        ON customer_training AS InputTable
        USING
        InputColumns ('months_active', 'support_tickets', 'usage_decline_pct',
                      'payment_delays', 'competitor_contact', 'satisfaction_score')
        ResponseColumn ('churned')
        Kernel ('rbf')
        Gamma (0.05)
        C (2.0)
    ) AS dt
) WITH DATA;

-- Score customers with churn probabilities
SELECT * FROM TD_SVMPredict (
    ON active_customers AS InputTable PARTITION BY ANY
    ON churn_svm_model AS ModelTable DIMENSION
    USING
    IDColumn ('customer_id')
    OutputProb ('true')
    Responses ('no_churn', 'churn')
    Accumulate ('customer_name', 'account_value', 'tenure_months')
) AS dt
ORDER BY prob_churn DESC;  -- Highest churn risk first

/*
Sample Output:
customer_id | prediction | prob_no_churn | prob_churn | customer_name      | account_value | tenure_months
------------|------------|---------------|------------|--------------------|---------------|---------------
C78901      | churn      | 0.18          | 0.82       | John Anderson      | 125000        | 36
C45612      | churn      | 0.25          | 0.75       | Mary Johnson       | 98000         | 24
C12345      | no_churn   | 0.72          | 0.28       | David Lee          | 45000         | 48
C23456      | no_churn   | 0.88          | 0.12       | Sarah Kim          | 67000         | 60

Interpretation:
- C78901: 82% churn risk → Immediate intervention by account manager
- C45612: 75% churn risk → Retention campaign, special offer
- C12345: 28% churn risk → Standard nurture campaign
- C23456: 12% churn risk → Monitor, no immediate action
*/

-- Create targeted retention campaigns
CREATE TABLE retention_campaigns AS (
    SELECT
        customer_id,
        customer_name,
        account_value,
        prob_churn,
        CASE
            WHEN prob_churn >= 0.70 THEN 'VIP_RETENTION'
            WHEN prob_churn >= 0.50 THEN 'STANDARD_RETENTION'
            WHEN prob_churn >= 0.30 THEN 'EARLY_WARNING'
            ELSE 'MAINTAIN'
        END AS campaign_type,
        CASE
            WHEN prob_churn >= 0.70 THEN account_value * 0.10  -- 10% discount
            WHEN prob_churn >= 0.50 THEN account_value * 0.05  -- 5% discount
            ELSE 0
        END AS max_discount_offer
    FROM TD_SVMPredict (
        ON active_customers AS InputTable PARTITION BY ANY
        ON churn_svm_model AS ModelTable DIMENSION
        USING
        IDColumn ('customer_id')
        OutputProb ('true')
        Responses ('no_churn', 'churn')
        Accumulate ('customer_name', 'account_value')
    ) AS dt
    WHERE prob_churn >= 0.30  -- Only target at-risk customers
) WITH DATA;

-- Business Impact:
-- Churn rate reduced from 18% to 12% through targeted interventions
-- Retention campaign ROI: 4.2x (saved $2.8M in annual recurring revenue)
-- Focused efforts on high-value at-risk customers
```

### Example 3: Medical Diagnosis Classification

**Business Context:** Classify patients as having a disease or not based on diagnostic test results and symptoms.

```sql
-- Train diagnostic SVM model
CREATE TABLE diagnosis_svm_model AS (
    SELECT * FROM TD_SVM (
        ON patient_training AS InputTable
        USING
        InputColumns ('age', 'bmi', 'blood_pressure', 'glucose_level',
                      'cholesterol', 'family_history_score', 'symptom_score')
        ResponseColumn ('disease_present')
        Kernel ('rbf')
        Gamma (0.2)
        C (1.5)
    ) AS dt
) WITH DATA;

-- Classify new patients
SELECT * FROM TD_SVMPredict (
    ON new_patients AS InputTable PARTITION BY ANY
    ON diagnosis_svm_model AS ModelTable DIMENSION
    USING
    IDColumn ('patient_id')
    OutputProb ('true')
    Responses ('healthy', 'disease')
    Accumulate ('patient_name', 'age', 'referring_physician')
) AS dt
ORDER BY prob_disease DESC;

/*
Sample Output:
patient_id | prediction | prob_healthy | prob_disease | patient_name    | age | referring_physician
-----------|------------|--------------|--------------|-----------------|-----|--------------------
PT5012     | disease    | 0.15         | 0.85         | John Anderson   | 58  | Dr. Smith
PT5089     | disease    | 0.32         | 0.68         | Mary Johnson    | 62  | Dr. Chen
PT5045     | healthy    | 0.75         | 0.25         | David Lee       | 45  | Dr. Garcia
PT5101     | healthy    | 0.92         | 0.08         | Sarah Kim       | 38  | Dr. Brown

Interpretation:
- PT5012: 85% disease probability → Order confirmatory tests, specialist referral
- PT5089: 68% disease probability → Additional diagnostic workup recommended
- PT5045: 25% disease probability → Preventive counseling, recheck in 6 months
- PT5101: 8% disease probability → Routine follow-up
*/

-- Generate clinical recommendations
CREATE TABLE clinical_recommendations AS (
    SELECT
        patient_id,
        patient_name,
        age,
        prob_disease,
        CASE
            WHEN prob_disease >= 0.75 THEN 'SPECIALIST_REFERRAL'
            WHEN prob_disease >= 0.50 THEN 'ADDITIONAL_TESTING'
            WHEN prob_disease >= 0.25 THEN 'RECHECK_6_MONTHS'
            ELSE 'ROUTINE_FOLLOWUP'
        END AS recommended_action,
        CASE
            WHEN prob_disease >= 0.75 THEN 'Urgent - within 2 weeks'
            WHEN prob_disease >= 0.50 THEN 'Standard - within 1 month'
            WHEN prob_disease >= 0.25 THEN 'Routine - 6 month follow-up'
            ELSE 'Annual physical'
        END AS timeline
    FROM TD_SVMPredict (
        ON new_patients AS InputTable PARTITION BY ANY
        ON diagnosis_svm_model AS ModelTable DIMENSION
        USING
        IDColumn ('patient_id')
        OutputProb ('true')
        Responses ('healthy', 'disease')
        Accumulate ('patient_name', 'age')
    ) AS dt
) WITH DATA;

-- Business Impact:
-- Early disease detection improved by 35%
-- Reduced unnecessary specialist referrals by 22%
-- IMPORTANT: Model assists physicians, does not replace medical judgment
```

### Example 4: Multi-Class Product Categorization

**Business Context:** Automatically categorize products into quality tiers (premium, standard, budget) based on manufacturing specifications.

```sql
-- Train multi-class SVM
CREATE TABLE product_quality_svm_model AS (
    SELECT * FROM TD_SVM (
        ON product_training AS InputTable
        USING
        InputColumns ('material_grade', 'tolerance_precision', 'durability_score',
                      'finish_quality', 'feature_count', 'component_cost')
        ResponseColumn ('quality_tier')
        Kernel ('rbf')
        Gamma (0.1)
        C (1.0)
    ) AS dt
) WITH DATA;

-- Classify new products
SELECT * FROM TD_SVMPredict (
    ON new_products AS InputTable PARTITION BY ANY
    ON product_quality_svm_model AS ModelTable DIMENSION
    USING
    IDColumn ('product_id')
    Accumulate ('product_name', 'target_market', 'estimated_cost')
) AS dt
ORDER BY product_id;

/*
Sample Output:
product_id | prediction | product_name              | target_market | estimated_cost
-----------|------------|---------------------------|---------------|---------------
PRD8801    | premium    | Professional Camera       | B2B           | 1850.00
PRD8802    | standard   | Consumer Camera           | B2C           | 450.00
PRD8803    | budget     | Entry-Level Camera        | B2C           | 125.00
PRD8804    | premium    | Industrial Sensor         | B2B           | 2200.00

Interpretation:
- PRD8801, PRD8804: Premium tier → High-end marketing, specialized sales channel
- PRD8802: Standard tier → Mass market retail, competitive pricing
- PRD8803: Budget tier → Value marketing, high-volume distribution
*/

-- Assign pricing strategy based on classification
CREATE TABLE product_strategy AS (
    SELECT
        product_id,
        product_name,
        estimated_cost,
        prediction AS quality_tier,
        CASE
            WHEN prediction = 'premium' THEN estimated_cost * 2.5
            WHEN prediction = 'standard' THEN estimated_cost * 1.8
            WHEN prediction = 'budget' THEN estimated_cost * 1.4
        END AS suggested_retail_price,
        CASE
            WHEN prediction = 'premium' THEN 'Specialized retailers, direct sales'
            WHEN prediction = 'standard' THEN 'Major retailers, online marketplaces'
            WHEN prediction = 'budget' THEN 'Discount retailers, bulk distributors'
        END AS distribution_channel
    FROM TD_SVMPredict (
        ON new_products AS InputTable PARTITION BY ANY
        ON product_quality_svm_model AS ModelTable DIMENSION
        USING
        IDColumn ('product_id')
        Accumulate ('product_name', 'estimated_cost')
    ) AS dt
) WITH DATA;

-- Business Impact:
-- Product categorization time reduced from 2 hours to 5 seconds per product
-- Pricing strategy consistency improved across product lines
-- Marketing resource allocation optimized by quality tier
```

### Example 5: Fraud Detection with Decision Function

**Business Context:** Detect fraudulent insurance claims using SVM, ranking by distance from decision boundary.

```sql
-- Train fraud detection SVM
CREATE TABLE fraud_svm_model AS (
    SELECT * FROM TD_SVM (
        ON claims_training AS InputTable
        USING
        InputColumns ('claim_amount', 'claimant_age', 'policy_age_days',
                      'prior_claims_count', 'incident_severity', 'witness_count')
        ResponseColumn ('is_fraud')
        Kernel ('rbf')
        Gamma (0.15)
        C (2.0)
    ) AS dt
) WITH DATA;

-- Score new claims
SELECT * FROM TD_SVMPredict (
    ON new_claims AS InputTable PARTITION BY ANY
    ON fraud_svm_model AS ModelTable DIMENSION
    USING
    IDColumn ('claim_id')
    OutputProb ('true')
    Responses ('legitimate', 'fraud')
    Accumulate ('claimant_name', 'claim_amount', 'policy_number', 'claim_date')
) AS dt
ORDER BY prob_fraud DESC;

/*
Sample Output:
claim_id | prediction | prob_legitimate | prob_fraud | claimant_name   | claim_amount | policy_number | claim_date
---------|------------|-----------------|------------|-----------------|--------------|---------------|------------
CLM9012  | fraud      | 0.12            | 0.88       | John Anderson   | 15000.00     | POL456789     | 2024-01-10
CLM9045  | fraud      | 0.28            | 0.72       | Mary Johnson    | 22000.00     | POL123456     | 2024-01-12
CLM9023  | legitimate | 0.82            | 0.18       | David Lee       | 3500.00      | POL789012     | 2024-01-11
CLM9067  | legitimate | 0.94            | 0.06       | Sarah Kim       | 1800.00      | POL345678     | 2024-01-13

Interpretation:
- CLM9012: 88% fraud → Deny claim, refer to special investigations unit
- CLM9045: 72% fraud → Field investigator review, request documentation
- CLM9023: 18% fraud → Standard processing with spot audit
- CLM9067: 6% fraud → Fast-track approval
*/

-- Create fraud investigation workflow
CREATE TABLE fraud_investigation AS (
    SELECT
        claim_id,
        claimant_name,
        claim_amount,
        prob_fraud,
        CASE
            WHEN prob_fraud >= 0.80 THEN 'DENY_AND_INVESTIGATE'
            WHEN prob_fraud >= 0.60 THEN 'FIELD_INVESTIGATION'
            WHEN prob_fraud >= 0.40 THEN 'ENHANCED_REVIEW'
            WHEN prob_fraud >= 0.20 THEN 'STANDARD_AUDIT'
            ELSE 'FAST_TRACK'
        END AS review_level,
        CASE
            WHEN prob_fraud >= 0.80 THEN claim_amount * 0.90  -- Expected savings
            WHEN prob_fraud >= 0.60 THEN claim_amount * 0.60
            WHEN prob_fraud >= 0.40 THEN claim_amount * 0.30
            ELSE 0
        END AS estimated_fraud_savings
    FROM TD_SVMPredict (
        ON new_claims AS InputTable PARTITION BY ANY
        ON fraud_svm_model AS ModelTable DIMENSION
        USING
        IDColumn ('claim_id')
        OutputProb ('true')
        Responses ('legitimate', 'fraud')
        Accumulate ('claimant_name', 'claim_amount')
    ) AS dt
) WITH DATA;

-- Calculate program ROI
SELECT
    review_level,
    COUNT(*) AS claim_count,
    SUM(claim_amount) AS total_claim_value,
    SUM(estimated_fraud_savings) AS potential_savings
FROM fraud_investigation
GROUP BY review_level
ORDER BY potential_savings DESC;

-- Business Impact:
-- Fraud losses reduced by $3.2M annually
-- Investigation resources focused on highest-probability fraud
-- False positive rate: 8% (industry average: 25%)
```

### Example 6: Image Classification for Quality Control

**Business Context:** Classify product images as defective or acceptable using SVM trained on image features.

```sql
-- Train SVM on image features extracted from quality products
CREATE TABLE image_quality_svm_model AS (
    SELECT * FROM TD_SVM (
        ON product_image_features AS InputTable
        USING
        InputColumns ('edge_density', 'color_uniformity', 'texture_variance',
                      'symmetry_score', 'defect_blob_count', 'contrast_ratio')
        ResponseColumn ('quality_status')
        Kernel ('rbf')
        Gamma (0.1)
        C (1.0)
    ) AS dt
) WITH DATA;

-- Classify images from production line
SELECT * FROM TD_SVMPredict (
    ON production_images AS InputTable PARTITION BY ANY
    ON image_quality_svm_model AS ModelTable DIMENSION
    USING
    IDColumn ('image_id')
    OutputProb ('true')
    Responses ('acceptable', 'defective')
    Accumulate ('product_serial', 'production_line', 'timestamp')
) AS dt
ORDER BY prob_defective DESC;

/*
Sample Output:
image_id | prediction  | prob_acceptable | prob_defective | product_serial | production_line | timestamp
---------|-------------|-----------------|----------------|----------------|-----------------|------------------
IMG5012  | defective   | 0.15            | 0.85           | SN789012       | LINE_A          | 2024-01-15 10:05
IMG5089  | defective   | 0.32            | 0.68           | SN123456       | LINE_B          | 2024-01-15 10:07
IMG5045  | acceptable  | 0.88            | 0.12           | SN456789       | LINE_A          | 2024-01-15 10:09
IMG5101  | acceptable  | 0.95            | 0.05           | SN901234       | LINE_C          | 2024-01-15 10:10

Interpretation:
- IMG5012: 85% defective → Reject, remove from production
- IMG5089: 68% defective → Flag for manual inspection
- IMG5045: 12% defective → Accept, spot check
- IMG5101: 5% defective → Accept, high confidence
*/

-- Analyze defect patterns by production line
SELECT
    production_line,
    COUNT(*) AS total_products,
    SUM(CASE WHEN prediction = 'defective' THEN 1 ELSE 0 END) AS defects,
    AVG(prob_defective) AS avg_defect_probability,
    CASE
        WHEN AVG(prob_defective) > 0.30 THEN 'STOP_LINE_FOR_CALIBRATION'
        WHEN AVG(prob_defective) > 0.15 THEN 'SCHEDULE_MAINTENANCE'
        ELSE 'NORMAL_OPERATION'
    END AS recommended_action
FROM TD_SVMPredict (
    ON production_images AS InputTable PARTITION BY ANY
    ON image_quality_svm_model AS ModelTable DIMENSION
    USING
    IDColumn ('image_id')
    OutputProb ('true')
    Responses ('acceptable', 'defective')
    Accumulate ('production_line')
) AS dt
GROUP BY production_line;

-- Business Impact:
-- Automated visual inspection replaced 15 human inspectors
-- Defect detection rate: 96% (human inspectors: 85%)
-- Inspection time reduced from 30 seconds to 2 seconds per product
```

## Common Use Cases

### Credit and Financial Services
- **Credit Approval**: Classify loan applications as approve/reject
- **Credit Scoring**: Risk stratification for lending decisions
- **Fraud Detection**: Transaction and claim fraud classification
- **Default Prediction**: Predict loan default probability

### Healthcare and Life Sciences
- **Disease Diagnosis**: Classify patients by disease presence
- **Medical Image Analysis**: Tumor detection, organ classification
- **Patient Risk Stratification**: Classify by readmission risk, mortality risk
- **Treatment Response**: Predict which patients will respond to treatment

### Marketing and Sales
- **Customer Churn**: Predict which customers will leave
- **Lead Scoring**: Classify leads by conversion probability
- **Campaign Response**: Predict customer response to marketing
- **Customer Segmentation**: Classify customers into behavioral groups

### Manufacturing and Quality
- **Quality Control**: Classify products as pass/fail
- **Defect Detection**: Identify manufacturing defects
- **Predictive Maintenance**: Classify equipment by failure risk
- **Process Optimization**: Classify production runs by quality

### Security and Compliance
- **Intrusion Detection**: Classify network traffic as normal/attack
- **Malware Detection**: Classify files as benign/malicious
- **Spam Filtering**: Email classification
- **Transaction Monitoring**: Suspicious activity detection

## Best Practices

### Model Training
1. **Feature Scaling**: Always standardize features (StandardScaler) before SVM
2. **Kernel Selection**: RBF kernel for non-linear problems, linear for text/high-dimensional data
3. **Hyperparameter Tuning**: Use grid search to find optimal C and gamma
4. **Class Balance**: Address imbalanced classes with class weights or resampling

### Prediction
1. **Feature Consistency**: Ensure test data has identical features as training
2. **Missing Values**: Handle before prediction (SVM cannot process NULLs)
3. **Feature Scaling**: Apply same scaling transformation used during training
4. **Probability Interpretation**: SVM probabilities are estimated (not true probabilities like Naive Bayes)

### Performance Optimization
1. **Batch Scoring**: Use PARTITION BY ANY for parallel processing
2. **Index ID Column**: Create index for faster joins with business tables
3. **Accumulate Wisely**: Only include necessary pass-through columns
4. **Support Vector Count**: Fewer support vectors = faster prediction

### Production Deployment
1. **Model Versioning**: Track model versions with training dates and parameters
2. **Threshold Tuning**: Adjust decision thresholds based on business costs
3. **Monitoring**: Track prediction distribution and probabilities over time
4. **A/B Testing**: Compare model versions before full deployment

### Interpretability
1. **Feature Importance**: Use permutation importance or SHAP for feature analysis
2. **Support Vectors**: Examine support vectors to understand decision boundary
3. **Decision Function**: Use distance from hyperplane for confidence scoring
4. **Probability Calibration**: Consider calibrating probabilities for better interpretation

## Related Functions

### Model Training
- **TD_SVM**: Train Support Vector Machine models (produces ModelTable input)
- **TD_OneClassSVM**: Train One-Class SVM for anomaly detection
- **TD_SVMSparse**: Train SVM on sparse data (text classification)

### Alternative Classifiers
- **TD_DecisionForest**: Tree-based classification for interpretability
- **TD_XGBoost**: Gradient boosting for highest accuracy
- **TD_GLM**: Logistic regression for linear classification
- **TD_NaiveBayes**: Probabilistic classification for text/categorical data

### Model Evaluation
- **TD_ClassificationEvaluator**: Evaluate classification performance with confusion matrix
- **TD_ROC**: Generate ROC curves and calculate AUC
- **TD_ConfusionMatrix**: Create confusion matrix for multi-class evaluation

### Data Preparation
- **TD_ScaleFit/Transform**: Essential for SVM - standardize features
- **TD_SimpleImputeFit/Transform**: Handle missing values before prediction
- **TD_OneHotEncodingFit/Transform**: Convert categorical variables for SVM

### Feature Engineering
- **TD_PolynomialFeaturesFit/Transform**: Create polynomial and interaction terms
- **TD_PCA**: Reduce dimensionality for high-dimensional data
- **TD_TFIDF**: Create text features for document classification

## Notes and Limitations

### General Limitations
1. **Feature Matching**: All feature columns from training must be present in test data
2. **No Missing Values**: SVM cannot handle NULLs - preprocess data first
3. **Feature Scaling Required**: SVM is very sensitive to feature scales
4. **No Native Probability**: Probabilities are estimated (Platt scaling), not inherent

### Model Characteristics
1. **Support Vector-Based**: Model defined by subset of training examples on decision boundary
2. **Maximum Margin**: Finds decision boundary that maximizes separation between classes
3. **Kernel Methods**: Can handle non-linear decision boundaries via kernel trick
4. **Multi-Class**: Uses one-vs-one or one-vs-all strategies for >2 classes

### Performance Considerations
1. **Training Time**: Can be slow for very large training sets (quadratic to cubic complexity)
2. **Prediction Speed**: Fast once trained (depends on number of support vectors)
3. **Memory**: Model size determined by support vectors (can be large for complex problems)
4. **High Dimensions**: SVM handles high-dimensional data well (robust to curse of dimensionality)

### Best Use Cases
- **When to Use SVM**: Non-linear patterns, high-dimensional data, need robustness, moderate training data size
- **When to Avoid SVM**: Very large training sets (>100K rows), need interpretability, need true probabilities
- **Alternatives**: Consider TD_XGBoost for better accuracy, TD_DecisionForest for interpretability, TD_GLM for speed

### Teradata-Specific Notes
1. **UTF8 Support**: ModelTable and InputTable support UTF8 character sets
2. **PARTITION BY ANY**: Enables parallel processing across AMPs
3. **DIMENSION Tables**: ModelTable must be DIMENSION for broadcast to all AMPs
4. **Deterministic**: Same input always produces same output (no randomness)

## Version Information

**Documentation Generated:** November 29, 2025
**Based on:** Teradata Database Analytic Functions Version 17.20
**Function Category:** Machine Learning - Model Scoring (Classification)
**Last Updated:** 2025-11-29
