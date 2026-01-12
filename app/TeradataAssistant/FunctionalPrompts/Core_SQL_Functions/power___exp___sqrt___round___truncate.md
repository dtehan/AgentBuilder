# POWER / EXP / SQRT / ROUND / TRUNCATE

These mathematical functions provide advanced numeric operations.

**POWER:** Raises a number to a power
```sql
SELECT POWER(2, 3) AS Result;  -- Returns: 8
SELECT POWER(10, 2) AS Result; -- Returns: 100
```

**SQRT:** Returns square root
```sql
SELECT SQRT(16) AS Result;     -- Returns: 4
SELECT SQRT(25) AS Result;     -- Returns: 5
```

**ROUND:** Rounds to specified decimal places
```sql
SELECT ROUND(3.14159, 2) AS Result;     -- Returns: 3.14
SELECT ROUND(123.567, -1) AS Result;    -- Returns: 120
```

**TRUNCATE:** Removes decimal places
```sql
SELECT TRUNCATE(3.99999, 2) AS Result;  -- Returns: 3.99
SELECT TRUNCATE(123.567, -1) AS Result; -- Returns: 120
```

**EXP:** Raises e to a power
```sql
SELECT EXP(1) AS Result;   -- Returns: 2.71828...
SELECT EXP(2) AS Result;   -- Returns: 7.38906...
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
