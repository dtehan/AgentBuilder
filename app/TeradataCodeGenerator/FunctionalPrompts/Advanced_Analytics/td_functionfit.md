# TD_FunctionFit

### Function Name
**TD_FunctionFit**

### Description
TD_FunctionFit determines whether specified numeric transformations can be applied to specified input columns and outputs a fit table to use as input to TD_FunctionTransform, which performs the actual transformations. The function validates that transformations are compatible with the data types and creates a configuration table that TD_FunctionTransform uses to apply mathematical functions to numeric columns.

Function transformations play a critical role in the machine learning pipeline by applying mathematical functions to columns of data to create new variables that can help improve the accuracy and robustness of machine learning models.

### When the Function Would Be Used
- **Data Normalization**: Transform data into a more standardized form using log, sigmoid, or tanh functions
- **Handling Non-linear Relationships**: Capture non-linear relationships between variables and targets
- **Mitigating Skewness**: Use log or power transformations to balance skewed data distributions
- **Addressing Heteroscedasticity**: Apply transformations when variance is not constant across levels
- **Feature Engineering**: Create new features through mathematical transformations
- **Reducing Outlier Impact**: Apply sigmoid or tanh to compress extreme values
- **Scale Normalization**: Map data into specific ranges (e.g., 0 to 1, -1 to 1)
- **Exponential Growth**: Capture exponential relationships with EXP transformation
- **Power Relationships**: Model power-law relationships with POW transformation
- **Preparing ML Features**: Transform features to improve model performance

### Common Transformations and Their Purposes

**Data Normalization**:
- **Log**: Scales down larger values while keeping smaller values relatively unchanged
- **Sigmoid**: Maps data into range [0, 1], reduces outlier impact
- **Tanh**: Maps data into range [-1, 1], symmetric around zero

**Non-linear Relationships**:
- **EXP**: Captures exponential growth patterns
- **POW**: Models power-law relationships
- **LOG**: Transforms multiplicative relationships to additive

**Skewness Mitigation**:
- **Log/Power/Sigmoid/Tanh**: Compress majority class values toward center, expand minority class toward tails
- Improves performance of algorithms sensitive to skewed data

**Heteroscedasticity**:
- **LOG**: Addresses non-constant variance across different variable levels
- Stabilizes variance for better model accuracy

### Syntax
```sql
CREATE TABLE output_table AS (
    TD_FunctionFit (
        ON { table | view | (query) } AS InputTable
        ON { table | view | (query) } AS TransformationTable DIMENSION
    )
) WITH DATA;
```

### Required Syntax Elements for TD_FunctionFit

**ON clause (InputTable)**
- Accepts the InputTable clause containing numeric columns to transform

**ON clause (TransformationTable DIMENSION)**
- Accepts the TransformationTable clause specifying transformations to apply
- Contains transformation specifications and parameters

### TransformationTable Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| TargetColumn | VARCHAR (CHARACTER SET LATIN or UNICODE) | Name of InputTable column to transform |
| Transformation | VARCHAR (CHARACTER SET LATIN or UNICODE) | Transformation to apply (see Allowed Transformations table) |
| Parameters | VARCHAR (CHARACTER SET LATIN or UNICODE) | [Optional] Transformation parameters in JSON format. If absent and transformation has parameter, function uses default value |
| DefaultValue | NUMERIC | [Optional] Default value for transformed value if TargetColumn is nonnumeric or NULL. If absent, function uses default value 0 |

### Allowed Transformations

| Transformation | Parameter | Operation on TargetColumn Value x |
|----------------|-----------|-----------------------------------|
| ABS | None | \|x\| (absolute value) |
| CEIL | None | CEIL(x) - Least integer ≥ x |
| EXP | None | e^x (e = 2.718) |
| FLOOR | None | FLOOR(x) - Greatest integer ≤ x |
| LOG | [Optional] {"base": base}<br>Default: e | LOG_base(x) |
| POW | [Optional] {"exponent": exponent}<br>Default: 1 | x^exponent |
| SIGMOID | None | 1 / (1 + e^-x) |
| TANH | None | (e^x - e^-x) / (e^x + e^-x) |

### Input Table Schema

**InputTable Schema**

| Column | Data Type | Description |
|--------|-----------|-------------|
| input_column | VARCHAR (CHARACTER SET LATIN or UNICODE) or NUMERIC | Column whose name can appear as TargetColumn in TransformationTable |

**TransformationTable Schema**

| Column | Data Type | Description |
|--------|-----------|-------------|
| TargetColumn | VARCHAR (CHARACTER SET LATIN or UNICODE) | Name of InputTable column to transform |
| Transformation | VARCHAR (CHARACTER SET LATIN or UNICODE) | Transformation to apply to TargetColumn |
| Parameters | VARCHAR (CHARACTER SET LATIN or UNICODE) | [Optional] Transformation parameters in JSON format |
| DefaultValue | NUMERIC | [Optional] Default value if TargetColumn is nonnumeric or NULL (default: 0) |

### Output Table Schema

Output table has the same schema as TransformationTable:

| Column | Data Type | Description |
|--------|-----------|-------------|
| TargetColumn | VARCHAR | Name of column to transform |
| Transformation | VARCHAR | Transformation to apply |
| Parameters | VARCHAR | [Optional] Transformation parameters in JSON format |
| DefaultValue | NUMERIC | [Optional] Default value for NULL or nonnumeric values |

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

**Example 1: Log Base 2 and Power Transformations**

First, create a transformation specification table:
```sql
CREATE TABLE transformations (
    TargetColumn VARCHAR(20),
    Transformation VARCHAR(20),
    Parameters VARCHAR(50),
    DefaultValue DECIMAL(10,9)
);

INSERT INTO transformations VALUES ('age', 'LOG', '{"base":2}', 0.000000000);
INSERT INTO transformations VALUES ('fare', 'POW', '{"exponent": 2}', 10.000000000);
```

Then apply TD_FunctionFit:
```sql
CREATE TABLE fit_out AS (
    SELECT * FROM TD_FunctionFit (
        ON function_input_table AS InputTable
        ON transformations AS TransformationTable DIMENSION
    ) AS dt
) WITH DATA;
```

**Output:**
```
TargetColumn  Transformation  Parameters          Defaultvalue
age           LOG             {"base":2}          0.000000000
fare          POW             {"exponent": 2}     10.000000000
```

**Example 2: Natural Log Transformation**
```sql
CREATE TABLE log_transformations (
    TargetColumn VARCHAR(20),
    Transformation VARCHAR(20)
);

INSERT INTO log_transformations VALUES ('age', 'LOG');
INSERT INTO log_transformations VALUES ('fare', 'LOG');

CREATE TABLE log_fit AS (
    SELECT * FROM TD_FunctionFit (
        ON function_input_table AS InputTable
        ON log_transformations AS TransformationTable DIMENSION
    ) AS dt
) WITH DATA;
```

**Example 3: Sigmoid Transformation for Normalization**
```sql
CREATE TABLE sigmoid_transformations (
    TargetColumn VARCHAR(20),
    Transformation VARCHAR(20),
    DefaultValue DECIMAL(5,2)
);

INSERT INTO sigmoid_transformations VALUES ('age', 'SIGMOID', 0.50);
INSERT INTO sigmoid_transformations VALUES ('fare', 'SIGMOID', 0.50);

CREATE TABLE sigmoid_fit AS (
    SELECT * FROM TD_FunctionFit (
        ON function_input_table AS InputTable
        ON sigmoid_transformations AS TransformationTable DIMENSION
    ) AS dt
) WITH DATA;
```

**Example 4: Multiple Transformations**
```sql
CREATE TABLE multi_transformations (
    TargetColumn VARCHAR(20),
    Transformation VARCHAR(20),
    Parameters VARCHAR(50),
    DefaultValue DECIMAL(10,5)
);

INSERT INTO multi_transformations VALUES ('age', 'LOG', '{"base":10}', 1.00000);
INSERT INTO multi_transformations VALUES ('fare', 'SQRT', NULL, 0.00000);
INSERT INTO multi_transformations VALUES ('sibsp', 'ABS', NULL, 0.00000);
INSERT INTO multi_transformations VALUES ('parch', 'CEIL', NULL, 0.00000);

CREATE TABLE multi_fit AS (
    SELECT * FROM TD_FunctionFit (
        ON function_input_table AS InputTable
        ON multi_transformations AS TransformationTable DIMENSION
    ) AS dt
) WITH DATA;
```

**Example 5: Exponential Transformation**
```sql
CREATE TABLE exp_transformations (
    TargetColumn VARCHAR(20),
    Transformation VARCHAR(20)
);

INSERT INTO exp_transformations VALUES ('age', 'EXP');

CREATE TABLE exp_fit AS (
    SELECT * FROM TD_FunctionFit (
        ON normalized_data AS InputTable
        ON exp_transformations AS TransformationTable DIMENSION
    ) AS dt
) WITH DATA;
```

**Example 6: Absolute Value for Error Metrics**
```sql
CREATE TABLE abs_transformations (
    TargetColumn VARCHAR(20),
    Transformation VARCHAR(20)
);

INSERT INTO abs_transformations VALUES ('error_value', 'ABS');
INSERT INTO abs_transformations VALUES ('residual', 'ABS');

CREATE TABLE abs_fit AS (
    SELECT * FROM TD_FunctionFit (
        ON prediction_results AS InputTable
        ON abs_transformations AS TransformationTable DIMENSION
    ) AS dt
) WITH DATA;
```

**Example 7: TANH Transformation for Neural Networks**
```sql
CREATE TABLE tanh_transformations (
    TargetColumn VARCHAR(20),
    Transformation VARCHAR(20),
    DefaultValue DECIMAL(5,3)
);

INSERT INTO tanh_transformations VALUES ('feature1', 'TANH', 0.000);
INSERT INTO tanh_transformations VALUES ('feature2', 'TANH', 0.000);
INSERT INTO tanh_transformations VALUES ('feature3', 'TANH', 0.000);

CREATE TABLE tanh_fit AS (
    SELECT * FROM TD_FunctionFit (
        ON ml_features AS InputTable
        ON tanh_transformations AS TransformationTable DIMENSION
    ) AS dt
) WITH DATA;
```

**Example 8: Custom Power Transformation**
```sql
CREATE TABLE power_transformations (
    TargetColumn VARCHAR(20),
    Transformation VARCHAR(20),
    Parameters VARCHAR(50)
);

INSERT INTO power_transformations VALUES ('area', 'POW', '{"exponent": 0.5}');  -- Square root
INSERT INTO power_transformations VALUES ('volume', 'POW', '{"exponent": 0.333}');  -- Cube root
INSERT INTO power_transformations VALUES ('price', 'POW', '{"exponent": 2}');  -- Square

CREATE TABLE power_fit AS (
    SELECT * FROM TD_FunctionFit (
        ON measurements AS InputTable
        ON power_transformations AS TransformationTable DIMENSION
    ) AS dt
) WITH DATA;
```

**Example 9: Floor and Ceiling for Binning Preparation**
```sql
CREATE TABLE round_transformations (
    TargetColumn VARCHAR(20),
    Transformation VARCHAR(20)
);

INSERT INTO round_transformations VALUES ('score', 'FLOOR');
INSERT INTO round_transformations VALUES ('rating', 'CEIL');

CREATE TABLE round_fit AS (
    SELECT * FROM TD_FunctionFit (
        ON student_grades AS InputTable
        ON round_transformations AS TransformationTable DIMENSION
    ) AS dt
) WITH DATA;
```

**Example 10: Complex Multi-Column Transformation Pipeline**
```sql
CREATE TABLE pipeline_transformations (
    TargetColumn VARCHAR(30),
    Transformation VARCHAR(20),
    Parameters VARCHAR(50),
    DefaultValue DECIMAL(10,5)
);

-- Normalize skewed income with log
INSERT INTO pipeline_transformations VALUES ('annual_income', 'LOG', '{"base":10}', 4.00000);

-- Sigmoid for probability scores
INSERT INTO pipeline_transformations VALUES ('default_risk', 'SIGMOID', NULL, 0.50000);

-- Power transformation for age (square root to reduce skew)
INSERT INTO pipeline_transformations VALUES ('age', 'POW', '{"exponent": 0.5}', 5.00000);

-- Absolute value for transaction differences
INSERT INTO pipeline_transformations VALUES ('balance_change', 'ABS', NULL, 0.00000);

CREATE TABLE pipeline_fit AS (
    SELECT * FROM TD_FunctionFit (
        ON customer_analytics AS InputTable
        ON pipeline_transformations AS TransformationTable DIMENSION
    ) AS dt
) WITH DATA;
```

### Use Cases and Applications

**1. Machine Learning Feature Engineering**
- Transform features to improve model performance
- Create non-linear features from linear ones
- Normalize feature scales for algorithms sensitive to scale
- Reduce impact of outliers on model training

**2. Statistical Modeling**
- Satisfy normality assumptions for parametric tests
- Stabilize variance (homoscedasticity)
- Linearize non-linear relationships
- Transform data for regression analysis

**3. Data Normalization**
- Scale features to similar ranges
- Prepare data for distance-based algorithms
- Normalize distributions for comparison
- Standardize inputs for neural networks

**4. Skewness Reduction**
- Transform right-skewed distributions with log
- Balance class distributions in classification
- Improve visualization of skewed data
- Make data more suitable for linear models

**5. Financial Analysis**
- Log-transform prices and returns
- Calculate growth rates with exponential transformations
- Normalize financial ratios
- Transform monetary values across different scales

**6. Scientific Computing**
- Apply domain-specific transformations
- Convert between measurement scales
- Normalize experimental data
- Prepare data for physical models

### Important Notes
- Transformation specifications are validated against input data
- Parameters must be in JSON format for LOG and POW transformations
- Default base for LOG is e (natural logarithm)
- Default exponent for POW is 1 (identity transformation)
- DefaultValue is used when input is NULL or nonnumeric (default: 0)
- Output table has same schema as TransformationTable input
- All transformations except LOG and POW have no parameters
- SIGMOID maps values to (0, 1), useful for probability-like features
- TANH maps values to (-1, 1), symmetric around zero
- Function only validates transformation compatibility; actual transformation done by TD_FunctionTransform
- ABS useful for error metrics and distance calculations
- CEIL and FLOOR useful for discretization and rounding
- Consider domain and data characteristics when choosing transformations

### Transformation Selection Guidelines

**For Right-Skewed Data**:
- Use LOG transformation
- Consider POW with exponent < 1

**For Left-Skewed Data**:
- Use POW with exponent > 1
- Consider EXP for extreme cases

**For Outliers**:
- Use SIGMOID or TANH to compress extreme values
- LOG transformation reduces outlier impact

**For Non-linearity**:
- Use POW for power-law relationships
- Use EXP for exponential growth
- Use LOG for diminishing returns patterns

**For Normalization**:
- SIGMOID: Range [0, 1], asymmetric
- TANH: Range [-1, 1], symmetric
- LOG: Compresses large values

### Related Functions
- **TD_FunctionTransform** - Applies transformations using TD_FunctionFit output (must be used after TD_FunctionFit)
- **TD_NumApply** - Alternative function for numeric transformations
- **TD_ScaleFit** - For standardization and min-max scaling
- **TD_BinCodeFit** - For discretization of continuous variables

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Transform Functions
