# CONCAT / ||

**Function Name:** CONCAT or ||

**Description:** Concatenates two or more strings together.

**When to Use:**
- Combine first and last names
- Build full addresses
- Create display strings
- Combine codes
- Build formatted output

**Syntax:**
```sql
CONCAT(string1, string2, ...)  or  string1 || string2 || ...
```

**Examples:**

**Example 1 - Basic Concatenation**
```sql
SELECT CONCAT('Hello', ' ', 'World') AS Result;
-- or
SELECT 'Hello' || ' ' || 'World' AS Result;
-- Returns: 'Hello World'
```

**Example 2 - Full Name**
```sql
SELECT 
    FirstName,
    LastName,
    FirstName || ' ' || LastName AS FullName
FROM Employees;
```

**Example 3 - Full Address**
```sql
SELECT 
    Street || ', ' || City || ', ' || State || ' ' || ZipCode AS FullAddress
FROM Addresses;
```

**Example 4 - Formatted Phone**
```sql
SELECT 
    AreaCode,
    Exchange,
    LineNumber,
    '(' || AreaCode || ') ' || Exchange || '-' || LineNumber AS FormattedPhone
FROM PhoneNumbers;
```

**Example 5 - Create IDs**
```sql
SELECT 
    Department,
    EmployeeNumber,
    Department || '-' || EmployeeNumber AS EmployeeID
FROM Employees;
```

**Example 6 - Build URLs**
```sql
SELECT 
    Domain,
    Path,
    'https://' || Domain || '/' || Path AS FullURL
FROM WebResources;
```

**Example 7 - Combine Codes**
```sql
SELECT 
    CountryCode,
    AreaCode,
    LocalCode,
    CountryCode || AreaCode || LocalCode AS DiamondCode
FROM RegionalCodes;
```

**Example 8 - Build Email**
```sql
SELECT 
    FirstName,
    LastName,
    Company,
    LOWER(FirstName || '.' || LastName || '@' || Company || '.com') AS Email
FROM Users;
```

**Example 9 - Create Display Text**
```sql
SELECT 
    ProductName,
    Price,
    ProductName || ' - $' || Price AS DisplayText
FROM Products;
```

**Example 10 - Concatenate Multiple Columns**
```sql
SELECT 
    Title || ' ' || FirstName || ' ' || LastName || ', ' || Department AS EmployeeCard
FROM Employees;
```

---

### 8-15. ADDITIONAL STRING FUNCTIONS

**UPPER:** Converts to uppercase
```sql
SELECT UPPER('hello') AS Result;  -- Returns: 'HELLO'
```

**LOWER:** Converts to lowercase
```sql
SELECT LOWER('HELLO') AS Result;  -- Returns: 'hello'
```

**TRIM / LTRIM / RTRIM:** Removes spaces
```sql
SELECT TRIM('  hello  ') AS Result;    -- Returns: 'hello'
SELECT LTRIM('  hello') AS Result;     -- Returns: 'hello'
SELECT RTRIM('hello  ') AS Result;     -- Returns: 'hello'
```

**LENGTH / CHARACTER_LENGTH:** Returns string length
```sql
SELECT LENGTH('hello') AS Result;  -- Returns: 5
```

**POSITION / CHARINDEX:** Finds position of substring
```sql
SELECT POSITION('o' IN 'hello') AS Result;  -- Returns: 5
SELECT CHARINDEX('ll', 'hello') AS Result;  -- Returns: 3
```

**REPLACE:** Replaces substring
```sql
SELECT REPLACE('hello', 'l', 'L') AS Result;  -- Returns: 'heLLo'
```

**INSTR:** Similar to POSITION
```sql
SELECT INSTR('hello', 'l') AS Result;  -- Returns: 3
```

---

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
