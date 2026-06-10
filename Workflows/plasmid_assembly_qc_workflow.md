# Plasmid assembly quality control and circular overlap removal workflow

## Author

Gabriela Calcáneo-Hernández

## Purpose

This workflow identifies and removes duplicated circular overlaps commonly found in plasmid assemblies generated from long-read sequencing data.

The workflow can be applied to any circular plasmid assembly prior to annotation, comparative genomics, or publication.

---

## Requirements

### Software

* MUMmer (`nucmer`, `show-coords`, `dnadiff`, `delta-filter`)
* SAMtools
* BLAST+
* mummerplot

### Input files

Reference plasmid:

```text
reference_plasmid.fasta
```

Query plasmid assembly:

```text
assembled_plasmid.fasta
```

---

# 1. Compare reference and query plasmids

Generate pairwise alignment statistics.

```bash
dnadiff \
    -p plasmid_compare \
    reference_plasmid.fasta \
    assembled_plasmid.fasta
```

Important output files:

```text
plasmid_compare.report
plasmid_compare.1coords
plasmid_compare.rdiff
plasmid_compare.qdiff
plasmid_compare.snps
```

Inspect alignment coordinates:

```bash
less plasmid_compare.1coords
```

Inspect structural differences:

```bash
cat plasmid_compare.rdiff
cat plasmid_compare.qdiff
```

---

# 2. Compare plasmid sizes

Calculate sequence lengths.

```bash
grep -v ">" reference_plasmid.fasta | wc -c
grep -v ">" assembled_plasmid.fasta | wc -c
```

Large size increases may indicate duplicated circular overlaps.

Common warning signs:

* Query plasmid substantially longer than reference
* Large terminal duplications
* Two nearly identical alignment blocks

---

# 3. Detect internal duplicated regions

Perform self-alignment.

```bash
nucmer \
    --maxmatch \
    -p self_alignment \
    assembled_plasmid.fasta \
    assembled_plasmid.fasta
```

View coordinates:

```bash
show-coords -rcl self_alignment.delta | less
```

Look for large duplicated regions near the beginning and end of the assembly.

Example pattern:

```text
1-15000 aligned with 105000-120000
```

This often indicates a duplicated circular overlap.

---

# 4. Trim the circular overlap

Index FASTA:

```bash
samtools faidx assembled_plasmid.fasta
```

Extract the non-redundant region:

```bash
samtools faidx \
    assembled_plasmid.fasta \
    contig_name:start-end \
    > plasmid_clean.fasta
```

Replace:

```text
contig_name
start
end
```

with coordinates determined from the self-alignment.

---

# 5. Verify the cleaned assembly

Align the cleaned plasmid against the reference.

```bash
nucmer \
    --prefix verify \
    reference_plasmid.fasta \
    plasmid_clean.fasta
```

Filter best alignments:

```bash
delta-filter -1 verify.delta > verify.filtered.delta
```

Inspect coordinates:

```bash
show-coords -rcl verify.filtered.delta
```

Expected result:

* Full-length alignment
* No large duplicated terminal regions
* Possible split alignment due to different circular start coordinates

---

# 6. Check for remaining duplications

Perform self-BLAST.

```bash
blastn \
    -query plasmid_clean.fasta \
    -subject plasmid_clean.fasta \
    -outfmt 6 | sort -k4 -nr | head
```

Interpretation:

* Small internal repeats are common
* Large end-to-end duplicated blocks should be absent

---

# 7. Generate dotplots

Visualize structural agreement.

```bash
nucmer \
    --prefix plasmid_plot \
    reference_plasmid.fasta \
    plasmid_clean.fasta
```

Generate plot:

```bash
mummerplot \
    --png \
    --layout \
    -p plasmid_plot \
    plasmid_plot.delta
```

Expected result:

* Continuous diagonal
* Split diagonal acceptable for circular molecules with different start positions
* Large duplicated regions should be absent

---

# Final output

Publication-ready plasmid assembly:

```text
plasmid_clean.fasta
```

Use this cleaned sequence for:

* Genome annotation
* Comparative genomics
* Variant analysis
* Public database submission
* Publication figures

---

# Notes

Long-read assemblers frequently duplicate the overlap region of circular replicons.

Always verify:

* assembly length
* self-alignment
* reference alignment
* dotplot structure

before using a plasmid assembly for downstream analyses.
