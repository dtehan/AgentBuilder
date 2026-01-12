# MOD

**Function Name:** MOD

**Description:** Returns the remainder after division of one number by another. Also known as the modulo operator.

**When to Use:**
- Calculate remainders
- Determine cycling patterns
- Find alternating patterns
- Distribute items evenly
- Validation checks

**Syntax:**
```sql
MOD(dividend, divisor)
```

**Examples:**

**Example 1 - Basic Modulo**
```sql
SELECT MOD(17, 5) AS Remainder;  -- Returns: 2
SELECT MOD(20, 3) AS Remainder;  -- Returns: 2
```

**Example 2 - Odd/Even Detection**
```sql
SELECT 
    Number,
    CASE WHEN MOD(Number, 2) = 0 THEN 'Even' ELSE 'Odd' END AS NumberType
FROM Numbers;
```

**Example 3 - Cycling Pattern**
```sql
SELECT 
    EventID,
    DayNumber,
    MOD(DayNumber, 7) AS DayOfWeek
FROM EventLog;
```

**Example 4 - Distribution**
```sql
SELECT 
    ItemID,
    ItemNumber,
    MOD(ItemNumber, 4) AS AssignedQueue
FROM ProcessingQueue;
```

**Example 5 - Data Partitioning**
```sql
SELECT 
    RecordID,
    MOD(RecordID, 10) AS Partition
FROM DataPartition;
```

**Example 6 - Shift Assignment**
```sql
SELECT 
    EmployeeID,
    EmployeeNumber,
    CASE MOD(EmployeeNumber, 3)
        WHEN 0 THEN 'Shift A'
        WHEN 1 THEN 'Shift B'
        ELSE 'Shift C'
    END AS AssignedShift
FROM Employees;
```

**Example 7 - Batch Processing**
```sql
SELECT 
    RecordID,
    CASE WHEN MOD(RecordID, 100) = 0 THEN 'Process' ELSE 'Skip' END AS Action
FROM LargeDataset;
```

**Example 8 - Validation**
```sql
SELECT 
    CheckNumber,
    Value,
    CASE WHEN MOD(CheckNumber, 2) = MOD(Value, 2) THEN 'Valid' ELSE 'Invalid' END AS Validation
FROM Checksums;
```

**Example 9 - Rotation Schedule**
```sql
SELECT 
    ScheduleID,
    WeekNumber,
    MOD(WeekNumber, 4) AS RotationWeek
FROM ScheduleRotation;
```

**Example 10 - Sampling**
```sql
SELECT 
    RecordID,
    Data
FROM SourceData
WHERE MOD(RecordID, 10) = 0;  -- Sample every 10th record
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
