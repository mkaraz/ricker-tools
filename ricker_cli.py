#!/usr/bin/env python3
"""Command-line interface for Ricker wavelet conversions.

Examples:
  # From peak frequency to full and half spans
  python ricker_cli.py --freq 30

  # From full zero-crossing length (seconds) to frequency
  python ricker_cli.py --length 0.0150053

  # From half zero-crossing span (milliseconds) to frequency
  python ricker_cli.py --half-ms 5.62697

If multiple inputs are given, they must be consistent; conversions are
printed for whichever argument you supply. Only one of --freq, --length,
--half-ms should normally be specified.
"""
from __future__ import annotations

import argparse
from typing import Optional

from ricker import (
    zero_crossing_length_from_peak_freq,
    peak_freq_from_zero_crossing_length,
    half_zero_crossing_ms_from_peak_freq,
    peak_freq_from_half_zero_crossing_ms,
)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Ricker wavelet conversion tool")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument(
        "--freq", type=float, help="Peak (dominant) frequency in Hz"
    )
    g.add_argument(
        "--length", type=float, help="Full zero-crossing span L in seconds"
    )
    g.add_argument(
        "--half-ms", type=float, help="Half zero-crossing span in milliseconds"
    )
    p.add_argument(
        "--precision",
        type=int,
        default=6,
        help="Decimal places for output (default 6)",
    )
    return p


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    prec = args.precision
    # Build a numeric formatting function respecting precision
    def fmt(x: float) -> str:
        return f"{x:.{prec}f}"

    if args.freq is not None:
        f_val = args.freq
        try:
            L_val = float(zero_crossing_length_from_peak_freq(f_val))
            half_ms_val = float(half_zero_crossing_ms_from_peak_freq(f_val))
        except ValueError as e:  # pragma: no cover
            parser.error(str(e))
        print(f"Input frequency (Hz): {fmt(f_val)}")
        print(f"Zero-crossing length L (s): {fmt(L_val)}")
        print(f"Half zero-crossing span (ms): {fmt(half_ms_val)}")
        return 0

    if args.length is not None:
        L_val = args.length
        try:
            f_val = float(peak_freq_from_zero_crossing_length(L_val))
            half_ms_val = float(half_zero_crossing_ms_from_peak_freq(f_val))
        except ValueError as e:  # pragma: no cover
            parser.error(str(e))
        print(f"Input zero-crossing length L (s): {fmt(L_val)}")
        print(f"Frequency (Hz): {fmt(f_val)}")
        print(f"Half zero-crossing span (ms): {fmt(half_ms_val)}")
        return 0

    if args.half_ms is not None:
        half_ms_val = args.half_ms
        try:
            f_val = float(peak_freq_from_half_zero_crossing_ms(half_ms_val))
            L_val = float(zero_crossing_length_from_peak_freq(f_val))
        except ValueError as e:  # pragma: no cover
            parser.error(str(e))
        print(f"Input half zero-crossing span (ms): {fmt(half_ms_val)}")
        print(f"Frequency (Hz): {fmt(f_val)}")
        print(f"Zero-crossing length L (s): {fmt(L_val)}")
        return 0

    parser.error("No valid option provided")  # pragma: no cover
    return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
