"""
Standard Weights of Evidence calculations for 3D mineral prospectivity modeling.

This module implements the classical Weights of Evidence method for combining
multiple evidential layers to generate posterior probability maps.
"""

import logging
from typing import List, Optional, Tuple, Dict
from pathlib import Path
import pandas as pd

from . import core
from . import io as wofe_io

logger = logging.getLogger(__name__)


class WeightsOfEvidence:
    """
    Weights of Evidence calculator for 3D mineral prospectivity modeling.

    This class implements the classical WofE method, calculating positive and
    negative weights for evidential layers and combining them to produce
    posterior probability, odds, and logit values.

    Parameters
    ----------
    input_file : str
        Path to input CSV file with columns: X, Y, Z, Grade, Fac1, Fac2, ...
    threshold_target : float
        Threshold value for the target element to define deposits
    thresholds_factors : List[float]
        List of threshold values for each evidential factor
    output_dir : Optional[str], optional
        Directory for output files, by default "./output"

    Attributes
    ----------
    num_total : float
        Total number of voxels
    num_deposits : float
        Number of deposit-bearing voxels
    w_pos : List[float]
        Positive weights for each factor
    w_neg : List[float]
        Negative weights for each factor
    prior_p : float
        Prior probability
    prior_o : float
        Prior odds
    prior_l : float
        Prior logit
    """

    def __init__(
        self,
        input_file: str,
        threshold_target: float,
        thresholds_factors: List[float],
        output_dir: Optional[str] = None,
    ):
        self.input_file = Path(input_file)
        self.threshold_target = threshold_target
        self.thresholds_factors = thresholds_factors
        self.output_dir = Path(output_dir) if output_dir else Path("./output")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Validate input
        wofe_io.validate_input_file(str(self.input_file), min_columns=4 + len(thresholds_factors))

        # Initialize calculated values
        self.num_total: Optional[float] = None
        self.num_deposits: Optional[float] = None
        self.w_pos: Optional[List[float]] = None
        self.w_neg: Optional[List[float]] = None
        self.prior_p: Optional[float] = None
        self.prior_o: Optional[float] = None
        self.prior_l: Optional[float] = None

        logger.info(f"Initialized WeightsOfEvidence with {len(thresholds_factors)} factors")

    def calculate_counts(self) -> Tuple[float, float, List[float], List[float]]:
        """
        Calculate voxel counts for different categories.

        Returns
        -------
        Tuple[float, float, List[float], List[float]]
            num_total, num_deposits, num_binary, num_binary_deposits
        """
        data = wofe_io.read_csv_data(str(self.input_file))

        # Count total voxels
        num_total = float(len(data))

        # Count deposit-bearing voxels
        num_deposits = sum(1 for row in data if float(row[3]) > self.threshold_target)
        num_deposits = float(num_deposits)

        # Count anomalous voxels for each factor
        num_binary = [0.0] * len(self.thresholds_factors)
        for row in data:
            for i, threshold in enumerate(self.thresholds_factors):
                if float(row[i + 4]) > threshold:
                    num_binary[i] += 1

        # Count intersections of deposits and anomalous voxels
        num_binary_deposits = [0.0] * len(self.thresholds_factors)
        for row in data:
            if float(row[3]) > self.threshold_target:
                for i, threshold in enumerate(self.thresholds_factors):
                    if float(row[i + 4]) > threshold:
                        num_binary_deposits[i] += 1

        self.num_total = num_total
        self.num_deposits = num_deposits

        logger.info(f"Total voxels: {num_total}, Deposit voxels: {num_deposits}")
        logger.info(f"Binary counts: {num_binary}")
        logger.info(f"Binary-deposit intersections: {num_binary_deposits}")

        return num_total, num_deposits, num_binary, num_binary_deposits

    def calculate_weights(self) -> Tuple[List[float], List[float]]:
        """
        Calculate positive and negative weights for all factors.

        Returns
        -------
        Tuple[List[float], List[float]]
            Positive weights and negative weights
        """
        num_total, num_deposits, num_binary, num_binary_deposits = self.calculate_counts()

        # Calculate probabilities
        prob_bd, prob_bd_abs, prob_b_abs_d, prob_b_abs_d_abs = core.calculate_probabilities(
            num_total, num_deposits, num_binary, num_binary_deposits
        )

        # Calculate weights
        w_pos, w_neg = core.calculate_weights(
            prob_bd, prob_bd_abs, prob_b_abs_d, prob_b_abs_d_abs
        )

        # Calculate prior values
        prior_p, prior_o, prior_l = core.calculate_prior(num_deposits, num_total)

        self.w_pos = w_pos
        self.w_neg = w_neg
        self.prior_p = prior_p
        self.prior_o = prior_o
        self.prior_l = prior_l

        logger.info(f"Positive weights: {w_pos}")
        logger.info(f"Negative weights: {w_neg}")
        logger.info(f"Prior probability: {prior_p:.6f}, odds: {prior_o:.6f}, logit: {prior_l:.6f}")

        return w_pos, w_neg

    def generate_weights_file(self, output_file: Optional[str] = None) -> str:
        """
        Generate a file with weights assigned to each voxel.

        Parameters
        ----------
        output_file : Optional[str], optional
            Output file path, by default None (will use output_dir/weights.csv)

        Returns
        -------
        str
            Path to the generated file
        """
        if self.w_pos is None or self.w_neg is None:
            self.calculate_weights()

        if output_file is None:
            output_file = self.output_dir / "weights.csv"

        data = wofe_io.read_csv_data(str(self.input_file))
        output_data = []

        for row in data:
            output_row = [row[0], row[1], row[2]]  # X, Y, Z
            for i, threshold in enumerate(self.thresholds_factors):
                if float(row[i + 4]) > threshold:
                    output_row.append(self.w_pos[i])
                else:
                    output_row.append(self.w_neg[i])
            output_data.append(output_row)

        wofe_io.write_csv_data(str(output_file), output_data)
        logger.info(f"Generated weights file: {output_file}")
        return str(output_file)

    def generate_posterior_logit(
        self,
        weights_file: Optional[str] = None,
        output_file: Optional[str] = None,
    ) -> str:
        """
        Generate posterior logit values.

        Parameters
        ----------
        weights_file : Optional[str], optional
            Input weights file, by default None (will use generated weights)
        output_file : Optional[str], optional
            Output file path, by default None (will use output_dir/posterior_logit.csv)

        Returns
        -------
        str
            Path to the generated file
        """
        if weights_file is None:
            weights_file = self.generate_weights_file()

        if output_file is None:
            output_file = self.output_dir / "posterior_logit.csv"

        data = wofe_io.read_csv_data(weights_file)
        output_data = []

        for row in data:
            if len(row) > 1:
                weights = [float(w) for w in row[3:]]
                posterior_logit = core.calculate_posterior_logit(self.prior_l, weights)
                output_data.append([row[0], row[1], row[2], posterior_logit])

        wofe_io.write_csv_data(str(output_file), output_data)
        logger.info(f"Generated posterior logit file: {output_file}")
        return str(output_file)

    def generate_posterior_odds(
        self,
        logit_file: Optional[str] = None,
        output_file: Optional[str] = None,
    ) -> str:
        """
        Generate posterior odds values.

        Parameters
        ----------
        logit_file : Optional[str], optional
            Input logit file, by default None
        output_file : Optional[str], optional
            Output file path, by default None

        Returns
        -------
        str
            Path to the generated file
        """
        if logit_file is None:
            logit_file = self.generate_posterior_logit()

        if output_file is None:
            output_file = self.output_dir / "posterior_odds.csv"

        data = wofe_io.read_csv_data(logit_file)
        output_data = []

        for row in data:
            if len(row) > 1:
                posterior_odds = core.calculate_posterior_odds(float(row[3]))
                output_data.append([row[0], row[1], row[2], posterior_odds])

        wofe_io.write_csv_data(str(output_file), output_data)
        logger.info(f"Generated posterior odds file: {output_file}")
        return str(output_file)

    def generate_posterior_probability(
        self,
        odds_file: Optional[str] = None,
        output_file: Optional[str] = None,
    ) -> str:
        """
        Generate posterior probability values.

        Parameters
        ----------
        odds_file : Optional[str], optional
            Input odds file, by default None
        output_file : Optional[str], optional
            Output file path, by default None

        Returns
        -------
        str
            Path to the generated file
        """
        if odds_file is None:
            odds_file = self.generate_posterior_odds()

        if output_file is None:
            output_file = self.output_dir / "posterior_probability.csv"

        data = wofe_io.read_csv_data(odds_file)
        output_data = []

        for row in data:
            if len(row) > 1:
                posterior_prob = core.calculate_posterior_probability(float(row[3]))
                output_data.append([row[0], row[1], row[2], posterior_prob])

        wofe_io.write_csv_data(str(output_file), output_data)
        logger.info(f"Generated posterior probability file: {output_file}")
        return str(output_file)

    def run_complete_analysis(self) -> Dict[str, str]:
        """
        Run the complete WofE analysis pipeline.

        Returns
        -------
        Dict[str, str]
            Dictionary mapping output types to file paths
        """
        logger.info("Starting complete WofE analysis")

        # Calculate weights
        self.calculate_weights()

        # Generate all outputs
        weights_file = self.generate_weights_file()
        logit_file = self.generate_posterior_logit(weights_file)
        odds_file = self.generate_posterior_odds(logit_file)
        prob_file = self.generate_posterior_probability(odds_file)

        results = {
            "weights": weights_file,
            "posterior_logit": logit_file,
            "posterior_odds": odds_file,
            "posterior_probability": prob_file,
        }

        logger.info("Complete WofE analysis finished")
        return results
