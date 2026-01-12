# TD_ANOVA

## Function Name
- **TD_ANOVA**: Analysis of Variance - Tests differences between means of three or more groups

## Description
TD_ANOVA performs one-way analysis of variance (ANOVA), a statistical test used to analyze the difference between the means of three or more groups. The function tests whether at least one group mean differs significantly from the others by comparing the variance between groups to the variance within groups.

ANOVA is a fundamental statistical technique that extends the two-sample t-test to situations with multiple groups. It calculates an F-statistic and associated p-value to determine whether observed differences in group means are statistically significant or could have occurred by chance.

### Characteristics
- Tests null hypothesis that all group means are equal
- Returns F-statistic, p-value, and degrees of freedom
- Provides sum of squares, mean square values for interpretation
- Supports continuous dependent variables and categorical grouping variables
- More powerful than multiple t-tests (avoids inflated Type I error)
- Assumption: normal distribution and equal variances across groups

### Limitations
- ANOVA only tells you that at least one group differs, not which specific groups differ
- Requires post-hoc tests (like Tukey's HSD) to identify specific group differences
- Sensitive to violations of equal variance assumption
- Assumes independence of observations
- Less robust with very small sample sizes per group

## When to Use TD_ANOVA

TD_ANOVA is essential for comparing multiple groups simultaneously in various business and analytical scenarios:

### A/B/n Testing and Experimentation
- Compare 3+ variants in website design tests
- Evaluate multiple pricing strategies
- Test multiple marketing campaign variations
- Compare different product formulations
- Assess multiple treatment groups in trials

### Customer Segmentation Analysis
- Compare metrics across customer segments
- Analyze spending patterns by loyalty tier
- Test satisfaction scores across regions
- Compare engagement across user personas
- Evaluate performance by age groups or demographics

### Quality Control and Process Optimization
- Compare output quality across production lines
- Test multiple process improvement methods
- Evaluate consistency across manufacturing facilities
- Compare defect rates across shifts or teams
- Assess quality metrics across suppliers

### Business Performance Analysis
- Compare sales performance across regions
- Analyze revenue by product category
- Test employee productivity across departments
- Compare customer lifetime value by acquisition channel
- Evaluate profitability across business units

### Research and Statistical Analysis
- Validate hypothesis about group differences
- Support decision-making with statistical evidence
- Identify factors that significantly impact outcomes
- Quantify variability between and within groups

## Syntax

```sql
TD_ANOVA (
    DependentColumn ('dependent_variable'),
    FactorColumn ('grouping_variable'),
    [ Alpha (alpha_value) ]
)
```

**Note:** You can call this function from:
- The FROM clause of a SELECT statement
- As part of a CREATE TABLE statement
- As part of a CREATE VIEW statement

## Required Elements

### DependentColumn
**Required**: Specify the name of the column containing the continuous variable to test.
- **Data Type**: Numeric (INTEGER, FLOAT, DECIMAL, etc.)
- **Description**: The metric you want to compare across groups (e.g., revenue, conversion_rate, response_time)
- **Constraint**: Must be continuous numeric data

### FactorColumn
**Required**: Specify the name of the column containing the categorical grouping variable.
- **Data Type**: Any categorical type (VARCHAR, INTEGER for codes)
- **Description**: The variable that defines groups to compare (e.g., region, test_variant, customer_segment)
- **Constraint**: Must have 2 or more distinct values
- **Best Practice**: Should have 3+ groups (use t-test for 2 groups)

## Optional Elements

### Alpha
Specify the significance level for the hypothesis test.
- **Default**: 0.05 (95% confidence level)
- **Valid Range**: 0 < alpha < 1
- **Common Values**:
  - 0.01: 99% confidence (strict, reduces Type I error)
  - 0.05: 95% confidence (standard in most research)
  - 0.10: 90% confidence (lenient, increases power)
- **Interpretation**: If p-value < alpha, reject null hypothesis

## Input Schema

### Input Table Schema
The input table should contain observations with a continuous dependent variable and categorical grouping variable.

| Column | Data Type | Description |
|--------|-----------|-------------|
| dependent_variable | Numeric | Continuous metric to compare (e.g., sales, time, score) |
| grouping_variable | Categorical | Group identifiers (e.g., region, variant, segment) |
| additional_columns | ANY | Optional columns for context |

**Data Requirements:**
- At least 2 observations per group (preferably 30+ for normality assumption)
- Total sample size should be adequate for desired power (typically 100+ observations)
- No missing values in dependent or factor columns
- Ideally, equal or similar sample sizes across groups

## Output Schema

### Output Table Schema
The output table contains ANOVA results with variance decomposition.

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| source | VARCHAR | Source of variation ('Between Groups', 'Within Groups', 'Total') |
| sum_of_squares | FLOAT | Sum of squared deviations from mean |
| degrees_of_freedom | INTEGER | Number of independent values (k-1 for between, N-k for within) |
| mean_square | FLOAT | Sum of squares divided by degrees of freedom |
| f_statistic | FLOAT | Ratio of between-group to within-group variance |
| p_value | FLOAT | Probability of observing F-statistic if null hypothesis is true |

**Interpretation:**
- **F-statistic**: Larger values indicate greater between-group differences relative to within-group variability
- **p-value < alpha**: Reject null hypothesis (at least one group mean differs)
- **p-value ≥ alpha**: Fail to reject null hypothesis (no significant difference detected)

## Code Examples

### Example 1: Basic ANOVA - Compare Sales Across Regions

Test if average sales differ significantly across three regions:

```sql
-- Create ANOVA results table
CREATE TABLE sales_anova_results AS (
    SELECT * FROM TD_ANOVA(
        ON regional_sales
        USING
        DependentColumn('monthly_sales')
        FactorColumn('region')
        Alpha(0.05)
    )
) WITH DATA;

-- View ANOVA results
SELECT
    source,
    sum_of_squares,
    degrees_of_freedom,
    mean_square,
    f_statistic,
    p_value,
    CASE
        WHEN p_value < 0.05 THEN 'Significant - Regions differ'
        ELSE 'Not Significant - No difference detected'
    END as interpretation
FROM sales_anova_results;
```

**Result Interpretation:**
- If p_value < 0.05: At least one region has significantly different sales
- Requires post-hoc analysis to identify which specific regions differ

### Example 2: A/B/C/D Testing - Compare Conversion Rates

Test multiple website variants simultaneously:

```sql
-- Compare conversion rates across 4 design variants
CREATE TABLE conversion_test_anova AS (
    SELECT * FROM TD_ANOVA(
        ON website_ab_test
        USING
        DependentColumn('conversion_rate')
        FactorColumn('variant')
        Alpha(0.01)  -- Stricter significance level
    )
) WITH DATA;

-- Comprehensive results view
SELECT
    source,
    ROUND(sum_of_squares, 4) as ss,
    degrees_of_freedom as df,
    ROUND(mean_square, 4) as ms,
    ROUND(f_statistic, 3) as f_stat,
    ROUND(p_value, 6) as p_val,
    CASE
        WHEN p_value < 0.01 THEN '** Highly Significant **'
        WHEN p_value < 0.05 THEN '* Significant *'
        ELSE 'Not Significant'
    END as result
FROM conversion_test_anova
ORDER BY
    CASE source
        WHEN 'Between Groups' THEN 1
        WHEN 'Within Groups' THEN 2
        ELSE 3
    END;
```

**Business Application:**
- p-value < 0.01: Strong evidence that variants have different conversion rates
- Proceed with pairwise comparisons to identify best-performing variant

### Example 3: Customer Segmentation - Compare Average Order Value

Analyze if different customer segments have different purchasing behaviors:

```sql
-- Test AOV differences across customer loyalty tiers
CREATE TABLE segment_aov_anova AS (
    SELECT * FROM TD_ANOVA(
        ON customer_transactions
        USING
        DependentColumn('order_value')
        FactorColumn('loyalty_tier')
        Alpha(0.05)
    )
) WITH DATA;

-- Extract key metrics
SELECT
    f_statistic,
    p_value,
    CASE
        WHEN p_value < 0.001 THEN 'p < 0.001 (Highly Significant)'
        WHEN p_value < 0.01 THEN 'p < 0.01 (Very Significant)'
        WHEN p_value < 0.05 THEN 'p < 0.05 (Significant)'
        ELSE 'p >= 0.05 (Not Significant)'
    END as significance_level,
    -- Effect size (Eta-squared): proportion of variance explained by groups
    (SELECT sum_of_squares FROM segment_aov_anova WHERE source = 'Between Groups') /
    (SELECT sum_of_squares FROM segment_aov_anova WHERE source = 'Total') as eta_squared
FROM segment_aov_anova
WHERE source = 'Between Groups';
```

**Effect Size Interpretation (Eta-squared):**
- 0.01 - 0.06: Small effect
- 0.06 - 0.14: Medium effect
- > 0.14: Large effect

### Example 4: Production Quality Control - Multiple Production Lines

Compare product quality metrics across manufacturing facilities:

```sql
-- Quality score comparison across 5 production facilities
CREATE TABLE quality_anova AS (
    SELECT * FROM TD_ANOVA(
        ON production_data
        USING
        DependentColumn('quality_score')
        FactorColumn('facility_id')
        Alpha(0.05)
    )
) WITH DATA;

-- Full ANOVA table with percentage of variance
WITH anova_detailed AS (
    SELECT
        source,
        sum_of_squares,
        degrees_of_freedom,
        mean_square,
        f_statistic,
        p_value,
        sum_of_squares / (SELECT sum_of_squares FROM quality_anova WHERE source = 'Total') * 100
            as pct_variance_explained
    FROM quality_anova
)
SELECT
    source,
    ROUND(sum_of_squares, 2) as ss,
    degrees_of_freedom as df,
    ROUND(mean_square, 2) as ms,
    ROUND(pct_variance_explained, 1) as pct_var,
    CASE
        WHEN source = 'Between Groups' THEN ROUND(f_statistic, 3)
        ELSE NULL
    END as f_stat,
    CASE
        WHEN source = 'Between Groups' THEN ROUND(p_value, 6)
        ELSE NULL
    END as p_val
FROM anova_detailed
ORDER BY
    CASE source
        WHEN 'Between Groups' THEN 1
        WHEN 'Within Groups' THEN 2
        ELSE 3
    END;
```

**Quality Control Decision:**
- If significant: Investigate facility-level differences, standardize processes
- If not significant: Quality is consistent across facilities

### Example 5: Complete ANOVA Workflow with Post-Hoc Analysis

End-to-end analysis with descriptive statistics and pairwise comparisons:

```sql
-- Step 1: Descriptive statistics by group
CREATE TABLE group_descriptives AS (
    SELECT
        treatment_group,
        COUNT(*) as n,
        ROUND(AVG(response_time), 2) as mean_response,
        ROUND(STDDEV_POP(response_time), 2) as std_dev,
        ROUND(MIN(response_time), 2) as min_val,
        ROUND(MAX(response_time), 2) as max_val
    FROM system_performance
    GROUP BY treatment_group
) WITH DATA;

-- Step 2: Run ANOVA
CREATE TABLE performance_anova AS (
    SELECT * FROM TD_ANOVA(
        ON system_performance
        USING
        DependentColumn('response_time')
        FactorColumn('treatment_group')
        Alpha(0.05)
    )
) WITH DATA;

-- Step 3: Comprehensive Report
SELECT
    'Descriptive Statistics' as section,
    CAST(treatment_group AS VARCHAR(50)) as detail,
    n as value1,
    mean_response as value2,
    std_dev as value3
FROM group_descriptives

UNION ALL

SELECT
    'ANOVA Results' as section,
    source as detail,
    f_statistic as value1,
    p_value as value2,
    CAST(NULL AS FLOAT) as value3
FROM performance_anova
WHERE source = 'Between Groups'

ORDER BY section DESC, detail;

-- Step 4: Post-hoc pairwise comparisons (if ANOVA significant)
CREATE TABLE pairwise_comparisons AS (
    SELECT
        g1.treatment_group as group_1,
        g2.treatment_group as group_2,
        g1.mean_response as mean_1,
        g2.mean_response as mean_2,
        ROUND(g1.mean_response - g2.mean_response, 2) as mean_diff,
        ROUND((g1.mean_response - g2.mean_response) / g1.mean_response * 100, 1) as pct_change,
        -- Simple effect size (Cohen's d)
        ROUND(
            ABS(g1.mean_response - g2.mean_response) /
            SQRT((POWER(g1.std_dev, 2) + POWER(g2.std_dev, 2)) / 2),
            3
        ) as cohens_d
    FROM group_descriptives g1
    CROSS JOIN group_descriptives g2
    WHERE g1.treatment_group < g2.treatment_group
) WITH DATA;

SELECT * FROM pairwise_comparisons
ORDER BY ABS(mean_diff) DESC;
```

**Workflow Benefits:**
- Comprehensive understanding of group differences
- Quantifies both statistical and practical significance
- Identifies specific group pairs that differ most

## Common Use Cases

### 1. Marketing Campaign Optimization

```sql
-- Compare ROI across multiple marketing channels
CREATE TABLE marketing_anova AS (
    SELECT * FROM TD_ANOVA(
        ON campaign_performance
        USING
        DependentColumn('roi_percentage')
        FactorColumn('marketing_channel')
        Alpha(0.05)
    )
) WITH DATA;

-- Identify if channel selection matters
SELECT
    CASE
        WHEN p_value < 0.05 THEN 'Reallocate budget to best-performing channels'
        ELSE 'All channels perform similarly'
    END as recommendation,
    f_statistic,
    p_value
FROM marketing_anova
WHERE source = 'Between Groups';
```

### 2. Employee Performance Evaluation

```sql
-- Test if training method affects sales performance
CREATE TABLE training_effectiveness AS (
    SELECT * FROM TD_ANOVA(
        ON sales_rep_performance
        USING
        DependentColumn('quarterly_sales')
        FactorColumn('training_method')
        Alpha(0.01)
    )
) WITH DATA;

SELECT
    f_statistic,
    p_value,
    CASE
        WHEN p_value < 0.01 THEN 'Training method significantly impacts sales - identify best method'
        ELSE 'Training methods have similar effectiveness'
    END as conclusion
FROM training_effectiveness
WHERE source = 'Between Groups';
```

### 3. Product Pricing Strategy

```sql
-- Compare average cart value across pricing tiers
CREATE TABLE pricing_strategy_anova AS (
    SELECT * FROM TD_ANOVA(
        ON customer_orders
        USING
        DependentColumn('cart_value')
        FactorColumn('pricing_tier')
        Alpha(0.05)
    )
) WITH DATA;

-- Calculate effect size for business impact
SELECT
    f_statistic,
    p_value,
    (SELECT sum_of_squares FROM pricing_strategy_anova WHERE source = 'Between Groups') /
    (SELECT sum_of_squares FROM pricing_strategy_anova WHERE source = 'Total') as eta_squared,
    CASE
        WHEN p_value < 0.05 THEN 'Pricing tier significantly affects cart value'
        ELSE 'Consider unified pricing strategy'
    END as recommendation
FROM pricing_strategy_anova
WHERE source = 'Between Groups';
```

## Best Practices

1. **Check Assumptions Before Testing**:
   - **Normality**: Use histograms or Q-Q plots (or check if mean ≈ median)
   - **Equal Variances**: Compare standard deviations across groups (ratio should be < 2)
   - **Independence**: Ensure observations are independent
   - **Sample Size**: Aim for n ≥ 30 per group when possible

2. **Interpret Results Holistically**:
   - Don't rely solely on p-values
   - Calculate and report effect size (eta-squared or omega-squared)
   - Use confidence intervals for mean differences
   - Consider practical significance alongside statistical significance

3. **Conduct Post-Hoc Tests**:
   - ANOVA only tells you "at least one group differs"
   - Use Tukey's HSD, Bonferroni, or Scheffé tests for pairwise comparisons
   - Adjust alpha level for multiple comparisons to control Type I error

4. **Report Descriptive Statistics**:
   - Always include group means, standard deviations, and sample sizes
   - Visualize group differences with box plots or bar charts
   - Show both statistical output and business context

5. **Handle Violations Appropriately**:
   - **Unequal variances**: Use Welch's ANOVA or robust ANOVA
   - **Non-normal data**: Transform data (log, sqrt) or use Kruskal-Wallis test
   - **Small samples**: Bootstrap methods or non-parametric alternatives

6. **Sample Size and Power**:
   - Conduct power analysis before data collection
   - Aim for 80% power to detect meaningful effects
   - Larger effect sizes require smaller samples, but be conservative

7. **Business Context**:
   - Significant statistical results may not be practically important
   - A 0.1% improvement might be significant but not worth implementing
   - Always tie statistical findings back to business decisions

## Related Functions

- **TD_FTest**: Test equality of variances between two groups (assumption check for ANOVA)
- **TD_ZTest**: Compare means between two groups with large samples
- **TD_ChiSq**: Test independence of categorical variables
- **TD_UnivariateStatistics**: Descriptive statistics for each group
- **STDDEV_POP / VARIANCE**: Calculate variability within groups
- **AVG / PERCENTILE_CONT**: Summarize central tendency by group

## Notes and Limitations

1. **Post-Hoc Testing Required**:
   - ANOVA doesn't identify which specific groups differ
   - Requires additional pairwise comparison tests
   - Apply multiple testing corrections (Bonferroni, FDR)

2. **Assumption Sensitivity**:
   - Results can be unreliable with severe violations
   - Equal variance assumption is particularly important
   - Consider robust alternatives if assumptions violated

3. **Sample Size Considerations**:
   - Unequal group sizes reduce power
   - Very small groups (n < 10) may not meet normality assumption
   - Very large samples may detect trivial differences as significant

4. **One-Way ANOVA Only**:
   - TD_ANOVA tests one factor at a time
   - For multiple factors, use factorial ANOVA or GLM approaches
   - Consider interaction effects in multi-factor designs

5. **Effect Size Importance**:
   - F-statistic and p-value don't indicate magnitude of difference
   - Always calculate eta-squared or omega-squared
   - Small effects can be significant with large samples

6. **Interpretation Caution**:
   - "No significant difference" ≠ "groups are identical"
   - May lack power to detect true differences
   - Report confidence intervals to show uncertainty

## Version Information

- **Function Version**: Based on Teradata Database Analytic Functions Version 17.20
- **Generated**: November 28, 2025
- **Category**: Hypothesis Testing / Statistical Analysis
