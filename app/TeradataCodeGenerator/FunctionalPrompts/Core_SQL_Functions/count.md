# COUNT

### Function Name
**COUNT**

### Description
Returns a column value that is the total number of qualified rows in value_expression. COUNT can operate on any data type. COUNT(*) counts all rows including nulls, COUNT(column) counts non-null values, and COUNT(DISTINCT column) counts unique non-null values.

### When the Function Would Be Used
- Count total number of employees per department
- Determine number of distinct customers
- Find number of orders placed in a period
- Count non-null values in a column
- Determine number of unique products sold
- Count transactions by type
- Find number of rows matching criteria

### Syntax
```sql
COUNT ( { [ DISTINCT | ALL ] value_expression | * } )
```

### Code Examples

**Example 1: Count All Rows**
```sql
SELECT COUNT(*) AS TotalEmployees
FROM Employee;
```

**Example 2: Count by Department**
```sql
SELECT DeptNo, COUNT(*) AS EmployeeCount
FROM Employee
GROUP BY DeptNo
ORDER BY DeptNo;
```

**Example 3: Count Non-Null Values**
```sql
SELECT COUNT(DeptNo) AS DeptNoCount
FROM Employee;
```

**Example 4: Count with WHERE Clause**
```sql
SELECT COUNT(Gender)
FROM Employee
WHERE Gender = 'M';
```

**Example 5: Count Distinct Values**
```sql
SELECT COUNT(DISTINCT DeptNo) AS UniqueDepartments
FROM Employee;
```

**Example 6: Count with GROUP BY and WHERE**
```sql
SELECT DeptNo, COUNT(DeptNo) AS NonNullDeptCount
FROM Employee
WHERE HireDate > '2020-01-01'
GROUP BY DeptNo
ORDER BY DeptNo;
```

**Example 7: Multiple Count Functions**
```sql
SELECT 
    COUNT(*) AS TotalRows,
    COUNT(DeptNo) AS NonNullDeptNo,
    COUNT(DISTINCT DeptNo) AS DistinctDepts
FROM Employee;
```

**Example 8: Count by Multiple Grouping Columns**
```sql
SELECT 
    DeptNo,
    Gender,
    COUNT(*) AS EmployeeCount
FROM Employee
GROUP BY DeptNo, Gender
ORDER BY DeptNo, Gender;
```

**Example 9: Count with HAVING Clause**
```sql
SELECT 
    DeptNo,
    COUNT(*) AS DeptSize
FROM Employee
GROUP BY DeptNo
HAVING COUNT(*) > 5
ORDER BY DeptSize DESC;
```

**Example 10: Count in Join Operation**
```sql
SELECT 
    d.DeptName,
    COUNT(e.EmployeeID) AS EmployeeCount
FROM Department d
LEFT JOIN Employee e ON d.DeptNo = e.DeptNo
GROUP BY d.DeptName
ORDER BY EmployeeCount DESC;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
