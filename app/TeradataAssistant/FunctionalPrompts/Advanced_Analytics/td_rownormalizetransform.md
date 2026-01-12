# TD_RowNormalizeTransform

### Function Name
**TD_RowNormalizeTransform**

### Description
TD_RowNormalizeTransform applies row-wise normalization using the specifications created by TD_RowNormalizeFit. This function performs the actual transformation of data, scaling values within each row according to the normalization approach (UNITVECTOR, FRACTION, PERCENTAGE, or INDEX) defined in the FitTable.

This is the execution component of the row normalization pipeline. After TD_RowNormalizeFit defines the normalization method and parameters, TD_RowNormalizeTransform applies these rules to transform data row-by-row. Unlike column normalization which scales features independently across observations, row normalization ensures that values within each observation maintain relative proportions or are scaled to a consistent magnitude.

The transformation is deterministic given a FitTable, ensuring consistent normalization across training, validation, test, and production datasets. This consistency is essential for machine learning pipelines and analytical workflows where data must be identically transformed across all datasets.

### When the Function Would Be Used
- **Apply Row Normalization**: Execute row-wise scaling transformations
- **ML Pipeline Execution**: Transform training and test data consistently
- **Text Document Processing**: Normalize TF-IDF vectors for similarity
- **Production Scoring**: Transform incoming data in real-time
- **Compositional Data Transform**: Convert to proportions or percentages
- **Image Feature Normalization**: Scale pixel intensities per image
- **Portfolio Rebalancing**: Convert holdings to target percentages
- **Survey Data Processing**: Scale responses within respondents
- **Gene Expression Analysis**: Normalize expression within samples
- **Time Series Index Creation**: Generate relative indices with base periods

### Syntax

```sql
TD_RowNormalizeTransform (
    ON { table | view | (query) } AS InputTable [ PARTITION BY ANY ]
    ON { table | view | (query) } AS FitTable AS FitTableAlias DIMENSION
    USING
    [ Accumulate ({'accumulate_column' | 'accumulate_column_range'}[,...]) ]
)
```

### Required Syntax Elements for TD_RowNormalizeTransform

**ON clause (InputTable)**
- Accepts the InputTable clause containing data to transform
- Must have same columns as data used for TD_RowNormalizeFit
- PARTITION BY ANY recommended for parallel processing

**ON clause (FitTable DIMENSION)**
- Accepts the FitTable clause (output from TD_RowNormalizeFit)
- Contains row normalization specifications
- DIMENSION keyword required

### Optional Syntax Elements for TD_RowNormalizeTransform

**Accumulate**
- Specify input table column names to copy to the output table
- Useful for preserving identifiers, keys, and metadata
- Supports column range notation
- Typically includes ID columns and non-transformed features

### Input Table Schema

**InputTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | Numeric types (INTEGER, BIGINT, FLOAT, DOUBLE PRECISION, DECIMAL, NUMERIC) | Columns specified in TD_RowNormalizeFit TargetColumns |
| accumulate_column | ANY | [Optional] Columns to preserve in output table |

**FitTable Schema:**

See TD_RowNormalizeFit Output table schema. This is the specification table created by TD_RowNormalizeFit function.

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| accumulate_column | Same as InputTable | Columns specified in Accumulate parameter |
| normalized_column | DOUBLE PRECISION | Row-normalized versions of target columns with same names as original |

All normalized columns are DOUBLE PRECISION type regardless of input type.

### Code Examples

**Input Data: compositional_data**
```
id  component_a  component_b  component_c  component_d
1   30.0         50.0         15.0         5.0
2   10.0         20.0         60.0         10.0
3   25.0         25.0         25.0         25.0
```

**FitTable: rownorm_fraction_fit** (created by TD_RowNormalizeFit)
```
-- Created with: Approach('FRACTION')
-- TargetColumns('component_a', 'component_b', 'component_c', 'component_d')
```

**Example 1: FRACTION Transformation (Proportions)**
```sql
-- Step 1: Create fit table (already done)
CREATE TABLE rownorm_fraction_fit AS (
    SELECT * FROM TD_RowNormalizeFit (
        ON compositional_data AS InputTable
        USING
        TargetColumns('component_a', 'component_b', 'component_c', 'component_d')
        Approach('FRACTION')
    ) AS dt
) WITH DATA;

-- Step 2: Apply transformation
SELECT * FROM TD_RowNormalizeTransform (
    ON compositional_data AS InputTable
    ON rownorm_fraction_fit AS FitTable DIMENSION
    USING
    Accumulate('id')
) AS dt
ORDER BY id;
```

**Output:**
```
id  component_a  component_b  component_c  component_d
1   0.30         0.50         0.15         0.05         (sums to 1.0)
2   0.10         0.20         0.60         0.10         (sums to 1.0)
3   0.25         0.25         0.25         0.25         (sums to 1.0)
```

**Example 2: PERCENTAGE Transformation**
```sql
-- Transform budget to percentages
CREATE TABLE budget_normalized AS (
    SELECT * FROM TD_RowNormalizeTransform (
        ON budget_data AS InputTable
        ON rownorm_percentage_fit AS FitTable DIMENSION
        USING
        Accumulate('department_id', 'year')
    ) AS dt
) WITH DATA;

-- Each row now sums to 100%
```

**Example 3: UNITVECTOR Transformation for Text**
```sql
-- Create unit vectors for document similarity
CREATE TABLE doc_unitvector_fit AS (
    SELECT * FROM TD_RowNormalizeFit (
        ON document_features AS InputTable
        USING
        TargetColumns('[3:1002]')  -- 1000 TF-IDF features
        Approach('UNITVECTOR')
    ) AS dt
) WITH DATA;

-- Apply transformation
CREATE TABLE documents_normalized AS (
    SELECT * FROM TD_RowNormalizeTransform (
        ON document_features AS InputTable
        ON doc_unitvector_fit AS FitTable DIMENSION
        USING
        Accumulate('document_id', 'category')
    ) AS dt
) WITH DATA;

-- Now ready for cosine similarity calculations
```

**Example 4: INDEX Transformation for Time Series**
```sql
-- Create price index with January as base (=100)
CREATE TABLE price_index_fit AS (
    SELECT * FROM TD_RowNormalizeFit (
        ON monthly_prices AS InputTable
        USING
        TargetColumns('jan_price', 'feb_price', 'mar_price', 'apr_price', 'may_price', 'jun_price')
        Approach('INDEX')
        BaseColumn('jan_price')
        BaseValue(100)
    ) AS dt
) WITH DATA;

-- Transform to index values
SELECT * FROM TD_RowNormalizeTransform (
    ON monthly_prices AS InputTable
    ON price_index_fit AS FitTable DIMENSION
    USING
    Accumulate('product_id', 'product_name')
) AS dt
ORDER BY product_id;
```

**Output (example for one product):**
```
product_id  product_name  jan_price  feb_price  mar_price  apr_price  may_price  jun_price
101         Widget_A      100.0      105.2      98.4       102.6      110.8      107.2
```

**Example 5: Transform Training and Test Data**
```sql
-- Transform training set
CREATE TABLE training_normalized AS (
    SELECT * FROM TD_RowNormalizeTransform (
        ON training_data AS InputTable
        ON rownorm_fit AS FitTable DIMENSION
        USING
        Accumulate('id', 'target')
    ) AS dt
) WITH DATA;

-- Transform test set with same FitTable
CREATE TABLE test_normalized AS (
    SELECT * FROM TD_RowNormalizeTransform (
        ON test_data AS InputTable
        ON rownorm_fit AS FitTable DIMENSION  -- Same FitTable!
        USING
        Accumulate('id')
    ) AS dt
) WITH DATA;
```

**Example 6: Portfolio Allocation to Percentages**
```sql
-- Normalize portfolio holdings to percentages
CREATE TABLE portfolios_normalized AS (
    SELECT * FROM TD_RowNormalizeTransform (
        ON portfolio_holdings AS InputTable
        ON portfolio_norm_fit AS FitTable DIMENSION
        USING
        Accumulate('portfolio_id', 'client_name', 'total_value')
    ) AS dt
) WITH DATA;

-- Each portfolio now shows percentage allocation
SELECT
    portfolio_id,
    client_name,
    stocks AS stocks_pct,
    bonds AS bonds_pct,
    real_estate AS real_estate_pct
FROM portfolios_normalized;
```

**Example 7: Survey Response Normalization**
```sql
-- Normalize survey responses to show relative importance
SELECT * FROM TD_RowNormalizeTransform (
    ON survey_responses AS InputTable
    ON survey_norm_fit AS FitTable DIMENSION
    USING
    Accumulate('respondent_id', 'survey_date')
) AS dt
ORDER BY respondent_id;

-- Shows which questions were rated highest by each respondent (relative to their own ratings)
```

**Example 8: Market Basket Analysis**
```sql
-- Normalize item quantities per transaction
CREATE TABLE baskets_normalized AS (
    SELECT * FROM TD_RowNormalizeTransform (
        ON transaction_items AS InputTable
        ON basket_norm_fit AS FitTable DIMENSION
        USING
        Accumulate('transaction_id', 'customer_id', 'transaction_date')
    ) AS dt
) WITH DATA;

-- Each transaction shows items as fractions of total quantity
```

**Example 9: Gene Expression Normalization**
```sql
-- Normalize gene expression levels within samples
CREATE TABLE gene_expr_normalized AS (
    SELECT * FROM TD_RowNormalizeTransform (
        ON gene_expression AS InputTable
        ON gene_norm_fit AS FitTable DIMENSION
        USING
        Accumulate('sample_id', 'patient_id', 'tissue_type')
    ) AS dt
) WITH DATA;

-- Removes sample-specific technical variation for comparison
```

**Example 10: Complete ML Pipeline**
```sql
-- End-to-end row normalization pipeline
-- Step 1: Create fit on training data only
CREATE TABLE rownorm_fit AS (
    SELECT * FROM TD_RowNormalizeFit (
        ON training_data AS InputTable
        USING
        TargetColumns('[3:53]')  -- 50 features
        Approach('UNITVECTOR')
    ) AS dt
) WITH DATA;

-- Step 2: Transform training data
CREATE TABLE train_normalized AS (
    SELECT * FROM TD_RowNormalizeTransform (
        ON training_data AS InputTable
        ON rownorm_fit AS FitTable DIMENSION
        USING
        Accumulate('id', 'target')
    ) AS dt
) WITH DATA;

-- Step 3: Transform validation data (same FitTable)
CREATE TABLE validation_normalized AS (
    SELECT * FROM TD_RowNormalizeTransform (
        ON validation_data AS InputTable
        ON rownorm_fit AS FitTable DIMENSION
        USING
        Accumulate('id', 'target')
    ) AS dt
) WITH DATA;

-- Step 4: Transform test data (same FitTable)
CREATE TABLE test_normalized AS (
    SELECT * FROM TD_RowNormalizeTransform (
        ON test_data AS InputTable
        ON rownorm_fit AS FitTable DIMENSION
        USING
        Accumulate('id')
    ) AS dt
) WITH DATA;

-- Step 5: Train model on normalized data
-- Step 6: Validate and evaluate
```

### Row Normalization Transformation Process

**Before Transformation (FRACTION approach):**
```
id  a     b     c     d
1   30    50    15    5      (sum = 100)
2   10    20    60    10     (sum = 100)
```

**After Transformation:**
```
id  a      b      c      d
1   0.30   0.50   0.15   0.05   (sum = 1.0)
2   0.10   0.20   0.60   0.10   (sum = 1.0)
```

**Before Transformation (UNITVECTOR approach):**
```
id  x    y    z
1   3    4    0      (L2 norm = 5)
2   1    0    0      (L2 norm = 1)
```

**After Transformation:**
```
id  x      y      z
1   0.60   0.80   0.00   (L2 norm = 1)
2   1.00   0.00   0.00   (L2 norm = 1)
```

**Key Transformation Characteristics:**
- Values scaled within each row independently
- Row relationships preserved (proportions, magnitudes)
- Original column names retained
- All output columns are DOUBLE PRECISION
- Accumulate columns passed through unchanged

### Use Cases and Applications

**1. Text Analytics and Document Similarity**
- Normalize TF-IDF vectors for cosine similarity
- Create comparable document representations
- Enable semantic search and clustering
- Prepare for recommendation systems

**2. Compositional Data Analysis**
- Analyze data representing parts of a whole
- Geological and chemical composition studies
- Microbiome abundance analysis
- Budget and resource allocation analysis

**3. Portfolio and Financial Analysis**
- Convert asset holdings to percentage allocations
- Compare portfolio compositions
- Analyze allocation changes over time
- Risk and return attribution analysis

**4. Image Processing and Computer Vision**
- Normalize pixel intensities per image
- Remove lighting variation effects
- Create comparable image features
- Enable image similarity search

**5. Survey and Questionnaire Analysis**
- Ipsative scoring (within-person normalization)
- Remove response style bias
- Analyze relative preferences
- Understand priority rankings

**6. Gene Expression and Bioinformatics**
- Normalize expression within samples
- Remove technical batch effects
- Enable cross-sample comparisons
- Differential expression analysis

**7. Market Basket and Transaction Analysis**
- Analyze item composition per transaction
- Identify purchasing patterns
- Calculate product associations
- Bundling and cross-sell analysis

**8. Budget and Spend Analysis**
- Convert absolute amounts to percentages
- Compare departmental allocations
- Track spending priorities over time
- Benchmark against peers

**9. Time Series and Economic Indicators**
- Create price and performance indices
- Analyze relative changes over time
- Economic benchmarking
- Track indicator movements

**10. Recommendation and Collaborative Filtering**
- Normalize user-item interaction data
- Create user preference profiles
- Calculate item similarities
- Enable collaborative filtering

### Important Notes

**Train-Test Consistency:**
- Always create FitTable using only training data
- Apply same FitTable to training, validation, and test sets
- Never fit on test data to prevent data leakage
- Store FitTable with model artifacts for production

**Output Data Types:**
- All normalized columns are DOUBLE PRECISION
- Original column names preserved
- Accumulate columns retain original types
- Consider downstream precision requirements

**NULL Handling:**
- NULL values in target columns cause transformation errors
- Remove or impute NULLs before transformation
- Use TD_SimpleImputeFit/Transform for imputation
- All target columns must be non-NULL

**Approach-Specific Results:**
- **UNITVECTOR**: Each row has L2 norm = 1
- **FRACTION**: Each row sums to 1.0
- **PERCENTAGE**: Each row sums to 100.0
- **INDEX**: Base column/value = BaseValue (typically 100)

**Zero-Sum Rows:**
- FRACTION/PERCENTAGE: Undefined if row sum = 0
- UNITVECTOR: Undefined if all values = 0
- INDEX: Undefined if base value = 0
- Handle edge cases in data preparation

**Negative Values:**
- UNITVECTOR: Handles negatives correctly
- FRACTION/PERCENTAGE: Typically require non-negative values
- INDEX: Works with negatives if base non-zero
- Validate data characteristics match approach

**Computational Performance:**
- Row-wise operations are efficient
- PARTITION BY ANY enables parallel processing
- Scales well to large datasets
- Minimal memory overhead

**Comparison to Column Normalization:**
- Row normalization: within-observation scaling
- Column normalization (TD_ScaleTransform): within-feature scaling
- Different analytical objectives
- Not interchangeable

### Best Practices

**1. Consistent Transformation Across Datasets**
- Create FitTable on training data only
- Apply to all datasets (train, validation, test, production)
- Store FitTable with model version control
- Document normalization approach and rationale

**2. Data Preparation Before Transformation**
- Impute missing values first
- Validate data characteristics (non-negative for FRACTION/PERCENTAGE)
- Check for zero-sum or all-zero rows
- Handle outliers appropriately

**3. Validate Transformation Results**
- Verify row sums/norms match expectations
- Check for NaN or Inf values
- Compare input/output distributions
- Test on sample data first

**4. Choose Appropriate Approach**
- UNITVECTOR for similarity/distance calculations
- FRACTION/PERCENTAGE for compositional data
- INDEX for time series and benchmarking
- Match approach to analytical goals

**5. Handle Edge Cases**
- Implement checks for zero sums/norms
- Handle negative values appropriately
- Manage extreme value ratios (INDEX)
- Test with boundary conditions

**6. Production Deployment**
- Store FitTable with trained model
- Validate FitTable compatibility before scoring
- Implement input validation
- Monitor for transformation issues

**7. Combine with Other Transformations**
- May combine with column scaling
- Consider transformation order
- Document complete pipeline
- Test combined effects

**8. Monitor Downstream Impact**
- Track model performance after normalization
- Compare to unnormalized baseline
- Validate business impact
- Adjust approach if needed

**9. Documentation and Governance**
- Document normalization approach and parameters
- Record BaseColumn/BaseValue choices
- Maintain transformation specifications
- Enable reproducibility and auditing

**10. Performance Optimization**
- Use PARTITION BY ANY for parallel processing
- Consider incremental transformation for large data
- Monitor query performance
- Optimize for production latency

### Related Functions
- **TD_RowNormalizeFit** - Creates row normalization specifications (must be run before TD_RowNormalizeTransform)
- **TD_ScaleTransform** - Column-wise normalization (alternative approach)
- **TD_SimpleImputeFit** - Handle missing values before normalization
- **TD_SimpleImputeTransform** - Apply imputation

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Transform Functions
