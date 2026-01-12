# NVL / COALESCE

**Function Name:** NVL | COALESCE

**Description:** Returns an alternative value if the expression is NULL.

**When to Use:**
- Handle NULL values in calculations
- Provide default values
- Replace missing data
- Standardize output

**Syntax:**
```sql
NVL(expression, replacement_value)  or  COALESCE(expr1, expr2, ..., exprN)
```

**Examples:**

**Example 1 - Replace NULL with Default**
```sql
SELECT 
    EmployeeID,
    Commission,
    NVL(Commission, 0) AS CommissionValue
FROM Employees;
```

**Example 2 - Multiple Options**
```sql
SELECT 
    OrderID,
    COALESCE(SpecialInstructions, GeneralInstructions, 'No Instructions') AS Instructions
FROM Orders;
```

**Example 3 - Calculations with NULLs**
```sql
SELECT 
    ProductID,
    Price * NVL(Quantity, 0) AS LineAmount
FROM OrderItems;
```

**Example 4 - Contact Information**
```sql
SELECT 
    PersonID,
    COALESCE(CellPhone, WorkPhone, HomePhone, 'No Phone') AS ContactNumber
FROM Contacts;
```

**Example 5 - Address Fallback**
```sql
SELECT 
    CustomerID,
    COALESCE(BillingAddress, ShippingAddress, 'No Address') AS PrimaryAddress
FROM Customers;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
