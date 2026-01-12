# TD_OneHotEncodingTransform

### Function Name
**TD_OneHotEncodingTransform**

### Description
TD_OneHotEncodingTransform encodes specified attributes and categorical values as one-hot numeric vectors using the output from TD_OneHotEncodingFit. This function performs the actual transformation of categorical variables into binary (0 or 1) columns, creating a separate binary column for each unique category value.

One-hot encoding is essential for machine learning algorithms that cannot work directly with categorical data. By converting each category into a binary column, the transformation eliminates any implied ordinal relationship between categories and enables algorithms like linear regression, neural networks, and distance-based models to process categorical features effectively.

### When the Function Would Be Used
- **Machine Learning Preprocessing**: Apply encoding to training and test datasets
- **Feature Transformation**: Convert categorical variables to numeric binary vectors
- **Model Input Preparation**: Prepare encoded features for algorithms requiring numeric input
- **Consistent Encoding**: Apply same encoding scheme to multiple datasets
- **Production Pipelines**: Transform new data using pre-defined encoding specifications
- **Cross-Validation**: Apply consistent encoding across different data folds
- **A/B Testing**: Ensure consistent feature encoding across test groups
- **Real-time Scoring**: Transform categorical features in production environments
- **Data Integration**: Standardize categorical representations across data sources
- **Eliminating Ordinal Bias**: Prevent models from learning false ordering relationships

### Syntax

**Dense Input Format:**
```sql
TD_OneHotEncodingTransform (
    ON { table | view | (query) } AS InputTable [ PARTITION BY ANY ]
    ON { table | view | (query) } AS FitTable AS FitTableAlias DIMENSION
    USING
    [ Accumulate ({'accumulate_column' | 'accumulate_column_range'}[,...]) ]
)
```

**Sparse Input Format:**
```sql
TD_OneHotEncodingTransform (
    ON { table | view | (query) } AS InputTable PARTITION BY attribute_column
    ON { table | view | (query) } AS FitTable AS FitTableAlias DIMENSION
    USING
    [ Accumulate ({'accumulate_column' | 'accumulate_column_range'}[,...]) ]
)
```

### Required Syntax Elements for TD_OneHotEncodingTransform

**ON clause (InputTable)**
- Accepts the InputTable clause containing data to transform
- Must have same structure as data used for TD_OneHotEncodingFit

**ON clause (FitTable DIMENSION)**
- Accepts the FitTable clause (output from TD_OneHotEncodingFit)
- Contains encoding specifications and category definitions

### Optional Syntax Elements for TD_OneHotEncodingTransform

**Accumulate**
- Specify input table column names to copy to the output table
- Useful for preserving identifiers, keys, and metadata columns
- Supports column range notation

### Input Table Schema

**Dense InputTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | CHAR or VARCHAR (CHARACTER SET LATIN or UNICODE) | Categorical columns to be encoded as specified in TD_OneHotEncodingFit |
| accumulate_column | ANY | [Optional] Columns to preserve in output table |

**Sparse InputTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| attribute_column | CHAR or VARCHAR (CHARACTER SET LATIN or UNICODE) | Column containing attribute names |
| value_column | CHAR or VARCHAR (CHARACTER SET LATIN or UNICODE) | Column containing attribute values |
| accumulate_column | ANY | [Optional] Columns to preserve in output table |

**FitTable Schema:**

See TD_OneHotEncodingFit Output table schema. This is the output created by TD_OneHotEncodingFit function.

### Output Table Schema

**Dense Input Output:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| accumulate_column | Same as InputTable | Columns specified in Accumulate parameter |
| <targetColumn>_<category1> | INTEGER | Binary column: 1 if row has category1, 0 otherwise |
| <targetColumn>_<category2> | INTEGER | Binary column: 1 if row has category2, 0 otherwise |
| ... | INTEGER | One column for each category value |
| <targetColumn>_other | INTEGER | Binary column: 1 if value not in specified categories, 0 otherwise |

**Sparse Input Output:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| accumulate_column | Same as InputTable | Columns specified in Accumulate parameter |
| <attribute>_<value1> | INTEGER | Binary column: 1 if attribute has value1, 0 otherwise |
| <attribute>_<value2> | INTEGER | Binary column: 1 if attribute has value2, 0 otherwise |
| ... | INTEGER | One column for each attribute-value pair |

### Code Examples

**Input Data: onehot_titanic_dataset**
```
Passenger_id  Survived  Pclass  Name                  Age  Gender  City  Cabin
1             0         A       Mr. Owen Harris       22   male    Pune  a
2             1         B       Mrs. John Bradley     38   female  Hyd   a
3             1         C       Mrs. Laina            26   female  Pune  b
4             0         B       Mrs. Jacques Heath    25   female  Hyd   c
5             1         D       Mr. John Doe          27   male    Del   a
6             1         E       Mr. Ben Tennison      22   male    Hyd   b
```

**FitTable: nonLinearCombineFit_output** (created by TD_OneHotEncodingFit)
```
Gender  Gender_female  Gender_male  Gender_other  Cabin  Cabin_a  Cabin_b  Cabin_c  Cabin_other  City  City_Del  City_Hyd  City_Pune
```

**Example 1: Dense Input with Auto Approach**
```sql
-- First create fit table
CREATE TABLE onehot_fit AS (
    SELECT * FROM TD_OneHotEncodingFit(
        ON onehot_titanic_dataset AS INPUTTABLE
        USING
        TargetColumn('Gender','Cabin','City')
        OtherColumnName('other')
        IsInputDense('true')
        CategoryCounts(2,3,3)
        Approach('Auto')
    ) AS dt
) WITH DATA;

-- Then apply transformation
SELECT * FROM TD_OneHotEncodingTransform (
    ON onehot_titanic_dataset AS InputTable
    ON onehot_fit AS FitTable DIMENSION
    USING
    Accumulate('Passenger_id', 'Survived', 'Pclass', 'Name', 'Age')
) AS dt
ORDER BY Passenger_id;
```

**Output:**
```
Passenger_id  Survived  Pclass  Name                  Age  Gender_female  Gender_male  Gender_other  Cabin_a  Cabin_b  Cabin_c  Cabin_other  City_Del  City_Hyd  City_Pune
1             0         A       Mr. Owen Harris       22   0              1            0             1        0        0        0            0         0         1
2             1         B       Mrs. John Bradley     38   1              0            0             1        0        0        0            0         1         0
3             1         C       Mrs. Laina            26   1              0            0             0        1        0        0            0         0         1
4             0         B       Mrs. Jacques Heath    25   1              0            0             0        0        1        0            0         1         0
5             1         D       Mr. John Doe          27   0              1            0             1        0        0        0            1         0         0
6             1         E       Mr. Ben Tennison      22   0              1            0             0        1        0        0            0         1         0
```

**Example 2: Single Column Encoding**
```sql
-- Fit on training data
CREATE TABLE region_fit AS (
    SELECT * FROM TD_OneHotEncodingFit(
        ON customer_train AS INPUTTABLE
        USING
        TargetColumn('region')
        IsInputDense('true')
        CategoryCounts(4)
        Approach('Auto')
    ) AS dt
) WITH DATA;

-- Transform training data
SELECT * FROM TD_OneHotEncodingTransform (
    ON customer_train AS InputTable
    ON region_fit AS FitTable DIMENSION
    USING
    Accumulate('customer_id', 'target')
) AS dt
ORDER BY customer_id;
```

**Example 3: Transform Test Data with Same Encoding**
```sql
-- Use the same fit table created from training data
SELECT * FROM TD_OneHotEncodingTransform (
    ON customer_test AS InputTable
    ON region_fit AS FitTable DIMENSION
    USING
    Accumulate('customer_id')
) AS dt
ORDER BY customer_id;
```

**Example 4: Multiple Columns with Different Category Counts**
```sql
-- Fit table with multiple columns
CREATE TABLE product_fit AS (
    SELECT * FROM TD_OneHotEncodingFit(
        ON product_data AS INPUTTABLE
        USING
        TargetColumn('category', 'brand', 'color')
        IsInputDense('true')
        CategoryCounts(5, 10, 7)
        Approach('Auto')
    ) AS dt
) WITH DATA;

-- Transform with accumulation
SELECT * FROM TD_OneHotEncodingTransform (
    ON product_data AS InputTable
    ON product_fit AS FitTable DIMENSION
    USING
    Accumulate('product_id', 'price', 'stock_level')
) AS dt;
```

**Example 5: Using CategoryTable with List Approach**
```sql
-- Create fit with explicit categories
CREATE TABLE survey_fit AS (
    SELECT * FROM TD_OneHotEncodingFit(
        ON survey_data AS INPUTTABLE
        ON category_definitions AS categoryTable DIMENSION
        USING
        TargetColumn('satisfaction')
        TargetColumnNames('column_name')
        CategoriesColumn('category')
        IsInputDense('true')
        Approach('List')
    ) AS dt
) WITH DATA;

-- Transform survey responses
SELECT * FROM TD_OneHotEncodingTransform (
    ON survey_data AS InputTable
    ON survey_fit AS FitTable DIMENSION
    USING
    Accumulate('survey_id', 'respondent_id', 'survey_date')
) AS dt
ORDER BY survey_id;
```

**Example 6: Sparse Input Format**
```sql
-- Create sparse input fit table
CREATE TABLE sparse_fit AS (
    SELECT * FROM TD_OneHotEncodingFit(
        ON sparse_features AS InputTable PARTITION BY attribute_column
        USING
        IsInputDense('false')
        TargetAttributes('Gender', 'Cabin', 'City')
        AttributeColumn('attribute_column')
        ValueColumn('value_column')
    ) AS dt
) WITH DATA;

-- Transform sparse data
SELECT * FROM TD_OneHotEncodingTransform (
    ON sparse_features AS InputTable PARTITION BY attribute_column
    ON sparse_fit AS FitTable DIMENSION
    USING
    Accumulate('id')
) AS dt
ORDER BY id;
```

**Example 7: Complete ML Pipeline - Training**
```sql
-- Step 1: Create fit table on training data only
CREATE TABLE ml_encoding_fit AS (
    SELECT * FROM TD_OneHotEncodingFit(
        ON training_data AS INPUTTABLE
        USING
        TargetColumn('region', 'product_type', 'customer_segment')
        IsInputDense('true')
        CategoryCounts(5, 10, 3)
        Approach('Auto')
    ) AS dt
) WITH DATA;

-- Step 2: Transform training data
CREATE TABLE training_encoded AS (
    SELECT * FROM TD_OneHotEncodingTransform (
        ON training_data AS InputTable
        ON ml_encoding_fit AS FitTable DIMENSION
        USING
        Accumulate('customer_id', 'purchase_amount', 'target')
    ) AS dt
) WITH DATA;
```

**Example 8: Complete ML Pipeline - Testing**
```sql
-- Step 3: Transform test data using same fit table
CREATE TABLE test_encoded AS (
    SELECT * FROM TD_OneHotEncodingTransform (
        ON test_data AS InputTable
        ON ml_encoding_fit AS FitTable DIMENSION
        USING
        Accumulate('customer_id', 'purchase_amount')
    ) AS dt
) WITH DATA;
```

**Example 9: Handling Unknown Categories**
```sql
-- Categories in test data not seen in training will go to 'other' column
SELECT
    customer_id,
    region_north,
    region_south,
    region_east,
    region_west,
    region_other  -- Will be 1 for any unseen regions
FROM TD_OneHotEncodingTransform (
    ON new_customers AS InputTable
    ON region_fit AS FitTable DIMENSION
    USING
    Accumulate('customer_id')
) AS dt
WHERE region_other = 1;  -- Find customers from unknown regions
```

**Example 10: Column Range Notation**
```sql
-- Use column range to accumulate multiple columns efficiently
SELECT * FROM TD_OneHotEncodingTransform (
    ON customer_features AS InputTable
    ON features_fit AS FitTable DIMENSION
    USING
    Accumulate('[1:5]', 'customer_name', '[10:12]')  -- Accumulate columns 1-5, customer_name, and 10-12
) AS dt
ORDER BY customer_id;
```

### One-Hot Encoding Transformation Process

**Before Transformation:**
```
Passenger  Gender  City
1          male    Pune
2          female  Hyd
3          female  Pune
```

**After Transformation:**
```
Passenger  Gender_male  Gender_female  City_Pune  City_Hyd  City_Del
1          1            0              1          0         0
2          0            1              0          1         0
3          0            1              1          0         0
```

**Key Characteristics:**
- Each row has exactly one 1 in each group of binary columns
- All other values in that group are 0
- "Other" column captures categories not in fit table
- Binary encoding eliminates ordinal assumptions

### Use Cases and Applications

**1. Machine Learning Model Training**
- Prepare categorical features for scikit-learn, TensorFlow, PyTorch models
- Convert nominal categories for linear regression, logistic regression
- Create numeric inputs for neural networks
- Support ensemble methods (Random Forest, XGBoost, LightGBM)

**2. Cross-Validation Workflows**
- Apply consistent encoding across different CV folds
- Ensure fair model comparison with standardized features
- Prevent data leakage between training and validation sets
- Maintain category consistency in stratified splits

**3. Production Model Scoring**
- Transform incoming data in real-time scoring systems
- Apply pre-trained encoding schemes to new observations
- Handle unknown categories gracefully with 'other' column
- Ensure production features match training features exactly

**4. A/B Testing and Experimentation**
- Standardize categorical features across test groups
- Enable fair comparison between treatment and control
- Maintain feature consistency for causal inference
- Support uplift modeling with encoded features

**5. Distance-Based Algorithms**
- Enable K-means clustering with categorical data
- Support K-NN classification with mixed feature types
- Calculate distances between categorical observations
- Facilitate hierarchical clustering with encoded features

**6. Linear Models**
- Prepare categorical predictors for linear regression
- Support logistic regression with multiple categorical features
- Enable coefficient interpretation per category
- Avoid multicollinearity from ordinal encoding

**7. Deep Learning Applications**
- Create binary inputs for dense neural network layers
- Prepare categorical features before embedding layers
- Support attention mechanisms with category indicators
- Enable category-specific learned representations

**8. Time Series Forecasting**
- Encode seasonal categorical indicators (month, day of week)
- Transform location or store identifiers
- Create binary indicators for promotional periods
- Support hierarchical forecasting with categorical features

**9. Recommendation Systems**
- Encode user demographics and preferences
- Transform product categories and attributes
- Create interaction features between user and item categories
- Support content-based and hybrid recommendation approaches

**10. Natural Language Processing**
- Encode document categories and topics
- Transform author, genre, or language identifiers
- Create binary indicators for text metadata
- Support multi-label classification with category features

### Important Notes

**Encoding Consistency:**
- Always create FitTable on training data only
- Apply same FitTable to both training and test data
- This prevents data leakage and ensures consistent encoding
- Categories in test data not in FitTable go to 'other' column

**Multiple Column Support:**
- Available in release 17.20.03.07 and later
- Earlier versions accept only one target column
- Each target column creates its own set of binary columns

**Limitations:**
- Maximum unique columns in TargetColumn: 2018
- Maximum categories per column: 2018
- Maximum category length: 128 characters
- Target column name + category < 128 characters
- All categories treated equally (no weighting)

**Output Schema:**
- Binary columns created for each category: <column>_<category>
- Values are INTEGER type (0 or 1)
- Original categorical columns are replaced by binary columns
- Accumulate parameter preserves specified columns

**Unknown Category Handling:**
- Categories not in FitTable encoded as 1 in 'other' column
- OtherColumnName parameter specifies name of 'other' column
- Default 'other' column name is 'other'
- Essential for handling production data drift

**Sparse vs Dense:**
- Dense format: Traditional table with columns (most common)
- Sparse format: Attribute-value pairs (for very wide categorical data)
- Choose based on data structure and memory efficiency

**Performance Considerations:**
- High cardinality categories create many columns
- Consider dimensionality reduction after encoding
- May need feature selection to reduce column count
- Monitor memory usage with very high cardinality

**NULL Handling:**
- NULL values in categorical columns encoded via 'other' column
- Specify appropriate DefaultValue in FitTable if needed
- Consider imputing NULLs before encoding if business logic allows

### Best Practices

**1. Train-Test Consistency**
- Create FitTable using only training data
- Apply to training, validation, and test sets
- Never fit on test data
- Store FitTable for production use

**2. Handle High Cardinality**
- Consider grouping rare categories before encoding
- Use target encoding for very high cardinality features
- Implement minimum frequency thresholds
- Apply dimensionality reduction post-encoding

**3. Monitor Category Distribution**
- Check for categories appearing only in test data
- Validate 'other' column frequency in production
- Track category drift over time
- Retrain fit table periodically

**4. Feature Selection After Encoding**
- Many binary columns may be low variance
- Apply variance threshold to remove near-constant columns
- Use feature importance from tree models
- Consider L1 regularization to reduce features

**5. Documentation**
- Document category mappings from FitTable
- Store FitTable with model artifacts
- Track encoding version with model version
- Maintain category definitions for interpretability

**6. Production Deployment**
- Validate input categories before transformation
- Log warnings for unknown categories
- Monitor 'other' column frequencies
- Implement category mapping updates carefully

### Related Functions
- **TD_OneHotEncodingFit** - Creates encoding specifications (must be run before TD_OneHotEncodingTransform)
- **TD_OrdinalEncodingTransform** - Alternative for ordinal categorical data
- **TD_TargetEncodingTransform** - Alternative using target statistics
- **TD_ScaleTransform** - Often used after one-hot encoding for normalization
- **TD_ColumnTransformer** - Combined transformation pipeline including encoding

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Transform Functions
