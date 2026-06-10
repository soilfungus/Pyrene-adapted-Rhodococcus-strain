# Hybrid bacterial genome assembly workflow

## Purpose

This workflow describes a reusable strategy for assembling and polishing a bacterial genome using Oxford Nanopore long reads and Illumina paired-end reads.

The workflow includes:

- long-read assembly with Canu
- troubleshooting low-coverage or stalled correction steps
- Illumina-based polishing with Pilon
- basic assembly checking

## Requirements

- conda or mamba
- Canu
- BWA
- SAMtools
- Pilon
- Nanopore FASTQ file
- Illumina paired-end FASTQ files

## Input files

```text
long_reads.fastq
sample_R1.fastq.gz
sample_R2.fastq.gz
```

Optional reference genome:

```text
reference_genome.fasta
```

## 1. Create Canu environment

```bash
conda create -n canu_env python=3.11 -y
conda activate canu_env
conda install -c conda-forge -c bioconda canu -y
```

Check installation:

```bash
canu --version
```

## 2. Run Canu assembly

Replace `7m` with the expected genome size.

```bash
canu \
  -p sample \
  -d sample_canu \
  genomeSize=7m \
  -nanopore long_reads.fastq \
  useGrid=false \
  maxThreads=8
```

Expected output:

```text
sample_canu/sample.contigs.fasta
```

Check contigs:

```bash
grep ">" sample_canu/sample.contigs.fasta
```

## 3. Check number of Nanopore reads

```bash
wc -l long_reads.fastq
```

FASTQ files contain 4 lines per read:

```text
number_of_reads = total_lines / 4
```

## 4. Troubleshooting Canu correction step

If Canu stalls during the correction overlap step, for example at:

```text
cormhap
```

you can rerun Canu treating reads as corrected:

```bash
canu \
  -p sample \
  -d sample_canu \
  genomeSize=7m \
  -nanopore long_reads.fastq \
  useGrid=false \
  maxThreads=8 \
  -corrected \
  stopOnLowCoverage=5
```

Expected output:

```text
sample_canu/sample.contigs.fasta
```

## 5. Install polishing tools

```bash
conda install -c bioconda bwa samtools pilon -y
```

## 6. Polish assembly with Illumina reads

Create a script:

```bash
nano run_pilon.sh
```

Paste:

```bash
#!/bin/bash

GENOME="sample_canu/sample.contigs.fasta"
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

Make the script executable:

```bash
chmod +x run_pilon.sh
```

Run polishing:

```bash
./run_pilon.sh
```

Final polished assembly:

```text
pilon_round6.fasta
```

## 7. Check Pilon corrections

```bash
wc -l pilon_round*.changes
```

A good polishing process usually shows fewer corrections in later rounds.

Example pattern:

```text
many corrections in early rounds
fewer corrections in later rounds
few or no corrections in final rounds
```

## 8. Basic assembly checks

Check number of contigs:

```bash
grep -c ">" pilon_round6.fasta
```

Check total assembly size:

```bash
grep -v ">" pilon_round6.fasta | wc -c
```

Optional: calculate genome statistics with a custom script:

```bash
python Python/genome_summary.py pilon_round6.fasta
```

## 9. Suggested output files to keep

```text
sample_canu/sample.contigs.fasta
pilon_round6.fasta
pilon_round*.changes
```
