# TD_FunctionTransform

### Function Name
**TD_FunctionTransform**

### Description
TD_FunctionTransform applies numeric transformations to input columns using the TD_FunctionFit output. This function performs the actual mathematical transformations on data, converting values according to the specifications defined in the fit table. The transformations help normalize data, capture non-linear relationships, reduce skewness, and prepare features for machine learning models.

By transforming columns of data into new variables that capture important information, machine learning models can make better predictions and achieve better performance across a wide range of applications.

### When the Function Would Be Used
- **Feature Engineering**: Create transformed features for machine learning models
- **Data Normalization**: Standardize data distributions for better model performance
- **Handling Non-linearity**: Transform features to capture non-linear patterns
- **Skewness Reduction**: Apply log or power transformations to balance distributions
- **Outlier Mitigation**: Use sigmoid or tanh to compress extreme values
- **Scale Adjustment**: Normalize features to similar ranges
- **Variance Stabilization**: Address heteroscedasticity in regression models
- **Growth Rate Calculation**: Apply exponential transformations for time series
- **Distance Metrics**: Use absolute value for error calculations
- **Neural Network Preparation**: Apply sigmoid/tanh activations to input features

### Syntax
```sql
TD_FunctionTransform (
    ON { table | view | (query) } AS InputTable
    ON { table | view | (query) } AS FitTable DIMENSION
    USING
    [ IDColumns ({ 'id_column' | id_column_range }[,...])]
)
```

### Required Syntax Elements for TD_FunctionTransform

**ON clause (InputTable)**
- Accepts the InputTable clause containing data to transform
- Must have same structure as data used for TD_FunctionFit

**ON clause (FitTable DIMENSION)**
- Accepts the FitTable clause (output from TD_FunctionFit)
- Contains transformation specifications and parameters

### Optional Syntax Elements for TD_FunctionTransform

**IDColumns**
- Specify names of InputTable columns with NUMERIC datatypes to exclude from transformations
- VARCHAR columns are automatically excluded
- No id_column can be a target_column in the TransformationTable used for TD_FunctionFit
- Useful for preserving identifiers and metadata columns

### Input Table Schema

**InputTable Schema**

| Column | Data Type | Description |
|--------|-----------|-------------|
| input_column | NUMERIC or VARCHAR | Column to potentially transform. NUMERIC columns are transformed based on FitTable, VARCHAR columns automatically excluded |
| id_column | NUMERIC | [Optional] Column to exclude from transformation via IDColumns parameter |

**FitTable Schema**

See TD_FunctionFit Output table schema. This is the output created by TD_FunctionFit function.

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| input_column | If NUMERIC in TD_FunctionFit InputTable: DOUBLE PRECISION<br>Otherwise: Same as in TD_FunctionFit InputTable | Transformed values or original values if not transformed |

### Code Examples

**Input Table: function_input_table**
```
passenger  survived  pclass  name                                               gender  age  sibsp  parch  fare
1          0         3       Braund; Mr. Owen Harris                            male    22   1      0      7.250000000
2          1         1       Cumings; Mrs. John Bradley (Florence Briggs Thayer) female  38   1      0      71.283300000
3          1         3       Heikkinen; Miss. Laina                             female  26   0      0      7.925000000
4          1         1       Futrelle; Mrs. Jacques Heath (Lily May Peel)       female  35   1      0      53.100000000
5          0         3       Allen; Mr. William Henry                           male    35   0      0      8.050000000
```

**FitTable: fit_out** (created by TD_FunctionFit)
```
TargetColumn  Transformation  Parameters          Defaultvalue
age           LOG             {"base":2}          0.000000000
fare          POW             {"exponent": 2}     10.000000000
```

**Example 1: Apply Log and Power Transformations**
```sql
SELECT * FROM TD_FunctionTransform (
    ON function_input_table AS InputTable
    ON fit_out AS FitTable DIMENSION
    USING
    IDColumns ('[0:2]','[6:7]')  -- Exclude passenger, survived, pclass, sibsp, parch
) AS dt
ORDER BY Passenger;
```

**Output:**
```
passenger  survived  pclass  name                                               gender  age                  sibsp  parch  fare
1          0         3       Braund; Mr. Owen Harris                            male    4.45943161863730E000  1      0      5.25625000000000E001
2          1         1       Cumings; Mrs. John Bradley (Florence Briggs Thayer) female  5.24792751344359E000  1      0      5.08130885889000E003
3          1         3       Heikkinen; Miss. Laina                             female  4.70043971814109E000  0      0      6.28056250000000E001
4          1         1       Futrelle; Mrs. Jacques Heath (Lily May Peel)       female  5.12928301694497E000  1      0      2.81961000000000E003
5          0         3       Allen; Mr. William Henry                           male    5.12928301694497E000  0      0      6.48025000000000E001
```

**Example 2: Natural Log Transformation**
```sql
-- First create fit table with TD_FunctionFit
CREATE TABLE log_fit AS (
    SELECT * FROM TD_FunctionFit (
        ON sales_data AS InputTable
        ON log_spec AS TransformationTable DIMENSION
    ) AS dt
) WITH DATA;

-- Then apply transformation
SELECT * FROM TD_FunctionTransform (
    ON sales_data AS InputTable
    ON log_fit AS FitTable DIMENSION
    USING
    IDColumns ('transaction_id', 'customer_id', 'date')
) AS dt
ORDER BY transaction_id;
```

**Example 3: Sigmoid Transformation for Neural Network**
```sql
-- Apply sigmoid to normalize features to [0,1] range
SELECT * FROM TD_FunctionTransform (
    ON ml_features AS InputTable
    ON sigmoid_fit AS FitTable DIMENSION
    USING
    IDColumns ('id', 'label')
) AS dt;
```

**Example 4: Multiple Transformations on Different Columns**
```sql
-- Apply different transformations to different columns
SELECT * FROM TD_FunctionTransform (
    ON customer_metrics AS InputTable
    ON multi_transform_fit AS FitTable DIMENSION
    USING
    IDColumns ('customer_id', 'registration_date')
) AS dt
ORDER BY customer_id;
```

**Example 5: Absolute Value for Error Calculation**
```sql
-- Transform prediction errors to absolute values
SELECT * FROM TD_FunctionTransform (
    ON prediction_results AS InputTable
    ON abs_fit AS FitTable DIMENSION
    USING
    IDColumns ('model_id', 'prediction_id', 'actual_value', 'predicted_value')
) AS dt;
```

**Example 6: Exponential Transformation for Growth Rate**
```sql
-- Apply exponential transformation to log-normalized data
SELECT * FROM TD_FunctionTransform (
    ON normalized_returns AS InputTable
    ON exp_fit AS FitTable DIMENSION
    USING
    IDColumns ('stock_id', 'date')
) AS dt
ORDER BY stock_id, date;
```

**Example 7: TANH Transformation for Symmetric Normalization**
```sql
-- Apply tanh to map features to [-1, 1] range
SELECT * FROM TD_FunctionTransform (
    ON sentiment_features AS InputTable
    ON tanh_fit AS FitTable DIMENSION
    USING
    IDColumns ('document_id', 'category')
) AS dt;
```

**Example 8: Power Transformation for Variance Stabilization**
```sql
-- Apply square root transformation to stabilize variance
SELECT * FROM TD_FunctionTransform (
    ON count_data AS InputTable
    ON sqrt_fit AS FitTable DIMENSION
    USING
    IDColumns ('region_id', 'period')
) AS dt
ORDER BY region_id, period;
```

**Example 9: CEIL and FLOOR for Discretization**
```sql
-- Round values up or down for binning preparation
SELECT * FROM TD_FunctionTransform (
    ON grade_data AS InputTable
    ON round_fit AS FitTable DIMENSION
    USING
    IDColumns ('student_id', 'course_id')
) AS dt;
```

**Example 10: Complete ML Pipeline Example**
```sql
-- Step 1: Create fit table on training data
CREATE TABLE training_transform_fit AS (
    SELECT * FROM TD_FunctionFit (
        ON training_data AS InputTable
        ON transformation_spec AS TransformationTable DIMENSION
    ) AS dt
) WITH DATA;

-- Step 2: Transform training data
CREATE TABLE training_transformed AS (
    SELECT * FROM TD_FunctionTransform (
        ON training_data AS InputTable
        ON training_transform_fit AS FitTable DIMENSION
        USING
        IDColumns ('customer_id', 'target')
    ) AS dt
) WITH DATA;

-- Step 3: Transform test data using same transformations
CREATE TABLE test_transformed AS (
    SELECT * FROM TD_FunctionTransform (
        ON test_data AS InputTable
        ON training_transform_fit AS FitTable DIMENSION
        USING
        IDColumns ('customer_id')
    ) AS dt
) WITH DATA;
```

### Transformation Effects

**LOG Transformation**:
- Input: [1, 10, 100, 1000]
- Output (base 10): [0, 1, 2, 3]
- Effect: Compresses large values, expands small values

**POW Transformation (exponent = 2)**:
- Input: [1, 2, 3, 4]
- Output: [1, 4, 9, 16]
- Effect: Amplifies differences between values

**SIGMOID Transformation**:
- Input: [-5, 0, 5]
- Output: [0.007, 0.5, 0.993]
- Effect: Maps to (0, 1) range, compresses extremes

**TANH Transformation**:
- Input: [-5, 0, 5]
- Output: [-1.0, 0.0, 1.0]
- Effect: Maps to (-1, 1) range, symmetric

**ABS Transformation**:
- Input: [-5, -2, 0, 3, 7]
- Output: [5, 2, 0, 3, 7]
- Effect: All values become non-negative

**EXP Transformation**:
- Input: [0, 1, 2, 3]
- Output: [1, 2.718, 7.389, 20.086]
- Effect: Exponential growth pattern

### Use Cases and Applications

**1. Machine Learning Preprocessing**
- Normalize features for gradient descent algorithms
- Transform skewed features for better model performance
- Create non-linear features from linear ones
- Prepare data for distance-based algorithms

**2. Statistical Analysis**
- Satisfy normality assumptions for hypothesis tests
- Stabilize variance for ANOVA
- Transform data for linear regression
- Address heteroscedasticity

**3. Time Series Analysis**
- Log-transform for multiplicative models
- Transform to stationary series
- Normalize seasonal patterns
- Handle exponential growth trends

**4. Financial Modeling**
- Log-transform prices for returns calculation
- Normalize financial ratios
- Transform volatility measures
- Calculate growth rates

**5. Image Processing**
- Normalize pixel intensities
- Apply gamma correction (power transformation)
- Sigmoid for contrast adjustment
- Log transformation for dynamic range compression

**6. Natural Language Processing**
- Transform term frequencies (TF-IDF uses log)
- Normalize word embeddings
- Apply sigmoid to attention scores
- Transform probability distributions

### Important Notes
- Input data must have same structure as TD_FunctionFit input
- Transformations are applied based on FitTable specifications
- VARCHAR columns are automatically excluded from transformation
- Use IDColumns to preserve identifier and metadata columns
- Numeric columns become DOUBLE PRECISION after transformation
- Transformation is deterministic - same input produces same output
- NULL values are handled according to DefaultValue in FitTable
- Function applies transformations element-wise to each value
- Multiple columns can be transformed in single operation
- Same FitTable can be used on training and test data for consistency

### Best Practices

**1. Train-Test Consistency**
- Create FitTable on training data only
- Apply same FitTable to both training and test data
- This prevents data leakage

**2. Handle Missing Values First**
- Impute or remove NULLs before transformation
- Or specify appropriate DefaultValue in FitTable

**3. Understand Your Data**
- Check data distribution before choosing transformation
- Use TD_UnivariateStatistics and TD_Histogram
- Consider domain knowledge

**4. Validate Transformations**
- Check output ranges make sense
- Verify no unexpected NULL values
- Ensure transformations improve model performance

**5. Document Transformations**
- Keep clear records of which transformations were applied
- Store FitTable for reproducibility
- Document rationale for each transformation

**6. Consider Interpretability**
- Complex transformations reduce interpretability
- Balance performance vs. explainability
- Consider inverse transformations for predictions

### Related Functions
- **TD_FunctionFit** - Creates transformation specifications (must be run before TD_FunctionTransform)
- **TD_NumApply** - Alternative for applying numeric transformations
- **TD_ScaleTransform** - For standardization and min-max scaling
- **TD_BinCodeTransform** - For discretization of continuous variables

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Transform Functions
