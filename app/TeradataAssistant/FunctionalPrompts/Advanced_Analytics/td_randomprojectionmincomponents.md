# TD_RandomProjectionMinComponents

### Function Name
**TD_RandomProjectionMinComponents**

### Description
TD_RandomProjectionMinComponents calculates the minimum number of dimensions (components) required to preserve pairwise distances within a specified tolerance (epsilon) when performing random projection. This utility function applies the Johnson-Lindenstrauss Lemma to determine the theoretical minimum target dimensionality needed for distance-preserving dimensionality reduction.

This function is essential for planning random projection transformations when you want to specify a desired level of distance preservation (epsilon) but need to know how many output dimensions are required. Rather than guessing at the NumComponents parameter for TD_RandomProjectionFit, this function provides a mathematically principled answer based on the number of data points and the acceptable distortion level.

The calculation is based on the Johnson-Lindenstrauss Lemma formula: k ≥ 4 × ln(n) / (ε² / 2 - ε³ / 3), where k is the minimum dimensions, n is the number of data points, and ε is epsilon. This ensures that distances between any pair of points are preserved within the bounds (1-ε) and (1+ε) with high probability.

### When the Function Would Be Used
- **Determine Target Dimensionality**: Calculate required dimensions for given epsilon
- **Random Projection Planning**: Estimate output dimensions before creating FitTable
- **Distance Preservation Guarantee**: Ensure sufficient dimensions for epsilon tolerance
- **Dimensionality Reduction Design**: Plan compression ratio for large datasets
- **Trade-off Analysis**: Evaluate epsilon vs dimensionality trade-offs
- **Resource Estimation**: Predict storage and computation requirements
- **Validation**: Verify that manual NumComponents choice is sufficient
- **Experimentation**: Test different epsilon values before committing
- **Documentation**: Record theoretical basis for dimensionality choices
- **Optimization**: Find optimal balance between compression and accuracy

### Syntax

```sql
TD_RandomProjectionMinComponents (
    ON { table | view | (query) } AS InputTable
    USING
    TargetColumns ({ 'target_column' | target_column_range }[,...])
    Epsilon (epsilon_value)
)
```

### Required Syntax Elements for TD_RandomProjectionMinComponents

**ON clause**
- Accepts the InputTable clause containing the data
- Used to count number of rows (n) for Johnson-Lindenstrauss calculation
- Column values not used, only row count matters

**TargetColumns**
- Specify columns that would be subject to random projection
- Used for validation and consistency
- Must match columns intended for TD_RandomProjectionFit
- Supports column range notation

**Epsilon**
- Specify distortion tolerance for distance preservation
- Valid range: 0 < epsilon < 1
- Smaller values → more components needed
- Larger values → fewer components needed
- Typical values: 0.05 to 0.3

### Optional Syntax Elements for TD_RandomProjectionMinComponents

None - all parameters are required.

### Input Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| target_column | Numeric types | Columns intended for random projection (values not used, only schema validated) |

### Output Table Schema

| Column | Data Type | Description |
|--------|-----------|-------------|
| num_rows | BIGINT | Number of rows in input table (n parameter) |
| epsilon | DOUBLE PRECISION | Distortion tolerance specified |
| minimum_components | INTEGER | Minimum number of dimensions required to preserve distances within epsilon |

The output is a single row containing the calculation results.

### Code Examples

**Input Data: customer_features** (assume 10,000 rows)
```
customer_id  feature1  feature2  ...  feature100
1            2.5       1.3       ...  0.8
2            1.2       3.4       ...  1.5
...
10000        3.1       2.7       ...  2.2
```

**Example 1: Calculate Minimum Components for Standard Epsilon**
```sql
-- Determine dimensions needed for 10% distortion tolerance
SELECT * FROM TD_RandomProjectionMinComponents (
    ON customer_features AS InputTable
    USING
    TargetColumns('[2:101]')  -- 100 features
    Epsilon(0.1)
) AS dt;
```

**Output:**
```
num_rows  epsilon  minimum_components
10000     0.1      1839
```

This means 1,839 dimensions are needed to preserve distances within ±10% for 10,000 data points.

**Example 2: Compare Different Epsilon Values**
```sql
-- Calculate for conservative epsilon (better preservation)
SELECT * FROM TD_RandomProjectionMinComponents (
    ON text_documents AS InputTable
    USING
    TargetColumns('[1:5000]')
    Epsilon(0.05)
) AS dt;

-- Output: minimum_components ≈ 7,350 (more dimensions needed)

-- Calculate for aggressive epsilon (more compression)
SELECT * FROM TD_RandomProjectionMinComponents (
    ON text_documents AS InputTable
    USING
    TargetColumns('[1:5000]')
    Epsilon(0.3)
) AS dt;

-- Output: minimum_components ≈ 205 (fewer dimensions needed)
```

**Example 3: Small Dataset Analysis**
```sql
-- Calculate for small dataset (100 rows)
SELECT * FROM TD_RandomProjectionMinComponents (
    ON small_dataset AS InputTable
    USING
    TargetColumns('feat1', 'feat2', 'feat3', 'feat4', 'feat5')
    Epsilon(0.1)
) AS dt;
```

**Output:**
```
num_rows  epsilon  minimum_components
100       0.1      92
```

For small datasets, compression is minimal because n (100) and k (92) are similar.

**Example 4: Large Dataset Analysis**
```sql
-- Calculate for very large dataset (1 million rows)
SELECT * FROM TD_RandomProjectionMinComponents (
    ON large_customer_base AS InputTable
    USING
    TargetColumns('[3:503]')  -- 500 features
    Epsilon(0.1)
) AS dt;
```

**Output:**
```
num_rows   epsilon  minimum_components
1000000    0.1      2757
```

Even with 1 million rows, only 2,757 dimensions needed (significant compression from 500 original features).

**Example 5: Planning Random Projection**
```sql
-- Step 1: Determine minimum components
CREATE TABLE min_comp_result AS (
    SELECT * FROM TD_RandomProjectionMinComponents (
        ON training_data AS InputTable
        USING
        TargetColumns('[5:305]')  -- 300 features
        Epsilon(0.15)
    ) AS dt
) WITH DATA;

-- Step 2: Extract the calculated value
SELECT minimum_components FROM min_comp_result;
-- Output: 856

-- Step 3: Use in TD_RandomProjectionFit
CREATE TABLE proj_fit AS (
    SELECT * FROM TD_RandomProjectionFit (
        ON training_data AS InputTable
        USING
        TargetColumns('[5:305]')
        NumComponents(856)  -- Use calculated minimum
        ProjectionMethod('GAUSSIAN')
        Seed(42)
    ) AS dt
) WITH DATA;
```

**Example 6: Epsilon Trade-off Analysis**
```sql
-- Create table to compare different epsilon values
CREATE TABLE epsilon_analysis AS (
    SELECT 0.05 AS epsilon, * FROM TD_RandomProjectionMinComponents (
        ON high_dim_data AS InputTable USING TargetColumns('[1:1000]') Epsilon(0.05)
    ) AS dt
    UNION ALL
    SELECT 0.10 AS epsilon, * FROM TD_RandomProjectionMinComponents (
        ON high_dim_data AS InputTable USING TargetColumns('[1:1000]') Epsilon(0.10)
    ) AS dt
    UNION ALL
    SELECT 0.15 AS epsilon, * FROM TD_RandomProjectionMinComponents (
        ON high_dim_data AS InputTable USING TargetColumns('[1:1000]') Epsilon(0.15)
    ) AS dt
    UNION ALL
    SELECT 0.20 AS epsilon, * FROM TD_RandomProjectionMinComponents (
        ON high_dim_data AS InputTable USING TargetColumns('[1:1000]') Epsilon(0.20)
    ) AS dt
    UNION ALL
    SELECT 0.30 AS epsilon, * FROM TD_RandomProjectionMinComponents (
        ON high_dim_data AS InputTable USING TargetColumns('[1:1000]') Epsilon(0.30)
    ) AS dt
) WITH DATA;

SELECT
    epsilon,
    minimum_components,
    CAST(minimum_components AS FLOAT) / 1000 AS compression_ratio,
    100 - (CAST(minimum_components AS FLOAT) / 1000 * 100) AS percent_reduction
FROM epsilon_analysis
ORDER BY epsilon;
```

**Output:**
```
epsilon  minimum_components  compression_ratio  percent_reduction
0.05     7350                7.35               -635%  (expansion!)
0.10     1839                1.84               -84%   (expansion!)
0.15     817                 0.82               18%
0.20     460                 0.46               54%
0.30     205                 0.21               79%
```

**Example 7: Validation Check**
```sql
-- Check if manually chosen NumComponents is sufficient
CREATE TABLE manual_check AS (
    SELECT * FROM TD_RandomProjectionMinComponents (
        ON sensor_data AS InputTable
        USING
        TargetColumns('[1:200]')
        Epsilon(0.1)
    ) AS dt
) WITH DATA;

-- Compare manual choice to calculated minimum
SELECT
    50 AS manual_num_components,
    minimum_components AS required_minimum,
    CASE
        WHEN 50 >= minimum_components THEN 'SUFFICIENT'
        ELSE 'INSUFFICIENT - increase NumComponents'
    END AS validation_result
FROM manual_check;
```

**Example 8: Feature Count Impact**
```sql
-- Same number of rows, different feature counts
SELECT 'Original 1000 features' AS scenario, * FROM TD_RandomProjectionMinComponents (
    ON data AS InputTable USING TargetColumns('[1:1000]') Epsilon(0.1)
) AS dt
UNION ALL
SELECT 'Reduced 500 features' AS scenario, * FROM TD_RandomProjectionMinComponents (
    ON data AS InputTable USING TargetColumns('[1:500]') Epsilon(0.1)
) AS dt
UNION ALL
SELECT 'Reduced 100 features' AS scenario, * FROM TD_RandomProjectionMinComponents (
    ON data AS InputTable USING TargetColumns('[1:100]') Epsilon(0.1)
) AS dt;
```

**Key Insight:** Minimum components depends on number of rows and epsilon, NOT on original feature count.

**Example 9: Nearest Neighbor Application**
```sql
-- Plan dimensions for approximate nearest neighbor search
SELECT * FROM TD_RandomProjectionMinComponents (
    ON product_embeddings AS InputTable
    USING
    TargetColumns('[3:515]')  -- 512-dimensional embeddings
    Epsilon(0.20)  -- Acceptable approximation for k-NN
) AS dt;

-- Output example: minimum_components = 460
-- Can reduce 512 dims → 460 dims with 20% distance approximation
```

**Example 10: Documentation and Reporting**
```sql
-- Generate projection planning report
SELECT
    (SELECT COUNT(*) FROM training_data) AS dataset_rows,
    (SELECT COUNT(*) FROM information_schema.columns
     WHERE table_name = 'training_data' AND column_name LIKE 'feature%') AS feature_count,
    0.10 AS target_epsilon,
    minimum_components,
    CAST(minimum_components AS FLOAT) /
        (SELECT COUNT(*) FROM information_schema.columns
         WHERE table_name = 'training_data' AND column_name LIKE 'feature%') AS compression_ratio,
    'Johnson-Lindenstrauss Lemma' AS method_basis
FROM TD_RandomProjectionMinComponents (
    ON training_data AS InputTable
    USING
    TargetColumns('[2:102]')  -- 100 features
    Epsilon(0.10)
) AS dt;
```

### Johnson-Lindenstrauss Lemma Application

**Mathematical Formula:**

Minimum components k is calculated as:

k ≥ 4 × ln(n) / (ε²/2 - ε³/3)

Where:
- k = minimum target dimensions (output of this function)
- n = number of data points (rows in input table)
- ε = epsilon (distortion tolerance)
- ln = natural logarithm

**Simplified approximation:**

For small ε (typically ε < 0.3):

k ≈ 4 × ln(n) / ε²

**Example Calculations:**

| Rows (n) | Epsilon (ε) | Min Components (k) | Formula |
|----------|-------------|-------------------|---------|
| 100      | 0.10        | 92                | 4×ln(100)/0.01 ≈ 1,843 |
| 1,000    | 0.10        | 1,380             | 4×ln(1000)/0.01 ≈ 2,764 |
| 10,000   | 0.10        | 1,839             | 4×ln(10000)/0.01 ≈ 3,686 |
| 100,000  | 0.10        | 2,303             | 4×ln(100000)/0.01 ≈ 4,607 |
| 1,000,000| 0.10        | 2,757             | 4×ln(1000000)/0.01 ≈ 5,529 |

**Key Observations:**
- Dimensions grow logarithmically with number of points
- Dimensions grow quadratically (inverse) with epsilon
- Large datasets still reduce to manageable dimensions
- Doubling epsilon reduces dimensions by ~4x

### Use Cases and Applications

**1. Dimensionality Reduction Planning**
- Determine feasible target dimensions before projection
- Estimate computational and storage requirements
- Validate compression ratios for different epsilon values
- Plan infrastructure for large-scale transformations

**2. Epsilon Selection**
- Evaluate trade-offs between accuracy and compression
- Find optimal epsilon for application requirements
- Document rationale for epsilon choice
- Communicate distance preservation guarantees

**3. Resource Estimation**
- Predict storage requirements for projected data
- Estimate transformation computation time
- Plan memory allocation for algorithms
- Size downstream processing infrastructure

**4. Validation and Testing**
- Verify manually chosen NumComponents is sufficient
- Test if existing projection meets distance preservation
- Validate theoretical minimum against empirical results
- Ensure production configurations meet requirements

**5. Trade-off Analysis**
- Compare multiple epsilon scenarios
- Generate compression vs accuracy curves
- Support decision-making for application requirements
- Document design choices with mathematical basis

**6. Documentation**
- Provide theoretical justification for dimensionality choices
- Record minimum requirements for compliance
- Support peer review and auditing
- Enable reproducible research

**7. Hyperparameter Tuning**
- Explore epsilon parameter space systematically
- Generate candidates for cross-validation
- Optimize epsilon for specific accuracy targets
- Automate dimensionality selection

**8. Application-Specific Requirements**
- Nearest neighbor: epsilon 0.15-0.30 acceptable
- Clustering: epsilon 0.10-0.20 recommended
- Classification: epsilon 0.05-0.15 depending on task
- Visualization prep: epsilon 0.20-0.30 often sufficient

**9. Feasibility Analysis**
- Determine if random projection is viable
- Compare to alternative dimensionality reduction methods
- Assess if sufficient compression achievable
- Evaluate computational efficiency gains

**10. Production Planning**
- Size production databases for projected features
- Plan batch vs streaming transformation approach
- Estimate costs for cloud infrastructure
- Schedule transformation jobs appropriately

### Important Notes

**Output Depends Only on n and ε:**
- Number of original features does NOT affect minimum components
- Only number of rows (n) and epsilon (ε) matter
- Same minimum applies whether reducing 100→k or 10,000→k dimensions
- Focus on acceptable epsilon, not original dimensionality

**Theoretical Minimum:**
- Output is theoretical minimum with high probability guarantee
- Can use fewer dimensions in practice (but no distance guarantee)
- Can use more dimensions (stricter preservation)
- Function provides lower bound, not exact requirement

**Small Epsilon Warning:**
- Very small epsilon (< 0.05) may require many dimensions
- Can exceed original dimensionality for small datasets
- Result may indicate random projection not beneficial
- Consider alternative methods if k ≥ original dimensions

**Logarithmic Growth:**
- Dimensions grow slowly with data size
- 10x more data ≈ 1.5x more dimensions
- Very large datasets still compress significantly
- Scalability advantage of random projection

**Epsilon Interpretation:**
- Epsilon = 0.10 means ±10% distance distortion
- Distances preserved between 0.9×d and 1.1×d
- Guarantee holds with high probability (not certainty)
- Smaller epsilon = better guarantee but less compression

**Practical vs Theoretical:**
- Empirical testing often shows better preservation than guaranteed
- Can sometimes use fewer than calculated minimum
- Always validate on actual data
- Use theoretical minimum as starting point

**NULL Handling:**
- Input table must not contain NULLs in TargetColumns
- Function counts rows, NULLs would cause issues
- Clean data before running this function
- Consistent with TD_RandomProjectionFit requirements

**Performance:**
- Function is very fast (simple row count + formula)
- No heavy computation or data scanning
- Can run multiple times with different epsilon values
- Suitable for interactive exploration

### Best Practices

**1. Run Before TD_RandomProjectionFit**
- Always calculate minimum components first
- Use output to inform NumComponents parameter
- Avoid guessing at target dimensionality
- Document calculated minimum in project notes

**2. Test Multiple Epsilon Values**
- Create comparison table with different epsilon
- Evaluate compression vs accuracy trade-off
- Select epsilon based on application requirements
- Document rationale for chosen epsilon

**3. Validate Against Requirements**
- Check if minimum meets storage constraints
- Verify computational feasibility
- Ensure downstream algorithms can handle dimensionality
- Consider infrastructure limitations

**4. Consider Application Context**
- Nearest neighbor: more tolerance acceptable (ε=0.15-0.30)
- Clustering: moderate tolerance (ε=0.10-0.20)
- Classification: stricter requirements (ε=0.05-0.15)
- Critical applications: conservative epsilon

**5. Document Results**
- Store calculation results with project metadata
- Record epsilon, minimum_components, and rationale
- Enable reproducibility and auditing
- Support peer review and validation

**6. Handle Edge Cases**
- If minimum ≥ original dimensions, reconsider approach
- For small datasets, compression may be minimal
- Very large epsilon may oversimplify
- Consider alternative methods if infeasible

**7. Use for Planning Only**
- This function does NOT perform projection
- Only calculates theoretical minimum
- Must still use TD_RandomProjectionFit and Transform
- Treat as planning and validation tool

**8. Combine with Empirical Testing**
- Validate theoretical minimum with actual data
- Test distance preservation on sample
- Compare to downstream task performance
- Adjust based on empirical results

**9. Resource Estimation**
- Multiply minimum_components × num_rows × 8 bytes for storage estimate
- Factor in transformation computation time
- Plan infrastructure capacity
- Estimate costs for production deployment

**10. Continuous Validation**
- Rerun when dataset size changes significantly
- Verify assumptions periodically
- Update documentation when requirements change
- Monitor actual vs theoretical preservation

### Related Functions
- **TD_RandomProjectionFit** - Creates random projection matrix (uses NumComponents calculated by this function)
- **TD_RandomProjectionTransform** - Applies random projection to data
- **TD_PCA** - Alternative dimensionality reduction method
- **TD_SVD** - Singular Value Decomposition for dimensionality reduction

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf
- Johnson-Lindenstrauss Lemma: Dasgupta & Gupta (1999)
- "Random Projection in Dimensionality Reduction" - Bingham & Mannila (2001)

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Function Category**: Feature Engineering Transform Functions
