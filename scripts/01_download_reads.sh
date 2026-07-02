#!/bin/bash
# Download raw reads from NCBI SRA (PRJNA605983)
# Requires: SRA Toolkit (fasterq-dump)
# Accessions: WIV05 (SRR11092057, SRR11092061 — MGISEQ-2000)
#             WIV06 (SRR11092059 — MiSeq, platform control)
#             WIV07-2 (SRR11092056 — MGISEQ-2000)

set -e

OUTDIR="reads"
mkdir -p "$OUTDIR"

ACCESSIONS=(
    "SRR11092057"   # WIV05  — MGISEQ-2000
    "SRR11092061"   # WIV05  — MGISEQ-2000 (replicate)
    "SRR11092059"   # WIV06  — MiSeq (platform control)
    "SRR11092056"   # WIV07-2 — MGISEQ-2000
)

for ACC in "${ACCESSIONS[@]}"; do
    echo "Downloading $ACC..."
    fasterq-dump "$ACC" --outdir "$OUTDIR" --split-files --threads 8
    echo "$ACC done."
done

echo "All reads downloaded to $OUTDIR/"
