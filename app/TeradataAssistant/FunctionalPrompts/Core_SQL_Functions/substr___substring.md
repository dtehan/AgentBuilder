# SUBSTR / SUBSTRING

**Function Name:** SUBSTR | SUBSTRING

**Description:** Extracts a substring from a string starting at a specified position for a specified length.

**When to Use:**
- Extract portions of strings
- Parse formatted data
- Extract ZIP codes or codes
- Get initials from names
- Manipulate string data

**Syntax:**
```sql
SUBSTR(string, start_position [, length])
```

**Examples:**

**Example 1 - Basic Substring**
```sql
SELECT SUBSTR('HelloWorld', 1, 5) AS Result;  -- Returns: 'Hello'
SELECT SUBSTR('Database', 5, 4) AS Result;    -- Returns: 'base'
```

**Example 2 - Extract Area Code**
```sql
SELECT 
    PhoneNumber,
    SUBSTR(PhoneNumber, 1, 3) AS AreaCode
FROM Contacts;
```

**Example 3 - Parse Date String**
```sql
SELECT 
    DateString,
    SUBSTR(DateString, 1, 4) AS Year,
    SUBSTR(DateString, 6, 2) AS Month,
    SUBSTR(DateString, 9, 2) AS Day
FROM DateData;
```

**Example 4 - Extract Initials**
```sql
SELECT 
    FirstName,
    LastName,
    SUBSTR(FirstName, 1, 1) || '.' || SUBSTR(LastName, 1, 1) AS Initials
FROM Employees;
```

**Example 5 - Extract Domain from Email**
```sql
SELECT 
    Email,
    SUBSTR(Email, POSITION('@' IN Email) + 1) AS Domain
FROM EmailList;
```

**Example 6 - Extract Product Code**
```sql
SELECT 
    SkuNumber,
    SUBSTR(SkuNumber, 1, 3) AS ProductLine,
    SUBSTR(SkuNumber, 4, 2) AS Category
FROM Products;
```

**Example 7 - Extract State from Address**
```sql
SELECT 
    Address,
    SUBSTR(Address, -5, 2) AS StateCode
FROM Addresses;
```

**Example 8 - Mid-String Extraction**
```sql
SELECT 
    FullText,
    SUBSTR(FullText, 10, 20) AS MiddleSection
FROM TextData;
```

**Example 9 - Remove Prefix**
```sql
SELECT 
    ItemCode,
    SUBSTR(ItemCode, 4) AS CodeWithoutPrefix
FROM Items
WHERE ItemCode LIKE 'PRE_%';
```

**Example 10 - Extract Multiple Parts**
```sql
SELECT 
    ReferenceNumber,
    SUBSTR(ReferenceNumber, 1, 2) AS System,
    SUBSTR(ReferenceNumber, 3, 4) AS Type,
    SUBSTR(ReferenceNumber, 7) AS ID
FROM References;
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
