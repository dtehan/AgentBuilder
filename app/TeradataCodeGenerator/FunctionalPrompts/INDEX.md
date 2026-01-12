You are a Teradata SQL expert with extensive experience. You will refer to the fuction documentation as shown in the markdown files listed below.  Read the .md files only as required to answer the question. Do not read any other files. 

Leverage the examples provided in the .md files to answer the question.  


# Teradata SQL Functions - Individual File Reference Index

**Total Functions**: 131
**Source**: Teradata Database Analytic Functions Version 17.20
**Generated**: November 22, 2025

## How to Use This Collection

Each function has its own dedicated markdown file containing:
- **Function Name** - Official names and aliases
- **Description** - What the function does and its characteristics
- **When to Use** - Business/analytical use cases and scenarios
- **Syntax** - Official SQL syntax with parameters
- **Code Examples** - 5-10 practical, production-ready examples

---

## Aggregate Functions (17 files)

Aggregate functions operate on sets of rows and return a single result value.

| File | Function | Purpose |
|------|----------|---------|
| [avg_average_ave.md](Core_SQL_Functions/avg_average_ave.md) | AVG, AVERAGE, AVE | Calculate arithmetic average |
| [corr.md](Core_SQL_Functions/corr.md) | CORR | Pearson correlation coefficient |
| [count.md](Core_SQL_Functions/count.md) | COUNT | Count rows or non-null values |
| [covar_pop.md](Core_SQL_Functions/covar_pop.md) | COVAR_POP | Population covariance |
| [covar_samp.md](Core_SQL_Functions/covar_samp.md) | COVAR_SAMP | Sample covariance |
| [grouping.md](Core_SQL_Functions/grouping.md) | GROUPING | Identify grouped columns in ROLLUP/CUBE |
| [kurtosis.md](Core_SQL_Functions/kurtosis.md) | KURTOSIS | Distribution kurtosis/tailedness |
| [maximum.md](Core_SQL_Functions/maximum.md) | MAXIMUM, MAX | Find maximum value |
| [minimum.md](Core_SQL_Functions/minimum.md) | MINIMUM, MIN | Find minimum value |
| [pivot.md](Core_SQL_Functions/pivot.md) | PIVOT | Rotate rows to columns |
| [skew.md](Core_SQL_Functions/skew.md) | SKEW | Distribution skewness |
| [stddev_pop.md](Core_SQL_Functions/stddev_pop.md) | STDDEV_POP | Population standard deviation |
| [stddev_samp.md](Core_SQL_Functions/stddev_samp.md) | STDDEV_SAMP | Sample standard deviation |
| [sum.md](Core_SQL_Functions/sum.md) | SUM | Sum numeric values |
| [unpivot.md](Core_SQL_Functions/unpivot.md) | UNPIVOT | Rotate columns to rows |
| [var_pop.md](Core_SQL_Functions/var_pop.md) | VAR_POP | Population variance |
| [var_samp.md](Core_SQL_Functions/var_samp.md) | VAR_SAMP | Sample variance |

## Numeric/Scalar Functions (5 files)

Scalar functions operate on individual values and return transformed values.

| File | Function | Purpose |
|------|----------|---------|
| [abs.md](Core_SQL_Functions/abs.md) | ABS | Absolute value |
| [ceil___ceiling.md](Core_SQL_Functions/ceil___ceiling.md) | CEIL, CEILING | Round up to nearest integer |
| [floor.md](Core_SQL_Functions/floor.md) | FLOOR | Round down to nearest integer |
| [mod.md](Core_SQL_Functions/mod.md) | MOD | Remainder after division |
| [power___exp___sqrt___round___truncate.md](Core_SQL_Functions/power___exp___sqrt___round___truncate.md) | POWER, EXP, SQRT, ROUND, TRUNCATE | Advanced math operations |

## String/Character Functions (2 files)

String functions for text manipulation and processing.

| File | Function | Purpose |
|------|----------|---------|
| [concat__.md](Core_SQL_Functions/concat__.md) | CONCAT, \|\| | Concatenate strings |
| [substr___substring.md](Core_SQL_Functions/substr___substring.md) | SUBSTR, SUBSTRING | Extract substring |

## Date/Time Functions (3 files)

Date and time functions for temporal data handling.

| File | Function | Purpose |
|------|----------|---------|
| [current_date___date.md](Core_SQL_Functions/current_date___date.md) | CURRENT_DATE, DATE() | Get current date |
| [extract.md](Core_SQL_Functions/extract.md) | EXTRACT | Extract date components |
| [add_months___date_add___date_sub.md](Core_SQL_Functions/add_months___date_add___date_sub.md) | ADD_MONTHS, DATE_ADD, DATE_SUB | Date arithmetic |

## Comparison/Conditional Functions (4 files)

Functions for comparisons and conditional logic.

| File | Function | Purpose |
|------|----------|---------|
| [decode.md](Core_SQL_Functions/decode.md) | DECODE | Conditional value mapping |
| [greatest___least.md](Core_SQL_Functions/greatest___least.md) | GREATEST, LEAST | Maximum/minimum from list |
| [nvl___coalesce.md](Core_SQL_Functions/nvl___coalesce.md) | NVL, COALESCE | Replace NULL with value |
| [nvl2.md](Core_SQL_Functions/nvl2.md) | NVL2 | Conditional on NULL status |

## Window/Analytic Functions (8 files)

Window functions operate over result sets returning a value for each row.

### Ranking Functions (4 files)

| File | Function | Purpose |
|------|----------|---------|
| [row_number.md](Core_SQL_Functions/row_number.md) | ROW_NUMBER | Sequential row numbering |
| [rank.md](Core_SQL_Functions/rank.md) | RANK | Ranking with gaps for ties |
| [dense_rank.md](Core_SQL_Functions/dense_rank.md) | DENSE_RANK | Ranking without gaps |
| [percent_rank.md](Core_SQL_Functions/percent_rank.md) | PERCENT_RANK | Relative position as percentage |

### Positional/Offset Functions (4 files)

| File | Function | Purpose |
|------|----------|---------|
| [lag.md](Core_SQL_Functions/lag.md) | LAG | Access previous row value |
| [lead.md](Core_SQL_Functions/lead.md) | LEAD | Access next row value |
| [nth_value.md](Core_SQL_Functions/nth_value.md) | NTH_VALUE | Access Nth row value |
| [ntile.md](Core_SQL_Functions/ntile.md) | NTILE | Divide into equal groups |


---

# Teradata Analytic Functions

## How to Use This Collection

Each function has its own dedicated markdown file containing:
- **Function Name** - Official names and aliases
- **Description** - What the function does and its characteristics
- **When to Use** - Business/analytical use cases and scenarios
- **Syntax** - Official SQL syntax with parameters
- **Code Examples** - 5-10 practical, production-ready examples

**Document Version**: 1.0
**Last Updated**: November 22, 2025
**Total Functions Documented**: 131
**Source**: Teradata Database Analytic Functions Version 17.20


## Data Cleaning Functions (4 files)

Functions for data cleaning, validation, and format conversion.

| File | Function | Purpose |
|------|----------|---------|
| [pack.md](Advanced_Analytics/pack.md) | PACK | Pack data into compact format |
| [stringsimilarity.md](Advanced_Analytics/stringsimilarity.md) | StringSimilarity | Calculate string similarity metrics |
| [td_convertto.md](Advanced_Analytics/td_convertto.md) | TD_ConvertTo | Convert data between formats |
| [unpack.md](Advanced_Analytics/unpack.md) | UNPACK | Unpack compact data format |

## Data Exploration Functions (16 files)

Functions for analyzing and summarizing data.

| File | Function | Purpose |
|------|----------|---------|
| [movingaverage.md](Advanced_Analytics/movingaverage.md) | MovingAverage | Calculate moving averages |
| [td_categoricalsummary.md](Advanced_Analytics/td_categoricalsummary.md) | TD_CategoricalSummary | Summarize categorical data |
| [td_columnsummary.md](Advanced_Analytics/td_columnsummary.md) | TD_ColumnSummary | Summarize column statistics |
| [td_getfutilecolumns.md](Advanced_Analytics/td_getfutilecolumns.md) | TD_GetFutileColumns | Identify futile columns |
| [td_getrowswithoutmissingvalues.md](Advanced_Analytics/td_getrowswithoutmissingvalues.md) | TD_GetRowsWithoutMissingValues | Filter rows without missing values |
| [td_getrowswithmissingvalues.md](Advanced_Analytics/td_getrowswithmissingvalues.md) | TD_GetRowsWithMissingValues | Filter rows with missing values |
| [td_histogram.md](Advanced_Analytics/td_histogram.md) | TD_Histogram | Generate histograms |
| [td_outlierfilterfit.md](Advanced_Analytics/td_outlierfilterfit.md) | TD_OutlierFilterFit | Fit outlier filter model |
| [td_outlierfilterfittest.md](Advanced_Analytics/td_outlierfilterfittest.md) | TD_OutlierFilterFitTest | Test outlier filter fit |
| [td_outlierfiltertransform.md](Advanced_Analytics/td_outlierfiltertransform.md) | TD_OutlierFilterTransform | Apply outlier filter |
| [td_qqnorm.md](Advanced_Analytics/td_qqnorm.md) | TD_QQNorm | Q-Q normality plot |
| [td_simpleimputefit.md](Advanced_Analytics/td_simpleimputefit.md) | TD_SimpleImputeFit | Fit simple imputation model |
| [td_simpleimputetransform.md](Advanced_Analytics/td_simpleimputetransform.md) | TD_SimpleImputeTransform | Apply simple imputation |
| [td_univariatestatistics.md](Advanced_Analytics/td_univariatestatistics.md) | TD_UnivariateStatistics | Univariate statistical analysis |
| [td_whichmax.md](Advanced_Analytics/td_whichmax.md) | TD_WhichMax | Find index of maximum value |
| [td_whichmin.md](Advanced_Analytics/td_whichmin.md) | TD_WhichMin | Find index of minimum value |

## Feature Engineering Functions (25 files)

Functions for transforming and engineering features.

| File | Function | Purpose |
|------|----------|---------|
| [antiselect.md](Advanced_Analytics/antiselect.md) | Antiselect | Select columns to exclude |
| [td_bincodefit.md](Advanced_Analytics/td_bincodefit.md) | TD_BinCodeFit | Fit binning transformation |
| [td_bincodetransform.md](Advanced_Analytics/td_bincodetransform.md) | TD_BinCodeTransform | Apply binning transformation |
| [td_columntransformer.md](Advanced_Analytics/td_columntransformer.md) | TD_ColumnTransformer | Transform columns |
| [td_functionfit.md](Advanced_Analytics/td_functionfit.md) | TD_FunctionFit | Fit function transformation |
| [td_functiontransform.md](Advanced_Analytics/td_functiontransform.md) | TD_FunctionTransform | Apply function transformation |
| [td_nonlinearcombinefit.md](Advanced_Analytics/td_nonlinearcombinefit.md) | TD_NonLinearCombineFit | Fit non-linear combination |
| [td_nonlinearcombinetransform.md](Advanced_Analytics/td_nonlinearcombinetransform.md) | TD_NonLinearCombineTransform | Apply non-linear combination |
| [td_onehotencodingfit.md](Advanced_Analytics/td_onehotencodingfit.md) | TD_OneHotEncodingFit | Fit one-hot encoding |
| [td_onehotencodingtransform.md](Advanced_Analytics/td_onehotencodingtransform.md) | TD_OneHotEncodingTransform | Apply one-hot encoding |
| [td_ordinalencodingfit.md](Advanced_Analytics/td_ordinalencodingfit.md) | TD_OrdinalEncodingFit | Fit ordinal encoding |
| [td_ordinalencodingtransform.md](Advanced_Analytics/td_ordinalencodingtransform.md) | TD_OrdinalEncodingTransform | Apply ordinal encoding |
| [td_pivoting.md](Advanced_Analytics/td_pivoting.md) | TD_Pivoting | Pivot data to dense format |
| [td_polynomialfeaturesfit.md](Advanced_Analytics/td_polynomialfeaturesfit.md) | TD_PolynomialFeaturesFit | Fit polynomial features |
| [td_polynomialfeaturestransform.md](Advanced_Analytics/td_polynomialfeaturestransform.md) | TD_PolynomialFeaturesTransform | Apply polynomial features |
| [td_randomprojectionfit.md](Advanced_Analytics/td_randomprojectionfit.md) | TD_RandomProjectionFit | Fit random projection |
| [td_randomprojectionmincomponents.md](Advanced_Analytics/td_randomprojectionmincomponents.md) | TD_RandomProjectionMinComponents | Determine min components |
| [td_randomprojectiontransform.md](Advanced_Analytics/td_randomprojectiontransform.md) | TD_RandomProjectionTransform | Apply random projection |
| [td_rownormalizefit.md](Advanced_Analytics/td_rownormalizefit.md) | TD_RowNormalizeFit | Fit row normalization |
| [td_rownormalizetransform.md](Advanced_Analytics/td_rownormalizetransform.md) | TD_RowNormalizeTransform | Apply row normalization |
| [td_scalefit.md](Advanced_Analytics/td_scalefit.md) | TD_ScaleFit | Fit scaling transformation |
| [td_scaletransform.md](Advanced_Analytics/td_scaletransform.md) | TD_ScaleTransform | Apply scaling transformation |
| [td_targetencodingfit.md](Advanced_Analytics/td_targetencodingfit.md) | TD_TargetEncodingFit | Fit target encoding |
| [td_targetencodingtransform.md](Advanced_Analytics/td_targetencodingtransform.md) | TD_TargetEncodingTransform | Apply target encoding |
| [td_unpivoting.md](Advanced_Analytics/td_unpivoting.md) | TD_Unpivoting | Unpivot data to sparse format |

## Feature Engineering Utility Functions (4 files)

Utility functions for feature engineering workflows.

| File | Function | Purpose |
|------|----------|---------|
| [td_fillrowid.md](Advanced_Analytics/td_fillrowid.md) | TD_FillRowID | Fill row IDs |
| [td_numapply.md](Advanced_Analytics/td_numapply.md) | TD_NumApply | Apply numeric function to columns |
| [td_roundcolumns.md](Advanced_Analytics/td_roundcolumns.md) | TD_RoundColumns | Round numeric columns |
| [td_strapply.md](Advanced_Analytics/td_strapply.md) | TD_StrApply | Apply string function to columns |

## Model Training Functions (9 files)

Functions for training machine learning models.

| File | Function | Purpose |
|------|----------|---------|
| [td_decisionforest.md](Advanced_Analytics/td_decisionforest.md) | TD_DecisionForest | Decision Forest model training |
| [td_glm.md](Advanced_Analytics/td_glm.md) | TD_GLM | Generalized Linear Model |
| [td_kmeans.md](Advanced_Analytics/td_kmeans.md) | TD_KMeans | K-Means clustering |
| [td_knn.md](Advanced_Analytics/td_knn.md) | TD_KNN | K-Nearest Neighbors |
| [td_naivebayes.md](Advanced_Analytics/td_naivebayes.md) | TD_NaiveBayes | Naive Bayes classifier |
| [td_oneclasssvm.md](Advanced_Analytics/td_oneclasssvm.md) | TD_OneClassSVM | One-Class SVM |
| [td_svm.md](Advanced_Analytics/td_svm.md) | TD_SVM | Support Vector Machine |
| [td_xgboost.md](Advanced_Analytics/td_xgboost.md) | TD_XGBoost | XGBoost model training |
| [td_naivebayestextclassifiertrainer.md](Advanced_Analytics/td_naivebayestextclassifiertrainer.md) | TD_NaiveBayesTextClassifierTrainer | Naive Bayes text classifier trainer |

## Model Scoring Functions (9 files)

Functions for generating predictions from trained models.

| File | Function | Purpose |
|------|----------|---------|
| [td_decisionforestpredict.md](Advanced_Analytics/td_decisionforestpredict.md) | TD_DecisionForestPredict | Decision Forest predictions |
| [td_glmpredict.md](Advanced_Analytics/td_glmpredict.md) | TD_GLMPredict | GLM predictions |
| [td_kmeanspredict.md](Advanced_Analytics/td_kmeanspredict.md) | TD_KMeansPredict | K-Means cluster assignment |
| [td_naivebayespredict.md](Advanced_Analytics/td_naivebayespredict.md) | TD_NaiveBayesPredict | Naive Bayes predictions |
| [td_naivebayestextclassifierpredict.md](Advanced_Analytics/td_naivebayestextclassifierpredict.md) | TD_NaiveBayesTextClassifierPredict | Naive Bayes text classifier predictions |
| [td_oneclasssvmpredict.md](Advanced_Analytics/td_oneclasssvmpredict.md) | TD_OneClassSVMPredict | One-Class SVM predictions |
| [td_svmpredict.md](Advanced_Analytics/td_svmpredict.md) | TD_SVM predictions |
| [td_vectordistance.md](Advanced_Analytics/td_vectordistance.md) | TD_VectorDistance | Vector distance calculations |
| [td_xgboostpredict.md](Advanced_Analytics/td_xgboostpredict.md) | TD_XGBoostPredict | XGBoost predictions |

## Model Evaluation Functions (6 files)

Functions for evaluating model performance.

| File | Function | Purpose |
|------|----------|---------|
| [td_classificationevaluator.md](Advanced_Analytics/td_classificationevaluator.md) | TD_ClassificationEvaluator | Classification metrics |
| [td_regressionevaluator.md](Advanced_Analytics/td_regressionevaluator.md) | TD_RegressionEvaluator | Regression metrics |
| [td_roc.md](Advanced_Analytics/td_roc.md) | TD_ROC | ROC curve generation |
| [td_shap.md](Advanced_Analytics/td_shap.md) | TD_SHAP | SHAP value computation |
| [td_silhouette.md](Advanced_Analytics/td_silhouette.md) | TD_Silhouette | Silhouette coefficient |
| [td_traintestsplit.md](Advanced_Analytics/td_traintestsplit.md) | TD_TrainTestSplit | Train-test split |

## Text Analytics Functions (7 files)

Functions for natural language processing and text analysis.

| File | Function | Purpose |
|------|----------|---------|
| [td_ngramsplitter.md](Advanced_Analytics/td_ngramsplitter.md) | TD_Ngramsplitter | N-gram tokenization |
| [td_nerextractor.md](Advanced_Analytics/td_nerextractor.md) | TD_NERExtractor | Named Entity Recognition |
| [td_sentimentextractor.md](Advanced_Analytics/td_sentimentextractor.md) | TD_SentimentExtractor | Sentiment analysis |
| [td_textmorph.md](Advanced_Analytics/td_textmorph.md) | TD_TextMorph | Text morphing/lemmatization |
| [td_textparser.md](Advanced_Analytics/td_textparser.md) | TD_TextParser | Text parsing |
| [td_tfidf.md](Advanced_Analytics/td_tfidf.md) | TD_TFIDF | TF-IDF calculation |
| [td_wordembeddings.md](Advanced_Analytics/td_wordembeddings.md) | TD_WordEmbeddings | Word embeddings |

## Hypothesis Testing Functions (4 files)

Functions for statistical hypothesis testing.

| File | Function | Purpose |
|------|----------|---------|
| [td_anova.md](Advanced_Analytics/td_anova.md) | TD_ANOVA | ANOVA test |
| [td_chisq.md](Advanced_Analytics/td_chisq.md) | TD_ChiSq | Chi-square test |
| [td_ftest.md](Advanced_Analytics/td_ftest.md) | TD_FTest | F-test |
| [td_ztest.md](Advanced_Analytics/td_ztest.md) | TD_ZTest | Z-test |

## Association Analysis Functions (1 file)

Functions for association rule mining and analysis.

| File | Function | Purpose |
|------|----------|---------|
| [td_cfilter.md](Advanced_Analytics/td_cfilter.md) | TD_CFilter | Association filtering |

## Path and Pattern Analysis Functions (3 files)

Functions for analyzing paths and patterns in sequential data.

| File | Function | Purpose |
|------|----------|---------|
| [td_attribution.md](Advanced_Analytics/td_attribution.md) | Attribution | Attribution analysis |
| [td_npath.md](Advanced_Analytics/td_npath.md) | nPath | Pattern path analysis |
| [td_sessionize.md](Advanced_Analytics/td_sessionize.md) | Sessionize | Session identification |
