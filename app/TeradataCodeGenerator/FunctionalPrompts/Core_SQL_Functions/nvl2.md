# NVL2

**Function Name:** NVL2

**Description:** Returns one value if expression is NOT NULL, another if it IS NULL.

**When to Use:**
- Conditional replacement based on NULL
- Two-way conditional logic
- State-dependent values

**Syntax:**
```sql
NVL2(expression, not_null_value, null_value)
```

**Examples:**

**Example 1 - Presence Check**
```sql
SELECT 
    OrderID,
    ShippingDate,
    NVL2(ShippingDate, 'Shipped', 'Pending') AS ShippingStatus
FROM Orders;
```

**Example 2 - Payment Status**
```sql
SELECT 
    InvoiceID,
    PaymentDate,
    NVL2(PaymentDate, Amount, 0) AS CollectedAmount
FROM Invoices;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
