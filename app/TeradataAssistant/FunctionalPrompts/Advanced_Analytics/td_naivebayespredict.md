# TD_NaiveBayesPredict

## Function Name
**TD_NaiveBayesPredict** - Naive Bayes Classification Prediction

**Aliases:** NaiveBayesPredict

## Description

TD_NaiveBayesPredict applies a trained Naive Bayes classifier to new data for classification. Naive Bayes is a probabilistic machine learning algorithm based on Bayes' theorem with the "naive" assumption of conditional independence between features given the class label. Despite this simplifying assumption, Naive Bayes often performs remarkably well, especially for text classification, spam filtering, and categorical data.

**Key Characteristics:**
- **Probabilistic Classification**: Returns class probabilities based on Bayes' theorem
- **Fast Training & Prediction**: Computationally efficient, scales well to large datasets
- **Handles Categorical Data**: Naturally suited for discrete/categorical features
- **Text Classification**: Excellent for document classification, sentiment analysis, spam detection
- **Small Data Performance**: Works well even with limited training data
- **Multi-Class Support**: Naturally extends to multi-class classification problems

The function takes a trained Naive Bayes model (from TD_NaiveBayes) and calculates posterior probabilities for each class, predicting the class with the highest probability.

## When to Use TD_NaiveBayesPredict

**Business Applications:**
- **Email Spam Filtering**: Classify emails as spam or legitimate based on word frequencies
- **Sentiment Analysis**: Predict positive/negative/neutral sentiment from customer reviews
- **Document Classification**: Categorize news articles, support tickets, or legal documents
- **Customer Intent Detection**: Classify customer inquiries for routing to appropriate teams
- **Medical Diagnosis**: Predict disease presence based on symptoms and test results
- **Fraud Detection**: Flag suspicious transactions based on categorical features
- **Product Categorization**: Auto-assign products to categories based on attributes
- **Churn Prediction**: Classify customers by churn risk using categorical features

**Use TD_NaiveBayesPredict When You Need To:**
- Apply a trained Naive Bayes model to new observations
- Score test data for model evaluation
- Classify text documents or categorical data in production
- Get probability estimates for each class
- Deploy fast, interpretable classification models
- Handle high-dimensional categorical feature spaces

**Analytical Use Cases:**
- Real-time content moderation (toxic comment detection)
- Automated support ticket routing
- Product recommendation based on categorical preferences
- Risk stratification with categorical medical variables
- A/B test segment prediction

## Syntax

```sql
SELECT * FROM TD_NaiveBayesPredict (
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
- Categorical or numeric features (Naive Bayes handles both)

### ModelTable (DIMENSION)
The trained Naive Bayes model table produced by TD_NaiveBayes function. Contains:
- Prior probabilities for each class
- Conditional probabilities P(feature | class) for each feature-class combination
- Feature metadata (categorical levels, distributions)
- Model type (Multinomial, Gaussian, Bernoulli)

### IDColumn
Specifies the column that uniquely identifies each row in InputTable.

**Syntax:** `IDColumn('column_name')`

**Example:**
```sql
IDColumn('document_id')
```

## Optional Elements

### Accumulate
Specifies columns from InputTable to include in output (pass-through columns).

**Syntax:** `Accumulate('column1', 'column2', ...)`

**Example:**
```sql
Accumulate('document_id', 'title', 'publish_date', 'author')
```

### OutputProb
Whether to output predicted probabilities for each class.

**Values:**
- `'true'`: Include probability columns (prob_class1, prob_class2, etc.)
- `'false'`: Output only predicted class (default)

**Syntax:** `OutputProb('true')`

**Use Cases:**
- **Threshold Tuning**: Adjust decision threshold based on business costs
- **Confidence Assessment**: Evaluate prediction certainty
- **Multi-Label**: Select top-K classes above probability threshold
- **Risk Scoring**: Use probability as continuous risk score

### Responses
Specifies the class labels in the order corresponding to probability columns when OutputProb is true.

**Syntax:** `Responses('class1', 'class2', ...)`

**Example:**
```sql
Responses('spam', 'not_spam')  -- For binary classification
Responses('positive', 'negative', 'neutral')  -- For sentiment analysis
```

## Input Schema

### InputTable
| Column | Data Type | Description |
|--------|-----------|-------------|
| id_column | INTEGER, VARCHAR | Unique identifier for each row |
| feature_1 | CATEGORICAL/NUMERIC | First feature (same type as training) |
| feature_2 | CATEGORICAL/NUMERIC | Second feature (same type as training) |
| ... | CATEGORICAL/NUMERIC | Additional features (must match training) |
| accumulate_cols | ANY | Optional columns to pass through |

**Requirements:**
- All feature columns from training must be present
- Column names must match training data exactly
- For text classification: features are word frequencies or binary indicators
- Missing values: Handle before prediction (Naive Bayes typically requires complete data)

### ModelTable
Standard output from TD_NaiveBayes function containing:
- Prior probabilities: P(class)
- Conditional probabilities: P(feature | class)
- Feature distributions (Gaussian parameters for continuous features)
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
| prediction | VARCHAR/INTEGER | Predicted class label (argmax of probabilities) |
| prob_class1 | DOUBLE PRECISION | Probability of first class |
| prob_class2 | DOUBLE PRECISION | Probability of second class |
| ... | DOUBLE PRECISION | Additional class probabilities |
| accumulate_cols | Same as input | Pass-through columns if specified |

**Notes:**
- Probabilities sum to 1.0 across all classes
- Prediction is the class with maximum posterior probability
- Probabilities calculated using Bayes' theorem: P(class | features)

## Code Examples

### Example 1: Email Spam Classification - Basic

**Business Context:** A company has trained a Naive Bayes model on historical emails to automatically filter spam. Score incoming emails.

```sql
-- Train Naive Bayes on email features
CREATE TABLE email_nb_model AS (
    SELECT * FROM TD_NaiveBayes (
        ON email_training AS InputTable
        USING
        InputColumns ('contains_urgent', 'has_external_link', 'subject_length',
                      'sender_domain_age_days', 'num_recipients', 'has_attachment')
        ResponseColumn ('is_spam')
        ModelType ('Gaussian')  -- Features are numeric
    ) AS dt
) WITH DATA;

-- Classify new emails
SELECT * FROM TD_NaiveBayesPredict (
    ON incoming_emails AS InputTable PARTITION BY ANY
    ON email_nb_model AS ModelTable DIMENSION
    USING
    IDColumn ('email_id')
    Accumulate ('sender', 'subject', 'received_time')
) AS dt
ORDER BY email_id;

/*
Sample Output:
email_id | prediction | sender                    | subject                  | received_time
---------|------------|---------------------------|--------------------------|------------------
EM1001   | not_spam   | john@company.com          | Q4 Budget Review         | 2024-01-15 09:15
EM1002   | spam       | offers@promo-site.xyz     | URGENT: Claim Your Prize | 2024-01-15 09:16
EM1003   | not_spam   | sarah@partner.com         | Meeting Confirmation     | 2024-01-15 09:17
EM1004   | spam       | deal@random-site.com      | Limited Time Offer!!!    | 2024-01-15 09:18

Interpretation:
- EM1001, EM1003: Legitimate emails → Deliver to inbox
- EM1002, EM1004: Spam detected → Move to spam folder
*/

-- Business Impact:
-- Reduced spam in user inboxes by 96%
-- Automated email filtering saves 15 minutes per user per day
```

### Example 2: Sentiment Analysis with Confidence Scores

**Business Context:** Analyze customer review sentiment to prioritize responses. Use probability scores to identify low-confidence predictions requiring human review.

```sql
-- Train sentiment classifier on product reviews
CREATE TABLE sentiment_nb_model AS (
    SELECT * FROM TD_NaiveBayes (
        ON review_training AS InputTable
        USING
        InputColumns ('word_positive_count', 'word_negative_count', 'exclamation_count',
                      'rating_mentioned', 'comparison_count', 'question_count')
        ResponseColumn ('sentiment')
        ModelType ('Multinomial')  -- Count-based features
    ) AS dt
) WITH DATA;

-- Score new reviews with sentiment probabilities
SELECT * FROM TD_NaiveBayesPredict (
    ON new_reviews AS InputTable PARTITION BY ANY
    ON sentiment_nb_model AS ModelTable DIMENSION
    USING
    IDColumn ('review_id')
    OutputProb ('true')
    Responses ('positive', 'negative', 'neutral')
    Accumulate ('customer_id', 'product_id', 'review_text_snippet', 'review_date')
) AS dt
ORDER BY prob_negative DESC;  -- Most negative reviews first

/*
Sample Output:
review_id | prediction | prob_positive | prob_negative | prob_neutral | customer_id | product_id | review_text_snippet      | review_date
----------|------------|---------------|---------------|--------------|-------------|------------|--------------------------|------------
REV5012   | negative   | 0.08          | 0.85          | 0.07         | C78901      | P4521      | "Terrible quality..."    | 2024-01-15
REV5089   | negative   | 0.15          | 0.72          | 0.13         | C45612      | P1234      | "Disappointed with..."   | 2024-01-15
REV5045   | positive   | 0.78          | 0.10          | 0.12         | C12345      | P4521      | "Excellent product..."   | 2024-01-15
REV5023   | neutral    | 0.42          | 0.38          | 0.20         | C23456      | P9876      | "It's okay, average..."  | 2024-01-15

Interpretation:
- REV5012: 85% negative → Priority escalation to customer service
- REV5089: 72% negative → Follow-up with customer, investigate issue
- REV5045: 78% positive → Feature in marketing materials
- REV5023: Low confidence (max prob 42%) → Manual review needed
*/

-- Create action queue based on sentiment and confidence
CREATE TABLE review_action_queue AS (
    SELECT
        review_id,
        customer_id,
        product_id,
        prediction AS sentiment,
        prob_negative,
        prob_positive,
        GREATEST(prob_positive, prob_negative, prob_neutral) AS confidence,
        CASE
            WHEN prob_negative >= 0.70 THEN 'ESCALATE_URGENT'
            WHEN prob_negative >= 0.50 THEN 'FOLLOW_UP'
            WHEN prob_positive >= 0.70 THEN 'FEATURE_IN_MARKETING'
            WHEN GREATEST(prob_positive, prob_negative, prob_neutral) < 0.50 THEN 'MANUAL_REVIEW'
            ELSE 'MONITOR'
        END AS action
    FROM TD_NaiveBayesPredict (
        ON new_reviews AS InputTable PARTITION BY ANY
        ON sentiment_nb_model AS ModelTable DIMENSION
        USING
        IDColumn ('review_id')
        OutputProb ('true')
        Responses ('positive', 'negative', 'neutral')
        Accumulate ('customer_id', 'product_id')
    ) AS dt
) WITH DATA;

-- Business Impact:
-- Response time to negative reviews reduced from 48 hours to 4 hours
-- Customer satisfaction improved by 18% through proactive outreach
-- Identified product quality issues 3x faster
```

### Example 3: Support Ticket Routing

**Business Context:** Automatically route incoming support tickets to the appropriate team based on ticket content and metadata.

```sql
-- Train classifier on historical ticket routing
CREATE TABLE ticket_nb_model AS (
    SELECT * FROM TD_NaiveBayes (
        ON ticket_history AS InputTable
        USING
        InputColumns ('keyword_billing', 'keyword_technical', 'keyword_account',
                      'keyword_product', 'customer_tenure_days', 'previous_tickets_30d')
        ResponseColumn ('assigned_team')
        ModelType ('Multinomial')
    ) AS dt
) WITH DATA;

-- Route new tickets
SELECT * FROM TD_NaiveBayesPredict (
    ON incoming_tickets AS InputTable PARTITION BY ANY
    ON ticket_nb_model AS ModelTable DIMENSION
    USING
    IDColumn ('ticket_id')
    Accumulate ('customer_id', 'subject', 'priority', 'created_time')
) AS dt
ORDER BY ticket_id;

/*
Sample Output:
ticket_id | prediction       | customer_id | subject                        | priority | created_time
----------|------------------|-------------|--------------------------------|----------|------------------
TKT8801   | billing          | C45012      | Issue with invoice             | Medium   | 2024-01-15 10:30
TKT8802   | technical        | C78934      | App crashes on startup         | High     | 2024-01-15 10:32
TKT8803   | account          | C12567      | Cannot reset password          | Low      | 2024-01-15 10:35
TKT8804   | product          | C89234      | Feature request: Dark mode     | Low      | 2024-01-15 10:40

Interpretation:
- TKT8801 → Route to Billing Team
- TKT8802 → Route to Technical Support (high priority)
- TKT8803 → Route to Account Management
- TKT8804 → Route to Product Team
*/

-- Calculate routing accuracy and team workload
SELECT
    prediction AS assigned_team,
    COUNT(*) AS ticket_count,
    AVG(CASE WHEN priority = 'High' THEN 1 ELSE 0 END) * 100 AS pct_high_priority,
    COUNT(*) * 1.0 / SUM(COUNT(*)) OVER () * 100 AS pct_of_total
FROM TD_NaiveBayesPredict (
    ON incoming_tickets AS InputTable PARTITION BY ANY
    ON ticket_nb_model AS ModelTable DIMENSION
    USING
    IDColumn ('ticket_id')
    Accumulate ('priority')
) AS dt
GROUP BY prediction;

-- Business Impact:
-- Ticket routing time reduced from 2 hours to 30 seconds
-- 92% routing accuracy, reducing ticket re-assignments by 75%
-- Customer satisfaction (CSAT) improved by 14%
```

### Example 4: Medical Diagnosis Support

**Business Context:** Assist physicians by predicting disease probability based on symptoms and test results (categorical features).

```sql
-- Train diagnostic model
CREATE TABLE diagnosis_nb_model AS (
    SELECT * FROM TD_NaiveBayes (
        ON patient_diagnosis_training AS InputTable
        USING
        InputColumns ('symptom_fever', 'symptom_cough', 'symptom_fatigue',
                      'test_wbc_elevated', 'test_crp_positive', 'age_group', 'comorbidities')
        ResponseColumn ('diagnosis')
        ModelType ('Multinomial')
    ) AS dt
) WITH DATA;

-- Predict diagnosis for new patients
SELECT * FROM TD_NaiveBayesPredict (
    ON new_patient_presentations AS InputTable PARTITION BY ANY
    ON diagnosis_nb_model AS ModelTable DIMENSION
    USING
    IDColumn ('patient_id')
    OutputProb ('true')
    Responses ('viral_infection', 'bacterial_infection', 'other')
    Accumulate ('patient_name', 'admission_date', 'chief_complaint')
) AS dt
ORDER BY patient_id;

/*
Sample Output:
patient_id | prediction          | prob_viral | prob_bacterial | prob_other | patient_name   | admission_date | chief_complaint
-----------|---------------------|------------|----------------|------------|----------------|----------------|------------------
PT1001     | viral_infection     | 0.72       | 0.18           | 0.10       | John Anderson  | 2024-01-15     | Fever, cough
PT1002     | bacterial_infection | 0.22       | 0.68           | 0.10       | Mary Johnson   | 2024-01-15     | High fever, chills
PT1003     | viral_infection     | 0.65       | 0.25           | 0.10       | David Lee      | 2024-01-15     | Sore throat
PT1004     | other               | 0.15       | 0.20           | 0.65       | Sarah Kim      | 2024-01-15     | Chest pain

Interpretation:
- PT1001: 72% viral infection → Symptomatic treatment, viral panel
- PT1002: 68% bacterial infection → Consider antibiotics, blood culture
- PT1003: 65% viral infection → Supportive care
- PT1004: 65% other diagnosis → Investigate alternative causes
*/

-- Flag uncertain diagnoses for specialist review
CREATE TABLE uncertain_diagnoses AS (
    SELECT
        patient_id,
        patient_name,
        prediction,
        GREATEST(prob_viral, prob_bacterial, prob_other) AS max_probability,
        CASE
            WHEN GREATEST(prob_viral, prob_bacterial, prob_other) < 0.60 THEN 'SPECIALIST_CONSULT'
            WHEN prob_bacterial >= 0.60 THEN 'CONSIDER_ANTIBIOTICS'
            ELSE 'STANDARD_PROTOCOL'
        END AS clinical_action
    FROM TD_NaiveBayesPredict (
        ON new_patient_presentations AS InputTable PARTITION BY ANY
        ON diagnosis_nb_model AS ModelTable DIMENSION
        USING
        IDColumn ('patient_id')
        OutputProb ('true')
        Responses ('viral_infection', 'bacterial_infection', 'other')
        Accumulate ('patient_name')
    ) AS dt
) WITH DATA;

-- Business Impact:
-- Diagnostic decision support reduces time to treatment by 35%
-- Antibiotic prescription accuracy improved by 22%
-- IMPORTANT: Model assists physicians, does not replace clinical judgment
```

### Example 5: Document Classification for News Articles

**Business Context:** Automatically categorize incoming news articles into topic categories for content management and recommendation.

```sql
-- Train document classifier
CREATE TABLE news_nb_model AS (
    SELECT * FROM TD_NaiveBayes (
        ON news_training AS InputTable
        USING
        InputColumns ('word_freq_economy', 'word_freq_sports', 'word_freq_politics',
                      'word_freq_technology', 'word_freq_health', 'article_length',
                      'has_video', 'source_type')
        ResponseColumn ('category')
        ModelType ('Multinomial')
    ) AS dt
) WITH DATA;

-- Classify new articles
SELECT * FROM TD_NaiveBayesPredict (
    ON new_articles AS InputTable PARTITION BY ANY
    ON news_nb_model AS ModelTable DIMENSION
    USING
    IDColumn ('article_id')
    OutputProb ('true')
    Responses ('business', 'sports', 'politics', 'technology', 'health')
    Accumulate ('title', 'author', 'publish_time')
) AS dt
ORDER BY article_id;

/*
Sample Output:
article_id | prediction | prob_biz | prob_sport | prob_pol | prob_tech | prob_health | title                         | author       | publish_time
-----------|------------|----------|------------|----------|-----------|-------------|-------------------------------|--------------|------------------
ART5001    | technology | 0.12     | 0.05       | 0.15     | 0.62      | 0.06        | AI Breakthrough Announced     | John Smith   | 2024-01-15 08:00
ART5002    | sports     | 0.08     | 0.78       | 0.05     | 0.04      | 0.05        | Championship Game Preview     | Sarah Chen   | 2024-01-15 08:15
ART5003    | business   | 0.68     | 0.05       | 0.12     | 0.10      | 0.05        | Market Rally Continues        | Emily Garcia | 2024-01-15 08:30
ART5004    | politics   | 0.18     | 0.05       | 0.58     | 0.12      | 0.07        | Election Results Analysis     | David Lee    | 2024-01-15 08:45

Interpretation:
- ART5001: 62% technology → Tag as Tech, recommend to tech readers
- ART5002: 78% sports → Feature on sports homepage
- ART5003: 68% business → Include in business newsletter
- ART5004: 58% politics → Moderate confidence, verify category
*/

-- Multi-label classification: Assign secondary categories
CREATE TABLE article_categories AS (
    SELECT
        article_id,
        title,
        prediction AS primary_category,
        CASE
            WHEN prob_biz >= 0.25 AND prediction <> 'business' THEN 'business'
            WHEN prob_sport >= 0.25 AND prediction <> 'sports' THEN 'sports'
            WHEN prob_pol >= 0.25 AND prediction <> 'politics' THEN 'politics'
            WHEN prob_tech >= 0.25 AND prediction <> 'technology' THEN 'technology'
            WHEN prob_health >= 0.25 AND prediction <> 'health' THEN 'health'
            ELSE NULL
        END AS secondary_category
    FROM TD_NaiveBayesPredict (
        ON new_articles AS InputTable PARTITION BY ANY
        ON news_nb_model AS ModelTable DIMENSION
        USING
        IDColumn ('article_id')
        OutputProb ('true')
        Responses ('business', 'sports', 'politics', 'technology', 'health')
        Accumulate ('title')
    ) AS dt
) WITH DATA;

-- Business Impact:
-- Content categorization time reduced from 5 minutes to 1 second per article
-- Recommendation engine CTR improved by 24%
-- Multi-category tagging increased content discovery by 35%
```

### Example 6: Fraud Detection with Categorical Features

**Business Context:** Detect potentially fraudulent insurance claims based on categorical claim characteristics.

```sql
-- Train fraud detection model
CREATE TABLE fraud_nb_model AS (
    SELECT * FROM TD_NaiveBayes (
        ON claims_training AS InputTable
        USING
        InputColumns ('claim_type', 'incident_location_type', 'day_of_week',
                      'claimant_history_category', 'witness_present', 'police_report_filed')
        ResponseColumn ('is_fraudulent')
        ModelType ('Multinomial')
    ) AS dt
) WITH DATA;

-- Score new claims for fraud risk
SELECT * FROM TD_NaiveBayesPredict (
    ON new_claims AS InputTable PARTITION BY ANY
    ON fraud_nb_model AS ModelTable DIMENSION
    USING
    IDColumn ('claim_id')
    OutputProb ('true')
    Responses ('not_fraud', 'fraud')
    Accumulate ('claimant_id', 'claim_amount', 'incident_date', 'claim_type')
) AS dt
ORDER BY prob_fraud DESC;  -- Highest fraud probability first

/*
Sample Output:
claim_id | prediction | prob_not_fraud | prob_fraud | claimant_id | claim_amount | incident_date | claim_type
---------|------------|----------------|------------|-------------|--------------|---------------|-------------
CLM9012  | fraud      | 0.18           | 0.82       | CLT45012    | 8500.00      | 2024-01-10    | Theft
CLM9045  | fraud      | 0.28           | 0.72       | CLT78934    | 12000.00     | 2024-01-12    | Fire
CLM9023  | not_fraud  | 0.85           | 0.15       | CLT12345    | 2500.00      | 2024-01-11    | Collision
CLM9067  | not_fraud  | 0.92           | 0.08       | CLT67890    | 1800.00      | 2024-01-13    | Hail damage

Interpretation:
- CLM9012: 82% fraud probability → Full investigation, deny payment
- CLM9045: 72% fraud probability → Field adjuster visit, verify details
- CLM9023: 15% fraud probability → Standard processing with spot check
- CLM9067: 8% fraud probability → Fast-track approval
*/

-- Create fraud investigation queue
CREATE TABLE fraud_investigation_queue AS (
    SELECT
        claim_id,
        claimant_id,
        claim_amount,
        claim_type,
        prob_fraud,
        CASE
            WHEN prob_fraud >= 0.75 THEN 'SPECIAL_INVESTIGATIONS_UNIT'
            WHEN prob_fraud >= 0.50 THEN 'FIELD_ADJUSTER_VERIFICATION'
            WHEN prob_fraud >= 0.30 THEN 'ENHANCED_DOCUMENTATION'
            ELSE 'STANDARD_PROCESSING'
        END AS investigation_level,
        CASE
            WHEN prob_fraud >= 0.75 THEN claim_amount * 0.80  -- Estimated savings
            WHEN prob_fraud >= 0.50 THEN claim_amount * 0.50
            ELSE 0
        END AS potential_savings
    FROM TD_NaiveBayesPredict (
        ON new_claims AS InputTable PARTITION BY ANY
        ON fraud_nb_model AS ModelTable DIMENSION
        USING
        IDColumn ('claim_id')
        OutputProb ('true')
        Responses ('not_fraud', 'fraud')
        Accumulate ('claimant_id', 'claim_amount', 'claim_type')
    ) AS dt
    WHERE prob_fraud >= 0.30  -- Only investigate moderate-to-high risk
) WITH DATA;

-- Business Impact:
-- Fraud detection rate improved by 58%
-- False positive rate reduced by 40% (fewer legitimate claims flagged)
-- Estimated annual fraud savings: $4.2M
```

## Common Use Cases

### Text and Document Analysis
- **Spam Filtering**: Email and comment spam detection
- **Sentiment Analysis**: Customer review sentiment classification
- **Document Categorization**: News, legal documents, support tickets
- **Intent Classification**: Chatbot and search query intent detection

### Customer Analytics
- **Churn Prediction**: Classify customers by churn risk using categorical features
- **Customer Segmentation**: Group customers by behavior categories
- **Lead Scoring**: Classify leads by conversion probability
- **Purchase Intent**: Predict product interest from browsing behavior

### Healthcare and Medical
- **Diagnosis Support**: Predict disease based on symptoms (categorical)
- **Patient Risk Stratification**: Classify patients by risk categories
- **Treatment Recommendation**: Suggest treatment based on patient characteristics
- **Readmission Prediction**: Predict hospital readmission risk

### Fraud and Risk Management
- **Transaction Fraud**: Detect fraudulent transactions using categorical features
- **Insurance Claims**: Flag suspicious claims for investigation
- **Identity Verification**: Classify authentication attempts as legitimate or fraudulent
- **Credit Risk**: Assess loan default risk with categorical applicant features

### Operations and Support
- **Ticket Routing**: Automatically assign support tickets to teams
- **Content Moderation**: Classify user-generated content as appropriate/inappropriate
- **Quality Control**: Classify products as pass/fail based on inspection features
- **Complaint Classification**: Categorize customer complaints by issue type

## Best Practices

### Model Training and Application
1. **Feature Independence**: Naive Bayes assumes feature independence - works best when features are not highly correlated
2. **Categorical Features**: Particularly effective for categorical/discrete features (words, categories, binary indicators)
3. **Feature Scaling**: Not required (unlike distance-based methods) - Naive Bayes uses probabilities
4. **Missing Values**: Handle before prediction - impute or use special "missing" category

### Probability Interpretation
1. **Use OutputProb**: Always request probabilities for threshold tuning and confidence assessment
2. **Calibration**: Naive Bayes probabilities may not be well-calibrated - consider recalibration for critical decisions
3. **Low Confidence**: Flag predictions with max probability < 0.60 for manual review
4. **Multi-Label**: Use probability thresholds to assign multiple labels (secondary categories)

### Performance Optimization
1. **Fast Training**: Naive Bayes trains very quickly - suitable for frequent retraining
2. **Fast Prediction**: Prediction is extremely fast - suitable for real-time scoring
3. **Scalability**: Scales well to high-dimensional feature spaces (e.g., text with 10,000+ words)
4. **Batch Scoring**: Use PARTITION BY ANY for parallel processing

### Production Deployment
1. **Model Versioning**: Track model versions with dates (nb_model_2024_Q1)
2. **Threshold Tuning**: Adjust decision thresholds based on business costs (false positives vs false negatives)
3. **Monitoring**: Track prediction distribution and confidence scores over time
4. **A/B Testing**: Compare model versions on real traffic before full deployment

### Feature Engineering
1. **Text Features**: Use word frequencies, TF-IDF, or binary word presence
2. **Categorical Encoding**: Keep categories as-is (don't one-hot encode for Naive Bayes)
3. **Binning**: Convert continuous features to categorical bins if needed
4. **Feature Selection**: Remove highly correlated features to preserve independence assumption

## Related Functions

### Model Training
- **TD_NaiveBayes**: Train Naive Bayes classification models (produces ModelTable input)
- **TD_TextParser**: Extract features from text documents for text classification
- **TD_TFIDF**: Calculate TF-IDF features for document classification

### Alternative Classifiers
- **TD_DecisionForest**: Tree-based classification for non-linear patterns
- **TD_XGBoost**: Gradient boosting for higher accuracy (slower training)
- **TD_GLM**: Logistic regression for linear classification
- **TD_SVM**: Support Vector Machines for complex decision boundaries

### Model Evaluation
- **TD_ClassificationEvaluator**: Evaluate classification performance with confusion matrix
- **TD_ROC**: Generate ROC curves and calculate AUC for binary classification
- **TD_ConfusionMatrix**: Create confusion matrix for multi-class evaluation

### Data Preparation
- **TD_SimpleImputeFit/Transform**: Handle missing values
- **TD_TargetEncodingFit/Transform**: Encode categorical variables based on target
- **TD_StringSimilarity**: Find similar categories for grouping

### Feature Engineering
- **TD_NGram**: Generate n-grams for text classification
- **TD_TextParser**: Parse and tokenize text documents
- **TD_TFIDF**: Calculate term frequency-inverse document frequency

## Notes and Limitations

### General Limitations
1. **Feature Independence Assumption**: Assumes features are conditionally independent given class (often violated in practice)
2. **Zero Probability Problem**: If a feature-class combination wasn't seen in training, probability is zero (Laplace smoothing helps)
3. **Feature Matching**: All feature columns from training must be present in test data
4. **Continuous Features**: Gaussian Naive Bayes for continuous features assumes normal distribution

### Model Characteristics
1. **Simple Model**: May underperform complex models (Random Forest, XGBoost) on complex problems
2. **Linear Decision Boundary**: Naive Bayes creates linear decision boundaries in log-probability space
3. **Probability Calibration**: Predicted probabilities may be poorly calibrated (too extreme)
4. **Rare Categories**: Struggles with rare categorical levels not seen in training

### Performance Considerations
1. **Training Speed**: Very fast training - suitable for real-time model updates
2. **Prediction Speed**: Extremely fast prediction - ideal for high-throughput applications
3. **Memory**: Small model size - probabilities for each feature-class combination
4. **High Dimensions**: Handles high-dimensional data well (curse of dimensionality is less severe)

### Best Use Cases
- **When to Use Naive Bayes**: Text classification, categorical features, need speed and interpretability, small training data
- **When to Avoid Naive Bayes**: Highly correlated features, complex non-linear relationships, need highest accuracy
- **Alternatives**: Consider TD_XGBoost or TD_DecisionForest for better accuracy (at cost of speed and interpretability)

### Teradata-Specific Notes
1. **UTF8 Support**: ModelTable and InputTable support UTF8 character sets (important for text)
2. **PARTITION BY ANY**: Enables parallel processing across AMPs
3. **DIMENSION Tables**: ModelTable must be DIMENSION for broadcast to all AMPs
4. **Model Types**: Supports Multinomial (categorical/count), Gaussian (continuous), Bernoulli (binary)

## Version Information

**Documentation Generated:** November 29, 2025
**Based on:** Teradata Database Analytic Functions Version 17.20
**Function Category:** Machine Learning - Model Scoring (Classification)
**Last Updated:** 2025-11-29
