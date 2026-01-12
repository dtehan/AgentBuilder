# CORR

### Function Name
**CORR**

### Description
Returns the Sample Pearson product moment correlation coefficient of its arguments for all non-null data point pairs. The correlation coefficient ranges from -1.00 to +1.00, measuring the linear association between two variables.

### When the Function Would Be Used
- Analyze relationship between sales price and number sold
- Correlate advertising spend with revenue
- Determine relationship between temperature and product demand
- Analyze correlation between student study hours and grades
- Examine relationship between employee experience and performance ratings
- Correlate website traffic with conversion rates

### Syntax
```sql
CORR (value_expression_1, value_expression_2)
```

### Code Examples

**Example 1: Basic Correlation Between Two Variables**
```sql
SELECT CAST(CORR(NbrSold, SalesPrice) AS DECIMAL(6,4)) AS CorrelationCoeff
FROM HomeSales
WHERE area = 358711030
AND SalesPrice BETWEEN 160000 AND 280000;
```

**Example 2: Correlation with GROUP BY**
```sql
SELECT 
    Area,
    CAST(CORR(NbrSold, SalesPrice) AS DECIMAL(6,4)) AS CorrelationCoeff
FROM HomeSales
GROUP BY Area;
```

**Example 3: Correlation Between Height and Weight**
```sql
SELECT CAST(CORR(Height, Weight) AS DECIMAL(6,4)) AS HeightWeightCorr
FROM PhysicalData;
```

**Example 4: Correlation with WHERE Filter**
```sql
SELECT CAST(CORR(Temperature, IceCreamSales) AS DECIMAL(6,4)) AS TempSalesCorr
FROM SeasonalData
WHERE Season = 'Summer';
```

**Example 5: Multiple Correlations in One Query**
```sql
SELECT 
    CAST(CORR(AdvertisingSpend, Revenue) AS DECIMAL(6,4)) AS AdvRevCorr,
    CAST(CORR(AdvertisingSpend, CustomerCount) AS DECIMAL(6,4)) AS AdvCustCorr,
    CAST(CORR(Revenue, CustomerCount) AS DECIMAL(6,4)) AS RevCustCorr
FROM BusinessMetrics;
```

**Example 6: Correlation by Business Segment**
```sql
SELECT 
    Segment,
    CAST(CORR(MarketingBudget, Sales) AS DECIMAL(6,4)) AS BudgetSalesCorr
FROM SegmentPerformance
GROUP BY Segment
HAVING CORR(MarketingBudget, Sales) > 0.7;
```

**Example 7: Correlation Between Employee Variables**
```sql
SELECT CAST(CORR(YearsExperience, PerformanceRating) AS DECIMAL(6,4)) AS ExpPerformCorr
FROM EmployeeData
WHERE Department IN ('Sales', 'IT');
```

**Example 8: Year-over-Year Correlation Analysis**
```sql
SELECT 
    Year,
    CAST(CORR(QuarterNumber, Revenue) AS DECIMAL(6,4)) AS SeasonalCorr
FROM QuarterlyRevenue
GROUP BY Year;
```

**Example 9: Correlation with Casting**
```sql
SELECT 
    ProductLine,
    CAST(CORR(CAST(Quantity AS DECIMAL), CAST(UnitPrice AS DECIMAL)) AS DECIMAL(6,4)) AS QtyPriceCorr
FROM ProductSales
GROUP BY ProductLine;
```

**Example 10: Correlation with Integer Data**
```sql
SELECT 
    CAST(CORR(
        CAST(WebsiteVisitors AS DECIMAL),
        CAST(PurchaseTransactions AS DECIMAL)
    ) AS DECIMAL(6,4)) AS VisitorTransactionCorr
FROM WebAnalytics;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
