# ROW_NUMBER

### Function Name
**ROW_NUMBER**

### Description
Returns a unique sequential integer for each row within a partition of a result set, starting at 1 for the first row in each partition. ROW_NUMBER is useful for creating sequential numbering, identifying the Nth occurrence, or selecting the top N records per group.

### When the Function Would Be Used
- Assign unique sequential numbers to rows
- Select top N records within each group
- Create row identifiers for deduplication
- Rank items sequentially within categories
- Assign row identifiers for further processing
- Create unique IDs within partitions
- Select first/last N records per group

### Syntax
```sql
ROW_NUMBER() OVER (
    [ PARTITION BY partition_column(s) ]
    ORDER BY sort_column(s) [ ASC | DESC ]
)
```

### Code Examples

**Example 1: Basic Row Numbering**
```sql
SELECT 
    EmployeeID,
    EmployeeName,
    Salary,
    ROW_NUMBER() OVER (ORDER BY Salary DESC) AS SalaryRank
FROM Employee
ORDER BY SalaryRank;
```

**Example 2: Row Number by Department**
```sql
SELECT 
    Department,
    EmployeeID,
    EmployeeName,
    Salary,
    ROW_NUMBER() OVER (PARTITION BY Department ORDER BY Salary DESC) AS DeptRank
FROM Employee
ORDER BY Department, DeptRank;
```

**Example 3: Select Top 5 per Department**
```sql
SELECT 
    Department,
    EmployeeID,
    EmployeeName,
    Salary
FROM (
    SELECT 
        Department,
        EmployeeID,
        EmployeeName,
        Salary,
        ROW_NUMBER() OVER (PARTITION BY Department ORDER BY Salary DESC) AS RN
    FROM Employee
)
WHERE RN <= 5;
```

**Example 4: Remove Duplicates**
```sql
SELECT 
    CustomerID,
    Email,
    PhoneNumber
FROM (
    SELECT 
        CustomerID,
        Email,
        PhoneNumber,
        ROW_NUMBER() OVER (PARTITION BY Email ORDER BY CustomerID) AS RN
    FROM Customers
)
WHERE RN = 1;
```

**Example 5: Sequential Assignment**
```sql
SELECT 
    OrderID,
    OrderDate,
    Amount,
    ROW_NUMBER() OVER (ORDER BY OrderDate) AS SequenceNumber
FROM Orders;
```

**Example 6: Split Data into Batches**
```sql
SELECT 
    RecordID,
    Data,
    CEIL(ROW_NUMBER() OVER (ORDER BY RecordID) / 1000.0) AS BatchNumber
FROM LargeDataset;
```

**Example 7: Multiple Partitions**
```sql
SELECT 
    Region,
    Store,
    Sales,
    ROW_NUMBER() OVER (PARTITION BY Region, Store ORDER BY Sales DESC) AS StoreRank
FROM StoreSales;
```

**Example 8: Date-based Sequencing**
```sql
SELECT 
    CustomerID,
    OrderDate,
    Amount,
    ROW_NUMBER() OVER (PARTITION BY CustomerID ORDER BY OrderDate) AS OrderSequence
FROM Orders;
```

**Example 9: Page Number Assignment**
```sql
SELECT 
    RecordID,
    RecordValue,
    CEIL(ROW_NUMBER() OVER (ORDER BY RecordID) / 100.0) AS PageNumber
FROM Records;
```

**Example 10: Find Nth Occurrence**
```sql
SELECT 
    TransactionID,
    AccountID,
    Amount,
    TransactionDate
FROM (
    SELECT 
        TransactionID,
        AccountID,
        Amount,
        TransactionDate,
        ROW_NUMBER() OVER (PARTITION BY AccountID ORDER BY TransactionDate DESC) AS RN
    FROM Transactions
)
WHERE RN = 3;  -- Third most recent transaction
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
