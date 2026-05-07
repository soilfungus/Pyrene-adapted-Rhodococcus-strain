from Bio import SeqIO

# Load both assemblies
wt = next(SeqIO.parse("wt.fasta", "fasta"))
ad = next(SeqIO.parse("ad.fasta", "fasta"))

print(f"WT length:  {len(wt.seq):,} bp")
print(f"AD length:  {len(ad.seq):,} bp")
print(f"Difference: {abs(len(wt.seq) - len(ad.seq))} bp")

# Compare the first 1000 bases
print("\nComparing first 1000 bases...")
differences = 0
for i, (wt_base, ad_base) in enumerate(zip(wt.seq[:1000], ad.seq[:1000])):
    if wt_base != ad_base:
        print(f"  Position {i+1}: WT={wt_base}  AD={ad_base}")
        differences += 1

print(f"\nDifferences found in first 1000 bp: {differences}")