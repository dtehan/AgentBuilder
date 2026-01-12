# TD_KMeans

### Function Name
**TD_KMeans**

### Description
TD_KMeans is an unsupervised machine learning algorithm that groups observations into K distinct clusters based on similarity, where each observation belongs to the cluster with the nearest mean (centroid). This iterative clustering function partitions datasets into homogeneous groups by minimizing within-cluster variance, assigning points to nearest centroids, and recalculating centroids until convergence or maximum iterations. The algorithm assumes similar data points are close together in the feature space and leverages Teradata's parallel architecture to efficiently process large datasets by training models across distributed AMPs.

The K-means clustering algorithm operates by repeatedly performing two steps: (1) assigning each data point to the nearest cluster centroid based on Euclidean distance, and (2) recalculating centroids as the mean of all points assigned to each cluster. The function supports two initialization methods for selecting initial centroids: random selection from input data points, or the KMeans++ algorithm which intelligently chooses well-separated initial centroids to improve clustering quality and convergence speed. Users can either specify the number of clusters (NumClusters) or provide a table of initial centroids (InitialCentroidsTable), with the function running multiple initializations (NumInit) to select the model with minimum total within-cluster sum of squares.

TD_KMeans outputs comprehensive clustering results including cluster centroids, cluster sizes, within-cluster sum of squares per cluster, and optional cluster assignments for each input observation. The function provides key metrics for evaluating clustering quality: total within-cluster sum of squares (measure of compactness), between-cluster sum of squares (measure of separation), and convergence information. Users can leverage the Elbow method by running TD_KMeans with different K values and plotting total within-cluster sum of squares to determine optimal cluster count. The function handles missing values by excluding rows with NULL entries in target columns, supports deterministic results via seed parameters, and enables evaluation via TD_Silhouette for cluster quality assessment.

### When the Function Would Be Used
- **Customer Segmentation**: Group customers by purchasing behavior, demographics, or preferences
- **Market Segmentation**: Identify distinct market segments for targeted strategies
- **Document Clustering**: Group similar documents or articles by topic
- **Image Segmentation**: Partition images into regions with similar properties
- **Anomaly Detection**: Identify outliers as points distant from cluster centroids
- **Pattern Recognition**: Discover natural groupings in unlabeled data
- **Data Compression**: Reduce dataset size by replacing points with cluster centroids
- **Feature Engineering**: Create cluster membership as categorical features
- **Recommendation Systems**: Group users or items for collaborative filtering
- **Network Analysis**: Identify communities in social or communication networks
- **Genomic Clustering**: Group genes or proteins by expression patterns
- **Inventory Management**: Segment products for targeted inventory strategies
- **Fraud Detection**: Identify unusual transaction patterns via clustering
- **Load Balancing**: Distribute computing tasks based on resource similarity
- **Geographic Clustering**: Group locations by proximity or characteristics
- **Sensor Data Analysis**: Identify operational modes in equipment data
- **Color Quantization**: Reduce colors in images via clustering
- **Time Series Clustering**: Group temporal patterns for forecasting
- **Healthcare Stratification**: Segment patients for personalized treatment
- **Risk Assessment**: Group entities by risk profiles

### Syntax

```sql
TD_KMeans (
    ON { table | view | (query) } AS InputTable
    [ ON { table | view | (query) } AS InitialCentroidsTable DIMENSION ]
    [ OUT [ PERMANENT | VOLATILE ] TABLE ModelTable(model_output_table_name) ]
    USING
    IdColumn('id_column')
    TargetColumns({'target_column'|'target_column_range'}[,...])
    [ InitialCentroidsMethod({'random'|'kmeans++'}) ]
    [ NumClusters(number_of_clusters) ]
    [ Seed(seed_value) ]
    [ StopThreshold(threshold_value) ]
    [ MaxIterNum(number_of_iterations) ]
    [ NumInit(num_init) ]
    [ OutputClusterAssignment({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
)
```

### Required Syntax Elements for TD_KMeans

**ON clause (InputTable)**
- Accepts table, view, or query containing data to cluster
- Can have no partition, PARTITION BY ANY, or PARTITION BY ANY ORDER BY
- Do NOT specify PARTITION BY column (function reports error)
- Each row represents an observation to be clustered

**IdColumn**
- Specify input table column name containing unique identifier for each row
- Must be unique across all rows
- Used to track observation assignments and in output

**TargetColumns**
- Specify input table column names for clustering (features used for distance calculations)
- All columns must be numeric data types
- Supports column range notation (e.g., '[1:5]')
- Function calculates Euclidean distance using these columns

### Optional Syntax Elements for TD_KMeans

**ON clause (InitialCentroidsTable)**
- Accepts DIMENSION table containing initial centroid values
- Alternative to random initialization or KMeans++
- Must contain same target columns as InputTable
- If provided, NumClusters is inferred from number of rows
- Enables deterministic results across runs

**OUT clause (ModelTable)**
- Specify PERMANENT or VOLATILE table name to save clustering model
- Model contains cluster centroids, sizes, within-cluster sum of squares
- Use for deployment with TD_KMeansPredict
- If not specified, model returned as temporary result

**InitialCentroidsMethod**
- Specify initialization method for selecting initial centroids
- 'random': Randomly select centroids from input data points
- 'kmeans++': Use KMeans++ algorithm for smart initialization (improves quality and speed)
- Not required if InitialCentroidsTable provided
- Default: 'random'

**NumClusters**
- Specify number of clusters (K) to create
- Must be positive integer
- Not required if InitialCentroidsTable provided (K inferred from table)
- Cannot provide both NumClusters and InitialCentroidsTable (error reported)
- Choosing optimal K: use Elbow method or Silhouette analysis

**Seed**
- Specify non-negative integer seed for reproducible random centroid selection
- Controls random sampling of initial centroids
- Use for deterministic results on same machine configuration
- Not required if InitialCentroidsTable provided
- Results may vary across different machine configurations without InitialCentroidsTable

**StopThreshold**
- Specify convergence threshold for centroid movement
- Algorithm converges if distance between old and new centroids < threshold
- Smaller values = tighter convergence, more iterations
- Must be non-negative float
- Default: 0.0395

**MaxIterNum**
- Specify maximum number of iterations for K-means algorithm
- Algorithm stops after this many iterations even if not converged
- Prevents infinite loops for difficult convergence scenarios
- Must be positive integer
- Default: 10

**NumInit**
- Specify number of times to repeat clustering with different initial seeds
- Function returns model with lowest total within-cluster sum of squares
- Each initialization uses different random centroid seeds
- Reduces sensitivity to poor initialization
- Not required if InitialCentroidsTable provided
- Must be positive integer
- Default: 1

**OutputClusterAssignment**
- Specify whether to return cluster assignment for each input observation
- 'true': Output contains IdColumn and assigned cluster ID for each row
- 'false': Output contains cluster centroids and statistics only
- Default: False

### Input Table Schema

**InputTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| IdColumn | Any | Unique identifier for each input table row |
| TargetColumns | BYTEINT, SMALLINT, INTEGER, BIGINT, DECIMAL, NUMERIC, FLOAT, REAL, DOUBLE PRECISION | Numeric columns used for clustering (features for distance calculation) |

**InitialCentroidsTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| Initial_Clusterid_Column | BYTEINT, SMALLINT, INTEGER, BIGINT | Unique identifiers for initial centroids (cluster IDs) |
| TargetColumns | BYTEINT, SMALLINT, INTEGER, BIGINT, DECIMAL, NUMERIC, FLOAT, REAL, DOUBLE PRECISION | Initial centroid values for each feature (must match InputTable TargetColumns) |

**Important Notes:**
- Function skips rows with NULL values in any TargetColumn
- InputTable and InitialCentroidsTable must have matching TargetColumns (same names and data types)

### Output Table Schema

**Output When OutputClusterAssignment = False (Cluster Model):**

| Column | Data Type | Description |
|--------|-----------|-------------|
| TD_CLUSTERID_KMEANS | BIGINT | Unique identifier for the cluster (0, 1, 2, ..., K-1) |
| TargetColumns | REAL | Centroid values for each feature (cluster centers) |
| TD_SIZE_KMEANS | BIGINT | Number of observations assigned to the cluster |
| TD_WITHINSS_KMEANS | REAL | Within-cluster sum of squares (sum of squared distances from points to centroid) |
| Id_Column | Same as InputTable IdColumn | Column name from InputTable (contains NULL values) |
| TD_MODELINFO_KMEANS | VARCHAR(128) CHARACTER SET LATIN | Model metadata including: Converged (True/False), Number of Iterations, Number of Clusters, Total_WithinSS, Between_SS, Method for InitialCentroids (Random, KMeans++, or Externally supplied) |

**Output When OutputClusterAssignment = True (Cluster Assignments):**

| Column | Data Type | Description |
|--------|-----------|-------------|
| Id_Column | Same as InputTable IdColumn | Unique identifier for input observations copied from InputTable |
| TD_CLUSTERID_KMEANS | BIGINT | Cluster ID assigned to the observation (0, 1, 2, ..., K-1) |

**Key Model Metrics:**
- **Converged**: Whether algorithm reached convergence (True/False)
- **Number of Iterations**: Iterations performed before convergence or MaxIterNum
- **Number of Clusters**: K clusters produced
- **Total_WithinSS**: Total within-cluster sum of squares (lower = more compact clusters)
- **Between_SS**: Between-cluster sum of squares (higher = better separation)
- **Method for InitialCentroids**: Initialization method used

### Code Examples

**Input Data: customer_data**
```
customer_id  annual_spend  purchase_frequency  avg_order_value
1            1500          12                  125
2            8000          48                  166
3            2000          8                   250
4            9500          52                  182
```

**Example 1: Basic K-Means Clustering (K=3)**
```sql
-- Cluster customers into 3 segments
SELECT * FROM TD_KMeans (
    ON customer_data AS InputTable
    USING
    IdColumn('customer_id')
    TargetColumns('annual_spend', 'purchase_frequency', 'avg_order_value')
    NumClusters(3)
    Seed(42)
    MaxIterNum(50)
    StopThreshold(0.01)
) AS dt
ORDER BY TD_CLUSTERID_KMEANS;

-- Output: 3 cluster centroids with sizes and within-cluster SS
-- Shows natural customer segments based on purchasing behavior
```

**Example 2: Using KMeans++ Initialization**
```sql
-- Use KMeans++ for better initial centroids
SELECT * FROM TD_KMeans (
    ON product_features AS InputTable
    USING
    IdColumn('product_id')
    TargetColumns('price', 'rating', 'sales_volume', 'review_count')
    NumClusters(5)
    InitialCentroidsMethod('kmeans++')
    Seed(123)
    MaxIterNum(100)
) AS dt
ORDER BY TD_CLUSTERID_KMEANS;

-- KMeans++ selects well-separated initial centroids
-- Often converges faster and produces better clusters than random init
```

**Example 3: Multiple Random Initializations**
```sql
-- Run 10 initializations, return best clustering
SELECT * FROM TD_KMeans (
    ON sensor_readings AS InputTable
    USING
    IdColumn('sensor_id')
    TargetColumns('temperature', 'pressure', 'vibration', 'power_consumption')
    NumClusters(4)
    Seed(456)
    NumInit(10)  -- Run 10 times with different seeds
    MaxIterNum(50)
) AS dt;

-- Function returns clustering with lowest Total_WithinSS
-- Reduces sensitivity to poor random initialization
```

**Example 4: Get Cluster Assignments**
```sql
-- Cluster customers and return assignments
SELECT * FROM TD_KMeans (
    ON customer_rfm AS InputTable
    USING
    IdColumn('customer_id')
    TargetColumns('recency', 'frequency', 'monetary')
    NumClusters(4)
    Seed(789)
    OutputClusterAssignment('true')
) AS dt
ORDER BY customer_id;

-- Output: customer_id and assigned TD_CLUSTERID_KMEANS
-- Use assignments for targeted marketing campaigns
```

**Example 5: Save Model for Later Use**
```sql
-- Train and save K-means model
SELECT * FROM TD_KMeans (
    ON customer_train AS InputTable
    OUT VOLATILE TABLE ModelTable(customer_kmeans_model)
    USING
    IdColumn('customer_id')
    TargetColumns('lifetime_value', 'churn_score', 'engagement_score')
    NumClusters(3)
    InitialCentroidsMethod('kmeans++')
    Seed(101)
    MaxIterNum(100)
) AS dt;

-- Model saved to customer_kmeans_model table
-- Use with TD_KMeansPredict to assign new customers to clusters
```

**Example 6: Provide Initial Centroids**
```sql
-- Create initial centroids table
CREATE VOLATILE TABLE initial_centers (
    cluster_id INTEGER,
    feature1 FLOAT,
    feature2 FLOAT,
    feature3 FLOAT
) ON COMMIT PRESERVE ROWS;

INSERT INTO initial_centers VALUES (0, 10.0, 5.0, 2.5);
INSERT INTO initial_centers VALUES (1, 50.0, 25.0, 12.5);
INSERT INTO initial_centers VALUES (2, 90.0, 45.0, 22.5);

-- Cluster using provided initial centroids
SELECT * FROM TD_KMeans (
    ON transaction_data AS InputTable
    ON initial_centers AS InitialCentroidsTable DIMENSION
    USING
    IdColumn('transaction_id')
    TargetColumns('feature1', 'feature2', 'feature3')
    MaxIterNum(50)
) AS dt;

-- Deterministic results using same initial centroids
-- K inferred from initial_centers (3 clusters)
```

**Example 7: Elbow Method for Optimal K**
```sql
-- Run K-means for K=2 through K=10
-- For K=2
CREATE VOLATILE TABLE kmeans_k2 AS (
    SELECT * FROM TD_KMeans (
        ON customer_features AS InputTable
        USING
        IdColumn('customer_id')
        TargetColumns('[1:10]')
        NumClusters(2)
        Seed(42)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- For K=3
CREATE VOLATILE TABLE kmeans_k3 AS (
    SELECT * FROM TD_KMeans (
        ON customer_features AS InputTable
        USING
        IdColumn('customer_id')
        TargetColumns('[1:10]')
        NumClusters(3)
        Seed(42)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- ... repeat for K=4 through K=10

-- Extract Total_WithinSS from each model
SELECT 2 AS k, CAST(SUBSTR(TD_MODELINFO_KMEANS,
       POSITION('Total_WithinSS' IN TD_MODELINFO_KMEANS)+17, 20) AS FLOAT) AS total_withinss
FROM kmeans_k2
WHERE TD_MODELINFO_KMEANS LIKE '%Total_WithinSS%'
UNION ALL
SELECT 3 AS k, CAST(SUBSTR(TD_MODELINFO_KMEANS,
       POSITION('Total_WithinSS' IN TD_MODELINFO_KMEANS)+17, 20) AS FLOAT)
FROM kmeans_k3
WHERE TD_MODELINFO_KMEANS LIKE '%Total_WithinSS%'
-- ... continue for all K values

-- Plot K vs Total_WithinSS to find "elbow" (optimal K)
-- Elbow = point where adding clusters shows diminishing returns
```

**Example 8: Image Color Quantization**
```sql
-- Reduce image colors via clustering RGB values
-- Input: pixels table with r, g, b columns
SELECT * FROM TD_KMeans (
    ON image_pixels AS InputTable
    OUT VOLATILE TABLE ModelTable(color_palette)
    USING
    IdColumn('pixel_id')
    TargetColumns('r', 'g', 'b')
    NumClusters(16)  -- Reduce to 16 colors
    InitialCentroidsMethod('kmeans++')
    Seed(202)
    MaxIterNum(20)
    OutputClusterAssignment('true')
) AS dt;

-- Centroids represent 16-color palette
-- Assignments map each pixel to nearest palette color
-- Compressed representation for storage or transmission
```

**Example 9: Anomaly Detection via Clustering**
```sql
-- Cluster normal transactions, identify outliers
-- Step 1: Cluster transactions
CREATE VOLATILE TABLE transaction_clusters AS (
    SELECT * FROM TD_KMeans (
        ON transactions AS InputTable
        USING
        IdColumn('transaction_id')
        TargetColumns('amount', 'time_of_day', 'location_risk', 'merchant_category')
        NumClusters(10)
        InitialCentroidsMethod('kmeans++')
        Seed(303)
        OutputClusterAssignment('true')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 2: Calculate distance from each transaction to its cluster center
-- (requires joining with centroid values and computing distance)
-- Transactions with large distances = potential anomalies

-- Alternative: Use small K to create dense clusters
-- Points not fitting any cluster well = anomalies
```

**Example 10: Complete Workflow (Cluster + Profile + Predict)**
```sql
-- Step 1: Cluster training customers
CREATE VOLATILE TABLE customer_segments AS (
    SELECT * FROM TD_KMeans (
        ON customer_train AS InputTable
        OUT VOLATILE TABLE ModelTable(customer_kmeans_model)
        USING
        IdColumn('customer_id')
        TargetColumns('recency_days', 'total_purchases', 'avg_order_value',
                      'engagement_score')
        NumClusters(4)
        InitialCentroidsMethod('kmeans++')
        Seed(404)
        NumInit(5)
        MaxIterNum(100)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 2: Get cluster assignments for training customers
CREATE VOLATILE TABLE train_assignments AS (
    SELECT * FROM TD_KMeans (
        ON customer_train AS InputTable
        ON customer_kmeans_model AS InitialCentroidsTable DIMENSION
        USING
        IdColumn('customer_id')
        TargetColumns('recency_days', 'total_purchases', 'avg_order_value',
                      'engagement_score')
        OutputClusterAssignment('true')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 3: Profile each cluster (analyze characteristics)
SELECT
    ca.TD_CLUSTERID_KMEANS AS cluster,
    COUNT(*) AS customer_count,
    AVG(ct.recency_days) AS avg_recency,
    AVG(ct.total_purchases) AS avg_purchases,
    AVG(ct.avg_order_value) AS avg_order_val,
    AVG(ct.engagement_score) AS avg_engagement
FROM train_assignments ca
JOIN customer_train ct ON ca.customer_id = ct.customer_id
GROUP BY ca.TD_CLUSTERID_KMEANS
ORDER BY cluster;

-- Step 4: Assign new customers to clusters using TD_KMeansPredict
SELECT * FROM TD_KMeansPredict (
    ON customer_new AS InputTable PARTITION BY ANY
    ON customer_kmeans_model AS ModelTable DIMENSION
    USING
    IdColumn('customer_id')
) AS dt;

-- Output: New customers assigned to nearest existing cluster
-- Apply segment-specific strategies (retention, upsell, etc.)
```

### K-Means Algorithm Details

**Algorithm Steps:**
1. Initialize K cluster centroids:
   - Random: Select K random data points as initial centroids
   - KMeans++: Iteratively select centroids with probability proportional to distance from nearest existing centroid
   - Provided: Use InitialCentroidsTable centroids
2. Assignment Step:
   - For each observation, calculate Euclidean distance to all K centroids
   - Assign observation to nearest centroid (minimum distance)
3. Update Step:
   - For each cluster, recalculate centroid as mean of all assigned observations
   - Centroid_j = (1/|C_j|) * Σ(x_i) for all x_i in cluster C_j
4. Convergence Check:
   - Calculate distance between old and new centroids
   - If all centroid movements < StopThreshold: converge and stop
   - If MaxIterNum reached: stop (may not be fully converged)
   - Otherwise: repeat steps 2-4

**Distance Metric:**
- Euclidean distance: d(x, y) = √(Σ(x_i - y_i)²)
- Computed across all TargetColumns

**Objective Function:**
- Minimize Total Within-Cluster Sum of Squares (Total_WithinSS)
- Total_WithinSS = Σ_j Σ_(x in C_j) ||x - centroid_j||²
- Lower Total_WithinSS = more compact, homogeneous clusters

**Between-Cluster Sum of Squares:**
- Measures separation between clusters
- Between_SS = Σ_j |C_j| * ||centroid_j - global_mean||²
- Higher Between_SS = better separated clusters

**Convergence:**
- Algorithm converges when centroids stabilize (movement < StopThreshold)
- May not converge in MaxIterNum iterations for difficult data
- Multiple initializations (NumInit) help find better solutions

### Use Cases and Applications

**1. Customer Segmentation**
- RFM (Recency, Frequency, Monetary) clustering
- Behavioral segmentation for marketing
- Customer lifetime value grouping
- Churn risk segmentation

**2. Market Analysis**
- Geographic market segmentation
- Product category grouping
- Competitive positioning analysis
- Price tier identification

**3. Image Processing**
- Image compression via color quantization
- Object segmentation in computer vision
- Texture classification
- Image retrieval systems

**4. Document Analysis**
- Topic clustering for text documents
- News article categorization
- Patent classification
- Email organization

**5. Anomaly Detection**
- Fraud detection in transactions
- Network intrusion detection
- Manufacturing defect identification
- Health monitoring outliers

**6. Recommendation Systems**
- User clustering for collaborative filtering
- Product grouping for recommendations
- Content-based filtering
- Hybrid recommendation approaches

**7. Bioinformatics**
- Gene expression clustering
- Protein sequence grouping
- Disease subtype identification
- Drug discovery compound clustering

**8. Network Analysis**
- Community detection in social networks
- Server clustering for load balancing
- Routing optimization
- Sensor network organization

**9. Inventory Management**
- Product assortment optimization
- Demand pattern clustering
- Warehouse layout optimization
- SKU rationalization

**10. Financial Services**
- Portfolio risk clustering
- Credit scoring segments
- Trading pattern identification
- Insurance risk grouping

### Important Notes

**Choosing Optimal K:**
- **Elbow Method**: Plot Total_WithinSS vs K, look for "elbow" (point of diminishing returns)
- **Silhouette Analysis**: Use TD_Silhouette function to evaluate cluster quality for different K
- **Business Requirements**: Sometimes K determined by business needs (e.g., 3 tiers: low/medium/high)
- **Rule of Thumb**: Start with K ≈ √(n/2) where n is number of observations

**Initialization Methods:**
- **Random**: Fast but may lead to poor solutions, use NumInit>1 to mitigate
- **KMeans++**: Smarter initialization, typically faster convergence and better clusters
- **Provided Centroids**: Use InitialCentroidsTable for reproducible or domain-driven starting points

**Deterministic Results:**
- Use Seed parameter for reproducible results on same machine
- Results may vary across machine configurations without InitialCentroidsTable
- InitialCentroidsTable provides most deterministic results
- Multiple runs with NumInit may produce different "best" result

**Handling Missing Values:**
- Function automatically skips rows with NULL in any TargetColumn
- Missing values not imputed automatically
- Use TD_SimpleImpute before clustering if needed
- Consider whether missing data has patterns that should be preserved

**Feature Scaling:**
- K-means uses Euclidean distance, sensitive to feature scales
- **Strongly recommended**: Standardize features using TD_Scale before clustering
- Features with larger ranges dominate distance calculations
- Example: Income ($10k-$200k) dominates age (18-80) if not scaled

**Convergence and Iterations:**
- Algorithm may not always converge within MaxIterNum
- Increase MaxIterNum if convergence not reached
- Decrease StopThreshold for tighter convergence
- Check TD_MODELINFO_KMEANS for convergence status

**Performance Considerations:**
- Computational complexity: O(n*K*i*d) where n=observations, K=clusters, i=iterations, d=dimensions
- Scales well to large datasets via parallel processing
- More clusters (K) and features (d) increase computation time
- Use column range notation for many features

**Evaluation Metrics:**
- **Total_WithinSS**: Lower = more compact clusters (but always decreases with increasing K)
- **Between_SS**: Higher = better separated clusters
- **Silhouette Score**: Use TD_Silhouette (ranges -1 to 1, higher is better)
- **Business Validation**: Check if clusters make sense for domain

### Best Practices

**1. Scale Features Before Clustering**
- Always use TD_ScaleFit and TD_ScaleTransform to standardize features
- Prevents features with larger ranges from dominating
- Use ScaleMethod='STD' for most cases
- Document scaling parameters for production deployment

**2. Experiment with Different K Values**
- Try range of K values (e.g., 2 to 10)
- Use Elbow method to identify optimal K
- Use TD_Silhouette for quantitative cluster quality
- Consider business constraints on number of segments

**3. Use KMeans++ Initialization**
- Prefer InitialCentroidsMethod='kmeans++' over 'random'
- Typically converges faster with better results
- Especially important for large K or complex data
- Still use Seed for reproducibility

**4. Run Multiple Initializations**
- Set NumInit=5 or 10 to reduce initialization sensitivity
- Function returns clustering with best Total_WithinSS
- Increases computation time proportionally
- More important for random initialization than KMeans++

**5. Set Appropriate Convergence Criteria**
- StopThreshold=0.01 to 0.1: Balanced convergence
- Smaller threshold: Tighter convergence, more iterations
- MaxIterNum=50 to 100: Usually sufficient
- Monitor convergence status in TD_MODELINFO_KMEANS

**6. Profile Clusters After Training**
- Examine cluster sizes (avoid very small or very large clusters)
- Analyze cluster centroids for interpretability
- Compare feature distributions across clusters
- Validate clusters make business sense

**7. Handle Missing Values Appropriately**
- Impute missing values before clustering (TD_SimpleImpute)
- Choose imputation strategy based on data
- Alternatively, create "missing value" indicator features
- Document missing value handling for reproducibility

**8. Save Models for Production**
- Use OUT TABLE ModelTable to save trained models
- Deploy saved models with TD_KMeansPredict
- Version control models for reproducibility
- Document model parameters and training data

**9. Evaluate Cluster Quality**
- Calculate within-cluster variance
- Use TD_Silhouette for quantitative assessment
- Check cluster separation (Between_SS)
- Validate with domain experts

**10. Iterate and Refine**
- Start with simple feature set
- Add features iteratively and reassess clusters
- Experiment with feature engineering (ratios, interactions)
- A/B test cluster-based strategies before full deployment

### Related Functions
- **TD_KMeansPredict** - Assign new observations to existing clusters
- **TD_Silhouette** - Evaluate cluster quality and optimal K
- **TD_Scale** - Standardize features before clustering (highly recommended)
- **TD_SimpleImpute** - Handle missing values before clustering
- **TD_PCA** - Reduce dimensionality before clustering
- **TD_UnivariateStatistics** - Profile clusters after training
- **TD_DecisionForest** - Alternative for supervised classification
- **TD_OneClassSVM** - Alternative for anomaly detection

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Model Training Functions
