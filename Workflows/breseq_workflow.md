# breseq Variant Calling Workflow

## Purpose

Identify mutations in laboratory-evolved microbial strains using next-generation sequencing reads and a reference genome.

## Requirements

- conda or mamba
- breseq
- reference genome in FASTA format
- paired-end Illumina reads

## Install breseq

```bash
conda install -c bioconda breseq -y

# breseq Workflow

## Run breseq

```bash
breseq \
    -r reference_genome.fasta \
    sample_R1.fastq.gz \
    sample_R2.fastq.gz \
    -o breseq_output
```

### Parameters

| Parameter | Description |
|------------|------------|
| `-r` | Reference genome FASTA |
| `sample_R1.fastq.gz` | Forward reads |
| `sample_R2.fastq.gz` | Reverse reads |
| `-o` | Output directory |
