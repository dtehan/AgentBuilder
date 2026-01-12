# FLOOR

**Function Name:** FLOOR

**Description:** Returns the largest integer less than or equal to a numeric expression. Rounds down to the nearest integer.

**When to Use:**
- Round down for conservative estimates
- Calculate available capacity
- Floor division operations
- Data truncation
- Conservative financial calculations

**Syntax:**
```sql
FLOOR(numeric_expression)
```

**Examples:**

**Example 1 - Basic Floor**
```sql
SELECT FLOOR(3.9) AS FlooredValue;  -- Returns: 3
SELECT FLOOR(5.1) AS FlooredValue;  -- Returns: 5
```

**Example 2 - Available Capacity**
```sql
SELECT 
    WarehouseID,
    TotalCapacity,
    FLOOR(TotalCapacity / 50.0) AS MaxBoxes
FROM Warehouses;
```

**Example 3 - Conservative Budget**
```sql
SELECT 
    ProjectID,
    TotalBudget,
    FLOOR(TotalBudget * 0.8) AS SperableBudget
FROM Projects;
```

**Example 4 - Rating Calculation**
```sql
SELECT 
    ProductID,
    AverageScore,
    FLOOR(AverageScore) AS StarRating
FROM ProductReviews;
```

**Example 5 - Batch Count**
```sql
SELECT 
    ItemCount,
    FLOOR(ItemCount / 100) AS CompleteHundreds
FROM DataProcessing;
```

**Example 6 - Age Calculation**
```sql
SELECT 
    PersonID,
    BirthDate,
    FLOOR((CURRENT_DATE - BirthDate) / 365.25) AS Age
FROM People;
```

**Example 7 - Integer Division**
```sql
SELECT 
    Numerator,
    Denominator,
    FLOOR(Numerator / Denominator) AS QuotientInteger
FROM MathOperations;
```

**Example 8 - Performance Tier**
```sql
SELECT 
    EmployeeID,
    PerformanceScore,
    FLOOR(PerformanceScore / 10) AS TierLevel
FROM EmployeeReviews;
```

**Example 9 - Time Intervals**
```sql
SELECT 
    EventID,
    DurationSeconds,
    FLOOR(DurationSeconds / 60) AS MinutesElapsed
FROM EventLog;
```

**Example 10 - Inventory Levels**
```sql
SELECT 
    SKU,
    AvailableStock,
    FLOOR(AvailableStock / 5) AS SetCount
FROM Inventory;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
