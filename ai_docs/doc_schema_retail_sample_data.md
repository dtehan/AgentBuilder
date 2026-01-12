# Database Schema Documentation: retail_sample_data

**Generated:** 2026-01-06
**Database Platform:** Teradata

---

## Overview

The `retail_sample_data` database contains tables supporting retail business operations, including customer information, sales transactions, and transaction line-item details. This schema provides a foundation for retail analytics, customer insights, and sales performance analysis.

---

## Tables Summary

| Table Name | Description | Column Count |
|------------|-------------|--------------|
| ev_customers | Customer master data with personal and demographic information | 35 |
| sales_transaction_line_parquet_ft | Sales transaction line items stored in Parquet format (foreign table) | 14 |
| RETAIL_TRANSACTIONS | Retail transaction records with order and payment details | 15 |

---

## Table Details

### 1. ev_customers

#### Business Description

The `ev_customers` table serves as the customer master data repository, containing comprehensive customer profiles including personal identification, contact information, physical attributes, payment details, and geographic location data. This table supports customer relationship management, marketing segmentation, and personalized customer experiences.

#### Schema Information

- **Database:** retail_sample_data
- **Table Name:** ev_customers
- **Column Count:** 35

#### Columns

| Column Name | Data Type | Business Description |
|-------------|-----------|---------------------|
| Id | INTEGER | Primary identifier for each customer record |
| GivenName | VARCHAR | Customer's first name |
| Surname | VARCHAR | Customer's last name/family name |
| MiddleInitial | VARCHAR | Customer's middle initial |
| Gender | VARCHAR | Customer's gender |
| Birthday | VARCHAR | Customer's date of birth |
| BloodType | VARCHAR | Customer's blood type |
| StreetAddress | VARCHAR | Street address for customer residence |
| City | VARCHAR | City of residence |
| State | VARCHAR | State or province of residence |
| ZipCode | INTEGER | Postal/ZIP code |
| Country | VARCHAR | Country of residence |
| Latitude | FLOAT | Geographic latitude coordinate |
| Longitude | FLOAT | Geographic longitude coordinate |
| Location | VARCHAR | Combined or formatted location information |
| TelephoneNumber | VARCHAR | Customer's phone number |
| EmailAddress | VARCHAR | Customer's email address |
| Username | VARCHAR | Customer's account username |
| Passwd | VARCHAR | Customer's password (encrypted/hashed) |
| DomainName | VARCHAR | Email domain or web domain |
| CCNumber | VARCHAR | Credit card number |
| CCType | VARCHAR | Credit card type (Visa, MasterCard, etc.) |
| CCExpires | VARCHAR | Credit card expiration date |
| CVV2 | VARCHAR | Credit card security code |
| Company | VARCHAR | Customer's employer or company name |
| Occupation | VARCHAR | Customer's job title or profession |
| Vehicle | VARCHAR | Customer's vehicle information |
| NationalID | VARCHAR | National identification number |
| UPS | VARCHAR | UPS shipping identifier or tracking preference |
| GUID | VARCHAR | Globally unique identifier for the customer |
| MothersMaiden | VARCHAR | Mother's maiden name (security question) |
| FeetInches | VARCHAR | Customer's height in feet and inches |
| Centimeters | FLOAT | Customer's height in centimeters |
| Pounds | FLOAT | Customer's weight in pounds |
| Kilograms | VARCHAR | Customer's weight in kilograms |

#### Relationships

- **Inferred:** May link to `RETAIL_TRANSACTIONS` via customer identifier fields
- **Note:** No explicit foreign key relationships detected in recent query patterns

#### Sample Data

*Note: Sample data preview unavailable due to access permissions on this table.*

---

### 2. sales_transaction_line_parquet_ft

#### Business Description

The `sales_transaction_line_parquet_ft` table is a foreign table that stores detailed line-item information for sales transactions. Data is stored in Parquet format on Amazon S3, enabling efficient columnar storage and retrieval for large-scale analytics. Each record represents an individual item within a sales transaction, capturing pricing, quantity, timing, and status information.

#### Schema Information

- **Database:** retail_sample_data
- **Table Name:** sales_transaction_line_parquet_ft
- **Table Type:** Foreign Table (Parquet on S3)
- **Column Count:** 14

#### Columns

| Column Name | Data Type | Business Description |
|-------------|-----------|---------------------|
| SalesTranId | INTEGER | Unique identifier for the parent sales transaction |
| SalesTranLineNum | SMALLINT | Line number within the transaction (for multi-item orders) |
| ItemId | BIGINT | Unique identifier for the product/item sold |
| ItemQty | SMALLINT | Quantity of items purchased |
| UnitSellingPriceAmt | DECIMAL | Selling price per unit |
| UnitCostAmt | DECIMAL | Cost per unit (for margin calculations) |
| TranLineStatusCd | CHAR | Status code for the transaction line (e.g., 'R' for Regular) |
| TranLineSalesTypeCd | CHAR | Type of sale (e.g., 'REGULAR') |
| SalesTranLineStartDttm | TIMESTAMP | Start timestamp of the transaction line |
| SalesTranLineEndDttm | TIMESTAMP | End timestamp of the transaction line |
| TranLineDate | DATE | Date of the transaction |
| locationid | SMALLINT | Numeric identifier for the store/location |
| Location | VARCHAR | S3 path to the source Parquet file |
| dssupdatetime | BYTEINT | Data synchronization update timestamp indicator |

#### Relationships

- **SalesTranId:** Links to parent transaction records
- **ItemId:** Links to product/item master data
- **locationid:** Links to store/location master data

#### Sample Data

| SalesTranId | SalesTranLineNum | ItemId | ItemQty | UnitSellingPriceAmt | UnitCostAmt | TranLineStatusCd | TranLineDate | locationid |
|-------------|------------------|--------|---------|---------------------|-------------|------------------|--------------|------------|
| 5000028 | 9 | 7535511244 | 1 | 1.99 | 1.19 | R | 2009-01-03 | 151 |
| 6000157 | 9 | 4770 | 2 | 1.50 | 0.98 | R | 2009-01-03 | 101 |
| 10000203 | 31 | 4124440025 | 1 | 2.00 | 1.76 | R | 2007-11-17 | 115 |
| 7000357 | 6 | 9396651052 | 1 | 1.99 | 1.49 | R | 2007-11-17 | 101 |
| 30000007 | 9 | 2840004172 | 1 | 2.50 | 2.44 | R | 2007-12-09 | 133 |

---

### 3. RETAIL_TRANSACTIONS

#### Business Description

The `RETAIL_TRANSACTIONS` table captures comprehensive retail transaction data including order details, payment information, customer feedback, and operational metrics. This table supports sales analytics, customer behavior analysis, coupon effectiveness tracking, and operational performance monitoring.

#### Schema Information

- **Database:** retail_sample_data
- **Table Name:** RETAIL_TRANSACTIONS
- **Column Count:** 15

#### Columns

| Column Name | Data Type | Business Description |
|-------------|-----------|---------------------|
| ID | INTEGER | Primary key - unique transaction record identifier |
| TXNID | VARCHAR | Business transaction identifier (alphanumeric code) |
| CREATED_AT | TIMESTAMP | Date and time when the transaction was created |
| CUSTOMER_ID | INTEGER | Foreign key to customer records |
| CUSTOMERNAME | VARCHAR | Customer's full name (denormalized) |
| STORE_ID | INTEGER | Identifier for the store where transaction occurred |
| PRODUCT_ID | INTEGER | Identifier for the product purchased |
| AMOUNT | DECIMAL | Total transaction amount |
| GROSSMARGIN | DECIMAL | Gross profit margin on the transaction |
| PAYMENTTYPE | VARCHAR | Payment method (Cash, Credit Card, Debit Card, Paypal, Google Pay, Stripe) |
| ORDERTYPE | VARCHAR | Order channel (in-store, drive-thru, call-in) |
| COUPONCODE | VARCHAR | Promotional coupon code used (if any) |
| COUPONTYPE | VARCHAR | Type of coupon (National, Regional, One-time Personal) |
| CUSTOMERREVIEW | INTEGER | Customer satisfaction rating (1-5 scale) |
| SERVINGTIME | INTEGER | Time to serve the customer (in seconds) |

#### Relationships

- **CUSTOMER_ID:** Links to customer master data (potentially `ev_customers`)
- **STORE_ID:** Links to store/location master data
- **PRODUCT_ID:** Links to product catalog

#### Sample Data

| ID | TXNID | CREATED_AT | CUSTOMERNAME | AMOUNT | PAYMENTTYPE | ORDERTYPE | COUPONCODE | CUSTOMERREVIEW |
|----|-------|------------|--------------|--------|-------------|-----------|------------|----------------|
| 33788742 | YUGFPCSPAH | 2018-08-22 12:56:04 | Frank Mackenzie | 8.12 | Debit Card | in-store | None | 2 |
| 34222621 | AEAPWSCT2P | 2019-09-09 10:16:57 | Lucas Peters | 7.14 | Stripe | drive-thru | BUY5GET1 | 1 |
| 38132489 | H9B59SEM6R | 2018-07-14 16:05:36 | Luke Sanderson | 2.12 | Paypal | call-in | BOGO | 5 |
| 35990031 | U3Y7LZHGB5 | 2019-05-31 14:31:28 | Michelle Hodges | 2.14 | Google Pay | call-in | BUY5GET1 | 1 |
| 38192258 | 02NQA3K81Q | 2018-08-28 15:05:28 | Joshua Marshall | 7.70 | Cash | call-in | BUY5GET1 | 3 |

---

## Entity Relationship Diagram (Conceptual)

```
+------------------+       +---------------------------+
|   ev_customers   |       | sales_transaction_line_   |
|------------------|       |      parquet_ft           |
| Id (PK)          |       |---------------------------|
| GivenName        |       | SalesTranId               |
| Surname          |       | SalesTranLineNum          |
| ...              |       | ItemId                    |
+--------+---------+       | ItemQty                   |
         |                 | UnitSellingPriceAmt       |
         |                 | locationid                |
         | (inferred)      | ...                       |
         |                 +---------------------------+
         v
+------------------+
|RETAIL_TRANSACTIONS|
|------------------|
| ID (PK)          |
| TXNID            |
| CUSTOMER_ID (FK) |-----> ev_customers.Id (inferred)
| STORE_ID         |
| PRODUCT_ID       |
| AMOUNT           |
| ...              |
+------------------+
```

---

## Usage Statistics

No recent query activity has been recorded for tables in this schema. This may indicate:
- The schema is used for batch processing or ETL operations
- Query logging is not enabled for this database
- The tables are primarily used for data storage rather than interactive queries

---

## Data Quality Notes

1. **ev_customers table:**
   - Contains sensitive PII data (credit card numbers, passwords, national IDs)
   - Consider implementing data masking or encryption for sensitive columns
   - Mixed data types for similar attributes (e.g., Kilograms as VARCHAR vs Pounds as FLOAT)

2. **sales_transaction_line_parquet_ft:**
   - Foreign table backed by S3 Parquet files
   - Data spans from 2007 to 2009 based on sample records
   - Status codes appear to use fixed-width character fields with padding

3. **RETAIL_TRANSACTIONS:**
   - Customer name is denormalized (stored directly rather than referenced)
   - Data spans 2018-2019 based on sample records
   - Review scores range from 1-5

---

## Recommended Use Cases

| Use Case | Primary Tables | Key Columns |
|----------|----------------|-------------|
| Customer Segmentation | ev_customers | State, City, Occupation, Gender |
| Sales Performance Analysis | RETAIL_TRANSACTIONS, sales_transaction_line_parquet_ft | AMOUNT, GROSSMARGIN, UnitSellingPriceAmt |
| Coupon Effectiveness | RETAIL_TRANSACTIONS | COUPONCODE, COUPONTYPE, AMOUNT |
| Operational Efficiency | RETAIL_TRANSACTIONS | SERVINGTIME, ORDERTYPE |
| Geographic Analysis | ev_customers, RETAIL_TRANSACTIONS | Latitude, Longitude, STORE_ID |

---

## Document History

| Date | Version | Author | Changes |
|------|---------|--------|---------|
| 2026-01-06 | 1.0 | Auto-generated | Initial documentation |
