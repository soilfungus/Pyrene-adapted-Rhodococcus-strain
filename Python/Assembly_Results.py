from Bio import SeqIO
from Bio.SeqUtils import gc_fraction

# Change this to your actual file name
fasta_file = "ad.fasta"

# Collect stats
lengths = []
total_gc = 0
total_bases = 0

for record in SeqIO.parse(fasta_file, "fasta"):
    seq_len = len(record.seq)
    gc = gc_fraction(record.seq) * 100
    lengths.append(seq_len)
    total_bases += seq_len
    print(f"{record.id:<30} {seq_len:<12} {gc:.2f}%")

# Summary
print("\n" + "=" * 50)
print(f"Total contigs/scaffolds : {len(lengths)}")
print(f"Total assembly size     : {total_bases:,} bp")
print(f"Largest contig          : {max(lengths):,} bp")
print(f"Smallest contig         : {min(lengths):,} bp")
print(f"Average contig size     : {int(sum(lengths)/len(lengths)):,} bp")

# N50 calculation
sorted_lengths = sorted(lengths, reverse=True)
cumsum = 0
for l in sorted_lengths:
    cumsum += l
    if cumsum >= total_bases / 2:
        print(f"N50                     : {l:,} bp")
        break
