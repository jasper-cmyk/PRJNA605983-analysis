#!/usr/bin/env python3
"""Phylogenetic tree v3 — lichte achtergrond, leesbare labels, patent als anker."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from Bio import Phylo

TREEFILE = "results/phylo_tree_v2.contree"
OUTFILE  = "results/phylo_tree_v3.png"

PATENT   = {"704B_2"}
OUTGROUP = {"RatG13"}
EARLY    = {
    "SARS-CoV-2_28Dec2019_submission",
    "GWHABKF00000001-WH-01_2019",
    "NC_045512.2",
}

def color(name):
    if not name:          return "#cccccc"
    if name in OUTGROUP:  return "#c0392b"   # rood
    if name in PATENT:    return "#27ae60"   # groen
    if name in EARLY:     return "#e67e22"   # oranje
    return "#2980b9"                          # blauw

def label(name):
    labels = {
        "RatG13":                              "RatG13 ▶ outgroup (~14% divergent)",
        "704B_2":                              "704B_2 ▶ Zhou Yusen patent SEQ5 (RBD-Fc, CN111333704B) ★",
        "SARS-CoV-2_28Dec2019_submission":     "SARS-CoV-2 28 dec 2019 ★",
        "GWHABKF00000001-WH-01_2019":          "WH-01 2019 ★",
        "NC_045512.2":                         "NC_045512.2 Wuhan-Hu-1 ★",
    }
    return labels.get(name, name)

tree = Phylo.read(TREEFILE, "newick")
tree.root_with_outgroup({"name": "RatG13"})

# Cladogram: gelijke taklengtes
for clade in tree.find_clades():
    clade.branch_length = 1.0

terminals = tree.get_terminals()
n = len(terminals)
fig_h = max(44, n * 0.23 + 4)

fig, ax = plt.subplots(figsize=(18, fig_h))
fig.patch.set_facecolor("white")
ax.set_facecolor("#f8f9fa")

Phylo.draw(tree, axes=ax, do_show=False,
           label_func=label,
           label_colors=lambda nm: color(nm) if nm else "#cccccc")

# Labels stylen
for text in ax.texts:
    raw = text.get_text()
    # strip onze toevoegingen terug naar originele naam voor kleurcheck
    orig = (raw.replace(" ▶ outgroup (~14% divergent)", "")
               .replace(" ▶ Zhou Yusen patent SEQ5 (RBD-Fc, CN111333704B) ★", "")
               .replace(" ★", "").strip())
    c = color(orig)
    is_key = orig in EARLY or orig in OUTGROUP or orig in PATENT
    text.set_color(c)
    text.set_fontsize(8.5 if is_key else 5.5)
    text.set_fontweight("bold" if is_key else "normal")

# Assen
ax.set_facecolor("#f8f9fa")
ax.set_title(
    "SARS-CoV-2 Fylogenetische Boom  —  117 sequenties (cladogram)\n"
    "IQ-TREE2 · GTR+G · 1000 ultrafast bootstrap · Geroot op RatG13\n"
    "Bron: PRJCA002163 (Zhengli et al.) + CN111333704B (Zhou Yusen patent) | Jasper Vermeer, 29 juni 2026",
    color="#222222", fontsize=10, pad=14, loc="left", fontweight="bold")
ax.set_xlabel("Evolutionaire stappen (cladogram)", color="#555555", fontsize=8)
ax.set_ylabel("Sequenties (n=117)", color="#555555", fontsize=8)
ax.tick_params(colors="#888888", labelsize=7)
for sp in ax.spines.values():
    sp.set_edgecolor("#dddddd")

# Legenda
legend_handles = [
    mpatches.Patch(color="#c0392b", label="RatG13 — outgroup (~14% divergent van SARS-CoV-2)"),
    mpatches.Patch(color="#27ae60", label="704B_2 — Zhou Yusen patent SEQ5 (CN111333704B, RBD-Fc linker-vrij)"),
    mpatches.Patch(color="#e67e22", label="Vroegste Wuhan-sequenties (december 2019)"),
    mpatches.Patch(color="#2980b9", label="WIV isolaten — PRJCA002163"),
]
ax.legend(handles=legend_handles, loc="lower right",
          facecolor="white", labelcolor="#222222",
          edgecolor="#cccccc", fontsize=9, framealpha=1.0)

ax.annotate(
    "⚠  83/117 interne takken: lengte ≈ 0  →  star-topologie\n"
    "Groen anker (704B_2) = Zhou Yusen patentsequentie SEQ5\n"
    "Positie in boom toont fylogenetische afstand tot vroege isolaten",
    xy=(0.02, 0.02), xycoords="axes fraction",
    color="#333333", fontsize=8,
    bbox=dict(boxstyle="round,pad=0.5", facecolor="white",
              edgecolor="#e67e22", alpha=1.0))

plt.tight_layout()
plt.savefig(OUTFILE, dpi=180, bbox_inches="tight", facecolor="white")
print(f"Boom opgeslagen: {OUTFILE}")
