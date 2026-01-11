"""
Example: Fuzzy Weights of Evidence Analysis

This example demonstrates how to use fuzzy WofE for continuous data.
"""

from threedwofe import FuzzyWeightsOfEvidence

# Define input parameters
INPUT_FILE = "data.csv"  # Your input CSV file
THRESHOLD_TARGET = 0.4  # Threshold for target element (deposits)
OUTPUT_DIR = "./fuzzy_results"  # Output directory

# Factor indices to process (0-based, after X, Y, Z, Grade columns)
FACTOR_INDICES = [0, 1, 2]

# Create fuzzy WofE analyzer
fuzzy_wofe = FuzzyWeightsOfEvidence(
    input_file=INPUT_FILE,
    threshold_target=THRESHOLD_TARGET,
    output_dir=OUTPUT_DIR,
)

# Calculate basic statistics
fuzzy_wofe.calculate_counts()
print(f"Total voxels: {fuzzy_wofe.num_total}")
print(f"Deposit voxels: {fuzzy_wofe.num_deposits}")
print(f"Prior probability: {fuzzy_wofe.prior_p:.6f}")

# Calculate fuzzy weights for each factor
thresholds_list = []
weights_list = []

for factor_idx in FACTOR_INDICES:
    print(f"\nProcessing factor {factor_idx}...")
    thresholds, weights = fuzzy_wofe.calculate_fuzzy_weights(
        factor_index=factor_idx,
        percentiles=[10, 25, 50, 75, 90],
    )
    thresholds_list.append(thresholds)
    weights_list.append(weights)
    print(f"  Thresholds: {thresholds}")
    print(f"  Weights: {weights}")

# Apply fuzzy weights
weights_file = fuzzy_wofe.apply_fuzzy_weights(thresholds_list, weights_list)
print(f"\nGenerated fuzzy weights: {weights_file}")

# Generate posterior probability
prob_file = fuzzy_wofe.generate_posterior_probability(weights_file)
print(f"Generated posterior probability: {prob_file}")

# Generate fuzzy scores using logistic function
scores_file = fuzzy_wofe.calculate_logistic_fuzzy_scores(factor_indices=FACTOR_INDICES)
print(f"Generated fuzzy scores: {scores_file}")

print("\nFuzzy WofE analysis complete!")
