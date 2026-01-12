# LAG

### Function Name
**LAG**

### Description
Returns the value of an expression from a row at a specified physical offset BEFORE the current row within the partition. Useful for comparing current values with previous values.

### When the Function Would Be Used
- Calculate period-over-period changes
- Compare current value with previous
- Detect sequential changes
- Calculate differences from previous period
- Analyze trends over time
- Find price changes
- Calculate daily/weekly/monthly changes

### Syntax
```sql
LAG(expression [, offset [, default_value]]) OVER (
    [ PARTITION BY partition_column(s) ]
    ORDER BY sort_column(s)
)
```

### Code Examples

**Example 1: Previous Value**
```sql
SELECT 
    Date,
    DailySales,
    LAG(DailySales) OVER (ORDER BY Date) AS PreviousDaySales,
    DailySales - LAG(DailySales) OVER (ORDER BY Date) AS DailyChange
FROM DailySalesData
ORDER BY Date;
```

**Example 2: Month-over-Month Change**
```sql
SELECT 
    Month,
    Revenue,
    LAG(Revenue, 1) OVER (ORDER BY Month) AS PreviousMonth,
    Revenue - LAG(Revenue, 1) OVER (ORDER BY Month) AS MonthlyCchange
FROM MonthlyRevenue;
```

**Example 3: Year-over-Year Comparison**
```sql
SELECT 
    Date,
    CurrentYearSales,
    LAG(CurrentYearSales, 365) OVER (ORDER BY Date) AS LastYearSales,
    CurrentYearSales - LAG(CurrentYearSales, 365) OVER (ORDER BY Date) AS YoYChange
FROM DailySales;
```

**Example 4: Price History**
```sql
SELECT 
    Date,
    ProductID,
    Price,
    LAG(Price) OVER (PARTITION BY ProductID ORDER BY Date) AS PreviousPrice,
    Price - LAG(Price) OVER (PARTITION BY ProductID ORDER BY Date) AS PriceChange
FROM ProductPriceHistory;
```

**Example 5: Student Score Tracking**
```sql
SELECT 
    StudentID,
    TestDate,
    TestScore,
    LAG(TestScore) OVER (PARTITION BY StudentID ORDER BY TestDate) AS PreviousScore,
    TestScore - LAG(TestScore) OVER (PARTITION BY StudentID ORDER BY TestDate) AS ScoreImprovement
FROM StudentTests;
```

**Example 6: With Default Value**
```sql
SELECT 
    TransactionID,
    TransactionDate,
    Amount,
    LAG(Amount, 1, 0) OVER (PARTITION BY AccountID ORDER BY TransactionDate) AS PreviousAmount
FROM Transactions;
```

**Example 7: Multiple Lags**
```sql
SELECT 
    Date,
    Sales,
    LAG(Sales, 1) OVER (ORDER BY Date) AS Lag1,
    LAG(Sales, 2) OVER (ORDER BY Date) AS Lag2,
    LAG(Sales, 3) OVER (ORDER BY Date) AS Lag3
FROM DailySales;
```

**Example 8: Calculate Percentage Change**
```sql
SELECT 
    Date,
    StockPrice,
    LAG(StockPrice) OVER (ORDER BY Date) AS PreviousPrice,
    CAST(100.0 * (StockPrice - LAG(StockPrice) OVER (ORDER BY Date)) / LAG(StockPrice) OVER (ORDER BY Date) AS DECIMAL(10,2)) AS PercentChange
FROM StockHistory;
```

**Example 9: Detect Anomalies**
```sql
SELECT 
    Date,
    Value,
    LAG(Value) OVER (ORDER BY Date) AS PreviousValue,
    ABS(Value - LAG(Value) OVER (ORDER BY Date)) AS ValueChange
FROM SensorData
WHERE ABS(Value - LAG(Value) OVER (ORDER BY Date)) > Threshold;
```

**Example 10: Trend Analysis**
```sql
SELECT 
    Month,
    Sales,
    LAG(Sales) OVER (ORDER BY Month) AS PreviousMonth,
    CASE 
        WHEN Sales > LAG(Sales) OVER (ORDER BY Month) THEN 'Increase'
        WHEN Sales < LAG(Sales) OVER (ORDER BY Month) THEN 'Decrease'
        ELSE 'No Change'
    END AS Trend
FROM MonthlySales;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
