# VAR_POP

### Function Name
**VAR_POP**

### Description
Returns the population variance for the data points in value_expression. Use when you have the entire population of data. Variance is the square of standard deviation. Returns the REAL data type.

### When the Function Would Be Used
- Calculate population variance for complete datasets
- Measure data dispersion in entire populations
- Analyze price variance across all products
- Determine variability in complete sales data
- Assess spread in comprehensive datasets
- Evaluate consistency across all items
- Calculate total variance in populations

### Syntax
```sql
VAR_POP ([ DISTINCT | ALL ] value_expression)
```

### Code Examples

**Example 1: Basic Population Variance**
```sql
SELECT VAR_POP(Salary) AS SalaryVariance
FROM Employee;
```

**Example 2: Population Variance by Group**
```sql
SELECT 
    Department,
    VAR_POP(Salary) AS DeptVariance
FROM Employee
GROUP BY Department;
```

**Example 3: Population Variance with Count**
```sql
SELECT 
    COUNT(*) AS RecordCount,
    AVG(Price) AS AvgPrice,
    VAR_POP(Price) AS PriceVariance
FROM Products;
```

**Example 4: Population Variance with WHERE**
```sql
SELECT 
    Region,
    VAR_POP(Revenue) AS RevenueVariance
FROM Sales
WHERE Year = 2024
GROUP BY Region;
```

**Example 5: Comparing Pop vs Sample Variance**
```sql
SELECT 
    Department,
    VAR_POP(Salary) AS PopVariance,
    VAR_SAMP(Salary) AS SampVariance
FROM Employee
GROUP BY Department;
```

**Example 6: Population Variance with DISTINCT**
```sql
SELECT 
    VAR_POP(DISTINCT Price) AS DistinctPriceVariance
FROM ProductCatalog;
```

**Example 7: Variance Analysis**
```sql
SELECT 
    ProcessLine,
    AVG(OutputQuality) AS AvgQuality,
    VAR_POP(OutputQuality) AS QualityVariance
FROM ManufacturingData
GROUP BY ProcessLine;
```

**Example 8: Consistency Measurement**
```sql
SELECT 
    Region,
    VAR_POP(DailySales) AS SalesVariance
FROM RegionalSales
GROUP BY Region
HAVING VAR_POP(DailySales) > 10000000;
```

**Example 9: Statistical Summary**
```sql
SELECT 
    Category,
    COUNT(*) AS n,
    AVG(Value) AS Mean,
    VAR_POP(Value) AS PopVariance,
    SQRT(VAR_POP(Value)) AS StdDev
FROM AnalyticsData
GROUP BY Category;
```

**Example 10: Dispersion Comparison**
```sql
SELECT 
    Department,
    VAR_POP(Salary) AS SalaryDispersion
FROM EmployeeData
GROUP BY Department
ORDER BY SalaryDispersion DESC;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
