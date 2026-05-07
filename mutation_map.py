from Bio import SeqIO
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

vcf_file = "biolearn_adapt2.vcf"
genome_file = "ad.fasta"

# Get genome length
genome = next(SeqIO.parse(genome_file, "fasta"))
genome_length = len(genome.seq)

# Parse VCF
positions = []
types = []
refs = []
alts = []

with open(vcf_file, "r") as f:
    for line in f:
        if line.startswith("#"):
            continue
        cols = line.strip().split("\t")
        if len(cols) < 8:
            continue

        pos = int(cols[1])
        ref = cols[3]
        alt = cols[4]

        # Classify mutation type
        if len(ref) > len(alt):
            mut_type = "Deletion"
        elif len(ref) < len(alt):
            mut_type = "Insertion"
        else:
            mut_type = "SNP"

        positions.append(pos)
        types.append(mut_type)
        refs.append(ref)
        alts.append(alt)

# Assign colors
color_map = {"SNP": "steelblue", "Insertion": "green", "Deletion": "red"}
colors = [color_map[t] for t in types]

# Plot
fig, ax = plt.subplots(figsize=(14, 4))

# Draw genome as a grey bar
ax.barh(0, genome_length, height=0.1, color="lightgrey", edgecolor="black", zorder=1)

# Draw each mutation as a vertical line
for pos, color, mut_type, ref, alt in zip(positions, colors, types, refs, alts):
    ax.vlines(pos, -0.4, 0.4, color=color, linewidth=2.5, zorder=2)

# Annotate each mutation
for pos, mut_type, ref, alt in zip(positions, types, refs, alts):
    if mut_type == "Deletion":
        label = f"DEL\n{pos:,}"
    elif mut_type == "Insertion":
        label = f"INS\n{pos:,}"
    else:
        label = f"{ref}→{alt}\n{pos:,}"
    ax.text(pos, 0.55, label, fontsize=6.5, ha="center", va="bottom", rotation=0)

# Legend
legend_patches = [
    mpatches.Patch(color="steelblue", label=f"SNP ({types.count('SNP')})"),
    mpatches.Patch(color="green",     label=f"Insertion ({types.count('Insertion')})"),
    mpatches.Patch(color="red",       label=f"Deletion ({types.count('Deletion')})")
]
ax.legend(handles=legend_patches, loc="lower right", fontsize=9)

# Formatting
ax.set_xlim(0, genome_length)
ax.set_ylim(-1, 1.5)
ax.set_xlabel("Genome Position (bp)", fontsize=11)
ax.set_title(f"Mutation Map — AD vs WT\n{genome_length:,} bp genome  |  {len(positions)} total variants", fontsize=12)
ax.set_yticks([])
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

plt.tight_layout()
plt.savefig("mutation_map.png", dpi=150)
plt.show()

print(f"Plot saved as mutation_map.png")
print(f"\nSummary:")
print(f"  SNPs:       {types.count('SNP')}")
print(f"  Insertions: {types.count('Insertion')}")
print(f"  Deletions:  {types.count('Deletion')}")