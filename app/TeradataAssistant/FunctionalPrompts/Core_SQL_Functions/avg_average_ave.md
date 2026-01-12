# AVG (AVERAGE, AVE)

### Function Name
**AVG** | **AVERAGE** | **AVE**

### Description
Returns the arithmetic average of all values in value_expression. AVG is valid only for numeric data. Nulls are not included in the result computation. This function returns the REAL data type.

### When the Function Would Be Used
- Calculate average sales by region
- Determine average employee salary
- Find mean values in numeric datasets
- Compute average performance metrics
- Analyze average transaction amounts
- Calculate average time spent on activities
- Determine average pricing across products

### Syntax
```sql
{ AVERAGE | AVG | AVE } ( [ DISTINCT | ALL ] value_expression )
```

### Code Examples

**Example 1: Basic Average Calculation**
```sql
SELECT AVG(Salary) AS AvgSalary
FROM Employee;
```

**Example 2: Average with GROUP BY**
```sql
SELECT Region, AVG(sales) AS AvgSales
FROM sales_tbl
GROUP BY Region
ORDER BY Region;
```

**Example 3: Average with DISTINCT**
```sql
SELECT AVG(DISTINCT Price) AS AvgUniquePrice
FROM Products;
```

**Example 4: Average with WHERE Clause**
```sql
SELECT Department, AVG(salary) AS AvgDeptSalary
FROM Employee
WHERE salary > 30000
GROUP BY Department;
```

**Example 5: Average with Date Filtering**
```sql
SELECT AVG(OrderAmount) AS AvgMonthlyOrder
FROM Orders
WHERE OrderDate BETWEEN '2024-01-01' AND '2024-01-31';
```

**Example 6: Average with Multiple Aggregates**
```sql
SELECT 
    Department,
    COUNT(*) AS EmployeeCount,
    AVG(Salary) AS AvgSalary,
    MAX(Salary) AS MaxSalary
FROM Employee
GROUP BY Department;
```

**Example 7: Average with CAST for Decimal Results**
```sql
SELECT CAST(AVG(Price) AS DECIMAL(9,2)) AS AvgPrice
FROM Products;
```

**Example 8: Average with HAVING Clause**
```sql
SELECT Department, AVG(Salary) AS AvgSalary
FROM Employee
GROUP BY Department
HAVING AVG(Salary) > 50000;
```

**Example 9: Average with Subquery**
```sql
SELECT 
    (SELECT AVG(Salary) FROM Employee WHERE Department = 'Sales') AS SalesAvgSalary,
    (SELECT AVG(Salary) FROM Employee WHERE Department = 'IT') AS ITAvgSalary;
```

**Example 10: Average with Window Function**
```sql
SELECT 
    Department,
    EmployeeName,
    Salary,
    AVG(Salary) OVER (PARTITION BY Department) AS DeptAvgSalary
FROM Employee;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
