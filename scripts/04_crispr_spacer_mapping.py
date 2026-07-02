#!/usr/bin/env python3
"""Map gRNA spacers to local reference sequences (exact + up to 3 mismatches)."""

import os
import glob

SPACERS = [
    ("spacer_1_n12", "GGACTGGGGCAGATGCTCAG"),
    ("spacer_2_n10", "TCGGCTGTTCGGCGCCAGGC"),
    ("spacer_3_n4",  "CTCTAGCTTCGCCATGTACA"),
    ("spacer_4_n2",  "TCAGTCCCACCAATCCATGG"),
    ("spacer_5_n2",  "AGCCCTTTCTCCAAGGGGCC"),
    ("spacer_6_n2",  "ACTGGGGCAGATGCTCAGAG"),
]

REF_DIR = "reference"
MAX_MM = 3

def rc(seq):
    comp = str.maketrans("ACGTacgtN", "TGCAtgcaN")
    return seq.translate(comp)[::-1]

def mismatches(a, b):
    return sum(x != y for x, y in zip(a, b))

def load_fasta(path):
    seqs = {}
    name = None
    buf = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if name:
                    seqs[name] = "".join(buf)
                name = line[1:].split()[0]
                buf = []
            else:
                buf.append(line.upper())
    if name:
        seqs[name] = "".join(buf)
    return seqs

def search_spacer(spacer, seq, seq_name, ref_file, results):
    slen = len(spacer)
    spacer_rc = rc(spacer)
    for strand, query in [("+", spacer), ("-", spacer_rc)]:
        for i in range(len(seq) - slen + 1):
            window = seq[i:i+slen]
            if "N" in window:
                continue
            mm = mismatches(query, window)
            if mm <= MAX_MM:
                results.append({
                    "ref": os.path.basename(ref_file),
                    "seq": seq_name,
                    "pos": i + 1,
                    "strand": strand,
                    "mm": mm,
                    "match": window,
                })

def main():
    ref_files = sorted(glob.glob(f"{REF_DIR}/*.fasta"))
    # Exclude BWA index files (only .fasta without extra extensions)
    ref_files = [f for f in ref_files if f.endswith(".fasta")]

    print(f"Searching {len(SPACERS)} spacers against {len(ref_files)} references (max {MAX_MM} mismatches)\n")

    all_hits = {}
    for sp_name, spacer in SPACERS:
        hits = []
        for ref_file in ref_files:
            try:
                seqs = load_fasta(ref_file)
            except Exception:
                continue
            for seq_name, seq in seqs.items():
                search_spacer(spacer, seq, seq_name, ref_file, hits)
        hits.sort(key=lambda x: x["mm"])
        all_hits[sp_name] = (spacer, hits)

    # Print results
    for sp_name, (spacer, hits) in all_hits.items():
        print(f"{'='*60}")
        print(f"{sp_name}: {spacer}")
        if not hits:
            print("  → Geen treffer in lokale referenties")
        else:
            for h in hits[:10]:
                print(f"  [{h['mm']} mm] {h['strand']} strand | pos {h['pos']:>7} | {h['ref']} ({h['seq'][:40]})")
                if h['mm'] > 0:
                    # Show alignment
                    query = spacer if h['strand'] == '+' else rc(spacer)
                    diffs = "".join("|" if a==b else "X" for a,b in zip(query, h['match']))
                    print(f"          query: {query}")
                    print(f"          match: {h['match']}")
                    print(f"                 {diffs}")
        print()

if __name__ == "__main__":
    main()
