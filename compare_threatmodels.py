#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
import difflib
from pathlib import Path
from typing import Optional


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare two threatmodel profiles and show a unified diff.\n"
            "Uses `app.py --profile <name>` (and optionally `--section <name>`)."
        )
    )
    parser.add_argument(
        "profile_a",
        help="Name of the first profile to compare.",
    )
        parser.add_argument(
        "--no-header",
        action="store_true",
        help="Hide the first diff header lines (---/+++).",
    )

    parser.add_argument(
        "profile_b",
        help="Name of the second profile to compare.",
    )
    parser.add_argument(
        "--app-path",
        type=str,
        default="app.py",
        help="Path to app.py (default: ./app.py).",
    )
    parser.add_argument(
        "--section",
        "-s",
        type=str,
        help=(
            "Optional section to compare (e.g. overview, assets, adversaries, "
            "attack-surfaces, mitigations). If omitted, the full threatmodel is compared."
        ),
    )
    parser.add_argument(
        "--ignore-case",
        "-i",
        action="store_true",
        help="Case-insensitive comparison (lowercases both sides before diff).",
    )
    parser.add_argument(
        "--context-lines",
        "-C",
        type=int,
        default=3,
        help="Number of context lines for the unified diff (default: 3).",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable simple ANSI colors in the diff output.",
    )
    return parser.parse_args()


def run_profile(
    app_path: Path,
    profile: str,
    section: Optional[str] = None,
) -> str:
    if not app_path.is_file():
        print(f"ERROR: app.py not found at {app_path}", file=sys.stderr)
        sys.exit(1)

    cmd = [sys.executable, str(app_path), "--profile", profile]
    if section:
        cmd.extend(["--section", section])

    result = subprocess.run(
        cmd,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        print(
            f"ERROR: `app.py --profile {profile}` failed with code {result.returncode}.",
            file=sys.stderr,
        )
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)

    return result.stdout


def colorize(line: str, no_color: bool) -> str:
    """Very simple colorizer for diff output."""
    if no_color:
        return line

    RESET = "\033[0m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    CYAN = "\033[36m"
    for line in diff:
        if args.no_header and (line.startswith("---") or line.startswith("+++")):
            continue
        any_output = True
        print(colorize(line, args.no_color))

    if line.startswith("+") and not line.startswith("+++"):
        return f"{GREEN}{line}{RESET}"
    if line.startswith("-") and not line.startswith("---"):
        return f"{RED}{line}{RESET}"
    if line.startswith("@@"):
        return f"{CYAN}{line}{RESET}"
    return line


def main() -> None:
    args = parse_args()
    app_path = Path(args.app_path)

    section = args.section

    # Fetch both profiles
    text_a = run_profile(app_path, args.profile_a, section=section)
    text_b = run_profile(app_path, args.profile_b, section=section)

    if args.ignore_case:
        a_lines = [line.lower() for line in text_a.splitlines(keepends=False)]
        b_lines = [line.lower() for line in text_b.splitlines(keepends=False)]
    else:
        a_lines = text_a.splitlines(keepends=False)
        b_lines = text_b.splitlines(keepends=False)

    from_label = args.profile_a if not section else f"{args.profile_a} ({section})"
    to_label = args.profile_b if not section else f"{args.profile_b} ({section})"

    diff = difflib.unified_diff(
        a_lines,
        b_lines,
        fromfile=from_label,
        tofile=to_label,
        lineterm="",
        n=args.context_lines,
    )

    any_output = False
    for line in diff:
        any_output = True
        print(colorize(line, args.no_color))

    if not any_output:
        print("Profiles are identical (under the chosen options).")


if __name__ == "__main__":
    main()
