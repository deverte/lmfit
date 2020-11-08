"""Fitting peaks data with theoretical curve: 'A_0 + A · (t - t_0) · exp(- k · (t - t_0))'.

Fitting peaks data with theoretical curve: 'A_0 + A · (t - t_0) · exp(- k · (t - t_0))' using
Levenberg–Marquardt (LM) algorithm
(see. https://en.wikipedia.org/wiki/Levenberg%E2%80%93Marquardt_algorithm).

    Typical usage example:

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
"""

from typing import List
from typing import Tuple

import numpy as np
import pandas as pd
from scipy import optimize

from . import data_extraction as de


def theoretical_curve(solution: List[float], t: List[float]) -> List[float]:
    """Builds theoretical curve with the found parameters.

    Builds theoretical curve 'A_0 + A · (t - t_0) · exp(- k · (t - t_0))' with the found parameters
    `A_0`, `A`, `t_0`, `k`.

    Args:
        solution: List of an arguments `A_0`, `A`, `t_0`, `k`.
        t: List of times corresponding to peak times.

    Returns:
        list: Theoretical curve data.
    """
    return solution[0] + solution[1] * (t - solution[2]) * np.exp(- solution[3] * (t - solution[2]))

def vec_curve(Y: List[float], t: List[float], roots: List[float]) -> List[float]:
    """Prepares curve for LM algorithm.

    Prepares curve 'A_0 + A · (t - t_0) · exp(- k · (t - t_0))' for LM algorithm for finding
    `A_0`, `A`, `t_0`, `k` parameters.

    Args:
        Y: List of an experimental data.
        t: List of times.
        roots: Initial parameters data.

    Returns:
        list: Prepared curve for LM algorithm with vectorized parameters.
    """
    return Y - (roots[0] + roots[1] * (t - roots[2]) * np.exp(- roots[3] * (t - roots[2])))

def auto_baseline(data):
    numeric_values = list(filter(lambda value: not np.isnan(value), data))
    return np.mean(numeric_values) + np.std(numeric_values)

def fit_peaks(
    data: pd.Series, baseline: float = None, expansion: int = 2,
    fp: int = 200, A: float = 4.5, k: float = 0.2) -> Tuple[pd.Series, List[float], List[float], float]:
    """Calculates theoretical parameters from an experimental curve with help of LM algorithm.

    Calculates theoretical parameters from an experimental curve with help of LM algorithm and
    returns theoretical curves, these parameters and their errors.

    Args:
        data: Initial data.
        baseline: Data separator line. Will be automatically calculated if `None` with
            std(data) + mean(data). Default: None
        expansion: Value at which the peaks will expand (on both directions).
        fp: Number of fitting points.
        A: `A` parameter.
        k: `k` parameter.

    Returns:
        pd.Series: Theoretical curves,
        List[float]: List of calculated parameters,
        List[float]: List of errors,
        float: Baseline value.
    """
    if baseline is None:
        baseline = auto_baseline(data)

    data_above_baseline = de.baseline_cut(data, baseline)
    peaks = de.separate_peaks(data_above_baseline)
    embedded_peaks = de.add_expansions(data, peaks, expansion)

    theoretical_curves = pd.Series()
    parameters = []
    qtf = []
    for peak in embedded_peaks:
        # Initial parameters
        A_0 = peak.iloc[0]
        t_0 = peak.index[0]
        
        sol = optimize.root(
            lambda x: vec_curve(peak.values, peak.index, x),
            [A_0, A, t_0, k],
            method='lm')
        sol_parameters = np.abs(sol.x)
        sol_qtf = np.abs(sol.qtf)

        if check_peak(A_0, A, t_0, sol_qtf, peak):
            fitting_times = np.linspace(peak.index[0], peak.index[-1], fp)

            theoretical_curve_data = theoretical_curve(sol_parameters, fitting_times)
            theoretical_curve_series = pd.Series(data=theoretical_curve_data, index=fitting_times)

            theoretical_curves = theoretical_curves.append(theoretical_curve_series)
            parameters.append(sol_parameters)
            qtf.append(sol_qtf)
    
    return theoretical_curves, parameters, qtf, baseline

def check_peak(A_0, A, t_0, qtf, peak):
    """Checks peak on some conditions.

    Check peak with conditions:
    1. A_0 / A * exp > 1.
    2. t_0 > 0
    3. std(qtf) < 100
    4. peak amplitude > 5

    Args:
        A_0: `A_0` parameter.
        A: `A` parameter.
        t_0: `t_0` parameter.
        qtf: Error.
        peak: Peak data.
    
    Returns:
        bool: `True` if conditions are done, else `False`.
    """
    peak_amplitude = np.max(peak) - np.min(peak)
    if (A_0 / A * np.exp(1) > 1) and (t_0 > 0) and (np.std(qtf) < 100) and (peak_amplitude > 5):
        return True
    else:
        return False