#!/bin/bash
# Multi-reference alignment for PRJNA605983 samples
# References: SARS-CoV-2 (NC_045512.2), SpyCas9 (KM099231.1),
#             RBD-Fc junction (CN111333704B SEQ5), H7N9 HA, Nipah NP
# Requires: BWA-MEM, samtools

set -e

REF="reference/multi_ref_combined.fasta"
READS_DIR="reads"
OUT_DIR="results"

mkdir -p "$OUT_DIR"

# Build BWA index (run once)
if [ ! -f "${REF}.bwt" ]; then
    echo "Building BWA index..."
    bwa index "$REF"
fi

declare -A SAMPLES=(
    ["WIV05"]="SRR11092057"
    ["WIV05b"]="SRR11092061"
    ["WIV06_MiSeq"]="SRR11092059"
    ["WIV07-2"]="SRR11092056"
)

for LABEL in "${!SAMPLES[@]}"; do
    ACC="${SAMPLES[$LABEL]}"
    R1="${READS_DIR}/${ACC}_1.fastq"
    R2="${READS_DIR}/${ACC}_2.fastq"
    OUT_BAM="${OUT_DIR}/${LABEL}.bam"

    echo "=== Aligning $LABEL ($ACC) ==="
    bwa mem -t 8 "$REF" "$R1" "$R2" \
        2>"${OUT_DIR}/${LABEL}_bwa.log" \
        | samtools sort -@ 4 -o "$OUT_BAM"
    samtools index "$OUT_BAM"

    echo "--- flagstat ---"
    samtools flagstat "$OUT_BAM"

    echo "--- reads per reference ---"
    samtools idxstats "$OUT_BAM"
    echo ""
done

echo "Alignments complete. BAM files in $OUT_DIR/"
