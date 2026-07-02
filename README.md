# Forensic Bioinformatic Analysis of PRJNA605983 and PRJCA002163

**Authors:** Jasper Vermeer¹ · Rogier Louwen²  
**Affiliations:** ¹Sovereign Health Botanicals, Ghent, Belgium · ²CCassured, Ulvenhout, The Netherlands  
**Corresponding author:** R. Louwen — [r.louwen@ccassured.com](mailto:r.louwen@ccassured.com)

> This repository contains all code, reference sequences, and result summaries supporting the *Matters Arising* comment submitted to *Nature* in response to Zhou et al. (2020, PMID 32015507).

---

## Background

Zhou et al. (2020) reported the first SARS-CoV-2 genome sequences from bronchoalveolar lavage fluid (BALF) samples collected from patients in Wuhan in December 2019. The raw sequencing data were deposited in NCBI SRA under accession **PRJNA605983** (MGISEQ-2000 and MiSeq platforms). A companion dataset of 114 assembled genomes from the same cohort was deposited in NGDC under **PRJCA002163**.

This analysis identifies five categories of anomalies in the publicly available raw data that warrant clarification from the original authors.

---

## Five Key Findings

### 1. RBD-Fc Fusion Sequences (Section 1)
Reads mapping to the RBD-Fc junction of Zhou Yusen's patented SARS-CoV-2 vaccine construct (CN111333704B, SEQ ID NO. 4) are present in BALF samples collected in December 2019 — prior to the patent filing date of 24 February 2020. The RBD terminus transitions directly into the IgG1-Fc hinge zone without an interposed linker, consistent with the patent's "optimal embodiment."

### 2. CRISPR/SpCas9 guide RNA Spacers (Section 2)
The SpyCas9 scaffold sequence (`GTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGT...`) is present in WIV05 (SRR11092057, MGISEQ-2000). Four 20-nt targeting spacers extracted from scaffold-containing reads map exclusively to *Mus musculus* genomic loci:

| Spacer | Reads | Target gene | Function |
|--------|-------|-------------|----------|
| GGACTGGGGCAGATGCTCAG | 12 | *Cd68* | Pan-macrophage marker |
| AGCCCTTTCTCCAAGGGGCC | 2 | *Procr* | Endothelial Protein C receptor |
| TCAGTCCCACCAATCCATGG | 2 | *Mecp2* | Epigenetic regulator, chrX |
| CTCTAGCTTCGCCATGTACA | 4 | *Sat1* | Polyamine metabolism |

These spacers are absent from hg38, absent from all SARS-CoV-2 sequences, and absent from the MiSeq platform control (WIV06, SRR11092059).

### 3. GPS Metadata Anomaly (Section 3)
Batch 2 of PRJCA002163 (101 samples, SAMC311431–SAMC311531, submitted January 2021) carries GPS coordinates 38.98°N 77.11°W in the structured metadata field — corresponding to Walter Reed National Military Medical Center, Bethesda, Maryland, USA — while the free-text collection location field reads "China: Wuhan." Batch 1 (ICU and YB samples, submitted January–March 2020) carries correct Wuhan coordinates.

### 4. Phylogenetic Star Topology and nsp12 Clonality (Section 4)
IQ-TREE2 analysis (GTR+G, 1000 UFBoot, outgroups ZC45/ZXC21) reveals a pronounced star topology: 83/117 internal branches have length ≈ 0. Comparison with ZC45 and ZXC21 branch lengths (100–1000× longer) is inconsistent with natural viral evolution over 4 months of circulation.

nsp12 (RdRp, 3,212 nt) clonality across 111 assemblies:
- **96/111 assemblies: 100.000% nucleotide identity** to NC_045512.2
- Mean identity: 99.9916%
- Expected substitutions after 4 months at SARS-CoV-2 mutation rate (~10⁻³/site/year): ~1.07 per copy
- Observed in 86.5% of assemblies: 0

### 5. H7N9 and Nipah Sequences (Section 5)
Avian influenza H7N9 hemagglutinin reads are present in 3 BALF samples. Nipah virus nucleoprotein reads (634 reads in WIV05, 683 reads in WIV07-2) replicate the independent finding of Quay et al. (2021). Neither pathogen is reported in the original methods.

---

## Repository Structure

```
PRJNA605983-analysis/
├── scripts/
│   ├── 01_download_reads.sh              # fasterq-dump from NCBI SRA
│   ├── 02_align_multi_reference.sh       # BWA-MEM multi-reference alignment
│   ├── 03_crispr_spacer_extraction.py    # Extract gRNA spacers from scaffold reads
│   ├── 04_crispr_spacer_mapping.py       # Map spacers to reference genomes
│   ├── 05_phylogenetic_analysis.sh       # MAFFT + IQ-TREE2 pipeline
│   ├── 06_nsp12_clonality.sh             # nsp12 identity calculation
│   └── visualize_tree.py                 # Phylogenetic tree figure
├── reference/
│   └── accessions.txt                    # GenBank accessions for all references
├── results/
│   ├── figures/
│   │   └── phylo_tree_v4.png             # Final phylogenetic tree figure
│   ├── CRISPR_spacer_analysis.md         # Detailed spacer results
│   ├── RBD_analysis.md                   # RBD-Fc alignment results
│   └── RBD_Fc_junction_analysis.md       # Junction read analysis
├── data/
│   └── (sequence inputs — see Data Availability)
├── environment.yml                       # Conda environment
└── .gitignore
```

---

## Reproducibility

### Environment setup
```bash
conda env create -f environment.yml
conda activate prjna605983
```

### Full pipeline
```bash
bash scripts/01_download_reads.sh          # ~15 GB total
bash scripts/02_align_multi_reference.sh
python3 scripts/03_crispr_spacer_extraction.py results/WIV05.bam
python3 scripts/04_crispr_spacer_mapping.py
bash scripts/05_phylogenetic_analysis.sh
bash scripts/06_nsp12_clonality.sh
python3 scripts/visualize_tree.py
```

---

## Data Availability

| Dataset | Accession | Repository |
|---------|-----------|------------|
| Raw reads (PRJNA605983) | SRR11092056, SRR11092057, SRR11092059, SRR11092061 | NCBI SRA |
| Assembled genomes (PRJCA002163) | SAMC311431–SAMC311531 | NGDC |
| BAM files (this analysis) | 10.5281/zenodo.21136779 | Zenodo |
| Code (this repository) | 10.5281/zenodo.21136779 | Zenodo / GitHub |

---

## Citation

Vermeer J, Louwen R. *Anomalies in the raw sequencing data of the first SARS-CoV-2 patient samples: a Matters Arising comment on Zhou et al. (2020).* Submitted to *Nature*, July 2026.

---

## License

MIT License. See [LICENSE](LICENSE).

---

*Analysis performed on: ThinkPad / Ubuntu 22.04 · BWA 0.7.17 · samtools 1.19 · MAFFT 7.520 · IQ-TREE2 2.3.5 · Python 3.11*
