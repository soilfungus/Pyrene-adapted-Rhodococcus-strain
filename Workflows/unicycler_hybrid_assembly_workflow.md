# Simple hybrid bacterial genome assembly and polishing workflow

## Author

Gabriela Calcáneo-Hernández

## Overview

This workflow describes a general strategy for assembling and polishing a bacterial genome using:

* Oxford Nanopore long reads
* Illumina paired-end reads
* Unicycler hybrid assembly
* Medaka polishing
* Pilon polishing

The workflow is suitable for bacterial chromosomes and plasmids.

---

## Requirements

### Software

* Unicycler
* Medaka
* BWA
* SAMtools
* Pilon

### Input files

Nanopore reads:

```text
long_reads.fastq
```

Illumina paired-end reads:

```text
sample_R1.fastq.gz
sample_R2.fastq.gz
```

Optional reference genome:

```text
reference_genome.fasta
```

---

# 1. Create Unicycler environment

```bash
conda create -n unicycler_env python=3.11 -y
conda activate unicycler_env
```

Install Unicycler:

```bash
conda install -c bioconda -c conda-forge unicycler -y
```

Verify installation:

```bash
unicycler --help
```

---

# 2. Run hybrid assembly

Navigate to the working directory:

```bash
cd /path/to/project
```

Run Unicycler:

```bash
unicycler \
    -1 sample_R1.fastq.gz \
    -2 sample_R2.fastq.gz \
    -l long_reads.fastq \
    -o assembly_output \
    --threads 8
```

Main output:

```text
assembly_output/assembly.fasta
```

---

# 3. Evaluate assembly

Count assembled replicons:

```bash
grep -c ">" assembly_output/assembly.fasta
```

Check assembly size:

```bash
grep -v ">" assembly_output/assembly.fasta | wc -c
```

Optional:

```bash
python Python/genome_summary.py assembly_output/assembly.fasta
```

Review:

* chromosome completeness
* plasmid completeness
* total assembly size
* contig count

---

# 4. Nanopore-based polishing with Medaka

Create Medaka environment:

```bash
conda create -n medaka_env -c conda-forge -c bioconda medaka -y
conda activate medaka_env
```

Run polishing:

```bash
medaka_consensus \
    -i long_reads.fastq \
    -d assembly_output/assembly.fasta \
    -o medaka_output \
    -t 8
```

Output:

```text
medaka_output/consensus.fasta
```

---

# 5. Illumina-based polishing with Pilon

```bash
conda install -c bioconda bwa samtools pilon -y
```

Create a polishing script:

```bash
nano run_pilon.sh
```

Paste:

```bash
#!/bin/bash

GENOME="medaka_output/consensus.fasta"
R1="sample_R1.fastq.gz"
R2="sample_R2.fastq.gz"

THREADS=8
ROUNDS=6

for i in $(seq 1 $ROUNDS)
do
    echo "Starting Pilon round $i"

    bwa index "$GENOME"

    bwa mem -t "$THREADS" "$GENOME" "$R1" "$R2" | \
        samtools sort -o "illumina_round${i}.bam"

    samtools index "illumina_round${i}.bam"

    pilon \
        --genome "$GENOME" \
        --bam "illumina_round${i}.bam" \
        --output "pilon_round${i}" \
        --threads "$THREADS"

    GENOME="pilon_round${i}.fasta"
done
```

Make executable:

```bash
chmod +x run_pilon.sh
```

Run:

```bash
./run_pilon.sh
```

Final assembly:

```text
pilon_round6.fasta
```

---

# 7. Assess polishing progress

Check correction counts:

```bash
wc -l pilon_round*.changes
```

A successful polishing process generally shows:

* many corrections in early rounds
* progressively fewer corrections in later rounds
* minimal corrections in the final rounds

---

# 8. Final assembly assessment

Check assembly statistics:

```bash
python Python/genome_summary.py pilon_round6.fasta
```

Optional quality assessment:

```bash
busco \
    -i pilon_round6.fasta \
    -m genome \
    -l bacteria_odb10 \
    -o busco_results
```

Optional annotation:

```bash
bakta \
    --db /path/to/bakta_db \
    pilon_round6.fasta
```

---

# Workflow summary

```text
Nanopore reads
        +
Illumina reads
        ↓
Unicycler
        ↓
assembly.fasta
        ↓
Medaka
        ↓
consensus.fasta
        ↓
Pilon round 1
        ↓
Pilon round 2
        ↓
Pilon round 3
        ↓
Pilon round 4
        ↓
Pilon round 5
        ↓
Pilon round 6
        ↓
Final polished assembly
```

---

# Notes

* Hybrid assembly often produces more complete bacterial genomes than short-read-only approaches.
* Long reads improve structural resolution of chromosomes and plasmids.
* Illumina polishing improves base-level accuracy.
* The optimal number of Pilon rounds depends on read quality and assembly quality.
