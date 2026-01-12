# TD_ScaleTransform

### Function Name
**TD_ScaleTransform**

### Description
TD_ScaleTransform applies feature scaling transformations using the statistics calculated by TD_ScaleFit. This function performs the actual scaling of numeric features according to the chosen scaling method (Z-score, Min-Max, MaxAbs, etc.), transforming raw feature values into normalized or standardized values suitable for machine learning algorithms.

This is the execution component of the feature scaling pipeline. After TD_ScaleFit calculates and stores scaling statistics (mean, standard deviation, min, max, etc.) in a FitTable, TD_ScaleTransform applies these statistics to transform data consistently across training, validation, test, and production datasets. Consistent scaling is fundamental to machine learning success, ensuring that all datasets undergo identical transformations using parameters derived solely from training data.

The transformation is deterministic given a FitTable, enabling reproducible preprocessing pipelines. This consistency prevents data leakage, maintains model validity, and ensures that production predictions use the same feature scales as model training.

### When the Function Would Be Used
- **Apply Feature Scaling**: Execute scaling transformations on data
- **ML Pipeline Execution**: Transform training, validation, and test data
- **Production Scoring**: Scale incoming data for real-time predictions
- **Model Training**: Prepare features for gradient descent algorithms
- **Distance Calculations**: Enable fair similarity computations
- **Neural Network Input**: Normalize features for faster convergence
- **Regularized Models**: Ensure balanced regularization across features
- **Cross-Dataset Consistency**: Apply identical scaling to multiple datasets
- **Feature Engineering**: Create standardized features for modeling
- **Algorithm Preprocessing**: Prepare data for distance-based algorithms

### Syntax

**Dense Input Format:**
```sql
TD_ScaleTransform (
    ON { table | view | (query) } AS InputTable [ PARTITION BY ANY ]
    ON { table | view | (query) } AS FitTable AS FitTableAlias DIMENSION
    USING
    [ Accumulate ({'accumulate_column' | 'accumulate_column_range'}[,...]) ]
)
```

**Sparse Input Format:**
```sql
TD_ScaleTransform (
    ON { table | view | (query) } AS InputTable PARTITION BY attribute_column
    ON { table | view | (query) } AS FitTable AS FitTableAlias DIMENSION
    USING
    [ Accumulate ({'accumulate_column' | 'accumulate_column_range'}[,...]) ]
)
```

### Required Syntax Elements for TD_ScaleTransform

**ON clause (InputTable)**
- Accepts the InputTable clause containing data to scale
- Must have same columns as data used for TD_ScaleFit
- PARTITION BY ANY recommended for parallel processing (dense format)
- PARTITION BY attribute_column required (sparse format)

**ON clause (FitTable DIMENSION)**
- Accepts the FitTable clause (output from TD_ScaleFit)
- Contains scaling statistics and method specification
- DIMENSION keyword required

### Optional Syntax Elements for TD_ScaleTransform

**Accumulate**
- Specify input table column names to copy to output table
- Useful for preserving identifiers, keys, and metadata
- Supports column range notation
- Typically includes ID columns and target variable (for training)

### Input Table Schema

**Dense InputTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | Numeric types | Columns specified in TD_ScaleFit TargetColumns |
| accumulate_column | ANY | [Optional] Columns to preserve in output |

**Sparse InputTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| attribute_column | VARCHAR | Column containing attribute names |
| value_column | Numeric types | Column containing numeric values |
| accumulate_column | ANY | [Optional] Columns to preserve in output |

**FitTable Schema:**

See TD_ScaleFit Output table schema. This is the statistics table created by TD_ScaleFit function.

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| accumulate_column | Same as InputTable | Columns specified in Accumulate parameter |
| scaled_column | DOUBLE PRECISION | Scaled versions of target columns with same names as original |

All scaled columns are DOUBLE PRECISION type regardless of input type.

### Code Examples

**Input Data: customer_features**
```
customer_id  age  income   credit_score  years_customer
1            25   45000    650           2.0
2            45   85000    720           10.0
3            35   62000    680           5.0
```

**FitTable: scale_fit_zscore** (created by TD_ScaleFit)
```
-- Created with ScaleMethod('MEAN') on training data
-- Contains mean and std for each feature
```

**Example 1: Z-Score Transformation (MEAN Method)**
```sql
-- Step 1: Create fit table (already done)
CREATE TABLE scale_fit_zscore AS (
    SELECT * FROM TD_ScaleFit (
        ON training_data AS InputTable
        USING
        TargetColumns('age', 'income', 'credit_score', 'years_customer')
        ScaleMethod('MEAN')
        MissValue('OMIT')
    ) AS dt
) WITH DATA;

-- Step 2: Apply transformation to training data
SELECT * FROM TD_ScaleTransform (
    ON customer_features AS InputTable
    ON scale_fit_zscore AS FitTable DIMENSION
    USING
    Accumulate('customer_id')
) AS dt
ORDER BY customer_id;
```

**Output:**
```
customer_id  age    income  credit_score  years_customer
1            -1.11  -0.96   -0.92         -0.97
2            0.74   0.42    0.78          0.58
3            -0.19  -0.37   -0.19         -0.39
```

**Transformation Applied:** (x - mean) / std for each feature

**Example 2: Transform Training and Test Data**
```sql
-- Transform training set
CREATE TABLE training_scaled AS (
    SELECT * FROM TD_ScaleTransform (
        ON training_data AS InputTable
        ON scale_fit AS FitTable DIMENSION
        USING
        Accumulate('id', 'target')
    ) AS dt
) WITH DATA;

-- Transform test set with SAME FitTable
CREATE TABLE test_scaled AS (
    SELECT * FROM TD_ScaleTransform (
        ON test_data AS InputTable
        ON scale_fit AS FitTable DIMENSION  -- Same FitTable!
        USING
        Accumulate('id')
    ) AS dt
) WITH DATA;
```

**Example 3: Min-Max Transformation (RANGE Method)**
```sql
-- Create Min-Max fit
CREATE TABLE scale_fit_minmax AS (
    SELECT * FROM TD_ScaleFit (
        ON training_data AS InputTable
        USING
        TargetColumns('age', 'income', 'credit_score')
        ScaleMethod('RANGE')
    ) AS dt
) WITH DATA;

-- Apply transformation to scale features to [0, 1]
SELECT * FROM TD_ScaleTransform (
    ON new_data AS InputTable
    ON scale_fit_minmax AS FitTable DIMENSION
    USING
    Accumulate('id')
) AS dt;
```

**Output:** All features scaled to [0, 1] range

**Example 4: MaxAbs Transformation for Sparse Data**
```sql
-- Apply MaxAbs scaling (preserves zeros, good for sparse data)
CREATE TABLE sparse_scaled AS (
    SELECT * FROM TD_ScaleTransform (
        ON sparse_features AS InputTable
        ON maxabs_fit AS FitTable DIMENSION
        USING
        Accumulate('feature_id')
    ) AS dt
) WITH DATA;

-- Features now in [-1, 1] range with zeros preserved
```

**Example 5: Production Scoring Pipeline**
```sql
-- Score new customers using model trained on scaled data
-- Step 1: Scale incoming data using production FitTable
CREATE TABLE new_customers_scaled AS (
    SELECT * FROM TD_ScaleTransform (
        ON new_customers AS InputTable
        ON prod_scale_fit AS FitTable DIMENSION  -- Production FitTable
        USING
        Accumulate('customer_id', 'customer_name')
    ) AS dt
) WITH DATA;

-- Step 2: Apply trained model
SELECT * FROM TD_GLMPredict (
    ON new_customers_scaled AS InputTable
    ON trained_model AS ModelTable DIMENSION
    USING
    IDColumn('customer_id')
    Accumulate('customer_name')
) AS dt;
```

**Example 6: Neural Network Preprocessing**
```sql
-- Scale features for neural network
CREATE TABLE nn_features_scaled AS (
    SELECT * FROM TD_ScaleTransform (
        ON nn_input_data AS InputTable
        ON nn_scale_fit AS FitTable DIMENSION
        USING
        Accumulate('id', 'target')
    ) AS dt
) WITH DATA;

-- Critical for NN convergence and stability
```

**Example 7: K-Means Clustering with Scaling**
```sql
-- Step 1: Scale features
CREATE TABLE data_scaled AS (
    SELECT * FROM TD_ScaleTransform (
        ON customer_data AS InputTable
        ON scale_fit AS FitTable DIMENSION
        USING
        Accumulate('customer_id')
    ) AS dt
) WITH DATA;

-- Step 2: Cluster on scaled features
CREATE TABLE clusters AS (
    SELECT * FROM TD_KMeans (
        ON data_scaled AS InputTable
        USING
        TargetColumns('[2:]')  -- All scaled features
        NumClusters(5)
        Seed(123)
    ) AS dt
) WITH DATA;
```

**Example 8: Complete ML Pipeline**
```sql
-- End-to-end scaling pipeline
-- Step 1: Fit on training data only
CREATE TABLE scale_fit AS (
    SELECT * FROM TD_ScaleFit (
        ON training_data AS InputTable
        USING
        TargetColumns('[5:55]')  -- 50 features
        ScaleMethod('MEAN')
    ) AS dt
) WITH DATA;

-- Step 2: Transform training data
CREATE TABLE train_scaled AS (
    SELECT * FROM TD_ScaleTransform (
        ON training_data AS InputTable
        ON scale_fit AS FitTable DIMENSION
        USING
        Accumulate('id', 'target')
    ) AS dt
) WITH DATA;

-- Step 3: Transform validation data
CREATE TABLE val_scaled AS (
    SELECT * FROM TD_ScaleTransform (
        ON validation_data AS InputTable
        ON scale_fit AS FitTable DIMENSION
        USING
        Accumulate('id', 'target')
    ) AS dt
) WITH DATA;

-- Step 4: Transform test data
CREATE TABLE test_scaled AS (
    SELECT * FROM TD_ScaleTransform (
        ON test_data AS InputTable
        ON scale_fit AS FitTable DIMENSION
        USING
        Accumulate('id')
    ) AS dt
) WITH DATA;

-- Step 5: Train model on train_scaled
-- Step 6: Validate on val_scaled
-- Step 7: Evaluate on test_scaled
```

**Example 9: Sparse Format Transformation**
```sql
-- Transform sparse attribute-value data
CREATE TABLE sparse_scaled AS (
    SELECT * FROM TD_ScaleTransform (
        ON sparse_features AS InputTable PARTITION BY attribute_name
        ON sparse_scale_fit AS FitTable DIMENSION
        USING
        Accumulate('id')
    ) AS dt
) WITH DATA;
```

**Example 10: Custom Rescaling (RESCALE Method)**
```sql
-- Apply custom linear transformation (y = 10x + 5)
SELECT * FROM TD_ScaleTransform (
    ON feature_data AS InputTable
    ON rescale_fit AS FitTable DIMENSION
    USING
    Accumulate('id', 'category')
) AS dt;

-- Useful for unit conversions or domain-specific transformations
```

### Feature Scaling Transformation Process

**Before Transformation (original features):**
```
id  age  income  credit_score
1   25   45000   650
2   45   85000   720
3   35   62000   680
```

**After Z-Score Transformation (MEAN method):**
```
id  age    income  credit_score
1   -1.11  -0.96   -0.92
2   0.74   0.42    0.78
3   -0.19  -0.37   -0.19
```

**After Min-Max Transformation (RANGE method):**
```
id  age   income  credit_score
1   0.00  0.00    0.00
2   1.00  1.00    1.00
3   0.50  0.42    0.43
```

**Key Transformation Characteristics:**
- Values transformed using FitTable statistics
- Original column names preserved
- All output columns are DOUBLE PRECISION
- Accumulate columns passed through unchanged
- Deterministic transformation (same input + FitTable = same output)

### Use Cases and Applications

**1. Neural Network Training**
- Scale features to accelerate convergence
- Prevent vanishing/exploding gradients
- Ensure balanced feature contributions
- Improve model stability and performance

**2. Gradient Descent Algorithms**
- Linear regression, logistic regression
- Faster convergence with scaled features
- Balanced gradient contributions
- Prevents oscillation during optimization

**3. Distance-Based Algorithms**
- K-Nearest Neighbors (k-NN)
- K-Means clustering
- DBSCAN, hierarchical clustering
- Fair distance calculations across features

**4. Support Vector Machines (SVM)**
- Required for RBF and polynomial kernels
- Balanced margin calculations
- Improved optimization performance
- Better generalization

**5. Regularized Linear Models**
- Ridge, Lasso, ElasticNet regression
- Ensures regularization affects all features equally
- Prevents bias toward large-magnitude features
- Improves coefficient interpretability

**6. Principal Component Analysis (PCA)**
- Scaled features essential for meaningful components
- Prevents dominant features from overwhelming analysis
- Enables fair variance explanation
- Standard preprocessing for dimensionality reduction

**7. Ensemble Methods**
- Gradient boosting (XGBoost, LightGBM, CatBoost)
- Random forests (optional but doesn't hurt)
- Stacking and blending ensembles
- Improves meta-model performance

**8. Recommender Systems**
- Collaborative filtering
- Content-based filtering
- Hybrid recommender systems
- Fair similarity calculations

**9. Time Series Forecasting**
- LSTM, GRU neural networks
- ARIMA with exogenous variables
- Prophet with additional regressors
- Improved convergence and stability

**10. Image and Signal Processing**
- Pixel intensity normalization
- Convolutional neural network preprocessing
- Signal amplitude normalization
- Feature extraction pipelines

### Important Notes

**Train-Test Consistency:**
- CRITICAL: Always fit on training data only
- Apply same FitTable to all datasets
- Never fit on test data (causes data leakage)
- Store FitTable with model artifacts for production

**Output Data Types:**
- All scaled columns are DOUBLE PRECISION
- Original column names preserved
- Accumulate columns retain original types
- Consider storage and computational implications

**NULL Handling:**
- NULL values propagate through transformation
- If input feature is NULL, output is NULL
- Handle NULLs before scaling (imputation)
- Use TD_SimpleImputeFit/Transform first

**Scaling Method Results:**
- **MEAN**: mean≈0, std≈1
- **RANGE**: values in [0, 1]
- **MAXABS**: values in [-1, 1]
- **SUM**: values sum to 1.0
- Each method produces different distributions

**Outliers:**
- Outliers in new data may fall outside training range
- RANGE: New data may exceed [0, 1] if outside training min/max
- MEAN: Outliers become large z-scores (e.g., z>3)
- Monitor for extreme values in production

**Computational Performance:**
- Transformation is fast (simple arithmetic)
- PARTITION BY ANY enables parallel processing
- Scales well to large datasets
- Minimal memory overhead

**Sparse Data:**
- MAXABS preserves zeros (good for sparse features)
- MEAN/RANGE may destroy sparsity (centering adds non-zeros)
- Choose method based on data structure
- Consider sparsity preservation needs

**Comparison to Other Transformations:**
- Column-wise scaling (TD_ScaleTransform)
- Row-wise normalization (TD_RowNormalizeTransform)
- Different objectives and applications
- Not interchangeable

### Best Practices

**1. Consistent Transformation Across Datasets**
- Fit on training data only
- Apply to all datasets with same FitTable
- Store FitTable with model
- Version control transformation artifacts

**2. Preprocessing Order Matters**
- Imputation → Outlier Removal → Scaling
- Handle NULLs before scaling
- Remove outliers before scaling (if needed)
- Document preprocessing pipeline

**3. Validate Transformation Results**
- Check scaled feature distributions
- Verify z-scores not extreme (typically -3 to +3)
- Monitor for NaN or Inf values
- Test on sample data first

**4. Production Deployment**
- Deploy FitTable with model
- Validate compatibility before scoring
- Implement input validation
- Monitor for scaling issues

**5. Handle Edge Cases**
- New data outside training range
- Extreme outliers in production
- NULL values in input
- Zero standard deviation features (constant)

**6. Monitor Performance**
- Track model accuracy after scaling
- Compare to unscaled baseline
- Validate business impact
- Adjust scaling method if needed

**7. Don't Scale Certain Features**
- Binary features (0/1) often don't need scaling
- Categorical encoded features (one-hot)
- Target variable (typically not scaled for classification)
- Features already on comparable scales

**8. Inverse Transformations**
- For regression, may scale target variable
- Inverse-transform predictions to original scale
- Store scaling parameters for inverse transform
- Document transformation and inverse procedures

**9. Documentation and Governance**
- Document scaling method and parameters
- Record FitTable creation date and data
- Maintain transformation specifications
- Enable reproducibility and auditing

**10. Test Different Methods**
- Compare model performance with different scaling
- MEAN for most cases
- RANGE for neural networks
- MAXABS for sparse data
- Validate on holdout data

### Related Functions
- **TD_ScaleFit** - Creates scaling statistics (must be run before TD_ScaleTransform)
- **TD_SimpleImputeFit/Transform** - Handle missing values before scaling
- **TD_OutlierFilterFit** - Remove outliers before scaling
- **TD_PolynomialFeaturesFit** - Often used after scaling
- **TD_RowNormalizeTransform** - Row-wise normalization (alternative)

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Transform Functions
