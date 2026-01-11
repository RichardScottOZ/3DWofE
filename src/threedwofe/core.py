"""
Core utilities for Weights of Evidence calculations.

This module provides common mathematical and statistical functions used in both
standard and fuzzy WofE calculations.
"""

import math
from typing import List, Tuple


def calculate_probabilities(
    num_total: float,
    num_deposits: float,
    num_binary: List[float],
    num_binary_deposits: List[float],
) -> Tuple[List[float], List[float], List[float], List[float]]:
    """
    Calculate various probabilities needed for WofE calculations.

    Parameters
    ----------
    num_total : float
        Total number of voxels
    num_deposits : float
        Number of known mineralization-bearing voxels
    num_binary : List[float]
        Number of anomalous voxels in evidential models
    num_binary_deposits : List[float]
        Number of intersected mineralization-bearing voxels and anomalous voxels

    Returns
    -------
    Tuple[List[float], List[float], List[float], List[float]]
        ProBD, ProBD_abs, ProB_absD, ProB_absD_abs
    """
    # Probability of deposit given binary pattern
    prob_bd = [n / num_deposits for n in num_binary_deposits]

    # Probability of deposit absent given binary pattern
    prob_bd_abs = [
        (n - num_binary_deposits[i]) / (num_total - num_deposits)
        for i, n in enumerate(num_binary)
    ]

    # Probability of binary pattern absent given deposit
    prob_b_abs_d = [(num_deposits - n) / num_deposits for n in num_binary_deposits]

    # Probability of binary pattern absent given deposit absent
    prob_b_abs_d_abs = [
        (num_total - n - num_deposits + num_binary_deposits[i]) / (num_total - num_deposits)
        for i, n in enumerate(num_binary)
    ]

    return prob_bd, prob_bd_abs, prob_b_abs_d, prob_b_abs_d_abs


def calculate_weights(
    prob_bd: List[float],
    prob_bd_abs: List[float],
    prob_b_abs_d: List[float],
    prob_b_abs_d_abs: List[float],
) -> Tuple[List[float], List[float]]:
    """
    Calculate positive and negative weights.

    Parameters
    ----------
    prob_bd : List[float]
        Probability of deposit given binary pattern
    prob_bd_abs : List[float]
        Probability of deposit absent given binary pattern
    prob_b_abs_d : List[float]
        Probability of binary pattern absent given deposit
    prob_b_abs_d_abs : List[float]
        Probability of binary pattern absent given deposit absent

    Returns
    -------
    Tuple[List[float], List[float]]
        w_pos (positive weights), w_neg (negative weights)
    """
    # Likelihood ratio for positive weights
    ls = [p / prob_bd_abs[i] for i, p in enumerate(prob_bd)]
    w_pos = [math.log(i) for i in ls]

    # Likelihood ratio for negative weights
    ln = [p / prob_b_abs_d_abs[i] for i, p in enumerate(prob_b_abs_d)]
    w_neg = [math.log(i) for i in ln]

    return w_pos, w_neg


def calculate_prior(num_deposits: float, num_total: float) -> Tuple[float, float, float]:
    """
    Calculate prior probability, odds, and logit.

    Parameters
    ----------
    num_deposits : float
        Number of known mineralization-bearing voxels
    num_total : float
        Total number of voxels

    Returns
    -------
    Tuple[float, float, float]
        prior_p (probability), prior_o (odds), prior_l (logit)
    """
    prior_p = num_deposits / num_total
    prior_o = prior_p / (1 - prior_p)
    prior_l = math.log(prior_o)
    return prior_p, prior_o, prior_l


def calculate_posterior_probability(posterior_odds: float) -> float:
    """
    Calculate posterior probability from posterior odds.

    Parameters
    ----------
    posterior_odds : float
        Posterior odds value

    Returns
    -------
    float
        Posterior probability
    """
    return posterior_odds / (1 + posterior_odds)


def calculate_posterior_logit(prior_l: float, weights: List[float]) -> float:
    """
    Calculate posterior logit from prior logit and weights.

    Parameters
    ----------
    prior_l : float
        Prior logit
    weights : List[float]
        List of weights to combine

    Returns
    -------
    float
        Posterior logit
    """
    return prior_l + sum(weights)


def calculate_posterior_odds(posterior_logit: float) -> float:
    """
    Calculate posterior odds from posterior logit.

    Parameters
    ----------
    posterior_logit : float
        Posterior logit value

    Returns
    -------
    float
        Posterior odds
    """
    return math.exp(posterior_logit)
