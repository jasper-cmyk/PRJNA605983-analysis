#!/usr/bin/env python3
"""
Supplemental Figures 3 & 4 — Vermeer & Louwen 2026
Reads real samtools depth files for all 5 HiSeq BALF samples.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import os

RES = "/home/jasper/wuhan-analysis/results"
OUT = "/home/jasper/wuhan-analysis/results/figures"
os.makedirs(OUT, exist_ok=True)

# ── Genome lengths ─────────────────────────────────────────────────────────────
L_H7  = 1683
L_NiV = 18252
L_COV = 29903

# ── Samples (HiSeq) ───────────────────────────────────────────────────────────
SAMPLES = [
    ("WIV02-2", "SRR11092063", "#1d4ed8"),
    ("WIV04-2", "SRR11092062", "#7c3aed"),
    ("WIV05",   "SRR11092061", "#dc2626"),
    ("WIV06-2", "SRR11092060", "#059669"),
    ("WIV07-2", "SRR11092059", "#d97706"),
]

def load_depth(path, length):
    d = np.zeros(length + 1)
    if not os.path.exists(path):
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
    """Cap at 99th percentile for readable y-axis."""
    p99 = np.percentile(arr[arr > 0], 99) if (arr > 0).any() else 1
    return np.minimum(arr, p99), p99

# ══════════════════════════════════════════════════════════════════════════════
# SUPPLEMENTAL FIGURE 4 — H7N9 in all 5 deep-sequenced samples
# ══════════════════════════════════════════════════════════════════════════════
fig4, axes = plt.subplots(5, 1, figsize=(14, 14),
                           facecolor='white', sharex=True)
fig4.suptitle(
    'Supplemental Figure 4 — H7N9 HA (KC853766) read depth\n'
    'across all five deep-sequenced BALF samples (PRJNA605983)',
    fontsize=12, fontweight='bold', y=0.98, color='#0f172a')

for ax, (label, srr, col) in zip(axes, SAMPLES):
    depth_file = os.path.join(RES, f"{label}_H7N9_depth.txt")
    d = load_depth(depth_file, L_H7)
    d_cap, ymax = cap99(d)
    pos = np.arange(len(d))

    ax.fill_between(pos, d_cap, alpha=0.85, color=col, zorder=2)
    ax.set_xlim(0, L_H7)
    ax.set_ylim(0, max(ymax * 1.15, 1))
    ax.set_facecolor('#fef2f2')
    ax.set_ylabel('Depth (×)', fontsize=8, color='#475569')
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(labelsize=7.5)

    total = int(d.sum())
    mapped = int((d > 0).sum())
    breadth = mapped / L_H7 * 100
    mean_d = d.mean()

    ax.text(0.01, 0.92, f'{label}  ({srr})',
            transform=ax.transAxes, fontsize=9, fontweight='bold',
            color=col, va='top')
    ax.text(0.99, 0.92,
            f'mean {mean_d:.1f}×  |  breadth {breadth:.1f}%',
            transform=ax.transAxes, fontsize=8, color='#475569',
            va='top', ha='right')

axes[-1].set_xlabel('H7N9 HA genomic position (nt)', fontsize=9, color='#475569')
fig4.tight_layout(rect=[0, 0, 1, 0.96])
out4 = os.path.join(OUT, "Suppl_Fig4_H7N9_all_samples.png")
fig4.savefig(out4, dpi=300, bbox_inches='tight')
plt.close(fig4)
print(f"Saved: {out4}")

# ══════════════════════════════════════════════════════════════════════════════
# SUPPLEMENTAL FIGURE 3b — Nipah in all 5 deep-sequenced samples
# ══════════════════════════════════════════════════════════════════════════════
fig3b, axes3b = plt.subplots(5, 1, figsize=(14, 14),
                              facecolor='white', sharex=True)
fig3b.suptitle(
    'Nipah virus (AY988601) read depth\n'
    'across all five deep-sequenced BALF samples (PRJNA605983)',
    fontsize=12, fontweight='bold', y=0.98, color='#0f172a')

for ax, (label, srr, col) in zip(axes3b, SAMPLES):
    depth_file = os.path.join(RES, f"{label}_Nipah_depth.txt")
    d = load_depth(depth_file, L_NiV)
    d_cap, ymax = cap99(d)
    pos = np.arange(len(d))

    ax.fill_between(pos, d_cap, alpha=0.85, color='#7c3aed', zorder=2)
    ax.set_xlim(0, L_NiV)
    ax.set_ylim(0, max(ymax * 1.15, 1))
    ax.set_facecolor('#f5f3ff')
    ax.set_ylabel('Depth (×)', fontsize=8, color='#475569')
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(labelsize=7.5)

    total = int(d.sum())
    mapped = int((d > 0).sum())
    breadth = mapped / L_NiV * 100
    mean_d = d.mean()

    ax.text(0.01, 0.92, f'{label}  ({srr})',
            transform=ax.transAxes, fontsize=9, fontweight='bold',
            color=col, va='top')
    ax.text(0.99, 0.92,
            f'mean {mean_d:.3f}×  |  breadth {breadth:.1f}%',
            transform=ax.transAxes, fontsize=8, color='#475569',
            va='top', ha='right')

axes3b[-1].set_xlabel('Nipah genomic position (nt)', fontsize=9, color='#475569')
fig3b.tight_layout(rect=[0, 0, 1, 0.96])
out3b = os.path.join(OUT, "Suppl_Fig3b_Nipah_all_samples.png")
fig3b.savefig(out3b, dpi=300, bbox_inches='tight')
plt.close(fig3b)
print(f"Saved: {out3b}")

# ══════════════════════════════════════════════════════════════════════════════
# SUPPLEMENTAL FIGURE 3c — SARS-CoV-2 in all 5 deep-sequenced samples
# ══════════════════════════════════════════════════════════════════════════════
fig3c, axes3c = plt.subplots(5, 1, figsize=(14, 14),
                              facecolor='white', sharex=True)
fig3c.suptitle(
    'SARS-CoV-2 (NC_045512.2) read depth\n'
    'across all five deep-sequenced BALF samples (PRJNA605983)',
    fontsize=12, fontweight='bold', y=0.98, color='#0f172a')

for ax, (label, srr, col) in zip(axes3c, SAMPLES):
    depth_file = os.path.join(RES, f"{label}_SARS2_depth.txt")
    d = load_depth(depth_file, L_COV)
    d_cap, ymax = cap99(d)
    pos = np.arange(len(d))

    ax.fill_between(pos, d_cap, alpha=0.85, color='#059669', zorder=2)
    ax.set_xlim(0, L_COV)
    ax.set_ylim(0, max(ymax * 1.15, 1))
    ax.set_facecolor('#ecfdf5')
    ax.set_ylabel('Depth (×)', fontsize=8, color='#475569')
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(labelsize=7.5)

    total = int(d.sum())
    mapped = int((d > 0).sum())
    breadth = mapped / L_COV * 100
    mean_d = d.mean()

    ax.text(0.01, 0.92, f'{label}  ({srr})',
            transform=ax.transAxes, fontsize=9, fontweight='bold',
            color=col, va='top')
    ax.text(0.99, 0.92,
            f'mean {mean_d:.1f}×  |  breadth {breadth:.1f}%',
            transform=ax.transAxes, fontsize=8, color='#475569',
            va='top', ha='right')

axes3c[-1].set_xlabel('SARS-CoV-2 genomic position (nt)', fontsize=9, color='#475569')
fig3c.tight_layout(rect=[0, 0, 1, 0.96])
out3c = os.path.join(OUT, "Suppl_Fig3c_SARS2_all_samples.png")
fig3c.savefig(out3c, dpi=300, bbox_inches='tight')
plt.close(fig3c)
print(f"Saved: {out3c}")

print("\nAlle figuren gegenereerd in:", OUT)
