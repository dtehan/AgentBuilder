# TD_RandomProjectionTransform

### Function Name
**TD_RandomProjectionTransform**

### Description
TD_RandomProjectionTransform applies dimensionality reduction using the random projection matrix created by TD_RandomProjectionFit. This function performs the actual transformation of high-dimensional data to a lower-dimensional space by multiplying the input feature vectors with the random projection matrix, effectively reducing the number of dimensions while approximately preserving pairwise distances according to the Johnson-Lindenstrauss guarantee.

This is the execution component of the random projection pipeline. After TD_RandomProjectionFit generates the random projection matrix specifications (the FitTable), TD_RandomProjectionTransform applies this matrix to transform data from the original high-dimensional feature space to the reduced-dimensional space. The transformation is a linear operation that combines the original features using random weights to create new, compressed feature representations.

The transformation is deterministic given a FitTable, ensuring consistent dimensionality reduction across training, validation, test, and production datasets. This consistency is essential for machine learning pipelines where all data splits must undergo identical transformations to maintain model validity and prevent data leakage.

### When the Function Would Be Used
- **Apply Dimensionality Reduction**: Execute reduction to lower-dimensional space
- **ML Pipeline Execution**: Transform training and test data consistently
- **Production Scoring**: Reduce dimensions of incoming data in real-time
- **Computational Acceleration**: Speed up downstream algorithms on reduced data
- **Memory Optimization**: Reduce storage requirements for high-dimensional features
- **Distance Preservation**: Transform while maintaining approximate pairwise distances
- **Clustering Preprocessing**: Reduce dimensions before K-Means or DBSCAN
- **Nearest Neighbor Search**: Enable fast approximate similarity search
- **Visualization Preparation**: Initial reduction before t-SNE or UMAP
- **Consistent Feature Engineering**: Ensure identical transformations across datasets

### Syntax

```sql
TD_RandomProjectionTransform (
    ON { table | view | (query) } AS InputTable [ PARTITION BY ANY ]
    ON { table | view | (query) } AS FitTable AS FitTableAlias DIMENSION
    USING
    [ Accumulate ({'accumulate_column' | 'accumulate_column_range'}[,...]) ]
)
```

### Required Syntax Elements for TD_RandomProjectionTransform

**ON clause (InputTable)**
- Accepts the InputTable clause containing high-dimensional data to transform
- Must have same columns as data used for TD_RandomProjectionFit
- PARTITION BY ANY recommended for parallel processing

**ON clause (FitTable DIMENSION)**
- Accepts the FitTable clause (output from TD_RandomProjectionFit)
- Contains random projection matrix specifications
- DIMENSION keyword required

### Optional Syntax Elements for TD_RandomProjectionTransform

**Accumulate**
- Specify input table column names to copy to the output table
- Useful for preserving identifiers, keys, and metadata
- Supports column range notation
- Typically includes ID columns and target variables

### Input Table Schema

**InputTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | Numeric types (INTEGER, BIGINT, FLOAT, DOUBLE PRECISION, DECIMAL, NUMERIC) | High-dimensional features specified in TD_RandomProjectionFit TargetColumns |
| accumulate_column | ANY | [Optional] Columns to preserve in output table |

**FitTable Schema:**

See TD_RandomProjectionFit Output table schema. This is the projection matrix created by TD_RandomProjectionFit function.

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| accumulate_column | Same as InputTable | Columns specified in Accumulate parameter |
| component_1 | DOUBLE PRECISION | First projected dimension |
| component_2 | DOUBLE PRECISION | Second projected dimension |
| ... | DOUBLE PRECISION | Additional projected dimensions |
| component_k | DOUBLE PRECISION | k-th projected dimension (where k = NumComponents from Fit) |

The number of component columns equals the NumComponents specified in TD_RandomProjectionFit.

### Code Examples

**Input Data: high_dimensional_data**
```
id  feat1  feat2  feat3  feat4  feat5  feat6  feat7  feat8  feat9  feat10
1   2.5    1.3    3.7    0.5    2.1    4.2    1.8    3.3    0.9    2.7
2   1.2    3.4    0.8    2.9    1.5    3.1    2.3    1.7    3.8    1.1
3   3.8    2.1    1.4    3.5    0.7    1.9    3.2    2.6    1.3    3.4
```

**FitTable: random_proj_fit** (created by TD_RandomProjectionFit)
```
-- Created with: NumComponents(3), TargetColumns('[1:10]'), ProjectionMethod('GAUSSIAN')
-- Reduces 10 dimensions to 3 dimensions
```

**Example 1: Basic Random Projection Transformation**
```sql
-- Step 1: Create fit table (already done)
CREATE TABLE random_proj_fit AS (
    SELECT * FROM TD_RandomProjectionFit (
        ON high_dimensional_data AS InputTable
        USING
        TargetColumns('[2:11]')  -- 10 features
        NumComponents(3)
        ProjectionMethod('GAUSSIAN')
        Seed(42)
    ) AS dt
) WITH DATA;

-- Step 2: Apply transformation
SELECT * FROM TD_RandomProjectionTransform (
    ON high_dimensional_data AS InputTable
    ON random_proj_fit AS FitTable DIMENSION
    USING
    Accumulate('id')
) AS dt
ORDER BY id;
```

**Output:**
```
id  component_1  component_2  component_3
1   5.234        -1.892       3.456
2   4.123        2.567        -0.891
3   6.789        0.234        2.134
```

**Transformation:** 10 dimensions → 3 dimensions

**Example 2: Transform Training Data**
```sql
-- Transform training set with random projection
CREATE TABLE training_reduced AS (
    SELECT * FROM TD_RandomProjectionTransform (
        ON training_data AS InputTable
        ON proj_fit AS FitTable DIMENSION
        USING
        Accumulate('customer_id', 'target')
    ) AS dt
) WITH DATA;

-- Now ready for faster model training on reduced dimensions
```

**Example 3: Transform Test Data with Same FitTable**
```sql
-- Apply same random projection to test set
CREATE TABLE test_reduced AS (
    SELECT * FROM TD_RandomProjectionTransform (
        ON test_data AS InputTable
        ON proj_fit AS FitTable DIMENSION  -- Same FitTable as training
        USING
        Accumulate('customer_id')
    ) AS dt
) WITH DATA;

-- Ensures consistent transformation across train/test
```

**Example 4: Text Feature Dimensionality Reduction**
```sql
-- Create sparse projection fit for TF-IDF vectors
CREATE TABLE tfidf_proj_fit AS (
    SELECT * FROM TD_RandomProjectionFit (
        ON tfidf_vectors AS InputTable
        USING
        TargetColumns('[3:1002]')  -- 1000 TF-IDF features
        NumComponents(50)
        ProjectionMethod('SPARSE')
        Density(0.01)
        Seed(777)
    ) AS dt
) WITH DATA;

-- Transform to 50 dimensions for faster processing
SELECT * FROM TD_RandomProjectionTransform (
    ON tfidf_vectors AS InputTable
    ON tfidf_proj_fit AS FitTable DIMENSION
    USING
    Accumulate('document_id', 'category')
) AS dt
ORDER BY document_id;
```

**Result:** 1000 TF-IDF dimensions → 50 projected dimensions

**Example 5: Image Feature Compression**
```sql
-- Reduce image embeddings from 2048 to 128 dimensions
CREATE TABLE image_proj_fit AS (
    SELECT * FROM TD_RandomProjectionFit (
        ON image_features AS InputTable
        USING
        TargetColumns('[3:2050]')  -- 2048 image features
        NumComponents(128)
        ProjectionMethod('GAUSSIAN')
        Seed(2024)
    ) AS dt
) WITH DATA;

-- Apply transformation
CREATE TABLE images_reduced AS (
    SELECT * FROM TD_RandomProjectionTransform (
        ON image_features AS InputTable
        ON image_proj_fit AS FitTable DIMENSION
        USING
        Accumulate('image_id', 'image_path')
    ) AS dt
) WITH DATA;
```

**Example 6: Clustering Pipeline**
```sql
-- Step 1: Random projection (already done - proj_fit created)
-- Step 2: Transform data
CREATE TABLE data_reduced AS (
    SELECT * FROM TD_RandomProjectionTransform (
        ON customer_features AS InputTable
        ON proj_fit AS FitTable DIMENSION
        USING
        Accumulate('customer_id')
    ) AS dt
) WITH DATA;

-- Step 3: K-Means clustering on reduced dimensions
CREATE TABLE clusters AS (
    SELECT * FROM TD_KMeans (
        ON data_reduced AS InputTable
        USING
        TargetColumns('[2:]')  -- All component columns
        NumClusters(5)
        Seed(123)
    ) AS dt
) WITH DATA;
```

**Example 7: Nearest Neighbor Preprocessing**
```sql
-- Reduce embeddings for fast approximate k-NN
CREATE TABLE embeddings_reduced AS (
    SELECT * FROM TD_RandomProjectionTransform (
        ON product_embeddings AS InputTable
        ON knn_proj_fit AS FitTable DIMENSION
        USING
        Accumulate('product_id', 'product_name')
    ) AS dt
) WITH DATA;

-- Use reduced embeddings for similarity search
-- 10-100x faster than original high-dimensional search
```

**Example 8: Production Scoring**
```sql
-- Score new customers using model trained on reduced dimensions
-- Step 1: Transform incoming data with production FitTable
CREATE TABLE new_customers_reduced AS (
    SELECT * FROM TD_RandomProjectionTransform (
        ON new_customers AS InputTable
        ON proj_fit AS FitTable DIMENSION  -- Use production FitTable
        USING
        Accumulate('customer_id', 'customer_name')
    ) AS dt
) WITH DATA;

-- Step 2: Apply trained model for predictions
SELECT * FROM TD_GLMPredict (
    ON new_customers_reduced AS InputTable
    ON trained_model AS ModelTable DIMENSION
    USING
    IDColumn('customer_id')
    Accumulate('customer_name')
) AS dt;
```

**Example 9: Visualization Preparation**
```sql
-- Initial reduction before t-SNE (speeds up t-SNE significantly)
-- Step 1: Reduce 5000 dims to 50 dims with random projection
CREATE TABLE data_prereduced AS (
    SELECT * FROM TD_RandomProjectionTransform (
        ON high_dim_data AS InputTable
        ON proj_fit_50d AS FitTable DIMENSION
        USING
        Accumulate('id', 'label')
    ) AS dt
) WITH DATA;

-- Step 2: Apply t-SNE on reduced 50-dimensional data (much faster)
-- t-SNE typically works best with 50-100 input dimensions
```

**Example 10: Complete ML Pipeline with Validation**
```sql
-- End-to-end random projection pipeline
-- Step 1: Create random projection fit on training data only
CREATE TABLE proj_fit AS (
    SELECT * FROM TD_RandomProjectionFit (
        ON training_data AS InputTable
        USING
        TargetColumns('[3:503]')  -- 500 features
        NumComponents(75)
        ProjectionMethod('GAUSSIAN')
        Seed(12345)
    ) AS dt
) WITH DATA;

-- Step 2: Transform training data
CREATE TABLE train_reduced AS (
    SELECT * FROM TD_RandomProjectionTransform (
        ON training_data AS InputTable
        ON proj_fit AS FitTable DIMENSION
        USING
        Accumulate('id', 'target')
    ) AS dt
) WITH DATA;

-- Step 3: Transform validation data (same FitTable)
CREATE TABLE validation_reduced AS (
    SELECT * FROM TD_RandomProjectionTransform (
        ON validation_data AS InputTable
        ON proj_fit AS FitTable DIMENSION
        USING
        Accumulate('id', 'target')
    ) AS dt
) WITH DATA;

-- Step 4: Transform test data (same FitTable)
CREATE TABLE test_reduced AS (
    SELECT * FROM TD_RandomProjectionTransform (
        ON test_data AS InputTable
        ON proj_fit AS FitTable DIMENSION
        USING
        Accumulate('id', 'target')
    ) AS dt
) WITH DATA;

-- Step 5: Train model on train_reduced (75 dimensions instead of 500)
-- Step 6: Validate on validation_reduced
-- Step 7: Final evaluation on test_reduced
```

### Random Projection Transformation Process

**Before Transformation (10 dimensions):**
```
id  f1   f2   f3   f4   f5   f6   f7   f8   f9   f10
1   2.5  1.3  3.7  0.5  2.1  4.2  1.8  3.3  0.9  2.7
2   1.2  3.4  0.8  2.9  1.5  3.1  2.3  1.7  3.8  1.1
```

**After Transformation (3 dimensions):**
```
id  component_1  component_2  component_3
1   5.234        -1.892       3.456
2   4.123        2.567        -0.891
```

**Key Transformation Characteristics:**
- Original features combined via weighted sum
- Weights determined by random projection matrix
- Number of output dimensions = NumComponents from Fit
- Distances approximately preserved within epsilon tolerance
- Linear transformation (fast computation)

**Mathematical Operation:**

For each row: **y** = **R** × **x**

Where:
- **x** = original high-dimensional vector (d dimensions)
- **R** = random projection matrix (k × d matrix from FitTable)
- **y** = projected low-dimensional vector (k dimensions)
- k << d (significant dimensionality reduction)

### Use Cases and Applications

**1. Large-Scale Machine Learning**
- Speed up model training on high-dimensional data
- Reduce memory requirements for gradient boosting
- Enable training on larger datasets
- Accelerate hyperparameter tuning

**2. Text and NLP Analytics**
- Reduce TF-IDF vector dimensionality for faster processing
- Compress word embeddings (e.g., 300d → 50d)
- Enable scalable document similarity computations
- Speed up text classification pipelines

**3. Image and Computer Vision**
- Compress CNN features (e.g., 2048d → 128d)
- Reduce image embeddings for similarity search
- Enable real-time image processing
- Speed up image retrieval systems

**4. Recommender Systems**
- Reduce user-item interaction dimensions
- Compress latent factor representations
- Speed up collaborative filtering
- Enable real-time recommendations

**5. Nearest Neighbor and Similarity Search**
- Accelerate approximate k-NN search
- Enable fast similarity queries at scale
- Reduce index size for search systems
- Maintain acceptable accuracy with distance preservation

**6. Clustering at Scale**
- Preprocess data for K-Means clustering
- Speed up hierarchical clustering
- Enable DBSCAN on large feature sets
- Improve clustering scalability

**7. Anomaly Detection**
- Reduce dimensions while preserving outlier structures
- Speed up distance-based anomaly detection
- Enable real-time fraud detection systems
- Process high-dimensional sensor data streams

**8. Time Series Analysis**
- Reduce multivariate time series dimensionality
- Compress sensor data streams
- Speed up time series similarity search
- Enable scalable forecasting

**9. Bioinformatics and Genomics**
- Reduce gene expression data dimensions
- Compress protein sequence features
- Speed up genomic sequence similarity search
- Enable large-scale population genetics analysis

**10. Real-Time Processing**
- Reduce feature space for low-latency predictions
- Enable real-time scoring with lower computational cost
- Stream processing of high-dimensional data
- Edge computing on resource-constrained devices

### Important Notes

**Train-Test Consistency:**
- Always create FitTable using only training data
- Apply same FitTable to training, validation, and test sets
- Never fit on test data to prevent data leakage
- Store FitTable with model artifacts for production

**Output Dimensionality:**
- Number of component columns = NumComponents from FitTable
- Column names: component_1, component_2, ..., component_k
- All components are DOUBLE PRECISION type
- Components are linear combinations of original features

**Distance Preservation:**
- Pairwise distances approximately preserved
- Guarantee based on Johnson-Lindenstrauss Lemma
- Distortion bounded by epsilon from Fit step
- Works for Euclidean distances

**NULL Handling:**
- NULL values in input features result in NULL components
- If any input feature is NULL, all output components may be NULL
- Consider imputation before transformation
- Use TD_SimpleImputeFit/Transform for missing values

**Computational Performance:**
- Transformation is matrix multiplication (fast operation)
- SPARSE projection method faster than GAUSSIAN
- Use PARTITION BY ANY for parallel processing
- Scales well to very large datasets

**Data Type Requirements:**
- Input features must be numeric types
- Non-numeric columns must be accumulated (not transformed)
- Output components always DOUBLE PRECISION
- Accumulate columns preserve original types

**Reproducibility:**
- Same FitTable produces identical transformation
- Critical for production consistency
- Seed in Fit ensures reproducibility
- Version control FitTable with models

**Comparison to PCA Transform:**
- Faster than PCA transformation
- No variance explained (purely random)
- Distance preservation instead of variance preservation
- Better computational efficiency for very large data
- PCA better for interpretability

### Best Practices

**1. Consistent Transformation Across Datasets**
- Create FitTable on training data only
- Apply to all datasets (train, validation, test, production)
- Store FitTable with model version control
- Document projection parameters

**2. Preprocessing Before Transformation**
- Impute missing values first (TD_SimpleImputeFit/Transform)
- Consider scaling features (though not required)
- Remove constant or near-constant features
- Handle outliers appropriately

**3. Validate Distance Preservation**
- Sample pairs of points before/after projection
- Calculate distance preservation ratio
- Verify epsilon tolerance met empirically
- Compare to theoretical guarantee

**4. Monitor Downstream Performance**
- Track model accuracy on reduced dimensions
- Compare to original high-dimensional model
- Measure computation time savings
- Balance speed vs accuracy trade-offs

**5. Production Deployment**
- Store FitTable with trained model
- Validate FitTable compatibility before scoring
- Implement input validation for production data
- Monitor for numerical issues

**6. Optimize for Use Case**
- Use SPARSE method for very high dimensions
- Adjust epsilon based on accuracy requirements
- Consider computational constraints
- Test multiple configurations

**7. Combine with Other Techniques**
- Use after feature selection for better results
- Combine with scaling for normalized inputs
- Cascade with other dimensionality reduction
- Apply before specific algorithms (clustering, k-NN)

**8. Handle Large Datasets Efficiently**
- Use PARTITION BY ANY for parallel processing
- Consider incremental transformation for very large data
- Monitor memory usage
- Optimize query performance

**9. Validate Transformation Quality**
- Test on sample data first
- Verify output dimensionality matches expectations
- Check for numerical overflow or underflow
- Compare train/test feature distributions

**10. Documentation and Governance**
- Document transformation parameters
- Record NumComponents, epsilon, seed, method
- Maintain transformation specifications
- Enable reproducibility and auditing

### Related Functions
- **TD_RandomProjectionFit** - Creates random projection matrix (must be run before TD_RandomProjectionTransform)
- **TD_RandomProjectionMinComponents** - Calculates minimum components needed
- **TD_KMeans** - Clustering algorithm often used after dimensionality reduction
- **TD_PCA** - Alternative dimensionality reduction method
- **TD_ScaleFit** - Feature scaling (optional preprocessing)

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf
- Johnson-Lindenstrauss Lemma: Dasgupta & Gupta (1999)

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Transform Functions
