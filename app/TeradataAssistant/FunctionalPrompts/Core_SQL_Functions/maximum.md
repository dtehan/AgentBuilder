# MAXIMUM

### Function Name
**MAXIMUM** | **MAX**

### Description
Returns a column value that is the maximum value for value_expression. Can be used with DISTINCT to find the maximum of unique values only. Works with any comparable data type.

### When the Function Would Be Used
- Find the highest salary in a department
- Identify the maximum sales amount
- Determine the latest date in a dataset
- Find the largest transaction amount
- Locate peak performance metrics
- Identify maximum stock prices
- Find the most expensive product

### Syntax
```sql
{ MAXIMUM | MAX } ( [ DISTINCT | ALL ] value_expression )
```

### Code Examples

**Example 1: Basic Maximum Value**
```sql
SELECT MAX(Salary) AS HighestSalary
FROM Employee;
```

**Example 2: Maximum with GROUP BY**
```sql
SELECT 
    Department,
    MAX(Salary) AS DeptMaxSalary
FROM Employee
GROUP BY Department;
```

**Example 3: Maximum with WHERE**
```sql
SELECT MAX(Price) AS MaxProductPrice
FROM Products
WHERE Category = 'Electronics';
```

**Example 4: Maximum with DISTINCT**
```sql
SELECT MAX(DISTINCT Price) AS MaxUniquePrice
FROM ProductCatalog;
```

**Example 5: Maximum Date**
```sql
SELECT MAX(OrderDate) AS MostRecentOrder
FROM Orders;
```

**Example 6: Multiple Maximums**
```sql
SELECT 
    MAX(Salary) AS MaxSalary,
    MAX(Bonus) AS MaxBonus,
    MAX(Commission) AS MaxCommission
FROM SalesEmployee;
```

**Example 7: Maximum with HAVING**
```sql
SELECT 
    Region,
    MAX(Sales) AS RegionMaxSales
FROM RegionalSales
GROUP BY Region
HAVING MAX(Sales) > 100000;
```

**Example 8: Maximum with ORDER BY**
```sql
SELECT 
    ProductLine,
    MAX(UnitPrice) AS MaxUnitPrice
FROM ProductInventory
GROUP BY ProductLine
ORDER BY MaxUnitPrice DESC;
```

**Example 9: Maximum with Subquery**
```sql
SELECT 
    EmployeeName,
    Salary
FROM Employee
WHERE Salary = (SELECT MAX(Salary) FROM Employee);
```

**Example 10: Maximum with Window Function**
```sql
SELECT 
    Department,
    EmployeeName,
    Salary,
    MAX(Salary) OVER (PARTITION BY Department) AS DeptMaxSalary
FROM Employee;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
