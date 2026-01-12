# ADD_MONTHS / DATE_ADD / DATE_SUB

**Function Name:** ADD_MONTHS

**Description:** Adds or subtracts months from a date.

**When to Use:**
- Calculate future dates
- Calculate anniversary dates
- Project deadlines
- Calculate aging
- Project future periods

**Syntax:**
```sql
ADD_MONTHS(date_expression, months_to_add)
```

**Examples:**

**Example 1 - Add Months**
```sql
SELECT ADD_MONTHS(CURRENT_DATE, 3) AS FutureDate;
```

**Example 2 - Subtract Months**
```sql
SELECT ADD_MONTHS(CURRENT_DATE, -12) AS OneYearAgo;
```

**Example 3 - Project Renewal Dates**
```sql
SELECT 
    ContractID,
    StartDate,
    ADD_MONTHS(StartDate, 12) AS RenewalDate
FROM Contracts;
```

**Example 4 - Calculate Expiration**
```sql
SELECT 
    ProductID,
    ManufactureDate,
    ADD_MONTHS(ManufactureDate, 24) AS ExpirationDate
FROM Products;
```

**Example 5 - Age Cohorts**
```sql
SELECT 
    CustomerID,
    JoinDate,
    CASE 
        WHEN ADD_MONTHS(JoinDate, 12) < CURRENT_DATE THEN '1+ Years'
        WHEN ADD_MONTHS(JoinDate, 6) < CURRENT_DATE THEN '6-12 Months'
        ELSE 'New (< 6 Months)'
    END AS CustomerCohort
FROM Customers;
```

**Example 6 - Payment Schedule**
```sql
SELECT 
    LoanID,
    LoanDate,
    ADD_MONTHS(LoanDate, 12) AS PaymentDue1,
    ADD_MONTHS(LoanDate, 24) AS PaymentDue2,
    ADD_MONTHS(LoanDate, 36) AS PaymentDue3
FROM Loans;
```

**Example 7 - Warranty Period**
```sql
SELECT 
    PurchaseID,
    PurchaseDate,
    ADD_MONTHS(PurchaseDate, 24) AS WarrantyExpiration
FROM Purchases;
```

**Example 8 - Project Quarter Dates**
```sql
SELECT 
    QuarterID,
    StartDate,
    ADD_MONTHS(StartDate, 3) AS EndDate
FROM Quarters;
```

**Example 9 - Historical Analysis**
```sql
SELECT 
    MetricID,
    MeasurementDate,
    MetricValue,
    ADD_MONTHS(MeasurementDate, -12) AS YearAgoDate
FROM Metrics;
```

**Example 10 - Milestone Tracking**
```sql
SELECT 
    ProjectID,
    StartDate,
    ADD_MONTHS(StartDate, 3) AS Phase1End,
    ADD_MONTHS(StartDate, 6) AS Phase2End,
    ADD_MONTHS(StartDate, 12) AS ProjectEnd
FROM Projects;
```

---

### 19-25. OTHER DATE FUNCTIONS

**CURRENT_TIMESTAMP / NOW:** Returns current date and time
```sql
SELECT CURRENT_TIMESTAMP AS CurrentDateTime;
SELECT NOW() AS CurrentDateTime;
```

**CURRENT_TIME:** Returns current time
```sql
SELECT CURRENT_TIME AS CurrentTime;
```

**DATEDIFF:** Calculates difference between dates
```sql
SELECT DATEDIFF(DAY, '2024-01-01', '2024-12-31') AS DaysDifference;
```

**DATETRUNC / TRUNC:** Truncates date to period
```sql
SELECT TRUNC(CURRENT_DATE, 'MONTH') AS FirstOfMonth;
```

**DAY / MONTH / YEAR:** Extract individual components
```sql
SELECT DAY(CURRENT_DATE) AS DayOfMonth;
SELECT MONTH(CURRENT_DATE) AS CurrentMonth;
SELECT YEAR(CURRENT_DATE) AS CurrentYear;
```

**DAYNAME / MONTHNAME:** Return day/month names
```sql
SELECT DAYNAME(CURRENT_DATE) AS DayName;
SELECT MONTHNAME(CURRENT_DATE) AS MonthName;
```

**LAST_DAY:** Returns last day of month
```sql
SELECT LAST_DAY(CURRENT_DATE) AS LastDayOfMonth;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
