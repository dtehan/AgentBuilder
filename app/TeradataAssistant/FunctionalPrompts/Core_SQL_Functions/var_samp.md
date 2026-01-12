# VAR_SAMP

### Function Name
**VAR_SAMP**

### Description
Returns the sample variance for the data points in value_expression. Use when you have a sample of data and want to infer about the population. Uses n-1 as divisor. Returns the REAL data type.

### When the Function Would Be Used
- Calculate sample variance for statistical analysis
- Estimate population variance from sample data
- Analyze variance in sample test results
- Determine variability estimates from surveys
- Project dispersion based on sampled data
- Make population inferences from samples
- Build statistical confidence intervals

### Syntax
```sql
VAR_SAMP ([ DISTINCT | ALL ] value_expression)
```

### Code Examples

**Example 1: Basic Sample Variance**
```sql
SELECT VAR_SAMP(TestScore) AS ScoreVariance
FROM StudentSample;
```

**Example 2: Sample Variance by Group**
```sql
SELECT 
    TeacherID,
    VAR_SAMP(StudentScore) AS ScoreVariance
FROM ClassSample
GROUP BY TeacherID;
```

**Example 3: Sample Variance with Statistics**
```sql
SELECT 
    COUNT(*) AS SampleSize,
    AVG(Measurement) AS SampleMean,
    VAR_SAMP(Measurement) AS SampleVariance
FROM ExperimentalSample;
```

**Example 4: Sample Variance for Survey**
```sql
SELECT 
    Region,
    VAR_SAMP(SurveyResponse) AS ResponseVariance
FROM SurveySample
WHERE SampleYear = 2024
GROUP BY Region;
```

**Example 5: Variance Estimates**
```sql
SELECT 
    Product,
    VAR_SAMP(SamplePrice) AS PriceVarianceEstimate
FROM PriceSample
GROUP BY Product;
```

**Example 6: Sample Variance Calculation**
```sql
SELECT 
    SampleID,
    COUNT(*) AS n,
    AVG(Value) AS SampleMean,
    VAR_SAMP(Value) AS SampleVariance,
    SQRT(VAR_SAMP(Value)) AS SampleStdDev
FROM DataSample
GROUP BY SampleID;
```

**Example 7: Quality Estimation**
```sql
SELECT 
    LotNumber,
    COUNT(*) AS SampleSize,
    AVG(Defects) AS AvgDefects,
    VAR_SAMP(Defects) AS DefectVariance
FROM QualitySample
GROUP BY LotNumber;
```

**Example 8: Statistical Inference**
```sql
SELECT 
    Department,
    VAR_SAMP(SalaryIncrease) AS SalaryIncreaseVariance
FROM SalaryAuditSample
GROUP BY Department;
```

**Example 9: Population vs Sample Estimates**
```sql
SELECT 
    Category,
    COUNT(*) AS SampleSize,
    VAR_SAMP(Value) AS SampleVariance
FROM AnalysisSample
GROUP BY Category
ORDER BY SampleSize DESC;
```

**Example 10: Confidence Interval with Variance**
```sql
SELECT 
    ExperimentID,
    COUNT(*) AS n,
    AVG(Result) AS Mean,
    VAR_SAMP(Result) AS Variance,
    SQRT(VAR_SAMP(Result) / COUNT(*)) AS StandardError
FROM ExperimentResults
GROUP BY ExperimentID;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
