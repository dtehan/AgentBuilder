# TD_ScaleFit

### Function Name
**TD_ScaleFit**

### Description
TD_ScaleFit calculates scaling statistics (mean, standard deviation, min, max, etc.) for numeric features and stores them in a FitTable for use by TD_ScaleTransform. This function is the foundation of feature scaling, a critical preprocessing step in machine learning that ensures all features are on comparable scales, preventing features with larger magnitudes from dominating model training.

Feature scaling is essential because many machine learning algorithms (gradient descent-based methods, distance-based algorithms, regularized models) are sensitive to feature scales. Without scaling, features with larger numeric ranges can disproportionately influence model weights, learning rates, and distance calculations. TD_ScaleFit supports eight scaling methods to accommodate different data distributions and algorithmic requirements.

The function supports both dense (traditional columnar) and sparse (attribute-value) data formats, making it versatile for various data structures. It can perform global scaling (using statistics from all data) or individual column scaling, with options to customize transformations using multipliers and intercepts.

### When the Function Would Be Used
- **ML Preprocessing**: Scale features before training machine learning models
- **Gradient Descent Optimization**: Ensure faster convergence by normalizing features
- **Distance-Based Algorithms**: Enable fair distance calculations (k-NN, K-Means, SVM)
- **Regularization**: Ensure regularization affects all features equally
- **Neural Network Training**: Accelerate convergence with normalized inputs
- **Linear/Logistic Regression**: Improve coefficient interpretability
- **Feature Engineering**: Create standardized features for modeling
- **Principal Component Analysis**: Prepare data for PCA/dimensionality reduction
- **Ensemble Methods**: Normalize features for gradient boosting, random forests
- **Cross-Dataset Comparison**: Enable comparison of features across datasets

### Syntax

**Dense Input Format:**
```sql
TD_ScaleFit (
    ON { table | view | (query) } AS InputTable
    USING
    TargetColumns ({ 'target_column' | target_column_range }[,...])
    ScaleMethod ('MEAN' | 'SUM' | 'USTD' | 'STD' | 'RANGE' | 'MIDRANGE' | 'MAXABS' | 'RESCALE')
    [ MissValue ('KEEP' | 'OMIT' | 'FAIL') ]
    [ GlobalScale ('true' | 'false') ]
    [ Multiplier (multiplier_value) ]
    [ Intercept (intercept_value) ]
)
```

**Sparse Input Format:**
```sql
TD_ScaleFit (
    ON { table | view | (query) } AS InputTable PARTITION BY attribute_column
    USING
    TargetAttributes ('target_attribute' [,...])
    AttributeColumn ('attribute_column')
    ValueColumn ('value_column')
    ScaleMethod ('MEAN' | 'SUM' | 'USTD' | 'STD' | 'RANGE' | 'MIDRANGE' | 'MAXABS' | 'RESCALE')
    [ MissValue ('KEEP' | 'OMIT' | 'FAIL') ]
    [ GlobalScale ('true' | 'false') ]
    [ Multiplier (multiplier_value) ]
    [ Intercept (intercept_value) ]
)
```

### Required Syntax Elements for TD_ScaleFit

**ON clause**
- Accepts the InputTable clause containing numeric features
- For sparse format: PARTITION BY attribute_column required

**TargetColumns (Dense) or TargetAttributes (Sparse)**
- Specify columns/attributes to scale
- Must be numeric data types
- Supports column range notation (dense format only)

**ScaleMethod**
- Specify scaling method to compute statistics
- **MEAN**: Z-score normalization (mean=0, std=1)
- **SUM**: Scale by sum of values
- **USTD**: Standardize by unbiased standard deviation
- **STD**: Standardize by standard deviation
- **RANGE**: Min-max normalization to [0, 1]
- **MIDRANGE**: Center by midpoint, scale by range
- **MAXABS**: Scale by maximum absolute value to [-1, 1]
- **RESCALE**: Linear transformation with custom multiplier/intercept

**AttributeColumn (Sparse only)**
- Column containing attribute names in sparse format

**ValueColumn (Sparse only)**
- Column containing attribute values in sparse format

### Optional Syntax Elements for TD_ScaleFit

**MissValue**
- Specify how to handle missing (NULL) values
- **'KEEP'**: Keep NULL values (default)
- **'OMIT'**: Exclude NULLs from statistics calculation
- **'FAIL'**: Fail if NULLs encountered
- Default: 'KEEP'

**GlobalScale**
- Specify whether to use global scaling across all columns
- **'true'**: Use same scaling parameters for all columns (single mean, std, etc.)
- **'false'**: Scale each column independently (default)
- Default: 'false'

**Multiplier**
- Specify multiplier for RESCALE method
- Numeric value to multiply scaled values
- Used in linear transformation: y = multiplier × x + intercept
- Only applicable with ScaleMethod='RESCALE'

**Intercept**
- Specify intercept for RESCALE method
- Numeric value to add to scaled values
- Used in linear transformation: y = multiplier × x + intercept
- Only applicable with ScaleMethod='RESCALE'

### Input Table Schema

**Dense InputTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | Numeric types (INTEGER, BIGINT, FLOAT, DOUBLE PRECISION, DECIMAL, NUMERIC) | Columns to be scaled |

**Sparse InputTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| attribute_column | VARCHAR | Column containing attribute names |
| value_column | Numeric types | Column containing numeric values |

### Output Table Schema (FitTable)

| Column | Data Type | Description |
|--------|-----------|-------------|
| column_name (or attribute) | VARCHAR | Name of the column/attribute |
| scale_method | VARCHAR | Scaling method used |
| mean | DOUBLE PRECISION | Mean value (for MEAN, STD, USTD methods) |
| std | DOUBLE PRECISION | Standard deviation (for MEAN, STD, USTD methods) |
| min | DOUBLE PRECISION | Minimum value (for RANGE, MIDRANGE methods) |
| max | DOUBLE PRECISION | Maximum value (for RANGE, MIDRANGE, MAXABS methods) |
| sum | DOUBLE PRECISION | Sum of values (for SUM method) |
| multiplier | DOUBLE PRECISION | Multiplier value (for RESCALE method) |
| intercept | DOUBLE PRECISION | Intercept value (for RESCALE method) |

The FitTable contains statistics needed by TD_ScaleTransform. Not all columns are populated for every method; only relevant statistics for the chosen ScaleMethod are stored.

### Code Examples

**Input Data: customer_features**
```
customer_id  age  income   credit_score  years_customer
1            25   45000    650           2.0
2            45   85000    720           10.0
3            35   62000    680           5.0
4            52   120000   750           15.0
5            28   52000    640           3.0
```

**Example 1: Z-Score Normalization (MEAN Method)**
```sql
-- Standardize features to mean=0, std=1
CREATE TABLE scale_fit_zscore AS (
    SELECT * FROM TD_ScaleFit (
        ON customer_features AS InputTable
        USING
        TargetColumns('age', 'income', 'credit_score', 'years_customer')
        ScaleMethod('MEAN')
        MissValue('OMIT')
    ) AS dt
) WITH DATA;

-- View scaling statistics
SELECT * FROM scale_fit_zscore;
```

**Output FitTable:**
```
column_name      scale_method  mean      std        min  max  sum  multiplier  intercept
age              MEAN          37.0      10.84      NULL NULL NULL NULL        NULL
income           MEAN          72800     28946      NULL NULL NULL NULL        NULL
credit_score     MEAN          688       41.23      NULL NULL NULL NULL        NULL
years_customer   MEAN          7.0       5.15       NULL NULL NULL NULL        NULL
```

**Example 2: Min-Max Normalization (RANGE Method)**
```sql
-- Scale features to [0, 1] range
CREATE TABLE scale_fit_minmax AS (
    SELECT * FROM TD_ScaleFit (
        ON customer_features AS InputTable
        USING
        TargetColumns('age', 'income', 'credit_score')
        ScaleMethod('RANGE')
    ) AS dt
) WITH DATA;
```

**Output FitTable:**
```
column_name     scale_method  mean  std   min    max     sum  multiplier  intercept
age             RANGE         NULL  NULL  25     52      NULL NULL        NULL
income          RANGE         NULL  NULL  45000  120000  NULL NULL        NULL
credit_score    RANGE         NULL  NULL  640    750     NULL NULL        NULL
```

**Example 3: Max Absolute Value Scaling (MAXABS Method)**
```sql
-- Scale to [-1, 1] based on maximum absolute value
CREATE TABLE scale_fit_maxabs AS (
    SELECT * FROM TD_ScaleFit (
        ON sensor_data AS InputTable
        USING
        TargetColumns('sensor1', 'sensor2', 'sensor3', 'sensor4')
        ScaleMethod('MAXABS')
    ) AS dt
) WITH DATA;

-- Preserves zeros, useful for sparse data
```

**Example 4: Custom Rescaling with Multiplier and Intercept**
```sql
-- Custom linear transformation: y = 10x + 5
CREATE TABLE scale_fit_custom AS (
    SELECT * FROM TD_ScaleFit (
        ON feature_data AS InputTable
        USING
        TargetColumns('feature1', 'feature2')
        ScaleMethod('RESCALE')
        Multiplier(10)
        Intercept(5)
    ) AS dt
) WITH DATA;
```

**Example 5: Global Scaling**
```sql
-- Use same scaling parameters for all columns
CREATE TABLE scale_fit_global AS (
    SELECT * FROM TD_ScaleFit (
        ON multi_feature_data AS InputTable
        USING
        TargetColumns('[3:103]')  -- 100 features
        ScaleMethod('MEAN')
        GlobalScale('true')  -- Single mean/std for all columns
    ) AS dt
) WITH DATA;

-- All columns scaled using global mean and standard deviation
```

**Example 6: Sparse Format Scaling**
```sql
-- Scale sparse attribute-value data
CREATE TABLE scale_fit_sparse AS (
    SELECT * FROM TD_ScaleFit (
        ON sparse_features AS InputTable PARTITION BY attribute_name
        USING
        TargetAttributes('age', 'income', 'balance')
        AttributeColumn('attribute_name')
        ValueColumn('attribute_value')
        ScaleMethod('MEAN')
        MissValue('OMIT')
    ) AS dt
) WITH DATA;
```

**Example 7: Training Data Scaling (ML Pipeline)**
```sql
-- Step 1: Calculate scaling statistics on training data ONLY
CREATE TABLE train_scale_fit AS (
    SELECT * FROM TD_ScaleFit (
        ON training_data AS InputTable
        USING
        TargetColumns('[5:55]')  -- 50 numeric features
        ScaleMethod('MEAN')
        MissValue('OMIT')
    ) AS dt
) WITH DATA;

-- Store this FitTable for applying to train, validation, test, production data
```

**Example 8: Different Scaling Methods Comparison**
```sql
-- Compare different scaling methods for same data
-- Method 1: Z-score (MEAN)
CREATE TABLE fit_mean AS (
    SELECT * FROM TD_ScaleFit (ON data AS InputTable USING TargetColumns('feature1', 'feature2') ScaleMethod('MEAN'))
) WITH DATA;

-- Method 2: Min-Max (RANGE)
CREATE TABLE fit_range AS (
    SELECT * FROM TD_ScaleFit (ON data AS InputTable USING TargetColumns('feature1', 'feature2') ScaleMethod('RANGE'))
) WITH DATA;

-- Method 3: MaxAbs
CREATE TABLE fit_maxabs AS (
    SELECT * FROM TD_ScaleFit (ON data AS InputTable USING TargetColumns('feature1', 'feature2') ScaleMethod('MAXABS'))
) WITH DATA;
```

**Example 9: Handle Missing Values**
```sql
-- Omit NULL values from statistics calculation
CREATE TABLE scale_fit_omit_nulls AS (
    SELECT * FROM TD_ScaleFit (
        ON data_with_nulls AS InputTable
        USING
        TargetColumns('feat1', 'feat2', 'feat3')
        ScaleMethod('MEAN')
        MissValue('OMIT')  -- Exclude NULLs from mean/std calculation
    ) AS dt
) WITH DATA;
```

**Example 10: Neural Network Preprocessing**
```sql
-- Prepare features for neural network training
CREATE TABLE nn_scale_fit AS (
    SELECT * FROM TD_ScaleFit (
        ON nn_training_data AS InputTable
        USING
        TargetColumns('[10:60]')  -- All input features
        ScaleMethod('MEAN')  -- Z-score normalization for NN
        MissValue('FAIL')  -- Ensure no NULLs
    ) AS dt
) WITH DATA;

-- Critical for neural network convergence
```

### Scaling Methods Explained

**1. MEAN (Z-Score Normalization)**

Formula: x_scaled = (x - μ) / σ

Where:
- μ = mean of feature
- σ = standard deviation

**Result:** mean=0, std=1

**Use Cases:**
- Most common scaling method
- Ideal for gradient descent algorithms
- Required for algorithms assuming normally distributed data
- Good for linear/logistic regression, neural networks, SVM with RBF kernel

**2. SUM (Sum Normalization)**

Formula: x_scaled = x / Σx

**Result:** Values sum to 1.0

**Use Cases:**
- Probability-like features
- Proportion-based features
- Similar to column-wise FRACTION normalization

**3. USTD (Unbiased Standard Deviation)**

Formula: x_scaled = (x - μ) / s

Where:
- μ = mean
- s = unbiased standard deviation (n-1 divisor)

**Result:** Similar to MEAN but using unbiased estimator

**Use Cases:**
- Small sample sizes
- Statistical inference applications

**4. STD (Standard Deviation)**

Formula: x_scaled = x / σ

Where:
- σ = standard deviation (not centered)

**Result:** Scaled by std only, not centered

**Use Cases:**
- When centering not desired
- Preserving distribution shape

**5. RANGE (Min-Max Normalization)**

Formula: x_scaled = (x - min) / (max - min)

**Result:** Values in [0, 1] range

**Use Cases:**
- Neural networks (activation function ranges)
- Image processing (pixel intensities)
- When bounded range required
- Algorithms sensitive to outliers (preserves them)

**6. MIDRANGE (Midpoint Normalization)**

Formula: x_scaled = (x - midpoint) / range

Where:
- midpoint = (min + max) / 2
- range = max - min

**Result:** Centered at 0, scaled by range

**Use Cases:**
- Symmetric distributions
- When midpoint more meaningful than mean

**7. MAXABS (Maximum Absolute Value Scaling)**

Formula: x_scaled = x / max(|x|)

**Result:** Values in [-1, 1] range

**Use Cases:**
- Sparse data (preserves zeros)
- Signed features where sign important
- When centering would destroy sparsity

**8. RESCALE (Custom Linear Transformation)**

Formula: x_scaled = multiplier × x + intercept

**Result:** Custom scaling with specified parameters

**Use Cases:**
- Domain-specific transformations
- Converting units (e.g., Celsius to Fahrenheit)
- Custom business logic

### Use Cases and Applications

**1. Neural Network Training**
- Z-score (MEAN) or Min-Max (RANGE) normalization
- Prevents vanishing/exploding gradients
- Accelerates convergence
- Improves model stability

**2. Gradient Descent Optimization**
- Z-score normalization for faster convergence
- Prevents oscillation during optimization
- Ensures balanced feature contributions
- Critical for linear/logistic regression

**3. Distance-Based Algorithms**
- K-Means clustering
- K-Nearest Neighbors (k-NN)
- DBSCAN clustering
- Ensures fair distance calculations

**4. Support Vector Machines (SVM)**
- Required for RBF and polynomial kernels
- Ensures balanced margin calculations
- Improves optimization convergence
- Z-score or Min-Max recommended

**5. Regularized Models**
- Linear regression with L1/L2 regularization
- Ensures regularization affects all features equally
- Prevents bias toward high-magnitude features
- Critical for Ridge, Lasso, ElasticNet

**6. Principal Component Analysis (PCA)**
- Features must be scaled for meaningful components
- Z-score normalization typically used
- Prevents dominant features from overwhelming analysis

**7. Recommender Systems**
- Normalize user ratings or item features
- Enable fair similarity calculations
- Collaborative filtering preprocessing

**8. Time Series Forecasting**
- Normalize features for LSTM, GRU networks
- Improve convergence and stability
- Handle varying magnitude patterns

**9. Image Processing**
- Pixel intensity normalization
- Min-Max to [0, 1] or [-1, 1]
- Prepare for convolutional neural networks

**10. Cross-Dataset Analysis**
- Enable comparison across datasets
- Standardize features for meta-analysis
- Combine data from different sources

### Important Notes

**Train-Test Consistency:**
- CRITICAL: Always fit on training data only
- Apply same FitTable to train, validation, test, production
- Never fit on test data (causes data leakage)
- Store FitTable with model artifacts

**ScaleMethod Selection:**
- **Gradient descent algorithms**: MEAN (Z-score)
- **Neural networks**: MEAN or RANGE
- **Tree-based models**: Often don't require scaling (but doesn't hurt)
- **Distance-based algorithms**: MEAN or RANGE
- **Sparse data**: MAXABS (preserves zeros)

**Missing Values:**
- Handle NULLs before scaling (OMIT or impute first)
- MissValue='OMIT' excludes NULLs from statistics
- Consider imputation with TD_SimpleImputeFit first

**Outliers:**
- MEAN sensitive to outliers (affects mean/std)
- RANGE very sensitive (outliers define range)
- Consider outlier removal before scaling
- MAXABS robust for signed data

**GlobalScale:**
- Use sparingly (destroys individual feature characteristics)
- Useful when all features on similar scales already
- Not recommended for diverse feature types

**Dense vs Sparse:**
- Dense format: Traditional columnar data
- Sparse format: Attribute-value pairs (text features, one-hot encoded)
- Choose based on data structure

**Computational Considerations:**
- Fit operation calculates statistics (fast)
- Scales well to large datasets
- Minimal memory overhead

### Best Practices

**1. Always Fit on Training Data Only**
- Calculate scaling statistics from training set
- Apply to all other datasets (validation, test, production)
- Prevents data leakage and ensures fair evaluation

**2. Choose Appropriate ScaleMethod**
- Default: MEAN (Z-score) for most ML applications
- RANGE for neural networks, image data
- MAXABS for sparse data
- Match method to algorithm requirements

**3. Handle Missing Values First**
- Impute or remove NULLs before scaling
- Use MissValue='OMIT' to exclude from statistics
- Document imputation strategy

**4. Consider Outliers**
- Detect and handle outliers before scaling
- MEAN and RANGE sensitive to outliers
- Consider robust scaling methods
- Use TD_OutlierFilterFit if needed

**5. Store FitTable with Model**
- Version control FitTable
- Deploy with trained model
- Document scaling method and parameters
- Enable reproducible predictions

**6. Validate Scaling Results**
- Check scaled feature distributions
- Verify mean≈0, std≈1 for MEAN method
- Test on sample data first
- Monitor for numerical issues

**7. Scale After Imputation**
- Impute missing values first
- Then apply scaling
- Order matters in preprocessing pipeline

**8. Don't Scale Target Variable**
- Typically only scale input features
- For regression, may scale target (but inverse-transform predictions)
- Classification targets never scaled

**9. Document Preprocessing Pipeline**
- Record all transformations
- Maintain transformation order
- Enable reproducibility
- Support model governance

**10. Test Different Methods**
- Compare model performance with different scaling
- Validate on holdout data
- Choose method based on empirical results
- Consider computational tradeoffs

### Related Functions
- **TD_ScaleTransform** - Applies scaling using FitTable (must be used after TD_ScaleFit)
- **TD_SimpleImputeFit** - Handle missing values before scaling
- **TD_SimpleImputeTransform** - Apply imputation
- **TD_OutlierFilterFit** - Remove outliers before scaling
- **TD_PolynomialFeaturesFit** - Often used after scaling

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Transform Functions
