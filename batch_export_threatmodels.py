#!/usr/bin/env python3

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export all threatmodel profiles to individual files."
    )
        parser.add_argument(
        "--no-code-block",
        action="store_true",
        help="Do not wrap the content in a ```text code block.",
    )

    parser.add_argument(
        "--app-path",
        type=str,
        default="app.py",
        help="Path to app.py (default: ./app.py).",
    )
    parser.add_argument(
        "--out-dir",
        type=str,
        default="exports",
        help="Directory to write files into (default: ./exports).",
    )
    parser.add_argument(
        "--format",
        choices=("md", "txt"),
        default="md",
        help="File format: md (Markdown) or txt (plain text). Default: md.",
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
    # simple filter: non-empty & not comments
    profiles = [l for l in lines if l and not l.startswith("#")]
    return profiles


def run_profile(app_path: Path, profile: str) -> str:
    cmd = [sys.executable, str(app_path), "--profile", profile]
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


def wrap_markdown(profile: str, body: str, heading_level: int = 1, use_code_block: bool = True) -> str:
    body = body.rstrip("\n")
    heading_prefix = "#" * max(1, min(6, heading_level))
    if use_code_block:
        return f"{heading_prefix} Threat model: `{profile}`\n\n```text\n{body}\n```\n"
    return f"{heading_prefix} Threat model: `{profile}`\n\n{body}\n"



def main() -> None:
    args = parse_args()
    app_path = Path(args.app_path)
    out_dir = Path(args.out_dir)

    profiles = run_list_profiles(app_path)
    if not profiles:
        print("No profiles found; nothing to export.", file=sys.stderr)
        sys.exit(1)
            content = wrap_markdown(
                profile,
                text,
                heading_level=args.heading_level,
                use_code_block=not args.no_code_block,
            )

    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Found profiles: {', '.join(profiles)}")
    print(f"Writing exports to: {out_dir.resolve()}")

    for profile in profiles:
        try:
            text = run_profile(app_path, profile)
        except Exception as e:  # noqa: BLE001
            print(f"ERROR exporting profile '{profile}': {e}", file=sys.stderr)
            continue

        if args.format == "md":
            content = wrap_markdown(profile, text)
            ext = ".md"
        else:
            content = text
            ext = ".txt"

        out_path = out_dir / f"{profile}{ext}"
        out_path.write_text(content, encoding="utf-8")
        print(f"  - wrote {out_path}")

    print("Done.")


if __name__ == "__main__":
    main()
