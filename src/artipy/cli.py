import argparse
import random

from artipy.analysis.simulate import create_random_artifact
from artipy.artifacts import ArtifactBuilder
from artipy.types import STAT_NAMES, ArtifactSlot, StatType

INVERTED_STAT_NAMES: dict[str, StatType] = {
    str(v).lower(): k for k, v in STAT_NAMES.items()
}


def create_artifact(args: argparse.Namespace) -> None:
    """Create an artifact based on the passed arguments.

    Args:
        args (argparse.Namespace): The arguments passed into the command line
    """
    if args.random:
        a_slot: ArtifactSlot = ArtifactSlot(random.choice(list(ArtifactSlot)))
        artifact = create_random_artifact(a_slot, args.rarity)
        print(artifact)
    else:
        artifact = (
            ArtifactBuilder()
            .with_level(args.level)
            .with_rarity(args.rarity)
            .with_mainstat(INVERTED_STAT_NAMES[args.mainstat.lower()])
            .with_substats(amount=max(0, args.rarity - 1))
            .with_slot(args.slot)
            .build()
        )
        print(artifact)


def main() -> None:
    """The main function for the artipy CLI."""
    parser = argparse.ArgumentParser(prog="artipy", description="Create an artifact.")
    subparsers = parser.add_subparsers()

    create_parser = subparsers.add_parser("create", help="Create an artifact.")
    create_parser.add_argument(
        "-l", "--level", type=int, default=0, help="The level of the artifact."
    )
    create_parser.add_argument(
        "-r", "--rarity", type=int, default=5, help="The rarity of the artifact."
    )
    create_parser.add_argument(
        "-m",
        "--mainstat",
        type=str,
        default="hp",
        help="The mainstat of the artifact.",
    )
    create_parser.add_argument(
        "-s",
        "--slot",
        type=str,
        default=ArtifactSlot.FLOWER,
        help="The slot of the artifact.",
    )
    create_parser.add_argument(
        "--random",
        action="store_true",
        help="Generate a random artifact.",
    )

    create_parser.set_defaults(func=create_artifact)

    args = parser.parse_args()
    args.func(args) if "func" in args else parser.print_help()


if __name__ == "__main__":
    main()
