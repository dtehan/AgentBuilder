# TD_NaiveBayesTextClassifierTrainer

## Function Name
- **TD_NaiveBayesTextClassifierTrainer**: Trains a Naive Bayes text classification model using labeled document-token pairs

## Description
The TD_NaiveBayesTextClassifierTrainer function calculates the conditional probabilities for token-category pairs, the prior probabilities, and the missing token probabilities for all categories. The trainer function trains the model with the probability values, and the predict function (TD_NaiveBayesTextClassifierPredict) uses the values to classify documents into categories.

### Characteristics
- Probabilistic text classification approach
- Two model types: Multinomial and Bernoulli
- Handles missing tokens with probability estimates
- Outputs compact probability model
- Fast training on labeled data
- Suitable for multi-class classification

### How Naive Bayes Works
Naive Bayes classifiers apply Bayes' theorem with the "naive" assumption that features (tokens) are independent given the class label. Despite this simplification, they often perform well for text classification.

**Model Types**:
- **Multinomial**: Uses token counts (good for longer documents, multiple occurrences matter)
- **Bernoulli**: Uses token presence/absence (good for shorter documents, binary features)

## When to Use TD_NaiveBayesTextClassifierTrainer

### Text Classification Tasks
- Document categorization (topics, themes, genres)
- Sentiment classification (positive/negative/neutral)
- Spam detection (spam/not spam)
- Language identification
- Intent classification for chatbots

### When Naive Bayes is Appropriate
**Use when**:
- You have labeled training data
- Features are relatively independent
- Need fast training and prediction
- Interpretable model is important
- Working with text/categorical data
- Have limited computational resources

**Consider alternatives when**:
- Feature interactions are important
- Need highest accuracy (vs speed/simplicity)
- Have very small training sets
- Feature dependencies are strong

## Syntax

```sql
TD_NaiveBayesTextClassifierTrainer (
    ON { table | view | (query) } AS InputTable
    [ OUT [ PERMANENT | VOLATILE ] TABLE ModelTable (model_table_name) ]
    USING
    TokenColumn ('token_column')
    DocCategoryColumn ('doc_category_column')
    [{
        [ ModelType ('Multinomial') ]
    }
    |
    {
        ModelType ('Bernoulli')
        DocIDColumn ('doc_id_column')
    }]
)
```

**Note:** You can call this function from:
- The FROM clause of a SELECT statement
- As part of a CREATE TABLE statement
- As part of a CREATE VIEW statement

## Required Elements

### ON Clause
Accepts the InputTable clause containing labeled training documents in document-token format.

### TokenColumn
**Required**: Specify the InputTable column name that contains the classified tokens.
- **Data Type**: CHAR or VARCHAR
- **Purpose**: Individual words/terms from documents

### DocCategoryColumn
**Required**: Specify the InputTable column name that contains the document category.
- **Data Type**: CHAR or VARCHAR
- **Purpose**: Class labels for training documents

### DocIDColumn
**Required for Bernoulli model type**: Specify the InputTable column name that contains the document identifier.
- **Data Type**: BYTEINT, SMALLINT, INTEGER, BIGINT or CHAR/VARCHAR
- **Purpose**: Uniquely identifies documents for Bernoulli model

## Optional Elements

### OUT Clause
Specify output model table name and type.
- **Format**: OUT [PERMANENT | VOLATILE] TABLE ModelTable (model_table_name)
- **Default**: Results returned to client
- **Options**:
  - PERMANENT TABLE: Persists after session
  - VOLATILE TABLE: Removed at session end

### ModelType
Specify the model type of the text classifier.
- **Default**: 'Multinomial'
- **Values**:
  - **'Multinomial'**: Token frequency matters (counts multiple occurrences)
  - **'Bernoulli'**: Token presence matters (binary: present or absent)

**Choosing Model Type**:

**Multinomial**:
- Use for longer documents where term frequency is meaningful
- Captures how often terms appear
- Good for topic classification, longer reviews
- No DocIDColumn needed

**Bernoulli**:
- Use for shorter documents where presence/absence is more important
- Binary features (word appears or doesn't)
- Good for spam detection, short messages
- Requires DocIDColumn

## Input Schema

### Input Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| doc_id_column | BYTEINT, SMALLINT, INTEGER, BIGINT, CHAR, VARCHAR | The InputTable column name that contains the document identifier. **Required for Bernoulli model type** |
| token_column | CHAR or VARCHAR | The column name that contains the classified training tokens from a tokenization function |
| doc_category_column | CHAR or VARCHAR | The category of the document (class label) |

**Important**: The following vocabulary token names are reserved and cannot be used:
- NAIVE_BAYES_TEXT_MODEL_TYPE
- NAIVE_BAYES_PRIOR_PROBABILITY
- NAIVE_BAYES_MISSING_TOKEN_PROBABILITY

## Output Schema

### Output Table Schema

The model table contains probabilities needed for classification:

| Column | Data Type | Description |
|--------|-----------|-------------|
| token | VARCHAR (UNICODE) | The classified training tokens |
| category | VARCHAR (UNICODE) | The category of the token |
| prob | DOUBLE PRECISION | The probability of the token in the category |

**Special Rows in Model**:
- **NAIVE_BAYES_TEXT_MODEL_TYPE**: Indicates model type (MULTINOMIAL or BERNOULLI)
- **NAIVE_BAYES_PRIOR_PROBABILITY**: Prior probability for each category P(C)
- **NAIVE_BAYES_MISSING_TOKEN_PROBABILITY**: Probability for unseen tokens in each category

## Code Examples

### Example Setup: Prepare Training Data

Create and tokenize training documents:

```sql
-- Original training documents
CREATE TABLE complaints_train (
    doc_id INTEGER,
    doc_name VARCHAR(10),
    text_data VARCHAR(1000),
    category VARCHAR(20)
);

INSERT INTO complaints_train VALUES
(1, 'A', 'ELECTRICAL CONTROL MODULE IS SHORTENING OUT, CAUSING THE VEHICLE TO STALL. ENGINE WILL BECOME TOTALLY INOPERATIVE.', 'no_crash');

INSERT INTO complaints_train VALUES
(2, 'B', 'ABS BRAKES FAIL TO OPERATE PROPERLY, AND AIR BAGS FAILED TO DEPLOY DURING A CRASH AT APPROX. 28 MPH IMPACT.', 'crash');

INSERT INTO complaints_train VALUES
(3, 'C', 'WHILE DRIVING AT 60 MPH GAS PEDAL GOT STUCK DUE TO THE RUBBER THAT IS AROUND THE GAS PEDAL.', 'no_crash');

INSERT INTO complaints_train VALUES
(4, 'D', 'THERE IS A KNOCKING NOISE COMING FROM THE CATALYTIC CONVERTER, AND THE VEHICLE IS STALLING.', 'no_crash');

INSERT INTO complaints_train VALUES
(5, 'E', 'CONSUMER WAS MAKING A TURN, DRIVING AT APPROX 5-10 MPH WHEN CONSUMER HIT ANOTHER VEHICLE. UPON IMPACT, DUAL AIRBAGS DID NOT DEPLOY.', 'crash');

-- Tokenize training documents
CREATE MULTISET TABLE complaints_tokenized AS (
    SELECT
        doc_id,
        category,
        LOWER(CAST(token AS VARCHAR(20))) AS token
    FROM TD_TextParser (
        ON complaints_train AS InputTable
        USING
        TextColumn ('text_data')
        OutputByWord ('true')
        Accumulate ('doc_id', 'category')
    ) AS dt
) WITH DATA;
```

**Tokenized Training Data**:

| doc_id | category | token |
|--------|----------|-------|
| 1 | no_crash | vehicl |
| 1 | no_crash | motor |
| 1 | no_crash | separ |
| 2 | crash | deploy |
| 2 | crash | anoth |
| 2 | crash | end |
| 2 | crash | vehicl |
| 2 | crash | airbag |
| 3 | no_crash | sunroof |
| 3 | no_crash | leak |
| 4 | crash | driver |
| 4 | crash | sustain |
| 4 | crash | injuri |

### Example 1: Train Multinomial Model

Train a Multinomial Naive Bayes model:

```sql
SELECT * FROM TD_NaiveBayesTextClassifierTrainer (
    ON complaints_tokenized AS InputTable
    USING
    TokenColumn ('token')
    DocCategoryColumn ('category')
    ModelType ('Multinomial')
) AS dt
ORDER BY category, token;
```

**Purpose**: Train model where token frequency matters (counts multiple occurrences).

**Output Model Table**:

| token | category | prob |
|-------|----------|------|
| driver | crash | 0.076923077 |
| vehicl | no_crash | 0.086956522 |
| leak | no_crash | 0.086956522 |
| anoth | crash | 0.076923077 |
| deploy | crash | 0.076923077 |
| airbag | crash | 0.076923077 |
| from | no_crash | 0.086956522 |
| NAIVE_BAYES_PRIOR_PROBABILITY | crash | 0.588235294 |
| separ | no_crash | 0.086956522 |
| end | crash | 0.076923077 |
| NAIVE_BAYES_MISSING_TOKEN_PROBABILITY | crash | 0.038461538 |
| vehicl | crash | 0.076923077 |
| NAIVE_BAYES_PRIOR_PROBABILITY | no_crash | 0.411764706 |
| NAIVE_BAYES_MISSING_TOKEN_PROBABILITY | no_crash | 0.043478261 |
| NAIVE_BAYES_TEXT_MODEL_TYPE | MULTINOMIAL | 1.000000000 |

**Interpretation**:
- Prior probability of 'crash': 58.8%
- Prior probability of 'no_crash': 41.2%
- Token probabilities: P(token|category)
- Missing token probabilities for smoothing

### Example 2: Train Bernoulli Model

Train a Bernoulli Naive Bayes model (presence/absence):

```sql
SELECT * FROM TD_NaiveBayesTextClassifierTrainer (
    ON complaints_tokenized AS InputTable
    USING
    TokenColumn ('token')
    DocCategoryColumn ('category')
    DocIDColumn ('doc_id')
    ModelType ('Bernoulli')
) AS dt
ORDER BY category, token;
```

**Purpose**: Train model where only token presence matters (binary features).

**Output Model Table**:

| token | category | prob |
|-------|----------|------|
| airbag | crash | 0.666666667 |
| anoth | crash | 0.666666667 |
| deploy | crash | 0.666666667 |
| driver | crash | 0.333333333 |
| leak | no_crash | 0.5 |
| separ | no_crash | 0.5 |
| vehicl | crash | 0.666666667 |
| vehicl | no_crash | 0.5 |
| NAIVE_BAYES_PRIOR_PROBABILITY | crash | 0.4 |
| NAIVE_BAYES_PRIOR_PROBABILITY | no_crash | 0.6 |
| NAIVE_BAYES_TEXT_MODEL_TYPE | BERNOULLI | 1.000000000 |

**Interpretation**:
- Token probabilities: P(token present|category)
- For example, 66.7% of 'crash' documents contain 'airbag'

### Example 3: Save Model to Permanent Table

Create persistent model table:

```sql
SELECT * FROM TD_NaiveBayesTextClassifierTrainer (
    ON complaints_tokenized AS InputTable
    OUT PERMANENT TABLE complaints_nb_model
    USING
    TokenColumn ('token')
    DocCategoryColumn ('category')
    ModelType ('Multinomial')
) AS dt;

-- Model saved to complaints_nb_model table
-- Can be reused for predictions without retraining
```

**Purpose**: Save trained model for repeated use with predict function.

## Common Use Cases

### 1. Sentiment Classification

Train model to classify review sentiment:

```sql
-- Prepare sentiment training data
CREATE TABLE review_tokens AS (
    SELECT
        review_id,
        CASE
            WHEN rating >= 4 THEN 'positive'
            WHEN rating <= 2 THEN 'negative'
            ELSE 'neutral'
        END as sentiment,
        token
    FROM TD_TextParser (
        ON product_reviews AS InputTable
        USING
        TextColumn ('review_text')
        ConvertToLowerCase ('true')
        RemoveStopWords ('true')
        Accumulate ('review_id', 'rating')
    ) AS dt
    WHERE rating IN (1,2,4,5)  -- Exclude neutral for clarity
) WITH DATA;

-- Train sentiment classifier
SELECT * FROM TD_NaiveBayesTextClassifierTrainer (
    ON review_tokens AS InputTable
    OUT PERMANENT TABLE sentiment_model
    USING
    TokenColumn ('token')
    DocCategoryColumn ('sentiment')
    ModelType ('Multinomial')
) AS dt;
```

### 2. Spam Detection

Train spam classifier:

```sql
-- Tokenize email data
CREATE TABLE email_tokens AS (
    SELECT
        email_id,
        is_spam,
        token
    FROM TD_TextParser (
        ON email_corpus AS InputTable
        USING
        TextColumn ('email_body')
        ConvertToLowerCase ('true')
        Accumulate ('email_id', 'is_spam')
    ) AS dt
) WITH DATA;

-- Train spam detector (Bernoulli model for short messages)
SELECT * FROM TD_NaiveBayesTextClassifierTrainer (
    ON email_tokens AS InputTable
    OUT PERMANENT TABLE spam_detector_model
    USING
    TokenColumn ('token')
    DocCategoryColumn ('is_spam')
    DocIDColumn ('email_id')
    ModelType ('Bernoulli')
) AS dt;
```

### 3. Topic Classification

Train multi-class topic classifier:

```sql
-- Tokenize documents by topic
CREATE TABLE topic_tokens AS (
    SELECT
        doc_id,
        topic,
        token
    FROM TD_TextParser (
        ON news_articles AS InputTable
        USING
        TextColumn ('article_text')
        ConvertToLowerCase ('true')
        RemoveStopWords ('true')
        StemTokens ('true')
        Accumulate ('doc_id', 'topic')
    ) AS dt
) WITH DATA;

-- Train topic classifier
SELECT * FROM TD_NaiveBayesTextClassifierTrainer (
    ON topic_tokens AS InputTable
    OUT PERMANENT TABLE topic_classifier_model
    USING
    TokenColumn ('token')
    DocCategoryColumn ('topic')
    ModelType ('Multinomial')
) AS dt;
```

### 4. Intent Classification (Chatbot)

Train intent classifier for chatbot:

```sql
-- Prepare training utterances
CREATE TABLE intent_tokens AS (
    SELECT
        utterance_id,
        intent,
        token
    FROM TD_TextParser (
        ON training_utterances AS InputTable
        USING
        TextColumn ('user_message')
        ConvertToLowerCase ('true')
        Accumulate ('utterance_id', 'intent')
    ) AS dt
) WITH DATA;

-- Train intent classifier (Bernoulli for short messages)
SELECT * FROM TD_NaiveBayesTextClassifierTrainer (
    ON intent_tokens AS InputTable
    OUT PERMANENT TABLE chatbot_intent_model
    USING
    TokenColumn ('token')
    DocCategoryColumn ('intent')
    DocIDColumn ('utterance_id')
    ModelType ('Bernoulli')
) AS dt;
```

## Best Practices

### 1. Choose Appropriate Model Type

**Multinomial**:
```sql
-- For longer documents, reviews, articles
ModelType ('Multinomial')

-- When:
-- - Documents are longer (>50 words)
-- - Term frequency is meaningful
-- - Topic classification
-- - No DocIDColumn needed
```

**Bernoulli**:
```sql
-- For shorter messages, titles, tags
ModelType ('Bernoulli')
DocIDColumn ('doc_id')  -- Required!

-- When:
-- - Documents are short (<50 words)
-- - Presence/absence is what matters
-- - Spam detection
-- - Requires DocIDColumn
```

### 2. Prepare Training Data Properly

```sql
-- Good training data pipeline:
-- 1. Tokenize with TD_TextParser
-- 2. Clean text (lowercase, remove stops, stem)
-- 3. Ensure balanced classes (or handle imbalance)
-- 4. Remove very rare tokens (appear in <2 documents)
-- 5. Remove very common tokens (appear in >90% documents)

-- Example preprocessing:
CREATE TABLE clean_tokens AS (
    SELECT doc_id, category, token
    FROM (
        SELECT
            doc_id,
            category,
            token,
            COUNT(*) OVER (PARTITION BY token) as token_doc_freq
        FROM parsed_docs
    ) t
    WHERE token_doc_freq >= 2  -- Remove very rare
      AND token_doc_freq <= (0.9 * (SELECT COUNT(DISTINCT doc_id) FROM parsed_docs))
      AND CHAR_LENGTH(token) >= 3  -- Remove short tokens
) WITH DATA;
```

### 3. Handle Class Imbalance

```sql
-- For imbalanced classes, consider:
-- 1. Undersample majority class
-- 2. Oversample minority class
-- 3. Use stratified sampling

-- Example: Balance classes by undersampling
CREATE TABLE balanced_training AS (
    SELECT * FROM (
        SELECT *, ROW_NUMBER() OVER (PARTITION BY category ORDER BY RANDOM()) as rn
        FROM training_tokens
    ) t
    WHERE rn <= (SELECT MIN(class_count) FROM (
        SELECT category, COUNT(DISTINCT doc_id) as class_count
        FROM training_tokens
        GROUP BY category
    ) counts)
) WITH DATA;
```

### 4. Reserve Tokens

**Never use these token names** (they're reserved):
- NAIVE_BAYES_TEXT_MODEL_TYPE
- NAIVE_BAYES_PRIOR_PROBABILITY
- NAIVE_BAYES_MISSING_TOKEN_PROBABILITY

### 5. Model Persistence

```sql
-- Always save model to permanent table for reuse
OUT PERMANENT TABLE my_classifier_model

-- Benefits:
-- - Reuse without retraining
-- - Consistent predictions
-- - Share model across sessions
-- - Track model versions
```

### 6. Validate Model Quality

```sql
-- After training, check model characteristics:

-- 1. Check class priors
SELECT token, category, prob
FROM model_table
WHERE token = 'NAIVE_BAYES_PRIOR_PROBABILITY'
ORDER BY category;

-- 2. Check most probable tokens per class
SELECT category, token, prob
FROM model_table
WHERE token NOT LIKE 'NAIVE_BAYES%'
ORDER BY category, prob DESC
LIMIT 20;

-- 3. Verify model type
SELECT token, category, prob
FROM model_table
WHERE token = 'NAIVE_BAYES_TEXT_MODEL_TYPE';
```

## Related Functions

- **TD_NaiveBayesTextClassifierPredict**: Use trained model to classify new documents
- **TD_TextParser**: Tokenize documents before training
- **TD_TextMorph**: Lemmatize tokens for better features
- **TD_TFIDF**: Alternative feature engineering approach

## Notes and Limitations

### 1. Input Data Format
- Requires document-token pairs (one row per token occurrence)
- Typically created by TD_TextParser or similar tokenization
- Must include document category labels
- Bernoulli model requires document IDs

### 2. Model Type Selection
- **Multinomial**: Does NOT require DocIDColumn
- **Bernoulli**: REQUIRES DocIDColumn
- Cannot change model type after training
- Must retrain for different model type

### 3. Reserved Token Names
The following tokens are reserved and cannot appear in training data:
- NAIVE_BAYES_TEXT_MODEL_TYPE
- NAIVE_BAYES_PRIOR_PROBABILITY
- NAIVE_BAYES_MISSING_TOKEN_PROBABILITY

Using these will cause errors or incorrect models.

### 4. Probability Calculations
- Uses Laplace smoothing for unseen tokens
- Missing token probability prevents zero probabilities
- Prior probabilities calculated from training data distribution
- Conditional probabilities: P(token|category)

### 5. Model Size
- Model table size proportional to:
  - Number of unique tokens
  - Number of categories
  - Approximately: |unique_tokens| × |categories| rows
- Large vocabularies create large models
- Consider feature selection for very large vocabularies

### 6. Training Data Requirements
- Needs labeled data (document-category pairs)
- More training data generally improves performance
- Should have multiple examples per category
- Ideally, balanced class distribution

### 7. Feature Independence Assumption
- Assumes tokens are independent given category
- This is "naive" but often works well in practice
- May underperform when feature interactions are important
- Consider more sophisticated models (XGBoost, GLM) for complex dependencies

### 8. Character Sets
- Supports CHAR and VARCHAR data types
- Both LATIN and UNICODE character sets supported
- Ensure consistent character sets across training data

### 9. Output Format
- Model stored as probability table
- Not human-readable without interpretation
- Use with TD_NaiveBayesTextClassifierPredict for classification
- Can inspect probabilities for model understanding

### 10. Retraining
- Must retrain if:
  - New categories emerge
  - Training data significantly changes
  - Model performance degrades
  - Feature engineering changes
- Training is typically fast (seconds to minutes)

## Version Information

- **Function Version**: Based on Teradata Database Analytic Functions Version 17.20
- **Generated**: November 28, 2025
- **Algorithm**: Naive Bayes text classification (Multinomial and Bernoulli models)
