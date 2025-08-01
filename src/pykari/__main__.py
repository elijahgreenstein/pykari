"""Command line management."""

import argparse
from pathlib import Path

from .build import generate
from .setup import setup


def main() -> None:
    """Build or set up a Pykari static site."""
    parser = argparse.ArgumentParser(
        prog="Pykari",
        description="Build site from source (default action) or set up a new project.",
    )
    parser.add_argument(
        "--setup",
        metavar="DIRECTORY",
        required=False,
        nargs=1,
        help="set up new project in named directory",
    )
    args = parser.parse_args()
    if args.setup:
        setup(Path(args.setup[0]))
    else:
        generate()


if __name__ == "__main__":
    main()
