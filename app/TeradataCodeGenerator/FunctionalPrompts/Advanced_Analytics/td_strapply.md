# TD_StrApply

### Function Name
**TD_StrApply**

### Description
TD_StrApply is a string manipulation function that applies specified string operators to input table columns, enabling batch transformation of text data through operations like trimming, padding, case conversion, concatenation, substring extraction, and pattern matching. This function provides comprehensive string processing capabilities for data cleansing, standardization, and feature engineering in text-heavy analytical workflows and data preparation pipelines.

The function supports 13 distinct string operators addressing common text manipulation needs: CHARTOHEXINT for encoding, GETNCHARS for extraction, INITCAP for title case, STRING CON for concatenation, STRINGINDEX for searching, STRINGLIKE for pattern matching, STRINGPAD for alignment, STRINGREVERSE for reversal, STRINGTRIM for cleaning, SUBSTRING for slicing, TOLOWER/TOUPPER for case conversion, TRIMSPACES for whitespace removal, and UNICODESTRING for character set conversion. Each operator is applied element-wise to every value in the specified target columns, enabling efficient transformation of millions of string values through Teradata's parallel processing.

TD_StrApply seamlessly integrates into ETL pipelines and data quality workflows, offering both in-place transformation (replacing original values) and additive transformation (creating new columns alongside originals). The function handles both LATIN and UNICODE character sets, supports flexible operating sides (left/right), case sensitivity controls, and escape character specifications for pattern matching. This makes it indispensable for data engineers and analysts who need to standardize, clean, transform, and extract information from string columns as part of comprehensive data preparation workflows.

### When the Function Would Be Used
- **Data Standardization**: Normalize text formats across datasets
- **Data Cleansing**: Remove unwanted spaces, characters, and inconsistencies
- **Case Normalization**: Convert text to uppercase, lowercase, or title case
- **String Extraction**: Extract substrings and patterns from text columns
- **Text Padding**: Align strings to fixed widths for formatting
- **Pattern Matching**: Find and extract patterns from unstructured text
- **Concatenation**: Combine multiple text elements
- **String Indexing**: Locate positions of substrings
- **Character Set Conversion**: Convert between LATIN and UNICODE
- **Feature Engineering**: Create text-based features for ML models
- **Email Parsing**: Extract domains, usernames from email addresses
- **Name Standardization**: Normalize person, company, location names
- **URL Processing**: Extract domains, protocols, paths from URLs
- **Data Quality**: Clean and validate text data
- **Report Formatting**: Format strings for display

### Syntax

```sql
TD_StrApply (
    ON { table | view | (query) } AS InputTable PARTITION BY ANY
    USING
    TargetColumns ({ 'target_column' | target_column_range }[,...])
    [ OutputColumns ('output_column' [,...]) ]
    [ Accumulate ({ 'accumulate_column' | accumulate_column_range }[,...]) ]
    StringOperation (str_operator)
    [ String ('string')]
    [ StringLength ('length') ]
    [ OperatingSide ({ 'Left' | 'Right' })]
    [ IsCaseSpecific ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
    [ EscapeString ('escape_string')]
    [ IgnoreTrailingBlank ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
    [ StartIndex ('start_index')]
    [ InPlace ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'})]
)
```

### Required Syntax Elements for TD_StrApply

**ON clause (InputTable)**
- Accepts InputTable clause with PARTITION BY ANY for parallel processing
- Text columns must be CHAR or VARCHAR with LATIN or UNICODE character set

**TargetColumns**
- Specify names of InputTable columns to apply string operator
- Must be CHAR or VARCHAR (CHARACTER SET LATIN or UNICODE)
- Supports column range notation
- Multiple columns can be transformed simultaneously

**StringOperation**
- Specify the string operator to apply:

| Operator | Description |
|----------|-------------|
| CHARTOHEXINT | Converts value to hexadecimal representation |
| GETNCHARS | Returns length characters from value (left or right side) |
| INITCAP | Capitalizes first letter of value |
| STRINGCON | Concatenates string to value |
| STRINGINDEX | Returns index of first character of string in value |
| STRINGLIKE | Returns first string matching pattern if exists in value |
| STRINGPAD | Pads value with string to length (left or right side) |
| STRINGREVERSE | Reverses order of characters in value |
| STRINGTRIM | Trims string from value (left or right side) |
| SUBSTRING | Returns substring starting at start_index with length from value |
| TOLOWER | Replaces uppercase letters with lowercase equivalents |
| TOUPPER | Replaces lowercase letters with uppercase equivalents |
| TRIMSPACES | Trims leading and trailing space characters |
| UNICODESTRING | Converts LATIN value to UNICODE |

### Optional Syntax Elements for TD_StrApply

**OutputColumns**
- Specify names for output columns (ignored with InPlace='true')
- One output_column per target_column
- Maximum 128 characters per column name
- Default: target_column_operator
- Required if default name exceeds 128 characters

**Accumulate**
- Specify InputTable columns to copy unchanged to output table
- Preserves identifiers, keys, and metadata
- With InPlace='true', no target_column can be accumulate_column

**String**
- Required when str_operator needs string argument:
  - **STRINGCON**: String to concatenate
  - **STRINGINDEX**: String to search for
  - **STRINGLIKE**: Pattern to match
  - **STRINGPAD**: String to use for padding
  - **STRINGTRIM**: String to trim from value

**StringLength**
- Required when str_operator needs length argument:
  - **GETNCHARS**: Number of characters to return
  - **STRINGPAD**: Length to pad value to
  - **SUBSTRING**: Length of substring

**OperatingSide**
- Applies to: GETNCHARS, STRINGPAD, STRINGTRIM
- Specify which side to operate on: 'Left' or 'Right'
- Default: 'Left'

**IsCaseSpecific**
- Applies to: STRINGINDEX, STRINGLIKE
- Specify if search is case-sensitive
- Default: 'true' (case-sensitive)

**EscapeString**
- Applies to: STRINGLIKE
- Specify escape characters for pattern matching

**IgnoreTrailingBlank**
- Applies to: STRINGLIKE
- Specify whether to ignore trailing spaces
- Default: depends on operator

**StartIndex**
- Applies to: SUBSTRING
- Specify starting position for substring (1-indexed)

**InPlace**
- Specify whether to replace original values or create new columns
- **'true'**: Replace target column values
- **'false'**: Create new columns alongside originals
- Default: 'true'

### Input Table Schema

**InputTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | CHAR, VARCHAR (CHARACTER SET LATIN or UNICODE) | Columns to which to apply str_operator |
| accumulate_column | ANY | [Optional] Columns to preserve in output |

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| accumulate_column | Same as InputTable | Columns copied from InputTable |
| output_column | Same as InputTable | Transformed columns (name depends on InPlace setting) |

With InPlace='true', output_column is target_column (values replaced).
With InPlace='false', output_column specified by OutputColumns or defaults to target_column_operator.

### Code Examples

**Input Data: employee_data**
```
emp_id  name                  email                     department
1       john smith            john.smith@company.com    sales
2       MARY JOHNSON          MARY.JOHNSON@COMPANY.COM  marketing
3       robert WILLIAMS       robert.w@company.com      engineering
4       susan brown           s.brown@company.com       hr
```

**Example 1: TOUPPER - Uppercase Conversion**
```sql
-- Convert department names to uppercase
SELECT * FROM TD_StrApply (
    ON employee_data AS InputTable PARTITION BY ANY
    USING
    TargetColumns ('department')
    StringOperation ('TOUPPER')
    Accumulate ('emp_id', 'name')
    InPlace ('true')
) AS dt
ORDER BY emp_id;
```

**Output:**
```
emp_id  name             department
1       john smith       SALES
2       MARY JOHNSON     MARKETING
3       robert WILLIAMS  ENGINEERING
4       susan brown      HR
```

**Example 2: INITCAP - Title Case**
```sql
-- Capitalize first letter of each word in names
SELECT * FROM TD_StrApply (
    ON employee_data AS InputTable PARTITION BY ANY
    USING
    TargetColumns ('name')
    StringOperation ('INITCAP')
    Accumulate ('emp_id', 'email')
    InPlace ('false')
    OutputColumns ('name_proper')
) AS dt;
```

**Output:**
```
emp_id  name             name_proper      email
1       john smith       John Smith       john.smith@company.com
2       MARY JOHNSON     Mary Johnson     MARY.JOHNSON@COMPANY.COM
3       robert WILLIAMS  Robert Williams  robert.w@company.com
```

**Example 3: STRINGINDEX - Find Substring Position**
```sql
-- Find position of '@' in email addresses
SELECT * FROM TD_StrApply (
    ON employee_data AS InputTable PARTITION BY ANY
    USING
    TargetColumns ('email')
    StringOperation ('STRINGINDEX')
    String ('@')
    Accumulate ('emp_id', 'name', 'email')
    InPlace ('false')
    OutputColumns ('at_position')
) AS dt;

-- Returns character position of '@' symbol
```

**Example 4: SUBSTRING - Extract Domain**
```sql
-- Extract email domain (characters after '@')
SELECT
    emp_id,
    name,
    email,
    SUBSTR(email, at_pos + 1) AS domain
FROM TD_StrApply (
    ON employee_data AS InputTable PARTITION BY ANY
    USING
    TargetColumns ('email')
    StringOperation ('STRINGINDEX')
    String ('@')
    Accumulate ('emp_id', 'name', 'email')
    InPlace ('false')
    OutputColumns ('at_pos')
) AS dt;

-- Extracts: company.com from john.smith@company.com
```

**Example 5: STRINGCON - Concatenation**
```sql
-- Add prefix to department codes
SELECT * FROM TD_StrApply (
    ON department_data AS InputTable PARTITION BY ANY
    USING
    TargetColumns ('dept_code')
    StringOperation ('STRINGCON')
    String ('DEPT-')
    Accumulate ('dept_id', 'dept_name')
    InPlace ('false')
    OutputColumns ('full_code')
) AS dt;

-- 'HR' becomes 'DEPT-HR'
-- 'IT' becomes 'DEPT-IT'
```

**Example 6: TRIMSPACES - Remove Extra Whitespace**
```sql
-- Clean whitespace from text fields
SELECT * FROM TD_StrApply (
    ON messy_data AS InputTable PARTITION BY ANY
    USING
    TargetColumns ('customer_name', 'address', 'city')
    StringOperation ('TRIMSPACES')
    Accumulate ('customer_id')
    InPlace ('true')
) AS dt;

-- '  John Smith  ' becomes 'John Smith'
-- 'New York  ' becomes 'New York'
```

**Example 7: GETNCHARS - Extract First N Characters**
```sql
-- Extract first 3 characters as code
SELECT * FROM TD_StrApply (
    ON product_data AS InputTable PARTITION BY ANY
    USING
    TargetColumns ('product_name')
    StringOperation ('GETNCHARS')
    StringLength (3)
    OperatingSide ('Left')
    Accumulate ('product_id', 'product_name')
    InPlace ('false')
    OutputColumns ('product_code')
) AS dt;

-- 'Laptop Computer' → 'Lap'
-- 'Desktop PC' → 'Des'
```

**Example 8: STRINGPAD - Pad to Fixed Width**
```sql
-- Pad account numbers to 10 characters with zeros
SELECT * FROM TD_StrApply (
    ON accounts AS InputTable PARTITION BY ANY
    USING
    TargetColumns ('account_num')
    StringOperation ('STRINGPAD')
    String ('0')
    StringLength (10)
    OperatingSide ('Left')
    Accumulate ('customer_id', 'account_type')
    InPlace ('false')
    OutputColumns ('account_padded')
) AS dt;

-- '12345' becomes '0000012345'
-- '987' becomes '0000000987'
```

**Example 9: STRINGTRIM - Remove Prefix/Suffix**
```sql
-- Remove 'www.' prefix from URLs
SELECT * FROM TD_StrApply (
    ON website_data AS InputTable PARTITION BY ANY
    USING
    TargetColumns ('url')
    StringOperation ('STRINGTRIM')
    String ('www.')
    OperatingSide ('Left')
    Accumulate ('site_id', 'site_name')
    InPlace ('false')
    OutputColumns ('url_clean')
) AS dt;

-- 'www.example.com' becomes 'example.com'
-- 'www.test.org' becomes 'test.org'
```

**Example 10: Complete Text Cleaning Pipeline**
```sql
-- Step 1: Trim whitespace
CREATE TABLE names_trimmed AS (
    SELECT * FROM TD_StrApply (
        ON customer_data AS InputTable PARTITION BY ANY
        USING
        TargetColumns ('first_name', 'last_name')
        StringOperation ('TRIMSPACES')
        Accumulate ('customer_id')
        InPlace ('true')
    ) AS dt
) WITH DATA;

-- Step 2: Title case
CREATE TABLE names_proper AS (
    SELECT * FROM TD_StrApply (
        ON names_trimmed AS InputTable PARTITION BY ANY
        USING
        TargetColumns ('first_name', 'last_name')
        StringOperation ('INITCAP')
        Accumulate ('customer_id')
        InPlace ('true')
    ) AS dt
) WITH DATA;

-- Result: Clean, properly capitalized names
```

### String Operators Explained

**1. TOUPPER** - Convert to Uppercase
- Replaces all lowercase letters with uppercase equivalents
- Leaves uppercase letters and non-letters unchanged
- Use for case-insensitive comparisons and standardization

**2. TOLOWER** - Convert to Lowercase
- Replaces all uppercase letters with lowercase equivalents
- Leaves lowercase letters and non-letters unchanged
- Use for case-insensitive matching and normalization

**3. INITCAP** - Title Case
- Capitalizes first letter of each word
- Converts remaining letters to lowercase
- Words separated by spaces or punctuation

**4. TRIMSPACES** - Remove Leading/Trailing Spaces
- Removes spaces from both ends of string
- Preserves internal spaces
- Essential for data cleansing

**5. STRINGTRIM** - Remove Specified String
- Removes specified string from left or right
- OperatingSide controls which end
- Useful for prefix/suffix removal

**6. STRINGCON** - Concatenate String
- Appends specified string to value
- Creates combined strings
- Useful for adding prefixes/suffixes

**7. STRINGPAD** - Pad to Length
- Pads string to specified length
- OperatingSide controls pad direction (left/right)
- String parameter specifies pad character

**8. GETNCHARS** - Extract N Characters
- Returns first N (left) or last N (right) characters
- OperatingSide controls which end
- Useful for code extraction

**9. SUBSTRING** - Extract Substring
- Returns substring from start_index with specified length
- 1-indexed (first character is position 1)
- Flexible extraction

**10. STRINGINDEX** - Find Substring Position
- Returns position of first occurrence of substring
- Returns 0 if not found
- Case-sensitivity controlled by IsCaseSpecific

**11. STRINGLIKE** - Pattern Matching
- Finds first string matching pattern
- Supports wildcards and escape characters
- IsCaseSpecific controls case sensitivity

**12. STRINGREVERSE** - Reverse String
- Reverses character order
- 'ABC' becomes 'CBA'
- Useful for specialized processing

**13. CHARTOHEXINT** - Convert to Hexadecimal
- Converts characters to hex representation
- Useful for encoding and hashing
- Creates hexadecimal string

**14. UNICODESTRING** - Convert to Unicode
- Converts LATIN character set to UNICODE
- Enables international character support
- Essential for multilingual data

### Use Cases and Applications

**1. Data Standardization**
- Normalize case (all uppercase or lowercase)
- Title case for proper nouns
- Trim whitespace consistently
- Remove prefixes/suffixes

**2. Email Processing**
- Extract domains from addresses
- Normalize to lowercase
- Validate format patterns
- Create domain-based features

**3. Name Cleansing**
- Standardize person names (title case)
- Remove titles (Mr., Mrs., Dr.)
- Handle multi-part surnames
- Clean data entry inconsistencies

**4. URL/Domain Parsing**
- Remove protocols (http://, https://)
- Extract domains from full URLs
- Normalize www. prefix
- Create domain-level features

**5. String Feature Engineering**
- Extract first N characters as codes
- Create length-based features
- Pattern matching for categories
- Substring extraction for attributes

**6. Data Quality**
- Trim whitespace from all text
- Standardize case formats
- Remove special characters
- Validate and clean inconsistent entries

**7. Report Formatting**
- Pad numbers with zeros for alignment
- Format strings to fixed widths
- Create display-ready strings
- Align columnar text output

**8. Text Normalization for ML**
- Lowercase all text for modeling
- Remove punctuation and special characters
- Standardize formats
- Create consistent features

**9. Database Standardization**
- Clean legacy data inconsistencies
- Align formats across merged systems
- Standardize codes and identifiers
- Prepare for data warehouse integration

**10. Privacy and Masking**
- Extract substrings for anonymization
- Replace sensitive portions
- Create masked versions
- Support GDPR compliance

### Important Notes

**Character Set Support:**
- Supports CHAR and VARCHAR types
- Both LATIN and UNICODE character sets
- Use UNICODESTRING to convert LATIN to UNICODE
- Consider character set when processing international text

**InPlace vs New Columns:**
- InPlace='true' replaces original values (destructive)
- InPlace='false' creates new columns (preserves originals)
- Preserve originals for validation and debugging
- Consider storage tradeoffs

**Case Sensitivity:**
- STRINGINDEX and STRINGLIKE support IsCaseSpecific
- Default is case-sensitive (IsCaseSpecific='true')
- Set to 'false' for case-insensitive matching
- Important for user input matching

**Operator-Specific Parameters:**
- Some operators require specific parameters
- String required for: STRINGCON, STRINGINDEX, STRINGLIKE, STRINGPAD, STRINGTRIM
- StringLength required for: GETNCHARS, STRINGPAD, SUBSTRING
- StartIndex required for: SUBSTRING
- Validate parameter combinations

**Performance:**
- Efficient parallel processing with PARTITION BY ANY
- Scales well to large datasets
- Minimal memory overhead
- Consider batch processing for very large tables

**NULL Handling:**
- NULL values remain NULL after transformation
- Operations do not create or remove NULLs
- NULL-safe processing

**Column Naming:**
- Default naming: target_column_operator
- Specify OutputColumns if default exceeds 128 characters
- Use descriptive names for clarity

**Pattern Matching Complexity:**
- STRINGLIKE supports pattern wildcards
- EscapeString enables special character matching
- Test patterns thoroughly
- Consider performance for complex patterns

### Best Practices

**1. Preserve Original Data**
- Use InPlace='false' to keep originals
- Enables validation and comparison
- Supports debugging and analysis
- Facilitates rollback if needed

**2. Clean Data Consistently**
- Apply TRIMSPACES to all text columns
- Standardize case formats (TOUPPER, TOLOWER, INITCAP)
- Document cleansing rules
- Test with sample data first

**3. Choose Appropriate Operator**
- TOUPPER/TOLOWER for case normalization
- INITCAP for proper nouns
- TRIMSPACES for whitespace removal
- SUBSTRING for extraction

**4. Handle Edge Cases**
- Test with NULL values
- Validate empty strings
- Check special characters
- Test boundary conditions

**5. Use Descriptive Column Names**
- Specify meaningful OutputColumns names
- Follow naming conventions
- Document purpose in data dictionary
- Enable easy interpretation

**6. Validate Transformation Results**
- Check for unexpected NULLs
- Verify pattern matching accuracy
- Compare before/after distributions
- Test on sample data

**7. Combine Multiple Operations**
- Chain transformations in sequence
- Build complete cleansing pipelines
- Test combined effects
- Document transformation order

**8. Optimize for Performance**
- Use PARTITION BY ANY for parallelism
- Batch multiple column transformations
- Consider incremental processing
- Monitor resource utilization

**9. Document String Operations**
- Record which operator applied to which columns
- Document rationale for transformations
- Maintain specifications
- Enable reproducibility

**10. Test with International Characters**
- Validate UNICODE support when needed
- Test with non-ASCII characters
- Consider locale-specific rules
- Use UNICODESTRING for conversion

### Related Functions
- **TD_NumApply** - Apply numeric operators to numeric columns
- **UPPER() / LOWER()** - SQL built-in case conversion functions
- **TRIM() / LTRIM() / RTRIM()** - SQL built-in trimming functions
- **SUBSTR() / SUBSTRING()** - SQL built-in substring extraction
- **CONCAT() / ||** - SQL built-in concatenation operators

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Utility Functions
