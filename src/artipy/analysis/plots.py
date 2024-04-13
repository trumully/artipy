from decimal import Decimal

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from artipy.artifacts import Artifact
from artipy.stats import STAT_NAMES

from .analyse import (
    RollMagnitude,
    calculate_artifact_crit_value,
    calculate_artifact_roll_value,
    calculate_substat_roll_magnitudes,
    calculate_substat_rolls,
)
from .simulate import create_multiple_random_artifacts, upgrade_artifact_to_max

ROUND_TO = Decimal("1E-2")


def plot_artifact_substat_rolls(artifact: Artifact) -> None:
    substat_rolls = {
        STAT_NAMES[substat.name]: calculate_substat_rolls(substat)
        for substat in artifact.get_substats()
    }
    df = pd.DataFrame(substat_rolls.items(), columns=["stat", "rolls"])
    pie_figure = px.pie(df, values="rolls", names="stat")

    magnitudes_flat = [
        tuple(i.value for i in calculate_substat_roll_magnitudes(substat))
        for substat in artifact.get_substats()
    ]
    magnitudes_to_dict = {
        STAT_NAMES[substat.name]: {
            i.value: magnitudes_flat[idx].count(i.value) for i in RollMagnitude
        }
        for idx, substat in enumerate(artifact.get_substats())
    }
    magnitudes_to_long_form = [
        {"stat_name": stat_name, "magnitude": magnitude, "count": count}
        for stat_name, magnitudes in magnitudes_to_dict.items()
        for magnitude, count in magnitudes.items()
    ]
    df_long = pd.DataFrame(magnitudes_to_long_form)
    bar_traces = []
    for stat_name in df_long["stat_name"].unique():
        df_filtered = df_long[df_long["stat_name"] == stat_name]
        bar_traces.append(
            go.Bar(
                x=df_filtered["magnitude"],
                y=df_filtered["count"],
                name=stat_name,
                text=df_filtered["count"],
                textposition="auto",
            )
        )

    fig = make_subplots(
        rows=1,
        cols=len(bar_traces) + 1,
        specs=[[{"type": "pie"}] + [{"type": "bar"}] * len(bar_traces)],
        column_widths=[0.4] + [0.6 / len(bar_traces)] * len(bar_traces),
        subplot_titles=[
            f"Substat rolls on Artifact with {sum(substat_rolls.values())} total rolls",
            *(
                f"{stat} ({substat_rolls[STAT_NAMES[stat.name]]} rolls)"
                for stat in artifact.get_substats()
            ),
        ],
    )

    fig.add_trace(pie_figure.data[0], row=1, col=1)
    for i, trace in enumerate(bar_traces, start=2):
        fig.add_trace(trace, row=1, col=i)

    fig.update_layout(showlegend=False)

    fig.show()


def plot_crit_value_distribution(iterations: int = 1_000) -> None:
    for a in (artifacts := create_multiple_random_artifacts(iterations)):
        upgrade_artifact_to_max(a)

    crit_values = [
        calculate_artifact_crit_value(a).quantize(ROUND_TO) for a in artifacts
    ]
    df = pd.DataFrame(crit_values, columns=["crit_value"])

    bins = [0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0]
    labels = [f"{bins[i]}-{bins[i+1]}" for i in range(len(bins) - 1)]
    df["crit_value_range"] = pd.cut(df["crit_value"], bins=bins, labels=labels)

    fig = px.histogram(
        df,
        x="crit_value",
        color="crit_value_range",
        title=f"Crit Rate Distribution of {iterations:,} Artifacts",
    )

    fig.show()


def plot_roll_value_distribution(iterations: int = 1_000) -> None:
    for a in (artifacts := create_multiple_random_artifacts(iterations)):
        upgrade_artifact_to_max(a)
    roll_values = [calculate_artifact_roll_value(a) for a in artifacts]
    df = pd.DataFrame(roll_values, columns=["roll_value"])
    fig = px.histogram(
        df, x="roll_value", title=f"Roll Value Distribution of {iterations:,} Artifacts"
    )
    fig.show()
