# TD_GLM

### Function Name
**TD_GLM** (Generalized Linear Model)

### Description
TD_GLM is a flexible supervised learning function that performs regression and classification analysis on datasets using generalized linear models (GLMs) from the exponential family of distributions. The function supports Gaussian (regression with squared error loss) and Binomial (binary classification with logistic loss) families, implementing linear and logistic regression through the highly scalable Minibatch Stochastic Gradient Descent (SGD) algorithm. TD_GLM extends traditional linear regression to accommodate various response distributions while maintaining the interpretability of coefficients and enabling efficient training on large datasets through distributed parallel processing across Teradata AMPs.

The function utilizes SGD to estimate gradients in minibatches (defined by BatchSize) and updates model parameters with a learning rate, supporting multiple learning rate schedules (constant, optimal, invtime, adaptive) and acceleration techniques (Momentum, Nesterov). TD_GLM provides comprehensive regularization options including L1 (LASSO), L2 (Ridge), and Elastic Net penalties to control overfitting and perform feature selection. The algorithm employs convergence criteria based on loss improvement tolerance across iterations, automatically stopping when performance plateaus or reaching maximum iterations. Additionally, the function supports LocalSGD for distributed environments, running multiple local batch iterations on each AMP before global aggregation to reduce communication overhead and accelerate convergence.

TD_GLM operates in two modes: partition-by-any (training entire dataset as single model) and partition-by-key (micromodeling - training separate models per partition segment). The function supports stepwise feature selection (forward, backward, bidirectional) for automated variable selection based on model improvement criteria. All features must be standardized before training using TD_Scale functions due to gradient sensitivity to feature scales, and categorical variables require numeric conversion via encoding functions. The output includes trained models with coefficients, statistical metrics (MSE, Log-Likelihood, AIC, BIC), and optional meta-information tables tracking training progress per iteration for model diagnostics and optimization.

### When the Function Would Be Used
- **Linear Regression**: Model continuous outcomes with normally distributed errors
- **Logistic Regression**: Perform binary classification with probability predictions
- **Feature Selection**: Identify influential predictors via L1 regularization or stepwise methods
- **Large-Scale Training**: Train models efficiently on massive datasets via SGD
- **Regularized Regression**: Prevent overfitting with L1, L2, or Elastic Net penalties
- **Distributed Modeling**: Train models in parallel across data partitions
- **Micromodeling**: Build separate models for each business segment or group
- **Interpretable Models**: Generate coefficient-based models with clear feature relationships
- **Sparse Solutions**: Perform automatic feature selection via LASSO (L1) regularization
- **Ridge Regression**: Handle multicollinearity with L2 penalty
- **Credit Scoring**: Predict loan default probability with interpretable coefficients
- **Customer Churn**: Model churn likelihood with logistic regression
- **Price Prediction**: Forecast product prices or valuations using linear regression
- **Click-Through Rate (CTR)**: Predict ad click probability for online advertising
- **Medical Risk Assessment**: Estimate disease probability from patient characteristics
- **Fraud Detection**: Classify transactions as fraudulent using logistic regression
- **Demand Forecasting**: Predict future sales or resource requirements
- **A/B Testing Analysis**: Measure treatment effects in experiments
- **Customer Lifetime Value**: Estimate future revenue from customers
- **Insurance Underwriting**: Assess risk and premium pricing

### Syntax

**TD_GLM Syntax Using Partition by Any (Single Model)**

```sql
TD_GLM (
    ON { table | view | (query) } AS InputTable [ PARTITION BY ANY ]
    [ OUT TABLE MetaInformationTable (meta_table) ]
    USING
    InputColumns ({'input_column'|input_column_range }[,...])
    ResponseColumn('response_column')
    [ Family ('Gaussian' | 'Binomial') ]
    [ BatchSize (batchsize) ]
    [ MaxIterNum (max_iter) ]
    [ RegularizationLambda (lambda) ]
    [ Alpha (alpha) ]
    [ IterNumNoChange (n_iter_no_change) ]
    [ Tolerance (tolerance) ]
    [ Intercept ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
    [ ClassWeights ('class:weight,...') ]
    [ LearningRate ('constant'|'optimal'|'invtime'|'adaptive') ]
    [ InitialEta (eta0) ]
    [ DecayRate (gamma) ]
    [ DecaySteps (decay_steps) ]
    [ Momentum (momentum) ]
    [ Nesterov ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
    [ LocalSGDIterations(local_iterations) ]
    [ StepwiseDirection ('forward'|'backward'|'both' | 'bidirectional')
    [ MaxStepsNum (max_stepwise_steps) ]
    [ InitialStepwiseColumns ({initialstate_columns | initialstate_column_range }[,...])]
)
```

**TD_GLM Syntax Using Partition by Key (Micromodeling)**

```sql
TD_GLM (
    ON { table | view | (query) } AS InputTable PARTITION BY partition_by_column [ ORDER BY id_column ]
    [ ON { table | view | (query) } AS AttributeTable PARTITION BY partition_by_column ]
    [ ON { table | view | (query) } AS ParameterTable PARTITION BY partition_by_column ]
    USING
    InputColumns({'input_column'| input_column_range}[...])
    ResponseColumn (response_column)
    [ PartitionColumn ('partition_column') ]
    [ Family ('Gaussian' | 'Binomial') ]
    [ BatchSize (batchsize) ]
    [ MaxIterNum (max_iter) ]
    [ RegularizationLambda (lambda) ]
    [ Alpha (alpha) ]
    [ IterNumNoChange (n_iter_no_change) ]
    [ Tolerance (tolerance) ]
    [ Intercept ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
    [ ClassWeights ('class:weight,...') ]
    [ LearningRate ('constant'|'optimal'|'invtime'|'adaptive') ]
    [ InitialEta (eta0) ]
    [ DecayRate (gamma) ]
    [ DecaySteps (decay_steps) ]
    [ Momentum (momentum) ]
    [ Nesterov ({'true'|'t'|'yes'|'y'|'1'|'false'|'f'|'no'|'n'|'0'}) ]
    [ IterationMode ('batch'|'epoch')]
)
```

### Required Syntax Elements for TD_GLM

**ON clause (InputTable)**
- Accepts table, view, or query containing training data
- Partition by ANY: Trains entire dataset as single model
- Partition by Key: Trains separate model per partition (micromodeling)
- ORDER BY clause (optional): Ensures deterministic results in partition-by-key mode

**InputColumns**
- Specify input table column names for training (predictors, features, independent variables)
- All columns must be numeric data types
- Supports column range notation (e.g., '[1:20]')
- **CRITICAL**: Features must be standardized using TD_Scale before training

**ResponseColumn**
- Specify column containing response values (dependent variable)
- For Gaussian family: Continuous numeric values (regression)
- For Binomial family: Binary values 0 or 1 (classification)

### Optional Syntax Elements for TD_GLM

**OUT TABLE MetaInformationTable** [Partition by ANY only]
- Specify output table name for training progress information
- Contains iteration-level metrics: iteration number, rows processed, learning rate, loss, best loss
- Useful for diagnostics and convergence analysis
- For stepwise regression: includes step number, features added/deleted, scores, model composition

**PartitionColumn** [Partition by Key only]
- Specify partition column name matching partition_by_column in ON clause
- Required when partition column uses Unicode or foreign language characters

**Family**
- Specify distribution exponential family
- 'Gaussian': Linear regression with squared error loss (continuous response)
- 'Binomial': Logistic regression with logistic loss (binary 0/1 response)
- Default: 'Gaussian'

**BatchSize**
- Specify number of observations processed per minibatch per AMP
- Value of 0 or exceeding AMP rows processes all rows (becomes Gradient Descent)
- Smaller batches: more frequent updates, noisier gradients, faster initial progress
- Larger batches: smoother gradients, better convergence, more memory
- Default: 10

**MaxIterNum**
- Specify maximum number of iterations (minibatches) over training data
- Algorithm stops after this many iterations regardless of convergence
- Must be positive integer < 10,000,000
- Default: 300

**RegularizationLambda**
- Specify regularization strength (penalty amount)
- Higher values = stronger regularization = simpler models
- Value of 0 = no regularization
- Also used to compute optimal learning rate when LearningRate='optimal'
- Must be non-negative float
- Default: 0.02

**Alpha**
- Specify Elastic Net mixing parameter (contribution ratio of L1 vs L2)
- Only effective when RegularizationLambda > 0
- 1.0 = pure L1 (LASSO) - sparse solutions, feature selection
- 0.0 = pure L2 (Ridge) - distributed coefficients, handles multicollinearity
- 0.0 < Alpha < 1.0 = Elastic Net (combination of L1 and L2)
- Default: 0.15 (15% L1, 85% L2)

**IterNumNoChange**
- Specify iterations with no improvement (within tolerance) before early stopping
- Value of 0 = no early stopping (continues until MaxIterNum)
- Prevents unnecessary computation when model plateaus
- Must be non-negative integer
- Default: 50

**Tolerance**
- Specify minimum loss improvement threshold for convergence
- Algorithm stops if loss improvement < tolerance for IterNumNoChange iterations
- Applicable when IterNumNoChange > 0
- Must be positive float
- Default: 0.001

**Intercept**
- Specify whether to estimate intercept term
- True: Estimate intercept (use when data not centered)
- False: No intercept (use when data already centered or zero-intercept model)
- Default: True

**ClassWeights** [Binomial family only]
- Specify weights for each class to handle imbalanced datasets
- Format: '0:weight0,1:weight1'
- Example: '0:1.0,1:2.0' gives class 1 double weight of class 0
- Omitted class weight assumed 1.0
- Default: '0:1.0,1:1.0'

**LearningRate**
- Specify learning rate schedule algorithm
- 'constant': Fixed learning rate (uses InitialEta for all iterations)
- 'optimal': Automatically computed based on RegularizationLambda
- 'invtime': Inverse time decay (decreases over time)
- 'adaptive': Adaptive decay with plateau detection (decreases when loss stops improving)
- Default: 'invtime' for Gaussian, 'optimal' for Binomial

**InitialEta**
- Specify initial learning rate value
- For LearningRate='constant': used for all iterations
- For other schedules: starting point that decays over time
- Must be numeric value
- Default: 0.05

**DecayRate**
- Specify decay rate for learning rate schedules
- Applicable for 'invtime' and 'adaptive' schedules
- Controls how quickly learning rate decreases
- Must be numeric value
- Default: 0.25

**DecaySteps**
- Specify iterations without decay for 'adaptive' learning rate
- Learning rate changes by DecayRate after this many iterations
- Controls plateau detection sensitivity
- Must be integer
- Default: 5

**Momentum**
- Specify momentum optimizer value for accelerated learning
- Value of 0 = momentum disabled
- Larger values (0.6-0.95) = higher momentum contribution
- Reduces oscillations and speeds convergence
- Must be float between 0 and 1
- Default: 0

**Nesterov**
- Specify whether to use Nesterov accelerated gradient
- Only applicable when Momentum > 0
- True: Use Nesterov optimization (lookahead momentum)
- False: Use standard momentum
- Default: True

**LocalSGDIterations** [Partition by ANY only]
- Specify local iterations for LocalSGD algorithm
- Value of 0 = LocalSGD disabled (standard SGD)
- Value > 0 = enables LocalSGD with specified local iterations
- Reduces communication costs in distributed training
- Recommended settings: LocalSGDIterations=10, MaxIterNum=100, BatchSize=50
- Default: 0

**StepwiseDirection** [Partition by ANY only]
- Specify stepwise feature selection algorithm
- 'forward': Start empty, add features one-by-one (best improvement)
- 'backward': Start full, remove features one-by-one (best improvement)
- 'both' or 'bidirectional': Add or remove features at each step
- Algorithm stops when no improvement possible
- Useful for automatic feature selection

**MaxStepsNum** [Partition by ANY only with StepwiseDirection]
- Specify maximum steps for stepwise algorithm
- Value of 0 = run until convergence
- Limits computational cost for large feature sets
- Default: 5

**InitialStepwiseColumns** [Partition by ANY only with StepwiseDirection]
- Specify starting features for stepwise algorithm
- Used as initial state model for 'both'/'bidirectional' selection
- For 'forward': typically empty (not specified)
- For 'backward': typically all features (not specified)
- For 'both': custom starting point

**IterationMode** [Partition by Key only]
- Specify iteration granularity
- 'Batch': One iteration per batch (update after each batch)
- 'Epoch': One iteration per epoch (update after processing all batches in partition)
- Default: 'Batch'

### Input Table Schema

**InputTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| partition_by_column | CHARACTER, VARCHAR, INTEGER, BIGINT, SMALLINT, BYTEINT | [Partition by Key only] Unique identifier for each model partition |
| id_column | CHARACTER, VARCHAR, INTEGER, BIGINT, SMALLINT, BYTEINT | [Optional for ORDER BY] Unique identifier for each row |
| input_column | INTEGER, BIGINT, SMALLINT, BYTEINT, FLOAT, DECIMAL, NUMBER | Numeric columns used to train GLM model (standardized features) |
| response_column | INTEGER, BIGINT, SMALLINT, BYTEINT (Binomial)<br>All numeric types (Gaussian) | Column containing response value for each observation |

**AttributeTable Schema** [Partition by Key only]:

| Column | Data Type | Description |
|--------|-----------|-------------|
| partition_by_column | CHARACTER, VARCHAR, INTEGER, BIGINT, SMALLINT, BYTEINT | Unique identifier matching InputTable partition |
| attribute_column | VARCHAR | Names of target columns to use from InputTable (must be unique, no duplicates) |

**ParameterTable Schema** [Partition by Key only]:

| Column | Data Type | Description |
|--------|-----------|-------------|
| partition_by_column | CHARACTER, VARCHAR, INTEGER, BIGINT, SMALLINT, BYTEINT | Unique identifier matching InputTable partition |
| parameter_column | VARCHAR | Syntax element name (Family, BatchSize, MaxIterNum, RegularizationLambda, Alpha, etc.) |
| value_column | VARCHAR | Value to use for the syntax element |

**Important Notes:**
- All input features must be standardized using TD_ScaleFit and TD_ScaleTransform
- Categorical variables must be converted to numeric using encoding functions
- Function skips rows with missing (NULL) values during training

### Output Table Schema

**Model Output Schema (Partition by ANY):**

| Column | Data Type | Description |
|--------|-----------|-------------|
| attribute | SMALLINT | Numeric index: 0 for intercept, positive for predictors, negative for model metrics |
| predictor | VARCHAR | Name of predictor or model metric |
| estimate | FLOAT | Predictor weight (coefficient) or numeric metric value |
| value | VARCHAR | String-based metric values (e.g., 'SQUARED_ERROR', 'L2', 'CONVERGED') |

**Model Output Schema (Partition by Key):**

| Column | Data Type | Description |
|--------|-----------|-------------|
| partition_by_column | Same as InputTable | Partition identifier (same data type as original) |
| attribute | SMALLINT | Numeric index: 0 for intercept, positive for predictors, negative for model metrics |
| predictor | VARCHAR | Name of predictor or model metric |
| estimate | FLOAT | Predictor weight (coefficient) or numeric metric value |
| value | VARCHAR | String-based metric values (e.g., 'SQUARED_ERROR', 'L2', 'CONVERGED') |

**Model Metrics Stored (attribute < 0):**
- Loss Function (SQUARED_ERROR or LOG)
- MSE (Gaussian) or Log-Likelihood (Binomial)
- Number of Observations
- AIC (Akaike Information Criterion)
- BIC (Bayesian Information Criterion)
- Number of Iterations (with convergence status)
- Regularization amount and type (L1, L2, Elasticnet)
- Learning Rate (Initial and Final)
- Momentum and Nesterov settings
- LocalSGD Iterations

**MetaInformationTable Output Schema** [Partition by ANY only]:

| Column | Data Type | Description |
|--------|-----------|-------------|
| iteration | INTEGER | Iteration number (epoch number) |
| num_rows | BIGINT | Total number of rows processed so far |
| eta | FLOAT | Learning rate for this iteration |
| loss | FLOAT | Loss value in this iteration |
| best_loss | FLOAT | Best loss achieved until this iteration |

**MetaInformationTable with StepwiseDirection:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| Step | INTEGER | Step number in stepwise algorithm |
| SubStep | INTEGER | Feature number tested (added/deleted) within step |
| Description | VARCHAR | Description of action: feature added (+feature) or deleted (-feature) |
| Score | FLOAT | Model score after action, best score per step, best overall score |
| Model | VARCHAR | List of variable names contained in model at this step |

### Code Examples

**Input Data: credit_data (scaled)**
```
id  a1        a2        a7        a10       a13       a14       outcome
1   -0.453    -0.025    -0.405    -0.772    0.886     -0.226    1
2   0.218     2.177     0.143     1.253     0.239     -0.130    1
3   -1.132    -0.772    -0.199    -0.547    -0.761    -0.644    0
4   -0.658    1.202     0.006     0.803     -0.544    -0.120    1
```

**Example 1: Basic Logistic Regression (Binary Classification)**
```sql
-- Train logistic regression model for binary outcome
CREATE VOLATILE TABLE glm_credit_model AS (
    SELECT * FROM TD_GLM (
        ON credit_train_scaled AS InputTable PARTITION BY ANY
        USING
        InputColumns('a1', 'a2', 'a7', 'a10', 'a13', 'a14')
        ResponseColumn('outcome')
        Family('Binomial')
        BatchSize(20)
        MaxIterNum(200)
        RegularizationLambda(0.01)
        LearningRate('optimal')
        Tolerance(0.001)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Output: Model coefficients and metrics (AIC, BIC, Log-Likelihood)
-- Use with TD_GLMPredict for predictions
```

**Example 2: Linear Regression (Gaussian Family)**
```sql
-- Train linear regression model for house price prediction
CREATE VOLATILE TABLE glm_housing_model AS (
    SELECT * FROM TD_GLM (
        ON housing_train_scaled AS InputTable PARTITION BY ANY
        USING
        InputColumns('medinc', 'houseage', 'averooms', 'avebedrms',
                     'population', 'aveoccup', 'latitude', 'longitude')
        ResponseColumn('medianvalue')
        Family('Gaussian')
        BatchSize(50)
        MaxIterNum(300)
        RegularizationLambda(0.02)
        Alpha(0.5)  -- Elastic Net (50% L1, 50% L2)
        LearningRate('invtime')
        InitialEta(0.01)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Output: Linear regression coefficients for house price prediction
```

**Example 3: LASSO Regression (L1 for Feature Selection)**
```sql
-- Train LASSO model for automatic feature selection
CREATE VOLATILE TABLE glm_lasso_model AS (
    SELECT * FROM TD_GLM (
        ON customer_data_scaled AS InputTable PARTITION BY ANY
        OUT TABLE MetaInformationTable(lasso_meta)
        USING
        InputColumns('[1:50]')  -- 50 features
        ResponseColumn('churn')
        Family('Binomial')
        RegularizationLambda(0.1)  -- Strong regularization
        Alpha(1.0)  -- Pure L1 (LASSO)
        BatchSize(30)
        MaxIterNum(500)
        IterNumNoChange(100)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Alpha=1.0 drives many coefficients to exactly zero (sparse solution)
-- Check which features have non-zero coefficients for selection
SELECT predictor, estimate
FROM glm_lasso_model
WHERE attribute > 0 AND ABS(estimate) > 0.001
ORDER BY ABS(estimate) DESC;
```

**Example 4: Ridge Regression (L2 for Multicollinearity)**
```sql
-- Train Ridge regression for correlated features
CREATE VOLATILE TABLE glm_ridge_model AS (
    SELECT * FROM TD_GLM (
        ON correlated_features_scaled AS InputTable PARTITION BY ANY
        USING
        InputColumns('[1:30]')
        ResponseColumn('target')
        Family('Gaussian')
        RegularizationLambda(0.5)  -- Strong L2 penalty
        Alpha(0.0)  -- Pure L2 (Ridge)
        BatchSize(40)
        MaxIterNum(300)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Alpha=0.0 distributes coefficients across correlated features
-- Handles multicollinearity better than unregularized regression
```

**Example 5: Momentum and Nesterov Acceleration**
```sql
-- Train model with momentum for faster convergence
CREATE VOLATILE TABLE glm_momentum_model AS (
    SELECT * FROM TD_GLM (
        ON large_dataset_scaled AS InputTable PARTITION BY ANY
        USING
        InputColumns('[1:20]')
        ResponseColumn('outcome')
        Family('Binomial')
        BatchSize(100)
        MaxIterNum(200)
        RegularizationLambda(0.01)
        LearningRate('constant')
        InitialEta(0.01)
        Momentum(0.9)  -- High momentum
        Nesterov('true')  -- Use Nesterov optimization
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Momentum=0.9 with Nesterov reduces oscillations
-- Speeds up convergence significantly for large datasets
```

**Example 6: Adaptive Learning Rate**
```sql
-- Train model with adaptive learning rate that decreases when loss plateaus
CREATE VOLATILE TABLE glm_adaptive_model AS (
    SELECT * FROM TD_GLM (
        ON training_data_scaled AS InputTable PARTITION BY ANY
        OUT TABLE MetaInformationTable(adaptive_meta)
        USING
        InputColumns('[2:15]')
        ResponseColumn('target')
        Family('Gaussian')
        BatchSize(25)
        MaxIterNum(400)
        LearningRate('adaptive')
        InitialEta(0.05)
        DecayRate(0.5)  -- Halve learning rate on plateau
        DecaySteps(10)  -- Check every 10 iterations
        IterNumNoChange(50)
        Tolerance(0.0001)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Adaptive schedule automatically reduces learning rate when stuck
-- Examine adaptive_meta table to see learning rate changes over time
SELECT iteration, eta, loss, best_loss
FROM adaptive_meta
WHERE MOD(iteration, 10) = 0
ORDER BY iteration;
```

**Example 7: LocalSGD for Distributed Training**
```sql
-- Train model with LocalSGD for faster distributed learning
CREATE VOLATILE TABLE glm_localsgd_model AS (
    SELECT * FROM TD_GLM (
        ON massive_dataset_scaled AS InputTable PARTITION BY ANY
        OUT TABLE MetaInformationTable(localsgd_meta)
        USING
        InputColumns('[1:40]')
        ResponseColumn('outcome')
        Family('Binomial')
        BatchSize(50)
        MaxIterNum(100)
        LocalSGDIterations(10)  -- 10 local iterations per global sync
        RegularizationLambda(0.02)
        IterNumNoChange(5)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- LocalSGD reduces communication between AMPs
-- Converges in fewer global iterations (though more local iterations)
-- Ideal for large clusters and many features
```

**Example 8: Forward Stepwise Feature Selection**
```sql
-- Train model with forward stepwise feature selection
CREATE VOLATILE TABLE glm_forward_model AS (
    SELECT * FROM TD_GLM (
        ON feature_candidates_scaled AS InputTable PARTITION BY ANY
        OUT TABLE MetaInformationTable(stepwise_meta)
        USING
        InputColumns('[1:30]')  -- 30 candidate features
        ResponseColumn('target')
        Family('Gaussian')
        BatchSize(20)
        MaxIterNum(100)
        StepwiseDirection('forward')
        MaxStepsNum(10)  -- Maximum 10 features
        LearningRate('optimal')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Examine stepwise process: which features added at each step
SELECT Step, Description, Score, Model
FROM stepwise_meta
WHERE Description LIKE '%Best%' OR Description LIKE '+%'
ORDER BY Step;

-- Final model contains only features that improved score
```

**Example 9: Partition by Key Micromodeling (Separate Model per Segment)**
```sql
-- Train separate model for each customer segment
CREATE VOLATILE TABLE glm_segment_models AS (
    SELECT * FROM TD_GLM (
        ON customer_train_scaled AS InputTable PARTITION BY segment_id ORDER BY customer_id
        USING
        InputColumns('tenure', 'monthly_charges', 'total_charges', 'num_services')
        ResponseColumn('churn')
        PartitionColumn('segment_id')
        Family('Binomial')
        BatchSize(10)
        MaxIterNum(200)
        RegularizationLambda(0.05)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Output: Separate model coefficients for each segment_id
-- Each segment gets customized model capturing local patterns
SELECT segment_id, predictor, estimate
FROM glm_segment_models
WHERE attribute >= 0
ORDER BY segment_id, attribute;
```

**Example 10: Complete Workflow (Scale + Train + Predict + Evaluate)**
```sql
-- Step 1: Standardize features
CREATE VOLATILE TABLE scale_fit AS (
    SELECT * FROM TD_ScaleFit (
        ON credit_raw AS InputTable
        OUT VOLATILE TABLE OutputTable(credit_scale_model)
        USING
        TargetColumns('a1', 'a2', 'a7', 'a10', 'a13', 'a14')
        ScaleMethod('STD')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 2: Transform training data
CREATE VOLATILE TABLE credit_train_scaled AS (
    SELECT * FROM TD_ScaleTransform (
        ON credit_train AS InputTable
        ON credit_scale_model AS FitTable DIMENSION
        USING
        Accumulate('id', 'outcome')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 3: Train GLM model
CREATE VOLATILE TABLE glm_model AS (
    SELECT * FROM TD_GLM (
        ON credit_train_scaled AS InputTable PARTITION BY ANY
        USING
        InputColumns('a1', 'a2', 'a7', 'a10', 'a13', 'a14')
        ResponseColumn('outcome')
        Family('Binomial')
        BatchSize(20)
        MaxIterNum(300)
        RegularizationLambda(0.02)
        Alpha(0.15)
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 4: Transform test data
CREATE VOLATILE TABLE credit_test_scaled AS (
    SELECT * FROM TD_ScaleTransform (
        ON credit_test AS InputTable
        ON credit_scale_model AS FitTable DIMENSION
        USING
        Accumulate('id', 'outcome')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 5: Make predictions
CREATE VOLATILE TABLE predictions AS (
    SELECT * FROM TD_GLMPredict (
        ON credit_test_scaled AS InputTable PARTITION BY ANY
        ON glm_model AS ModelTable DIMENSION
        USING
        IDColumn('id')
        Accumulate('outcome')
    ) AS dt
) WITH DATA ON COMMIT PRESERVE ROWS;

-- Step 6: Evaluate performance
SELECT * FROM TD_ClassificationEvaluator (
    ON predictions AS InputTable PARTITION BY ANY
    USING
    ObservationColumn('outcome')
    PredictionColumn('prediction')
    NumClasses(2)
) AS dt;

-- Output: Accuracy, Precision, Recall, F1-Score, Confusion Matrix
```

### Generalized Linear Models Mathematical Foundation

**GLM Components:**

**Linear Predictor:**
- η = Xβ where X is feature matrix, β is coefficient vector

**Link Function:**
- Relates linear predictor to expected value of response: g(μ) = η
- Gaussian family: Identity link g(μ) = μ (linear regression)
- Binomial family: Logit link g(μ) = log(μ/(1-μ)) (logistic regression)

**Variance Function:**
- Var(Y) = φ·V(μ) where φ is scale parameter, V(μ) is variance function

**Optimization:**
- Minibatch SGD updates: w = w - η·(λ·w - (1/b)·Σ gradient)
- Gradient depends on loss function and link function
- Learning rate η adjusted by schedule (constant, optimal, invtime, adaptive)

**Regularization:**
- Elastic Net penalty: Penalty = λ·(α·||w||₁ + (1-α)/2·||w||₂²)
- α=1.0: LASSO (L1) - sparse solutions
- α=0.0: Ridge (L2) - distributed coefficients
- 0<α<1: Elastic Net - balanced approach

### Use Cases and Applications

**1. Financial Services**
- Credit scoring and loan approval
- Fraud detection for transactions
- Default probability estimation
- Customer lifetime value prediction

**2. Marketing and Advertising**
- Click-through rate (CTR) prediction
- Conversion probability modeling
- Customer response to campaigns
- Attribution modeling for marketing channels

**3. Healthcare and Medicine**
- Disease risk assessment
- Readmission probability
- Treatment effectiveness analysis
- Patient outcome prediction

**4. E-Commerce and Retail**
- Customer churn prediction
- Purchase probability estimation
- Demand forecasting
- Price elasticity modeling

**5. Insurance**
- Claim probability estimation
- Premium pricing optimization
- Risk assessment for policies
- Fraud detection

**6. Telecommunications**
- Customer churn modeling
- Service upgrade probability
- Network usage prediction
- Customer lifetime value

**7. Human Resources**
- Employee attrition prediction
- Performance rating estimation
- Hiring success probability
- Training effectiveness

**8. Real Estate**
- Property price prediction
- Sale probability estimation
- Rent forecasting
- Market trend analysis

**9. Manufacturing**
- Quality control and defect prediction
- Equipment failure probability
- Production output forecasting
- Supply chain optimization

**10. Energy and Utilities**
- Energy consumption forecasting
- Demand prediction for grid management
- Equipment maintenance scheduling
- Customer usage pattern modeling

### Important Notes

**Feature Standardization - CRITICAL:**
- **MUST** standardize all input features using TD_ScaleFit and TD_ScaleTransform before training
- SGD is highly sensitive to feature scales
- Unstandardized features lead to poor convergence and inaccurate models
- Use ScaleMethod='STD' (standardization) for most cases

**Data Preprocessing:**
- **Categorical Variables**: Convert to numeric using TD_OneHotEncoding, TD_OrdinalEncoding, or TD_TargetEncoding
- **Missing Values**: Function skips rows with NULL values - use TD_SimpleImpute to fill missing values
- **Response Variable**: Binomial family requires binary 0/1 values

**Partition by ANY vs Partition by Key:**
- **Partition by ANY**: Single global model trained on entire dataset
- **Partition by Key**: Separate models per partition (micromodeling for segmentation)
- Partition-by-any supports LocalSGD and StepwiseDirection
- Partition-by-key supports AttributeTable and ParameterTable for per-partition customization

**Learning Rate Selection:**
- Start with 'optimal' or 'invtime' schedules
- Use 'constant' only if you know appropriate learning rate
- Too high: model diverges or oscillates
- Too low: slow convergence, may not reach optimum
- Monitor MetaInformationTable to diagnose learning rate issues

**Regularization Strategy:**
- **No Regularization** (λ=0): Risk of overfitting, only for simple models or large data
- **L2/Ridge** (α=0): Handle multicollinearity, all features retained
- **L1/LASSO** (α=1): Automatic feature selection, sparse solutions
- **Elastic Net** (0<α<1): Balanced approach, recommended for most cases

**Convergence Monitoring:**
- Use MetaInformationTable (OUT TABLE) to track training progress
- Plot loss over iterations to diagnose convergence issues
- Increase MaxIterNum if model hasn't converged
- Adjust IterNumNoChange and Tolerance for early stopping behavior

**Momentum and Acceleration:**
- Momentum=0.6-0.95 speeds up convergence
- Nesterov=true with Momentum provides better optimization
- Particularly effective for large datasets and complex models
- May cause instability with high learning rates

**LocalSGD Benefits:**
- Reduces communication overhead in distributed training
- Converges faster (fewer global iterations)
- Recommended for large clusters and many features
- Settings: LocalSGDIterations=10, MaxIterNum=100, BatchSize=50

**Stepwise Feature Selection:**
- Automated but computationally expensive
- Use when unsure which features to include
- Forward: Best for small starting feature sets
- Backward: Best when starting with all features
- Both/Bidirectional: Most flexible but slowest

**Model Metrics:**
- **MSE**: Mean squared error (Gaussian) - lower is better
- **Log-Likelihood**: Goodness of fit (Binomial) - higher is better
- **AIC**: Akaike Information Criterion - lower is better (balances fit vs complexity)
- **BIC**: Bayesian Information Criterion - lower is better (stronger complexity penalty than AIC)

### Best Practices

**1. Always Standardize Features**
- Use TD_ScaleFit with ScaleMethod='STD' on training data
- Apply TD_ScaleTransform to both training and test data using same FitTable
- Never train GLM without standardization
- Save FitTable for production scoring

**2. Start with Simple Models**
- Begin with default parameters and no regularization
- Add regularization if overfitting observed
- Use Alpha=0.15 (Elastic Net) as safe starting point
- Tune hyperparameters incrementally

**3. Monitor Training with MetaInformationTable**
- Always use OUT TABLE MetaInformationTable for diagnostics
- Plot loss vs iteration to check convergence
- Verify loss is decreasing and not oscillating
- Adjust learning rate if loss plateaus or diverges

**4. Tune Batch Size Appropriately**
- Larger batches (50-100): Smoother gradients, better for large datasets
- Smaller batches (10-30): Faster updates, good for medium datasets
- Very small batches (<10): Noisy but can escape local minima
- BatchSize=0 or >rows: Full gradient descent (deterministic but slow)

**5. Set Realistic Convergence Criteria**
- IterNumNoChange=50, Tolerance=0.001: Balanced early stopping
- Increase IterNumNoChange for more patience
- Decrease Tolerance for tighter convergence
- Use MaxIterNum as safety limit (300-500 typical)

**6. Handle Class Imbalance**
- Use ClassWeights for imbalanced binary classification
- Example: '0:1.0,1:5.0' for 5:1 imbalance (5x more class 0 than class 1)
- Alternative: Oversample minority class or undersample majority class
- Evaluate with Precision/Recall/F1, not just Accuracy

**7. Choose Regularization Wisely**
- Start with Lambda=0.01-0.05 for moderate regularization
- Increase Lambda if overfitting (train accuracy >> test accuracy)
- Use Alpha=1.0 (LASSO) for feature selection
- Use Alpha=0.0 (Ridge) for multicollinearity
- Use Alpha=0.15-0.5 (Elastic Net) for general purpose

**8. Use Momentum for Large Datasets**
- Set Momentum=0.9, Nesterov=true for datasets >100k rows
- Significantly speeds up convergence
- Reduces oscillations in loss function
- May need to reduce learning rate slightly

**9. Leverage LocalSGD for Distributed Data**
- Use LocalSGDIterations=10 for large cluster deployments
- Reduces communication costs between AMPs
- Especially beneficial with many features (>50)
- Monitor convergence as behavior differs from standard SGD

**10. Evaluate Model Comprehensively**
- Use TD_ClassificationEvaluator for classification metrics
- Use TD_RegressionEvaluator for regression metrics
- Examine coefficients for interpretability
- Check AIC/BIC for model complexity assessment
- Validate on held-out test set before deployment

### Related Functions
- **TD_GLMPredict** - Make predictions using trained GLM model
- **TD_ScaleFit** - Standardize features (required preprocessing)
- **TD_ScaleTransform** - Apply standardization to new data
- **TD_SimpleImpute** - Fill missing values before training
- **TD_OneHotEncoding** - Convert categorical variables to numeric
- **TD_OrdinalEncoding** - Encode ordinal categorical variables
- **TD_TargetEncoding** - Encode high-cardinality categories
- **TD_ClassificationEvaluator** - Evaluate classification model performance
- **TD_RegressionEvaluator** - Evaluate regression model performance
- **TD_ROC** - Generate ROC curves and AUC for binary classifiers
- **TD_DecisionForest** - Alternative ensemble method
- **TD_XGBoost** - Alternative gradient boosting method
- **TD_SVM** - Alternative linear classifier with hinge loss

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Model Training Functions
