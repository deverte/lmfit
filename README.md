# lmfit

lmfit — python package for fitting peaks data with theoretical curve:
<img src="https://latex.codecogs.com/gif.latex?Y&space;=&space;A_0&space;&plus;&space;A&space;\cdot&space;(t&space;-&space;t_0)&space;\cdot&space;e^{-&space;k&space;\cdot&space;(t&space;-&space;t_0)}" title="Y = A_0 + A \cdot (t - t_0) \cdot e^{- k \cdot (t - t_0)}" />
with parameters <img src="https://latex.codecogs.com/gif.latex?A_0" title="A_0" />, <img src="https://latex.codecogs.com/gif.latex?A" title="A" />, <img src="https://latex.codecogs.com/gif.latex?t_0" title="t_0" /> and <img src="https://latex.codecogs.com/gif.latex?k" title="k" />.
using Levenberg–Marquardt (LM) algorithm (see [Wikipedia — Levenberg–Marquardt algorithm](https://en.wikipedia.org/wiki/Levenberg%E2%80%93Marquardt_algorithm)).

---


- [Installation](#installation)
- [Usage](#usage)
- [Package information](#package-information)
- [License](#license)


---

## Installation
```sh
pip install https://github.com/deverte/lmfit/releases/download/v0.1.0/lmfit-0.1.0-py3-none-any.whl
```

or

```sh
pip install https://github.com/deverte/lmfit/releases/download/v0.1.0/lmfit-0.1.0.tar.gz
```

## Usage
```py
import pandas as pd
import lmfit as lm

# Data selection
data_path = 'some/data/path'
df = pd.read_csv(data_path, sep=',', decimal='.', index_col=0, na_values='')
data = df['Track 0'] # Select required series

# Fitting settings
baseline = 21.5
expansion = 2
fp = 200
# Theoretical curve parameters
A = 4.5
k = 0.2

# Fitting curves
theoretical_curves, parameters, qtf = lmfit.fit_peaks(
    data, baseline=baseline, expansion=expansion, fp=fp, A=A, k=k)

# Showing results
print('Parameters:', parameters, 'qtf:', qtf)

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