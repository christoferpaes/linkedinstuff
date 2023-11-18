import networkx as nx
import matplotlib.pyplot as plt
from Bio import Phylo

tree = Phylo.read("phylo.xml", "phyloxml")
net = Phylo.to_networkx(tree)

# Create a labels dictionary with node names as keys and labels as values
labels = {node: node.name for node in net.nodes() if hasattr(node, 'name')}

# Draw the networkx plot with adjusted node positions for increased space between nodes
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(net, k=1)  # Increase the k value for more space between nodes
nx.draw(net, pos, with_labels=True, labels=labels, node_size=500, node_color='skyblue', font_size=8)
plt.show()
