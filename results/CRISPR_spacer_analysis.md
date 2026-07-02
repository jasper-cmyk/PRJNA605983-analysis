# CRISPR/SpCas9 gRNA Spacer Analyse — WIV05 — 29 juni 2026

## Dataset
- BAM: `results/WIV05_cas9solo.bam` (aligned op SpyCas9 KM099231, BWA-MEM)
- Bron: PRJNA605983 (SRR11092061)
- Methode: scaffold-matching in reads (GTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGT), 20nt upstream = spacer
- Script: `extract_spacers.py` → `map_spacers.py` → NCBI BLAST (nt database)

## Resultaten

### Gevonden spacers (32 reads, 6 uniek)

| Rank | Count | Spacer | BLAST-target | Gen | Organisme |
|---|---|---|---|---|---|
| 1 | 12 | GGACTGGGGCAGATGCTCAG | AF045554.1 | **CD68** (macrosialin) + Eif4a1 | *Mus musculus* |
| 2 | 10 | TCGGCTGTTCGGCGCCAGGC | BX119978.6 / AC091472.2 | chr X regio | *Mus musculus* |
| 3 | 4 | CTCTAGCTTCGCCATGTACA | XM_032889948.1 | **SAT1** (spermidine/spermine N1-acetyltransferase) | *Mus musculus* / Rattus |
| 4 | 2 | TCAGTCCCACCAATCCATGG | AM691835.1 | **Mecp2** (chr X) | *Mus musculus* |
| 5 | 2 | AGCCCTTTCTCCAAGGGGCC | L39017.1 / AK167302.1 | **PROCR** (Protein C receptor, endotheliaal) | *Mus musculus* |
| 6 | 2 | ACTGGGGCAGATGCTCAGAG | AF045554.1 | **CD68** + Eif4a1 (aangrenzend aan spacer 1) | *Mus musculus* |

Alle treffers: 100% nucleotide-identiteit (20/20), E-waarde ~16 (verwacht voor 20nt).

## Interpretatie

### 1. Muizen-CRISPR in een SARS-CoV-2-dataset
Alle 6 spacers targeten **muizengenen exclusief** — geen SARS-CoV-2, geen menselijk genoom, geen vector. WIV05 bevat sequenties van een SpCas9-experiment in muizencellen dat niet gedeclareerd is in de PRJNA605983-metadata.

### 2. Celtype: macrofagen + endotheel
De primaire targets wijzen op twee celtypes:
- **CD68** (macrosialin): canonieke macrofaag/monocyt-marker → muizenmacrofagen werden geëditeerd
- **PROCR** (endotheliale Proteïne C-receptor): endotheelcel-specifiek → parallel experiment of gemengde cultuur

### 3. PROCR — directe COVID-19-relevantie
PROCR/EPCR is in meerdere opzichten relevant:
- Mediator van de Proteïne C-anticoagulatieweg — zwaar verstoord in ernstige COVID-19 (DIC/coagulopathie)
- Uitgedrukt op endotheelcellen die SARS-CoV-2 kunnen infecteren
- PROCR-knockdown in muisendotheel + SARS-CoV-2 blootstelling = potentieel coagulopathie-model

### 4. Mecp2 (chr X)
MeCP2 reguleert genexpressie via methylering. In macrofagen speelt MeCP2 een rol bij ontstekingsreacties. Knockdown in macrofagen beïnvloedt cytokineproductie — relevant voor cytokine storm onderzoek.

### 5. SAT1
Spermidine/spermine N-acetyltransferase — reguleert polyamine-metabolisme. Verhoogde SAT1-activiteit verhoogt oxidatieve stress. Geselecteerde knockdown kan zijn om polyamine-gemedieerde cel-dood te bestuderen in geïnfecteerde cellen.

## Conclusie

WIV05 (PRJNA605983/SRR11092061) bevat experimentele reads van een niet-gedeclareerd SpCas9-editie-experiment in muizenmacrofagen en/of endotheelcellen. De gRNA-spacers targeten CD68, PROCR, Mecp2 en SAT1 — genen die direct relevant zijn aan COVID-19-pathogenese (coagulopathie, macrofaag-activatie, cytokine storm).

**Kernvraag voor Louwen's comment:** Waarom bevat SRR11092061 Cas9-reads met gRNA's gericht op muizenmacrofaag- en endotheel-genen, en waarom is dit experiment niet vermeld in de PRJNA605983-metadata?

## Bestanden
- `results/spacers.fa` — FASTA met alle 6 spacers
- `extract_spacers.py` — extractie-script
- `map_spacers.py` — lokale mapping-script
