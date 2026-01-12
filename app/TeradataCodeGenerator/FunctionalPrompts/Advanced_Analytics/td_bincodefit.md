# TD_BinCodeFit

### Function Name
**TD_BinCodeFit**

### Description
TD_BinCodeFit converts numeric data to categorical data by binning (also known as bucketing or discretization) the numeric data into multiple numeric ranges. Binning is a data transformation technique that divides continuous numerical data into discrete intervals or "bins" and assigns categorical labels to each bin. This process simplifies data analysis, reduces the impact of minor observation errors, and can help improve model performance by capturing non-linear relationships.

The function determines whether specified binning transformations can be applied to specified input columns and outputs a fit table to use as input to TD_BinCodeTransform, which performs the actual transformation.

### When the Function Would Be Used
- **Feature Engineering**: Creating categorical features from continuous variables for machine learning models
- **Data Simplification**: Reducing complexity of continuous variables while preserving important patterns
- **Handling Non-linear Relationships**: Capturing non-linear patterns that linear models might miss
- **Reducing Noise**: Minimizing the impact of minor measurement errors or outliers
- **Model Interpretability**: Making models easier to understand by grouping values into meaningful categories
- **Handling Skewed Distributions**: Normalizing highly skewed data by creating appropriate bins
- **Age Grouping**: Converting exact ages into age ranges (e.g., 0-20, 21-45, 46-90)
- **Income Brackets**: Grouping income values into standard brackets for analysis
- **Credit Scoring**: Creating risk categories from continuous credit scores
- **Customer Segmentation**: Grouping customers based on purchase amounts or behavior metrics

### Binning Concepts

**Equal-Width Binning**:
- Divides the data range into k equal-width intervals
- Bin width: w = (max - min) / k
- Simple and intuitive, but sensitive to outliers
- May create bins with very different frequencies

**Variable-Width Binning**:
- Allows custom bin boundaries based on domain knowledge
- Bins can have different widths
- More flexible for handling skewed distributions
- Requires manual specification of min/max values for each bin
- Maximum 10,000 bins per column

### Syntax
```sql
TD_BinCodeFit (
    ON { table | view | (query) } AS InputTable
    [ ON { table | view | (query) } AS FitTable DIMENSION ]
    USING
    MethodType ({ 'Equal-Width' | 'Variable-Width' })
    TargetColumns ({ 'target_column' | target_column_range }[,...])
    [ NBins ({ 'nbin' | nbin_i,... }) ]
    [ MinValueColumn ('minvalue_column') ]
    [ MaxValueColumn ('maxvalue_column') ]
    [ LabelColumn ('label_column') ]
    [ TargetColNames ('targetcolnames_column') ]
)
```

### Required Syntax Elements for TD_BinCodeFit

**ON clause (InputTable)**
- Accepts the InputTable clause containing numeric data to be binned

**ON clause (FitTable DIMENSION)**
- [Required with MethodType ('Variable-Width'), ignored otherwise]
- Accepts the FitTable clause containing bin specifications

**MethodType**
- Specify the binning method:
  - **'Equal-Width'**: Divides data into k equal-width intervals
  - **'Variable-Width'**: Uses custom bin boundaries from FitTable

**TargetColumns**
- Specify the InputTable columns to bin-code
- Supports column ranges using bracket notation (e.g., '[5]', '[1:3]')

**NBins**
- [Required with Equal-Width and Variable-Width methods]
- Specify the number of bins as an integer value
- If only one value specified, applies to all target columns
- Maximum value: 10,000 bins per column

### Optional Syntax Elements for TD_BinCodeFit

**MinValueColumn**
- [Required with Variable-Width method, optional with Equal-Width]
- Specify the FitTable column name containing minimum bin values

**MaxValueColumn**
- [Required with Variable-Width method, optional with Equal-Width]
- Specify the FitTable column name containing maximum bin values

**LabelColumn**
- [Optional with Variable-Width method]
- Specify the FitTable column name containing bin labels

**TargetColNames**
- [Required when FitTable has multiple target columns]
- Specify the FitTable column name containing target column names

### Input Table Schema

**InputTable Schema**

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | BYTEINT, SMALLINT, INTEGER, BIGINT, DECIMAL/NUMERIC, FLOAT, REAL, DOUBLE PRECISION | Column to bin-code |

**FitTable Schema** (Required with Variable-Width method)

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_names_column | CHAR, VARCHAR (CHARACTER SET LATIN or UNICODE) | Bin column name |
| minvalue_column | BYTEINT, SMALLINT, INTEGER, BIGINT, DECIMAL/NUMERIC, FLOAT, REAL, DOUBLE PRECISION | Minimum value of the bin |
| maxvalue_column | BYTEINT, SMALLINT, INTEGER, BIGINT, DECIMAL/NUMERIC, FLOAT, REAL, DOUBLE PRECISION | Maximum value of the bin |
| label_column | CHAR, VARCHAR (CHARACTER SET LATIN or UNICODE) | Bin labels |

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| TD_ColumnName_BINFIT | VARCHAR (CHARACTER SET UNICODE) | Bin column name |
| TD_MinValue_BINFIT | DOUBLE PRECISION | Minimum value of the bin |
| TD_MaxValue_BINFIT | DOUBLE PRECISION | Maximum value of the bin |
| TD_LabelPrefix_BINFIT | VARCHAR (CHARACTER SET UNICODE) | [Column appears only with MethodType ('Equal-Width')] Label prefix |
| TD_Label_BINFIT | VARCHAR (CHARACTER SET UNICODE) | [Column appears only with MethodType ('Variable-Width')] Bin label |
| TD_Bins_BINFIT | INTEGER | Bin count |
| TD_IndexValue_BINFIT | SMALLINT | Index value |
| TD_MaxLenLabel_BINFIT | SMALLINT | Maximum bin label length |
| target_column | Same as in Input table | Target column for TD_BinCodeTransform |

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

**Example 1: Variable-Width Binning with Custom Age Groups**

First, create a FitInput table with custom age ranges:
```sql
CREATE TABLE FitInputTable (
    ColumnName VARCHAR(20),
    MinValue DOUBLE PRECISION,
    MaxValue DOUBLE PRECISION,
    Label VARCHAR(20)
);

INSERT INTO FitInputTable VALUES ('age', 0.00, 20.00, 'Young Age');
INSERT INTO FitInputTable VALUES ('age', 21.00, 45.00, 'Middle Age');
INSERT INTO FitInputTable VALUES ('age', 46.00, 90.00, 'Old Age');
```

Then apply TD_BinCodeFit:
```sql
CREATE TABLE FitOutputTable AS (
    SELECT * FROM TD_BinCodeFit (
        ON bin_titanic_train AS InputTable
        ON FitInputTable AS FitInput DIMENSION
        USING
        TargetColumns ('age')
        MethodType ('Variable-Width')
        MinValueColumn ('MinValue')
        MaxValueColumn ('MaxValue')
        LabelColumn ('Label')
        TargetColNames ('ColumnName')
    ) AS dt
) WITH DATA;
```

**Output:**
```
TD_ColumnName_BINFIT  TD_MinValue_BINFIT  TD_MaxValue_BINFIT  TD_Label_BINFIT  TD_Bins_BINFIT  TD_IndexValue_BINFIT  TD_MaxLenLabel_BINFIT  age
age                   46.0                90.0                Old Age          3               0                     10                     null
age                   21.0                45.0                Middle Age       3               0                     10                     null
age                   0.0                 20.0                Young Age        3               0                     10                     null
```

**Example 2: Variable-Width Using Column Index**
```sql
-- Using column index [5] instead of column name 'age'
CREATE TABLE FitOutputTable AS (
    SELECT * FROM TD_BinCodeFit (
        ON bin_titanic_train AS InputTable
        ON FitInputTable AS FitInput DIMENSION
        USING
        TargetColumns ('[5]')
        MethodType ('Variable-Width')
        MinValueColumn ('MinValue')
        MaxValueColumn ('MaxValue')
        LabelColumn ('Label')
        TargetColNames ('ColumnName')
    ) AS dt
) WITH DATA;
```

**Example 3: Equal-Width Binning**
```sql
-- Divide fare into 5 equal-width bins
CREATE TABLE FareBinsFit AS (
    SELECT * FROM TD_BinCodeFit (
        ON bin_titanic_train AS InputTable
        USING
        TargetColumns ('fare')
        MethodType ('Equal-Width')
        NBins ('5')
    ) AS dt
) WITH DATA;
```

**Example 4: Multiple Columns with Variable-Width**
```sql
-- Create FitInput for multiple columns
CREATE TABLE MultiFitInput (
    ColumnName VARCHAR(20),
    MinValue DOUBLE PRECISION,
    MaxValue DOUBLE PRECISION,
    Label VARCHAR(20)
);

INSERT INTO MultiFitInput VALUES ('age', 0, 20, 'Young');
INSERT INTO MultiFitInput VALUES ('age', 21, 60, 'Adult');
INSERT INTO MultiFitInput VALUES ('age', 61, 100, 'Senior');
INSERT INTO MultiFitInput VALUES ('fare', 0, 20, 'Low Fare');
INSERT INTO MultiFitInput VALUES ('fare', 21, 50, 'Medium Fare');
INSERT INTO MultiFitInput VALUES ('fare', 51, 100, 'High Fare');

CREATE TABLE MultiBinsFit AS (
    SELECT * FROM TD_BinCodeFit (
        ON bin_titanic_train AS InputTable
        ON MultiFitInput AS FitInput DIMENSION
        USING
        TargetColumns ('age', 'fare')
        MethodType ('Variable-Width')
        MinValueColumn ('MinValue')
        MaxValueColumn ('MaxValue')
        LabelColumn ('Label')
        TargetColNames ('ColumnName')
    ) AS dt
) WITH DATA;
```

**Example 5: Income Brackets**
```sql
-- Create custom income brackets
CREATE TABLE IncomeBins (
    ColumnName VARCHAR(20),
    MinValue DOUBLE PRECISION,
    MaxValue DOUBLE PRECISION,
    Label VARCHAR(30)
);

INSERT INTO IncomeBins VALUES ('annual_income', 0, 25000, 'Low Income');
INSERT INTO IncomeBins VALUES ('annual_income', 25001, 75000, 'Middle Income');
INSERT INTO IncomeBins VALUES ('annual_income', 75001, 150000, 'Upper Middle');
INSERT INTO IncomeBins VALUES ('annual_income', 150001, 999999999, 'High Income');

CREATE TABLE IncomeFit AS (
    SELECT * FROM TD_BinCodeFit (
        ON customer_data AS InputTable
        ON IncomeBins AS FitInput DIMENSION
        USING
        TargetColumns ('annual_income')
        MethodType ('Variable-Width')
        MinValueColumn ('MinValue')
        MaxValueColumn ('MaxValue')
        LabelColumn ('Label')
        TargetColNames ('ColumnName')
    ) AS dt
) WITH DATA;
```

**Example 6: Credit Score Risk Categories**
```sql
-- Bin credit scores into risk categories
CREATE TABLE CreditScoreBins (
    ColumnName VARCHAR(20),
    MinValue DOUBLE PRECISION,
    MaxValue DOUBLE PRECISION,
    Label VARCHAR(20)
);

INSERT INTO CreditScoreBins VALUES ('credit_score', 300, 579, 'Poor');
INSERT INTO CreditScoreBins VALUES ('credit_score', 580, 669, 'Fair');
INSERT INTO CreditScoreBins VALUES ('credit_score', 670, 739, 'Good');
INSERT INTO CreditScoreBins VALUES ('credit_score', 740, 799, 'Very Good');
INSERT INTO CreditScoreBins VALUES ('credit_score', 800, 850, 'Exceptional');

CREATE TABLE CreditScoreFit AS (
    SELECT * FROM TD_BinCodeFit (
        ON applicant_data AS InputTable
        ON CreditScoreBins AS FitInput DIMENSION
        USING
        TargetColumns ('credit_score')
        MethodType ('Variable-Width')
        MinValueColumn ('MinValue')
        MaxValueColumn ('MaxValue')
        LabelColumn ('Label')
        TargetColNames ('ColumnName')
    ) AS dt
) WITH DATA;
```

**Example 7: Temperature Ranges**
```sql
-- Create temperature range bins
CREATE TABLE TempBins (
    ColumnName VARCHAR(20),
    MinValue DOUBLE PRECISION,
    MaxValue DOUBLE PRECISION,
    Label VARCHAR(20)
);

INSERT INTO TempBins VALUES ('temperature', -50, 0, 'Freezing');
INSERT INTO TempBins VALUES ('temperature', 1, 15, 'Cold');
INSERT INTO TempBins VALUES ('temperature', 16, 25, 'Moderate');
INSERT INTO TempBins VALUES ('temperature', 26, 35, 'Warm');
INSERT INTO TempBins VALUES ('temperature', 36, 100, 'Hot');

CREATE TABLE TempFit AS (
    SELECT * FROM TD_BinCodeFit (
        ON weather_data AS InputTable
        ON TempBins AS FitInput DIMENSION
        USING
        TargetColumns ('temperature')
        MethodType ('Variable-Width')
        MinValueColumn ('MinValue')
        MaxValueColumn ('MaxValue')
        LabelColumn ('Label')
        TargetColNames ('ColumnName')
    ) AS dt
) WITH DATA;
```

**Example 8: Equal-Width for Multiple Columns**
```sql
-- Apply equal-width binning to multiple numeric columns
CREATE TABLE MultiColumnFit AS (
    SELECT * FROM TD_BinCodeFit (
        ON sales_data AS InputTable
        USING
        TargetColumns ('price', 'quantity', 'discount')
        MethodType ('Equal-Width')
        NBins ('10', '5', '3')  -- Different bin counts per column
    ) AS dt
) WITH DATA;
```

**Example 9: Transaction Amount Categories**
```sql
-- Categorize transaction amounts
CREATE TABLE TransactionBins (
    ColumnName VARCHAR(20),
    MinValue DOUBLE PRECISION,
    MaxValue DOUBLE PRECISION,
    Label VARCHAR(20)
);

INSERT INTO TransactionBins VALUES ('amount', 0, 50, 'Micro');
INSERT INTO TransactionBins VALUES ('amount', 51, 200, 'Small');
INSERT INTO TransactionBins VALUES ('amount', 201, 1000, 'Medium');
INSERT INTO TransactionBins VALUES ('amount', 1001, 5000, 'Large');
INSERT INTO TransactionBins VALUES ('amount', 5001, 999999, 'Very Large');

CREATE TABLE TransactionFit AS (
    SELECT * FROM TD_BinCodeFit (
        ON transactions AS InputTable
        ON TransactionBins AS FitInput DIMENSION
        USING
        TargetColumns ('amount')
        MethodType ('Variable-Width')
        MinValueColumn ('MinValue')
        MaxValueColumn ('MaxValue')
        LabelColumn ('Label')
        TargetColNames ('ColumnName')
    ) AS dt
) WITH DATA;
```

**Example 10: Column Range with Equal-Width**
```sql
-- Bin multiple consecutive columns using range notation
CREATE TABLE RangeBinsFit AS (
    SELECT * FROM TD_BinCodeFit (
        ON sensor_readings AS InputTable
        USING
        TargetColumns ('[3:7]')  -- Columns 3 through 7
        MethodType ('Equal-Width')
        NBins ('8')  -- Same bin count for all columns
    ) AS dt
) WITH DATA;
```

### Use Cases and Applications

**1. Machine Learning Feature Engineering**
- Convert continuous variables to categorical for tree-based models
- Create ordinal features that capture non-linear relationships
- Reduce overfitting by grouping similar values
- Handle skewed distributions in features

**2. Customer Segmentation**
- Group customers by purchase amounts (low, medium, high spenders)
- Categorize by age demographics
- Segment by transaction frequency
- Create loyalty tiers based on activity metrics

**3. Risk Assessment**
- Credit score categorization (poor, fair, good, excellent)
- Income-based risk tiers
- Age-based insurance categories
- Financial exposure levels

**4. Data Simplification**
- Reduce noise in continuous measurements
- Standardize reporting categories
- Create human-readable segments
- Simplify complex numerical ranges

**5. Performance Analysis**
- Response time categories (fast, medium, slow)
- Load level bins (low, moderate, high, critical)
- Performance score ranges
- Efficiency tiers

**6. Business Intelligence**
- Revenue brackets for reporting
- Product price tiers
- Geographic region groupings
- Time period classifications

### Important Notes
- Maximum of 10,000 bins per column
- Variable-Width method requires FitTable with bin specifications
- Equal-Width method divides range into equal intervals: w = (max - min) / k
- Bin boundaries: Function must determine whether boundary values belong to left or right bin
- The fit table output is used as input to TD_BinCodeTransform for actual transformation
- Binning is irreversible - original precision is lost after transformation
- Choose bin count carefully: too few bins lose information, too many bins may not simplify enough
- Variable-Width binning allows for domain expertise to inform bin boundaries
- Consider data distribution when choosing Equal-Width vs Variable-Width method
- For skewed distributions, Variable-Width often produces better results

### Related Functions
- **TD_BinCodeTransform** - Applies binning transformation using TD_BinCodeFit output
- **TD_Histogram** - Analyzes data distribution to inform binning decisions
- **TD_UnivariateStatistics** - Provides statistics to help determine appropriate bin boundaries
- **TD_OrdinalEncodingFit** - Encodes categorical data with ordinal values
- **TD_OneHotEncodingFit** - Creates binary vectors from categorical data

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Transform Functions
