#!/usr/bin/env python3

"""
FASTA GC Content Calculator

Purpose:
    Calculate sequence length and GC content for all sequences
    in a FASTA file.

Outputs:
    - Sequence ID
    - Sequence length
    - GC content (%)

Usage:
    python fasta_gc_content.py sequences.fasta

Dependencies:
    Biopython

Reference:
    Cock et al. (2009) Biopython.
    Bioinformatics 25(11):1422-1423.
    doi:10.1093/bioinformatics/btp163
"""

import argparse
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction


def analyze_fasta(fasta_file):
    """Calculate length and GC content for each sequence."""

    print(f"{'Sequence ID':<30} {'Length (bp)':<15} {'GC (%)'}")
    print("-" * 60)

    sequence_count = 0

    for record in SeqIO.parse(fasta_file, "fasta"):
        gc_percent = gc_fraction(record.seq) * 100

        print(
            f"{record.id:<30} "
            f"{len(record.seq):<15,} "
            f"{gc_percent:.2f}"
        )

        sequence_count += 1

    print("-" * 60)
    print(f"Sequences analyzed: {sequence_count}")


def main():
    parser = argparse.ArgumentParser(
        description="Calculate GC content for sequences in a FASTA file."
    )

    parser.add_argument(
        "fasta",
        help="Input FASTA file"
    )

    args = parser.parse_args()

    analyze_fasta(args.fasta)


if __name__ == "__main__":
    main()
