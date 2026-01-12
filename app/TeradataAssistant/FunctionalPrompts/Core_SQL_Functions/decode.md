# DECODE

**Function Name:** DECODE

**Description:** Compares an expression to a series of values and returns a corresponding result.

**When to Use:**
- Simple conditional logic
- Code translation
- Status mapping
- Value replacement
- Simplified CASE statements

**Syntax:**
```sql
DECODE(expression, search_value1, result1, [search_value2, result2, ...] [, default_result])
```

**Examples:**

**Example 1 - Status Translation**
```sql
SELECT 
    OrderID,
    Status,
    DECODE(Status, 
        'P', 'Pending',
        'S', 'Shipped',
        'D', 'Delivered',
        'C', 'Cancelled',
        'Unknown'
    ) AS StatusDescription
FROM Orders;
```

**Example 2 - Department Code**
```sql
SELECT 
    EmployeeID,
    DeptCode,
    DECODE(DeptCode,
        'A', 'Administration',
        'S', 'Sales',
        'M', 'Marketing',
        'T', 'Technology',
        'Finance'
    ) AS DepartmentName
FROM Employees;
```

**Example 3 - Product Category**
```sql
SELECT 
    ProductID,
    CategoryCode,
    DECODE(CategoryCode,
        '1', 'Electronics',
        '2', 'Clothing',
        '3', 'Food',
        '4', 'Books',
        'Other'
    ) AS CategoryName
FROM Products;
```

**Example 4 - Priority Level**
```sql
SELECT 
    TicketID,
    PriorityCode,
    DECODE(PriorityCode,
        '1', 'Critical',
        '2', 'High',
        '3', 'Medium',
        '4', 'Low',
        'Unknown'
    ) AS Priority
FROM SupportTickets;
```

**Example 5 - Gender Translation**
```sql
SELECT 
    PersonID,
    Gender,
    DECODE(Gender,
        'M', 'Male',
        'F', 'Female',
        'O', 'Other',
        'Not Specified'
    ) AS GenderDescription
FROM People;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
