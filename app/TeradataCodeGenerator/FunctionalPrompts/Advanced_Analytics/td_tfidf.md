# TD_TFIDF

## Function Name
- **TD_TFIDF**: Calculates Term Frequency-Inverse Document Frequency (TF-IDF) scores for document vectorization

## Description
Term Frequency-Inverse Document Frequency (TF-IDF) is a technique for evaluating the importance of a specific term in a specific document in a document set. Term frequency (tf) is the number of times that the term appears in the document and inverse document frequency (idf) is the number of times that the term appears in the document set. The TF-IDF score for a term is tf * idf. A term with a high TF-IDF score is relevant to the specific document.

You can use the TF-IDF scores as input for document clustering and classification algorithms, including:
- Cosine-similarity
- Latent Dirichlet allocation
- K-means clustering
- K-nearest neighbors

TD_TFIDF function represents each document as an N-dimensional vector, where N is the number of terms in the document set (therefore, the document vector is sparse). Each entry in the document vector is the TF-IDF score of a term.

### Characteristics
- Converts documents to numerical vectors
- Identifies important terms in documents
- Supports multiple normalization methods
- Configurable for TF, IDF, and overall regularization
- Creates sparse document representations
- Enables document similarity calculations

## When to Use TD_TFIDF

### Document Classification
- Prepare text features for classification models
- Identify discriminative terms for categories
- Create document similarity metrics

### Information Retrieval
- Rank documents by relevance to queries
- Build search engines with TF-IDF weighting
- Improve search result quality

### Document Clustering
- Group similar documents together
- Find document topics and themes
- Create document similarity matrices

### Feature Engineering
- Generate numerical features from text
- Reduce dimensionality while preserving information
- Create input for machine learning algorithms

### Content Recommendation
- Find similar documents for recommendations
- Measure document similarity
- Build content-based filtering systems

## Syntax

```sql
TD_TFIDF (
    ON { table | view | (query) } AS InputTable
    USING
    DocIdColumn ('docid_column')
    TokenColumn ('token_column')
    [ TFNormalization ({'BOOL'|'COUNT'|'NORMAL'|'LOG'|'AUGMENT'}) ]
    [ IDFNormalization ({'UNARY'|'LOG'|'LOGNORM'|'SMOOTH'}) ]
    [ Regularization ({'L2'|'L1'|'NONE'}) ]
    [ Accumulate ({ 'accumulate_column' | accumulate_column_range }[,...]) ]
)
```

**Note:** You can call this function from:
- The FROM clause of a SELECT statement
- As part of a CREATE TABLE statement
- As part of a CREATE VIEW statement

## Required Elements

### ON Clause
Specifies the table name, view name or query as an InputTable.

### DocIdColumn
**Required**: Specifies the column with the document identifier.
- **Data Type**: BYTEINT, SMALLINT, INTEGER, BIGINT
- **Purpose**: Uniquely identifies each document in the corpus

### TokenColumn
**Required**: Specifies the column with the document tokens.
- **Data Type**: CHAR, VARCHAR
- **Purpose**: Contains the individual words/terms from documents

## Optional Elements

### TFNormalization
Specifies the normalization method for calculating the term frequency (TF).
- **Default**: 'NORMAL'
- **Purpose**: Determines how to weight term frequency in documents

**Available Methods**:

| Method | Formula | Description |
|--------|---------|-------------|
| **BOOL** | tf(t,d) = 1 if t occurs in d; otherwise 0 | Boolean frequency: Term presence/absence only |
| **COUNT** | tf(t,d) = f(t,d) | Raw frequency: Simple count of term occurrences |
| **NORMAL** | tf(t,d) = f(t,d) / sum{w : w ∈ d} | Normalized frequency: Raw frequency divided by total terms in document |
| **LOG** | tf(t,d) = 1 + log(f(t,d)) | Logarithmically-scaled frequency: Natural logarithm of raw frequency |
| **AUGMENT** | tf(t,d) = 0.5 + (0.5 × f(t,d) / max{f(w,d) : w ∈ d}) | Augmented frequency: Prevents bias towards longer documents by dividing by max term frequency |

Where:
- t = term
- d = document
- f(t,d) = raw frequency (number of times t occurs in d)
- w = any term in document d

### IDFNormalization
Specifies the normalization method for calculating the inverse document frequency (IDF).
- **Default**: 'LOG'
- **Purpose**: Determines how to weight term rarity across corpus

**Available Methods**:

| Method | Formula | Description |
|--------|---------|-------------|
| **UNARY** | idf(t,D) = 1 | Used to disable IDF calculation (all terms weighted equally) |
| **LOG** | idf(t,D) = log(N/Nt) | Standard IDF: Logarithm of total documents divided by documents containing term |
| **LOGNORM** | idf(t,D) = 1 + log(N / Nt) | Log-normalized IDF: Adds 1 to standard IDF |
| **SMOOTH** | idf(t,D) = 1 + log((1 + N) / (1 + Nt)) | Smooth IDF: Prevents division by zero and smooths values |

Where:
- D = corpus (document set)
- N = total number of documents in corpus (N = |D|)
- Nt = number of documents where term t appears (Nt = |{d ∈ D : t ∈ d}|)

### Regularization
Specifies the regularization method for calculating the TF-IDF score.
- **Default**: 'NONE'
- **Purpose**: Normalizes final TF-IDF vectors for comparability

**Available Methods**:

| Method | Formula | Description |
|--------|---------|-------------|
| **L2** | tfidf(t,d) = (tf × idf) / sqrt(Σ(tf × idf)²) | Euclidean normalization: Normalizes vector to unit length |
| **L1** | tfidf(t,d) = (tf × idf) / Σ\|tf × idf\| | Manhattan normalization: Normalizes by sum of absolute values |
| **NONE** | tfidf(t,d) = tf(t,d) × idf(t,D) | No regularization: Simple product of TF and IDF |

Where:
- The sum is over all terms w in document d
- tf and idf are calculated according to their respective normalization methods

### Accumulate
Specifies the input columns to copy to the output table.
- **Purpose**: Preserve metadata columns in output
- **Format**: Column names or ranges

## Input Schema

### Input Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| doc_id_column | BYTEINT, SMALLINT, INTEGER, BIGINT | Column with the document identifier |
| token_column | CHAR, VARCHAR | Column with the document tokens |
| accumulate_column | Any | Column which needs to be copied to the output table |

**Input Format**: The input table should contain document-token pairs, typically created by tokenizing documents using TD_TextParser or similar function.

## Output Schema

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| doc_id_column | BYTEINT, SMALLINT, INTEGER, BIGINT | Document identifier of document d |
| token_column | CHAR, VARCHAR | Term t |
| TD_TF | FLOAT | Term frequency of term t in document d, calculated as specified by TFNormalization formula |
| TD_IDF | FLOAT | Inverse document frequency of term t in document corpus D, calculated as specified by IDFNormalization formula |
| TD_TF_IDF | FLOAT | TFIDF score of term t in document d in corpus D, calculated as specified by the Regularization formula |
| accumulate_column | Any | Accumulate column copied from input to output |

## Code Examples

### Example Setup: Create and Tokenize Input Data

Create the original input table:

```sql
CREATE TABLE tfidf_input (
    docid INTEGER,
    content VARCHAR(100),
    category VARCHAR(10)
);

INSERT INTO tfidf_input VALUES
(1, 'The quick brown fox jumps over the lazy fox.', 'Animals');

INSERT INTO tfidf_input VALUES
(2, 'Scientists conducted experiments in the lab to analyze the chemical reactions.', 'Science');

INSERT INTO tfidf_input VALUES
(3, 'Using advanced equipments in the lab, scientists observed unexpected reactions in the lab.', 'Science');
```

Tokenize the documents:

```sql
CREATE MULTISET TABLE tfidf_input_tokenized AS (
    SELECT
        docid,
        CAST(token AS VARCHAR(15)) AS token,
        category
    FROM TD_TextParser (
        ON tfidf_input AS InputTable
        USING
        TextColumn ('content')
        ConvertToLowerCase ('true')
        OutputByWord ('true')
        Punctuation ('\[.,?\!\]')
        RemoveStopWords ('true')
        StemTokens ('true')
        Accumulate ('docid', 'category')
    ) AS dt
) WITH DATA;
```

**Tokenized Input Table**:

| docid | token | category |
|-------|-------|----------|
| 1 | brown | Animals |
| 1 | fox | Animals |
| 1 | fox | Animals |
| 1 | jump | Animals |
| 1 | lazi | Animals |
| 1 | over | Animals |
| 1 | quick | Animals |
| 2 | analyz | Science |
| 2 | chemic | Science |
| 2 | conduct | Science |
| 2 | experi | Science |
| 2 | lab | Science |
| 2 | reaction | Science |
| 2 | scientist | Science |
| 3 | advanc | Science |
| 3 | equip | Science |
| 3 | lab | Science |
| 3 | observ | Science |
| 3 | reaction | Science |
| 3 | scientist | Science |
| 3 | unexpect | Science |
| 3 | use | Science |

### Example 1: Standard TF-IDF with LOG and L2 Normalization

Calculate TF-IDF with logarithmic scaling and L2 normalization:

```sql
SELECT * FROM TD_TFIDF (
    ON tfidf_input_tokenized AS InputTable
    USING
    DocIdColumn ('docid')
    TokenColumn ('token')
    TFNormalization ('LOG')
    IDFNormalization ('SMOOTH')
    Regularization ('L2')
    Accumulate ('category')
) AS dt
ORDER BY docid, token;
```

**Purpose**: Standard TF-IDF with unit-length document vectors for cosine similarity.

**Sample Output**:

| docid | token | TD_TF | TD_IDF | TD_TF_IDF | category |
|-------|-------|-------|--------|-----------|----------|
| 1 | brown | 1.000 | 1.693 | 0.357 | Animals |
| 1 | fox | 1.693 | 1.693 | 0.604 | Animals |
| 1 | jump | 1.000 | 1.693 | 0.357 | Animals |
| 1 | lazi | 1.000 | 1.693 | 0.357 | Animals |
| 1 | over | 1.000 | 1.693 | 0.357 | Animals |
| 1 | quick | 1.000 | 1.693 | 0.357 | Animals |
| 2 | analyz | 1.000 | 1.693 | 0.418 | Science |
| 2 | chemic | 1.000 | 1.693 | 0.418 | Science |
| 2 | conduct | 1.000 | 1.693 | 0.418 | Science |
| 2 | experi | 1.000 | 1.693 | 0.418 | Science |
| 2 | lab | 1.693 | 1.288 | 0.318 | Science |
| 2 | reaction | 1.000 | 1.288 | 0.318 | Science |
| 2 | scientist | 1.000 | 1.288 | 0.318 | Science |

**Key Observations**:
- "fox" has highest TF-IDF in doc 1 (appears twice, unique to Animals)
- "lab" has lower IDF (appears in multiple Science documents)
- L2 normalization makes vectors unit-length for similarity calculations

### Example 2: Boolean TF with UNARY IDF (Disable IDF)

Simple term presence/absence weighting:

```sql
SELECT * FROM TD_TFIDF (
    ON tfidf_input_tokenized AS InputTable
    USING
    DocIdColumn ('docid')
    TokenColumn ('token')
    TFNormalization ('BOOL')
    IDFNormalization ('UNARY')
    Regularization ('NONE')
    Accumulate ('category')
) AS dt
ORDER BY docid, token;
```

**Purpose**: Binary features indicating term presence (useful for short documents or binary classification).

**Sample Output**:

| docid | token | TD_TF | TD_IDF | TD_TF_IDF | category |
|-------|-------|-------|--------|-----------|----------|
| 1 | brown | 1.000 | 1.000 | 1.000 | Animals |
| 1 | fox | 1.000 | 1.000 | 1.000 | Animals |
| 1 | jump | 1.000 | 1.000 | 1.000 | Animals |
| 2 | analyz | 1.000 | 1.000 | 1.000 | Science |
| 2 | lab | 1.000 | 1.000 | 1.000 | Science |

**Note**: All present terms have score of 1.0, absent terms not included.

### Example 3: Raw Count with L1 Normalization

Use raw term counts normalized by L1:

```sql
SELECT * FROM TD_TFIDF (
    ON tfidf_input_tokenized AS InputTable
    USING
    DocIdColumn ('docid')
    TokenColumn ('token')
    TFNormalization ('COUNT')
    IDFNormalization ('LOG')
    Regularization ('L1')
    Accumulate ('category')
) AS dt
ORDER BY docid, token;
```

**Purpose**: Probability-like distribution over terms (sums to 1).

### Example 4: Augmented Frequency for Long Documents

Prevent bias towards longer documents:

```sql
SELECT * FROM TD_TFIDF (
    ON tfidf_input_tokenized AS InputTable
    USING
    DocIdColumn ('docid')
    TokenColumn ('token')
    TFNormalization ('AUGMENT')
    IDFNormalization ('LOGNORM')
    Regularization ('L2')
    Accumulate ('category')
) AS dt
ORDER BY docid, token;
```

**Purpose**: Handle varying document lengths fairly.

## Common Use Cases

### 1. Document Similarity Calculation

Calculate cosine similarity between documents:

```sql
-- Step 1: Calculate TF-IDF vectors
CREATE TABLE doc_vectors AS (
    SELECT
        docid,
        token,
        TD_TF_IDF as tfidf_score
    FROM TD_TFIDF (
        ON tokenized_docs AS InputTable
        USING
        DocIdColumn ('docid')
        TokenColumn ('token')
        TFNormalization ('LOG')
        IDFNormalization ('SMOOTH')
        Regularization ('L2')
    ) AS dt
) WITH DATA;

-- Step 2: Calculate cosine similarity
SELECT
    a.docid as doc1,
    b.docid as doc2,
    SUM(a.tfidf_score * b.tfidf_score) as cosine_similarity
FROM doc_vectors a
INNER JOIN doc_vectors b
    ON a.token = b.token
    AND a.docid < b.docid
GROUP BY a.docid, b.docid
ORDER BY cosine_similarity DESC;
```

### 2. Keyword Extraction

Find most important terms for each document:

```sql
-- Extract top 10 keywords per document
SELECT
    docid,
    category,
    token as keyword,
    TD_TF_IDF as importance_score,
    ROW_NUMBER() OVER (PARTITION BY docid ORDER BY TD_TF_IDF DESC) as rank
FROM TD_TFIDF (
    ON tokenized_docs AS InputTable
    USING
    DocIdColumn ('docid')
    TokenColumn ('token')
    TFNormalization ('LOG')
    IDFNormalization ('SMOOTH')
    Regularization ('NONE')
    Accumulate ('category')
) AS dt
QUALIFY rank <= 10
ORDER BY docid, rank;
```

### 3. Document Classification Features

Prepare features for classification model:

```sql
-- Create TF-IDF feature matrix for classification
CREATE TABLE classification_features AS (
    SELECT
        t.docid,
        t.category as label,
        CAST(t.token AS VARCHAR(50)) as feature_name,
        t.TD_TF_IDF as feature_value
    FROM TD_TFIDF (
        ON training_docs_tokenized AS InputTable
        USING
        DocIdColumn ('docid')
        TokenColumn ('token')
        TFNormalization ('LOG')
        IDFNormalization ('SMOOTH')
        Regularization ('L2')
        Accumulate ('category')
    ) AS t
    WHERE TD_TF_IDF > 0.01  -- Filter low-value features
) WITH DATA;

-- Pivot to wide format for ML algorithms
-- (use appropriate ML function for classification)
```

### 4. Information Retrieval Ranking

Rank documents by relevance to query:

```sql
-- Tokenize query
CREATE VOLATILE TABLE query_tokens AS (
    SELECT token
    FROM TD_TextParser (
        ON (SELECT 'machine learning algorithms' as query_text) AS InputTable
        USING
        TextColumn ('query_text')
        ConvertToLowerCase ('true')
        StemTokens ('true')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Score documents against query
SELECT
    d.docid,
    d.title,
    SUM(d.TD_TF_IDF) as relevance_score
FROM TD_TFIDF (
    ON doc_tokens AS InputTable
    USING
    DocIdColumn ('docid')
    TokenColumn ('token')
    TFNormalization ('LOG')
    IDFNormalization ('SMOOTH')
    Regularization ('L2')
    Accumulate ('title')
) AS d
INNER JOIN query_tokens q
    ON d.token = q.token
GROUP BY d.docid, d.title
ORDER BY relevance_score DESC
LIMIT 20;
```

## Best Practices

### 1. Choose Appropriate TF Normalization

**BOOL**: Use when:
- Document length varies significantly
- Term presence is more important than frequency
- Working with short documents or tags

**LOG**: Use when:
- Want to dampen effect of high-frequency terms
- Standard choice for most applications
- Balances term importance

**NORMAL**: Use when:
- Document length normalization is critical
- Creating probability distributions
- Comparing across documents of different lengths

**AUGMENT**: Use when:
- Document length varies dramatically
- Want to prevent bias towards longer documents
- Need to balance between short and long documents

### 2. Choose Appropriate IDF Normalization

**LOG**: Use for:
- Standard TF-IDF applications
- General document ranking
- Most common choice

**SMOOTH**: Use for:
- Handling rare terms
- Preventing zero division
- More stable results with small corpora

**LOGNORM**: Use for:
- Ensuring all IDF values are positive
- Mathematical convenience
- Similar to LOG but shifted

**UNARY**: Use for:
- Disabling IDF weighting
- When all terms should be weighted equally
- Testing TF impact alone

### 3. Choose Appropriate Regularization

**L2 (Euclidean)**: Use for:
- Cosine similarity calculations
- Document clustering
- Most common choice
- Creates unit-length vectors

**L1 (Manhattan)**: Use for:
- Probability-like distributions
- Sparse representations
- When sum-to-one normalization needed

**NONE**: Use for:
- Raw TF-IDF scores
- When downstream process handles normalization
- Interpretability over comparability

### 4. Preprocessing Recommendations

```sql
-- Recommended preprocessing pipeline:
-- 1. Tokenize with TD_TextParser
--    - Convert to lowercase
--    - Remove stop words
--    - Stem tokens (optional)
--    - Remove punctuation

-- 2. Filter tokens
--    - Remove very rare terms (appear in < 2 documents)
--    - Remove very common terms (appear in > 80% documents)
--    - Keep tokens with reasonable length (3-20 characters)

-- 3. Apply TD_TFIDF
--    - Choose appropriate normalization methods
--    - Preserve document metadata with Accumulate
```

### 5. Performance Optimization

```sql
-- For large corpora:
-- 1. Filter input before TF-IDF calculation
WHERE token_length BETWEEN 3 AND 20
  AND token NOT IN (SELECT term FROM very_common_terms)

-- 2. Sample documents for parameter tuning
SAMPLE 0.1

-- 3. Create indexes on document ID for joins
CREATE INDEX idx_docid ON tfidf_results(docid);

-- 4. Filter low TF-IDF scores in output
WHERE TD_TF_IDF > 0.01
```

## Related Functions

- **TD_TextParser**: Tokenize documents before TF-IDF calculation
- **TD_Ngramsplitter**: Create n-gram features for TF-IDF
- **TD_WordEmbeddings**: Alternative to TF-IDF for document representation
- **TD_TextMorph**: Lemmatize tokens before TF-IDF

## Notes and Limitations

### 1. Input Requirements
- Input must be in document-token pairs format
- Typically created by TD_TextParser or similar tokenization
- Each row represents one token occurrence in one document
- Duplicate token occurrences should be preserved

### 2. Sparse Representation
- Output only includes terms that appear in documents
- Absent terms (with TF-IDF = 0) are not included
- Results in sparse document vectors
- Efficient for high-dimensional spaces

### 3. Document Vector Dimensionality
- Vector dimension = Total unique terms in corpus
- Can be very high-dimensional
- Consider dimensionality reduction techniques:
  - Filter low TF-IDF scores
  - Remove rare/common terms
  - Use feature selection methods

### 4. Normalization Impact
- Different normalization methods produce different scales
- Regularization methods make vectors comparable
- L2 normalization essential for cosine similarity
- Choose methods based on downstream use case

### 5. Computational Complexity
- Scales with total token count in corpus
- Large corpora may require significant processing time
- Consider filtering and sampling for very large datasets

### 6. IDF Calculation
- IDF calculated across entire input corpus
- Sensitive to corpus size and composition
- Rare terms in small corpora may have unstable IDF values
- Use SMOOTH IDF for small or imbalanced corpora

### 7. Memory Considerations
- Output table size = Input table size + calculated columns
- Large corpora generate large output tables
- Consider filtering output or aggregating results
- Use appropriate storage mechanisms

### 8. Document Length Bias
- Raw counts favor longer documents
- Use AUGMENT or NORMAL TF normalization for mixed lengths
- L2 regularization also helps with length normalization

## Version Information

- **Function Version**: Based on Teradata Database Analytic Functions Version 17.20
- **Generated**: November 28, 2025
- **Algorithm**: Term Frequency-Inverse Document Frequency (TF-IDF)
