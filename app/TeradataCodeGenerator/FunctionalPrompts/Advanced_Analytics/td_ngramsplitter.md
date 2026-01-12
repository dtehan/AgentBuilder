# TD_Ngramsplitter

## Function Name
- **TD_Ngramsplitter**: Splits text into n-grams for natural language processing analysis

## Description
TD_Ngramsplitter considers each input row to be one document, and returns a row for each unique n-gram in each document. TD_Ngramsplitter also returns, for each document, the counts of each n-gram and the total number of n-grams.

TD_Ngramsplitter is an algorithm used in natural language processing to divide text into smaller units known as n-grams. An n-gram is a sequence of n items, such as words, letters or characters, taken from a given sample of text or speech. The TD_Ngramsplitter algorithm takes a string of text as input and returns a list of n-grams based on a specified value of n.

### Characteristics
- Creates n-grams of specified lengths from input text
- Returns frequency counts for each unique n-gram
- Supports overlapping and non-overlapping n-grams
- Handles punctuation removal and case conversion
- Supports sentence boundaries through reset characters
- Can output total n-gram counts per document

### Limitations
One potential limitation of the TD_Ngramsplitter algorithm is that it can produce a large number of n-grams, especially when n is large. This can result in a high-dimensional feature space that can negatively impact the performance of NLP models. To address this issue, various techniques have been developed to reduce the number of n-grams used in NLP tasks.

## When to Use TD_Ngramsplitter

TD_Ngramsplitter is a technique used in analytics to break down text data into smaller components called n-grams. An n-gram is a sequence of n words from a given text.

For example, a 2-gram (or bigram) of the sentence "The quick brown fox jumps over the lazy dog" would be "The quick", "quick brown", "brown fox", "fox jumps", "jumps over", "over the", "the lazy", and "lazy dog".

Use TD_Ngramsplitter in analytics for various purposes such as:

### Text Classification
By breaking down text into n-grams, you can create features that represent the context of the text, which can be used for text classification tasks such as:
- Sentiment analysis
- Spam detection
- Topic modeling

### Language Modeling
N-grams are used to build language models that predict the likelihood of a given sequence of words. For example, a trigram language model can predict the likelihood of the next word given the two previous words.

### Information Retrieval
N-grams are also used in information retrieval systems such as search engines to match queries with relevant documents. By breaking down documents into n-grams, you can efficiently index the documents and quickly retrieve relevant documents for a given query.

## Syntax

```sql
TD_Ngramsplitter (
    ON { table | view | (query) }
    USING
    TextColumn ('text_column')
    Grams ({ gram_number | 'value_range' }[,...])
    [ Delimiter ({'delimiter_character' | '[regex_string]'}) ]
    [ OverLapping ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
    [ ConvertToLowerCase ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
    [ Reset ({'reset_characters'| '[regex_string]'}) ]
    [ Punctuation ({'punctuation_characters' | '[regex_string]'}) ]
    [ OutputTotalGramCount ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
    [ TotalCountColName ('total_count_column') ]
    [ Accumulate ({ 'accumulate_column' | accumulate_column_range }[,...]) ]
    [ NGramColName ('ngram_column') ]
    [ GramLengthColName ('gram_length_column') ]
    [ FrequencyColName ('frequency_column') ]
)
```

**Note:** You can call this function from:
- The FROM clause of a SELECT statement
- As part of a CREATE TABLE statement
- As part of a CREATE VIEW statement

## Required Elements

### ON Clause
Accepts the InputTable clause. TD_Ngramsplitter takes one input table that contains the documents for which n-grams have to be generated.

### TextColumn
**Required**: Specify the name of the column that contains the input text.
- **Data Type**: VARCHAR or CLOB
- **Constraint**: This column must have a SQL string data type

### Grams
**Required**: Specify the length, in words, of each n-gram (that is, the value of n).
- **Format**: Single value (e.g., '3') or range (e.g., '2-4')
- **Range Format**: integer1-integer2, where integer1 ≤ integer2
- **Constraint**: Values must be positive integers
- **Multiple Values**: Specify multiple values or ranges separated by commas

## Optional Elements

### Delimiter
Specify, with a regular expression, the character or string that separates words in the input text.
- **Default**: ' ' (space)
- **Format**: Single character or regex pattern
- **Examples**:
  - ' ' (space)
  - '\t' (tab)
  - '[\\s,;]' (whitespace, comma, or semicolon)

### OverLapping
Specify whether the function allows overlapping n-grams.
- **Default**: 'true'
- **Values**:
  - 'true': Each word in each sentence starts an n-gram, if enough words follow it in the same sentence to form a whole n-gram of the specified size
  - 'false': N-grams do not overlap

### ConvertToLowerCase
Specify whether the function converts all letters in the input text to lowercase.
- **Default**: 'true'
- **Values**: 'true' or 'false'
- **Purpose**: Ensures case-insensitive n-gram matching

### Reset
Specify, with a regular expression, the character or string that ends a sentence.
- **Default**: '.,?!'
- **Format**: String or regex pattern
- **Purpose**: For information on sentences, see the Reset syntax element description
- **Note**: N-grams do not span sentence boundaries

### Punctuation
Specify, with a regular expression, the punctuation characters for the function to remove before evaluating the input text.
- **Default**: '\`~#^&*()-'
- **Format**: String or regex pattern
- **Character Sets**: Punctuation characters can be from both Unicode and Latin character sets

### OutputTotalGramCount
Specify whether the function returns the total number of n-grams in the document (that is, in the row) for each length n specified in the Grams syntax element.
- **Default**: 'false'
- **Values**: 'true' or 'false'
- **Note**: If you specify 'true', the TotalCountColName syntax element determines the name of the output table column that contains these totals
- **Important**: The total number of n-grams is not necessarily the number of unique n-grams

### TotalCountColName
Specify the name of the output table column that appears if the value of the OutputTotalGramCount syntax element is 'true'.
- **Default**: 'totalcnt'
- **Data Type**: INTEGER

### Accumulate
Specify the names of the input table columns to copy to the output table for each n-gram.
- **Default**: All input columns for each n-gram
- **Constraint**: These columns cannot have the same names as those specified by the syntax elements NGramColName, GramLengthColName, and TotalCountColName

### NGramColName
Specify the name of the output table column that is to contain the created n-grams.
- **Default**: 'ngram'
- **Data Type**: VARCHAR

### GramLengthColName
Specify the name of the output table column that is to contain the length of n-gram (in words).
- **Default**: 'n'
- **Data Type**: INTEGER

### FrequencyColName
Specify the name of the output table column that is to contain the count of each unique n-gram (that is, the number of times that each unique n-gram appears in the document).
- **Default**: 'frequency'
- **Data Type**: INTEGER

## Input Schema

### Input Table Schema
The input table has a row for each document to tokenize.

| Column | Data Type | Description |
|--------|-----------|-------------|
| text_column | VARCHAR or CLOB | Document to tokenize |
| accumulate_columns | ANY | Columns to copy to output table |

## Output Schema

### Output Table Schema
The output table has a row for each unique n-gram in each input document.

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| totalcnt | INTEGER | Total number of n-grams in the document. This column appears only if OutputTotalGramCount is 'true' |
| Accumulate_columns | ANY | Columns copied from input table |
| ngram | VARCHAR | Generated n-grams |
| n | INTEGER | Length of n-gram in words (value n) |
| frequency | INTEGER | Count of each unique n-gram in the document |

## Code Examples

### Example Input Data

Create sample input table:

```sql
CREATE TABLE paragraphs_input (
    paraid INTEGER,
    paratopic VARCHAR(100),
    paratext VARCHAR(5000)
);

INSERT INTO paragraphs_input VALUES
(1, 'Decision Trees',
 'Decision tree learning uses a decision tree as a predictive model which maps observations about an item to conclusions about the items target value. It is one of the predictive modeling approaches used in statistics, data mining, and machine learning. Tree models where the target variable can take a finite set of values are called classification trees. In these tree structures, leaves represent class labels and branches represent conjunctions of features that lead to those class labels. Decision trees where the target variable can take continuous values (typically real numbers) are called regression trees.');

INSERT INTO paragraphs_input VALUES
(2, 'Simple Regression',
 'In statistics, simple linear regression is the least squares estimator of a linear regression model with a single explanatory variable. In other words, simple linear regression fits a straight line through the set of n points in such a way that makes the sum of squared residuals of the model (that is, vertical distances between the points of the data set and the fitted line) as small as possible.');
```

### Example 1: Basic N-Gram Generation (Omit Accumulate)

Generate 4-6 grams with total count output:

```sql
SELECT * FROM TD_Ngramsplitter (
    ON paragraphs_input
    USING
    TextColumn ('paratext')
    Grams ('4-6')
    OutputTotalGramCount ('true')
) AS dt;
```

**Result**: Returns n-grams of length 4, 5, and 6 with their frequencies and total counts for each document.

### Example 2: N-Gram Generation with Accumulate

Generate 4-6 grams while preserving document metadata:

```sql
SELECT * FROM TD_Ngramsplitter (
    ON paragraphs_input
    USING
    TextColumn ('paratext')
    Grams ('4-6')
    OutputTotalGramCount ('true')
    Accumulate ('[0:1]')
) AS dt;
```

**Result**: Returns n-grams with document ID and topic information preserved.

| paraid | paratopic | paratext | ngram | n | frequency | totalcnt |
|--------|-----------|----------|-------|---|-----------|----------|
| 1 | Decision Trees | Decision tree lear... | a decision tree as | 4 | 1 | 73 |
| 2 | Simple Regression | In statistics, simp... | a linear regression model | 4 | 1 | 55 |
| 1 | Decision Trees | Decision tree lear... | a decision tree as | 5 | 1 | 66 |

### Example 3: Using Regular Expression with Punctuation (Range A-Z and a-z)

Remove all non-alphabetic characters:

```sql
SELECT * FROM TD_Ngramsplitter (
    ON text_data
    USING
    TextColumn ('text_data')
    Grams ('4-6')
    Punctuation('[^A-Za-z]')
    OutputTotalGramCount ('true')
) AS dt;
```

**Purpose**: This removes all characters except A-Z and a-z, useful for cleaning text with numbers and special characters.

**Sample Output**:

| id | text_data | city | ngram | n | frequency | totalcnt |
|----|-----------|------|-------|---|-----------|----------|
| 5 | Quetta, the fruit... | Quetta | is admired for its | 4 | 1 | 8 |
| 7 | Karachi$$ - The... | Karachi | karachi the city of | 4 | 1 | 3 |
| 6 | Islamabad! 123... | Islamabad | a city with greenery | 4 | 1 | 7 |

### Example 4: Remove All Punctuation Marks

Remove all punctuation using POSIX character class:

```sql
SELECT * FROM TD_Ngramsplitter (
    ON text_data
    USING
    TextColumn ('text_data')
    Grams ('4-6')
    Punctuation('[[:punct:]]')
    OutputTotalGramCount ('true')
) AS dt;
```

**Purpose**: Removes all punctuation marks while keeping numbers and letters.

**Sample Output**:

| id | text_data | city | ngram | n | frequency | totalcnt |
|----|-----------|------|-------|---|-----------|----------|
| 5 | Quetta, the fruit... | Quetta | is admired for its | 4 | 1 | 8 |
| 9 | Peshawar&&& - Home... | Peshawar | peshawar home to 1 | 4 | 1 | 3 |
| 7 | Karachi$$ - The... | Karachi | the city of 5 | 4 | 1 | 5 |

### Example 5: Remove Punctuation and Reset at Punctuation

Treat punctuation as sentence boundaries:

```sql
SELECT * FROM TD_Ngramsplitter (
    ON text_data
    USING
    TextColumn ('text_data')
    Grams ('4-6')
    Punctuation('[[:punct:]]')
    Reset('[[:punct:]]')
    OutputTotalGramCount ('true')
) AS dt;
```

**Purpose**: Removes punctuation and prevents n-grams from spanning across punctuation marks (sentence boundaries).

**Sample Output**:

| id | text_data | city | ngram | n | frequency | totalcnt |
|----|-----------|------|-------|---|-----------|----------|
| 5 | Quetta, the fruit... | Quetta | is admired for its | 4 | 1 | 8 |
| 7 | Karachi$$ - The... | Karachi | the city of 5 | 4 | 1 | 3 |
| 6 | Islamabad! 123... | Islamabad | a city with 20 | 4 | 1 | 1 |

### Example 6: Using Delimiter with Punctuation

Use punctuation as delimiter:

```sql
SELECT * FROM TD_Ngramsplitter (
    ON text_data
    USING
    TextColumn ('text_data')
    Grams ('1-2')
    Punctuation('[[:punct:]]')
    Delimiter('[;,]')
    OutputTotalGramCount ('true')
) AS dt;
```

**Purpose**: Uses semicolons and commas as word delimiters while removing other punctuation.

**Sample Output**:

| id | text_data | city | ngram | n | frequency | totalcnt |
|----|-----------|------|-------|---|-----------|----------|
| 5 | Quetta, the fruit... | Quetta | quetta | 1 | 1 | 3 |
| 9 | Peshawar&&& - Home... | Peshawar | peshawar home to 1 | 1 | 1 | 2 |
| 7 | Karachi$$ - The... | Karachi | vibrant | 1 | 1 | 2 |

### Example 7: Processing Unicode Data with Punctuation Removal

Handle multilingual text (Unicode support):

```sql
SELECT * FROM TD_Ngramsplitter (
    ON input_data
    USING
    TextColumn ('content')
    Grams ('4-6')
    Punctuation('[[:punct:]]')
    OutputTotalGramCount ('true')
    Accumulate('docid')
) AS dt;
```

**Purpose**: Process Unicode text (Telugu, Hindi, Japanese, etc.) while removing punctuation marks from various character sets.

**Sample Output** (showing Telugu text processing):

| docid | ngram | n | frequency | totalcnt |
|-------|-------|---|-----------|----------|
| 1 | इस पर भल अभल | 4 | 1 | 192 |
| 1 | किा दक वि इस | 4 | 1 | 192 |
| 1 | की पलठ ने की | 4 | 1 | 192 |
| 1 | ఈ నెల 19 చివరి | 4 | 1 | 192 |

## Common Use Cases

### 1. Text Feature Engineering
Extract n-grams as features for machine learning models:

```sql
-- Extract bigrams and trigrams for text classification
SELECT paraid, ngram, frequency
FROM TD_Ngramsplitter (
    ON documents
    USING
    TextColumn ('content')
    Grams ('2-3')
    ConvertToLowerCase ('true')
    Accumulate ('paraid')
) AS dt
WHERE frequency >= 2;  -- Filter for meaningful patterns
```

### 2. Language Pattern Analysis
Identify common phrases in customer feedback:

```sql
-- Find most common 3-word phrases
SELECT ngram, SUM(frequency) as total_occurrences
FROM TD_Ngramsplitter (
    ON customer_reviews
    USING
    TextColumn ('review_text')
    Grams ('3')
    ConvertToLowerCase ('true')
) AS dt
GROUP BY ngram
ORDER BY total_occurrences DESC
LIMIT 20;
```

### 3. Document Similarity Preprocessing
Prepare text for cosine similarity calculations:

```sql
-- Generate n-gram vectors for each document
SELECT doc_id, ngram, frequency
FROM TD_Ngramsplitter (
    ON corpus
    USING
    TextColumn ('document_text')
    Grams ('2-4')
    ConvertToLowerCase ('true')
    Accumulate ('doc_id')
) AS dt;
```

## Best Practices

1. **Choose Appropriate N-Gram Size**:
   - Unigrams (n=1): Individual words, good for basic analysis
   - Bigrams (n=2): Two-word phrases, capture basic context
   - Trigrams (n=3): Three-word phrases, capture more context
   - Higher values: More specific but sparse

2. **Handle Overlapping**:
   - Use OverLapping('true') for comprehensive analysis
   - Use OverLapping('false') for distinct phrase extraction

3. **Clean Your Text**:
   - Use ConvertToLowerCase for case-insensitive matching
   - Configure Punctuation to remove noise
   - Use Reset to respect sentence boundaries

4. **Regular Expression Tips**:
   - Use '[[:punct:]]' to remove all punctuation
   - Use '[^A-Za-z]' to keep only alphabetic characters
   - Use '[\s,;]' for custom delimiters

5. **Performance Optimization**:
   - Start with smaller n-gram ranges (2-3) before expanding
   - Use Accumulate selectively to reduce output size
   - Filter low-frequency n-grams in subsequent queries

6. **Unicode Considerations**:
   - Ensure consistent character set across all input data
   - Use appropriate regex patterns for different languages
   - Test with sample data before processing large datasets

## Related Functions

- **TD_TextParser**: Tokenize text into individual words
- **TD_TFIDF**: Calculate term frequency-inverse document frequency
- **TD_WordEmbeddings**: Generate word embeddings for semantic analysis
- **TD_NERExtractor**: Extract named entities from text

## Notes and Limitations

1. **Memory Constraints**:
   - Large n-gram values can generate many combinations
   - May result in high-dimensional feature space
   - Consider filtering or dimensionality reduction techniques

2. **Character Sets**:
   - Both UNICODE and LATIN character sets supported
   - All input tables must share the same character set
   - Mixed character sets will result in errors

3. **Regular Expression Escaping**:
   - Some special characters need one backslash for literal match: \ ^ $ . | ? * + ( ) [ ] { }
   - No escape characters needed for some special characters in string format

4. **Sentence Boundaries**:
   - N-grams do not span across reset characters
   - Default reset characters: '.,?!'
   - Configure appropriately based on your text format

5. **Output Volume**:
   - Output size can be substantial for large documents
   - Use OutputTotalGramCount judiciously
   - Consider aggregating results in subsequent queries

## Version Information

- **Function Version**: Based on Teradata Database Analytic Functions Version 17.20
- **Generated**: November 22, 2025
