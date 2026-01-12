# KURTOSIS

### Function Name
**KURTOSIS**

### Description
Returns the kurtosis of the distribution of value_expression. Kurtosis measures the 'tailedness' or peakedness of a probability distribution. Positive kurtosis indicates heavier tails and sharper peak; negative kurtosis indicates lighter tails and flatter peak. This function returns the REAL data type.

### When the Function Would Be Used
- Analyze the peakedness or flatness of data distributions
- Detect outliers in statistical analysis
- Measure the tail risk in financial data
- Compare distribution shapes across datasets
- Quality control in manufacturing processes
- Identify extreme value risks
- Assess data normality for statistical tests

### Syntax
```sql
KURTOSIS ([ DISTINCT | ALL ] value_expression)
```

### Code Examples

**Example 1: Basic Kurtosis Calculation**
```sql
SELECT KURTOSIS(SalesAmount) AS SalesKurtosis
FROM SalesData;
```

**Example 2: Kurtosis by Sales Region**
```sql
SELECT 
    Region,
    KURTOSIS(SalesAmount) AS KurtosisValue
FROM SalesData
GROUP BY Region;
```

**Example 3: Kurtosis with Type Casting**
```sql
SELECT 
    CAST(KURTOSIS(Price) AS DECIMAL(10,6)) AS PriceKurtosis
FROM ProductCatalog;
```

**Example 4: Kurtosis with WHERE Clause**
```sql
SELECT 
    Department,
    KURTOSIS(Salary) AS SalaryKurtosis
FROM Employee
WHERE HireDate BETWEEN '2020-01-01' AND '2024-01-01'
GROUP BY Department;
```

**Example 5: Multiple Distribution Analysis with Kurtosis**
```sql
SELECT 
    KURTOSIS(Age) AS AgeKurtosis,
    KURTOSIS(Salary) AS SalaryKurtosis,
    KURTOSIS(YearsService) AS YearsServiceKurtosis
FROM EmployeeData;
```

**Example 6: Kurtosis with DISTINCT**
```sql
SELECT 
    KURTOSIS(DISTINCT ProductPrice) AS DistinctPriceKurtosis
FROM ProductInventory;
```

**Example 7: Kurtosis with Complex Filtering**
```sql
SELECT 
    SalesQuarter,
    KURTOSIS(QuarterlyRevenue) AS RevenueKurtosis
FROM QuarterlyResults
WHERE Region IN ('North', 'South')
GROUP BY SalesQuarter
HAVING KURTOSIS(QuarterlyRevenue) > 2.5;
```

**Example 8: Comparing Kurtosis with Other Distribution Metrics**
```sql
SELECT 
    Category,
    COUNT(*) AS RecordCount,
    AVG(Value) AS MeanValue,
    KURTOSIS(Value) AS KurtosisValue,
    STDDEV_POP(Value) AS StdDev
FROM DataDistribution
GROUP BY Category;
```

**Example 9: Kurtosis for Anomaly Detection**
```sql
SELECT 
    ProcessLine,
    KURTOSIS(OutputQuality) AS QualityKurtosis
FROM ManufacturingMetrics
WHERE KURTOSIS(OutputQuality) > 3.0
GROUP BY ProcessLine;
```

**Example 10: Kurtosis Analysis by Time Period**
```sql
SELECT 
    Year,
    Month,
    CAST(KURTOSIS(DailyReturn) AS DECIMAL(10,4)) AS ReturnKurtosis
FROM StockMarketData
GROUP BY Year, Month
ORDER BY Year DESC, Month DESC;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
