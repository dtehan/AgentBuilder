# TD_SentimentExtractor

## Function Name
- **TD_SentimentExtractor**: Extracts sentiment (positive, negative, or neutral) from text using dictionary-based analysis

## Description
TD_SentimentExtractor uses a dictionary model to extract the sentiment (positive, negative, or neutral) of each input document or sentence.

The dictionary model consists of WordNet, a lexical database of the English language, and negation words such as no, not, neither, never, and so on.

The function handles negated sentiments as follows:
- **-1** if the sentiment is negated. For example, "I am not happy."
- **-1** if one word separates the sentiment and a negation word. For example, "I am not very happy."
- **+1** if two or more words separate the sentiment and a negation word. For example, "I am not saying I am happy."

### Characteristics
- Dictionary-based sentiment analysis using WordNet
- Document-level or sentence-level analysis
- Handles negation patterns intelligently
- Supports custom sentiment dictionaries
- Provides sentiment scores and detailed word analysis
- English language support only

### Dictionary Flexibility
- Can use default sentiment dictionary (built-in)
- Can provide custom dictionary through CustomDictionaryTable
- Can add additional entries through AdditionalDictionaryTable
- Can output the dictionary used through OutputDictionaryTable

## When to Use TD_SentimentExtractor

### Customer Feedback Analysis
- Analyze product reviews for positive/negative sentiment
- Monitor customer service interactions
- Track brand perception across social media

### Market Research
- Understand consumer opinions about products or services
- Analyze survey responses and open-ended feedback
- Track sentiment trends over time

### Content Moderation
- Identify negative or toxic content
- Flag concerning messages for review
- Prioritize responses based on sentiment

### Business Intelligence
- Monitor employee feedback and satisfaction
- Analyze stakeholder communications
- Track public sentiment about company initiatives

## Syntax

```sql
TD_SentimentExtractor (
    ON { table | view | (query) } AS InputTable PARTITION BY ANY
    [ ON { table | view | (query) } AS CustomDictionaryTable DIMENSION ]
    [ ON { table | view | (query) } AS AdditionalDictionaryTable DIMENSION ]
    [ OUT PERMANENT TABLE OutputDictionaryTable (output_table_name) ]
    USING
    TextColumn ('text_column')
    [ Accumulate ({ 'accumulate_column' | accumulate_column_range }[,...]) ]
    [ AnalysisType ({ 'DOCUMENT' | 'SENTENCE' }) ]
    [ Priority ({ 'NONE' | 'NEGATIVE_RECALL' | 'NEGATIVE_PRECISION' |
                 'POSITIVE_RECALL' | 'POSITIVE_PRECISION'}) ]
    [ OutputType ({ 'ALL' | 'POS' | 'NEG' | 'NEU' }) ]
)
```

**Note:** You can call this function from:
- The FROM clause of a SELECT statement
- As part of a CREATE TABLE statement
- As part of a CREATE VIEW statement

## Required Elements

### ON Clause (InputTable)
Accepts the InputTable clause with PARTITION BY ANY.

### TextColumn
**Required**: Specifies the input column name that contains text for sentiment analysis.
- **Data Type**: CHAR, VARCHAR, or CLOB
- **Constraint**: Must contain text data suitable for sentiment analysis

## Optional Elements

### ON Clause (Dictionaries)
Accepts the CustomDictionaryTable, AdditionalDictionaryTable, and OutputDictionaryTable clauses.

**Dictionary Usage Options**:
1. **Default Dictionary**: Omit all dictionary ON clauses to use built-in WordNet dictionary
2. **Custom Dictionary**: Provide CustomDictionaryTable to replace default dictionary
3. **Additional Entries**: Provide AdditionalDictionaryTable to add to either default or custom dictionary
4. **Output Dictionary**: Use OutputDictionaryTable OUT clause to view dictionary contents used

### Accumulate
Specifies the input table column names to copy to the output table.
- **Purpose**: Preserve document identifiers and metadata in results

### AnalysisType
Specifies the analysis level to analyze each document or sentence.
- **Default**: 'DOCUMENT'
- **Values**:
  - **'DOCUMENT'**: Analyze entire document as one unit
  - **'SENTENCE'**: Analyze each sentence separately

### Priority
Specifies priority for sentiment classification results.
- **Default**: 'NONE'
- **Values**:
  - **'NONE'**: Provide all results the same priority (default behavior)
  - **'NEGATIVE_RECALL'**: Maximize negative results, including lower-confidence classifications
  - **'NEGATIVE_PRECISION'**: Only high-confidence negative classifications
  - **'POSITIVE_RECALL'**: Maximize positive results, including lower-confidence classifications
  - **'POSITIVE_PRECISION'**: Only high-confidence positive classifications

### OutputType
Specifies which sentiment types to return in results.
- **Default**: 'ALL'
- **Values**:
  - **'ALL'**: Returns all results (positive, negative, and neutral)
  - **'POS'**: Returns only results with positive sentiments
  - **'NEG'**: Returns only results with negative sentiments
  - **'NEU'**: Returns only results with neutral sentiments

## Input Schema

### Input Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| text_column | CHAR, VARCHAR, CLOB | The InputTable column name that contains text for sentiment analysis |
| accumulate_column | ANY | The InputTable column names to copy to the output table |

### Custom/Additional Dictionary Table Schema

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| sentiment_word | CHAR, VARCHAR | The column name that contains the sentiment word |
| polarity_strength | BYTEINT, SMALLINT, INTEGER | The column name that contains the strength of the sentiment word |

**Polarity Strength Values**:
- Positive numbers: Positive sentiment (1 = positive, 2 = very positive)
- Negative numbers: Negative sentiment (-1 = negative, -2 = very negative)
- Zero: Neutral

## Output Schema

### Output Table Schema

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| AccumulateColumns | ANY | The specified InputTable column names copied to the output table |
| content | VARCHAR | The column contains the sentence extracted from the document. The column displays if you use SENTENCE as the AnalysisType |
| polarity | VARCHAR | The sentiment value of the result. Values are POS (positive), NEG (negative), or NEU (neutral) |
| sentiment_score | INTEGER | The sentiment score of polarity. Values are 0 (neutral), 1 (higher than neutral), or 2 (higher than 1) |
| sentiment_words | VARCHAR | The string that contains a total positive score, total negative score, and sentiment words with their polarity_strength and frequency enclosed in parenthesis |

### Output Dictionary Table Schema

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| sentiment_word | VARCHAR | The column that contains the sentiment word |
| polarity_strength | INTEGER | The column that contains the strength of the sentiment word |

## Code Examples

### Example Setup: Input Tables

Create the input table with product reviews:

```sql
CREATE TABLE sentiment_extract_input (
    id INTEGER,
    product VARCHAR(50),
    category VARCHAR(10),
    review VARCHAR(5000)
);

-- Positive reviews
INSERT INTO sentiment_extract_input VALUES
(1, 'camera', 'POS',
 'we primarily bought this camera for high image quality and excellent video capability without paying the price for a dslr. it has excelled in what we expected of it, and consequently represented excellent value for me. all my friends want my camera for their vacations. i would recommend this camera to anybody. definitely worth the price. plus, when you buy some accessories, it becomes even more powerful');

INSERT INTO sentiment_extract_input VALUES
(2, 'office suite', 'POS',
 'compatibility. it is a very intuitive suite and the drag and drop functionality is terrific. it is the best office suite i have used to date. it is launched before office 2010 and it is ages ahead of it already. the fact that i could comfortable import xls, doc, ppt and modify them, and then export them back to the doc, xls, ppt is terrific. i needed the');

-- Negative reviews
INSERT INTO sentiment_extract_input VALUES
(8, 'camera', 'NEG',
 'i hate my camera, and im stuck with it. this camera sucks so bad, even the dealers on ebay have difficulty selling it. horrible indoors, does not capture fast action, screwy software, no suprise, and screwy audio/video codec that does not work with hardly any app');

INSERT INTO sentiment_extract_input VALUES
(9, 'television', 'NEG',
 'this is a known issue. $3k is way too much money to drop onto a piece of crap. poor customer support. after about 1 and a half years and hardly using the tv, a big yellow pixilated stain appeared. product is very inferior and subject to several lawsuits. i expressed my dissatifaction with the situation as');
```

Create custom sentiment dictionary:

```sql
CREATE TABLE sentiment_word (
    sentiment_word VARCHAR(50),
    polarity_strength INTEGER
);

INSERT INTO sentiment_word VALUES
('big', 0),
('constant', 0),
('crap', -2),
('difficulty', -1),
('disappointed', -1),
('excellent', 2),
('fun', 1),
('incredible', 2),
('love', 1),
('mistake', -1),
('nice', 1),
('not tolerate', -1),
('outstanding', 2),
('screwed', 2),
('small', 0),
('stuck', -1),
('terrific', 2),
('terrible', -2),
('update', 0);
```

Create additional sentiment words:

```sql
CREATE TABLE sentiment_word_add (
    sentiment_word VARCHAR(50),
    polarity_strength INTEGER
);

INSERT INTO sentiment_word_add VALUES
('love', 2),  -- Override default 'love' with stronger positive
('need for repair', -2),
('repair', -1);
```

### Example 1: Document-Level Analysis with Default Dictionary

Analyze sentiment at the document level using built-in dictionary:

```sql
SELECT * FROM TD_SentimentExtractor (
    ON sentiment_extract_input AS InputTable PARTITION BY ANY
    USING
    TextColumn ('review')
    Accumulate ('id', 'product')
    AnalysisType ('DOCUMENT')
) AS dt
ORDER BY id;
```

**Purpose**: Get overall sentiment for each complete review using default WordNet dictionary.

**Sample Output**:

| id | product | polarity | sentiment_score | sentiment_words |
|----|---------|----------|-----------------|-----------------|
| 1 | camera | POS | 2 | In total, positive score:7 negative score:0. excelled 1 (1), excellent 1 (2), powerful 1 (1), worth 1 (1), recommend 1 (1), capability 1 (1) |
| 2 | office suite | POS | 2 | In total, positive score:5 negative score:-1. drag -1 (1), intuitive 1 (1), best 1 (1), comfortable 1 (1), terrific 1 (2) |
| 8 | camera | NEG | 2 | In total, positive score:0 negative score:-10. stuck -1 (1), sucks -1 (1), screwy -1 (2), not fast -1 (1), bad -1 (1), difficulty -1 (1), horrible -1 (1), not work -1 (1), hate -1 (1) |
| 9 | television | NEG | 2 | In total, positive score:1 negative score:-5. crap -1 (1), issue -1 (1), stain -1 (1), inferior -1 (1), poor -1 (1), support 1 (1) |

### Example 2: Sentence-Level Analysis with Custom Dictionary

Analyze sentiment at the sentence level using custom dictionary:

```sql
SELECT * FROM TD_SentimentExtractor (
    ON sentiment_extract_input AS InputTable PARTITION BY ANY
    ON sentiment_word AS CustomDictionaryTable DIMENSION
    USING
    TextColumn ('review')
    Accumulate ('id', 'product')
    AnalysisType ('SENTENCE')
) AS dt
ORDER BY id;
```

**Purpose**: Get sentiment for each individual sentence using custom sentiment dictionary.

**Sample Output**:

| id | product | content | polarity | sentiment_score | sentiment_words |
|----|---------|---------|----------|-----------------|-----------------|
| 1 | camera | we primarily bought this camera for high image quality and excellent video capability without paying the price for a dslr .it has excelled in what we expected of it, and consequently represented excellent value for me .all my friends want my camera for their vacations . | POS | 2 | In total, positive score:4 negative score:0. excellent 2 (2) |
| 1 | camera | i would recommend this camera to anybody .definitely worth the price .plus, when you buy some accessories, it becomes even more powerful | NEU | 0 | |
| 8 | camera | this camera sucks so bad, even the dealers on ebay have difficulty selling it. | NEG | 2 | In total, positive score:0 negative score:-1. difficulty -1 (1) |
| 8 | camera | i hate my camera, and im stuck with it . | NEG | 2 | In total, positive score:0 negative score:-1. stuck -1 (1) |

### Example 3: Using Additional Dictionary with Default

Add custom words to the default dictionary:

```sql
SELECT * FROM TD_SentimentExtractor (
    ON sentiment_extract_input AS InputTable PARTITION BY ANY
    ON sentiment_word_add AS AdditionalDictionaryTable DIMENSION
    USING
    TextColumn ('review')
    Accumulate ('id', 'product')
    AnalysisType ('DOCUMENT')
) AS dt
ORDER BY id;
```

**Purpose**: Enhance default dictionary with domain-specific sentiment words.

**Sample Output**:

| id | product | polarity | sentiment_score | sentiment_words |
|----|---------|----------|-----------------|-----------------|
| 1 | camera | POS | 2 | In total, positive score:7 negative score:0. excelled 1 (1), excellent 1 (2), powerful 1 (1), worth 1 (1), recommend 1 (1), capability 1 (1) |
| 3 | camera | POS | 2 | In total, positive score:6 negative score:-1. decent 1 (1), good 1 (1), irritations -1 (1), nice 1 (1), love 2 (1), obtainable 1 (1) |
| 10 | camera | NEG | 2 | In total, positive score:0 negative score:-5. failing -1 (1), need for repair -2 (1), issue -1 (1), never recommend -1 (1) |

### Example 4: Filter Only Negative Sentiments

Extract only negative sentiment results:

```sql
SELECT * FROM TD_SentimentExtractor (
    ON sentiment_extract_input AS InputTable PARTITION BY ANY
    USING
    TextColumn ('review')
    Accumulate ('id', 'product', 'category')
    AnalysisType ('DOCUMENT')
    OutputType ('NEG')
) AS dt
ORDER BY id;
```

**Purpose**: Focus analysis on negative reviews for quality improvement.

**Sample Output**:

| id | product | category | polarity | sentiment_score | sentiment_words |
|----|---------|----------|----------|-----------------|-----------------|
| 6 | gps | NEG | NEG | 2 | In total, positive score:0 negative score:-3. lack -1 (1), complaints -1 (1), mistakes -1 (1) |
| 7 | gps | NEG | NEG | 2 | In total, positive score:1 negative score:-3. disapointed -1 (1), screwed -1 (1), difficult -1 (1), support 1 (1) |
| 8 | camera | NEG | NEG | 2 | In total, positive score:0 negative score:-10. stuck -1 (1), sucks -1 (1), screwy -1 (2), not fast -1 (1), bad -1 (1), difficulty -1 (1), horrible -1 (1), not work -1 (1), hate -1 (1) |
| 9 | television | NEG | NEG | 2 | In total, positive score:1 negative score:-5. crap -1 (1), issue -1 (1), stain -1 (1), inferior -1 (1), poor -1 (1), support 1 (1) |

### Example 5: Sentence-Level with Negative Precision

Get high-confidence negative sentences:

```sql
SELECT * FROM TD_SentimentExtractor (
    ON sentiment_extract_input AS InputTable PARTITION BY ANY
    USING
    TextColumn ('review')
    Accumulate ('id', 'product')
    AnalysisType ('SENTENCE')
    Priority ('NEGATIVE_PRECISION')
    OutputType ('NEG')
) AS dt
ORDER BY id;
```

**Purpose**: Identify definitively negative sentences with high confidence.

### Example 6: Output Dictionary Table

View the dictionary used for sentiment analysis:

```sql
SELECT * FROM TD_SentimentExtractor (
    ON sentiment_extract_input AS InputTable PARTITION BY ANY
    ON sentiment_word AS CustomDictionaryTable DIMENSION
    ON sentiment_word_add AS AdditionalDictionaryTable DIMENSION
    OUT PERMANENT TABLE sentiment_dictionary_used
    USING
    TextColumn ('review')
    Accumulate ('id', 'product')
    AnalysisType ('DOCUMENT')
) AS dt;

-- View the dictionary
SELECT * FROM sentiment_dictionary_used
ORDER BY polarity_strength DESC, sentiment_word;
```

**Purpose**: Audit and verify which sentiment words were used in analysis.

## Common Use Cases

### 1. Product Review Monitoring

Track sentiment trends for products over time:

```sql
-- Daily sentiment aggregation
SELECT
    CAST(review_date AS DATE) as review_day,
    product_name,
    COUNT(*) as total_reviews,
    SUM(CASE WHEN polarity = 'POS' THEN 1 ELSE 0 END) as positive,
    SUM(CASE WHEN polarity = 'NEG' THEN 1 ELSE 0 END) as negative,
    SUM(CASE WHEN polarity = 'NEU' THEN 1 ELSE 0 END) as neutral,
    AVG(sentiment_score) as avg_sentiment_score
FROM TD_SentimentExtractor (
    ON product_reviews AS InputTable PARTITION BY ANY
    USING
    TextColumn ('review_text')
    Accumulate ('product_name', 'review_date')
    AnalysisType ('DOCUMENT')
) AS dt
GROUP BY review_day, product_name
ORDER BY review_day DESC, product_name;
```

### 2. Customer Support Prioritization

Identify urgent negative feedback requiring immediate attention:

```sql
-- Flag high-priority negative support tickets
SELECT
    ticket_id,
    customer_id,
    subject,
    polarity,
    sentiment_score,
    CASE
        WHEN polarity = 'NEG' AND sentiment_score >= 2 THEN 'URGENT'
        WHEN polarity = 'NEG' AND sentiment_score >= 1 THEN 'HIGH'
        ELSE 'NORMAL'
    END as priority_level
FROM TD_SentimentExtractor (
    ON support_tickets AS InputTable PARTITION BY ANY
    USING
    TextColumn ('ticket_description')
    Accumulate ('ticket_id', 'customer_id', 'subject', 'created_date')
    AnalysisType ('DOCUMENT')
    Priority ('NEGATIVE_PRECISION')
) AS dt
WHERE polarity = 'NEG'
ORDER BY sentiment_score DESC, created_date;
```

### 3. Survey Response Analysis

Analyze open-ended survey responses:

```sql
-- Sentiment analysis by survey question
SELECT
    question_id,
    question_text,
    polarity,
    COUNT(*) as response_count,
    AVG(sentiment_score) as avg_sentiment
FROM TD_SentimentExtractor (
    ON survey_responses AS InputTable PARTITION BY ANY
    USING
    TextColumn ('response_text')
    Accumulate ('survey_id', 'question_id', 'question_text', 'respondent_id')
    AnalysisType ('DOCUMENT')
) AS dt
GROUP BY question_id, question_text, polarity
ORDER BY question_id, polarity;
```

### 4. Social Media Monitoring

Track brand sentiment on social media:

```sql
-- Hourly sentiment tracking with custom brand dictionary
SELECT
    DATE_TRUNC('hour', post_timestamp) as hour_bucket,
    platform,
    polarity,
    COUNT(*) as post_count,
    AVG(sentiment_score) as avg_score
FROM TD_SentimentExtractor (
    ON social_media_posts AS InputTable PARTITION BY ANY
    ON brand_sentiment_dict AS AdditionalDictionaryTable DIMENSION
    USING
    TextColumn ('post_content')
    Accumulate ('post_id', 'platform', 'post_timestamp', 'author')
    AnalysisType ('DOCUMENT')
) AS dt
WHERE post_timestamp >= CURRENT_TIMESTAMP - INTERVAL '24' HOUR
GROUP BY hour_bucket, platform, polarity
ORDER BY hour_bucket DESC, platform;
```

## Best Practices

### 1. Choose Appropriate Analysis Type

**Document-level** for:
- Product reviews
- Survey responses
- Support tickets
- Overall sentiment trends

**Sentence-level** for:
- Detailed analysis of mixed sentiment
- Identifying specific pain points
- Quote extraction
- Granular sentiment tracking

### 2. Dictionary Selection

Use **default dictionary** when:
- General sentiment analysis is sufficient
- No domain-specific terms are critical
- Quick analysis is needed

Use **custom dictionary** when:
- Domain-specific terminology is important
- Default dictionary is inadequate
- Brand-specific terms need special handling

Use **additional dictionary** when:
- Mostly satisfied with default
- Need to add a few domain-specific terms
- Want to override specific word sentiments

### 3. Priority Settings

Choose priority based on business goals:

```sql
-- Maximize detection of negative feedback
Priority ('NEGATIVE_RECALL')

-- Only flag definitively negative content
Priority ('NEGATIVE_PRECISION')

-- Balanced approach
Priority ('NONE')
```

### 4. Handle Negation Carefully

Be aware of negation handling:
- "not happy" → negative
- "not very happy" → negative (1 word separation)
- "not saying I am happy" → positive (2+ word separation)

Test with your specific text patterns.

### 5. Filter Output Appropriately

```sql
-- Focus on actionable insights
WHERE polarity = 'NEG' AND sentiment_score >= 2

-- Exclude neutral for clearer trends
WHERE polarity IN ('POS', 'NEG')

-- Get specific sentiment type
OutputType ('NEG')  -- In function call
```

### 6. Validate Dictionary Contents

Always check your custom dictionary:

```sql
-- Verify dictionary before use
SELECT sentiment_word, polarity_strength
FROM custom_sentiment_dict
ORDER BY polarity_strength DESC, sentiment_word;

-- Check for duplicates
SELECT sentiment_word, COUNT(*)
FROM custom_sentiment_dict
GROUP BY sentiment_word
HAVING COUNT(*) > 1;
```

## Related Functions

- **TD_TextParser**: Tokenize text before sentiment analysis
- **TD_Ngramsplitter**: Extract phrase patterns for custom dictionaries
- **TD_NERExtractor**: Identify entities mentioned with sentiment
- **TD_TextMorph**: Lemmatize words for better dictionary matching

## Notes and Limitations

### 1. Language Support
- **English only**: Currently supports English language exclusively
- Character sets: UNICODE and LATIN supported
- No multilingual sentiment analysis

### 2. Negation Handling
The function uses distance-based rules for negation:
- Adjacent: Sentiment is negated
- 1 word gap: Sentiment is negated
- 2+ word gap: Sentiment is NOT negated

May not work perfectly for all sentence structures.

### 3. Dictionary Limitations
- Maximum sentiment word length: **128 characters**
- Maximum 10 words in a sentiment phrase
- Polarity strength must be integer values

### 4. Output Column Limitations
- **sentiment_words** column: Maximum **32000 characters**
  - If exceeded, ellipsis (...) displays at end
- **content** column: Maximum **32000 characters**
- Maximum sentence length: **32000 characters**

### 5. Dictionary Requirements
When using custom or additional dictionaries:
- Column names must be: **sentiment_word** and **polarity_strength**
- Data types must match schema requirements
- Character set must match InputTable

### 6. Sentiment Scoring
- Sentiment score values: **0** (neutral), **1** (moderate), **2** (strong)
- Based on aggregate positive and negative word counts
- May not capture nuanced sentiment in complex text

### 7. Context Limitations
- Does not understand sarcasm or irony
- May struggle with domain-specific jargon (without custom dictionary)
- Cultural context not considered
- No tone or emotion detection beyond word sentiment

### 8. Performance Considerations
- Document-level analysis is faster than sentence-level
- Custom dictionaries may impact performance
- Large text documents may be slow
- Consider filtering input for better performance

## Version Information

- **Function Version**: Based on Teradata Database Analytic Functions Version 17.20
- **Generated**: November 28, 2025
- **Lexical Database**: WordNet (English language)
