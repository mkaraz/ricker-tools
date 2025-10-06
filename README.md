# Ricker Wavelet Helpers

This small module provides conversions between a Ricker wavelet's peak (dominant) frequency parameter \(f\) and the time span between the two zero crossings that bracket t=0.

**Author:** Matt Karazincir  
**Created:** 2025-10-06

## Formula

Standard form assumed:

```
r(t) = (1 - 2 π² f² t²) * exp(- π² f² t²)
```

Zero crossings satisfy:
```
1 - 2 π² f² t² = 0  ⇒  t = ± 1 / (π f √2)
```
Time between the two zero crossings around t=0:
```
L = √2 / (π f)
```
Inverse:
```
f = √2 / (π L)
```

## Functions

- `zero_crossing_length_from_peak_freq(f)` → length(s) `L`
- `peak_freq_from_zero_crossing_length(length)` → frequency(ies) `f`
- `half_zero_crossing_ms_from_peak_freq(f)` → half of zero-crossing span in ms
- `peak_freq_from_half_zero_crossing_ms(half_ms)` → frequency from half-span ms

Both functions accept scalars or array-like inputs (NumPy vectorized) and raise `ValueError` if any input is non-positive.

## Quick Usage

```python
from ricker import (
    zero_crossing_length_from_peak_freq,
    peak_freq_from_zero_crossing_length,
)

f = 30.0  # Hz
L = zero_crossing_length_from_peak_freq(f)
print(f"Zero-crossing length: {L:.6f} s")

f_back = peak_freq_from_zero_crossing_length(L)
print(f"Recovered frequency: {f_back:.2f} Hz")

half_ms = half_zero_crossing_ms_from_peak_freq(f)
print(f"Half zero-crossing span: {half_ms:.4f} ms")

f_back2 = peak_freq_from_half_zero_crossing_ms(half_ms)
print(f"Recovered frequency (half-span invert): {f_back2:.2f} Hz")
```

Expected output (approximately):
```
Zero-crossing length: 0.015003 s
Recovered frequency: 30.00 Hz
```

## Testing

If you have `pytest` installed:
```
pytest -q
```

## Notes

If you use an alternate Ricker parameterization (e.g. different constant factors in the exponent), adjust the formulas accordingly. This implementation matches the common seismic definition shown above.

## Install (Editable)

```bash
pip install -e .
```

Then use the console script:

```bash
ricker --freq 30
```

Or from Python:

```python
from ricker import half_zero_crossing_ms_from_peak_freq
print(half_zero_crossing_ms_from_peak_freq(20))
```

## Command-Line Examples

```bash
# From frequency
ricker --freq 20

# From full zero-crossing length (seconds)
ricker --length 0.01500527

# From half zero-crossing span (ms)
ricker --half-ms 11.2539
```

## Publish to GitHub

1. Create a new empty repository on GitHub (e.g. `ricker-tools`).
2. Initialize and push:
    ```bash
    git init
    git add .
    git commit -m "Initial commit: Ricker tools"
    git branch -M main
    git remote add origin git@github.com:YOUR_USER/ricker-tools.git
    git push -u origin main
    ```

## Build a Distribution

```bash
python -m build
```

Upload (optional):
```bash
twine upload dist/*
```

## License

MIT (see `LICENSE`).

## Troubleshooting Installation ("no setup.py" error)

If someone sees an error about missing `setup.py` when running `pip install -e .`,
their pip/setuptools is too old to support modern PEP 660 editable installs.

Fix:

```bash
python -m pip install --upgrade pip setuptools wheel
pip install -e .
```

Legacy fallback: a minimal `setup.py` is included, so after upgrading it should work.
Verify versions:

```bash
python -m pip --version
python - <<'PY'
import setuptools, sys
print('setuptools', setuptools.__version__, 'python', sys.version)
PY
```

Recommended: pip ≥ 23, setuptools ≥ 68.
