# TD_RandomProjectionFit

### Function Name
**TD_RandomProjectionFit**

### Description
TD_RandomProjectionFit creates a random projection matrix that defines how to reduce high-dimensional data to a lower-dimensional space while approximately preserving pairwise distances between data points. This function generates the transformation specifications based on the Johnson-Lindenstrauss Lemma, which guarantees that distances are preserved within a specified tolerance (epsilon) when projecting to an appropriately sized lower-dimensional space.

Random projection is a powerful dimensionality reduction technique that offers computational advantages over methods like PCA or SVD. Unlike PCA which requires expensive eigenvalue decomposition, random projection uses a randomly generated matrix, making it extremely fast and scalable to very large datasets. The method is particularly effective for sparse high-dimensional data and provides theoretical guarantees on distance preservation.

The function supports two projection methods: GAUSSIAN (using normally distributed random values) and SPARSE (using sparse random matrices with mostly zero values for computational efficiency). The output FitTable contains the random projection matrix used by TD_RandomProjectionTransform to perform the actual dimensionality reduction.

### When the Function Would Be Used
- **Dimensionality Reduction**: Reduce feature space while preserving distances
- **Large-Scale ML**: Preprocess high-dimensional data for faster training
- **Sparse Data Processing**: Efficiently reduce dimensionality of sparse matrices
- **Nearest Neighbor Search**: Accelerate distance-based algorithms
- **Clustering Preprocessing**: Reduce dimensions before K-Means or DBSCAN
- **Text Analytics**: Reduce dimensionality of TF-IDF or word embedding vectors
- **Image Processing**: Compress high-dimensional image features
- **Anomaly Detection**: Reduce dimensions while preserving outlier structures
- **Visualization Preparation**: Preliminary reduction before t-SNE or UMAP
- **Computational Efficiency**: Speed up algorithms with lower-dimensional data

### Syntax

```sql
TD_RandomProjectionFit (
    ON { table | view | (query) } AS InputTable
    USING
    TargetColumns ({ 'target_column' | target_column_range }[,...])
    [ NumComponents (num_components) ]
    [ Epsilon (epsilon_value) ]
    [ ProjectionMethod ('GAUSSIAN' | 'SPARSE') ]
    [ Density (density_value) ]
    [ Seed (seed_value) ]
)
```

### Required Syntax Elements for TD_RandomProjectionFit

**ON clause**
- Accepts the InputTable clause containing numeric features
- Data used for dimension calculation, not for fitting

**TargetColumns**
- Specify numeric columns to be projected to lower dimensions
- Must be numeric data types
- Supports column range notation
- These columns will be reduced to NumComponents dimensions

### Optional Syntax Elements for TD_RandomProjectionFit

**NumComponents**
- Specify number of dimensions in reduced space
- Must be positive integer less than number of TargetColumns
- If specified, Epsilon is ignored
- If omitted, calculated from Epsilon using Johnson-Lindenstrauss formula
- Default: Calculated from Epsilon

**Epsilon**
- Specify distortion tolerance for distance preservation
- Valid range: 0 < epsilon < 1
- Smaller values = better distance preservation but higher dimensions
- Larger values = more aggressive reduction but more distortion
- Default: 0.1
- Ignored if NumComponents specified

**ProjectionMethod**
- Specify type of random matrix to generate
- Valid values: 'GAUSSIAN' or 'SPARSE'
- GAUSSIAN: Uses normally distributed random values (more accurate)
- SPARSE: Uses sparse random matrix (faster, lower memory)
- Default: 'GAUSSIAN'

**Density**
- Specify density of sparse random matrix
- Only applicable when ProjectionMethod='SPARSE'
- Valid range: 0 < density ≤ 1
- Lower values = sparser matrix = faster computation
- Recommended: 1/√(number of features)
- Default: Auto-calculated

**Seed**
- Specify random seed for reproducible projections
- Positive integer value
- Use same seed to regenerate identical projection matrix
- Different seeds produce different (but equally valid) projections
- Default: Random seed

### Input Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | Numeric types (INTEGER, BIGINT, FLOAT, DOUBLE PRECISION, DECIMAL, NUMERIC) | High-dimensional features to be reduced |

### Output Table Schema (FitTable)

The output is a projection matrix specification table:

| Column | Data Type | Description |
|--------|-----------|-------------|
| component_id | INTEGER | Index of the output component dimension |
| target_column | VARCHAR | Name of input feature column |
| projection_weight | DOUBLE PRECISION | Random weight for projection matrix |

The FitTable represents the random projection matrix where each row defines one element of the matrix mapping input features to output components.

### Code Examples

**Input Data: high_dimensional_data**
```
id  feature1  feature2  feature3  feature4  feature5  feature6  feature7  feature8  feature9  feature10
1   2.5       1.3       3.7       0.5       2.1       4.2       1.8       3.3       0.9       2.7
2   1.2       3.4       0.8       2.9       1.5       3.1       2.3       1.7       3.8       1.1
3   3.8       2.1       1.4       3.5       0.7       1.9       3.2       2.6       1.3       3.4
```

**Example 1: Basic Random Projection (Auto NumComponents)**
```sql
-- Create random projection fit using epsilon to determine dimensions
CREATE TABLE random_proj_fit AS (
    SELECT * FROM TD_RandomProjectionFit (
        ON high_dimensional_data AS InputTable
        USING
        TargetColumns('feature1', 'feature2', 'feature3', 'feature4', 'feature5',
                      'feature6', 'feature7', 'feature8', 'feature9', 'feature10')
        Epsilon(0.1)
        ProjectionMethod('GAUSSIAN')
        Seed(42)
    ) AS dt
) WITH DATA;

-- Check resulting dimensions
SELECT DISTINCT component_id FROM random_proj_fit ORDER BY component_id;
```

**Output:** NumComponents automatically calculated to preserve distances within 10% tolerance

**Example 2: Specify Exact Number of Components**
```sql
-- Reduce 100 dimensions to exactly 20 dimensions
CREATE TABLE proj_fit_20d AS (
    SELECT * FROM TD_RandomProjectionFit (
        ON text_features AS InputTable
        USING
        TargetColumns('[1:100]')  -- All 100 feature columns
        NumComponents(20)         -- Reduce to 20 dimensions
        ProjectionMethod('GAUSSIAN')
        Seed(12345)
    ) AS dt
) WITH DATA;
```

**Example 3: Sparse Random Projection**
```sql
-- Use sparse projection for computational efficiency
CREATE TABLE sparse_proj_fit AS (
    SELECT * FROM TD_RandomProjectionFit (
        ON sparse_text_data AS InputTable
        USING
        TargetColumns('[1:5000]')  -- 5000 sparse features
        NumComponents(100)
        ProjectionMethod('SPARSE')
        Density(0.01)  -- Very sparse matrix (1% non-zero)
        Seed(999)
    ) AS dt
) WITH DATA;
```

**Example 4: Different Epsilon Values**
```sql
-- Conservative projection (more dimensions retained)
CREATE TABLE proj_conservative AS (
    SELECT * FROM TD_RandomProjectionFit (
        ON customer_features AS InputTable
        USING
        TargetColumns('[2:50]')
        Epsilon(0.05)  -- Small epsilon = better preservation = more dimensions
        ProjectionMethod('GAUSSIAN')
    ) AS dt
) WITH DATA;

-- Aggressive projection (fewer dimensions)
CREATE TABLE proj_aggressive AS (
    SELECT * FROM TD_RandomProjectionFit (
        ON customer_features AS InputTable
        USING
        TargetColumns('[2:50]')
        Epsilon(0.3)  -- Large epsilon = more distortion = fewer dimensions
        ProjectionMethod('GAUSSIAN')
    ) AS dt
) WITH DATA;
```

**Example 5: Text Feature Reduction**
```sql
-- Reduce TF-IDF feature vectors for faster processing
CREATE TABLE tfidf_proj_fit AS (
    SELECT * FROM TD_RandomProjectionFit (
        ON tfidf_vectors AS InputTable
        USING
        TargetColumns('[3:1000]')  -- 998 TF-IDF features
        NumComponents(50)
        ProjectionMethod('SPARSE')
        Seed(777)
    ) AS dt
) WITH DATA;

-- Use for document clustering or classification
```

**Example 6: Image Feature Reduction**
```sql
-- Reduce high-dimensional image features
CREATE TABLE image_proj_fit AS (
    SELECT * FROM TD_RandomProjectionFit (
        ON image_features AS InputTable
        USING
        TargetColumns('[5:2053]')  -- 2048 image feature dimensions
        NumComponents(128)
        ProjectionMethod('GAUSSIAN')
        Seed(2024)
    ) AS dt
) WITH DATA;
```

**Example 7: Reproducible Projections with Seed**
```sql
-- Create projection with specific seed for reproducibility
CREATE TABLE proj_reproducible AS (
    SELECT * FROM TD_RandomProjectionFit (
        ON training_data AS InputTable
        USING
        TargetColumns('[1:200]')
        NumComponents(30)
        ProjectionMethod('GAUSSIAN')
        Seed(123)  -- Same seed produces same projection matrix
    ) AS dt
) WITH DATA;

-- Later, use same seed to regenerate identical projection
-- This ensures train/test consistency
```

**Example 8: Nearest Neighbor Preprocessing**
```sql
-- Reduce dimensions before k-NN search for speed
CREATE TABLE knn_proj_fit AS (
    SELECT * FROM TD_RandomProjectionFit (
        ON product_embeddings AS InputTable
        USING
        TargetColumns('[2:300]')  -- 299 embedding dimensions
        Epsilon(0.15)  -- Acceptable distortion for approximate NN
        ProjectionMethod('SPARSE')
    ) AS dt
) WITH DATA;

-- Apply to enable fast approximate nearest neighbor search
```

**Example 9: Clustering Preprocessing**
```sql
-- Reduce dimensions before K-Means clustering
CREATE TABLE cluster_proj_fit AS (
    SELECT * FROM TD_RandomProjectionFit (
        ON customer_behavioral_features AS InputTable
        USING
        TargetColumns('[5:104]')  -- 100 behavioral features
        NumComponents(25)
        ProjectionMethod('GAUSSIAN')
        Seed(555)
    ) AS dt
) WITH DATA;

-- Transform data, then apply TD_KMeans on reduced dimensions
```

**Example 10: Calculating Minimum Components from Epsilon**
```sql
-- Use TD_RandomProjectionMinComponents to calculate required dimensions
SELECT * FROM TD_RandomProjectionMinComponents (
    ON high_dimensional_data AS InputTable
    USING
    TargetColumns('[1:500]')
    Epsilon(0.1)
) AS dt;

-- Output: minimum_components = 75 (example)

-- Then create fit with calculated components
CREATE TABLE proj_fit_calculated AS (
    SELECT * FROM TD_RandomProjectionFit (
        ON high_dimensional_data AS InputTable
        USING
        TargetColumns('[1:500]')
        NumComponents(75)  -- Use calculated minimum
        ProjectionMethod('GAUSSIAN')
        Seed(888)
    ) AS dt
) WITH DATA;
```

### Johnson-Lindenstrauss Lemma

**Theoretical Foundation:**

The Johnson-Lindenstrauss Lemma guarantees that a set of n points in high-dimensional space can be embedded into a k-dimensional space where k is logarithmic in n, while approximately preserving pairwise distances.

**Formula for Minimum Dimensions:**

k ≥ 4 × ln(n) / (ε² / 2 - ε³ / 3)

Where:
- k = minimum number of target dimensions (NumComponents)
- n = number of data points
- ε = epsilon (distortion tolerance)

**Distance Preservation:**

For any two points u and v in original space, their distance in projected space satisfies:

(1 - ε) × ||u - v||² ≤ ||f(u) - f(v)||² ≤ (1 + ε) × ||u - v||²

Where f is the random projection transformation.

**Example:**
- 1000 data points, ε = 0.1
- Minimum dimensions ≈ 4 × ln(1000) / (0.01 - 0.00033) ≈ 2,857
- Distances preserved within ±10%

### Use Cases and Applications

**1. Large-Scale Machine Learning**
- Reduce feature space for faster model training
- Preprocessing for gradient boosting and neural networks
- Enable training on memory-constrained systems
- Accelerate hyperparameter tuning

**2. Text and NLP Analytics**
- Reduce TF-IDF vector dimensionality
- Compress word embeddings for efficiency
- Speed up document similarity computations
- Enable scalable topic modeling

**3. Image and Computer Vision**
- Reduce CNN feature dimensions
- Compress image embeddings
- Speed up image similarity search
- Enable real-time image processing

**4. Recommender Systems**
- Reduce user-item interaction dimensions
- Compress latent factor representations
- Speed up collaborative filtering
- Enable scalable matrix factorization

**5. Nearest Neighbor Search**
- Accelerate k-NN search with approximate distances
- Enable fast similarity queries
- Improve computational efficiency
- Maintain acceptable accuracy with distance preservation

**6. Clustering Applications**
- Preprocess high-dimensional data for K-Means
- Speed up hierarchical clustering
- Enable DBSCAN on large feature sets
- Improve clustering scalability

**7. Anomaly Detection**
- Reduce dimensions while preserving outlier structures
- Speed up distance-based anomaly detection
- Enable real-time fraud detection
- Maintain detection accuracy

**8. Time Series Analysis**
- Reduce dimensionality of multivariate time series
- Compress sensor data streams
- Speed up similarity search in time series
- Enable scalable forecasting

**9. Bioinformatics and Genomics**
- Reduce gene expression data dimensions
- Compress protein sequence features
- Speed up sequence similarity search
- Enable large-scale genomic analysis

**10. Visualization Preprocessing**
- Initial reduction before t-SNE or UMAP
- Speed up 2D/3D visualization generation
- Enable visualization of very large datasets
- Maintain cluster structures

### Important Notes

**Distance Preservation Guarantee:**
- Random projection preserves pairwise distances with high probability
- Guarantee based on Johnson-Lindenstrauss Lemma
- Distance distortion bounded by epsilon parameter
- Works for Euclidean distances

**Epsilon vs NumComponents:**
- Specify either Epsilon OR NumComponents, not both
- If NumComponents specified, Epsilon ignored
- Smaller Epsilon → more components required → better preservation
- Use Epsilon when unsure of target dimensionality

**Projection Method Selection:**
- GAUSSIAN: More accurate, higher memory usage
- SPARSE: Faster computation, lower memory, slightly less accurate
- Use SPARSE for very high dimensions (>1000)
- Use GAUSSIAN for moderate dimensions (<1000)

**Computational Complexity:**
- Fit operation is fast (generates random matrix)
- No expensive eigenvalue decomposition like PCA
- Sparse projection significantly faster than Gaussian
- Scales well to very large feature spaces

**Seed for Reproducibility:**
- Same seed produces identical projection matrix
- Critical for train/test consistency
- Store seed with model artifacts
- Different seeds produce different (but valid) projections

**Sparse Matrix Density:**
- Default density ≈ 1/√d where d is number of features
- Lower density = faster but slightly less accurate
- Very sparse matrices (density < 0.01) for extreme dimensions
- Balance speed vs accuracy based on application

**NULL Handling:**
- NULL values not supported in TargetColumns
- Remove or impute NULLs before projection
- Use TD_SimpleImputeFit/Transform for imputation
- NULLs will cause errors during transformation

**Comparison to PCA:**
- Faster than PCA (no eigenvalue decomposition)
- No variance maximization (purely random)
- Distance preservation instead of variance preservation
- Better for very large datasets
- PCA better for interpretability

### Best Practices

**1. Choose Appropriate Epsilon**
- Start with ε = 0.1 (10% distortion tolerance)
- Smaller ε for critical applications (e.g., 0.05)
- Larger ε for aggressive reduction (e.g., 0.2-0.3)
- Validate on holdout data

**2. Use Sparse Projection for Large Dimensions**
- SPARSE method for features > 1000
- Significantly faster with minimal accuracy loss
- Lower memory footprint
- Adjust density based on sparsity

**3. Always Set Seed for Production**
- Use consistent seed across train/validation/test
- Store seed with model version
- Enable reproducible results
- Document seed value

**4. Validate Distance Preservation**
- Sample data points before/after projection
- Calculate distance preservation ratio
- Verify epsilon tolerance met
- Monitor for edge cases

**5. Preprocessing Before Projection**
- Impute missing values first
- Consider scaling features (though not required)
- Remove constant or near-constant features
- Handle outliers appropriately

**6. Calculate Minimum Components**
- Use TD_RandomProjectionMinComponents to determine k
- Provides theoretical minimum for given epsilon
- Balance theory with practical considerations
- Validate with actual data

**7. Store FitTable with Model**
- Save projection matrix for production use
- Version control FitTable
- Document projection parameters
- Enable consistent transformation

**8. Monitor Performance**
- Track downstream model accuracy
- Compare to original high-dimensional model
- Measure computation time savings
- Balance speed vs accuracy

**9. Combine with Other Techniques**
- Use after feature selection
- Combine with PCA for interpretability
- Cascade with other dimensionality reduction
- Apply before clustering or classification

**10. Handle Sparse Input Data**
- Random projection works well with sparse features
- Use SPARSE projection method for sparse input
- Maintains sparsity benefits
- Ideal for text and categorical data

### Related Functions
- **TD_RandomProjectionTransform** - Applies random projection using FitTable (must be used after TD_RandomProjectionFit)
- **TD_RandomProjectionMinComponents** - Calculates minimum components needed for given epsilon
- **TD_PCA** - Alternative dimensionality reduction with variance maximization
- **TD_SVD** - Singular Value Decomposition for dimensionality reduction
- **TD_ScaleFit** - Feature scaling (optional preprocessing)

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf
- Johnson-Lindenstrauss Lemma: Dasgupta & Gupta (1999)

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Transform Functions
