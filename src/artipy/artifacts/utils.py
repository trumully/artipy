"""Utility functions for the artifacts module."""

import random

type Seq[T] = tuple[T, ...] | list[T]


def choose[T](population: Seq[T], weights: tuple[float]) -> T:
    """Helper function to choose a random element from a population with weights.
    This skips having to do slicing of the result of random.choices.

    Args:
        population (Seq[T]): The population to choose from.
        weights (tuple[float]): The weights of the population.

    Returns:
        T: The chosen element.
    """
    return random.choices(population, weights)[0]
