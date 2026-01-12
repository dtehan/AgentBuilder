# LEAD

### Function Name
**LEAD**

### Description
Returns the value of an expression from a row at a specified physical offset AFTER the current row within the partition. The opposite of LAG. Useful for looking ahead to future values.

### When the Function Would Be Used
- Predict next values
- Compare current with future
- Find sequential patterns
- Identify upcoming changes
- Forecast trends
- Detect future anomalies
- Plan for future events

### Syntax
```sql
LEAD(expression [, offset [, default_value]]) OVER (
    [ PARTITION BY partition_column(s) ]
    ORDER BY sort_column(s)
)
```

### Code Examples

**Example 1: Next Value**
```sql
SELECT 
    Date,
    DailySales,
    LEAD(DailySales) OVER (ORDER BY Date) AS NextDaySales
FROM DailySalesData
ORDER BY Date;
```

**Example 2: Look Ahead 30 Days**
```sql
SELECT 
    Date,
    Sales,
    LEAD(Sales, 30) OVER (ORDER BY Date) AS Sales30DaysLater
FROM DailySales;
```

**Example 3: Detect Sequential Issues**
```sql
SELECT 
    OrderID,
    OrderDate,
    Status,
    LEAD(Status) OVER (PARTITION BY CustomerID ORDER BY OrderDate) AS NextStatus
FROM Orders;
```

**Example 4: Calculate Time Between Events**
```sql
SELECT 
    EventID,
    EventDate,
    EventType,
    LEAD(EventDate) OVER (PARTITION BY DeviceID ORDER BY EventDate) AS NextEventDate,
    LEAD(EventDate) OVER (PARTITION BY DeviceID ORDER BY EventDate) - EventDate AS DaysBetweenEvents
FROM DeviceEvents;
```

**Example 5: Price Prediction Analysis**
```sql
SELECT 
    Date,
    CurrentPrice,
    LEAD(CurrentPrice) OVER (ORDER BY Date) AS NextPrice,
    LEAD(CurrentPrice) OVER (ORDER BY Date) - CurrentPrice AS PriceDifference
FROM StockPrices;
```

**Example 6: Multi-step Lookahead**
```sql
SELECT 
    Month,
    Revenue,
    LEAD(Revenue, 1) OVER (ORDER BY Month) AS Next1Month,
    LEAD(Revenue, 2) OVER (ORDER BY Month) AS Next2Months,
    LEAD(Revenue, 3) OVER (ORDER BY Month) AS Next3Months
FROM MonthlyRevenue;
```

**Example 7: With Default for End Rows**
```sql
SELECT 
    Date,
    Value,
    LEAD(Value, 1, 0) OVER (ORDER BY Date) AS NextValue
FROM TimeSeries;
```

**Example 8: Identify Changes**
```sql
SELECT 
    Date,
    Status,
    LEAD(Status) OVER (ORDER BY Date) AS NextStatus,
    CASE 
        WHEN LEAD(Status) OVER (ORDER BY Date) <> Status THEN 'Change Expected'
        ELSE 'No Change'
    END AS StatusChange
FROM StatusHistory;
```

**Example 9: Calculate Expected Growth**
```sql
SELECT 
    Year,
    Revenue,
    LEAD(Revenue) OVER (ORDER BY Year) AS NextYearRevenue,
    CAST(100.0 * (LEAD(Revenue) OVER (ORDER BY Year) - Revenue) / Revenue AS DECIMAL(10,2)) AS ExpectedGrowthPercent
FROM AnnualRevenue;
```

**Example 10: Event Forecasting**
```sql
SELECT 
    Date,
    EventCount,
    LEAD(EventCount) OVER (ORDER BY Date) AS TomorrowCount,
    LEAD(EventCount, 7) OVER (ORDER BY Date) AS NextWeekCount
FROM DailyEvents;
```

---

## 16-17. FIRST_VALUE / LAST_VALUE

### Function Names
**FIRST_VALUE** | **LAST_VALUE**

### Description
- **FIRST_VALUE**: Returns the first value in an ordered set of rows
- **LAST_VALUE**: Returns the last value in an ordered set of rows

### When to Use
- Compare with first/last in group
- Calculate from baseline (first value)
- Find changes from start to end
- Identify first/last occurrence
- Track cumulative progress
- Performance comparison against baseline

### Syntax
```sql
FIRST_VALUE(expression) OVER (
    [ PARTITION BY partition_column(s) ]
    ORDER BY sort_column(s)
    [ frame_specification ]
)

LAST_VALUE(expression) OVER (
    [ PARTITION BY partition_column(s) ]
    ORDER BY sort_column(s)
    [ frame_specification ]
)
```

### Code Examples

**Example 1: First Order Date**
```sql
SELECT 
    CustomerID,
    OrderID,
    OrderDate,
    FIRST_VALUE(OrderDate) OVER (PARTITION BY CustomerID ORDER BY OrderDate) AS FirstOrderDate
FROM Orders;
```

**Example 2: Starting Price Comparison**
```sql
SELECT 
    Date,
    Price,
    FIRST_VALUE(Price) OVER (PARTITION BY StockID ORDER BY Date) AS StartingPrice,
    Price - FIRST_VALUE(Price) OVER (PARTITION BY StockID ORDER BY Date) AS PriceChange
FROM StockPrices;
```

**Example 3: Last Known Value**
```sql
SELECT 
    Date,
    Value,
    LAST_VALUE(Value) OVER (PARTITION BY SensorID ORDER BY Date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS LastValue
FROM SensorReadings;
```

**Example 4: Progress Tracking**
```sql
SELECT 
    ProjectID,
    MilestoneDate,
    Progress,
    FIRST_VALUE(Progress) OVER (PARTITION BY ProjectID ORDER BY MilestoneDate) AS StartingProgress,
    LAST_VALUE(Progress) OVER (PARTITION BY ProjectID ORDER BY MilestoneDate ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS FinalProgress
FROM ProjectMilestones;
```

**Example 5: Baseline Comparison**
```sql
SELECT 
    Year,
    Quarter,
    Revenue,
    FIRST_VALUE(Revenue) OVER (PARTITION BY Year ORDER BY Quarter) AS Q1Revenue,
    CAST(100.0 * (Revenue - FIRST_VALUE(Revenue) OVER (PARTITION BY Year ORDER BY Quarter)) / FIRST_VALUE(Revenue) OVER (PARTITION BY Year ORDER BY Quarter) AS DECIMAL(10,2)) AS PercentFromQ1
FROM QuarterlyRevenue;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
