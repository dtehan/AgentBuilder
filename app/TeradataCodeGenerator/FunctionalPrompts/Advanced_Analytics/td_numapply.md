# TD_NumApply

### Function Name
**TD_NumApply**

### Description
TD_NumApply applies specified numeric operators (mathematical transformations) to input table columns, enabling element-wise transformation of numeric data through functions like exponential, logarithmic, sigmoid, inverse hyperbolic sine, and hyperbolic tangent. This function provides essential mathematical operations for feature engineering, data normalization, and preparing numeric data for machine learning and statistical analysis workflows.

The function supports five powerful numeric operators that address common data transformation needs: EXP for exponential growth/decay modeling, LOG for handling skewed distributions and normalizing scale, SIGMOID for bounded transformations and neural network activations, SININV for variance stabilization, and TANH for bounded non-linear transformations. Each operator is applied element-wise to every value in the specified target columns, enabling efficient batch transformation of large datasets through Teradata's parallel processing architecture.

TD_NumApply seamlessly integrates into data preprocessing pipelines, offering both in-place transformation (replacing original values) and additive transformation (creating new columns alongside originals). The function's parallel processing capabilities make it highly efficient for transforming millions of rows, while its flexible parameter system allows precise control over transformation behavior, column naming, and output structure. This makes it indispensable for data scientists and engineers who need to apply standardmathematical transformations as part of feature engineering and data preparation workflows.

### When the Function Would Be Used
- **Feature Engineering**: Apply mathematical transformations to create model-ready features
- **Data Normalization**: Transform skewed distributions to more normal distributions
- **Neural Network Preparation**: Apply activation functions for deep learning preprocessing
- **Exponential Modeling**: Model growth, decay, and compound interest scenarios
- **Log Transformation**: Handle right-skewed data and stabilize variance
- **Sigmoid Transformation**: Bound values to (0, 1) range for probability-like features
- **Variance Stabilization**: Apply SININV to stabilize variance across ranges
- **Non-Linear Features**: Create non-linear transformations for ML algorithms
- **Scale Normalization**: Bring features to comparable scales
- **Multiplicative to Additive**: Convert multiplicative relationships to additive via LOG
- **Activation Functions**: Prepare features using neural network activation functions
- **Domain Transformation**: Transform features to appropriate domains for modeling
- **Outlier Dampening**: Reduce impact of extreme values through transformations
- **Percentage Change**: Model percent change and multiplicative factors

### Syntax

```sql
TD_NumApply (
    ON { table | view | (query) } AS InputTable [ PARTITION BY ANY [ ORDER BY order_column ] ]
    USING
    TargetColumns ({ 'target_column' | target_column_range }[,...])
    [ OutputColumns ('output_column' [,...]) ]
    [ Accumulate ({ 'accumulate_column' | accumulate_column_range }[,...]) ]
    ApplyMethod ('num_operator')
    [ SigmoidStyle ({ 'logit' | 'modifiedlogit' | 'tanh' )]
    [ InPlace ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'})]
)
```

### Required Syntax Elements for TD_NumApply

**ON clause (InputTable)**
- Accepts the InputTable clause containing numeric data to transform
- Supports PARTITION BY ANY for parallel processing
- Optional ORDER BY for ordered processing

**TargetColumns**
- Specify names of InputTable columns to apply numeric operator
- Must be numeric data types
- Supports column range notation
- Supports multiple columns for batch transformation

**ApplyMethod**
- Specify the numeric operator to apply
- Valid values:
  - **'EXP'**: Exponential function (e^x), raises e to power of value
  - **'LOG'**: Base 10 logarithm, computes log₁₀(x)
  - **'SIGMOID'**: Sigmoid function, bounded (0, 1) transformation
  - **'SININV'**: Inverse hyperbolic sine (arcsinh), variance stabilization
  - **'TANH'**: Hyperbolic tangent, bounded (-1, 1) transformation

### Optional Syntax Elements for TD_NumApply

**OutputColumns**
- Specify names for output columns (ignored with InPlace='true')
- One output_column per target_column
- Maximum 128 characters per column name
- Default: target_column_operator (e.g., age_exp, income_log)
- Required if default name exceeds 128 characters

**Accumulate**
- Specify InputTable columns to copy to output table
- Preserves identifiers, keys, and metadata
- Supports column range notation
- With InPlace='true', no target_column can be accumulate_column

**SigmoidStyle**
- Specify sigmoid function variant (required with ApplyMethod='sigmoid')
- Valid values:
  - **'logit'**: Standard logistic sigmoid, f(x) = 1 / (1 + e^(-x))
  - **'modifiedlogit'**: Modified logistic sigmoid
  - **'tanh'**: Tanh-based sigmoid variant
- Default: 'logit'

**InPlace**
- Specify whether to replace original values or create new columns
- **'true'**: Replace target column values with transformed values
- **'false'**: Copy target columns and add new transformed columns
- With InPlace='true', no target_column can be accumulate_column
- Default: 'true'

### Input Table Schema

**InputTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | NUMERIC (INTEGER, BIGINT, FLOAT, DOUBLE PRECISION, DECIMAL, NUMERIC) | Columns to which to apply num_operator |
| accumulate_column | ANY | [Optional] Columns to preserve in output |

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| accumulate_column | Same as InputTable | Columns copied from InputTable |
| output_column | Same as InputTable | Transformed columns (name depends on InPlace setting) |

With InPlace='true', output_column is target_column (values replaced).
With InPlace='false', output_column is specified by OutputColumns or defaults to target_column_operator.

### Code Examples

**Input Data: passenger_data**
```
passenger_id  age  fare     height_cm
1             22   7.25     170.5
2             38   71.28    165.2
3             26   7.93     172.8
4             35   53.10    168.3
5             35   8.05     175.1
```

**Example 1: LOG Transformation (Handle Skewed Data)**
```sql
-- Apply log transformation to fare column (right-skewed)
SELECT * FROM TD_NumApply (
    ON passenger_data AS InputTable PARTITION BY ANY
    USING
    TargetColumns ('fare')
    ApplyMethod ('LOG')
    Accumulate ('passenger_id', 'age')
    InPlace ('false')
    OutputColumns ('fare_log')
) AS dt
ORDER BY passenger_id;
```

**Output:**
```
passenger_id  age  fare     fare_log
1             22   7.25     0.860
2             38   71.28    1.853
3             26   7.93     0.899
4             35   53.10    1.725
5             35   8.05     0.906
```

**Use Case**: Log transformation normalizes right-skewed fare distribution for modeling.

**Example 2: EXP Transformation (Exponential Growth)**
```sql
-- Apply exponential transformation for growth modeling
SELECT * FROM TD_NumApply (
    ON growth_rates AS InputTable PARTITION BY ANY
    USING
    TargetColumns ('growth_rate')
    ApplyMethod ('EXP')
    Accumulate ('year', 'region')
    InPlace ('false')
    OutputColumns ('growth_multiplier')
) AS dt;

-- Converts growth rates to multipliers (e^r)
-- Example: 0.05 growth rate → 1.0513 multiplier (5.13% growth)
```

**Example 3: SIGMOID Transformation (Bound to 0-1)**
```sql
-- Apply sigmoid to create probability-like features
SELECT * FROM TD_NumApply (
    ON feature_data AS InputTable PARTITION BY ANY
    USING
    TargetColumns ('raw_score')
    ApplyMethod ('SIGMOID')
    SigmoidStyle ('logit')
    Accumulate ('customer_id')
    InPlace ('false')
    OutputColumns ('prob_score')
) AS dt;

-- Transforms unbounded scores to (0, 1) range
-- Useful for creating probability-like features from raw scores
```

**Example 4: Multiple Columns with LOG**
```sql
-- Apply log transformation to multiple skewed features
SELECT * FROM TD_NumApply (
    ON skewed_features AS InputTable PARTITION BY ANY
    USING
    TargetColumns ('income', 'house_value', 'loan_amount')
    ApplyMethod ('LOG')
    Accumulate ('customer_id')
    InPlace ('true')  -- Replace original values
) AS dt;

-- Transforms all three right-skewed features in place
-- income, house_value, loan_amount now contain log-transformed values
```

**Example 5: TANH Transformation (Bound to -1 to 1)**
```sql
-- Apply tanh for bounded non-linear transformation
SELECT * FROM TD_NumApply (
    ON normalized_features AS InputTable PARTITION BY ANY
    USING
    TargetColumns ('feature1', 'feature2', 'feature3')
    ApplyMethod ('TANH')
    Accumulate ('observation_id', 'target')
    InPlace ('false')
    OutputColumns ('feature1_tanh', 'feature2_tanh', 'feature3_tanh')
) AS dt;

-- Creates tanh-transformed features bounded to (-1, 1)
-- Useful as neural network activation or non-linear feature
```

**Example 6: SININV for Variance Stabilization**
```sql
-- Apply inverse hyperbolic sine for variance stabilization
SELECT * FROM TD_NumApply (
    ON count_data AS InputTable PARTITION BY ANY
    USING
    TargetColumns ('event_count', 'page_views', 'clicks')
    ApplyMethod ('SININV')
    Accumulate ('user_id', 'date')
    InPlace ('false')
) AS dt;

-- SININV stabilizes variance for count data
-- Similar to LOG but handles zeros and negative values
```

**Example 7: Complete Feature Engineering Pipeline**
```sql
-- Step 1: Log-transform skewed features
CREATE TABLE features_log AS (
    SELECT * FROM TD_NumApply (
        ON raw_features AS InputTable PARTITION BY ANY
        USING
        TargetColumns ('income', 'debt', 'assets')
        ApplyMethod ('LOG')
        Accumulate ('customer_id', 'age', 'credit_score')
        InPlace ('false')
        OutputColumns ('income_log', 'debt_log', 'assets_log')
    ) AS dt
) WITH DATA;

-- Step 2: Apply sigmoid to create bounded features
CREATE TABLE features_engineered AS (
    SELECT * FROM TD_NumApply (
        ON features_log AS InputTable PARTITION BY ANY
        USING
        TargetColumns ('credit_score')
        ApplyMethod ('SIGMOID')
        SigmoidStyle ('logit')
        Accumulate ('[:]')  -- All columns
        InPlace ('false')
        OutputColumns ('credit_score_sigmoid')
    ) AS dt
) WITH DATA;

-- Result: Log-transformed financial features + sigmoid credit score
```

**Example 8: Neural Network Feature Preparation**
```sql
-- Apply tanh activation for neural network features
SELECT * FROM TD_NumApply (
    ON scaled_features AS InputTable PARTITION BY ANY
    USING
    TargetColumns ('[3:52]')  -- 50 numeric features
    ApplyMethod ('TANH')
    Accumulate ('id', 'target')
    InPlace ('true')
) AS dt;

-- Applies tanh activation to all features
-- Common preprocessing for neural network hidden layers
```

**Example 9: Exponential Decay Modeling**
```sql
-- Model time decay using exponential function
SELECT
    event_id,
    days_ago,
    -days_ago * 0.1 AS decay_rate,
    weight
FROM TD_NumApply (
    ON events AS InputTable PARTITION BY ANY
    USING
    TargetColumns ('decay_rate')  -- Created in SELECT
    ApplyMethod ('EXP')
    Accumulate ('event_id', 'days_ago')
    InPlace ('false')
    OutputColumns ('weight')
) AS dt;

-- Applies exponential decay: weight = e^(-0.1 * days_ago)
-- Recent events have weight near 1.0, old events near 0
```

**Example 10: Handle Different Sigmoid Styles**
```sql
-- Compare different sigmoid transformations
-- Standard logistic sigmoid
CREATE TABLE sigmoid_logit AS (
    SELECT * FROM TD_NumApply (
        ON raw_data AS InputTable PARTITION BY ANY
        USING
        TargetColumns ('raw_value')
        ApplyMethod ('SIGMOID')
        SigmoidStyle ('logit')
        Accumulate ('id')
        InPlace ('false')
        OutputColumns ('sigmoid_logit')
    ) AS dt
) WITH DATA;

-- Tanh-based sigmoid
CREATE TABLE sigmoid_tanh AS (
    SELECT * FROM TD_NumApply (
        ON raw_data AS InputTable PARTITION BY ANY
        USING
        TargetColumns ('raw_value')
        ApplyMethod ('SIGMOID')
        SigmoidStyle ('tanh')
        Accumulate ('id')
        InPlace ('false')
        OutputColumns ('sigmoid_tanh')
    ) AS dt
) WITH DATA;

-- Different sigmoid styles produce different value ranges and shapes
```

### Numeric Operators Explained

**1. EXP (Exponential Function)**

**Formula**: f(x) = e^x (where e ≈ 2.71828)

**Range**: (0, +∞) for all real x

**Use Cases**:
- Exponential growth and decay modeling
- Compound interest calculations
- Population growth projections
- Radioactive decay modeling
- Probability density functions

**Example**:
```
x = 0    → e^0 = 1.000
x = 1    → e^1 = 2.718
x = 2    → e^2 = 7.389
x = -1   → e^(-1) = 0.368
```

**2. LOG (Base 10 Logarithm)**

**Formula**: f(x) = log₁₀(x)

**Domain**: x > 0 (undefined for x ≤ 0)

**Range**: (-∞, +∞)

**Use Cases**:
- Transform right-skewed distributions
- Normalize scale for features with wide ranges
- Convert multiplicative effects to additive
- Linearize exponential relationships
- Handle features spanning multiple orders of magnitude

**Example**:
```
x = 1     → log₁₀(1) = 0.000
x = 10    → log₁₀(10) = 1.000
x = 100   → log₁₀(100) = 2.000
x = 1000  → log₁₀(1000) = 3.000
```

**Benefits**:
- Brings extreme values closer together
- Makes skewed data more normal
- Enables fair comparison across scales

**3. SIGMOID (Logistic Function)**

**Formula**: f(x) = 1 / (1 + e^(-x))

**Range**: (0, 1) for all real x

**Properties**:
- f(0) = 0.5
- f(-∞) → 0
- f(+∞) → 1
- Symmetric around x = 0

**Use Cases**:
- Neural network activation functions
- Probability modeling and calibration
- Bounded feature transformation
- Classification model outputs
- Smooth thresholding functions

**Example**:
```
x = -5   → 0.007 (near 0)
x = -2   → 0.119
x = 0    → 0.500
x = 2    → 0.881
x = 5    → 0.993 (near 1)
```

**4. SININV (Inverse Hyperbolic Sine / arcsinh)**

**Formula**: f(x) = sinh^(-1)(x) = ln(x + √(x² + 1))

**Domain**: All real numbers

**Range**: All real numbers

**Use Cases**:
- Variance stabilization for count data
- Similar to LOG but handles zero and negative values
- Transform data with mixed positive/negative values
- Alternative to LOG when zeros present
- Stabilize heteroscedastic variance

**Example**:
```
x = -10  → -2.998
x = 0    → 0.000
x = 10   → 2.998
x = 100  → 5.298
```

**Benefits**:
- Similar properties to LOG for large positive values
- Handles zeros (log(0) undefined, sinh^(-1)(0) = 0)
- Handles negative values (log(x<0) undefined)

**5. TANH (Hyperbolic Tangent)**

**Formula**: f(x) = (e^x - e^(-x)) / (e^x + e^(-x))

**Range**: (-1, 1) for all real x

**Properties**:
- f(0) = 0
- f(-∞) → -1
- f(+∞) → 1
- Odd function: f(-x) = -f(x)

**Use Cases**:
- Neural network activation functions
- Zero-centered bounded transformation
- Non-linear feature creation
- Alternative to sigmoid for centered data
- Hidden layer activations in feedforward networks

**Example**:
```
x = -3   → -0.995 (near -1)
x = -1   → -0.762
x = 0    → 0.000
x = 1    → 0.762
x = 3    → 0.995 (near 1)
```

### Use Cases and Applications

**1. Feature Engineering for Machine Learning**
- Create non-linear features from linear ones
- Transform skewed features for better model performance
- Generate activation-like features for neural networks
- Normalize feature scales and distributions

**2. Data Normalization and Preprocessing**
- Handle right-skewed distributions (income, prices)
- Transform exponential growth to linear
- Bring features to comparable scales
- Prepare data for linear models and algorithms

**3. Neural Network Preparation**
- Apply activation functions to features
- Create tanh-transformed features for hidden layers
- Generate sigmoid outputs for classification
- Preprocess features for deep learning

**4. Financial and Economic Modeling**
- Model compound interest and growth
- Transform price data to log returns
- Calculate exponential decay factors
- Model time value of money

**5. Scientific and Engineering Applications**
- Radioactive decay calculations
- Population growth modeling
- Chemical reaction kinetics
- Signal processing transformations

**6. Statistical Analysis**
- Variance stabilization with SININV
- Transform data to meet normality assumptions
- Handle heteroscedasticity
- Linearize relationships

**7. Count Data Transformation**
- Transform counts with LOG or SININV
- Handle zero counts (SININV advantage)
- Stabilize variance for Poisson-like data
- Prepare count features for regression

**8. Outlier Dampening**
- Reduce impact of extreme values with LOG
- Bound extreme values with SIGMOID or TANH
- Make distributions more symmetric
- Improve model robustness

**9. Probability Modeling**
- Transform scores to probability-like values (SIGMOID)
- Create bounded probability features
- Calibrate model outputs
- Smooth binary indicators

**10. Domain-Specific Transformations**
- Convert exponential relationships to linear (LOG)
- Model growth and decay processes (EXP)
- Create bounded indicators (SIGMOID, TANH)
- Transform between domains (linear → log → exponential)

### Important Notes

**Mathematical Domain Restrictions:**
- **LOG**: Requires x > 0 (undefined for x ≤ 0)
- **EXP**: Accepts all x but can overflow for very large x
- **SIGMOID, TANH**: Accept all real x
- **SININV**: Accepts all real x (advantage over LOG)
- Validate data ranges before transformation

**Numerical Stability:**
- EXP can cause overflow for large positive values
- LOG undefined for zero and negative values
- Consider replacing zeros with small positive values before LOG
- Or use SININV as alternative to handle zeros

**InPlace vs New Columns:**
- InPlace='true' replaces original values (destructive)
- InPlace='false' creates new columns (preserves originals)
- Preserve originals for debugging and validation
- Consider storage tradeoffs

**Column Naming:**
- Default naming: target_column_operator (e.g., income_log)
- Specify OutputColumns if default exceeds 128 characters
- Use descriptive names for clarity
- Follow naming conventions

**Performance Considerations:**
- Parallel processing with PARTITION BY ANY
- Efficient element-wise transformations
- Scales well to large datasets
- Minimal memory overhead

**Transformation Reversibility:**
- EXP and LOG are inverse operations
- SIGMOID and TANH are not easily reversible
- Consider if inverse transformation needed
- Document transformation for reproducibility

**Use with Other Transformations:**
- Often combined with scaling (TD_ScaleTransform)
- May precede or follow other feature engineering
- Consider transformation order carefully
- Test transformation pipeline thoroughly

**Data Type Preservation:**
- Output columns have same data type as input
- Consider precision for DECIMAL/NUMERIC types
- Verify sufficient precision for transformed values
- Monitor for precision loss

### Best Practices

**1. Validate Input Ranges**
- Check for zeros/negatives before LOG
- Validate expected value ranges
- Handle edge cases explicitly
- Test with sample data first

**2. Preserve Original Features**
- Use InPlace='false' to keep originals
- Enables comparison and validation
- Supports debugging and analysis
- Facilitates reversibility

**3. Document Transformations**
- Record which operator applied to which columns
- Document rationale for transformation choice
- Maintain transformation specifications
- Enable reproducibility

**4. Choose Appropriate Operators**
- LOG for right-skewed distributions
- EXP for growth/decay modeling
- SIGMOID for bounded (0,1) transformations
- TANH for bounded (-1,1) transformations
- SININV for variance stabilization with zeros

**5. Handle Edge Cases**
- Replace zeros before LOG (add small constant)
- Or use SININV for data with zeros
- Validate no undefined values
- Test extreme values

**6. Use Descriptive Column Names**
- Specify meaningful OutputColumns names
- Follow naming conventions
- Document purpose in data dictionary
- Enable easy interpretation

**7. Combine with Data Validation**
- Validate transformation results
- Check for NaN, Inf, NULL values
- Verify expected value ranges
- Compare distributions before/after

**8. Integrate into Pipelines**
- Apply early in feature engineering pipeline
- Before scaling and normalization
- Test transformation order
- Validate end-to-end results

**9. Monitor Performance**
- Profile execution time on large datasets
- Optimize partitioning strategy
- Consider batch processing for very large data
- Monitor resource utilization

**10. Test Transformation Impact**
- Validate model performance with/without transformation
- Compare multiple transformation strategies
- Test on holdout data
- Select based on validation metrics

### Related Functions
- **TD_StrApply** - Apply string operators to text columns
- **TD_ScaleTransform** - Feature scaling and normalization
- **TD_FunctionFit / TD_FunctionTransform** - Custom user-defined transformations
- **TD_PolynomialFeaturesTransform** - Polynomial feature generation
- **LOG() / EXP()** - SQL built-in math functions (alternative for simple cases)

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Utility Functions
