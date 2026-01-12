# COVAR_SAMP

### Function Name
**COVAR_SAMP**

### Description
Returns the sample covariance of its arguments for all non-null data point pairs. Sample covariance uses n-1 as the divisor instead of n (population). Returns NULL if there are no non-null data point pairs.

### When the Function Would Be Used
- Analyze sample covariance from survey data
- Determine relationship variability in sampled data
- Examine joint variability in experimental samples
- Estimate population covariance from sample data
- Analyze relationship between sampled measurements
- Measure covariance in statistical sampling studies
- Examine sample data relationships for inference

### Syntax
```sql
COVAR_SAMP (value_expression_1, value_expression_2)
```

### Code Examples

**Example 1: Basic Sample Covariance**
```sql
SELECT 
    COVAR_SAMP(Height, Weight) AS SampleCovarianceHW
FROM SamplePhysicalData;
```

**Example 2: Sample Covariance with Output Formatting**
```sql
SELECT 
    CAST(COVAR_SAMP(Height, Weight) AS DECIMAL(10,6)) AS SampleCovHW
FROM RegressionTable
WHERE c1 IS NOT NULL;
```

**Example 3: Sample Covariance by Group**
```sql
SELECT 
    Region,
    COVAR_SAMP(Height, Weight) AS SampleCovarianceHW
FROM RegionalSampleData
GROUP BY Region;
```

**Example 4: Stock Return Covariance**
```sql
SELECT COVAR_SAMP(Stock_A_Return, Stock_B_Return) AS SampleReturnCovariance
FROM PortfolioSampleData
WHERE SamplePeriod = 'Q4_2024';
```

**Example 5: Multiple Sample Covariances**
```sql
SELECT 
    COVAR_SAMP(Temperature, Humidity) AS TempHumidCov,
    COVAR_SAMP(Temperature, Pressure) AS TempPressCov,
    COVAR_SAMP(Humidity, Pressure) AS HumidPressCov
FROM WeatherSamples
WHERE Season = 'Winter';
```

**Example 6: Sample Covariance with WHERE Clause**
```sql
SELECT 
    StudyGroup,
    COVAR_SAMP(StudyHours, ExamScore) AS StudyScoreCov
FROM StudentSampleData
WHERE ExamScore >= 60
GROUP BY StudyGroup;
```

**Example 7: Sample Covariance with Type Casting**
```sql
SELECT 
    CAST(COVAR_SAMP(
        CAST(SalesVolume AS DECIMAL),
        CAST(UnitCost AS DECIMAL)
    ) AS DECIMAL(12,4)) AS VolumeCostSampleCov
FROM SalesInventorySample;
```

**Example 8: Sample Covariance with Aggregates**
```sql
SELECT 
    Department,
    COUNT(*) AS SampleSize,
    COVAR_SAMP(Salary, BonusAmount) AS SalaryBonusCov,
    AVG(Salary) AS AvgSalary
FROM EmployeeSample
WHERE Tenure > 1
GROUP BY Department;
```

**Example 9: Longitudinal Data Sample Covariance**
```sql
SELECT 
    PatientGroup,
    COVAR_SAMP(BaselineMeasure, FollowUpMeasure) AS MeasureChangeCov
FROM MedicalStudySample
WHERE CompletedFollowUp = TRUE
GROUP BY PatientGroup;
```

**Example 10: Time Series Sample Covariance**
```sql
SELECT 
    Year,
    COVAR_SAMP(Monthly_Sales, Monthly_Inventory) AS SalesInventoryCov,
    COUNT(*) AS MonthsInSample
FROM MonthlySalesInventory
WHERE Year >= CURRENT_YEAR - 2
GROUP BY Year
HAVING COUNT(*) >= 10
ORDER BY Year DESC;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
