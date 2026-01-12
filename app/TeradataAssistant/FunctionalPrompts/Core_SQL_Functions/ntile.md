# NTILE

### Function Name
**NTILE**

### Description
Divides rows into a specified number of approximately equal groups and assigns each row a group number. Useful for creating quartiles, quintiles, or other equal-sized groups.

### When to Use
- Create quartiles, quintiles, deciles
- Divide data into equal groups
- Segment data for analysis
- Create performance tiers
- Divide into percentile groups
- Create balanced groups

### Syntax
```sql
NTILE(num_buckets) OVER (
    [ PARTITION BY partition_column(s) ]
    ORDER BY sort_column(s)
)
```

### Code Examples

**Example 1: Create Quartiles**
```sql
SELECT 
    CustomerID,
    LifetimeValue,
    NTILE(4) OVER (ORDER BY LifetimeValue DESC) AS ValueQuartile
FROM Customers;
```

**Example 2: Segment into 10 Groups**
```sql
SELECT 
    EmployeeID,
    Salary,
    NTILE(10) OVER (ORDER BY Salary DESC) AS SalaryDecile
FROM Employee;
```

**Example 3: Performance Tiers**
```sql
SELECT 
    EmployeeID,
    PerformanceScore,
    NTILE(5) OVER (PARTITION BY Department ORDER BY PerformanceScore DESC) AS PerformanceTier
FROM EmployeeReview;
```

**Example 4: Sales Ranking Segments**
```sql
SELECT 
    ProductID,
    MonthlySales,
    NTILE(3) OVER (ORDER BY MonthlySales DESC) AS SalesTier
FROM ProductSales;
```

**Example 5: Customer Value Tiers**
```sql
SELECT 
    CustomerID,
    TotalPurchases,
    NTILE(4) OVER (ORDER BY TotalPurchases DESC) AS CustomerTier,
    CASE 
        WHEN NTILE(4) OVER (ORDER BY TotalPurchases DESC) = 1 THEN 'VIP'
        WHEN NTILE(4) OVER (ORDER BY TotalPurchases DESC) = 2 THEN 'Premium'
        WHEN NTILE(4) OVER (ORDER BY TotalPurchases DESC) = 3 THEN 'Standard'
        ELSE 'Basic'
    END AS TierLabel
FROM Customers;
```

---

## 20-21. PERCENT_CONT / PERCENT_DISC

### Function Names
**PERCENT_CONT** | **PERCENT_DISC**

### Description
- **PERCENT_CONT**: Interpolates continuous values for percentiles
- **PERCENT_DISC**: Returns discrete percentile values

### Syntax
```sql
PERCENT_CONT(percentile) WITHIN GROUP (ORDER BY sort_column)
PERCENT_DISC(percentile) WITHIN GROUP (ORDER BY sort_column)
```

### Code Examples

**Example 1: Median with PERCENT_CONT**
```sql
SELECT 
    Department,
    PERCENT_CONT(0.5) WITHIN GROUP (ORDER BY Salary) AS MedianSalary
FROM Employee
GROUP BY Department;
```

**Example 2: Quartile Analysis**
```sql
SELECT 
    PERCENT_DISC(0.25) WITHIN GROUP (ORDER BY Price) AS Q1,
    PERCENT_DISC(0.50) WITHIN GROUP (ORDER BY Price) AS Q2,
    PERCENT_DISC(0.75) WITHIN GROUP (ORDER BY Price) AS Q3
FROM Products;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
