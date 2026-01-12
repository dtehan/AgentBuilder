---
name: Text Analytics Workflow
allowed-tools:
description: Complete workflow for text analytics and NLP in Teradata
argument-hint: [database_name] [table_name] [text_column] [task_type]
---

# Text Analytics Workflow

## Overview
This workflow guides you through text analytics and Natural Language Processing (NLP) tasks in Teradata, including sentiment analysis, entity extraction, text classification, and text mining.

## Variables
DATABASE_NAME: $1
TABLE_NAME: $2
TEXT_COLUMN: $3
TASK_TYPE: $4 (sentiment|entity|classification|mining)

## Prerequisites
- Source table should have text data in ${TEXT_COLUMN}
- Text should be in supported language (primarily English)
- For classification: labeled training data required
- For sentiment/entity: no labels needed (pre-trained models)

## Text Analytics Use Cases

### Sentiment Analysis
- Customer review sentiment (positive/negative/neutral)
- Social media monitoring
- Brand perception analysis
- Product feedback analysis
- Customer satisfaction measurement
- Employee feedback analysis

### Named Entity Recognition (NER)
- Extract people names, organizations, locations
- Product mention extraction
- Date and time extraction
- Medical entity extraction
- Legal document analysis

### Text Classification
- Email categorization (spam detection)
- Support ticket routing
- Document classification
- Topic categorization
- Intent detection
- Priority assignment

### Text Mining and Analytics
- Keyword extraction
- Topic modeling
- Document similarity
- Text summarization
- Trend analysis
- Content recommendation

### Advanced NLP
- Text embeddings for similarity
- Document clustering
- Question answering
- Information extraction

## Workflow Stages

### Stage 0: Data Preparation and Exploration

**Verify text data exists:**
```sql
-- Check text data availability
SELECT COUNT(*) as total_rows,
       COUNT(${TEXT_COLUMN}) as non_null_text,
       COUNT(DISTINCT ${TEXT_COLUMN}) as unique_texts
FROM ${DATABASE_NAME}.${TABLE_NAME};

-- Sample text data
SELECT ${TEXT_COLUMN}
FROM ${DATABASE_NAME}.${TABLE_NAME}
SAMPLE 10;
```

**Analyze text characteristics:**
```sql
-- Text length distribution
SELECT
    AVG(CHARACTER_LENGTH(${TEXT_COLUMN})) as avg_length,
    MIN(CHARACTER_LENGTH(${TEXT_COLUMN})) as min_length,
    MAX(CHARACTER_LENGTH(${TEXT_COLUMN})) as max_length,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY CHARACTER_LENGTH(${TEXT_COLUMN})) as median_length
FROM ${DATABASE_NAME}.${TABLE_NAME}
WHERE ${TEXT_COLUMN} IS NOT NULL;

-- Text length categories
SELECT
    CASE
        WHEN CHARACTER_LENGTH(${TEXT_COLUMN}) < 50 THEN 'Very Short (<50)'
        WHEN CHARACTER_LENGTH(${TEXT_COLUMN}) < 200 THEN 'Short (50-200)'
        WHEN CHARACTER_LENGTH(${TEXT_COLUMN}) < 1000 THEN 'Medium (200-1000)'
        WHEN CHARACTER_LENGTH(${TEXT_COLUMN}) < 5000 THEN 'Long (1000-5000)'
        ELSE 'Very Long (>5000)'
    END as length_category,
    COUNT(*) as count,
    CAST(COUNT(*) AS FLOAT) / SUM(COUNT(*)) OVER () * 100 as percentage
FROM ${DATABASE_NAME}.${TABLE_NAME}
WHERE ${TEXT_COLUMN} IS NOT NULL
GROUP BY 1
ORDER BY 1;
```

### Stage 1: Text Preprocessing

**Parse and tokenize text:**
```sql
-- Parse text into tokens (words)
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_parsed AS
SELECT
    t.*,
    p.token,
    p.position as token_position
FROM ${DATABASE_NAME}.${TABLE_NAME} t,
     TD_TextParser(
         TextColumn('${TEXT_COLUMN}'),
         ToLowerCase(1),              -- Convert to lowercase
         RemovePunctuation(1),        -- Remove punctuation
         RemoveStopWords(1),          -- Remove common words (the, is, at, etc.)
         Language('en')               -- English language
     ) p
WITH DATA;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_textparser.md

**Generate n-grams (word combinations):**
```sql
-- Create bigrams and trigrams
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_ngrams AS
SELECT
    t.*,
    n.ngram,
    n.n as ngram_size
FROM ${DATABASE_NAME}.${TABLE_NAME} t,
     TD_NGramSplitter(
         TextColumn('${TEXT_COLUMN}'),
         NGramSize(2),                -- 2 for bigrams, 3 for trigrams
         ToLowerCase(1)
     ) n
WITH DATA;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_ngramsplitter.md

### Stage 2: Task-Specific Analysis

#### Task A: Sentiment Analysis

**Extract sentiment using pre-trained model:**
```sql
-- Sentiment extraction
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_sentiment AS
SELECT
    t.*,
    s.sentiment,                      -- positive, negative, neutral
    s.sentiment_score,                -- Confidence score (0-1)
    s.positive_score,
    s.negative_score,
    s.neutral_score
FROM ${DATABASE_NAME}.${TABLE_NAME} t,
     TD_SentimentExtractor(
         TextColumn('${TEXT_COLUMN}'),
         Language('en'),
         Model('vader')                -- VADER or other sentiment models
     ) s
WITH DATA;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_sentimentextractor.md

**Analyze sentiment distribution:**
```sql
-- Sentiment summary statistics
SELECT
    sentiment,
    COUNT(*) as count,
    CAST(COUNT(*) AS FLOAT) / SUM(COUNT(*)) OVER () * 100 as percentage,
    AVG(sentiment_score) as avg_confidence,
    MIN(sentiment_score) as min_confidence,
    MAX(sentiment_score) as max_confidence
FROM ${DATABASE_NAME}.${TABLE_NAME}_sentiment
GROUP BY sentiment
ORDER BY count DESC;
```

**Identify high-confidence sentiments:**
```sql
-- Strong positive and negative sentiments
SELECT
    sentiment,
    ${TEXT_COLUMN},
    sentiment_score,
    positive_score,
    negative_score
FROM ${DATABASE_NAME}.${TABLE_NAME}_sentiment
WHERE sentiment_score > 0.8  -- High confidence
ORDER BY sentiment_score DESC;
```

**Time-series sentiment analysis:**
```sql
-- Sentiment trends over time (if date column exists)
SELECT
    DATE_TRUNC('day', date_column) as date,
    sentiment,
    COUNT(*) as count,
    AVG(sentiment_score) as avg_sentiment_score
FROM ${DATABASE_NAME}.${TABLE_NAME}_sentiment
GROUP BY 1, 2
ORDER BY 1, 2;
```

#### Task B: Named Entity Recognition (NER)

**Extract entities from text:**
```sql
-- Named Entity Recognition
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_entities AS
SELECT
    t.*,
    e.entity,                         -- Extracted entity text
    e.entity_type,                    -- PERSON, ORGANIZATION, LOCATION, DATE, etc.
    e.start_position,
    e.end_position,
    e.confidence_score
FROM ${DATABASE_NAME}.${TABLE_NAME} t,
     TD_NERExtractor(
         TextColumn('${TEXT_COLUMN}'),
         EntityTypes('PERSON', 'ORGANIZATION', 'LOCATION', 'DATE'),
         Language('en')
     ) e
WITH DATA;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_nerextractor.md

**Entity frequency analysis:**
```sql
-- Most common entities by type
SELECT
    entity_type,
    entity,
    COUNT(*) as frequency,
    AVG(confidence_score) as avg_confidence
FROM ${DATABASE_NAME}.${TABLE_NAME}_entities
GROUP BY entity_type, entity
ORDER BY entity_type, frequency DESC;
```

**Co-occurrence analysis:**
```sql
-- Find entities that appear together
WITH doc_entities AS (
    SELECT
        row_id,
        entity_type,
        entity
    FROM ${DATABASE_NAME}.${TABLE_NAME}_entities
)
SELECT
    e1.entity as entity_1,
    e2.entity as entity_2,
    COUNT(*) as co_occurrence_count
FROM doc_entities e1
JOIN doc_entities e2 ON e1.row_id = e2.row_id AND e1.entity < e2.entity
WHERE e1.entity_type = 'ORGANIZATION'
  AND e2.entity_type = 'LOCATION'
GROUP BY e1.entity, e2.entity
HAVING COUNT(*) > 5
ORDER BY co_occurrence_count DESC;
```

**Entity-based document classification:**
```sql
-- Classify documents by dominant entity types
SELECT
    row_id,
    entity_type,
    COUNT(*) as entity_count,
    RANK() OVER (PARTITION BY row_id ORDER BY COUNT(*) DESC) as type_rank
FROM ${DATABASE_NAME}.${TABLE_NAME}_entities
GROUP BY row_id, entity_type
QUALIFY type_rank = 1;
```

#### Task C: Text Classification

**Prepare data for classification:**
```sql
-- Create train/test split for text classification
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_text_split AS
SELECT
    *,
    CASE WHEN RANDOM(1,100) <= 80 THEN 'TRAIN' ELSE 'TEST' END as dataset_split
FROM ${DATABASE_NAME}.${TABLE_NAME}
WHERE label_column IS NOT NULL
WITH DATA;
```

**Calculate TF-IDF features:**
```sql
-- TF-IDF feature extraction
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_tfidf AS
SELECT
    t.*,
    tf.term,
    tf.tf_idf_score,
    tf.term_frequency,
    tf.document_frequency
FROM ${DATABASE_NAME}.${TABLE_NAME}_text_split t,
     TD_TFIDF(
         TextColumn('${TEXT_COLUMN}'),
         DocIDColumn('row_id'),
         MaxFeatures(1000),            -- Top 1000 terms
         MinDF(2),                     -- Minimum document frequency
         MaxDF(0.8)                    -- Maximum document frequency (80%)
     ) tf
WHERE t.dataset_split = 'TRAIN'
WITH DATA;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_tfidf.md

**Train Naive Bayes text classifier:**
```sql
-- Train Naive Bayes for text classification
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_nb_text_model AS
SELECT TD_NaiveBayesTextClassifierTrainer(
    TextColumn('${TEXT_COLUMN}'),
    ClassColumn('label_column'),
    ModelType('multinomial'),
    TopK(1000),                       -- Use top 1000 features
    MinDocFreq(2),
    MaxDocFreq(0.9)
)
FROM ${DATABASE_NAME}.${TABLE_NAME}_text_split
WHERE dataset_split = 'TRAIN'
WITH DATA;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_naivebayestextclassifiertrainer.md

**Predict text categories:**
```sql
-- Classify test documents
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_text_predictions AS
SELECT
    t.*,
    p.prediction as predicted_category,
    p.confidence_score
FROM ${DATABASE_NAME}.${TABLE_NAME}_text_split t,
     TD_NaiveBayesTextClassifierPredict(
         ModelTable(${DATABASE_NAME}.${TABLE_NAME}_nb_text_model),
         TextColumn('${TEXT_COLUMN}'),
         TopK(10)                      -- Return top 10 predictions
     ) p
WHERE t.dataset_split = 'TEST'
WITH DATA;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_naivebayestextclassifierpredict.md

**Evaluate classification performance:**
```sql
-- Calculate classification metrics
SELECT
    label_column as actual_category,
    predicted_category,
    COUNT(*) as count,
    AVG(confidence_score) as avg_confidence
FROM ${DATABASE_NAME}.${TABLE_NAME}_text_predictions
GROUP BY label_column, predicted_category
ORDER BY label_column, count DESC;

-- Overall accuracy
SELECT
    COUNT(*) as total,
    SUM(CASE WHEN label_column = predicted_category THEN 1 ELSE 0 END) as correct,
    CAST(SUM(CASE WHEN label_column = predicted_category THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) as accuracy
FROM ${DATABASE_NAME}.${TABLE_NAME}_text_predictions;
```

#### Task D: Text Mining and Feature Extraction

**Calculate word embeddings:**
```sql
-- Generate word embeddings (word2vec-style)
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_embeddings AS
SELECT
    w.word,
    w.vector,
    w.vector_dimension
FROM TD_WordEmbeddings(
    InputTable(${DATABASE_NAME}.${TABLE_NAME}_parsed),
    TextColumn('token'),
    VectorSize(100),                  -- 100-dimensional embeddings
    WindowSize(5),                    -- Context window
    MinCount(5),                      -- Minimum word frequency
    Algorithm('skipgram')             -- skipgram or cbow
)
FROM ${DATABASE_NAME}.${TABLE_NAME}_parsed
WITH DATA;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_wordembeddings.md

**Calculate document similarity using TF-IDF:**
```sql
-- Document similarity matrix
WITH doc_vectors AS (
    SELECT
        row_id,
        term,
        tf_idf_score
    FROM ${DATABASE_NAME}.${TABLE_NAME}_tfidf
)
SELECT
    d1.row_id as doc1,
    d2.row_id as doc2,
    SUM(d1.tf_idf_score * d2.tf_idf_score) /
        (SQRT(SUM(POWER(d1.tf_idf_score, 2))) * SQRT(SUM(POWER(d2.tf_idf_score, 2)))) as cosine_similarity
FROM doc_vectors d1
JOIN doc_vectors d2 ON d1.term = d2.term AND d1.row_id < d2.row_id
GROUP BY d1.row_id, d2.row_id
HAVING cosine_similarity > 0.5        -- Only keep similar documents
ORDER BY cosine_similarity DESC
LIMIT 100;
```

**Extract key terms per document:**
```sql
-- Top keywords per document
SELECT
    row_id,
    term,
    tf_idf_score,
    RANK() OVER (PARTITION BY row_id ORDER BY tf_idf_score DESC) as term_rank
FROM ${DATABASE_NAME}.${TABLE_NAME}_tfidf
QUALIFY term_rank <= 10               -- Top 10 terms per document
ORDER BY row_id, term_rank;
```

**Topic modeling with clustering:**
```sql
-- Cluster documents by content similarity
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_topics AS
SELECT
    t.row_id,
    t.${TEXT_COLUMN},
    c.cluster_id as topic_id
FROM ${DATABASE_NAME}.${TABLE_NAME} t,
     TD_KMeans(
         K(10),                        -- 10 topics
         MaxIterations(100)
     ) c,
     ${DATABASE_NAME}.${TABLE_NAME}_tfidf tf
WHERE t.row_id = tf.row_id
WITH DATA;

-- Characterize each topic by top terms
SELECT
    topic_id,
    term,
    AVG(tf_idf_score) as avg_tfidf,
    COUNT(*) as doc_count,
    RANK() OVER (PARTITION BY topic_id ORDER BY AVG(tf_idf_score) DESC) as term_rank
FROM ${DATABASE_NAME}.${TABLE_NAME}_topics tp
JOIN ${DATABASE_NAME}.${TABLE_NAME}_tfidf tf ON tp.row_id = tf.row_id
GROUP BY topic_id, term
QUALIFY term_rank <= 20
ORDER BY topic_id, term_rank;
```

### Stage 3: Advanced Text Analytics

#### Word Frequency Analysis

```sql
-- Most common words/tokens
SELECT
    token,
    COUNT(*) as frequency,
    COUNT(DISTINCT row_id) as document_frequency,
    CAST(COUNT(DISTINCT row_id) AS FLOAT) / (SELECT COUNT(DISTINCT row_id) FROM ${DATABASE_NAME}.${TABLE_NAME}_parsed) as doc_frequency_pct
FROM ${DATABASE_NAME}.${TABLE_NAME}_parsed
GROUP BY token
ORDER BY frequency DESC
LIMIT 50;
```

#### N-gram Analysis

```sql
-- Most common bigrams and trigrams
SELECT
    ngram,
    ngram_size,
    COUNT(*) as frequency,
    COUNT(DISTINCT row_id) as document_frequency
FROM ${DATABASE_NAME}.${TABLE_NAME}_ngrams
GROUP BY ngram, ngram_size
ORDER BY frequency DESC
LIMIT 100;
```

#### Sentiment by Category

```sql
-- Average sentiment by product/category (if categorical column exists)
SELECT
    category_column,
    AVG(CASE WHEN sentiment = 'positive' THEN sentiment_score
             WHEN sentiment = 'negative' THEN -sentiment_score
             ELSE 0 END) as sentiment_score,
    COUNT(*) as review_count,
    SUM(CASE WHEN sentiment = 'positive' THEN 1 ELSE 0 END) as positive_count,
    SUM(CASE WHEN sentiment = 'negative' THEN 1 ELSE 0 END) as negative_count,
    SUM(CASE WHEN sentiment = 'neutral' THEN 1 ELSE 0 END) as neutral_count
FROM ${DATABASE_NAME}.${TABLE_NAME}_sentiment
GROUP BY category_column
ORDER BY sentiment_score DESC;
```

#### Entity Sentiment Correlation

```sql
-- Sentiment associated with specific entities
SELECT
    e.entity,
    e.entity_type,
    AVG(s.sentiment_score) as avg_sentiment,
    COUNT(*) as mention_count,
    SUM(CASE WHEN s.sentiment = 'positive' THEN 1 ELSE 0 END) as positive_mentions,
    SUM(CASE WHEN s.sentiment = 'negative' THEN 1 ELSE 0 END) as negative_mentions
FROM ${DATABASE_NAME}.${TABLE_NAME}_entities e
JOIN ${DATABASE_NAME}.${TABLE_NAME}_sentiment s ON e.row_id = s.row_id
WHERE e.entity_type = 'ORGANIZATION'
GROUP BY e.entity, e.entity_type
HAVING COUNT(*) >= 10
ORDER BY mention_count DESC;
```

### Stage 4: Model Evaluation and Interpretation

#### Sentiment Model Evaluation

```sql
-- If ground truth labels exist
WITH evaluation AS (
    SELECT
        CASE WHEN true_sentiment = sentiment THEN 1 ELSE 0 END as correct,
        sentiment,
        sentiment_score
    FROM ${DATABASE_NAME}.${TABLE_NAME}_sentiment
    WHERE true_sentiment IS NOT NULL
)
SELECT
    sentiment,
    COUNT(*) as predictions,
    SUM(correct) as correct_predictions,
    CAST(SUM(correct) AS FLOAT) / COUNT(*) as accuracy,
    AVG(sentiment_score) as avg_confidence
FROM evaluation
GROUP BY sentiment
ORDER BY sentiment;
```

#### Text Classification Confusion Matrix

```sql
-- Detailed confusion matrix for text classification
SELECT
    label_column as actual,
    predicted_category as predicted,
    COUNT(*) as count,
    AVG(confidence_score) as avg_confidence
FROM ${DATABASE_NAME}.${TABLE_NAME}_text_predictions
GROUP BY label_column, predicted_category
ORDER BY actual, count DESC;
```

#### Feature Importance for Classification

```sql
-- Most discriminative terms per class
SELECT
    class_label,
    term,
    term_importance,
    RANK() OVER (PARTITION BY class_label ORDER BY term_importance DESC) as importance_rank
FROM ${DATABASE_NAME}.${TABLE_NAME}_nb_text_model
QUALIFY importance_rank <= 20
ORDER BY class_label, importance_rank;
```

### Stage 5: Production Deployment

#### Create Sentiment Analysis View

```sql
-- Production sentiment analysis view
CREATE VIEW ${DATABASE_NAME}.${TABLE_NAME}_live_sentiment AS
SELECT
    t.*,
    s.sentiment,
    s.sentiment_score,
    s.positive_score,
    s.negative_score,
    CURRENT_TIMESTAMP as analysis_timestamp
FROM ${DATABASE_NAME}.${TABLE_NAME} t,
     TD_SentimentExtractor(
         TextColumn('${TEXT_COLUMN}'),
         Language('en')
     ) s;
```

#### Create Entity Extraction View

```sql
-- Production entity extraction view
CREATE VIEW ${DATABASE_NAME}.${TABLE_NAME}_live_entities AS
SELECT
    t.*,
    e.entity,
    e.entity_type,
    e.confidence_score,
    CURRENT_TIMESTAMP as extraction_timestamp
FROM ${DATABASE_NAME}.${TABLE_NAME} t,
     TD_NERExtractor(
         TextColumn('${TEXT_COLUMN}'),
         EntityTypes('PERSON', 'ORGANIZATION', 'LOCATION')
     ) e;
```

#### Batch Text Classification

```sql
-- Classify new documents
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_new_classifications AS
SELECT
    new_data.*,
    p.prediction as predicted_category,
    p.confidence_score,
    CURRENT_DATE as classification_date
FROM ${DATABASE_NAME}.${TABLE_NAME}_new_data new_data,
     TD_NaiveBayesTextClassifierPredict(
         ModelTable(${DATABASE_NAME}.${TABLE_NAME}_nb_text_model),
         TextColumn('${TEXT_COLUMN}')
     ) p
WITH DATA;
```

#### Monitor Text Analytics Performance

```sql
-- Track sentiment distribution over time
SELECT
    DATE_TRUNC('day', analysis_timestamp) as date,
    sentiment,
    COUNT(*) as count,
    AVG(sentiment_score) as avg_confidence
FROM ${DATABASE_NAME}.${TABLE_NAME}_live_sentiment
GROUP BY 1, 2
ORDER BY 1, 2;
```

#### Alert on Sentiment Shifts

```sql
-- Detect significant sentiment changes
WITH recent_sentiment AS (
    SELECT AVG(CASE WHEN sentiment = 'positive' THEN 1
                    WHEN sentiment = 'negative' THEN -1
                    ELSE 0 END) as recent_score
    FROM ${DATABASE_NAME}.${TABLE_NAME}_live_sentiment
    WHERE analysis_timestamp >= CURRENT_TIMESTAMP - INTERVAL '7' DAY
),
baseline_sentiment AS (
    SELECT AVG(CASE WHEN sentiment = 'positive' THEN 1
                    WHEN sentiment = 'negative' THEN -1
                    ELSE 0 END) as baseline_score
    FROM ${DATABASE_NAME}.${TABLE_NAME}_sentiment
)
SELECT
    recent_score,
    baseline_score,
    recent_score - baseline_score as sentiment_change,
    CASE WHEN ABS(recent_score - baseline_score) > 0.2
         THEN 'ALERT: Significant Sentiment Shift'
         ELSE 'Normal' END as status
FROM recent_sentiment, baseline_sentiment;
```

## Decision Guides

### Choosing Text Analytics Task

**Use Sentiment Analysis when:**
- Analyzing customer reviews or feedback
- Monitoring brand perception
- Measuring customer satisfaction
- Analyzing social media posts
- Evaluating product reception

**Use Named Entity Recognition when:**
- Extracting structured information from text
- Building knowledge graphs
- Identifying key actors and locations
- Processing legal or medical documents
- Content tagging and indexing

**Use Text Classification when:**
- Routing support tickets
- Spam detection
- Document categorization
- Intent detection
- Priority assignment

**Use Text Mining when:**
- Discovering topics in documents
- Finding similar documents
- Extracting keywords
- Trend analysis
- Content recommendation

### Preprocessing Decisions

**Remove stop words when:**
- Doing topic modeling or clustering
- Building classification models
- Extracting keywords

**Keep stop words when:**
- Analyzing sentiment (negations are important)
- Extracting phrases or n-grams
- Preserving linguistic structure

**Use n-grams when:**
- Capturing phrases (e.g., "not good")
- Improving classification accuracy
- Identifying common expressions

### Model Selection for Text Classification

**Use Naive Bayes when:**
- Have limited training data
- Need fast training and scoring
- Text has clear categorical signals
- Need interpretable features

**Use XGBoost/RF (with TF-IDF features) when:**
- Have sufficient training data
- Need highest accuracy
- Can tolerate longer training
- Features are well-engineered

## Output Artifacts

This workflow produces:
1. `${TABLE_NAME}_parsed` - Tokenized text data
2. `${TABLE_NAME}_sentiment` - Sentiment analysis results
3. `${TABLE_NAME}_entities` - Extracted named entities
4. `${TABLE_NAME}_text_predictions` - Text classification results
5. `${TABLE_NAME}_tfidf` - TF-IDF features
6. `${TABLE_NAME}_embeddings` - Word embeddings
7. `${TABLE_NAME}_topics` - Topic assignments
8. Production views for live analytics

## Best Practices

1. **Clean text data** - Remove noise, HTML tags, special characters
2. **Handle language properly** - Specify correct language parameter
3. **Use appropriate preprocessing** - Consider task requirements
4. **Monitor confidence scores** - Low confidence indicates uncertainty
5. **Validate on sample** - Review results on sample before full deployment
6. **Consider context** - Negations can flip sentiment
7. **Handle short text carefully** - May have insufficient context
8. **Use n-grams for phrases** - Capture multi-word expressions
9. **Balance training data** - Ensure all classes represented
10. **Regular retraining** - Language evolves over time

## Common Issues and Solutions

### Issue: Poor Sentiment Accuracy
**Cause:** Sarcasm, domain-specific language, or context
**Solutions:**
- Train custom sentiment model with domain data
- Review confidence scores
- Consider context (n-grams)
- Handle negations explicitly
- Use ensemble of models

### Issue: Too Many/Few Entities Extracted
**Cause:** Threshold too low/high or wrong entity types
**Solutions:**
- Adjust confidence threshold
- Specify relevant entity types
- Filter by entity length
- Use domain-specific NER models
- Post-process results

### Issue: Text Classification Low Accuracy
**Cause:** Insufficient training data or poor features
**Solutions:**
- Collect more labeled data
- Use TF-IDF features
- Try n-grams (bigrams, trigrams)
- Balance training classes
- Feature selection (remove rare/common terms)
- Try ensemble methods

### Issue: Missing Important Terms
**Cause:** Stop word removal too aggressive
**Solutions:**
- Customize stop word list
- Keep domain-specific terms
- Use lower case but keep structure
- Review tokenization results

### Issue: Slow Text Processing
**Cause:** Large documents or complex operations
**Solutions:**
- Batch processing instead of row-by-row
- Limit text length (truncate long docs)
- Reduce feature count (MaxFeatures)
- Parallel processing
- Sample for exploratory analysis

### Issue: Inconsistent Results Across Batches
**Cause:** Model versioning or data drift
**Solutions:**
- Version control models
- Monitor input data distribution
- Regular retraining schedule
- Track performance metrics
- Document preprocessing steps

## Function Reference Summary

### Text Preprocessing
- FunctionalPrompts/Advanced_Analytics/td_textparser.md
- FunctionalPrompts/Advanced_Analytics/td_ngramsplitter.md

### Sentiment Analysis
- FunctionalPrompts/Advanced_Analytics/td_sentimentextractor.md

### Entity Extraction
- FunctionalPrompts/Advanced_Analytics/td_nerextractor.md

### Text Classification
- FunctionalPrompts/Advanced_Analytics/td_naivebayestextclassifiertrainer.md
- FunctionalPrompts/Advanced_Analytics/td_naivebayestextclassifierpredict.md

### Feature Extraction
- FunctionalPrompts/Advanced_Analytics/td_tfidf.md
- FunctionalPrompts/Advanced_Analytics/td_wordembeddings.md

---

**File Created**: 2025-11-28
**Version**: 1.0
**Workflow Type**: Text Analytics
**Parent Persona**: persona_data_scientist.md
