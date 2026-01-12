# CURRENT_DATE / DATE()

**Function Name:** CURRENT_DATE | DATE()

**Description:** Returns the current date in the system.

**When to Use:**
- Get today's date for reports
- Calculate age or tenure
- Set default dates
- Filter current period data
- Calculate date differences

**Syntax:**
```sql
CURRENT_DATE  or  DATE()
```

**Examples:**

**Example 1 - Get Current Date**
```sql
SELECT CURRENT_DATE AS TodaysDate;
```

**Example 2 - Today's Data**
```sql
SELECT 
    OrderID,
    OrderDate,
    Amount
FROM Orders
WHERE OrderDate = CURRENT_DATE;
```

**Example 3 - Recent Data**
```sql
SELECT 
    TransactionID,
    TransactionDate,
    Amount
FROM Transactions
WHERE TransactionDate >= CURRENT_DATE - 30;
```

**Example 4 - Date Comparison**
```sql
SELECT 
    InvoiceID,
    InvoiceDate,
    DueDate,
    CASE 
        WHEN DueDate < CURRENT_DATE THEN 'Overdue'
        WHEN DueDate = CURRENT_DATE THEN 'Due Today'
        ELSE 'Not Yet Due'
    END AS Status
FROM Invoices;
```

**Example 5 - Calculate Age**
```sql
SELECT 
    EmployeeID,
    BirthDate,
    CURRENT_DATE - BirthDate AS AgeInDays,
    (CURRENT_DATE - BirthDate) / 365 AS AgeInYears
FROM Employees;
```

**Example 6 - Tenure Calculation**
```sql
SELECT 
    EmployeeID,
    HireDate,
    CURRENT_DATE - HireDate AS TenureInDays
FROM Employees;
```

**Example 7 - Set Default Date**
```sql
INSERT INTO AuditLog
VALUES (RecordID, CURRENT_DATE, 'Created');
```

**Example 8 - Date Range**
```sql
SELECT 
    SalesID,
    SalesDate,
    Amount
FROM Sales
WHERE SalesDate BETWEEN CURRENT_DATE - 7 AND CURRENT_DATE;
```

**Example 9 - This Year**
```sql
SELECT 
    EventID,
    EventDate
FROM Events
WHERE YEAR(EventDate) = YEAR(CURRENT_DATE);
```

**Example 10 - Compare Periods**
```sql
SELECT 
    TransactionDate,
    SUM(Amount) AS DailyTotal
FROM Transactions
WHERE TransactionDate >= CURRENT_DATE - 90
GROUP BY TransactionDate
ORDER BY TransactionDate DESC;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
