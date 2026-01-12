# STDDEV_SAMP

### Function Name
**STDDEV_SAMP** | **STDDEV**

### Description
Returns the sample standard deviation for the non-null data points in value_expression. Use when you have a sample of data and want to infer about the population. Uses n-1 as divisor. This function returns the REAL data type.

### When the Function Would Be Used
- Calculate sample standard deviation for statistical inference
- Estimate population variability from sample data
- Analyze test results from sample batches
- Determine deviation estimates in survey data
- Project spread based on sampled measurements
- Build confidence intervals from samples
- Make population inferences from samples

### Syntax
```sql
{ STDDEV_SAMP | STDDEV } ([ DISTINCT | ALL ] value_expression)
```

### Code Examples

**Example 1: Basic Sample Standard Deviation**
```sql
SELECT CAST(STDDEV_SAMP(TestScore) AS DECIMAL(10,2)) AS ScoreStdDev
FROM StudentSample;
```

**Example 2: Sample StdDev by Group**
```sql
SELECT 
    TeacherID,
    CAST(STDDEV_SAMP(StudentScore) AS DECIMAL(10,2)) AS ScoreStdDev
FROM ClassSample
GROUP BY TeacherID;
```

**Example 3: Sample StdDev with Statistical Summary**
```sql
SELECT 
    COUNT(*) AS SampleSize,
    AVG(Measurement) AS SampleMean,
    CAST(STDDEV_SAMP(Measurement) AS DECIMAL(10,4)) AS SampleStdDev
FROM ExperimentalSample;
```

**Example 4: Sample StdDev for Survey Data**
```sql
SELECT 
    Region,
    CAST(STDDEV_SAMP(SurveyResponse) AS DECIMAL(10,2)) AS ResponseStdDev
FROM SurveySample
WHERE SampleYear = 2024
GROUP BY Region;
```

**Example 5: Comparing Sample Estimates**
```sql
SELECT 
    Product,
    CAST(STDDEV_SAMP(SamplePrice) AS DECIMAL(10,2)) AS PriceEstimate
FROM PriceSample
GROUP BY Product;
```

**Example 6: Sample StdDev with Confidence Calculation**
```sql
SELECT 
    SampleID,
    COUNT(*) AS n,
    AVG(Value) AS SampleMean,
    CAST(STDDEV_SAMP(Value) AS DECIMAL(10,4)) AS SampleStdDev,
    CAST(STDDEV_SAMP(Value) / SQRT(COUNT(*)) AS DECIMAL(10,6)) AS StandardError
FROM DataSample
GROUP BY SampleID;
```

**Example 7: Sample StdDev for Quality Estimation**
```sql
SELECT 
    LotNumber,
    COUNT(*) AS SampleSize,
    AVG(Defects) AS AvgDefects,
    CAST(STDDEV_SAMP(Defects) AS DECIMAL(10,4)) AS DefectStdDev
FROM QualitySample
GROUP BY LotNumber;
```

**Example 8: Statistical Inference**
```sql
SELECT 
    Department,
    CAST(STDDEV_SAMP(SalaryIncrease) AS DECIMAL(10,2)) AS SalaryIncreaseStdDev
FROM SalaryAuditSample
GROUP BY Department;
```

**Example 9: Population vs Sample Estimation**
```sql
SELECT 
    Category,
    COUNT(*) AS SampleSize,
    CAST(STDDEV_SAMP(Value) AS DECIMAL(10,4)) AS SampleStdDev
FROM AnalysisSample
GROUP BY Category
ORDER BY SampleSize DESC;
```

**Example 10: Confidence Interval Calculation**
```sql
SELECT 
    ExperimentID,
    COUNT(*) AS n,
    AVG(Result) AS Mean,
    CAST(STDDEV_SAMP(Result) AS DECIMAL(10,4)) AS StdDev,
    CAST(AVG(Result) - 1.96 * STDDEV_SAMP(Result) / SQRT(COUNT(*)) AS DECIMAL(10,4)) AS CI_Lower,
    CAST(AVG(Result) + 1.96 * STDDEV_SAMP(Result) / SQRT(COUNT(*)) AS DECIMAL(10,4)) AS CI_Upper
FROM ExperimentResults
GROUP BY ExperimentID;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
