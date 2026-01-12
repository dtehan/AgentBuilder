# Machine Learning & Data Engineering Workflows

Complete end-to-end ML workflows for Teradata covering data preparation, model training, evaluation, and deployment.

## Overview

This directory contains **7 comprehensive ML workflows** covering all aspects of machine learning and data science in Teradata. These workflows are accessed through the `persona_data_scientist.md` and `persona_data_engineer.md` personas.

## Workflow Categories

1. **Data Preparation** - Transform raw data to ML-ready format
2. **Supervised Learning** - Classification and Regression
3. **Unsupervised Learning** - Clustering
4. **Anomaly Detection** - Fraud and outlier detection
5. **Text Analytics** - NLP and text mining
6. **Statistical Analysis** - Hypothesis testing and A/B testing

---

## Available Workflows

### ml_dataPreparation.md
**Comprehensive Data Preparation for Machine Learning**

A complete 7-stage pipeline that transforms raw data into ML-ready datasets.

**Arguments**: `database_name` `table_name` `target_column`
- `database_name`: Source database
- `table_name`: Source table with raw data
- `target_column`: Target variable for ML (for supervised learning)

**7-Stage Pipeline**:

#### Stage 1: Data Profiling and Assessment
- Understand data structure and quality
- Statistical summaries for numeric columns
- Categorical distributions
- Missing value identification
- Initial data quality checks

**Functions Used**:
- TD_UnivariateStatistics
- TD_CategoricalSummary
- TD_ColumnSummary
- TD_GetRowsWithMissingValues
- COUNT, AVG, MIN, MAX, STDDEV

#### Stage 2: Data Cleansing
- Outlier detection and removal
- Duplicate identification and removal
- Futile column identification
- Data validation

**Functions Used**:
- TD_OutlierFilterFit / TD_OutlierFilterTransform
- TD_GetFutileColumns
- ROW_NUMBER (for deduplication)

#### Stage 3: Missing Data Handling
- Simple imputation (mean, median, mode)
- NULL replacement strategies
- Missing value pattern analysis
- Complete case selection

**Functions Used**:
- TD_SimpleImputeFit / TD_SimpleImputeTransform
- TD_GetRowsWithoutMissingValues
- NVL / COALESCE

#### Stage 4: Feature Engineering and Transformation
- Numeric feature scaling (standardization, min-max)
- Binning continuous variables
- Polynomial feature creation
- Non-linear transformations

**Functions Used**:
- TD_ScaleFit / TD_ScaleTransform
- TD_BinCodeFit / TD_BinCodeTransform
- TD_PolynomialFeaturesFit / TD_PolynomialFeaturesTransform

#### Stage 5: Categorical Encoding
- One-hot encoding for nominal categories
- Ordinal encoding for ordered categories
- Target encoding for high-cardinality features
- Manual mapping with DECODE

**Functions Used**:
- TD_OneHotEncodingFit / TD_OneHotEncodingTransform
- TD_OrdinalEncodingFit / TD_OrdinalEncodingTransform
- TD_TargetEncodingFit / TD_TargetEncodingTransform
- DECODE

#### Stage 6: Train-Test Split
- Dataset splitting for validation
- Stratified sampling
- Random assignment
- Reproducible splits

**Functions Used**:
- TD_TrainTestSplit
- ROW_NUMBER with MOD

#### Stage 7: Final Validation
- Verify no missing values
- Confirm all features are numeric
- Check data distributions
- Validate train-test split

**Functions Used**:
- COUNT, AVG, STDDEV
- MIN, MAX
- System catalog queries

**Output Tables**:
1. `${TABLE_NAME}_missing_rows` - Rows with missing values (VIEW)
2. `${TABLE_NAME}_impute_model` - Imputation model
3. `${TABLE_NAME}_imputed` - Imputed data
4. `${TABLE_NAME}_outlier_model` - Outlier detection model
5. `${TABLE_NAME}_no_outliers` - Outlier-removed data
6. `${TABLE_NAME}_scale_model` - Scaling model
7. `${TABLE_NAME}_scaled` - Scaled features
8. `${TABLE_NAME}_onehot_model` - Encoding model
9. `${TABLE_NAME}_encoded` - Encoded features
10. `${TABLE_NAME}_ml_ready` - Final ML-ready dataset with train/test split

---

## Decision Guides

The workflow includes comprehensive decision guides to help choose the right techniques:

### Missing Value Strategy

| Scenario | Strategy | Function/Method |
|----------|----------|-----------------|
| <5% missing, random | Remove rows | TD_GetRowsWithoutMissingValues |
| Numeric, 5-30% missing | Impute with mean/median | TD_SimpleImputeFit (mean/median) |
| Categorical, <30% missing | Impute with mode | TD_SimpleImputeFit (mode) |
| Categorical, any % | Create 'UNKNOWN' category | COALESCE(col, 'UNKNOWN') |
| >30% missing | Drop column or custom logic | Manual analysis |

### Encoding Strategy

| Feature Type | Cardinality | Strategy | Function |
|-------------|-------------|----------|----------|
| Nominal | Low (<10) | One-Hot Encoding | TD_OneHotEncodingFit |
| Nominal | High (>50) | Target Encoding | TD_TargetEncodingFit |
| Ordinal | Any | Ordinal Encoding | TD_OrdinalEncodingFit |
| Binary | 2 | Manual (0/1) | DECODE or CASE |

### Scaling Strategy

| Model Type | Need Scaling? | Method | Function |
|-----------|---------------|--------|----------|
| Tree-based (XGBoost, RF) | No | N/A | N/A |
| Linear (GLM) | Yes | Standardization | TD_ScaleFit (standardization) |
| Distance-based (KNN, SVM, K-Means) | Yes | Standardization | TD_ScaleFit (standardization) |
| Neural Networks | Yes | Min-Max | TD_ScaleFit (min-max) |

---

## Use Cases by Persona

### Data Engineer Persona
**Primary user of ml_dataPreparation.md**

Use for:
- ETL/ELT pipeline development
- Data cleansing and quality improvement
- Missing value handling
- Outlier detection and removal
- Feature engineering
- Data transformation

**Example Tasks**:
```
"Clean my sales data - it has missing values and outliers"
"Prepare customer table for analytics"
"Transform raw transaction data for ML"
"Handle NULL values in product table"
```

### Data Scientist Persona
**Uses ml_dataPreparation.md as first step in ML workflow**

Use for:
- Data preparation before model training
- Feature engineering for predictive models
- Ensuring ML-ready data quality
- Creating train-test splits

**Example Tasks**:
```
"Build a churn prediction model" → starts with data prep
"Train a classification model for customer segmentation"
"Predict sales using XGBoost" → prep data first
```

**Typical Flow**:
1. Data preparation (ml_dataPreparation.md)
2. Model training (FunctionalPrompts/Advanced_Analytics/td_xgboost.md)
3. Model scoring (FunctionalPrompts/Advanced_Analytics/td_xgboostpredict.md)
4. Model evaluation (FunctionalPrompts/Advanced_Analytics/td_classificationevaluator.md)

---

## Complete Example Workflow

### Customer Churn Prediction (End-to-End)

**Phase 1: Data Preparation**
```sql
-- Use ml_dataPreparation.md workflow
-- Input: customer_db.customer_data with churn_flag
-- Output: customer_ml_ready with train/test split

-- Stages executed:
-- 1. Profile: TD_UnivariateStatistics on all columns
-- 2. Clean: TD_OutlierFilterFit/Transform on numeric features
-- 3. Impute: TD_SimpleImputeFit with mean/mode strategy
-- 4. Scale: TD_ScaleFit with standardization
-- 5. Encode: TD_OneHotEncodingFit for categorical features
-- 6. Split: TD_TrainTestSplit with 80/20 ratio
-- 7. Validate: Check for completeness and distributions

-- Result: customer_ml_ready table ready for training
```

**Phase 2: Model Training** (Data Scientist continues)
```sql
-- Reference: FunctionalPrompts/Advanced_Analytics/td_xgboost.md
CREATE TABLE churn_model AS
SELECT TD_XGBoost(
    ModelType('classification'),
    TargetColumn('churn_flag'),
    NumTrees(100),
    MaxDepth(6)
) FROM customer_ml_ready
WHERE dataset_split = 'TRAIN'
WITH DATA;
```

**Phase 3: Model Scoring**
```sql
-- Reference: FunctionalPrompts/Advanced_Analytics/td_xgboostpredict.md
CREATE TABLE churn_predictions AS
SELECT TD_XGBoostPredict(
    ModelTable(churn_model),
    OutputProb(1)
) FROM customer_ml_ready
WHERE dataset_split = 'TEST'
WITH DATA;
```

**Phase 4: Model Evaluation**
```sql
-- Reference: FunctionalPrompts/Advanced_Analytics/td_classificationevaluator.md
SELECT TD_ClassificationEvaluator(
    ObservationColumn('churn_flag'),
    PredictionColumn('prediction'),
    Metrics('Accuracy', 'Precision', 'Recall', 'F1', 'AUC')
) FROM churn_predictions;
```

---

## ml_classification.md
**Binary and Multiclass Classification**

Complete workflow for building classification models to predict categorical outcomes.

**Arguments**: `database_name` `table_name` `target_column`

**8-Stage Workflow**:
- Stage 0: Data Preparation Check
- Stage 1: Problem Definition (Binary vs Multiclass, Class Balance)
- Stage 2: Model Selection with User Choice
- Stage 3: Model Training
- Stage 4: Model Scoring
- Stage 5: Model Evaluation
- Stage 6: Model Interpretation (SHAP)
- Stage 7: Production Deployment

**Models Covered**:
- **TD_XGBoost** - Best overall performance (recommended)
- **TD_DecisionForest** - Interpretability and feature importance
- **TD_GLM** - Logistic regression for linear relationships
- **TD_SVM** - Complex decision boundaries
- **TD_NaiveBayes** - Fast baseline model
- **TD_KNN** - Instance-based learning

**Evaluation Metrics**:
- TD_ClassificationEvaluator (Accuracy, Precision, Recall, F1, AUC)
- TD_ROC for ROC curve analysis
- Confusion matrix
- TD_SHAP for feature importance

**Use Cases**:
- Customer churn prediction (churn/no churn)
- Fraud detection (fraud/legitimate)
- Credit risk assessment (default/no default)
- Email classification (spam/not spam)
- Product category prediction
- Customer segment classification
- Disease diagnosis

**Function References**:
- FunctionalPrompts/Advanced_Analytics/td_xgboost.md
- FunctionalPrompts/Advanced_Analytics/td_decisionforest.md
- FunctionalPrompts/Advanced_Analytics/td_glm.md
- FunctionalPrompts/Advanced_Analytics/td_svm.md
- FunctionalPrompts/Advanced_Analytics/td_naivebayes.md
- FunctionalPrompts/Advanced_Analytics/td_knn.md
- FunctionalPrompts/Advanced_Analytics/td_classificationevaluator.md
- FunctionalPrompts/Advanced_Analytics/td_roc.md
- FunctionalPrompts/Advanced_Analytics/td_shap.md

---

## ml_regression.md
**Numeric Value Prediction**

Complete workflow for building regression models to predict continuous numeric values.

**Arguments**: `database_name` `table_name` `target_column`

**8-Stage Workflow**:
- Stage 0: Data Preparation Check
- Stage 1: Problem Definition (Target Variable Analysis)
- Stage 2: Model Selection with User Choice
- Stage 3: Model Training
- Stage 4: Model Scoring
- Stage 5: Model Evaluation
- Stage 6: Model Interpretation (Residual Analysis, SHAP)
- Stage 7: Production Deployment

**Models Covered**:
- **TD_XGBoost** - Best performance for non-linear relationships (recommended)
- **TD_DecisionForest** - Feature importance and non-linear patterns
- **TD_GLM** - Linear, Ridge, Lasso, ElasticNet regression

**Evaluation Metrics**:
- TD_RegressionEvaluator (RMSE, MAE, R², MAPE)
- Residual analysis
- Prediction vs Actual plots
- TD_SHAP for feature importance

**Use Cases**:
- Sales forecasting
- Price prediction
- Demand estimation
- Revenue forecasting
- Stock price prediction
- Customer lifetime value prediction
- Real estate valuation

**Function References**:
- FunctionalPrompts/Advanced_Analytics/td_xgboost.md
- FunctionalPrompts/Advanced_Analytics/td_decisionforest.md
- FunctionalPrompts/Advanced_Analytics/td_glm.md
- FunctionalPrompts/Advanced_Analytics/td_regressionevaluator.md
- FunctionalPrompts/Advanced_Analytics/td_shap.md

---

## ml_clustering.md
**Customer Segmentation and Pattern Discovery**

Complete workflow for unsupervised clustering to discover natural groupings in data.

**Arguments**: `database_name` `table_name`

**8-Stage Workflow**:
- Stage 0: Data Preparation Check
- Stage 1: Problem Definition (Clustering Objectives)
- Stage 2: Optimal K Selection (Elbow Method, Silhouette Analysis)
- Stage 3: Model Training (Multiple K Values)
- Stage 4: Cluster Assignment
- Stage 5: Cluster Quality Evaluation
- Stage 6: Cluster Profiling and Interpretation
- Stage 7: Production Deployment

**Models Covered**:
- **TD_KMeans** - Standard K-means clustering

**Evaluation Metrics**:
- TD_Silhouette for cluster quality
- Within-cluster sum of squares (WCSS)
- Between-cluster distance
- Cluster size distribution

**Use Cases**:
- Customer segmentation
- Market segmentation
- Product categorization
- Anomaly detection via clustering
- Image segmentation
- Document clustering

**Function References**:
- FunctionalPrompts/Advanced_Analytics/td_kmeans.md
- FunctionalPrompts/Advanced_Analytics/td_kmeanspredict.md
- FunctionalPrompts/Advanced_Analytics/td_silhouette.md

---

## ml_anomalyDetection.md
**Fraud Detection and Outlier Identification**

Complete workflow for identifying anomalies, outliers, and unusual patterns in data.

**Arguments**: `database_name` `table_name`

**8-Stage Workflow**:
- Stage 0: Data Preparation Check
- Stage 1: Problem Definition (Normal vs Anomalous Behavior)
- Stage 2: Model Selection with User Choice
- Stage 3: Model Training
- Stage 4: Anomaly Scoring
- Stage 5: Threshold Tuning and Evaluation
- Stage 6: Anomaly Investigation
- Stage 7: Production Deployment with Monitoring

**Models Covered**:
- **TD_OneClassSVM** - Isolation-based anomaly detection (recommended)
- **TD_OutlierFilter** - Statistical outlier detection

**Evaluation Metrics**:
- Precision, Recall, F1 at different thresholds
- Contamination rate analysis
- Anomaly score distribution
- False positive rate

**Use Cases**:
- Fraud detection (transactions, insurance claims)
- Network intrusion detection
- Manufacturing quality control
- System health monitoring
- Credit card fraud
- IoT sensor anomaly detection

**Function References**:
- FunctionalPrompts/Advanced_Analytics/td_oneclasssvm.md
- FunctionalPrompts/Advanced_Analytics/td_oneclasssvmpredict.md
- FunctionalPrompts/Advanced_Analytics/td_outlierfilterfit.md
- FunctionalPrompts/Advanced_Analytics/td_outlierfiltertransform.md

---

## ml_textAnalytics.md
**Natural Language Processing and Text Mining**

Complete workflow for text analysis including sentiment analysis, entity extraction, and text classification.

**Arguments**: `database_name` `table_name` `text_column`

**6-Stage Workflow**:
- Stage 0: Data Preparation Check
- Stage 1: Problem Definition and Text Preprocessing
- Stage 2: Task-Specific Analysis
  - Sentiment Analysis
  - Named Entity Recognition
  - Text Classification
  - Document Similarity
- Stage 3: Model Training (for classification tasks)
- Stage 4: Evaluation and Interpretation
- Stage 5: Production Deployment

**Capabilities Covered**:
- **TD_SentimentExtractor** - Sentiment analysis (positive/negative/neutral)
- **TD_NERExtractor** - Named Entity Recognition (people, places, organizations)
- **TD_NaiveBayesTextClassifier** - Text document classification
- **TD_TFIDF** - Term frequency-inverse document frequency
- **TD_WordEmbeddings** - Word vector representations
- **TD_TextParser** - Text tokenization and preprocessing
- **TD_NGramSplitter** - N-gram generation

**Use Cases**:
- Customer review sentiment analysis
- Social media monitoring
- Document classification
- Entity extraction from text
- Topic modeling
- Spam detection
- Customer feedback analysis

**Function References**:
- FunctionalPrompts/Advanced_Analytics/td_sentimentextractor.md
- FunctionalPrompts/Advanced_Analytics/td_nerextractor.md
- FunctionalPrompts/Advanced_Analytics/td_naivebayestextclassifiertrainer.md
- FunctionalPrompts/Advanced_Analytics/td_naivebayestextclassifierpredict.md
- FunctionalPrompts/Advanced_Analytics/td_tfidf.md
- FunctionalPrompts/Advanced_Analytics/td_wordembeddings.md
- FunctionalPrompts/Advanced_Analytics/td_textparser.md
- FunctionalPrompts/Advanced_Analytics/td_ngramsplitter.md

---

## ml_statisticalTesting.md
**Hypothesis Testing and A/B Testing**

Complete workflow for statistical hypothesis testing to validate assumptions and compare groups.

**Arguments**: `database_name` `table_name`

**7-Stage Workflow**:
- Stage 0: Data Preparation Check
- Stage 1: Problem Definition (Hypothesis Formulation)
- Stage 2: Test Selection Based on Data Type
- Stage 3: Assumption Validation
- Stage 4: Test Execution
- Stage 5: Results Interpretation (P-values, Effect Sizes)
- Stage 6: Reporting and Recommendations

**Tests Covered**:
- **TD_ANOVA** - Analysis of Variance (comparing means across 3+ groups)
- **TD_ChiSq** - Chi-Square test (categorical data relationships)
- **TD_FTest** - F-test (variance comparison)
- **TD_ZTest** - Z-test (large sample mean comparison)

**Evaluation Metrics**:
- P-values and statistical significance
- Effect sizes (Cohen's d, Cramér's V)
- Confidence intervals
- Power analysis

**Use Cases**:
- A/B testing (marketing campaigns, website changes)
- Group comparisons (treatment vs control)
- Quality control testing
- Survey analysis
- Clinical trial analysis
- Feature effectiveness testing

**Function References**:
- FunctionalPrompts/Advanced_Analytics/td_anova.md
- FunctionalPrompts/Advanced_Analytics/td_chisq.md
- FunctionalPrompts/Advanced_Analytics/td_ftest.md
- FunctionalPrompts/Advanced_Analytics/td_ztest.md

---

## Function References

The workflows in this directory reference numerous functions:

### Data Profiling
- `../../FunctionalPrompts/Advanced_Analytics/td_univariatestatistics.md`
- `../../FunctionalPrompts/Advanced_Analytics/td_categoricalsummary.md`
- `../../FunctionalPrompts/Advanced_Analytics/td_columnsummary.md`
- `../../FunctionalPrompts/Advanced_Analytics/td_histogram.md`

### Missing Values
- `../../FunctionalPrompts/Advanced_Analytics/td_getrowswithmissingvalues.md`
- `../../FunctionalPrompts/Advanced_Analytics/td_getrowswithoutmissingvalues.md`
- `../../FunctionalPrompts/Advanced_Analytics/td_simpleimputefit.md`
- `../../FunctionalPrompts/Advanced_Analytics/td_simpleimputetransform.md`
- `../../FunctionalPrompts/Core_SQL_Functions/nvl___coalesce.md`

### Outlier Detection
- `../../FunctionalPrompts/Advanced_Analytics/td_outlierfilterfit.md`
- `../../FunctionalPrompts/Advanced_Analytics/td_outlierfiltertransform.md`

### Feature Engineering
- `../../FunctionalPrompts/Advanced_Analytics/td_scalefit.md`
- `../../FunctionalPrompts/Advanced_Analytics/td_scaletransform.md`
- `../../FunctionalPrompts/Advanced_Analytics/td_bincodefit.md`
- `../../FunctionalPrompts/Advanced_Analytics/td_bincodetransform.md`
- `../../FunctionalPrompts/Advanced_Analytics/td_polynomialfeaturesfit.md`
- `../../FunctionalPrompts/Advanced_Analytics/td_polynomialfeaturestransform.md`

### Encoding
- `../../FunctionalPrompts/Advanced_Analytics/td_onehotencodingfit.md`
- `../../FunctionalPrompts/Advanced_Analytics/td_onehotencodingtransform.md`
- `../../FunctionalPrompts/Advanced_Analytics/td_ordinalencodingfit.md`
- `../../FunctionalPrompts/Advanced_Analytics/td_ordinalencodingtransform.md`
- `../../FunctionalPrompts/Advanced_Analytics/td_targetencodingfit.md`
- `../../FunctionalPrompts/Advanced_Analytics/td_targetencodingtransform.md`
- `../../FunctionalPrompts/Core_SQL_Functions/decode.md`

### Core SQL
- `../../FunctionalPrompts/Core_SQL_Functions/count.md`
- `../../FunctionalPrompts/Core_SQL_Functions/avg_average_ave.md`
- `../../FunctionalPrompts/Core_SQL_Functions/row_number.md`
- `../../FunctionalPrompts/Core_SQL_Functions/mod.md`

---

## Best Practices

### Data Preparation

1. **Always profile first** - Understand data before transforming
2. **Document decisions** - Track why specific techniques were chosen
3. **Preserve models** - Save transformation models for production
4. **Test incrementally** - Validate each stage before proceeding
5. **Monitor distributions** - Check feature distributions after transformations

### ML Pipeline Development

1. **Reproducibility** - Use seeds for random operations
2. **Version control** - Track model and data versions
3. **Separate concerns** - Keep data prep separate from modeling
4. **Validate thoroughly** - Check train/test split quality
5. **Document lineage** - Track data transformations

### Production Deployment

1. **Same pipeline** - Use same transformations in production
2. **Save models** - Keep all fit models for consistency
3. **Monitor drift** - Compare production data to training data
4. **Retrain schedule** - Plan periodic retraining
5. **Error handling** - Gracefully handle missing or invalid data

---

## Extending ML Workflows

### Adding a New ML Workflow

1. **Create workflow file**: `ml_[workflow_name].md`
2. **Define structure**:
   - Arguments and variables
   - Workflow stages
   - SQL examples with functions
   - Decision guides
   - Output artifacts
   - Function references
3. **Update routing**: Add to persona files
4. **Update this README**: Document new workflow

### Workflow Template

```markdown
---
name: ML Workflow Name
description: Brief description
argument-hint: [database] [table] [target]
---

## Overview
[Purpose and goals]

## Variables
DATABASE: $1
TABLE: $2
TARGET: $3

## Workflow Stages
[Stage-by-stage process]

## Decision Guides
[How to choose techniques]

## SQL Examples
[Production-ready code]

## Function References
[Links to function docs]

## Output Artifacts
[Expected results]
```

---

## Related Documentation

- **Parent personas**:
  - `../persona_data_scientist.md`
  - `../persona_data_engineer.md`
- **Entry point**: `../teradata_assistant.md`
- **System overview**: `../../CLAUDE.MD`
- **Function docs**: `../../FunctionalPrompts/`

---

**Access these workflows through persona files for best results!**
