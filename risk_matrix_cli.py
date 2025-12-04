"""
risk_matrix_cli

A small CLI tool that prints qualitative risk matrices for Web3
privacy/soundness projects. Designed as a companion to web3_threatmodel_cli.
"""
import argparse
import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Any

__version__ = "0.1.0"
__all__ = [
    "RiskCell",
    "RiskProfile",
    "PROFILES",
    "parse_args",
    "print_human",
    "main",
]

@dataclass
class RiskCell:
    """A single qualitative risk entry in the risk matrix.

    Each cell captures an asset, the main threat, and its likelihood/impact.
    """
    asset: str
    threat: str
    likelihood: str  # low / medium / high
    impact: str      # low / medium / high
    notes: str


@dataclass
class RiskProfile:
    """A named risk profile consisting of a summary and a list of risk cells."""
    key: str
    name: str
    summary: str
    matrix: List[RiskCell]
JSONDict = Dict[str, Any]

VALID_LEVELS = {"low", "medium", "high"}


def validate_profile(profile: RiskProfile) -> None:
    for cell in profile.matrix:
        if cell.likelihood not in VALID_LEVELS:
            raise ValueError(f"Invalid likelihood {cell.likelihood!r} in profile {profile.key}")
        if cell.impact not in VALID_LEVELS:
            raise ValueError(f"Invalid impact {cell.impact!r} in profile {profile.key}")

PROFILES: Dict[str, RiskProfile] = {
    "aztec": RiskProfile(
        key="aztec",
        name="Aztec-style zk privacy rollup",
        summary=(
            "Privacy-preserving L2 with encrypted balances and zk circuits. "
            "Main worries are proof system soundness, DA failures, and key compromise."
        ),
        matrix=[
            RiskCell(
                asset="Encrypted balances and notes",
                threat="Compromised proving key or circuit bug",
                likelihood="medium",
                impact="high",
                notes="Can silently break confidentiality or enable inflation.",
            ),
            RiskCell(
                asset="L2 state commitment",
                threat="Data availability failure / withheld batches",
                likelihood="medium",
                impact="high",
                notes="Users may not be able to exit or prove ownership.",
            ),
            RiskCell(
                asset="Bridge contracts",
                threat="L1 <> L2 bridge logic bug",
                likelihood="low",
                impact="high",
                notes="Typical catastrophic failure: locked or stolen funds.",
            ),
            RiskCell(
                asset="Sequencer / coordinator",
                threat="Censorship or MEV abuse",
                likelihood="high",
                impact="medium",
                notes="Can degrade UX and fairness, even if safety is preserved.",
            ),
        ],
    ),
    "zama": RiskProfile(
        key="zama",
        name="Zama-style FHE + Web3 stack",
        summary=(
            "Encrypted compute over sensitive data with FHE and Web3 anchoring. "
            "Main worries are key management, performance-induced shortcuts, and side channels."
        ),
        matrix=[
            RiskCell(
                asset="FHE private keys",
                threat="Key exfiltration from compute cluster",
                likelihood="medium",
                impact="high",
                notes="Decryption of historical ciphertexts is usually game over.",
            ),
            RiskCell(
                asset="Encrypted data streams",
                threat="Traffic analysis and metadata leakage",
                likelihood="high",
                impact="medium",
                notes="Patterns may leak business-sensitive info even if content stays private.",
            ),
            RiskCell(
                asset="On-chain anchors / hashes",
                threat="Mismatched commitments between FHE world and chain",
                likelihood="low",
                impact="high",
                notes="Breaks auditability or can be abused to fake computations.",
            ),
            RiskCell(
                asset="Compute nodes",
                threat="Side-channel attacks on FHE runtimes",
                likelihood="medium",
                impact="medium",
                notes="Timing and cache patterns may leak partial information.",
            ),
        ],
    ),
    "soundness": RiskProfile(
        key="soundness",
        name="Soundness-first protocol lab",
        summary=(
            "Specification-driven, research-heavy protocol work. "
            "Main worries are spec/implementation drift and unsafe experimental deployments."
        ),
        matrix=[
            RiskCell(
                asset="Reference specification",
                threat="Implementation deviates from spec",
                likelihood="medium",
                impact="high",
                notes="Breaks assumptions used in proofs and reviews.",
            ),
            RiskCell(
                asset="Test deployments / devnets",
                threat="Experimental features exposed to real value",
                likelihood="medium",
                impact="medium",
                notes="Prototype code accidentally becomes security-critical.",
            ),
            RiskCell(
                asset="Proof artifacts",
                threat="Outdated proofs kept as authoritative",
                likelihood="high",
                impact="medium",
                notes="Teams may over-trust proofs that no longer match the system.",
            ),
            RiskCell(
                asset="Upgrade and governance path",
                threat="Rushed changes bypassing review process",
                likelihood="medium",
                impact="high",
                notes="Undermines the whole soundness-first culture.",
            ),
        ],
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="risk_matrix_cli",
        description=(
            "Print a small qualitative risk matrix for Web3 privacy/soundness projects. "
            "Designed as a companion to web3_threatmodel_cli."
        ),
    )
     parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show program's version number and exit.",
    )
    parser.add_argument(
        "--profile",
        choices=list(PROFILES.keys()),
        default="aztec",
        help="Which profile to use (aztec, zama, soundness). Default: aztec.",
    )
        parser.add_argument(
        "--list-profiles",
        action="store_true",
        help="List available profiles and exit.",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON instead of human-readable text.",
    )
    return parser.parse_args()
    
def _color_level(level: str) -> str:
    """Return a colorized level string for terminals that support ANSI."""
    mapping = {
        "low": "\033[32mLOW\033[0m",      # green
        "medium": "\033[33mMEDIUM\033[0m",  # yellow
        "high": "\033[31mHIGH\033[0m",    # red
    }
    return mapping.get(level.lower(), level)


def print_human(profile: RiskProfile) -> None:
    """Print a human-readable risk matrix for the given profile."""
    print("🔐 risk_matrix_cli")
    print(f"Profile : {profile.name} ({profile.key})")
    print("")
    print("Summary:")
    print(f"  {profile.summary}")
    print("")
    print("Risk matrix (likelihood x impact):")
    for idx, cell in enumerate(profile.matrix, start=1):
        print(f"{idx}. Asset      : {cell.asset}")
        print(f"   Threat     : {cell.threat}")
        print(f"   Likelihood : {_color_level(cell.likelihood)}")
        print(f"   Impact     : {_color_level(cell.impact)}")
        print(f"   Notes      : {cell.notes}")
        print("")


def main() -> None:
    args = parse_args()

    if args.list_profiles:
        print("Available profiles:")
        for key, profile in PROFILES.items():
            print(f"  {key:10s} - {profile.name}")
        return

    profile = PROFILES[args.profile]


    if args.json:
                payload: JSONDict = {
, Any] = {
            "profile": profile.key,
            "name": profile.name,
            "summary": profile.summary,
            "matrix": [asdict(cell) for cell in profile.matrix],
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print_human(profile)


if __name__ == "__main__":
    main()
