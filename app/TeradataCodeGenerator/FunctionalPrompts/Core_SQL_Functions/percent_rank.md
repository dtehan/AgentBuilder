# PERCENT_RANK

### Function Name
**PERCENT_RANK**

### Description
Returns the relative rank of each row as a value between 0 and 1 (inclusive). Calculates the position as (rank - 1) / (total rows - 1). Useful for percentile analysis.

### When the Function Would Be Used
- Calculate percentile positions
- Determine relative ranking
- Find percentile groups
- Analyze distribution positions
- Create percentile analysis
- Identify top X percent
- Quartile and decile analysis

### Syntax
```sql
PERCENT_RANK() OVER (
    [ PARTITION BY partition_column(s) ]
    ORDER BY sort_column(s) [ ASC | DESC ]
)
```

### Code Examples

**Example 1: Basic Percent Rank**
```sql
SELECT 
    EmployeeName,
    Salary,
    CAST(PERCENT_RANK() OVER (ORDER BY Salary DESC) AS DECIMAL(5,4)) AS PercentRank
FROM Employee;
```

**Example 2: Top 25 Percent**
```sql
SELECT 
    EmployeeName,
    Salary,
    PERCENT_RANK() OVER (ORDER BY Salary DESC) AS PercentRank
FROM Employee
WHERE PERCENT_RANK() OVER (ORDER BY Salary DESC) <= 0.25;
```

**Example 3: Department-level Percentile**
```sql
SELECT 
    Department,
    EmployeeName,
    Salary,
    CAST(PERCENT_RANK() OVER (PARTITION BY Department ORDER BY Salary DESC) AS DECIMAL(5,4)) AS DeptPercentRank
FROM Employee;
```

**Example 4: Percentile Analysis**
```sql
SELECT 
    ProductID,
    Sales,
    CAST(PERCENT_RANK() OVER (ORDER BY Sales DESC) AS DECIMAL(5,4)) AS SalesPercentile
FROM Products;
```

**Example 5: Identify Top Performers**
```sql
SELECT 
    StudentID,
    StudentName,
    TestScore,
    PERCENT_RANK() OVER (ORDER BY TestScore DESC) AS PercentRank
FROM StudentTests
WHERE PERCENT_RANK() OVER (ORDER BY TestScore DESC) < 0.1;  -- Top 10%
```

**Example 6: Revenue Percentile**
```sql
SELECT 
    CustomerID,
    LifetimeRevenue,
    CAST(PERCENT_RANK() OVER (ORDER BY LifetimeRevenue DESC) AS DECIMAL(5,4)) AS RevenuePercentile
FROM Customers;
```

**Example 7: Multi-partition Percentile**
```sql
SELECT 
    Region,
    Store,
    Sales,
    CAST(PERCENT_RANK() OVER (PARTITION BY Region ORDER BY Sales DESC) AS DECIMAL(5,4)) AS RegionalPercentile
FROM StoreSales;
```

**Example 8: Performance Percentile**
```sql
SELECT 
    EmployeeID,
    PerformanceScore,
    PERCENT_RANK() OVER (ORDER BY PerformanceScore DESC) AS PerformancePercentile
FROM EmployeeReview;
```

**Example 9: Quartile Assignment**
```sql
SELECT 
    CustomerID,
    SpendAmount,
    CASE 
        WHEN PERCENT_RANK() OVER (ORDER BY SpendAmount DESC) <= 0.25 THEN 'Q1'
        WHEN PERCENT_RANK() OVER (ORDER BY SpendAmount DESC) <= 0.50 THEN 'Q2'
        WHEN PERCENT_RANK() OVER (ORDER BY SpendAmount DESC) <= 0.75 THEN 'Q3'
        ELSE 'Q4'
    END AS Quartile
FROM Customers;
```

**Example 10: Decile Analysis**
```sql
SELECT 
    ProductID,
    Sales,
    CEIL(PERCENT_RANK() OVER (ORDER BY Sales DESC) * 10) AS Decile
FROM Products;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
