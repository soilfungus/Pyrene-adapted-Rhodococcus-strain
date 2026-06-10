# SNP Calling Workflow with BWA, SAMtools, and BCFtools

## Author

Gabriela Calcáneo-Hernández

## Purpose

Map paired-end sequencing reads to a reference genome and call sequence variants using BWA, SAMtools, and BCFtools.

This workflow is useful for comparing evolved, mutant, or experimental strains against a reference genome.

## Requirements

- conda or mamba
- BWA
- SAMtools
- BCFtools
- Reference genome in FASTA format
- Paired-end FASTQ files

## 1. Create conda environment

```bash
conda create -n snp_env -c bioconda -c conda-forge bwa samtools bcftools -y
```

Activate the environment:

```bash
conda activate snp_env
```

## 2. Prepare input files

Example file structure:

```text
project/
├── reference_genome.fasta
├── sample_R1.fastq.gz
└── sample_R2.fastq.gz
```

## 3. Index the reference genome

```bash
bwa index reference_genome.fasta
```

This creates BWA index files such as:

```text
.amb
.ann
.bwt
.pac
.sa
```

## 4. Map reads to the reference genome

```bash
bwa mem \
  reference_genome.fasta \
  sample_R1.fastq.gz \
  sample_R2.fastq.gz \
  > sample.sam
```

## 5. Convert SAM to BAM

```bash
samtools view -Sb sample.sam > sample.bam
```

## 6. Sort BAM file

```bash
samtools sort sample.bam -o sample.sorted.bam
```

## 7. Index sorted BAM file

```bash
samtools index sample.sorted.bam
```

This creates:

```text
sample.sorted.bam.bai
```

## 8. Call variants

```bash
bcftools mpileup \
  -f reference_genome.fasta \
  sample.sorted.bam | \
bcftools call \
  -mv \
  -Ov \
  -o sample.vcf
```

## 9. Inspect VCF file

```bash
less sample.vcf
```

Count variants:

```bash
grep -v "^#" sample.vcf | wc -l
```

## 10. Filter variants

Example filtering criteria:

```bash
bcftools filter \
  -i 'QUAL>30 && DP>10 && MQ>30' \
  sample.vcf \
  -o sample.filtered.vcf
```

## Output files

```text
sample.sam
sample.bam
sample.sorted.bam
sample.sorted.bam.bai
sample.vcf
sample.filtered.vcf
```

## Notes

- `QUAL > 30` keeps higher-confidence variants.
- `DP > 10` keeps variants with read depth greater than 10.
- `MQ > 30` keeps variants supported by reads with good mapping quality.
- FASTQ-based SNP calling may detect variants missed by assembly comparison.
- For bacterial laboratory evolution experiments, compare this output with results from tools such as breseq.
