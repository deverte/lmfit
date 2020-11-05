"""Extraction and preprocessing peaks data."""

from typing import List

import pandas as pd


def baseline_cut(data: pd.Series, baseline: float) -> pd.Series:
    """Selects data above the baseline.

    Args:
        data: Initial data.
        baseline: Data separator line.

    Returns:
        pandas.Series: Data above the baseline.
    """
    return data[data > baseline]

def separate_peaks(data: pd.Series) -> List[pd.Series]:
    """Separates peaks from each other.

    Args:
        data: Data above baseline.

    Returns:
        List[pandas.Series]: List of separated peaks.
    """
    times = data.index
    peaks = [[]]
    for i, t in enumerate(times):
        if t - times[i - 1] > 1:
            peaks.append([])
        peaks[-1].append(t)
    return [data[p] for p in peaks]

def add_expansions(data: pd.Series, peaks: List[pd.Series], expansion: int) -> List[pd.Series]:
    """Expands data to specified value.

    Args:
        data: Initial data.
        peaks: Separated peaks.
        expansion: Value at which the peaks will expand (on both directions).

    Returns:
        List[pandas.Series]: List of separated peaks with expansion.
    """
    embedded_peaks = []
    for peak in peaks:
        start = peak.index[0] - expansion
        finish = peak.index[-1] + expansion + 1
        # Check interval
        while start < data.index[0]: start = start + 1
        while finish > data.index[-1]: finish = finish - 1 

        embedded_peaks.append(data[start : finish])
    return embedded_peaks