# NTH_VALUE

### Function Name
**NTH_VALUE**

### Description
Returns the value from the Nth row within an ordered partition of rows. Useful for accessing specific positions in a sequence without knowing the exact order.

### Syntax
```sql
NTH_VALUE(expression, n) OVER (
    [ PARTITION BY partition_column(s) ]
    ORDER BY sort_column(s)
    [ frame_specification ]
)
```

### Code Examples

**Example 1: Get Third Highest**
```sql
SELECT 
    EmployeeID,
    Salary,
    NTH_VALUE(Salary, 3) OVER (ORDER BY Salary DESC) AS ThirdHighest
FROM Employee;
```

**Example 2: Top 3 Sales by Department**
```sql
SELECT 
    Department,
    EmployeeName,
    Sales,
    NTH_VALUE(Sales, 1) OVER (PARTITION BY Department ORDER BY Sales DESC) AS Top1,
    NTH_VALUE(Sales, 2) OVER (PARTITION BY Department ORDER BY Sales DESC) AS Top2,
    NTH_VALUE(Sales, 3) OVER (PARTITION BY Department ORDER BY Sales DESC) AS Top3
FROM SalesData;
```

**Example 3: Median Approximation**
```sql
SELECT 
    Category,
    Price,
    NTH_VALUE(Price, CEIL(COUNT(*) OVER (PARTITION BY Category) / 2.0)) OVER (PARTITION BY Category ORDER BY Price) AS MedianPrice
FROM Products;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
