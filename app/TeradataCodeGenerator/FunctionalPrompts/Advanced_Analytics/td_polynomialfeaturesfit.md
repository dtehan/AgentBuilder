# TD_PolynomialFeaturesFit

### Function Name
**TD_PolynomialFeaturesFit**

### Description
TD_PolynomialFeaturesFit creates a specification table that defines how to generate polynomial features from input numeric columns. This function prepares the metadata and transformation rules for creating polynomial combinations, including interaction terms and higher-degree polynomial terms, which are then applied by TD_PolynomialFeaturesTransform.

Polynomial features are essential for capturing non-linear relationships in data by generating new features that are polynomial combinations of the original features. For example, given features [x, y], polynomial features of degree 2 would include [1, x, y, x², xy, y²]. These features enable linear models to learn non-linear patterns, making them particularly valuable for regression tasks where relationships between variables are inherently non-linear.

The function supports three key aspects of polynomial feature generation: the degree of polynomial terms (up to degree 3), whether to include interaction terms only, and whether to include a bias term (constant 1). The output specification table is then used by TD_PolynomialFeaturesTransform to perform the actual feature generation.

### When the Function Would Be Used
- **Non-Linear Regression**: Enable linear models to capture non-linear relationships
- **Feature Engineering**: Create polynomial and interaction features for ML pipelines
- **Model Improvement**: Enhance model performance by adding polynomial terms
- **Interaction Detection**: Generate cross-product terms to capture feature interactions
- **Curve Fitting**: Create polynomial basis for fitting non-linear curves
- **Ridge/Lasso Regression**: Generate polynomial features with regularization
- **SVM with Polynomial Kernel**: Explicit feature generation alternative
- **Scientific Modeling**: Physics, chemistry models with polynomial relationships
- **Time Series Forecasting**: Polynomial trend components
- **Data Transformation**: Prepare features for gradient boosting and tree models

### Syntax

**Dense Input Format:**
```sql
TD_PolynomialFeaturesFit (
    ON { table | view | (query) } AS InputTable
    USING
    TargetColumns ({ 'target_column' | target_column_range }[,...])
    [ Degree (degree_value) ]
    [ IncludeBias ('true' | 'false') ]
    [ InteractionOnly ('true' | 'false') ]
)
```

### Required Syntax Elements for TD_PolynomialFeaturesFit

**ON clause**
- Accepts the InputTable clause containing numeric columns
- Data is used only for schema validation, not for computation

**TargetColumns**
- Specify numeric columns from which to generate polynomial features
- Maximum 5 columns can be specified
- Supports column range notation
- Must be numeric data types (INTEGER, FLOAT, DOUBLE PRECISION, etc.)

### Optional Syntax Elements for TD_PolynomialFeaturesFit

**Degree**
- Specify maximum degree of polynomial features to generate
- Valid values: 1, 2, or 3
- Default: 2
- Degree 1: Original features only
- Degree 2: Original + squares + pairwise interactions
- Degree 3: Original + squares + cubes + all interaction terms

**IncludeBias**
- Specify whether to include bias column (constant value 1)
- Valid values: 'true' or 'false'
- Default: 'true'
- Bias term useful as intercept in linear regression

**InteractionOnly**
- Specify whether to generate only interaction terms (no individual polynomial terms)
- Valid values: 'true' or 'false'
- Default: 'false'
- When 'true': generates only cross-product terms (xy, xyz), not x², x³

### Input Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | Numeric types (INTEGER, BIGINT, SMALLINT, NUMERIC, DECIMAL, FLOAT, DOUBLE PRECISION) | Columns from which polynomial features will be generated |

### Output Table Schema (FitTable)

The output is a specification table with column metadata:

| Column | Data Type | Description |
|--------|-----------|-------------|
| column_name | VARCHAR | Name of the output polynomial feature column |
| polynomial_specification | VARCHAR | Definition of how the polynomial feature is computed |

The FitTable contains the transformation rules used by TD_PolynomialFeaturesTransform.

### Code Examples

**Input Data: polynomialFeaturesFit_input**
```
id  x1    x2    x3
1   2.0   3.0   1.5
2   4.0   1.0   2.0
3   1.5   2.5   1.0
4   3.5   4.0   3.0
```

**Example 1: Basic Polynomial Features (Degree 2)**
```sql
-- Generate polynomial features up to degree 2 with bias
CREATE TABLE poly_fit_basic AS (
    SELECT * FROM TD_PolynomialFeaturesFit (
        ON polynomialFeaturesFit_input AS InputTable
        USING
        TargetColumns('x1', 'x2')
        Degree(2)
        IncludeBias('true')
        InteractionOnly('false')
    ) AS dt
) WITH DATA;

-- View the fit specification
SELECT * FROM poly_fit_basic;
```

**Output FitTable:**
```
column_name  polynomial_specification
1            Bias (constant 1)
x1           Original feature x1
x2           Original feature x2
x1_x1        x1 squared
x1_x2        x1 * x2 (interaction)
x2_x2        x2 squared
```

**Resulting Features:** [1, x1, x2, x1², x1·x2, x2²]

**Example 2: Degree 3 Polynomial Features**
```sql
-- Generate polynomial features up to degree 3
CREATE TABLE poly_fit_degree3 AS (
    SELECT * FROM TD_PolynomialFeaturesFit (
        ON polynomialFeaturesFit_input AS InputTable
        USING
        TargetColumns('x1', 'x2')
        Degree(3)
        IncludeBias('true')
    ) AS dt
) WITH DATA;
```

**Resulting Features:** [1, x1, x2, x1², x1·x2, x2², x1³, x1²·x2, x1·x2², x2³]

**Example 3: Interaction Terms Only**
```sql
-- Generate only interaction terms (no individual polynomial terms)
CREATE TABLE poly_fit_interact AS (
    SELECT * FROM TD_PolynomialFeaturesFit (
        ON polynomialFeaturesFit_input AS InputTable
        USING
        TargetColumns('x1', 'x2', 'x3')
        Degree(2)
        IncludeBias('false')
        InteractionOnly('true')
    ) AS dt
) WITH DATA;
```

**Resulting Features:** [x1, x2, x3, x1·x2, x1·x3, x2·x3]
(No x1², x2², x3² terms because InteractionOnly='true')

**Example 4: Three Features with All Interactions**
```sql
-- Generate polynomial features from three variables
CREATE TABLE poly_fit_three AS (
    SELECT * FROM TD_PolynomialFeaturesFit (
        ON polynomialFeaturesFit_input AS InputTable
        USING
        TargetColumns('x1', 'x2', 'x3')
        Degree(2)
        IncludeBias('true')
        InteractionOnly('false')
    ) AS dt
) WITH DATA;
```

**Resulting Features:** [1, x1, x2, x3, x1², x1·x2, x1·x3, x2², x2·x3, x3²]

**Example 5: Column Range Notation**
```sql
-- Use column range to specify target columns
CREATE TABLE poly_fit_range AS (
    SELECT * FROM TD_PolynomialFeaturesFit (
        ON sensor_measurements AS InputTable
        USING
        TargetColumns('[1:4]')  -- Columns 1 through 4
        Degree(2)
        IncludeBias('true')
    ) AS dt
) WITH DATA;
```

**Example 6: No Bias Term**
```sql
-- Generate polynomial features without bias column
CREATE TABLE poly_fit_nobias AS (
    SELECT * FROM TD_PolynomialFeaturesFit (
        ON customer_features AS InputTable
        USING
        TargetColumns('age', 'income', 'tenure')
        Degree(2)
        IncludeBias('false')  -- Exclude constant term
    ) AS dt
) WITH DATA;
```

**Example 7: Degree 1 (Original Features Only)**
```sql
-- Degree 1 returns original features plus bias (if included)
CREATE TABLE poly_fit_degree1 AS (
    SELECT * FROM TD_PolynomialFeaturesFit (
        ON polynomialFeaturesFit_input AS InputTable
        USING
        TargetColumns('x1', 'x2')
        Degree(1)
        IncludeBias('true')
    ) AS dt
) WITH DATA;
```

**Resulting Features:** [1, x1, x2]

**Example 8: Regression Pipeline Setup**
```sql
-- Step 1: Create polynomial feature specification for regression
CREATE TABLE regression_poly_fit AS (
    SELECT * FROM TD_PolynomialFeaturesFit (
        ON training_data AS InputTable
        USING
        TargetColumns('temperature', 'pressure', 'humidity')
        Degree(2)
        IncludeBias('true')
    ) AS dt
) WITH DATA;

-- Step 2: Apply transformation (using TD_PolynomialFeaturesTransform)
-- Step 3: Train linear regression on polynomial features
-- This enables linear regression to model non-linear relationships
```

**Example 9: Maximum Columns (5 Features)**
```sql
-- Use maximum allowed 5 target columns
CREATE TABLE poly_fit_max AS (
    SELECT * FROM TD_PolynomialFeaturesFit (
        ON sensor_data AS InputTable
        USING
        TargetColumns('sensor1', 'sensor2', 'sensor3', 'sensor4', 'sensor5')
        Degree(2)
        IncludeBias('true')
        InteractionOnly('false')
    ) AS dt
) WITH DATA;

-- This generates: 5 original + 5 squared + 10 pairwise interactions + 1 bias = 21 features
```

**Example 10: Three-Way Interactions (Degree 3)**
```sql
-- Generate three-way interaction terms
CREATE TABLE poly_fit_threeway AS (
    SELECT * FROM TD_PolynomialFeaturesFit (
        ON experiment_data AS InputTable
        USING
        TargetColumns('factor_a', 'factor_b', 'factor_c')
        Degree(3)
        IncludeBias('true')
        InteractionOnly('false')
    ) AS dt
) WITH DATA;
```

**Resulting Features Include:**
- Degree 0: [1] (bias)
- Degree 1: [a, b, c]
- Degree 2: [a², ab, ac, b², bc, c²]
- Degree 3: [a³, a²b, a²c, ab², abc, ac², b³, b²c, bc², c³]

### Polynomial Feature Generation Explained

**Feature Expansion Example:**

**Original Features:** [x1, x2]

**Degree 1 (IncludeBias='true'):**
```
[1, x1, x2]
```

**Degree 2 (IncludeBias='true'):**
```
[1, x1, x2, x1², x1·x2, x2²]
```

**Degree 3 (IncludeBias='true'):**
```
[1, x1, x2, x1², x1·x2, x2², x1³, x1²·x2, x1·x2², x2³]
```

**Degree 2 with InteractionOnly='true':**
```
[x1, x2, x1·x2]
```
(No squared terms, only cross-products)

**Number of Output Features:**

For n input features and degree d (with bias):
- **Degree 1**: n + 1 features
- **Degree 2**: n + 1 + n + n(n+1)/2 = (n+1)(n+2)/2 features
- **Degree 3**: (n+1)(n+2)(n+3)/6 features

Example with 3 features:
- **Degree 1**: 4 features [1, x1, x2, x3]
- **Degree 2**: 10 features
- **Degree 3**: 20 features

### Use Cases and Applications

**1. Non-Linear Regression**
- Fit polynomial curves to data
- Model quadratic, cubic relationships
- Capture diminishing returns effects
- Handle non-linear growth patterns

**2. Ridge and Lasso Regression**
- Generate polynomial features for regularized regression
- Control overfitting with regularization
- Feature selection with Lasso
- Handle multicollinearity in polynomial terms

**3. Interaction Effect Analysis**
- Detect multiplicative relationships between features
- Model synergy effects (e.g., drug interactions)
- Analyze combined factor impacts
- Econometric interaction modeling

**4. Curve Fitting and Trend Analysis**
- Fit polynomial trends to time series
- Model seasonal patterns with polynomial components
- Forecast based on polynomial trends
- Scientific curve fitting applications

**5. Machine Learning Feature Engineering**
- Enhance gradient boosting models with polynomial features
- Create features for Support Vector Machines
- Improve neural network performance
- Generate basis functions for kernel methods

**6. Scientific and Engineering Applications**
- Physics equations (projectile motion, wave equations)
- Chemical reaction kinetics
- Engineering stress-strain relationships
- Thermodynamic property modeling

**7. Economic and Financial Modeling**
- Model diminishing marginal utility
- Capture non-linear price elasticity
- Risk-return tradeoff curves
- Production function estimation

**8. Marketing Analytics**
- Saturation effects in advertising spend
- Interaction between marketing channels
- Customer lifetime value curves
- Price optimization with non-linear demand

**9. Healthcare and Biostatistics**
- Dose-response curves
- Growth curve modeling
- Pharmacokinetic modeling
- Disease progression patterns

**10. Environmental and Climate Modeling**
- Temperature-humidity interactions
- Pollution dispersion models
- Soil-water-nutrient interactions
- Climate variable relationships

### Important Notes

**Feature Count Explosion:**
- Number of features grows rapidly with degree and input features
- 3 features at degree 3 = 20 output features
- 5 features at degree 2 = 21 output features
- Monitor dimensionality to avoid overfitting

**Column Limit:**
- Maximum 5 target columns can be specified
- Limitation prevents excessive feature explosion
- Consider selecting most important features
- Use domain knowledge to choose relevant interactions

**Degree Limit:**
- Maximum degree is 3
- Higher degrees prone to overfitting
- Degree 2 typically sufficient for most applications
- Degree 3 useful for complex scientific models

**Data Type Requirements:**
- Target columns must be numeric types
- Non-numeric columns will cause errors
- Convert categorical variables first (using encoding functions)
- NULL values handled by Transform function

**Computational Considerations:**
- Fit operation is lightweight (metadata only)
- Transform operation computationally expensive
- High-degree polynomials increase computation time
- Consider subsetting data for large datasets

**InteractionOnly vs Full Polynomial:**
- InteractionOnly='true': Only cross-products (x·y, x·y·z)
- InteractionOnly='false': All terms including squares/cubes
- Interaction-only reduces feature count significantly
- Use when interested only in multiplicative effects

**Bias Term:**
- Bias term (constant 1) important for regression intercept
- Omit bias if using algorithms that add intercept automatically
- Include bias for most linear regression applications

**Multicollinearity:**
- Polynomial features highly correlated with originals
- Use regularization (Ridge, Lasso) to handle collinearity
- Consider feature selection techniques
- Monitor variance inflation factors (VIF)

### Best Practices

**1. Start with Lower Degrees**
- Begin with degree 2, increase only if necessary
- Higher degrees increase overfitting risk
- Validate performance on holdout set
- Use cross-validation to choose optimal degree

**2. Feature Selection**
- Select most important original features first
- Limit to 5 columns maximum
- Use domain knowledge to identify key interactions
- Avoid including highly correlated features

**3. Regularization**
- Always use regularization with polynomial features
- Ridge regression controls multicollinearity
- Lasso performs feature selection
- ElasticNet combines both approaches

**4. Scale Features First**
- Standardize features before polynomial transformation
- Prevents numerical instability
- Ensures features on similar scales
- Use TD_ScaleFit/TD_ScaleTransform before polynomial fit

**5. Monitor Overfitting**
- Compare training vs validation performance
- Use learning curves to detect overfitting
- Implement cross-validation
- Monitor model complexity metrics

**6. Consider InteractionOnly**
- Use when primarily interested in multiplicative effects
- Reduces feature count significantly
- Appropriate for designed experiments
- Useful in ANOVA-style analysis

**7. Documentation**
- Document which features and degree used
- Record rationale for feature selection
- Track model performance across polynomial degrees
- Maintain transformation specifications with model

**8. Production Deployment**
- Store FitTable with model artifacts
- Ensure consistent transformation in production
- Monitor for numerical overflow with high-degree terms
- Validate input data ranges

**9. Interpretability**
- Higher-degree polynomials harder to interpret
- Document feature meanings
- Consider model explanations (SHAP values)
- Balance accuracy with interpretability

**10. Alternative Approaches**
- Consider splines for more flexible curves
- Kernel methods avoid explicit feature generation
- Tree-based models capture non-linearity without polynomials
- Neural networks learn non-linear transformations

### Related Functions
- **TD_PolynomialFeaturesTransform** - Applies polynomial transformation using FitTable (must be used after TD_PolynomialFeaturesFit)
- **TD_ScaleFit** - Feature scaling, should be applied before polynomial transformation
- **TD_ScaleTransform** - Apply scaling to features
- **TD_GLM** - Generalized Linear Models that can use polynomial features
- **TD_RandomProjectionFit** - Alternative dimensionality expansion/reduction technique

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Transform Functions
