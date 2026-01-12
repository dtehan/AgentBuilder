# TD_TextMorph

## Function Name
- **TD_TextMorph**: Generates morphs (standard form/dictionary form) of tokens using English lemmatization

## Description
The TD_TextMorph function generates morphs (standard form/Dictionary form) of the given tokens in the input dataset using lemmatization algorithm based on English Dictionary. You can specify part of speech (POS) to generate morphs of specified POS for the given input token. This function also supports single output such that if the input token has multiple morphs of different part of speech, it will generate only one output.

### Characteristics
- Lemmatization based on English dictionary
- Converts words to their base/root form
- Supports part-of-speech (POS) filtering
- Can return single or multiple morphs per word
- Handles nouns, verbs, adjectives, and adverbs
- English language support only

### What is Lemmatization?
Lemmatization is the process of reducing words to their base or dictionary form (called a lemma). Unlike stemming, which simply removes suffixes, lemmatization uses vocabulary and morphological analysis to return the actual root word.

**Examples**:
- "running" → "run" (verb)
- "better" → "good" (adjective) or "well" (adverb)
- "mice" → "mouse" (noun)

## When to Use TD_TextMorph

### Text Normalization
- Standardize words to their base forms before analysis
- Reduce vocabulary size for machine learning models
- Improve matching accuracy in search and retrieval

### Feature Engineering
- Create consistent features for NLP models
- Group related word forms together
- Reduce dimensionality in text analytics

### Information Retrieval
- Improve search recall by matching word variants
- Handle different tenses and forms in queries
- Build more effective search indexes

### Linguistic Analysis
- Study word usage patterns across forms
- Analyze language structure and grammar
- Prepare text for part-of-speech analysis

## Syntax

```sql
TD_TextMorph (
    ON { table | view | (query) } AS InputTable
    USING
    WordColumn ('word_column')
    [ POSTagColumn ('pos_tag_column') ]
    [ SingleOutput ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
    [ POS ({'noun'|'verb'|'adj'|'adv'}) ]
    [ Accumulate ({ 'accumulate_column' | 'accumulate_column_range' }[,...]) ]
)
```

**Note:** You can call this function from:
- The FROM clause of a SELECT statement
- As part of a CREATE TABLE statement
- As part of a CREATE VIEW statement

## Required Elements

### ON Clause
Accept the InputTable clause.

### WordColumn
**Required**: Specify the name of the input column that contains words for which morphs to be generated.
- **Constraint**: If WordColumn is not specified, an error is returned
- **Maximum**: 1 column is allowed
- **Character Set**: Supports only English language with LATIN or UNICODE characters input
- **Error**: Otherwise, an error is returned

## Optional Elements

### POSTagColumn
Specify the name of the input table column that contains the part of speech (POS) tags of the words.
- **Purpose**: If you specify this syntax element, the function outputs each morph according to its POS tag
- **Maximum**: 1 column is allowed
- **Character Set**: Supports only English language with LATIN or UNICODE characters input

### SingleOutput
Specify whether to output only one morph for each word.
- **Default**: 'true'
- **Values**:
  - **'true'**: Output only one morph per word (first based on POS precedence)
  - **'false'**: Output all possible morphs for each word

### POS
Specify the parts of speech to output.
- **Default**: All parts of speech
- **Values**: 'noun', 'verb', 'adj', 'adv'
- **Precedence Order**: 'noun', 'verb', 'adj', 'adv' (if SingleOutput is 'true')
- **Behavior**: Specification order is irrelevant; function uses precedence order
- **Note**: The function does not determine the part of speech of the word from its context; it uses all possible parts of speech for the word in the dictionary
- **Multiple Values**: Can specify multiple POS types

## Input Schema

### Input Table Schema

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| word_column | VARCHAR (LATIN or UNICODE) | The input tokens for which morphs to be generated |
| pos_tag_column | VARCHAR (LATIN or UNICODE) | The POS tag of word. This column in inputTable is required when POSTagColumn argument is passed |
| Accumulate | ANY | Column to copy to output table |

**Accumulate Limits**:
- Maximum **2043** names allowed (with POSTagColumn argument)
- Maximum **2044** names allowed (without POSTagColumn argument)

### POS Tag Reference

The following table summarizes the English POSTagger tags and their corresponding TextMorph parts of speech:

| Tag # | POSTagger Tag | Description | Examples | TextMorph POS |
|-------|---------------|-------------|----------|---------------|
| 1 | CC | Coordinating conjunction | and | |
| 2 | CD | Cardinal number | 1, third | |
| 3 | DT | Determiner | the | |
| 4 | EX | Existential there | there is | |
| 5 | FW | Foreign word | hors d'oeuvre | |
| 6 | IN | Preposition or coordinating conjunction | in, of, like | |
| 7 | JJ | Adjective | green | adj |
| 8 | JJR | Adjective, comparative | greener | adj |
| 9 | JJB | Adjective, superlative | greenest | adj |
| 10 | LS | List item marker | 1. | |
| 11 | MD | Modal | could, will | |
| 12 | NN | Noun, singular or mass | table | noun |
| 13 | NNS | Noun, plural | tables | noun |
| 14 | NNP | Noun, proper, singular | John | noun |
| 15 | NNPS | Noun, proper, plural | Vikings | noun |
| 16 | PDT | Predeterminer | both boys | |
| 17 | POS | Possessive | friend's | noun |
| 18 | PRP | Pronoun, personal | I, he, it | |
| 19 | PRPS | Pronoun, possessive | my, his | |
| 20 | RB | Adverb | however, usually, normally, here, good | adv |
| 21 | RBR | Adverb, comparative | better | adv |
| 22 | RBS | Adverb, superlative | best | adv |
| 23 | RP | Particle | give up | |
| 24 | SYM | Symbol | | |
| 25 | TO | to | to go, to him | |
| 26 | UH | Interjection | uh, huh, hmm | |
| 27 | VB | Verb, base form | take | verb |
| 28 | VBD | Verb, past tense | took | verb |
| 29 | VBG | Verb, gerund or present participle | taking | verb |
| 30 | VBN | Verb, past participle | taken | verb |
| 31 | VBP | Verb, non-third-person singular present | take | verb |
| 32 | VBZ | Verb, third-person singular present | takes | verb |
| 33 | WDT | Wh- determiner | which | |
| 34 | WP | Wh- pronoun | who, what | |
| 35 | WP | Wh- pronoun, possessive | whose | |
| 36 | WRB | Wh- adverb | where, when | |

## Output Schema

### Output Table Schema

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| Accumulate columns | ANY | Column copied from input to output |
| word_column | VARCHAR | Tokens/words for which morphs to be generated |
| TD_Morph | VARCHAR | Standard form or Dictionary form of the given tokens generated based on English Dictionary |
| POS | VARCHAR | A pos can be 'noun', 'verb', 'adj', or 'adv' |

## Code Examples

### Example Setup: Input Data

Create the input table with various word forms:

```sql
CREATE TABLE words_input (
    id INTEGER,
    word VARCHAR(10) CHARACTER SET LATIN NOT CASESPECIFIC
) PRIMARY INDEX (id);

INSERT INTO words_input VALUES(1, 'regression');
INSERT INTO words_input VALUES(2, 'Roger');
INSERT INTO words_input VALUES(3, 'better');
INSERT INTO words_input VALUES(4, 'datum');
INSERT INTO words_input VALUES(5, 'quickly');
INSERT INTO words_input VALUES(6, 'proud');
INSERT INTO words_input VALUES(7, 'father');
INSERT INTO words_input VALUES(8, 'juniors');
INSERT INTO words_input VALUES(9, 'doing');
INSERT INTO words_input VALUES(10, 'being');
INSERT INTO words_input VALUES(11, 'negating');
INSERT INTO words_input VALUES(12, 'yearly');
```

**Input Table**:

| id | word |
|----|------|
| 1 | regression |
| 2 | Roger |
| 3 | better |
| 4 | datum |
| 5 | quickly |
| 6 | proud |
| 7 | father |
| 8 | juniors |
| 9 | doing |
| 10 | being |
| 11 | negating |
| 12 | yearly |

### Example 1: SingleOutput Set to 'True'

Get only one morph per word (first by precedence):

```sql
SELECT * FROM TD_TextMorph(
    ON words_input AS inputtable
    USING
    WordColumn('word')
    SingleOutput('True')
    Accumulate('id')
) AS dt
ORDER BY 1, 2;
```

**Purpose**: Get the most common form of each word (precedence: noun > verb > adj > adv).

**Result**:

| id | word | TD_Morph | POS |
|----|------|----------|-----|
| 1 | regression | regression | NOUN |
| 2 | roger | Roger | NULL |
| 3 | better | better | NOUN |
| 4 | datum | datum | NOUN |
| 5 | quickly | quickly | ADV |
| 6 | proud | proud | ADJ |
| 7 | father | father | NOUN |
| 8 | juniors | junior | NOUN |
| 9 | doing | do | VERB |
| 10 | being | being | NOUN |
| 11 | negating | negate | VERB |
| 12 | yearly | yearly | NOUN |

### Example 2: SingleOutput Set to 'False'

Get all possible morphs for each word:

```sql
SELECT * FROM TD_TextMorph (
    ON words_input AS inputtable
    USING
    WordColumn('word')
    SingleOutput('false')
    Accumulate('id')
) AS dt
ORDER BY 1, 2;
```

**Purpose**: See all possible base forms and their parts of speech for each word.

**Result**:

| id | word | TD_Morph | POS |
|----|------|----------|-----|
| 1 | regression | regression | NOUN |
| 2 | Roger | Roger | NULL |
| 3 | better | better | VERB |
| 3 | better | well | ADV |
| 3 | better | good | ADJ |
| 3 | better | well | ADJ |
| 3 | better | better | NOUN |
| 4 | datum | datum | NOUN |
| 5 | quickly | quickly | ADV |
| 6 | proud | proud | ADJ |
| 7 | father | father | NOUN |
| 7 | father | father | VERB |
| 8 | juniors | junior | NOUN |
| 9 | doing | do | VERB |
| 10 | being | be | VERB |
| 10 | being | being | NOUN |
| 11 | negating | negate | VERB |
| 12 | yearly | yearly | ADV |
| 12 | yearly | yearly | ADJ |
| 12 | yearly | yearly | NOUN |

**Note**: "better" has 5 different morphs across different parts of speech.

### Example 3: POS Argument Specified with SingleOutput 'False'

Get morphs only for nouns and verbs:

```sql
SELECT * FROM TD_TextMorph (
    ON words_input AS inputtable
    USING
    WordColumn('word')
    SingleOutput('false')
    POS('noun', 'verb')
    Accumulate('id')
) AS dt
ORDER BY 1, 2;
```

**Purpose**: Filter morphs to specific parts of speech (useful for focused analysis).

**Result**:

| id | word | TD_Morph | POS |
|----|------|----------|-----|
| 1 | regression | regression | NOUN |
| 3 | better | better | VERB |
| 3 | better | better | NOUN |
| 4 | datum | datum | NOUN |
| 7 | father | father | NOUN |
| 7 | father | father | VERB |
| 8 | juniors | junior | NOUN |
| 9 | doing | do | VERB |
| 10 | being | be | VERB |
| 10 | being | being | NOUN |
| 11 | negating | negate | VERB |
| 12 | yearly | yearly | NOUN |

### Example 4: POS Argument Specified with SingleOutput 'True'

Get only one morph, preferring nouns and verbs:

```sql
SELECT * FROM TD_TextMorph (
    ON words_input AS inputtable
    USING
    WordColumn('word')
    SingleOutput('true')
    POS('noun', 'verb')
    Accumulate('id')
) AS dt
ORDER BY 1, 2;
```

**Purpose**: Get single morph with POS preference (noun first, then verb).

**Result**:

| id | word | TD_Morph | POS |
|----|------|----------|-----|
| 1 | regression | regression | NOUN |
| 3 | better | better | NOUN |
| 4 | datum | datum | NOUN |
| 7 | father | father | NOUN |
| 8 | juniors | junior | NOUN |
| 9 | doing | do | VERB |
| 10 | being | being | NOUN |
| 11 | negating | negate | VERB |
| 12 | yearly | yearly | NOUN |

**Note**: Words without noun/verb forms are excluded (e.g., "quickly", "proud").

### Example 5: Using POSTagColumn Argument

Lemmatize words based on their actual POS tags:

First, create input with POS tags:

```sql
CREATE TABLE pos_input (
    id INTEGER,
    word VARCHAR(50) CHARACTER SET LATIN,
    pos_tag VARCHAR(10) CHARACTER SET LATIN
);

INSERT INTO pos_input VALUES(1, 'roger', 'NN');
INSERT INTO pos_input VALUES(2, 'federer', 'NN');
INSERT INTO pos_input VALUES(3, 'born', 'VBN');
INSERT INTO pos_input VALUES(4, 'on', 'IN');
INSERT INTO pos_input VALUES(5, '8', 'CD');
INSERT INTO pos_input VALUES(6, 'august', 'NN');
INSERT INTO pos_input VALUES(7, '1981', 'CD');
INSERT INTO pos_input VALUES(11, 'greatest', 'JJS');
INSERT INTO pos_input VALUES(12, 'tennis', 'NN');
INSERT INTO pos_input VALUES(13, 'player', 'NN');
INSERT INTO pos_input VALUES(16, 'has', 'VBZ');
INSERT INTO pos_input VALUES(17, 'been', 'VBN');
INSERT INTO pos_input VALUES(18, 'continuously', 'RB');
INSERT INTO pos_input VALUES(19, 'ranked', 'VBN');
INSERT INTO pos_input VALUES(37, 'titles', 'NNS');
INSERT INTO pos_input VALUES(39, 'times', 'NNS');
```

Query with POS tags:

```sql
SELECT * FROM TD_TextMorph (
    ON pos_input AS inputTable
    USING
    WordColumn ('word')
    POSTagColumn ('pos_tag')
    Accumulate ('id', 'pos_tag')
) AS dt
ORDER BY id;
```

**Purpose**: Generate morphs based on known POS tags (more accurate than guessing).

**Sample Result**:

| id | pos_tag | word | TD_Morph | POS |
|----|---------|------|----------|-----|
| 1 | NN | roger | roger | NOUN |
| 2 | NN | federer | federer | NOUN |
| 3 | VBN | born | bear | VERB |
| 4 | IN | on | on | NULL |
| 5 | CD | 8 | 8 | NULL |
| 6 | NN | august | august | NOUN |
| 11 | JJS | greatest | great | ADJ |
| 12 | NN | tennis | tennis | NOUN |
| 13 | NN | player | player | NOUN |
| 16 | VBZ | has | have | VERB |
| 17 | VBN | been | be | VERB |
| 18 | RB | continuously | continuously | ADV |
| 19 | VBN | ranked | rank | VERB |
| 37 | NNS | titles | title | NOUN |
| 39 | NNS | times | time | NOUN |

## Common Use Cases

### 1. Text Preprocessing Pipeline

Lemmatize tokens before analysis:

```sql
-- Step 1: Tokenize text
CREATE TABLE tokenized_text AS (
    SELECT doc_id, CAST(token AS VARCHAR(50)) AS token
    FROM TD_TextParser(
        ON documents AS InputTable
        USING
        TextColumn('content')
        ConvertToLowerCase('true')
        Accumulate('doc_id')
    ) AS dt
) WITH DATA;

-- Step 2: Lemmatize tokens
CREATE TABLE lemmatized_text AS (
    SELECT doc_id, token, TD_Morph as lemma, POS
    FROM TD_TextMorph(
        ON tokenized_text AS InputTable
        USING
        WordColumn('token')
        SingleOutput('true')
        Accumulate('doc_id')
    ) AS dt
) WITH DATA;
```

### 2. Vocabulary Reduction for Machine Learning

Reduce feature space by grouping word forms:

```sql
-- Count lemmatized word frequencies
SELECT
    TD_Morph as base_word,
    POS,
    COUNT(DISTINCT token) as variant_count,
    COUNT(*) as total_occurrences
FROM TD_TextMorph(
    ON document_tokens AS InputTable
    USING
    WordColumn('token')
    SingleOutput('true')
    Accumulate('doc_id')
) AS dt
GROUP BY TD_Morph, POS
HAVING COUNT(DISTINCT token) > 1
ORDER BY variant_count DESC, total_occurrences DESC;
```

### 3. Search Query Expansion

Improve search by lemmatizing queries:

```sql
-- Lemmatize search terms
SELECT
    query_id,
    search_term,
    TD_Morph as base_term,
    POS
FROM TD_TextMorph(
    ON search_queries AS InputTable
    USING
    WordColumn('search_term')
    SingleOutput('false')
    Accumulate('query_id', 'user_id')
) AS dt;

-- Use base terms to match against lemmatized document index
```

### 4. Part-of-Speech Focused Analysis

Extract only verbs or nouns for specific analysis:

```sql
-- Extract only action words (verbs)
SELECT
    doc_id,
    token,
    TD_Morph as verb_lemma
FROM TD_TextMorph(
    ON document_tokens AS InputTable
    USING
    WordColumn('token')
    SingleOutput('true')
    POS('verb')
    Accumulate('doc_id')
) AS dt;

-- Use for action extraction, intent analysis, etc.
```

## Best Practices

### 1. Choose SingleOutput Based on Need

**Use SingleOutput('true') when**:
- You need one canonical form per word
- Working with feature vectors for ML
- Building search indexes
- Reducing dimensionality

**Use SingleOutput('false') when**:
- Exploring word meanings
- Need to preserve ambiguity
- Analyzing linguistic properties
- Building comprehensive dictionaries

### 2. Specify POS When Possible

```sql
-- Better: Use POSTagColumn if you have POS tags
POSTagColumn('pos_tag')

-- Good: Filter to relevant POS
POS('noun', 'verb')

-- Okay: Let function determine all POS
-- (no POS argument)
```

### 3. Combine with Text Parsing

Always tokenize before lemmatizing:

```sql
-- Good practice: Parse then lemmatize
TD_TextParser → TD_TextMorph

-- This ensures proper word boundaries
```

### 4. Handle NULL Results

Some words may not have morphs:

```sql
SELECT
    word,
    COALESCE(TD_Morph, word) as normalized_word,
    POS
FROM TD_TextMorph(...) AS dt;
```

### 5. Consider Context

TD_TextMorph doesn't use context, so:
- "run" (verb) and "run" (noun) both → "run"
- Use POSTagColumn with actual POS tags for accuracy
- Consider part-of-speech tagging before lemmatization

### 6. Character Set Consistency

```sql
-- Ensure consistent character sets
CREATE TABLE input_words (
    word VARCHAR(100) CHARACTER SET LATIN
);

-- NOT mixed:
-- word VARCHAR(100) CHARACTER SET UNICODE
```

## Related Functions

- **TD_TextParser**: Tokenize text into words before lemmatization
- **TD_Ngramsplitter**: Create n-grams from lemmatized text
- **TD_TFIDF**: Calculate TF-IDF on lemmatized tokens
- **TD_NERExtractor**: Extract entities from lemmatized text

## Notes and Limitations

### 1. Language Support
- **English only**: Only supports English language
- **Character sets**: LATIN or UNICODE for English characters
- No multilingual support

### 2. Context-Free Processing
- Function does not consider word context
- Cannot disambiguate based on sentence meaning
- Use POSTagColumn for accurate POS-based lemmatization

### 3. Word Column Constraints
- **Maximum 1 column** for WordColumn
- Must be VARCHAR type
- Error if multiple columns specified

### 4. Accumulate Limits
- Maximum **2044** columns (without POSTagColumn)
- Maximum **2043** columns (with POSTagColumn)
- Includes all accumulated columns

### 5. POS Precedence
When SingleOutput('true') and no POS filter:
1. NOUN (first priority)
2. VERB
3. ADJ
4. ADV (last priority)

### 6. NULL Results
- Words not in dictionary return NULL for TD_Morph
- Proper nouns often return NULL or original form
- Unknown words return NULL

### 7. No CLOB Support
- This function does not support CLOB data types
- Use VARCHAR for word column

### 8. POS Tag Requirements
- When using POSTagColumn, column must exist in input
- POS tags must follow standard Penn Treebank format
- Invalid tags may produce unexpected results

### 9. UTF8 Client Requirement
- Requires UTF8 client character set for UNICODE data
- Does not support Pass Through Characters (PTCs)
- Does not support KanjiSJIS or Graphic data types

## Version Information

- **Function Version**: Based on Teradata Database Analytic Functions Version 17.20
- **Generated**: November 28, 2025
- **Lemmatization**: Based on English Dictionary
