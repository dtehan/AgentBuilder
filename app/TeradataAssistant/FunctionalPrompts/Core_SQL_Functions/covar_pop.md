# COVAR_POP

### Function Name
**COVAR_POP**

### Description
Returns the population covariance of its arguments for all non-null data point pairs. Covariance measures whether two random variables vary in the same way. Returns NULL if there are no non-null data point pairs.

### When the Function Would Be Used
- Analyze covariance between stock prices in a portfolio
- Determine relationship variability between supply and demand
- Examine joint variability between two measurements
- Analyze relationship between asset returns
- Measure covariance between economic indicators
- Analyze relationship variability in experimental data
- Examine joint variability in quality metrics

### Syntax
```sql
COVAR_POP (value_expression_1, value_expression_2)
```

### Code Examples

**Example 1: Basic Population Covariance**
```sql
SELECT COVAR_POP(Height, Weight) AS PopCovarianceHW
FROM PhysicalData;
```

**Example 2: Population Covariance by Group**
```sql
SELECT 
    Gender,
    COVAR_POP(Height, Weight) AS PopCovarianceHW
FROM PhysicalData
GROUP BY Gender;
```

**Example 3: Stock Price Covariance**
```sql
SELECT COVAR_POP(StockA_Price, StockB_Price) AS StockCovariance
FROM PortfolioData
WHERE TradingDate BETWEEN '2024-01-01' AND '2024-12-31';
```

**Example 4: Multiple Covariance Measures**
```sql
SELECT 
    COVAR_POP(Supply, Demand) AS SupplyDemandCov,
    COVAR_POP(Price, Demand) AS PriceDemandCov,
    COVAR_POP(Supply, Price) AS SupplyPriceCov
FROM MarketData;
```

**Example 5: Population Covariance with WHERE Filter**
```sql
SELECT 
    Region,
    COVAR_POP(AdSpend, Revenue) AS AdRevenueCovariance
FROM RegionalMetrics
WHERE Year = 2024
GROUP BY Region;
```

**Example 6: Covariance Between Numeric Conversions**
```sql
SELECT CAST(COVAR_POP(
    CAST(Quantity AS DECIMAL),
    CAST(Price AS DECIMAL)
) AS DECIMAL(10,4)) AS QtyPriceCov
FROM ProductTransactions;
```

**Example 7: Population Covariance with Multiple Aggregates**
```sql
SELECT 
    Department,
    COUNT(*) AS RecordCount,
    COVAR_POP(ExperienceYears, Salary) AS ExpSalaryCov,
    AVG(Salary) AS AvgSalary
FROM EmployeeData
GROUP BY Department;
```

**Example 8: Covariance for Quality Control**
```sql
SELECT 
    ProcessLine,
    COVAR_POP(Temperature, YieldPercentage) AS TempYieldCov
FROM ManufacturingData
WHERE Quality_Status = 'Approved'
GROUP BY ProcessLine;
```

**Example 9: Time Series Covariance**
```sql
SELECT 
    Year,
    COVAR_POP(QuarterlyGrowth, MarketShare) AS GrowthShareCov
FROM BusinessPerformance
WHERE Market = 'Domestic'
GROUP BY Year
ORDER BY Year;
```

**Example 10: Covariance with Complex Filtering**
```sql
SELECT 
    COVAR_POP(
        CAST(API_Response_Time AS DECIMAL),
        CAST(Error_Rate AS DECIMAL)
    ) AS ResponseErrorCov
FROM SystemMetrics
WHERE Server NOT IN ('Backup', 'Dev')
AND Timestamp >= CURRENT_DATE - 30;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
