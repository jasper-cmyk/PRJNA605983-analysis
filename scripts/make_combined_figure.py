#!/usr/bin/env python3
"""
Supplemental Figure 3 — Library-stratified coverage profiles (MGISEQ-2000RS)
H7N9 HA / Nipah / SARS-CoV-2 in PRJNA605983 BALF libraries
WIV07-2 (SRR11092059) vs WIV02-2 (SRR11092063) — both MGISEQ-2000RS
Note: NCBI SRA incorrectly lists PRJNA605983 platform as "Illumina HiSeq 3000"
      Filename prefix v300043428 identifies MGISEQ-2000RS (BGI flowcell v300)
      Confirmed by depositor: Louwen, "Sequencing platforms used.docx", July 2026
Real depth data from BWA-MEM alignments verified 10 July 2026
Vermeer & Louwen 2026  |  300 dpi
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import numpy as np
import os

RES = "/home/jasper/wuhan-analysis/results"
OUT = "/home/jasper/wuhan-analysis/results/figures"
os.makedirs(OUT, exist_ok=True)

L_H7  = 1683
L_NiV = 18252
L_COV = 29903


def load_depth(path, length):
    d = np.zeros(length + 1)
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return d[1:]
    with open(path) as fh:
        for line in fh:
            parts = line.strip().split('\t')
            if len(parts) < 3:
                continue
            pos = int(parts[1])
            cov = float(parts[2])
            if 1 <= pos <= length:
                d[pos] = cov
    return d[1:]


def cap99(arr):
    vals = arr[arr > 0]
    if len(vals) == 0:
        return arr, 1.0
    p99 = np.percentile(vals, 99)
    return np.minimum(arr, p99), p99


# ── Panel definitions ──────────────────────────────────────────────────────────
# MGISEQ-2000RS WIV07-2 (SRR11092059)  vs  MGISEQ-2000RS WIV02-2 (SRR11092063)
# (NCBI SRA metadata incorrectly labels these as Illumina HiSeq 3000)
#
# Stats from BWA-MEM flagstat (BAMs deleted after depth extraction):
#   WIV07-2  H7N9 : 18,046 primary reads  (234.6 RPM)
#   WIV07-2  Nipah:    683 reads
#   WIV07-2  SARS2: 76,052 reads
#   WIV02-2  H7N9 :    106 primary reads  (0.79 RPM)
#   WIV02-2  Nipah:      0 reads
#   WIV02-2  SARS2: 365,033 primary reads
#
GROUPS = [
    {
        "title": "SARS-CoV-2  (NC_045512.2, 29,903 nt)",
        "color": "#059669",
        "bg":    "#ecfdf5",
        "panels": [
            dict(platform="MGISEQ  WIV07-2 (SRR11092059)",
                 depthfile="WIV07-2_SARS2_depth.txt",
                 reads="76,052",
                 narrative="patient SARS-CoV-2 infection  (both platforms)",
                 length=L_COV),
            dict(platform="MGISEQ-2000RS  WIV02-2 (SRR11092063)",
                 depthfile="WIV02-2_SARS2_depth.txt",
                 reads="365,033",
                 narrative="patient SARS-CoV-2 infection  (higher depth in WIV02-2 library)",
                 length=L_COV),
        ]
    },
    {
        "title": "H7N9 HA  (KC853766, 1,683 nt)  —  pVAX1 construct signal",
        "color": "#dc2626",
        "bg":    "#fef2f2",
        "panels": [
            dict(platform="MGISEQ  WIV07-2 (SRR11092059)",
                 depthfile="WIV07-2_H7N9_depth.txt",
                 reads="18,046",
                 narrative="uniform plateau: cloned insert signature  (234.6 RPM)",
                 length=L_H7),
            dict(platform="MGISEQ-2000RS  WIV02-2 (SRR11092063)",
                 depthfile="WIV02-2_H7N9_depth.txt",
                 reads="106",
                 narrative="low-level signal  (0.79 RPM  ·  297× library-specific RPM differential)",
                 length=L_H7),
        ]
    },
    {
        "title": "Nipah virus  (AY988601, 18,252 nt)  —  BSL-4 infectious clone signal",
        "color": "#7c3aed",
        "bg":    "#f5f3ff",
        "panels": [
            dict(platform="MGISEQ  WIV07-2 (SRR11092059)",
                 depthfile="WIV07-2_Nipah_depth.txt",
                 reads="683",
                 narrative="genuine signal (HDV ribozyme + T7 terminator documented by Zhang 2021)",
                 length=L_NiV),
            dict(platform="MGISEQ-2000RS  WIV02-2 (SRR11092063)",
                 depthfile="WIV02-2_Nipah_depth.txt",
                 reads="0",
                 narrative="SAMPLE-SPECIFIC: 0/134,166,390 reads mapped  →  library-specific contaminant (not platform-wide)",
                 length=L_NiV),
        ]
    },
]

# ── Layout: 3 groups × 2 panels + group headers ───────────────────────────────
N_GROUPS = 3
fig = plt.figure(figsize=(16, 22), facecolor='white')

fig.text(0.5, 0.995,
    'Supplemental Figure 3 — Library-stratified read coverage in PRJNA605983 BALF samples (MGISEQ-2000RS)',
    ha='center', va='top', fontsize=12, fontweight='bold', color='#0f172a')
fig.text(0.5, 0.982,
    'WIV07-2 (SRR11092059) vs WIV02-2 (SRR11092063)  ·  both MGISEQ-2000RS  ·  BWA-MEM alignments verified 10 July 2026  ·  Vermeer & Louwen 2026',
    ha='center', va='top', fontsize=9, color='#475569')

hs = gridspec.GridSpec(
    8, 1, figure=fig,
    height_ratios=[1, 1, 0.18, 1, 1, 0.18, 1, 1],
    hspace=0.0,
    top=0.935, bottom=0.04, left=0.09, right=0.97
)

row_map = [0, 1, 3, 4, 6, 7]
panel_list = [(g, p) for g in GROUPS for p in g["panels"]]

for idx, ((group, panel), row) in enumerate(zip(panel_list, row_map)):
    ax = fig.add_subplot(hs[row])
    color  = group["color"]
    bg     = group["bg"]
    length = panel["length"]

    d = load_depth(os.path.join(RES, panel["depthfile"]), length)
    d_cap, ymax = cap99(d)

    cov_pos = int((d > 0).sum())
    breadth = cov_pos / length * 100
    mean_d  = d.mean()

    pos = np.arange(length)
    ax.fill_between(pos, d_cap, alpha=0.85, color=color, zorder=2)
    ax.set_xlim(0, length)
    ax.set_ylim(0, max(ymax * 1.35, 1))
    ax.set_facecolor(bg)
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(labelsize=7.5)
    ax.set_xticklabels([])

    is_first = (idx % 2 == 0)

    if is_first:
        ax.text(0.0, 1.04, group["title"],
                transform=ax.transAxes, fontsize=9.5, fontweight='bold',
                color=color, va='bottom', ha='left', clip_on=False,
                bbox=dict(boxstyle='round,pad=0.25', facecolor='white',
                          edgecolor=color, linewidth=1.2, alpha=0.97))

    plat_bg = '#1e3a5f' if 'WIV07' in panel["platform"] else '#2d5016'
    ax.text(0.003, 0.97, panel["platform"],
            transform=ax.transAxes, fontsize=8, fontweight='bold',
            color='white', va='top', ha='left',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=plat_bg,
                      edgecolor='none', alpha=0.88))

    stats_text = (f"{panel['reads']} reads  ·  {breadth:.1f}% breadth  ·  "
                  f"{mean_d:.2f}× depth  →  {panel['narrative']}")
    ax.text(0.997, 0.97, stats_text,
            transform=ax.transAxes, fontsize=7.2, color='#1e293b',
            va='top', ha='right',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='white',
                      edgecolor='#e2e8f0', linewidth=0.8, alpha=0.92))

    ax.set_ylabel('Depth (×)', fontsize=7.5, color='#64748b', labelpad=3)

    if not is_first:
        ax.spines['top'].set_visible(True)
        ax.spines['top'].set_linewidth(0.6)
        ax.spines['top'].set_color('#cbd5e1')
        ax.spines['top'].set_linestyle('--')

last_ax = fig.get_axes()[-1]
last_ax.set_xticklabels([f'{int(x):,}' for x in last_ax.get_xticks()],
                         fontsize=7.5)
last_ax.set_xlabel('Genomic position (nt)', fontsize=9, color='#475569')

legend_elements = [
    mpatches.Patch(facecolor='#1e3a5f', label='MGISEQ-2000RS  —  WIV07-2 (SRR11092059)  [high H7N9/Nipah library]'),
    mpatches.Patch(facecolor='#2d5016', label='MGISEQ-2000RS  —  WIV02-2 (SRR11092063)  [low H7N9, Nipah-absent library]'),
]
fig.legend(handles=legend_elements, loc='lower center', ncol=2,
           fontsize=8, frameon=True, framealpha=0.95,
           edgecolor='#cbd5e1', bbox_to_anchor=(0.5, 0.012))

outpath = os.path.join(OUT, "Suppl_Fig3_combined_library_stratified.png")
fig.savefig(outpath, dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(f"Saved: {outpath}")
