# EXTRACT

**Function Name:** EXTRACT

**Description:** Extracts a specific part (year, month, day, hour, etc.) from a date or timestamp.

**When to Use:**
- Extract date components
- Group by time periods
- Create time hierarchies
- Filter by specific periods
- Generate reports by month/year

**Syntax:**
```sql
EXTRACT(datepart FROM date_expression)
```

**Examples:**

**Example 1 - Extract Year**
```sql
SELECT 
    OrderDate,
    EXTRACT(YEAR FROM OrderDate) AS OrderYear
FROM Orders;
```

**Example 2 - Extract Month**
```sql
SELECT 
    EXTRACT(MONTH FROM CURRENT_DATE) AS CurrentMonth;
```

**Example 3 - Group by Month**
```sql
SELECT 
    EXTRACT(YEAR FROM OrderDate) AS Year,
    EXTRACT(MONTH FROM OrderDate) AS Month,
    SUM(Amount) AS MonthlySales
FROM Orders
GROUP BY EXTRACT(YEAR FROM OrderDate), EXTRACT(MONTH FROM OrderDate);
```

**Example 4 - Extract Day of Week**
```sql
SELECT 
    OrderDate,
    EXTRACT(DAY_OF_WEEK FROM OrderDate) AS DayOfWeek
FROM Orders;
```

**Example 5 - Extract Hour**
```sql
SELECT 
    EventTime,
    EXTRACT(HOUR FROM EventTime) AS Hour
FROM EventLog;
```

**Example 6 - Quarter Analysis**
```sql
SELECT 
    EXTRACT(YEAR FROM SalesDate) AS Year,
    EXTRACT(QUARTER FROM SalesDate) AS Quarter,
    SUM(Sales) AS QuarterlySales
FROM SalesData
GROUP BY EXTRACT(YEAR FROM SalesDate), EXTRACT(QUARTER FROM SalesDate);
```

**Example 7 - Year-to-Date**
```sql
SELECT 
    SalesID,
    SalesDate,
    Amount
FROM Sales
WHERE EXTRACT(YEAR FROM SalesDate) = EXTRACT(YEAR FROM CURRENT_DATE);
```

**Example 8 - Fiscal Period**
```sql
SELECT 
    TransactionDate,
    Amount,
    CASE 
        WHEN EXTRACT(MONTH FROM TransactionDate) IN (1,2,3) THEN 'Q1'
        WHEN EXTRACT(MONTH FROM TransactionDate) IN (4,5,6) THEN 'Q2'
        WHEN EXTRACT(MONTH FROM TransactionDate) IN (7,8,9) THEN 'Q3'
        ELSE 'Q4'
    END AS FiscalQuarter
FROM Transactions;
```

**Example 9 - Filter by Day**
```sql
SELECT 
    EventID,
    EventTime
FROM Events
WHERE EXTRACT(DAY FROM EventTime) = 15;
```

**Example 10 - Monthly Comparison**
```sql
SELECT 
    EXTRACT(MONTH FROM OrderDate) AS Month,
    COUNT(*) AS OrderCount,
    SUM(Amount) AS TotalAmount
FROM Orders
WHERE EXTRACT(YEAR FROM OrderDate) = 2024
GROUP BY EXTRACT(MONTH FROM OrderDate);
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
