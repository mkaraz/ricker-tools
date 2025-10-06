from setuptools import setup

# Minimal legacy fallback so older pip/setuptools (pre-PEP 660) editable installs
# that expect a setup.py don't fail. All metadata is in pyproject.toml.
# Usage (legacy env):
#   pip install -e .
# Modern environments will use pyproject.toml directly.

if __name__ == "__main__":
    setup()
