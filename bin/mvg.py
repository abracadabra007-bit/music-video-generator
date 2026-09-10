#!/usr/bin/env python
"""Alternative entry point for the CLI interface on Windows."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.cli import cli


if __name__ == '__main__':
    cli()
