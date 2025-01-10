#!/usr/bin/env python3
"""Pre-commit hooks to check that sphinx docs build correctly."""

import argparse
import subprocess  # nosec
import sys
from collections.abc import Sequence
from typing import Literal


def requires_build(_filenames: Sequence[str], always_build: bool) -> bool:
    """Use filenames list to check if anything has changed in the documentation folder."""
    if not always_build:
        # Always return true for now (we rebuild with breathe/exhale so source code changes also require doc build)
        # In future allow rebuild e.g. only if files in the docs directory change
        pass

    return True


def build(builder: str, src_dir: str, output_dir: str, flags: list[str]) -> Literal[0, 1]:
    """Invoke ``sphinx-build`` to build the docs."""
    # Run Sphinx to build the documentation
    flags = [i.strip('"') for i in flags]
    command: list[str] = ["sphinx-build", *flags, "--builder", builder, src_dir, output_dir]
    output: subprocess.CompletedProcess = subprocess.run(command, check=False)  # nosec # noqa: S603
    ret: int = output.returncode

    # It's very weird that pre-commit marks this as 'PASSED' if I return an error code 512...! Workaround:
    return 0 if ret == 0 else 1


def main(argv: Sequence[str] | None = None) -> int:
    """Define the main routine."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--always-build",
        type=bool,
        default=True,
        help="Always rebuild, even if no doc files have changed (useful if using \
             breathe/exhale to extract docstrings from code)",
    )
    parser.add_argument(
        "--flags",
        nargs="*",
        default=['"-W"'],
        help="Arguments passed to sphinx-build",
    )
    parser.add_argument(
        "--builder",
        type=str,
        default="html",
        help="Builder to use to generate the documentation",
    )
    parser.add_argument(
        "--source-dir",
        type=str,
        default="docs",
        help="Directory containing documentation sources (where the conf.py file exists)",
    )
    parser.add_argument(
        "--output-dir",
        "--html-dir",
        type=str,
        default="docs/_build/html",
        help="Directory to output the documentation to",
    )
    parser.add_argument(
        "filenames",
        nargs="*",
        help="Filenames pre-commit believes are changed",
    )

    args: argparse.Namespace = parser.parse_args(argv)
    if requires_build(args.filenames, args.always_build):
        return build(args.builder, args.source_dir, args.output_dir, args.flags)

    return 0


if __name__ == "__main__":
    sys.exit(main())
