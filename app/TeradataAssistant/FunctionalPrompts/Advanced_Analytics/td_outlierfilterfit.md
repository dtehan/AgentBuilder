# TD_OutlierFilterFit

### Function Name
**TD_OutlierFilterFit**

### Description
Calculates the lower_percentile, upper_percentile, count of rows, and median for the

### When the Function Would Be Used
- Performing advanced data analysis and transformation
- Building predictive models and machine learning workflows
- Feature engineering and data preparation
- Statistical analysis and hypothesis testing
- Text processing and natural language analysis

### Syntax
For complete syntax details, refer to Teradata Database Analytic Functions documentation (B035-1206-172K.pdf, Release 17.20)

### Code Examples

**Example 1: Basic Usage**
```sql
-- Consult Teradata documentation for function-specific syntax
SELECT TD_OutlierFilterFit(...) FROM table_name;
```

**Example 2: With Parameters**
```sql
-- See Teradata documentation for parameter details
SELECT TD_OutlierFilterFit(parameter1, parameter2, ...) FROM table_name;
```

**Example 3: Advanced Usage**
```sql
-- For advanced examples, refer to the official Teradata documentation
SELECT TD_OutlierFilterFit(...) FROM table_name WHERE condition;
```

**Example 4: With GROUP BY**
```sql
SELECT 
    group_column,
    TD_OutlierFilterFit(...)
FROM table_name
GROUP BY group_column;
```

**Example 5: In Subquery**
```sql
SELECT *
FROM (
    SELECT TD_OutlierFilterFit(...) 
    FROM table_name
) subquery;
```

### Related Functions
- See Teradata Database Analytic Functions documentation for related functions
- Review similar functions in the Data Exploration category

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Note**: This is a template documentation. For complete syntax, parameters, and examples, consult the official Teradata documentation.