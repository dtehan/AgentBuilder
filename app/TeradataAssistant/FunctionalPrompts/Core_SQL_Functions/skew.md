# SKEW

### Function Name
**SKEW**

### Description
Returns the skewness of the distribution of value_expression. Skewness measures the asymmetry of a probability distribution. Positive skew indicates right-tailedness (long tail on right), negative skew indicates left-tailedness (long tail on left). This function returns the REAL data type.

### When the Function Would Be Used
- Measure distribution asymmetry in datasets
- Analyze data symmetry for statistical inference
- Detect skewed distributions in quality control
- Compare distribution shapes across populations
- Identify asymmetrical patterns in business metrics
- Assess normality assumptions for statistical tests
- Detect outliers and extreme values

### Syntax
```sql
SKEW ([ DISTINCT | ALL ] value_expression)
```

### Code Examples

**Example 1: Basic Skewness Calculation**
```sql
SELECT CAST(SKEW(SalesAmount) AS DECIMAL(10,6)) AS SalesSkew
FROM SalesData;
```

**Example 2: Skewness by Department**
```sql
SELECT 
    Department,
    CAST(SKEW(Salary) AS DECIMAL(10,6)) AS SalarySkew
FROM Employee
GROUP BY Department;
```

**Example 3: Skewness Analysis**
```sql
SELECT 
    CAST(SKEW(Price) AS DECIMAL(10,6)) AS PriceSkew
FROM ProductCatalog
WHERE Status = 'Active';
```

**Example 4: Skewness with WHERE Filter**
```sql
SELECT 
    Region,
    CAST(SKEW(Revenue) AS DECIMAL(10,6)) AS RevenueSkew
FROM RegionalPerformance
WHERE Year = 2024
GROUP BY Region;
```

**Example 5: Skewness with Distribution Stats**
```sql
SELECT 
    Category,
    COUNT(*) AS RecordCount,
    AVG(Value) AS MeanValue,
    CAST(SKEW(Value) AS DECIMAL(10,6)) AS SkewValue,
    CAST(KURTOSIS(Value) AS DECIMAL(10,6)) AS KurtosisValue
FROM DataDistribution
GROUP BY Category;
```

**Example 6: Skewness with DISTINCT**
```sql
SELECT 
    CAST(SKEW(DISTINCT ProductPrice) AS DECIMAL(10,6)) AS DistinctPriceSkew
FROM ProductInventory;
```

**Example 7: Detecting Skewed Distributions**
```sql
SELECT 
    ProcessLine,
    CAST(SKEW(OutputQuality) AS DECIMAL(10,6)) AS QualitySkew
FROM ManufacturingMetrics
WHERE CAST(SKEW(OutputQuality) AS DECIMAL(10,6)) > 1.0
GROUP BY ProcessLine;
```

**Example 8: Skewness for Anomaly Detection**
```sql
SELECT 
    Year,
    CAST(SKEW(DailyReturn) AS DECIMAL(10,6)) AS ReturnSkew
FROM StockMarketData
GROUP BY Year
HAVING CAST(SKEW(DailyReturn) AS DECIMAL(10,6)) > 0.5;
```

**Example 9: Comparing Skewness Across Groups**
```sql
SELECT 
    Department,
    Job_Title,
    CAST(SKEW(Compensation) AS DECIMAL(10,6)) AS CompSkew
FROM EmployeeData
GROUP BY Department, Job_Title
ORDER BY CompSkew DESC;
```

**Example 10: Skewness with Multiple Statistical Measures**
```sql
SELECT 
    Segment,
    COUNT(*) AS n,
    AVG(Value) AS Mean,
    STDDEV_POP(Value) AS StdDev,
    CAST(SKEW(Value) AS DECIMAL(10,6)) AS Skew,
    CAST(KURTOSIS(Value) AS DECIMAL(10,6)) AS Kurtosis
FROM BusinessMetrics
GROUP BY Segment
ORDER BY Skew DESC;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
