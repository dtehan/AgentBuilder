# TD_SVM

### Function Name
**TD_SVM**

### Description
TD_SVM trains a Support Vector Machine classifier for binary and multi-class classification tasks, finding the optimal hyperplane that maximizes the margin between classes in high-dimensional feature space. This supervised learning algorithm excels at creating robust decision boundaries by focusing on support vectors (training samples closest to the decision boundary), making it less susceptible to outliers and effective even with limited training data. SVM transforms input features using kernel functions (RBF, Linear, Polynomial, Sigmoid) to map non-linearly separable data into higher dimensions where linear separation becomes possible, enabling complex non-linear classification boundaries while maintaining mathematical elegance and strong theoretical foundations.

The algorithm works by finding the hyperplane that maximizes the distance (margin) to the nearest training samples of each class, which is mathematically proven to provide good generalization to unseen data. TD_SVM uses the C parameter to control the trade-off between maximizing the margin and minimizing classification errors - smaller C values create wider margins but tolerate more misclassifications (regularization), while larger C values enforce stricter classification but risk overfitting. For multi-class problems, SVM uses a one-vs-one or one-vs-all strategy to decompose the problem into multiple binary classifications. The model stores only support vectors (typically 10-40% of training data), making predictions memory-efficient and fast despite the complexity of the decision boundary.

TD_SVM is particularly effective for medium-sized datasets (thousands to hundreds of thousands of samples) with complex decision boundaries, high-dimensional feature spaces (where curse of dimensionality affects other algorithms), and applications requiring strong theoretical guarantees on generalization performance. It handles non-linear patterns naturally through kernel transformations without requiring explicit feature engineering, provides interpretable support vectors that define the decision boundary, and offers probabilistic outputs for ranking and confidence estimation. While SVM requires careful feature scaling and hyperparameter tuning, it consistently delivers state-of-the-art performance on diverse classification tasks from image recognition to text classification, bioinformatics, fraud detection, and medical diagnosis.

### When the Function Would Be Used
- **Binary Classification**: Two-class classification with complex decision boundaries
- **Multi-Class Classification**: Classify among multiple categories or labels
- **Image Classification**: Recognize objects, faces, handwriting, medical images
- **Text Classification**: Categorize documents, emails, sentiment analysis
- **Bioinformatics**: Gene classification, protein structure prediction, disease diagnosis
- **Fraud Detection**: Identify fraudulent vs legitimate transactions
- **Medical Diagnosis**: Disease classification from symptoms and test results
- **Credit Scoring**: Approve/reject credit applications based on risk
- **Face Recognition**: Identify individuals from facial features
- **Handwriting Recognition**: OCR and digit recognition
- **Spam Filtering**: Classify emails as spam or legitimate
- **Customer Churn Prediction**: Predict which customers will churn
- **Sentiment Analysis**: Classify text sentiment as positive/negative/neutral
- **Gene Expression Analysis**: Classify cancer subtypes from gene data
- **Remote Sensing**: Classify land use from satellite imagery
- **Quality Control**: Classify products as defective or acceptable
- **Network Intrusion Detection**: Classify network traffic as normal or attack
- **Voice Recognition**: Classify spoken words or speaker identity
- **Financial Market Prediction**: Classify market movements
- **Recommender Systems**: Classify user preferences for recommendations
- **Anomaly Detection**: Classify normal vs anomalous behavior (with One-Class SVM)
- **Chemical Compound Classification**: Predict compound properties
- **Protein Function Prediction**: Classify protein functions from structure
- **Weather Pattern Classification**: Classify weather conditions or forecasts

### Syntax

```sql
TD_SVM (
    ON { table | view | (query) } AS InputTable PARTITION BY ANY
    USING
    ResponseColumn ('response_column')
    InputColumns ({ 'input_column' | input_column_range }[,...])
    [ KernelType ({ 'RBF' | 'LINEAR' | 'POLY' | 'SIGMOID' }) ]
    [ Cost (c_value) ]
    [ Gamma (gamma_value) ]
    [ Degree (degree_value) ]
    [ Coef0 (coef0_value) ]
    [ CacheSize (cache_mb) ]
    [ Tolerance (tolerance_value) ]
    [ MaxIterNum (max_iterations) ]
    [ Seed (random_seed) ]
    [ Probability ({'true' | 'false'}) ]
    [ ClassWeights ('class:weight' [,...]) ]
    [ Accumulate ({ 'accumulate_column' | accumulate_column_range }[,...]) ]
) AS alias
```

### Required Syntax Elements for TD_SVM

**ON clause (InputTable)**
- Training data with features and class labels
- PARTITION BY ANY for distributed parallel training
- Must contain labeled examples from all classes

**ResponseColumn**
- Column containing class labels
- Can be INTEGER, VARCHAR, or any data type
- For binary classification: 2 distinct values (e.g., 0/1, 'yes'/'no')
- For multi-class: 3+ distinct values
- Must not contain NULL values

**InputColumns**
- Feature columns to use for classification
- Must be numeric data types (INTEGER, DOUBLE PRECISION, etc.)
- Supports column range notation ('[1:10]')
- Multiple columns define the feature space

### Optional Syntax Elements for TD_SVM

**KernelType**
- Kernel function for feature transformation
- **'RBF'** (Radial Basis Function): Gaussian kernel for non-linear boundaries
  - Most versatile, default choice
  - Creates smooth, circular decision boundaries
  - Best for most non-linear classification problems
- **'LINEAR'**: Linear kernel for linear boundaries
  - Fastest training and prediction
  - Best for linearly separable data or high-dimensional sparse features
  - Equivalent to logistic regression but with maximum margin
- **'POLY'**: Polynomial kernel for polynomial decision boundaries
  - Good for non-linear patterns with polynomial structure
  - Controlled by Degree parameter
- **'SIGMOID'**: Sigmoid/tanh kernel
  - Similar to neural network activation
  - Less commonly used than RBF
- Default: 'RBF'

**Cost (C parameter)**
- Regularization parameter controlling margin vs misclassification trade-off
- Range: C > 0 (typically 0.001 to 1000)
- **Smaller C** (e.g., 0.01-1): Wider margin, more regularization, tolerates errors
  - More robust to outliers
  - Better generalization
  - Risk of underfitting
- **Larger C** (e.g., 10-1000): Narrower margin, less regularization, enforces accuracy
  - Fits training data more tightly
  - Risk of overfitting
- Default: 1.0

**Gamma**
- Kernel coefficient for RBF, POLY, and SIGMOID kernels
- Controls influence range of individual training examples:
  - **Smaller Gamma** (e.g., 0.001-0.01): Broader influence, smoother boundary
  - **Larger Gamma** (e.g., 1-10): Narrower influence, more complex boundary
- For RBF kernel: gamma = 1 / (2 * σ²) where σ is the Gaussian width
- Default: 1 / n_features (automatically calculated)
- Critical hyperparameter requiring tuning

**Degree**
- Polynomial degree for POLY kernel
- Defines order of polynomial transformation
- Range: positive integers (typically 2-5)
- Degree=2: Quadratic decision boundary
- Degree=3: Cubic decision boundary
- Higher degree → more complex boundaries
- Default: 3

**Coef0**
- Independent coefficient term in POLY and SIGMOID kernels
- Affects kernel calculation: (gamma * <x, y> + Coef0)^Degree
- Influences balance between high-degree and low-degree terms
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
- Use same seed for deterministic behavior

**Probability**
- Whether to enable probability estimation
- **'true'**: Enables probabilistic outputs (additional computational cost)
- **'false'**: Only class predictions (faster)
- Probability estimates use Platt scaling calibration
- Default: 'false'

**ClassWeights**
- Specify misclassification penalties for each class
- Format: 'class1:weight1', 'class2:weight2', ...
- Larger weight → greater penalty for misclassifying that class
- Useful for imbalanced datasets
- Default: uniform weights (1.0 for all classes)

**Accumulate**
- Columns to copy from input to output unchanged
- Useful for preserving identifiers, timestamps, metadata

### Input Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| response_column | ANY | Class labels (no NULLs) |
| input_column | NUMERIC (INTEGER, BIGINT, DOUBLE PRECISION, DECIMAL) | Feature columns for classification |
| accumulate_column | ANY | [Optional] Columns to preserve in output |

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| model_id | INTEGER | Model identifier |
| kernel_type | VARCHAR | Kernel used: RBF, LINEAR, POLY, SIGMOID |
| cost | DOUBLE PRECISION | C parameter used for training |
| gamma | DOUBLE PRECISION | Gamma parameter (NULL for LINEAR) |
| degree | INTEGER | Polynomial degree (NULL for non-POLY) |
| coef0 | DOUBLE PRECISION | Coefficient term (NULL for RBF and LINEAR) |
| n_classes | INTEGER | Number of classes in classification |
| classes | VARCHAR (JSON) | List of class labels |
| n_support_vectors | INTEGER | Total number of support vectors |
| support_vectors_per_class | VARCHAR (JSON) | Support vector counts per class |
| support_vector_indices | VARCHAR (JSON) | Indices of support vectors from training data |
| support_vectors | VARCHAR (JSON) | Support vector feature values |
| dual_coefficients | VARCHAR (JSON) | Alpha coefficients for support vectors |
| intercepts | VARCHAR (JSON) | Intercepts for decision functions |
| n_features | INTEGER | Number of features used |
| feature_columns | VARCHAR | Names of feature columns |
| probability_enabled | BOOLEAN | Whether probability estimation is enabled |

Model output contains support vectors and parameters for prediction by TD_SVMPredict.

### Code Examples

**Input Data: customer_data**
```
customer_id  age  income  purchases  support_calls  tenure_months  churned
1            35   65000   12         2              24             0
2            28   45000   3          8              6              1
3            42   85000   25         1              48             0
4            31   50000   5          10             8              1
5            55   95000   40         0              72             0
```

**Example 1: Binary Classification with RBF Kernel**
```sql
-- Train SVM classifier for customer churn
CREATE VOLATILE TABLE churn_model AS (
    SELECT * FROM TD_SVM (
        ON customer_train AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('churned')
        InputColumns('age', 'income', 'purchases', 'support_calls', 'tenure_months')
        KernelType('RBF')
        Cost(1.0)
        Gamma(0.1)
        Seed(42)
        Accumulate('customer_id')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Creates maximum-margin decision boundary between churned and non-churned
```

**Example 2: Linear SVM for High-Dimensional Data**
```sql
-- Fast linear SVM for text classification
CREATE VOLATILE TABLE text_classifier AS (
    SELECT * FROM TD_SVM (
        ON document_features AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('category')
        InputColumns('[1:1000]')  -- 1000 TF-IDF features
        KernelType('LINEAR')  -- Efficient for high-dimensional sparse features
        Cost(0.1)  -- Lower C for regularization
        Seed(42)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Linear kernel ideal for text and high-dimensional data
```

**Example 3: Multi-Class Classification**
```sql
-- Classify iris species (3 classes)
CREATE VOLATILE TABLE iris_classifier AS (
    SELECT * FROM TD_SVM (
        ON iris_train AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('species')  -- 'setosa', 'versicolor', 'virginica'
        InputColumns('sepal_length', 'sepal_width', 'petal_length', 'petal_width')
        KernelType('RBF')
        Cost(1.0)
        Gamma(0.5)
        Seed(42)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Automatically handles multi-class with one-vs-one strategy
```

**Example 4: SVM with Probability Estimation**
```sql
-- Enable probabilistic outputs for ranking
CREATE VOLATILE TABLE fraud_classifier AS (
    SELECT * FROM TD_SVM (
        ON transactions_train AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('is_fraud')
        InputColumns('amount', 'merchant_category', 'time_of_day', 'location')
        KernelType('RBF')
        Cost(10.0)  -- High C for accuracy (fraud is critical)
        Gamma(0.1)
        Probability('true')  -- Enable probability estimates
        Seed(42)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Predictions include probability estimates for fraud vs legitimate
```

**Example 5: Handling Imbalanced Data with Class Weights**
```sql
-- Address class imbalance (1% fraud, 99% legitimate)
CREATE VOLATILE TABLE fraud_model AS (
    SELECT * FROM TD_SVM (
        ON transactions AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('is_fraud')  -- 0=legitimate, 1=fraud
        InputColumns('amount', 'merchant_category', 'location', 'time_of_day')
        KernelType('RBF')
        Cost(1.0)
        Gamma(0.1)
        ClassWeights('0:1.0', '1:99.0')  -- 99x penalty for missing fraud
        Seed(42)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Higher weight on minority class improves recall
```

**Example 6: Polynomial Kernel for Non-Linear Boundaries**
```sql
-- Capture polynomial decision boundaries
CREATE VOLATILE TABLE quality_classifier AS (
    SELECT * FROM TD_SVM (
        ON product_measurements AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('quality_class')  -- 'pass', 'fail'
        InputColumns('dimension1', 'dimension2', 'dimension3', 'weight', 'hardness')
        KernelType('POLY')
        Degree(2)  -- Quadratic decision boundary
        Cost(1.0)
        Gamma(0.1)
        Coef0(1.0)
        Seed(42)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Polynomial kernel captures curved decision boundaries
```

**Example 7: Complete Workflow - Scale, Train, Predict, Evaluate**
```sql
-- Step 1: Standardize features (CRITICAL for SVM)
CREATE VOLATILE TABLE scale_fit AS (
    SELECT * FROM TD_ScaleFit (
        ON customer_train AS InputTable
        OUT VOLATILE TABLE OutputTable(scaler_model)
        USING
        TargetColumns('age', 'income', 'purchases', 'support_calls', 'tenure_months')
        ScaleMethod('STD')  -- Standardize to mean=0, std=1
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

CREATE VOLATILE TABLE customer_train_scaled AS (
    SELECT * FROM TD_ScaleTransform (
        ON customer_train AS InputTable
        ON scaler_model AS ModelTable DIMENSION
        USING
        Accumulate('customer_id', 'churned')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

CREATE VOLATILE TABLE customer_test_scaled AS (
    SELECT * FROM TD_ScaleTransform (
        ON customer_test AS InputTable
        ON scaler_model AS ModelTable DIMENSION
        USING
        Accumulate('customer_id', 'churned')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 2: Train SVM model on scaled data
CREATE VOLATILE TABLE churn_model AS (
    SELECT * FROM TD_SVM (
        ON customer_train_scaled AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('churned')
        InputColumns('age_scaled', 'income_scaled', 'purchases_scaled',
                     'support_calls_scaled', 'tenure_months_scaled')
        KernelType('RBF')
        Cost(1.0)
        Gamma(0.1)
        Probability('true')
        Seed(42)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 3: Make predictions on test data
CREATE VOLATILE TABLE churn_predictions AS (
    SELECT * FROM TD_SVMPredict (
        ON customer_test_scaled AS InputTable PARTITION BY ANY
        ON churn_model AS ModelTable DIMENSION
        USING
        IDColumn('customer_id')
        Accumulate('churned')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 4: Evaluate model performance
SELECT * FROM TD_ClassificationEvaluator (
    ON churn_predictions AS InputTable
    USING
    ObservationColumn('churned')
    PredictionColumn('prediction')
) AS dt;

-- Returns accuracy, precision, recall, F1-score, confusion matrix
```

**Example 8: Hyperparameter Grid Search**
```sql
-- Test multiple Cost and Gamma combinations
CREATE VOLATILE TABLE model_c01_g01 AS (
    SELECT * FROM TD_SVM (
        ON train_data AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('class')
        InputColumns('feature1', 'feature2', 'feature3')
        KernelType('RBF')
        Cost(0.1)
        Gamma(0.1)
        Seed(42)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

CREATE VOLATILE TABLE model_c10_g01 AS (
    SELECT * FROM TD_SVM (
        ON train_data AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('class')
        InputColumns('feature1', 'feature2', 'feature3')
        KernelType('RBF')
        Cost(10.0)
        Gamma(0.1)
        Seed(42)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Predict and evaluate each model on validation set
-- Choose model with best F1-score or accuracy
```

**Example 9: Medical Diagnosis Classification**
```sql
-- Classify disease from patient test results
CREATE VOLATILE TABLE diagnosis_model AS (
    SELECT * FROM TD_SVM (
        ON patient_records AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('diagnosis')  -- 'healthy', 'type1_diabetes', 'type2_diabetes'
        InputColumns('glucose', 'blood_pressure', 'bmi', 'age', 'family_history')
        KernelType('RBF')
        Cost(1.0)
        Gamma(0.2)
        Probability('true')  -- Get confidence for medical decisions
        Seed(42)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Multi-class medical diagnosis with probability estimates
```

**Example 10: Image Classification (Feature-Based)**
```sql
-- Classify images from extracted features
CREATE VOLATILE TABLE image_classifier AS (
    SELECT * FROM TD_SVM (
        ON image_features AS InputTable PARTITION BY ANY
        USING
        ResponseColumn('image_category')  -- 'cat', 'dog', 'bird', 'fish'
        InputColumns('[1:128]')  -- 128 image feature dimensions
        KernelType('RBF')
        Cost(10.0)
        Gamma(0.05)
        Probability('true')
        Seed(42)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Multi-class image classification from feature vectors
```

### Algorithm Details

**Support Vector Machine Formulation:**

SVM finds the optimal hyperplane that maximizes the margin between classes.

**Optimization Problem (Binary Classification):**
```
Minimize: (1/2) ||w||² + C Σᵢ ξᵢ

Subject to:
  yᵢ(w · φ(xᵢ) + b) ≥ 1 - ξᵢ
  ξᵢ ≥ 0

Where:
- w: weight vector defining hyperplane
- b: bias/intercept
- φ(x): kernel-induced feature mapping
- ξᵢ: slack variables (allow misclassifications)
- C: cost parameter (regularization)
- yᵢ ∈ {-1, +1}: class labels
```

**Decision Function:**

For a new point x, the predicted class is:
```
f(x) = sign(Σᵢ αᵢ yᵢ K(xᵢ, x) + b)

Where:
- αᵢ: dual coefficients (Lagrange multipliers)
- yᵢ: class labels of support vectors
- K(xᵢ, x): kernel function
- xᵢ: support vectors
- b: intercept

Interpretation:
- f(x) > 0: Predict class +1
- f(x) < 0: Predict class -1
- |f(x)|: Distance from hyperplane (confidence)
```

**Kernel Functions:**

**RBF (Radial Basis Function):**
```
K(x, y) = exp(-gamma * ||x - y||²)

- Maps to infinite-dimensional space
- Creates non-linear decision boundaries
- Most versatile kernel
- Gamma controls locality of influence
```

**Linear:**
```
K(x, y) = x · y

- Dot product in original space
- Creates linear decision boundary
- Fastest training and prediction
- Best for linearly separable data
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
- Less common than RBF
```

**Multi-Class Strategy:**

TD_SVM handles multi-class classification using **one-vs-one** approach:
```
For K classes:
- Train K(K-1)/2 binary classifiers
- Each classifier trained on pair of classes
- Prediction uses majority voting

Example for 3 classes (A, B, C):
- Train classifier: A vs B
- Train classifier: A vs C
- Train classifier: B vs C
- Predict: vote from all 3 classifiers
```

**Support Vectors:**

Support vectors are training points that lie on or within the margin:
- Points on margin (αᵢ > 0, ξᵢ = 0): Define decision boundary
- Points within margin (αᵢ > 0, ξᵢ > 0): Misclassified or close to boundary

Only support vectors affect predictions, making model memory-efficient.

**Margin:**

The margin is the distance between the hyperplane and nearest point:
```
Margin = 2 / ||w||

Maximizing margin is equivalent to minimizing ||w||²
Larger margin → Better generalization to unseen data
```

**Cost Parameter (C) Interpretation:**

C controls the trade-off between margin size and classification errors:
```
Small C (e.g., 0.1):
- Wider margin (more regularization)
- Tolerates more misclassifications
- Better generalization, prevents overfitting
- More support vectors

Large C (e.g., 100):
- Narrower margin (less regularization)
- Enforces stricter classification
- Fits training data more tightly
- Fewer support vectors
- Risk of overfitting
```

### Use Cases and Applications

**1. Text and Document Classification**
- Spam detection and email filtering
- News article categorization
- Sentiment analysis of reviews
- Document topic classification
- Language detection
- Author attribution

**2. Image Recognition and Computer Vision**
- Face recognition and verification
- Handwritten digit recognition (OCR)
- Object detection and classification
- Medical image analysis
- Satellite image classification
- Quality inspection from images

**3. Bioinformatics and Genomics**
- Gene expression classification
- Protein structure prediction
- Cancer subtype classification
- Drug response prediction
- Disease diagnosis from biomarkers
- Sequence classification

**4. Financial Services**
- Credit scoring and loan approval
- Fraud detection in transactions
- Stock market prediction
- Customer segmentation
- Risk assessment
- Portfolio management

**5. Healthcare and Medical Diagnosis**
- Disease classification from symptoms
- Cancer detection from imaging
- Drug discovery and response prediction
- Patient risk stratification
- Medical record classification
- Epidemic prediction

**6. Customer Analytics**
- Churn prediction
- Customer lifetime value classification
- Purchase intent prediction
- Segmentation for targeting
- Lead scoring
- Next best action recommendation

**7. Quality Control and Manufacturing**
- Defect detection and classification
- Product quality grading
- Process control and monitoring
- Fault diagnosis
- Predictive maintenance
- Assembly line optimization

**8. Cybersecurity and Network Analysis**
- Intrusion detection systems
- Malware classification
- Network traffic classification
- Anomaly detection
- Phishing detection
- User authentication

**9. Natural Language Processing**
- Part-of-speech tagging
- Named entity recognition
- Intent classification for chatbots
- Question answering systems
- Text summarization
- Machine translation

**10. Remote Sensing and Geospatial Analysis**
- Land use classification
- Crop type identification
- Urban planning and mapping
- Environmental monitoring
- Disaster assessment
- Resource exploration

### Important Notes

**Feature Scaling is CRITICAL:**
- SVM is extremely sensitive to feature scales
- **ALWAYS standardize features** before training
- Use TD_ScaleFit with ScaleMethod='STD'
- Features with larger scales dominate the model
- Failure to scale severely degrades performance

**Cost (C) Parameter Selection:**
- Critical hyperparameter affecting bias-variance trade-off
- Small C (0.01-1): More regularization, simpler model, prevents overfitting
- Large C (10-1000): Less regularization, complex model, risk of overfitting
- Start with C=1.0, then grid search [0.01, 0.1, 1, 10, 100]
- Use cross-validation to select optimal C

**Gamma Parameter Tuning:**
- For RBF kernel, Gamma is second most important hyperparameter
- Small Gamma (0.001-0.01): Smooth, simple decision boundary
- Large Gamma (1-10): Complex, wiggly decision boundary (overfitting risk)
- Default (1/n_features) is reasonable starting point
- Grid search Gamma: [0.001, 0.01, 0.1, 1.0]

**Kernel Selection:**
- **RBF**: Default choice, works for most problems, non-linear boundaries
- **Linear**: Use for high-dimensional sparse data (text, genomics)
- **Polynomial**: Use if domain suggests polynomial patterns
- **Sigmoid**: Rarely used, similar to RBF
- When in doubt, start with RBF kernel

**Class Imbalance Handling:**
- Use ClassWeights to penalize minority class misclassifications
- Set weight proportional to inverse class frequency
- Example: 90% class 0, 10% class 1 → weights '0:1', '1:9'
- Alternative: resample training data (oversample minority, undersample majority)
- Monitor precision/recall, not just accuracy

**Computational Complexity:**
- Training: O(n² × d) to O(n³ × d) where n=samples, d=features
- Can be slow for large datasets (>100k samples)
- Prediction: O(n_support_vectors × d) - typically much faster
- Memory: Stores only support vectors (10-40% of training data)
- Use CacheSize to trade memory for speed

**Probability Estimation:**
- Probability='true' enables probabilistic outputs
- Uses Platt scaling for calibration (additional training pass)
- Increases training time but provides confidence scores
- Useful for ranking predictions or threshold tuning
- Probabilities may not be perfectly calibrated

**Multi-Class Classification:**
- One-vs-one strategy: K(K-1)/2 binary classifiers for K classes
- Training time scales quadratically with number of classes
- Prediction uses voting (can be slower for many classes)
- Alternative: use TD_GLM for multinomial classification if many classes

**Support Vector Interpretation:**
- Support vectors are the "hard cases" defining decision boundary
- More support vectors → More complex model
- Fewer support vectors → Simpler model, faster prediction
- Examine support vectors to understand what drives classification

**Overfitting vs Underfitting:**
- Overfitting symptoms: High training accuracy, low test accuracy
  - Solutions: Decrease C, decrease Gamma, use Linear kernel
- Underfitting symptoms: Low training and test accuracy
  - Solutions: Increase C, increase Gamma, use RBF kernel, add features

### Best Practices

**1. Always Standardize Features**
- Use TD_ScaleFit with ScaleMethod='STD' before training
- Critical for SVM performance
- Apply same scaling to test/production data
- Verify mean ≈ 0, std ≈ 1 after scaling

**2. Hyperparameter Tuning Strategy**
- Start with default: RBF kernel, C=1.0, Gamma=1/n_features
- Grid search C: [0.01, 0.1, 1, 10, 100]
- Grid search Gamma: [0.001, 0.01, 0.1, 1.0]
- Use cross-validation or hold-out validation set
- Balance training accuracy vs validation accuracy

**3. Handle Class Imbalance**
- Check class distribution in training data
- Use ClassWeights for imbalanced datasets
- Set weights inversely proportional to class frequencies
- Monitor precision, recall, F1-score (not just accuracy)
- Consider resampling techniques if extreme imbalance

**4. Kernel Selection Guidelines**
- **Linear kernel**: High-dimensional sparse data (text, genomics), faster training
- **RBF kernel**: Most problems, non-linear patterns, medium dimensions
- **Polynomial kernel**: Domain knowledge suggests polynomial structure
- Test multiple kernels on validation set
- RBF is safe default choice

**5. Start with Smaller Samples**
- SVM training time scales poorly with sample size
- Test on subset (10k-50k samples) first
- Tune hyperparameters on subset
- Train final model on full dataset
- Consider TD_XGBoost or TD_DecisionForest for very large datasets

**6. Enable Probability for Ranking**
- Use Probability='true' if you need confidence scores
- Useful for ranking predictions by confidence
- Enables threshold tuning in production
- Allows ROC curve analysis
- Small computational overhead

**7. Monitor Support Vectors**
- Check n_support_vectors in model output
- Very high percentage (>80%) suggests model complexity
- Very low percentage (<5%) suggests underfitting
- Typical: 10-40% of training samples
- More support vectors → Slower prediction

**8. Handle Missing Values**
- SVM does not handle NULL values
- Impute missing values before training
- Use TD_SimpleImputeFit for imputation
- Consider creating "missing" indicator features
- Missing data can significantly impact performance

**9. Feature Engineering**
- SVM benefits from good features
- Remove highly correlated features
- Consider polynomial features if using Linear kernel
- Domain-specific feature engineering often helps
- Feature selection can improve performance

**10. Production Deployment**
- Store scaler model and SVM model together
- Always scale production data before prediction
- Monitor prediction latency (depends on n_support_vectors)
- Track accuracy over time (detect concept drift)
- Retrain periodically with new data
- Maintain rollback capability

### Related Functions

**Model Training:**
- **TD_OneClassSVM** - One-class SVM for anomaly detection
- **TD_DecisionForest** - Ensemble tree model, often faster for large datasets
- **TD_XGBoost** - Gradient boosting, often more accurate
- **TD_GLM** - Logistic regression, faster and simpler baseline
- **TD_NaiveBayes** - Fast probabilistic classifier

**Model Scoring:**
- **TD_SVMPredict** - Apply trained SVM model to new data

**Model Evaluation:**
- **TD_ClassificationEvaluator** - Compute accuracy, precision, recall, F1, confusion matrix
- **TD_ROC** - ROC curve and AUC for binary classification
- **TD_ConfusionMatrix** - Detailed confusion matrix

**Feature Preparation:**
- **TD_ScaleFit** - CRITICAL: Standardize features before training
- **TD_ScaleTransform** - Apply scaling to new data
- **TD_SimpleImputeFit** - Handle missing values
- **TD_OneHotEncodingFit** - Encode categorical features
- **TD_PCA** - Reduce dimensionality

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf
- [Support Vector Machines - Scikit-learn Documentation](https://scikit-learn.org/stable/modules/svm.html)
- [A Practical Guide to Support Vector Classification](https://www.csie.ntu.edu.tw/~cjlin/papers/guide/guide.pdf)
- [StatQuest: Support Vector Machines](https://www.youtube.com/watch?v=efR1C6CvhmE)

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Model Training Functions (Classification)
