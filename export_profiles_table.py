#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path
from typing import List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export web3_threatmodel_cli profiles as a Markdown table."
    )
    parser.add_argument(
        "--app-path",
        type=str,
        default="app.py",
        help="Path to app.py (default: ./app.py).",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="-",
        help="Output file path, or '-' for stdout (default: '-').",
    )
    return parser.parse_args()


def run_list_profiles(app_path: Path) -> List[str]:
    if not app_path.is_file():
        print(f"ERROR: app.py not found at {app_path}", file=sys.stderr)
        sys.exit(1)

    cmd = [sys.executable, str(app_path), "--list-profiles"]

    result = subprocess.run(
        cmd,
        text=True,
        capture_output=True,
        check=False,
    )

    if result.returncode != 0:
        print("ERROR: `app.py --list-profiles` failed.", file=sys.stderr)
        if result.stderr:
            print("stderr:", result.stderr, file=sys.stderr)
        sys.exit(result.returncode)

    lines = [l.strip() for l in result.stdout.splitlines()]
    # Filter out empty / separator lines
    profiles = [l for l in lines if l and not l.startswith("#")]
    return profiles


def make_markdown_table(profiles: List[str]) -> str:
    """
    Very simple Markdown table:

    | Profile | Description |
    | ------- | ----------- |
    | aztec   | aztec       |
    | zama    | zama        |

    You can later edit the Description column manually.
    """
    lines = []
    lines.append("| Profile | Description |")
    lines.append("| ------- | ----------- |")

    for p in profiles:
        # You can customize this: right now Description == name
        lines.append(f"| `{p}` | `{p}` |")

    return "\n".join(lines) + "\n"


def write_output(text: str, output: str) -> None:
    if output == "-" or output == "":
        sys.stdout.write(text)
        if not text.endswith("\n"):
            sys.stdout.write("\n")
        return

    path = Path(output)
    try:
        path.write_text(text, encoding="utf-8")
    except OSError as e:
        print(f"ERROR: failed to write output file {path}: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    args = parse_args()
    app_path = Path(args.app_path)
 debug(f"Current working directory: {Path.cwd()}")
    profiles = run_list_profiles(app_path)
    if not profiles:
        print("No profiles found in `app.py --list-profiles` output.", file=sys.stderr)
        sys.exit(1)

    markdown = make_markdown_table(profiles)
    write_output(markdown, args.output)


if __name__ == "__main__":
    main()
