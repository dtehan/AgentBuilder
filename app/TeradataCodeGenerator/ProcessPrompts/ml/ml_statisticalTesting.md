---
name: Statistical Testing Workflow
allowed-tools:
description: Complete workflow for statistical hypothesis testing in Teradata
argument-hint: [database_name] [table_name] [test_type] [variables]
---

# Statistical Testing Workflow

## Overview
This workflow guides you through statistical hypothesis testing in Teradata, including A/B testing, group comparisons, and hypothesis validation using rigorous statistical methods.

## Variables
DATABASE_NAME: $1
TABLE_NAME: $2
TEST_TYPE: $3 (anova|chisq|ftest|ztest|ttest)
VARIABLES: $4 (comma-separated list of variables to test)

## Prerequisites
- Data should be properly structured with groups/categories
- Sample sizes should be adequate for chosen test
- Assumptions of each test should be validated
- Understanding of hypothesis testing fundamentals

## Statistical Testing Use Cases

### A/B Testing and Experimentation
- Website conversion rate comparison
- Email campaign effectiveness
- Feature launch impact analysis
- Pricing strategy validation
- UI/UX variant testing
- Marketing channel performance

### Group Comparisons
- Customer segment differences
- Regional performance comparison
- Product line analysis
- Time period comparisons
- Treatment vs. control groups
- Before/after analysis

### Quality Control and Process Validation
- Manufacturing process consistency
- Service quality metrics
- Operational efficiency testing
- Compliance validation
- SLA achievement testing

### Business Decision Support
- Market segment homogeneity
- Promotion effectiveness
- Risk assessment validation
- Strategy evaluation
- Resource allocation decisions

### Research and Analytics
- Correlation validation
- Causal inference
- Survey analysis
- Clinical trial analysis
- Social science research

## Workflow Stages

### Stage 0: Data Exploration and Validation

**Verify data structure:**
```sql
-- Check data availability and structure
SELECT COUNT(*) as total_rows,
       COUNT(DISTINCT group_column) as num_groups,
       COUNT(metric_column) as non_null_metrics
FROM ${DATABASE_NAME}.${TABLE_NAME};

-- Sample data inspection
SELECT *
FROM ${DATABASE_NAME}.${TABLE_NAME}
SAMPLE 20;
```

**Analyze group distributions:**
```sql
-- Group sizes and basic statistics
SELECT
    group_column,
    COUNT(*) as sample_size,
    AVG(metric_column) as mean,
    STDDEV_POP(metric_column) as std_dev,
    MIN(metric_column) as min_value,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY metric_column) as q1,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY metric_column) as median,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY metric_column) as q3,
    MAX(metric_column) as max_value
FROM ${DATABASE_NAME}.${TABLE_NAME}
GROUP BY group_column
ORDER BY group_column;
```

**Check for missing data:**
```sql
-- Missing data analysis
SELECT
    COUNT(*) as total_rows,
    COUNT(metric_column) as non_null_metrics,
    COUNT(*) - COUNT(metric_column) as missing_count,
    CAST(COUNT(*) - COUNT(metric_column) AS FLOAT) / COUNT(*) * 100 as missing_percentage
FROM ${DATABASE_NAME}.${TABLE_NAME};
```

### Stage 1: Problem Definition and Hypothesis Formulation

**Define Statistical Hypotheses:**

1. **State the Research Question:**
   - What are you trying to prove or disprove?
   - What is the business decision dependent on this test?

2. **Formulate Null Hypothesis (H0):**
   - **ANOVA/F-Test**: All group means are equal
   - **Chi-Square**: Variables are independent (no association)
   - **Z-Test/T-Test**: Group means are equal (no difference)

3. **Formulate Alternative Hypothesis (H1):**
   - **ANOVA/F-Test**: At least one group mean differs
   - **Chi-Square**: Variables are associated
   - **Z-Test/T-Test**: Group means are different

4. **Set Significance Level (Alpha):**
   - **α = 0.05** (Standard - 95% confidence)
   - **α = 0.01** (Strict - 99% confidence)
   - **α = 0.10** (Lenient - 90% confidence)

**Decision Rule:**
- If p-value < α: Reject null hypothesis (statistically significant)
- If p-value ≥ α: Fail to reject null hypothesis (not significant)

### Stage 2: Test Selection and Assumptions

**Decision Matrix: Which Statistical Test?**

| Test | Use Case | Data Type | Assumptions | Teradata Function |
|------|----------|-----------|-------------|-------------------|
| **ANOVA** | Compare 3+ group means | Continuous metric, categorical groups | Normal distribution, equal variances | TD_ANOVA |
| **Chi-Square** | Test independence of categorical variables | Categorical data | Expected frequencies ≥ 5 | TD_ChiSq |
| **F-Test** | Compare two variances | Continuous metrics | Normal distribution | TD_FTest |
| **Z-Test** | Compare means (large samples) | Continuous metric | Normal distribution, n>30 | TD_ZTest |
| **T-Test** | Compare means (small samples) | Continuous metric | Normal distribution, n≤30 | TD_TTest |

**Ask User:**
"Which statistical test do you need?
1. **ANOVA** - Compare means across 3+ groups
2. **Chi-Square** - Test independence of categorical variables
3. **F-Test** - Compare variances between two groups
4. **Z-Test** - Compare means with large samples (n>30)
5. **T-Test** - Compare means with small samples (n≤30)"

### Stage 3: Assumption Validation

#### Check Normality Assumption

```sql
-- Visual normality check: Compare mean and median
WITH stats AS (
    SELECT
        group_column,
        AVG(metric_column) as mean,
        PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY metric_column) as median,
        STDDEV_POP(metric_column) as std_dev
    FROM ${DATABASE_NAME}.${TABLE_NAME}
    GROUP BY group_column
)
SELECT
    group_column,
    mean,
    median,
    ABS(mean - median) / NULLIFZERO(std_dev) as skewness_indicator
FROM stats;
```

**Normality Interpretation:**
- **skewness_indicator < 0.2**: Likely normal
- **skewness_indicator 0.2-0.5**: Moderately skewed
- **skewness_indicator > 0.5**: Highly skewed (consider transformation)

#### Check Equal Variance Assumption (Homoscedasticity)

```sql
-- Compare variances across groups
WITH variances AS (
    SELECT
        group_column,
        COUNT(*) as n,
        VARIANCE(metric_column) as variance,
        STDDEV_POP(metric_column) as std_dev
    FROM ${DATABASE_NAME}.${TABLE_NAME}
    GROUP BY group_column
)
SELECT
    group_column,
    n,
    variance,
    std_dev,
    variance / NULLIFZERO((SELECT MAX(variance) FROM variances)) as variance_ratio
FROM variances
ORDER BY group_column;
```

**Equal Variance Interpretation:**
- **variance_ratio between 0.5 and 2.0**: Approximately equal variances
- **variance_ratio < 0.5 or > 2.0**: Consider Welch's correction or non-parametric test

#### Check Sample Size Requirements

```sql
-- Verify adequate sample sizes
SELECT
    group_column,
    COUNT(*) as sample_size,
    CASE
        WHEN COUNT(*) < 10 THEN 'Too Small - Use non-parametric test'
        WHEN COUNT(*) < 30 THEN 'Small - Use T-Test'
        WHEN COUNT(*) >= 30 THEN 'Large - Use Z-Test or ANOVA'
    END as sample_size_category
FROM ${DATABASE_NAME}.${TABLE_NAME}
GROUP BY group_column
ORDER BY sample_size;
```

### Stage 4: Statistical Test Execution

#### Test A: ANOVA (Analysis of Variance)

**Use case:** Compare means across 3 or more groups

```sql
-- One-Way ANOVA
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_anova_results AS
SELECT TD_ANOVA(
    DependentColumn('metric_column'),    -- Continuous variable to test
    FactorColumn('group_column'),        -- Grouping variable
    Alpha(0.05)                          -- Significance level
)
FROM ${DATABASE_NAME}.${TABLE_NAME}
WITH DATA;

-- View ANOVA results
SELECT
    source,                               -- Between groups, Within groups, Total
    sum_of_squares,
    degrees_of_freedom,
    mean_square,
    f_statistic,
    p_value,
    CASE WHEN p_value < 0.05 THEN 'Significant' ELSE 'Not Significant' END as result
FROM ${DATABASE_NAME}.${TABLE_NAME}_anova_results;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_anova.md

**ANOVA Interpretation:**
- **F-statistic**: Ratio of between-group to within-group variability
- **p-value < 0.05**: At least one group mean differs significantly
- **p-value ≥ 0.05**: No significant difference between groups

**Post-hoc Analysis (if ANOVA is significant):**
```sql
-- Pairwise comparisons to identify which groups differ
WITH group_stats AS (
    SELECT
        group_column,
        AVG(metric_column) as group_mean,
        COUNT(*) as group_n,
        STDDEV_POP(metric_column) as group_std
    FROM ${DATABASE_NAME}.${TABLE_NAME}
    GROUP BY group_column
)
SELECT
    g1.group_column as group_1,
    g2.group_column as group_2,
    g1.group_mean as mean_1,
    g2.group_mean as mean_2,
    ABS(g1.group_mean - g2.group_mean) as mean_difference,
    -- Simple effect size (Cohen's d approximation)
    ABS(g1.group_mean - g2.group_mean) /
        SQRT((POWER(g1.group_std, 2) + POWER(g2.group_std, 2)) / 2) as effect_size
FROM group_stats g1
CROSS JOIN group_stats g2
WHERE g1.group_column < g2.group_column
ORDER BY mean_difference DESC;
```

#### Test B: Chi-Square Test of Independence

**Use case:** Test if two categorical variables are independent

```sql
-- Chi-Square Test
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_chisq_results AS
SELECT TD_ChiSq(
    Row_Column('category_1'),            -- First categorical variable
    Column_Column('category_2'),         -- Second categorical variable
    Alpha(0.05)
)
FROM ${DATABASE_NAME}.${TABLE_NAME}
WITH DATA;

-- View Chi-Square results
SELECT
    chi_square_statistic,
    degrees_of_freedom,
    p_value,
    CASE WHEN p_value < 0.05 THEN 'Variables are Associated (Reject H0)'
         ELSE 'Variables are Independent (Fail to Reject H0)' END as interpretation
FROM ${DATABASE_NAME}.${TABLE_NAME}_chisq_results;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_chisq.md

**Contingency Table Analysis:**
```sql
-- Create contingency table with observed and expected frequencies
WITH observed AS (
    SELECT
        category_1,
        category_2,
        COUNT(*) as observed_count
    FROM ${DATABASE_NAME}.${TABLE_NAME}
    GROUP BY category_1, category_2
),
totals AS (
    SELECT
        SUM(observed_count) as grand_total
    FROM observed
),
row_totals AS (
    SELECT category_1, SUM(observed_count) as row_total
    FROM observed
    GROUP BY category_1
),
col_totals AS (
    SELECT category_2, SUM(observed_count) as col_total
    FROM observed
    GROUP BY category_2
)
SELECT
    o.category_1,
    o.category_2,
    o.observed_count,
    CAST(r.row_total AS FLOAT) * c.col_total / t.grand_total as expected_count,
    POWER(o.observed_count - (CAST(r.row_total AS FLOAT) * c.col_total / t.grand_total), 2) /
        NULLIFZERO(CAST(r.row_total AS FLOAT) * c.col_total / t.grand_total) as chi_square_contribution
FROM observed o, row_totals r, col_totals c, totals t
WHERE o.category_1 = r.category_1
  AND o.category_2 = c.category_2
ORDER BY chi_square_contribution DESC;
```

**Chi-Square Interpretation:**
- **p-value < 0.05**: Variables are associated (dependent)
- **p-value ≥ 0.05**: Variables are independent
- **Chi-square contribution**: Shows which cells contribute most to association

#### Test C: F-Test (Variance Comparison)

**Use case:** Compare variances between two groups

```sql
-- F-Test for Equal Variances
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_ftest_results AS
SELECT TD_FTest(
    Sample1Column('group_1_values'),     -- First group values
    Sample2Column('group_2_values'),     -- Second group values
    Alpha(0.05),
    Alternative('two-sided')             -- 'two-sided', 'less', 'greater'
)
FROM (
    SELECT
        MAX(CASE WHEN group_column = 'Group1' THEN metric_column END) as group_1_values,
        MAX(CASE WHEN group_column = 'Group2' THEN metric_column END) as group_2_values
    FROM ${DATABASE_NAME}.${TABLE_NAME}
    GROUP BY row_id
)
WITH DATA;

-- View F-Test results
SELECT
    f_statistic,
    numerator_df,
    denominator_df,
    p_value,
    CASE WHEN p_value < 0.05 THEN 'Variances are Different'
         ELSE 'Variances are Equal' END as interpretation
FROM ${DATABASE_NAME}.${TABLE_NAME}_ftest_results;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_ftest.md

**Variance Ratio Analysis:**
```sql
-- Calculate variance ratio
WITH group_variances AS (
    SELECT
        group_column,
        VARIANCE(metric_column) as variance,
        STDDEV_POP(metric_column) as std_dev,
        COUNT(*) as n
    FROM ${DATABASE_NAME}.${TABLE_NAME}
    WHERE group_column IN ('Group1', 'Group2')
    GROUP BY group_column
)
SELECT
    g1.variance as variance_group1,
    g2.variance as variance_group2,
    g1.variance / NULLIFZERO(g2.variance) as variance_ratio,
    g1.std_dev as std_dev_group1,
    g2.std_dev as std_dev_group2
FROM group_variances g1, group_variances g2
WHERE g1.group_column = 'Group1'
  AND g2.group_column = 'Group2';
```

#### Test D: Z-Test (Large Sample Mean Comparison)

**Use case:** Compare means between groups with large samples (n > 30)

```sql
-- Two-Sample Z-Test
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_ztest_results AS
SELECT TD_ZTest(
    Sample1Column('group_1_values'),     -- First group values
    Sample2Column('group_2_values'),     -- Second group values
    Alpha(0.05),
    Alternative('two-sided'),            -- 'two-sided', 'less', 'greater'
    PopulationStdDev1(NULL),             -- Use sample std if unknown
    PopulationStdDev2(NULL)
)
FROM (
    SELECT
        MAX(CASE WHEN group_column = 'Group1' THEN metric_column END) as group_1_values,
        MAX(CASE WHEN group_column = 'Group2' THEN metric_column END) as group_2_values
    FROM ${DATABASE_NAME}.${TABLE_NAME}
    GROUP BY row_id
)
WITH DATA;

-- View Z-Test results
SELECT
    z_statistic,
    p_value,
    mean_difference,
    standard_error,
    confidence_interval_lower,
    confidence_interval_upper,
    CASE WHEN p_value < 0.05 THEN 'Means are Significantly Different'
         ELSE 'No Significant Difference' END as interpretation
FROM ${DATABASE_NAME}.${TABLE_NAME}_ztest_results;
```

**Function Reference**: FunctionalPrompts/Advanced_Analytics/td_ztest.md

**Detailed Group Comparison:**
```sql
-- Calculate effect size and confidence intervals
WITH group_stats AS (
    SELECT
        group_column,
        COUNT(*) as n,
        AVG(metric_column) as mean,
        STDDEV_POP(metric_column) as std_dev,
        STDDEV_POP(metric_column) / SQRT(COUNT(*)) as std_error
    FROM ${DATABASE_NAME}.${TABLE_NAME}
    WHERE group_column IN ('Group1', 'Group2')
    GROUP BY group_column
)
SELECT
    g1.mean as mean_group1,
    g2.mean as mean_group2,
    g1.mean - g2.mean as mean_difference,
    SQRT(POWER(g1.std_error, 2) + POWER(g2.std_error, 2)) as pooled_se,
    -- 95% Confidence Interval for difference
    (g1.mean - g2.mean) - 1.96 * SQRT(POWER(g1.std_error, 2) + POWER(g2.std_error, 2)) as ci_lower,
    (g1.mean - g2.mean) + 1.96 * SQRT(POWER(g1.std_error, 2) + POWER(g2.std_error, 2)) as ci_upper,
    -- Cohen's d (effect size)
    (g1.mean - g2.mean) / SQRT((POWER(g1.std_dev, 2) + POWER(g2.std_dev, 2)) / 2) as cohens_d
FROM group_stats g1, group_stats g2
WHERE g1.group_column = 'Group1'
  AND g2.group_column = 'Group2';
```

**Effect Size Interpretation (Cohen's d):**
- **|d| < 0.2**: Negligible effect
- **|d| 0.2-0.5**: Small effect
- **|d| 0.5-0.8**: Medium effect
- **|d| > 0.8**: Large effect

### Stage 5: Results Interpretation and Reporting

#### Statistical Significance vs. Practical Significance

```sql
-- Comprehensive test summary
WITH test_results AS (
    SELECT
        'Group1 vs Group2' as comparison,
        g1.n as n1,
        g2.n as n2,
        g1.mean as mean1,
        g2.mean as mean2,
        g1.mean - g2.mean as mean_diff,
        (g1.mean - g2.mean) / NULLIFZERO(g1.mean) * 100 as pct_change,
        SQRT((POWER(g1.std_dev, 2) / g1.n) + (POWER(g2.std_dev, 2) / g2.n)) as se_diff,
        (g1.mean - g2.mean) / SQRT((POWER(g1.std_dev, 2) + POWER(g2.std_dev, 2)) / 2) as effect_size
    FROM (
        SELECT
            COUNT(*) as n,
            AVG(metric_column) as mean,
            STDDEV_POP(metric_column) as std_dev
        FROM ${DATABASE_NAME}.${TABLE_NAME}
        WHERE group_column = 'Group1'
    ) g1,
    (
        SELECT
            COUNT(*) as n,
            AVG(metric_column) as mean,
            STDDEV_POP(metric_column) as std_dev
        FROM ${DATABASE_NAME}.${TABLE_NAME}
        WHERE group_column = 'Group2'
    ) g2
)
SELECT
    *,
    -- Z-score calculation
    mean_diff / NULLIFZERO(se_diff) as z_score,
    -- Approximate p-value (two-tailed)
    CASE
        WHEN ABS(mean_diff / NULLIFZERO(se_diff)) > 2.576 THEN '< 0.01 (Highly Significant)'
        WHEN ABS(mean_diff / NULLIFZERO(se_diff)) > 1.96 THEN '< 0.05 (Significant)'
        ELSE '>= 0.05 (Not Significant)'
    END as significance,
    CASE
        WHEN ABS(effect_size) < 0.2 THEN 'Negligible'
        WHEN ABS(effect_size) < 0.5 THEN 'Small'
        WHEN ABS(effect_size) < 0.8 THEN 'Medium'
        ELSE 'Large'
    END as practical_significance
FROM test_results;
```

#### A/B Test Decision Framework

```sql
-- A/B Test Summary Report
CREATE TABLE ${DATABASE_NAME}.${TABLE_NAME}_ab_test_summary AS
WITH control_stats AS (
    SELECT
        COUNT(*) as n_control,
        AVG(conversion_metric) as conversion_rate_control,
        STDDEV_POP(conversion_metric) as std_control
    FROM ${DATABASE_NAME}.${TABLE_NAME}
    WHERE test_group = 'Control'
),
treatment_stats AS (
    SELECT
        COUNT(*) as n_treatment,
        AVG(conversion_metric) as conversion_rate_treatment,
        STDDEV_POP(conversion_metric) as std_treatment
    FROM ${DATABASE_NAME}.${TABLE_NAME}
    WHERE test_group = 'Treatment'
)
SELECT
    c.n_control,
    t.n_treatment,
    c.conversion_rate_control,
    t.conversion_rate_treatment,
    t.conversion_rate_treatment - c.conversion_rate_control as absolute_lift,
    (t.conversion_rate_treatment - c.conversion_rate_control) /
        NULLIFZERO(c.conversion_rate_control) * 100 as relative_lift_pct,
    -- Z-test for proportions
    (t.conversion_rate_treatment - c.conversion_rate_control) /
        SQRT((c.conversion_rate_control * (1 - c.conversion_rate_control) / c.n_control) +
             (t.conversion_rate_treatment * (1 - t.conversion_rate_treatment) / t.n_treatment)) as z_score,
    CASE
        WHEN ABS((t.conversion_rate_treatment - c.conversion_rate_control) /
            SQRT((c.conversion_rate_control * (1 - c.conversion_rate_control) / c.n_control) +
                 (t.conversion_rate_treatment * (1 - t.conversion_rate_treatment) / t.n_treatment))) > 1.96
        THEN 'YES - Roll out treatment'
        ELSE 'NO - Keep control'
    END as decision
FROM control_stats c, treatment_stats t
WITH DATA;
```

### Stage 6: Power Analysis and Sample Size Planning

#### Post-hoc Power Analysis

```sql
-- Calculate achieved statistical power
WITH test_params AS (
    SELECT
        g1.mean - g2.mean as observed_diff,
        SQRT((POWER(g1.std_dev, 2) + POWER(g2.std_dev, 2)) / 2) as pooled_std,
        g1.n as n1,
        g2.n as n2
    FROM (
        SELECT AVG(metric_column) as mean, STDDEV_POP(metric_column) as std_dev, COUNT(*) as n
        FROM ${DATABASE_NAME}.${TABLE_NAME} WHERE group_column = 'Group1'
    ) g1,
    (
        SELECT AVG(metric_column) as mean, STDDEV_POP(metric_column) as std_dev, COUNT(*) as n
        FROM ${DATABASE_NAME}.${TABLE_NAME} WHERE group_column = 'Group2'
    ) g2
)
SELECT
    observed_diff,
    pooled_std,
    observed_diff / NULLIFZERO(pooled_std) as effect_size,
    n1,
    n2,
    -- Critical z-value for alpha = 0.05
    1.96 as critical_z,
    -- Non-centrality parameter
    (observed_diff / NULLIFZERO(pooled_std)) * SQRT((n1 * n2) / (n1 + n2)) as ncp,
    CASE
        WHEN (observed_diff / NULLIFZERO(pooled_std)) * SQRT((n1 * n2) / (n1 + n2)) > 2.8 THEN '> 0.90 (Excellent)'
        WHEN (observed_diff / NULLIFZERO(pooled_std)) * SQRT((n1 * n2) / (n1 + n2)) > 2.5 THEN '0.80-0.90 (Good)'
        WHEN (observed_diff / NULLIFZERO(pooled_std)) * SQRT((n1 * n2) / (n1 + n2)) > 2.0 THEN '0.70-0.80 (Acceptable)'
        ELSE '< 0.70 (Underpowered)'
    END as power_assessment
FROM test_params;
```

#### Required Sample Size Calculation

```sql
-- Calculate required sample size for desired power
WITH design_params AS (
    SELECT
        0.5 as expected_effect_size,     -- Cohen's d
        0.05 as alpha,                    -- Significance level
        0.80 as desired_power,            -- 80% power
        2.8 as required_ncp               -- For 80% power with alpha=0.05
)
SELECT
    expected_effect_size,
    alpha,
    desired_power,
    -- Required sample size per group
    CEIL(2 * POWER(required_ncp / expected_effect_size, 2)) as required_n_per_group,
    CEIL(2 * POWER(required_ncp / expected_effect_size, 2)) * 2 as total_required_n
FROM design_params;
```

### Stage 7: Production Deployment and Monitoring

#### Create Statistical Testing View

```sql
-- Ongoing A/B test monitoring view
CREATE VIEW ${DATABASE_NAME}.${TABLE_NAME}_test_monitor AS
WITH daily_stats AS (
    SELECT
        test_date,
        test_group,
        COUNT(*) as daily_n,
        AVG(metric_column) as daily_mean,
        STDDEV_POP(metric_column) as daily_std
    FROM ${DATABASE_NAME}.${TABLE_NAME}
    GROUP BY test_date, test_group
)
SELECT
    c.test_date,
    c.daily_n as control_n,
    t.daily_n as treatment_n,
    c.daily_mean as control_mean,
    t.daily_mean as treatment_mean,
    t.daily_mean - c.daily_mean as mean_difference,
    (t.daily_mean - c.daily_mean) / NULLIFZERO(c.daily_mean) * 100 as lift_pct,
    -- Simple z-test
    (t.daily_mean - c.daily_mean) /
        SQRT((POWER(c.daily_std, 2) / c.daily_n) + (POWER(t.daily_std, 2) / t.daily_n)) as z_score,
    CASE
        WHEN ABS((t.daily_mean - c.daily_mean) /
            SQRT((POWER(c.daily_std, 2) / c.daily_n) + (POWER(t.daily_std, 2) / t.daily_n))) > 1.96
        THEN 'Significant'
        ELSE 'Not Significant'
    END as daily_significance
FROM daily_stats c
JOIN daily_stats t ON c.test_date = t.test_date
WHERE c.test_group = 'Control'
  AND t.test_group = 'Treatment';
```

#### Sequential Testing (Early Stopping)

```sql
-- Monitor test for early stopping
WITH cumulative_stats AS (
    SELECT
        test_date,
        test_group,
        SUM(COUNT(*)) OVER (PARTITION BY test_group ORDER BY test_date) as cumulative_n,
        AVG(AVG(metric_column)) OVER (PARTITION BY test_group ORDER BY test_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as cumulative_mean
    FROM ${DATABASE_NAME}.${TABLE_NAME}
    GROUP BY test_date, test_group
)
SELECT
    c.test_date,
    c.cumulative_n as control_n,
    t.cumulative_n as treatment_n,
    c.cumulative_mean as control_mean,
    t.cumulative_mean as treatment_mean,
    (t.cumulative_mean - c.cumulative_mean) / NULLIFZERO(c.cumulative_mean) * 100 as cumulative_lift,
    CASE
        WHEN t.cumulative_n >= 1000 AND ABS(t.cumulative_mean - c.cumulative_mean) / c.cumulative_mean > 0.05
        THEN 'Consider Early Stopping'
        WHEN t.cumulative_n >= 5000
        THEN 'Sufficient Sample Size'
        ELSE 'Continue Testing'
    END as recommendation
FROM cumulative_stats c
JOIN cumulative_stats t ON c.test_date = t.test_date
WHERE c.test_group = 'Control'
  AND t.test_group = 'Treatment'
ORDER BY c.test_date;
```

#### Alert on Significant Results

```sql
-- Alert system for significant findings
SELECT
    test_name,
    test_date,
    p_value,
    effect_size,
    'ALERT: Statistically Significant Result Detected' as alert_message
FROM ${DATABASE_NAME}.${TABLE_NAME}_test_results
WHERE p_value < 0.05
  AND ABS(effect_size) > 0.3  -- Practical significance threshold
  AND test_date = CURRENT_DATE;
```

## Decision Guides

### Choosing the Right Test

**Use ANOVA when:**
- Comparing means across 3 or more groups
- One continuous dependent variable
- One categorical independent variable
- Assumption of normality and equal variances met

**Use Chi-Square when:**
- Both variables are categorical
- Testing independence/association
- Expected frequencies ≥ 5 in each cell
- Data is count/frequency data

**Use F-Test when:**
- Comparing variances between two groups
- Testing assumption for T-test or ANOVA
- Quality control applications
- Process consistency validation

**Use Z-Test when:**
- Comparing means between two groups
- Large sample sizes (n > 30 per group)
- Population standard deviation known (or can use sample)
- Testing proportions or conversion rates

**Use T-Test when:**
- Comparing means between two groups
- Small sample sizes (n ≤ 30 per group)
- Population standard deviation unknown
- Normally distributed data

### Interpreting P-Values

**P-value < 0.001:**
- Highly statistically significant
- Very strong evidence against null hypothesis
- Result is unlikely due to chance

**P-value 0.001-0.01:**
- Statistically significant
- Strong evidence against null hypothesis
- Commonly reported as p < 0.01

**P-value 0.01-0.05:**
- Statistically significant (at α = 0.05)
- Moderate evidence against null hypothesis
- Standard threshold for significance

**P-value 0.05-0.10:**
- Marginally significant
- Weak evidence against null hypothesis
- Consider effect size and context

**P-value > 0.10:**
- Not statistically significant
- Insufficient evidence to reject null hypothesis
- Does not prove null hypothesis is true

### Effect Size Guidelines

**Always report effect size alongside p-value:**

**Cohen's d (mean differences):**
- Small: 0.2 - 0.5
- Medium: 0.5 - 0.8
- Large: > 0.8

**Correlation coefficients:**
- Small: 0.1 - 0.3
- Medium: 0.3 - 0.5
- Large: > 0.5

**Percentage change:**
- Consider business context
- 5% may be huge or negligible depending on domain
- Always evaluate practical significance

## Output Artifacts

This workflow produces:
1. `${TABLE_NAME}_anova_results` - ANOVA test results
2. `${TABLE_NAME}_chisq_results` - Chi-square test results
3. `${TABLE_NAME}_ftest_results` - F-test results
4. `${TABLE_NAME}_ztest_results` - Z-test results
5. `${TABLE_NAME}_ab_test_summary` - A/B test summary
6. `${TABLE_NAME}_test_monitor` - Ongoing test monitoring view
7. Statistical significance indicators
8. Effect size measurements
9. Confidence intervals
10. Power analysis results

## Best Practices

1. **Always check assumptions** - Validate normality, equal variance, sample size
2. **Report effect sizes** - P-values alone are insufficient
3. **Use confidence intervals** - Provide range of plausible values
4. **Consider practical significance** - Statistical ≠ business significant
5. **Avoid p-hacking** - Don't test multiple hypotheses without correction
6. **Plan sample size** - Power analysis before collecting data
7. **Document decisions** - Record alpha level, test choice rationale
8. **Check for outliers** - Extreme values can distort results
9. **Use appropriate corrections** - Bonferroni for multiple comparisons
10. **Validate with holdout** - Confirm results on new data

## Common Issues and Solutions

### Issue: P-value at boundary (e.g., 0.051)
**Interpretation:** Marginally not significant
**Solutions:**
- Report exact p-value (don't just say "not significant")
- Consider effect size and confidence intervals
- Evaluate practical significance
- Consider collecting more data
- Don't selectively report based on p = 0.049 vs 0.051

### Issue: Significant but tiny effect size
**Cause:** Very large sample size
**Solutions:**
- Always report effect size
- Focus on practical significance
- Use confidence intervals
- Consider business impact
- Don't overinterpret statistical significance

### Issue: Non-normal data
**Cause:** Skewed distributions, outliers
**Solutions:**
- Transform data (log, sqrt, Box-Cox)
- Use non-parametric tests (Mann-Whitney, Kruskal-Wallis)
- Increase sample size (CLT helps)
- Remove outliers if justified
- Use robust statistical methods

### Issue: Unequal variances
**Cause:** Heteroscedasticity
**Solutions:**
- Use Welch's correction for T-test
- Transform data to stabilize variance
- Use non-parametric tests
- Report results with caveat
- Consider robust standard errors

### Issue: Multiple testing problem
**Cause:** Testing many hypotheses increases Type I error
**Solutions:**
- Apply Bonferroni correction (divide α by number of tests)
- Use False Discovery Rate (FDR) methods
- Plan primary vs secondary hypotheses
- Report all tests conducted
- Use hierarchical testing approach

### Issue: Insufficient sample size
**Cause:** Underpowered study
**Solutions:**
- Conduct power analysis before study
- Collect more data if possible
- Report power analysis results
- Use confidence intervals (more informative)
- Don't conclude "no effect" from non-significance

## Function Reference Summary

### Statistical Tests
- FunctionalPrompts/Advanced_Analytics/td_anova.md
- FunctionalPrompts/Advanced_Analytics/td_chisq.md
- FunctionalPrompts/Advanced_Analytics/td_ftest.md
- FunctionalPrompts/Advanced_Analytics/td_ztest.md

### Related Functions
- Standard SQL aggregate functions (AVG, STDDEV_POP, VARIANCE, etc.)
- PERCENTILE_CONT for quantile calculations

---

**File Created**: 2025-11-28
**Version**: 1.0
**Workflow Type**: Statistical Testing
**Parent Persona**: persona_data_scientist.md
