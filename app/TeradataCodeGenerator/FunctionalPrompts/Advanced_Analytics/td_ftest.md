# TD_FTest

## Function Name
- **TD_FTest**: F-Test for Equality of Variances - Tests if two samples have equal variances

## Description
TD_FTest performs an F-test, for which the test statistic has an F-distribution under the null hypothesis. The F-test is primarily used to compare the variances of two populations to determine if they are significantly different. This is a critical assumption check for many parametric statistical tests, including the two-sample t-test and ANOVA.

The F-test calculates the ratio of two sample variances. If the populations have equal variances, this ratio should be close to 1. The F-statistic follows an F-distribution with degrees of freedom based on the sample sizes of both groups. The test can be one-tailed (testing if one variance is greater) or two-tailed (testing if variances are different in either direction).

### Characteristics
- Tests null hypothesis that two population variances are equal
- Returns F-statistic, degrees of freedom, and p-value
- Can perform one-tailed or two-tailed tests
- Parametric test assuming normal distributions
- Sensitive to departures from normality
- Commonly used as assumption check for t-tests and ANOVA

### Limitations
- Highly sensitive to non-normality (more so than t-test)
- Only compares two groups at a time
- Less robust than Levene's test or Bartlett's test for equal variance
- Cannot determine practical significance of variance difference
- Assumption of normality is critical for valid results

## When to Use TD_FTest

TD_FTest is essential for comparing variability between two groups in various analytical scenarios:

### Statistical Assumption Testing
- Check equal variance assumption before performing two-sample t-test
- Validate homoscedasticity assumption for ANOVA
- Determine if pooled or separate variance t-test is appropriate
- Verify assumptions for regression analysis
- Assess variance equality in experimental designs

### Quality Control and Process Consistency
- Compare process variability between two production lines
- Test if new process has same consistency as current process
- Evaluate if quality variance differs between suppliers
- Compare measurement precision between instruments
- Assess consistency between manufacturing shifts

### Risk and Volatility Analysis
- Compare volatility between two investment portfolios
- Test if risk levels differ between two strategies
- Evaluate variance in returns between asset classes
- Compare variability in sales between regions
- Assess consistency of customer behavior patterns

### Method Comparison and Validation
- Compare precision of two measurement methods
- Test if new testing procedure has similar variability
- Evaluate consistency between manual and automated processes
- Compare variability of different forecasting models
- Assess reproducibility between laboratories

### Before-After Studies
- Test if process improvement reduced variability
- Compare variance before and after intervention
- Evaluate if training reduced performance inconsistency
- Test if system upgrade affected output stability
- Assess if policy change impacted variation

## Syntax

```sql
TD_FTest (
    Sample1Column ('first_sample_column'),
    Sample2Column ('second_sample_column'),
    [ Alpha (alpha_value) ],
    [ Alternative ('test_type') ]
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
- **Examples**: response_time_group1, sales_process_A, measurement_method_1
- **Constraint**: Must contain at least 2 non-null numeric values

### Sample2Column
**Required**: Specify the name of the column containing values for the second sample.
- **Data Type**: Numeric (INTEGER, FLOAT, DECIMAL, etc.)
- **Description**: Continuous measurements from second group
- **Examples**: response_time_group2, sales_process_B, measurement_method_2
- **Constraint**: Must contain at least 2 non-null numeric values

## Optional Elements

### Alpha
Specify the significance level for the hypothesis test.
- **Default**: 0.05 (95% confidence level)
- **Valid Range**: 0 < alpha < 1
- **Common Values**:
  - 0.01: 99% confidence (strict, reduces Type I error)
  - 0.05: 95% confidence (standard in most research)
  - 0.10: 90% confidence (lenient, increases power)
- **Interpretation**: If p-value < alpha, reject null hypothesis (variances differ)

### Alternative
Specify the type of alternative hypothesis.
- **Default**: 'two-sided'
- **Valid Values**:
  - **'two-sided'**: Test if variances are different (var1 ≠ var2)
  - **'greater'**: Test if variance1 > variance2
  - **'less'**: Test if variance1 < variance2
- **Use Cases**:
  - Two-sided: Most common, tests any difference
  - Greater: Test if first group has more variability
  - Less: Test if first group has less variability

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
- Data should be approximately normally distributed
- Observations must be independent within and between groups

**Alternative Structure:**
- Single value column with group indicator
- Use CASE statement to pivot into two columns for TD_FTest

## Output Schema

### Output Table Schema
The output table contains F-test results.

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| f_statistic | FLOAT | Ratio of sample variances (variance1 / variance2) |
| numerator_df | INTEGER | Degrees of freedom for numerator (n1 - 1) |
| denominator_df | INTEGER | Degrees of freedom for denominator (n2 - 1) |
| p_value | FLOAT | Probability of observing F-statistic if variances are equal |
| variance_1 | FLOAT | Sample variance of first group |
| variance_2 | FLOAT | Sample variance of second group |
| critical_value | FLOAT | Critical F-value at specified alpha level |

**Interpretation:**
- **f_statistic**: Ratio of variances; values near 1 suggest equal variances
- **f_statistic >> 1**: First group has much larger variance
- **f_statistic << 1**: Second group has much larger variance
- **p_value < alpha**: Reject null hypothesis (variances are significantly different)
- **p_value ≥ alpha**: Fail to reject null hypothesis (no significant difference in variances)

## Code Examples

### Example 1: Basic F-Test - Compare Process Variability

Test if two production processes have equal variance in output quality:

```sql
-- Prepare data with separate columns for each process
WITH process_data AS (
    SELECT
        MAX(CASE WHEN process_id = 'Process_A' THEN quality_score END) as process_a_score,
        MAX(CASE WHEN process_id = 'Process_B' THEN quality_score END) as process_b_score,
        batch_id
    FROM quality_measurements
    GROUP BY batch_id
)
CREATE TABLE process_variance_ftest AS (
    SELECT * FROM TD_FTest(
        ON process_data
        USING
        Sample1Column('process_a_score')
        Sample2Column('process_b_score')
        Alpha(0.05)
        Alternative('two-sided')
    )
) WITH DATA;

-- View results with interpretation
SELECT
    f_statistic,
    numerator_df,
    denominator_df,
    p_value,
    variance_1,
    variance_2,
    variance_1 / NULLIFZERO(variance_2) as variance_ratio,
    CASE
        WHEN p_value < 0.05 THEN 'Variances are DIFFERENT - Use Welch t-test'
        ELSE 'Variances are EQUAL - Can use pooled t-test'
    END as recommendation
FROM process_variance_ftest;
```

**Quality Control Decision:**
- Equal variances: Processes have similar consistency
- Different variances: One process is less stable, requires investigation

### Example 2: Before-After Variance Comparison

Test if process improvement reduced output variability:

```sql
-- Test if variance decreased after process improvement
WITH improvement_data AS (
    SELECT
        MAX(CASE WHEN period = 'Before' THEN cycle_time END) as before_time,
        MAX(CASE WHEN period = 'After' THEN cycle_time END) as after_time,
        measurement_id
    FROM process_measurements
    GROUP BY measurement_id
)
CREATE TABLE improvement_ftest AS (
    SELECT * FROM TD_FTest(
        ON improvement_data
        USING
        Sample1Column('before_time')
        Sample2Column('after_time')
        Alpha(0.05)
        Alternative('greater')  -- Test if before variance > after variance
    )
) WITH DATA;

-- Comprehensive analysis
WITH ftest_result AS (
    SELECT * FROM improvement_ftest
),
descriptive_stats AS (
    SELECT
        'Before' as period,
        AVG(cycle_time) as mean,
        STDDEV_POP(cycle_time) as std_dev,
        VARIANCE(cycle_time) as variance,
        COUNT(*) as n
    FROM process_measurements
    WHERE period = 'Before'
    UNION ALL
    SELECT
        'After' as period,
        AVG(cycle_time) as mean,
        STDDEV_POP(cycle_time) as std_dev,
        VARIANCE(cycle_time) as variance,
        COUNT(*) as n
    FROM process_measurements
    WHERE period = 'After'
)
SELECT
    d.period,
    ROUND(d.mean, 2) as mean_time,
    ROUND(d.std_dev, 2) as std_dev,
    ROUND(d.variance, 2) as variance,
    d.n as sample_size,
    CASE d.period
        WHEN 'Before' THEN ROUND((SELECT f_statistic FROM ftest_result), 3)
        ELSE NULL
    END as f_statistic,
    CASE d.period
        WHEN 'Before' THEN ROUND((SELECT p_value FROM ftest_result), 6)
        ELSE NULL
    END as p_value,
    CASE d.period
        WHEN 'After' THEN
            CASE
                WHEN (SELECT p_value FROM ftest_result) < 0.05
                THEN 'Variability significantly reduced'
                ELSE 'No significant reduction in variability'
            END
        ELSE NULL
    END as conclusion
FROM descriptive_stats d
ORDER BY d.period DESC;
```

**Process Improvement Validation:**
- p-value < 0.05: Improvement successfully reduced variability
- p-value ≥ 0.05: No significant change in consistency

### Example 3: Assumption Check for T-Test

Validate equal variance assumption before comparing group means:

```sql
-- Step 1: F-test for equal variances
WITH group_data AS (
    SELECT
        MAX(CASE WHEN test_group = 'Control' THEN metric_value END) as control_value,
        MAX(CASE WHEN test_group = 'Treatment' THEN metric_value END) as treatment_value,
        subject_id
    FROM experiment_data
    GROUP BY subject_id
)
CREATE TABLE variance_assumption_check AS (
    SELECT * FROM TD_FTest(
        ON group_data
        USING
        Sample1Column('control_value')
        Sample2Column('treatment_value')
        Alpha(0.05)
        Alternative('two-sided')
    )
) WITH DATA;

-- Step 2: Determine appropriate t-test approach
SELECT
    f_statistic,
    p_value,
    CASE
        WHEN p_value >= 0.05 THEN 'Equal Variance Assumption MET'
        ELSE 'Equal Variance Assumption VIOLATED'
    END as assumption_status,
    CASE
        WHEN p_value >= 0.05 THEN 'Use standard two-sample t-test with pooled variance'
        ELSE 'Use Welch t-test (separate variances)'
    END as recommended_test,
    CASE
        WHEN f_statistic BETWEEN 0.5 AND 2.0 THEN 'Variances are similar (ratio < 2:1)'
        WHEN f_statistic > 2.0 THEN 'Control group has much higher variance'
        ELSE 'Treatment group has much higher variance'
    END as variance_comparison
FROM variance_assumption_check;
```

**Statistical Workflow:**
1. Run F-test first to check assumption
2. Choose appropriate t-test based on F-test result
3. Report F-test result alongside t-test

### Example 4: Multi-Group Variance Comparison

Compare variances across multiple pairs of groups:

```sql
-- Compare all pairwise variances between suppliers
CREATE TABLE supplier_variance_comparison AS (
    -- Supplier A vs B
    WITH ab_data AS (
        SELECT
            MAX(CASE WHEN supplier = 'A' THEN defect_rate END) as supplier_a,
            MAX(CASE WHEN supplier = 'B' THEN defect_rate END) as supplier_b,
            batch_id
        FROM quality_data
        GROUP BY batch_id
    )
    SELECT 'A vs B' as comparison, * FROM TD_FTest(
        ON ab_data
        USING Sample1Column('supplier_a') Sample2Column('supplier_b') Alpha(0.05) Alternative('two-sided')
    )

    UNION ALL

    -- Supplier A vs C
    WITH ac_data AS (
        SELECT
            MAX(CASE WHEN supplier = 'A' THEN defect_rate END) as supplier_a,
            MAX(CASE WHEN supplier = 'C' THEN defect_rate END) as supplier_c,
            batch_id
        FROM quality_data
        GROUP BY batch_id
    )
    SELECT 'A vs C' as comparison, * FROM TD_FTest(
        ON ac_data
        USING Sample1Column('supplier_a') Sample2Column('supplier_c') Alpha(0.05) Alternative('two-sided')
    )

    UNION ALL

    -- Supplier B vs C
    WITH bc_data AS (
        SELECT
            MAX(CASE WHEN supplier = 'B' THEN defect_rate END) as supplier_b,
            MAX(CASE WHEN supplier = 'C' THEN defect_rate END) as supplier_c,
            batch_id
        FROM quality_data
        GROUP BY batch_id
    )
    SELECT 'B vs C' as comparison, * FROM TD_FTest(
        ON bc_data
        USING Sample1Column('supplier_b') Sample2Column('supplier_c') Alpha(0.05) Alternative('two-sided')
    )
) WITH DATA;

-- Summarize all comparisons
SELECT
    comparison,
    ROUND(f_statistic, 3) as f_stat,
    ROUND(p_value, 4) as p_val,
    ROUND(variance_1, 2) as var_1,
    ROUND(variance_2, 2) as var_2,
    CASE
        WHEN p_value < 0.05 THEN 'Significant Difference'
        ELSE 'No Significant Difference'
    END as result,
    CASE
        WHEN p_value < 0.05 THEN
            CASE
                WHEN variance_1 > variance_2 THEN 'First supplier more variable'
                ELSE 'Second supplier more variable'
            END
        ELSE 'Similar variability'
    END as interpretation
FROM supplier_variance_comparison
ORDER BY p_value;
```

**Note:** Apply Bonferroni correction for multiple comparisons (alpha = 0.05 / 3 = 0.0167)

### Example 5: Measurement System Precision Comparison

Compare precision of two measurement instruments:

```sql
-- Test if new instrument has similar precision to reference standard
WITH instrument_data AS (
    SELECT
        MAX(CASE WHEN instrument = 'Reference' THEN measurement END) as reference_measure,
        MAX(CASE WHEN instrument = 'New' THEN measurement END) as new_measure,
        sample_id
    FROM calibration_study
    GROUP BY sample_id
)
CREATE TABLE instrument_precision_ftest AS (
    SELECT * FROM TD_FTest(
        ON instrument_data
        USING
        Sample1Column('reference_measure')
        Sample2Column('new_measure')
        Alpha(0.01)  -- Stricter for validation study
        Alternative('two-sided')
    )
) WITH DATA;

-- Detailed precision report
WITH ftest_results AS (
    SELECT * FROM instrument_precision_ftest
),
instrument_stats AS (
    SELECT
        instrument,
        COUNT(*) as n_measurements,
        AVG(measurement) as mean_value,
        STDDEV_POP(measurement) as std_dev,
        VARIANCE(measurement) as variance,
        -- Coefficient of Variation (CV%)
        (STDDEV_POP(measurement) / NULLIFZERO(AVG(measurement))) * 100 as cv_percent
    FROM calibration_study
    GROUP BY instrument
)
SELECT
    i.instrument,
    i.n_measurements,
    ROUND(i.mean_value, 3) as mean,
    ROUND(i.std_dev, 4) as std_dev,
    ROUND(i.variance, 6) as variance,
    ROUND(i.cv_percent, 2) as cv_pct,
    CASE i.instrument
        WHEN 'Reference' THEN ROUND((SELECT f_statistic FROM ftest_results), 3)
        ELSE NULL
    END as f_statistic,
    CASE i.instrument
        WHEN 'Reference' THEN ROUND((SELECT p_value FROM ftest_results), 6)
        ELSE NULL
    END as p_value,
    CASE i.instrument
        WHEN 'New' THEN
            CASE
                WHEN (SELECT p_value FROM ftest_results) >= 0.01
                THEN 'VALIDATED - Similar precision to reference'
                ELSE 'FAILED - Precision differs from reference'
            END
        ELSE NULL
    END as validation_result
FROM instrument_stats i
ORDER BY i.instrument;
```

**Validation Decision:**
- p-value ≥ 0.01: New instrument validated, can replace reference
- p-value < 0.01: New instrument precision differs, requires calibration

### Example 6: Investment Portfolio Risk Comparison

Compare volatility between two investment strategies:

```sql
-- Test if portfolios have equal return volatility
WITH portfolio_returns AS (
    SELECT
        MAX(CASE WHEN portfolio = 'Conservative' THEN daily_return END) as conservative_return,
        MAX(CASE WHEN portfolio = 'Aggressive' THEN daily_return END) as aggressive_return,
        trade_date
    FROM portfolio_performance
    GROUP BY trade_date
)
CREATE TABLE portfolio_risk_ftest AS (
    SELECT * FROM TD_FTest(
        ON portfolio_returns
        USING
        Sample1Column('aggressive_return')  -- Expect higher variance
        Sample2Column('conservative_return')
        Alpha(0.05)
        Alternative('greater')  -- Test if aggressive > conservative variance
    )
) WITH DATA;

-- Risk comparison report
WITH risk_metrics AS (
    SELECT
        portfolio,
        AVG(daily_return) as mean_return,
        STDDEV_POP(daily_return) as volatility,
        VARIANCE(daily_return) as variance,
        (AVG(daily_return) / NULLIFZERO(STDDEV_POP(daily_return))) as sharpe_ratio_proxy
    FROM portfolio_performance
    GROUP BY portfolio
)
SELECT
    r.*,
    ROUND((SELECT f_statistic FROM portfolio_risk_ftest), 3) as f_statistic,
    ROUND((SELECT p_value FROM portfolio_risk_ftest), 4) as p_value,
    CASE
        WHEN (SELECT p_value FROM portfolio_risk_ftest) < 0.05
        THEN 'Aggressive portfolio has significantly higher risk'
        ELSE 'Risk levels are not significantly different'
    END as risk_assessment
FROM risk_metrics r
ORDER BY r.variance DESC;
```

**Investment Decision:**
- Significant difference: Risk levels align with strategy intent
- No difference: Portfolios not sufficiently differentiated by risk

## Common Use Cases

### 1. ANOVA Assumption Validation

```sql
-- Check equal variance assumption before ANOVA
-- If any pairwise comparison has unequal variance, consider Welch ANOVA
CREATE TABLE anova_assumption_ftests AS (
    -- Compare each pair of groups
    ...
) WITH DATA;

SELECT
    COUNT(*) as total_comparisons,
    SUM(CASE WHEN p_value < 0.05 THEN 1 ELSE 0 END) as violations,
    CASE
        WHEN SUM(CASE WHEN p_value < 0.05 THEN 1 ELSE 0 END) = 0
        THEN 'ANOVA assumptions met - proceed with standard ANOVA'
        ELSE 'Unequal variances detected - use Welch ANOVA or transform data'
    END as recommendation
FROM anova_assumption_ftests;
```

### 2. Quality Control - Process Consistency Monitoring

```sql
-- Monitor if process variance remains stable over time
CREATE TABLE weekly_variance_ftest AS (
    WITH weekly_data AS (
        SELECT
            MAX(CASE WHEN week = CURRENT_WEEK THEN metric END) as current_week,
            MAX(CASE WHEN week = CURRENT_WEEK - 1 THEN metric END) as previous_week,
            unit_id
        FROM production_data
        GROUP BY unit_id
    )
    SELECT CURRENT_WEEK as comparison_week, * FROM TD_FTest(
        ON weekly_data
        USING Sample1Column('current_week') Sample2Column('previous_week')
        Alpha(0.05) Alternative('two-sided')
    )
) WITH DATA;

-- Alert on significant changes
SELECT
    comparison_week,
    f_statistic,
    p_value,
    CASE
        WHEN p_value < 0.05 THEN 'ALERT: Process variance changed - investigate'
        ELSE 'Process stable'
    END as status
FROM weekly_variance_ftest
WHERE p_value < 0.05;
```

### 3. A/B Test Heterogeneous Treatment Effects

```sql
-- Test if treatment effect varies more than control (heterogeneous effects)
WITH treatment_variance AS (
    SELECT * FROM TD_FTest(
        ON ab_test_outcomes
        USING Sample1Column('treatment_outcome') Sample2Column('control_outcome')
        Alpha(0.05) Alternative('greater')
    )
)
SELECT
    CASE
        WHEN p_value < 0.05
        THEN 'Treatment has heterogeneous effects - segment analysis recommended'
        ELSE 'Treatment effect is consistent across users'
    END as recommendation
FROM treatment_variance;
```

## Best Practices

1. **Check Normality First**:
   - F-test is very sensitive to non-normality
   - Use Q-Q plots, histograms, or Shapiro-Wilk test
   - Consider Levene's test or Bartlett's test as alternatives (more robust)

2. **Choose Appropriate Alternative Hypothesis**:
   - Use 'two-sided' for general variance equality testing
   - Use 'greater' or 'less' only when direction is predicted a priori
   - One-sided tests have more power but require theoretical justification

3. **Interpret F-Statistic Magnitude**:
   - F ≈ 1: Variances are similar
   - F > 2 or F < 0.5: Variances differ by factor of 2+ (practically significant)
   - Very large or very small F: Strong evidence of variance difference

4. **Consider Effect Size**:
   - Variance ratio provides practical significance
   - Ratio between 0.5 and 2.0: Variances similar enough for most purposes
   - Report actual variances alongside F-statistic

5. **Sample Size Matters**:
   - F-test power increases with sample size
   - Small samples: May miss real variance differences
   - Large samples: May detect trivial differences as significant

6. **Use as Preliminary Test**:
   - F-test commonly used before t-test or ANOVA
   - If variances unequal, use Welch t-test or Welch ANOVA
   - Don't skip F-test in assumption checking workflow

7. **Report Comprehensively**:
   - Include sample sizes, variances, F-statistic, df, p-value
   - Report variance ratio for practical interpretation
   - Provide context on implications for subsequent analyses

## Related Functions

- **TD_ANOVA**: Compare means across groups (assumes equal variances)
- **TD_ZTest**: Compare means between two groups (large samples)
- **TD_UnivariateStatistics**: Calculate variances and other descriptive statistics
- **VARIANCE / STDDEV_POP**: Calculate sample variances manually
- **TD_OutlierFilterFit**: Remove outliers that may distort variance estimates

## Notes and Limitations

1. **Sensitivity to Non-Normality**:
   - F-test assumes both samples come from normal distributions
   - More sensitive to this assumption than t-test
   - With non-normal data, use Levene's test or Bartlett's test instead

2. **Two-Group Limitation**:
   - F-test only compares two variances at a time
   - For 3+ groups, use Levene's test or Bartlett's test
   - Multiple pairwise F-tests require correction for multiple comparisons

3. **Sample Size Effects**:
   - Unequal sample sizes acceptable but affect power
   - Very unequal sample sizes (ratio > 4:1) may reduce reliability
   - Very large samples may detect trivial differences

4. **Alternative Tests**:
   - **Levene's test**: More robust to non-normality
   - **Bartlett's test**: More powerful under normality
   - **Brown-Forsythe test**: Robust alternative to Levene's test

5. **Interpretation Caution**:
   - "Equal variances" means no detectable difference, not identical
   - Non-significant result may be due to low power
   - Always report confidence intervals when possible

6. **Practical vs Statistical Significance**:
   - Variance ratio of 1.5 may be significant but not practically important
   - Variance ratio > 2.0 often considered practically significant
   - Context matters: 10% vs 20% defect rate variance has different implications than $10 vs $20 price variance

7. **Assumption Testing Cascade**:
   - F-test result determines which subsequent test to use
   - If F-test rejects (p < 0.05): Use Welch t-test
   - If F-test doesn't reject (p ≥ 0.05): Can use pooled t-test

## Version Information

- **Function Version**: Based on Teradata Database Analytic Functions Version 17.20
- **Generated**: November 28, 2025
- **Category**: Hypothesis Testing / Statistical Analysis
