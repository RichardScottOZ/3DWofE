"""
Input/Output operations for 3DWofE data handling.

This module provides functions for reading and writing CSV data files used in
Weights of Evidence calculations.
"""

import csv
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import pandas as pd

logger = logging.getLogger(__name__)


def read_csv_data(
    filepath: str,
    has_header: bool = False,
) -> List[List[str]]:
    """
    Read data from a CSV file.

    Parameters
    ----------
    filepath : str
        Path to the CSV file
    has_header : bool, optional
        Whether the CSV has a header row, by default False

    Returns
    -------
    List[List[str]]
        List of rows, where each row is a list of values
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Input file not found: {filepath}")

    data = []
    with open(filepath, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        if has_header:
            next(reader)  # Skip header
        for row in reader:
            if row:  # Skip empty rows
                data.append(row)

    logger.info(f"Read {len(data)} rows from {filepath}")
    return data


def write_csv_data(
    filepath: str,
    data: List[List[Any]],
    header: Optional[List[str]] = None,
) -> None:
    """
    Write data to a CSV file.

    Parameters
    ----------
    filepath : str
        Path to the output CSV file
    data : List[List[Any]]
        List of rows to write
    header : Optional[List[str]], optional
        Header row to write, by default None
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if header:
            writer.writerow(header)
        writer.writerows(data)

    logger.info(f"Wrote {len(data)} rows to {filepath}")


def read_dataframe(
    filepath: str,
    column_names: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Read data from a CSV file into a pandas DataFrame.

    Parameters
    ----------
    filepath : str
        Path to the CSV file
    column_names : Optional[List[str]], optional
        Column names to use, by default None (will use file header or generate indices)

    Returns
    -------
    pd.DataFrame
        DataFrame containing the data
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Input file not found: {filepath}")

    if column_names:
        df = pd.read_csv(filepath, names=column_names, header=None)
    else:
        df = pd.read_csv(filepath)

    logger.info(f"Read DataFrame with shape {df.shape} from {filepath}")
    return df


def write_dataframe(
    filepath: str,
    df: pd.DataFrame,
    include_index: bool = False,
    include_header: bool = True,
) -> None:
    """
    Write a pandas DataFrame to a CSV file.

    Parameters
    ----------
    filepath : str
        Path to the output CSV file
    df : pd.DataFrame
        DataFrame to write
    include_index : bool, optional
        Whether to include the index, by default False
    include_header : bool, optional
        Whether to include the header, by default True
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(filepath, index=include_index, header=include_header)
    logger.info(f"Wrote DataFrame with shape {df.shape} to {filepath}")


def count_rows(filepath: str) -> int:
    """
    Count the number of rows in a CSV file.

    Parameters
    ----------
    filepath : str
        Path to the CSV file

    Returns
    -------
    int
        Number of rows in the file
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Input file not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as file:
        return sum(1 for _ in csv.reader(file))


def validate_input_file(
    filepath: str,
    min_columns: int = 4,
) -> bool:
    """
    Validate that an input file has the expected format.

    Parameters
    ----------
    filepath : str
        Path to the CSV file
    min_columns : int, optional
        Minimum number of columns expected, by default 4 (X, Y, Z, Grade)

    Returns
    -------
    bool
        True if valid, raises ValueError otherwise
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Input file not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        first_row = next(reader, None)

        if first_row is None:
            raise ValueError(f"File is empty: {filepath}")

        if len(first_row) < min_columns:
            raise ValueError(
                f"File has {len(first_row)} columns, expected at least {min_columns}"
            )

    return True
