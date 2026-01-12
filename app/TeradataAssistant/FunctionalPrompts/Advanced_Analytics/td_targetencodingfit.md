# TD_TargetEncodingFit

### Function Name
**TD_TargetEncodingFit**

### Description
TD_TargetEncodingFit creates a specification table (FitTable) for encoding categorical variables using target variable statistics. This function calculates Bayesian posterior estimates that replace categorical values with numeric representations based on their relationship to the target variable, enabling machine learning algorithms to learn from high-cardinality categorical features that are difficult to handle with traditional one-hot encoding.

This is the specification component of the target encoding pipeline. Target encoding (also called mean encoding or likelihood encoding) transforms categorical features by computing a weighted average between the category's target mean and the global target mean, using Bayesian methods to prevent overfitting on rare categories. The function supports three Bayesian encoder methods (CBM_BETA for binary targets, CBM_DIRICHLET for multiclass targets, CBM_GAUSSIAN_INVERSE_GAMMA for continuous targets), each using prior distributions to regularize estimates.

The FitTable produced contains the encoding mappings and parameters needed by TD_TargetEncodingTransform to apply consistent transformations. Target encoding is particularly valuable for high-cardinality categorical features (cities, zip codes, product IDs, user IDs) where one-hot encoding would create excessive dimensionality, and it often significantly improves model performance by capturing the predictive relationship between categories and the target variable.

### When the Function Would Be Used
- **High-Cardinality Categoricals**: Encode features with many unique values (cities, zip codes, IDs)
- **Boosting Model Features**: Create powerful features for gradient boosting algorithms
- **Regularized Encoding**: Apply Bayesian smoothing to prevent overfitting on rare categories
- **Dimensionality Reduction**: Replace high-dimensional one-hot encodings with single numeric columns
- **Predictive Encoding**: Capture target relationships in categorical features
- **Feature Engineering**: Create features that encode domain knowledge from training data
- **Model Performance**: Improve accuracy for tree-based and linear models
- **Cold Start Handling**: Use priors to handle unseen categories gracefully
- **Binary Classification**: Encode categories based on positive class rates
- **Multiclass Problems**: Encode categories for multiple target classes
- **Regression Tasks**: Encode categories based on mean target values
- **Cross-Validation Pipelines**: Create fit specifications for consistent encoding
- **Production ML Pipelines**: Generate encoding tables for deployment
- **A/B Testing Analysis**: Encode test variants with performance metrics

### Syntax

**Binary Target (Classification):**
```sql
TD_TargetEncodingFit (
    ON { table | view | (query) } AS InputTable
    ON { table | view | (query) } AS CategoricalTable AS CategoricalTableAlias DIMENSION
    USING
    TargetColumn ('target_column')
    CategoricalColumns ({ 'categorical_column' | categorical_column_range }[,...])
    EncoderMethod ('CBM_BETA')
    [ AlphaPrior (alpha_value) ]
    [ BetaPrior (beta_value) ]
)
```

**Multiclass Target:**
```sql
TD_TargetEncodingFit (
    ON { table | view | (query) } AS InputTable
    ON { table | view | (query) } AS CategoricalTable AS CategoricalTableAlias DIMENSION
    USING
    TargetColumn ('target_column')
    CategoricalColumns ({ 'categorical_column' | categorical_column_range }[,...])
    EncoderMethod ('CBM_DIRICHLET')
    NumDistinctResponses (num_classes)
    [ AlphaPrior (alpha_value) ]
)
```

**Continuous Target (Regression):**
```sql
TD_TargetEncodingFit (
    ON { table | view | (query) } AS InputTable
    ON { table | view | (query) } AS CategoricalTable AS CategoricalTableAlias DIMENSION
    USING
    TargetColumn ('target_column')
    CategoricalColumns ({ 'categorical_column' | categorical_column_range }[,...])
    EncoderMethod ('CBM_GAUSSIAN_INVERSE_GAMMA')
    [ AlphaPrior (alpha_value) ]
    [ BetaPrior (beta_value) ]
)
```

### Required Syntax Elements for TD_TargetEncodingFit

**ON clause (InputTable)**
- Accepts the InputTable clause containing training data
- Must include target column and categorical columns
- Each categorical column limited to maximum 4000 unique values

**ON clause (CategoricalTable DIMENSION)**
- Accepts the CategoricalTable with category-target statistics
- Typically the same as InputTable
- DIMENSION keyword required

**TargetColumn**
- Specify target variable column name
- Must be numeric for all encoder methods
- Binary targets: 0/1 encoding
- Multiclass targets: Integer class labels (0, 1, 2, ...)
- Continuous targets: Any numeric values

**CategoricalColumns**
- Specify categorical columns to encode
- Must contain VARCHAR or categorical data
- Each column limited to 4000 unique values
- Supports column range notation

**EncoderMethod**
- Specify Bayesian encoding method
- **CBM_BETA**: Binary classification targets (Bernoulli trials)
- **CBM_DIRICHLET**: Multiclass classification targets
- **CBM_GAUSSIAN_INVERSE_GAMMA**: Continuous regression targets

### Optional Syntax Elements for TD_TargetEncodingFit

**AlphaPrior**
- Alpha parameter for prior distribution
- **CBM_BETA**: Alpha (prior successes), default: 1.0
- **CBM_DIRICHLET**: Alpha (concentration parameter), default: 1.0
- **CBM_GAUSSIAN_INVERSE_GAMMA**: Alpha (shape parameter), default: 3.0
- Higher values = stronger regularization toward global mean

**BetaPrior**
- Beta parameter for prior distribution
- **CBM_BETA**: Beta (prior failures), default: 1.0
- **CBM_GAUSSIAN_INVERSE_GAMMA**: Beta (scale parameter), default: 1.0
- Not used for CBM_DIRICHLET
- Controls variance of prior distribution

**NumDistinctResponses**
- Number of distinct target classes
- Required for CBM_DIRICHLET (multiclass)
- Not used for CBM_BETA or CBM_GAUSSIAN_INVERSE_GAMMA
- Must match actual number of classes in data

### Input Table Schema

**InputTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | Numeric types (INTEGER for classification, any numeric for regression) | Target variable to predict |
| categorical_column | VARCHAR | Categorical features to encode (max 4000 unique values per column) |
| other_columns | ANY | [Optional] Other columns in dataset |

**CategoricalTable Schema:**

Typically the same as InputTable, containing category-target relationships.

### Output Table Schema (FitTable)

| Column | Data Type | Description |
|--------|-----------|-------------|
| categorical_column_name | VARCHAR | Name of categorical column |
| category_value | VARCHAR | Unique category value |
| encoding_value | DOUBLE PRECISION | Bayesian posterior estimate for category |
| encoder_method | VARCHAR | Encoding method used |
| alpha_prior | DOUBLE PRECISION | Alpha prior parameter |
| beta_prior | DOUBLE PRECISION | [Optional] Beta prior parameter |
| category_count | INTEGER | Number of observations for category |
| global_mean | DOUBLE PRECISION | Overall target mean (prior mean) |

The FitTable contains encoding mappings for each category in each categorical column.

### Code Examples

**Input Data: customer_data**
```
customer_id  city          country  payment_method  churned
1            New York      USA      Credit Card     0
2            Los Angeles   USA      PayPal          1
3            Chicago       USA      Credit Card     0
4            London        UK       Debit Card      1
5            Manchester    UK       PayPal          1
```

**Example 1: Binary Classification (CBM_BETA)**
```sql
-- Encode high-cardinality city feature for churn prediction
CREATE TABLE target_encoding_fit_binary AS (
    SELECT * FROM TD_TargetEncodingFit (
        ON customer_data AS InputTable
        ON customer_data AS CategoricalTable DIMENSION
        USING
        TargetColumn('churned')
        CategoricalColumns('city', 'payment_method')
        EncoderMethod('CBM_BETA')
        AlphaPrior(1.0)
        BetaPrior(1.0)
    ) AS dt
) WITH DATA;

-- View encoding mappings
SELECT * FROM target_encoding_fit_binary
WHERE categorical_column_name = 'city'
ORDER BY category_value;
```

**Output FitTable:**
```
categorical_column_name  category_value  encoding_value  category_count  global_mean
city                     New York        0.33            1               0.40
city                     Los Angeles     0.50            1               0.40
city                     Chicago         0.33            1               0.40
city                     London          0.50            1               0.40
city                     Manchester      0.50            1               0.40
```

**Encoding Formula (CBM_BETA):**
encoding = (category_successes + alpha) / (category_total + alpha + beta)

**Example 2: High-Cardinality Feature (Zip Codes)**
```sql
-- Encode 5000 unique zip codes for loan default prediction
CREATE TABLE zip_encoding_fit AS (
    SELECT * FROM TD_TargetEncodingFit (
        ON loan_applications AS InputTable
        ON loan_applications AS CategoricalTable DIMENSION
        USING
        TargetColumn('defaulted')
        CategoricalColumns('zip_code')
        EncoderMethod('CBM_BETA')
        AlphaPrior(5.0)    -- Stronger regularization
        BetaPrior(5.0)
    ) AS dt
) WITH DATA;

-- High alpha/beta = rare zip codes pull toward global mean
-- Common zip codes use their actual default rates
```

**Example 3: Multiclass Classification (CBM_DIRICHLET)**
```sql
-- Encode categories for product category prediction (5 classes)
CREATE TABLE multiclass_encoding_fit AS (
    SELECT * FROM TD_TargetEncodingFit (
        ON product_views AS InputTable
        ON product_views AS CategoricalTable DIMENSION
        USING
        TargetColumn('purchased_category')  -- 0, 1, 2, 3, 4
        CategoricalColumns('user_country', 'referrer_domain')
        EncoderMethod('CBM_DIRICHLET')
        NumDistinctResponses(5)
        AlphaPrior(2.0)
    ) AS dt
) WITH DATA;

-- Creates encoding for each class
```

**Example 4: Regression Target (CBM_GAUSSIAN_INVERSE_GAMMA)**
```sql
-- Encode categorical features for house price prediction
CREATE TABLE regression_encoding_fit AS (
    SELECT * FROM TD_TargetEncodingFit (
        ON housing_data AS InputTable
        ON housing_data AS CategoricalTable DIMENSION
        USING
        TargetColumn('sale_price')
        CategoricalColumns('neighborhood', 'school_district', 'zoning_type')
        EncoderMethod('CBM_GAUSSIAN_INVERSE_GAMMA')
        AlphaPrior(3.0)
        BetaPrior(1.0)
    ) AS dt
) WITH DATA;

-- Neighborhoods with few sales pull toward global mean price
-- Neighborhoods with many sales use their actual mean price
```

**Example 5: Multiple Categorical Features**
```sql
-- Encode several high-cardinality features for click prediction
CREATE TABLE click_encoding_fit AS (
    SELECT * FROM TD_TargetEncodingFit (
        ON ad_impressions AS InputTable
        ON ad_impressions AS CategoricalTable DIMENSION
        USING
        TargetColumn('clicked')
        CategoricalColumns('device_id', 'publisher_id', 'advertiser_id', 'geo_location')
        EncoderMethod('CBM_BETA')
        AlphaPrior(2.0)
        BetaPrior(8.0)  -- Prior: 20% click rate
    ) AS dt
) WITH DATA;

-- Each categorical column gets its own encoding mappings
```

**Example 6: Weak vs Strong Regularization**
```sql
-- Weak regularization (trust category statistics)
CREATE TABLE weak_regularization_fit AS (
    SELECT * FROM TD_TargetEncodingFit (
        ON large_dataset AS InputTable
        ON large_dataset AS CategoricalTable DIMENSION
        USING
        TargetColumn('converted')
        CategoricalColumns('campaign_id')
        EncoderMethod('CBM_BETA')
        AlphaPrior(0.5)   -- Weak prior
        BetaPrior(0.5)
    ) AS dt
) WITH DATA;

-- Strong regularization (pull toward global mean)
CREATE TABLE strong_regularization_fit AS (
    SELECT * FROM TD_TargetEncodingFit (
        ON small_dataset AS InputTable
        ON small_dataset AS CategoricalTable DIMENSION
        USING
        TargetColumn('converted')
        CategoricalColumns('campaign_id')
        EncoderMethod('CBM_BETA')
        AlphaPrior(10.0)  -- Strong prior
        BetaPrior(10.0)
    ) AS dt
) WITH DATA;
```

**Example 7: Customer Segmentation Encoding**
```sql
-- Encode customer segments for LTV prediction
CREATE TABLE segment_encoding_fit AS (
    SELECT * FROM TD_TargetEncodingFit (
        ON customer_ltv AS InputTable
        ON customer_ltv AS CategoricalTable DIMENSION
        USING
        TargetColumn('lifetime_value')
        CategoricalColumns('acquisition_channel', 'first_purchase_category', 'geographic_region')
        EncoderMethod('CBM_GAUSSIAN_INVERSE_GAMMA')
        AlphaPrior(5.0)
        BetaPrior(2.0)
    ) AS dt
) WITH DATA;

-- Segments encode average LTV for that segment
```

**Example 8: A/B Test Variant Encoding**
```sql
-- Encode experiment variants with conversion rates
CREATE TABLE variant_encoding_fit AS (
    SELECT * FROM TD_TargetEncodingFit (
        ON experiment_results AS InputTable
        ON experiment_results AS CategoricalTable DIMENSION
        USING
        TargetColumn('converted')
        CategoricalColumns('test_variant', 'user_segment')
        EncoderMethod('CBM_BETA')
        AlphaPrior(1.0)
        BetaPrior(1.0)
    ) AS dt
) WITH DATA;

-- Each variant gets encoded with its conversion rate
```

**Example 9: E-commerce Product Category Encoding**
```sql
-- Encode product categories for purchase prediction
CREATE TABLE product_encoding_fit AS (
    SELECT * FROM TD_TargetEncodingFit (
        ON product_views AS InputTable
        ON product_views AS CategoricalTable DIMENSION
        USING
        TargetColumn('purchased')
        CategoricalColumns('product_category', 'brand', 'vendor')
        EncoderMethod('CBM_BETA')
        AlphaPrior(3.0)
        BetaPrior(7.0)  -- Prior: 30% purchase rate
    ) AS dt
) WITH DATA;

-- Categories with high purchase rates get higher encodings
```

**Example 10: Complete ML Pipeline with Target Encoding**
```sql
-- Step 1: Create target encoding fit on training data only
CREATE TABLE train_target_fit AS (
    SELECT * FROM TD_TargetEncodingFit (
        ON training_set AS InputTable
        ON training_set AS CategoricalTable DIMENSION
        USING
        TargetColumn('churned')
        CategoricalColumns('city', 'state', 'zip_code', 'product_tier', 'sales_rep_id')
        EncoderMethod('CBM_BETA')
        AlphaPrior(5.0)
        BetaPrior(5.0)
    ) AS dt
) WITH DATA;

-- Step 2: Transform training data (using TD_TargetEncodingTransform)
-- Step 3: Transform validation data with same FitTable
-- Step 4: Transform test data with same FitTable
-- Step 5: Train model on encoded features
-- Step 6: Deploy FitTable with model for production scoring

-- CRITICAL: Always fit on training data only!
```

### Target Encoding Methods Explained

**1. CBM_BETA (Binary Classification)**

**Use Case**: Binary target (0/1, Yes/No, Success/Failure)

**Bayesian Model**: Beta-Binomial conjugate prior

**Formula**:
```
encoded_value = (category_successes + alpha) / (category_total + alpha + beta)
```

**Example**:
```
Category: "New York"
Observations: 100
Churned: 30
Global churn rate: 0.25
Alpha: 5, Beta: 5

encoded_value = (30 + 5) / (100 + 5 + 5) = 35/110 = 0.318
```

**Interpretation**: Weighted average between category rate (0.30) and global rate (0.25)

**2. CBM_DIRICHLET (Multiclass Classification)**

**Use Case**: Multiclass target (3+ classes)

**Bayesian Model**: Dirichlet-Multinomial conjugate prior

**Formula**:
```
encoded_value_class_k = (category_count_class_k + alpha) / (category_total + alpha × num_classes)
```

**Example**:
```
Category: "USA"
Total: 200
Class 0: 80, Class 1: 70, Class 2: 50
Alpha: 2.0, Num classes: 3

encoded_value_class_0 = (80 + 2) / (200 + 2×3) = 82/206 = 0.398
encoded_value_class_1 = (70 + 2) / (200 + 2×3) = 72/206 = 0.350
encoded_value_class_2 = (50 + 2) / (200 + 2×3) = 52/206 = 0.252
```

**3. CBM_GAUSSIAN_INVERSE_GAMMA (Regression)**

**Use Case**: Continuous target variable

**Bayesian Model**: Normal-Inverse-Gamma conjugate prior

**Formula**:
```
encoded_value = (category_sum + alpha × global_mean) / (category_count + alpha)
```

**Example**:
```
Category: "Downtown"
Observations: 50
Mean price: $500,000
Category sum: $25,000,000
Global mean: $400,000
Alpha: 3.0

encoded_value = (25,000,000 + 3 × 400,000) / (50 + 3)
              = 26,200,000 / 53
              = $494,340
```

**Interpretation**: Shrinkage toward global mean, stronger for rare categories

### Use Cases and Applications

**1. High-Cardinality Feature Handling**
- Zip codes, city names, postal codes
- User IDs, customer IDs, session IDs
- Product SKUs, catalog IDs
- Domain names, URLs, email domains

**2. Gradient Boosting Feature Engineering**
- XGBoost, LightGBM, CatBoost
- Powerful single-column features
- Better than one-hot encoding for trees
- Captures monotonic relationships

**3. Click-Through Rate (CTR) Prediction**
- Ad campaigns, publishers, advertisers
- Device IDs, user segments
- Geographic locations
- Creative variants

**4. Customer Churn Prediction**
- Sales representatives, account managers
- Product tiers, subscription plans
- Acquisition channels, campaigns
- Geographic regions, territories

**5. Fraud Detection**
- Merchant IDs, transaction types
- Geographic locations, IP addresses
- Device fingerprints, user agents
- Payment methods, card types

**6. Recommendation Systems**
- User-item interaction encoding
- Category preferences
- Brand affinities
- Content type preferences

**7. Price Prediction and Valuation**
- Neighborhood, school district
- Brand, manufacturer
- Condition, features
- Market segment, category

**8. Credit Risk Modeling**
- Occupation, employer
- Geographic location
- Loan purpose, collateral type
- Industry, sector

**9. Conversion Rate Optimization**
- Landing pages, traffic sources
- Marketing campaigns, creatives
- User segments, cohorts
- Product categories, offers

**10. Natural Language Processing**
- Word encoding based on sentiment
- Entity encoding based on outcomes
- Topic encoding for classification
- Author/source encoding

### Important Notes

**Overfitting Risk:**
- Target encoding can cause severe overfitting if not properly regularized
- Always use Bayesian priors (alpha, beta) to smooth estimates
- Larger alpha/beta = stronger regularization toward global mean
- Essential for rare categories with few observations

**Data Leakage Prevention:**
- CRITICAL: Always fit on training data only
- Never fit on validation or test data
- Apply same FitTable to all datasets
- For cross-validation, use out-of-fold encoding

**Maximum Categories:**
- Each categorical column limited to 4000 unique values
- Function will fail if limit exceeded
- Consider grouping rare categories before encoding
- Or use frequency-based filtering

**Prior Selection:**
- **Weak priors (0.5-1.0)**: Large datasets, many observations per category
- **Medium priors (2.0-5.0)**: Typical use case
- **Strong priors (10.0+)**: Small datasets, rare categories, high variance
- Prior should reflect confidence in global mean

**Unseen Categories:**
- Categories in test data not in FitTable get global mean encoding
- Or NULL if no default specified
- Handle with prior or explicit unknown category
- Monitor for production drift

**Multi-Target Encoding:**
- One FitTable per target variable
- Cannot encode for multiple targets simultaneously
- Run separate fits for different targets
- Combine results in downstream pipeline

**Encoder Method Selection:**
- **CBM_BETA**: Binary classification (most common)
- **CBM_DIRICHLET**: Multiclass (3+ classes)
- **CBM_GAUSSIAN_INVERSE_GAMMA**: Regression tasks
- Match method to target variable type

**Computational Performance:**
- Fit operation computes category statistics
- Efficient aggregation over InputTable
- DIMENSION clause enables broadcasting
- Scales well to millions of rows

### Best Practices

**1. Always Fit on Training Data Only**
- Fit on training set exclusively
- Transform all datasets (train, val, test) with same FitTable
- Never include test data in fit calculation
- Prevents severe data leakage and overfitting

**2. Use Appropriate Priors**
- Start with medium priors (alpha=2-5, beta=2-5)
- Increase for rare categories or small datasets
- Decrease for large datasets with many observations per category
- Experiment and validate on holdout data

**3. Handle Rare Categories**
- Group rare categories into "Other" before encoding
- Or use strong priors to shrink toward global mean
- Consider frequency-based thresholds
- Document grouping strategy

**4. Validate Encoding Quality**
- Check encoding distributions
- Verify rare categories not overfit
- Compare category encodings to intuition
- Test on holdout data for overfitting

**5. Combine with Other Features**
- Use target encoding alongside original categorical features
- Combine with one-hot encoding for important categories
- Add interaction features
- Stack with other feature engineering

**6. Cross-Validation Strategy**
- Use out-of-fold encoding for CV
- Fit on K-1 folds, transform on held-out fold
- Prevents leakage within CV
- Or use sufficient regularization

**7. Monitor for Drift**
- Track proportion of unseen categories in production
- Monitor encoding value distributions
- Retrain fit periodically on recent data
- Alert on distribution shifts

**8. Store FitTable with Model**
- Deploy FitTable as model artifact
- Version control with model version
- Document prior choices and rationale
- Enable reproducible predictions

**9. Test Edge Cases**
- NULL values in categorical columns
- Empty strings, whitespace
- Case sensitivity issues
- Special characters

**10. Document Encoding Strategy**
- Record encoder method and priors
- Explain category grouping rules
- Document handling of unseen categories
- Enable reproducibility and auditing

### Related Functions
- **TD_TargetEncodingTransform** - Applies target encoding using FitTable (must be used after TD_TargetEncodingFit)
- **TD_OneHotEncodingFit** - Alternative encoding for low-cardinality categoricals
- **TD_OrdinalEncodingFit** - Ordinal encoding for ordered categories
- **TD_ScaleFit** - Scale numeric features after target encoding
- **TD_XGBoost** - Often benefits from target-encoded features

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Transform Functions
