# 3DWofE - Three-dimensional Weights of Evidence

[![DOI](https://zenodo.org/badge/205634309.svg)](https://zenodo.org/badge/latestdoi/205634309)

A professional Python package for 3D mineral prospectivity modeling using the Weights of Evidence (WofE) method.

## Overview

This package provides robust and efficient tools for three-dimensional weights of evidence modeling in mineral exploration. It implements both ordinary and fuzzy WofE approaches for combining multiple evidential layers to generate posterior probability maps.

**Key Features:**
- 🎯 Standard Weights of Evidence calculations
- 🌟 Fuzzy Weights of Evidence for continuous data
- 📊 Comprehensive statistical outputs
- 🚀 Efficient processing of large 3D datasets
- 💻 Command-line interface and Python API
- 📝 Well-documented with type hints
- 🔧 Modern Python packaging (pip installable)

## Installation

### From source

```bash
# Clone the repository
git clone https://github.com/RichardScottOZ/3DWofE.git
cd 3DWofE

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### From PyPI (when published)

```bash
pip install threedwofe
```

## Quick Start

### Command Line Interface

#### Standard WofE Analysis

```bash
threedwofe wofe \
  --input data.csv \
  --threshold-target 0.4 \
  --thresholds-factors 0.5,0.6,0.7 \
  --output ./results
```

#### Fuzzy WofE Analysis

```bash
threedwofe fuzzy \
  --input data.csv \
  --threshold-target 0.4 \
  --factor-indices 0,1,2 \
  --output ./fuzzy_results
```

### Python API

#### Standard WofE

```python
from threedwofe import WeightsOfEvidence

# Create analyzer
wofe = WeightsOfEvidence(
    input_file="data.csv",
    threshold_target=0.4,
    thresholds_factors=[0.5, 0.6, 0.7],
    output_dir="./results"
)

# Run complete analysis
results = wofe.run_complete_analysis()

# Access results
print(f"Prior probability: {wofe.prior_p:.6f}")
print(f"Positive weights: {wofe.w_pos}")
print(f"Negative weights: {wofe.w_neg}")
```

#### Fuzzy WofE

```python
from threedwofe import FuzzyWeightsOfEvidence

# Create analyzer
fuzzy_wofe = FuzzyWeightsOfEvidence(
    input_file="data.csv",
    threshold_target=0.4,
    output_dir="./fuzzy_results"
)

# Calculate fuzzy weights
thresholds, weights = fuzzy_wofe.calculate_fuzzy_weights(
    factor_index=0,
    percentiles=[10, 25, 50, 75, 90]
)

# Generate posterior probability
weights_file = fuzzy_wofe.apply_fuzzy_weights([thresholds], [weights])
prob_file = fuzzy_wofe.generate_posterior_probability(weights_file)
```

## Input Data Format

The input CSV file should have the following column structure:

```
X, Y, Z, Grade, Factor1, Factor2, Factor3, ...
```

- **X, Y, Z**: Spatial coordinates of voxels
- **Grade**: Target element concentration (used to define deposits)
- **Factor1, Factor2, ...**: Evidential factors/features

Example:
```csv
100.5,200.3,50.0,0.45,0.62,0.78,0.55
100.5,200.3,51.0,0.38,0.51,0.69,0.48
...
```

## Output Files

The package generates several output files:

### Standard WofE
- `weights.csv`: Assigned weights (positive/negative) for each voxel
- `posterior_logit.csv`: Posterior logit values
- `posterior_odds.csv`: Posterior odds values
- `posterior_probability.csv`: Final posterior probability values

### Fuzzy WofE
- `fuzzy_weights.csv`: Fuzzy weights for each voxel
- `fuzzy_scores.csv`: Fuzzy membership scores (logistic function)
- `fuzzy_posterior_probability.csv`: Final posterior probability values

## Methodology

### Weights of Evidence

The WofE method is a Bayesian approach for combining evidence from multiple sources. It calculates:

1. **Prior Probability**: Base probability of mineralization
2. **Positive Weight (W+)**: Evidence supporting mineralization
3. **Negative Weight (W-)**: Evidence against mineralization
4. **Posterior Probability**: Updated probability after combining evidence

### Fuzzy WofE

The fuzzy approach extends classical WofE to handle:
- Continuous data (no hard thresholds)
- Uncertainty in evidential layers
- Gradual transitions using fuzzy membership functions

## Examples

See the `examples/` directory for detailed usage examples:
- `basic_wofe.py`: Standard WofE analysis
- `fuzzy_wofe.py`: Fuzzy WofE analysis

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black src/
```

### Type Checking

```bash
mypy src/
```

## Architecture

The package is organized into modular components:

```
threedwofe/
├── __init__.py          # Package initialization
├── core.py              # Core mathematical functions
├── wofe.py              # Standard WofE implementation
├── fuzzy_wofe.py        # Fuzzy WofE implementation
├── io.py                # Input/output operations
└── cli.py               # Command-line interface
```

## References

1. Bonham-Carter, G. F., Agterberg, F. P., Wright, D. F., 1989, Weights of evidence modelling: a new approach to mapping mineral potential, in: Statistical Applications in the Earth Sciences, Geological Survey of Canada, 171–183

2. Bonham-Carter, G. F., 1994, Geographic Information Systems for Geoscientists: Modeling with GIS, Elsevier

3. Cheng, Q., Agterberg, F. P., 1999, Fuzzy weights of evidence method and its application in mineral potential mapping, Natural Resources Research, 8, 27–35

4. Farahbakhsh, E., Hezarkhani, A., Eslamkish, T., Bahroudi, A., Chandra, R., 2020, Three-dimensional weights of evidence modeling of a concealed porphyry Cu deposit in Iran, Geochemistry: Exploration, Environment, Analysis

5. Farahbakhsh, E., Hezarkhani, A., Eslamkish, T., Bahroudi, A., Chandra, R., 2020, 3DWofE: An open-source software for three-dimensional weights of evidence modeling, Software Impacts

## Workflow

![Workflow Chart](https://user-images.githubusercontent.com/72196131/140813238-8f3d4ca0-5a63-4278-85df-f05f480078f2.png)

For more details, see the [workflow paper](https://www.sciencedirect.com/science/article/pii/S2665963820300300).

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this software in your research, please cite:

```bibtex
@software{3dwofe2020,
  author = {Farahbakhsh, Ehsan and Scott, Richard},
  title = {3DWofE: Three-dimensional Weights of Evidence},
  year = {2020},
  publisher = {GitHub},
  url = {https://github.com/RichardScottOZ/3DWofE},
  doi = {10.5281/zenodo.205634309}
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or contributions, please visit:
- GitHub Issues: https://github.com/RichardScottOZ/3DWofE/issues
- Repository: https://github.com/RichardScottOZ/3DWofE

## Acknowledgments

Original research by Ehsan Farahbakhsh and collaborators. This package version refactored for robustness, efficiency, and clarity.

Also see the CodeOcean capsule: https://codeocean.com/capsule/6217621/tree/v1
