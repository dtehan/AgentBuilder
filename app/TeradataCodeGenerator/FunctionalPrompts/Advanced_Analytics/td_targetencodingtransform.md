# TD_TargetEncodingTransform

### Function Name
**TD_TargetEncodingTransform**

### Description
TD_TargetEncodingTransform applies target encoding transformations using the specifications created by TD_TargetEncodingFit. This function replaces categorical values with numeric encodings derived from Bayesian posterior estimates based on the relationship between categories and the target variable, enabling machine learning algorithms to learn from high-cardinality categorical features that traditional one-hot encoding cannot handle effectively.

This is the execution component of the target encoding pipeline. After TD_TargetEncodingFit calculates Bayesian posterior estimates for each category-target relationship and stores them in a FitTable, TD_TargetEncodingTransform looks up each categorical value and replaces it with its corresponding numeric encoding. The transformation ensures consistency across training, validation, test, and production datasets by using the same encoding mappings derived exclusively from training data.

The transformation is deterministic given a FitTable, enabling reproducible preprocessing pipelines essential for machine learning deployment. Target encoding often dramatically improves model performance by capturing the predictive signal within categorical features, particularly for high-cardinality features (cities, zip codes, product IDs, user IDs) where one-hot encoding would create unwieldy dimensionality. The Bayesian approach with priors prevents overfitting on rare categories by regularizing estimates toward the global mean.

### When the Function Would Be Used
- **Apply Target Encoding**: Execute categorical-to-numeric transformations
- **ML Pipeline Execution**: Transform training, validation, and test data consistently
- **High-Cardinality Features**: Encode features with thousands of unique values
- **Production Scoring**: Transform incoming data for real-time predictions
- **Gradient Boosting Pipelines**: Create powerful features for tree-based models
- **Dimensionality Reduction**: Replace wide one-hot encodings with single numeric columns
- **Cross-Validation Workflows**: Apply consistent encoding across folds
- **Feature Engineering**: Generate predictive numeric features from categories
- **Model Deployment**: Apply production encoding with deployed FitTable
- **A/B Testing Analysis**: Transform test variants with encoded performance
- **Fraud Detection**: Encode merchants, IPs, devices with fraud rates
- **Churn Prediction**: Encode segments, channels, reps with churn rates
- **CTR Prediction**: Encode campaigns, publishers, creatives with click rates
- **Recommendation Systems**: Encode user-item interactions numerically

### Syntax

```sql
TD_TargetEncodingTransform (
    ON { table | view | (query) } AS InputTable [ PARTITION BY ANY ]
    ON { table | view | (query) } AS FitTable AS FitTableAlias DIMENSION
    USING
    [ Accumulate ({'accumulate_column' | 'accumulate_column_range'}[,...]) ]
)
```

### Required Syntax Elements for TD_TargetEncodingTransform

**ON clause (InputTable)**
- Accepts the InputTable clause containing data to transform
- Must have same categorical columns as data used for TD_TargetEncodingFit
- PARTITION BY ANY recommended for parallel processing

**ON clause (FitTable DIMENSION)**
- Accepts the FitTable clause (output from TD_TargetEncodingFit)
- Contains encoding mappings and specifications
- DIMENSION keyword required

### Optional Syntax Elements for TD_TargetEncodingTransform

**Accumulate**
- Specify input table column names to copy to output table
- Useful for preserving identifiers, keys, and metadata
- Supports column range notation
- Typically includes ID columns and target variable (for training)

### Input Table Schema

**InputTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| categorical_column | VARCHAR | Columns to be target-encoded (must match FitTable) |
| accumulate_column | ANY | [Optional] Columns to preserve in output |

**FitTable Schema:**

See TD_TargetEncodingFit Output table schema. This is the encoding specification table created by TD_TargetEncodingFit function.

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| accumulate_column | Same as InputTable | Columns specified in Accumulate parameter |
| encoded_column | DOUBLE PRECISION | Target-encoded versions of categorical columns (new column names = original + '_encoded') |
| original_categorical_column | VARCHAR | [Optional] Original categorical columns if not replaced |

Target-encoded columns are DOUBLE PRECISION type and typically have '_encoded' suffix.

### Code Examples

**Input Data: customer_data**
```
customer_id  city          payment_method  churned
1            New York      Credit Card     0
2            Los Angeles   PayPal          1
3            Chicago       Credit Card     0
4            London        Debit Card      1
5            Manchester    PayPal          1
```

**FitTable: target_encoding_fit** (created by TD_TargetEncodingFit)
```
categorical_column_name  category_value  encoding_value
city                     New York        0.33
city                     Los Angeles     0.50
city                     Chicago         0.33
city                     London          0.50
city                     Manchester      0.50
```

**Example 1: Basic Target Encoding Transformation**
```sql
-- Step 1: Create FitTable on training data (already done)
CREATE TABLE target_encoding_fit AS (
    SELECT * FROM TD_TargetEncodingFit (
        ON training_data AS InputTable
        ON training_data AS CategoricalTable DIMENSION
        USING
        TargetColumn('churned')
        CategoricalColumns('city', 'payment_method')
        EncoderMethod('CBM_BETA')
        AlphaPrior(5.0)
        BetaPrior(5.0)
    ) AS dt
) WITH DATA;

-- Step 2: Apply transformation to training data
SELECT * FROM TD_TargetEncodingTransform (
    ON customer_data AS InputTable
    ON target_encoding_fit AS FitTable DIMENSION
    USING
    Accumulate('customer_id', 'churned')
) AS dt
ORDER BY customer_id;
```

**Output:**
```
customer_id  churned  city_encoded  payment_method_encoded
1            0        0.33          0.28
2            1        0.50          0.45
3            0        0.33          0.28
4            1        0.50          0.35
5            1        0.50          0.45
```

**Example 2: Transform Training and Test Data**
```sql
-- Transform training set
CREATE TABLE training_encoded AS (
    SELECT * FROM TD_TargetEncodingTransform (
        ON training_data AS InputTable
        ON target_fit AS FitTable DIMENSION
        USING
        Accumulate('id', 'target')
    ) AS dt
) WITH DATA;

-- Transform test set with SAME FitTable
CREATE TABLE test_encoded AS (
    SELECT * FROM TD_TargetEncodingTransform (
        ON test_data AS InputTable
        ON target_fit AS FitTable DIMENSION  -- Same FitTable!
        USING
        Accumulate('id')
    ) AS dt
) WITH DATA;

-- CRITICAL: Same encoding applied to both datasets
```

**Example 3: High-Cardinality Zip Code Encoding**
```sql
-- Transform loan applications with 5000 unique zip codes
CREATE TABLE loans_encoded AS (
    SELECT * FROM TD_TargetEncodingTransform (
        ON loan_applications AS InputTable
        ON zip_encoding_fit AS FitTable DIMENSION
        USING
        Accumulate('application_id', 'applicant_name', 'loan_amount', 'defaulted')
    ) AS dt
) WITH DATA;

-- zip_code column replaced with zip_code_encoded (numeric)
-- Ready for model training with manageable dimensionality
```

**Example 4: Multiple Categorical Features**
```sql
-- Encode several high-cardinality features for click prediction
CREATE TABLE ads_encoded AS (
    SELECT * FROM TD_TargetEncodingTransform (
        ON ad_impressions AS InputTable
        ON click_encoding_fit AS FitTable DIMENSION
        USING
        Accumulate('impression_id', 'timestamp', 'clicked')
    ) AS dt
) WITH DATA;

-- Transforms: device_id, publisher_id, advertiser_id, geo_location
-- Each becomes a numeric column with click rate encoding
```

**Example 5: Complete ML Pipeline**
```sql
-- End-to-end target encoding pipeline
-- Step 1: Create fit on training data only
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

-- Step 2: Transform training data
CREATE TABLE train_encoded AS (
    SELECT * FROM TD_TargetEncodingTransform (
        ON training_set AS InputTable
        ON train_target_fit AS FitTable DIMENSION
        USING
        Accumulate('customer_id', 'churned')
    ) AS dt
) WITH DATA;

-- Step 3: Transform validation data (same FitTable)
CREATE TABLE val_encoded AS (
    SELECT * FROM TD_TargetEncodingTransform (
        ON validation_set AS InputTable
        ON train_target_fit AS FitTable DIMENSION
        USING
        Accumulate('customer_id', 'churned')
    ) AS dt
) WITH DATA;

-- Step 4: Transform test data (same FitTable)
CREATE TABLE test_encoded AS (
    SELECT * FROM TD_TargetEncodingTransform (
        ON test_set AS InputTable
        ON train_target_fit AS FitTable DIMENSION
        USING
        Accumulate('customer_id')
    ) AS dt
) WITH DATA;

-- Step 5: Train XGBoost model on train_encoded
-- Step 6: Validate on val_encoded
-- Step 7: Evaluate on test_encoded
```

**Example 6: Production Scoring Pipeline**
```sql
-- Score new customers using model trained on target-encoded data
-- Step 1: Transform incoming data using production FitTable
CREATE TABLE new_customers_encoded AS (
    SELECT * FROM TD_TargetEncodingTransform (
        ON new_customers AS InputTable
        ON prod_target_fit AS FitTable DIMENSION  -- Production FitTable
        USING
        Accumulate('customer_id', 'customer_name', 'signup_date')
    ) AS dt
) WITH DATA;

-- Step 2: Apply trained model
SELECT * FROM TD_XGBoostPredict (
    ON new_customers_encoded AS InputTable
    ON trained_xgboost_model AS ModelTable DIMENSION
    USING
    IDColumn('customer_id')
    Accumulate('customer_name', 'signup_date')
) AS dt;
```

**Example 7: Multiclass Target Encoding**
```sql
-- Transform features for product category prediction (5 classes)
CREATE TABLE products_encoded AS (
    SELECT * FROM TD_TargetEncodingTransform (
        ON product_views AS InputTable
        ON multiclass_encoding_fit AS FitTable DIMENSION
        USING
        Accumulate('view_id', 'user_id', 'purchased_category')
    ) AS dt
) WITH DATA;

-- user_country and referrer_domain encoded with class probabilities
```

**Example 8: Regression Target Encoding**
```sql
-- Transform categorical features for house price prediction
CREATE TABLE houses_encoded AS (
    SELECT * FROM TD_TargetEncodingTransform (
        ON housing_data AS InputTable
        ON regression_encoding_fit AS FitTable DIMENSION
        USING
        Accumulate('house_id', 'address', 'sale_price')
    ) AS dt
) WITH DATA;

-- neighborhood, school_district, zoning_type encoded with average sale prices
```

**Example 9: Combine with Other Feature Engineering**
```sql
-- Create comprehensive feature set with multiple transformations
-- Step 1: Target encode high-cardinality categoricals
CREATE TABLE data_target_encoded AS (
    SELECT * FROM TD_TargetEncodingTransform (
        ON raw_data AS InputTable
        ON target_fit AS FitTable DIMENSION
        USING
        Accumulate('id', 'target', 'numeric_features')
    ) AS dt
) WITH DATA;

-- Step 2: One-hot encode low-cardinality categoricals
CREATE TABLE data_onehot AS (
    SELECT * FROM TD_OneHotEncodingTransform (
        ON data_target_encoded AS InputTable
        ON onehot_fit AS FitTable DIMENSION
        USING
        Accumulate('id', 'target', 'numeric_features', '*_encoded')
    ) AS dt
) WITH DATA;

-- Step 3: Scale all numeric features
CREATE TABLE data_ml_ready AS (
    SELECT * FROM TD_ScaleTransform (
        ON data_onehot AS InputTable
        ON scale_fit AS FitTable DIMENSION
        USING
        Accumulate('id', 'target')
    ) AS dt
) WITH DATA;

-- Final dataset with target encoding + one-hot + scaling
```

**Example 10: Handle Unseen Categories**
```sql
-- Transform test data that may have unseen categories
CREATE TABLE test_encoded AS (
    SELECT
        t.*,
        COALESCE(city_encoded, 0.40) AS city_encoded_final,  -- Use global mean for unseen
        COALESCE(category_encoded, 0.25) AS category_encoded_final
    FROM TD_TargetEncodingTransform (
        ON test_data AS InputTable
        ON target_fit AS FitTable DIMENSION
        USING
        Accumulate('id', 'city', 'category')
    ) AS t
) WITH DATA;

-- Unseen categories get NULL, replaced with global mean via COALESCE
```

### Target Encoding Transformation Process

**Before Transformation:**
```
customer_id  city          payment_method
1            New York      Credit Card
2            Los Angeles   PayPal
3            Chicago       Credit Card
4            London        Debit Card
```

**FitTable (encoding mappings):**
```
categorical_column_name  category_value  encoding_value
city                     New York        0.33
city                     Los Angeles     0.50
city                     Chicago         0.33
city                     London          0.50
payment_method           Credit Card     0.28
payment_method           PayPal          0.45
payment_method           Debit Card      0.35
```

**After Transformation:**
```
customer_id  city_encoded  payment_method_encoded
1            0.33          0.28
2            0.50          0.45
3            0.33          0.28
4            0.50          0.35
```

**Key Transformation Characteristics:**
- Categorical values replaced with numeric encodings
- Encodings derived from training data target statistics
- Bayesian regularization prevents overfitting
- Unseen categories handled with global mean or NULL
- Deterministic transformation (same input + FitTable = same output)

### Use Cases and Applications

**1. Gradient Boosting Model Features**
- XGBoost, LightGBM, CatBoost feature engineering
- Powerful single-column features from high-cardinality categoricals
- Often superior to one-hot encoding for tree models
- Captures monotonic category-target relationships

**2. Click-Through Rate (CTR) Prediction**
- Encode ad campaigns with click rates
- Encode publishers, advertisers, creatives
- Encode device IDs, user segments, geolocations
- Dramatically improves CTR model performance

**3. Customer Churn Prediction**
- Encode sales reps with churn rates
- Encode product tiers, subscription plans
- Encode acquisition channels, marketing campaigns
- Encode geographic regions, territories

**4. Fraud Detection**
- Encode merchant IDs with fraud rates
- Encode IP addresses, device fingerprints
- Encode transaction types, payment methods
- Enable real-time fraud scoring

**5. E-commerce Recommendations**
- Encode product categories with purchase rates
- Encode brands, vendors with conversion rates
- Encode user segments with engagement metrics
- Personalized recommendation features

**6. Price Prediction Models**
- Encode neighborhoods with average prices
- Encode school districts, zip codes
- Encode brands, manufacturers, conditions
- Real estate and automotive valuation

**7. Credit Risk Modeling**
- Encode occupations with default rates
- Encode employers, industries, sectors
- Encode loan purposes, collateral types
- Geographic risk encoding

**8. Conversion Rate Optimization**
- Encode landing pages with conversion rates
- Encode traffic sources, campaigns, creatives
- Encode user segments, cohorts, tests
- A/B testing variant encoding

**9. Natural Language Processing**
- Encode words with sentiment scores
- Encode entities with outcome rates
- Encode authors, sources with metrics
- Topic and category encoding

**10. Healthcare and Medicine**
- Encode hospitals with outcome rates
- Encode procedures with complication rates
- Encode medications with efficacy metrics
- Diagnostic code encoding

### Important Notes

**Train-Test Consistency:**
- CRITICAL: Always fit on training data only
- Apply same FitTable to training, validation, and test sets
- Never fit on test data (causes severe data leakage)
- Store FitTable with model artifacts for production

**Output Data Types:**
- All encoded columns are DOUBLE PRECISION
- Column names typically have '_encoded' suffix
- Original categorical columns can be retained via Accumulate
- Consider downstream model requirements

**Unseen Categories:**
- Categories in test data not in FitTable may get NULL or global mean
- Monitor proportion of unseen categories in production
- Consider retraining fit periodically on recent data
- Implement fallback logic for NULL encodings

**Data Leakage Risk:**
- Target encoding highly susceptible to leakage if misused
- NEVER fit on validation or test data
- For cross-validation, use out-of-fold encoding
- Or ensure sufficient Bayesian regularization

**Performance Impact:**
- Target encoding often dramatically improves model performance
- Particularly effective for high-cardinality categoricals
- Captures non-linear category-target relationships
- Can outperform one-hot encoding for tree models

**Overfitting Prevention:**
- Bayesian priors in FitTable prevent overfitting on rare categories
- Rare categories pull toward global mean
- Common categories use observed rates
- Validate on holdout data to detect overfitting

**Computational Performance:**
- Transformation is efficient (lookup operation)
- PARTITION BY ANY enables parallel processing
- Scales well to millions of rows
- Minimal memory overhead

**Combination with Other Encodings:**
- Can combine target encoding with one-hot encoding
- Target encode high-cardinality features
- One-hot encode low-cardinality features
- Provides complementary information to models

### Best Practices

**1. Consistent Transformation Across Datasets**
- Fit on training data only
- Transform all datasets (train, val, test, production) with same FitTable
- Never refit on new data subsets
- Version control FitTable with model

**2. Handle Unseen Categories Gracefully**
- Implement fallback for NULL encodings
- Use global mean as default for unseen categories
- Monitor unseen category rates in production
- Consider retraining fit periodically

**3. Validate Transformation Results**
- Check encoded feature distributions
- Verify no extreme values or NaNs
- Compare train/test encoding distributions
- Test on sample data first

**4. Preserve Original Features**
- Use Accumulate to retain original categorical columns
- Enables debugging and analysis
- Allows model interpretation
- Facilitates data quality monitoring

**5. Combine with Other Transformations**
- Use target encoding alongside one-hot encoding
- Scale numeric features after target encoding
- Create interaction features with encoded values
- Stack multiple feature engineering techniques

**6. Production Deployment**
- Deploy FitTable as versioned model artifact
- Validate FitTable compatibility before scoring
- Implement input validation for categoricals
- Monitor for encoding issues and drift

**7. Document Encoding Strategy**
- Record FitTable creation date and training data
- Document handling of unseen categories
- Maintain encoding specifications
- Enable reproducibility and auditing

**8. Test Edge Cases**
- NULL values in categorical columns
- Empty strings, whitespace variations
- Case sensitivity issues
- Special characters in categories

**9. Monitor Downstream Impact**
- Track model performance with target encoding
- Compare to one-hot encoding baseline
- Validate business impact of predictions
- Adjust encoding strategy if needed

**10. Cross-Validation Considerations**
- Use out-of-fold encoding for proper CV
- Fit on K-1 folds, transform held-out fold
- Prevents leakage within cross-validation
- Or use sufficient Bayesian regularization

### Related Functions
- **TD_TargetEncodingFit** - Creates target encoding specifications (must be run before TD_TargetEncodingTransform)
- **TD_OneHotEncodingTransform** - Alternative encoding for low-cardinality categoricals
- **TD_OrdinalEncodingTransform** - Ordinal encoding for ordered categories
- **TD_ScaleTransform** - Scale numeric features after target encoding
- **TD_XGBoost** - Gradient boosting often benefits from target-encoded features

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Transform Functions
