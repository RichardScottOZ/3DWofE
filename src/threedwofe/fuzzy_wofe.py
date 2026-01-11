"""
Fuzzy Weights of Evidence calculations for 3D mineral prospectivity modeling.

This module implements the fuzzy WofE method, which uses fuzzy membership
functions to handle continuous data and uncertainty in evidential layers.
"""

import logging
import math
from typing import List, Optional, Dict, Tuple
from pathlib import Path
import numpy as np

from . import core
from . import io as wofe_io

logger = logging.getLogger(__name__)


class FuzzyWeightsOfEvidence:
    """
    Fuzzy Weights of Evidence calculator for 3D mineral prospectivity modeling.

    This class implements the fuzzy WofE method, which is suitable for
    continuous data and uses fuzzy membership functions to assign weights.

    Parameters
    ----------
    input_file : str
        Path to input CSV file with columns: X, Y, Z, Grade, Fac1, Fac2, ...
    threshold_target : float
        Threshold value for the target element to define deposits
    output_dir : Optional[str], optional
        Directory for output files, by default "./output"

    Attributes
    ----------
    num_total : float
        Total number of voxels
    num_deposits : float
        Number of deposit-bearing voxels
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
        output_dir: Optional[str] = None,
    ):
        self.input_file = Path(input_file)
        self.threshold_target = threshold_target
        self.output_dir = Path(output_dir) if output_dir else Path("./output")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Validate input
        wofe_io.validate_input_file(str(self.input_file), min_columns=4)

        # Initialize calculated values
        self.num_total: Optional[float] = None
        self.num_deposits: Optional[float] = None
        self.prior_p: Optional[float] = None
        self.prior_o: Optional[float] = None
        self.prior_l: Optional[float] = None

        logger.info("Initialized FuzzyWeightsOfEvidence")

    def calculate_counts(self) -> Tuple[float, float]:
        """
        Calculate basic voxel counts.

        Returns
        -------
        Tuple[float, float]
            num_total, num_deposits
        """
        data = wofe_io.read_csv_data(str(self.input_file))

        # Count total voxels
        num_total = float(len(data))

        # Count deposit-bearing voxels
        num_deposits = sum(1 for row in data if float(row[3]) > self.threshold_target)
        num_deposits = float(num_deposits)

        self.num_total = num_total
        self.num_deposits = num_deposits

        # Calculate prior values
        self.prior_p, self.prior_o, self.prior_l = core.calculate_prior(
            num_deposits, num_total
        )

        logger.info(f"Total voxels: {num_total}, Deposit voxels: {num_deposits}")
        logger.info(f"Prior probability: {self.prior_p:.6f}")

        return num_total, num_deposits

    def calculate_fuzzy_weights(
        self,
        factor_index: int,
        percentiles: Optional[List[float]] = None,
    ) -> Tuple[List[float], List[float]]:
        """
        Calculate fuzzy weights for a continuous factor using percentile-based thresholds.

        Parameters
        ----------
        factor_index : int
            Index of the factor column (0-based after X,Y,Z,Grade columns)
        percentiles : Optional[List[float]], optional
            List of percentiles to use for thresholds, by default [10, 25, 50, 75, 90]

        Returns
        -------
        Tuple[List[float], List[float]]
            thresholds, fuzzy_weights
        """
        if percentiles is None:
            percentiles = [10, 25, 50, 75, 90]

        data = wofe_io.read_csv_data(str(self.input_file))

        # Extract factor values
        factor_col = 4 + factor_index
        factor_values = [float(row[factor_col]) for row in data if len(row) > factor_col]

        # Calculate percentile thresholds
        thresholds = [np.percentile(factor_values, p) for p in percentiles]

        # Calculate weights for each threshold range
        fuzzy_weights = []
        for i in range(len(thresholds) + 1):
            if i == 0:
                # Below first threshold
                count_total = sum(1 for v in factor_values if v <= thresholds[0])
                count_deposits = sum(
                    1
                    for row in data
                    if len(row) > factor_col
                    and float(row[3]) > self.threshold_target
                    and float(row[factor_col]) <= thresholds[0]
                )
            elif i == len(thresholds):
                # Above last threshold
                count_total = sum(1 for v in factor_values if v > thresholds[-1])
                count_deposits = sum(
                    1
                    for row in data
                    if len(row) > factor_col
                    and float(row[3]) > self.threshold_target
                    and float(row[factor_col]) > thresholds[-1]
                )
            else:
                # Between thresholds
                count_total = sum(
                    1 for v in factor_values if thresholds[i - 1] < v <= thresholds[i]
                )
                count_deposits = sum(
                    1
                    for row in data
                    if len(row) > factor_col
                    and float(row[3]) > self.threshold_target
                    and thresholds[i - 1] < float(row[factor_col]) <= thresholds[i]
                )

            # Calculate weight (avoid division by zero)
            if count_total > 0 and count_deposits > 0:
                prob_d_given_b = count_deposits / self.num_deposits
                prob_d_given_not_b = (count_total - count_deposits) / (
                    self.num_total - self.num_deposits
                )
                if prob_d_given_not_b > 0:
                    weight = math.log(prob_d_given_b / prob_d_given_not_b)
                else:
                    weight = 0.0
            else:
                weight = 0.0

            fuzzy_weights.append(weight)

        logger.info(f"Calculated fuzzy weights for factor {factor_index}")
        logger.info(f"Thresholds: {thresholds}")
        logger.info(f"Fuzzy weights: {fuzzy_weights}")

        return thresholds, fuzzy_weights

    def apply_fuzzy_weights(
        self,
        thresholds_list: List[List[float]],
        weights_list: List[List[float]],
        output_file: Optional[str] = None,
    ) -> str:
        """
        Apply fuzzy weights to continuous factors.

        Parameters
        ----------
        thresholds_list : List[List[float]]
            List of threshold lists for each factor
        weights_list : List[List[float]]
            List of weight lists for each factor
        output_file : Optional[str], optional
            Output file path, by default None

        Returns
        -------
        str
            Path to the generated file
        """
        if output_file is None:
            output_file = self.output_dir / "fuzzy_weights.csv"

        data = wofe_io.read_csv_data(str(self.input_file))
        output_data = []

        for row in data:
            output_row = [row[0], row[1], row[2]]  # X, Y, Z

            # Process each factor
            for factor_idx, (thresholds, weights) in enumerate(
                zip(thresholds_list, weights_list)
            ):
                factor_col = 4 + factor_idx
                if len(row) <= factor_col:
                    continue

                factor_value = float(row[factor_col])

                # Find appropriate weight based on thresholds
                weight = 0.0
                if factor_value <= thresholds[0]:
                    weight = weights[0]
                elif factor_value > thresholds[-1]:
                    weight = weights[-1]
                else:
                    for i in range(len(thresholds) - 1):
                        if thresholds[i] < factor_value <= thresholds[i + 1]:
                            weight = weights[i + 1]
                            break

                output_row.append(weight)

            output_data.append(output_row)

        wofe_io.write_csv_data(str(output_file), output_data)
        logger.info(f"Applied fuzzy weights to file: {output_file}")
        return str(output_file)

    def calculate_logistic_fuzzy_scores(
        self,
        factor_indices: List[int],
        output_file: Optional[str] = None,
    ) -> str:
        """
        Calculate fuzzy scores using logistic membership function.

        The logistic function transforms factor values into [0,1] fuzzy space,
        useful for P-V (Prediction-Volume) analysis.

        Parameters
        ----------
        factor_indices : List[int]
            Indices of factors to transform (0-based after X,Y,Z,Grade)
        output_file : Optional[str], optional
            Output file path, by default None

        Returns
        -------
        str
            Path to the generated file
        """
        if output_file is None:
            output_file = self.output_dir / "fuzzy_scores.csv"

        data = wofe_io.read_csv_data(str(self.input_file))

        # Calculate min and max for each factor
        min_max_values = []
        for factor_idx in factor_indices:
            factor_col = 4 + factor_idx
            values = [float(row[factor_col]) for row in data if len(row) > factor_col]
            min_max_values.append((min(values), max(values)))

        # Calculate logistic function parameters
        params = []
        for min_val, max_val in min_max_values:
            s = (2 * math.log(99)) / (max_val - min_val)
            i = (max_val + min_val) / 2
            params.append((s, i))

        # Apply logistic transformation
        output_data = []
        for row in data:
            output_row = [row[3]]  # Grade
            for factor_idx, (s, i) in zip(factor_indices, params):
                factor_col = 4 + factor_idx
                if len(row) > factor_col:
                    value = float(row[factor_col])
                    fuzzy_score = 1 / (1 + math.exp(-s * (value - i)))
                    output_row.append(fuzzy_score)
            output_data.append(output_row)

        wofe_io.write_csv_data(str(output_file), output_data)
        logger.info(f"Generated fuzzy scores using logistic function: {output_file}")
        return str(output_file)

    def generate_posterior_probability(
        self,
        weights_file: str,
        output_file: Optional[str] = None,
    ) -> str:
        """
        Generate posterior probability from fuzzy weights.

        Parameters
        ----------
        weights_file : str
            Input file with fuzzy weights
        output_file : Optional[str], optional
            Output file path, by default None

        Returns
        -------
        str
            Path to the generated file
        """
        if self.prior_l is None:
            self.calculate_counts()

        if output_file is None:
            output_file = self.output_dir / "fuzzy_posterior_probability.csv"

        data = wofe_io.read_csv_data(weights_file)
        output_data = []

        for row in data:
            if len(row) > 3:
                weights = [float(w) for w in row[3:]]
                posterior_logit = core.calculate_posterior_logit(self.prior_l, weights)
                posterior_odds = core.calculate_posterior_odds(posterior_logit)
                posterior_prob = core.calculate_posterior_probability(posterior_odds)
                output_data.append([row[0], row[1], row[2], posterior_prob])

        wofe_io.write_csv_data(str(output_file), output_data)
        logger.info(f"Generated fuzzy posterior probability file: {output_file}")
        return str(output_file)
