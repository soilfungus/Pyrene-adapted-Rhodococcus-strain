from Bio import SeqIO

wt = next(SeqIO.parse("wt.fasta", "fasta"))
ad = next(SeqIO.parse("ad.fasta", "fasta"))

print(f"WT length:  {len(wt.seq):,} bp")
print(f"AD length:  {len(ad.seq):,} bp")
print(f"Difference: {abs(len(wt.seq) - len(ad.seq))} bp")

print("\nScanning entire genome for differences...")
differences = 0
shorter_len = min(len(wt.seq), len(ad.seq))

for i, (wt_base, ad_base) in enumerate(zip(wt.seq, ad.seq)):
    if wt_base != ad_base:
        # Show surrounding context (20 bases either side)
        start = max(0, i - 20)
        end = min(shorter_len, i + 20)
        print(f"\n  Position {i+1:,}:")
        print(f"  WT: ...{wt.seq[start:i]}[{wt_base}]{wt.seq[i+1:end]}...")
        print(f"  AD: ...{ad.seq[start:i]}[{ad_base}]{ad.seq[i+1:end]}...")
        differences += 1

        if differences >= 20:  # stop after 20 to avoid flooding output
            print("\n  ... (more differences found, stopping at 20)")
            break

print(f"\nTotal SNPs found in aligned region: {differences}")
print(f"\nNote: The {abs(len(wt.seq) - len(ad.seq))} bp size difference")
print(f"suggests an insertion/deletion (indel) exists somewhere too.")
print(f"Indels are harder to find by simple comparison — breseq handles these best.")
