# PIVOT

### Function Name
**PIVOT**

### Description
PIVOT is a data restructuring operation that converts rows into columns. It aggregates data by specified columns and rotates the data from a row-based layout to a column-based layout.

### When the Function Would Be Used
- Convert monthly sales data to columns by month
- Transform sales by region into columns
- Restructure time series data
- Create cross-tabulation reports
- Convert categorical data to wide format
- Prepare data for analysis tools
- Create pivot table-like structures

### Syntax
```sql
SELECT ...
FROM table_name
PIVOT (
    aggregate_function(column)
    FOR pivot_column IN (value1, value2, ..., valueN)
);
```

### Code Examples

**Example 1: Basic PIVOT Converting Quarters to Columns**
```sql
SELECT 
    Product,
    [Q1], [Q2], [Q3], [Q4]
FROM (
    SELECT Product, Quarter, Sales
    FROM QuarterlySales
)
PIVOT (
    SUM(Sales)
    FOR Quarter IN ('Q1', 'Q2', 'Q3', 'Q4')
);
```

**Example 2: PIVOT with Region Data**
```sql
SELECT 
    Product,
    [North], [South], [East], [West]
FROM (
    SELECT Product, Region, Revenue
    FROM RegionalRevenue
)
PIVOT (
    SUM(Revenue)
    FOR Region IN ('North', 'South', 'East', 'West')
);
```

**Example 3: PIVOT with Monthly Sales**
```sql
SELECT 
    ProductID,
    [Jan], [Feb], [Mar], [Apr], [May], [Jun],
    [Jul], [Aug], [Sep], [Oct], [Nov], [Dec]
FROM (
    SELECT ProductID, MONTH(SalesDate) AS MonthNum, SalesAmount
    FROM MonthlySales
)
PIVOT (
    SUM(SalesAmount)
    FOR MonthNum IN (1,2,3,4,5,6,7,8,9,10,11,12)
);
```

**Example 4: PIVOT with Count Aggregation**
```sql
SELECT 
    Department,
    [M], [F], [Other]
FROM (
    SELECT Department, Gender, EmployeeID
    FROM Employee
)
PIVOT (
    COUNT(EmployeeID)
    FOR Gender IN ('M', 'F', 'Other')
);
```

**Example 5: PIVOT with Nested Query**
```sql
SELECT 
    EmployeeID,
    [Basic], [Medical], [Dental], [Vision]
FROM (
    SELECT EmployeeID, BenefitType, BenefitAmount
    FROM EmployeeBenefits
    WHERE BenefitAmount > 0
)
PIVOT (
    SUM(BenefitAmount)
    FOR BenefitType IN ('Basic', 'Medical', 'Dental', 'Vision')
);
```

**Example 6: PIVOT with Multiple Aggregations**
```sql
SELECT 
    Customer,
    [2022_Revenue], [2023_Revenue], [2024_Revenue],
    [2022_Orders], [2023_Orders], [2024_Orders]
FROM (
    SELECT 
        Customer, 
        YEAR(OrderDate) AS OrderYear, 
        OrderAmount,
        OrderID
    FROM CustomerOrders
)
PIVOT (
    SUM(OrderAmount) AS Revenue,
    COUNT(DISTINCT OrderID) AS Orders
    FOR OrderYear IN (2022, 2023, 2024)
);
```

**Example 7: PIVOT with Category Cross-tab**
```sql
SELECT 
    ProductCategory,
    [Small], [Medium], [Large], [XLarge]
FROM (
    SELECT ProductCategory, SizeCategory, Quantity
    FROM InventoryBySize
)
PIVOT (
    SUM(Quantity)
    FOR SizeCategory IN ('Small', 'Medium', 'Large', 'XLarge')
);
```

**Example 8: PIVOT with Dynamic Column Values**
```sql
SELECT 
    Customer,
    [Yes] AS Purchased,
    [No] AS NotPurchased
FROM (
    SELECT Customer, PurchaseFlag, COUNT(*) AS cnt
    FROM CustomerActivity
    GROUP BY Customer, PurchaseFlag
)
PIVOT (
    SUM(cnt)
    FOR PurchaseFlag IN ('Yes', 'No')
);
```

**Example 9: PIVOT with Year-to-Date Data**
```sql
SELECT 
    SalesTeamMember,
    [Jan_Target], [Feb_Target], [Mar_Target],
    [Jan_Actual], [Feb_Actual], [Mar_Actual]
FROM (
    SELECT 
        SalesTeamMember, 
        CONCAT(MonthName, '_', MeasureType) AS Metric,
        Amount
    FROM SalesTargets
)
PIVOT (
    SUM(Amount)
    FOR Metric IN (
        'Jan_Target', 'Feb_Target', 'Mar_Target',
        'Jan_Actual', 'Feb_Actual', 'Mar_Actual'
    )
);
```

**Example 10: PIVOT with Conditional Aggregation**
```sql
SELECT 
    Store,
    [High_Volume], [Medium_Volume], [Low_Volume]
FROM (
    SELECT 
        Store, 
        CASE 
            WHEN DailySales > 50000 THEN 'High_Volume'
            WHEN DailySales > 20000 THEN 'Medium_Volume'
            ELSE 'Low_Volume'
        END AS VolumeCategory,
        DailySales
    FROM DailySalesData
)
PIVOT (
    AVG(DailySales)
    FOR VolumeCategory IN ('High_Volume', 'Medium_Volume', 'Low_Volume')
);
```

---

## 11-19. REGRESSION FUNCTIONS (REGR_*)

These functions perform linear regression analysis. They calculate various statistical measures related to linear regression between two variables.

### REGR_AVGX, REGR_AVGY, REGR_COUNT, REGR_INTERCEPT, REGR_R2, REGR_SLOPE, REGR_SXX, REGR_SXY, REGR_SYY

### Description
The REGR_* family of functions provides regression analysis capabilities:
- **REGR_AVGX**: Returns average of X values
- **REGR_AVGY**: Returns average of Y values
- **REGR_COUNT**: Returns count of non-null pairs
- **REGR_INTERCEPT**: Returns Y-intercept of regression line
- **REGR_R2**: Returns coefficient of determination (R-squared)
- **REGR_SLOPE**: Returns slope of regression line
- **REGR_SXX**: Returns sum of squares of X deviations
- **REGR_SXY**: Returns sum of cross-products of X and Y deviations
- **REGR_SYY**: Returns sum of squares of Y deviations

### When to Use
- Perform linear regression analysis
- Forecast future values based on trends
- Analyze statistical relationships between variables
- Calculate regression statistics for reports
- Build predictive models
- Analyze time series data trends

### Combined Example (All REGR Functions)
```sql
SELECT 
    REGR_COUNT(Sales, Month) AS DataPointCount,
    CAST(REGR_AVGX(Sales, Month) AS DECIMAL(10,2)) AS AvgMonth,
    CAST(REGR_AVGY(Sales, Month) AS DECIMAL(10,2)) AS AvgSales,
    CAST(REGR_SLOPE(Sales, Month) AS DECIMAL(10,4)) AS SlopeValue,
    CAST(REGR_INTERCEPT(Sales, Month) AS DECIMAL(10,2)) AS InterceptValue,
    CAST(REGR_R2(Sales, Month) AS DECIMAL(10,6)) AS RSquaredValue,
    CAST(REGR_SXX(Sales, Month) AS DECIMAL(15,2)) AS SXXValue,
    CAST(REGR_SXY(Sales, Month) AS DECIMAL(15,2)) AS SXYValue,
    CAST(REGR_SYY(Sales, Month) AS DECIMAL(15,2)) AS SYYValue
FROM MonthlySalesData
GROUP BY Year;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
