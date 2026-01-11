"""
threedwofe: Three-dimensional Weights of Evidence for mineral prospectivity modeling

This package provides tools for 3D mineral prospectivity modeling using the Weights of
Evidence (WofE) method, including both ordinary and fuzzy WofE approaches.

Main modules:
- wofe: Standard Weights of Evidence calculations
- fuzzy_wofe: Fuzzy Weights of Evidence calculations
- utils: Utility functions for data processing
- io: Input/output operations for data handling
"""

__version__ = "1.0.0"
__author__ = "Ehsan Farahbakhsh, Richard Scott"
__license__ = "GPL-3.0"

from .wofe import WeightsOfEvidence
from .fuzzy_wofe import FuzzyWeightsOfEvidence

__all__ = [
    "WeightsOfEvidence",
    "FuzzyWeightsOfEvidence",
]
