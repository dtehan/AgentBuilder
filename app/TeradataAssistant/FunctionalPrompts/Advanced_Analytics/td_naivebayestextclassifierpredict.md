# TD_NaiveBayesTextClassifierPredict

## Function Name
- **TD_NaiveBayesTextClassifierPredict**: Applies trained Naive Bayes model to classify new documents

## Description
This function uses the model output by TD_NaiveBayesTextClassifierTrainer function to analyze the input data and make predictions. It classifies documents into categories based on the trained probabilistic model.

### Characteristics
- Uses trained Naive Bayes model for classification
- Supports both Multinomial and Bernoulli models
- Returns top-K predictions or specific response categories
- Calculates log-likelihood and probability scores
- Handles unseen tokens with smoothing
- Fast prediction on new documents

### How It Works
The function applies Bayes' theorem to calculate the probability that a document belongs to each category based on its tokens and the trained model probabilities. It returns the most likely categories with their confidence scores.

## When to Use TD_NaiveBayesTextClassifierPredict

### After Training a Model
Use this function after training a Naive Bayes model with TD_NaiveBayesTextClassifierTrainer to:
- Classify new, unlabeled documents
- Predict categories for test data
- Apply model to production data
- Evaluate model performance

### Classification Tasks
- Document categorization
- Sentiment prediction
- Spam detection
- Topic identification
- Intent classification

## Syntax

```sql
TD_NaiveBayesTextClassifierPredict (
    ON { table | view | (query) } AS PredictorValues
        PARTITION BY doc_id_column [,...]
    ON { table | view | (query) } AS Model DIMENSION
    USING
    InputTokenColumn ('input_token_column')
    [ ModelType ({ 'Multinomial' | 'Bernoulli' }) ]
    DocIDColumns ({ 'doc_id_column' | 'doc_id_column_range' }[,...])
    [ ModelTokenColumn ('model_token_column')
      ModelCategoryColumn ('model_category_column')
      ModelProbColumn ('model_probability_column') ]
    [ TopK ({ num_of_top_k_predictions | 'num_of_top_k_predictions' }) |
      Responses ('response' [,...]) ]
    [ OutputProb ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
    [ Accumulate ({ 'accumulate_column' | accumulate_column_range }[,...]) ]
)
```

**Note:** You can call this function from:
- The FROM clause of a SELECT statement
- As part of a CREATE TABLE statement
- As part of a CREATE VIEW statement

## Required Elements

### ON Clause (PredictorValues)
Contains test data for which to predict outcomes, in document-token pairs.
- **Format**: PARTITION BY doc_id_column
- **Purpose**: Groups tokens by document for classification

**Input Preparation**: To transform input documents into this form, use:
- TD_TextParser (recommended)
- ML Engine TextTokenizer or TextParser

### ON Clause (Model)
Model output by TD_NaiveBayesTextClassifierTrainer.
- **Format**: DIMENSION (model loaded into memory)
- **Source**: Trained model table from trainer function

### InputTokenColumn
**Required**: Specify the name of the PredictorValues column that contains the tokens.
- **Data Type**: CHARACTER or VARCHAR
- **Purpose**: Tokens from documents to classify

### DocIDColumns
**Required**: Specify the names of the PredictorValues columns that contain the document identifier.
- **Format**: Single column or range
- **Purpose**: Uniquely identifies documents for prediction
- **Examples**: 'doc_id' or '[0:1]' for first two columns

## Optional Elements

### ModelType
Specify the model type of the text classifier.
- **Default**: 'Multinomial'
- **Values**: 'Multinomial' or 'Bernoulli'
- **Note**: Must match the model type used during training

### ModelTokenColumn
Specify the name of the Model table column that contains the tokens.
- **Default**: First column of Model table
- **Purpose**: Maps to token vocabulary in model

### ModelCategoryColumn
Specify the name of the Model table column that contains the prediction categories.
- **Default**: Second column of Model table
- **Purpose**: Identifies category labels

### ModelProbColumn
Specify the name of the Model table column that contains the probability values.
- **Default**: Third column of Model table
- **Purpose**: Retrieves trained probabilities

**Important**: Specify either all or none of ModelTokenColumn, ModelCategoryColumn, and ModelProbColumn.

### TopK
Specify the number of most likely prediction categories to output with their log-likelihood values.
- **Purpose**: Get top predictions (e.g., top 10 most likely categories)
- **Default**: All prediction categories
- **Disallowed With**: Responses parameter
- **Example**: TopK ('5') returns 5 most likely categories

### Responses
Specify the labels for which to output log-likelihood values and probabilities.
- **Purpose**: Get predictions for specific categories only
- **Disallowed With**: TopK parameter
- **Example**: Responses ('spam', 'not_spam')

**Note**: Specifying neither TopK nor Responses is equivalent to specifying TopK.

### OutputProb
Specify whether to output the calculated probability for each observation.
- **Default**: 'false'
- **Values**: 'true' or 'false'
- **Purpose**: Include probability scores along with log-likelihood
- **Calculation**: max(softmax(loglik)) or softmax(loglik_response)

### Accumulate
Specify the names of the PredictorValues table columns to copy to the output table.
- **Purpose**: Preserve metadata in predictions
- **Note**: Not applicable with token-embedding operation

## Input Schema

### PredictorValues Schema

Contains test data in document-token pairs:

| Column | Data Type | Description |
|--------|-----------|-------------|
| doc_id_column | CHARACTER, VARCHAR, INTEGER, or SMALLINT | Identifier of document containing test tokens |
| token_column | CHARACTER or VARCHAR | Test token |
| accumulate_column | Any | Column to copy to output table |

### Model Schema

Model output by TD_NaiveBayesTextClassifierTrainer:

| Column | Data Type | Description |
|--------|-----------|-------------|
| token | CHARACTER or VARCHAR (UNICODE or LATIN) | Classified training token |
| category | CHARACTER or VARCHAR (UNICODE or LATIN) | Prediction category for token |
| prob | DOUBLE PRECISION | Probability that token is in category |

## Output Schema

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| doc_id | CHARACTER, VARCHAR, INTEGER, or SMALLINT | Single- or multiple-column document identifier |
| prediction | VARCHAR | Prediction category (most likely class) |
| loglik | DOUBLE PRECISION | Log-likelihood that document belongs to category |
| loglik_response | DOUBLE PRECISION | [Appears only with Responses] Log-likelihood for specified response |
| prob | DOUBLE PRECISION | [Appears with OutputProb('true') without Responses] Probability that document belongs to predicted class: max(softmax(loglik)) |
| prob_response | DOUBLE PRECISION | [Appears with OutputProb('true') and Responses] Probability for specified response: softmax(loglik_response) |
| accumulate_column | Same as in PredictorValues | Column copied from PredictorValues table |

**Log-Likelihood**: Natural logarithm of probability (negative values, closer to 0 is higher probability)
**Probability**: Actual probability value (0 to 1, higher is more confident)

## Code Examples

### Example Setup: Prepare Test Data

Using the model trained in TD_NaiveBayesTextClassifierTrainer examples:

```sql
-- Create test documents
CREATE TABLE complaints_test (
    doc_id INTEGER,
    doc_name VARCHAR(10),
    text_data VARCHAR(1000)
);

INSERT INTO complaints_test VALUES
(1, 'A', 'ELECTRICAL CONTROL MODULE IS SHORTENING OUT, CAUSING THE VEHICLE TO STALL. ENGINE WILL BECOME TOTALLY INOPERATIVE. CONSUMER HAD TO CHANGE ALTERNATOR/ BATTERY AND STARTER, AND MODULE REPLACED 4 TIMES, BUT DEFECT STILL OCCURRING CANNOT DETERMINE WHAT IS CAUSING THE PROBLEM.');

INSERT INTO complaints_test VALUES
(2, 'B', 'ABS BRAKES FAIL TO OPERATE PROPERLY, AND AIR BAGS FAILED TO DEPLOY DURING A CRASH AT APPROX. 28 MPH IMPACT. MANUFACTURER NOTIFIED.');

INSERT INTO complaints_test VALUES
(3, 'C', 'WHILE DRIVING AT 60 MPH GAS PEDAL GOT STUCK DUE TO THE RUBBER THAT IS AROUND THE GAS PEDAL.');

INSERT INTO complaints_test VALUES
(4, 'D', 'THERE IS A KNOCKING NOISE COMING FROM THE CATALYTIC CONVERTER, AND THE VEHICLE IS STALLING. ALSO, HAS PROBLEM WITH THE STEERING.');

INSERT INTO complaints_test VALUES
(5, 'E', 'CONSUMER WAS MAKING A TURN, DRIVING AT APPROX 5-10 MPH WHEN CONSUMER HIT ANOTHER VEHICLE. UPON IMPACT, DUAL AIRBAGS DID NOT DEPLOY. ALL DAMAGE WAS DONE FROM ENGINE TO TRANSMISSION, TO THE FRONT OF VEHICLE, AND THE VEHICLE CONSIDERED A TOTAL LOSS.');

-- Tokenize test documents
CREATE MULTISET TABLE complaints_test_tokenized AS (
    SELECT
        doc_id,
        doc_name,
        LOWER(CAST(token AS VARCHAR(20))) AS token
    FROM TD_TextParser (
        ON complaints_test AS InputTable
        USING
        TextColumn ('text_data')
        OutputByWord ('true')
        Accumulate ('doc_id', 'doc_name')
    ) AS dt
) WITH DATA;
```

### Example 1: TopK Specified with Probabilities

Get top 2 predictions with probabilities:

```sql
SELECT * FROM TD_NaiveBayesTextClassifierPredict (
    ON complaints_test_tokenized AS PredictorValues PARTITION BY doc_id
    ON complaints_tokens_model AS Model DIMENSION
    USING
    ModelType ('Bernoulli')
    InputTokenColumn ('token')
    DocIDColumns ('doc_id')
    OutputProb ('true')
    Accumulate ('doc_name')
    TopK ('2')
) AS dt
ORDER BY doc_id;
```

**Purpose**: Get top 2 most likely categories with confidence scores.

**Sample Output**:

| doc_id | prediction | loglik | prob | doc_name |
|--------|-----------|----------------------|----------------------|----------|
| 1 | crash | -1.38044220625651E+002 | 1.41243173571687E-009 | A |
| 1 | no_crash | -1.17666267644292E+002 | 9.99999998587568E-001 | A |
| 2 | crash | -1.04652470718918E+002 | 1.70704288519507E-003 | B |
| 2 | no_crash | -9.82811865081127E+001 | 9.98292957114805E-001 | B |
| 3 | crash | -1.03026451289745E+002 | 2.26862573862878E-012 | C |
| 3 | no_crash | -7.62146044204976E+001 | 9.99999999997731E-001 | C |
| 4 | crash | -1.10830711173169E+002 | 1.42026355157382E-011 | D |
| 4 | no_crash | -8.58531176043404E+001 | 9.99999999985797E-001 | D |
| 5 | no_crash | -1.23936921216052E+002 | 3.43620138383542E-002 | E |
| 5 | crash | -1.20601083912966E+002 | 9.65637986161646E-001 | E |

**Interpretation**:
- Doc 1-4: Predicted as 'no_crash' with high confidence (>99.8%)
- Doc 5: Predicted as 'crash' with 96.6% confidence
- Both categories shown for each document with their probabilities

### Example 2: Responses Specified

Get predictions for specific categories only:

```sql
SELECT * FROM TD_NaiveBayesTextClassifierPredict (
    ON complaints_test_tokenized AS PredictorValues PARTITION BY doc_id
    ON complaints_tokens_model AS Model DIMENSION
    USING
    ModelType ('Bernoulli')
    InputTokenColumn ('token')
    DocIDColumns ('doc_id')
    OutputProb ('true')
    Accumulate ('doc_name')
    Responses ('crash', 'no crash')
) AS dt
ORDER BY doc_id;
```

**Purpose**: Get probabilities for specific categories of interest.

**Sample Output**:

| doc_id | prediction | loglik_crash | loglik_no_crash | prob_crash | prob_no_crash | doc_name |
|--------|-----------|--------------|-----------------|------------|---------------|----------|
| 1 | no_crash | -138.044 | -117.666 | 1.41E-09 | 0.999999999 | A |
| 2 | no_crash | -104.652 | -98.281 | 1.71E-03 | 0.998293 | B |
| 3 | no_crash | -103.026 | -76.215 | 2.27E-12 | 1.000000000 | C |
| 4 | no_crash | -110.831 | -85.853 | 1.42E-11 | 1.000000000 | D |
| 5 | crash | -120.601 | -123.937 | 0.965638 | 0.034362 | E |

**Interpretation**:
- Each document gets one prediction (highest probability class)
- Both specified response probabilities shown
- Doc 5: crash probability (96.6%) > no_crash probability (3.4%)

### Example 3: Single Most Likely Prediction

Get only the most likely category (TopK=1):

```sql
SELECT * FROM TD_NaiveBayesTextClassifierPredict (
    ON complaints_test_tokenized AS PredictorValues PARTITION BY doc_id
    ON complaints_tokens_model AS Model DIMENSION
    USING
    ModelType ('Bernoulli')
    InputTokenColumn ('token')
    DocIDColumns ('doc_id')
    OutputProb ('true')
    Accumulate ('doc_name')
    TopK ('1')
) AS dt
ORDER BY doc_id;
```

**Purpose**: Get only the predicted class for each document.

**Sample Output**:

| doc_id | prediction | loglik | prob | doc_name |
|--------|-----------|--------|------|----------|
| 1 | no_crash | -117.666 | 0.999999999 | A |
| 2 | no_crash | -98.281 | 0.998293 | B |
| 3 | no_crash | -76.215 | 1.000000000 | C |
| 4 | no_crash | -85.853 | 1.000000000 | D |
| 5 | crash | -120.601 | 0.965638 | E |

### Example 4: Multinomial Model Prediction

Use with Multinomial model:

```sql
SELECT * FROM TD_NaiveBayesTextClassifierPredict (
    ON test_data_tokenized AS PredictorValues PARTITION BY doc_id
    ON multinomial_model AS Model DIMENSION
    USING
    ModelType ('Multinomial')
    InputTokenColumn ('token')
    DocIDColumns ('doc_id')
    OutputProb ('true')
    TopK ('3')
) AS dt
ORDER BY doc_id, prob DESC;
```

**Purpose**: Classify with Multinomial model (frequency-based).

## Common Use Cases

### 1. Production Classification Pipeline

Apply classifier to new documents:

```sql
-- Tokenize incoming documents
CREATE VOLATILE TABLE new_docs_tokenized AS (
    SELECT
        doc_id,
        LOWER(token) as token
    FROM TD_TextParser (
        ON incoming_documents AS InputTable
        USING
        TextColumn ('content')
        ConvertToLowerCase ('true')
        Accumulate ('doc_id', 'source', 'timestamp')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Classify documents
CREATE TABLE classification_results AS (
    SELECT
        doc_id,
        prediction as category,
        prob as confidence,
        source,
        timestamp
    FROM TD_NaiveBayesTextClassifierPredict (
        ON new_docs_tokenized AS PredictorValues PARTITION BY doc_id
        ON production_model AS Model DIMENSION
        USING
        InputTokenColumn ('token')
        DocIDColumns ('doc_id')
        OutputProb ('true')
        Accumulate ('source', 'timestamp')
        TopK ('1')
    ) AS dt
) WITH DATA;
```

### 2. Model Evaluation on Test Set

Evaluate model performance:

```sql
-- Get predictions on test set
CREATE TABLE test_predictions AS (
    SELECT
        t.doc_id,
        t.true_category,
        p.prediction,
        p.prob as confidence
    FROM TD_NaiveBayesTextClassifierPredict (
        ON test_tokens AS PredictorValues PARTITION BY doc_id
        ON trained_model AS Model DIMENSION
        USING
        InputTokenColumn ('token')
        DocIDColumns ('doc_id')
        OutputProb ('true')
        TopK ('1')
    ) AS p
    INNER JOIN test_docs t ON p.doc_id = t.doc_id
) WITH DATA;

-- Calculate accuracy
SELECT
    COUNT(*) as total,
    SUM(CASE WHEN true_category = prediction THEN 1 ELSE 0 END) as correct,
    SUM(CASE WHEN true_category = prediction THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as accuracy_pct
FROM test_predictions;

-- Confusion matrix
SELECT
    true_category,
    prediction,
    COUNT(*) as count
FROM test_predictions
GROUP BY true_category, prediction
ORDER BY true_category, prediction;
```

### 3. Confidence-Based Routing

Route documents based on confidence:

```sql
-- Classify and route by confidence
SELECT
    doc_id,
    content,
    prediction,
    prob as confidence,
    CASE
        WHEN prob >= 0.9 THEN 'auto_route'
        WHEN prob >= 0.7 THEN 'review_queue'
        ELSE 'manual_review'
    END as routing_decision
FROM TD_NaiveBayesTextClassifierPredict (
    ON document_tokens AS PredictorValues PARTITION BY doc_id
    ON classifier_model AS Model DIMENSION
    USING
    InputTokenColumn ('token')
    DocIDColumns ('doc_id')
    OutputProb ('true')
    Accumulate ('content')
    TopK ('1')
) AS dt;
```

### 4. Multi-Label Classification

Get multiple category predictions:

```sql
-- Get top 3 categories per document
SELECT
    doc_id,
    title,
    prediction as category,
    prob as confidence,
    ROW_NUMBER() OVER (PARTITION BY doc_id ORDER BY prob DESC) as rank
FROM TD_NaiveBayesTextClassifierPredict (
    ON article_tokens AS PredictorValues PARTITION BY doc_id
    ON topic_model AS Model DIMENSION
    USING
    InputTokenColumn ('token')
    DocIDColumns ('doc_id')
    OutputProb ('true')
    Accumulate ('title')
    TopK ('3')
) AS dt
WHERE prob > 0.1  -- Minimum confidence threshold
ORDER BY doc_id, rank;
```

## Best Practices

### 1. Match Model Type

```sql
-- MUST match training model type!
-- If trained with Multinomial:
ModelType ('Multinomial')

-- If trained with Bernoulli:
ModelType ('Bernoulli')

-- Mismatch will produce incorrect results
```

### 2. Preprocess Consistently

```sql
-- Test data preprocessing MUST match training preprocessing
-- If training used:
-- - ConvertToLowerCase('true')
-- - RemoveStopWords('true')
-- - StemTokens('true')

-- Then test data must use same preprocessing:
TD_TextParser (
    ...
    ConvertToLowerCase('true')
    RemoveStopWords('true')
    StemTokens('true')
    ...
)
```

### 3. Use TopK for Efficiency

```sql
-- For single prediction:
TopK ('1')  -- Most efficient

-- For top categories:
TopK ('3')  -- Get top 3

-- For specific categories only:
Responses ('category1', 'category2')  -- Targeted
```

### 4. Include Probabilities for Decisions

```sql
-- Always use OutputProb('true') for:
-- - Confidence thresholds
-- - Human review routing
-- - Model evaluation
-- - Debugging predictions

OutputProb ('true')
```

### 5. Handle Low Confidence Predictions

```sql
-- Filter or flag low confidence predictions
SELECT *,
    CASE
        WHEN prob < 0.5 THEN 'LOW_CONFIDENCE'
        WHEN prob < 0.7 THEN 'MEDIUM_CONFIDENCE'
        ELSE 'HIGH_CONFIDENCE'
    END as confidence_level
FROM predictions
WHERE prob >= 0.3;  -- Minimum threshold
```

### 6. Partition Correctly

```sql
-- ALWAYS partition by document ID:
PARTITION BY doc_id

-- For multiple ID columns:
PARTITION BY doc_id, doc_source

-- Must match DocIDColumns specification
```

## Related Functions

- **TD_NaiveBayesTextClassifierTrainer**: Train the model used by this function
- **TD_TextParser**: Tokenize documents for prediction
- **TD_TextMorph**: Lemmatize tokens before prediction
- **TD_ClassificationEvaluator**: Evaluate prediction quality

## Notes and Limitations

### 1. Input Format Requirements
- Input must be document-token pairs
- One row per token occurrence
- Must be partitioned by document ID
- Typically created by TD_TextParser

### 2. Model Type Must Match
- ModelType parameter must match training model type
- Multinomial expects frequency-based features
- Bernoulli expects presence/absence features
- Mismatch produces incorrect probabilities

### 3. Preprocessing Consistency
**Critical**: Test data preprocessing must exactly match training:
- Same lowercasing settings
- Same stop word removal
- Same stemming/lemmatization
- Same punctuation handling

Inconsistency will degrade performance.

### 4. TopK vs Responses
- **Cannot use both** TopK and Responses simultaneously
- Choose based on need:
  - TopK: Top N predictions
  - Responses: Specific categories
  - Neither: All categories (equivalent to TopK)

### 5. Output Probabilities
- **LogLikelihood (loglik)**: Log of probability (negative values, closer to 0 is better)
- **Probability (prob)**: Actual probability (0-1 range, higher is better)
- Use OutputProb('true') to get both
- Probabilities sum to 1 across all categories for a document

### 6. Unseen Tokens
- Tokens not in training model are handled with smoothing
- Missing token probability from model prevents zero probabilities
- Very different vocabulary from training may reduce accuracy

### 7. Performance Considerations
- PARTITION BY groups tokens by document
- Model loaded as DIMENSION (in memory)
- Large models may impact memory usage
- TopK('1') is most efficient for single predictions

### 8. Model Column Specifications
- ModelTokenColumn, ModelCategoryColumn, ModelProbColumn must all be specified together or none
- Default assumptions work for standard trainer output
- Only specify if model has non-standard column names/order

### 9. Accumulate Limitations
- Accumulate columns copied from PredictorValues table
- Not applicable with token-level operations
- Use to preserve metadata (IDs, timestamps, etc.)

### 10. Probability Calculation
- **With TopK, no Responses**: prob = max(softmax(loglik))
- **With Responses**: prob_response = softmax(loglik_response)
- Softmax ensures probabilities sum to 1
- Uses log-likelihood for numerical stability

## Version Information

- **Function Version**: Based on Teradata Database Analytic Functions Version 17.20
- **Generated**: November 28, 2025
- **Algorithm**: Naive Bayes classification (prediction phase)
- **Companion Function**: TD_NaiveBayesTextClassifierTrainer
