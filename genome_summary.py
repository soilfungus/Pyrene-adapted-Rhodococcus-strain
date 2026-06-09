from Bio import SeqIO
from Bio.SeqUtils import gc_fraction
import os

# Folder where all your FASTA files are
fasta_folder = "."  # "." means current folder

# Collect results
results = []

# Loop through every FASTA file in the folder
for filename in os.listdir(fasta_folder):
    if filename.endswith(".fasta") or filename.endswith(".fa") or filename.endswith(".fna"):
        
        lengths = []
        total_gc_bases = 0
        total_bases = 0

        for record in SeqIO.parse(filename, "fasta"):
            seq_len = len(record.seq)
            lengths.append(seq_len)
            total_bases += seq_len
            total_gc_bases += gc_fraction(record.seq) * seq_len

        if lengths:
            # N50 calculation
            sorted_lengths = sorted(lengths, reverse=True)
            cumsum = 0
            n50 = 0
            for l in sorted_lengths:
                cumsum += l
                if cumsum >= total_bases / 2:
                    n50 = l
                    break

            results.append({
                "File": filename,
                "Contigs": len(lengths),
                "Total size (bp)": total_bases,
                "Largest contig": max(lengths),
                "N50": n50,
                "GC (%)": round(total_gc_bases / total_bases * 100, 2)
            })

# Print results as a table
if results:
    # Header
    print(f"{'File':<35} {'Contigs':<10} {'Size (bp)':<15} {'Largest':<15} {'N50':<15} {'GC%'}")
    print("-" * 100)
    
    for r in results:
        print(f"{r['File']:<35} {r['Contigs']:<10} {r['Total size (bp)']:<15,} {r['Largest contig']:<15,} {r['N50']:<15,} {r['GC (%)']}")
else:
    print("No FASTA files found in this folder!")
