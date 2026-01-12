# ABS

**Function Name:** ABS

**Description:** Returns the absolute value (non-negative) of a numeric expression. Removes the negative sign if present.

**When to Use:**
- Calculate distance or magnitude
- Find absolute differences
- Remove negative signs for calculations
- Validate data ranges
- Calculate absolute changes

**Syntax:**
```sql
ABS(numeric_expression)
```

**Examples:**

**Example 1 - Basic Absolute Value**
```sql
SELECT ABS(-100) AS AbsoluteValue;  -- Returns: 100
SELECT ABS(75) AS AbsoluteValue;    -- Returns: 75
```

**Example 2 - Column Operation**
```sql
SELECT 
    EmployeeID,
    Salary,
    ABS(Salary - AvgSalary) AS DifferencFromAvg
FROM EmployeeData;
```

**Example 3 - Finding Biggest Differences**
```sql
SELECT 
    Product,
    CurrentPrice,
    PreviousPrice,
    ABS(CurrentPrice - PreviousPrice) AS PriceChange
FROM ProductHistory
ORDER BY PriceChange DESC;
```

**Example 4 - Variance Analysis**
```sql
SELECT 
    Department,
    ActualExpense,
    BudgetedExpense,
    ABS(ActualExpense - BudgetedExpense) AS Variance
FROM BudgetAnalysis
WHERE ABS(ActualExpense - BudgetedExpense) > 1000;
```

**Example 5 - Scientific Calculations**
```sql
SELECT 
    MeasurementID,
    ExpectedValue,
    ObservedValue,
    ABS(ExpectedValue - ObservedValue) AS Error
FROM ExperimentalData;
```

**Example 6 - Financial Calculations**
```sql
SELECT 
    TransactionID,
    Amount,
    ABS(Amount) AS AbsoluteAmount
FROM Transactions;
```

**Example 7 - Quality Control**
```sql
SELECT 
    LotNumber,
    TargetDimension,
    ActualDimension,
    ABS(TargetDimension - ActualDimension) AS Deviation
FROM ManufacturingQC
WHERE ABS(TargetDimension - ActualDimension) > 0.5;
```

**Example 8 - Statistical Analysis**
```sql
SELECT 
    ABS(Value1 - Value2) AS Distance
FROM DataPoints
ORDER BY Distance;
```

**Example 9 - Threshold Detection**
```sql
SELECT 
    SensorID,
    Reading,
    BaselineReading,
    ABS(Reading - BaselineReading) AS Deviation
FROM SensorData
HAVING ABS(Reading - BaselineReading) > 10;
```

**Example 10 - Reconciliation**
```sql
SELECT 
    BatchID,
    BookValue,
    PhysicalValue,
    ABS(BookValue - PhysicalValue) AS Discrepancy
FROM InventoryReconciliation
WHERE ABS(BookValue - PhysicalValue) > 0;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
