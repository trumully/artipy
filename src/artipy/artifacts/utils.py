import random
from typing import Any


def choose(population: tuple[Any], weights: list[float | int]) -> Any:
    """Choose a random element from a population with given weights."""
    return random.choices(population, weights)[0]
