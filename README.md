This Python package performs a step by step 2-sample Kolmogorov-Smirnov test supported by figures. The p-value is computed using a customizable Monte-Carlo method. 

Installation
============

To use the package, you must install Python3, e.g. through [Anaconda](https://www.anaconda.com/download). The package relies on standard Python libraries: `numpy`, `scipy`, `random`, `matplotlib`.

Download and extract the ZIP file, enter the folder and open a console locally.

``` console
	#pip install numpy scipy matplotlib random
	pip install -e .
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