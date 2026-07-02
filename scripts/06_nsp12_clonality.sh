#!/bin/bash
# nsp12 (RdRp) clonality analysis across 111 PRJCA002163 assemblies
# Extracts nsp12 region (nt 13025-16236 of NC_045512.2) and computes
# pairwise nucleotide identity to the reference.
# Requires: samtools faidx, MAFFT, Python 3

set -e

ASSEMBLIES="data/sequences_PRJCA002123_assemblies.fasta"
REF_NSP12="reference/nsp12_NC045512.fasta"   # nt 13025-16236, 3212 nt
OUTDIR="results"

mkdir -p "$OUTDIR"

# Extract nsp12 region from each assembly via MAFFT pairwise
echo "Aligning all assemblies to nsp12 reference..."
mafft --auto --addfragments "$ASSEMBLIES" --thread 8 "$REF_NSP12" \
    > "${OUTDIR}/nsp12_aligned.fasta"

# Compute pairwise identity to NC_045512.2
python3 - <<'EOF'
from Bio import SeqIO
import sys

records = list(SeqIO.parse("results/nsp12_aligned.fasta", "fasta"))
ref = next(r for r in records if "NC_045512" in r.id)
ref_seq = str(ref.seq).upper()

results = []
for r in records:
    if "NC_045512" in r.id:
        continue
    seq = str(r.seq).upper()
    matches = sum(a == b for a, b in zip(ref_seq, seq)
                  if a != '-' and b != '-')
    total = sum(1 for a, b in zip(ref_seq, seq)
                if a != '-' and b != '-')
    pct = 100 * matches / total if total > 0 else 0
    mismatches = total - matches
    results.append((r.id, pct, mismatches, total))

results.sort(key=lambda x: -x[1])

print(f"{'Assembly':<40} {'Identity%':>10} {'Mismatches':>12} {'Compared_nt':>12}")
print("-" * 80)
for name, pct, mm, tot in results:
    print(f"{name:<40} {pct:>10.4f} {mm:>12} {tot:>12}")

perfect = sum(1 for _, pct, _, _ in results if pct == 100.0)
print(f"\nTotal assemblies: {len(results)}")
print(f"100.000% identical to NC_045512.2: {perfect} ({100*perfect/len(results):.1f}%)")
print(f"Mean identity: {sum(p for _,p,_,_ in results)/len(results):.4f}%")
EOF

echo "nsp12 clonality analysis complete."
