#!/usr/bin/env python3

"""
VCF to Table Converter

Purpose:
    Parse a VCF file and generate a clean summary table of variants.

Outputs:
    - Position
    - Reference allele
    - Alternate allele
    - Gene (if available)
    - INFO field summary

Usage:
    python vcf_to_table.py variants.vcf

Dependencies:
    None (standard Python only)

Compatible with:
    - breseq VCF files
    - most standard VCF files
"""

import argparse


def extract_gene(info_field):
    """Extract gene name from INFO field."""

    for field in info_field.split(";"):
        if field.startswith("gene="):
            return field.split("=", 1)[1]

        if field.startswith("GENE="):
            return field.split("=", 1)[1]

    return "unknown"


def parse_vcf(vcf_file):
    """Parse variants from a VCF file."""

    variants = []

    with open(vcf_file) as handle:
        for line in handle:

            if line.startswith("#"):
                continue

            columns = line.strip().split("\t")

            if len(columns) < 8:
                continue

            chromosome = columns[0]
            position = columns[1]
            reference = columns[3]
            alternate = columns[4]
            info = columns[7]

            variants.append({
                "chromosome": chromosome,
                "position": position,
                "reference": reference,
                "alternate": alternate,
                "gene": extract_gene(info),
                "info": info[:60]
            })

    return variants


def print_table(variants):
    """Print formatted variant table."""

    print(
        f"{'Chromosome':<20} "
        f"{'Position':<12} "
        f"{'Ref':<8} "
        f"{'Alt':<8} "
        f"{'Gene':<20} "
        f"{'Info'}"
    )

    print("-" * 110)

    for variant in variants:
        print(
            f"{variant['chromosome']:<20} "
            f"{variant['position']:<12} "
            f"{variant['reference']:<8} "
            f"{variant['alternate']:<8} "
            f"{variant['gene']:<20} "
            f"{variant['info']}"
        )

    print(f"\nTotal variants found: {len(variants)}")


def main():

    parser = argparse.ArgumentParser(
        description="Convert a VCF file into a readable variant summary table."
    )

    parser.add_argument(
        "vcf",
        help="Input VCF file"
    )

    args = parser.parse_args()

    variants = parse_vcf(args.vcf)

    if not variants:
        print("No variants found.")
        return

    print_table(variants)


if __name__ == "__main__":
    main()
