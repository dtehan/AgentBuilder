# TD_VectorDistance

### Function Name
**TD_VectorDistance**

### Description
TD_VectorDistance computes pairwise distance or similarity measurements between target vectors and reference vectors using multiple distance metrics including Euclidean, Manhattan, Cosine Similarity, Chebyshev, and Minkowski distances. This utility function enables efficient similarity comparisons across large vector datasets, supporting applications from nearest neighbor search to recommendation systems. By calculating how close or far apart vectors are in multi-dimensional feature space, TD_VectorDistance provides the mathematical foundation for clustering validation, similarity-based retrieval, anomaly detection, and finding similar items based on their feature representations.

The function accepts two input tables - a target table containing vectors to compare and a reference table containing vectors to compare against - and computes the specified distance metric between every target vector and every reference vector (or a subset based on TopK). Multiple distance metrics accommodate different data characteristics and use cases: Euclidean distance measures straight-line geometric distance (ideal for continuous features), Manhattan distance computes city-block distance (robust to outliers), Cosine similarity measures angular similarity (perfect for text and high-dimensional sparse data where magnitude is less important than direction), Chebyshev distance measures maximum difference across dimensions, and Minkowski distance generalizes both Euclidean and Manhattan as special cases.

TD_VectorDistance is highly versatile, supporting both dense and sparse vector representations, enabling TopK nearest neighbor retrieval to limit output size, and handling large-scale pairwise comparisons efficiently through parallel processing. The function integrates seamlessly into ML pipelines for tasks like finding similar customers, products, or documents, validating cluster quality by measuring intra-cluster and inter-cluster distances, implementing K-Nearest Neighbors algorithms manually, building recommendation systems based on item or user similarity, and detecting anomalies by identifying points far from reference distributions. Whether measuring similarity for collaborative filtering, evaluating embedding quality, or implementing custom distance-based algorithms, TD_VectorDistance provides the flexible distance computation engine needed for diverse analytical applications.

### When the Function Would Be Used
- **Similarity Search**: Find most similar items, customers, products, or documents
- **Nearest Neighbor Retrieval**: Identify K nearest neighbors for recommendations or classification
- **Recommendation Systems**: Recommend similar products based on feature similarity
- **Clustering Validation**: Measure intra-cluster compactness and inter-cluster separation
- **Anomaly Detection**: Identify outliers based on distance from normal reference points
- **Duplicate Detection**: Find near-duplicate records based on feature similarity
- **Customer Segmentation**: Group similar customers based on behavioral features
- **Product Matching**: Match products across catalogs based on feature similarity
- **Document Similarity**: Find similar documents for search or organization
- **Image Similarity**: Compare images based on feature vector embeddings
- **Fraud Detection**: Identify transactions similar to known fraud patterns
- **Content-Based Filtering**: Recommend items with similar attributes
- **Collaborative Filtering**: Find users/items with similar rating patterns
- **Embedding Evaluation**: Measure quality of learned vector representations
- **Query Expansion**: Find related search terms based on embedding similarity
- **Entity Resolution**: Match and merge similar records across databases
- **Time Series Similarity**: Compare time series based on feature vectors
- **Social Network Analysis**: Identify users with similar connection patterns
- **Market Basket Analysis**: Find products frequently bought together
- **Biometric Matching**: Match fingerprints, faces, or voice patterns
- **Genomic Similarity**: Compare DNA/protein sequences based on features
- **Chemical Similarity**: Find similar chemical compounds for drug discovery
- **Geospatial Proximity**: Measure distance between locations in feature space
- **Custom KNN Implementation**: Build manual K-Nearest Neighbors algorithms

### Syntax

```sql
TD_VectorDistance (
    ON { table | view | (query) } AS TargetTable PARTITION BY target_id_column
    ON { table | view | (query) } AS ReferenceTable DIMENSION
    USING
    TargetIDColumn ('target_id_column')
    ReferenceIDColumn ('reference_id_column')
    TargetFeatures ({ 'target_feature_column' | target_feature_column_range }[,...])
    ReferenceFeatures ({ 'reference_feature_column' | reference_feature_column_range }[,...])
    [ DistanceMeasure ({ 'EUCLIDEAN' | 'MANHATTAN' | 'COSINE' | 'CHEBYSHEV' | 'MINKOWSKI' }) ]
    [ MinkowskiPower (power_value) ]
    [ TopK (k_value) ]
    [ Accumulate ({ 'accumulate_column' | accumulate_column_range }[,...]) ]
) AS alias
```

### Required Syntax Elements for TD_VectorDistance

**ON clause (TargetTable)**
- Table containing target vectors to compare
- PARTITION BY target ID column for parallel processing
- Each row represents one target vector

**ON clause (ReferenceTable)**
- Table containing reference vectors to compare against
- DIMENSION: entire reference table copied to each AMP for distance computation
- Each row represents one reference vector

**TargetIDColumn**
- Column in TargetTable uniquely identifying each target vector
- Used to identify which target vector produced each distance result
- Any data type (INTEGER, VARCHAR, etc.)

**ReferenceIDColumn**
- Column in ReferenceTable uniquely identifying each reference vector
- Used to identify which reference vector each distance corresponds to
- Any data type (INTEGER, VARCHAR, etc.)

**TargetFeatures**
- Feature columns in TargetTable forming target vectors
- Must be numeric data types (INTEGER, DOUBLE PRECISION, etc.)
- Supports column range notation ('[1:10]')
- Number of features must match ReferenceFeatures

**ReferenceFeatures**
- Feature columns in ReferenceTable forming reference vectors
- Must be numeric data types
- Supports column range notation
- Must have same number of columns as TargetFeatures

### Optional Syntax Elements for TD_VectorDistance

**DistanceMeasure**
- Distance/similarity metric to compute
- **'EUCLIDEAN'**: Euclidean (L2) distance - straight-line geometric distance
  - Formula: sqrt(Σ(xᵢ - yᵢ)²)
  - Range: [0, ∞) - lower is more similar
  - Use for: Continuous features, when magnitude matters
  - Most common choice for general-purpose distance
- **'MANHATTAN'**: Manhattan (L1) distance - city-block distance
  - Formula: Σ|xᵢ - yᵢ|
  - Range: [0, ∞) - lower is more similar
  - Use for: Continuous features, robust to outliers, high-dimensional data
  - Less sensitive to outliers than Euclidean
- **'COSINE'**: Cosine similarity - angular similarity between vectors
  - Formula: (x · y) / (||x|| × ||y||)
  - Range: [-1, 1] - higher is more similar (1 = identical direction)
  - Use for: Text embeddings, sparse data, when magnitude doesn't matter
  - Measures direction, ignores magnitude
- **'CHEBYSHEV'**: Chebyshev (L∞) distance - maximum difference
  - Formula: max(|xᵢ - yᵢ|)
  - Range: [0, ∞) - lower is more similar
  - Use for: When worst-case difference matters, game AI pathfinding
  - Sensitive to single large dimension difference
- **'MINKOWSKI'**: Minkowski distance - generalization of Euclidean and Manhattan
  - Formula: (Σ|xᵢ - yᵢ|ᵖ)^(1/p)
  - Range: [0, ∞) - lower is more similar
  - p=1: Manhattan, p=2: Euclidean, p=∞: Chebyshev
  - Use with MinkowskiPower parameter
- Default: 'EUCLIDEAN'

**MinkowskiPower**
- Power parameter (p) for Minkowski distance
- Only used when DistanceMeasure='MINKOWSKI'
- Range: p ≥ 1 (typically 1-10)
- p=1: Manhattan distance
- p=2: Euclidean distance
- Higher p: Increasingly dominated by largest differences
- Default: 2 (Euclidean)

**TopK**
- Return only K nearest reference vectors for each target
- Limits output to K smallest distances per target vector
- Reduces output size and focuses on most similar items
- Range: K ≥ 1
- If not specified: returns distances to all reference vectors
- Use for nearest neighbor retrieval and recommendation systems

**Accumulate**
- Columns from TargetTable to copy to output unchanged
- Useful for preserving metadata, labels, timestamps

### Input Table Schemas

**TargetTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_id_column | ANY | Unique identifier for each target vector |
| target_feature_column | NUMERIC (INTEGER, BIGINT, DOUBLE PRECISION, DECIMAL) | Feature values forming target vector |
| accumulate_column | ANY | [Optional] Columns to preserve in output |

**ReferenceTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| reference_id_column | ANY | Unique identifier for each reference vector |
| reference_feature_column | NUMERIC | Feature values forming reference vector |

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_id | Same as TargetIDColumn | ID of target vector |
| reference_id | Same as ReferenceIDColumn | ID of reference vector |
| distance | DOUBLE PRECISION | Computed distance or similarity value |
| accumulate_column | Same as TargetTable | Columns copied from TargetTable |

For each target vector, output contains one row per reference vector (or K rows if TopK specified), showing distance/similarity between them.

### Code Examples

**Input Data:**

**target_customers (Target vectors)**
```
customer_id  age  income  purchases  recency
1001         35   65000   12         30
1002         28   45000   3          90
1003         42   85000   25         15
```

**reference_customers (Reference vectors)**
```
customer_id  age  income  purchases  recency
2001         36   67000   13         25
2002         27   43000   2          95
2003         41   88000   28         10
2004         50   120000  40         5
```

**Example 1: Basic Euclidean Distance**
```sql
-- Find distance between target and reference customers
SELECT * FROM TD_VectorDistance (
    ON target_customers AS TargetTable PARTITION BY customer_id
    ON reference_customers AS ReferenceTable DIMENSION
    USING
    TargetIDColumn('customer_id')
    ReferenceIDColumn('customer_id')
    TargetFeatures('age', 'income', 'purchases', 'recency')
    ReferenceFeatures('age', 'income', 'purchases', 'recency')
    DistanceMeasure('EUCLIDEAN')
) AS dt
ORDER BY target_id, distance ASC;

-- Returns pairwise Euclidean distances
-- Smaller distance = more similar customers
```

**Example 2: Find K Nearest Neighbors**
```sql
-- Find 3 most similar reference customers for each target
SELECT * FROM TD_VectorDistance (
    ON target_customers AS TargetTable PARTITION BY customer_id
    ON reference_customers AS ReferenceTable DIMENSION
    USING
    TargetIDColumn('customer_id')
    ReferenceIDColumn('customer_id')
    TargetFeatures('age', 'income', 'purchases', 'recency')
    ReferenceFeatures('age', 'income', 'purchases', 'recency')
    DistanceMeasure('EUCLIDEAN')
    TopK(3)  -- Only 3 nearest neighbors
) AS dt
ORDER BY target_id, distance ASC;

-- Returns only 3 most similar customers per target
-- Reduces output size and focuses on nearest neighbors
```

**Example 3: Cosine Similarity for Document Vectors**
```sql
-- Find similar documents based on TF-IDF features
SELECT
    target_id AS query_doc,
    reference_id AS similar_doc,
    distance AS similarity_score  -- Higher = more similar
FROM TD_VectorDistance (
    ON query_documents AS TargetTable PARTITION BY doc_id
    ON corpus_documents AS ReferenceTable DIMENSION
    USING
    TargetIDColumn('doc_id')
    ReferenceIDColumn('doc_id')
    TargetFeatures('[1:500]')  -- 500 TF-IDF features
    ReferenceFeatures('[1:500]')
    DistanceMeasure('COSINE')
    TopK(10)  -- Top 10 most similar documents
) AS dt
WHERE target_id != reference_id  -- Exclude self-matches
ORDER BY query_doc, similarity_score DESC;

-- Cosine similarity ideal for text/sparse data
-- Measures direction similarity regardless of magnitude
```

**Example 4: Manhattan Distance (Robust to Outliers)**
```sql
-- Product similarity using Manhattan distance
SELECT * FROM TD_VectorDistance (
    ON target_products AS TargetTable PARTITION BY product_id
    ON reference_products AS ReferenceTable DIMENSION
    USING
    TargetIDColumn('product_id')
    ReferenceIDColumn('product_id')
    TargetFeatures('price', 'rating', 'sales_volume', 'review_count')
    ReferenceFeatures('price', 'rating', 'sales_volume', 'review_count')
    DistanceMeasure('MANHATTAN')
    TopK(5)
) AS dt
ORDER BY target_id, distance ASC;

-- Manhattan distance more robust to outliers than Euclidean
-- Good for features with different scales
```

**Example 5: Recommendation System**
```sql
-- Recommend similar products based on features
SELECT
    t.product_name AS target_product,
    r.product_name AS recommended_product,
    d.distance AS similarity_score
FROM TD_VectorDistance (
    ON current_products AS TargetTable PARTITION BY product_id
    ON catalog_products AS ReferenceTable DIMENSION
    USING
    TargetIDColumn('product_id')
    ReferenceIDColumn('product_id')
    TargetFeatures('price', 'category_code', 'brand_code', 'feature_score')
    ReferenceFeatures('price', 'category_code', 'brand_code', 'feature_score')
    DistanceMeasure('EUCLIDEAN')
    TopK(5)
    Accumulate('product_name')
) AS d
JOIN catalog_products r ON d.reference_id = r.product_id
WHERE d.target_id != d.reference_id  -- Exclude self
ORDER BY t.product_name, d.distance ASC;

-- Returns 5 most similar products for recommendations
```

**Example 6: Anomaly Detection Using Distance**
```sql
-- Find transactions far from normal reference transactions
SELECT
    target_id AS transaction_id,
    AVG(distance) AS avg_distance_to_normal,
    MIN(distance) AS min_distance_to_normal
FROM TD_VectorDistance (
    ON test_transactions AS TargetTable PARTITION BY transaction_id
    ON normal_transactions AS ReferenceTable DIMENSION
    USING
    TargetIDColumn('transaction_id')
    ReferenceIDColumn('transaction_id')
    TargetFeatures('amount', 'merchant_category', 'time_of_day', 'location_distance')
    ReferenceFeatures('amount', 'merchant_category', 'time_of_day', 'location_distance')
    DistanceMeasure('EUCLIDEAN')
) AS dt
GROUP BY target_id
HAVING MIN(distance) > 10.0  -- Flag if far from all normal transactions
ORDER BY avg_distance_to_normal DESC;

-- Transactions with large distances are potential anomalies
```

**Example 7: Clustering Quality Evaluation**
```sql
-- Measure intra-cluster distances (within cluster 1)
SELECT
    AVG(distance) AS avg_intra_cluster_distance,
    STDDEV(distance) AS stddev_intra_cluster_distance
FROM TD_VectorDistance (
    ON cluster1_members AS TargetTable PARTITION BY customer_id
    ON cluster1_members AS ReferenceTable DIMENSION
    USING
    TargetIDColumn('customer_id')
    ReferenceIDColumn('customer_id')
    TargetFeatures('age', 'income', 'purchases')
    ReferenceFeatures('age', 'income', 'purchases')
    DistanceMeasure('EUCLIDEAN')
) AS dt
WHERE target_id != reference_id;

-- Smaller intra-cluster distance = tighter, more cohesive cluster
-- Use to validate clustering quality
```

**Example 8: Duplicate Detection**
```sql
-- Find near-duplicate records
SELECT
    target_id AS record_id,
    reference_id AS potential_duplicate,
    distance
FROM TD_VectorDistance (
    ON customer_records AS TargetTable PARTITION BY record_id
    ON customer_records AS ReferenceTable DIMENSION
    USING
    TargetIDColumn('record_id')
    ReferenceIDColumn('record_id')
    TargetFeatures('name_similarity', 'address_similarity', 'age', 'phone_similarity')
    ReferenceFeatures('name_similarity', 'address_similarity', 'age', 'phone_similarity')
    DistanceMeasure('EUCLIDEAN')
) AS dt
WHERE target_id < reference_id  -- Avoid duplicate pairs
  AND distance < 0.1  -- Very close = likely duplicate
ORDER BY distance ASC;

-- Identifies potential duplicate records for deduplication
```

**Example 9: Time Series Similarity**
```sql
-- Find similar time series based on statistical features
SELECT * FROM TD_VectorDistance (
    ON target_sensors AS TargetTable PARTITION BY sensor_id
    ON reference_sensors AS ReferenceTable DIMENSION
    USING
    TargetIDColumn('sensor_id')
    ReferenceIDColumn('sensor_id')
    TargetFeatures('mean_value', 'std_dev', 'max_value', 'min_value',
                   'trend_slope', 'seasonality_amplitude')
    ReferenceFeatures('mean_value', 'std_dev', 'max_value', 'min_value',
                      'trend_slope', 'seasonality_amplitude')
    DistanceMeasure('EUCLIDEAN')
    TopK(5)
) AS dt
ORDER BY target_id, distance ASC;

-- Finds sensors with similar temporal patterns
```

**Example 10: Image Similarity from Embeddings**
```sql
-- Find similar images based on CNN embeddings
SELECT
    target_id AS query_image,
    reference_id AS similar_image,
    distance AS similarity_score
FROM TD_VectorDistance (
    ON query_image_embeddings AS TargetTable PARTITION BY image_id
    ON image_database_embeddings AS ReferenceTable DIMENSION
    USING
    TargetIDColumn('image_id')
    ReferenceIDColumn('image_id')
    TargetFeatures('[1:512]')  -- 512-dimensional CNN embedding
    ReferenceFeatures('[1:512]')
    DistanceMeasure('COSINE')  -- Cosine similarity for embeddings
    TopK(10)
) AS dt
WHERE target_id != reference_id
ORDER BY query_image, similarity_score DESC;

-- Returns 10 most visually similar images
-- Cosine similarity standard for deep learning embeddings
```

### Algorithm Details

**Distance Metrics Formulas:**

For vectors x = (x₁, x₂, ..., xₙ) and y = (y₁, y₂, ..., yₙ):

**Euclidean Distance (L2):**
```
d(x, y) = sqrt(Σᵢ (xᵢ - yᵢ)²)
        = sqrt((x₁-y₁)² + (x₂-y₂)² + ... + (xₙ-yₙ)²)

Properties:
- Straight-line geometric distance
- Sensitive to feature scales (requires standardization)
- Sensitive to outliers (squared differences)
- Most common general-purpose distance metric
- Range: [0, ∞)
```

**Manhattan Distance (L1):**
```
d(x, y) = Σᵢ |xᵢ - yᵢ|
        = |x₁-y₁| + |x₂-y₂| + ... + |xₙ-yₙ|

Properties:
- Sum of absolute differences (city-block distance)
- More robust to outliers than Euclidean
- Computationally simpler (no squares or square roots)
- Good for high-dimensional sparse data
- Range: [0, ∞)
```

**Cosine Similarity:**
```
similarity(x, y) = (x · y) / (||x|| × ||y||)
                 = Σᵢ(xᵢ × yᵢ) / (sqrt(Σᵢ xᵢ²) × sqrt(Σᵢ yᵢ²))

Cosine Distance = 1 - similarity

Properties:
- Measures angular similarity (direction)
- Ignores magnitude (scale-invariant)
- Ideal for sparse, high-dimensional data (text, embeddings)
- Range: similarity ∈ [-1, 1] (1 = identical direction, -1 = opposite)
- Range: distance ∈ [0, 2]
```

**Chebyshev Distance (L∞):**
```
d(x, y) = max |xᵢ - yᵢ|
        = max(|x₁-y₁|, |x₂-y₂|, ..., |xₙ-yₙ|)

Properties:
- Maximum absolute difference across all dimensions
- Sensitive to single dimension with large difference
- Used in game AI (chessboard distance)
- Computationally efficient
- Range: [0, ∞)
```

**Minkowski Distance:**
```
d(x, y) = (Σᵢ |xᵢ - yᵢ|ᵖ)^(1/p)

Special cases:
- p=1: Manhattan distance
- p=2: Euclidean distance
- p→∞: Chebyshev distance

Properties:
- Generalizes Euclidean and Manhattan
- Higher p → More dominated by largest differences
- Flexible but requires tuning parameter p
- Range: [0, ∞)
```

**TopK Selection:**

When TopK is specified:
```
For each target vector:
1. Compute distance to all reference vectors
2. Sort distances in ascending order (or descending for cosine similarity)
3. Return only the K smallest distances (K nearest neighbors)

Reduces output from N×M to N×K rows
where N = target vectors, M = reference vectors, K = TopK
```

**Computational Complexity:**
```
Without TopK:
- Time: O(N × M × D) where N=targets, M=references, D=dimensions
- Space: O(N × M) output rows

With TopK:
- Time: O(N × M × D + N × M × log(K)) for heap-based TopK selection
- Space: O(N × K) output rows

Cosine similarity additional cost:
- Requires computing vector norms: O(N × D + M × D)
```

### Use Cases and Applications

**1. Recommendation Systems**
- Product recommendations based on feature similarity
- Content-based filtering
- Similar item suggestions
- "Customers who liked this also liked..."
- Collaborative filtering with user/item embeddings

**2. Nearest Neighbor Search**
- K-Nearest Neighbors (KNN) algorithm implementation
- Similar customer identification
- Pattern matching
- Case-based reasoning
- Instance-based learning

**3. Document and Text Similarity**
- Similar document retrieval
- Plagiarism detection
- Text deduplication
- Query expansion
- Semantic search

**4. Clustering Validation**
- Intra-cluster distance measurement (compactness)
- Inter-cluster distance measurement (separation)
- Silhouette score calculation
- Davies-Bouldin index computation
- Cluster quality assessment

**5. Anomaly Detection**
- Identify points far from reference distribution
- Outlier detection via distance thresholds
- Novelty detection
- Fraud identification
- Intrusion detection

**6. Duplicate Detection and Entity Resolution**
- Find near-duplicate records
- Entity matching across databases
- Data deduplication
- Fuzzy matching
- Record linkage

**7. Image and Video Similarity**
- Visual search
- Similar image retrieval
- Face recognition and verification
- Content-based image retrieval (CBIR)
- Video fingerprinting

**8. Embedding Evaluation**
- Validate quality of learned embeddings
- Measure semantic similarity in embedding space
- Evaluate word2vec, BERT, image embeddings
- Test if similar items have similar embeddings

**9. Time Series Analysis**
- Find similar temporal patterns
- Time series classification
- Anomaly detection in sensor data
- Pattern matching in financial data
- Weather pattern similarity

**10. Bioinformatics and Genomics**
- DNA/protein sequence similarity
- Gene expression pattern matching
- Drug compound similarity
- Patient similarity for precision medicine
- Protein structure comparison

### Important Notes

**Feature Scaling is Critical:**
- Euclidean, Manhattan, Chebyshev, and Minkowski distances are scale-sensitive
- Features with larger scales dominate distance calculations
- **ALWAYS standardize features** before computing distance (except Cosine)
- Use TD_ScaleFit with ScaleMethod='STD' to standardize
- Cosine similarity is scale-invariant (doesn't require standardization)

**Distance Metric Selection:**
- **Euclidean**: General-purpose, continuous features, when magnitude matters
- **Manhattan**: Robust to outliers, high-dimensional data, interpretable
- **Cosine**: Text/embeddings, sparse data, when direction matters more than magnitude
- **Chebyshev**: When worst-case difference matters
- **Minkowski**: Experimental, flexible generalization

**ReferenceTable DIMENSION:**
- Entire reference table copied to each AMP
- Can cause memory issues if reference table is very large
- Limit reference table size (<100k rows recommended)
- For large reference tables, consider splitting into batches
- DIMENSION required for pairwise distance computation

**TopK Parameter:**
- Dramatically reduces output size (from N×M to N×K)
- Essential for large-scale nearest neighbor retrieval
- Use TopK for recommendation systems
- Without TopK, output can be enormous (1M targets × 1M refs = 1 trillion rows)
- TopK=10-100 typical for most applications

**NULL Handling:**
- TD_VectorDistance does not handle NULL values gracefully
- NULLs in features will cause incorrect distance calculations
- Impute or remove NULLs before calling function
- Use TD_SimpleImputeFit to handle missing values

**Cosine Similarity Interpretation:**
- Returns similarity (not distance): higher = more similar
- Range: [-1, 1] where 1 = identical direction, 0 = orthogonal, -1 = opposite
- Convert to distance: cosine_distance = 1 - cosine_similarity
- Commonly used for text (TF-IDF), word embeddings, document vectors
- Scale-invariant: sim([1,2,3], [2,4,6]) = 1.0

**Self-Matches:**
- When target and reference are same table, each item matches itself perfectly
- Distance to self is always 0 (or similarity 1.0 for cosine)
- Filter self-matches: WHERE target_id != reference_id
- For duplicate detection, avoid double-counting: WHERE target_id < reference_id

**Performance Considerations:**
- Computational cost: O(N × M × D)
- Output size without TopK: N × M rows
- Use TopK to limit output
- Parallel processing across AMPs (partitioned by target_id)
- Consider feature dimensionality reduction (PCA) if D is very large

**Distance vs Similarity:**
- Distance metrics (Euclidean, Manhattan, Chebyshev, Minkowski): **lower is more similar**
- Similarity metrics (Cosine): **higher is more similar**
- Be careful with sorting and thresholds
- Euclidean distance [0, ∞), Cosine similarity [-1, 1]

**Symmetry:**
- Distance metrics are symmetric: d(x,y) = d(y,x)
- Swapping target and reference produces same distances
- Can leverage symmetry for efficiency in some use cases

### Best Practices

**1. Always Standardize Features (Except Cosine)**
- Use TD_ScaleFit with ScaleMethod='STD' before distance calculation
- Critical for Euclidean, Manhattan, Chebyshev, Minkowski
- Not necessary for Cosine similarity
- Features with larger scales dominate if not standardized
- Verify mean ≈ 0, std ≈ 1 after scaling

**2. Choose Appropriate Distance Metric**
- **Euclidean**: Default choice, continuous features, general-purpose
- **Manhattan**: High-dimensional, outliers present, interpretability needed
- **Cosine**: Text data, sparse features, embeddings, magnitude doesn't matter
- **Chebyshev**: Worst-case scenarios, game AI
- Test multiple metrics on validation data

**3. Use TopK to Limit Output**
- Always specify TopK unless you truly need all pairwise distances
- TopK=10-100 typical for recommendations
- Reduces output from potentially billions to manageable size
- Essential for scalability

**4. Handle NULL Values**
- Impute NULLs before calling TD_VectorDistance
- Use TD_SimpleImputeFit with appropriate strategy
- Or filter out rows with NULLs
- NULLs cause incorrect distance calculations

**5. Filter Self-Matches**
- When target = reference table, exclude self-matches
- Add WHERE target_id != reference_id
- Distance to self is always 0 (not useful)
- For duplicates, use WHERE target_id < reference_id to avoid both (A,B) and (B,A)

**6. Manage Reference Table Size**
- Reference table (DIMENSION) copied to each AMP
- Keep reference table reasonably sized (<100k rows)
- For larger reference sets, batch the computation
- Monitor memory usage

**7. Reduce Dimensionality if Needed**
- High-dimensional features (D > 1000) slow computation
- Consider dimensionality reduction (TD_PCA)
- Reduces computation from O(N×M×D) to O(N×M×D')
- Often improves distance quality (curse of dimensionality)

**8. Validate Distance Results**
- Check a few examples manually
- Verify that known similar items have small distances
- Ensure distance metric matches domain intuition
- Test with known ground truth pairs

**9. Leverage for Custom Algorithms**
- Use TD_VectorDistance to implement custom KNN
- Build recommendation engines
- Create distance-based features for models
- Implement collaborative filtering
- Manual control over distance computation

**10. Monitor Performance**
- Computation cost: O(N × M × D)
- For N=10k targets, M=100k refs, D=100 features: 100 billion distance calculations
- Use TopK to dramatically reduce output size
- Consider parallel batching for very large datasets
- Profile and optimize feature dimensions

### Related Functions

**Distance and Similarity:**
- **TD_KNN** - K-Nearest Neighbors algorithm with automatic distance computation
- **TD_Silhouette** - Clustering validation using silhouette score (distance-based)

**Feature Preparation:**
- **TD_ScaleFit** - CRITICAL: Standardize features before distance computation
- **TD_ScaleTransform** - Apply scaling to new data
- **TD_PCA** - Reduce dimensionality to improve distance computation
- **TD_SimpleImputeFit** - Handle missing values

**Embedding and Transformation:**
- **TD_TF** - Create term frequency vectors for text
- **TD_TFIDF** - Create TF-IDF vectors for text similarity
- **TD_TextParser** - Parse text into tokens for feature extraction
- **Word2Vec** - Create word embeddings for semantic similarity

**Clustering:**
- **TD_KMeans** - Uses distance internally for cluster assignment
- **TD_KMeansPredict** - Assigns points to clusters based on distance

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf
- [Distance Metrics - Wikipedia](https://en.wikipedia.org/wiki/Distance_(mathematics))
- [Cosine Similarity - Wikipedia](https://en.wikipedia.org/wiki/Cosine_similarity)
- [Scikit-learn Distance Metrics](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise_distances.html)

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Model Training Functions (Distance Computation Utility)
