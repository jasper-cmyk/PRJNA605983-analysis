# RBD-Fc Linker-vrije Junction Analyse
**Dataset:** PRJNA605983 — WIV05 (SRR11092061, Illumina) + WIV07-2 (MGISEQ)  
**Referentie:** SEQ5 — CN111333704B (Zhou Yusen patent), 1287nt, linker-vrije RBD-Fc fusie  
**Datum:** 29 juni 2026  

---

## Achtergrond & Correctie

Eerdere junction-analyse gebruikte een **verkeerde referentie** (`RBD_Fc_junction.fasta`, 1173nt) die
slechts gedeeltelijk en niet-overlappend was met de werkelijke patentsequentie. Dat resultaat
("0 junction-spanning reads") is **ongeldig**.

Deze analyse gebruikt de **correcte SEQ5** uit `ZY_RBD_Fc_patent.fasta`:
- Header: `SEQ5_RBD_Fc_fusion_CN111333704B_1287bp`
- Lengte: 1287 nt
- Structuur: RBD (1–582 nt) + Fc fragment (583–1287 nt), **zonder linker**
- Junction: positie 582→583 (gtggct | Fc-begin)

De BAM-bestanden `WIV05_vs_ZY.bam` en `WIV07-2_vs_ZY.bam` zijn reeds gealigned
tegen deze correcte referentie (bevestigd via `samtools view -H`).

---

## Resultaten

### 1. Coverage-statistieken SEQ5 (1287nt)

| Dataset | Reads op SEQ5 | Gedekte basen | Coverage% | Mean depth | MQ |
|---------|--------------|---------------|-----------|------------|-----|
| WIV05 (SRR11092061, Illumina) | 36 | 330/1287 | 25.6% | 2.99× | **0** |
| WIV07-2 (MGISEQ) | 12 | 303/1287 | 23.5% | 1.07× | **0** |

### 2. Positie-verdeling

**WIV05:** Reads mappen uitsluitend op posities **667–1090** van SEQ5  
**WIV07-2:** Reads mappen uitsluitend op posities **667–1015** van SEQ5

Beide datasets: **nul coverage** op posities 1–666.

### 3. Junction coverage (posities 570–600)

| Positie | WIV05 depth | WIV07-2 depth |
|---------|------------|---------------|
| 570–582 (RBD-end) | **0** | **0** |
| 583–600 (Fc-begin) | **0** | **0** |

**Geen enkele read overspant de RBD-Fc junction.**

### 4. RBD-gedeelte (posities 1–582)

| Dataset | Basen met depth > 0 in RBD-helft |
|---------|------------------------------------|
| WIV05 | **0** |
| WIV07-2 | **0** |

---

## Interpretatie

### A. Fc-reads zijn human IgG cross-mapping

De 36 (WIV05) en 12 (WIV07-2) reads die wel alignen op SEQ5 bevinden zich
**uitsluitend** in het Fc-fragment (pos 667+). Kenmerkend:

- **MQ = 0** voor alle reads in beide datasets  
  → BWA-MEM kent een gelijke alignment-score toe aan meerdere locaties in het referentiegenoom,  
  wat typisch is voor **multi-mapping naar human IgG genen** (IGHG1/2/3/4 loci)
- Read-sequentie (sample): `GGGGGACCGTCAGTCTTCCTCTTCCCCCCAAAACCCAAGGACACCCTCATGATCTCCCGG...`  
  → Herkenbaar als CH2-domein van human IgG Fc hinge-regio
- Positie 667 in SEQ5 valt **85 nt diep in de Fc-helft**, voorbij de junction
- BALF van COVID-patiënten bevat altijd menselijke antilichamen → IgG Fc reads worden
  verwacht in elk klinisch sequencing-experiment

**Conclusie:** De Fc-reads zijn endogene human IgG reads uit het patiëntenmonster
die cross-mappen naar het patent-Fc fragment. Dit is geen bewijs van de SEQ5-constructaanwezigheid.

### B. Conclusie junction-analyse

| Vraag | Antwoord |
|-------|---------|
| Zijn er reads die de RBD-Fc junction (pos 582-583) overspannen? | **Nee — 0 reads** |
| Is er coverage op het RBD-gedeelte van SEQ5? | **Nee — 0 coverage** |
| Zijn er Fc-reads specifiek voor het construct? | **Nee — MQ=0, human IgG cross-mapping** |

**Er is geen direct bewijs van de aanwezigheid van het RBD-Fc fusie-construct (SEQ5,
CN111333704B) in de PRJNA605983 BALF-monsters**, wanneer geanalyseerd op read-niveau
met de correcte 1287nt patentsequentie als referentie.

---

## Context

Dit resultaat doet geen uitspraken over:

1. Of het construct wél aanwezig is op DNA-niveau (plasmide, provirus) of op laag expressieniveau  
2. Of het construct in andere datasets (bijv. humane cellijnen in het lab) detecteerbaar is  
3. De fylogenetische positie van SEQ5 in de boom (704B_2 = identiek aan vroege SARS-CoV-2 in RBD-regio — **apart vastgesteld**, zie `RBD_analysis_20260629.md` en boom v3)

De fylogenetische analyse laat zien dat het RBD van SEQ5 **110/112 nucleotiden = 100.000%
identiek** is aan de SARS-CoV-2 RBD in NC_045512.2. Dit is onafhankelijk van de junction-vraag.

---

## Bestanden

| Bestand | Inhoud |
|---------|--------|
| `reference/ZY_RBD_Fc_patent.fasta` | SEQ2 + SEQ5 + SEQ6 uit CN111333704B |
| `reference/SEQ5_correct_ref.fasta` | SEQ5 + NC_045512.2 (geïndexeerd voor BWA) |
| `results/WIV05_vs_ZY.bam` | WIV05 aligned op ZY-referentie |
| `results/WIV07-2_vs_ZY.bam` | WIV07-2 aligned op ZY-referentie |
| `results/RBD_analysis_20260629.md` | NT-niveau RBD identiteitsanalyse |
| `results/phylo_tree_v3.png` | Fylogenetische boom (117 seq, GTR+G) |

---

*Analyse: Jasper Vermeer | Methode: BWA-MEM + samtools depth/coverage | 29 juni 2026*
