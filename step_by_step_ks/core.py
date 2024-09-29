import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ecdf
import random
import os

def randomize(list_in):

    """
    Randomly shuffles the elements of a given list and returns the shuffled list.

    This function creates a copy of the input list and applies a random shuffle, 
    leaving the original list unchanged.

    Parameters
    ----------
    list_in : list
        The input list to be shuffled.

    Returns
    -------
    list
        A new list with the elements randomly shuffled.

    Examples
    --------
    >>> my_list = [1, 2, 3, 4, 5]
    >>> randomize(my_list)
    [4, 1, 5, 2, 3]
    
    Notes
    -----
    The input list remains unchanged as the function operates on a copy.
    """

    shuff = list_in.copy()
    random.shuffle(shuff)
    return shuff

def raw_ks_test(data1, data2, alternative='1 less than 2', plot=True, save_ecdf_path=None):

    """
    Perform a custom Kolmogorov-Smirnov (KS) test to compare two empirical distributions.

    This function compares two datasets using a KS test to determine if one distribution 
    is "less than" or "greater than" the other based on their empirical cumulative distribution 
    functions (ECDFs). It returns the KS statistic and the location of the maximum difference 
    between the two ECDFs. Optionally, it plots the ECDFs and the difference.

    Parameters
    ----------
    data1 : array-like
        The first dataset (empirical distribution) to compare.
    data2 : array-like
        The second dataset (empirical distribution) to compare.
    alternative : str, optional, default='1 less than 2'
        Specifies the alternative hypothesis for the test. 
        - '1 less than 2' or '2 more than 1': Test if distribution 1 is generally less than distribution 2.
        - '1 more than 2' or '2 less than 1': Test if distribution 1 is generally greater than distribution 2.
    plot : bool, optional, default=True
        If True, generates a plot of the ECDFs and the KS statistic.

    Returns
    -------
    dict
        A dictionary containing:
        - 'stat' : float
            The KS statistic, representing the maximum difference between the two ECDFs.
        - 'location' : float
            The location (x-value) of the maximum difference between the two ECDFs.

    Notes
    -----
    - This is a one-sided KS test that evaluates the alternative hypothesis based 
      on whether one distribution is greater or less than the other.
    - The ECDFs are generated from the input data and evaluated at all unique values 
      in the combined dataset.

    Example
    -------
    >>> data1 = np.random.normal(0, 1, 100)
    >>> data2 = np.random.normal(1, 1, 100)
    >>> result = raw_ks_test(data1, data2, alternative='1 less than 2', plot=True)
    >>> print(result)
    {'stat': 0.25, 'location': 0.5}
    
    """

    data1 = np.sort(data1)
    ecdf1 = ecdf(data1)

    data2 = np.sort(data2)
    ecdf2 = ecdf(data2)
    
    size1,size2 = len(data1),len(data2)
    all_x = np.sort(np.concatenate((data1,data2)))

    if alternative=='1 less than 2' or alternative=='2 greater than 1':
        diff = ecdf1.cdf.evaluate(all_x) - ecdf2.cdf.evaluate(all_x)
    elif alternative=='2 less than 1' or alternative=='1 greater than 2':
        diff = ecdf2.cdf.evaluate(all_x) - ecdf1.cdf.evaluate(all_x) 
    else:
        print('Please set a valid alternative...')
        os.abort()
    # elif alternative=='1 greater than 2' or '2 less than 1':
    #   diff = ecdf2.cdf.evaluate(all_x) - ecdf1.cdf.evaluate(all_x)    

    
    peak = all_x[np.argmax(diff)]
    stat = max(diff)

    if plot:
        fig,ax = plt.subplots(1,1,figsize=(4,3))
        ax.plot(all_x, ecdf1.cdf.evaluate(all_x),label='dist 1')
        ax.plot(all_x, ecdf2.cdf.evaluate(all_x),label="dist 2")
        ax.plot(all_x, diff, label="(1) - (2)")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xlabel('total dist')
        ax.set_ylabel('prob(x <= X)')
        ymin,ymax = ax.get_ylim()
        ax.vlines(peak,ecdf2.cdf.evaluate(peak),ecdf1.cdf.evaluate(peak),color='k',linestyle='--',label=f'S = {round(stat,3)}\nxS = {round(peak,3)}')
        ax.legend()
        plt.tight_layout()
        if save_ecdf_path is not None:
            plt.savefig(save_ecdf_path, bbox_inches='tight',dpi=300)
        plt.show()
    
    return {"stat": stat, "location": peak}

def bootstrap_pvalue(data1, data2, reference_stat, alternative="1 less than 2", nloop=1000, respect_ratio=True, replacement=False, bootstrap_size=None, plot=True, save_stat_distribution_path=None, *args):

    """
    Estimate the p-value using a bootstrap method based on the KS statistic.

    This function performs a bootstrap procedure to compute a p-value by shuffling the 
    combined data from two distributions and recalculating the KS statistic. The resulting 
    p-value is the proportion of bootstrap samples where the statistic is greater than or 
    equal to the reference statistic.

    Parameters
    ----------
    data1 : array-like
        The first dataset (empirical distribution) to compare.
    data2 : array-like
        The second dataset (empirical distribution) to compare.
    reference_stat : float
        The KS statistic computed from the original data, used as a reference to compare against the bootstrap samples.
    alternative : str, optional, default="1 less than 2"
        Specifies the alternative hypothesis for the KS test:
        - '1 less than 2' or '2 greater than 1': Tests if distribution 1 is generally less than distribution 2.
        - '1 greater than 2' or '2 less than 1': Tests if distribution 1 is generally greater than distribution 2.
    nloop : int, optional, default=1000
        The number of bootstrap iterations (loops).
    respect_ratio : bool, optional, default=True
        If True, the bootstrap procedure respects the size ratio between data1 and data2 during resampling.
    replacement : bool, optional, default=False
        If True, sampling is done with replacement. If False, sampling is done without replacement.
    bootstrap_size : int, optional, default=None
        If specified, this sets the size of the bootstrap samples to be drawn. If None, the size of the original data is used.
    plot : bool, optional, default=True
        If True, a histogram of the KS statistics from the bootstrap samples is plotted along with the reference KS statistic.

    Returns
    -------
    pvalue : float
        The estimated p-value based on the bootstrap procedure. This is the proportion of bootstrap statistics that are greater than or equal to the reference statistic.

    Notes
    -----
    - The bootstrap method shuffles and resamples the combined data from `data1` and `data2`, 
      recalculating the KS statistic to generate a distribution of statistics.
    - The p-value is computed as the fraction of bootstrap statistics that are greater than or 
      equal to the reference statistic.

    Example
    -------
    >>> data1 = np.random.normal(0, 1, 100)
    >>> data2 = np.random.normal(1, 1, 100)
    >>> reference_stat = raw_ks_test(data1, data2, alternative='1 less than 2', plot=False)['stat']
    >>> pvalue = bootstrap_pvalue(data1, data2, reference_stat, alternative='1 less than 2', nloop=1000, plot=True)
    >>> print(f"P-value: {pvalue}")
    """
    
    size1,size2 = len(data1),len(data2)
    all_x = list(np.concatenate((data1, data2),axis=0))
    
    s=0
    stat_distribution = []
    
    for i in range(nloop):
        
        # For each loop shuffle
        if respect_ratio:
            shuffled = randomize(all_x)   
            d1 = shuffled[:size1]
            if not replacement:
                d2 = shuffled[size1:]
            else:
                shuffled2 = randomize(all_x)
                d2 = shuffled2[:size12]
        
        if isinstance(bootstrap_size, int):
            shuffled = randomize(all_x) 
            d1 = shuffled[:bootstrap_size]
            if not replacement:
                d2 = shuffled[bootstrap_size:(int(2*bootstrap_size))]
            else:
                shuffled2 = randomize(all_x)
                d2 = shuffled2[:bootstrap_size]
        
        test = raw_ks_test(d1, d2, alternative=alternative, plot=False)
        stat = test['stat']
        
        stat_distribution.append(stat)
        if stat>=reference_stat:
            s+=1
    
    pvalue = s/nloop
    
    if plot==True:
        fig,ax = plt.subplots(1,1,figsize=(4,3))
        ax.hist(stat_distribution, alpha=0.6)
        ymin,ymax = ax.get_ylim()
        ax.vlines(reference_stat,0,ymax,color='r')
        ax.set_xlabel(r'KS statistic $S$')
        ax.set_ylabel('#')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        plt.tight_layout()
        if save_stat_distribution_path is not None:
            plt.savefig(save_stat_distribution_path,bbox_inches="tight",dpi=300)
        plt.show()    
    
    return pvalue

def ks_test(data1, data2, alternative='1 less than 2', plot_ecdf=False, bootstrap_loops=1000, bootstrap_respect_ratio=True, bootstrap_replacement=False, bootstrap_size=None, bootstrap_plot=True, save_ecdf_path=None, save_stat_distribution_path=None):
    
    """
    Performs a two-sample Kolmogorov-Smirnov (KS) test with an optional bootstrap procedure for p-value estimation.

    The function first calculates the KS statistic between two datasets using the empirical cumulative distribution 
    functions (ECDFs). Then, it uses a bootstrap method to estimate the p-value by shuffling and resampling the 
    combined data. The test result includes the KS statistic, the location where the maximum difference occurs, 
    and the estimated p-value.

    Parameters
    ----------
    data1 : array-like
        The first dataset (empirical distribution) to compare.
    data2 : array-like
        The second dataset (empirical distribution) to compare.
    alternative : str, optional, default='1 less than 2'
        Specifies the alternative hypothesis for the KS test:
        - '1 less than 2' or '2 greater than 1': Tests if distribution 1 is generally less than distribution 2.
        - '1 greater than 2' or '2 less than 1': Tests if distribution 1 is generally greater than distribution 2.
    plot_ecdf : bool, optional, default=False
        If True, plots the ECDF of the two datasets along with their difference.
    bootstrap_loops : int, optional, default=1000
        The number of bootstrap iterations (loops) for estimating the p-value.
    bootstrap_respect_ratio : bool, optional, default=True
        If True, the bootstrap procedure respects the size ratio between data1 and data2 during resampling.
    bootstrap_replacement : bool, optional, default=False
        If True, the bootstrap samples are drawn with replacement.
    bootstrap_size : int, optional, default=None
        If specified, this sets the size of the bootstrap samples. If None, the original data sizes are used.
    bootstrap_plot : bool, optional, default=True
        If True, plots the distribution of KS statistics generated by the bootstrap procedure.

    Returns
    -------
    test : dict
        A dictionary containing:
        - 'stat': The KS statistic (maximum difference between the two ECDFs).
        - 'location': The point where the maximum difference occurs.
        - 'pvalue': The estimated p-value from the bootstrap procedure.

    Notes
    -----
    - The KS statistic measures the maximum distance between the ECDFs of two datasets.
    - The p-value is estimated through bootstrapping by shuffling and resampling the combined datasets, and 
      recalculating the KS statistic for each resample. The fraction of bootstrap samples with a KS statistic 
      greater than or equal to the original KS statistic gives the p-value.

    Example
    -------
    >>> data1 = np.random.normal(0, 1, 100)
    >>> data2 = np.random.normal(1, 1, 100)
    >>> result = ks_test(data1, data2, alternative='1 less than 2', bootstrap_loops=1000, plot_ecdf=True, bootstrap_plot=True)
    >>> print(f"KS Statistic: {result['stat']}, P-value: {result['pvalue']}")
    """
    
    test = raw_ks_test(data1, data2, alternative=alternative, plot=plot_ecdf, save_ecdf_path=save_ecdf_path)
    reference_stat = test['stat']
    pvalue = bootstrap_pvalue(data1, data2, reference_stat, alternative=alternative, plot=bootstrap_plot, nloop=bootstrap_loops, replacement=bootstrap_replacement, bootstrap_size=bootstrap_size, save_stat_distribution_path=save_stat_distribution_path)
    test.update({'pvalue': pvalue})

    return test

if __name__=="__main__":
    
    # data = np.load('../data/dico.npy',allow_pickle=True)
    # data1 = data.item()['data1']
    # data2 = data.item()['data2']
    # test = ks_test(data1, data2, alternative='1 less than 2',plot_ecdf=True,bootstrap_loops=1000, bootstrap_plot=True, bootstrap_size=None, bootstrap_replacement=False)
    # print(f'{test=}')

    data1 = np.random.normal(8,4, size=150)
    data2 = np.random.normal(9,3, size=150)
    test = ks_test(data1, data2, alternative='1 less than 2',plot_ecdf=True,bootstrap_loops=3000, bootstrap_plot=True, bootstrap_size=None, bootstrap_replacement=False)
    print(f'{test=}')


