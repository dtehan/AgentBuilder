# TD_ChiSq

## Function Name
- **TD_ChiSq**: Pearson's Chi-Square Test - Tests independence of categorical variables

## Description
TD_ChiSq performs Pearson's chi-squared test for independence, a statistical test used to determine whether there is a significant association between two categorical variables. The function compares observed frequencies in a contingency table to the frequencies expected if the variables were truly independent.

The chi-square test is one of the most widely used non-parametric statistical tests in data analysis. It calculates a chi-square statistic by summing the squared differences between observed and expected frequencies, weighted by the expected frequencies. The resulting statistic follows a chi-square distribution, allowing calculation of a p-value to assess statistical significance.

### Characteristics
- Tests null hypothesis that two categorical variables are independent (not associated)
- Works with nominal or ordinal categorical data
- Returns chi-square statistic, degrees of freedom, and p-value
- Non-parametric test (no assumption of normal distribution)
- Can handle any number of categories in each variable
- Requires sufficient expected frequencies (typically ≥ 5 per cell)

### Limitations
- Cannot determine direction or strength of association (only presence/absence)
- Sensitive to sample size (large samples may find trivial associations significant)
- Requires expected frequencies ≥ 5 in each cell (use Fisher's exact test if violated)
- Does not indicate causation, only association
- Cannot handle continuous variables without binning

## When to Use TD_ChiSq

TD_ChiSq is essential for analyzing relationships between categorical variables in various business and research scenarios:

### Market Research and Customer Analysis
- Test if product preference varies by demographic group
- Determine if customer churn is associated with service plan
- Analyze relationship between geographic region and purchase behavior
- Test if customer satisfaction depends on support channel used
- Evaluate if loyalty program membership affects purchase frequency category

### A/B Testing and Experimentation
- Test if conversion (yes/no) differs across test variants
- Determine if click-through rates vary by email template
- Analyze relationship between feature usage and user segment
- Test if signup method is associated with activation rate
- Evaluate if device type affects completion rate

### Quality Control and Process Analysis
- Test if defect occurrence is independent of production shift
- Determine if quality grade varies by supplier
- Analyze relationship between inspection result and facility
- Test if error type is associated with process step
- Evaluate if compliance status varies by department

### Healthcare and Clinical Research
- Test if treatment outcome is independent of patient group
- Determine if disease prevalence varies by risk factor
- Analyze relationship between diagnosis and demographic factors
- Test if adverse event occurrence is associated with drug dosage level
- Evaluate if recovery status depends on treatment protocol

### Social Science and Survey Analysis
- Test if survey response patterns vary by respondent characteristics
- Determine if voting preference is associated with age group
- Analyze relationship between education level and employment status
- Test if opinion (agree/disagree/neutral) varies by demographic
- Evaluate if behavior change is associated with intervention group

## Syntax

```sql
TD_ChiSq (
    Row_Column ('row_variable'),
    Column_Column ('column_variable'),
    [ Alpha (alpha_value) ]
)
```

**Note:** You can call this function from:
- The FROM clause of a SELECT statement
- As part of a CREATE TABLE statement
- As part of a CREATE VIEW statement

## Required Elements

### Row_Column
**Required**: Specify the name of the column representing the first categorical variable (displayed as rows in contingency table).
- **Data Type**: Categorical (VARCHAR, INTEGER for codes, etc.)
- **Description**: First categorical variable in the independence test
- **Examples**: customer_segment, product_category, geographic_region, treatment_group
- **Constraint**: Must have at least 2 distinct categories

### Column_Column
**Required**: Specify the name of the column representing the second categorical variable (displayed as columns in contingency table).
- **Data Type**: Categorical (VARCHAR, INTEGER for codes, etc.)
- **Description**: Second categorical variable in the independence test
- **Examples**: purchase_status, satisfaction_level, response_category, outcome
- **Constraint**: Must have at least 2 distinct categories

## Optional Elements

### Alpha
Specify the significance level for the hypothesis test.
- **Default**: 0.05 (95% confidence level)
- **Valid Range**: 0 < alpha < 1
- **Common Values**:
  - 0.01: 99% confidence (strict, reduces Type I error)
  - 0.05: 95% confidence (standard in most research)
  - 0.10: 90% confidence (lenient, increases power)
- **Interpretation**: If p-value < alpha, reject null hypothesis (variables are associated)

## Input Schema

### Input Table Schema
The input table should contain observations with two categorical variables.

| Column | Data Type | Description |
|--------|-----------|-------------|
| row_variable | Categorical | First categorical variable (e.g., segment, region, group) |
| column_variable | Categorical | Second categorical variable (e.g., outcome, status, response) |
| additional_columns | ANY | Optional columns for context |

**Data Requirements:**
- Each row represents one observation
- No missing values in row_variable or column_variable
- Expected frequency ≥ 5 in each cell of contingency table (otherwise use Fisher's exact test)
- Observations must be independent
- Categories should be mutually exclusive and exhaustive

## Output Schema

### Output Table Schema
The output table contains chi-square test results.

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| chi_square_statistic | FLOAT | Chi-square test statistic (sum of (O-E)²/E across all cells) |
| degrees_of_freedom | INTEGER | (number of rows - 1) × (number of columns - 1) |
| p_value | FLOAT | Probability of observing chi-square statistic if variables are independent |
| critical_value | FLOAT | Critical value from chi-square distribution at specified alpha level |

**Interpretation:**
- **chi_square_statistic**: Larger values indicate stronger association between variables
- **p_value < alpha**: Reject null hypothesis (variables are associated/dependent)
- **p_value ≥ alpha**: Fail to reject null hypothesis (no significant association detected)
- **chi_square_statistic > critical_value**: Alternative way to reject null hypothesis

## Code Examples

### Example 1: Basic Chi-Square Test - Product Preference by Region

Test if product preference is independent of geographic region:

```sql
-- Test association between region and preferred product
CREATE TABLE product_preference_chisq AS (
    SELECT * FROM TD_ChiSq(
        ON customer_preferences
        USING
        Row_Column('region')
        Column_Column('preferred_product')
        Alpha(0.05)
    )
) WITH DATA;

-- View results
SELECT
    chi_square_statistic,
    degrees_of_freedom,
    p_value,
    critical_value,
    CASE
        WHEN p_value < 0.05 THEN 'Product preference DEPENDS on region'
        ELSE 'Product preference is INDEPENDENT of region'
    END as interpretation,
    CASE
        WHEN chi_square_statistic > critical_value THEN 'Reject H0'
        ELSE 'Fail to Reject H0'
    END as decision
FROM product_preference_chisq;
```

**Business Application:**
- If significant: Tailor product offerings and marketing by region
- If not significant: Use uniform product strategy across regions

### Example 2: A/B Test Conversion Analysis

Test if conversion rate differs between control and treatment groups:

```sql
-- Chi-square test for A/B test conversion
CREATE TABLE ab_test_chisq AS (
    SELECT * FROM TD_ChiSq(
        ON ab_test_results
        USING
        Row_Column('test_variant')  -- Control vs Treatment
        Column_Column('converted')  -- Yes vs No
        Alpha(0.01)  -- Stricter significance level
    )
) WITH DATA;

-- Comprehensive result with effect size
WITH chisq_result AS (
    SELECT
        chi_square_statistic,
        degrees_of_freedom,
        p_value,
        critical_value
    FROM ab_test_chisq
),
contingency_table AS (
    SELECT
        test_variant,
        converted,
        COUNT(*) as observed_count
    FROM ab_test_results
    GROUP BY test_variant, converted
),
totals AS (
    SELECT SUM(observed_count) as n_total FROM contingency_table
)
SELECT
    c.chi_square_statistic,
    c.p_value,
    CASE
        WHEN c.p_value < 0.001 THEN 'p < 0.001 (Highly Significant)'
        WHEN c.p_value < 0.01 THEN 'p < 0.01 (Very Significant)'
        WHEN c.p_value < 0.05 THEN 'p < 0.05 (Significant)'
        ELSE 'p >= 0.05 (Not Significant)'
    END as significance_level,
    -- Cramér's V (effect size for chi-square)
    SQRT(c.chi_square_statistic / (t.n_total * (c.degrees_of_freedom / LEAST(1, 1)))) as cramers_v,
    CASE
        WHEN SQRT(c.chi_square_statistic / t.n_total) < 0.1 THEN 'Negligible Association'
        WHEN SQRT(c.chi_square_statistic / t.n_total) < 0.3 THEN 'Weak Association'
        WHEN SQRT(c.chi_square_statistic / t.n_total) < 0.5 THEN 'Moderate Association'
        ELSE 'Strong Association'
    END as effect_size_interpretation
FROM chisq_result c, totals t;
```

**Cramér's V Interpretation:**
- 0.00 - 0.10: Negligible association
- 0.10 - 0.30: Weak association
- 0.30 - 0.50: Moderate association
- > 0.50: Strong association

### Example 3: Customer Churn Analysis by Service Plan

Determine if churn rate is associated with subscription tier:

```sql
-- Test if churn depends on subscription plan
CREATE TABLE churn_analysis_chisq AS (
    SELECT * FROM TD_ChiSq(
        ON customer_data
        USING
        Row_Column('subscription_tier')  -- Basic, Premium, Enterprise
        Column_Column('churned_status')  -- Active vs Churned
        Alpha(0.05)
    )
) WITH DATA;

-- Detailed analysis with contingency table
WITH chisq_result AS (
    SELECT * FROM churn_analysis_chisq
),
observed_freq AS (
    SELECT
        subscription_tier,
        churned_status,
        COUNT(*) as observed_count
    FROM customer_data
    GROUP BY subscription_tier, churned_status
),
row_totals AS (
    SELECT subscription_tier, SUM(observed_count) as row_total
    FROM observed_freq
    GROUP BY subscription_tier
),
col_totals AS (
    SELECT churned_status, SUM(observed_count) as col_total
    FROM observed_freq
    GROUP BY churned_status
),
grand_total AS (
    SELECT SUM(observed_count) as n FROM observed_freq
)
SELECT
    o.subscription_tier,
    o.churned_status,
    o.observed_count,
    -- Calculate expected frequency
    CAST(r.row_total AS FLOAT) * c.col_total / g.n as expected_count,
    -- Cell contribution to chi-square
    POWER(o.observed_count - (CAST(r.row_total AS FLOAT) * c.col_total / g.n), 2) /
        (CAST(r.row_total AS FLOAT) * c.col_total / g.n) as chi_sq_contribution,
    -- Percentage of total chi-square
    (POWER(o.observed_count - (CAST(r.row_total AS FLOAT) * c.col_total / g.n), 2) /
        (CAST(r.row_total AS FLOAT) * c.col_total / g.n)) /
        (SELECT chi_square_statistic FROM chisq_result) * 100 as pct_of_chi_sq
FROM observed_freq o, row_totals r, col_totals c, grand_total g
WHERE o.subscription_tier = r.subscription_tier
  AND o.churned_status = c.churned_status
ORDER BY chi_sq_contribution DESC;
```

**Cell Analysis:**
- High chi_sq_contribution indicates cells that deviate most from independence
- Identify which tier/status combinations drive the association
- Target retention efforts at high-risk segments

### Example 4: Quality Control - Defect Rate by Supplier

Test if defect occurrence is independent of supplier:

```sql
-- Chi-square test for quality by supplier
CREATE TABLE quality_chisq AS (
    SELECT * FROM TD_ChiSq(
        ON inspection_results
        USING
        Row_Column('supplier_id')
        Column_Column('quality_grade')  -- Pass, Minor Defect, Major Defect
        Alpha(0.01)
    )
) WITH DATA;

-- Summary with observed vs expected frequencies
WITH chisq_stats AS (
    SELECT * FROM quality_chisq
)
SELECT
    'Chi-Square Test Results' as summary_type,
    chi_square_statistic as stat_value,
    degrees_of_freedom as df,
    p_value as p_val,
    CASE
        WHEN p_value < 0.01 THEN 'Quality varies significantly by supplier - AUDIT NEEDED'
        ELSE 'Quality is consistent across suppliers'
    END as recommendation
FROM chisq_stats

UNION ALL

-- Add contingency table summary
SELECT
    'Contingency Table' as summary_type,
    CAST(supplier_id AS FLOAT) as stat_value,
    CAST(NULL AS INTEGER) as df,
    CAST(NULL AS FLOAT) as p_val,
    quality_grade || ': ' || CAST(COUNT(*) AS VARCHAR(20)) as recommendation
FROM inspection_results
GROUP BY supplier_id, quality_grade
ORDER BY summary_type DESC, stat_value;
```

**Quality Decision:**
- Significant result: Some suppliers have different quality profiles
- Investigate high chi-square contribution cells
- Consider supplier consolidation or re-qualification

### Example 5: Healthcare - Treatment Outcome by Age Group

Analyze relationship between patient age group and treatment outcome:

```sql
-- Test if treatment outcome is independent of age group
CREATE TABLE treatment_outcome_chisq AS (
    SELECT * FROM TD_ChiSq(
        ON patient_outcomes
        USING
        Row_Column('age_group')  -- 18-30, 31-50, 51-70, 71+
        Column_Column('outcome')  -- Improved, No Change, Worsened
        Alpha(0.05)
    )
) WITH DATA;

-- Comprehensive report with standardized residuals
WITH chisq_result AS (
    SELECT * FROM treatment_outcome_chisq
),
observed_freq AS (
    SELECT
        age_group,
        outcome,
        COUNT(*) as obs_count,
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY age_group) as row_pct
    FROM patient_outcomes
    GROUP BY age_group, outcome
),
row_totals AS (
    SELECT age_group, SUM(obs_count) as row_total FROM observed_freq GROUP BY age_group
),
col_totals AS (
    SELECT outcome, SUM(obs_count) as col_total FROM observed_freq GROUP BY outcome
),
grand_total AS (
    SELECT SUM(obs_count) as n FROM observed_freq
)
SELECT
    'Test Statistics' as report_section,
    'Chi-Square' as metric,
    ROUND((SELECT chi_square_statistic FROM chisq_result), 3) as value,
    'p-value: ' || CAST(ROUND((SELECT p_value FROM chisq_result), 6) AS VARCHAR(20)) as interpretation

UNION ALL

SELECT
    'Observed Frequencies' as report_section,
    o.age_group || ' - ' || o.outcome as metric,
    o.obs_count as value,
    CAST(ROUND(o.row_pct, 1) AS VARCHAR(20)) || '% of age group' as interpretation
FROM observed_freq o

UNION ALL

SELECT
    'Decision' as report_section,
    CASE
        WHEN (SELECT p_value FROM chisq_result) < 0.05
        THEN 'Outcome varies by age'
        ELSE 'Outcome independent of age'
    END as metric,
    CAST(NULL AS FLOAT) as value,
    CASE
        WHEN (SELECT p_value FROM chisq_result) < 0.05
        THEN 'Age-specific treatment protocols recommended'
        ELSE 'Standard protocol appropriate for all ages'
    END as interpretation

ORDER BY report_section DESC, metric;
```

**Clinical Application:**
- Significant: Different age groups respond differently to treatment
- Develop age-stratified treatment guidelines
- Consider age as a factor in treatment selection

### Example 6: Survey Analysis - Opinion by Demographic

Test relationship between demographic group and survey response:

```sql
-- Chi-square test for opinion independence
CREATE TABLE survey_opinion_chisq AS (
    SELECT * FROM TD_ChiSq(
        ON survey_responses
        USING
        Row_Column('demographic_segment')  -- Segment A, B, C, D
        Column_Column('opinion_category')  -- Strongly Agree, Agree, Neutral, Disagree, Strongly Disagree
        Alpha(0.05)
    )
) WITH DATA;

-- Calculate multiple association measures
WITH chisq_stats AS (
    SELECT * FROM survey_opinion_chisq
),
sample_info AS (
    SELECT
        COUNT(*) as n_total,
        COUNT(DISTINCT demographic_segment) as n_rows,
        COUNT(DISTINCT opinion_category) as n_cols
    FROM survey_responses
)
SELECT
    c.chi_square_statistic,
    c.degrees_of_freedom,
    ROUND(c.p_value, 6) as p_value,
    -- Cramér's V (standardized effect size)
    ROUND(SQRT(c.chi_square_statistic / (s.n_total * LEAST(s.n_rows - 1, s.n_cols - 1))), 3) as cramers_v,
    -- Contingency Coefficient
    ROUND(SQRT(c.chi_square_statistic / (c.chi_square_statistic + s.n_total)), 3) as contingency_coef,
    CASE
        WHEN c.p_value < 0.001 THEN '*** Highly Significant Association'
        WHEN c.p_value < 0.01 THEN '** Very Significant Association'
        WHEN c.p_value < 0.05 THEN '* Significant Association'
        ELSE 'No Significant Association'
    END as result,
    CASE
        WHEN SQRT(c.chi_square_statistic / (s.n_total * LEAST(s.n_rows - 1, s.n_cols - 1))) < 0.1 THEN 'Negligible'
        WHEN SQRT(c.chi_square_statistic / (s.n_total * LEAST(s.n_rows - 1, s.n_cols - 1))) < 0.3 THEN 'Weak'
        WHEN SQRT(c.chi_square_statistic / (s.n_total * LEAST(s.n_rows - 1, s.n_cols - 1))) < 0.5 THEN 'Moderate'
        ELSE 'Strong'
    END as effect_magnitude
FROM chisq_stats c, sample_info s;
```

**Survey Insight:**
- Significant association: Opinions differ across demographic segments
- Target messaging and policy decisions by segment
- Effect size indicates practical importance of differences

## Common Use Cases

### 1. Customer Segmentation Validation

```sql
-- Verify if customer behavior segments have different conversion patterns
CREATE TABLE segment_conversion_chisq AS (
    SELECT * FROM TD_ChiSq(
        ON customer_behavior
        USING
        Row_Column('behavior_segment')
        Column_Column('conversion_tier')  -- High, Medium, Low
        Alpha(0.05)
    )
) WITH DATA;

SELECT
    CASE
        WHEN p_value < 0.05 THEN 'Segments have different conversion patterns - Segmentation is valid'
        ELSE 'No difference detected - Reconsider segmentation approach'
    END as validation_result
FROM segment_conversion_chisq;
```

### 2. Risk Factor Analysis

```sql
-- Test if risk factor presence is associated with adverse outcome
CREATE TABLE risk_factor_chisq AS (
    SELECT * FROM TD_ChiSq(
        ON patient_data
        USING
        Row_Column('risk_factor_present')  -- Yes vs No
        Column_Column('adverse_outcome')  -- Occurred vs Did Not Occur
        Alpha(0.01)
    )
) WITH DATA;

-- Calculate odds ratio from contingency table
WITH counts AS (
    SELECT
        risk_factor_present,
        adverse_outcome,
        COUNT(*) as cnt
    FROM patient_data
    GROUP BY risk_factor_present, adverse_outcome
)
SELECT
    (SELECT cnt FROM counts WHERE risk_factor_present = 'Yes' AND adverse_outcome = 'Occurred') *
    (SELECT cnt FROM counts WHERE risk_factor_present = 'No' AND adverse_outcome = 'Did Not Occur') /
    NULLIFZERO(
        (SELECT cnt FROM counts WHERE risk_factor_present = 'Yes' AND adverse_outcome = 'Did Not Occur') *
        (SELECT cnt FROM counts WHERE risk_factor_present = 'No' AND adverse_outcome = 'Occurred')
    ) as odds_ratio,
    p_value
FROM risk_factor_chisq;
```

### 3. Feature Importance for Categorical Predictors

```sql
-- Test which categorical features are associated with target variable
CREATE TABLE feature_importance_summary AS (
    SELECT 'gender' as feature_name, * FROM TD_ChiSq(
        ON model_data USING Row_Column('gender') Column_Column('target') Alpha(0.05)
    )
    UNION ALL
    SELECT 'region' as feature_name, * FROM TD_ChiSq(
        ON model_data USING Row_Column('region') Column_Column('target') Alpha(0.05)
    )
    UNION ALL
    SELECT 'product_category' as feature_name, * FROM TD_ChiSq(
        ON model_data USING Row_Column('product_category') Column_Column('target') Alpha(0.05)
    )
) WITH DATA;

-- Rank features by association strength
SELECT
    feature_name,
    chi_square_statistic,
    p_value,
    RANK() OVER (ORDER BY chi_square_statistic DESC) as importance_rank,
    CASE WHEN p_value < 0.05 THEN 'Include in Model' ELSE 'Consider Excluding' END as recommendation
FROM feature_importance_summary
ORDER BY chi_square_statistic DESC;
```

## Best Practices

1. **Verify Expected Frequency Assumption**:
   - Expected frequency ≥ 5 in all cells (80% rule: at least 80% of cells)
   - If violated, combine categories or use Fisher's exact test
   - Calculate expected frequencies: (row_total × column_total) / grand_total

2. **Calculate and Report Effect Size**:
   - Chi-square statistic is influenced by sample size
   - Use Cramér's V for standardized effect size
   - Report both statistical and practical significance

3. **Examine Contingency Table**:
   - Don't just look at overall p-value
   - Calculate standardized residuals to find which cells drive association
   - Identify patterns in observed vs expected frequencies

4. **Consider Sample Size**:
   - Very large samples may detect trivial associations as significant
   - Very small samples may lack power to detect real associations
   - Aim for adequate but not excessive sample sizes

5. **Interpret Causation Carefully**:
   - Association ≠ causation
   - Chi-square tests correlation, not causal direction
   - Use experimental design or causal inference methods for causation

6. **Handle Multiple Testing**:
   - Testing many variable pairs increases Type I error
   - Apply Bonferroni correction: divide alpha by number of tests
   - Or use False Discovery Rate (FDR) methods

7. **Report Comprehensive Results**:
   - Include contingency table with counts and percentages
   - Report chi-square statistic, df, p-value, and effect size
   - Provide business context and interpretation
   - Visualize with mosaic plots or stacked bar charts

## Related Functions

- **TD_ANOVA**: Compare means across multiple groups (continuous dependent variable)
- **TD_FTest**: Compare variances between two groups
- **TD_ZTest**: Compare proportions between two groups (alternative for 2×2 tables)
- **COUNT / GROUP BY**: Create contingency tables manually
- **CASE WHEN**: Bin continuous variables into categories for chi-square test

## Notes and Limitations

1. **Expected Frequency Rule**:
   - Classic rule: All cells should have expected frequency ≥ 5
   - Modern rule: At least 80% of cells should have expected frequency ≥ 5
   - For 2×2 tables with small samples, use Fisher's exact test instead

2. **Sample Size Effects**:
   - Large samples: Even trivial associations become significant
   - Small samples: May lack power to detect real associations
   - Always examine effect size alongside p-value

3. **Continuity Correction**:
   - Some implementations apply Yates' continuity correction for 2×2 tables
   - Check if TD_ChiSq applies this correction
   - Correction is conservative (increases p-value)

4. **Independence Assumption**:
   - Each observation must be independent
   - Repeated measures or paired data violate assumption
   - Use McNemar's test for paired categorical data

5. **Direction of Association**:
   - Chi-square doesn't indicate which variable influences the other
   - Cannot determine causation from chi-square test alone
   - Use odds ratios or relative risk for 2×2 tables

6. **Multiple Categories**:
   - With many categories, chi-square may have low power
   - Consider collapsing rare categories
   - Or use more sophisticated methods (correspondence analysis)

7. **Non-Significant Results**:
   - "No significant association" ≠ "variables are independent"
   - May lack power to detect weak associations
   - Report confidence intervals when possible

## Version Information

- **Function Version**: Based on Teradata Database Analytic Functions Version 17.20
- **Generated**: November 28, 2025
- **Category**: Hypothesis Testing / Statistical Analysis
