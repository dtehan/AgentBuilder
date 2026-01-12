# TD_OneHotEncodingFit

### Function Name
**TD_OneHotEncodingFit**

### Description
TD_OneHotEncodingFit outputs a table of attributes and categorical values to input to TD_OneHotEncodingTransform, which encodes them as one-hot numeric vectors. A one-hot vector contains 0 or 1, where it is set to 1 if a specific categorical value is true (for example, M in a gender column would be 1, all other values are 0).

One hot encoding is a technique used to represent categorical data as numerical data by creating a binary vector for each category or level of a categorical variable, with each vector having a length equal to the number of possible categories.

### When the Function Would Be Used
- **Machine Learning Preprocessing**: Convert categorical variables to numeric format for algorithms
- **Categorical Feature Encoding**: Prepare categorical data for models requiring numeric input
- **Eliminating Ordinal Bias**: Avoid imposing false ordering on nominal categories
- **Neural Networks**: Create numeric inputs for deep learning models
- **Logistic Regression**: Prepare categorical predictors for regression analysis
- **Tree-Based Models**: Enhance decision tree and random forest performance
- **Distance-Based Algorithms**: Enable K-means, KNN with categorical data
- **Dimensionality Expansion**: Create multiple binary features from single categorical column
- **Feature Engineering**: Generate interaction-ready binary features
- **Avoiding Label Encoding Bias**: Prevent models from learning incorrect ordinal relationships

### One Hot Encoding Concepts

**What is One Hot Encoding?**

In one hot encoding:
- A value of 1 is assigned to the corresponding category for a particular observation
- A value of 0 is assigned to all other categories
- This results in a matrix of 1's and 0's where each row represents a single observation
- Each column represents a category

**Example:**

Original data:
```
Fruit          Category_Value  Price
apple          1               5
mango          2               10
apple          1               15
orange         3               20
```

After one-hot encoding the Fruit column:
```
apple  mango  orange  price
1      0      0       5
0      1      0       10
1      0      0       15
0      0      1       20
```

**Benefits:**
- No ordinal relationship implied between categories
- Each category treated independently
- Prevents bias in algorithms that interpret numeric values as ordered
- Works well with linear models and neural networks

### Syntax

**Dense Input Format:**
```sql
TD_OneHotEncodingFit (
    ON { table | view | (query) } AS InputTable [ PARTITION BY ANY ]
    [ ON { table | view | (query) } AS CategoryTable DIMENSION ]
    USING
    IsInputDense ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'})
    TargetColumn ({'target_column' | 'target_column_range'}[,...])
    {
        Approach ('LIST')
        {
            CategoricalValues ('category_i'[,...])
            |
            TargetColumnNames ('targetcolnames_column')
            CategoriesColumn ('category_column')
        }
    }
    |
    Approach ('AUTO')
    [ OtherColumnName ('other_column_name' | 'other_column_name_i', ...) ]
    [ CategoryCounts (category_count | category_count_i, ...)]
)
```

**Sparse Input Format:**
```sql
TD_OneHotEncodingFit (
    ON { table | view | (query) } AS InputTable PARTITION BY attribute_column
    USING
    IsInputDense ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'})
    TargetAttributes ('attribute_name'[,...])
    [ OtherAttributesNames ('other_attribute_name'[,...])]
    AttributeColumn ('attribute_column')
    ValueColumn ('value_column_name')
)
```

### Required Syntax Elements for TD_OneHotEncodingFit

**ON clause**
- Accept the InputTable clause
- Applicable for both dense and sparse input format

**IsInputDense**
- Specify whether the input is dense or sparse
- 'true' for dense format, 'false' for sparse format

**TargetColumn**
- [Required with IsInputDense ('true')]
- Specify the InputTable categorical columns to be encoded
- Maximum unique columns: 2018

**CategoryCounts**
- [Required with AUTO Approach]
- Specify category counts for each TargetColumn
- Number of values must equal number of TargetColumns

**CategoricalValues**
- [Required with Approach LIST and single target column]
- Specify list of categories to encode in desired order
- Maximum categories: 2018
- Maximum characters: target column name + category < 128

**AttributeColumn**
- [Required with IsInputDense ('false')]
- Specify name of InputTable column containing attributes

**ValueColumn**
- [Required with IsInputDense ('false')]
- Specify name of InputTable column containing attribute values

**TargetAttributes**
- [Required with IsInputDense ('false')]
- Specify attributes to encode in one-hot form
- Every target_attribute must be in attribute_column

### Optional Syntax Elements for TD_OneHotEncodingFit

**ON clause for CategoryTable**
- Accept CategoryTable clause for dense input only

**TargetColumnNames**
- Specify CategoryTable column containing target column names

**CategoriesColumn**
- Specify CategoryTable column containing category values

**Approach**
- Specify method: 'AUTO' (from input data) or 'LIST' (user-provided)
- Default: 'LIST'

**OtherColumnName**
- [Optional with IsInputDense ('true')]
- Column name for one-hot encoding of unspecified values
- Default: 'other'

**OtherAttributeNames**
- [Optional with IsInputDense ('false')]
- Category name for attributes not in TargetAttributes
- nth other_attribute corresponds to nth target_attribute

### Input Table Schema

**Dense InputTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | CHAR or VARCHAR (CHARACTER SET LATIN or UNICODE) | Columns from InputTable to be encoded |

**Sparse InputTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| attribute_column | CHAR or VARCHAR (CHARACTER SET LATIN or UNICODE) | Column containing attributes |
| value_column | CHAR or VARCHAR (CHARACTER SET LATIN or UNICODE) | Column containing attribute values |

**CategoryTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| ColumnName | CHAR or VARCHAR (CHARACTER SET LATIN or UNICODE) | Column containing target column names |
| CategoryValue | CHAR or VARCHAR (CHARACTER SET LATIN or UNICODE) | Column containing category values (max 128 chars) |

### Output Table Schema

**Dense Input Output:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| targetColumn_name | INTEGER | Used to identify TargetColumns in Transform function |
| <targetColumn>_<cat_value> | VARCHAR (CHARACTER SET UNICODE) | Preserves column definition for Transform function. Contains NULL values |
| <targetColumn>_<other> | VARCHAR (CHARACTER SET UNICODE) | Preserves column definition for Transform function. Contains NULL values |

**Sparse Input Output:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| TD_VALUE_TYPE_OHEFIT | INTEGER | 1 if row has attribute_column-target_attribute pair. 0 if row has attribute_column-other_attribute pair |
| attribute_column | VARCHAR (CHARACTER SET UNICODE) | Preserves attribute column name. Contains only NULL values |
| value_column | VARCHAR (CHARACTER SET UNICODE) | Preserves value column name. Contains only NULL values |

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

**Example 1: Dense Input with Auto Approach**
```sql
SELECT * FROM TD_OneHotEncodingFit(
    ON onehot_titanic_dataset AS INPUTTABLE
    USING
    TargetColumn('Gender','Cabin','City')
    OtherColumnName('other')
    IsInputDense('true')
    CategoryCounts(2,3,3)
    Approach('Auto')
) AS dt;
```

**Output:**
```
Gender  Gender_female  Gender_male  Gender_other  Cabin  Cabin_a  Cabin_b  Cabin_c  Cabin_other  City  City_Del  City_Hyd  City_Pune
```

**Example 2: Dense Input with List Approach and CategoryTable**

First create CategoryTable:
```sql
CREATE TABLE categoryTable (
    column_name VARCHAR(20),
    category VARCHAR(20)
);

INSERT INTO categoryTable VALUES('Gender','Male');
INSERT INTO categoryTable VALUES('Gender','Female');
INSERT INTO categoryTable VALUES('Cabin','a');
INSERT INTO categoryTable VALUES('Cabin','b');
INSERT INTO categoryTable VALUES('Cabin','c');
INSERT INTO categoryTable VALUES('City','Del');
INSERT INTO categoryTable VALUES('City','Hyd');
```

Then apply fit:
```sql
SELECT * FROM TD_OneHotEncodingFit(
    ON onehot_titanic_dataset AS INPUTTABLE
    ON categoryTable AS categoryTable DIMENSION
    USING
    TargetColumn('Gender','Cabin','City')
    CategoryCounts(2,3,2)
    TargetColumnNames ('column_name')
    CategoriesColumn ('category')
    OtherColumnName('other')
    IsInputDense('true')
    Approach('List')
) AS dt;
```

**Example 3: Sparse Input Format**

First create sparse input:
```sql
CREATE TABLE onehot_sparse_input (
    id INTEGER,
    attribute_column VARCHAR(20),
    value_column VARCHAR(20)
);

INSERT INTO onehot_sparse_input VALUES (1, 'Gender', 'male');
INSERT INTO onehot_sparse_input VALUES (2, 'Gender', 'female');
INSERT INTO onehot_sparse_input VALUES (3, 'Gender', 'female');
INSERT INTO onehot_sparse_input VALUES (1, 'City', 'Del');
INSERT INTO onehot_sparse_input VALUES (2, 'City', 'Hyd');
INSERT INTO onehot_sparse_input VALUES (3, 'City', 'Pune');
```

Then apply fit:
```sql
SELECT * FROM TD_OneHotEncodingFit(
    ON onehot_sparse_input AS InputTable PARTITION BY attribute_column
    USING
    IsInputDense ('false')
    TargetAttributes ('Gender','Cabin','City')
    AttributeColumn ('attribute_column')
    ValueColumn ('value_column')
) AS dt
ORDER BY 1,2;
```

**Example 4: Single Column Encoding**
```sql
SELECT * FROM TD_OneHotEncodingFit(
    ON customer_data AS INPUTTABLE
    USING
    TargetColumn('region')
    IsInputDense('true')
    CategoryCounts(4)
    Approach('Auto')
) AS dt;
```

**Example 5: Multiple Columns with Different Category Counts**
```sql
SELECT * FROM TD_OneHotEncodingFit(
    ON product_data AS INPUTTABLE
    USING
    TargetColumn('category', 'brand', 'color')
    IsInputDense('true')
    CategoryCounts(5, 10, 7)
    Approach('Auto')
) AS dt;
```

**Example 6: Explicit Category List**
```sql
SELECT * FROM TD_OneHotEncodingFit(
    ON survey_data AS INPUTTABLE
    USING
    TargetColumn('satisfaction')
    IsInputDense('true')
    CategoricalValues('Very Satisfied', 'Satisfied', 'Neutral', 'Dissatisfied', 'Very Dissatisfied')
    Approach('List')
) AS dt;
```

**Example 7: Custom Other Column Name**
```sql
SELECT * FROM TD_OneHotEncodingFit(
    ON transaction_data AS INPUTTABLE
    USING
    TargetColumn('payment_method')
    IsInputDense('true')
    CategoryCounts(5)
    OtherColumnName('unknown_payment')
    Approach('Auto')
) AS dt;
```

**Example 8: Column Range Notation**
```sql
SELECT * FROM TD_OneHotEncodingFit(
    ON features_table AS INPUTTABLE
    USING
    TargetColumn('[3:5]')  -- Encode columns 3, 4, and 5
    IsInputDense('true')
    CategoryCounts(4, 3, 6)
    Approach('Auto')
) AS dt;
```

**Example 9: Sparse Format with Custom Other Names**
```sql
SELECT * FROM TD_OneHotEncodingFit(
    ON sparse_features AS InputTable PARTITION BY attribute_column
    USING
    IsInputDense('false')
    TargetAttributes('Color', 'Size', 'Material')
    OtherAttributesNames('Other_Color', 'Other_Size', 'Other_Material')
    AttributeColumn('attribute_column')
    ValueColumn('value_column')
) AS dt;
```

**Example 10: Complete ML Pipeline Setup**
```sql
-- Create fit table for training data
CREATE TABLE training_onehot_fit AS (
    SELECT * FROM TD_OneHotEncodingFit(
        ON training_data AS INPUTTABLE
        USING
        TargetColumn('region', 'product_type', 'customer_segment')
        IsInputDense('true')
        CategoryCounts(5, 10, 3)
        Approach('Auto')
    ) AS dt
) WITH DATA;

-- This fit table will be used for both training and test data transformation
```

### Use Cases and Applications

**1. Machine Learning Preprocessing**
- Prepare categorical features for scikit-learn, TensorFlow, PyTorch
- Convert nominal categories for regression models
- Encode features for neural networks
- Prepare data for ensemble methods

**2. Avoiding Ordinal Bias**
- Prevent false ordering (e.g., red=1, blue=2, green=3 implies ordering)
- Treat each category independently
- Eliminate numeric relationship assumptions
- Improve model interpretability

**3. Distance-Based Algorithms**
- Enable K-means clustering with categorical data
- Prepare features for K-NN classification
- Support hierarchical clustering
- Calculate distances between categorical observations

**4. Linear Models**
- Prepare categorical predictors for linear regression
- Support logistic regression with categorical features
- Enable GLM with nominal predictors
- Facilitate coefficient interpretation per category

**5. Deep Learning**
- Create binary inputs for neural networks
- Prepare embeddings layer inputs
- Support categorical cross-entropy loss
- Enable attention mechanisms with categories

**6. Feature Engineering**
- Create interaction-ready binary features
- Generate category-specific indicators
- Support conditional feature engineering
- Enable category-wise transformations

### Important Notes

**Multiple Column Support:**
- Available in release 17.20.03.07 and later
- Earlier versions accept only one target column

**Limitations:**
- Maximum unique columns in TargetColumn: 2018
- Maximum categories per column: 2018
- Maximum category length: 128 characters
- Target column name + category < 128 characters
- Returns all distinct categories including those with low frequency
- NULL categories are handled via OtherColumnName

**Auto vs List Approach:**
- **AUTO**: Discovers categories from data automatically
- **LIST**: Uses user-specified categories only
- LIST provides better control over category order
- AUTO adapts to data variations

**Dense vs Sparse:**
- **Dense**: Traditional table format with columns
- **Sparse**: Attribute-value pair format
- Choose based on data structure and storage efficiency

### Related Functions
- **TD_OneHotEncodingTransform** - Applies one-hot encoding using fit output (must be used after TD_OneHotEncodingFit)
- **TD_OrdinalEncodingFit** - Alternative for ordinal categorical data
- **TD_TargetEncodingFit** - Encoding based on target variable statistics
- **TD_BinCodeFit** - For continuous variable discretization

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Transform Functions
