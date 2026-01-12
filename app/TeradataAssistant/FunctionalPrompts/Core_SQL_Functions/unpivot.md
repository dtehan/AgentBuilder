# UNPIVOT

### Function Name
**UNPIVOT**

### Description
UNPIVOT is the inverse of PIVOT. It transforms data from columns into rows, converting wide-format data to long-format data. Each column value becomes a row with an associated value.

### When the Function Would Be Used
- Convert quarterly columns to rows
- Transform region columns into separate rows
- Convert monthly data columns to row format
- Normalize wide-format data
- Prepare data for time series analysis
- Restructure data for data warehouse loading
- Convert transposed data back to normal form

### Syntax
```sql
SELECT ...
FROM table_name
UNPIVOT (
    value_column
    FOR column_name IN (column_list)
);
```

### Code Examples

**Example 1: Basic UNPIVOT with Quarters**
```sql
SELECT 
    Product,
    Quarter,
    Sales
FROM (
    SELECT Product, Q1, Q2, Q3, Q4
    FROM QuarterlySalesWide
)
UNPIVOT (
    Sales FOR Quarter IN (Q1, Q2, Q3, Q4)
);
```

**Example 2: UNPIVOT Monthly Data**
```sql
SELECT 
    ProductID,
    Month,
    SalesAmount
FROM (
    SELECT ProductID, Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec
    FROM MonthlySalesWide
)
UNPIVOT (
    SalesAmount FOR Month IN (Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec)
);
```

**Example 3: UNPIVOT Regional Data**
```sql
SELECT 
    Product,
    Region,
    Revenue
FROM (
    SELECT Product, North, South, East, West
    FROM RegionalRevenueWide
)
UNPIVOT (
    Revenue FOR Region IN (North, South, East, West)
);
```

**Example 4: UNPIVOT with Multiple Value Columns**
```sql
SELECT 
    Customer,
    Year,
    Revenue,
    OrderCount
FROM (
    SELECT 
        Customer, 
        Revenue_2022, Revenue_2023, Revenue_2024,
        Orders_2022, Orders_2023, Orders_2024
    FROM CustomerMetricsWide
)
UNPIVOT (
    (Revenue, OrderCount)
    FOR Year IN (
        (Revenue_2022, Orders_2022) AS 2022,
        (Revenue_2023, Orders_2023) AS 2023,
        (Revenue_2024, Orders_2024) AS 2024
    )
);
```

**Example 5: UNPIVOT with Benefit Types**
```sql
SELECT 
    EmployeeID,
    BenefitType,
    BenefitAmount
FROM (
    SELECT EmployeeID, BasicHealth, Dental, Vision, Life
    FROM EmployeeBenefitsWide
)
UNPIVOT (
    BenefitAmount FOR BenefitType IN (BasicHealth, Dental, Vision, Life)
);
```

**Example 6: UNPIVOT with Filtered Results**
```sql
SELECT 
    EmployeeID,
    BenefitType,
    Amount
FROM (
    SELECT EmployeeID, Premium, Basic, Standard, Economy
    FROM PlanOptionsWide
)
UNPIVOT (
    Amount FOR BenefitType IN (Premium, Basic, Standard, Economy)
)
WHERE Amount > 0;
```

**Example 7: UNPIVOT Converting Scores to Rows**
```sql
SELECT 
    StudentID,
    Subject,
    Score
FROM (
    SELECT StudentID, Math, English, Science, History
    FROM StudentScoresWide
)
UNPIVOT (
    Score FOR Subject IN (Math, English, Science, History)
)
ORDER BY StudentID, Subject;
```

**Example 8: UNPIVOT with Year Data**
```sql
SELECT 
    Department,
    Year,
    Budget
FROM (
    SELECT Department, Budget_2022, Budget_2023, Budget_2024
    FROM BudgetWide
)
UNPIVOT (
    Budget FOR Year IN (Budget_2022, Budget_2023, Budget_2024)
)
ORDER BY Department, Year;
```

**Example 9: UNPIVOT for Time Series**
```sql
SELECT 
    Store,
    Month,
    DailySales
FROM (
    SELECT Store, Mon_Avg, Tue_Avg, Wed_Avg, Thu_Avg, Fri_Avg, Sat_Avg, Sun_Avg
    FROM DailyAverageWide
)
UNPIVOT (
    DailySales FOR Month IN (Mon_Avg, Tue_Avg, Wed_Avg, Thu_Avg, Fri_Avg, Sat_Avg, Sun_Avg)
);
```

**Example 10: UNPIVOT with Named Columns**
```sql
SELECT 
    Category,
    MeasureType,
    MeasureValue
FROM (
    SELECT Category, Target_2024, Actual_2024, Variance_2024
    FROM PerformanceWide
)
UNPIVOT (
    MeasureValue FOR MeasureType IN (Target_2024, Actual_2024, Variance_2024)
);
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
