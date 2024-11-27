"""This module contains functions to simulate artifacts."""
# No typestubs for plotly.
# pyright: reportMissingTypeStubs=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false

import itertools
import math
import random
from collections.abc import Callable, Mapping
from decimal import Decimal
from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from artipy import UPGRADE_STEP
from artipy.artifacts import Artifact, ArtifactBuilder
from artipy.stats import SubStat
from artipy.types import STAT_NAMES, VALID_MAINSTATS, ArtifactSlot, RollMagnitude, StatType
from artipy.utils import choose, possible_substat_values

ROUND_TO = Decimal("1E-2")

type SubstatMethod[R] = Callable[[SubStat], R]
type ArtifactMethod[R] = Callable[[Artifact], R]


def create_random_artifact(slot: ArtifactSlot, rarity: int = 5) -> Artifact:
    """Create a random artifact.

    Args:
        slot (artipy.types.ArtifactSlot): The slot of the artifact.
        rarity (int, optional): The rarity of the artifact. Defaults to 5.

    Returns:
        artipy.artifacts.Artifact: The random artifact.
    """

    max_substats = rarity - 1
    substat_count = max(0, max_substats if random.random() < 0.2 else max_substats - 1)  # noqa: PLR2004
    mainstats, mainstat_weights = zip(*VALID_MAINSTATS[slot].items(), strict=False)
    return (
        ArtifactBuilder()
        .with_mainstat(choose(mainstats, mainstat_weights))
        .with_rarity(rarity)
        .with_substats(amount=substat_count)
        .with_slot(slot)
        .build()
    )


def upgrade_artifact_to_max(artifact: Artifact) -> Artifact:
    """Upgrade an artifact to its maximum level.

    Args:
        artifact (artipy.artifacts.Artifact): The artifact to upgrade.

    Returns:
        artipy.artifacts.Artifact: The upgraded artifact.
    """
    while artifact.level < artifact.rarity * 4:
        artifact.upgrade()
    return artifact


def create_multiple_random_artifacts(amount: int = 1) -> list[Artifact]:
    """Create multiple random artifacts.

    Args:
        amount (int, optional): The amount of artifacts to generate. Defaults to 1.

    Returns:
        list[artipy.artifacts.Artifact]: The list of random artifacts.
    """
    result: list[Artifact] = []
    for _ in range(amount):
        slot: ArtifactSlot = ArtifactSlot(random.choice(list(ArtifactSlot)))
        result.append(create_random_artifact(slot))
    return result


ROLL_MULTIPLIERS: dict[int, tuple[float, ...]] = {
    1: (0.8, 1.0),
    2: (0.7, 0.85, 1.0),
    3: (0.7, 0.8, 0.9, 1.0),
    4: (0.7, 0.8, 0.9, 1.0),
    5: (0.7, 0.8, 0.9, 1.0),
}


def calculate_substat_roll_value(substat: SubStat) -> Decimal:
    """Calculate the substat roll value. This is the value of the substat divided by the
    highest possible value of the substat.

    Args:
        substat (artipy.stats.SubStat): The substat to calculate the roll value for.

    Returns:
        Decimal: The roll value of the substat.
    """
    stat_value = substat.value
    highest_value = max(possible_substat_values(substat.name, substat.rarity))

    if substat.name.is_pct:
        stat_value *= 100
        highest_value *= 100

    return stat_value / highest_value


def calculate_substat_rolls(substat: SubStat) -> int:
    """Calculate the number of rolls of a substat. This is the difference between the
    actual roll value and the average roll value divided by the average roll value.

    Args:
        substat (artipy.stats.SubStat): The substat to calculate the rolls for.

    Returns:
        int: The number of rolls of the substat.
    """
    possible_rolls = possible_substat_values(substat.name, substat.rarity)
    average_roll = Decimal(sum(possible_rolls) / len(possible_rolls))
    return math.ceil((substat.value - average_roll) / average_roll)


def calculate_substat_roll_magnitudes(substat: SubStat) -> tuple[RollMagnitude, ...]:
    """Calculate the roll magnitudes of a substat. This is the closest roll magnitude
    to the actual roll value for each roll.

    Args:
        substat (artipy.stats.SubStat): The substat to calculate the roll magnitudes
                                        for.

    Returns:
        tuple[RollMagnitude, ...]: The roll magnitudes of the substat.
    """

    def get_magnitude(
        values: tuple[Decimal, ...],
        value_to_index: Decimal,
    ) -> RollMagnitude:
        index = values.index(value_to_index)
        return RollMagnitude.closest(ROLL_MULTIPLIERS[substat.rarity][index])

    possible_rolls = possible_substat_values(substat.name, substat.rarity)
    rolls_actual = calculate_substat_rolls(substat)

    combinations = list(
        itertools.combinations_with_replacement(possible_rolls, rolls_actual),
    )
    combination = min(combinations, key=lambda x: abs(sum(x) - substat.value))
    return tuple(get_magnitude(possible_rolls, value) for value in combination)


def calculate_artifact_roll_value(artifact: Artifact) -> Decimal:
    """Calculate the roll value of an artifact. This is the sum of the roll values of
    all substats.

    Args:
        artifact (artipy.artifacts.Artifact): The artifact to calculate the roll value

    Returns:
        Decimal: The roll value of the artifact.
    """
    return Decimal(
        sum(calculate_substat_roll_value(substat) for substat in artifact.substats),
    )


def calculate_artifact_maximum_roll_value(artifact: Artifact) -> Decimal:
    """Calculate the maximum roll value of an artifact. This is the roll value of the
    artifact with all remaining rolls being maximum rolls.

    Args:
        artifact (artipy.artifacts.Artifact): The artifact to calculate the maximum

    Returns:
        Decimal: The maximum roll value of the artifact.
    """
    artifact_max_level = artifact.rarity * 4
    remaining_rolls = (artifact_max_level - artifact.level) // UPGRADE_STEP
    return Decimal(calculate_artifact_roll_value(artifact) + remaining_rolls)


def calculate_artifact_crit_value(artifact: Artifact) -> Decimal:
    """Calculate the crit value of an artifact. This is the sum of the crit damage and
    the crit rate times two.

    Args:
        artifact (artipy.artifacts.Artifact): The artifact to calculate the crit value

    Returns:
        Decimal: The crit value of the artifact.
    """
    crit_dmg = sum(substat.value for substat in artifact.substats if substat.name == StatType.CRIT_DMG) * 100
    crit_rate = sum(substat.value for substat in artifact.substats if substat.name == StatType.CRIT_RATE) * 100
    return Decimal(crit_dmg + crit_rate * 2)


ARTIFACT_ATTRIBUTES: Mapping[str, ArtifactMethod[Decimal]] = {
    "roll_value": calculate_artifact_roll_value,
    "crit_value": calculate_artifact_crit_value,
}

SUBSTAT_ATTRIBUTES: Mapping[str, SubstatMethod[int]] = {
    "rolls": calculate_substat_rolls,
}


def plot_artifact_substat_rolls(artifact: Artifact) -> None:
    """Plot the substat rolls of an artifact.

    Args:
        artifact (artipy.artifacts.Artifact): The artifact to plot the substat rolls for.
    """
    substat_rolls = {STAT_NAMES[substat.name]: calculate_substat_rolls(substat) for substat in artifact.substats}
    stat_rolls_df = pd.DataFrame(substat_rolls.items(), columns=["stat", "rolls"])

    colors = px.colors.qualitative.Plotly

    pie_figure = px.pie(
        stat_rolls_df,
        values="rolls",
        names="stat",
        color_discrete_sequence=colors,
    )

    magnitudes_flat = [
        tuple(i.value for i in calculate_substat_roll_magnitudes(substat)) for substat in artifact.substats
    ]
    magnitudes_to_dict = {
        STAT_NAMES[substat.name]: {i.value: magnitudes_flat[idx].count(i.value) for i in RollMagnitude}
        for idx, substat in enumerate(artifact.substats)
    }
    magnitudes_to_long_form = [
        {"stat_name": stat_name, "magnitude": magnitude, "count": count}
        for stat_name, magnitudes in magnitudes_to_dict.items()
        for magnitude, count in magnitudes.items()
    ]
    df_long = pd.DataFrame(magnitudes_to_long_form)
    bar_traces = []
    for idx, stat_name in enumerate(df_long["stat_name"].unique()):
        df_filtered = df_long[df_long["stat_name"] == stat_name]
        bar_traces.append(
            go.Bar(
                x=df_filtered["magnitude"],
                y=df_filtered["count"],
                name=stat_name,
                text=df_filtered["count"],
                textposition="auto",
                marker_color=colors[idx % len(colors)],
            ),
        )

    fig = make_subplots(
        rows=1,
        cols=len(bar_traces) + 1,
        specs=[[{"type": "pie"}] + [{"type": "bar"}] * len(bar_traces)],
        column_widths=[0.4] + [0.6 / len(bar_traces)] * len(bar_traces),
        subplot_titles=[
            f"Substat rolls on Artifact with {sum(substat_rolls.values())} total rolls",
            *(f"{stat} ({substat_rolls[STAT_NAMES[stat.name]]} rolls)" for stat in artifact.substats),
        ],
    )

    fig.add_trace(pie_figure.data[0], row=1, col=1)
    for i, trace in enumerate(bar_traces, start=2):
        fig.add_trace(trace, row=1, col=i)

    fig.update_layout(showlegend=False)

    fig.show()


def plot_crit_value_distribution(iterations: int = 1000) -> None:
    """Plot the crit value distribution of artifacts.

    Args:
        iterations (int, optional): The artifacts to generate. Defaults to 1000.
    """
    for a in (artifacts := create_multiple_random_artifacts(iterations)):
        upgrade_artifact_to_max(a)

    crit_values = [calculate_artifact_crit_value(a).quantize(ROUND_TO) for a in artifacts]
    crit_value_df = pd.DataFrame(crit_values, columns=["crit_value"])

    bins = [0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0]
    labels = [f"{bins[i]}-{bins[i + 1]}" for i in range(len(bins) - 1)]
    crit_value_df["crit_value_range"] = pd.cut(crit_value_df["crit_value"], bins=bins, labels=labels)

    fig = px.histogram(
        crit_value_df,
        x="crit_value",
        color="crit_value_range",
        title=f"Crit Rate Distribution of {iterations:,} Artifacts",
    )

    fig.show()


def plot_roll_value_distribution(iterations: int = 1000) -> None:
    """Plot the roll value distribution of artifacts.

    Args:
        iterations (int, optional): The number of artifacts. Defaults to 1000.
    """
    for a in (artifacts := create_multiple_random_artifacts(iterations)):
        upgrade_artifact_to_max(a)
    roll_values = [calculate_artifact_roll_value(a) for a in artifacts]
    roll_value_df = pd.DataFrame(roll_values, columns=["roll_value"])
    fig = px.histogram(
        roll_value_df,
        x="roll_value",
        title=f"Roll Value Distribution of {iterations:,} Artifacts",
    )
    fig.show()


def plot_expected_against_actual_mainstats(iterations: int = 1000) -> None:
    """Plot the expected mainstats against the actual mainstats of artifacts.

    Args:
        iterations (int, optional): The artifacts to generate. Defaults to 1000.
    """

    for a in (artifacts := create_multiple_random_artifacts(iterations)):
        upgrade_artifact_to_max(a)

    expected_mainstats: dict[ArtifactSlot, dict[StatType, float]] = {
        ArtifactSlot(k): v for k, v in VALID_MAINSTATS.items() if k not in (ArtifactSlot.FLOWER, ArtifactSlot.PLUME)
    }
    actual_mainstats: dict[ArtifactSlot, list[StatType]] = {k: [] for k in expected_mainstats}

    for a in artifacts:
        slot: ArtifactSlot = ArtifactSlot(str(a.artifact_slot))
        if slot in expected_mainstats and a.mainstat is not None:
            actual_mainstats[slot].append(a.mainstat.name)

    actual_mainstats_pct: dict[ArtifactSlot, dict[StatType, float]] = {
        k: {stat: (v.count(stat) / len(v)) * 100 for stat in v} for k, v in actual_mainstats.items()
    }

    fig = make_subplots(
        rows=1,
        cols=len(expected_mainstats),
        subplot_titles=list(expected_mainstats),
    )

    for i, slot in enumerate(expected_mainstats, start=1):
        col = (i - 1) % len(expected_mainstats) + 1
        fig.add_trace(
            go.Bar(
                x=list(expected_mainstats[slot]),
                y=list(expected_mainstats[slot].values()),
                name="Expected",
                marker={"color": "#FF6961"},
            ),
            row=1,
            col=col,
        )
        fig.add_trace(
            go.Bar(
                x=list(actual_mainstats_pct[slot]),
                y=list(actual_mainstats_pct[slot].values()),
                name="Actual",
                marker={"color": "#B4D8E7"},
            ),
            row=1,
            col=col,
        )

    fig.update_layout(barmode="overlay", showlegend=False)
    fig.show()


def plot_multi_value_distribution(
    iterations: int = 1000,
    *,
    attributes: tuple[str],
) -> None:
    """Plot a combined histogram of multiple attributes of artifacts.

    Args:
        attributes (tuple[str]): The attributes to plot.
        iterations (int, optional): The artifacts to generate. Defaults to 1000.

    Raises:
        ValueError: If an invalid attribute is passed.
    """
    all_attributes: Mapping[str, Callable[..., Any]] = {**ARTIFACT_ATTRIBUTES, **SUBSTAT_ATTRIBUTES}
    for attr in attributes:
        if attr not in all_attributes:
            msg = f"Invalid attribute: {attr}\nValid attributes: {all_attributes}"
            raise ValueError(msg)

    for a in (artifacts := create_multiple_random_artifacts(iterations)):
        upgrade_artifact_to_max(a)

    concatted_df = pd.DataFrame()
    for attr in attributes:
        values = [all_attributes[attr](a) for a in artifacts if all_attributes[attr](a) > 0]
        attr_df = pd.DataFrame(values, columns=[attr])
        concatted_df = pd.concat([concatted_df, attr_df])

    fig = px.histogram(
        concatted_df,
        x=concatted_df.columns,
        title=f"Value Distribution of {iterations:,} Artifacts",
    )

    fig.show()
