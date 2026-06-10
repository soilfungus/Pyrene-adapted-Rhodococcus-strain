#!/usr/bin/env python3

"""
Mutation Map Generator

Purpose:
    Visualize mutations from a VCF file across a genome sequence.

Features:
    - SNP detection
    - Insertion detection
    - Deletion detection
    - Genome-wide mutation map
    - Mutation summary

Usage:
    python mutation_map.py genome.fasta variants.vcf

Dependencies:
    Biopython
    matplotlib

Example:
    python mutation_map.py genome.fasta variants.vcf
"""

import argparse
from Bio import SeqIO
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def classify_variant(ref, alt):
    """Classify variant type."""

    if len(ref) > len(alt):
        return "Deletion"

    if len(ref) < len(alt):
        return "Insertion"

    return "SNP"


def parse_vcf(vcf_file):
    """Extract variant information from a VCF file."""

    positions = []
    variant_types = []
    references = []
    alternates = []

    with open(vcf_file) as handle:

        for line in handle:

            if line.startswith("#"):
                continue

            columns = line.strip().split("\t")

            if len(columns) < 8:
                continue

            position = int(columns[1])
            reference = columns[3]
            alternate = columns[4]

            variant_type = classify_variant(reference, alternate)

            positions.append(position)
            variant_types.append(variant_type)
            references.append(reference)
            alternates.append(alternate)

    return positions, variant_types, references, alternates


def create_mutation_map(
    genome_length,
    positions,
    variant_types,
    references,
    alternates,
    output_file
):
    """Generate mutation map figure."""

    color_map = {
        "SNP": "steelblue",
        "Insertion": "green",
        "Deletion": "red"
    }

    fig, ax = plt.subplots(figsize=(14, 4))

    ax.barh(
        y=0,
        width=genome_length,
        height=0.1,
        color="lightgrey",
        edgecolor="black",
        zorder=1
    )

    for pos, variant_type in zip(positions, variant_types):

        ax.vlines(
            pos,
            -0.4,
            0.4,
            color=color_map[variant_type],
            linewidth=2.5,
            zorder=2
        )

    for pos, variant_type, ref, alt in zip(
        positions,
        variant_types,
        references,
        alternates
    ):

        if variant_type == "Deletion":
            label = f"DEL\n{pos:,}"

        elif variant_type == "Insertion":
            label = f"INS\n{pos:,}"

        else:
            label = f"{ref}>{alt}\n{pos:,}"

        ax.text(
            pos,
            0.55,
            label,
            fontsize=6,
            ha="center"
        )

    legend_patches = [
        mpatches.Patch(
            color="steelblue",
            label=f"SNP ({variant_types.count('SNP')})"
        ),
        mpatches.Patch(
            color="green",
            label=f"Insertion ({variant_types.count('Insertion')})"
        ),
        mpatches.Patch(
            color="red",
            label=f"Deletion ({variant_types.count('Deletion')})"
        )
    ]

    ax.legend(
        handles=legend_patches,
        loc="lower right"
    )

    ax.set_xlim(0, genome_length)
    ax.set_ylim(-1, 1.5)

    ax.set_xlabel("Genome Position (bp)")

    ax.set_title(
        f"Genome Mutation Map\n"
        f"{genome_length:,} bp | "
        f"{len(positions)} variants"
    )

    ax.set_yticks([])

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300)

    print(f"Figure saved: {output_file}")


def main():

    parser = argparse.ArgumentParser(
        description="Generate a genome-wide mutation map from a VCF file."
    )

    parser.add_argument(
        "genome",
        help="Reference genome FASTA file"
    )

    parser.add_argument(
        "vcf",
        help="VCF file"
    )

    parser.add_argument(
        "-o",
        "--output",
        default="mutation_map.png",
        help="Output figure name"
    )

    args = parser.parse_args()

    genome = next(SeqIO.parse(args.genome, "fasta"))
    genome_length = len(genome.seq)

    positions, variant_types, references, alternates = parse_vcf(args.vcf)

    create_mutation_map(
        genome_length,
        positions,
        variant_types,
        references,
        alternates,
        args.output
    )

    print("\nSummary")
    print("-" * 20)
    print(f"SNPs:       {variant_types.count('SNP')}")
    print(f"Insertions: {variant_types.count('Insertion')}")
    print(f"Deletions:  {variant_types.count('Deletion')}")


if __name__ == "__main__":
    main()
