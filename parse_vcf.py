# Parse a breseq VCF file into a clean readable table

vcf_file = "biolearn_adapt2.vcf"

variants = []

with open(vcf_file, "r") as f:
    for line in f:
        # Skip header lines
        if line.startswith("#"):
            continue
        
        # Split each line into columns
        cols = line.strip().split("\t")
        if len(cols) < 8:
            continue
        
        chrom    = cols[0]   # chromosome/contig
        position = cols[1]   # position in genome
        ref      = cols[3]   # reference base (WT)
        alt      = cols[4]   # alternate base (mutant)
        info     = cols[7]   # extra information

        # Try to extract gene name from INFO field
        gene = "unknown"
        for field in info.split(";"):
            if field.startswith("gene=") or field.startswith("GENE="):
                gene = field.split("=")[1]

        variants.append({
            "Position": position,
            "Ref": ref,
            "Alt": alt,
            "Gene": gene,
            "Info": info[:60]  # truncate long info
        })

# Print clean table
print(f"{'Position':<12} {'Ref':<10} {'Alt':<10} {'Gene':<20} {'Info'}")
print("-" * 90)
for v in variants:
    print(f"{v['Position']:<12} {v['Ref']:<10} {v['Alt']:<10} {v['Gene']:<20} {v['Info']}")

print(f"\nTotal variants found: {len(variants)}")