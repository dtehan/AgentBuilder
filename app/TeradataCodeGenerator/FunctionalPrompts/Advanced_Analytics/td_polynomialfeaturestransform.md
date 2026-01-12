# TD_PolynomialFeaturesTransform

### Function Name
**TD_PolynomialFeaturesTransform**

### Description
TD_PolynomialFeaturesTransform applies polynomial feature generation using the specifications created by TD_PolynomialFeaturesFit. This function performs the actual transformation of numeric input features into polynomial combinations, including squares, cubes, and interaction terms based on the predefined rules in the FitTable.

This function is the execution component of the polynomial feature generation pipeline. After TD_PolynomialFeaturesFit defines the transformation metadata (which features to generate, their degree, whether to include bias), TD_PolynomialFeaturesTransform applies these rules to create the expanded feature matrix. The transformation generates new columns containing polynomial combinations of the original features, enabling linear models to capture non-linear relationships.

The polynomial transformation is deterministic and reproducible, ensuring consistent feature generation across training, validation, and test datasets when using the same FitTable. This consistency is critical for machine learning pipelines where features must be identically transformed across all data splits.

### When the Function Would Be Used
- **Apply Polynomial Transformations**: Execute polynomial feature generation on data
- **ML Pipeline Execution**: Transform training and test data consistently
- **Non-Linear Feature Generation**: Create polynomial basis for linear models
- **Production Scoring**: Transform incoming data for model predictions
- **Regression Modeling**: Prepare features for polynomial regression
- **Feature Expansion**: Increase feature space with polynomial terms
- **Interaction Capture**: Generate multiplicative feature combinations
- **Curve Fitting Applications**: Create polynomial basis functions
- **Scientific Modeling**: Apply polynomial transformations to experimental data
- **Consistent Preprocessing**: Ensure identical transformations across datasets

### Syntax

**Dense Input Format:**
```sql
TD_PolynomialFeaturesTransform (
    ON { table | view | (query) } AS InputTable [ PARTITION BY ANY ]
    ON { table | view | (query) } AS FitTable AS FitTableAlias DIMENSION
    USING
    [ Accumulate ({'accumulate_column' | 'accumulate_column_range'}[,...]) ]
)
```

### Required Syntax Elements for TD_PolynomialFeaturesTransform

**ON clause (InputTable)**
- Accepts the InputTable clause containing numeric data to transform
- Must have same structure and columns as data used for TD_PolynomialFeaturesFit
- PARTITION BY ANY recommended for parallel processing

**ON clause (FitTable DIMENSION)**
- Accepts the FitTable clause (output from TD_PolynomialFeaturesFit)
- Contains polynomial feature specifications and transformation rules
- DIMENSION keyword required

### Optional Syntax Elements for TD_PolynomialFeaturesTransform

**Accumulate**
- Specify input table column names to copy to the output table
- Useful for preserving identifiers, keys, and non-transformed columns
- Supports column range notation
- Typically includes ID columns and target variables

### Input Table Schema

**InputTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | Numeric types (INTEGER, BIGINT, SMALLINT, NUMERIC, DECIMAL, FLOAT, DOUBLE PRECISION) | Numeric columns specified in TD_PolynomialFeaturesFit TargetColumns |
| accumulate_column | ANY | [Optional] Columns to preserve in output table |

**FitTable Schema:**

See TD_PolynomialFeaturesFit Output table schema. This is the specification table created by TD_PolynomialFeaturesFit function.

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| accumulate_column | Same as InputTable | Columns specified in Accumulate parameter |
| polynomial_feature_columns | DOUBLE PRECISION | Generated polynomial feature columns as specified in FitTable |

The number and names of polynomial feature columns depend on the FitTable specifications (Degree, IncludeBias, InteractionOnly).

### Code Examples

**Input Data: polynomialFeaturesTransform_input**
```
id  x1    x2    target
1   2.0   3.0   15.5
2   4.0   1.0   18.2
3   1.5   2.5   12.8
4   3.5   4.0   22.1
5   2.5   3.5   17.9
```

**FitTable: poly_fit_degree2** (created by TD_PolynomialFeaturesFit)
```
-- Created with: TargetColumns('x1', 'x2'), Degree(2), IncludeBias('true')
-- Generates columns: [1, x1, x2, x1², x1·x2, x2²]
```

**Example 1: Basic Polynomial Transformation (Degree 2)**
```sql
-- Step 1: Create fit table (already done in TD_PolynomialFeaturesFit examples)
CREATE TABLE poly_fit_degree2 AS (
    SELECT * FROM TD_PolynomialFeaturesFit (
        ON polynomialFeaturesTransform_input AS InputTable
        USING
        TargetColumns('x1', 'x2')
        Degree(2)
        IncludeBias('true')
    ) AS dt
) WITH DATA;

-- Step 2: Apply transformation
SELECT * FROM TD_PolynomialFeaturesTransform (
    ON polynomialFeaturesTransform_input AS InputTable
    ON poly_fit_degree2 AS FitTable DIMENSION
    USING
    Accumulate('id', 'target')
) AS dt
ORDER BY id;
```

**Output:**
```
id  target  col_1  col_x1  col_x2  col_x1_x1  col_x1_x2  col_x2_x2
1   15.5    1.0    2.0     3.0     4.0        6.0        9.0
2   18.2    1.0    4.0     1.0     16.0       4.0        1.0
3   12.8    1.0    1.5     2.5     2.25       3.75       6.25
4   22.1    1.0    3.5     4.0     12.25      14.0       16.0
5   17.9    1.0    2.5     3.5     6.25       8.75       12.25
```

**Transformation Applied:** [x1, x2] → [1, x1, x2, x1², x1·x2, x2²]

**Example 2: Transform Training Data**
```sql
-- Transform training set with polynomial features
CREATE TABLE training_poly AS (
    SELECT * FROM TD_PolynomialFeaturesTransform (
        ON training_data AS InputTable
        ON poly_fit AS FitTable DIMENSION
        USING
        Accumulate('customer_id', 'target')
    ) AS dt
) WITH DATA;

-- Now ready for linear regression with non-linear features
```

**Example 3: Transform Test Data with Same FitTable**
```sql
-- Apply same polynomial transformation to test set
CREATE TABLE test_poly AS (
    SELECT * FROM TD_PolynomialFeaturesTransform (
        ON test_data AS InputTable
        ON poly_fit AS FitTable DIMENSION  -- Same FitTable as training
        USING
        Accumulate('customer_id')
    ) AS dt
) WITH DATA;

-- Ensures consistent feature generation across train/test
```

**Example 4: Degree 3 Polynomial Transformation**
```sql
-- Create degree 3 fit table
CREATE TABLE poly_fit_degree3 AS (
    SELECT * FROM TD_PolynomialFeaturesFit (
        ON sensor_data AS InputTable
        USING
        TargetColumns('temperature', 'pressure')
        Degree(3)
        IncludeBias('true')
    ) AS dt
) WITH DATA;

-- Apply degree 3 transformation
SELECT * FROM TD_PolynomialFeaturesTransform (
    ON sensor_data AS InputTable
    ON poly_fit_degree3 AS FitTable DIMENSION
    USING
    Accumulate('sensor_id', 'timestamp', 'alert_status')
) AS dt
ORDER BY sensor_id, timestamp;
```

**Output includes:** [1, temp, pres, temp², temp·pres, pres², temp³, temp²·pres, temp·pres², pres³]

**Example 5: Interaction Terms Only**
```sql
-- Create interaction-only fit table
CREATE TABLE poly_fit_interact AS (
    SELECT * FROM TD_PolynomialFeaturesFit (
        ON experiment_data AS InputTable
        USING
        TargetColumns('factor_a', 'factor_b', 'factor_c')
        Degree(2)
        IncludeBias('false')
        InteractionOnly('true')
    ) AS dt
) WITH DATA;

-- Apply interaction transformation
SELECT * FROM TD_PolynomialFeaturesTransform (
    ON experiment_data AS InputTable
    ON poly_fit_interact AS FitTable DIMENSION
    USING
    Accumulate('experiment_id', 'result')
) AS dt;
```

**Output includes:** [a, b, c, a·b, a·c, b·c] (no squared terms)

**Example 6: Ridge Regression Pipeline**
```sql
-- Complete polynomial regression pipeline
-- Step 1: Fit polynomial features (done previously)
-- Step 2: Transform training data
CREATE TABLE train_poly AS (
    SELECT * FROM TD_PolynomialFeaturesTransform (
        ON training_raw AS InputTable
        ON poly_fit AS FitTable DIMENSION
        USING
        Accumulate('id', 'sales')
    ) AS dt
) WITH DATA;

-- Step 3: Train ridge regression on polynomial features
CREATE TABLE ridge_model AS (
    SELECT * FROM TD_GLM (
        ON train_poly AS InputTable
        USING
        TargetColumn('sales')
        InputColumns('[2:]')  -- All polynomial features
        Family('GAUSSIAN')
        Alpha(0.1)  -- Ridge regularization
        LinkFunction('IDENTITY')
    ) AS dt
) WITH DATA;
```

**Example 7: Multiple Features with Polynomial Terms**
```sql
-- Transform with 4 features to degree 2
SELECT
    id,
    fare,
    col_1 AS bias,
    col_age AS age,
    col_fare_orig AS fare_orig,
    col_parch AS parch,
    col_sibsp AS sibsp,
    col_age_age AS age_squared,
    col_age_fare_orig AS age_fare_interaction,
    col_age_parch AS age_parch_interaction,
    col_age_sibsp AS age_sibsp_interaction,
    col_fare_orig_fare_orig AS fare_squared,
    col_fare_orig_parch AS fare_parch_interaction,
    col_fare_orig_sibsp AS fare_sibsp_interaction,
    col_parch_parch AS parch_squared,
    col_parch_sibsp AS parch_sibsp_interaction,
    col_sibsp_sibsp AS sibsp_squared
FROM TD_PolynomialFeaturesTransform (
    ON titanic_data AS InputTable
    ON poly_fit_4features AS FitTable DIMENSION
    USING
    Accumulate('id', 'fare')
) AS dt
ORDER BY id;
```

**Example 8: Production Scoring**
```sql
-- Score new customers using polynomial model
-- Step 1: Transform incoming data with stored FitTable
CREATE TABLE new_customers_poly AS (
    SELECT * FROM TD_PolynomialFeaturesTransform (
        ON new_customers AS InputTable
        ON poly_fit AS FitTable DIMENSION  -- Use production FitTable
        USING
        Accumulate('customer_id', 'customer_name')
    ) AS dt
) WITH DATA;

-- Step 2: Apply trained model for predictions
SELECT * FROM TD_GLMPredict (
    ON new_customers_poly AS InputTable
    ON ridge_model AS ModelTable DIMENSION
    USING
    IDColumn('customer_id')
    Accumulate('customer_name')
) AS dt;
```

**Example 9: Time Series Polynomial Trend**
```sql
-- Create polynomial trend features for forecasting
CREATE TABLE poly_fit_time AS (
    SELECT * FROM TD_PolynomialFeaturesFit (
        ON time_series AS InputTable
        USING
        TargetColumns('time_index')
        Degree(3)
        IncludeBias('true')
    ) AS dt
) WITH DATA;

-- Transform to create polynomial time trend
SELECT * FROM TD_PolynomialFeaturesTransform (
    ON time_series AS InputTable
    ON poly_fit_time AS FitTable DIMENSION
    USING
    Accumulate('date', 'value', 'time_index')
) AS dt
ORDER BY date;
```

**Output:** Creates polynomial time features [1, t, t², t³] for trend modeling

**Example 10: Complete ML Pipeline with Validation**
```sql
-- End-to-end polynomial regression pipeline
-- Step 1: Create polynomial fit on training data only
CREATE TABLE poly_fit AS (
    SELECT * FROM TD_PolynomialFeaturesFit (
        ON training_data AS InputTable
        USING
        TargetColumns('feature1', 'feature2', 'feature3')
        Degree(2)
        IncludeBias('true')
    ) AS dt
) WITH DATA;

-- Step 2: Transform training data
CREATE TABLE train_transformed AS (
    SELECT * FROM TD_PolynomialFeaturesTransform (
        ON training_data AS InputTable
        ON poly_fit AS FitTable DIMENSION
        USING
        Accumulate('id', 'target')
    ) AS dt
) WITH DATA;

-- Step 3: Transform validation data (same FitTable)
CREATE TABLE validation_transformed AS (
    SELECT * FROM TD_PolynomialFeaturesTransform (
        ON validation_data AS InputTable
        ON poly_fit AS FitTable DIMENSION
        USING
        Accumulate('id', 'target')
    ) AS dt
) WITH DATA;

-- Step 4: Transform test data (same FitTable)
CREATE TABLE test_transformed AS (
    SELECT * FROM TD_PolynomialFeaturesTransform (
        ON test_data AS InputTable
        ON poly_fit AS FitTable DIMENSION
        USING
        Accumulate('id', 'target')
    ) AS dt
) WITH DATA;

-- Step 5: Train model on train_transformed
-- Step 6: Validate on validation_transformed
-- Step 7: Final evaluation on test_transformed
```

### Polynomial Transformation Process

**Before Transformation:**
```
id  x1   x2
1   2.0  3.0
2   4.0  1.0
```

**After Transformation (Degree 2 with Bias):**
```
id  1    x1   x2   x1²   x1·x2  x2²
1   1.0  2.0  3.0  4.0   6.0    9.0
2   1.0  4.0  1.0  16.0  4.0    1.0
```

**Key Transformation Characteristics:**
- Original features preserved in output
- New polynomial columns added
- Bias column contains constant value 1.0
- Interaction terms are multiplicative combinations
- Square/cube terms are powers of original features
- Column names follow pattern: col_feature1_feature2

### Use Cases and Applications

**1. Non-Linear Regression**
- Enable linear models to fit non-linear patterns
- Polynomial regression for curve fitting
- Capture quadratic and cubic relationships
- Model diminishing returns and saturation effects

**2. Machine Learning Model Training**
- Prepare features for linear regression
- Ridge and Lasso regression with polynomial features
- Support Vector Machines with explicit polynomial kernel
- Gradient boosting with polynomial features

**3. Scientific and Engineering Modeling**
- Physics equations with polynomial relationships
- Chemical reaction kinetics modeling
- Stress-strain curve fitting
- Thermodynamic property modeling

**4. Economic and Financial Analysis**
- Model non-linear price-demand relationships
- Capture diminishing marginal utility
- Risk-return tradeoff curves
- Production function estimation

**5. Time Series Forecasting**
- Polynomial trend components
- Seasonal pattern modeling with polynomial basis
- Non-linear trend extrapolation
- Curve fitting for historical patterns

**6. Marketing and Sales Analytics**
- Advertising saturation effects
- Customer lifetime value curves
- Price optimization with non-linear response
- Marketing channel interaction effects

**7. Healthcare and Biostatistics**
- Dose-response curve modeling
- Growth curve analysis
- Pharmacokinetic modeling
- Disease progression patterns

**8. Environmental Modeling**
- Temperature-humidity interaction effects
- Pollution dispersion models
- Climate variable interactions
- Ecosystem variable relationships

**9. Quality Control and Manufacturing**
- Process optimization with interaction effects
- Response surface methodology
- Designed experiments with polynomial models
- Quality-parameter relationship modeling

**10. Customer Analytics and Segmentation**
- Non-linear customer behavior modeling
- Interaction effects in churn prediction
- Customer value scoring with polynomial features
- Propensity modeling with feature interactions

### Important Notes

**Train-Test Consistency:**
- Always create FitTable using only training data
- Apply same FitTable to training, validation, and test sets
- Never fit on test data to prevent data leakage
- Store FitTable with model artifacts for production

**Output Column Naming:**
- Generated columns follow pattern: col_feature1_feature2_...
- Bias column typically named: col_1
- Original feature columns: col_featurename
- Squared terms: col_featurename_featurename
- Interaction terms: col_feature1_feature2

**Data Type Handling:**
- All output polynomial features are DOUBLE PRECISION
- Input features must be numeric types
- Non-numeric columns must be accumulated (not transformed)
- NULL values in input features result in NULL polynomial features

**Feature Count:**
- Number of output columns depends on Degree, IncludeBias, InteractionOnly
- 2 features, degree 2, with bias = 6 columns
- 3 features, degree 2, with bias = 10 columns
- 5 features, degree 2, with bias = 21 columns
- Monitor feature count to avoid overfitting

**Computational Performance:**
- Transformation is computationally intensive
- High-degree polynomials increase processing time
- Large datasets may require distributed processing
- Use PARTITION BY ANY for parallel processing

**NULL Handling:**
- NULL values in input features propagate to polynomial features
- If x1 is NULL, x1², x1·x2, etc. will all be NULL
- Consider imputation before polynomial transformation
- Accumulate columns preserve NULL values unchanged

**Numerical Stability:**
- Large input values can cause overflow with high degrees
- Scale features before polynomial transformation (TD_ScaleFit/Transform)
- Monitor for numerical overflow warnings
- Consider standardization to prevent instability

**Memory and Storage:**
- Polynomial transformation increases data size significantly
- More features = larger output tables
- Monitor storage requirements for large datasets
- Consider sampling for very large datasets

### Best Practices

**1. Feature Scaling Before Transformation**
- Standardize features before polynomial transformation
- Use TD_ScaleFit and TD_ScaleTransform first
- Prevents numerical overflow and instability
- Ensures features on comparable scales

**2. Consistent Transformation Across Datasets**
- Create FitTable on training data only
- Apply to all datasets (train, validation, test)
- Store FitTable with model version control
- Document transformation specifications

**3. Monitor Feature Count**
- Avoid excessive feature explosion
- Start with lower degrees (degree 2)
- Use InteractionOnly when appropriate
- Select most important features for transformation

**4. Regularization Required**
- Always use regularization with polynomial features
- Ridge regression controls multicollinearity
- Lasso performs feature selection
- Validate on holdout data to detect overfitting

**5. Production Deployment**
- Store FitTable with trained model
- Validate FitTable compatibility before scoring
- Implement input validation for production data
- Monitor for numerical issues in production

**6. Feature Interpretability**
- Document polynomial feature meanings
- Maintain mapping from generated columns to formulas
- Consider visualization of polynomial effects
- Use model explanation tools (SHAP) for interpretability

**7. Validation and Testing**
- Test transformation on sample data first
- Verify output feature counts match expectations
- Compare train/test feature distributions
- Implement unit tests for transformation pipeline

**8. Handle Missing Data**
- Impute missing values before transformation
- Document imputation strategy
- Consider impact of NULLs on polynomial features
- Use TD_SimpleImputeFit/Transform before polynomial transform

**9. Performance Optimization**
- Use PARTITION BY ANY for parallel processing
- Consider incremental transformation for large datasets
- Monitor query performance and optimize
- Cache FitTable for repeated transformations

**10. Alternative Approaches**
- Consider splines for more flexible non-linear modeling
- Kernel SVM avoids explicit polynomial feature generation
- Tree-based models capture non-linearity without polynomials
- Neural networks learn transformations automatically

### Related Functions
- **TD_PolynomialFeaturesFit** - Creates polynomial feature specifications (must be run before TD_PolynomialFeaturesTransform)
- **TD_ScaleFit** - Feature scaling, recommended before polynomial transformation
- **TD_ScaleTransform** - Apply scaling to features
- **TD_GLM** - Generalized Linear Models for polynomial regression
- **TD_GLMPredict** - Score new data with GLM models
- **TD_SimpleImputeFit** - Handle missing values before transformation

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Transform Functions
