from Bio import Phylo
from io import StringIO  # Importing StringIO from io module

# Defining relationships in Newick format
tree_data = (
    "(Prokaryotic_ancestor, (Archaean_ancestor, Bacterial_ancestor),"
    "(Cyanobacteria, (Methanogens, Proteobacteria)),"
    "(Actinobacteria, (Firmicutes, (Thermophiles, Sulfolobus_Thermophilic_archaea))),"
    "(Primitive_eukaryotic_cells, (Unicellular_eukaryotic_organisms, (Protists, (Simple_algae, (Amoebas, (Ciliates, Flagellates)))))))" 
)

# Parse the tree data
tree = Phylo.read(StringIO(tree_data), "newick")

# Display or draw the tree
Phylo.draw(tree)

