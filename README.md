# Forensic Bioinformatic Analysis of PRJNA605983 and PRJCA002163

**Authors:** Jasper Vermeer¹ · Rogier Louwen²
**Affiliations:** ¹Sovereign Health Botanicals, Ghent, Belgium · ²CCassured, Breda, The Netherlands
**Corresponding author:** R. Louwen — [r.louwen@ccassured.com](mailto:r.louwen@ccassured.com)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21136779.svg)](https://doi.org/10.5281/zenodo.21136779)

> **Status:** Manuscript submitted to *Nature* and deposited as a preprint on bioRxiv — July 2026.

---

## Background

Zhou et al. (2020) reported the first SARS-CoV-2 genome sequences from bronchoalveolar lavage fluid (BALF) samples collected from patients in Wuhan in December 2019. The raw sequencing data were deposited in NCBI SRA under accession **PRJNA605983** (MGISEQ-2000RS and Illumina MiSeq platforms; NCBI SRA metadata incorrectly records some accessions as "Illumina HiSeq 3000"). A companion dataset of 114 assembled genomes from the same cohort was deposited in NGDC under **PRJCA002163**.

This analysis identifies five categories of anomalies in the publicly available raw data that warrant clarification from the original authors.

---

## Six Key Findings

### 1. RBD-Fc Fusion Sequences and Nucleotide Clonality (Sections 1–2)

Reads mapping to the RBD-Fc junction of Zhou Yusen's patented SARS-CoV-2 vaccine construct (CN111333704B, SEQ ID NO. 4) are present in BALF samples collected in December 2019 — prior to the patent filing date of 24 February 2020. The RBD terminus transitions directly into the IgG1-Fc hinge zone without an interposed linker, consistent with the patent's "optimal embodiment."

Independent nucleotide-level analysis of 111 PRJCA002163 assemblies reveals near-complete clonality at two independent genomic regions:
- **RBD (667 nt):** 109/111 assemblies at 100.000% identity to NC_045512.2
- **nsp12/RdRp (3,212 nt):** 96/111 assemblies at 100.000% identity; mean 99.9916%

At the observed SARS-CoV-2 mutation rate (~10⁻³ / site / year), four months of natural circulation would be expected to produce ~0.17 substitutions per RBD copy and ~1.07 per nsp12 copy. The observed pattern is inconsistent with sustained natural transmission.

### 2. CRISPR/SpCas9 guide RNA Spacers (Section 3)

The SpCas9 scaffold sequence (`GTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGT...`) is present in WIV05 (SRR11092061, MGISEQ-2000RS). Six targeting spacers extracted from scaffold-containing reads map exclusively to *Mus musculus* genomic loci:

| Spacer | Reads | Target gene | Function |
|--------|-------|-------------|----------|
| SP1 | 12 | *Cd68* | Pan-macrophage marker |
| SP2 | 2 | chrX locus | — |
| SP3 | 4 | *Sat1* | Polyamine metabolism |
| SP4 | 2 | *Mecp2* | Epigenetic regulator, chrX |
| SP5 | 8 | *Procr* | Endothelial Protein C receptor |
| SP6 | 4 | *Cd68*-adjacent | — |

All spacers are absent from hg38, absent from all SARS-CoV-2 sequences, and absent from the Illumina MiSeq platform control (WIV06, SRR11092056) at comparable depth.

### 3. GPS Metadata Anomaly (Section 5)

Batch 2 of PRJCA002163 (101 samples, SAMC311431–SAMC311531, submitted January 2021) carries GPS coordinates **38.98°N 77.11°W** in the structured metadata field — corresponding to **Walter Reed National Military Medical Center, Bethesda, Maryland, USA** — while the free-text collection location field reads "China: Wuhan." Batch 1 (ICU and YB samples, submitted January–March 2020) carries correct Wuhan coordinates.

### 4. Phylogenetic Star Topology and RecCA Rooting Inversion (Sections 6, 9)

IQ-TREE2 analysis (GTR+G, 1000 UFBoot, outgroups ZC45/ZXC21) reveals a pronounced star topology: 83/117 internal branches have length ≈ 0. ZC45 and ZXC21 branches are 100–1,000× longer, providing a hard empirical baseline for genuine evolutionary distance. This is inconsistent with natural viral evolution over four months of circulation.

RecCA-corrected phylogenetic rooting assigns **90.2% posterior probability to Lineage A** as the ancestral root (vs 8.0% in unconstrained models), separating the pandemic origin from the Huanan Seafood Market cluster (Lineage B).

### 5. Restriction Enzyme Signatures at Spike Insertions (Section 7)

The two SARS-CoV-2-specific spike insertions (Inserts 1 and 4, absent from RaTG13) each carry restriction enzyme signatures characteristic of directional molecular cloning:

- **Insert 1** (NC_045512.2 positions 21,740–21,829; 90 nt): flanked by NcoI-compatible sequences (CCATG / CATGGT). NcoI (CCATGG, 4-nt CATG overhang) is widely used for expression vector cloning. Wholly absent from RaTG13.
- **Insert 4** (encompassing the furin cleavage site, FCS; positions 23,453–23,752): flanked by two NdeI recognition sequences (CATATG) at 65 nt and 560 nt upstream of the FCS. NdeI is the standard restriction site for directional insertion into pET-series expression vectors. The inter-NdeI distance of 495 nt falls within the size range routinely used for restriction-fragment-based inserts in coronavirus reverse genetics systems. The dual-NdeI flanking architecture is absent from RaTG13, where the FCS itself does not exist.

The two ancestrally-inherited insertions (Inserts 2 and 3, present in RaTG13 at ~91% and ~75% identity) carry no equivalent restriction signatures. This dichotomy is consistent with the DEFUSE proposal methodology (Daszak et al., DARPA HR001118S0017-PREEMPT-PA-001, 2018). Restriction enzyme recognition sequences arise naturally in viral genomes; their presence alone does not constitute proof of engineering, and multiple alternative explanations remain formally possible.

### 6. Library-Specific Detection of H7N9 and Nipah (Section 4)

Avian influenza H7N9 hemagglutinin (KC853766) reads are present in all five deep-sequenced BALF samples, with extreme library-specific variation (all samples MGISEQ-2000RS):

| Sample | SRR | Platform | H7N9 mean depth | H7N9 RPM |
|--------|-----|----------|-----------------|----------|
| WIV07-2 | SRR11092059 | MGISEQ-2000RS | 1,472× | 234.6 |
| WIV04-2 | SRR11092062 | MGISEQ-2000RS | 26.65× | — |
| WIV05 | SRR11092061 | MGISEQ-2000RS | 8.94× | — |
| WIV02-2 | SRR11092063 | MGISEQ-2000RS | 8.74× | 0.79 |
| WIV06-2 | SRR11092060 | MGISEQ-2000RS | 4.95× | — |

> **Note:** NCBI SRA metadata for PRJNA605983 incorrectly lists the sequencing platform as "Illumina HiSeq 3000" for SRR11092060–SRR11092063. The original filenames (prefix `v300043428`) and depositor confirmation identify all five deep-sequenced libraries as **MGISEQ-2000RS** (BGI flowcell v300).

WIV07-2 shows 55× higher H7N9 mean depth than the next highest sample (WIV04-2, 26.65×), consistent with amplification of a pVAX1-H7N9-HA construct in the WIV07-2 library.

Nipah virus (AY988601) reads show **sample-specific variation within MGISEQ-2000RS**: present in WIV07-2 (683 reads, 36.8% breadth) and WIV05 (21.1% breadth), but yielding **zero reads** in the MGISEQ-2000RS library of WIV02-2 (SRR11092063; 134,166,390 reads) despite 100% H7N9 breadth in the same library. This library-specific pattern excludes biological co-infection and is consistent with sample-specific laboratory contamination.

Neither H7N9 nor Nipah is mentioned in the Zhou et al. (2020) methods. The negative control dataset (CRA002390; Wuhan University, Yu Zhou; 4 MiSeq BALF samples, patients 1+2) is negative for both pathogens.

### 7. Platform Metadata Manipulation in NCBI SRA (Supplementary)

A forensic audit of the NCBI SRA metadata reveals that the five deep-sequenced BALF libraries (SRR11092059–SRR11092063) are recorded as "Illumina HiSeq 3000" or "Illumina HiSeq 1000." Six independent lines of evidence establish this as deliberate mislabeling:

| Evidence | Detail |
|----------|--------|
| FASTQ read headers | BGI flowcell ID `v300043428` embedded in every read by the instrument |
| SRA alias field | Original filename `v300043428_L02_126_1.fq.gz` stored alongside `Illumina HiSeq 3000` in the same XML record |
| ENA DESIGN_DESCRIPTION | Depositors wrote "performed on the **MGISEQ-2000RS** platform" in free-text for all five libraries |
| NGDC/GSA CRA002423 | Same authors correctly recorded **MGISEQ-2000RS** in the Chinese national database for the same five libraries |
| Post-publication timing | PRJNA605983 went public 15 days after paper publication (2020-02-18); not cited in the data availability statement; mislabeling was introduced in a voluntary, separately planned deposit |
| Library prep kit | MGIEasy RNA Library Prep Set (Cat. No. 1000006384) named in submission — a BGI-proprietary kit incompatible with any Illumina instrument |

The three co-submitted Illumina MiSeq libraries (SRR11092056–58, SRR11092064) are correctly labeled on both NCBI and NGDC. The mislabeling is selective and internally inconsistent (both "HiSeq 3000" and "HiSeq 1000" used for libraries from a single flowcell), precluding a parsimonious administrative explanation. All four major public databases were searched for the missing flowcell positions (NCBI, ENA, NGDC, CNGB): positions L04_1–120 and L02_128+ are absent from all.

Full forensic documentation: [`platform_mislabeling_investigation_EN.docx`](platform_mislabeling_investigation_EN.docx)

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
│   ├── make_combined_figure.py           # Suppl Fig 3: library-stratified coverage (MGISEQ-2000RS)
│   ├── make_suppl_figures.py             # Suppl Figs 3a/3b/4: all-sample depth profiles
│   └── visualize_tree.py                 # Phylogenetic tree figure
├── reference/
│   └── accessions.txt                    # GenBank accessions for all references
├── results/
│   ├── figures/
│   │   ├── phylo_tree_v4.png                              # Phylogenetic tree (Fig 3)
│   │   ├── Suppl_Fig3_combined_library_stratified.png     # Suppl Fig 3 main
│   │   ├── Suppl_Fig3b_Nipah_all_samples.png              # Suppl Fig 3a: Nipah, 5 samples
│   │   ├── Suppl_Fig3c_SARS2_all_samples.png              # Suppl Fig 3b: SARS-2, 5 samples
│   │   └── Suppl_Fig4_H7N9_all_samples.png                # Suppl Fig 4: H7N9, 5 samples
│   ├── CRISPR_spacer_analysis.md         # Detailed spacer results
│   ├── RBD_analysis.md                   # RBD-Fc alignment results
│   └── RBD_Fc_junction_analysis.md       # Junction read analysis
├── CRA002390/                            # Negative control: Wuhan University (Yu Zhou)
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
python3 scripts/make_combined_figure.py    # Suppl Fig 3 (library-stratified within MGISEQ-2000RS)
python3 scripts/make_suppl_figures.py      # Suppl Figs 3a/3b/4 (all samples)
```

All BWA-MEM alignments were verified on 10 July 2026. BAM files are available on Zenodo (see DOI above).

---

## Data Availability

| Dataset | Accession | Repository |
|---------|-----------|------------|
| Raw reads — MiSeq control (WIV06) | SRR11092056 | NCBI SRA |
| Raw reads — 5 deep-sequenced BALF samples | SRR11092059–SRR11092063 | NCBI SRA |
| Assembled genomes (PRJCA002163) | SAMC133236–SAMC311531 | NGDC |
| Negative control (CRA002390, Yu Zhou) | SAMC141144–SAMC141147 | NGDC |
| BAM files and depth data (this analysis) | [10.5281/zenodo.21136779](https://doi.org/10.5281/zenodo.21136779) | Zenodo |
| Code (this repository) | [10.5281/zenodo.21136779](https://doi.org/10.5281/zenodo.21136779) | Zenodo / GitHub |

---

## Citation

Vermeer J, Louwen R. *Formal Comment on the Genomic and Metagenomic Analyses of Early Patient BALF Samples from Zhou et al. (2020).* Submitted to *Nature*, July 2026. Preprint: bioRxiv (pending).

---

## License

MIT License. See [LICENSE](LICENSE).

---

*Analysis performed on: ThinkPad / Ubuntu 22.04 · BWA 0.7.17 · samtools 1.19 · MAFFT 7.520 · IQ-TREE2 2.3.5 · Python 3.11*
*Figures generated: 10 July 2026*
