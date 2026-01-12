# TD_XGBoost

### Function Name
**TD_XGBoost**

### Description
Performs classification and regression analysis on data sets and generates a model for

### When the Function Would Be Used
- Performing advanced data analysis and transformation
- Building predictive models and machine learning workflows
- Feature engineering and data preparation
- Statistical analysis and hypothesis testing
- Text processing and natural language analysis

### Syntax
    TD_XGBoost (
    ON { table | view | (query) } AS INPUTTABLE PARTITION BY ANY
    [ OUT [ PERMANENT | VOLATILE ] TABLE MetaInformationTable(output_table_name)]
    USING
    InputColumns ({'input_column'|input_column_range }[,…])
    ResponseColumn('response_column')
    [ ModelType ('classification'|'regression') ]
    [ MaxDepth (maxdepth) ]
    [ MinNodeSize (minnodesize) ]
    [ NumParallelTrees (numparalleltrees) ]
    [ RegularizationLambda (lambda) ]
    [ LearningRate (learningrate) ]
    [ ColumnSampling (sample_fraction) ]
    [ CoverageFactor (coveragefactor)]
    [ NumBoostRounds (numboostrounds) ]
    [ Seed (seed) ]
    [ BaseScore (basescore) ]
    Database Analytic Functions, Release 17.20 427
    6: Model Training Functions
    [ MinImpurity (minimpurity) ]
    [ TreeSize (treesize) ]
    [ DataRedistributionColumn (data_redistribution_column) ]
    [ MinRowsPerAmp (min_rows_per_amp) ]
    )


Required Syntax Elements for TD_XGBoost:

ON clause
    Specifies intput table used to train XGBoost model.
    The InputTable in TD_XGBoost query can have no partition at all, or have PARTITION BY
ANY clause.
InputColumns
    Specifies the input table columns name that need to be used for training the model
    (predictors, features, or independent variables).

Optional Syntax Elements for TD_XGBoost:

OUT clause
    Specifies the name of the output table that records training accuracy over iterations.
ModelType
    Specifies whether the analysis is a regression (continuous response variable) or a multiple-
    class classification (predicting result from the number of classes). Only Regression and
    Classification are accepted values.
    Default: Regression.
MaxDepth
    Specifies a decision tree stopping criterion. If the tree reaches a depth past this value, the algorithm could stops looking for splits. Decision trees can grow to ( 2(max_depth+1)-1) nodes. This stopping criterion has the greatest effect on the performance of the function. The
    maximum value is 2147483647.
    Default: 5
MinNodeSize
    Specifies a decision tree stopping criterion; the minimum size of any node within each decision tree.
    Default: 1
NumParallelTrees
    Specifies the parallels boosted trees number. The num_trees is an INTEGER value in the range [1, 10000]. Each boosted tree operates on a sample of data that fits in an AMP memory. By default, NumBoostedTrees is chosen equal to the number of AMPs with data. If NumBoostedTrees is greater than the number of AMPs with data, each boosting operates on a sample of the input data, and the function estimates sample size (number of rows) using this formula: sample_size = total_number_of_input_rows / number_of_trees
    The sample_size must fit in an AMP memory. It always uses the sample size (or tree size) that fits in an AMP memory to build tree models and ignores those rows cannot fit in memory.
    A higher NumBoostedTrees value may improve function run time but may decrease prediction accuracy.
    Default: -1
RegularizationLambda
    Specifies the L2 regularization that the loss function uses while boosting trees. The lambda is a DOUBLE PRECISION value in the range [0, 100000]. The higher the lambda, the stronger the regularization effect. The value 0 specifies no regularization.
    Default: 1
LearningRate
    Specifies the learning rate (weight) of a learned tree in each boosting step. After each boosting step, the algorithm multiplies the learner by shrinkage to make the boosting process more conservative. The shrinkage is a DOUBLE PRECISION value in the range (0, 1]. The value 1 specifies no shrinkage.
    Default: 0.5
ColumnSampling
    Specifies the features fraction to sample during boosting. The sample_fracti on is a DOUBLE PRECISION value in the range (0, 1].
    Default: 1.0
CoverageFactor
    Specifies the coverage level for the dataset while boosting trees (in percentage, for example, 1.25 = 125% coverage). You can only use CoverageFactor if you do not supply NumBoostedTrees. When NumBoostedTrees is specified, coverage depends on the value of NumBoostedTrees. If NumBoostedTrees is not specified, NumBoostedTrees is chosen to achieve this level of coverage.
    Default: 1.0
NumBoostRounds
    Specifies the iterations (rounds) number to boost the weak classifiers. The iterations must be an INTEGER in the range [1, 100000].
    Default: 10
Seed
    Specifies an integer value to use in determining the random seed for column sampling.
    Default: 1
BaseScore
    Specifies the initial prediction value for all data points. Typically that value would be set to the mean of the observed value in the training set. This information is shown in the meta row in the model table. For classification, basescore value must be in the range (0, 1) and the default value is 0.5. The regression case accepts any double values in the range [-1e50, 1e50] and the default value is 0.
    Default: 0
MinImpurity
    Specifies the minimum impurity at which the tree stops splitting further down. For regression, a criteria of squared error is used whereas for classification, gini impurity is used.
    Default: 0.0
TreeSize
    Specifies the rows number that each tree uses as its input data set. The function builds a tree using either the number of rows on an AMP, the number of rows that fit into the AMP memory (whichever is less), or the number of rows given by the TreeSize argument. By default, this value is computed as the minimum of the number of rows on an AMP, and the number of rows that fit into the AMP memory.
    Default: -1
DataRedistributionColumn
    Specifies the name of the column used to redistribute the data. The maximum value is 128.
    • If the number of unique values in this column is less than the result of "total number of input rows / MinRowsPerAmp argument", then the rows in the input table will be distributed to the AMPs equivalent to the number of unique values in this column.
    • If the number of unique values in this column is greater than the result of "total number of input rows / MinRowsPerAmp", then the rows in the input table will be distributed to the AMPs equivalent to the "total number of input rows / MinRowsPerAmp".
MinRowsPerAmp
    Specifies the minimum number of rows (input table rows) an AMP should have when data needs to be redistributed using DataRedistributionColumn.




### Code Examples

**Example 1: Basic Usage**
```sql
    SELECT * FROM TD_XGBoost (
    ON diabetes_sample PARTITION BY ANY
    OUT TABLE MetaInformationTable(xgb_out)
    USING
    ResponseColumn('response')
    InputColumns('[2:4]')
    MaxDepth(3)
    MinNodeSize(1)
    NumParallelTrees(2)
    ModelType('CLASSIFICATION')
    Seed(1)
    RegularizationLambda(1)
    LearningRate(0.5)
    NumBoostRounds(2)
    MinImpurity(0)
    ColumnSampling(1.0)
    ) as dt;
```

**Example 2: Basic Usage**
``` sql
    SELECT * FROM TD_XGBoost (
    ON housing_sample partition by ANY
    OUT TABLE MetaInformationTable(xgb_out)
    USING
    ResponseColumn('medv')
    InputColumns('[2:4]')
    MaxDepth(3)
    MinNodeSize(1)
    NumParallelTrees(1)
    ModelType('REGRESSION')
    Seed(1)
    RegularizationLambda(1000)
    LearningRate(0.8)
    NumBoostRounds(3)
    ColumnSampling(1.0)
    ) as dt;
```

**Example 3: Basic Usage**
```sql 
    SELECT * FROM TD_XGBoost (
    ON housing_full PARTITION BY ANY
    OUT TABLE MetaInformationTable(xgb_out)
    USING
    ResponseColumn('medv')
    InputColumns('[0:3]')
    MaxDepth(10)
    MinNodeSize(1)
    NumParallelTrees(2)
    ModelType('REGRESSION')
    Seed(1)
    RegularizationLambda(1000)
    LearningRate(0.8)
    NumBoostRounds(1)
    ColumnSampling(1.0)
    ) AS dt;
```

**Example 4: Basic Usage**
```sql 
    SELECT * FROM TD_XGBoost (
    ON iris_train_redist AS inputtable
    USING
    INPUTCOLUMNS ('[1:4]')
    RESPONSECOLUMN ('species')
    DataRedistributionColumn ('redist')
    MODELTYPE ('Classification')
    MAXDEPTH (1 )
    NUMBOOSTEDTREES (32 )
    ITERNUM (2 )
    SEED (1 )
    MinRowsPerAmp(10)
    isDebug('true')
    ) as dt
```

### Related Functions
- See Teradata Database Analytic Functions documentation for related functions
- Review similar functions in the Model Training category

### Additional Resources
- [Teradata Database Analytic Functions Documentation](https://docs.teradata.com)
- Official Examples and Use Cases in B035-1206-172K.pdf

---

**File Generated**: 2025-11-22
**Source**: Teradata Database Analytic Functions (B035-1206-172K.pdf, Release 17.20)
**Note**: This is a template documentation. For complete syntax, parameters, and examples, consult the official Teradata documentation.