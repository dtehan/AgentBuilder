# TD_DecisionForest

### Function Name
**TD_DecisionForest**

### Description
TD_DecisionForest is an ensemble machine learning algorithm that creates predictive models for classification and regression problems using bootstrap aggregation (bagging) of decision trees. This powerful supervised learning function builds multiple decision trees in parallel across Teradata AMPs and combines their predictions to improve accuracy, reduce overfitting, and enhance model generalization compared to single decision trees. The algorithm constructs each tree using a random subset of training data and features, forcing diversity among trees to improve overall prediction quality.

The decision forest algorithm works by iteratively evaluating input variables at each node to determine optimal split points, growing trees until stopping criteria are met (maximum depth, minimum node size, or minimum impurity). Each node represents a decision based on a single variable's value, and the tree recursively partitions data into smaller subsets. For classification, the forest predicts outcomes via majority voting among trees; for regression, it averages predictions across trees. The function automatically adjusts the number of trees based on data distribution across AMPs and coverage requirements, ensuring efficient parallel processing while maintaining model quality.

TD_DecisionForest supports both continuous and categorical input variables (after numeric conversion), handles multi-class classification (up to 500 classes), and provides extensive hyperparameter tuning capabilities including tree depth control, node size limits, feature sampling (Mtry), and coverage factors. The function outputs a JSON representation of each decision tree along with tree metadata, enabling model interpretability and deployment via TD_DecisionForestPredict. By leveraging Teradata's parallel architecture, decision forests scale efficiently to large datasets while providing robust predictions resistant to noise and outliers.

### When the Function Would Be Used
- **Classification Tasks**: Predict categorical outcomes from labeled training data
- **Regression Analysis**: Predict continuous target values using ensemble methods
- **Multi-Class Problems**: Handle classification problems with up to 500 distinct classes
- **Reduce Overfitting**: Improve generalization through ensemble averaging
- **Handle Non-Linear Relationships**: Capture complex interactions between features
- **Variable Importance Analysis**: Identify influential predictors for outcomes
- **Robust to Outliers**: Build models resistant to noisy or anomalous data
- **Feature Engineering**: Automatically discover feature interactions
- **Imbalanced Data**: Handle datasets with uneven class distributions
- **High-Dimensional Data**: Process datasets with many input variables
- **Interpretable Models**: Generate decision rules via JSON tree structure
- **Parallel Training**: Leverage distributed processing for large datasets
- **Missing Value Tolerance**: Skip observations with missing values during training
- **Customer Churn Prediction**: Identify customers likely to leave
- **Credit Risk Assessment**: Evaluate loan default probability
- **Fraud Detection**: Classify transactions as fraudulent or legitimate
- **Medical Diagnosis**: Predict disease presence from patient symptoms
- **Product Recommendation**: Classify user preferences for personalization
- **Predictive Maintenance**: Forecast equipment failures
- **Demand Forecasting**: Predict future sales or resource needs

### Syntax

```sql
TD_DecisionForest (
    ON { table | view | (query) } AS InputTable PARTITION BY ANY
    USING
    InputColumns ({'input_column'|input_column_range }[,...])
    ResponseColumn('response_column')
    [ MaxDepth (maxdepth) ]
    [ MinNodeSize (minnodesize) ]
    [ NumTrees (numtrees) ]
    [ ModelType ('classification'|'regression') ]
    [ TreeSize (treesize) ]
    [ CoverageFactor (coveragefactor) ]
    [ Seed (seed) ]
    [ Mtry (mtry) ]
    [ MtrySeed (mtryseed) ]
    [ MinImpurity (minimpurity) ]
)
```

### Required Syntax Elements for TD_DecisionForest

**ON clause (InputTable)**
- Accepts table, view, or query containing training data
- Must use PARTITION BY ANY for distributed tree building
- Each AMP builds trees using its data partition

**InputColumns**
- Specify input table column names for training (features, predictors, independent variables)
- All columns must be numeric data types
- Convert categorical columns to numeric values as preprocessing step
- Supports column range notation (e.g., '[2:12]')

**ResponseColumn**
- Specify column name containing classification labels or regression target values
- For classification: Must be INTEGER, SMALLINT, or BYTEINT (supports up to 500 classes)
- For regression: Supports all numeric types (FLOAT, DECIMAL, NUMBER, etc.)

### Optional Syntax Elements for TD_DecisionForest

**MaxDepth**
- Specify maximum depth of each tree in the forest
- Controls tree complexity and prevents overfitting
- Trees can grow to 2^(max_depth+1)-1 nodes
- Must be non-negative integer
- Default: 5

**MinNodeSize**
- Specify minimum number of observations required in a tree node
- Algorithm stops splitting nodes with observations ≤ this value
- Larger values create simpler trees and faster training
- Must be non-negative integer
- Default: 1

**NumTrees**
- Specify number of trees to build in the forest
- Must be greater than or equal to number of data AMPs
- Function adjusts: Number_of_trees = Num_AMPs_with_data * (NumTrees/Num_AMPs_with_data)
- More trees improve accuracy but increase processing time and complexity
- Maximum supported: 65,536 trees
- Default: -1 (function calculates based on CoverageFactor)

**ModelType**
- Specify analysis type: 'regression' or 'classification'
- Regression: Continuous response variable, minimizes variance in splits
- Classification: Discrete class labels, maximizes information gain in splits
- For classification, function only generates trees when AMP has multiple classes
- Default: 'regression'

**TreeSize**
- Specify number of rows each tree uses as input dataset
- Function uses minimum of: rows on AMP, rows fitting in memory, or TreeSize value
- Determines sample size for building each tree
- Function reserves ~40% available memory for input sample, rest for tree building
- Default: -1 (function computes internally based on available memory)

**CoverageFactor**
- Specify dataset coverage level in the forest (percentage)
- Controls how many trees are built: Number_of_AMP_trees = CoverageFactor * Num_Rows_AMP / TreeSize
- Value of 1.0 = 100% coverage, 2.0 = 200% coverage (doubles number of trees)
- Higher values increase processing time proportionally
- Default: 1.0

**Seed**
- Specify random seed for repeatable results
- Controls random sampling of data for each tree
- Use for reproducible model training
- Default: 1

**Mtry**
- Specify number of features to evaluate for best split at each node
- Higher values improve splitting quality but reduce forest robustness
- Lower values improve robustness and prevent overfitting
- Value of -1 uses all variables for each split
- Typical recommendation: sqrt(num_features) for classification, num_features/3 for regression
- Default: -1

**MtrySeed**
- Specify random seed for Mtry feature selection
- Controls which features are randomly selected at each split
- Use for reproducible feature sampling
- Default: 1

**MinImpurity**
- Specify minimum impurity threshold for node splitting
- Algorithm stops splitting nodes with impurity ≤ this value
- For classification: Gini impurity (0 = pure node, 0.5 = maximum impurity)
- For regression: Variance reduction
- Default: 0.0

### Input Table Schema

**InputTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| input_column | INTEGER, BIGINT, SMALLINT, BYTEINT, FLOAT, DECIMAL, NUMBER | Numeric columns used to train the DecisionForest model (predictors, features) |
| response_column | INTEGER, SMALLINT, BYTEINT (classification)<br>All numeric types (regression) | Column containing response value: class label for classification or continuous target for regression |

**Important Notes:**
- All input variables must be numeric (convert categorical columns as preprocessing)
- Function skips observations with missing values in any input column
- Use TD_SimpleImpute to assign missing values before training

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| task_index | SMALLINT | The AMP that produced the decision tree |
| tree_num | SMALLINT | The identified decision tree number within an AMP |
| regression_tree or classification_tree | VARCHAR | JSON representation of decision tree (truncated to 32000 bytes if larger, displayed across multiple rows with tree_order id) |

**JSON Decision Tree Elements:**

| JSON Element | Description |
|--------------|-------------|
| id_ | Unique identifier of the node |
| sum_ | [Regression] Sum of response variable values in the node |
| sumSq_ | [Regression] Sum of squared values of response variable in the node |
| responseCounts_ | [Classification] Number of observations in each class |
| size_ | Total number of observations in the node |
| maxDepth_ | Maximum possible depth from current node (max_depth for root, 0 for leaf) |
| split_ | JSON item describing split in the node |
| score_ | GINI score (classification) or variance reduction (regression) |
| attr_ | Attribute (feature) on which node is split |
| type_ | Split type: CLASSIFICATION_NUMERIC_SPLIT or REGRESSION_NUMERIC_SPLIT |
| leftNodeSize_ | Number of observations assigned to left child |
| rightNodeSize_ | Number of observations assigned to right child |
| leftChild_ | JSON item describing left child node |
| rightChild_ | JSON item describing right child node |
| nodeType_ | Node type: CLASSIFICATION_NODE, CLASSIFICATION_LEAF, REGRESSION_NODE, REGRESSION_LEAF |

### Code Examples

**Input Data: titanic_passengers**
```
passenger_id  pclass  fare         age  survived
1             3       7.25000000   22   0
2             1       71.28330000  38   1
3             3       7.92500000   26   1
4             1       53.10000000  35   1
5             3       8.05000000   35   0
```

**Example 1: Basic Classification Model**
```sql
-- Train decision forest for binary classification (survived prediction)
CREATE VOLATILE TABLE titanic_forest_model AS (
    SELECT * FROM TD_DecisionForest (
        ON titanic_train AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('survived')
        InputColumns('pclass', 'fare', 'age', 'sibsp', 'parch')
        ModelType('classification')
        NumTrees(10)
        MaxDepth(5)
        Seed(42)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Output: Forest model with 10 trees, JSON representation of each tree
-- Can be used with TD_DecisionForestPredict for predictions
```

**Example 2: Regression Model for Price Prediction**
```sql
-- Train decision forest to predict housing prices
CREATE VOLATILE TABLE housing_forest_model AS (
    SELECT * FROM TD_DecisionForest (
        ON housing_train AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('price')
        InputColumns('lotsize', 'bedrooms', 'bathrms', 'stories', 'garagepl')
        ModelType('regression')
        NumTrees(20)
        MaxDepth(8)
        MinNodeSize(5)
        Seed(123)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Output: Regression forest with 20 trees
-- Each tree predicts continuous price values
```

**Example 3: Multi-Class Classification**
```sql
-- Classify iris species (3 classes: setosa, versicolor, virginica)
CREATE VOLATILE TABLE iris_forest_model AS (
    SELECT * FROM TD_DecisionForest (
        ON iris_train AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('species_encoded')  -- 0, 1, 2 for three species
        InputColumns('sepal_length', 'sepal_width', 'petal_length', 'petal_width')
        ModelType('classification')
        NumTrees(15)
        MaxDepth(4)
        Mtry(2)  -- Use 2 features at each split
        Seed(456)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Output: Multi-class classifier supporting 3 species categories
```

**Example 4: Feature Sampling with Mtry**
```sql
-- Train forest with controlled feature sampling for robustness
CREATE VOLATILE TABLE credit_forest_model AS (
    SELECT * FROM TD_DecisionForest (
        ON credit_train AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('default')
        InputColumns('[1:20]')  -- 20 credit-related features
        ModelType('classification')
        NumTrees(50)
        MaxDepth(10)
        Mtry(5)  -- Evaluate 5 random features at each split
        MtrySeed(789)
        Seed(101)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Mtry=5 ensures diversity among trees by limiting feature choices
-- Improves forest robustness and reduces overfitting
```

**Example 5: Control Tree Complexity**
```sql
-- Train simpler trees to prevent overfitting
CREATE VOLATILE TABLE churn_forest_model AS (
    SELECT * FROM TD_DecisionForest (
        ON customer_train AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('churned')
        InputColumns('tenure', 'monthly_charges', 'total_charges',
                     'num_services', 'support_calls')
        ModelType('classification')
        NumTrees(25)
        MaxDepth(4)        -- Shallow trees
        MinNodeSize(10)    -- Require 10+ samples per leaf
        MinImpurity(0.01)  -- Stop splitting nearly-pure nodes
        Seed(202)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Shallow trees with larger leaves reduce overfitting
-- Good for smaller datasets or high noise
```

**Example 6: Adjust Coverage Factor**
```sql
-- Build more trees by increasing coverage
CREATE VOLATILE TABLE fraud_forest_model AS (
    SELECT * FROM TD_DecisionForest (
        ON transactions_train AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('is_fraud')
        InputColumns('amount', 'merchant_category', 'time_of_day',
                     'location_risk', 'card_age_days')
        ModelType('classification')
        CoverageFactor(2.0)  -- Build 2x more trees (200% coverage)
        MaxDepth(8)
        TreeSize(1000)       -- Each tree uses 1000 samples
        Seed(303)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- CoverageFactor=2.0 doubles number of trees
-- Improves accuracy but increases training time proportionally
```

**Example 7: Column Range Notation**
```sql
-- Use column ranges for many predictors
CREATE VOLATILE TABLE diagnosis_forest_model AS (
    SELECT * FROM TD_DecisionForest (
        ON patient_train AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('diagnosis')
        InputColumns('[3:50]')  -- Columns 3 through 50 (48 features)
        ModelType('classification')
        NumTrees(30)
        MaxDepth(6)
        Mtry(7)  -- sqrt(48) ≈ 7 features per split
        Seed(404)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Column range notation simplifies syntax for many features
```

**Example 8: Examining Tree Structure (Query Model)**
```sql
-- View decision trees from trained model
SELECT
    task_index,
    tree_num,
    SUBSTR(regression_tree, 1, 500) AS tree_preview
FROM housing_forest_model
WHERE regression_tree IS NOT NULL
ORDER BY task_index, tree_num;

-- Output shows JSON tree structure:
-- {"id_":1,"sum_":208.8,"sumSq_":4905.98,"size_":9,"maxDepth_":12,...}
-- Reveals tree splits, node sizes, and decision rules
```

**Example 9: Small Dataset Strategy**
```sql
-- For small datasets, distribute to single AMP with primary index
CREATE TABLE small_train (
    id INTEGER,
    feature1 FLOAT,
    feature2 FLOAT,
    target INTEGER,
    PRIMARY INDEX (id)
) WITH DATA;

-- Insert data with same id value for all rows to force single AMP
INSERT INTO small_train SELECT 1, feature1, feature2, target FROM source_data;

-- Train forest on single AMP
CREATE VOLATILE TABLE small_forest_model AS (
    SELECT * FROM TD_DecisionForest (
        ON small_train AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('target')
        InputColumns('feature1', 'feature2')
        ModelType('classification')
        NumTrees(10)
        Seed(505)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Ensures consistent training when dataset is very small
```

**Example 10: Complete Workflow (Train + Predict + Evaluate)**
```sql
-- Step 1: Train decision forest model
CREATE VOLATILE TABLE customer_churn_model AS (
    SELECT * FROM TD_DecisionForest (
        ON customer_train AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('churn')
        InputColumns('tenure', 'monthly_charges', 'contract_type_encoded',
                     'payment_method_encoded', 'internet_service_encoded')
        ModelType('classification')
        NumTrees(50)
        MaxDepth(8)
        MinNodeSize(5)
        Mtry(3)
        Seed(606)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 2: Make predictions on test set
CREATE VOLATILE TABLE churn_predictions AS (
    SELECT * FROM TD_DecisionForestPredict (
        ON customer_test AS InputTable PARTITION BY ANY
        ON customer_churn_model AS ModelTable DIMENSION
        USING
        IDColumn('customer_id')
        Accumulate('churn')  -- Actual label for evaluation
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 3: Evaluate model performance
SELECT * FROM TD_ClassificationEvaluator (
    ON churn_predictions AS InputTable PARTITION BY ANY
    USING
    ObservationColumn('churn')
    PredictionColumn('prediction')
    NumClasses(2)
) AS dt;

-- Output: Accuracy, Precision, Recall, F1-Score, Confusion Matrix
```

### Decision Forest Algorithm Details

**Tree Building Process:**
1. Select k initial cluster centroids (random or via KMeans++)
2. For each AMP with data partition:
   - Sample rows for tree (controlled by TreeSize or CoverageFactor)
   - For each node in tree:
     - Randomly select Mtry features to consider
     - Evaluate split quality for each feature
     - Choose feature and threshold with best score (Gini or variance reduction)
     - Split node into left (< threshold) and right (≥ threshold) children
     - Repeat until stopping criteria met (MaxDepth, MinNodeSize, MinImpurity)
3. Output trees in JSON format with metadata

**Splitting Criteria:**

**For Classification (Gini Impurity):**
- Gini = 1 - Σ(p_i²) where p_i is proportion of class i in node
- Lower Gini = purer node (better)
- Algorithm selects split minimizing weighted average child Gini

**For Regression (Variance Reduction):**
- For each split, calculate variance of each child node
- Select split minimizing weighted average child variance
- Variance = Σ((x_i - mean)²) / n

**Prediction Aggregation:**
- **Classification**: Majority vote among all trees
- **Regression**: Average of predictions from all trees

### Use Cases and Applications

**1. Customer Analytics**
- Churn prediction and retention modeling
- Customer lifetime value estimation
- Segmentation and targeting
- Cross-sell and upsell recommendations

**2. Financial Services**
- Credit scoring and loan default prediction
- Fraud detection for transactions
- Risk assessment and portfolio optimization
- Anti-money laundering (AML) detection

**3. Healthcare and Medicine**
- Disease diagnosis from symptoms and test results
- Patient readmission prediction
- Treatment outcome forecasting
- Drug response prediction

**4. E-Commerce and Retail**
- Product recommendation systems
- Demand forecasting for inventory
- Price optimization
- Customer sentiment classification

**5. Marketing and Advertising**
- Campaign response prediction
- Ad click-through rate (CTR) estimation
- Customer acquisition cost optimization
- Market basket analysis

**6. Manufacturing and Operations**
- Predictive maintenance for equipment
- Quality control and defect detection
- Supply chain optimization
- Production yield forecasting

**7. Telecommunications**
- Network failure prediction
- Customer service call routing
- Usage pattern classification
- Churn prevention strategies

**8. Insurance**
- Claims prediction and fraud detection
- Policyholder risk assessment
- Premium pricing optimization
- Loss ratio forecasting

**9. Human Resources**
- Employee attrition prediction
- Candidate screening and selection
- Performance rating prediction
- Training effectiveness evaluation

**10. Energy and Utilities**
- Energy consumption forecasting
- Equipment failure prediction
- Load balancing optimization
- Renewable energy production estimation

### Important Notes

**Data Preprocessing Requirements:**
- **Categorical Conversion**: All input columns must be numeric. Use TD_OneHotEncoding, TD_OrdinalEncoding, or TD_TargetEncoding for categorical features
- **Missing Value Handling**: Function automatically skips rows with NULL values in any input column. Use TD_SimpleImpute to fill missing values if needed
- **Feature Scaling**: Not required (trees are scale-invariant), but may improve interpretability

**Performance Considerations:**
- **Parallel Processing**: Trees built in parallel across AMPs with non-empty partitions
- **Tree Count Calculation**: Number_of_trees = Num_AMPs_with_data * (NumTrees / Num_AMPs_with_data)
- **Memory Usage**: Function reserves ~40% memory for input sample, rest for tree construction
- **Processing Time**: Doubling CoverageFactor doubles training time
- **TreeSize Impact**: Larger TreeSize increases memory usage but may improve tree quality

**Model Complexity Control:**
- **MaxDepth**: Primary control for overfitting (deeper = more complex)
- **MinNodeSize**: Prevents very small leaves (larger = simpler trees)
- **MinImpurity**: Stops splitting nearly-pure nodes
- **Mtry**: Controls feature diversity (lower = more robust forest)

**Classification-Specific Notes:**
- Supports binary and multi-class classification (up to 500 classes)
- Response values must be INTEGER, SMALLINT, or BYTEINT
- Function only builds trees on AMPs with multiple classes present
- Class imbalance may affect accuracy (consider class weighting in prediction)

**Regression-Specific Notes:**
- Supports all numeric response types
- Uses variance reduction for split selection
- Output trees predict continuous values
- Predictions are averages across all trees

**Deterministic Results:**
- Use Seed parameter for reproducible random sampling
- Use MtrySeed for reproducible feature selection
- Results vary across machine configurations without InitialCentroidsTable
- Use GET HASHAMP()+1 to determine Num_AMPs_with_data

**Small Dataset Handling:**
- For small datasets, distribute to single AMP using primary index with constant value
- Ensures all data available for tree construction
- Prevents data skew issues

**Maximum Limits:**
- Maximum 65,536 trees supported
- Maximum 500 classes for classification
- JSON output truncated at 32,000 bytes (spans multiple rows if larger)

### Best Practices

**1. Tune Number of Trees**
- Start with 10-50 trees and increase if accuracy improves
- More trees improve stability but increase training time
- Monitor diminishing returns (plot accuracy vs. num_trees)
- Consider computational budget when setting NumTrees

**2. Control Tree Depth**
- Start with MaxDepth=5-10 for most problems
- Deeper trees (15-20) for complex relationships
- Shallower trees (3-5) to prevent overfitting on small data
- Balance bias (shallow) vs. variance (deep)

**3. Use Feature Sampling (Mtry)**
- Classification: Mtry = sqrt(num_features)
- Regression: Mtry = num_features / 3
- Lower Mtry for more diverse, robust forests
- Higher Mtry for better individual tree performance

**4. Set Minimum Node Size**
- MinNodeSize=1 for large datasets (allows finest splits)
- MinNodeSize=5-10 for smaller datasets (prevents overfitting)
- MinNodeSize=20+ for very noisy data
- Larger values speed up training

**5. Handle Missing Values**
- Use TD_SimpleImpute before training
- Choose imputation strategy based on data (mean, median, mode)
- Consider creating "missing value indicator" features
- Document imputation choices for reproducibility

**6. Convert Categorical Variables**
- Use TD_OneHotEncoding for nominal categories
- Use TD_OrdinalEncoding for ordinal categories
- Use TD_TargetEncoding for high-cardinality categories
- Avoid label encoding unless natural ordering exists

**7. Split Training and Test Sets**
- Reserve 20-30% of data for testing
- Use TD_FillRowID with ORDER BY RANDOM() for random splits
- Ensure class balance in both train and test sets
- Use cross-validation for small datasets

**8. Monitor Training Progress**
- Check JSON output for tree structure and splits
- Verify trees are being built on all AMPs (task_index values)
- Inspect node sizes and depths
- Ensure trees are diverse (different splits)

**9. Evaluate Model Performance**
- Use TD_ClassificationEvaluator for classification metrics
- Use TD_RegressionEvaluator for regression metrics
- Examine confusion matrix for misclassification patterns
- Consider business costs when setting decision thresholds

**10. Iterate and Refine**
- Start with default parameters and establish baseline
- Tune one hyperparameter at a time
- Use grid search or random search for optimization
- Document parameter choices and performance
- Retrain periodically with fresh data

### Related Functions
- **TD_DecisionForestPredict** - Make predictions using trained forest model
- **TD_SimpleImpute** - Fill missing values before training
- **TD_OneHotEncoding** - Convert categorical variables to numeric
- **TD_OrdinalEncoding** - Encode ordinal categorical variables
- **TD_TargetEncoding** - Encode high-cardinality categories
- **TD_ClassificationEvaluator** - Evaluate classification model performance
- **TD_RegressionEvaluator** - Evaluate regression model performance
- **TD_XGBoost** - Alternative gradient boosting algorithm
- **TD_GLM** - Generalized linear models for regression/classification
- **TD_SVM** - Support vector machines for classification/regression

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Model Training Functions
