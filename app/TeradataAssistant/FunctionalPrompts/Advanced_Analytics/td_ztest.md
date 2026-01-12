# TD_ZTest

## Function Name
- **TD_ZTest**: Z-Test for Comparing Means - Tests if two samples have equal means with known or large-sample variance

## Description
TD_ZTest performs a Z-test, for which the distribution of the test statistic under the null hypothesis can be approximated by a standard normal (Z) distribution. The Z-test is used to compare the means of two populations when the population standard deviations are known or when sample sizes are large enough (typically n > 30) that the sample standard deviations provide reliable estimates.

The Z-test calculates a Z-statistic by dividing the difference between sample means by the standard error of the difference. This statistic follows a standard normal distribution under the null hypothesis that the population means are equal. The test can be one-tailed (testing if one mean is greater) or two-tailed (testing if means are different in either direction), and it provides p-values and confidence intervals for the mean difference.

### Characteristics
- Tests null hypothesis that two population means are equal
- Returns Z-statistic, p-value, confidence intervals, and standard error
- Can perform one-tailed or two-tailed tests
- Suitable for large samples (n > 30 per group)
- Can use known population standard deviations or estimate from samples
- More powerful than t-test with large samples
- Robust to moderate departures from normality with large samples (Central Limit Theorem)

### Limitations
- Requires large sample sizes (n > 30) if population standard deviation unknown
- Assumes independence of observations
- Less appropriate than t-test for small samples
- Cannot handle paired or matched samples directly
- Assumes reasonably normal distributions (less critical with large n)

## When to Use TD_ZTest

TD_ZTest is essential for comparing means between two groups in various analytical scenarios:

### A/B Testing and Experimentation
- Compare conversion rates between control and treatment groups
- Test if new website design improves user engagement metrics
- Evaluate impact of pricing changes on average order value
- Compare click-through rates between email campaigns
- Test if marketing interventions affect customer spending

### Business Performance Analysis
- Compare average sales between two regions or time periods
- Test if customer satisfaction scores differ between service channels
- Evaluate revenue differences between product lines
- Compare response times before and after system upgrade
- Test if employee productivity differs between training methods

### Quality Control and Process Improvement
- Compare mean product dimensions between production lines
- Test if process change affected average defect rates
- Evaluate if mean cycle time decreased after improvement
- Compare average quality scores between suppliers
- Test if mean customer wait time reduced after intervention

### Healthcare and Clinical Studies
- Compare mean treatment outcomes between control and treatment groups
- Test if average recovery time differs between protocols
- Evaluate if mean blood pressure changes with medication
- Compare average test scores between patient populations
- Test if mean symptom severity differs between interventions

### Customer Analytics and Segmentation
- Compare average customer lifetime value between segments
- Test if mean purchase frequency differs by loyalty tier
- Evaluate if average basket size varies by demographic group
- Compare mean engagement metrics across user cohorts
- Test if retention rates differ between acquisition channels

## Syntax

```sql
TD_ZTest (
    Sample1Column ('first_sample_column'),
    Sample2Column ('second_sample_column'),
    [ Alpha (alpha_value) ],
    [ Alternative ('test_type') ],
    [ PopulationStdDev1 (std_dev_1) ],
    [ PopulationStdDev2 (std_dev_2) ]
)
```

**Note:** You can call this function from:
- The FROM clause of a SELECT statement
- As part of a CREATE TABLE statement
- As part of a CREATE VIEW statement

## Required Elements

### Sample1Column
**Required**: Specify the name of the column containing values for the first sample.
- **Data Type**: Numeric (INTEGER, FLOAT, DECIMAL, etc.)
- **Description**: Continuous measurements from first group
- **Examples**: conversion_rate_control, sales_region_a, response_time_before
- **Constraint**: Must contain at least 30 non-null numeric values (recommended for CLT)

### Sample2Column
**Required**: Specify the name of the column containing values for the second sample.
- **Data Type**: Numeric (INTEGER, FLOAT, DECIMAL, etc.)
- **Description**: Continuous measurements from second group
- **Examples**: conversion_rate_treatment, sales_region_b, response_time_after
- **Constraint**: Must contain at least 30 non-null numeric values (recommended)

## Optional Elements

### Alpha
Specify the significance level for the hypothesis test.
- **Default**: 0.05 (95% confidence level)
- **Valid Range**: 0 < alpha < 1
- **Common Values**:
  - 0.01: 99% confidence (strict, reduces Type I error)
  - 0.05: 95% confidence (standard in most research)
  - 0.10: 90% confidence (lenient, increases power)
- **Interpretation**: If p-value < alpha, reject null hypothesis (means differ)

### Alternative
Specify the type of alternative hypothesis.
- **Default**: 'two-sided'
- **Valid Values**:
  - **'two-sided'**: Test if means are different (μ1 ≠ μ2)
  - **'greater'**: Test if mean1 > mean2
  - **'less'**: Test if mean1 < mean2
- **Use Cases**:
  - Two-sided: Most common, tests any difference
  - Greater: Test if first group has higher mean
  - Less: Test if first group has lower mean

### PopulationStdDev1
Specify the known population standard deviation for the first sample.
- **Default**: NULL (use sample standard deviation)
- **Data Type**: Positive numeric value
- **When to Use**:
  - When population standard deviation is known from historical data
  - In quality control with established process parameters
  - When sample standard deviation may be unreliable
- **If NULL**: Function estimates from sample data

### PopulationStdDev2
Specify the known population standard deviation for the second sample.
- **Default**: NULL (use sample standard deviation)
- **Data Type**: Positive numeric value
- **When to Use**: Same as PopulationStdDev1
- **If NULL**: Function estimates from sample data

## Input Schema

### Input Table Schema
The input table should contain paired observations or separate columns for two samples.

| Column | Data Type | Description |
|--------|-----------|-------------|
| sample_1_column | Numeric | Measurements from first group |
| sample_2_column | Numeric | Measurements from second group |
| identifier_column | ANY | Optional row identifier |

**Data Requirements:**
- Each column represents a separate sample
- Samples can have different sizes
- No missing values in sample columns
- Ideally n ≥ 30 per group for Central Limit Theorem
- Observations must be independent within and between groups
- Data should be reasonably continuous

**Alternative Structure:**
- Single value column with group indicator
- Use CASE statement to pivot into two columns for TD_ZTest

## Output Schema

### Output Table Schema
The output table contains Z-test results with comprehensive statistics.

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| z_statistic | FLOAT | Standardized test statistic (mean_diff / standard_error) |
| p_value | FLOAT | Probability of observing z-statistic if means are equal |
| mean_difference | FLOAT | Difference between sample means (mean1 - mean2) |
| standard_error | FLOAT | Standard error of the mean difference |
| confidence_interval_lower | FLOAT | Lower bound of (1-alpha)% confidence interval for mean difference |
| confidence_interval_upper | FLOAT | Upper bound of (1-alpha)% confidence interval for mean difference |
| sample_1_mean | FLOAT | Mean of first sample |
| sample_2_mean | FLOAT | Mean of second sample |
| sample_1_n | INTEGER | Sample size of first group |
| sample_2_n | INTEGER | Sample size of second group |

**Interpretation:**
- **z_statistic**: Larger absolute values indicate greater difference between means
  - |Z| > 1.96: Significant at α = 0.05 (two-tailed)
  - |Z| > 2.58: Significant at α = 0.01 (two-tailed)
- **p_value < alpha**: Reject null hypothesis (means are significantly different)
- **p_value ≥ alpha**: Fail to reject null hypothesis (no significant difference detected)
- **Confidence interval**: Range of plausible values for the true mean difference
  - If interval excludes 0: Means are significantly different
  - If interval includes 0: No significant difference

## Code Examples

### Example 1: Basic Z-Test - A/B Test Conversion Comparison

Compare conversion rates between control and treatment groups:

```sql
-- Prepare A/B test data with separate columns
WITH ab_data AS (
    SELECT
        MAX(CASE WHEN variant = 'Control' THEN converted END) as control_conversion,
        MAX(CASE WHEN variant = 'Treatment' THEN converted END) as treatment_conversion,
        user_id
    FROM ab_test_results
    GROUP BY user_id
)
CREATE TABLE conversion_ztest AS (
    SELECT * FROM TD_ZTest(
        ON ab_data
        USING
        Sample1Column('treatment_conversion')
        Sample2Column('control_conversion')
        Alpha(0.05)
        Alternative('greater')  -- Test if treatment > control
    )
) WITH DATA;

-- View comprehensive results
SELECT
    z_statistic,
    p_value,
    ROUND(mean_difference, 4) as mean_diff,
    ROUND(mean_difference / NULLIFZERO(sample_2_mean) * 100, 2) as lift_pct,
    ROUND(standard_error, 4) as std_error,
    ROUND(confidence_interval_lower, 4) as ci_lower,
    ROUND(confidence_interval_upper, 4) as ci_upper,
    sample_1_n,
    sample_2_n,
    CASE
        WHEN p_value < 0.05 THEN 'Treatment WINS - Roll out'
        ELSE 'No significant difference - Keep control'
    END as decision,
    CASE
        WHEN z_statistic > 2.58 THEN '*** Highly Significant (p < 0.01)'
        WHEN z_statistic > 1.96 THEN '** Significant (p < 0.05)'
        WHEN z_statistic > 1.645 THEN '* Marginally Significant (p < 0.10)'
        ELSE 'Not Significant'
    END as significance_stars
FROM conversion_ztest;
```

**Business Decision:**
- p-value < 0.05 + positive lift: Implement treatment
- p-value ≥ 0.05: Continue testing or revert to control

### Example 2: Before-After Analysis - Process Improvement

Test if process improvement reduced average response time:

```sql
-- Test if mean response time decreased after improvement
WITH improvement_data AS (
    SELECT
        MAX(CASE WHEN period = 'Before' THEN response_time END) as before_time,
        MAX(CASE WHEN period = 'After' THEN response_time END) as after_time,
        request_id
    FROM system_performance
    GROUP BY request_id
)
CREATE TABLE improvement_ztest AS (
    SELECT * FROM TD_ZTest(
        ON improvement_data
        USING
        Sample1Column('before_time')
        Sample2Column('after_time')
        Alpha(0.05)
        Alternative('greater')  -- Test if before > after (improvement)
    )
) WITH DATA;

-- Comprehensive improvement report
WITH ztest_results AS (
    SELECT * FROM improvement_ztest
),
descriptive_stats AS (
    SELECT
        'Before' as period,
        COUNT(*) as n,
        AVG(response_time) as mean_time,
        STDDEV_POP(response_time) as std_dev,
        PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY response_time) as median
    FROM system_performance
    WHERE period = 'Before'
    UNION ALL
    SELECT
        'After' as period,
        COUNT(*) as n,
        AVG(response_time) as mean_time,
        STDDEV_POP(response_time) as std_dev,
        PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY response_time) as median
    FROM system_performance
    WHERE period = 'After'
)
SELECT
    d.period,
    d.n,
    ROUND(d.mean_time, 2) as mean,
    ROUND(d.std_dev, 2) as std_dev,
    ROUND(d.median, 2) as median,
    CASE d.period
        WHEN 'Before' THEN ROUND((SELECT z_statistic FROM ztest_results), 3)
        ELSE NULL
    END as z_stat,
    CASE d.period
        WHEN 'Before' THEN ROUND((SELECT p_value FROM ztest_results), 6)
        ELSE NULL
    END as p_value,
    CASE d.period
        WHEN 'After' THEN
            ROUND((SELECT mean_difference FROM ztest_results), 2) || ' sec reduction (' ||
            ROUND((SELECT mean_difference FROM ztest_results) /
                  (SELECT sample_1_mean FROM ztest_results) * 100, 1) || '% improvement)'
        ELSE NULL
    END as improvement,
    CASE d.period
        WHEN 'After' THEN
            CASE
                WHEN (SELECT p_value FROM ztest_results) < 0.05
                THEN 'Statistically significant improvement achieved'
                ELSE 'No significant improvement detected'
            END
        ELSE NULL
    END as conclusion
FROM descriptive_stats d
ORDER BY d.period DESC;
```

**Process Improvement Validation:**
- p-value < 0.05 with positive mean_difference: Improvement successful
- Calculate practical significance (% improvement)
- Report confidence interval for improvement magnitude

### Example 3: Regional Performance Comparison

Compare average sales between two regions:

```sql
-- Test if average sales differ between regions
WITH regional_data AS (
    SELECT
        MAX(CASE WHEN region = 'North' THEN monthly_sales END) as north_sales,
        MAX(CASE WHEN region = 'South' THEN monthly_sales END) as south_sales,
        month_id
    FROM sales_data
    GROUP BY month_id
)
CREATE TABLE regional_sales_ztest AS (
    SELECT * FROM TD_ZTest(
        ON regional_data
        USING
        Sample1Column('north_sales')
        Sample2Column('south_sales')
        Alpha(0.05)
        Alternative('two-sided')  -- Test for any difference
    )
) WITH DATA;

-- Effect size calculation (Cohen's d)
WITH ztest_results AS (
    SELECT * FROM regional_sales_ztest
),
pooled_std AS (
    SELECT
        SQRT((
            (n_north - 1) * POWER(std_north, 2) +
            (n_south - 1) * POWER(std_south, 2)
        ) / (n_north + n_south - 2)) as pooled_std_dev
    FROM (
        SELECT
            COUNT(*) as n_north,
            STDDEV_POP(monthly_sales) as std_north
        FROM sales_data
        WHERE region = 'North'
    ) north,
    (
        SELECT
            COUNT(*) as n_south,
            STDDEV_POP(monthly_sales) as std_south
        FROM sales_data
        WHERE region = 'South'
    ) south
)
SELECT
    z.sample_1_mean as north_mean,
    z.sample_2_mean as south_mean,
    z.mean_difference,
    z.mean_difference / NULLIFZERO(z.sample_2_mean) * 100 as pct_difference,
    z.standard_error,
    z.confidence_interval_lower as ci_95_lower,
    z.confidence_interval_upper as ci_95_upper,
    z.z_statistic,
    z.p_value,
    -- Cohen's d (effect size)
    z.mean_difference / NULLIFZERO(p.pooled_std_dev) as cohens_d,
    CASE
        WHEN ABS(z.mean_difference / NULLIFZERO(p.pooled_std_dev)) < 0.2 THEN 'Negligible'
        WHEN ABS(z.mean_difference / NULLIFZERO(p.pooled_std_dev)) < 0.5 THEN 'Small'
        WHEN ABS(z.mean_difference / NULLIFZERO(p.pooled_std_dev)) < 0.8 THEN 'Medium'
        ELSE 'Large'
    END as effect_size_interpretation,
    CASE
        WHEN z.p_value < 0.05 THEN 'Regions have significantly different sales'
        ELSE 'No significant regional difference'
    END as conclusion
FROM ztest_results z, pooled_std p;
```

**Effect Size Interpretation (Cohen's d):**
- < 0.2: Negligible practical difference
- 0.2 - 0.5: Small effect (may not be practically important)
- 0.5 - 0.8: Medium effect (likely important)
- > 0.8: Large effect (definitely important)

### Example 4: Customer Segment Analysis

Compare average order value between customer segments:

```sql
-- Test if premium customers have higher average order value
WITH segment_data AS (
    SELECT
        MAX(CASE WHEN segment = 'Premium' THEN order_value END) as premium_aov,
        MAX(CASE WHEN segment = 'Standard' THEN order_value END) as standard_aov,
        customer_id
    FROM customer_orders
    GROUP BY customer_id
)
CREATE TABLE segment_aov_ztest AS (
    SELECT * FROM TD_ZTest(
        ON segment_data
        USING
        Sample1Column('premium_aov')
        Sample2Column('standard_aov')
        Alpha(0.01)  -- Stricter threshold for business decision
        Alternative('greater')  -- Test if premium > standard
    )
) WITH DATA;

-- Business value calculation
WITH ztest_results AS (
    SELECT * FROM segment_aov_ztest
),
customer_counts AS (
    SELECT
        segment,
        COUNT(DISTINCT customer_id) as n_customers
    FROM customer_orders
    GROUP BY segment
)
SELECT
    'Statistical Results' as metric_type,
    'Z-Statistic' as metric_name,
    z.z_statistic as metric_value,
    CAST(NULL AS VARCHAR(100)) as interpretation

FROM ztest_results z

UNION ALL

SELECT
    'Statistical Results' as metric_type,
    'P-Value' as metric_name,
    z.p_value as metric_value,
    CASE
        WHEN z.p_value < 0.01 THEN 'Highly Significant'
        ELSE 'Not Significant at α=0.01'
    END as interpretation
FROM ztest_results z

UNION ALL

SELECT
    'Business Metrics' as metric_type,
    'AOV Difference' as metric_name,
    z.mean_difference as metric_value,
    '$' || CAST(ROUND(z.mean_difference, 2) AS VARCHAR(20)) || ' higher for Premium' as interpretation
FROM ztest_results z

UNION ALL

SELECT
    'Business Metrics' as metric_type,
    'Lift %' as metric_name,
    (z.mean_difference / NULLIFZERO(z.sample_2_mean) * 100) as metric_value,
    CAST(ROUND((z.mean_difference / NULLIFZERO(z.sample_2_mean) * 100), 1) AS VARCHAR(20)) || '% lift' as interpretation
FROM ztest_results z

UNION ALL

SELECT
    'Revenue Impact' as metric_type,
    'Incremental Revenue (Annual)' as metric_name,
    z.mean_difference * c.n_customers * 12 as metric_value,
    '$' || CAST(ROUND(z.mean_difference * c.n_customers * 12, 0) AS VARCHAR(20)) || ' potential increase' as interpretation
FROM ztest_results z, customer_counts c
WHERE c.segment = 'Standard'  -- If all standard upgraded to premium

ORDER BY metric_type DESC, metric_name;
```

**Strategic Insight:**
- Quantify value of segment differentiation
- Calculate ROI of premium customer acquisition
- Support pricing and promotion strategy

### Example 5: Multiple Hypothesis Testing with Correction

Test multiple comparisons with Bonferroni correction:

```sql
-- Compare multiple marketing channels (pairwise)
CREATE TABLE channel_comparison_ztests AS (
    -- Email vs Social
    WITH email_social AS (
        SELECT
            MAX(CASE WHEN channel = 'Email' THEN roi END) as email_roi,
            MAX(CASE WHEN channel = 'Social' THEN roi END) as social_roi,
            campaign_id
        FROM marketing_performance
        GROUP BY campaign_id
    )
    SELECT 'Email vs Social' as comparison, * FROM TD_ZTest(
        ON email_social
        USING Sample1Column('email_roi') Sample2Column('social_roi')
        Alpha(0.05) Alternative('two-sided')
    )

    UNION ALL

    -- Email vs Search
    WITH email_search AS (
        SELECT
            MAX(CASE WHEN channel = 'Email' THEN roi END) as email_roi,
            MAX(CASE WHEN channel = 'Search' THEN roi END) as search_roi,
            campaign_id
        FROM marketing_performance
        GROUP BY campaign_id
    )
    SELECT 'Email vs Search' as comparison, * FROM TD_ZTest(
        ON email_search
        USING Sample1Column('email_roi') Sample2Column('search_roi')
        Alpha(0.05) Alternative('two-sided')
    )

    UNION ALL

    -- Social vs Search
    WITH social_search AS (
        SELECT
            MAX(CASE WHEN channel = 'Social' THEN roi END) as social_roi,
            MAX(CASE WHEN channel = 'Search' THEN roi END) as search_roi,
            campaign_id
        FROM marketing_performance
        GROUP BY campaign_id
    )
    SELECT 'Social vs Search' as comparison, * FROM TD_ZTest(
        ON social_search
        USING Sample1Column('social_roi') Sample2Column('search_roi')
        Alpha(0.05) Alternative('two-sided')
    )
) WITH DATA;

-- Apply Bonferroni correction
WITH n_comparisons AS (
    SELECT COUNT(*) as n_tests FROM channel_comparison_ztests
)
SELECT
    comparison,
    ROUND(z_statistic, 3) as z_stat,
    ROUND(p_value, 6) as p_value_raw,
    0.05 / (SELECT n_tests FROM n_comparisons) as bonferroni_alpha,
    CASE
        WHEN p_value < (0.05 / (SELECT n_tests FROM n_comparisons))
        THEN 'Significant (after correction)'
        WHEN p_value < 0.05
        THEN 'Significant (before correction only)'
        ELSE 'Not Significant'
    END as corrected_result,
    ROUND(mean_difference, 2) as mean_diff,
    ROUND(confidence_interval_lower, 2) as ci_lower,
    ROUND(confidence_interval_upper, 2) as ci_upper
FROM channel_comparison_ztests
ORDER BY p_value;
```

**Multiple Testing Note:**
- With 3 comparisons, Bonferroni alpha = 0.05 / 3 = 0.0167
- Reduces Type I error rate across all tests
- More conservative but protects against false discoveries

### Example 6: Power Analysis and Sample Size Planning

Calculate required sample size for desired power:

```sql
-- Post-hoc power analysis
WITH test_params AS (
    SELECT
        z.mean_difference as observed_diff,
        z.standard_error as se,
        z.sample_1_n as n1,
        z.sample_2_n as n2,
        -- Pooled standard deviation estimate
        z.standard_error * SQRT((z.sample_1_n * z.sample_2_n) / (z.sample_1_n + z.sample_2_n)) as pooled_std
    FROM improvement_ztest z
)
SELECT
    observed_diff,
    pooled_std,
    observed_diff / NULLIFZERO(pooled_std) as effect_size_cohens_d,
    n1,
    n2,
    -- Non-centrality parameter (for power calculation)
    (observed_diff / NULLIFZERO(pooled_std)) * SQRT((n1 * n2) / (n1 + n2)) as ncp,
    CASE
        WHEN (observed_diff / NULLIFZERO(pooled_std)) * SQRT((n1 * n2) / (n1 + n2)) > 2.8
        THEN '> 90% (Excellent Power)'
        WHEN (observed_diff / NULLIFZERO(pooled_std)) * SQRT((n1 * n2) / (n1 + n2)) > 2.5
        THEN '80-90% (Good Power)'
        WHEN (observed_diff / NULLIFZERO(pooled_std)) * SQRT((n1 * n2) / (n1 + n2)) > 2.0
        THEN '70-80% (Acceptable Power)'
        ELSE '< 70% (Underpowered)'
    END as achieved_power_assessment,
    -- Required sample size for 80% power with observed effect
    CEIL(2 * POWER(2.8 / (observed_diff / NULLIFZERO(pooled_std)), 2)) as required_n_per_group_80pct_power
FROM test_params;
```

**Power Analysis Interpretation:**
- NCP > 2.8: Test has > 90% power (excellent)
- NCP 2.5-2.8: Test has 80-90% power (good)
- NCP < 2.0: Test is underpowered, may miss true differences

## Common Use Cases

### 1. Conversion Rate Optimization

```sql
-- Test multiple variants against control
CREATE TABLE variant_testing AS (
    -- Compare each variant to control
    ...
) WITH DATA;

-- Rank variants by performance
SELECT
    comparison,
    mean_difference as lift,
    p_value,
    RANK() OVER (ORDER BY mean_difference DESC) as performance_rank,
    CASE
        WHEN p_value < 0.05 AND mean_difference > 0 THEN 'Winner - Consider rolling out'
        WHEN p_value >= 0.05 THEN 'No significant difference'
        ELSE 'Worse than control'
    END as recommendation
FROM variant_testing
ORDER BY mean_difference DESC;
```

### 2. Customer Satisfaction Monitoring

```sql
-- Monitor if satisfaction scores change over time
CREATE TABLE satisfaction_trend_ztest AS (
    WITH period_comparison AS (
        SELECT
            MAX(CASE WHEN period = 'Current_Quarter' THEN score END) as current_score,
            MAX(CASE WHEN period = 'Previous_Quarter' THEN score END) as previous_score,
            customer_id
        FROM satisfaction_surveys
        GROUP BY customer_id
    )
    SELECT * FROM TD_ZTest(
        ON period_comparison
        USING Sample1Column('current_score') Sample2Column('previous_score')
        Alpha(0.05) Alternative('two-sided')
    )
) WITH DATA;

-- Alert on significant changes
SELECT
    CASE
        WHEN p_value < 0.05 AND mean_difference > 0 THEN 'POSITIVE: Satisfaction improved'
        WHEN p_value < 0.05 AND mean_difference < 0 THEN 'ALERT: Satisfaction declined'
        ELSE 'Stable - no significant change'
    END as status,
    mean_difference as score_change,
    p_value
FROM satisfaction_trend_ztest;
```

### 3. Pricing Strategy Validation

```sql
-- Test if price change affected average order value
CREATE TABLE pricing_impact_ztest AS (
    WITH pricing_comparison AS (
        SELECT
            MAX(CASE WHEN pricing = 'New_Price' THEN order_value END) as new_price_aov,
            MAX(CASE WHEN pricing = 'Old_Price' THEN order_value END) as old_price_aov,
            customer_segment || '_' || CAST(week_id AS VARCHAR(10)) as comparison_unit
        FROM orders
        GROUP BY customer_segment, week_id
    )
    SELECT * FROM TD_ZTest(
        ON pricing_comparison
        USING Sample1Column('new_price_aov') Sample2Column('old_price_aov')
        Alpha(0.05) Alternative('two-sided')
    )
) WITH DATA;

-- Calculate revenue impact
SELECT
    mean_difference as aov_change,
    p_value,
    CASE
        WHEN p_value < 0.05 AND mean_difference < 0
        THEN 'Price increase reduced AOV - consider rollback'
        WHEN p_value < 0.05 AND mean_difference > 0
        THEN 'Price change increased AOV - successful'
        ELSE 'No significant impact on AOV'
    END as recommendation
FROM pricing_impact_ztest;
```

## Best Practices

1. **Verify Sample Size Requirements**:
   - Aim for n ≥ 30 per group for Central Limit Theorem
   - With n < 30, use t-test instead
   - Check if sample sizes are adequate for desired power (typically 80%)

2. **Check for Outliers**:
   - Extreme values can distort means and standard deviations
   - Use box plots or IQR method to detect outliers
   - Consider robust alternatives or removing outliers if justified

3. **Report Effect Size**:
   - P-value alone is insufficient
   - Calculate Cohen's d or percentage difference
   - Evaluate practical significance alongside statistical significance

4. **Use Confidence Intervals**:
   - CI provides range of plausible values for true difference
   - More informative than p-value alone
   - If CI excludes 0, effect is significant

5. **Choose Appropriate Alternative**:
   - Use 'two-sided' unless you have strong prior hypothesis
   - One-sided tests have more power but require theoretical justification
   - Pre-specify alternative hypothesis before seeing data

6. **Consider Equal Variance Assumption**:
   - Z-test assumes equal variances (less critical with large samples)
   - If variances very different, use Welch t-test
   - Check with F-test or examine variance ratio

7. **Report Comprehensively**:
   - Include sample sizes, means, standard deviations, effect size
   - Report Z-statistic, p-value, and confidence interval
   - Provide business context and practical interpretation
   - Visualize with error bars or distribution plots

## Related Functions

- **TD_ANOVA**: Compare means across 3+ groups
- **TD_FTest**: Test equality of variances (assumption check)
- **TD_ChiSq**: Test independence of categorical variables
- **TD_UnivariateStatistics**: Calculate descriptive statistics for each group
- **AVG / STDDEV_POP**: Calculate sample means and standard deviations manually

## Notes and Limitations

1. **Sample Size Requirements**:
   - Rule of thumb: n ≥ 30 per group for CLT approximation
   - With smaller samples, use t-test instead
   - Very large samples may detect trivial differences as significant

2. **Independence Assumption**:
   - Each observation must be independent
   - Repeated measures or paired data require paired t-test or Z-test for proportions
   - Clustered data may violate independence

3. **Normality Assumption**:
   - Less critical with large samples (CLT applies)
   - With small samples or severe non-normality, consider:
     - Data transformation (log, sqrt)
     - Non-parametric alternative (Mann-Whitney U test)
     - Bootstrap methods

4. **Equal Variance Assumption**:
   - Z-test typically assumes equal variances
   - Less critical with equal sample sizes
   - If variances very different (ratio > 4), consider Welch t-test

5. **One-Sample vs Two-Sample**:
   - TD_ZTest is for two-sample comparisons
   - For one-sample tests (compare to known value), use different approach

6. **Known vs Unknown Standard Deviation**:
   - If population SD known, specify in PopulationStdDev parameters
   - With unknown SD and large samples, Z-test and t-test converge
   - With unknown SD and small samples, t-test is more appropriate

7. **Statistical vs Practical Significance**:
   - Large samples may detect tiny differences as significant
   - Always evaluate effect size and business impact
   - Consider minimum detectable effect (MDE) in planning

8. **Multiple Comparisons**:
   - Testing many pairs increases Type I error rate
   - Apply Bonferroni correction: alpha / number of tests
   - Or use False Discovery Rate (FDR) methods

## Version Information

- **Function Version**: Based on Teradata Database Analytic Functions Version 17.20
- **Generated**: November 28, 2025
- **Category**: Hypothesis Testing / Statistical Analysis
