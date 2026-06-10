#!/usr/bin/env python3

"""
Genome Assembly Summary

Purpose:
    Calculate basic genome assembly statistics from a FASTA file.

Outputs:
    - Sequence ID
    - Sequence length
    - GC content
    - Total number of contigs/scaffolds
    - Total assembly size
    - Largest contig
    - Smallest contig
    - Average contig size
    - N50

Usage:
    python genome_summary.py input.fasta

Example:
    python genome_summary.py assembly.fasta
"""

import argparse
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction


def calculate_n50(lengths):
    """Calculate N50 from a list of sequence lengths."""
    total_length = sum(lengths)
    cumulative_length = 0

    for length in sorted(lengths, reverse=True):
        cumulative_length += length
        if cumulative_length >= total_length / 2:
            return length

    return None


def summarize_fasta(fasta_file):
    """Print assembly statistics for a FASTA file."""

    lengths = []
    total_bases = 0

    print("\nSequence summary")
    print("=" * 60)
    print(f"{'Sequence ID':<30} {'Length (bp)':<15} {'GC (%)'}")
    print("-" * 60)

    for record in SeqIO.parse(fasta_file, "fasta"):
        sequence_length = len(record.seq)
        gc_content = gc_fraction(record.seq) * 100

        lengths.append(sequence_length)
        total_bases += sequence_length

        print(f"{record.id:<30} {sequence_length:<15,} {gc_content:.2f}")

    if not lengths:
        raise ValueError("No sequences found. Check that the input file is a valid FASTA file.")

    print("\nAssembly summary")
    print("=" * 60)
    print(f"Total contigs/scaffolds : {len(lengths)}")
    print(f"Total assembly size     : {total_bases:,} bp")
    print(f"Largest contig          : {max(lengths):,} bp")
    print(f"Smallest contig         : {min(lengths):,} bp")
    print(f"Average contig size     : {int(sum(lengths) / len(lengths)):,} bp")
    print(f"N50                     : {calculate_n50(lengths):,} bp")


def main():
    parser = argparse.ArgumentParser(
        description="Calculate basic genome assembly statistics from a FASTA file."
    )

    parser.add_argument(
        "fasta",
        help="Input FASTA file"
    )

    args = parser.parse_args()

    summarize_fasta(args.fasta)


if __name__ == "__main__":
    main()
