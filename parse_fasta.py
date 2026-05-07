from Bio import SeqIO
from Bio.SeqUtils import gc_fraction

print(f"{'ID':<15} {'Length':<10} {'GC Content'}")
print("-" * 35)

for record in SeqIO.parse("my_sequences.fasta", "fasta"):
    gc = gc_fraction(record.seq) * 100
    print(f"{record.id:<15} {len(record.seq):<10} {gc:.2f}%")