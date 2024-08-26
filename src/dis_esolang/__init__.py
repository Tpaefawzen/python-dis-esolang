"""
Implementation of esoteric language Dis; Malbolge's wimpmode

The I/O is done through sys.stdin and sys.stdout in binary mode (not in Unicode mode).
"""

__all__ = [
        "Dis"
        ]

from .dis_esolang import (
        Dis,
        )
