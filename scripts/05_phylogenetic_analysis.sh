#!/bin/bash
# Phylogenetic analysis of PRJCA002163 assemblies (Zhengli et al.)
# plus outgroups ZC45, ZXC21 and RatG13
# Requires: MAFFT, IQ-TREE2

set -e

INPUT="data/sequences_PRJCA002163_plus_outgroups.fasta"
ALIGNED="results/tree_aligned.fasta"
TREE_PREFIX="results/phylo_tree"

# Step 1: Multiple sequence alignment
echo "=== MAFFT alignment ==="
mafft --auto --thread 8 "$INPUT" > "$ALIGNED"

# Step 2: IQ-TREE2 phylogenetic inference
# Model: GTR+G (general time reversible + gamma rate variation)
# 1000 ultrafast bootstrap replicates
# Outgroup: ZC45 + ZXC21 clade
echo "=== IQ-TREE2 ==="
iqtree2 -s "$ALIGNED" \
    -m GTR+G \
    -B 1000 \
    -nt AUTO \
    --prefix "$TREE_PREFIX" \
    -o "ZC45,ZXC21"

echo "Tree written to ${TREE_PREFIX}.treefile"
echo "Run visualize_tree.py to generate figure."
