"""Utility functions for the artifacts module."""

import random
from typing import Any


def choose(population: tuple[Any], weights: tuple[float | int]) -> Any:
    """Helper function to choose a random element from a population with weights.
    This skips having to do slicing of the result of random.choices.

    Args:
        population (tuple[Any]): The population to choose from.
        weights (tuple[float  |  int]): The weights of the population.

    Returns:
        Any: The chosen element.
    """
    return random.choices(population, weights)[0]
