#!/usr/bin/env python3

"""
Compare Assembly Statistics

Purpose:
    Calculate basic assembly statistics for all FASTA files
    in a folder.

Outputs:
    - File name
    - Number of contigs/scaffolds
    - Total assembly size
    - Largest contig/scaffold
    - N50
    - GC content

Usage:
    python compare_assemblies.py
    python compare_assemblies.py path/to/fasta_folder

Dependencies:
    Biopython

Reference:
    Cock et al. (2009) Biopython.
    Bioinformatics 25(11):1422-1423.
    doi:10.1093/bioinformatics/btp163
"""

import argparse
from pathlib import Path
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction


FASTA_EXTENSIONS = {".fasta", ".fa", ".fna"}


def calculate_n50(lengths):
    """Calculate N50 from a list of sequence lengths."""
    total_length = sum(lengths)
    cumulative_length = 0

    for length in sorted(lengths, reverse=True):
        cumulative_length += length
        if cumulative_length >= total_length / 2:
            return length

    return 0


def summarize_fasta(fasta_file):
    """Calculate assembly statistics for one FASTA file."""
    lengths = []
    total_gc_bases = 0
    total_bases = 0

    for record in SeqIO.parse(fasta_file, "fasta"):
        sequence_length = len(record.seq)
        lengths.append(sequence_length)
        total_bases += sequence_length
        total_gc_bases += gc_fraction(record.seq) * sequence_length

    if not lengths:
        return None

    return {
        "file": fasta_file.name,
        "contigs": len(lengths),
        "total_size": total_bases,
        "largest_contig": max(lengths),
        "n50": calculate_n50(lengths),
        "gc_percent": round((total_gc_bases / total_bases) * 100, 2),
    }


def find_fasta_files(folder):
    """Find FASTA files in the selected folder."""
    return sorted(
        file for file in folder.iterdir()
        if file.is_file() and file.suffix.lower() in FASTA_EXTENSIONS
    )


def print_results(results):
    """Print assembly statistics as a formatted table."""
    print(f"{'File':<35} {'Contigs':<10} {'Size (bp)':<15} {'Largest':<15} {'N50':<15} {'GC (%)'}")
    print("-" * 105)

    for result in results:
        print(
            f"{result['file']:<35} "
            f"{result['contigs']:<10} "
            f"{result['total_size']:<15,} "
            f"{result['largest_contig']:<15,} "
            f"{result['n50']:<15,} "
            f"{result['gc_percent']}"
        )


def main():
    parser = argparse.ArgumentParser(
        description="Compare assembly statistics for all FASTA files in a folder."
    )

    parser.add_argument(
        "folder",
        nargs="?",
        default=".",
        help="Folder containing FASTA files. Default: current folder."
    )

    args = parser.parse_args()
    folder = Path(args.folder)

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    fasta_files = find_fasta_files(folder)

    if not fasta_files:
        print("No FASTA files found in this folder.")
        return

    results = []

    for fasta_file in fasta_files:
        summary = summarize_fasta(fasta_file)
        if summary:
            results.append(summary)

    print_results(results)


if __name__ == "__main__":
    main()
