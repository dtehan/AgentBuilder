# TD_KNN

### Function Name
**TD_KNN** (K-Nearest Neighbors)

### Description
TD_KNN is a supervised learning algorithm that predicts outcomes for test data by computing similarity to training data based on distance metrics, implementing a non-parametric, instance-based approach where predictions are made directly from training examples without constructing an explicit model. The algorithm operates by calculating the distance between a test point and all training points, selecting the K closest neighbors, and making predictions based on majority voting (classification) or averaging (regression) of these neighbors. This lazy learning technique defers computation until prediction time, making it conceptually simple but computationally intensive, with O(N²) complexity that scales with both training and test dataset sizes.

K-Nearest Neighbors uses distance metrics—primarily Euclidean or Manhattan distance—to quantify similarity between data points in multi-dimensional feature space, where smaller distances indicate greater similarity. During prediction, KNN calculates distances from each test observation to every training observation, sorts by distance, selects the K nearest neighbors, and aggregates their outcomes: for classification via majority vote among neighbor labels, for regression via mean of neighbor values, or for neighbors mode by returning the nearest neighbor identities. The choice of K is critical—small K values capture local patterns but are sensitive to noise, while large K values provide smoother boundaries but may miss local structure. TD_KNN supports weighted voting where closer neighbors contribute more to predictions based on inverse distance weighting.

The function operates in three model types: classification (categorical prediction with probability outputs), regression (continuous value prediction), and neighbors (returning nearest neighbor identities for similarity search or recommendation). TD_KNN supports up to 2018 features and 1000 class labels for classification, with the training table provided as a DIMENSION input (copied to each AMP's spool), limiting scalability for very large training sets. The algorithm is scale-sensitive, requiring feature standardization for optimal performance, and is computationally expensive as query runtime increases significantly with larger training or test datasets. Alternative algorithms like decision trees, random forests, or neural networks may be more appropriate for large-scale problems, but KNN excels for small to medium datasets requiring simple, interpretable, non-parametric modeling.

### When the Function Would Be Used
- **Classification Tasks**: Predict categorical outcomes based on similar training examples
- **Regression Analysis**: Estimate continuous values from neighbor averages
- **Recommendation Systems**: Find similar users or items for collaborative filtering
- **Pattern Recognition**: Identify objects or patterns based on similarity
- **Anomaly Detection**: Detect outliers as points with distant neighbors
- **Image Recognition**: Classify images based on pixel similarity
- **Handwriting Recognition**: Identify characters from training examples
- **Medical Diagnosis**: Classify diseases based on similar patient profiles
- **Credit Scoring**: Assess credit risk from similar historical applicants
- **Customer Segmentation**: Group customers by behavioral similarity
- **Fraud Detection**: Identify fraudulent transactions via pattern matching
- **Text Classification**: Categorize documents by content similarity
- **Species Classification**: Identify organisms from characteristic measurements
- **Quality Control**: Detect defective products based on similar examples
- **Real Estate Valuation**: Predict property prices from comparable sales
- **Sentiment Analysis**: Classify text sentiment from similar examples
- **Collaborative Filtering**: Recommend products based on user similarity
- **Nearest Neighbor Search**: Find most similar data points for analysis
- **Imputation**: Fill missing values using similar observations
- **Prototype Selection**: Identify representative examples from datasets

### Syntax

```sql
TD_KNN(
    ON { table | view | (query) } AS TestTable PARTITION BY ANY
    ON { table | view | (query) } AS TrainingTable DIMENSION
    USING
    IDColumn('id_col_name')
    InputColumns({'target_column'| target_column_range}[...])
    [ ModelType('classification'|'regression'|'neighbors') ]
    [ K(k) ]
    [ Accumulate({'accumulate_column'|accumulate_column_range}[,...]) ]
    [ ResponseColumn(['response_column']) ]
    [ VotingWeight(voting_weight) ]
    [ Tolerance(tolerance) ]
    [ OutputProb('true'|'false'|'t'|'yes'|'y'|'1'|'f'|'no'|'n'|'0') ]
    [ Responses('response_list') ]
    [ EmitNeighbors('true'|'false'|'t'|'yes'|'y'|'1'|'f'|'no'|'n'|'0') ]
    [ EmitDistances('true'|'false'|'t'|'yes'|'y'|'1'|'f'|'no'|'n'|'0') ]
)
```

### Required Syntax Elements for TD_KNN

**ON clause (TestTable and TrainingTable)**
- TestTable: Contains observations to predict, uses PARTITION BY ANY
- TrainingTable: Contains labeled training data, uses DIMENSION clause
- **CRITICAL**: TrainingTable is DIMENSION input, copied to spool on each AMP (scalability limited by spool space)
- Both tables are required

**IDColumn**
- Specify column name that uniquely identifies data objects in both training and test tables
- Each entry must be unique (function reports error otherwise)
- Used to track predictions and neighbor relationships

**InputColumns**
- Specify training table column names used to compute distance between test and training objects
- Test table must have matching column names with same data types
- All columns must be numeric
- Maximum 2018 features supported

### Optional Syntax Elements for TD_KNN

**ModelType**
- Specify model type for KNN predictions
- 'classification': Predict categorical outcome via majority vote
- 'regression': Predict continuous outcome via neighbor average
- 'neighbors': Return K nearest neighbor identities (similarity search)
- Default: 'classification'

**K**
- Specify number of nearest neighbors to use in algorithm
- Must be positive integer > 0 and ≤ 100
- Small K: sensitive to noise, captures local patterns
- Large K: smoother predictions, less sensitive to outliers
- Default: 5

**Accumulate**
- Specify test table column names to copy to output table
- Useful for preserving identifiers, metadata, or actual labels
- Supports column range notation

**ResponseColumn** [Classification or Regression only]
- Specify training table column containing response values
- Classification: numeric class labels (converted to integers)
- Regression: numeric target values
- Invalid for neighbors model type
- Class labels must be numeric (maximum 1000 classes)

**VotingWeight** [Classification or Regression only]
- Specify voting weight as function of distance
- Weighted score: w = 1 / POWER(distance, voting_weight)
- voting_weight=0: equal weights (standard KNN)
- voting_weight>0: closer neighbors weighted more heavily
- Must be non-negative real number
- Default: 0

**Tolerance**
- Specify tolerance for defining smallest distance (prevents division by zero)
- For distance < tolerance, weight calculated as: w = 1 / POWER(tolerance, voting_weight)
- Only relevant when VotingWeight > 0
- Must be positive float
- Default: 0.0000001

**OutputProb** [Classification only]
- Specify whether to return class probabilities
- 'true': Returns probability for classes specified in Responses argument
- If Responses not specified: returns probability of predicted class only
- 'false': No probability output
- Invalid for regression or neighbors model types
- Default: False

**Responses** [Classification only, requires OutputProb=true]
- Specify class labels for which to return probabilities
- Class labels transformed to integer values
- Maximum 1000 classes
- Format: comma-separated list '0', '1', '2', etc.

**EmitNeighbors** [Classification or Regression]
- Specify whether to display neighbor identities in output
- 'true': Output includes neighbor_idK columns for each of K neighbors
- Default: true for neighbors model type (cannot be false)
- Default: false for classification or regression model types

**EmitDistances**
- Specify whether to display neighbor distances in output
- 'true': Output includes neighbor_distK columns showing Euclidean distances
- 'false': No distance information
- Default: False

### Input Table Schema

**TrainingTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| IDColumn | BYTEINT, SMALLINT, INTEGER, BIGINT | Unique identifier for training observations |
| InputColumns | NUMERIC | Columns used to compute distance between test and training points (must match TestTable columns) |
| ResponseColumn | NUMERIC (regression)<br>INTEGER (classification) | Response value for prediction (target variable for training) |

**TestTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| IDColumn | BYTEINT, SMALLINT, INTEGER, BIGINT | Unique identifier for test observations to predict |
| InputColumns | NUMERIC | Columns used to compute distance (must match TrainingTable columns in name and data type) |

**Important Notes:**
- InputColumns must have matching names and data types between TrainingTable and TestTable
- All InputColumns must be numeric
- TrainingTable is DIMENSION input (entire table copied to each AMP spool before processing)
- Maximum 2018 features (InputColumns) supported
- Maximum 1000 classes for classification

### Output Table Schema

**Output Schema (All Model Types):**

| Column | Data Type | Description |
|--------|-----------|-------------|
| id_column | Same as TestTable IDColumn | Unique identifier from test table |
| prediction | Same as ResponseColumn | [Classification/Regression] Predicted response value |
| prob | Double Precision | [Classification, OutputProb=true] Probability of predicted class |
| prob_k | Double Precision | [Classification, Responses specified] Probability of kth response |
| neighbor_idK | Same as TrainingTable IDColumn | [EmitNeighbors=true] ID of Kth nearest neighbor |
| neighbor_distK | Double Precision | [EmitDistances=true] Euclidean distance to Kth neighbor |
| accumulate_column | Same as TestTable | Accumulated columns specified in Accumulate argument |

**Key Notes:**
- K neighbors numbered as neighbor_id1, neighbor_id2, ..., neighbor_idK
- K distances numbered as neighbor_dist1, neighbor_dist2, ..., neighbor_distK
- For neighbors model type, only neighbor IDs and distances are returned (no prediction)

### Code Examples

**Input Data: person_train (Height, Age, Weight)**
```
id  height  age  weight
0   5.0     32   67
1   5.11    45   98
2   5.9     46   78
3   4.8     35   86
4   5.8     22   70
```

**Example 1: KNN Regression (Predict Weight)**
```sql
-- Predict weight based on height and age using 2 nearest neighbors
SELECT * FROM TD_KNN (
    ON person_test AS TestTable PARTITION BY ANY
    ON person_train AS TrainingTable DIMENSION
    USING
    K(2)
    ResponseColumn('weight')
    InputColumns('height', 'age')
    IDColumn('id')
    ModelType('regression')
    EmitNeighbors('true')
    EmitDistances('true')
) AS dt;

-- Output: predicted weight = average of 2 nearest neighbors' weights
-- Shows which training examples influenced prediction
```

**Example 2: KNN Classification with Probabilities**
```sql
-- Classify iris species with probability outputs
SELECT * FROM TD_KNN (
    ON iris_test AS TestTable PARTITION BY ANY
    ON iris_train AS TrainingTable DIMENSION
    USING
    K(3)
    ResponseColumn('species')
    InputColumns('sepal_length', 'sepal_width', 'petal_length', 'petal_width')
    IDColumn('id')
    ModelType('classification')
    OutputProb('true')
    Responses('0', '1', '2')  -- 3 species classes
    Accumulate('actual_species')
) AS dt;

-- Output: predicted species, prob_0, prob_1, prob_2
-- Probabilities show confidence in prediction
```

**Example 3: Find K Nearest Neighbors**
```sql
-- Find 5 most similar products for recommendation
SELECT * FROM TD_KNN (
    ON product_query AS TestTable PARTITION BY ANY
    ON product_catalog AS TrainingTable DIMENSION
    USING
    K(5)
    InputColumns('price', 'rating', 'category_encoded', 'popularity')
    IDColumn('product_id')
    ModelType('neighbors')
) AS dt;

-- Output: 5 nearest neighbor product IDs for each query product
-- Use for "customers also viewed" recommendations
```

**Example 4: Weighted KNN (Distance-Based Voting)**
```sql
-- Classify with inverse distance weighting
SELECT * FROM TD_KNN (
    ON customer_test AS TestTable PARTITION BY ANY
    ON customer_train AS TrainingTable DIMENSION
    USING
    K(10)
    ResponseColumn('churn')
    InputColumns('tenure', 'monthly_charges', 'total_purchases', 'support_calls')
    IDColumn('customer_id')
    ModelType('classification')
    VotingWeight(2.0)  -- w = 1/distance²
    Tolerance(0.001)
    Accumulate('actual_churn')
) AS dt;

-- Closer neighbors have quadratically more influence
-- Reduces impact of distant K neighbors
```

**Example 5: Anomaly Detection via KNN**
```sql
-- Identify outliers based on neighbor distances
SELECT * FROM TD_KNN (
    ON transactions AS TestTable PARTITION BY ANY
    ON normal_transactions AS TrainingTable DIMENSION
    USING
    K(5)
    InputColumns('amount', 'time_of_day', 'merchant_risk', 'location_distance')
    IDColumn('transaction_id')
    ModelType('neighbors')
    EmitDistances('true')
    Accumulate('amount', 'merchant')
) AS dt;

-- Transactions with large neighbor_dist1 = potential anomalies
-- Flag transactions where distance to nearest neighbor > threshold
```

**Example 6: Multi-Class Classification**
```sql
-- Classify handwritten digits (0-9)
SELECT * FROM TD_KNN (
    ON digit_test AS TestTable PARTITION BY ANY
    ON digit_train AS TrainingTable DIMENSION
    USING
    K(7)
    ResponseColumn('digit_label')
    InputColumns('[1:784]')  -- 28x28 pixel features
    IDColumn('image_id')
    ModelType('classification')
    EmitNeighbors('false')
    Accumulate('actual_digit')
) AS dt;

-- Predict digit label via majority vote of 7 nearest training images
-- Classic KNN application for image classification
```

**Example 7: Compare Multiple K Values**
```sql
-- Test K=1, K=5, K=10 to find optimal K
-- K=1
CREATE VOLATILE TABLE knn_k1 AS (
    SELECT * FROM TD_KNN (
        ON test_data AS TestTable PARTITION BY ANY
        ON train_data AS TrainingTable DIMENSION
        USING
        K(1)
        ResponseColumn('outcome')
        InputColumns('[1:10]')
        IDColumn('id')
        ModelType('classification')
        Accumulate('actual_outcome')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- K=5
CREATE VOLATILE TABLE knn_k5 AS (
    SELECT * FROM TD_KNN (
        ON test_data AS TestTable PARTITION BY ANY
        ON train_data AS TrainingTable DIMENSION
        USING
        K(5)
        ResponseColumn('outcome')
        InputColumns('[1:10]')
        IDColumn('id')
        ModelType('classification')
        Accumulate('actual_outcome')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Evaluate accuracy for each K
SELECT 1 AS k, SUM(CASE WHEN prediction = actual_outcome THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS accuracy
FROM knn_k1
UNION ALL
SELECT 5 AS k, SUM(CASE WHEN prediction = actual_outcome THEN 1 ELSE 0 END) * 1.0 / COUNT(*)
FROM knn_k5
ORDER BY accuracy DESC;
```

**Example 8: KNN for Imputation**
```sql
-- Fill missing values using nearest neighbors
-- Find neighbors for observations with missing values
CREATE VOLATILE TABLE neighbor_lookup AS (
    SELECT * FROM TD_KNN (
        ON data_with_missing AS TestTable PARTITION BY ANY
        ON data_complete AS TrainingTable DIMENSION
        USING
        K(3)
        InputColumns('feature1', 'feature2', 'feature3')  -- Non-missing features
        IDColumn('id')
        ModelType('regression')
        ResponseColumn('missing_feature')  -- Feature to impute
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Replace missing values with KNN predictions
UPDATE data_with_missing
SET missing_feature = (
    SELECT prediction
    FROM neighbor_lookup
    WHERE neighbor_lookup.id = data_with_missing.id
)
WHERE missing_feature IS NULL;
```

**Example 9: Collaborative Filtering Recommendations**
```sql
-- Find similar users for recommendation system
CREATE VOLATILE TABLE similar_users AS (
    SELECT * FROM TD_KNN (
        ON user_query AS TestTable PARTITION BY ANY
        ON user_profiles AS TrainingTable DIMENSION
        USING
        K(10)
        InputColumns('genre1_rating', 'genre2_rating', 'genre3_rating',
                     'avg_rating', 'total_purchases')
        IDColumn('user_id')
        ModelType('neighbors')
        EmitNeighbors('true')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Recommend products that similar users liked
SELECT
    su.user_id AS target_user,
    p.product_id,
    AVG(p.rating) AS predicted_rating
FROM similar_users su
CROSS JOIN LATERAL (
    SELECT neighbor_id1 AS similar_user FROM similar_users WHERE user_id = su.user_id
    UNION ALL
    SELECT neighbor_id2 FROM similar_users WHERE user_id = su.user_id
    -- ... continue for all K neighbors
) neighbors
JOIN purchases p ON p.user_id = neighbors.similar_user
WHERE NOT EXISTS (
    SELECT 1 FROM purchases p2
    WHERE p2.user_id = su.user_id AND p2.product_id = p.product_id
)
GROUP BY su.user_id, p.product_id
ORDER BY su.user_id, predicted_rating DESC;
```

**Example 10: Complete Workflow (Scale + Train + Predict + Evaluate)**
```sql
-- Step 1: Standardize features (critical for KNN)
CREATE VOLATILE TABLE scale_fit AS (
    SELECT * FROM TD_ScaleFit (
        ON credit_raw AS InputTable
        OUT VOLATILE TABLE OutputTable(credit_scale_model)
        USING
        TargetColumns('income', 'debt_ratio', 'credit_history', 'employment_years')
        ScaleMethod('STD')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 2: Transform training data
CREATE VOLATILE TABLE credit_train_scaled AS (
    SELECT * FROM TD_ScaleTransform (
        ON credit_train AS InputTable
        ON credit_scale_model AS FitTable DIMENSION
        USING
        Accumulate('id', 'default')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 3: Transform test data
CREATE VOLATILE TABLE credit_test_scaled AS (
    SELECT * FROM TD_ScaleTransform (
        ON credit_test AS InputTable
        ON credit_scale_model AS FitTable DIMENSION
        USING
        Accumulate('id', 'default')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 4: Apply KNN
CREATE VOLATILE TABLE knn_predictions AS (
    SELECT * FROM TD_KNN (
        ON credit_test_scaled AS TestTable PARTITION BY ANY
        ON credit_train_scaled AS TrainingTable DIMENSION
        USING
        K(7)
        ResponseColumn('default')
        InputColumns('income', 'debt_ratio', 'credit_history', 'employment_years')
        IDColumn('id')
        ModelType('classification')
        VotingWeight(1.0)
        Accumulate('default')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 5: Evaluate
SELECT * FROM TD_ClassificationEvaluator (
    ON knn_predictions AS InputTable PARTITION BY ANY
    USING
    ObservationColumn('default')
    PredictionColumn('prediction')
    NumClasses(2)
) AS dt;

-- Output: Accuracy, Precision, Recall, F1-Score
```

### K-Nearest Neighbors Algorithm Details

**Algorithm Steps:**
1. **Compute Distances**: For each test observation, calculate Euclidean distance to all training observations
   - Distance: d(x, y) = √(Σ(x_i - y_i)²) across all InputColumns
2. **Select K Neighbors**: Sort training observations by distance, select K nearest
3. **Make Prediction**:
   - **Classification**: Majority vote among K neighbors (optionally weighted by inverse distance)
   - **Regression**: Mean of K neighbor response values (optionally weighted)
   - **Neighbors**: Return K neighbor IDs and optionally distances

**Distance Metric:**
- Euclidean distance: d(x, y) = √(Σ(x_i - y_i)²)
- Computed across all InputColumns
- Sensitive to feature scales (standardization critical)

**Weighted Voting:**
- Standard KNN: Equal weight for all K neighbors
- Weighted KNN: w = 1 / POWER(distance, voting_weight)
- Voting_weight=1: Inverse distance weighting (closer neighbors weighted more)
- Voting_weight=2: Inverse square distance weighting (strong emphasis on closest)

**Classification Prediction:**
- Unweighted: prediction = argmax_c (count of class c among K neighbors)
- Weighted: prediction = argmax_c (Σ w_i for neighbors with class c)

**Regression Prediction:**
- Unweighted: prediction = (1/K) * Σ y_i for K neighbors
- Weighted: prediction = Σ(w_i * y_i) / Σ w_i

### Use Cases and Applications

**1. Classification**
- Medical diagnosis from patient symptoms
- Credit risk assessment
- Customer churn prediction
- Fraud detection
- Image classification

**2. Regression**
- Real estate price prediction
- Stock price forecasting
- Energy consumption estimation
- Quality score prediction
- Sales forecasting

**3. Recommendation Systems**
- Collaborative filtering (user-user similarity)
- Content-based recommendations (item-item similarity)
- Hybrid recommendation approaches
- "Customers also viewed" features
- Personalized product suggestions

**4. Pattern Recognition**
- Handwriting recognition
- Facial recognition
- Voice recognition
- Gesture recognition
- Object detection

**5. Anomaly Detection**
- Network intrusion detection
- Fraud detection via outlier analysis
- Equipment failure prediction
- Quality control outliers
- Unusual transaction identification

**6. Text Mining**
- Document classification
- Sentiment analysis
- Spam detection
- Topic categorization
- Author attribution

**7. Bioinformatics**
- Gene classification
- Protein structure prediction
- Disease diagnosis
- Drug discovery
- Species identification

**8. Image Processing**
- Image segmentation
- Object recognition
- Face detection
- Medical image analysis
- Satellite image classification

**9. Customer Analytics**
- Customer segmentation
- Lifetime value prediction
- Propensity modeling
- Next best action
- Cross-sell/upsell targeting

**10. Financial Services**
- Credit scoring
- Loan approval
- Default prediction
- Market segmentation
- Trading signal generation

### Important Notes

**Computational Complexity:**
- Algorithm complexity: O(N²) where N is number of observations
- Scales with both training dataset size and test dataset size
- Query runtime increases significantly as datasets grow
- **Alternative algorithms recommended for large datasets**: Decision trees, random forests, neural networks

**Training Table Scalability:**
- Training table is DIMENSION input (entire table copied to each AMP spool)
- Scalability limited by available spool space
- Use caution with large training datasets (>100k rows)
- Consider sampling training data if performance issues occur

**Feature Scaling - CRITICAL:**
- KNN uses Euclidean distance, highly sensitive to feature scales
- **MUST standardize features** using TD_ScaleFit and TD_ScaleTransform before KNN
- Features with larger ranges dominate distance calculations
- Example: Income ($10k-$200k) dominates age (18-80) without scaling

**Choosing Optimal K:**
- Small K (1-3): Sensitive to noise, captures local patterns, risk of overfitting
- Medium K (5-10): Balanced approach for most applications
- Large K (15-50): Smoother boundaries, less sensitive to outliers, risk of underfitting
- **Rule of thumb**: K ≈ √(N) where N is training set size
- Use cross-validation to find optimal K

**Lazy Learning Characteristics:**
- No explicit training phase (training data stored as-is)
- All computation occurs at prediction time
- Memory-intensive (stores entire training dataset)
- Prediction time increases with training set size

**Missing Values:**
- Function skips rows with NULL values
- Impute missing values before using KNN (TD_SimpleImpute)
- Alternatively, use KNN itself for imputation

**Feature Limits:**
- Maximum 2018 features (InputColumns) supported
- For high-dimensional data, consider dimensionality reduction (TD_PCA)
- Curse of dimensionality: KNN performance degrades with many features

**Classification Limits:**
- Maximum 1000 classes supported
- Class labels must be numeric integers
- For multi-class problems, ensure balanced training data

**Deterministic Results:**
- Results deterministic given same training and test data
- No randomization in algorithm
- Reproducible across runs

### Best Practices

**1. Always Standardize Features**
- **Critical**: Use TD_ScaleFit and TD_ScaleTransform before KNN
- Apply same scaling to training and test data
- Use ScaleMethod='STD' for most cases
- Save FitTable for production scoring

**2. Choose K Carefully**
- Start with K=5 as default
- Try odd K values to avoid tie votes (classification)
- Use cross-validation to tune K
- Plot accuracy vs K to find optimal value

**3. Use Weighted Voting for Better Predictions**
- Set VotingWeight=1.0 for inverse distance weighting
- Closer neighbors contribute more to prediction
- Reduces influence of distant K neighbors
- Particularly useful for larger K values

**4. Handle Imbalanced Classes**
- For imbalanced classification, consider:
  - Oversampling minority class in training data
  - Undersampling majority class
  - Adjusting VotingWeight to emphasize closest neighbors
- Evaluate with Precision/Recall/F1, not just Accuracy

**5. Optimize for Performance**
- Limit training dataset size if possible
- Use TD_RANDOMSAMPLE to create training subset
- Consider alternative algorithms for large datasets
- Monitor query execution time and spool usage

**6. Feature Engineering**
- Remove irrelevant features (hurt distance calculations)
- Create domain-specific features
- Use dimensionality reduction (TD_PCA) for many features
- Consider feature selection techniques

**7. Emit Neighbors for Interpretability**
- Set EmitNeighbors='true' to see which training examples influenced prediction
- Useful for debugging and explaining predictions
- EmitDistances='true' to assess confidence (large distances = uncertain predictions)

**8. Handle Missing Values**
- Impute missing values before KNN
- Use TD_SimpleImpute with appropriate strategy
- Consider domain-specific imputation
- Alternatively, use KNN itself for imputation (meta-approach)

**9. Validate Thoroughly**
- Use holdout test set for evaluation
- Perform k-fold cross-validation to tune K
- Examine confusion matrix for classification
- Analyze residuals for regression
- Check for overfitting (train vs test accuracy)

**10. Consider Alternatives for Large Data**
- KNN not suitable for very large training/test sets
- Alternatives: TD_DecisionForest, TD_XGBoost, TD_GLM, TD_SVM
- KNN best for: small-medium datasets, interpretability, non-parametric modeling

### Related Functions
- **TD_ScaleFit** - Standardize features (required preprocessing)
- **TD_ScaleTransform** - Apply standardization to new data
- **TD_SimpleImpute** - Fill missing values before training
- **TD_ClassificationEvaluator** - Evaluate classification performance
- **TD_RegressionEvaluator** - Evaluate regression performance
- **TD_PCA** - Reduce dimensionality for high-dimensional data
- **TD_VectorDistance** - Compute pairwise distances (underlying distance calculation)
- **TD_DecisionForest** - Alternative for large datasets
- **TD_GLM** - Alternative linear classifier
- **TD_KMeans** - Alternative for unsupervised clustering

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Model Training Functions
