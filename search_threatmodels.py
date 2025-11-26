#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Search threatmodel profiles for a given query string.\n"
            "Uses app.py --list-profiles and app.py --profile <name> under the hood."
        )
    )
    parser.add_argument(
        "query",
        help="Text to search for in the generated threatmodels.",
    )
    parser.add_argument(
    "--show-profiles",
    action="store_true",
    help="Print discovered profile names before searching.",
)

# after building `all_profiles`
if args.show_profiles:
    print("Profiles:", ", ".join(all_profiles))

    parser.add_argument(
        "--app-path",
        type=str,
        default="app.py",
        help="Path to app.py (default: ./app.py).",
    )
    parser.add_argument(
        "--profile",
        "-p",
        action="append",
        help=(
            "Limit search to one or more specific profiles. "
            "Can be given multiple times. If omitted, all profiles are searched."
        ),
    )
    parser.add_argument(
        "--section",
        "-s",
        type=str,
        help=(
            "Limit search to a specific section (e.g. overview, assets, adversaries, "
            "attack-surfaces, mitigations). If omitted, the full threatmodel is searched."
        ),
    )
    parser.add_argument(
        "--ignore-case",
        "-i",
        action="store_true",
        help="Case-insensitive search.",
    )
    parser.add_argument(
        "--show-context",
        action="store_true",
        help="Print the full threatmodel/section instead of matching lines only.",
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
            print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)

    lines = [l.strip() for l in result.stdout.splitlines()]
    profiles = [l for l in lines if l and not l.startswith("#")]
    return profiles


def run_profile(
    app_path: Path,
    profile: str,
    section: Optional[str] = None,
) -> str:
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
        raise RuntimeError(
            f"`app.py --profile {profile}` failed with code {result.returncode}.\n"
            f"stderr:\n{result.stderr}"
        )
    return result.stdout


def search_text(
    text: str,
    query: str,
    ignore_case: bool,
) -> List[str]:
    matches: List[str] = []
    if ignore_case:
        q = query.lower()
        for line in text.splitlines():
            if q in line.lower():
                matches.append(line)
    else:
        for line in text.splitlines():
            if query in line:
                matches.append(line)
    return matches


def main() -> None:
    args = parse_args()
    app_path = Path(args.app_path)

    try:
        all_profiles = run_list_profiles(app_path)
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001
        print(f"ERROR listing profiles: {e}", file=sys.stderr)
        sys.exit(1)

    if not all_profiles:
        print("No profiles found; nothing to search.", file=sys.stderr)
        sys.exit(1)

    if args.profile:
        selected = []
        requested = set(args.profile)
        for p in all_profiles:
            if p in requested:
                selected.append(p)
        missing = requested.difference(all_profiles)
        if missing:
            print(
                f"WARNING: unknown profiles requested: {', '.join(sorted(missing))}",
                file=sys.stderr,
            )
        profiles = selected
    else:
        profiles = all_profiles

    if not profiles:
        print("No matching profiles to search after filtering.", file=sys.stderr)
        sys.exit(1)

    query = args.query
    found_any = False

    for profile in profiles:
        try:
            text = run_profile(app_path, profile, section=args.section)
        except Exception as e:  # noqa: BLE001
            print(f"ERROR running profile '{profile}': {e}", file=sys.stderr)
            continue

        matches = search_text(text, query, ignore_case=args.ignore_case)
        if not matches:
            continue

        found_any = True
        header = f"=== Profile: {profile}"
        if args.section:
            header += f" | Section: {args.section}"
        header += " ==="
        print(header)

        if args.show_context:
            # Print full text if any matches are present
            print(text.rstrip("\n"))
        else:
            for line in matches:
                print(f"  {line}")
        print()  # blank line between profiles

    if not found_any:
        print(
            f"No matches for '{query}' in the selected profiles.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
