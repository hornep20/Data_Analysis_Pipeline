# https://numpy.org/doc/stable/reference/routines.math.html
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.preprocessing import StandardScaler

def norm_plot_and_test(series, bins=100):
    '''
    series (pd.Series)
    bins (int)
    '''
    
    # Set up empty lists to store results
    dist_names = []
    s_values = []
    p_values = []
    
    fig, axs = plt.subplots(2, 3, figsize=(17, 10))
    plt.subplots_adjust(hspace=0.4, wspace=0.4)
    
    v = series
    
    # original
    try:
        v.plot.hist(bins=bins, ax=axs[0,0])
        s, p = stats.normaltest(v, nan_policy='omit')
        s_values.append(s)
        p_values.append(p)
    except:
        s_values.append(np.nan)
        p_values.append(np.nan)
    
    # ln transformation
    try:
        v = series.apply(lambda x : np.log(x)) 
        v.plot.hist(bins=bins, ax=axs[0,1])
        s, p = stats.normaltest(v, nan_policy='omit')
        s_values.append(s)
        p_values.append(p)
    except:
        s_values.append(np.nan)
        p_values.append(np.nan)
        
    # SQRT transformation
    try:
        v = series.apply(lambda x : np.sqrt(x))
        v.plot.hist(bins=bins, ax=axs[0,2])
        s, p = stats.normaltest(v, nan_policy='omit')
        s_values.append(s)
        p_values.append(p)
    except:
        s_values.append(np.nan)
        p_values.append(np.nan)
        
    # Exponential transformation
    try:
        v = series.apply(lambda x : np.exp(x))
        v.plot.hist(bins=bins, ax=axs[1,0])
        s, p = stats.normaltest(v, nan_policy='omit')
        s_values.append(s)
        p_values.append(p)
    except:
        s_values.append(np.nan)
        p_values.append(np.nan)
        
    # Cube-root transformation
    try:
        v = series.apply(lambda x : np.cbrt(x))
        v.plot.hist(bins=bins, ax=axs[1,1])
        s, p = stats.normaltest(v, nan_policy='omit')
        s_values.append(s)
        p_values.append(p)
    except:
        s_values.append(np.nan)
        p_values.append(np.nan)
    
    # Boxcox -0.5 transformation
    try:
        v = pd.DataFrame(stats.boxcox(series, lmbda=-0.5))
        v.plot.hist(bins=bins, ax=axs[1,2])
        s, p = stats.normaltest(v.iloc[:,0], nan_policy='omit')
        s_values.append(s)
        p_values.append(p)
    except:
        s_values.append(np.nan)
        p_values.append(np.nan)
    
    title_list = [['Original', 'LN Transformed', 'SQRT Transformed'], ['Exp Transformed', 'Cube-root Transformed', 'Boxcox -0.5 Transformed']]
    i = 0
    j = 0
    for titles in title_list:
        for title in titles:
            dist_names.append(title)
            axs[i,j].set_title(title_list[i][j])
            j += 1
        i += 1
        j = 0
    plt.show()
    
    # Collate results and sort by goodness of fit (best at top)
    results = pd.DataFrame()
    results['Distribution'] = dist_names
    results['Statistic'] = s_values
    results['p_value'] = p_values
    results.sort_values(['p_value'], inplace=True)

    # Report results
    print ('\nDistributions (normal test) sorted by goodness of fit:')
    print ('----------------------------------------')
    print (results.sort_index())
    print ('*If p<0.05, reject null (not of the distribution)')
    
    
def kstest(series):
    # https://pythonhealthcare.org/2018/05/03/81-distribution-fitting-to-data/
    dist_names = ['beta',
              'expon',
              'gamma',
              'lognorm',
              'norm',
              'pearson3',
              'triang',
              'uniform',
              'weibull_min', 
              'weibull_max']
    
    y = np.array(series)
    size = len(y)
    
    sc = StandardScaler() 
    yy = y.reshape(-1,1)
    sc.fit(yy)
    y_std = sc.transform(yy)
    y_std = y_std.flatten()
    del yy

    # Set up empty lists to stroe results
    chi_square = []
    p_values = []

    # Set up 50 bins for chi-square test
    # Observed data will be approximately evenly distrubuted aross all bins
    percentile_bins = np.linspace(0,100,51)
    percentile_cutoffs = np.percentile(y_std, percentile_bins)
    observed_frequency, bins = (np.histogram(y_std, bins=percentile_cutoffs))
    cum_observed_frequency = np.cumsum(observed_frequency)

    # Loop through candidate distributions
    for distribution in dist_names:
        # Set up distribution and get fitted distribution parameters
        dist = getattr(stats, distribution)
        param = dist.fit(y_std)

        # Obtain the KS test P statistic, round it to 5 decimal places
        p = stats.kstest(y_std, distribution, args=param)[1]
        p = np.around(p, 5)
        p_values.append(p)    

        # Get expected counts in percentile bins
        # This is based on a 'cumulative distrubution function' (cdf)
        cdf_fitted = dist.cdf(percentile_cutoffs, *param[:-2], loc=param[-2], 
                              scale=param[-1])
        expected_frequency = []
        for bin in range(len(percentile_bins)-1):
            expected_cdf_area = cdf_fitted[bin+1] - cdf_fitted[bin]
            expected_frequency.append(expected_cdf_area)

        # calculate chi-squared
        expected_frequency = np.array(expected_frequency) * size
        cum_expected_frequency = np.cumsum(expected_frequency)
        ss = sum (((cum_expected_frequency - cum_observed_frequency) ** 2) / cum_observed_frequency)
        chi_square.append(ss)

    # Collate results and sort by goodness of fit (best at top)
    results = pd.DataFrame()
    results['Distribution'] = dist_names
    results['chi_square'] = chi_square
    results['p_value'] = p_values
    results.sort_values(['chi_square'], inplace=True)

    # Report results
    print ('\nDistributions (Kolmogorov-Smirnov test) sorted by goodness of fit:')
    print ('----------------------------------------')
    print (results.sort_index())
    print ('*If p<0.05, reject null (not of the distribution)')