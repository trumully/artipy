"""This module contains functions to plot various statistics of artifacts."""
# No typestubs for plotly.
# pyright: reportMissingTypeStubs=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false

from collections.abc import Callable, Mapping
from decimal import Decimal
from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from artipy.artifacts import Artifact
from artipy.stats.substat import SubStat
from artipy.types import STAT_NAMES, VALID_MAINSTATS, ArtifactSlot, StatType

from .analyse import (
    RollMagnitude,
    calculate_artifact_crit_value,
    calculate_artifact_roll_value,
    calculate_substat_roll_magnitudes,
    calculate_substat_rolls,
)
from .simulate import create_multiple_random_artifacts, upgrade_artifact_to_max

ROUND_TO = Decimal("1E-2")

type SubstatMethod[R] = Callable[[SubStat], R]
type ArtifactMethod[R] = Callable[[Artifact], R]

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
        artifact (artipy.artifacts.Artifact): The artifact to plot the substat rolls
                                              for.
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
