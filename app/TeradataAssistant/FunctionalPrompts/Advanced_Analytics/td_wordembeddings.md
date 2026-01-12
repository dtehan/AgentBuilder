# TD_WordEmbeddings

## Function Name
- **TD_WordEmbeddings**: Creates word and document embeddings using pre-trained vectors and calculates text similarity

## Description
Word embedding is the representation of a word/token in multi-dimensional space such that words/tokens with similar meanings have similar embeddings. Each word/token is mapped to a vector of real numbers that represent the word/token. The Analytics Database function TD_WordEmbeddings produces vectors for each piece of text and can find the similarity between the texts. The options are token-embedding, doc-embedding, token2token-similarity, and doc2doc-similarity.

The ModelTable contains pretrained words/tokens and their corresponding vector mappings in multidimensional space. You can use pre-defined vectors from Word Vectors, or train your own using packages such as GloVe or Word2Vec. Note that the ModelTable format expects the vectors in GloVe format (one word/token vector pair per row). To convert a Word2Vec file, simply delete the first row which contains the number of words or tokens and the number of dimensions.

### Characteristics
- Semantic representation of words and documents
- Pre-trained embeddings (GloVe, Word2Vec format)
- Four operation modes: token embedding, document embedding, token similarity, document similarity
- Supports text preprocessing (lowercasing, stemming, stop word removal)
- Calculates semantic similarity scores

## When to Use TD_WordEmbeddings

### Semantic Search
- Find documents with similar meaning (not just keyword matching)
- Improve search relevance with semantic understanding
- Handle synonyms and related terms automatically

### Document Similarity
- Group similar documents together
- Find duplicate or near-duplicate content
- Build recommendation systems based on content

### Text Classification
- Create features for classification models
- Capture semantic meaning in feature vectors
- Improve classification accuracy over TF-IDF

### Information Retrieval
- Rank search results by semantic relevance
- Query expansion using similar terms
- Cross-lingual search with multilingual embeddings

## Syntax

```sql
TD_WordEmbeddings (
    ON { table | view | (query) } AS InputTable PARTITION BY ANY
    ON { table | view | (query) } AS ModelTable DIMENSION
    USING
    IDColumn ('IDColumn')
    ModelVectorColumns ({ 'vector_columns | vector_columns_range' }[,...])
    ModelTextColumn ('text_columns')
    PrimaryColumn ('text_column')
    [ SecondaryColumn ('text_column') ]
    [ Accumulate ('text_column') ]
    [ Operation ({ 'token-embedding' | 'doc-embedding' |
                  'token2token-similarity'|'doc2doc-similarity'}) ]
    [ RemoveStopWords ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
    [ ConvertToLowerCase ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
    [ StemTokens ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
)
```

**Note:** You can call this function from:
- The FROM clause of a SELECT statement
- As part of a CREATE TABLE statement
- As part of a CREATE VIEW statement

## Required Elements

### IDColumn
**Required**: Identifier that uniquely identifies the row of the input table.
- **Data Type**: INTEGER, CHAR, VARCHAR (CHARACTER SET LATIN or UNICODE)

### ModelVectorColumns
**Required**: Range of columns in the model table that contains real value vector.
- **Format**: Column range specification (e.g., '[1:4]', '[1:100]')
- **Data Type**: REAL/FLOAT columns in model table

### ModelTextColumn
**Required**: Column that contains the token in the model.
- **Purpose**: Maps tokens to their embedding vectors
- **Data Type**: CHAR/VARCHAR

### PrimaryColumn
**Required**: Name of the input table column that contains the text.
- **Purpose**: Primary text to analyze (all operations)
- **Data Type**: CHAR, VARCHAR (CHARACTER SET LATIN)

## Optional Elements

### SecondaryColumn
Name of the input table column that contains the text for comparison.
- **Purpose**: Second text for similarity operations
- **Required For**: token2token-similarity and doc2doc-similarity operations
- **Not Applicable For**: token-embedding and doc-embedding operations
- **Data Type**: CHAR, VARCHAR (CHARACTER SET LATIN)

### Accumulate
List of columns to be added to the output from the input table.
- **Purpose**: Preserve metadata in output
- **Not Applicable For**: token-embedding operation

### Operation
Operation to be performed on the data.
- **Default**: 'token-embedding'

**Available Operations**:

| Operation | Description | Output |
|-----------|-------------|--------|
| **token-embedding** | Emits vectors to all tokens in the column. Each token is mapped to a vector of real numbers representing semantic meaning | Token vectors (v1, v2, ..., vN) |
| **doc-embedding** | Vectorizes each token in the document and combines them into a single document vector | Document vector (v1, v2, ..., vN) |
| **token2token-similarity** | Computes similarity between two tokens and quantifies the result value | Similarity score |
| **doc2doc-similarity** | Computes similarity between two documents and quantifies the result value | Similarity score |

**Operation Details**:

**token-embedding**: Maps individual words to their embedding vectors
- Example: "dog" → [0.1, 0.2, 0.3, 0.4, 0.5]
- Each dimension represents an aspect of the word's meaning
- Useful for word-level analysis and comparisons

**doc-embedding**: Creates a single vector representing an entire document
- Example: "The dog ran across the street" → [0.1, 0.2, 0.3, ...]
- Combines embeddings of all tokens (typically by averaging)
- Useful for document classification and clustering

**token2token-similarity**: Measures semantic similarity between two words
- Example: similarity("dog", "cat") > similarity("dog", "table")
- Uses cosine similarity of embedding vectors
- Values typically range from -1 (opposite) to 1 (identical)

**doc2doc-similarity**: Measures semantic similarity between two documents
- Example: Compares "The dog ran" with "The cat sat"
- Uses document embeddings (from doc-embedding operation)
- Higher scores indicate more similar content/meaning

### RemoveStopWords
Stop words in English include "the", "and", "in", "of", "to", "is", "it", "on", "at", etc.
- **Default**: 'false'
- **Purpose**: Remove common words before processing
- **Applicable To**: All operations except token2token-similarity

### ConvertToLowerCase
All operations are performed after converting input table text to lowercase letters.
- **Default**: 'true'
- **Purpose**: Normalize text for better embedding matching

### StemTokens
Converts word to its root word in the input table, such as converting "going" to "go".
- **Default**: 'false'
- **Purpose**: Normalize word forms for better embedding matching

## Input Schema

### Input Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| IDColumn | INTEGER, CHAR, VARCHAR (CHARACTER SET LATIN or UNICODE) | Identifier that uniquely identifies the row |
| PrimaryColumn | CHAR, VARCHAR (CHARACTER SET LATIN) | Name of the input column that contains the text |
| SecondaryColumn | CHAR, VARCHAR (CHARACTER SET LATIN) | Name of the input column that contains the text. Required for token2token-similarity and doc2doc-similarity |

### Model Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| ModelTextColumn | CHAR, VARCHAR | Token/word from vocabulary |
| Vector columns (v1, v2, ..., vN) | REAL/FLOAT | Embedding vector coordinates |

**Model Format**: GloVe format expected (one word-vector pair per row)
- Each row: token followed by N real numbers representing the embedding
- No header row with dimensions (Word2Vec files must have first row deleted)

## Output Schema

### Output for token-embedding and doc-embedding

| Column | Data Type | Description |
|--------|-----------|-------------|
| IDColumn | INTEGER, CHAR, VARCHAR | Unique row identifier |
| tokenColumn | VARCHAR (CHARACTER SET LATIN) | Tokens from the target column data. Applicable for token-embedding only |
| v1 | Real | Coordinate point of the first dimension |
| v2 | Real | Coordinate point of the second dimension |
| ... | Real | Additional dimensions as specified in model |
| vN | Real | Coordinate point of the Nth dimension |
| Accumulate columns | Same as input data type | Columns added from the input. Applicable for doc-embedding only |

**Note**: There are as many v columns as there are dimensions in the embedding model.

### Output for token2token-similarity and doc2doc-similarity

| Column | Data Type | Description |
|--------|-----------|-------------|
| IDColumn | INTEGER, CHAR, VARCHAR | Unique row identifier |
| similarity | Real | Similarity value between two text values (cosine similarity, typically -1 to 1) |
| Accumulate columns | Same as input data type | Columns added from the input |

## Code Examples

### Example Setup: Model Table and Input Data

Create the model table with pre-trained embeddings:

```sql
CREATE TABLE wordEmbedModel (
    token VARCHAR(50) CHARACTER SET LATIN,
    v1 REAL,
    v2 REAL,
    v3 REAL,
    v4 REAL
);

-- Insert pre-trained word embeddings (sample GloVe-format vectors)
INSERT INTO wordEmbedModel VALUES('assisted', 0.10058, 0.1914, 0.28125, 0.17382);
INSERT INTO wordEmbedModel VALUES('by', -0.11572, -0.03149, 0.15917, 0.13867);
INSERT INTO wordEmbedModel VALUES('delicious', -0.18164, -0.13281, 0.03906, 0.31445);
INSERT INTO wordEmbedModel VALUES('dinner', -0.06152, -0.08496, -0.15039, 0.42382);
INSERT INTO wordEmbedModel VALUES('food', -0.18164, -0.16503, -0.16601, 0.35742);
INSERT INTO wordEmbedModel VALUES('i', -0.22558, -0.01953, 0.09082, 0.2373);
INSERT INTO wordEmbedModel VALUES('like', 0.10351, 0.13769, -0.00297, 0.18164);
INSERT INTO wordEmbedModel VALUES('love', 0.10302, -0.15234, 0.02587, 0.16503);
INSERT INTO wordEmbedModel VALUES('pizza', -0.12597, 0.02539, 0.16699, 0.55078);
-- ... (more embeddings)
```

Create input table for token/document embedding:

```sql
CREATE TABLE wordEmb_inputTable (
    doc_id INTEGER,
    doc1 VARCHAR(200) CHARACTER SET LATIN,
    doc2 VARCHAR(200) CHARACTER SET LATIN
);

INSERT INTO wordEmb_inputTable VALUES
(1, 'I like pizza', 'I love pizza');

INSERT INTO wordEmb_inputTable VALUES
(2, 'single_token', 'token');

INSERT INTO wordEmb_inputTable VALUES
(3, 'food is delicious', 'dinner is yummy');

INSERT INTO wordEmb_inputTable VALUES
(4, 'tokyo hosting olympics', 'food is delicious');

INSERT INTO wordEmb_inputTable VALUES
(5, 'person xyz was assisted by nurses', 'few medics helped person xyz');
```

Create input table for similarity operations:

```sql
CREATE TABLE wordEmb_inputTable2 (
    token_id INTEGER,
    Token1 VARCHAR(50) CHARACTER SET LATIN,
    Token2 VARCHAR(50) CHARACTER SET LATIN
);

INSERT INTO wordEmb_inputTable2 VALUES(1, 'food', 'delicious');
INSERT INTO wordEmb_inputTable2 VALUES(2, 'pizza', 'food');
INSERT INTO wordEmb_inputTable2 VALUES(3, 'love', 'like');
INSERT INTO wordEmb_inputTable2 VALUES(4, 'nurses', 'olympics');
```

### Example 1: Token Embedding

Generate embedding vectors for individual tokens:

```sql
SELECT * FROM TD_wordembeddings (
    ON wordEmb_inputTable AS InputTable
    ON wordEmbedModel AS ModelTable DIMENSION
    USING
    IDColumn('doc_id')
    ModelVectorColumns('[1:4]')
    PrimaryColumn('doc1')
    Operation('token-embedding')
    ModelTextColumn('token')
) AS dt
ORDER BY doc_id ASC;
```

**Purpose**: Get embedding vectors for each individual word in documents.

**Sample Output**:

| id | token | v1 | v2 | v3 | v4 |
|----|-------|-------|-------|-------|-------|
| 1 | i | -0.22558 | -0.01953 | 0.09082 | 0.2373 |
| 1 | like | 0.10351 | 0.13769 | -0.00297 | 0.18164 |
| 1 | pizza | -0.12597 | 0.02539 | 0.16699 | 0.55078 |
| 2 | single_token | 0 | 0 | 0 | 0 |
| 3 | delicious | -0.18164 | -0.13281 | 0.03906 | 0.31445 |
| 3 | is | 0.00704 | -0.07324 | 0.17187 | 0.02258 |
| 3 | food | -0.18164 | 0.16503 | -0.16601 | 0.35742 |

**Note**: Tokens not in model (like "single_token") get zero vectors.

### Example 2: Document Embedding

Create document-level embedding vectors:

```sql
SELECT * FROM TD_wordembeddings (
    ON wordEmb_inputTable AS InputTable
    ON wordEmbedModel AS ModelTable DIMENSION
    USING
    IDColumn('doc_id')
    ModelVectorColumns('[1:4]')
    PrimaryColumn('doc1')
    Operation('doc-embedding')
    ModelTextColumn('token')
    Accumulate('doc1')
) AS dt
ORDER BY doc_id ASC;
```

**Purpose**: Get a single embedding vector representing each document.

**Sample Output**:

| doc_id | v1 | v2 | v3 | v4 | doc |
|--------|--------|--------|--------|--------|-----------------|
| 1 | -0.08268 | 0.04785 | 0.08494 | 0.32324 | i like pizza |
| 2 | 0 | 0 | 0 | 0 | single_token |
| 3 | -0.11874 | -0.01367 | 0.01497 | 0.23148 | food is delicious |
| 4 | -0.17236 | 0.07531 | 0.03615 | 0.16654 | tokyo hosting olympics |
| 5 | 0.03735 | 0.02129 | 0.07659 | 0.1263 | person xyz was assisted by nurses |

**Note**: Document vector is typically the average of token vectors.

### Example 3: Token-to-Token Similarity

Calculate semantic similarity between word pairs:

```sql
SELECT * FROM TD_wordembeddings (
    ON wordEmb_inputTable2 AS InputTable
    ON wordEmbedModel AS ModelTable DIMENSION
    USING
    IDColumn('token_id')
    ModelVectorColumns('[1:4]')
    PrimaryColumn('token1')
    SecondaryColumn('token2')
    Operation('token2token-similarity')
    ModelTextColumn('token')
    Accumulate('token1', 'token2')
) AS dt
ORDER BY token_id ASC;
```

**Purpose**: Measure semantic similarity between word pairs.

**Sample Output**:

| doc_id | Similarity | Token1 | Token2 |
|--------|-----------|--------|---------|
| 1 | 0.64836 | food | delicious |
| 2 | 0.71667 | pizza | food |
| 3 | 0.31491 | love | like |
| 4 | 0.21295 | nurses | olympics |

**Interpretation**:
- "pizza" and "food" are highly similar (0.72)
- "food" and "delicious" are related (0.65)
- "nurses" and "olympics" are not related (0.21)

### Example 4: Document-to-Document Similarity

Calculate semantic similarity between document pairs:

```sql
SELECT * FROM TD_wordembeddings (
    ON wordEmb_inputTable AS InputTable
    ON wordEmbedModel AS ModelTable DIMENSION
    USING
    IDColumn('doc_id')
    ModelVectorColumns('[1:4]')
    PrimaryColumn('doc1')
    SecondaryColumn('doc2')
    Operation('doc2doc-similarity')
    ModelTextColumn('token')
    Accumulate('doc1', 'doc2')
) AS dt
ORDER BY doc_id ASC;
```

**Purpose**: Measure semantic similarity between document pairs.

**Sample Output**:

| doc_id | Similarity | doc1 | doc2 |
|--------|-----------|------|------|
| 1 | 0.96055 | i like pizza | i love pizza |
| 2 | 0 | single_token | token |
| 3 | 0.97761 | food is delicious | dinner is yummy |
| 4 | 0.88368 | tokyo hosting olympics | food is delicious |
| 5 | 0.94299 | person xyz was assisted by nurses | few medics helped person xyz |

**Interpretation**:
- Documents 1 and 3 are very similar (>0.96) despite different words
- Document 2 has zero similarity (token not in model)
- Semantic similarity captured beyond exact word matching

## Common Use Cases

### 1. Semantic Document Search

Find documents similar to a query:

```sql
-- Create document embeddings for corpus
CREATE TABLE doc_embeddings AS (
    SELECT
        doc_id,
        v1, v2, v3, v4  -- Embedding dimensions
    FROM TD_WordEmbeddings (
        ON document_corpus AS InputTable
        ON pretrained_embeddings AS ModelTable DIMENSION
        USING
        IDColumn('doc_id')
        ModelVectorColumns('[1:300]')  -- 300-dim embeddings
        PrimaryColumn('content')
        Operation('doc-embedding')
        ModelTextColumn('word')
        ConvertToLowerCase('true')
        RemoveStopWords('true')
    ) AS dt
) WITH DATA;

-- Find similar documents to a query
CREATE VOLATILE TABLE query_embedding AS (
    SELECT v1, v2, v3, v4
    FROM TD_WordEmbeddings (
        ON (SELECT 'machine learning algorithms' as query_text) AS InputTable
        ON pretrained_embeddings AS ModelTable DIMENSION
        USING
        IDColumn('1' as id)
        ModelVectorColumns('[1:300]')
        PrimaryColumn('query_text')
        Operation('doc-embedding')
        ModelTextColumn('word')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Calculate similarities
-- (Use cosine similarity formula on embedding vectors)
```

### 2. Text Classification Feature Engineering

Use embeddings as features for classification:

```sql
-- Generate document embeddings as features
CREATE TABLE classification_features AS (
    SELECT
        doc_id,
        category as label,
        v1, v2, v3, v4, v5, v6, v7, v8, v9, v10  -- First 10 dimensions
    FROM TD_WordEmbeddings (
        ON training_docs AS InputTable
        ON word2vec_model AS ModelTable DIMENSION
        USING
        IDColumn('doc_id')
        ModelVectorColumns('[1:100]')
        PrimaryColumn('text')
        Operation('doc-embedding')
        ModelTextColumn('word')
        Accumulate('category')
        RemoveStopWords('true')
        StemTokens('true')
    ) AS dt
) WITH DATA;

-- Use these features in TD_XGBoost, TD_GLM, etc.
```

### 3. Synonym Detection and Expansion

Find semantically similar terms:

```sql
-- Find words similar to "excellent"
WITH target_embedding AS (
    SELECT v1, v2, v3, v4
    FROM TD_WordEmbeddings (
        ON (SELECT 'excellent' as word) AS InputTable
        ON glove_embeddings AS ModelTable DIMENSION
        USING
        IDColumn('1' as id)
        ModelVectorColumns('[1:50]')
        PrimaryColumn('word')
        Operation('token-embedding')
        ModelTextColumn('token')
    ) AS dt
)
-- Calculate similarity with all vocabulary words
-- (Compare target_embedding with all words in model)
```

### 4. Content-Based Recommendation

Recommend similar documents:

```sql
-- For each document, find most similar documents
SELECT
    a.doc_id as source_doc,
    b.doc_id as recommended_doc,
    similarity_score
FROM TD_WordEmbeddings (
    ON document_pairs AS InputTable
    ON embeddings_model AS ModelTable DIMENSION
    USING
    IDColumn('pair_id')
    ModelVectorColumns('[1:100]')
    PrimaryColumn('doc1_text')
    SecondaryColumn('doc2_text')
    Operation('doc2doc-similarity')
    ModelTextColumn('word')
    Accumulate('doc1_id', 'doc2_id')
) AS dt
WHERE similarity_score > 0.7  -- Threshold for "similar"
ORDER BY source_doc, similarity_score DESC;
```

## Best Practices

### 1. Choose Appropriate Pre-trained Embeddings

**GloVe** (Global Vectors):
- Good for general English text
- Available in different dimensions (50, 100, 200, 300)
- Trained on Wikipedia and web data

**Word2Vec**:
- Good for domain-specific applications
- Can be trained on your corpus
- Available pre-trained on Google News

**FastText**:
- Handles out-of-vocabulary words better
- Good for morphologically rich languages
- Subword information included

### 2. Embedding Dimensionality

```sql
-- Smaller dimensions (50-100): Faster, less memory, less expressive
ModelVectorColumns('[1:50]')

-- Medium dimensions (100-200): Good balance
ModelVectorColumns('[1:100]')

-- Larger dimensions (300+): More expressive, slower
ModelVectorColumns('[1:300]')
```

### 3. Text Preprocessing

```sql
-- Standard preprocessing pipeline:
ConvertToLowerCase('true')   -- Normalize case
RemoveStopWords('true')      -- Remove common words
StemTokens('false')          -- Usually not needed for embeddings

-- Stemming can hurt embedding matching
-- Better to rely on embeddings to capture word relationships
```

### 4. Handling Out-of-Vocabulary Words

```sql
-- Words not in model get zero vectors
-- Strategies:
-- 1. Use larger pre-trained models
-- 2. Train custom embeddings on your domain
-- 3. Use FastText (handles subwords)
-- 4. Filter/replace rare words before embedding
```

### 5. Similarity Interpretation

**Cosine Similarity Scale**:
- 1.0: Identical vectors (same meaning)
- 0.7-0.9: Very similar (synonyms, related concepts)
- 0.5-0.7: Moderately similar (related domain)
- 0.3-0.5: Weakly similar (distant relation)
- < 0.3: Not similar

### 6. Operation Selection

```sql
-- For word-level analysis:
Operation('token-embedding')

-- For document classification/clustering:
Operation('doc-embedding')

-- For semantic similarity of words:
Operation('token2token-similarity')

-- For document similarity/search:
Operation('doc2doc-similarity')
```

## Related Functions

- **TD_TextParser**: Tokenize text before embedding (if using token-embedding)
- **TD_TFIDF**: Alternative document representation (bag-of-words vs semantic)
- **TD_XGBoost/TD_GLM**: Use embeddings as features for classification
- **TD_KMeans**: Cluster documents using embedding vectors

## Notes and Limitations

### 1. Character Set Support
- **Supports**: CHARACTER SET LATIN only
- **Does not support**: CHARACTER SET UNICODE
- All input text must be LATIN character set

### 2. Model Format Requirements
- Expects **GloVe format**: one word-vector pair per row
- No header row with dimensions
- For Word2Vec files: Delete first row (contains metadata)
- Each row: token followed by N real numbers

### 3. Out-of-Vocabulary Handling
- Words not in model get **zero vectors**
- This can affect document embeddings
- Consider pre-trained models with larger vocabularies
- Or train custom embeddings on your domain

### 4. Document Embedding Calculation
- Typically **averages** token embeddings
- All tokens weighted equally
- No TF-IDF or importance weighting
- Consider preprocessing to remove noise

### 5. Similarity Calculation
- Uses **cosine similarity**
- Range: -1 (opposite) to 1 (identical)
- 0 indicates orthogonal (unrelated) vectors
- Normalized by vector magnitude

### 6. Performance Considerations
- Larger embedding dimensions = slower processing
- Model table should be indexed on token column
- Consider filtering input for large datasets
- Pre-compute embeddings for frequently accessed documents

### 7. Language Support
- English language only (for most pre-trained models)
- Multilingual embeddings available but require specific models
- Performance varies by language and model

### 8. Memory Requirements
- Model table loaded into memory (DIMENSION clause)
- Large models (millions of words, 300+ dimensions) require significant memory
- Consider model size vs available cluster memory

### 9. Accumulate Limitations
- **Not applicable** for token-embedding operation
- Only applicable for doc-embedding and similarity operations
- Preserves metadata in output

### 10. SecondaryColumn Requirements
- **Required** for similarity operations
- **Not used** for embedding operations
- Must be same data type as PrimaryColumn

## Version Information

- **Function Version**: Based on Teradata Database Analytic Functions Version 17.20
- **Generated**: November 28, 2025
- **Supported Formats**: GloVe, Word2Vec (converted)
- **Algorithm**: Word embeddings with cosine similarity
