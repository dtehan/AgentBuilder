# CEIL / CEILING

**Function Name:** CEIL | CEILING

**Description:** Returns the smallest integer greater than or equal to a numeric expression. Rounds up to the nearest integer.

**When to Use:**
- Round up measurements
- Calculate resource requirements
- Convert decimals to whole units
- Planning and forecasting
- Rounding up financial calculations

**Syntax:**
```sql
CEIL(numeric_expression)  or  CEILING(numeric_expression)
```

**Examples:**

**Example 1 - Basic Ceiling**
```sql
SELECT CEIL(3.2) AS CeiledValue;   -- Returns: 4
SELECT CEIL(5.0) AS CeiledValue;   -- Returns: 5
```

**Example 2 - Quantity Calculation**
```sql
SELECT 
    OrderID,
    TotalWeight,
    CEIL(TotalWeight / 50) AS BoxesNeeded
FROM Orders;
```

**Example 3 - Resource Planning**
```sql
SELECT 
    ProjectID,
    EstimatedHours,
    CEIL(EstimatedHours / 8) AS DaysNeeded
FROM ProjectPlanning;
```

**Example 4 - Pricing Calculation**
```sql
SELECT 
    ProductID,
    CostPerUnit,
    CEIL(CostPerUnit * 1.3) AS MinimumPrice
FROM Products;
```

**Example 5 - Batch Processing**
```sql
SELECT 
    ItemCount,
    CEIL(ItemCount / 100.0) AS BatchesRequired
FROM DataProcessing;
```

**Example 6 - Space Allocation**
```sql
SELECT 
    FileSize,
    CEIL(FileSize / 1024.0) AS KBytesAllocated
FROM FileStorage;
```

**Example 7 - Shipping Calculation**
```sql
SELECT 
    OrderID,
    ShippingWeight,
    CEIL(ShippingWeight / 0.5) AS ShippingUnits
FROM Shipments;
```

**Example 8 - Time Rounding**
```sql
SELECT 
    EventID,
    DurationMinutes,
    CEIL(DurationMinutes / 15.0) AS TimeSlots
FROM EventSchedule;
```

**Example 9 - Financial Rounding**
```sql
SELECT 
    InvoiceID,
    Amount,
    CEIL(Amount * 100) / 100 AS RoundedAmount
FROM Invoices;
```

**Example 10 - Capacity Planning**
```sql
SELECT 
    WarehouseID,
    TotalBoxes,
    CEIL(TotalBoxes / 1000.0) AS PalletCount
FROM WarehouseInventory;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
