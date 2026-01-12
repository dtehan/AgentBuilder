# SUM

### Function Name
**SUM**

### Description
Returns a column value that is the arithmetic sum of value_expression. Valid only for numeric data. Nulls are not included in the result computation. Returns the data type of the input expression.

### When the Function Would Be Used
- Calculate total sales revenue
- Sum employee salaries by department
- Total order amounts for customers
- Accumulate inventory quantities
- Calculate total expenses by category
- Sum budget allocations
- Total transaction amounts

### Syntax
```sql
SUM ( [ DISTINCT | ALL ] value_expression )
```

### Code Examples

**Example 1: Basic Sum Calculation**
```sql
SELECT SUM(Salary) AS TotalSalaries
FROM Employee;
```

**Example 2: Sum with GROUP BY**
```sql
SELECT 
    Department,
    SUM(Salary) AS DeptTotalSalary
FROM Employee
GROUP BY Department;
```

**Example 3: Sum with WHERE**
```sql
SELECT SUM(OrderAmount) AS TotalOrderAmount
FROM Orders
WHERE OrderDate >= '2024-01-01';
```

**Example 4: Sum with DISTINCT**
```sql
SELECT SUM(DISTINCT Price) AS UniqueProductSum
FROM Products;
```

**Example 5: Multiple Sums**
```sql
SELECT 
    SUM(Salary) AS TotalSalary,
    SUM(Bonus) AS TotalBonus,
    SUM(Commission) AS TotalCommission
FROM Employee;
```

**Example 6: Sum with CAST**
```sql
SELECT 
    Department,
    CAST(SUM(Revenue) AS DECIMAL(15,2)) AS DeptRevenue
FROM SalesData
GROUP BY Department;
```

**Example 7: Sum with HAVING**
```sql
SELECT 
    Customer,
    SUM(OrderAmount) AS CustomerTotal
FROM Orders
GROUP BY Customer
HAVING SUM(OrderAmount) > 50000;
```

**Example 8: Running Total with Window Function**
```sql
SELECT 
    OrderDate,
    OrderAmount,
    SUM(OrderAmount) OVER (ORDER BY OrderDate) AS RunningTotal
FROM Orders;
```

**Example 9: Sum with Date Grouping**
```sql
SELECT 
    YEAR(OrderDate) AS Year,
    MONTH(OrderDate) AS Month,
    SUM(OrderAmount) AS MonthlyTotal
FROM Orders
GROUP BY YEAR(OrderDate), MONTH(OrderDate)
ORDER BY Year, Month;
```

**Example 10: Sum with Multiple Dimensions**
```sql
SELECT 
    Region,
    ProductCategory,
    SUM(Revenue) AS CategoryRevenue
FROM Sales
GROUP BY Region, ProductCategory
ORDER BY Region, CategoryRevenue DESC;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
