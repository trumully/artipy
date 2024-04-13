import random
from typing import Any


def choose(population: tuple[Any], weights: tuple[float | int]) -> Any:
    """Shortcut function for random.choices to choose an individual item from a
    population based on weights.

    :param population: The population to choose from.
    :type population: tuple[Any]
    :param weights: The weights of the population.
    :type weights: tuple[float  |  int]
    :return: The chosen item.
    :rtype: Any
    """
    return random.choices(population, weights)[0]
