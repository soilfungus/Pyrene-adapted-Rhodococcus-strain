# RNA secondary structure analysis of non-coding mutations using RNAfold

## Author

Gabriela Calcáneo-Hernández

## Overview

This workflow describes how to evaluate the potential structural impact of mutations located in:

* 5′ untranslated regions (5′UTRs)
* intergenic regions
* promoter-proximal regions
* other non-coding genomic sequences

Predicted RNA secondary structures are generated using RNAfold from the ViennaRNA package and compared between reference and mutant sequences.

---

## Requirements

### Software

* Python 3
* Biopython
* ViennaRNA Package (RNAfold)

### Install Biopython

```bash
pip install biopython
```

### Install ViennaRNA

macOS:

```bash
brew install viennarna
```

Linux:

```bash
conda install -c bioconda viennarna
```

Verify installation:

```bash
RNAfold --version
```

---

# 1. Extract sequences of interest

Identify the genomic region surrounding the mutation.

Examples:

* 5′UTR upstream of a coding sequence
* intergenic region
* promoter region
* local window around the mutation

Example FASTA file:

```text
>Reference
ATGCGATCGATCGATCGATCGATCGATCG

>Mutant
ATGCGATCGATCGAATCGATCGATCGATCG
```

Save as:

```text
region.fa
```

---

# 2. Predict RNA secondary structures

Run RNAfold:

```bash
RNAfold < region.fa
```

Example output:

```text
>Reference
ATGCGATCGATCGATCGATCGATCGATCG
(((....)))............
(-15.20)

>Mutant
ATGCGATCGATCGAATCGATCGATCGATCG
((((...))))...........
(-16.10)
```

The value in parentheses corresponds to the minimum free energy (MFE) in kcal/mol.

---

# 3. Calculate ΔΔG

Calculate:

\Delta\Delta G = \Delta G_{Mutant} - \Delta G_{Reference}

Example:

```text
Reference ΔG = -15.20 kcal/mol
Mutant ΔG    = -16.10 kcal/mol
```

Calculation:

```text
ΔΔG = -16.10 - (-15.20)
ΔΔG = -0.90 kcal/mol
```

Interpretation:

* Negative ΔΔG → increased predicted stability
* Positive ΔΔG → decreased predicted stability
* Values near zero → minimal predicted structural effect

---

# 4. Compare structural features

Inspect the predicted structures.

Look for:

* altered stem-loop formation
* expanded hairpins
* loss of base pairing
* changes near ribosome-binding sites
* changes near start codons
* altered accessibility of regulatory motifs

Possible outcomes:

| Observation               | Possible Interpretation                    |
| ------------------------- | ------------------------------------------ |
| Stronger stem-loop        | Increased RNA stability                    |
| Weaker stem-loop          | Reduced RNA stability                      |
| RBS becomes occluded      | Reduced translation                        |
| RBS becomes exposed       | Increased translation                      |
| Minimal structural change | Mutation may act through another mechanism |

---

# 5. Analyze local windows

In addition to the full region, analyze a smaller window surrounding the mutation.

Example:

```text
Mutation ± 20 bp
Mutation ± 50 bp
Mutation ± 100 bp
```

Create a FASTA file:

```text
local_window.fa
```

Run:

```bash
RNAfold < local_window.fa
```

Local windows often reveal subtle structural effects that may be hidden in larger regions.

---

# 6. Compare multiple regions

Common regions to evaluate include:

* full intergenic region
* promoter-proximal sequence
* 5′UTR
* mutation-centered local window

Comparing multiple windows helps distinguish:

* local effects
* long-range structural effects
* negligible structural effects

---

# 7. Biological interpretation

Possible biological mechanisms include:

### Translational regulation

Indicators:

* altered RBS accessibility
* altered start codon accessibility
* changes in local RNA stability

### Transcriptional regulation

Indicators:

* minimal RNA structural effects
* mutation located near promoter elements
* mutation located in transcription-factor binding regions

### DNA-Level regulatory effects

Indicators:

* little or no RNA structural change
* mutation within repetitive tracts
* mutation near promoter architecture elements

---

# Suggested citation wording

RNA secondary structures were predicted using RNAfold from the ViennaRNA package. Minimum free-energy (MFE) structures were compared between reference and mutant sequences using:

\Delta\Delta G = \Delta G_{Mutant} - \Delta G_{Reference}

Negative ΔΔG values indicate increased predicted thermodynamic stability in the mutant sequence, whereas positive values indicate decreased predicted stability.

---

# Notes

* RNAfold predictions represent computational models rather than direct experimental measurements.
* Small ΔΔG values should be interpreted cautiously.
* Structural predictions are most informative when combined with genomic context and biological evidence.
* Evaluating multiple sequence windows often improves interpretation of non-coding mutations.
