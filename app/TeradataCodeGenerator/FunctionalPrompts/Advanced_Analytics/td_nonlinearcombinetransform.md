# TD_NonLinearCombineTransform

### Function Name
**TD_NonLinearCombineTransform**

### Description
TD_NonLinearCombineTransform generates the values of a new feature using the specified formula from the TD_NonLinearCombineFit function output. This function performs the actual computation of non-linear feature combinations, applying mathematical formulas to create derived features that capture complex relationships between original variables.

A non-linear combination transform takes one or more input variables and combines them using a non-linear mathematical formula to generate an output variable. Unlike linear transformations where the output is a linear combination of inputs, non-linear transformations can capture curves, bends, interactions, and complex patterns in data.

### When the Function Would Be Used
- **Create Engineered Features**: Generate new features for machine learning models
- **Apply Domain Formulas**: Implement business or scientific calculations
- **Generate Interaction Terms**: Create multiplicative combinations of features
- **Compute Polynomial Features**: Calculate squared, cubed, or higher-order terms
- **Calculate Derived Metrics**: Compute KPIs and business metrics from raw data
- **Implement Mathematical Models**: Apply physics, chemistry, or engineering formulas
- **Create Composite Scores**: Generate weighted combinations of multiple inputs
- **Feature Transformation**: Transform features to better capture non-linear patterns
- **Data Augmentation**: Expand feature space for improved model performance
- **Cross-feature Interactions**: Model how features influence each other

### Non-linear Transformation Concepts

Non-linear transformations are essential in machine learning and data analysis because:

**Capturing Complexity**:
- Many real-world relationships are non-linear
- Interaction effects between variables
- Diminishing or accelerating returns
- Threshold effects and tipping points

**Examples of Non-linear Relationships**:
- **Polynomial**: y = x² (area = side²)
- **Interaction**: y = x₁ × x₂ (revenue = price × quantity)
- **Ratio**: y = x₁/x₂ (efficiency = output/input)
- **Sigmoid**: Used in neural networks for non-linear activation
- **Compound**: y = x₁ × (1 + x₂)ⁿ (compound interest)

### Syntax
```sql
TD_NonLinearCombineTransform (
    ON { table | view | (query) } AS InputTable
    ON { table | view | (query) } AS FitTable DIMENSION
    USING
    [ Accumulate ({'accumulate_column' | 'accumulate_column_range'}[,...]) ]
)
```

### Required Syntax Elements for TD_NonLinearCombineTransform

**ON clause (InputTable)**
- Accept the InputTable clause containing data to transform

**ON clause (FitTable DIMENSION)**
- Accept the FitTable clause (output from TD_NonLinearCombineFit)
- Contains formula specification for transformation

### Optional Syntax Elements for TD_NonLinearCombineTransform

**Accumulate**
- Specify the input table column names to copy to the output table
- Useful for preserving identifiers and metadata columns
- Supports column range notation

### Input Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| TargetColumns | BYTEINT, SMALLINT, INTEGER, BIGINT, DECIMAL/NUMERIC, FLOAT, REAL, DOUBLE PRECISION | The input table column names to use in the non-linear combination |
| AccumulateColumns | ANY | The input table column names to copy to the output table |

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| AccumulateColumns | BYTEINT, SMALLINT, INTEGER, BIGINT, DECIMAL/NUMERIC, FLOAT, REAL, DOUBLE PRECISION | The specified columns in the Accumulate element copied to the output table |
| ResultColumn | REAL | The values calculated using the specified formula are displayed |

### Code Examples

**Input Table: nonLinearCombineFit_input**
```
passenger  survived  pclass  gender  age  sibsp  parch  fare     cabin  embarked
1          0         General male    22   1      0      7.25     null   S
2          1         Deluxe  female  38   1      1      71.28    C85    C
3          1         General female  26   0      0      7.93     null   S
4          1         Deluxe  female  35   1      0      53.10    C123   S
5          0         General male    35   0      1      8.05     null   S
```

**FitTable: nonLinearCombineFit_output**
```
total_cost         sibsp  parch  fare
Y=(X0+X1+1)*X2     null   null   null
```

**Example 1: Calculate Total Cost**
```sql
SELECT * FROM TD_NonLinearCombineTransform (
    ON nonLinearCombineFit_input AS InputTable
    ON nonLinearCombineFit_output AS FitTable DIMENSION
    USING
    Accumulate('Passenger')
) AS dt
ORDER BY 1;
```

**Output:**
```
passenger  TotalCost
1          14.50000
2          213.84000
3          7.93000
4          106.20000
5          16.10000
```

**Example 2: Calculate Area from Length and Width**
```sql
-- First create fit table
CREATE TABLE area_fit AS (
    SELECT * FROM TD_NonLinearCombineFit (
        ON measurements AS InputTable
        USING
        TargetColumns ('length', 'width')
        Formula ('Y=X0*X1')
        ResultColumn ('area')
    ) AS dt
) WITH DATA;

-- Then apply transformation
SELECT * FROM TD_NonLinearCombineTransform (
    ON measurements AS InputTable
    ON area_fit AS FitTable DIMENSION
    USING
    Accumulate('measurement_id', 'location')
) AS dt
ORDER BY measurement_id;
```

**Example 3: Calculate BMI**
```sql
-- Apply BMI formula: weight / (height^2)
SELECT * FROM TD_NonLinearCombineTransform (
    ON patient_data AS InputTable
    ON bmi_fit AS FitTable DIMENSION
    USING
    Accumulate('patient_id', 'name', 'age')
) AS dt
ORDER BY patient_id;
```

**Example Output:**
```
patient_id  name          age  bmi
P001        John Smith    35   24.5
P002        Jane Doe      42   22.3
P003        Bob Johnson   28   27.8
```

**Example 4: Calculate Revenue**
```sql
-- Revenue = quantity * unit_price * (1 - discount_rate)
SELECT * FROM TD_NonLinearCombineTransform (
    ON order_items AS InputTable
    ON revenue_fit AS FitTable DIMENSION
    USING
    Accumulate('order_id', 'product_id', 'order_date')
) AS dt
ORDER BY order_id, product_id;
```

**Example 5: Polynomial Feature Generation**
```sql
-- Create feature: X1^2 + X1*X2
SELECT * FROM TD_NonLinearCombineTransform (
    ON training_data AS InputTable
    ON poly_fit AS FitTable DIMENSION
    USING
    Accumulate('customer_id', 'target')
) AS dt;
```

**Example 6: Distance Calculation**
```sql
-- Calculate Euclidean distance: sqrt(x^2 + y^2)
SELECT * FROM TD_NonLinearCombineTransform (
    ON coordinates AS InputTable
    ON distance_fit AS FitTable DIMENSION
    USING
    Accumulate('point_id', 'location_name')
) AS dt
ORDER BY point_id;
```

**Example Output:**
```
point_id  location_name  distance_from_origin
PT001     Store A        5.83095
PT002     Store B        7.28011
PT003     Store C        3.16228
```

**Example 7: Compound Interest Calculation**
```sql
-- Future Value = principal * (1 + rate)^years
SELECT * FROM TD_NonLinearCombineTransform (
    ON investment_data AS InputTable
    ON compound_fit AS FitTable DIMENSION
    USING
    Accumulate('account_id', 'account_name', 'start_date')
) AS dt
ORDER BY account_id;
```

**Example 8: Profit Margin Calculation**
```sql
-- Profit Margin % = ((revenue - cost) / revenue) * 100
SELECT * FROM TD_NonLinearCombineTransform (
    ON financial_data AS InputTable
    ON margin_fit AS FitTable DIMENSION
    USING
    Accumulate('product_id', 'product_name', 'category')
) AS dt
ORDER BY profit_margin_pct DESC;
```

**Example Output:**
```
product_id  product_name  category    profit_margin_pct
PRD001      Widget A      Electronics 45.2
PRD002      Gadget B      Electronics 38.7
PRD003      Tool C        Hardware    22.5
```

**Example 9: Interaction Term for ML**
```sql
-- Create interaction: age * income / 1000
SELECT * FROM TD_NonLinearCombineTransform (
    ON customer_features AS InputTable
    ON interaction_fit AS FitTable DIMENSION
    USING
    Accumulate('customer_id')
) AS dt;
```

**Example 10: Complete ML Pipeline**
```sql
-- Step 1: Create fit table on training data (already done)

-- Step 2: Transform training data
CREATE TABLE training_transformed AS (
    SELECT * FROM TD_NonLinearCombineTransform (
        ON training_data AS InputTable
        ON training_fit AS FitTable DIMENSION
        USING
        Accumulate('customer_id', 'target')
    ) AS dt
) WITH DATA;

-- Step 3: Transform test data using same formula
CREATE TABLE test_transformed AS (
    SELECT * FROM TD_NonLinearCombineTransform (
        ON test_data AS InputTable
        ON training_fit AS FitTable DIMENSION
        USING
        Accumulate('customer_id')
    ) AS dt
) WITH DATA;
```

### Use Cases and Applications

**1. Machine Learning Feature Engineering**
- Create polynomial features for regression models
- Generate interaction terms for tree-based models
- Design composite features for neural networks
- Improve model expressiveness through feature combinations

**2. Business Metrics Calculation**
- Calculate KPIs from raw operational data
- Compute financial ratios and indicators
- Generate efficiency and productivity metrics
- Create composite performance scores

**3. Scientific Computing**
- Apply physics formulas (velocity, acceleration, force)
- Calculate chemical concentrations and reaction rates
- Compute engineering metrics (stress, strain, efficiency)
- Implement domain-specific mathematical models

**4. Financial Analysis**
- Calculate investment returns and growth rates
- Compute risk-adjusted performance metrics
- Generate profitability indicators
- Create credit scoring features

**5. Healthcare Analytics**
- Calculate medical indices (BMI, body surface area)
- Compute dosage adjustments
- Generate risk scores
- Create patient health metrics

**6. E-commerce Analytics**
- Calculate customer lifetime value estimates
- Compute basket metrics (average order value)
- Generate engagement scores
- Create recommendation features

### Important Notes
- Input data must have same structure as TD_NonLinearCombineFit input
- Formula is evaluated for each row in InputTable
- Target columns (X0, X1, X2, etc.) correspond to order in TargetColumns
- ResultColumn name defined in FitTable is used for output column
- NULL values in target columns may produce NULL or error depending on formula
- Use Accumulate to preserve necessary columns for analysis
- Transformation is applied row-wise to all input rows
- Same FitTable can be used on training and test data
- Formula must be valid SQL expression
- Division by zero should be handled in formula design

### Best Practices

**1. Train-Test Consistency**
- Create FitTable using only training data
- Apply same FitTable to both training and test sets
- This prevents data leakage and ensures consistency

**2. Handle Edge Cases**
- Add small constants to avoid division by zero
- Use COALESCE or CASE to handle NULLs
- Test formulas with boundary values

**3. Feature Scaling**
- Consider scales of combined features
- May need to normalize output for some algorithms
- Document any scaling applied in formulas

**4. Validate Output**
- Check output ranges make sense
- Verify no unexpected NULL values
- Ensure transformations improve model performance

**5. Document Formulas**
- Keep clear records of formula logic
- Document business rationale
- Store FitTable for reproducibility

**6. Performance Considerations**
- Complex formulas may impact query performance
- Test on sample data first
- Consider materialized views for frequently used transformations

### Related Functions
- **TD_NonLinearCombineFit** - Creates formula specification (must be run before TD_NonLinearCombineTransform)
- **TD_PolynomialFeaturesTransform** - Automated polynomial feature generation
- **TD_FunctionTransform** - Single-column mathematical transformations
- **TD_ColumnTransformer** - Combined transformation pipeline

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- [Teradata SQL Functions, Expressions, and Predicates](https://docs.teradata.com) (B035-1145)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Transform Functions
