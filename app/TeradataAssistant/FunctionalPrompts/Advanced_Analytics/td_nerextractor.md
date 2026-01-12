# TD_NERExtractor

## Function Name
- **TD_NERExtractor**: Named Entity Recognition (NER) extractor that identifies and labels specific elements within text

## Description
The TD_NERExtractor function performs Named Entity Recognition (NER) on input text according to user-defined dictionary words or regular expression (regex) patterns.

TD_NERExtractor can be used to match and label specific elements within a given input text. The function identifies the contents of the text by matching extracts from the text to specific words (dictionary) or string patterns using regular expressions.

### Characteristics
- Supports dictionary-based entity recognition
- Supports regex pattern-based entity recognition
- Provides context around matched entities
- Returns entity positions within text
- Handles both UNICODE and LATIN character sets
- Supports custom entity type definitions

### Use Cases
- Extract names, locations, organizations from documents
- Identify email addresses, phone numbers, monetary values
- Find dates, times, and numerical patterns
- Custom entity extraction for domain-specific terms
- Information extraction from unstructured text

## When to Use TD_NERExtractor

Use TD_NERExtractor for extracting and categorizing specific information from text:

### Information Extraction
- Extract structured data from unstructured text
- Identify and classify named entities (people, places, organizations)
- Find specific patterns (emails, URLs, phone numbers)

### Data Enrichment
- Tag documents with entity metadata
- Build knowledge graphs from text
- Create searchable indexes of entity mentions

### Text Analytics Preprocessing
- Prepare text for downstream analysis
- Identify key entities for summarization
- Extract features for machine learning models

### Domain-Specific Applications
- Medical: Extract drug names, diseases, symptoms
- Financial: Identify monetary amounts, companies, dates
- Legal: Extract case numbers, parties, dates

## Syntax

```sql
TD_NERExtractor (
    ON { table | view | (query) } AS InputTable [ PARTITION BY ANY ]
    [ ON { table | view | (query) } AS Dict DIMENSION ]
    [ ON { table | view | (query) } AS Rules DIMENSION ]
    USING
    TextColumn ('text_column')
    [ InputLanguage ('en') ]
    [ ShowContext (context_num) ]
    [ Accumulate ({ 'accumulate_column' | accumulate_column_range }[,...]) ]
)
```

**USING Clause Limitation**: The maximum number of rules and dictionary words (rows) is allowed to be up to 90% of the available memory of the cluster in use. There is no fixed limit in the number of rows between the two of them.

**Note:** You can call this function from:
- The FROM clause of a SELECT statement
- As part of a CREATE TABLE statement
- As part of a CREATE VIEW statement

## Required Elements

### ON Clause (InputTable)
Accepts the InputTable clause.

The InputTable in TD_NERExtractor query supports PARTITION BY clause, so it can have:
- No partition at all
- PARTITION BY ANY
- PARTITION BY 'column name'

### TextColumn
**Required**: Specify the name of the input column containing text to analyze.
- **Constraint**: Maximum 1 text column is supported
- **Error**: If more than 1 text column is provided, an error is returned
- **Data Type**: VARCHAR

## Optional Elements

### ON Clause (Dict and Rules)
Accepts the Dict and Rules clauses for dictionary and regex pattern definitions.

**Important Table Aliasing**:
- The input text table should be aliased with **InputTable**
- The Rules table should be aliased with **Rules**
- The dictionary table should be aliased as **Dict**
- Rules and Dict table should be **DIMENSION**
- If aliases are not specified or incorrect, an error is returned

### InputLanguage
Specify the language of the input text.
- **Default**: 'en' (English)
- **Current Support**: English only

### ShowContext
Specify the number of "context" words before and after the entity found.
- **Format**: Integer value
- **Behavior**: In cases where the match is close to the beginning or end of the input text, leading or trailing '…' will be included
- **Purpose**: Provides surrounding text for understanding entity context

### Accumulate
Specifies the names of the input columns to copy to the output table.
- **Constraint**: CLOB and BLOB columns cannot be part of Accumulate columns

## Input Schema

**Note**: Both UNICODE and LATIN character set are allowed, however, all input tables must share the same character set. For example, if TextColumn is UNICODE, the contents of Dict and Rules table must also be UNICODE.

### InputTable Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| text_column | VARCHAR | Column contains input text |
| accumulate_column | ANY | Column to copy to output table (CLOB and BLOB not allowed) |

### Rules Table Schema

**Important**: Column names for Rules table must be **type_ner** and **regex**; otherwise, an error will be thrown.

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| type_ner | VARCHAR | Name of the entity (tag/label) |
| regex | VARCHAR | Regular Expression pattern of the entity |

**Regular Expression Notes**:
- No escape characters are needed for some special characters
- Example: To find '$' character, use '\$', not '\\$'
- The following characters need to be escaped with one backslash for literal match:
  - '\\' - Backslash
  - '^' - Caret
  - '$' - Dollar sign
  - '.' - Period or dot
  - '|' - Vertical bar or pipe
  - '?' - Question mark
  - '*' - Asterisk or star
  - '+' - Plus sign
  - '(' ')' - Opening and closing parenthesis
  - '[' ']' - Opening and closing square bracket
  - '{' '}' - Opening and closing curly brackets

### Dict Table Schema

**Important**: Column names for Dict table must be **type_ner** and **dict**; otherwise, an error will be thrown.

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| type_ner | VARCHAR | Name of the entity (tag/label) |
| dict | VARCHAR | Dictionary word to match |

## Output Schema

### Output Table Schema

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| Accumulate_columns | ANY | Columns copied from input to output |
| sn | INTEGER | Match number in a given row |
| entity | VARCHAR CHARACTER SET LATIN or UNICODE | Matched string for a given dictionary word or regex pattern. Column size is fixed to 1000 characters. Character set will be the same as input tables |
| type | VARCHAR CHARACTER SET LATIN or UNICODE | User-defined entity name (tag/label) for matched dictionary word or regex pattern. Column size will be the largest of type_ner columns from rules or dict table. Character set will be the same as input tables |
| start | INTEGER | Word number in row where the match starts |
| end | INTEGER | Word number in row where the match ends |
| context | VARCHAR CHARACTER SET LATIN or UNICODE | [Optional] Only appears when ShowContext > 0 is passed. Column size will be the same as TextColumn, up to 16000 characters, whichever is smaller. Character set will be the same as input tables |
| approach | VARCHAR CHARACTER SET LATIN or UNICODE | Category of matched string: 'RULE' for regex rules, or 'DICT' for dictionary word. Column size is 4 characters fixed. Character set will be the same as input tables |

## Code Examples

### Example Setup: Input Tables

Create the input text table:

```sql
DROP TABLE ner_input_eng;
CREATE MULTISET TABLE ner_input_eng(
    id INTEGER,
    txt VARCHAR(500) CHARACTER SET LATIN NOT CASESPECIFIC
);

INSERT INTO ner_input_eng VALUES
(1, 'At end of August, the Janus Unconstrained fund held only 45 debt issues with 70 percent of its assets in U.S. government debt.');

INSERT INTO ner_input_eng VALUES
(2, 'One Treasury issue due June 2016 alone was worth 43 percent of the fund''s total assets.');

INSERT INTO ner_input_eng VALUES
(3, 'Most of the bonds have short durations, with the average maturity of just over three years, indicating a generally defensive posture.');

INSERT INTO ner_input_eng VALUES
(4, 'For Bill Gross, quitting Pimco''s $222 billion Total Return Fund to take over a $13 million fund at Janus Capital is like resigning the U.S. presidency to become city manager of Ashtabula, Ohio, population 18,800.');

INSERT INTO ner_input_eng VALUES
(5, 'Gross stunned the investing world on Friday with his abrupt departure from Pimco, the $2 trillion asset manager he co-founded in 1971 and where he had run the Total Return Fund, the world''s biggest bond fund, for more than 27 years.');

INSERT INTO ner_input_eng VALUES
(6, '[0-9]+');
```

Create the Rules table:

```sql
DROP TABLE ner_rule;
CREATE MULTISET TABLE ner_rule(
    type_ner VARCHAR(500) CHARACTER SET LATIN NOT CASESPECIFIC,
    regex VARCHAR(500) CHARACTER SET LATIN NOT CASESPECIFIC
);

INSERT INTO ner_rule VALUES
('email', '[\w\-]([\.\w])+[\w]+@([\w\-]+\.)+[a-zA-Z]{2,4}');

INSERT INTO ner_rule VALUES
('Money', '\s\$[0-9]+\s');

INSERT INTO ner_rule VALUES
('Digits', '\s[0-9]+\s');

INSERT INTO ner_rule VALUES
('Name', '[A-Z][a-z]+\s+[A-Z][a-z]+');
```

Create the Dictionary table:

```sql
DROP TABLE ner_dict;
CREATE MULTISET TABLE ner_dict(
    type_ner VARCHAR(500) CHARACTER SET LATIN NOT CASESPECIFIC,
    dict VARCHAR(500) CHARACTER SET LATIN NOT CASESPECIFIC
);

INSERT INTO ner_dict VALUES('location', 'Arkansas');
INSERT INTO ner_dict VALUES('location', 'Dublin');
INSERT INTO ner_dict VALUES('MISC', ' average maturity');
INSERT INTO ner_dict VALUES('location', 'Ohio ');
INSERT INTO ner_dict VALUES('month', ' June ');
INSERT INTO ner_dict VALUES('Last Name', ' Gross');
INSERT INTO ner_dict VALUES('digit regex', '[0-9]+');
```

### Example 1: Complete NER with Context

Extract entities using both rules and dictionary with context:

```sql
SELECT id, entity, "type", "start", "end", context, approach
FROM TD_NERExtractor(
    ON ner_input_eng AS InputTable
    ON ner_rule AS rules DIMENSION
    ON ner_dict AS dict DIMENSION
    USING
    TextColumn('txt')
    InputLanguage('en')
    ShowContext(3)
    Accumulate('id')
) AS dt
ORDER BY id, "start";
```

**Result**: Extracts names, money amounts, digits, locations, and months with 3 words of context on each side.

**Sample Output**:

| id | entity | type | start | end | context | approach |
|----|--------|------|-------|-----|---------|----------|
| 1 | Janus Unconstrained | Name | 6 | 7 | of August, the Janus Unconstrained fund held only | RULE |
| 1 | 45 | Digits | 11 | 11 | fund held only 45 debt issues with | RULE |
| 1 | 70 | Digits | 15 | 15 | debt issues with 70 percent of its | RULE |
| 2 | One Treasury | Name | 1 | 2 | ... ... ... One Treasury issue due June | RULE |
| 2 | June | month | 5 | 5 | Treasury issue due June 2016 alone was | DICT |
| 2 | 2016 | Digits | 6 | 6 | issue due June 2016 alone was worth | RULE |
| 2 | 43 | Digits | 10 | 10 | alone was worth 43 percent of the | RULE |
| 4 | For Bill | Name | 1 | 2 | ... ... ... For Bill Gross, quitting Pimco's | RULE |
| 4 | Gross | Last Name | 3 | 3 | ... For Bill Gross, quitting Pimco's $222 | DICT |
| 4 | $222 | Money | 6 | 6 | Gross, quitting Pimco's $222 billion Total Return | RULE |
| 4 | Ohio | location | 33 | 33 | manager of Ashtabula, Ohio, population 18,800. ... | DICT |

### Example 2: Extract Only Names

Extract only person names from text:

```sql
SELECT id, entity, "type", "start", "end", approach
FROM TD_NERExtractor(
    ON ner_input_eng AS InputTable
    ON ner_rule AS rules DIMENSION
    USING
    TextColumn('txt')
    InputLanguage('en')
    Accumulate('id')
) AS dt
WHERE "type" = 'Name'
ORDER BY id, "start";
```

**Purpose**: Focus on person name extraction using regex patterns.

**Sample Output**:

| id | entity | type | start | end | approach |
|----|--------|------|-------|-----|----------|
| 1 | Janus Unconstrained | Name | 6 | 7 | RULE |
| 2 | One Treasury | Name | 1 | 2 | RULE |
| 4 | For Bill | Name | 1 | 2 | RULE |
| 4 | Total Return | Name | 8 | 9 | RULE |
| 4 | Janus Capital | Name | 19 | 20 | RULE |
| 5 | Total Return | Name | 29 | 30 | RULE |

### Example 3: Extract Financial Information

Extract money amounts and digits:

```sql
SELECT id, entity, "type", "start", "end"
FROM TD_NERExtractor(
    ON ner_input_eng AS InputTable
    ON ner_rule AS rules DIMENSION
    USING
    TextColumn('txt')
    InputLanguage('en')
    Accumulate('id')
) AS dt
WHERE "type" IN ('Money', 'Digits')
ORDER BY id, "start";
```

**Purpose**: Focus on numerical and financial information extraction.

**Sample Output**:

| id | entity | type | start | end |
|----|--------|------|-------|-----|
| 1 | 45 | Digits | 11 | 11 |
| 1 | 70 | Digits | 15 | 15 |
| 2 | 2016 | Digits | 6 | 6 |
| 2 | 43 | Digits | 10 | 10 |
| 4 | $222 | Money | 6 | 6 |
| 4 | $13 | Money | 15 | 15 |
| 5 | $2 | Money | 15 | 15 |
| 5 | 1971 | Digits | 22 | 22 |
| 5 | 27 | Digits | 40 | 40 |

### Example 4: Dictionary-Only Extraction

Use only dictionary-based matching:

```sql
SELECT id, entity, "type", "start", "end", approach
FROM TD_NERExtractor(
    ON ner_input_eng AS InputTable
    ON ner_dict AS dict DIMENSION
    USING
    TextColumn('txt')
    InputLanguage('en')
    Accumulate('id')
) AS dt
ORDER BY id, "start";
```

**Purpose**: Extract only entities defined in the dictionary (no regex patterns).

**Sample Output**:

| id | entity | type | start | end | approach |
|----|--------|------|-------|-----|----------|
| 2 | June | month | 5 | 5 | DICT |
| 3 | average maturity | MISC | 10 | 11 | DICT |
| 4 | Gross | Last Name | 3 | 3 | DICT |
| 4 | Ohio | location | 33 | 33 | DICT |
| 5 | Gross | Last Name | 1 | 1 | DICT |

### Example 5: Rules-Only Extraction

Use only regex pattern-based matching:

```sql
SELECT id, entity, "type", "start", "end", approach
FROM TD_NERExtractor(
    ON ner_input_eng AS InputTable
    ON ner_rule AS rules DIMENSION
    USING
    TextColumn('txt')
    InputLanguage('en')
    Accumulate('id')
) AS dt
ORDER BY id, "start";
```

**Purpose**: Extract entities using only regular expression patterns (no dictionary).

## Common Use Cases

### 1. Customer Data Extraction

Extract contact information from customer messages:

```sql
-- Create rules for email, phone, and address patterns
CREATE TABLE contact_rules AS (
    SELECT 'email' AS type_ner,
           '[\w\-\.]+@([\w\-]+\.)+[a-zA-Z]{2,4}' AS regex
    UNION ALL
    SELECT 'phone', '\d{3}[-\.]\d{3}[-\.]\d{4}'
    UNION ALL
    SELECT 'zipcode', '\b\d{5}(-\d{4})?\b'
);

-- Extract contact information
SELECT customer_id, entity, type
FROM TD_NERExtractor(
    ON customer_messages AS InputTable
    ON contact_rules AS rules DIMENSION
    USING
    TextColumn('message_text')
    Accumulate('customer_id')
) AS dt;
```

### 2. Medical Record Processing

Extract medical entities from clinical notes:

```sql
-- Dictionary of medical terms
CREATE TABLE medical_dict AS (
    SELECT 'medication' AS type_ner, 'aspirin' AS dict
    UNION ALL
    SELECT 'medication', 'metformin'
    UNION ALL
    SELECT 'condition', 'diabetes'
    UNION ALL
    SELECT 'condition', 'hypertension'
);

-- Extract medical entities
SELECT record_id, entity, type, context
FROM TD_NERExtractor(
    ON clinical_notes AS InputTable
    ON medical_dict AS dict DIMENSION
    USING
    TextColumn('notes')
    ShowContext(5)
    Accumulate('record_id', 'patient_id')
) AS dt;
```

### 3. Financial Document Analysis

Extract financial metrics from reports:

```sql
-- Rules for financial patterns
CREATE TABLE financial_rules AS (
    SELECT 'currency' AS type_ner, '\$[0-9,]+(\.[0-9]{2})?' AS regex
    UNION ALL
    SELECT 'percentage', '[0-9]+\.?[0-9]*%'
    UNION ALL
    SELECT 'date', '\d{1,2}/\d{1,2}/\d{4}'
);

-- Extract financial data
SELECT doc_id, entity, type, start, end
FROM TD_NERExtractor(
    ON financial_reports AS InputTable
    ON financial_rules AS rules DIMENSION
    USING
    TextColumn('report_text')
    Accumulate('doc_id', 'company')
) AS dt
ORDER BY doc_id, start;
```

### 4. Social Media Analysis

Extract hashtags, mentions, and URLs:

```sql
-- Social media patterns
CREATE TABLE social_rules AS (
    SELECT 'hashtag' AS type_ner, '#[A-Za-z0-9_]+' AS regex
    UNION ALL
    SELECT 'mention', '@[A-Za-z0-9_]+'
    UNION ALL
    SELECT 'url', 'https?://[^\s]+'
);

-- Extract social media entities
SELECT post_id, entity, type
FROM TD_NERExtractor(
    ON social_posts AS InputTable
    ON social_rules AS rules DIMENSION
    USING
    TextColumn('post_content')
    Accumulate('post_id', 'user_id', 'timestamp')
) AS dt;
```

## Best Practices

### 1. Table Aliasing
Always use correct aliases to avoid errors:
```sql
ON input_data AS InputTable    -- Correct
ON rules_table AS Rules DIMENSION  -- Correct
ON dict_table AS Dict DIMENSION    -- Correct
```

### 2. Character Set Consistency
Ensure all tables use the same character set:
```sql
-- All tables should be either LATIN or UNICODE
CREATE TABLE input_text (...) CHARACTER SET LATIN;
CREATE TABLE rules (...) CHARACTER SET LATIN;
CREATE TABLE dictionary (...) CHARACTER SET LATIN;
```

### 3. Regular Expression Testing
Test regex patterns separately before using in production:
```sql
-- Test regex pattern
SELECT id, txt
FROM test_data
WHERE REGEXP_SIMILAR(txt, '\$[0-9]+\s', 'i') = 1;
```

### 4. Context Window Sizing
Choose appropriate context size based on use case:
- Small (1-2 words): Quick validation
- Medium (3-5 words): General understanding
- Large (7-10 words): Detailed context

### 5. Performance Optimization
- Keep dictionary and rules tables reasonably sized (up to 90% of available memory)
- Use specific regex patterns to reduce false positives
- Filter results in subsequent queries rather than creating overly complex patterns

### 6. Entity Type Organization
Use meaningful and consistent entity type names:
```sql
-- Good practice
'person_name', 'company_name', 'location_city'

-- Avoid
'type1', 'entity', 'misc'
```

## Related Functions

- **TD_TextParser**: Tokenize text before entity extraction
- **TD_SentimentExtractor**: Extract sentiment from text
- **TD_Ngramsplitter**: Generate n-grams for pattern analysis
- **TD_TextMorph**: Lemmatize tokens for better matching

## Notes and Limitations

### 1. Language Support
- Currently supports English only (InputLanguage: 'en')
- Future versions may support additional languages

### 2. Character Set Requirements
- Both UNICODE and LATIN supported
- All input tables must share the same character set
- Mixed character sets will cause errors

### 3. Memory Constraints
- Maximum rules + dictionary rows: Up to 90% of available cluster memory
- No fixed limit between the two
- Monitor memory usage for large dictionaries

### 4. UTF8 Client Requirement
- This function requires the UTF8 client character set for UNICODE data
- Does not support Pass Through Characters (PTCs)
- Does not support KanjiSJIS or Graphic data types

### 5. Column Naming
- Rules table must have columns: **type_ner** and **regex**
- Dict table must have columns: **type_ner** and **dict**
- Incorrect column names will cause errors

### 6. Output Size Limits
- Entity column: Fixed to 1000 characters
- Context column: Up to 16000 characters (or TextColumn size, whichever is smaller)
- Type column: Size of largest type_ner from rules or dict tables

### 7. Regular Expression Escaping
Special characters requiring one backslash escape:
- \ ^ $ . | ? * + ( ) [ ] { }

### 8. Position Tracking
- Start and end positions are word-based, not character-based
- Position counting begins at the start of the text

## Version Information

- **Function Version**: Based on Teradata Database Analytic Functions Version 17.20
- **Generated**: November 28, 2025
