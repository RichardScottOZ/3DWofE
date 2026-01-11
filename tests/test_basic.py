"""
Basic smoke tests for the threedwofe package.

These tests verify that the package can be imported and basic functionality works.
"""

import pytest
import tempfile
import os
from pathlib import Path


def test_package_import():
    """Test that the package can be imported."""
    import threedwofe
    assert threedwofe.__version__ == "1.0.0"


def test_wofe_import():
    """Test that WeightsOfEvidence can be imported."""
    from threedwofe import WeightsOfEvidence
    assert WeightsOfEvidence is not None


def test_fuzzy_wofe_import():
    """Test that FuzzyWeightsOfEvidence can be imported."""
    from threedwofe import FuzzyWeightsOfEvidence
    assert FuzzyWeightsOfEvidence is not None


def test_wofe_initialization():
    """Test that WeightsOfEvidence can be initialized."""
    from threedwofe import WeightsOfEvidence
    
    # Create a temporary CSV file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        # Write sample data: X, Y, Z, Grade, Fac1, Fac2, Fac3
        f.write("100,200,50,0.5,0.6,0.7,0.8\n")
        f.write("100,200,51,0.3,0.4,0.5,0.6\n")
        f.write("100,200,52,0.6,0.7,0.8,0.9\n")
        f.write("101,200,50,0.4,0.5,0.6,0.7\n")
        f.write("101,200,51,0.2,0.3,0.4,0.5\n")
        temp_file = f.name
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            wofe = WeightsOfEvidence(
                input_file=temp_file,
                threshold_target=0.4,
                thresholds_factors=[0.5, 0.6, 0.7],
                output_dir=temp_dir,
            )
            assert wofe is not None
            assert wofe.input_file == Path(temp_file)
            assert wofe.threshold_target == 0.4
            assert wofe.thresholds_factors == [0.5, 0.6, 0.7]
    finally:
        os.unlink(temp_file)


def test_fuzzy_wofe_initialization():
    """Test that FuzzyWeightsOfEvidence can be initialized."""
    from threedwofe import FuzzyWeightsOfEvidence
    
    # Create a temporary CSV file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        # Write sample data: X, Y, Z, Grade, Fac1, Fac2
        f.write("100,200,50,0.5,0.6,0.7\n")
        f.write("100,200,51,0.3,0.4,0.5\n")
        f.write("100,200,52,0.6,0.7,0.8\n")
        temp_file = f.name
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            fuzzy_wofe = FuzzyWeightsOfEvidence(
                input_file=temp_file,
                threshold_target=0.4,
                output_dir=temp_dir,
            )
            assert fuzzy_wofe is not None
            assert fuzzy_wofe.input_file == Path(temp_file)
            assert fuzzy_wofe.threshold_target == 0.4
    finally:
        os.unlink(temp_file)


def test_core_functions():
    """Test core utility functions."""
    from threedwofe.core import calculate_prior, calculate_posterior_probability
    
    # Test prior calculation
    prior_p, prior_o, prior_l = calculate_prior(10.0, 100.0)
    assert 0 < prior_p < 1
    assert prior_o > 0
    
    # Test posterior probability calculation
    posterior_prob = calculate_posterior_probability(2.0)
    assert 0 < posterior_prob < 1
