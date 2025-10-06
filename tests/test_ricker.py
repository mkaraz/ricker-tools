import math
import numpy as np
import sys, pathlib

# Ensure the project root (parent directory of tests) is on sys.path so that
# the module ricker.py can be imported when running pytest in environments
# that do not automatically add rootdir.
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ricker import (
    zero_crossing_length_from_peak_freq,
    peak_freq_from_zero_crossing_length,
    half_zero_crossing_ms_from_peak_freq,
    peak_freq_from_half_zero_crossing_ms,
)


def test_round_trip_scalar():
    f = 25.0
    L = zero_crossing_length_from_peak_freq(f)
    f_back = peak_freq_from_zero_crossing_length(L)
    assert math.isclose(f, float(f_back), rel_tol=1e-12)


def test_known_value():
    f = 30.0
    L = zero_crossing_length_from_peak_freq(f)
    # Expected L = sqrt(2) / (pi * f)
    expected = math.sqrt(2) / (math.pi * f)
    assert math.isclose(L, expected, rel_tol=1e-12)


def test_vectorized():
    freqs = np.array([10.0, 20.0, 40.0])
    lengths = zero_crossing_length_from_peak_freq(freqs)
    freqs_back = peak_freq_from_zero_crossing_length(lengths)
    assert np.allclose(freqs, freqs_back, rtol=1e-12)


def test_half_span_ms():
    f = 25.0
    half_ms = half_zero_crossing_ms_from_peak_freq(f)
    # Compute expected: (1000 * sqrt(2)) / (2 * pi * f)
    expected = 1000.0 * math.sqrt(2) / (2 * math.pi * f)
    assert math.isclose(float(half_ms), expected, rel_tol=1e-12)
    f_back = peak_freq_from_half_zero_crossing_ms(half_ms)
    assert math.isclose(f, float(f_back), rel_tol=1e-12)


def test_20_hz_values():
    f = 20.0
    # Full zero-crossing length L (s)
    L = zero_crossing_length_from_peak_freq(f)
    expected_L = math.sqrt(2) / (math.pi * f)
    assert math.isclose(float(L), expected_L, rel_tol=1e-12)
    # Half span in ms
    half_ms = half_zero_crossing_ms_from_peak_freq(f)
    expected_half_ms = 1000.0 * math.sqrt(2) / (2 * math.pi * f)
    assert math.isclose(float(half_ms), expected_half_ms, rel_tol=1e-12)
    # Round trips
    f_back1 = peak_freq_from_zero_crossing_length(L)
    f_back2 = peak_freq_from_half_zero_crossing_ms(half_ms)
    assert math.isclose(f, float(f_back1), rel_tol=1e-12)
    assert math.isclose(f, float(f_back2), rel_tol=1e-12)


def test_invalid_inputs():
    import pytest
    with pytest.raises(ValueError):
        zero_crossing_length_from_peak_freq(0)
    with pytest.raises(ValueError):
        peak_freq_from_zero_crossing_length(-1)
    with pytest.raises(ValueError):
        half_zero_crossing_ms_from_peak_freq(0)
    with pytest.raises(ValueError):
        peak_freq_from_half_zero_crossing_ms(0)
