![ico17](https://github.com/remyeltorro/step_by_step_ks/actions/workflows/test.yml/badge.svg)
![ico4](https://img.shields.io/pypi/v/step_by_step_ks)
![ico6](https://img.shields.io/github/downloads/remyeltorro/step_by_step_ks/total)
![ico5](https://img.shields.io/pypi/dm/step_by_step_ks)
![GitHub repo size](https://img.shields.io/github/repo-size/remyeltorro/step_by_step_ks)
![GitHub License](https://img.shields.io/github/license/remyeltorro/step_by_step_ks?link=https%3A%2F%2Fgithub.com%2Fremyeltorro%step_by_step_ks%2Fblob%2Fmain%2FLICENSE)
![ico2](https://img.shields.io/github/forks/remyeltorro/step_by_step_ks?link=https%3A%2F%2Fgithub.com%2Fremyeltorro%step_by_step_ks%2Fforks)
![ico3](https://img.shields.io/github/stars/remyeltorro/step_by_step_ks?link=https%3A%2F%2Fgithub.com%2Fremyeltorro%step_by_step_ks%2Fstargazers)



This Python package performs a 2-sample Kolmogorov-Smirnov test, step by step and supported by figures. The p-value is computed using a customizable bootstrap method. 

Installation
============

To use the package, you must install Python3, e.g. through [Anaconda](https://www.anaconda.com/download). The package relies on standard Python libraries: `numpy`, `scipy`, `random`, `matplotlib`.

Download and extract the ZIP file, enter the folder and open a console locally.

``` bash
pip install step_by_step_ks
```

How to use
==========

Once the package `step_by_step_ks` is installed and available in your Python environment, you can call the test as follows:

```python
from step_by_step_ks import ks_test
import numpy as np

# Generate fake empirical distributions
data1 = np.random.normal(8,4, size=250)
data2 = np.random.normal(9,3, size=150)

alternative = '1 less than 2'
bootstrap_loops = 1000

test = ks_test(data1, data2, alternative=alternative,plot_ecdf=True,bootstrap_loops=bootstrap_loops, bootstrap_plot=True, bootstrap_size=None, bootstrap_replacement=False)
print(f'{test=}')
```

To decompose, a first routine `raw_ks_test` computes the KS statistic for the provided distributions:

```python
from step_by_step_ks import raw_ks_test

test = raw_ks_test(data1, data2, alternative='1 less than 2', plot=True)
```

![ECDF plot](https://github.com/remyeltorro/step_by_step_ks/blob/main/assets/ecdf.png?raw=true)

Then to estimate the p-value one can perform a bootstrap to measure the KS statistic under the hypothesis that both distributions were sampled from the same distribution. 

```python
from step_by_step_ks import raw_ks_test

test = raw_ks_test(data1, data2, alternative='1 less than 2', plot=True)
reference_stat = test['stat']

pvalue = bootstrap_pvalue(data1, data2, reference_stat, alternative='1 less than 2', plot=True, nloop=1000, replacement=False)
pvalue
```

![KS statistic distribution](https://github.com/remyeltorro/step_by_step_ks/blob/main/assets/stat_dist.png?raw=true)
