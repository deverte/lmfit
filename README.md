# lmfit

lmfit — python package for fitting peaks data with theoretical curve:
<img src="https://latex.codecogs.com/gif.latex?Y&space;=&space;A_0&space;&plus;&space;A&space;\cdot&space;(t&space;-&space;t_0)&space;\cdot&space;e^{-&space;k&space;\cdot&space;(t&space;-&space;t_0)}" title="Y = A_0 + A \cdot (t - t_0) \cdot e^{- k \cdot (t - t_0)}" />
with parameters <img src="https://latex.codecogs.com/gif.latex?A_0" title="A_0" />, <img src="https://latex.codecogs.com/gif.latex?A" title="A" />, <img src="https://latex.codecogs.com/gif.latex?t_0" title="t_0" /> and <img src="https://latex.codecogs.com/gif.latex?k" title="k" />.
using Levenberg–Marquardt (LM) algorithm (see [Wikipedia — Levenberg–Marquardt algorithm](https://en.wikipedia.org/wiki/Levenberg%E2%80%93Marquardt_algorithm)).

---


- [Installation](#installation)
- [Documentation](#documentation)
    - [lmfit.fit](#lmfit.fit)
- [Usage](#usage)
- [Package information](#package-information)
- [License](#license)


---

## Installation
```sh
pip install https://github.com/deverte/lmfit/releases/download/v0.1.1/lmfit-0.1.1-py3-none-any.whl
```

or

```sh
pip install https://github.com/deverte/lmfit/releases/download/v0.1.1/lmfit-0.1.1.tar.gz
```

## Documentation
The main function of this package is `fit_peaks`.

### lmfit.fit(data, baseline=21.5, expansion=2, fp=200, A=4.5, k=0.2)
> Calculates theoretical parameters from an experimental curve with help of LM algorithm and returns theoretical curves, these parameters and their errors.  
>
> Args:  
&nbsp;&nbsp;&nbsp;&nbsp;`data` [*pandas.Series*]: Initial data.  
&nbsp;&nbsp;&nbsp;&nbsp;`baseline` [*float*]: Data separator line. Will be automatically calculated if `None` with std(data) + mean(data). Default: `None`.  
&nbsp;&nbsp;&nbsp;&nbsp;`expansion` [*int*]: Value at which the peaks will expand (on both directions). Default: `2`.  
&nbsp;&nbsp;&nbsp;&nbsp;`fp` [*int*]: Number of fitting points. Default: `200`.  
&nbsp;&nbsp;&nbsp;&nbsp;`A` [*float*]: Initial `A` parameter. Default: `4.5`.  
&nbsp;&nbsp;&nbsp;&nbsp;`k` [*float*]: Initial `k` parameter. Default: `0.2`.  
> 
> Returns:  
&nbsp;&nbsp;&nbsp;&nbsp;*pandas.Series*: Theoretical curves,  
&nbsp;&nbsp;&nbsp;&nbsp;*List[float]*: List of calculated parameters,  
&nbsp;&nbsp;&nbsp;&nbsp;*List[float]*: List of errors,  
&nbsp;&nbsp;&nbsp;&nbsp;*float*: Baseline value.  

Also you can read experimantal data and convert it to time series table with `read_data`.

### lmfit.read_data(data_path)
> Extracts experimantal data from table and transforms it to time series data. 
>
> Args:  
&nbsp;&nbsp;&nbsp;&nbsp;`data_path` [*str*]: Path to experimental data.   
> 
> Returns:  
&nbsp;&nbsp;&nbsp;&nbsp;*pandas.DataFrame*: Time series data table.  

## Usage
```py
import pandas as pd
import lmfit as lm

# Data selection
data_path = 'some/data/path'
track = 24

df = pd.read_data(data_path)
data = df[track] # Select required series

# Fitting settings
expansion = 2
fp = 200
# Theoretical curve parameters
A = 7
k = 1

# Fitting curves
theoretical_curves, parameters, qtf, baseline = lm.fit_peaks(
    data, baseline=None, expansion=expansion, fp=fp, A=A, k=k)

# Showing results
print('Parameters: ', parameters, 'qtf: ', qtf, 'baseline: ', baseline)

# Plotting
data.plot()
theoretical_curves.plot()
```

## Package information
Depends on these packages:
1. [NumPy](https://numpy.org/)
2. [pandas](https://pandas.pydata.org/)
3. [SciPy](https://www.scipy.org/)

## License
**[MIT](LICENSE)**