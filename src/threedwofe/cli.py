"""
Command-line interface for threedwofe package.

This module provides a user-friendly CLI for running Weights of Evidence analyses.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import List

from . import __version__
from .wofe import WeightsOfEvidence
from .fuzzy_wofe import FuzzyWeightsOfEvidence

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


def parse_float_list(value: str) -> List[float]:
    """Parse a comma-separated string of floats."""
    try:
        return [float(x.strip()) for x in value.split(",")]
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"Invalid float list: {e}")


def cmd_wofe(args):
    """Run standard Weights of Evidence analysis."""
    logger.info("Starting standard WofE analysis")
    logger.info(f"Input file: {args.input}")
    logger.info(f"Target threshold: {args.threshold_target}")
    logger.info(f"Factor thresholds: {args.thresholds_factors}")
    logger.info(f"Output directory: {args.output}")

    try:
        wofe = WeightsOfEvidence(
            input_file=args.input,
            threshold_target=args.threshold_target,
            thresholds_factors=args.thresholds_factors,
            output_dir=args.output,
        )

        results = wofe.run_complete_analysis()

        logger.info("Analysis complete! Generated files:")
        for key, filepath in results.items():
            logger.info(f"  {key}: {filepath}")

        return 0

    except Exception as e:
        logger.error(f"Error during WofE analysis: {e}", exc_info=True)
        return 1


def cmd_fuzzy(args):
    """Run fuzzy Weights of Evidence analysis."""
    logger.info("Starting fuzzy WofE analysis")
    logger.info(f"Input file: {args.input}")
    logger.info(f"Target threshold: {args.threshold_target}")
    logger.info(f"Output directory: {args.output}")

    try:
        fuzzy_wofe = FuzzyWeightsOfEvidence(
            input_file=args.input,
            threshold_target=args.threshold_target,
            output_dir=args.output,
        )

        # Calculate counts and prior
        fuzzy_wofe.calculate_counts()

        # Calculate fuzzy weights for each factor if specified
        if args.factor_indices:
            thresholds_list = []
            weights_list = []

            for factor_idx in args.factor_indices:
                thresholds, weights = fuzzy_wofe.calculate_fuzzy_weights(
                    factor_index=factor_idx,
                    percentiles=args.percentiles,
                )
                thresholds_list.append(thresholds)
                weights_list.append(weights)

            # Apply fuzzy weights
            weights_file = fuzzy_wofe.apply_fuzzy_weights(thresholds_list, weights_list)
            logger.info(f"Generated fuzzy weights: {weights_file}")

            # Generate posterior probability
            prob_file = fuzzy_wofe.generate_posterior_probability(weights_file)
            logger.info(f"Generated posterior probability: {prob_file}")

        # Generate fuzzy scores if requested
        if args.logistic_factors:
            scores_file = fuzzy_wofe.calculate_logistic_fuzzy_scores(
                factor_indices=args.logistic_factors
            )
            logger.info(f"Generated fuzzy scores: {scores_file}")

        logger.info("Fuzzy WofE analysis complete!")
        return 0

    except Exception as e:
        logger.error(f"Error during fuzzy WofE analysis: {e}", exc_info=True)
        return 1


def cmd_version(args):
    """Print version information."""
    print(f"threedwofe version {__version__}")
    return 0


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog="threedwofe",
        description="Three-dimensional Weights of Evidence for mineral prospectivity modeling",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Standard WofE analysis
  threedwofe wofe -i data.csv -t 0.4 -f 0.5,0.6,0.7 -o ./results

  # Fuzzy WofE analysis
  threedwofe fuzzy -i data.csv -t 0.4 --factor-indices 0,1,2 -o ./results

  # Generate fuzzy scores with logistic function
  threedwofe fuzzy -i data.csv -t 0.4 --logistic-factors 0,1 -o ./results

For more information, visit: https://github.com/RichardScottOZ/3DWofE
        """,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Standard WofE command
    wofe_parser = subparsers.add_parser(
        "wofe",
        help="Run standard Weights of Evidence analysis",
        description="Calculate weights of evidence and posterior probabilities using binary thresholds.",
    )
    wofe_parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Input CSV file with columns: X, Y, Z, Grade, Fac1, Fac2, ...",
    )
    wofe_parser.add_argument(
        "-t",
        "--threshold-target",
        type=float,
        required=True,
        help="Threshold value for target element to define deposits",
    )
    wofe_parser.add_argument(
        "-f",
        "--thresholds-factors",
        type=parse_float_list,
        required=True,
        help="Comma-separated threshold values for each factor (e.g., 0.5,0.6,0.7)",
    )
    wofe_parser.add_argument(
        "-o",
        "--output",
        default="./output",
        help="Output directory for results (default: ./output)",
    )
    wofe_parser.set_defaults(func=cmd_wofe)

    # Fuzzy WofE command
    fuzzy_parser = subparsers.add_parser(
        "fuzzy",
        help="Run fuzzy Weights of Evidence analysis",
        description="Calculate fuzzy weights of evidence for continuous data.",
    )
    fuzzy_parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Input CSV file with columns: X, Y, Z, Grade, Fac1, Fac2, ...",
    )
    fuzzy_parser.add_argument(
        "-t",
        "--threshold-target",
        type=float,
        required=True,
        help="Threshold value for target element to define deposits",
    )
    fuzzy_parser.add_argument(
        "--factor-indices",
        type=lambda x: [int(i) for i in x.split(",")],
        help="Comma-separated factor indices to process (0-based, e.g., 0,1,2)",
    )
    fuzzy_parser.add_argument(
        "--percentiles",
        type=parse_float_list,
        default=[10, 25, 50, 75, 90],
        help="Comma-separated percentiles for thresholds (default: 10,25,50,75,90)",
    )
    fuzzy_parser.add_argument(
        "--logistic-factors",
        type=lambda x: [int(i) for i in x.split(",")],
        help="Comma-separated factor indices for logistic fuzzy scores (0-based)",
    )
    fuzzy_parser.add_argument(
        "-o",
        "--output",
        default="./output",
        help="Output directory for results (default: ./output)",
    )
    fuzzy_parser.set_defaults(func=cmd_fuzzy)

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Execute command
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
