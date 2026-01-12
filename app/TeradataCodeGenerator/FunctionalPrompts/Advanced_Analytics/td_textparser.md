# TD_TextParser

## Function Name
- **TD_TextParser**: Text tokenizer that parses text into individual tokens with advanced preprocessing capabilities

## Description
A text parser, also known as a text tokenizer, is a software component that breaks a text into its constituent parts, such as words, phrases, sentences, or other meaningful units. Text parsing is an important technique in natural language processing (NLP) and is used in a wide range of applications, from search engines and chatbots to email filters and data analysis tools.

The TD_TextParser function performs the following operations:
- **Tokenizes** text with single-character delimiter values or PCRE regular expression delimiters
- **Removes punctuation** from the text and converts text to lowercase
- **Removes stop words** from the text
- **Converts words to their root forms** through stemming
- **Creates a row for each word** in the output table (or single row with all tokens)
- **Counts token occurrences** and tracks positions
- **Performs stemming**: identifies the common root form of a word by removing or replacing word suffixes

### Characteristics
- Flexible tokenization with regex support
- Built-in stop word removal
- Porter stemming algorithm support
- Token frequency counting
- Position tracking for tokens
- Single-row or multi-row output options
- Case conversion capabilities

### Important Note on Stemming
The stems resulting from stemming may not be actual words. For example:
- The stem for 'communicate' is 'commun'
- The stem for 'early' is 'earli' (trailing 'y' is replaced by 'i')

## When to Use TD_TextParser

### Text Feature Engineering
- Prepare text for machine learning models
- Create bag-of-words representations
- Generate token-based features

### Search Index Building
- Build inverted indexes for search engines
- Create searchable token repositories
- Generate keyword lists

### Text Analysis Preprocessing
- Clean and normalize text data
- Remove noise and stop words
- Standardize word forms

### Document Processing
- Parse documents for content analysis
- Extract meaningful tokens
- Prepare text for downstream analytics

## Syntax

```sql
TD_TextParser (
    ON { table | view | (query) } AS InputTable
    [ ON { table | view | (query) } AS StopWordsTable DIMENSION ]
    USING
    TextColumn ('text_column')
    [ ConvertToLowerCase ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
    [ StemTokens ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
    [ RemoveStopWords ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
    [ Delimiter ('delimiter_expression') ]
    [ DelimiterRegex ('delimiter_PCRE_regular_expression') ]
    [ Punctuation ('punctuation_expression') ]
    [ TokenColName ('token_column') ]
    [ Accumulate ({ 'accumulate_column' | 'accumulate_column_range' }[,...]) ]
    [ DocIDColumn ('docIdColumn') ]
    [ ListPositions ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
    [ TokenFrequency ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
    [ OutputByWord ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
)
```

**Note:** You can call this function from:
- The FROM clause of a SELECT statement
- As part of a CREATE TABLE statement
- As part of a CREATE VIEW statement

## Required Elements

### ON Clause (InputTable)
Accept the InputTable clause.

### TextColumn
**Required**: Specify the input table column name containing text to parse.
- **Data Type**: CHAR, VARCHAR, or CLOB
- **Character Set**: LATIN or UNICODE
- **Note**: CLOB LATIN/UTF16 is only supported on the Block File System on the primary cluster

## Optional Elements

### ON Clause (StopWordsTable)
Accept the StopWordsTable clause for custom stop word list.

### ConvertToLowerCase
Convert the text in the input table column name to lowercase.
- **Default**: 'true'
- **Note**: When StemTokens is set to 'true', TD_TextParser behaves as if ConvertToLowerCase had the value 'true' regardless of the actual value

### StemTokens
Convert the text in the input table column name to their root forms using Porter stemming.
- **Default**: 'false'
- **Behavior**: When 'true', automatically converts to lowercase

### Delimiter
Specify single-character delimiter values to apply to the text.
- **Default**: ' \\t\\n\\f\\r' (space, tab, newline, form feed, carriage return)
- **Format**: String of delimiter characters
- **Constraint**: Cannot use with DelimiterRegex

### DelimiterRegex
Specifies a PCRE regular expression that represents the token delimiter.
- **No default value**: User must provide a valid PCRE regex when used
- **Constraint**: Cannot use with Delimiter
- **Behavior**: Empty tokens are not part of the output and are silently discarded

### RemoveStopWords
Specify whether to remove stop words before parsing the text.
- **Default**: 'false'
- **Purpose**: Remove common words like "the", "a", "is", etc.
- **Requirement**: Requires StopWordsTable if 'true'

### Punctuation
Specify the punctuation characters to replace in the text with space.
- **Default**: '!#$%&()*+,-./:;?@\\^_\`{|}~'
- **Format**: String of punctuation characters

### TokenColName
Specify a name for the output column that contains the individual words from the text.
- **Default**: 'token'
- **Constraints**:
  - Cannot have spaces
  - Do not use any reserved SQL word
  - Cannot use column names requiring double quotations
  - No special characters, numerics only, or reserved keywords

### Accumulate
Specify the input table column names to copy to the output table.
- **Default**: All input columns are copied

### DocIDColumn
Specify the column name containing the unique identifier of input rows.
- **When Required**: Only if ListPositions is 'true' and/or TokenFrequency is 'true' AND OutputByWord is 'true'
- **Data Type**: BYTEINT, SMALLINT, INTEGER, BIGINT, CHAR, or VARCHAR

### ListPositions
Specify whether to output a list of comma-separated positions for each occurrence of a token.
- **Default**: 'false'
- **Behavior**:
  - 'true': Output comma-separated list of positions (requires OutputByWord 'true')
  - 'false': Output a row for each occurrence of the word
- **List Arrangement**: Ascending order
- **Note**: Function ignores this argument if OutputByWord is 'false'

### TokenFrequency
Specify whether to output a count of the total occurrences for each token.
- **Default**: 'false'
- **Note**: TD_TextParser ignores this argument if OutputByWord is 'false'

### OutputByWord
Specifies whether to output all tokens in a single cell or each token in a separate row.
- **Default**: 'true'
- **Values**:
  - 'true': Each token in a separate row
  - 'false': All tokens in a single cell (space-separated)

## Input Schema

### InputTable Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| text_column | CHAR, VARCHAR, CLOB CHARACTER SET LATIN/UNICODE | The column name that contains the text to parse |
| accumulate_column | Any | The input table column names to copy to the output table |
| docIdColumn | BYTEINT, SMALLINT, INTEGER, BIGINT, CHAR, VARCHAR | Unique identifier of input rows |

### StopWordsTable Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| words | CHAR, VARCHAR, CLOB CHARACTER SET LATIN/UNICODE | The column name that contains the stopwords |

## Output Schema

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| docIdColumn | BYTEINT, SMALLINT, INTEGER, BIGINT, CHAR, VARCHAR | Unique identifier of input rows. If provided, it is always the first column in output table |
| AccumulateColumns | ANY | Columns to be copied from input to output. Default: All input columns are copied to output |
| TokenColumn | VARCHAR | Column containing individual tokens. Default name: 'token' |
| frequency | INTEGER | (Optional) Value indicating the total occurrences of a token. Appears when TokenFrequency is 'true' |
| locations | VARCHAR or BIGINT | (Optional) Comma-separated list of values, sorted in ascending order. When ListPositions is 'true' and OutputByWord is 'true', type is VARCHAR. When ListPositions is 'false' and OutputByWord is 'true', each position displayed separately with type BIGINT |
| tokens | CHAR, VARCHAR, CLOB | (Optional) When OutputByWord is 'false': Space-separated list of tokens in a single cell |

## Code Examples

### Example Setup: Input Tables

Create test input table:

```sql
CREATE TABLE test_table (
    id INTEGER,
    paragraph VARCHAR(1000)
);

INSERT INTO test_table VALUES
(1, 'Programmers program with program, as.as programming languages a program');

INSERT INTO test_table VALUES
(2, 'The quick brown fox jumps over the lazy dog');
```

Create stop words table:

```sql
CREATE TABLE stopwords (
    word VARCHAR(10)
);

INSERT INTO stopwords VALUES('a');
INSERT INTO stopwords VALUES('an');
INSERT INTO stopwords VALUES('and');
INSERT INTO stopwords VALUES('the');
```

### Example 1: Basic Text Parsing with Stop Words

Parse text, remove stop words, and stem tokens:

```sql
SELECT * FROM TD_TextParser (
    ON test_table AS InputTable
    ON stopwords AS StopWordsTable DIMENSION
    USING
    TextColumn ('paragraph')
    StemTokens ('true')
    RemoveStopWords ('true')
    Accumulate ('id')
) AS dt
ORDER BY id, token;
```

**Purpose**: Clean and normalize text for analysis.

**Result**:

| id | token |
|----|-------|
| 1 | languag |
| 1 | program |
| 1 | program |
| 1 | programm |
| 1 | with |
| 2 | brown |
| 2 | dog |
| 2 | fox |
| 2 | jump |
| 2 | lazi |
| 2 | over |
| 2 | quick |

**Note**:
- Stop words removed ('the', 'a')
- Words stemmed ('programmers' → 'programm', 'lazy' → 'lazi')
- Duplicates preserved (two instances of 'program')

### Example 2: Token Frequency and Position List

Get token frequencies and their positions in documents:

```sql
SELECT * FROM TD_TextParser (
    ON test_table AS InputTable
    ON stopwords AS StopWordsTable DIMENSION
    USING
    TextColumn ('paragraph')
    RemoveStopWords ('true')
    DocIDColumn('id')
    ListPositions('t')
    TokenFrequency('t')
) AS dt
ORDER BY id, token;
```

**Purpose**: Track where and how often each token appears.

**Result**:

| id | paragraph | token | frequency | locations |
|----|-----------|-------|-----------|-----------|
| 1 | Programmers program... | programmers | 1 | 1 |
| 1 | Programmers program... | program | 2 | 2,8 |
| 1 | Programmers program... | with | 1 | 3 |
| 1 | Programmers program... | programming | 1 | 5 |
| 1 | Programmers program... | language | 1 | 6 |
| 2 | The quick brown... | quick | 1 | 1 |
| 2 | The quick brown... | brown | 1 | 2 |
| 2 | The quick brown... | fox | 1 | 3 |
| 2 | The quick brown... | jumps | 1 | 4 |

### Example 3: Single Row Output with All Tokens

Output all tokens in a single cell per document:

```sql
SELECT * FROM TD_TextParser (
    ON test_table AS InputTable
    ON stopwords AS StopWordsTable DIMENSION
    USING
    TextColumn ('paragraph')
    RemoveStopWords ('true')
    Delimiter(' ')
    OutputByWord('false')
) AS dt
ORDER BY id;
```

**Purpose**: Compact representation of all tokens.

**Result**:

| id | paragraph | tokens |
|----|-----------|--------|
| 1 | Programmers program... | programmers program program programming languages program |
| 2 | The quick brown... | quick brown fox jumps over lazy dog |

### Example 4: Using Regular Expression Delimiter

Use regex to define complex delimiter patterns:

```sql
SELECT * FROM TD_TextParser (
    ON test_table AS InputTable
    USING
    TextColumn ('paragraph')
    RemoveStopWords ('true')
    DocIDColumn('id')
    DelimiterRegex('[ \\t\\f\\r\\n]+')
    ListPositions('true')
) AS dt
ORDER BY id, locations;
```

**Purpose**: Handle multiple whitespace characters as delimiters.

**Result**:

| id | paragraph | tokens | locations |
|----|-----------|--------|-----------|
| 1 | Programmers program... | programmers | 1 |
| 1 | Programmers program... | program | 2,8 |
| 1 | Programmers program... | programming | 5 |
| 1 | Programmers program... | language | 6 |
| 2 | The quick brown... | quick | 1 |
| 2 | The quick brown... | brown | 2 |

### Example 5: Tokenization with Default Delimiter

Simple tokenization without stop word removal:

```sql
SELECT id, paragraph, token, locations
FROM TD_TextParser (
    ON test_table AS InputTable
    USING
    TextColumn ('paragraph')
) AS dt
ORDER BY id, locations;
```

**Purpose**: Basic word-level tokenization.

**Result**:

| id | paragraph | token | locations |
|----|-----------|-------|-----------|
| 1 | Programmers program... | programmers | 1 |
| 1 | Programmers program... | program | 2 |
| 1 | Programmers program... | with | 3 |
| 1 | Programmers program... | program | 4 |
| 1 | Programmers program... | as | 5 |
| 2 | The quick brown... | the | 0 |
| 2 | The quick brown... | quick | 1 |
| 2 | The quick brown... | brown | 2 |

## Common Use Cases

### 1. Text Preprocessing Pipeline

Complete text cleaning and normalization:

```sql
-- Create cleaned, stemmed tokens for ML
CREATE TABLE document_tokens AS (
    SELECT
        doc_id,
        token as stemmed_token,
        frequency
    FROM TD_TextParser (
        ON raw_documents AS InputTable
        ON standard_stopwords AS StopWordsTable DIMENSION
        USING
        TextColumn ('document_text')
        ConvertToLowerCase ('true')
        StemTokens ('true')
        RemoveStopWords ('true')
        DocIDColumn ('doc_id')
        TokenFrequency ('true')
        Accumulate ('doc_id', 'doc_category')
    ) AS dt
) WITH DATA;
```

### 2. Search Index Creation

Build inverted index for search functionality:

```sql
-- Create searchable token index with positions
CREATE TABLE search_index AS (
    SELECT
        token,
        doc_id,
        locations
    FROM TD_TextParser (
        ON documents AS InputTable
        USING
        TextColumn ('content')
        ConvertToLowerCase ('true')
        DocIDColumn ('doc_id')
        ListPositions ('true')
        Accumulate ('doc_id')
    ) AS dt
) WITH DATA;

-- Create index for fast lookup
CREATE INDEX idx_token ON search_index(token);
```

### 3. Word Frequency Analysis

Analyze most common words in corpus:

```sql
-- Find top 20 most frequent words
SELECT
    token,
    SUM(frequency) as total_frequency,
    COUNT(DISTINCT doc_id) as document_count
FROM TD_TextParser (
    ON corpus AS InputTable
    ON stopwords AS StopWordsTable DIMENSION
    USING
    TextColumn ('text')
    RemoveStopWords ('true')
    ConvertToLowerCase ('true')
    DocIDColumn ('doc_id')
    TokenFrequency ('true')
    Accumulate ('doc_id')
) AS dt
GROUP BY token
ORDER BY total_frequency DESC
LIMIT 20;
```

### 4. Document Comparison Preparation

Prepare documents for similarity analysis:

```sql
-- Generate token sets for each document
CREATE TABLE doc_token_sets AS (
    SELECT
        doc_id,
        tokens as token_list
    FROM TD_TextParser (
        ON documents AS InputTable
        ON stopwords AS StopWordsTable DIMENSION
        USING
        TextColumn ('content')
        StemTokens ('true')
        RemoveStopWords ('true')
        OutputByWord ('false')
        Accumulate ('doc_id')
    ) AS dt
) WITH DATA;

-- Use for Jaccard similarity or other metrics
```

## Best Practices

### 1. Choose Output Format Wisely

**OutputByWord('true')** for:
- Frequency analysis
- Position tracking
- Token-level operations
- Most ML preprocessing

**OutputByWord('false')** for:
- Compact storage
- Quick overview
- Simple bag-of-words representation

### 2. Stemming Considerations

```sql
-- Use stemming for:
-- - Search applications (better recall)
-- - Feature reduction
-- - Language modeling

StemTokens ('true')

-- Avoid stemming for:
-- - Exact matching requirements
-- - Sentiment analysis (meaning changes)
-- - Named entity recognition
```

### 3. Stop Word Management

```sql
-- Always use domain-appropriate stop words
-- Standard stop words for general text
ON standard_stopwords AS StopWordsTable DIMENSION

-- Custom stop words for domain-specific text
-- (e.g., legal, medical, technical documents)
```

### 4. Delimiter Selection

```sql
-- Simple case: use default or Delimiter
Delimiter(' ')

-- Complex case: use DelimiterRegex
DelimiterRegex('[ \\t\\n\\f\\r,;]+')

-- Never use both simultaneously
```

### 5. Position Tracking Setup

```sql
-- For position tracking, always specify:
DocIDColumn ('doc_id')          -- Required
ListPositions ('true')           -- Get positions
OutputByWord ('true')            -- Must be true
```

### 6. Performance Optimization

```sql
-- For large datasets:
-- 1. Filter input documents first
-- 2. Use simple delimiters when possible
-- 3. Limit Accumulate columns
-- 4. Consider OutputByWord('false') for storage

WHERE doc_date >= CURRENT_DATE - INTERVAL '30' DAY
```

## Related Functions

- **TD_TextMorph**: Lemmatization (more accurate than stemming)
- **TD_Ngramsplitter**: Generate n-grams from tokens
- **TD_TFIDF**: Calculate TF-IDF scores on parsed tokens
- **TD_SentimentExtractor**: Analyze sentiment of parsed text

## Notes and Limitations

### 1. Stemming Algorithm
- Uses **Porter stemming algorithm**
- May produce non-words (e.g., 'commun' from 'communicate')
- English-focused algorithm
- Consider TD_TextMorph for lemmatization instead

### 2. Locations Column Limit
- Locations column: **VARCHAR 64000** maximum
- Once limit reached, additional values ignored
- No error thrown when limit exceeded
- For very long documents, consider alternative approaches

### 3. Delimiter Constraints
- **Cannot use both** Delimiter and DelimiterRegex simultaneously
- If neither provided, default Delimiter value is used
- Empty tokens from DelimiterRegex are silently discarded

### 4. TokenColName Restrictions
When using ListPositions and TokenFrequency:
- Cannot have spaces
- No reserved SQL words
- No special characters requiring double quotations
- No numeric-only names
- No reserved keywords (e.g., 'Order', 'Select')

### 5. ConvertToLowerCase Behavior
- When StemTokens is 'true', function automatically converts to lowercase
- ConvertToLowerCase value is ignored when stemming
- Cannot stem without lowercasing

### 6. CLOB Support
- CLOB LATIN/UTF16 only supported on Block File System
- Not available for Object File System on primary cluster
- Use VARCHAR for broader compatibility

### 7. Stop Words Table
- Required when RemoveStopWords is 'true'
- Must use DIMENSION keyword
- Column must be named 'words'

### 8. Character Set Consistency
- Input table and StopWordsTable must have same character set
- Both LATIN and UNICODE supported
- Cannot mix character sets

### 9. TokenFrequency and ListPositions
Both require:
- DocIDColumn specified
- OutputByWord set to 'true'
- Proper document identifier column

### 10. Empty Token Handling
- With DelimiterRegex: Empty tokens silently discarded
- With standard Delimiter: Empty tokens may appear
- Punctuation removal occurs before tokenization

## Version Information

- **Function Version**: Based on Teradata Database Analytic Functions Version 17.20
- **Generated**: November 28, 2025
- **Stemming Algorithm**: Porter Stemmer
