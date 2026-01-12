# GREATEST / LEAST

**Function Name:** GREATEST | LEAST

**Description:** Returns the greatest or least value from a list of expressions.

**When to Use:**
- Find maximum/minimum from multiple columns
- Determine highest/lowest priority
- Compare multiple values
- Handle multiple conditions

**Syntax:**
```sql
GREATEST(expression1, expression2, ..., expressionN)
LEAST(expression1, expression2, ..., expressionN)
```

**Examples:**

**Example 1 - Greatest Value**
```sql
SELECT 
    EmployeeID,
    Salary,
    Bonus,
    Commission,
    GREATEST(Salary, Bonus, Commission) AS HighestAmount
FROM Employees;
```

**Example 2 - Latest Date**
```sql
SELECT 
    CustomerID,
    LastOrderDate,
    LastVisitDate,
    LastSupportDate,
    GREATEST(LastOrderDate, LastVisitDate, LastSupportDate) AS MostRecentActivity
FROM Customers;
```

**Example 3 - Lowest Price**
```sql
SELECT 
    ProductID,
    Supplier1Price,
    Supplier2Price,
    Supplier3Price,
    LEAST(Supplier1Price, Supplier2Price, Supplier3Price) AS LowestPrice
FROM Products;
```

**Example 4 - Earliest Date**
```sql
SELECT 
    EventID,
    ScheduledDate,
    PlannedDate,
    ActualDate,
    LEAST(ScheduledDate, PlannedDate, ActualDate) AS EarliestDate
FROM Events;
```

**Example 5 - Maximum Value**
```sql
SELECT 
    QuarterID,
    Q1_Sales,
    Q2_Sales,
    Q3_Sales,
    Q4_Sales,
    GREATEST(Q1_Sales, Q2_Sales, Q3_Sales, Q4_Sales) AS BestQuarter
FROM AnnualSales;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
