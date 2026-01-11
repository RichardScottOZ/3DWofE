"""
Example: Basic Weights of Evidence Analysis

This example demonstrates how to use the threedwofe package for a basic
Weights of Evidence analysis.
"""

from threedwofe import WeightsOfEvidence

# Define input parameters
INPUT_FILE = "data.csv"  # Your input CSV file
THRESHOLD_TARGET = 0.4  # Threshold for target element (deposits)
THRESHOLDS_FACTORS = [0.5, 0.6, 0.7]  # Thresholds for each evidential factor
OUTPUT_DIR = "./results"  # Output directory

# Create WofE analyzer
wofe = WeightsOfEvidence(
    input_file=INPUT_FILE,
    threshold_target=THRESHOLD_TARGET,
    thresholds_factors=THRESHOLDS_FACTORS,
    output_dir=OUTPUT_DIR,
)

# Run complete analysis
results = wofe.run_complete_analysis()

# Print results
print("Analysis complete! Generated files:")
for key, filepath in results.items():
    print(f"  {key}: {filepath}")

# Access calculated values
print(f"\nStatistics:")
print(f"  Total voxels: {wofe.num_total}")
print(f"  Deposit voxels: {wofe.num_deposits}")
print(f"  Prior probability: {wofe.prior_p:.6f}")
print(f"  Positive weights: {wofe.w_pos}")
print(f"  Negative weights: {wofe.w_neg}")
