import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm

def OLS(y, X):
    # Ordinary least squares (OLS) regression
    XC = sm.add_constant(X)
    results = sm.OLS(y, XC).fit()
    return results
    
def WLS(y, X):
    # Weighted least squares (WLS) regression
    XC = sm.add_constant(X)
    results = sm.WLS(y, XC, weight=1./(X**2)).fit()
    return results

def summary(results, pretty_print=False):
    if(pretty_print):
        display(results.summary())
    else:
        print(results.summary())
        
def fitplot(results, y, ylabel, X, Xlabel):
    if X.shape[1] != 1:
        print('Cannot plot since |X| > 1')
    else:
        plt.figure(figsize=(7,7))
        plt.scatter(X, y)
        yhat = results.params[1]*X+results.params[0]
        fig = plt.plot(X, yhat, lw=4, c='orange', label='regression line')
        plt.xlabel(Xlabel)
        plt.ylabel(ylabel)
        plt.show()
        

# https://docs.scipy.org/doc/scipy/reference/stats.html
def qqplot(data, title='Q-Q Plot'):
    dists = [[stats.chi2,      stats.exponnorm, stats.gamma,   stats.invgamma], 
             [stats.logistic,  stats.lognorm,   stats.norm,    stats.uniform]]
    titles = [['Chi2',     'Expon Norm', 'Gamma',  'Inv Gamma'],
              ['Logistic', 'Log Norm',   'Normal', 'Uniform']]
    fig, axs = plt.subplots(len(dists), len(dists[0]), figsize=(17, 7))
    plt.subplots_adjust(hspace=0.4, wspace=0.4)
    fig.suptitle(title, fontsize=18)
    i = 0
    j = 0
    for dist in dists:
        for d in dist:
            sm.graphics.qqplot(data, dist=d, line='45', fit=True, ax=axs[i,j])
            axs[i,j].set_title(titles[i][j])
            j += 1
        i += 1
        j = 0
    plt.show()