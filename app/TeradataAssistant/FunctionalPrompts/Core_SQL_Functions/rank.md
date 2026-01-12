# RANK

### Function Name
**RANK**

### Description
Returns the rank of each row within a partition of a result set. Rows with equal values receive the same rank, and the next rank skips accordingly. For example, if two rows tie for rank 1, the next rank is 3.

### When the Function Would Be Used
- Rank items by performance metrics
- Identify tied rankings
- Create competition-style rankings
- Rank products by sales
- Rank employees by performance
- Identify top performers with ties
- Create tiered analysis

### Syntax
```sql
RANK() OVER (
    [ PARTITION BY partition_column(s) ]
    ORDER BY sort_column(s) [ ASC | DESC ]
)
```

### Code Examples

**Example 1: Basic Ranking**
```sql
SELECT 
    EmployeeName,
    Salary,
    RANK() OVER (ORDER BY Salary DESC) AS SalaryRank
FROM Employee;
```

**Example 2: Ranking with Ties**
```sql
SELECT 
    EmployeeName,
    Salary,
    RANK() OVER (ORDER BY Salary DESC) AS SalaryRank
FROM Employee
WHERE RANK() OVER (ORDER BY Salary DESC) <= 5;
```

**Example 3: Department-level Ranking**
```sql
SELECT 
    Department,
    EmployeeName,
    PerformanceScore,
    RANK() OVER (PARTITION BY Department ORDER BY PerformanceScore DESC) AS DeptRank
FROM EmployeeReview;
```

**Example 4: Sales Ranking**
```sql
SELECT 
    ProductName,
    Region,
    Sales,
    RANK() OVER (PARTITION BY Region ORDER BY Sales DESC) AS RegionalRank
FROM RegionalSales;
```

**Example 5: Find Top Tied Performers**
```sql
SELECT 
    EmployeeName,
    TestScore,
    RANK() OVER (ORDER BY TestScore DESC) AS ScoreRank
FROM TestResults
WHERE RANK() OVER (ORDER BY TestScore DESC) = 1;
```

**Example 6: Multiple Sort Criteria**
```sql
SELECT 
    StudentID,
    SubjectID,
    Grade,
    RANK() OVER (PARTITION BY SubjectID ORDER BY Grade DESC, StudentID) AS GradeRank
FROM StudentGrades;
```

**Example 7: Time-based Ranking**
```sql
SELECT 
    RacerID,
    RacerName,
    RaceTime,
    RANK() OVER (ORDER BY RaceTime ASC) AS TimeRank
FROM RaceResults;
```

**Example 8: Revenue Ranking**
```sql
SELECT 
    CustomerID,
    Revenue,
    RANK() OVER (ORDER BY Revenue DESC) AS RevenueRank
FROM CustomerRevenue;
```

**Example 9: Ranking with Partitions**
```sql
SELECT 
    Year,
    Month,
    Sales,
    RANK() OVER (PARTITION BY Year ORDER BY Sales DESC) AS MonthlyRank
FROM MonthlySales;
```

**Example 10: Competition Ranking**
```sql
SELECT 
    CompetitorName,
    Score,
    RANK() OVER (ORDER BY Score DESC) AS CompetitionRank
FROM Competition
WHERE RANK() OVER (ORDER BY Score DESC) <= 10;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
