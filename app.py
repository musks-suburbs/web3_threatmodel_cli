#!/usr/bin/env python3
from typing import List, Dict

__version__ = "0.1.0"
@dataclass
class ThreatModel:
    key: str
    name: str
    overview: str
    assets: List[str] = field(default_factory=list)
    adversaries: List[str] = field(default_factory=list)
    attack_surfaces: List[str] = field(default_factory=list)
    mitigations: List[str] = field(default_factory=list)

PROFILE_KEYS = ["aztec", "zama", "soundness"]
SECTION_KEYS = ["overview", "assets", "adversaries", "attacks", "mitigations"]

def make_models() -> Dict[str, ThreatModel]:
      """Construct and return the built-in Web3 threat model profiles."""
    return {
        "aztec": ThreatModel(
            key="aztec",
            name="Aztec-style zk rollup",
            overview=(
                "A privacy-preserving Ethereum rollup using zero-knowledge proofs for "
                "confidential balances and private smart contracts."
            ),
            assets=[
                "Encrypted user balances and notes",
                "Viewing keys and decryption keys",
                "Proving and verification keys for zk circuits",
                "Layer 2 state roots and Merkle commitments",
                "Bridge contracts and rollup smart contracts on L1",
            ],
            adversaries=[
                "On-chain observers trying to deanonymize users",
                "Compromised sequencer attempting to censor or reorder transactions",
                "Malicious prover submitting invalid proofs",
                "Smart contract attackers exploiting rollup logic",
                "Insider threat leaking viewing keys or proving secrets",
            ],
            attack_surfaces=[
                "Bugs in zk circuits or constraint systems",
                "Incorrect implementation of cryptographic primitives",
                "Bridge contract vulnerabilities between L1 and L2",
                "Metadata leaks from transaction timing and fee patterns",
                "Trusted setup or key ceremony compromises, if applicable",
            ],
            mitigations=[
                "Independent audits of circuits, contracts, and cryptographic libraries",
                "Formal verification of core rollup and bridge logic where feasible",
                "Multi-party ceremonies or transparent setups for proving systems",
                "Fee and batching strategies to reduce metadata leakage",
                "Key management policies for proving keys and operational secrets",
            ],
        ),
        "zama": ThreatModel(
            key="zama",
            name="Zama-style FHE compute stack",
            overview=(
                "A system that performs computations directly on encrypted data using "
                "fully homomorphic encryption, often alongside Web3 components."
            ),
            assets=[
                "Long-term FHE secret keys and key shares",
                "Encrypted datasets stored in data lakes or logs",
                "Computation policies describing allowed FHE queries",
                "Metadata linking ciphertexts to users or organizations",
                "Partially decrypted results and post-processing pipelines",
            ],
            adversaries=[
                "Cloud operators with access to ciphertexts and compute nodes",
                "External attackers exfiltrating ciphertexts or key material",
                "Curious analysts attempting to infer data from encrypted outputs",
                "Application developers misconfiguring FHE parameters",
                "Colluding parties trying to reconstruct secret keys",
            ],
            attack_surfaces=[
                "Side channel leakage from FHE implementations",
                "Weak parameter choices leading to cryptanalytic attacks",
                "Decryption or key management endpoints",
                "Insecure storage of ciphertexts and backups",
                "Query pattern leakage and repeated computations on similar data",
            ],
            mitigations=[
                "Use hardened, well-reviewed FHE libraries with safe defaults",
                "Separate roles for key management and compute infrastructure",
                "Access control and logging for decryption operations",
                "Regular review of parameter choices against current research",
                "Rate limits and differential privacy techniques for result queries",
            ],
        ),
        "soundness": ThreatModel(
            key="soundness",
            name="Soundness-focused protocol lab",
            overview=(
                "A research and engineering environment where the main assets are "
                "protocol specifications, proofs of soundness, and reference implementations."
            ),
            assets=[
                "Formal specifications and protocol descriptions",
                "Soundness and security proofs, including mechanized proofs",
                "Reference implementations used as a basis for other systems",
                "Private design discussions and threat models",
                "Continuous integration and verification pipelines",
            ],
            adversaries=[
                "External attackers seeking to exploit specification oversights",
                "Well-resourced adversaries with access to alternative models",
                "Insiders bypassing review or verification processes",
                "Implementers cherry-picking parts of specs without proofs",
                "Attackers publishing misleading or incomplete analyses",
            ],
            attack_surfaces=[
                "Mismatch between formal models and real-world deployments",
                "Ambiguous specs that allow unsafe interpretations",
                "Gaps between reference code and production code",
                "Tooling issues in proof assistants or model checkers",
                "Insufficient review of assumptions and threat models over time",
            ],
            mitigations=[
                "Executable, unambiguous specifications aligned with implementations",
                "Independent review of proofs and modeling assumptions",
                "Conformance test suites derived from formal models",
                "Change management policies for specs and security claims",
                "Regular threat model updates tied to release cycles",
            ],
        ),
    }


def list_profiles(models: Dict[str, ThreatModel]) -> None:
    """Print the list of available profile keys and their human names."""
    print("Available profiles related to Web3 privacy and soundness:")
    for key in sorted(models.keys()):
        model = models[key]
        print(f"- {key}: {model.name}")
    print("")
    print("Use --profile with one of these keys to print a threat model.")


def section_title(section: str) -> str:
    mapping = {
        "overview": "Overview",
        "assets": "Assets to protect",
        "adversaries": "Adversaries",
        "attacks": "Attack surfaces",
        "mitigations": "Mitigations",
    }
    return mapping.get(section, section.capitalize())


def print_section(model: ThreatModel, section: str) -> None:
    print(section_title(section) + ":")
    print("")

    if section == "overview":
        print(model.overview)
        print("")
        return
    else:
        print(f"Unknown section: {section}")
        print("")
        return

    items: List[str]
    if section == "assets":
        items = model.assets
    elif section == "adversaries":
        items = model.adversaries
    elif section == "attacks":
        items = model.attack_surfaces
    elif section == "mitigations":
        items = model.mitigations
    else:
        print("Unknown section.")
        print("")
        return

    for i, item in enumerate(items, start=1):
        print(f"{i}. {item}")
    print("")


def print_full_model(model: ThreatModel) -> None:
    """Print all sections of a given ThreatModel in a human-readable format."""
    print(f"Threat model profile: {model.name}")
    print("")
    print_section(model, "overview")
    print_section(model, "assets")
    print_section(model, "adversaries")
    print_section(model, "attacks")
    print_section(model, "mitigations")
     print("Note:")
    print("This output is an educational starting point and does not replace a full security review.")
    print("")
    print("Always adapt and extend it for your specific protocol, chain, and deployment model.")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="web3_threatmodel_cli",
        description=(
            "Generate high level threat models for Web3 privacy projects inspired by "
            "ecosystems such as Aztec, Zama, and soundness-focused research labs."
        ),
    )
     parser.add_argument(
        "--profile",
        type=str,
        choices=PROFILE_KEYS,
        help="Select which profile to use (aztec, zama, soundness).",
    )
        parser.add_argument(
        "--version",
        action="store_true",
        help="Print version information and exit.",
    )

    parser.add_argument(
        "--section",
        type=str,
        choices=SECTION_KEYS,
        help="Print only a single section instead of the full threat model.",


    )
    parser.add_argument(
        "--list-profiles",
        action="store_true",
        help="List available profiles and exit.",
    )

    args = parser.parse_args()
    models = make_models()

    if args.list_profiles:
        list_profiles(models)
        return

    if not args.profile:
        print("web3_threatmodel_cli - Web3 privacy threat model helper")
        print("")
        list_profiles(models)
            print("Examples:")
        print("  python app.py --profile aztec")
        print("  python app.py --profile zama --section assets")
        print("  python app.py --profile soundness --section mitigations")
        print("  python app.py --profile soundness")
        return

    model = models[args.profile]
    if args.version:
        print(f"web3_threatmodel_cli version {__version__}")
        return

    if args.section:
        print(f"Threat model profile: {model.name}")
        print("")
        print_section(model, args.section)
        return

    print_full_model(model)


if __name__ == "__main__":
    main()
