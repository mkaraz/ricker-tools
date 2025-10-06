"""Ricker wavelet helper functions.

Provides conversions between a Ricker wavelet's peak (dominant) frequency
parameter ``f`` in the standard time-domain expression and the time span
between the two zero crossings that straddle t=0.

Standard form used:

    r(t) = (1 - 2 * (pi**2) * f**2 * t**2) * exp(-(pi**2) * f**2 * t**2)

Zero crossings solve 1 - 2 * (pi**2) * f**2 * t**2 = 0 giving
    t = ± 1 / (pi * f * sqrt(2))

Therefore the time between those two zero crossings is:
    L = sqrt(2) / (pi * f)

and the inverse:
    f = sqrt(2) / (pi * L)

Both conversions are provided below. Functions are vectorized via NumPy,
and accept scalars or array-like inputs.
"""
from __future__ import annotations

from typing import Union, Sequence
import numpy as np

Number = Union[int, float, np.number]
ArrayLike = Union[Number, Sequence[Number], np.ndarray]

_SQRT2 = np.sqrt(2.0)
_PI = np.pi


def zero_crossing_length_from_peak_freq(f: ArrayLike) -> np.ndarray:
    """Return the zero-crossing span around t=0 for a Ricker wavelet.

    Given the peak (dominant/central) frequency parameter ``f`` (Hz) in the
    standard Ricker formula, compute the time distance (seconds) between the
    two zero crossings immediately surrounding t=0.

    Parameters
    ----------
    f : array_like
        Positive frequency or frequencies in Hz.

    Returns
    -------
    ndarray
        Zero-crossing length(s) in seconds (same shape as broadcast input).

    Raises
    ------
    ValueError
        If any frequency is non-positive.
    """
    f_arr = np.asarray(f, dtype=float)
    if np.any(f_arr <= 0):
        raise ValueError("Frequency values must be positive.")
    return _SQRT2 / (_PI * f_arr)


def peak_freq_from_zero_crossing_length(length: ArrayLike) -> np.ndarray:
    """Invert zero-crossing span to the Ricker peak frequency parameter.

    Parameters
    ----------
    length : array_like
        Positive time span(s) in seconds between the two zero crossings
        surrounding t=0.

    Returns
    -------
    ndarray
        Peak frequency value(s) in Hz (same shape as broadcast input).

    Raises
    ------
    ValueError
        If any length is non-positive.
    """
    length_arr = np.asarray(length, dtype=float)
    if np.any(length_arr <= 0):
        raise ValueError("Length values must be positive.")
    return _SQRT2 / (_PI * length_arr)


def half_zero_crossing_ms_from_peak_freq(f: ArrayLike) -> np.ndarray:
    """Return half the zero-crossing span in milliseconds for frequency ``f``.

    Computes 0.5 * L where L is the full zero-crossing distance in seconds,
    then converts to milliseconds.

    half_ms = 1000 * ( (sqrt(2) / (pi * f)) / 2 ) = 1000 * sqrt(2) / (2 * pi * f)

    Parameters
    ----------
    f : array_like
        Positive frequency or frequencies in Hz.

    Returns
    -------
    ndarray
        Half-span values in milliseconds.
    """
    f_arr = np.asarray(f, dtype=float)
    if np.any(f_arr <= 0):
        raise ValueError("Frequency values must be positive.")
    # 0.5 * L * 1000 ms/s  => sqrt(2)/(pi*f) * 0.5 * 1000
    return (1000.0 * _SQRT2) / (2.0 * _PI * f_arr)


def peak_freq_from_half_zero_crossing_ms(half_ms: ArrayLike) -> np.ndarray:
    """Invert half zero-crossing span in ms back to frequency ``f`` (Hz).

    From half_ms = 1000 * sqrt(2) / (2 * pi * f)
    ⇒ f = 1000 * sqrt(2) / (2 * pi * half_ms)

    Parameters
    ----------
    half_ms : array_like
        Positive half zero-crossing span(s) in milliseconds.

    Returns
    -------
    ndarray
        Frequency(ies) in Hz.
    """
    half_ms_arr = np.asarray(half_ms, dtype=float)
    if np.any(half_ms_arr <= 0):
        raise ValueError("Half-span values must be positive.")
    return (1000.0 * _SQRT2) / (2.0 * _PI * half_ms_arr)


def _demo() -> None:  # pragma: no cover - simple manual demo
    f = 30.0  # Hz
    L = zero_crossing_length_from_peak_freq(f)
    f_back = peak_freq_from_zero_crossing_length(L)
    print(f"Input f = {f} Hz -> zero-crossing length L = {L:.6f} s -> back-converted f = {f_back:.6f} Hz")


if __name__ == "__main__":  # pragma: no cover
    _demo()
