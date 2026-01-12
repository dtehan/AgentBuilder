# TD_RowNormalizeFit

### Function Name
**TD_RowNormalizeFit**

### Description
TD_RowNormalizeFit creates a specification table that defines how to normalize data row-wise (across features within each observation). This function prepares the metadata for row-level normalization, where each row's values are scaled relative to other values in the same row, rather than normalizing columns independently. The specifications are then applied by TD_RowNormalizeTransform.

Row normalization is fundamentally different from column normalization (TD_ScaleFit). Instead of standardizing each feature across all observations, row normalization ensures that the values within each observation maintain relative proportions or magnitudes. This is particularly valuable for compositional data (where values represent parts of a whole), text analytics (term frequency normalization), and image processing (pixel intensity normalization).

The function supports four normalization approaches: UNITVECTOR (L2 norm), FRACTION (proportion of sum), PERCENTAGE (proportion as percentage), and INDEX (relative to a base value). Each approach serves different analytical needs, from vector space models to proportion analysis.

### When the Function Would Be Used
- **Compositional Data Analysis**: Normalize proportions that sum to 1 or 100%
- **Text Analytics**: TF-IDF and document term frequency normalization
- **Image Processing**: Pixel intensity normalization across images
- **Gene Expression Analysis**: Normalize expression levels within samples
- **Portfolio Analysis**: Normalize asset allocations within portfolios
- **Survey Response Normalization**: Scale responses relative to total per respondent
- **Market Basket Analysis**: Normalize item quantities per transaction
- **Budget Analysis**: Convert amounts to percentages of total budget
- **Vector Space Models**: Create unit vectors for cosine similarity
- **Feature Engineering**: Create ratio features relative to row totals

### Syntax

```sql
TD_RowNormalizeFit (
    ON { table | view | (query) } AS InputTable
    USING
    TargetColumns ({ 'target_column' | target_column_range }[,...])
    Approach ('UNITVECTOR' | 'FRACTION' | 'PERCENTAGE' | 'INDEX')
    [ BaseColumn ('base_column') ]
    [ BaseValue (base_value) ]
)
```

### Required Syntax Elements for TD_RowNormalizeFit

**ON clause**
- Accepts the InputTable clause containing numeric data
- Used for schema validation, not for calculation

**TargetColumns**
- Specify numeric columns to be row-normalized
- Must be numeric data types
- Supports column range notation
- These columns will be normalized row-wise

**Approach**
- Specify row normalization method
- Valid values: 'UNITVECTOR', 'FRACTION', 'PERCENTAGE', 'INDEX'
- **UNITVECTOR**: L2 normalization (unit vector with length 1)
- **FRACTION**: Each value divided by row sum (proportions)
- **PERCENTAGE**: Each value as percentage of row sum
- **INDEX**: Each value relative to base value (typically 100)

### Optional Syntax Elements for TD_RowNormalizeFit

**BaseColumn**
- Specify column to use as base for INDEX approach
- Only applicable when Approach='INDEX'
- Column must be in TargetColumns
- This column's value becomes the reference (typically set to 100)

**BaseValue**
- Specify fixed base value for INDEX approach
- Only applicable when Approach='INDEX' and BaseColumn not specified
- Default: 100
- All values scaled relative to this base

### Input Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | Numeric types (INTEGER, BIGINT, FLOAT, DOUBLE PRECISION, DECIMAL, NUMERIC) | Columns to be row-normalized |

### Output Table Schema (FitTable)

The output is a specification table with normalization parameters:

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | VARCHAR | Names of columns to be normalized |
| approach | VARCHAR | Normalization method (UNITVECTOR, FRACTION, PERCENTAGE, INDEX) |
| base_column | VARCHAR | [Optional] Base column for INDEX approach |
| base_value | DOUBLE PRECISION | [Optional] Base value for INDEX approach |

The FitTable contains the transformation rules used by TD_RowNormalizeTransform.

### Code Examples

**Input Data: compositional_data**
```
id  component_a  component_b  component_c  component_d
1   30.0         50.0         15.0         5.0
2   10.0         20.0         60.0         10.0
3   25.0         25.0         25.0         25.0
```

**Example 1: FRACTION Approach (Proportions)**
```sql
-- Normalize to proportions (values sum to 1 per row)
CREATE TABLE rownorm_fraction_fit AS (
    SELECT * FROM TD_RowNormalizeFit (
        ON compositional_data AS InputTable
        USING
        TargetColumns('component_a', 'component_b', 'component_c', 'component_d')
        Approach('FRACTION')
    ) AS dt
) WITH DATA;

-- View fit specifications
SELECT * FROM rownorm_fraction_fit;
```

**Output FitTable:**
```
target_column  approach   base_column  base_value
component_a    FRACTION   NULL         NULL
component_b    FRACTION   NULL         NULL
component_c    FRACTION   NULL         NULL
component_d    FRACTION   NULL         NULL
```

**Example 2: PERCENTAGE Approach**
```sql
-- Normalize to percentages (values sum to 100% per row)
CREATE TABLE rownorm_percentage_fit AS (
    SELECT * FROM TD_RowNormalizeFit (
        ON budget_data AS InputTable
        USING
        TargetColumns('marketing', 'operations', 'research', 'admin')
        Approach('PERCENTAGE')
    ) AS dt
) WITH DATA;
```

**Example 3: UNITVECTOR Approach (L2 Normalization)**
```sql
-- Create unit vectors (vector length = 1)
CREATE TABLE rownorm_unitvector_fit AS (
    SELECT * FROM TD_RowNormalizeFit (
        ON document_features AS InputTable
        USING
        TargetColumns('[3:1002]')  -- 1000 TF-IDF features
        Approach('UNITVECTOR')
    ) AS dt
) WITH DATA;

-- Used for cosine similarity in text analytics
```

**Example 4: INDEX Approach with BaseColumn**
```sql
-- Normalize relative to a base column
CREATE TABLE rownorm_index_fit AS (
    SELECT * FROM TD_RowNormalizeFit (
        ON price_series AS InputTable
        USING
        TargetColumns('jan_price', 'feb_price', 'mar_price', 'apr_price', 'may_price')
        Approach('INDEX')
        BaseColumn('jan_price')  -- January becomes 100
    ) AS dt
) WITH DATA;

-- Creates price index with January as base period
```

**Example 5: INDEX Approach with BaseValue**
```sql
-- Normalize relative to fixed base value
CREATE TABLE rownorm_index_base100_fit AS (
    SELECT * FROM TD_RowNormalizeFit (
        ON sensor_readings AS InputTable
        USING
        TargetColumns('sensor1', 'sensor2', 'sensor3', 'sensor4')
        Approach('INDEX')
        BaseValue(100)
    ) AS dt
) WITH DATA;

-- All values scaled so first reading = 100
```

**Example 6: Text Document Normalization**
```sql
-- Normalize term frequencies for document comparison
CREATE TABLE doc_rownorm_fit AS (
    SELECT * FROM TD_RowNormalizeFit (
        ON document_term_matrix AS InputTable
        USING
        TargetColumns('[4:5003]')  -- 5000 terms
        Approach('UNITVECTOR')
    ) AS dt
) WITH DATA;

-- Enables cosine similarity for document clustering
```

**Example 7: Portfolio Allocation Normalization**
```sql
-- Normalize portfolio holdings to percentages
CREATE TABLE portfolio_norm_fit AS (
    SELECT * FROM TD_RowNormalizeFit (
        ON portfolio_holdings AS InputTable
        USING
        TargetColumns('stocks', 'bonds', 'real_estate', 'commodities', 'cash')
        Approach('PERCENTAGE')
    ) AS dt
) WITH DATA;

-- Each row (portfolio) will sum to 100%
```

**Example 8: Survey Response Normalization**
```sql
-- Normalize likert scale responses per respondent
CREATE TABLE survey_norm_fit AS (
    SELECT * FROM TD_RowNormalizeFit (
        ON survey_responses AS InputTable
        USING
        TargetColumns('q1_rating', 'q2_rating', 'q3_rating', 'q4_rating', 'q5_rating')
        Approach('FRACTION')
    ) AS dt
) WITH DATA;

-- Shows relative importance of responses within each respondent
```

**Example 9: Market Basket Normalization**
```sql
-- Normalize item quantities per transaction
CREATE TABLE basket_norm_fit AS (
    SELECT * FROM TD_RowNormalizeFit (
        ON transaction_items AS InputTable
        USING
        TargetColumns('item1_qty', 'item2_qty', 'item3_qty', 'item4_qty', 'item5_qty')
        Approach('FRACTION')
    ) AS dt
) WITH DATA;

-- Each transaction's items represented as fractions of total quantity
```

**Example 10: Gene Expression Normalization**
```sql
-- Normalize gene expression levels within samples
CREATE TABLE gene_norm_fit AS (
    SELECT * FROM TD_RowNormalizeFit (
        ON gene_expression AS InputTable
        USING
        TargetColumns('[2:10001]')  -- 10000 genes
        Approach('UNITVECTOR')
    ) AS dt
) WITH DATA;

-- Removes sample-specific technical variation
```

### Row Normalization Approaches Explained

**1. UNITVECTOR (L2 Normalization)**

Formula: x_normalized = x / ||x||₂

Where ||x||₂ = √(x₁² + x₂² + ... + xₙ²)

**Example:**
```
Original row: [3, 4, 0]
L2 norm: √(3² + 4² + 0²) = √(9 + 16) = 5
Normalized: [3/5, 4/5, 0/5] = [0.6, 0.8, 0.0]
```

**Properties:**
- Result has unit length: ||x_normalized||₂ = 1
- Preserves direction, normalizes magnitude
- Ideal for cosine similarity calculations
- Used in text analytics and recommendation systems

**2. FRACTION (Proportion)**

Formula: x_normalized = x / Σx

**Example:**
```
Original row: [30, 50, 15, 5]
Sum: 30 + 50 + 15 + 5 = 100
Normalized: [30/100, 50/100, 15/100, 5/100] = [0.30, 0.50, 0.15, 0.05]
```

**Properties:**
- Values sum to 1.0 per row
- Represents proportions
- Ideal for compositional data
- Used in portfolio analysis, market share

**3. PERCENTAGE (Proportion × 100)**

Formula: x_normalized = (x / Σx) × 100

**Example:**
```
Original row: [30, 50, 15, 5]
Sum: 30 + 50 + 15 + 5 = 100
Normalized: [(30/100)×100, (50/100)×100, (15/100)×100, (5/100)×100] = [30%, 50%, 15%, 5%]
```

**Properties:**
- Values sum to 100% per row
- More intuitive than fractions
- Ideal for budget analysis, surveys
- Used in reporting and visualization

**4. INDEX (Relative to Base)**

Formula (with BaseColumn): x_normalized = (x / x_base) × BaseValue

Formula (without BaseColumn): x_normalized = (x / x_first) × BaseValue

**Example (with BaseColumn='jan_price', BaseValue=100):**
```
Original row: [50, 55, 48, 52] (jan, feb, mar, apr prices)
BaseColumn: jan_price = 50
Normalized: [(50/50)×100, (55/50)×100, (48/50)×100, (52/50)×100] = [100, 110, 96, 104]
```

**Properties:**
- Base period/column set to BaseValue (typically 100)
- Shows relative changes as index values
- Ideal for time series, price indices
- Used in economic analysis, benchmarking

### Use Cases and Applications

**1. Text Analytics and NLP**
- Normalize TF-IDF vectors for document similarity
- Create unit vectors for cosine similarity calculations
- Normalize term frequencies within documents
- Enable semantic search and clustering

**2. Compositional Data Analysis**
- Analyze data that represents parts of a whole
- Geological composition analysis
- Chemical composition studies
- Microbiome data analysis

**3. Portfolio and Financial Analysis**
- Normalize asset allocations to percentages
- Analyze portfolio composition changes
- Compare investment distributions
- Risk allocation analysis

**4. Image Processing**
- Normalize pixel intensities per image
- Create comparable image features
- Remove lighting variations
- Enable image similarity comparisons

**5. Survey and Questionnaire Analysis**
- Normalize responses within respondents
- Ipsative scoring (relative preferences)
- Remove response style bias
- Analyze relative priorities

**6. Gene Expression Analysis**
- Normalize expression levels within samples
- Remove technical variation
- Enable cross-sample comparisons
- Differential expression analysis

**7. Market Basket Analysis**
- Analyze item composition per transaction
- Identify purchasing patterns
- Calculate item associations
- Product bundling analysis

**8. Budget and Resource Allocation**
- Convert absolute amounts to percentages
- Compare budget structures
- Analyze spending priorities
- Track allocation changes over time

**9. Time Series Index Creation**
- Create price indices with base periods
- Analyze relative changes over time
- Economic indicator normalization
- Performance benchmarking

**10. Recommendation Systems**
- Normalize user-item interactions
- Create user preference vectors
- Enable collaborative filtering
- Calculate item similarities

### Important Notes

**Row-Wise vs Column-Wise:**
- Row normalization: scales within each observation (row)
- Column normalization (TD_ScaleFit): scales within each feature (column)
- Choose based on data structure and analytical goals
- Row normalization for compositional data, column for feature scaling

**Approach Selection:**
- **UNITVECTOR**: For distance/similarity calculations (cosine similarity)
- **FRACTION**: For compositional data, proportions
- **PERCENTAGE**: For reporting, visualization, intuitive interpretation
- **INDEX**: For time series, relative changes, benchmarking

**Zero and Negative Values:**
- UNITVECTOR: Works with negatives, problematic if all values zero
- FRACTION/PERCENTAGE: Requires non-negative values, undefined if sum=0
- INDEX: Works with negatives if base value non-zero
- Consider data characteristics when choosing approach

**BaseColumn vs BaseValue:**
- BaseColumn: Dynamic base (different for each row)
- BaseValue: Fixed base (constant across rows)
- BaseColumn useful for time series (base period)
- BaseValue useful for standardized indices

**NULL Handling:**
- NULLs in target columns will cause issues
- Remove or impute NULLs before fitting
- Use TD_SimpleImputeFit/Transform for imputation
- All target columns must have non-NULL values

**Fit Operation:**
- Fit operation is lightweight (metadata only)
- No actual data computation during fit
- Schema validation only
- Fast and efficient

**Sparse Data Considerations:**
- UNITVECTOR handles sparse data well
- FRACTION/PERCENTAGE work with sparse data
- INDEX may amplify sparsity effects
- Consider sparsity patterns when choosing approach

### Best Practices

**1. Choose Appropriate Approach**
- UNITVECTOR for vector space models and similarity
- FRACTION/PERCENTAGE for compositional data
- INDEX for time series and relative changes
- Match approach to analytical objectives

**2. Handle Missing Data First**
- Impute or remove NULLs before fitting
- Document imputation strategy
- Consider impact on row totals (FRACTION/PERCENTAGE)
- Use consistent imputation across datasets

**3. Validate Data Requirements**
- FRACTION/PERCENTAGE: Ensure non-negative values
- Check for zero-sum rows (undefined normalization)
- Validate base column values for INDEX
- Test with sample data first

**4. Consider Data Characteristics**
- Sparse vs dense data
- Value ranges and distributions
- Presence of outliers
- Compositional constraints

**5. Document Specifications**
- Record approach and rationale
- Store BaseColumn/BaseValue choices
- Maintain FitTable with model artifacts
- Enable reproducibility

**6. Consistent Application**
- Create FitTable on training data only
- Apply to train, validation, test, production
- Never fit on test data
- Version control FitTable

**7. Validate Normalization Results**
- Check row sums (FRACTION=1, PERCENTAGE=100)
- Verify vector lengths (UNITVECTOR=1)
- Validate index base values
- Test on sample data

**8. Handle Edge Cases**
- Zero-sum rows for FRACTION/PERCENTAGE
- All-zero rows for UNITVECTOR
- Negative values in base column for INDEX
- Implement appropriate error handling

**9. Combine with Other Transformations**
- May combine with column scaling (TD_ScaleFit)
- Consider order of operations
- Document transformation pipeline
- Test combined effects

**10. Production Deployment**
- Store FitTable with trained model
- Validate compatibility before scoring
- Implement input validation
- Monitor for normalization issues

### Related Functions
- **TD_RowNormalizeTransform** - Applies row normalization using FitTable (must be used after TD_RowNormalizeFit)
- **TD_ScaleFit** - Column-wise normalization (alternative approach)
- **TD_ScaleTransform** - Apply column-wise scaling
- **TD_SimpleImputeFit** - Handle missing values before normalization

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Transform Functions
