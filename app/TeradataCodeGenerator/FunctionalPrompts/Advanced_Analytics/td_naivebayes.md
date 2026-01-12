# TD_NaiveBayes

### Function Name
**TD_NaiveBayes**

### Description
TD_NaiveBayes trains a probabilistic classification model based on Bayes' theorem with strong (naive) independence assumptions between features. This supervised learning algorithm calculates conditional probabilities for each feature given each class label, then combines these probabilities to predict the most likely class for new observations. Despite its simplistic assumption that all features are independent, Naive Bayes often performs remarkably well in practice, particularly for text classification, spam detection, sentiment analysis, and scenarios with high-dimensional feature spaces where more complex models may overfit.

The algorithm works by learning probability distributions P(feature|class) for each feature-class combination during training, then applying Bayes' theorem to compute P(class|features) for prediction. TD_NaiveBayes supports both categorical and numerical (continuous) features, automatically calculating discrete probability tables for categorical variables and estimating Gaussian distributions for continuous variables. The function includes Laplace smoothing to handle zero probabilities and prevent prediction failures when encountering feature values not seen during training. This makes Naive Bayes particularly robust for sparse datasets, high-dimensional problems, and situations where training data may not cover all possible feature combinations.

TD_NaiveBayes excels in real-time prediction scenarios due to its computational efficiency - training requires only a single pass through the data to compute statistics, and prediction is extremely fast since it involves simple probability multiplications. The algorithm scales well to large datasets with many features, handles missing values gracefully, and provides interpretable probability outputs that quantify prediction confidence. While Naive Bayes assumes feature independence (rarely true in practice), it often compensates by being less prone to overfitting than complex models, making it an excellent baseline algorithm and highly effective for text classification tasks where bag-of-words feature representations naturally align with independence assumptions.

### When the Function Would Be Used
- **Text Classification**: Categorize documents into topics, genres, or categories
- **Spam Detection**: Filter spam emails based on word occurrence patterns
- **Sentiment Analysis**: Classify text as positive, negative, or neutral sentiment
- **Medical Diagnosis**: Predict diseases based on symptoms and test results
- **Customer Categorization**: Classify customers into segments based on behavior
- **Fraud Detection**: Identify fraudulent transactions from transaction features
- **News Article Classification**: Automatically categorize news by topic
- **Product Recommendation**: Predict product categories customers might prefer
- **Real-Time Prediction**: Deploy where low-latency predictions are critical
- **High-Dimensional Data**: Handle datasets with hundreds or thousands of features
- **Baseline Modeling**: Establish performance baseline before complex models
- **Sparse Data**: Work with datasets where many feature values are zero
- **Incremental Learning**: Update models with new data without full retraining
- **Multi-Class Classification**: Predict among many possible class labels
- **Probability Calibration**: Obtain probabilistic predictions for decision-making
- **Text Mining**: Extract patterns from unstructured text data
- **Social Media Analysis**: Classify posts, tweets, or comments
- **Email Categorization**: Auto-route emails to appropriate folders
- **Content Filtering**: Filter inappropriate or unwanted content
- **Intent Recognition**: Predict user intent from search queries or commands
- **Churn Prediction**: Identify customers likely to churn based on attributes
- **Lead Scoring**: Rank sales leads by conversion probability
- **Recommendation Systems**: Predict user preferences for content or products
- **A/B Test Analysis**: Predict which variant a user would prefer

### Syntax

**Dense Input Format:**
```sql
TD_NaiveBayes (
    ON { table | view | (query) } AS InputTable PARTITION BY ANY
    USING
    ResponseColumn ('response_column')
    NumericInputs ('numeric_column' [,...])
    CategoricalInputs ('categorical_column' [,...])
    [ ModelType ({ 'Multinomial' | 'Bernoulli' | 'Gaussian' }) ]
    [ Alpha (smoothing_parameter) ]
    [ FitPrior ({ 'true' | 'false' }) ]
    [ ClassPriors ('class:prior' [,...]) ]
) AS alias
```

**Sparse Input Format:**
```sql
TD_NaiveBayes (
    ON { table | view | (query) } AS InputTable PARTITION BY 1
    USING
    ResponseColumn ('response_column')
    CategoryColumn ('category_column')
    ValueColumn ('value_column')
    [ ModelType ({ 'Multinomial' | 'Bernoulli' }) ]
    [ Alpha (smoothing_parameter) ]
    [ FitPrior ({ 'true' | 'false' }) ]
    [ ClassPriors ('class:prior' [,...]) ]
) AS alias
```

### Required Syntax Elements for TD_NaiveBayes

**ON clause (InputTable)**
- Training data containing features and response variable
- **Dense format**: PARTITION BY ANY for standard feature columns
- **Sparse format**: PARTITION BY 1 for category-value pairs

**ResponseColumn**
- Column containing class labels for training
- Can be any data type (INTEGER, VARCHAR, etc.)
- Must not contain NULL values
- Defines the classification target

**Feature Specification (Dense Input)**
- **NumericInputs**: Columns with continuous numeric features
- **CategoricalInputs**: Columns with discrete categorical features
- At least one of NumericInputs or CategoricalInputs required
- Multiple columns can be specified in comma-separated lists

**Feature Specification (Sparse Input)**
- **CategoryColumn**: Column containing feature names/categories
- **ValueColumn**: Column containing feature values
- Used for sparse representations (e.g., word counts in text)

### Optional Syntax Elements for TD_NaiveBayes

**ModelType**
- Specifies the Naive Bayes variant to use
- **'Multinomial'**: For count-based features (word frequencies, categorical counts)
  - Best for: Text classification with word counts, discrete features with counts
  - Assumes features represent counts or frequencies
- **'Bernoulli'**: For binary features (presence/absence)
  - Best for: Binary feature vectors, document classification with word presence
  - Assumes features are binary (0/1) indicators
- **'Gaussian'**: For continuous features
  - Best for: Continuous numeric measurements
  - Assumes features follow Gaussian (normal) distributions
- Default: 'Multinomial' for sparse input, 'Gaussian' for dense numeric input

**Alpha**
- Laplace smoothing parameter (additive smoothing)
- Adds alpha to feature counts to prevent zero probabilities
- Range: alpha ≥ 0
- alpha = 0: No smoothing (may cause division by zero)
- alpha = 1: Standard Laplace smoothing (recommended default)
- alpha > 1: More aggressive smoothing
- Default: 1.0

**FitPrior**
- Whether to learn class prior probabilities from data
- **'true'**: Calculate priors as P(class) = count(class) / total_samples
- **'false'**: Use uniform priors (all classes equally likely)
- Default: 'true'

**ClassPriors**
- Manually specify prior probabilities for each class
- Format: 'class1:prior1', 'class2:prior2', ...
- Priors must sum to 1.0
- Overrides FitPrior parameter
- Useful when training data is imbalanced or non-representative

### Input Table Schema

**Dense Input Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| response_column | ANY | Class labels for training (no NULLs) |
| numeric_column | NUMERIC | Continuous features (treated as Gaussian distributed) |
| categorical_column | ANY | Discrete categorical features |

**Sparse Input Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| response_column | ANY | Class labels for training (no NULLs) |
| category_column | VARCHAR | Feature names/identifiers |
| value_column | NUMERIC | Feature values (counts or binary indicators) |

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| class_label | Same as ResponseColumn | Unique class labels from training data |
| class_prior | DOUBLE PRECISION | Prior probability P(class) for each class |
| feature_name | VARCHAR | Name of feature (column name or category) |
| feature_value | VARCHAR | Specific value of categorical feature (NULL for numeric) |
| feature_type | VARCHAR | 'Categorical', 'Numeric', or 'Bernoulli' |
| feature_stats | VARCHAR (JSON) | Statistics for feature given class (mean/variance for Gaussian, counts for categorical) |
| model_metadata | VARCHAR (JSON) | Model configuration (ModelType, Alpha, FitPrior) |

Model output contains learned probability distributions for prediction by TD_NaiveBayesPredict.

### Code Examples

**Input Data: spam_emails**
```
email_id  contains_urgent  contains_money  contains_click  word_count  is_spam
1         1                1               0               150         1
2         0                0               0               300         0
3         1                0               1               100         1
4         0                0               0               250         0
5         1                1               1               75          1
```

**Example 1: Multinomial Naive Bayes for Text Classification (Dense Input)**
```sql
-- Train spam classifier with count-based features
CREATE VOLATILE TABLE spam_model AS (
    SELECT * FROM TD_NaiveBayes (
        ON spam_emails AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('is_spam')
        CategoricalInputs('contains_urgent', 'contains_money', 'contains_click')
        NumericInputs('word_count')
        ModelType('Multinomial')
        Alpha(1.0)  -- Laplace smoothing
        FitPrior('true')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Model learns P(feature|spam) and P(feature|not_spam) for each feature
```

**Example 2: Bernoulli Naive Bayes for Binary Features**
```sql
-- Train on binary feature presence/absence
CREATE VOLATILE TABLE document_model AS (
    SELECT * FROM TD_NaiveBayes (
        ON document_features AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('category')
        CategoricalInputs('has_keyword1', 'has_keyword2', 'has_keyword3',
                         'has_image', 'has_link')
        ModelType('Bernoulli')  -- Binary features
        Alpha(1.0)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Optimized for binary (0/1) indicator features
```

**Example 3: Gaussian Naive Bayes for Continuous Features**
```sql
-- Train classifier on continuous measurements
CREATE VOLATILE TABLE iris_model AS (
    SELECT * FROM TD_NaiveBayes (
        ON iris_train AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('species')
        NumericInputs('sepal_length', 'sepal_width', 'petal_length', 'petal_width')
        ModelType('Gaussian')  -- Continuous features
        Alpha(0.0)  -- No smoothing for Gaussian
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Learns mean and variance for each feature per class
-- P(feature|class) ~ N(mean, variance)
```

**Example 4: Sparse Input Format for Text Data**
```sql
-- Train on sparse representation (word:count pairs)
-- Input format: doc_id, category, word, count
CREATE VOLATILE TABLE text_model AS (
    SELECT * FROM TD_NaiveBayes (
        ON document_word_counts AS InputTable PARTITION BY 1
        USING
        ResponseColumn('category')
        CategoryColumn('word')
        ValueColumn('count')
        ModelType('Multinomial')
        Alpha(1.0)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Efficient for high-dimensional sparse features (e.g., thousands of words)
```

**Example 5: Custom Class Priors for Imbalanced Data**
```sql
-- Manually adjust class priors to handle imbalance
CREATE VOLATILE TABLE fraud_model AS (
    SELECT * FROM TD_NaiveBayes (
        ON transactions AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('is_fraud')
        NumericInputs('amount', 'merchant_category', 'time_of_day')
        CategoricalInputs('card_type', 'location_match')
        ModelType('Gaussian')
        ClassPriors('0:0.5', '1:0.5')  -- Override natural 99:1 imbalance
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Prevents model from always predicting majority class
```

**Example 6: Sentiment Analysis with Mixed Features**
```sql
-- Classify review sentiment with categorical and numeric features
CREATE VOLATILE TABLE sentiment_model AS (
    SELECT * FROM TD_NaiveBayes (
        ON product_reviews AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('sentiment')  -- 'positive', 'neutral', 'negative'
        NumericInputs('rating', 'review_length', 'positive_word_count', 'negative_word_count')
        CategoricalInputs('verified_purchase', 'product_category')
        ModelType('Gaussian')
        Alpha(1.0)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Multi-class classification (3 classes)
```

**Example 7: Customer Segment Classification**
```sql
-- Classify customers into segments
CREATE VOLATILE TABLE segment_model AS (
    SELECT * FROM TD_NaiveBayes (
        ON customer_data AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('segment')  -- 'high_value', 'medium_value', 'low_value'
        NumericInputs('total_purchases', 'avg_order_value', 'recency_days', 'lifetime_value')
        CategoricalInputs('channel_preference', 'region', 'payment_method')
        FitPrior('true')  -- Learn priors from data
        Alpha(1.0)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Predicts customer segment for targeting and personalization
```

**Example 8: Complete Workflow - Train and Predict**
```sql
-- Step 1: Train Naive Bayes model
CREATE VOLATILE TABLE churn_model AS (
    SELECT * FROM TD_NaiveBayes (
        ON customers_train AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('churned')
        NumericInputs('tenure_months', 'monthly_charges', 'total_charges', 'support_calls')
        CategoricalInputs('contract_type', 'payment_method', 'internet_service')
        ModelType('Gaussian')
        Alpha(1.0)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 2: Make predictions on test data
CREATE VOLATILE TABLE churn_predictions AS (
    SELECT * FROM TD_NaiveBayesPredict (
        ON customers_test AS InputTable PARTITION BY ANY
        ON churn_model AS ModelTable DIMENSION
        USING
        IDColumn('customer_id')
        Accumulate('actual_churned')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 3: Evaluate model performance
SELECT * FROM TD_ClassificationEvaluator (
    ON churn_predictions AS InputTable
    USING
    ObservationColumn('actual_churned')
    PredictionColumn('prediction')
) AS dt;
```

**Example 9: News Article Categorization**
```sql
-- Classify news articles into topics
CREATE VOLATILE TABLE news_model AS (
    SELECT * FROM TD_NaiveBayes (
        ON news_articles AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('topic')  -- 'politics', 'sports', 'business', 'technology', 'entertainment'
        NumericInputs('article_length', 'num_images', 'num_links', 'reading_time')
        CategoricalInputs('author_category', 'publication_section', 'time_of_day')
        ModelType('Gaussian')
        Alpha(1.0)
        FitPrior('true')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Multi-class classification (5 topics)
-- Fast training and prediction for real-time categorization
```

**Example 10: Medical Diagnosis with No Smoothing**
```sql
-- Predict disease based on symptoms and test results
CREATE VOLATILE TABLE diagnosis_model AS (
    SELECT * FROM TD_NaiveBayes (
        ON patient_records AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('diagnosis')
        NumericInputs('temperature', 'blood_pressure', 'heart_rate', 'age', 'bmi')
        CategoricalInputs('gender', 'smoking_status', 'family_history', 'symptoms')
        ModelType('Gaussian')
        Alpha(0.0)  -- No smoothing for medical data with complete coverage
        FitPrior('false')  -- Use uniform priors (don't trust training distribution)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Provides probability distribution over diagnoses
```

### Algorithm Details

**Naive Bayes Theorem:**

For a sample with features X = (x₁, x₂, ..., xₙ), the predicted class is:

```
ŷ = argmax P(class|X)
      class

Using Bayes' theorem:
P(class|X) = P(X|class) × P(class) / P(X)

With naive independence assumption:
P(X|class) = P(x₁|class) × P(x₂|class) × ... × P(xₙ|class)

Therefore:
P(class|X) ∝ P(class) × ∏ᵢ P(xᵢ|class)
```

Since P(X) is constant across classes, we can ignore it for classification.

**Multinomial Naive Bayes:**

For count-based features (word frequencies):
```
P(xᵢ|class) = (count(xᵢ, class) + α) / (count(class) + α × n_features)

Where:
- count(xᵢ, class) = number of times feature i appears in class
- α = smoothing parameter (alpha)
- n_features = total number of distinct features
```

**Bernoulli Naive Bayes:**

For binary features (presence/absence):
```
P(xᵢ|class) = P(i|class) × xᵢ + (1 - P(i|class)) × (1 - xᵢ)

Where:
- P(i|class) = (count(i present in class) + α) / (count(class) + 2α)
- xᵢ ∈ {0, 1}
```

**Gaussian Naive Bayes:**

For continuous features:
```
P(xᵢ|class) = (1 / √(2π σᵢ²)) × exp(-(xᵢ - μᵢ)² / (2σᵢ²))

Where:
- μᵢ = mean of feature i for class
- σᵢ² = variance of feature i for class
```

**Laplace Smoothing:**

Prevents zero probabilities when feature values not seen during training:
```
Without smoothing (α = 0): P(x|class) = 0 if x never observed in class
With smoothing (α = 1): P(x|class) = α / (count(class) + α × n_features)

Ensures all probabilities > 0, preventing prediction failures.
```

**Class Priors:**

If FitPrior = 'true':
```
P(class) = count(class) / total_samples
```

If FitPrior = 'false':
```
P(class) = 1 / n_classes (uniform distribution)
```

If ClassPriors specified:
```
P(class) = user-specified value
```

### Use Cases and Applications

**1. Text Classification and NLP**
- Document categorization by topic or genre
- News article classification
- Email routing and organization
- Content moderation and filtering
- Language detection
- Author attribution
- Sentiment analysis at scale

**2. Spam and Fraud Detection**
- Email spam filtering
- SMS spam detection
- Comment spam identification
- Fraudulent transaction detection
- Fake review detection
- Bot account identification

**3. Sentiment Analysis**
- Product review sentiment classification
- Social media sentiment monitoring
- Customer feedback analysis
- Brand perception tracking
- Movie/restaurant review classification
- Survey response sentiment

**4. Customer Analytics**
- Customer segment classification
- Churn prediction
- Lead scoring and qualification
- Purchase intent prediction
- Customer lifetime value prediction
- Next best action recommendation

**5. Medical and Healthcare**
- Disease diagnosis from symptoms
- Patient risk stratification
- Medical record classification
- Drug response prediction
- Treatment recommendation
- Health outcome prediction

**6. E-Commerce and Recommendation**
- Product category prediction
- User preference modeling
- Content recommendation
- Purchase likelihood scoring
- Cross-sell opportunity identification
- Dynamic pricing segment assignment

**7. Real-Time Classification**
- Stream processing and real-time decisions
- Low-latency prediction services
- Online content filtering
- Real-time fraud detection
- Instant customer support routing
- Live sentiment analysis

**8. High-Dimensional Problems**
- Text data with thousands of words
- Gene expression classification
- Image feature classification
- Sparse feature sets
- Bag-of-words models
- TF-IDF feature classification

**9. Baseline and Benchmark Models**
- Establish performance baseline
- Quick proof-of-concept models
- Benchmark for complex models
- Feature importance assessment
- Simple interpretable models
- Rapid prototyping

**10. Multi-Class Classification**
- News topic classification (many categories)
- Product categorization (hierarchical)
- Intent recognition (multiple intents)
- Multi-label classification
- Fine-grained categorization
- Taxonomic classification

### Important Notes

**Feature Independence Assumption:**
- Naive Bayes assumes all features are independent given the class
- This assumption is rarely true in practice (e.g., words in documents are correlated)
- Despite this, Naive Bayes often performs well because:
  - It only needs to rank classes correctly, not estimate exact probabilities
  - Errors in probability estimates may cancel out
  - Independence assumption acts as regularization, reducing overfitting

**Model Type Selection:**
- **Multinomial**: Count-based features (word frequencies, categorical counts)
- **Bernoulli**: Binary features (word presence/absence, yes/no indicators)
- **Gaussian**: Continuous numeric features (measurements, scores)
- Using wrong model type can severely degrade performance
- Text classification typically uses Multinomial or Bernoulli

**Zero Probability Problem:**
- Without smoothing (α=0), encountering unseen feature value causes P=0
- This makes entire prediction probability zero (multiplication)
- Always use smoothing (α≥1) unless certain all feature values are represented
- α=1 (Laplace smoothing) is recommended default

**Class Imbalance:**
- Naive Bayes naturally handles imbalance through learned priors
- With severe imbalance, consider using ClassPriors to adjust
- Or use FitPrior='false' for uniform priors
- Alternative: resample training data or use cost-sensitive evaluation

**Feature Scaling:**
- Gaussian Naive Bayes does NOT require feature scaling
- Probability calculations use mean and variance, which are scale-invariant
- Unlike distance-based algorithms (KNN, SVM), no normalization needed
- However, scaling can help with numerical stability for extreme values

**Missing Values:**
- Naive Bayes handles missing values naturally
- Missing feature simply not included in probability multiplication
- Alternative: impute missing values before training
- Categorical: treat missing as separate category
- Numeric: impute with mean/median

**Computational Efficiency:**
- Training: O(n × d) - linear in samples and features
- Prediction: O(k × d) - linear in classes and features
- Very fast compared to complex models
- Scales well to large datasets and high dimensions
- Suitable for real-time prediction

**Probability Calibration:**
- Naive Bayes probability estimates are often poorly calibrated
- Probabilities may be too extreme (too close to 0 or 1)
- Use predictions for ranking/classification, not calibrated probability needs
- Apply calibration methods (isotonic regression, Platt scaling) if needed

**Sparse Input Efficiency:**
- Sparse format highly efficient for text with thousands of features
- Only non-zero feature values stored and processed
- Reduces memory and computation dramatically
- Use CategoryColumn/ValueColumn for sparse data

**Output Interpretation:**
- Model table contains learned probability distributions
- class_prior: P(class) for each class
- feature_stats: P(feature|class) distributions
- Use TD_NaiveBayesPredict for predictions
- Predictions include probability estimates for each class

### Best Practices

**1. Choose Appropriate Model Type**
- Text with word counts → Multinomial
- Text with word presence → Bernoulli
- Continuous measurements → Gaussian
- Mixed features → Separate models or transform to same type
- Match model type to feature distribution

**2. Apply Laplace Smoothing**
- Always use α ≥ 1 for production models
- α = 1 is recommended default
- Increase α if overfitting to rare features
- Only use α = 0 if certain all values are represented
- Smoothing is critical for text classification

**3. Handle Imbalanced Classes**
- Monitor class distribution in training data
- Use ClassPriors to adjust for imbalance if needed
- Set FitPrior='false' for uniform priors if training is non-representative
- Evaluate with balanced metrics (F1, balanced accuracy)
- Consider resampling techniques

**4. Prepare Features Appropriately**
- Remove highly correlated features (violates independence)
- Handle missing values before training
- Encode categorical features properly
- For text: remove stop words, apply stemming/lemmatization
- Feature engineering impacts Naive Bayes significantly

**5. Use Sparse Format for High-Dimensional Data**
- Text data with thousands of words
- One-hot encoded categorical features
- Any dataset where most feature values are zero
- Dramatically reduces memory and computation
- Enables scaling to millions of features

**6. Validate Feature Independence**
- While perfect independence is rare, extreme correlation hurts
- Check correlation matrix for numeric features
- Remove redundant features
- Feature selection can improve performance
- Trade-off between features and independence violation

**7. Compare with Baseline**
- Establish simple baseline (e.g., predict most common class)
- Compare Naive Bayes to baseline
- Use as benchmark for complex models
- Often Naive Bayes is sufficient, avoiding complex models
- Balance accuracy vs interpretability vs speed

**8. Leverage Probability Outputs**
- Use probability scores for ranking
- Set decision thresholds based on business requirements
- Top-k predictions for multi-label scenarios
- Confidence filtering (only predict if probability > threshold)
- Probability distributions inform decision-making

**9. Optimize for Production**
- Naive Bayes is inherently production-friendly (fast)
- Model is just probability tables (small memory footprint)
- No hyperparameter tuning typically needed
- Incremental learning possible by updating statistics
- Suitable for real-time APIs and stream processing

**10. Monitor and Evaluate**
- Track prediction accuracy over time
- Monitor for distribution shift (features change)
- Evaluate on held-out test set
- Use appropriate metrics (accuracy, precision, recall, F1)
- Compare probabilities to actual outcomes (calibration)
- Retrain periodically with new data

### Related Functions

**Model Training:**
- **TD_DecisionForest** - Ensemble tree model, often more accurate but slower
- **TD_GLM** - Logistic regression for binary/multinomial classification
- **TD_XGBoost** - Gradient boosting for higher accuracy
- **TD_SVM** - Support Vector Machine for classification

**Model Scoring:**
- **TD_NaiveBayesPredict** - Apply trained Naive Bayes model to new data
- **TD_NaiveBayesTextClassifier** - Specialized text classification variant

**Model Evaluation:**
- **TD_ClassificationEvaluator** - Compute accuracy, precision, recall, F1, confusion matrix
- **TD_ROC** - ROC curve analysis for binary classification

**Feature Preparation:**
- **TD_OneHotEncodingFit** - Encode categorical features
- **TD_SimpleImputeFit** - Handle missing values
- **TD_ScaleFit** - Standardize features (generally not needed for Naive Bayes)
- **TD_TextParser** - Parse and tokenize text for text classification

**Text Analytics:**
- **TD_TF** - Term frequency calculation for text features
- **TD_TFIDF** - TF-IDF weighting for text features

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf
- [Naive Bayes Classifier - Wikipedia](https://en.wikipedia.org/wiki/Naive_Bayes_classifier)
- [Scikit-learn Naive Bayes Documentation](https://scikit-learn.org/stable/modules/naive_bayes.html)

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Model Training Functions
