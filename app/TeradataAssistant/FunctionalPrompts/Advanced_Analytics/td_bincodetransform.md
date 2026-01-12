# TD_BinCodeTransform

### Function Name
**TD_BinCodeTransform**

### Description
TD_BinCodeTransform is a data transformation function that converts continuous numerical data into categorical data by applying binning transformations defined in the TD_BinCodeFit output. The function takes numeric values from input columns and replaces them with categorical labels (bin labels) based on which bin range each value falls into.

The binning process involves:
1. Determining the appropriate bin for each data value based on bin boundaries
2. Assigning data values to bins (the binning process)
3. Replacing numeric values with categorical labels for each bin

This transformation is useful for simplifying data, reducing complexity, and preparing features for machine learning algorithms that benefit from categorical inputs.

### When the Function Would Be Used
- **Machine Learning Preparation**: Converting continuous features to categorical for tree-based models
- **Data Discretization**: Simplifying continuous variables into meaningful categories
- **Feature Engineering**: Creating categorical features from numeric data for model training
- **Risk Categorization**: Converting risk scores into risk levels (Low, Medium, High)
- **Customer Segmentation**: Transforming behavioral metrics into segment categories
- **Age Grouping**: Converting exact ages into demographic categories
- **Income Classification**: Assigning income brackets to continuous income values
- **Performance Tiers**: Creating performance categories from numeric scores
- **Data Standardization**: Normalizing data representation across different ranges
- **Reducing Overfitting**: Grouping similar values to prevent model overfitting

### Binning Process

TD_BinCodeTransform follows a three-step process:

**Step 1: Determine Bin Size**
- Bins can be equal-width or variable-width based on TD_BinCodeFit configuration
- Equal-width: All bins have the same numeric range
- Variable-width: Bins have different ranges based on domain knowledge

**Step 2: Assign Data to Bins**
- Each value is assigned to the appropriate bin based on its numeric value
- If value x falls within [min, max] of a bin, it's assigned to that bin
- This process is called "binning"

**Step 3: Transform to Categorical**
- Each bin is assigned a categorical label
- Labels can be auto-generated or user-specified
- Numeric values are replaced with these categorical labels

### Advantages and Considerations

**Advantages:**
- Makes data easier to analyze, especially for large datasets
- Reduces impact of outliers by grouping extreme values
- Smooths out data variations
- Helps address overfitting in machine learning models
- Makes patterns more visible in visualizations

**Considerations:**
- Bin sizes must be carefully chosen
- Bins too wide: Loss of valuable information
- Bins too narrow: Data becomes too sparse, leading to potential overfitting
- Binning is irreversible - original precision is lost
- Choice of boundaries significantly impacts results

### Syntax
```sql
TD_BinCodeTransform (
    ON { table | view | (query) } AS InputTable
    ON { table | view | (query) } AS FitTable DIMENSION
    USING
    [ Accumulate ({ 'accumulate_column' | accumulate_column_range }[,...]) ]
)
```

### Required Syntax Elements for TD_BinCodeTransform

**ON clause (InputTable)**
- Accepts the InputTable clause containing numeric data to transform

**ON clause (FitTable DIMENSION)**
- Accepts the FitTable clause (output from TD_BinCodeFit)
- Contains bin specifications and boundaries

### Optional Syntax Elements for TD_BinCodeTransform

**Accumulate**
- Specify InputTable column names to copy to the output table
- Useful for preserving identifiers and non-transformed columns
- Supports column range notation

### Input Table Schema

**InputTable Schema**

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | BYTEINT, SMALLINT, INTEGER, BIGINT, DECIMAL/NUMERIC, FLOAT, REAL, DOUBLE PRECISION | Column to be transformed (same as TD_BinCodeFit input) |
| accumulate_column | Any | [Optional] Column to copy to output table |

**FitTable Schema**

See TD_BinCodeFit Output table schema. This is the output table created by TD_BinCodeFit function.

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| accumulate_column | Same as in InputTable | Column copied from InputTable |
| target_column | VARCHAR (CHARACTER SET UNICODE) | [Column appears once for each specified target_column] Bin labels replacing original numeric values |

### Code Examples

**Input Table: bin_titanic_train**
```
passenger  survived  pclass  name                                         gender  age  sibsp  parch  fare
97         0         1       Goldschmidt; Mr. George B                    male    71   0      0      34.6542
488        0         1       Kent; Mr. Edward Austin                      male    58   0      0      29.7
505        1         1       Maioni; Miss. Roberta                        female  16   0      0      86.5
631        1         1       Barkworth; Mr. Algernon Henry Wilson         male    80   0      0      30.0
873        0         1       Carlsson; Mr. Frans Olof                     male    33   0      0      5.0
```

**FitTable: FitOutputTable** (created by TD_BinCodeFit)
```
TD_ColumnName_BINFIT  TD_MinValue_BINFIT  TD_MaxValue_BINFIT  TD_Label_BINFIT  TD_Bins_BINFIT  TD_IndexValue_BINFIT
age                   46.0                90.0                Old Age          3               0
age                   21.0                45.0                Middle Age       3               0
age                   0.0                 20.0                Young Age        3               0
```

**Example 1: Basic Age Binning Transformation**
```sql
SELECT * FROM TD_BinCodeTransform (
    ON bin_titanic_train AS InputTable
    ON FitOutputTable AS FitTable DIMENSION
    USING
    Accumulate ('passenger')
) AS dt
ORDER BY passenger;
```

**Output:**
```
passenger  age
505        Young Age
631        Old Age
97         Old Age
488        Old Age
873        Middle Age
```

**Example 2: Transform with Multiple Accumulated Columns**
```sql
SELECT * FROM TD_BinCodeTransform (
    ON bin_titanic_train AS InputTable
    ON FitOutputTable AS FitTable DIMENSION
    USING
    Accumulate ('passenger', 'name', 'gender', 'survived')
) AS dt
ORDER BY passenger;
```

**Output:**
```
passenger  name                                         gender  survived  age
97         Goldschmidt; Mr. George B                    male    0         Old Age
488        Kent; Mr. Edward Austin                      male    0         Old Age
505        Maioni; Miss. Roberta                        female  1         Young Age
631        Barkworth; Mr. Algernon Henry Wilson         male    1         Old Age
873        Carlsson; Mr. Frans Olof                     male    0         Middle Age
```

**Example 3: Income Bracket Transformation**
```sql
-- First create bins with TD_BinCodeFit (see td_bincodefit.md for setup)
-- Then transform income values to brackets

SELECT * FROM TD_BinCodeTransform (
    ON customer_data AS InputTable
    ON IncomeFitTable AS FitTable DIMENSION
    USING
    Accumulate ('customer_id', 'customer_name')
) AS dt
ORDER BY customer_id;
```

**Example Output:**
```
customer_id  customer_name  annual_income
1001         John Smith     Middle Income
1002         Jane Doe       Upper Middle
1003         Bob Johnson    Low Income
1004         Alice Brown    High Income
```

**Example 4: Credit Score Risk Categories**
```sql
-- Transform credit scores into risk categories
SELECT * FROM TD_BinCodeTransform (
    ON applicant_data AS InputTable
    ON CreditScoreFitTable AS FitTable DIMENSION
    USING
    Accumulate ('applicant_id', 'applicant_name', 'application_date')
) AS dt
ORDER BY applicant_id;
```

**Example Output:**
```
applicant_id  applicant_name  application_date  credit_score
2001          Mary Wilson     2024-01-15        Good
2002          Tom Davis       2024-01-16        Exceptional
2003          Sarah Miller    2024-01-17        Fair
2004          Mike Anderson   2024-01-18        Very Good
```

**Example 5: Multiple Column Transformation**
```sql
-- Transform both age and fare columns simultaneously
SELECT * FROM TD_BinCodeTransform (
    ON bin_titanic_train AS InputTable
    ON MultiBinsFitTable AS FitTable DIMENSION
    USING
    Accumulate ('passenger', 'name', 'gender')
) AS dt
ORDER BY passenger;
```

**Example Output:**
```
passenger  name                                         gender  age         fare
97         Goldschmidt; Mr. George B                    male    Old Age     Medium Fare
488        Kent; Mr. Edward Austin                      male    Old Age     Medium Fare
505        Maioni; Miss. Roberta                        female  Young Age   High Fare
631        Barkworth; Mr. Algernon Henry Wilson         male    Old Age     Medium Fare
873        Carlsson; Mr. Frans Olof                     male    Middle Age  Low Fare
```

**Example 6: Temperature Category Transformation**
```sql
-- Convert temperature readings to categories
SELECT * FROM TD_BinCodeTransform (
    ON weather_data AS InputTable
    ON TempFitTable AS FitTable DIMENSION
    USING
    Accumulate ('station_id', 'reading_date', 'location')
) AS dt
ORDER BY station_id, reading_date;
```

**Example Output:**
```
station_id  reading_date  location     temperature
WX001       2024-01-15    New York     Cold
WX001       2024-01-16    New York     Freezing
WX002       2024-01-15    Miami        Warm
WX002       2024-01-16    Miami        Hot
```

**Example 7: Transaction Amount Categories**
```sql
-- Categorize transaction amounts
SELECT * FROM TD_BinCodeTransform (
    ON transactions AS InputTable
    ON TransactionFitTable AS FitTable DIMENSION
    USING
    Accumulate ('transaction_id', 'customer_id', 'transaction_date')
) AS dt
ORDER BY transaction_id;
```

**Example Output:**
```
transaction_id  customer_id  transaction_date  amount
TXN001          C1001        2024-01-15        Medium
TXN002          C1002        2024-01-15        Large
TXN003          C1003        2024-01-16        Small
TXN004          C1004        2024-01-16        Very Large
```

**Example 8: Response Time Performance Tiers**
```sql
-- Transform response times into performance categories
SELECT * FROM TD_BinCodeTransform (
    ON api_metrics AS InputTable
    ON ResponseTimeFitTable AS FitTable DIMENSION
    USING
    Accumulate ('request_id', 'endpoint', 'timestamp')
) AS dt
ORDER BY request_id;
```

**Example Output:**
```
request_id  endpoint          timestamp            response_time_ms
REQ001      /api/users        2024-01-15 10:00:00  Fast
REQ002      /api/products     2024-01-15 10:00:05  Medium
REQ003      /api/orders       2024-01-15 10:00:10  Slow
REQ004      /api/analytics    2024-01-15 10:00:15  Very Slow
```

**Example 9: Using Column Ranges for Accumulate**
```sql
-- Use column range notation to accumulate multiple columns
SELECT * FROM TD_BinCodeTransform (
    ON sensor_readings AS InputTable
    ON SensorBinsFitTable AS FitTable DIMENSION
    USING
    Accumulate ('[0:3]')  -- Accumulate columns 0 through 3
) AS dt
ORDER BY sensor_id, reading_time;
```

**Example 10: Complete ML Pipeline Transformation**
```sql
-- Transform training data for machine learning model
-- This example shows how binning fits into ML pipeline

-- Step 1: Already completed TD_BinCodeFit to create ML_FeatureBinsFit

-- Step 2: Transform training data
CREATE TABLE ml_training_transformed AS (
    SELECT * FROM TD_BinCodeTransform (
        ON ml_training_data AS InputTable
        ON ML_FeatureBinsFit AS FitTable DIMENSION
        USING
        Accumulate ('customer_id', 'target_variable')
    ) AS dt
) WITH DATA;

-- Step 3: Transform test data using the same bins
CREATE TABLE ml_test_transformed AS (
    SELECT * FROM TD_BinCodeTransform (
        ON ml_test_data AS InputTable
        ON ML_FeatureBinsFit AS FitTable DIMENSION
        USING
        Accumulate ('customer_id')
    ) AS dt
) WITH DATA;
```

### Use Cases and Applications

**1. Machine Learning Preprocessing**
- Convert continuous features to categorical for decision trees
- Create ordinal features for gradient boosting models
- Prepare features for algorithms that handle categorical data better
- Reduce dimensionality by grouping similar values

**2. Risk Management**
- Transform credit scores into risk categories
- Categorize financial exposure levels
- Create risk tiers from probability scores
- Classify debt-to-income ratios

**3. Customer Analytics**
- Segment customers by purchase amounts
- Categorize customer lifetime value
- Group by engagement levels
- Create demographic segments from ages

**4. Operational Monitoring**
- Categorize system performance metrics
- Create alert severity levels from numeric thresholds
- Group response times into SLA categories
- Classify resource utilization levels

**5. Healthcare Analytics**
- Categorize patient ages for demographic studies
- Group BMI values into health categories
- Classify blood pressure readings
- Create risk categories from test results

**6. Financial Analysis**
- Create income brackets for analysis
- Categorize investment amounts
- Group interest rates into tiers
- Classify transaction sizes

### Important Notes
- Input data must have the same structure as the data used for TD_BinCodeFit
- FitTable contains all bin definitions from TD_BinCodeFit
- Transformation is applied consistently across all rows
- Values outside defined bin ranges may need special handling
- Original numeric precision is lost after transformation
- Transformation is deterministic - same input always produces same output
- Use Accumulate parameter to preserve necessary columns for downstream analysis
- Target columns are converted from numeric to VARCHAR containing bin labels
- Multiple target columns can be transformed simultaneously
- The function copies bin labels, not the original numeric values

### Binning Best Practices
1. **Understand Data Distribution**: Use TD_Histogram and TD_UnivariateStatistics before binning
2. **Choose Appropriate Bin Count**: Balance between information retention and simplification
3. **Consider Domain Knowledge**: Use variable-width bins when you have domain expertise
4. **Validate Bins**: Check that bins capture meaningful distinctions
5. **Document Bin Definitions**: Keep clear records of what each bin represents
6. **Test on Hold-out Data**: Ensure bins work well on unseen data
7. **Monitor Bin Usage**: Check that all bins contain reasonable numbers of observations

### Related Functions
- **TD_BinCodeFit** - Creates bin definitions (must be run before TD_BinCodeTransform)
- **TD_Histogram** - Analyze data distribution to inform binning decisions
- **TD_UnivariateStatistics** - Understand data characteristics before binning
- **TD_OrdinalEncodingTransform** - Alternative encoding for ordered categories
- **TD_OneHotEncodingTransform** - Alternative encoding creating binary columns

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Transform Functions
