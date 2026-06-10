#!/usr/bin/env python3

"""
Compare Two FASTA Sequences

Purpose:
    Compare two FASTA sequences position by position and report
    the first sequence differences found in the aligned region.

Important:
    This script is useful for quick inspection of similar sequences.
    It does not perform sequence alignment. For genomes with large
    insertions, deletions, rearrangements, or many variants, use tools
    such as breseq, MUMmer, or minimap2.

Usage:
    python compare_two_fasta_sequences.py reference.fasta query.fasta
    python compare_two_fasta_sequences.py reference.fasta query.fasta --max-differences 50
    python compare_two_fasta_sequences.py reference.fasta query.fasta --context 30

Dependencies:
    Biopython
"""

import argparse
from Bio import SeqIO


def load_first_sequence(fasta_file):
    """Load the first sequence from a FASTA file."""
    return next(SeqIO.parse(fasta_file, "fasta"))


def compare_sequences(reference, query, max_differences=20, context=20):
    """Compare two sequences base by base."""

    reference_length = len(reference.seq)
    query_length = len(query.seq)
    shorter_length = min(reference_length, query_length)

    print(f"Reference ID: {reference.id}")
    print(f"Query ID:     {query.id}")
    print(f"Reference length: {reference_length:,} bp")
    print(f"Query length:     {query_length:,} bp")
    print(f"Length difference: {abs(reference_length - query_length):,} bp")

    print("\nScanning aligned region for differences...")

    total_differences = 0
    printed_differences = 0

    for i, (ref_base, query_base) in enumerate(
        zip(reference.seq[:shorter_length], query.seq[:shorter_length])
    ):
        if ref_base != query_base:
            total_differences += 1

            if printed_differences < max_differences:
                start = max(0, i - context)
                end = min(shorter_length, i + context + 1)

                print(f"\nPosition {i + 1:,}:")
                print(
                    f"Reference: ...{reference.seq[start:i]}"
                    f"[{ref_base}]"
                    f"{reference.seq[i + 1:end]}..."
                )
                print(
                    f"Query:     ...{query.seq[start:i]}"
                    f"[{query_base}]"
                    f"{query.seq[i + 1:end]}..."
                )

                printed_differences += 1

    if total_differences > max_differences:
        print(f"\n...output limited to first {max_differences} differences.")

    print(f"\nTotal differences in aligned region: {total_differences}")

    if reference_length != query_length:
        print(
            "\nNote: The sequence length difference suggests that one or more "
            "insertions/deletions may be present."
        )
        print(
            "This simple script does not locate indels accurately because it "
            "does not perform sequence alignment."
        )


def main():
    parser = argparse.ArgumentParser(
        description="Compare two FASTA sequences position by position."
    )

    parser.add_argument(
        "reference_fasta",
        help="Reference FASTA file"
    )

    parser.add_argument(
        "query_fasta",
        help="Query FASTA file"
    )

    parser.add_argument(
        "--max-differences",
        type=int,
        default=20,
        help="Maximum number of differences to print. Default: 20."
    )

    parser.add_argument(
        "--context",
        type=int,
        default=20,
        help="Number of bases shown on each side of a difference. Default: 20."
    )

    args = parser.parse_args()

    reference = load_first_sequence(args.reference_fasta)
    query = load_first_sequence(args.query_fasta)

    compare_sequences(
        reference,
        query,
        max_differences=args.max_differences,
        context=args.context
    )


if __name__ == "__main__":
    main()
