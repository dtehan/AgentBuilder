# TD_RoundColumns

### Function Name
**TD_RoundColumns**

### Description
TD_RoundColumns rounds the values of each specified input table column to a specified number of decimal places, providing precise control over numeric precision for data consistency, storage optimization, and analytical clarity. This function enables batch rounding of multiple numeric columns simultaneously, ensuring uniform precision across datasets while maintaining data integrity and supporting downstream analytical workflows.

Rounding numeric data to appropriate precision levels offers multiple benefits including data consistency across systems, reduced storage footprint for large datasets, improved computational performance, cleaner visualizations, and elimination of spurious precision that can obscure patterns. The function supports both positive precision (digits to the right of decimal point) and negative precision (rounding to tens, hundreds, thousands), enabling flexible control over numeric representation from fine-grained decimals to coarse-grained aggregations.

TD_RoundColumns seamlessly integrates into data engineering pipelines, applying efficient element-wise rounding transformations with minimal overhead. The function handles DECIMAL/NUMERIC types intelligently, automatically adjusting precision and scale to accommodate rounded values while respecting maximum precision constraints. This makes it essential for preparing clean, consistent numeric data for reporting, visualization, machine learning, and analytical applications where appropriate precision improves both interpretation and performance.

### When the Function Would Be Used
- **Data Consistency**: Ensure consistent numeric precision across datasets and systems
- **Storage Optimization**: Reduce dataset size by eliminating unnecessary decimal places
- **Improved Accuracy**: Focus on significant digits relevant to analysis
- **Visualization Enhancement**: Create cleaner charts and reports with appropriate precision
- **Performance Improvement**: Speed up computations by reducing numeric precision
- **Financial Rounding**: Apply standard rounding for monetary calculations
- **Report Preparation**: Format numeric data for presentation and reporting
- **Data Quality**: Eliminate false precision from measurements and calculations
- **Algorithm Performance**: Improve ML algorithm speed with reduced precision
- **Cross-System Integration**: Align precision standards across data sources
- **Measurement Rounding**: Round to measurement precision (e.g., nearest cm, kg)
- **Statistical Reporting**: Present results with appropriate significant figures
- **Data Anonymization**: Reduce granularity for privacy protection
- **Threshold Bucketing**: Round to boundaries for categorical creation

### Syntax

```sql
TD_RoundColumns (
    ON { table | view | (query) } AS InputTable
    USING
    TargetColumns ({ 'target_column' | target_column_range }[,...])
    [ PrecisionDigit (precision) ]
    [ Accumulate ({ 'accumulate_column' | accumulate_column_range }[,...]) ]
)
```

### Required Syntax Elements for TD_RoundColumns

**ON clause (InputTable)**
- Accepts the InputTable clause containing numeric data to round
- No partitioning required (operates on all rows)

**TargetColumns**
- Specify names of InputTable columns to round
- Must be numeric data types
- Supports column range notation
- Multiple columns can be rounded simultaneously

### Optional Syntax Elements for TD_RoundColumns

**PrecisionDigit**
- Specify number of decimal places for rounding
- **Positive precision**: Rounds to right of decimal point (e.g., 2 = hundredths place)
- **Negative precision**: Rounds to left of decimal point (e.g., -2 = hundreds place)
- **Zero precision**: Rounds to nearest integer
- Default: 0 (rounds to integer)

**Precision Adjustment for DECIMAL/NUMERIC**:
- If column precision < 38, function increases precision by 1 to accommodate rounding
- Example: DECIMAL(4,2) value 99.99 rounded to 0 places becomes DECIMAL(5,2) value 100.00
- If precision = 38, function reduces scale by 1 unless scale = 0
- Example: DECIMAL(38,36) value rounded becomes DECIMAL(38,35)

**Accumulate**
- Specify InputTable columns to copy to output table unchanged
- Preserves identifiers, keys, and non-numeric columns
- Supports column range notation

### Input Table Schema

**InputTable Schema:**

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | NUMERIC (INTEGER, BIGINT, FLOAT, DOUBLE PRECISION, DECIMAL, NUMERIC) | Columns to round to precision digits |
| accumulate_column | ANY | [Optional] Columns to preserve unchanged |

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | NUMERIC (same type as input, precision may increase by 1) | Rounded columns with values rounded to precision digits |
| accumulate_column | Same as InputTable | Columns copied unchanged from InputTable |

All target columns are rounded in place with same column names.

### Code Examples

**Input Data: titanic_passengers**
```
passenger_id  pclass  fare         survived
1             3       7.25000000   0
2             1       71.28330000  1
3             3       7.92500000   1
4             1       53.10000000  1
5             3       8.05000000   0
```

**Example 1: Round to 1 Decimal Place**
```sql
-- Round fare to nearest tenth
SELECT * FROM TD_RoundColumns (
    ON titanic_passengers AS InputTable
    USING
    TargetColumns ('fare')
    PrecisionDigit (1)
    Accumulate ('passenger_id', 'pclass', 'survived')
) AS dt
ORDER BY passenger_id;
```

**Output:**
```
passenger_id  pclass  survived  fare
1             3       0         7.3
2             1       1         71.3
3             3       1         7.9
4             1       1         53.1
5             3       0         8.1
```

**Example 2: Round to Integer (Default)**
```sql
-- Round fare to nearest whole number
SELECT * FROM TD_RoundColumns (
    ON titanic_passengers AS InputTable
    USING
    TargetColumns ('fare')
    -- PrecisionDigit (0) is default
    Accumulate ('passenger_id', 'pclass', 'survived')
) AS dt
ORDER BY passenger_id;
```

**Output:**
```
passenger_id  pclass  survived  fare
1             3       0         7
2             1       1         71
3             3       1         8
4             1       1         53
5             3       0         8
```

**Example 3: Multiple Columns**
```sql
-- Round multiple numeric columns
SELECT * FROM TD_RoundColumns (
    ON financial_data AS InputTable
    USING
    TargetColumns ('revenue', 'expenses', 'profit', 'tax_amount')
    PrecisionDigit (2)  -- Round to cents
    Accumulate ('company_id', 'fiscal_year')
) AS dt;

-- All financial columns rounded to 2 decimal places (cents)
```

**Example 4: Negative Precision (Round to Tens)**
```sql
-- Round population to nearest 10
SELECT * FROM TD_RoundColumns (
    ON city_stats AS InputTable
    USING
    TargetColumns ('population')
    PrecisionDigit (-1)  -- Round to tens place
    Accumulate ('city_name', 'state', 'country')
) AS dt;

-- Example: 123,456 → 123,460
--         987,654 → 987,650
```

**Example 5: Negative Precision (Round to Thousands)**
```sql
-- Round sales to nearest thousand for aggregation
SELECT * FROM TD_RoundColumns (
    ON sales_transactions AS InputTable
    USING
    TargetColumns ('transaction_amount')
    PrecisionDigit (-3)  -- Round to thousands
    Accumulate ('customer_id', 'transaction_date')
) AS dt;

-- Example: $12,345 → $12,000
--         $98,765 → $99,000
```

**Example 6: All Numeric Columns**
```sql
-- Round all columns using column range notation
SELECT * FROM TD_RoundColumns (
    ON measurements AS InputTable
    USING
    TargetColumns ('[:]')  -- All columns
    PrecisionDigit (1)
) AS dt;

-- Rounds every numeric column to 1 decimal place
```

**Example 7: Financial Data Standardization**
```sql
-- Standardize monetary values to 2 decimal places
CREATE TABLE sales_rounded AS (
    SELECT * FROM TD_RoundColumns (
        ON sales_data AS InputTable
        USING
        TargetColumns ('sale_price', 'cost', 'tax', 'discount', 'net_revenue')
        PrecisionDigit (2)
        Accumulate ('sale_id', 'customer_id', 'sale_date', 'product_id')
    ) AS dt
) WITH DATA;

-- All monetary columns now have exactly 2 decimal places
-- Ensures consistency for financial reporting
```

**Example 8: Measurement Data Rounding**
```sql
-- Round measurements to appropriate precision
SELECT * FROM TD_RoundColumns (
    ON sensor_readings AS InputTable
    USING
    TargetColumns ('temperature_c', 'humidity_pct', 'pressure_hpa')
    PrecisionDigit (1)  -- Appropriate for sensor precision
    Accumulate ('sensor_id', 'timestamp', 'location')
) AS dt;

-- Matches sensor precision (typically ±0.1 for these sensors)
-- Eliminates spurious precision from calculations
```

**Example 9: Privacy-Preserving Rounding**
```sql
-- Round sensitive numeric data for anonymization
SELECT * FROM TD_RoundColumns (
    ON patient_data AS InputTable
    USING
    TargetColumns ('age', 'weight_kg', 'height_cm', 'bmi')
    PrecisionDigit (0)  -- Round to integers
    Accumulate ('patient_id', 'admission_date', 'diagnosis')
) AS dt;

-- Reduces granularity of PII for privacy protection
-- Age: 45.7 → 46, Weight: 78.3 kg → 78 kg
```

**Example 10: Visualization-Ready Data**
```sql
-- Prepare data for clean visualization
CREATE TABLE chart_data AS (
    SELECT * FROM TD_RoundColumns (
        ON analytics_metrics AS InputTable
        USING
        TargetColumns ('avg_response_time', 'success_rate', 'throughput')
        PrecisionDigit (2)
        Accumulate ('date', 'service_name')
    ) AS dt
) WITH DATA;

-- Clean numbers for charts and dashboards
-- 0.847231 → 0.85, 123.456789 → 123.46
```

### Rounding Behavior

**Positive Precision (Decimal Places)**:
```
Value: 7.25               Value: 71.2833
PrecisionDigit(0) → 7     PrecisionDigit(0) → 71
PrecisionDigit(1) → 7.3   PrecisionDigit(1) → 71.3
PrecisionDigit(2) → 7.25  PrecisionDigit(2) → 71.28
```

**Negative Precision (Left of Decimal)**:
```
Value: 12,345
PrecisionDigit(0) → 12,345    (no rounding)
PrecisionDigit(-1) → 12,350   (nearest 10)
PrecisionDigit(-2) → 12,300   (nearest 100)
PrecisionDigit(-3) → 12,000   (nearest 1,000)
PrecisionDigit(-4) → 10,000   (nearest 10,000)
```

**Rounding Rules**:
- Standard mathematical rounding (round half up)
- 0.5 rounds to 1.0
- -0.5 rounds to -1.0
- Applied independently to each value

### Use Cases and Applications

**1. Financial Data Standardization**
- Round monetary values to standard 2 decimal places
- Ensure consistency across accounting systems
- Prepare data for financial reporting
- Align with currency precision standards

**2. Measurement Data Cleaning**
- Round to sensor/instrument precision
- Eliminate spurious precision from calculations
- Match measurement uncertainty
- Prepare data for scientific reporting

**3. Reporting and Visualization**
- Create clean, readable numbers for reports
- Format metrics for dashboards
- Prepare data for charts and graphs
- Eliminate distracting decimal places

**4. Storage Optimization**
- Reduce numeric precision for large datasets
- Decrease storage footprint
- Improve backup and transfer performance
- Optimize columnar compression

**5. Performance Improvement**
- Speed up ML algorithm training
- Reduce computational complexity
- Improve aggregation performance
- Enable faster sorting and joining

**6. Privacy Protection**
- Reduce granularity of sensitive numeric data
- Support k-anonymity techniques
- Generalize measurements for disclosure
- Create privacy-preserving datasets

**7. Data Integration**
- Align precision across heterogeneous sources
- Standardize numeric formats
- Enable consistent joins and comparisons
- Support data warehouse ETL

**8. Statistical Reporting**
- Present results with appropriate significant figures
- Match statistical test precision
- Report confidence intervals clearly
- Format p-values and effect sizes

**9. Business Metrics**
- Round KPIs to meaningful precision
- Standardize metric reporting
- Create executive dashboards
- Prepare investor reports

**10. Machine Learning Preprocessing**
- Reduce feature precision for regularization
- Improve model generalization
- Decrease overfitting risk
- Speed up training convergence

### Important Notes

**DECIMAL/NUMERIC Precision Handling:**
- Function automatically adjusts precision for DECIMAL/NUMERIC types
- Precision < 38: increases by 1 to accommodate rounding
- Precision = 38: reduces scale by 1 (unless scale = 0)
- Prevents overflow from rounding (e.g., 99.99 → 100.00)

**Data Type Preservation:**
- Function preserves original data types
- INTEGER/BIGINT remain INTEGER/BIGINT
- FLOAT/DOUBLE PRECISION remain FLOAT/DOUBLE PRECISION
- DECIMAL/NUMERIC retain type with adjusted precision/scale

**Rounding vs Truncation:**
- TD_RoundColumns performs mathematical rounding (not truncation)
- 0.5 rounds up to 1.0
- -0.5 rounds to -1.0 (round half away from zero)
- Use CAST/FLOOR/CEILING for truncation if needed

**NULL Handling:**
- NULL values remain NULL after rounding
- Rounding does not create or remove NULLs
- NULL-safe operation

**Performance:**
- Efficient element-wise operation
- Scales well to large datasets
- Minimal computational overhead
- No sorting or aggregation required

**Precision Loss:**
- Rounding is destructive (cannot be reversed)
- Original values are lost
- Consider preserving originals if needed
- Test rounding impact on downstream analysis

**Multiple Column Efficiency:**
- More efficient to round multiple columns in single call
- Use TargetColumns with multiple columns or ranges
- Reduces I/O and processing overhead

**Column Range Notation:**
- `'[:]'` rounds all columns
- `'[2:5]'` rounds columns 2 through 5
- Efficient for many columns

### Best Practices

**1. Choose Appropriate Precision**
- Match precision to data source accuracy
- Financial: 2 decimals for currency
- Percentages: 1-2 decimals typically sufficient
- Scientific: match instrument precision
- Consider downstream use cases

**2. Preserve Original Data**
- Create rounded copies, keep originals
- Enables validation and rollback
- Supports A/B testing of precision
- Document rounding decisions

**3. Document Rounding Strategy**
- Record precision choices and rationale
- Document which columns rounded and why
- Maintain data lineage
- Enable reproducibility

**4. Validate Impact**
- Test statistical properties before/after rounding
- Validate downstream analytics unchanged
- Check visualization clarity
- Assess storage savings

**5. Use Accumulate Effectively**
- Preserve identifiers and keys
- Keep non-numeric columns
- Maintain referential integrity
- Include metadata columns

**6. Consider Negative Precision**
- Round to 10s, 100s, 1000s for aggregation
- Useful for privacy and generalization
- Creates natural bucketing
- Simplifies large number displays

**7. Round at Appropriate Pipeline Stage**
- Round after transformations and calculations
- Before final storage or reporting
- Not during intermediate calculations
- Minimize cumulative rounding errors

**8. Test with Boundary Values**
- Test with values near rounding boundaries (0.5, 0.05, etc.)
- Verify handling of very large/small numbers
- Check NULL handling
- Validate DECIMAL precision adjustment

**9. Monitor Precision Requirements**
- Review if rounding too aggressive
- Check if precision loss affects results
- Adjust based on user feedback
- Balance accuracy vs clarity

**10. Combine with Data Quality Checks**
- Validate no unexpected NULLs or outliers
- Check rounded value distributions
- Verify no data loss
- Confirm expected value ranges

### Related Functions
- **ROUND()** - SQL built-in function for single value rounding
- **FLOOR() / CEILING()** - SQL functions for truncation
- **CAST()** - Type conversion with potential rounding
- **TD_NumApply** - Apply mathematical transformations
- **TRUNC()** - Truncate to specified precision (alternative to rounding)

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Utility Functions
