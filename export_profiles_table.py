"""Export web3_threatmodel_cli profiles to a Markdown table.

Runs `app.py --list-profiles`, parses the output, and writes a simple
Markdown table with one row per profile.
"""
#!/usr/bin/env python3

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List

EXIT_OK = 0
EXIT_APP_NOT_FOUND = 1
EXIT_LIST_PROFILES_FAILED = 2
EXIT_NO_PROFILES = 3
EXIT_WRITE_FAILED = 4

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the profile export tool."""
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
   # in run_list_profiles
        print(f"ERROR: app.py not found at {app_path}", file=sys.stderr)
        sys.exit(EXIT_APP_NOT_FOUND)

        cmd = [sys.executable, str(app_path), "--list-profiles"]
    print(f"Running command: {' '.join(cmd)}", file=sys.stderr)


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

      lines = [line.strip() for line in result.stdout.splitlines()]
    profiles = [line for line in lines if line and not line.startswith("#")]
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
    """Parse arguments, obtain profiles, and write the Markdown table."""
    args = parse_args()
    app_path = Path(args.app_path)

    profiles = run_list_profiles(app_path)
    if not profiles:
        print("No profiles found in `app.py --list-profiles` output.", file=sys.stderr)
        sys.exit(EXIT_NO_PROFILES)

    markdown = make_markdown_table(profiles)
    write_output(markdown, args.output)


if __name__ == "__main__":
    main()
