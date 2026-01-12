# STDDEV_POP

### Function Name
**STDDEV_POP** | **STDEV**

### Description
Returns the population standard deviation for the non-null data points in value_expression. Use when you have the entire population of data. Standard deviation measures the spread or dispersion of values from the mean. This function returns the REAL data type.

### When the Function Would Be Used
- Calculate population standard deviation for complete datasets
- Measure variability in entire product populations
- Analyze full company salary distributions
- Determine deviation in complete inventory counts
- Assess spread in comprehensive market data
- Evaluate consistency across all data points
- Measure total variability in populations

### Syntax
```sql
{ STDDEV_POP | STDEV } ([ DISTINCT | ALL ] value_expression)
```

### Code Examples

**Example 1: Basic Population Standard Deviation**
```sql
SELECT CAST(STDDEV_POP(Salary) AS DECIMAL(10,2)) AS SalaryStdDev
FROM Employee;
```

**Example 2: Population StdDev by Department**
```sql
SELECT 
    Department,
    CAST(STDDEV_POP(Salary) AS DECIMAL(10,2)) AS DeptStdDev
FROM Employee
GROUP BY Department;
```

**Example 3: Population StdDev with COUNT**
```sql
SELECT 
    COUNT(*) AS RecordCount,
    AVG(Price) AS AvgPrice,
    CAST(STDDEV_POP(Price) AS DECIMAL(10,2)) AS PriceStdDev
FROM Products;
```

**Example 4: Population StdDev with WHERE**
```sql
SELECT 
    Category,
    CAST(STDDEV_POP(Revenue) AS DECIMAL(10,2)) AS RevenueStdDev
FROM Sales
WHERE Year = 2024
GROUP BY Category;
```

**Example 5: Comparing Pop vs Sample StdDev**
```sql
SELECT 
    Department,
    CAST(STDDEV_POP(Salary) AS DECIMAL(10,2)) AS PopStdDev,
    CAST(STDDEV_SAMP(Salary) AS DECIMAL(10,2)) AS SampStdDev
FROM Employee
GROUP BY Department;
```

**Example 6: Population StdDev with DISTINCT**
```sql
SELECT 
    CAST(STDDEV_POP(DISTINCT Price) AS DECIMAL(10,2)) AS DistinctPriceStdDev
FROM ProductCatalog;
```

**Example 7: Quality Control Analysis**
```sql
SELECT 
    ProcessLine,
    AVG(OutputQuality) AS AvgQuality,
    CAST(STDDEV_POP(OutputQuality) AS DECIMAL(10,4)) AS QualityStdDev
FROM ManufacturingData
GROUP BY ProcessLine;
```

**Example 8: Variability Assessment**
```sql
SELECT 
    Region,
    CAST(STDDEV_POP(DailySales) AS DECIMAL(10,2)) AS SalesVariability
FROM RegionalSales
GROUP BY Region
HAVING CAST(STDDEV_POP(DailySales) AS DECIMAL(10,2)) > 5000;
```

**Example 9: Statistical Summary Report**
```sql
SELECT 
    Segment,
    COUNT(*) AS n,
    AVG(Value) AS Mean,
    CAST(STDDEV_POP(Value) AS DECIMAL(10,4)) AS PopStdDev,
    MIN(Value) AS MinValue,
    MAX(Value) AS MaxValue
FROM AnalyticsData
GROUP BY Segment;
```

**Example 10: Consistency Comparison**
```sql
SELECT 
    Department,
    Job_Title,
    CAST(STDDEV_POP(Salary) AS DECIMAL(10,2)) AS SalaryVariability
FROM EmployeeData
GROUP BY Department, Job_Title
ORDER BY SalaryVariability DESC;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
