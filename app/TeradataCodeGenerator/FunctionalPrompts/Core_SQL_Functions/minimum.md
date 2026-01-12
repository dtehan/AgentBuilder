# MINIMUM

### Function Name
**MINIMUM** | **MIN**

### Description
Returns a column value that is the minimum value for value_expression. Can be used with DISTINCT to find the minimum of unique values only. Works with any comparable data type.

### When the Function Would Be Used
- Find the lowest salary in a department
- Identify the minimum sales amount
- Determine the earliest date in a dataset
- Find the smallest transaction amount
- Locate the lowest performance metrics
- Identify minimum stock prices
- Find the least expensive product

### Syntax
```sql
{ MINIMUM | MIN } ( [ DISTINCT | ALL ] value_expression )
```

### Code Examples

**Example 1: Basic Minimum Value**
```sql
SELECT MIN(Salary) AS LowestSalary
FROM Employee;
```

**Example 2: Minimum with GROUP BY**
```sql
SELECT 
    Department,
    MIN(Salary) AS DeptMinSalary
FROM Employee
GROUP BY Department;
```

**Example 3: Minimum with WHERE**
```sql
SELECT MIN(Price) AS MinProductPrice
FROM Products
WHERE Category = 'Electronics';
```

**Example 4: Minimum with DISTINCT**
```sql
SELECT MIN(DISTINCT Price) AS MinUniquePrice
FROM ProductCatalog;
```

**Example 5: Minimum Date**
```sql
SELECT MIN(HireDate) AS EarliestHireDate
FROM Employee;
```

**Example 6: Multiple Minimums**
```sql
SELECT 
    MIN(Salary) AS MinSalary,
    MIN(Bonus) AS MinBonus,
    MIN(Commission) AS MinCommission
FROM SalesEmployee;
```

**Example 7: Minimum with HAVING**
```sql
SELECT 
    Region,
    MIN(Sales) AS RegionMinSales
FROM RegionalSales
GROUP BY Region
HAVING MIN(Sales) > 10000;
```

**Example 8: Minimum with ORDER BY**
```sql
SELECT 
    ProductLine,
    MIN(UnitPrice) AS MinUnitPrice
FROM ProductInventory
GROUP BY ProductLine
ORDER BY MinUnitPrice ASC;
```

**Example 9: Minimum with Subquery**
```sql
SELECT 
    EmployeeName,
    Salary
FROM Employee
WHERE Salary = (SELECT MIN(Salary) FROM Employee);
```

**Example 10: Minimum with Window Function**
```sql
SELECT 
    Department,
    EmployeeName,
    Salary,
    MIN(Salary) OVER (PARTITION BY Department) AS DeptMinSalary
FROM Employee;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
