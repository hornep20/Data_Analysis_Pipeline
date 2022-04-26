import itertools
import numpy as np
import pandas as pd
import scipy.stats as stats
import warnings

numeric = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
datetime = ['datetime']
numeric_datetime = numeric + datetime 

# Modified from: https://pandas-profiling.github.io/pandas-profiling/docs/master/model/correlations.html
def _cramers_corrected_stat(confusion_matrix, correction: bool) -> float:
    """Calculate the Cramer's V corrected stat for two variables.

    Args:
        confusion_matrix: Crosstab between two variables.
        correction: Should the correction be applied?

    Returns:
        The Cramer's V corrected stat for the two variables.
    """
    chi2 = stats.chi2_contingency(confusion_matrix, correction=correction)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r = confusion_matrix.shape[0]
    k = confusion_matrix.shape[1] if len(confusion_matrix.shape) > 1 else 1

    # Deal with NaNs later on
    with np.errstate(divide="ignore", invalid="ignore"):
        phi2corr = max(0.0, phi2 - ((k - 1.0) * (r - 1.0)) / (n - 1.0))
        rcorr = r - ((r - 1.0) ** 2.0) / (n - 1.0)
        kcorr = k - ((k - 1.0) ** 2.0) / (n - 1.0)
        rkcorr = min((kcorr - 1.0), (rcorr - 1.0))
        if rkcorr == 0.0:
            corr = 1.0
        else:
            corr = np.sqrt(phi2corr / rkcorr)
    return corr

def cramers(df, distinct_threshold) -> pd.DataFrame:
    temp = df.select_dtypes(exclude=numeric_datetime)

    categoricals = {
        col
        for col in temp.columns
        if temp[col].nunique() <= distinct_threshold
    }

    if len(categoricals) <= 1:
        return None

    matrix = np.zeros((len(categoricals), len(categoricals)))
    np.fill_diagonal(matrix, 1.0)
    correlation_matrix = pd.DataFrame(
        matrix,
        index=categoricals,
        columns=categoricals,
    )

    for name1, name2 in itertools.combinations(categoricals, 2):
        confusion_matrix = pd.crosstab(df[name1], df[name2])
        correlation_matrix.loc[name2, name1] = _cramers_corrected_stat(
            confusion_matrix, correction=True
        )
        correlation_matrix.loc[name1, name2] = correlation_matrix.loc[name2, name1]
    return correlation_matrix


def phik(df, categorical_distinct_threshold) -> pd.DataFrame:
    temp = df.select_dtypes(include=numeric)

    intcols = {
        col
        for col in temp.columns
        # DateTime currently excluded
        # In some use cases, it makes sense to convert it to interval
        # See https://github.com/KaveIO/PhiK/issues/7
        if 1 < temp[col].nunique()
    }
    
    selcols = {
        col
        for col in df.columns
        if 1 < df[col].nunique() <= categorical_distinct_threshold
    }
    selcols = selcols.union(intcols)

    if len(selcols) <= 1:
        return None

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import phik

        correlation = df[selcols].phik_matrix(interval_cols=intcols)

    return correlation