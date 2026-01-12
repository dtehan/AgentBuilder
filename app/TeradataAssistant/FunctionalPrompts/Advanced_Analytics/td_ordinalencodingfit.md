# TD_OrdinalEncodingFit

### Function Name
**TD_OrdinalEncodingFit**

### Description
TD_OrdinalEncodingFit creates specifications for encoding categorical variables as ordinal integers. This function maps each unique category value to a specific integer, preserving the ordinal relationship between categories. Unlike one-hot encoding which creates binary columns, ordinal encoding assigns a single integer value to each category, making it ideal for ordinal categorical data where categories have a natural order.

The function outputs a table containing category-to-integer mappings that TD_OrdinalEncodingTransform uses to perform the actual transformation. This approach is particularly useful when working with ordinal data like education levels (high school < bachelor < master < PhD), rating scales (poor < fair < good < excellent), or size categories (small < medium < large).

### When the Function Would Be Used
- **Ordinal Data Encoding**: Map naturally ordered categories to integers
- **Rating Scales**: Encode survey responses (1-5 stars, Likert scales)
- **Education Levels**: Transform educational attainment (high school, bachelor's, master's, PhD)
- **Skill Levels**: Encode proficiency (beginner, intermediate, advanced, expert)
- **Size Categories**: Transform size values (XS, S, M, L, XL)
- **Severity Levels**: Encode medical or incident severity (mild, moderate, severe)
- **Risk Categories**: Map risk levels (low, medium, high, critical)
- **Seniority Levels**: Transform job levels (junior, mid-level, senior, executive)
- **Grade Categories**: Encode academic grades (F, D, C, B, A)
- **Priority Levels**: Map task priorities (low, normal, high, urgent)

### Ordinal vs One-Hot Encoding

**Ordinal Encoding:**
- Maps categories to single integer column
- Preserves natural ordering between categories
- Compact representation (1 column instead of N)
- Suitable for tree-based models
- Example: {Low: 0, Medium: 1, High: 2}

**One-Hot Encoding:**
- Creates N binary columns for N categories
- No ordering implied between categories
- Larger representation (N columns)
- Suitable for linear models, neural networks
- Example: Low=[1,0,0], Medium=[0,1,0], High=[0,0,1]

**When to Use Ordinal:**
- Categories have meaningful order
- Working with tree-based algorithms (Decision Trees, Random Forest, XGBoost)
- Need to reduce dimensionality
- Categories are truly ordinal in nature

**When to Use One-Hot:**
- Categories are nominal (no natural order)
- Working with linear models or neural networks
- Want to avoid implying false ordering
- Categories are independent

### Syntax

**Dense Input Format:**
```sql
TD_OrdinalEncodingFit (
    ON { table | view | (query) } AS InputTable [ PARTITION BY ANY ]
    [ ON { table | view | (query) } AS CategoryTable DIMENSION ]
    USING
    IsInputDense ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'})
    TargetColumns ({'target_column' | 'target_column_range'}[,...])
    {
        Approach ('LIST')
        {
            CategoricalValues ('category_i'[,...])
            |
            TargetColumnNames ('target_colnames_column')
            CategoriesColumn ('category_column')
        }
    }
    |
    Approach ('AUTO')
    [ StartValue (start_value[,...]) ]
)
```

**Sparse Input Format:**
```sql
TD_OrdinalEncodingFit (
    ON { table | view | (query) } AS InputTable PARTITION BY attribute_column
    USING
    IsInputDense ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'})
    TargetAttributes ('attribute_name'[,...])
    AttributeColumn ('attribute_column')
    ValueColumn ('value_column')
    [ Approach ('AUTO' | 'LIST') ]
    [ StartValue (start_value[,...]) ]
)
```

### Required Syntax Elements for TD_OrdinalEncodingFit

**ON clause (InputTable)**
- Accept the InputTable clause containing categorical data
- Applicable for both dense and sparse input format

**IsInputDense**
- Specify whether the input is dense or sparse
- 'true' for dense format, 'false' for sparse format

**TargetColumns**
- [Required with IsInputDense ('true')]
- Specify the InputTable categorical columns to be encoded
- Maximum 4000 unique categories per column

**TargetAttributes**
- [Required with IsInputDense ('false')]
- Specify attributes to encode in ordinal form
- Every target_attribute must be in attribute_column

**AttributeColumn**
- [Required with IsInputDense ('false')]
- Specify name of InputTable column containing attributes

**ValueColumn**
- [Required with IsInputDense ('false')]
- Specify name of InputTable column containing attribute values

**Approach**
- Specify encoding method: 'AUTO' or 'LIST'
- AUTO: Automatic ordering based on data
- LIST: User-specified ordering via CategoricalValues or CategoryTable

**CategoricalValues**
- [Required with Approach LIST and single target column]
- Specify list of categories in desired ordinal order
- First category gets lowest value (StartValue)
- Maximum 4000 unique categories

### Optional Syntax Elements for TD_OrdinalEncodingFit

**ON clause for CategoryTable**
- Accept CategoryTable clause for dense input with LIST approach
- Contains predefined category-to-integer mappings

**TargetColumnNames**
- [Used with CategoryTable]
- Specify CategoryTable column containing target column names

**CategoriesColumn**
- [Used with CategoryTable]
- Specify CategoryTable column containing category values

**StartValue**
- Specify starting integer value for encoding
- Default: 0
- Can specify different start values for different columns
- Example: StartValue(0, 1, 10) for three target columns

### Input Table Schema

**Dense InputTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | CHAR or VARCHAR (CHARACTER SET LATIN or UNICODE) | Categorical columns to be encoded |

**Sparse InputTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| attribute_column | CHAR or VARCHAR (CHARACTER SET LATIN or UNICODE) | Column containing attribute names |
| value_column | CHAR or VARCHAR (CHARACTER SET LATIN or UNICODE) | Column containing attribute values |

**CategoryTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| ColumnName | CHAR or VARCHAR (CHARACTER SET LATIN or UNICODE) | Column containing target column names |
| CategoryValue | CHAR or VARCHAR (CHARACTER SET LATIN or UNICODE) | Column containing category values in desired order |

### Output Table Schema

**Dense Input Output:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| targetColumn_name | VARCHAR (CHARACTER SET UNICODE) | Name of the target column being encoded |
| <targetColumn>_<category1> | INTEGER | Ordinal value for category1 |
| <targetColumn>_<category2> | INTEGER | Ordinal value for category2 |
| ... | INTEGER | Ordinal values for all categories |
| <targetColumn>_TD_OTHER_CATEGORY | INTEGER | Default value for unknown categories |

**Sparse Input Output:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| attribute_column | VARCHAR (CHARACTER SET UNICODE) | Preserves attribute column name |
| value_column | VARCHAR (CHARACTER SET UNICODE) | Preserves value column name |
| ordinal_value | INTEGER | Ordinal integer mapping for each attribute-value pair |

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

**Example 1: Auto Approach with Dense Input**
```sql
SELECT * FROM TD_OrdinalEncodingFit(
    ON titanic_ordinal_dataset AS INPUTTABLE
    USING
    TargetColumns('Pclass', 'Education')
    IsInputDense('true')
    Approach('Auto')
    StartValue(1, 0)
) AS dt;
```

**Output:**
```
Pclass  Pclass_First  Pclass_Second  Pclass_Third  Pclass_TD_OTHER_CATEGORY  Education  Education_HighSchool  Education_Bachelor  Education_Master  Education_PhD  Education_TD_OTHER_CATEGORY
        1             2              3             -1                                   0                     1                   2                 3              -1
```

**Example 2: List Approach with Explicit Ordering**
```sql
SELECT * FROM TD_OrdinalEncodingFit(
    ON titanic_ordinal_dataset AS INPUTTABLE
    USING
    TargetColumns('Education')
    IsInputDense('true')
    Approach('List')
    CategoricalValues('High School', 'Bachelor', 'Master', 'PhD')
    StartValue(1)
) AS dt;
```

**Output:**
```
Education  Education_HighSchool  Education_Bachelor  Education_Master  Education_PhD  Education_TD_OTHER_CATEGORY
           1                     2                   3                 4              -1
```

**Example 3: Using CategoryTable for Custom Ordering**
```sql
-- Create category table with desired ordering
CREATE TABLE education_categories (
    column_name VARCHAR(20),
    category VARCHAR(30)
);

INSERT INTO education_categories VALUES('Education', 'High School');
INSERT INTO education_categories VALUES('Education', 'Bachelor');
INSERT INTO education_categories VALUES('Education', 'Master');
INSERT INTO education_categories VALUES('Education', 'PhD');

-- Create fit table
SELECT * FROM TD_OrdinalEncodingFit(
    ON titanic_ordinal_dataset AS INPUTTABLE
    ON education_categories AS categoryTable DIMENSION
    USING
    TargetColumns('Education')
    IsInputDense('true')
    Approach('List')
    TargetColumnNames('column_name')
    CategoriesColumn('category')
    StartValue(0)
) AS dt;
```

**Example 4: Multiple Columns with Different Start Values**
```sql
SELECT * FROM TD_OrdinalEncodingFit(
    ON customer_data AS INPUTTABLE
    USING
    TargetColumns('risk_level', 'priority', 'severity')
    IsInputDense('true')
    Approach('List')
    CategoricalValues('Low', 'Medium', 'High', 'Critical')
    StartValue(0, 1, 10)  -- Different start values for each column
) AS dt;
```

**Example 5: Rating Scale Encoding**
```sql
SELECT * FROM TD_OrdinalEncodingFit(
    ON survey_responses AS INPUTTABLE
    USING
    TargetColumns('satisfaction_rating')
    IsInputDense('true')
    Approach('List')
    CategoricalValues('Very Dissatisfied', 'Dissatisfied', 'Neutral', 'Satisfied', 'Very Satisfied')
    StartValue(1)
) AS dt;
```

**Example 6: Size Categories**
```sql
SELECT * FROM TD_OrdinalEncodingFit(
    ON product_inventory AS INPUTTABLE
    USING
    TargetColumns('size')
    IsInputDense('true')
    Approach('List')
    CategoricalValues('XS', 'S', 'M', 'L', 'XL', 'XXL')
    StartValue(0)
) AS dt;
```

**Example 7: Sparse Input Format**
```sql
SELECT * FROM TD_OrdinalEncodingFit(
    ON sparse_categorical AS InputTable PARTITION BY attribute_column
    USING
    IsInputDense('false')
    TargetAttributes('Education', 'Skill_Level')
    AttributeColumn('attribute_column')
    ValueColumn('value_column')
    Approach('Auto')
    StartValue(0)
) AS dt;
```

**Example 8: Job Seniority Levels**
```sql
SELECT * FROM TD_OrdinalEncodingFit(
    ON employee_data AS INPUTTABLE
    USING
    TargetColumns('seniority')
    IsInputDense('true')
    Approach('List')
    CategoricalValues('Junior', 'Mid-Level', 'Senior', 'Lead', 'Principal', 'Executive')
    StartValue(1)
) AS dt;
```

**Example 9: Credit Rating Categories**
```sql
SELECT * FROM TD_OrdinalEncodingFit(
    ON loan_applications AS INPUTTABLE
    USING
    TargetColumns('credit_rating')
    IsInputDense('true')
    Approach('List')
    CategoricalValues('Poor', 'Fair', 'Good', 'Very Good', 'Excellent')
    StartValue(300)  -- Starting at 300 to align with credit score ranges
) AS dt;
```

**Example 10: Complete ML Pipeline Setup**
```sql
-- Create fit table for training data
CREATE TABLE ordinal_fit AS (
    SELECT * FROM TD_OrdinalEncodingFit(
        ON training_data AS INPUTTABLE
        USING
        TargetColumns('education_level', 'experience_level', 'skill_rating')
        IsInputDense('true')
        Approach('List')
        CategoricalValues('High School', 'Bachelor', 'Master', 'PhD')
        StartValue(0, 1, 1)
    ) AS dt
) WITH DATA;

-- This fit table will be used for both training and test data transformation
```

### Ordinal Encoding Concepts

**Natural Ordering:**
Ordinal encoding is appropriate when categories have inherent ordering:
- Education: High School < Bachelor < Master < PhD
- Ratings: 1 star < 2 stars < 3 stars < 4 stars < 5 stars
- Size: XS < S < M < L < XL
- Severity: Mild < Moderate < Severe < Critical

**Mapping Process:**
```
Original: ['Low', 'Medium', 'High', 'Medium', 'Low']
Encoded:  [0,     1,        2,      1,        0]
```

**Advantages:**
- Compact representation (single column)
- Preserves ordering information
- Efficient for tree-based models
- Reduces dimensionality vs one-hot encoding

**Considerations:**
- Assumes equal distances between categories
- Linear models may treat gaps as meaningful
- Not suitable for nominal categories
- Tree-based models handle ordinal features well

### Use Cases and Applications

**1. Machine Learning Preprocessing**
- Encode ordinal features for tree-based models (Random Forest, XGBoost)
- Prepare categorical features with natural ordering
- Reduce feature space compared to one-hot encoding
- Support gradient boosting with ordinal categories

**2. Survey and Rating Analysis**
- Encode Likert scale responses (1-5, 1-7)
- Transform satisfaction ratings
- Map NPS categories (Detractors, Passives, Promoters)
- Encode sentiment levels (Very Negative to Very Positive)

**3. Educational Data Analysis**
- Map education levels to ordinal integers
- Encode grade categories (A, B, C, D, F)
- Transform skill proficiency levels
- Support educational attainment analysis

**4. Risk Assessment**
- Encode risk levels (Low, Medium, High, Critical)
- Map severity categories for incidents
- Transform priority levels
- Support risk-based decision models

**5. E-commerce and Retail**
- Encode product size categories
- Transform customer loyalty tiers (Bronze, Silver, Gold, Platinum)
- Map shipping priority levels
- Support inventory categorization

**6. Healthcare Analytics**
- Encode pain scales (0-10)
- Map disease severity levels
- Transform treatment urgency categories
- Support clinical decision making

**7. Human Resources**
- Encode job seniority levels
- Map performance ratings
- Transform experience categories
- Support career progression analysis

**8. Financial Services**
- Encode credit rating categories
- Map risk tolerance levels
- Transform investment experience levels
- Support credit scoring models

**9. Customer Segmentation**
- Encode customer value tiers
- Map engagement levels (Low, Medium, High)
- Transform lifecycle stages
- Support targeted marketing strategies

**10. Quality Assurance**
- Encode defect severity levels
- Map quality grades
- Transform inspection results
- Support quality control analysis

### Important Notes

**Ordering Specification:**
- LIST approach: Categories encoded in order specified by CategoricalValues
- AUTO approach: Alphabetical or data-driven ordering
- First category receives StartValue, subsequent categories increment by 1
- Use LIST approach when order matters for model performance

**Unknown Category Handling:**
- Categories not in fit table mapped to TD_OTHER_CATEGORY value
- Default value typically -1 (can be customized)
- Important for handling production data drift
- Monitor frequency of unknown categories

**Limitations:**
- Maximum 4000 unique categories per column
- Assumes equal intervals between ordinal levels
- May not be appropriate for nominal data
- Linear models interpret integers as having equal spacing

**StartValue Parameter:**
- Default: 0
- Can specify different start values for different columns
- Useful for aligning with business conventions (e.g., 1-5 ratings)
- Subsequent values increment by 1 from start value

**Multiple Column Support:**
- Can encode multiple columns in single operation
- Each column can have different StartValue
- All columns must use same Approach (AUTO or LIST)
- Categories mapped independently per column

**Dense vs Sparse:**
- Dense format: Traditional table with columns (most common)
- Sparse format: Attribute-value pairs (for very wide data)
- Choose based on data structure and efficiency

**Model Compatibility:**
- Tree-based models: Handle ordinal encoding well
- Linear models: May misinterpret distances between levels
- Neural networks: May benefit from embedding layers instead
- Distance-based algorithms: Consider scaling after encoding

### Best Practices

**1. Verify Natural Ordering**
- Ensure categories truly have ordinal relationship
- Consult domain experts on correct ordering
- Document ordering rationale
- Consider one-hot encoding if order unclear

**2. Consistent Encoding**
- Create fit table on training data only
- Apply to training, validation, and test sets
- Never fit on test data
- Store fit table with model artifacts

**3. Handle Unknown Categories**
- Plan for categories not in training data
- Monitor TD_OTHER_CATEGORY frequency
- Implement alerting for high unknown rates
- Consider retraining when categories drift

**4. StartValue Selection**
- Use meaningful start values aligned with domain
- Consider 0 for neutral starting point
- Use 1 for positive-only scales (1-5 ratings)
- Document start value choices

**5. Validate Transformations**
- Check encoded values match expectations
- Verify ordering preserved correctly
- Test with edge cases and boundary values
- Ensure transform output aligns with fit table

**6. Feature Engineering**
- Consider interactions with other features
- Apply scaling if using with distance-based algorithms
- Monitor for concept drift in categorical distributions
- Combine with other feature engineering techniques

### Related Functions
- **TD_OrdinalEncodingTransform** - Applies ordinal encoding using fit output (must be used after TD_OrdinalEncodingFit)
- **TD_OneHotEncodingFit** - Alternative for nominal categorical data
- **TD_TargetEncodingFit** - Alternative using target variable statistics
- **TD_ScaleFit** - Often used after ordinal encoding for normalization

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Transform Functions
