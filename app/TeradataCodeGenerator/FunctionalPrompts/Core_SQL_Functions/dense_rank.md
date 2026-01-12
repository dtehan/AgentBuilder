# DENSE_RANK

### Function Name
**DENSE_RANK**

### Description
Returns the dense rank of each row within a partition. Similar to RANK, but with no gaps in the ranking sequence. If two rows tie for rank 1, the next rank is 2 (not 3).

### When the Function Would Be Used
- Rank without gaps in sequence
- Create compact ranking lists
- Identify performance tiers
- Group items into ranking levels
- Create ranking categories
- Continuous ranking without skipping
- Performance tier analysis

### Syntax
```sql
DENSE_RANK() OVER (
    [ PARTITION BY partition_column(s) ]
    ORDER BY sort_column(s) [ ASC | DESC ]
)
```

### Code Examples

**Example 1: Dense Rank without Gaps**
```sql
SELECT 
    EmployeeName,
    Salary,
    DENSE_RANK() OVER (ORDER BY Salary DESC) AS SalaryRank
FROM Employee;
```

**Example 2: Compare RANK vs DENSE_RANK**
```sql
SELECT 
    EmployeeName,
    Salary,
    RANK() OVER (ORDER BY Salary DESC) AS StandardRank,
    DENSE_RANK() OVER (ORDER BY Salary DESC) AS DenseRank
FROM Employee;
```

**Example 3: Performance Tier Assignment**
```sql
SELECT 
    EmployeeID,
    PerformanceScore,
    DENSE_RANK() OVER (ORDER BY PerformanceScore DESC) AS TierLevel
FROM EmployeeReview;
```

**Example 4: Sales Category Ranking**
```sql
SELECT 
    ProductID,
    ProductName,
    MonthlySales,
    DENSE_RANK() OVER (ORDER BY MonthlySales DESC) AS SalesRank
FROM ProductPerformance;
```

**Example 5: Grade Distribution**
```sql
SELECT 
    StudentID,
    StudentName,
    GPA,
    DENSE_RANK() OVER (ORDER BY GPA DESC) AS GPARank
FROM StudentGPA;
```

**Example 6: Partition with Dense Rank**
```sql
SELECT 
    Department,
    EmployeeName,
    Salary,
    DENSE_RANK() OVER (PARTITION BY Department ORDER BY Salary DESC) AS DeptRank
FROM Employee;
```

**Example 7: Customer Value Tier**
```sql
SELECT 
    CustomerID,
    LifetimeValue,
    DENSE_RANK() OVER (ORDER BY LifetimeValue DESC) AS ValueTier
FROM Customers;
```

**Example 8: Product Quality Ranking**
```sql
SELECT 
    ProductID,
    QualityScore,
    DENSE_RANK() OVER (ORDER BY QualityScore DESC) AS QualityRank
FROM ProductQuality;
```

**Example 9: Continuous Ranking by Category**
```sql
SELECT 
    Category,
    ItemName,
    Rating,
    DENSE_RANK() OVER (PARTITION BY Category ORDER BY Rating DESC) AS CategoryRank
FROM Items;
```

**Example 10: Identify Ranking Brackets**
```sql
SELECT 
    EmployeeID,
    Salary,
    DENSE_RANK() OVER (ORDER BY Salary DESC) AS RankBracket
FROM Employee
WHERE DENSE_RANK() OVER (ORDER BY Salary DESC) <= 5;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
