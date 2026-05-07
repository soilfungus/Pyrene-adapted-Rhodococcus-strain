from Bio import SeqIO
from Bio.SeqUtils import gc_fraction
import matplotlib.pyplot as plt

# ── Change this to your actual file name ──
fasta_file = "ad.fasta"

# Collect data
contig_ids = []
gc_values = []
lengths = []

for record in SeqIO.parse(fasta_file, "fasta"):
    contig_ids.append(record.id)
    gc_values.append(gc_fraction(record.seq) * 100)
    lengths.append(len(record.seq))

# Plot — bubble size = contig length
plt.figure(figsize=(10, 6))
plt.scatter(
    range(len(contig_ids)),  # X axis = contig number
    gc_values,               # Y axis = GC content
    s=[l / 5000 for l in lengths],  # bubble size = contig length
    alpha=0.6,
    color="steelblue",
    edgecolors="black",
    linewidths=0.5
)

plt.axhline(y=sum(gc_values)/len(gc_values), color="red",
            linestyle="--", label="Mean GC")

plt.xlabel("Contig Index")
plt.ylabel("GC Content (%)")
plt.title("GC Content per Contig\n(bubble size = contig length)")
plt.legend()
plt.tight_layout()
plt.savefig("gc_plot.png", dpi=150)
plt.show()

print("Plot saved as gc_plot.png")