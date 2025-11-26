# web3_threatmodel_cli

This repository contains a tiny command line tool that prints ready to use threat model outlines for Web3 privacy projects. Profiles are loosely inspired by ecosystems such as Aztec style zero knowledge rollups, Zama style fully homomorphic encryption stacks, and soundness oriented protocol labs.

The repository consists of exactly two files:
- app.py
- README.md


## Purpose

The goal of this tool is to give you a structured starting point when documenting risks and assumptions for a Web3 project that touches privacy, cryptography, or formal soundness.

Rather than connecting to a node or blockchain network, the script focuses entirely on text based threat model sections:
- high level overview
- assets to protect
- adversaries
- attack surfaces
- mitigations

You can generate a full threat model or a single section for quick copy and paste into documents, wikis, or issue trackers.


## Profiles

The tool currently provides three profiles.

aztec
A profile for a privacy preserving rollup using zero knowledge proofs and encrypted balances.

zama
A profile for a system using fully homomorphic encryption on sensitive data in conjunction with Web3 components.

soundness
A profile for a research or engineering lab that focuses on formal specifications, soundness proofs, and reference protocols.

Each profile has its own view on assets, attackers, and mitigations, reflecting the different risks posed by zk rollups, FHE based computation, and proof focused environments.


## Installation

Requirements:
- Python 3.10 or newer
- A command line environment such as bash, zsh, or PowerShell

Steps:
1. Create a new GitHub repository with any name.
2. Place app.py and this README.md into the root of the repository.
3. Ensure that the python executable is available on your system PATH.
4. No external Python packages are required. The script uses only the standard library.


## Usage

All commands below assume you are in the root directory of the repository.

List available profiles:
python app.py --list-profiles

Print the full threat model for an Aztec inspired zk rollup:
python app.py --profile aztec

Print only the list of assets for a Zama inspired FHE stack:
python app.py --profile zama --section assets

Print only the mitigations section for a soundness focused protocol lab:
python app.py --profile soundness --section mitigations


## Output

The script prints plain text describing the selected profile. For a full threat model you will see:

- a profile name line
- a short overview paragraph
- a numbered list of assets
- a numbered list of adversaries
- a numbered list of attack surfaces
- a numbered list of mitigations
- a short note reminding you that the content is an educational starting point

When you request a single section with the section flag, only that part is printed so you can integrate it into an existing document.


## Notes

- The provided content is intentionally generic and simplified.
- Threat models need to be adapted to the exact protocol design, infrastructure, and deployment details of your system.
- For real systems, always combine these outlines with protocol specifications, implementation reviews, audits, and peer discussion.
- You are encouraged to fork the repository and tune the profiles or add new ones for your own Web3 projects.
## Tooling

- `scripts/search_threatmodels.py` – text search in generated threatmodels
- `batch_export_threatmodels.py` – export all profiles to files
