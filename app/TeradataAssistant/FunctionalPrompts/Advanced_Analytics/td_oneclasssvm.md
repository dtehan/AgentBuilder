# TD_OneClassSVM

### Function Name
**TD_OneClassSVM**

### Description
TD_OneClassSVM trains an unsupervised anomaly detection model that learns the normal distribution of a single class and identifies outliers, novelties, or anomalies as deviations from that distribution. Unlike traditional supervised classification that learns boundaries between multiple classes, One-Class SVM constructs a decision boundary around normal data in high-dimensional feature space, classifying points inside the boundary as normal and points outside as anomalies. This makes it ideal for scenarios where you have abundant examples of normal behavior but few or no examples of anomalies, which is common in fraud detection, intrusion detection, equipment failure prediction, and quality control applications.

The algorithm works by mapping input features to a high-dimensional space using a kernel function (RBF, Linear, Polynomial, or Sigmoid), then finding the smallest hypersphere or hyperplane that encapsulates the majority of training points while allowing a controlled fraction of points to fall outside (controlled by the Nu parameter). Points far from this boundary are classified as anomalies. TD_OneClassSVM is particularly effective when normal data clusters in feature space but anomalies are scattered or rare. The function uses support vectors (critical boundary points) to define the decision boundary, making predictions computationally efficient even for large datasets since only support vectors need to be stored and evaluated.

TD_OneClassSVM excels in real-world anomaly detection scenarios where collecting labeled anomaly examples is expensive, dangerous, or impossible. It handles high-dimensional data effectively through kernel transformations, automatically adapts to complex non-linear patterns in normal data via RBF kernels, and provides interpretable anomaly scores representing distance from the normal region. The Nu parameter allows direct control over the expected proportion of anomalies, making it easy to calibrate sensitivity based on domain knowledge. While One-Class SVM requires careful kernel and hyperparameter tuning, it provides robust anomaly detection that generalizes well to novel outlier patterns not seen during training.

### When the Function Would Be Used
- **Fraud Detection**: Identify fraudulent transactions among predominantly legitimate ones
- **Intrusion Detection**: Detect network intrusions and cybersecurity threats
- **Equipment Failure Prediction**: Identify abnormal sensor readings indicating impending failure
- **Quality Control**: Detect defective products in manufacturing processes
- **Medical Anomaly Detection**: Identify rare diseases or unusual patient conditions
- **Credit Card Fraud**: Flag suspicious transactions in real-time payment systems
- **Network Traffic Monitoring**: Detect DDoS attacks and unusual traffic patterns
- **Log Analysis**: Identify anomalous system logs indicating problems
- **Sensor Data Monitoring**: Detect unusual IoT sensor readings
- **Customer Behavior Analysis**: Identify unusual customer activity patterns
- **Supply Chain Monitoring**: Detect anomalies in logistics and inventory
- **Environmental Monitoring**: Identify unusual pollution levels or weather events
- **Predictive Maintenance**: Detect early signs of equipment degradation
- **Cybersecurity**: Identify zero-day attacks and novel threats
- **Financial Market Analysis**: Detect unusual trading patterns and market manipulation
- **Healthcare Monitoring**: Identify abnormal vital signs or test results
- **E-Commerce**: Detect fake reviews, bot accounts, or unusual purchasing patterns
- **Industrial Process Control**: Monitor manufacturing processes for deviations
- **Telecommunications**: Detect call fraud and network abuse
- **Energy Grid Monitoring**: Identify unusual power consumption or grid anomalies
- **Novelty Detection**: Identify previously unseen patterns in streaming data
- **Outlier Detection**: Remove outliers before training supervised models
- **One-Class Classification**: Build models when only one class is well-represented
- **Rare Event Detection**: Identify infrequent but critical events

### Syntax

```sql
TD_OneClassSVM (
    ON { table | view | (query) } AS InputTable PARTITION BY ANY
    USING
    TargetColumns ({ 'target_column' | target_column_range }[,...])
    [ KernelType ({ 'RBF' | 'LINEAR' | 'POLY' | 'SIGMOID' }) ]
    [ Nu (nu_value) ]
    [ Gamma (gamma_value) ]
    [ Degree (degree_value) ]
    [ Coef0 (coef0_value) ]
    [ CacheSize (cache_mb) ]
    [ Tolerance (tolerance_value) ]
    [ MaxIterNum (max_iterations) ]
    [ Seed (random_seed) ]
    [ Accumulate ({ 'accumulate_column' | accumulate_column_range }[,...]) ]
) AS alias
```

### Required Syntax Elements for TD_OneClassSVM

**ON clause (InputTable)**
- Training data representing normal/typical behavior
- PARTITION BY ANY for distributed parallel training
- Should contain predominantly normal examples with few/no anomalies

**TargetColumns**
- Feature columns to use for anomaly detection model
- Must be numeric data types (INTEGER, DOUBLE PRECISION, etc.)
- Supports column range notation ('[1:10]')
- Multiple columns define the feature space

### Optional Syntax Elements for TD_OneClassSVM

**KernelType**
- Kernel function for transforming features to high-dimensional space
- **'RBF'** (Radial Basis Function): Gaussian kernel for non-linear boundaries
  - Most common choice for anomaly detection
  - Creates smooth, circular decision boundaries
  - Works well for most real-world data distributions
- **'LINEAR'**: Linear kernel for linear boundaries
  - Faster training and prediction
  - Best when normal data is linearly separable
- **'POLY'**: Polynomial kernel for polynomial boundaries
  - Good for non-linear patterns with polynomial structure
  - Controlled by Degree parameter
- **'SIGMOID'**: Sigmoid kernel similar to neural network activation
  - Less commonly used for One-Class SVM
- Default: 'RBF'

**Nu**
- Upper bound on fraction of training errors (margin violations)
- Lower bound on fraction of support vectors
- Range: 0 < Nu ≤ 1
- Controls sensitivity to outliers:
  - **Smaller Nu** (e.g., 0.01-0.05): Tighter boundary, fewer outliers expected, higher sensitivity
  - **Larger Nu** (e.g., 0.1-0.2): Looser boundary, more outliers expected, lower sensitivity
- Interpretation: approximately Nu fraction of training data treated as outliers
- Default: 0.1 (expects ~10% outliers in training data)

**Gamma**
- Kernel coefficient for RBF, POLY, and SIGMOID kernels
- Controls influence range of individual training examples:
  - **Smaller Gamma**: Broader influence, smoother decision boundary
  - **Larger Gamma**: Narrower influence, more complex boundary (risk of overfitting)
- For RBF kernel: gamma = 1 / (2 * σ²) where σ is the Gaussian width
- Default: 1 / n_features (automatically calculated)
- Critical hyperparameter requiring tuning

**Degree**
- Polynomial degree for POLY kernel
- Defines order of polynomial transformation
- Range: positive integers (typically 2-5)
- Larger degree → more complex non-linear boundaries
- Default: 3

**Coef0**
- Independent coefficient term in POLY and SIGMOID kernels
- Affects kernel calculation: (gamma * <x, y> + Coef0)^Degree
- Can help with numerical stability
- Default: 0

**CacheSize**
- Kernel cache size in megabytes for optimization
- Larger cache → faster training (more memory usage)
- Recommended: 200-500 MB for large datasets
- Default: 100 MB

**Tolerance**
- Stopping criterion tolerance for optimization convergence
- Smaller tolerance → more precise solution (longer training)
- Range: typically 1e-3 to 1e-5
- Default: 0.001

**MaxIterNum**
- Maximum number of optimization iterations
- Prevents infinite loops if convergence is slow
- -1 for no limit (not recommended)
- Default: 100000

**Seed**
- Random seed for reproducible results
- Affects initialization of optimization algorithm
- Use same seed for deterministic behavior across runs

**Accumulate**
- Columns to copy from input to output unchanged
- Useful for preserving identifiers, timestamps, metadata

### Input Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | NUMERIC (INTEGER, BIGINT, DOUBLE PRECISION, DECIMAL) | Feature columns representing normal behavior |
| accumulate_column | ANY | [Optional] Columns to preserve in output |

**Important:** Training data should represent normal behavior with few/no anomalies. The algorithm learns what is "normal" from the training set.

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| model_id | INTEGER | Model identifier (typically 1 for single model) |
| kernel_type | VARCHAR | Kernel used: RBF, LINEAR, POLY, SIGMOID |
| nu | DOUBLE PRECISION | Nu parameter used for training |
| gamma | DOUBLE PRECISION | Gamma parameter used (NULL for LINEAR) |
| degree | INTEGER | Polynomial degree (NULL for non-POLY kernels) |
| coef0 | DOUBLE PRECISION | Coefficient term (NULL for RBF and LINEAR) |
| n_support_vectors | INTEGER | Number of support vectors identified |
| support_vector_indices | VARCHAR (JSON) | Indices of support vectors from training data |
| support_vectors | VARCHAR (JSON) | Support vector feature values |
| dual_coefficients | VARCHAR (JSON) | Alpha coefficients for support vectors |
| intercept | DOUBLE PRECISION | Intercept (rho) of decision function |
| n_features | INTEGER | Number of features used |
| feature_columns | VARCHAR | Names of feature columns |

Model output contains support vectors and parameters for prediction by TD_OneClassSVMPredict.

### Code Examples

**Input Data: transaction_features**
```
transaction_id  amount  merchant_category  time_of_day  distance_from_home  transaction_speed
1               45.50   5                  14.5         2.3                 0.8
2               120.00  8                  20.0         15.7                1.2
3               25.75   5                  12.0         1.1                 0.5
4               8500.00 12                 3.5          250.0               10.5  -- ANOMALY
5               67.20   3                  18.0         5.2                 0.9
```

**Example 1: Basic Anomaly Detection with RBF Kernel**
```sql
-- Train One-Class SVM on normal transactions
CREATE VOLATILE TABLE fraud_detector AS (
    SELECT * FROM TD_OneClassSVM (
        ON transaction_features AS InputTable PARTITION BY ANY
        USING
        TargetColumns('amount', 'merchant_category', 'time_of_day',
                      'distance_from_home', 'transaction_speed')
        KernelType('RBF')
        Nu(0.05)  -- Expect ~5% outliers
        Gamma(0.1)
        Seed(42)
        Accumulate('transaction_id')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Model learns normal transaction patterns
-- Identifies transactions far from normal behavior as fraud
```

**Example 2: Sensitive Anomaly Detection with Low Nu**
```sql
-- Very sensitive to outliers (tight boundary)
CREATE VOLATILE TABLE sensitive_detector AS (
    SELECT * FROM TD_OneClassSVM (
        ON sensor_readings AS InputTable PARTITION BY ANY
        USING
        TargetColumns('temperature', 'pressure', 'vibration', 'rpm')
        KernelType('RBF')
        Nu(0.01)  -- Only 1% of training data as outliers (very tight)
        Gamma(0.2)
        Seed(123)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Catches even small deviations from normal
-- Use when anomalies are rare and costly (e.g., equipment failure)
```

**Example 3: Linear Kernel for High-Dimensional Data**
```sql
-- Fast training with linear kernel
CREATE VOLATILE TABLE linear_anomaly_detector AS (
    SELECT * FROM TD_OneClassSVM (
        ON network_traffic AS InputTable PARTITION BY ANY
        USING
        TargetColumns('[1:50]')  -- 50 traffic features
        KernelType('LINEAR')  -- Faster for high-dimensional data
        Nu(0.1)
        Seed(42)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Linear kernel suitable for sparse, high-dimensional data
-- Common in text, network, and log data
```

**Example 4: Polynomial Kernel for Non-Linear Patterns**
```sql
-- Detect anomalies with polynomial decision boundary
CREATE VOLATILE TABLE poly_detector AS (
    SELECT * FROM TD_OneClassSVM (
        ON manufacturing_data AS InputTable PARTITION BY ANY
        USING
        TargetColumns('dimension1', 'dimension2', 'dimension3', 'hardness', 'weight')
        KernelType('POLY')
        Degree(3)  -- Cubic polynomial
        Gamma(0.1)
        Coef0(1.0)
        Nu(0.05)
        Seed(42)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Polynomial boundaries capture complex non-linear normal regions
```

**Example 5: Complete Workflow - Train and Predict**
```sql
-- Step 1: Standardize features (critical for SVM)
CREATE VOLATILE TABLE scale_fit AS (
    SELECT * FROM TD_ScaleFit (
        ON normal_transactions AS InputTable
        OUT VOLATILE TABLE OutputTable(scaler_model)
        USING
        TargetColumns('amount', 'time_of_day', 'distance', 'frequency')
        ScaleMethod('STD')  -- Standardize to mean=0, std=1
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

CREATE VOLATILE TABLE transactions_scaled AS (
    SELECT * FROM TD_ScaleTransform (
        ON all_transactions AS InputTable
        ON scaler_model AS ModelTable DIMENSION
        USING
        Accumulate('transaction_id', 'timestamp', 'customer_id')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 2: Train One-Class SVM on normal scaled data
CREATE VOLATILE TABLE anomaly_model AS (
    SELECT * FROM TD_OneClassSVM (
        ON transactions_scaled AS InputTable PARTITION BY ANY
        USING
        TargetColumns('amount_scaled', 'time_of_day_scaled',
                      'distance_scaled', 'frequency_scaled')
        KernelType('RBF')
        Nu(0.05)
        Gamma(0.1)
        Seed(42)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 3: Predict anomalies on new data (after scaling)
CREATE VOLATILE TABLE anomaly_predictions AS (
    SELECT * FROM TD_OneClassSVMPredict (
        ON transactions_scaled AS InputTable PARTITION BY ANY
        ON anomaly_model AS ModelTable DIMENSION
        USING
        IDColumn('transaction_id')
        Accumulate('customer_id', 'timestamp', 'amount')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 4: Analyze anomalies
SELECT
    customer_id,
    transaction_id,
    timestamp,
    amount,
    prediction,  -- 1 = normal, -1 = anomaly
    decision_function  -- Distance from boundary (negative = anomaly)
FROM anomaly_predictions
WHERE prediction = -1  -- Anomalies only
ORDER BY decision_function ASC;  -- Most anomalous first
```

**Example 6: Equipment Failure Detection**
```sql
-- Detect abnormal equipment sensor readings
CREATE VOLATILE TABLE equipment_monitor AS (
    SELECT * FROM TD_OneClassSVM (
        ON normal_sensor_data AS InputTable PARTITION BY ANY
        USING
        TargetColumns('motor_temperature', 'bearing_vibration', 'oil_pressure',
                      'rpm', 'current_draw', 'noise_level')
        KernelType('RBF')
        Nu(0.02)  -- Very sensitive (2% outliers)
        Gamma(0.15)
        Seed(42)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Predict and alert on new sensor readings
-- prediction = -1 triggers maintenance alert
```

**Example 7: Network Intrusion Detection**
```sql
-- Learn normal network traffic patterns
CREATE VOLATILE TABLE intrusion_detector AS (
    SELECT * FROM TD_OneClassSVM (
        ON normal_network_traffic AS InputTable PARTITION BY ANY
        USING
        TargetColumns('packet_size', 'packets_per_second', 'connection_duration',
                      'failed_logins', 'root_accesses', 'num_shells')
        KernelType('RBF')
        Nu(0.01)  -- Tight boundary (security critical)
        Gamma(0.1)
        CacheSize(500)  -- Large cache for faster training
        Seed(42)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Real-time intrusion detection
-- Catches novel attack patterns not seen before
```

**Example 8: Credit Card Fraud with Hyperparameter Tuning**
```sql
-- Test multiple Nu values to find optimal sensitivity
CREATE VOLATILE TABLE fraud_model_nu001 AS (
    SELECT * FROM TD_OneClassSVM (
        ON normal_transactions AS InputTable PARTITION BY ANY
        USING
        TargetColumns('amount', 'merchant_cat', 'location', 'time')
        KernelType('RBF')
        Nu(0.01)
        Gamma(0.1)
        Seed(42)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

CREATE VOLATILE TABLE fraud_model_nu005 AS (
    SELECT * FROM TD_OneClassSVM (
        ON normal_transactions AS InputTable PARTITION BY ANY
        USING
        TargetColumns('amount', 'merchant_cat', 'location', 'time')
        KernelType('RBF')
        Nu(0.05)
        Gamma(0.1)
        Seed(42)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Compare models on validation set
-- Choose model balancing false positives vs false negatives
```

**Example 9: Medical Anomaly Detection**
```sql
-- Identify unusual patient test results
CREATE VOLATILE TABLE medical_anomaly_detector AS (
    SELECT * FROM TD_OneClassSVM (
        ON normal_patient_tests AS InputTable PARTITION BY ANY
        USING
        TargetColumns('blood_pressure', 'heart_rate', 'temperature',
                      'white_blood_cell_count', 'glucose', 'cholesterol')
        KernelType('RBF')
        Nu(0.05)
        Gamma(0.1)
        Seed(42)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Flags patients with unusual combination of test results
-- Even if individual values are within normal ranges
```

**Example 10: Quality Control in Manufacturing**
```sql
-- Detect defective products based on measurements
CREATE VOLATILE TABLE quality_control_model AS (
    SELECT * FROM TD_OneClassSVM (
        ON good_products AS InputTable PARTITION BY ANY
        USING
        TargetColumns('length', 'width', 'height', 'weight',
                      'surface_roughness', 'hardness', 'color_value')
        KernelType('RBF')
        Nu(0.03)  -- 3% defect rate expected
        Gamma(0.2)
        Tolerance(0.0001)  -- High precision for quality control
        Seed(42)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Real-time quality inspection
-- Automatically flags defects for manual inspection
```

### Algorithm Details

**One-Class SVM Formulation:**

The algorithm finds a hyperplane that separates the normal data from the origin in feature space, with maximum margin.

**Optimization Problem:**
```
Minimize: (1/2) ||w||² - ρ + (1/(n·Nu)) Σᵢ ξᵢ

Subject to:
  w · φ(xᵢ) ≥ ρ - ξᵢ
  ξᵢ ≥ 0

Where:
- w: weight vector defining hyperplane
- ρ (rho): intercept/offset from origin
- φ(x): kernel-induced feature mapping
- ξᵢ: slack variables allowing some violations
- Nu: controls trade-off between margin size and violations
```

**Decision Function:**

For a new point x, the anomaly score is:
```
f(x) = sign(Σᵢ αᵢ K(xᵢ, x) - ρ)

Where:
- αᵢ: dual coefficients (Lagrange multipliers)
- K(xᵢ, x): kernel function
- xᵢ: support vectors
- ρ: intercept

Interpretation:
- f(x) = 1: Normal (inside boundary)
- f(x) = -1: Anomaly (outside boundary)
- |f(x)|: Distance from boundary (confidence)
```

**Kernel Functions:**

**RBF (Radial Basis Function):**
```
K(x, y) = exp(-gamma * ||x - y||²)

- Creates circular/spherical boundaries
- Gamma controls influence radius
- Most versatile kernel for anomaly detection
```

**Linear:**
```
K(x, y) = x · y

- Computes dot product in original space
- Fast and memory-efficient
- Best for linearly separable normal regions
```

**Polynomial:**
```
K(x, y) = (gamma * x · y + Coef0)^Degree

- Creates polynomial decision boundaries
- Degree controls complexity
- Good for polynomial patterns
```

**Sigmoid:**
```
K(x, y) = tanh(gamma * x · y + Coef0)

- Similar to neural network activation
- Less common for One-Class SVM
```

**Nu Parameter Interpretation:**

Nu has two interpretations:
1. **Upper bound** on fraction of outliers (training errors)
2. **Lower bound** on fraction of support vectors

```
If Nu = 0.1:
- At most 10% of training points will be misclassified
- At least 10% of training points will be support vectors

Smaller Nu → Tighter boundary, fewer outliers tolerated
Larger Nu → Looser boundary, more outliers tolerated
```

**Support Vectors:**

Support vectors are training points that define the decision boundary:
- Points on the boundary (αᵢ > 0, ξᵢ = 0)
- Points violating margin (αᵢ > 0, ξᵢ > 0)

Only support vectors affect predictions, making the model memory-efficient.

### Use Cases and Applications

**1. Financial Fraud Detection**
- Credit card fraud identification
- Insurance claim fraud detection
- Money laundering detection
- Trading anomaly detection
- Account takeover detection
- Payment fraud prevention

**2. Cybersecurity and Intrusion Detection**
- Network intrusion detection
- DDoS attack identification
- Malware detection
- Zero-day exploit detection
- Insider threat detection
- Anomalous user behavior detection

**3. Equipment and Predictive Maintenance**
- Industrial equipment failure prediction
- Vehicle diagnostics and failure prediction
- HVAC system anomaly detection
- Turbine and generator monitoring
- Pump and motor condition monitoring
- Bearing failure prediction

**4. Healthcare and Medical Diagnosis**
- Rare disease detection
- Unusual patient condition identification
- Medical image anomaly detection
- Drug response anomaly detection
- Vital sign monitoring and alerting
- Epidemic outbreak detection

**5. Quality Control and Manufacturing**
- Defective product detection
- Process anomaly identification
- Material defect detection
- Assembly line quality monitoring
- Pharmaceutical batch quality control
- Semiconductor wafer defect detection

**6. Network and System Monitoring**
- Server performance anomaly detection
- Application performance monitoring
- Log anomaly detection
- Resource usage anomaly detection
- API abuse detection
- Database query anomaly detection

**7. IoT and Sensor Monitoring**
- Smart home anomaly detection
- Environmental sensor monitoring
- Industrial IoT anomaly detection
- Vehicle sensor anomaly detection
- Agricultural sensor monitoring
- Energy grid monitoring

**8. E-Commerce and Retail**
- Fake review detection
- Bot account identification
- Unusual purchasing behavior detection
- Inventory anomaly detection
- Pricing anomaly detection
- Supply chain disruption detection

**9. Telecommunications**
- Call fraud detection
- Network traffic anomaly detection
- Service outage detection
- Customer churn early warning
- Roaming fraud detection
- SIM card cloning detection

**10. Environmental and Safety Monitoring**
- Pollution level anomaly detection
- Natural disaster early warning
- Radiation level monitoring
- Air quality anomaly detection
- Water quality monitoring
- Seismic activity anomaly detection

### Important Notes

**Feature Scaling is Critical:**
- One-Class SVM is extremely sensitive to feature scales
- **ALWAYS standardize features** before training (mean=0, std=1)
- Use TD_ScaleFit with ScaleMethod='STD'
- Failure to scale leads to poor performance
- Features with larger scales dominate the model

**Training Data Should Be Normal:**
- Training data should represent normal/typical behavior
- Contamination with anomalies degrades performance
- If possible, manually verify training data is clean
- Use outlier detection methods to clean training data first
- Nu parameter should match expected contamination rate

**Nu Parameter Selection:**
- Critical hyperparameter requiring domain knowledge
- Start with Nu matching expected anomaly rate
- Nu = 0.01: Very tight, expect 1% anomalies (high precision, low recall)
- Nu = 0.1: Moderate, expect 10% anomalies (balanced)
- Nu = 0.2: Loose, expect 20% anomalies (high recall, low precision)
- Tune based on false positive/false negative trade-off

**Gamma Parameter Tuning:**
- For RBF kernel, Gamma is critical hyperparameter
- **Too small**: Underfitting (boundary too smooth)
- **Too large**: Overfitting (boundary too complex)
- Default (1/n_features) is reasonable starting point
- Use cross-validation or held-out validation set to tune
- Rule of thumb: Gamma ~ 1 / (n_features * variance_of_features)

**Kernel Selection:**
- **RBF**: Default choice, works for most problems
- **Linear**: Use for high-dimensional sparse data (text, log data)
- **Polynomial**: Use if domain knowledge suggests polynomial patterns
- **Sigmoid**: Rarely used, similar to RBF
- When in doubt, start with RBF kernel

**Computational Complexity:**
- Training: O(n² × d) where n = samples, d = features (can be slow for large n)
- Prediction: O(n_support_vectors × d) (typically much faster)
- Memory: Stores only support vectors (typically 10-30% of training data)
- Use CacheSize to trade memory for speed during training

**Anomaly Score Interpretation:**
- Prediction: 1 = normal, -1 = anomaly
- Decision function value: distance from boundary
  - Large positive → Clearly normal
  - Near zero → On boundary (uncertain)
  - Large negative → Clearly anomalous
- Rank anomalies by decision function for prioritization

**Evaluation Challenges:**
- Labeled anomaly data often unavailable for evaluation
- Precision/recall/F1 require labeled test set
- Use domain expert validation on detected anomalies
- Monitor false positive rate (normal flagged as anomaly)
- Track business metrics (fraud caught, failures prevented)

**Class Imbalance:**
- One-Class SVM designed for severe class imbalance
- Learns from normal class only
- Doesn't require anomaly examples during training
- Ideal when anomalies are rare (<1%) and varied
- Alternative to standard binary classification for extreme imbalance

**Model Updating:**
- Retrain periodically as normal behavior evolves
- Concept drift: normal patterns change over time
- Use sliding time windows for training
- Monitor false positive rate to detect drift
- Incremental learning not supported (requires full retraining)

### Best Practices

**1. Always Standardize Features**
- Use TD_ScaleFit with ScaleMethod='STD' before training
- Critical for SVM performance
- Apply same scaling to prediction data
- Verify mean ≈ 0, std ≈ 1 after scaling
- Include scaling in production pipeline

**2. Curate Training Data Carefully**
- Ensure training data represents normal behavior only
- Remove known anomalies from training set
- Use domain knowledge to validate training data
- Consider using TD_OutlierFilterFit to pre-clean data
- Larger, cleaner training set → better model

**3. Tune Nu Based on Domain Knowledge**
- Estimate expected anomaly rate from domain expertise
- Set Nu slightly above expected rate
- Too low Nu → Overfitting, too many false positives
- Too high Nu → Underfitting, misses anomalies
- Validate on hold-out set with labeled anomalies if available

**4. Hyperparameter Tuning Strategy**
- Start with RBF kernel and default Gamma (1/n_features)
- Fix Nu based on domain knowledge
- Grid search Gamma: [0.001, 0.01, 0.1, 1.0, 10.0]
- Evaluate on validation set with known anomalies
- Balance precision (minimize false positives) vs recall (catch anomalies)

**5. Use Decision Function for Ranking**
- Don't just use binary prediction (normal/anomaly)
- Rank all points by decision function value
- Prioritize most anomalous (most negative) for investigation
- Set dynamic thresholds based on capacity for investigation
- Provides flexibility in production deployment

**6. Monitor and Retrain**
- Track false positive rate over time
- Sudden increase indicates concept drift (normal behavior changed)
- Retrain periodically (monthly, quarterly, depending on domain)
- Use recent data for retraining to adapt to changes
- Maintain A/B testing framework for model updates

**7. Combine with Domain Rules**
- One-Class SVM is data-driven, may miss domain-specific anomalies
- Combine with rule-based checks for known anomalies
- Use SVM for unknown/novel anomaly detection
- Ensemble approach: rules + One-Class SVM
- Leverage both statistical and domain knowledge

**8. Handle False Positives**
- Expect some false positives (normal flagged as anomaly)
- Set up feedback loop to label false positives
- Retrain excluding false positives or increasing Nu
- Use human-in-the-loop for final decisions
- Document false positive patterns for future improvements

**9. Validate with Domain Experts**
- Have experts review detected anomalies
- Build trust through validated true positives
- Learn from false positives to improve model
- Incorporate domain feedback into retraining
- Treat as collaboration between ML and domain expertise

**10. Production Deployment Strategy**
- Start with conservative threshold (low false positive rate)
- Gradually increase sensitivity based on feedback
- Implement alerting and investigation workflows
- Monitor latency and throughput in production
- Maintain rollback capability to previous model
- A/B test new models before full deployment

### Related Functions

**Model Training:**
- **TD_SVM** - Two-class or multi-class SVM for supervised classification
- **TD_IsolationForest** - Alternative tree-based anomaly detection
- **TD_OutlierFilterFit** - Statistical outlier detection for data cleaning
- **TD_LOF** - Local Outlier Factor for density-based anomaly detection

**Model Scoring:**
- **TD_OneClassSVMPredict** - Apply trained One-Class SVM model to new data

**Feature Preparation:**
- **TD_ScaleFit** - CRITICAL: Standardize features before training
- **TD_ScaleTransform** - Apply scaling to new data
- **TD_SimpleImputeFit** - Handle missing values
- **TD_PCA** - Reduce dimensionality before anomaly detection

**Model Evaluation:**
- **TD_ClassificationEvaluator** - Compute metrics (requires labeled anomalies)
- **TD_ROC** - ROC curve analysis (requires labeled test set)
- **TD_ConfusionMatrix** - Confusion matrix for binary classification

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf
- [One-Class SVM - Scikit-learn Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.svm.OneClassSVM.html)
- [Anomaly Detection with One-Class SVM](https://en.wikipedia.org/wiki/One-class_classification)
- [Support Vector Machines - StatQuest](https://www.youtube.com/watch?v=efR1C6CvhmE)

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Model Training Functions (Anomaly Detection)
