# TD_OrdinalEncodingTransform

### Function Name
**TD_OrdinalEncodingTransform**

### Description
TD_OrdinalEncodingTransform applies ordinal encoding to categorical variables using the mapping specifications created by TD_OrdinalEncodingFit. This function performs the actual transformation of categorical values into ordinal integers, replacing each category with its corresponding integer value based on the predefined mapping in the FitTable.

Unlike one-hot encoding which creates multiple binary columns, ordinal encoding produces a single numeric column where each category is represented by a unique integer. This transformation is ideal for ordinal categorical data where categories have a natural ordering, such as education levels, rating scales, or size categories. The compact representation makes it particularly efficient for tree-based machine learning algorithms.

### When the Function Would Be Used
- **Apply Ordinal Encoding**: Transform categorical variables to ordinal integers
- **ML Model Training**: Prepare ordinal features for machine learning models
- **Data Pipeline Execution**: Apply consistent encoding to training and test data
- **Production Scoring**: Transform incoming categorical data in real-time systems
- **Feature Transformation**: Convert ordered categories to numeric format
- **Dimensionality Reduction**: Replace categorical columns with single numeric column
- **Tree-Based Models**: Prepare features for Random Forest, XGBoost, Decision Trees
- **Rating Analysis**: Transform survey responses to numeric scale
- **Risk Assessment**: Convert risk categories to numeric severity levels
- **Consistent Preprocessing**: Ensure same encoding applied across datasets

### Syntax

**Dense Input Format:**
```sql
TD_OrdinalEncodingTransform (
    ON { table | view | (query) } AS InputTable [ PARTITION BY ANY ]
    ON { table | view | (query) } AS FitTable AS FitTableAlias DIMENSION
    USING
    [ Accumulate ({'accumulate_column' | 'accumulate_column_range'}[,...]) ]
)
```

**Sparse Input Format:**
```sql
TD_OrdinalEncodingTransform (
    ON { table | view | (query) } AS InputTable PARTITION BY attribute_column
    ON { table | view | (query) } AS FitTable AS FitTableAlias DIMENSION
    USING
    [ Accumulate ({'accumulate_column' | 'accumulate_column_range'}[,...]) ]
)
```

### Required Syntax Elements for TD_OrdinalEncodingTransform

**ON clause (InputTable)**
- Accepts the InputTable clause containing data to transform
- Must have same structure as data used for TD_OrdinalEncodingFit

**ON clause (FitTable DIMENSION)**
- Accepts the FitTable clause (output from TD_OrdinalEncodingFit)
- Contains category-to-integer mapping specifications

### Optional Syntax Elements for TD_OrdinalEncodingTransform

**Accumulate**
- Specify input table column names to copy to the output table
- Useful for preserving identifiers, keys, and metadata columns
- Supports column range notation

### Input Table Schema

**Dense InputTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | CHAR or VARCHAR (CHARACTER SET LATIN or UNICODE) | Categorical columns to be encoded as specified in TD_OrdinalEncodingFit |
| accumulate_column | ANY | [Optional] Columns to preserve in output table |

**Sparse InputTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| attribute_column | CHAR or VARCHAR (CHARACTER SET LATIN or UNICODE) | Column containing attribute names |
| value_column | CHAR or VARCHAR (CHARACTER SET LATIN or UNICODE) | Column containing attribute values |
| accumulate_column | ANY | [Optional] Columns to preserve in output table |

**FitTable Schema:**

See TD_OrdinalEncodingFit Output table schema. This is the output created by TD_OrdinalEncodingFit function.

### Output Table Schema

**Dense Input Output:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| accumulate_column | Same as InputTable | Columns specified in Accumulate parameter |
| <targetColumn> | INTEGER | Ordinal integer values replacing original categorical values |

**Sparse Input Output:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| accumulate_column | Same as InputTable | Columns specified in Accumulate parameter |
| attribute_column | VARCHAR | Attribute names preserved from input |
| value_column | INTEGER | Ordinal integer values for each attribute |

### Code Examples

**Input Data: titanic_ordinal_dataset**
```
Passenger_id  Survived  Pclass      Name                  Age  Gender  Education
1             0         Third       Mr. Owen Harris       22   male    High School
2             1         First       Mrs. John Bradley     38   female  Bachelor
3             1         Third       Mrs. Laina            26   female  Master
4             1         First       Mrs. Jacques Heath    35   female  PhD
5             0         Second      Mr. William Henry     35   male    Bachelor
6             1         Second      Mr. Ben Tennison      22   male    High School
```

**FitTable: ordinal_fit** (created by TD_OrdinalEncodingFit)
```
Education  Education_HighSchool  Education_Bachelor  Education_Master  Education_PhD  Education_TD_OTHER_CATEGORY
           1                     2                   3                 4              -1
```

**Example 1: Basic Ordinal Transformation**
```sql
-- First create fit table
CREATE TABLE ordinal_fit AS (
    SELECT * FROM TD_OrdinalEncodingFit(
        ON titanic_ordinal_dataset AS INPUTTABLE
        USING
        TargetColumns('Education', 'Pclass')
        IsInputDense('true')
        Approach('List')
        CategoricalValues('High School', 'Bachelor', 'Master', 'PhD')
        StartValue(1)
    ) AS dt
) WITH DATA;

-- Then apply transformation
SELECT * FROM TD_OrdinalEncodingTransform (
    ON titanic_ordinal_dataset AS InputTable
    ON ordinal_fit AS FitTable DIMENSION
    USING
    Accumulate('Passenger_id', 'Survived', 'Name', 'Age', 'Gender')
) AS dt
ORDER BY Passenger_id;
```

**Output:**
```
Passenger_id  Survived  Name                  Age  Gender  Education  Pclass
1             0         Mr. Owen Harris       22   male    1          3
2             1         Mrs. John Bradley     38   female  2          1
3             1         Mrs. Laina            26   female  3          3
4             1         Mrs. Jacques Heath    35   female  4          1
5             0         Mr. William Henry     35   male    2          2
6             1         Mr. Ben Tennison      22   male    1          2
```

**Example 2: Rating Scale Transformation**
```sql
-- Fit table for 1-5 rating scale
CREATE TABLE rating_fit AS (
    SELECT * FROM TD_OrdinalEncodingFit(
        ON survey_data AS INPUTTABLE
        USING
        TargetColumns('satisfaction')
        IsInputDense('true')
        Approach('List')
        CategoricalValues('Very Dissatisfied', 'Dissatisfied', 'Neutral', 'Satisfied', 'Very Satisfied')
        StartValue(1)
    ) AS dt
) WITH DATA;

-- Transform survey responses
SELECT * FROM TD_OrdinalEncodingTransform (
    ON survey_data AS InputTable
    ON rating_fit AS FitTable DIMENSION
    USING
    Accumulate('survey_id', 'customer_id', 'survey_date')
) AS dt
ORDER BY survey_id;
```

**Example 3: Transform Training Data**
```sql
-- Apply encoding to training set
CREATE TABLE training_encoded AS (
    SELECT * FROM TD_OrdinalEncodingTransform (
        ON training_data AS InputTable
        ON ordinal_fit AS FitTable DIMENSION
        USING
        Accumulate('customer_id', 'purchase_amount', 'target')
    ) AS dt
) WITH DATA;
```

**Example 4: Transform Test Data with Same Encoding**
```sql
-- Apply same encoding to test set
CREATE TABLE test_encoded AS (
    SELECT * FROM TD_OrdinalEncodingTransform (
        ON test_data AS InputTable
        ON ordinal_fit AS FitTable DIMENSION
        USING
        Accumulate('customer_id', 'purchase_amount')
    ) AS dt
) WITH DATA;
```

**Example 5: Multiple Columns Transformation**
```sql
-- Transform multiple ordinal columns
SELECT * FROM TD_OrdinalEncodingTransform (
    ON customer_data AS InputTable
    ON multi_ordinal_fit AS FitTable DIMENSION
    USING
    Accumulate('customer_id', 'name', 'registration_date')
) AS dt
ORDER BY customer_id;
```

**Example 6: Size Categories**
```sql
-- Fit for product sizes
CREATE TABLE size_fit AS (
    SELECT * FROM TD_OrdinalEncodingFit(
        ON product_data AS INPUTTABLE
        USING
        TargetColumns('size')
        IsInputDense('true')
        Approach('List')
        CategoricalValues('XS', 'S', 'M', 'L', 'XL', 'XXL')
        StartValue(0)
    ) AS dt
) WITH DATA;

-- Transform product sizes
SELECT
    product_id,
    product_name,
    size,
    price,
    stock
FROM TD_OrdinalEncodingTransform (
    ON product_data AS InputTable
    ON size_fit AS FitTable DIMENSION
    USING
    Accumulate('product_id', 'product_name', 'price', 'stock')
) AS dt
WHERE size >= 3;  -- Filter for L, XL, XXL (3, 4, 5)
```

**Example 7: Risk Level Transformation**
```sql
-- Transform risk levels to numeric scale
SELECT * FROM TD_OrdinalEncodingTransform (
    ON risk_assessments AS InputTable
    ON risk_fit AS FitTable DIMENSION
    USING
    Accumulate('assessment_id', 'customer_id', 'assessment_date', 'score')
) AS dt
ORDER BY risk_level DESC;  -- Order by encoded risk level (highest first)
```

**Example 8: Sparse Input Format**
```sql
-- Create sparse fit table
CREATE TABLE sparse_ordinal_fit AS (
    SELECT * FROM TD_OrdinalEncodingFit(
        ON sparse_features AS InputTable PARTITION BY attribute_column
        USING
        IsInputDense('false')
        TargetAttributes('Education', 'Skill_Level')
        AttributeColumn('attribute_column')
        ValueColumn('value_column')
        Approach('Auto')
        StartValue(0)
    ) AS dt
) WITH DATA;

-- Transform sparse data
SELECT * FROM TD_OrdinalEncodingTransform (
    ON sparse_features AS InputTable PARTITION BY attribute_column
    ON sparse_ordinal_fit AS FitTable DIMENSION
    USING
    Accumulate('id')
) AS dt
ORDER BY id;
```

**Example 9: Handling Unknown Categories**
```sql
-- Transform data with potential unknown categories
SELECT
    customer_id,
    education_level,
    CASE
        WHEN education_level = -1 THEN 'Unknown'
        ELSE CAST(education_level AS VARCHAR(10))
    END AS education_category
FROM TD_OrdinalEncodingTransform (
    ON new_customers AS InputTable
    ON education_fit AS FitTable DIMENSION
    USING
    Accumulate('customer_id')
) AS dt
WHERE education_level = -1;  -- Find customers with unknown education
```

**Example 10: Complete ML Pipeline**
```sql
-- Step 1: Fit on training data (already done)

-- Step 2: Transform training data
CREATE TABLE training_features AS (
    SELECT * FROM TD_OrdinalEncodingTransform (
        ON training_raw AS InputTable
        ON ordinal_fit AS FitTable DIMENSION
        USING
        Accumulate('customer_id', 'target', 'numeric_feature1', 'numeric_feature2')
    ) AS dt
) WITH DATA;

-- Step 3: Transform test data with same encoding
CREATE TABLE test_features AS (
    SELECT * FROM TD_OrdinalEncodingTransform (
        ON test_raw AS InputTable
        ON ordinal_fit AS FitTable DIMENSION
        USING
        Accumulate('customer_id', 'numeric_feature1', 'numeric_feature2')
    ) AS dt
) WITH DATA;

-- Step 4: Now both datasets have consistent ordinal encoding
SELECT
    'Training' AS dataset,
    COUNT(*) AS row_count,
    AVG(education_level) AS avg_education,
    AVG(experience_level) AS avg_experience
FROM training_features
UNION ALL
SELECT
    'Test' AS dataset,
    COUNT(*) AS row_count,
    AVG(education_level) AS avg_education,
    AVG(experience_level) AS avg_experience
FROM test_features;
```

### Ordinal Transformation Process

**Before Transformation:**
```
Passenger  Education
1          High School
2          Bachelor
3          Master
4          PhD
5          Bachelor
```

**After Transformation (with StartValue=1):**
```
Passenger  Education
1          1
2          2
3          3
4          4
5          2
```

**Key Characteristics:**
- Each category mapped to unique integer
- Order preserved: High School (1) < Bachelor (2) < Master (3) < PhD (4)
- Single column output (compact representation)
- Unknown categories mapped to TD_OTHER_CATEGORY value (typically -1)
- Integer values enable numeric operations and comparisons

### Use Cases and Applications

**1. Machine Learning Model Training**
- Prepare ordinal features for tree-based models (Random Forest, XGBoost, LightGBM)
- Encode categorical variables with natural ordering
- Reduce feature dimensionality vs one-hot encoding
- Support gradient boosting algorithms with ordinal features

**2. Survey and Feedback Analysis**
- Transform Likert scale responses to numeric values
- Encode satisfaction ratings (1-5, 1-7 scales)
- Map NPS categories for analysis
- Support statistical analysis of ordinal data

**3. Educational Analytics**
- Transform education levels to numeric scale
- Encode academic grades (A, B, C, D, F)
- Map skill proficiency levels
- Analyze educational progression patterns

**4. Risk and Compliance**
- Encode risk levels (Low, Medium, High, Critical) for scoring
- Transform severity categories in incident management
- Map priority levels for task management
- Support risk-weighted calculations

**5. E-commerce and Retail**
- Transform product size categories for inventory analysis
- Encode customer loyalty tiers for segmentation
- Map shipping priority levels
- Support product filtering and sorting

**6. Healthcare and Medical**
- Encode pain scales (0-10) for analysis
- Transform disease severity levels
- Map treatment urgency categories
- Support clinical decision support systems

**7. Human Resources**
- Transform job seniority levels for career analysis
- Encode performance ratings numerically
- Map experience categories
- Support compensation and promotion analysis

**8. Financial Services**
- Encode credit rating categories for risk models
- Transform risk tolerance levels
- Map investment experience for suitability analysis
- Support credit scoring and underwriting

**9. Customer Relationship Management**
- Transform customer value tiers (Bronze, Silver, Gold)
- Encode engagement levels (Low, Medium, High)
- Map customer lifecycle stages
- Support targeted marketing and segmentation

**10. Quality Management**
- Encode defect severity levels for prioritization
- Transform quality grades for analysis
- Map inspection results
- Support quality metrics and KPIs

### Important Notes

**Encoding Consistency:**
- Always create FitTable on training data only
- Apply same FitTable to training, validation, and test data
- This prevents data leakage and ensures consistent encoding
- Categories not in FitTable mapped to TD_OTHER_CATEGORY value

**Unknown Category Handling:**
- New categories in production data mapped to TD_OTHER_CATEGORY
- Default TD_OTHER_CATEGORY value typically -1
- Monitor frequency of unknown categories
- Consider retraining fit table if many unknowns appear

**Output Data Type:**
- Original categorical columns replaced with INTEGER type
- Values are ordinal integers based on FitTable mapping
- Can perform numeric operations (>, <, >=, <=, AVG, etc.)
- Suitable for tree-based models and numeric algorithms

**Multiple Column Support:**
- Can transform multiple ordinal columns in single operation
- Each column transformed independently according to FitTable
- Original column names preserved with integer values

**Sparse vs Dense:**
- Dense format: Traditional table with columns (most common)
- Sparse format: Attribute-value pairs (for very wide data)
- Choose based on data structure and efficiency needs

**Model Compatibility:**
- **Tree-based models**: Excellent compatibility (Random Forest, XGBoost, Decision Trees)
- **Linear models**: Use with caution (assumes equal distances between levels)
- **Neural networks**: Consider embedding layers as alternative
- **Distance-based algorithms**: Consider scaling after encoding

**NULL Handling:**
- NULL values in categorical columns treated as unknown category
- Mapped to TD_OTHER_CATEGORY value
- Consider imputing NULLs before encoding if business logic allows

**Performance Considerations:**
- More efficient than one-hot encoding (single column vs many)
- Faster computation for tree-based algorithms
- Reduced memory footprint
- Better for high-cardinality ordinal features

### Best Practices

**1. Train-Test Consistency**
- Create FitTable using only training data
- Apply to training, validation, and test sets
- Never fit on test data
- Store FitTable with model artifacts for production

**2. Verify Ordering Preserved**
- Check that integer mappings reflect correct ordering
- Validate StartValue and increments are appropriate
- Test with sample data before full transformation
- Document ordering logic for interpretability

**3. Monitor Unknown Categories**
- Track frequency of TD_OTHER_CATEGORY in production
- Implement alerts for high unknown rates
- Consider retraining when category distributions shift
- Log unknown categories for investigation

**4. Handle Edge Cases**
- Plan for categories not seen in training
- Implement validation for input data quality
- Consider business rules for unknown categories
- Test transformation with boundary values

**5. Feature Engineering**
- Consider interactions with other features
- Combine with other encoding techniques when appropriate
- Apply scaling if using with distance-based algorithms
- Monitor for concept drift in categorical distributions

**6. Documentation and Governance**
- Document category-to-integer mappings from FitTable
- Store FitTable with model version control
- Track encoding schema changes
- Maintain data dictionary for encoded features

**7. Production Deployment**
- Validate input categories before transformation
- Implement error handling for malformed data
- Monitor transformation performance
- Cache FitTable for real-time scoring efficiency

**8. Model Interpretability**
- Maintain mapping from integers back to categories
- Document what each integer value represents
- Consider impact on model explanations
- Provide category labels in model outputs when needed

### Related Functions
- **TD_OrdinalEncodingFit** - Creates encoding specifications (must be run before TD_OrdinalEncodingTransform)
- **TD_OneHotEncodingTransform** - Alternative for nominal categorical data
- **TD_TargetEncodingTransform** - Alternative using target variable statistics
- **TD_ScaleTransform** - Often used after ordinal encoding for normalization
- **TD_ColumnTransformer** - Combined transformation pipeline including encoding

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Transform Functions
