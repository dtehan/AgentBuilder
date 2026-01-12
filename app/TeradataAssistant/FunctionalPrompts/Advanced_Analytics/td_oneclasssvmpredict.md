# TD_OneClassSVMPredict

## Function Name
**TD_OneClassSVMPredict** - One-Class Support Vector Machine Prediction

**Aliases:** OneClassSVMPredict

## Description

TD_OneClassSVMPredict applies a trained One-Class SVM model to new data for anomaly detection and novelty detection. Unlike standard SVM which learns a decision boundary between two classes, One-Class SVM learns the boundary of normal data and flags observations that fall outside this boundary as anomalies or outliers. This unsupervised approach is particularly valuable when anomalous data is rare or unavailable during training.

**Key Characteristics:**
- **Anomaly Detection**: Identifies outliers and unusual patterns in data
- **Unsupervised Learning**: Trained only on normal data (no labeled anomalies required)
- **Decision Function**: Outputs anomaly score indicating distance from normal data boundary
- **Kernel Methods**: Uses RBF, polynomial, or linear kernels for non-linear boundary detection
- **Contamination Control**: Nu parameter controls expected proportion of outliers
- **Production-Ready**: Optimized for real-time fraud detection, quality control, security monitoring

The function takes a trained One-Class SVM model (from TD_OneClassSVM) and predicts whether new observations are normal (+1) or anomalous (-1).

## When to Use TD_OneClassSVMPredict

**Business Applications:**
- **Fraud Detection**: Identify unusual transactions, account behavior, or insurance claims
- **Network Security**: Detect intrusion attempts, unusual traffic patterns, or cyber attacks
- **Quality Control**: Flag defective products or manufacturing anomalies
- **Predictive Maintenance**: Identify abnormal sensor readings indicating equipment failure
- **Healthcare Monitoring**: Detect abnormal patient vitals or rare disease patterns
- **Credit Risk**: Identify unusual applicant profiles that deviate from normal patterns
- **System Monitoring**: Detect performance anomalies in servers, databases, or applications
- **Supply Chain**: Flag unusual shipment delays or inventory patterns

**Use TD_OneClassSVMPredict When You Need To:**
- Apply a trained One-Class SVM model to new observations
- Score data for anomaly/outlier detection in production
- Identify rare events without labeled anomaly examples
- Detect novelty (new patterns not seen in training)
- Monitor systems for unusual behavior
- Filter outliers before further analysis

**Analytical Use Cases:**
- Real-time fraud scoring
- Equipment health monitoring
- Network intrusion detection
- Data quality validation
- Rare event prediction
- Novelty detection in streaming data

## Syntax

```sql
SELECT * FROM TD_OneClassSVMPredict (
    ON { table | view | (query) } AS InputTable PARTITION BY ANY
    ON { table | view | (query) } AS ModelTable DIMENSION
    USING
    IDColumn ('id_column')
    [ Accumulate ('column' [,...]) ]
    [ OutputScoreColumn ('score_column_name') ]
) AS dt;
```

## Required Elements

### InputTable (PARTITION BY ANY)
The table containing data to score. Must include:
- All feature columns used during model training (same names and types)
- ID column for row identification
- Numeric features (One-Class SVM operates on continuous variables)

### ModelTable (DIMENSION)
The trained One-Class SVM model table produced by TD_OneClassSVM function. Contains:
- Support vectors (examples that define the decision boundary)
- Coefficients for each support vector
- Kernel parameters (type, gamma, etc.)
- Model hyperparameters (nu)

### IDColumn
Specifies the column that uniquely identifies each row in InputTable.

**Syntax:** `IDColumn('column_name')`

**Example:**
```sql
IDColumn('transaction_id')
```

## Optional Elements

### Accumulate
Specifies columns from InputTable to include in output (pass-through columns).

**Syntax:** `Accumulate('column1', 'column2', ...)`

**Example:**
```sql
Accumulate('transaction_id', 'customer_id', 'amount', 'timestamp')
```

### OutputScoreColumn
Name for the output column containing the anomaly score (decision function value).

**Syntax:** `OutputScoreColumn('score_column_name')`

**Default:** If not specified, the score column will be named 'score'

**Score Interpretation:**
- **Positive scores (> 0)**: Normal observations (inside decision boundary)
- **Negative scores (< 0)**: Anomalies (outside decision boundary)
- **Magnitude**: Distance from boundary - larger magnitude indicates more extreme

**Example:**
```sql
OutputScoreColumn('anomaly_score')
```

## Input Schema

### InputTable
| Column | Data Type | Description |
|--------|-----------|-------------|
| id_column | INTEGER, VARCHAR | Unique identifier for each row |
| feature_1 | NUMERIC | First feature (same as training) |
| feature_2 | NUMERIC | Second feature (same as training) |
| ... | NUMERIC | Additional features (must match training data) |
| accumulate_cols | ANY | Optional columns to pass through |

**Requirements:**
- All feature columns from training must be present
- Column names must match training data exactly
- Numeric data types for features
- No NULL values in features (handle missing values before prediction)
- Features should be scaled if scaling was applied during training

### ModelTable
Standard output from TD_OneClassSVM function containing:
- Support vectors
- Dual coefficients
- Kernel specification and parameters
- Intercept term
- Nu parameter

## Output Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| id_column | Same as input | Row identifier from InputTable |
| prediction | INTEGER | Predicted class: +1 (normal) or -1 (anomaly) |
| score_column | DOUBLE PRECISION | Anomaly score (decision function value) |
| accumulate_cols | Same as input | Pass-through columns if specified |

**Notes:**
- **prediction**: +1 indicates normal, -1 indicates anomaly
- **score**: Positive values are normal, negative values are anomalies
- **Threshold tuning**: Adjust decision threshold on score column for business needs
- **Ranking**: Sort by score ascending to prioritize most anomalous observations first

## Code Examples

### Example 1: Credit Card Fraud Detection - Basic

**Business Context:** A credit card company trains One-Class SVM on normal transaction patterns and flags potentially fraudulent transactions.

```sql
-- Train One-Class SVM on normal transactions only
CREATE TABLE fraud_ocsvm_model AS (
    SELECT * FROM TD_OneClassSVM (
        ON normal_transactions AS InputTable
        USING
        InputColumns ('amount', 'merchant_category', 'distance_from_home',
                      'transaction_hour', 'days_since_last_transaction')
        Nu (0.05)  -- Expect 5% of data to be outliers
        Kernel ('rbf')
        Gamma (0.1)
    ) AS dt
) WITH DATA;

-- Score new transactions
SELECT * FROM TD_OneClassSVMPredict (
    ON new_transactions AS InputTable PARTITION BY ANY
    ON fraud_ocsvm_model AS ModelTable DIMENSION
    USING
    IDColumn ('transaction_id')
    OutputScoreColumn ('anomaly_score')
    Accumulate ('customer_id', 'amount', 'merchant_name', 'transaction_time')
) AS dt
ORDER BY anomaly_score ASC;  -- Most anomalous first

/*
Sample Output:
transaction_id | prediction | anomaly_score | customer_id | amount  | merchant_name      | transaction_time
---------------|------------|---------------|-------------|---------|--------------------|-----------------
TXN9045        | -1         | -2.45         | C12345      | 3850.00 | Electronics Store  | 2024-01-15 03:22
TXN9082        | -1         | -1.87         | C67890      | 2200.00 | Online Retailer    | 2024-01-15 02:45
TXN9021        | 1          | 0.52          | C45678      | 125.50  | Grocery Store      | 2024-01-15 10:30
TXN9067        | 1          | 1.23          | C23456      | 42.30   | Coffee Shop        | 2024-01-15 08:15

Interpretation:
- TXN9045: Anomaly score -2.45 → Highly suspicious, block transaction
- TXN9082: Anomaly score -1.87 → Unusual pattern, require additional verification
- TXN9021: Anomaly score 0.52 → Normal transaction, slightly close to boundary
- TXN9067: Anomaly score 1.23 → Typical transaction, auto-approve
*/

-- Business Impact:
-- Fraud detection rate improved by 43% compared to rule-based system
-- Reduced false positives by 35%
-- Real-time fraud detection with <100ms latency
```

### Example 2: Network Intrusion Detection with Custom Thresholds

**Business Context:** Monitor network traffic for security threats by detecting unusual connection patterns.

```sql
-- Train One-Class SVM on normal network traffic
CREATE TABLE network_ocsvm_model AS (
    SELECT * FROM TD_OneClassSVM (
        ON normal_network_traffic AS InputTable
        USING
        InputColumns ('packets_per_second', 'bytes_per_packet', 'connection_duration',
                      'unique_destinations', 'port_entropy', 'protocol_distribution')
        Nu (0.02)  -- Very low expected outlier rate for security
        Kernel ('rbf')
        Gamma (0.05)
    ) AS dt
) WITH DATA;

-- Detect intrusions in real-time traffic
SELECT * FROM TD_OneClassSVMPredict (
    ON live_network_traffic AS InputTable PARTITION BY ANY
    ON network_ocsvm_model AS ModelTable DIMENSION
    USING
    IDColumn ('connection_id')
    OutputScoreColumn ('anomaly_score')
    Accumulate ('source_ip', 'dest_ip', 'timestamp', 'protocol')
) AS dt
ORDER BY anomaly_score ASC;  -- Most suspicious first

/*
Sample Output:
connection_id | prediction | anomaly_score | source_ip      | dest_ip        | timestamp           | protocol
--------------|------------|---------------|----------------|----------------|---------------------|----------
CONN5012      | -1         | -4.23         | 192.168.1.45   | 10.0.0.15      | 2024-01-15 14:22:05 | TCP
CONN5089      | -1         | -2.15         | 192.168.1.78   | 10.0.0.22      | 2024-01-15 14:22:08 | UDP
CONN5034      | -1         | -0.85         | 192.168.1.123  | 10.0.0.45      | 2024-01-15 14:22:10 | TCP
CONN5101      | 1          | 0.45          | 192.168.1.55   | 10.0.0.12      | 2024-01-15 14:22:11 | HTTP

Interpretation:
- CONN5012: Score -4.23 → Critical threat, immediate investigation (possible DDoS)
- CONN5089: Score -2.15 → High priority alert (unusual protocol behavior)
- CONN5034: Score -0.85 → Moderate alert, monitor closely
- CONN5101: Score 0.45 → Normal traffic
*/

-- Create tiered alert system with custom thresholds
CREATE TABLE security_alerts AS (
    SELECT
        connection_id,
        source_ip,
        dest_ip,
        protocol,
        anomaly_score,
        CASE
            WHEN anomaly_score <= -3.0 THEN 'CRITICAL_BLOCK'
            WHEN anomaly_score <= -2.0 THEN 'HIGH_INVESTIGATE'
            WHEN anomaly_score <= -1.0 THEN 'MEDIUM_MONITOR'
            WHEN anomaly_score <= -0.5 THEN 'LOW_LOG'
            ELSE 'NORMAL'
        END AS threat_level,
        CASE
            WHEN anomaly_score <= -3.0 THEN 'Block IP, escalate to security team'
            WHEN anomaly_score <= -2.0 THEN 'Detailed packet inspection'
            WHEN anomaly_score <= -1.0 THEN 'Enhanced logging, watch for patterns'
            WHEN anomaly_score <= -0.5 THEN 'Log for analysis'
            ELSE 'No action'
        END AS recommended_action
    FROM TD_OneClassSVMPredict (
        ON live_network_traffic AS InputTable PARTITION BY ANY
        ON network_ocsvm_model AS ModelTable DIMENSION
        USING
        IDColumn ('connection_id')
        OutputScoreColumn ('anomaly_score')
        Accumulate ('source_ip', 'dest_ip', 'protocol')
    ) AS dt
    WHERE anomaly_score <= -0.5  -- Only create alerts for anomalies
) WITH DATA;

-- Business Impact:
-- Detected 3 security incidents that bypassed traditional signature-based systems
-- Reduced mean time to detect (MTTD) from 4 hours to 12 minutes
-- 89% reduction in false positive alerts compared to rule-based IDS
```

### Example 3: Manufacturing Quality Control

**Business Context:** Detect defective products on assembly line by identifying sensor readings that deviate from normal manufacturing patterns.

```sql
-- Train model on quality products only
CREATE TABLE quality_ocsvm_model AS (
    SELECT * FROM TD_OneClassSVM (
        ON quality_products_training AS InputTable
        USING
        InputColumns ('temperature', 'pressure', 'vibration', 'torque',
                      'cycle_time', 'power_consumption')
        Nu (0.03)  -- Expect 3% defect rate
        Kernel ('rbf')
        Gamma (0.2)
    ) AS dt
) WITH DATA;

-- Score products in real-time
SELECT * FROM TD_OneClassSVMPredict (
    ON production_line AS InputTable PARTITION BY ANY
    ON quality_ocsvm_model AS ModelTable DIMENSION
    USING
    IDColumn ('product_id')
    OutputScoreColumn ('quality_score')
    Accumulate ('production_time', 'line_number', 'operator_id')
) AS dt
ORDER BY quality_score ASC;  -- Potential defects first

/*
Sample Output:
product_id | prediction | quality_score | production_time     | line_number | operator_id
-----------|------------|---------------|---------------------|-------------|------------
PROD8821   | -1         | -3.12         | 2024-01-15 10:05:23 | LINE_A      | OP_042
PROD8845   | -1         | -1.45         | 2024-01-15 10:07:41 | LINE_B      | OP_018
PROD8802   | 1          | 0.78          | 2024-01-15 10:03:15 | LINE_A      | OP_042
PROD8834   | 1          | 1.95          | 2024-01-15 10:06:52 | LINE_C      | OP_025

Interpretation:
- PROD8821: Quality score -3.12 → Reject, full inspection
- PROD8845: Quality score -1.45 → Flag for additional testing
- PROD8802: Quality score 0.78 → Pass, near threshold - spot check
- PROD8834: Quality score 1.95 → Pass, high confidence
*/

-- Analyze defect patterns by line and operator
SELECT
    line_number,
    operator_id,
    COUNT(*) AS total_products,
    SUM(CASE WHEN prediction = -1 THEN 1 ELSE 0 END) AS defects_detected,
    AVG(quality_score) AS avg_quality_score,
    MIN(quality_score) AS worst_quality_score
FROM TD_OneClassSVMPredict (
    ON production_line AS InputTable PARTITION BY ANY
    ON quality_ocsvm_model AS ModelTable DIMENSION
    USING
    IDColumn ('product_id')
    OutputScoreColumn ('quality_score')
    Accumulate ('line_number', 'operator_id')
) AS dt
GROUP BY line_number, operator_id
HAVING defects_detected > 0
ORDER BY defects_detected DESC;

-- Business Impact:
-- Reduced customer complaints about defective products by 68%
-- Caught defects 15 minutes earlier in production process
-- Estimated annual savings: $1.8M from reduced warranty claims
```

### Example 4: Predictive Maintenance for Equipment

**Business Context:** Predict equipment failures by detecting anomalous sensor patterns before catastrophic failure occurs.

```sql
-- Train on normal equipment operation
CREATE TABLE equipment_ocsvm_model AS (
    SELECT * FROM TD_OneClassSVM (
        ON normal_equipment_data AS InputTable
        USING
        InputColumns ('bearing_temp', 'motor_vibration', 'oil_pressure',
                      'rpm', 'power_draw', 'coolant_temp')
        Nu (0.01)  -- Expect rare failures
        Kernel ('rbf')
        Gamma (0.15)
    ) AS dt
) WITH DATA;

-- Monitor equipment health in real-time
CREATE TABLE equipment_health_monitoring AS (
    SELECT * FROM TD_OneClassSVMPredict (
        ON equipment_sensor_stream AS InputTable PARTITION BY ANY
        ON equipment_ocsvm_model AS ModelTable DIMENSION
        USING
        IDColumn ('sensor_reading_id')
        OutputScoreColumn ('health_score')
        Accumulate ('equipment_id', 'timestamp', 'operating_hours', 'last_maintenance')
    ) AS dt
) WITH DATA;

-- Generate maintenance alerts
SELECT
    equipment_id,
    timestamp,
    operating_hours,
    last_maintenance,
    health_score,
    CASE
        WHEN health_score <= -2.5 THEN 'IMMEDIATE_SHUTDOWN'
        WHEN health_score <= -1.5 THEN 'SCHEDULE_URGENT_MAINTENANCE'
        WHEN health_score <= -0.8 THEN 'PLAN_MAINTENANCE_NEXT_WEEK'
        WHEN health_score <= -0.3 THEN 'MONITOR_CLOSELY'
        ELSE 'HEALTHY'
    END AS equipment_status,
    DATEDIFF(DAY, last_maintenance, timestamp) AS days_since_maintenance
FROM equipment_health_monitoring
WHERE health_score <= -0.3  -- Only flag equipment with anomalies
ORDER BY health_score ASC;

/*
Sample Output:
equipment_id | timestamp           | operating_hours | last_maintenance | health_score | equipment_status              | days_since_maint
-------------|---------------------|-----------------|------------------|--------------|-------------------------------|-----------------
EQ_A042      | 2024-01-15 14:30:00 | 8750            | 2023-10-15       | -3.45        | IMMEDIATE_SHUTDOWN            | 92
EQ_B123      | 2024-01-15 14:30:00 | 6200            | 2023-12-01       | -1.92        | SCHEDULE_URGENT_MAINTENANCE   | 45
EQ_C089      | 2024-01-15 14:30:00 | 4100            | 2023-11-20       | -0.95        | PLAN_MAINTENANCE_NEXT_WEEK    | 56

Interpretation:
- EQ_A042: Critical failure imminent → Shut down immediately
- EQ_B123: Abnormal vibration pattern → Schedule maintenance within 48 hours
- EQ_C089: Early warning signs → Plan maintenance next week
*/

-- Calculate ROI of predictive maintenance
SELECT
    COUNT(DISTINCT equipment_id) AS equipment_monitored,
    SUM(CASE WHEN health_score <= -1.5 THEN 1 ELSE 0 END) AS failures_prevented,
    SUM(CASE WHEN health_score <= -1.5 THEN 1 ELSE 0 END) * 75000 AS estimated_cost_savings
FROM equipment_health_monitoring
WHERE prediction = -1;

-- Business Impact:
-- Prevented 12 equipment failures (estimated $900K in avoided downtime)
-- Reduced unplanned downtime by 78%
-- Improved equipment lifespan by 15% through proactive maintenance
```

### Example 5: Healthcare Patient Monitoring

**Business Context:** Detect abnormal patient vital signs that may indicate medical emergencies requiring immediate intervention.

```sql
-- Train on stable patients' vital signs
CREATE TABLE patient_ocsvm_model AS (
    SELECT * FROM TD_OneClassSVM (
        ON stable_patients_vitals AS InputTable
        USING
        InputColumns ('heart_rate', 'blood_pressure_systolic', 'blood_pressure_diastolic',
                      'respiratory_rate', 'oxygen_saturation', 'temperature')
        Nu (0.02)  -- 2% of readings may be abnormal
        Kernel ('rbf')
        Gamma (0.1)
    ) AS dt
) WITH DATA;

-- Monitor ICU patients in real-time
SELECT * FROM TD_OneClassSVMPredict (
    ON icu_patient_vitals AS InputTable PARTITION BY ANY
    ON patient_ocsvm_model AS ModelTable DIMENSION
    USING
    IDColumn ('reading_id')
    OutputScoreColumn ('health_score')
    Accumulate ('patient_id', 'patient_name', 'timestamp', 'room_number')
) AS dt
ORDER BY health_score ASC;  -- Most concerning readings first

/*
Sample Output:
reading_id | prediction | health_score | patient_id | patient_name   | timestamp           | room_number
-----------|------------|--------------|------------|----------------|---------------------|------------
READ5012   | -1         | -4.15        | PT1042     | John Anderson  | 2024-01-15 14:22:00 | ICU_205
READ5089   | -1         | -2.87        | PT1089     | Mary Johnson   | 2024-01-15 14:22:30 | ICU_210
READ5045   | -1         | -1.23        | PT1023     | David Lee      | 2024-01-15 14:23:00 | ICU_208
READ5101   | 1          | 0.85         | PT1067     | Sarah Kim      | 2024-01-15 14:23:30 | ICU_212

Interpretation:
- READ5012: Score -4.15 → Critical alert, immediate physician notification
- READ5089: Score -2.87 → High alert, nurse assessment within 5 minutes
- READ5045: Score -1.23 → Moderate alert, monitor closely, reassess in 15 minutes
- READ5101: Score 0.85 → Stable vital signs
*/

-- Generate clinical alerts
CREATE TABLE clinical_alert_queue AS (
    SELECT
        patient_id,
        patient_name,
        room_number,
        timestamp,
        health_score,
        CASE
            WHEN health_score <= -3.5 THEN 'CODE_BLUE'
            WHEN health_score <= -2.5 THEN 'RAPID_RESPONSE'
            WHEN health_score <= -1.5 THEN 'NURSE_ASSESSMENT'
            WHEN health_score <= -0.8 THEN 'ENHANCED_MONITORING'
            ELSE 'ROUTINE'
        END AS alert_level,
        CASE
            WHEN health_score <= -3.5 THEN 'Activate code blue team immediately'
            WHEN health_score <= -2.5 THEN 'Physician at bedside within 5 minutes'
            WHEN health_score <= -1.5 THEN 'Nurse assessment within 15 minutes'
            WHEN health_score <= -0.8 THEN 'Increase vital sign frequency to q15min'
            ELSE 'Continue routine monitoring'
        END AS recommended_action
    FROM TD_OneClassSVMPredict (
        ON icu_patient_vitals AS InputTable PARTITION BY ANY
        ON patient_ocsvm_model AS ModelTable DIMENSION
        USING
        IDColumn ('reading_id')
        OutputScoreColumn ('health_score')
        Accumulate ('patient_id', 'patient_name', 'room_number', 'timestamp')
    ) AS dt
    WHERE health_score <= -0.8  -- Only alert for abnormal vitals
) WITH DATA
ORDER BY health_score ASC, timestamp DESC;

-- Business Impact:
-- Early warning system reduced code blue events by 35%
-- Improved response time to patient deterioration from 45 min to 8 min
-- IMPORTANT: System augments clinical judgment, does not replace it
```

### Example 6: Credit Application Screening

**Business Context:** Flag unusual credit applications that deviate from typical applicant profiles for enhanced review.

```sql
-- Train on approved, performing loans
CREATE TABLE credit_ocsvm_model AS (
    SELECT * FROM TD_OneClassSVM (
        ON good_credit_applicants AS InputTable
        USING
        InputColumns ('income', 'debt_to_income_ratio', 'credit_score',
                      'employment_tenure_months', 'age', 'num_credit_accounts')
        Nu (0.10)  -- Expect 10% of applications to be unusual
        Kernel ('rbf')
        Gamma (0.05)
    ) AS dt
) WITH DATA;

-- Score new applications
SELECT * FROM TD_OneClassSVMPredict (
    ON new_credit_applications AS InputTable PARTITION BY ANY
    ON credit_ocsvm_model AS ModelTable DIMENSION
    USING
    IDColumn ('application_id')
    OutputScoreColumn ('profile_score')
    Accumulate ('applicant_name', 'requested_amount', 'application_date')
) AS dt
ORDER BY profile_score ASC;  -- Most unusual applications first

/*
Sample Output:
application_id | prediction | profile_score | applicant_name    | requested_amount | application_date
---------------|------------|---------------|-------------------|------------------|-----------------
APP9012        | -1         | -2.85         | John Smith        | 75000            | 2024-01-15
APP9045        | -1         | -1.52         | Mary Johnson      | 45000            | 2024-01-15
APP9023        | 1          | 0.42          | David Lee         | 28000            | 2024-01-15
APP9067        | 1          | 1.78          | Sarah Kim         | 15000            | 2024-01-15

Interpretation:
- APP9012: Score -2.85 → Highly unusual profile, manual underwriting required
- APP9045: Score -1.52 → Atypical applicant, enhanced verification
- APP9023: Score 0.42 → Normal profile, automated processing
- APP9067: Score 1.78 → Very typical applicant, expedited approval
*/

-- Route applications based on risk
CREATE TABLE application_routing AS (
    SELECT
        application_id,
        applicant_name,
        requested_amount,
        profile_score,
        CASE
            WHEN profile_score <= -2.0 THEN 'SENIOR_UNDERWRITER'
            WHEN profile_score <= -1.0 THEN 'ENHANCED_VERIFICATION'
            WHEN profile_score <= -0.5 THEN 'STANDARD_REVIEW'
            ELSE 'AUTO_DECISION_ENGINE'
        END AS review_channel,
        CASE
            WHEN profile_score <= -2.0 THEN 'Income verification, employment check, reference calls'
            WHEN profile_score <= -1.0 THEN 'Verify employment and income'
            WHEN profile_score <= -0.5 THEN 'Standard credit check'
            ELSE 'Automated approval/denial based on credit score'
        END AS required_due_diligence
    FROM TD_OneClassSVMPredict (
        ON new_credit_applications AS InputTable PARTITION BY ANY
        ON credit_ocsvm_model AS ModelTable DIMENSION
        USING
        IDColumn ('application_id')
        OutputScoreColumn ('profile_score')
        Accumulate ('applicant_name', 'requested_amount')
    ) AS dt
) WITH DATA;

-- Business Impact:
-- Fraud losses reduced by $620K annually through enhanced screening
-- 72% of applications auto-processed, reducing underwriter workload
-- Approval time for normal applications reduced from 3 days to 2 hours
```

## Common Use Cases

### Security and Fraud
- **Transaction Fraud**: Flag unusual purchases, transfers, or account activity
- **Identity Fraud**: Detect synthetic identities or account takeovers
- **Network Security**: Intrusion detection, DDoS detection, malware activity
- **Insurance Fraud**: Flag suspicious claims based on patterns

### Manufacturing and Quality
- **Quality Control**: Detect defective products on production lines
- **Process Monitoring**: Identify process deviations in manufacturing
- **Predictive Maintenance**: Detect equipment anomalies before failure
- **Supply Chain**: Flag unusual delays, shipments, or inventory patterns

### Healthcare and Life Sciences
- **Patient Monitoring**: Detect abnormal vital signs or lab results
- **Disease Detection**: Identify rare disease patterns
- **Clinical Trial**: Flag unusual patient responses or adverse events
- **Equipment Monitoring**: Detect medical device malfunctions

### IT and Operations
- **System Monitoring**: Detect server, database, or application anomalies
- **Log Analysis**: Identify unusual error patterns or security events
- **Performance Monitoring**: Flag degradation in system performance
- **Data Quality**: Detect corrupted or invalid data

### Finance and Risk
- **Credit Risk**: Identify unusual applicant profiles
- **Market Anomalies**: Detect unusual trading patterns or price movements
- **Regulatory Compliance**: Flag unusual transactions requiring reporting
- **Operational Risk**: Detect process failures or control breakdowns

## Best Practices

### Model Training
1. **Training Data**: Use only normal, high-quality data (no anomalies)
2. **Nu Parameter**: Set based on expected outlier rate (start with 0.05 = 5%)
3. **Feature Scaling**: Always scale features (StandardScaler) for SVM
4. **Kernel Selection**: RBF kernel works well for most cases; try linear for high-dimensional data

### Anomaly Scoring
1. **Use Score Column**: Don't rely solely on binary prediction; use continuous score for ranking
2. **Custom Thresholds**: Adjust decision threshold based on business costs (false positives vs. false negatives)
3. **Score Distribution**: Monitor score distribution over time to detect model drift
4. **Prioritization**: Rank anomalies by score magnitude for investigation priority

### Performance Optimization
1. **Feature Selection**: Remove irrelevant features to improve performance and reduce false positives
2. **Batch Scoring**: Use PARTITION BY ANY for parallel processing of large datasets
3. **Model Size**: Limit support vectors by tuning nu parameter
4. **Periodic Retraining**: Retrain model as "normal" patterns evolve

### Production Deployment
1. **Model Versioning**: Track model versions with training dates
2. **A/B Testing**: Compare model versions before full deployment
3. **Monitoring**: Track anomaly rate, score distribution, and business outcomes
4. **Feedback Loop**: Incorporate confirmed anomalies/false positives into retraining

### Business Integration
1. **Tiered Alerts**: Create multiple alert levels based on score thresholds
2. **Human Review**: Reserve most extreme anomalies for human investigation
3. **Automated Actions**: Auto-block or auto-approve based on clear thresholds
4. **ROI Tracking**: Measure financial impact of catching anomalies

## Related Functions

### Model Training
- **TD_OneClassSVM**: Train One-Class SVM models for anomaly detection (produces ModelTable input)
- **TD_SVMSparse**: Train standard two-class SVM for classification

### Alternative Anomaly Detection
- **TD_KMeans**: Distance-based anomaly detection using clustering
- **TD_IsolationForest**: Tree-based anomaly detection (alternative approach)
- **TD_LOF**: Local Outlier Factor for density-based anomaly detection

### Model Evaluation
- **TD_Silhouette**: Evaluate clustering quality (can validate One-Class SVM on training data)
- **TD_UnivariateStatistics**: Profile normal data characteristics

### Data Preparation
- **TD_ScaleFit/Transform**: Essential for SVM - standardize features before training/prediction
- **TD_SimpleImputeFit/Transform**: Handle missing values
- **TD_OutlierFilterFit/Transform**: Remove extreme outliers before training

### Feature Engineering
- **TD_PolynomialFeaturesFit/Transform**: Create interaction terms for richer anomaly detection
- **TD_PCA**: Reduce dimensionality for high-dimensional data

## Notes and Limitations

### General Limitations
1. **Feature Matching**: All feature columns from training must be present in test data
2. **No Missing Values**: One-Class SVM cannot handle NULLs - preprocess data first
3. **Feature Scaling Required**: SVM is sensitive to feature scales - always standardize
4. **Training Data Quality**: Model quality depends on having clean, normal-only training data

### Model Characteristics
1. **Unsupervised**: No labeled anomalies needed for training (only normal data)
2. **Non-Linear Boundaries**: RBF kernel captures complex normal data shapes
3. **Support Vectors**: Model defined by subset of training examples (support vectors)
4. **Nu Parameter**: Controls trade-off between boundary tightness and outlier tolerance

### Performance Considerations
1. **Training Time**: Can be slow for large training sets (quadratic complexity)
2. **Prediction Speed**: Fast once trained (depends on number of support vectors)
3. **Memory**: Model size determined by number of support vectors
4. **High Dimensions**: Performance can degrade in very high-dimensional spaces (>1000 features)

### Best Use Cases
- **When to Use One-Class SVM**: Anomalies are rare/unavailable, complex non-linear patterns, moderate-dimensional data
- **When to Avoid**: Very high-dimensional data (try PCA first), need interpretability (try Isolation Forest), real-time training required
- **Alternatives**: Consider TD_IsolationForest for faster training, TD_KMeans for interpretability

### Teradata-Specific Notes
1. **UTF8 Support**: ModelTable and InputTable support UTF8 character sets
2. **PARTITION BY ANY**: Enables parallel processing across AMPs
3. **DIMENSION Tables**: ModelTable must be DIMENSION for broadcast to all AMPs
4. **Deterministic**: Same input always produces same output

## Version Information

**Documentation Generated:** November 29, 2025
**Based on:** Teradata Database Analytic Functions Version 17.20
**Function Category:** Machine Learning - Model Scoring (Anomaly Detection)
**Last Updated:** 2025-11-29
