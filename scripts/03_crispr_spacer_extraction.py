#!/usr/bin/env python3
"""Extract gRNA spacers from SpCas9 reads by finding scaffold and taking 20nt upstream."""

import subprocess
import sys
from collections import Counter

SCAFFOLD = "GTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGT"
SCAFFOLD_RC = "ACGGACTAGCCTTATTTTAACTTGCTATTTCTAGCTCTAAAAC"
SPACER_LEN = 20
MIN_SCAFFOLD_MATCH = 20  # partial match threshold

def rc(seq):
    comp = str.maketrans("ACGTacgt", "TGCAtgca")
    return seq.translate(comp)[::-1]

def find_spacer(seq, scaffold, min_match=MIN_SCAFFOLD_MATCH):
    """Find scaffold in seq and return 20nt upstream, or None."""
    for offset in range(len(SCAFFOLD) - min_match + 1):
        fragment = SCAFFOLD[offset:offset + min_match]
        pos = seq.find(fragment)
        if pos >= 0:
            spacer_start = pos - offset - SPACER_LEN
            if spacer_start >= 0:
                return seq[spacer_start:spacer_start + SPACER_LEN], offset
    return None, None

def extract_from_bam(bam_path):
    spacers = []
    cmd = ["samtools", "view", bam_path]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)

    count = 0
    for line in proc.stdout:
        fields = line.split("\t")
        if len(fields) < 10:
            continue
        seq = fields[9]

        # Try forward
        spacer, _ = find_spacer(seq, SCAFFOLD)
        if spacer and len(spacer) == SPACER_LEN and all(c in "ACGT" for c in spacer):
            spacers.append(spacer)
            count += 1
            continue

        # Try reverse complement
        seq_rc = rc(seq)
        spacer, _ = find_spacer(seq_rc, SCAFFOLD)
        if spacer and len(spacer) == SPACER_LEN and all(c in "ACGT" for c in spacer):
            spacers.append(spacer)
            count += 1

    proc.wait()
    return spacers

def main():
    bam = sys.argv[1] if len(sys.argv) > 1 else "results/WIV05_cas9solo.bam"
    print(f"Extracting spacers from {bam}...", flush=True)

    spacers = extract_from_bam(bam)
    print(f"Found {len(spacers)} spacer-containing reads", flush=True)

    if not spacers:
        print("No spacers found. Check scaffold sequence or BAM content.")
        return

    counter = Counter(spacers)
    print(f"Unique spacers: {len(counter)}\n")

    # Write FASTA for MAFFT
    out_fasta = "results/spacers.fa"
    with open(out_fasta, "w") as f:
        for i, (spacer, count) in enumerate(counter.most_common(), 1):
            f.write(f">spacer_{i:04d}_n{count}\n{spacer}\n")

    print(f"Top 20 spacers:")
    print(f"{'Rank':<6} {'Count':>8}  {'Spacer'}")
    print("-" * 50)
    for i, (spacer, count) in enumerate(counter.most_common(20), 1):
        print(f"{i:<6} {count:>8}  {spacer}")

    print(f"\nFASTA geschreven naar {out_fasta}")

if __name__ == "__main__":
    main()
