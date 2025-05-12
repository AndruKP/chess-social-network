import graph_tool.all as gt
import matplotlib.pyplot as plt
import argparse
import os
import datetime

parser = argparse.ArgumentParser(description="Create a statistics log of a graph in GraphML format.")
parser.add_argument("graphml_file", help="Path to the input GraphML file")
parser.add_argument("output_directory", help="Path to the output directory, where report will be created")

args = parser.parse_args()

if not os.path.exists(args.output_directory):
    os.makedirs(args.output_directory)

g = gt.load_graph(args.graphml_file)

degrees = g.degree_property_map("total")
min_degree = min(degrees)
max_degree = max(degrees)

indegree = g.degree_property_map("in")
min_indegree = min(indegree)
max_indegree = max(indegree)

outdegree = g.degree_property_map("out")
min_outdegree = min(outdegree)
max_outdegree = max(outdegree)

mean_degree = 2 * g.num_edges() / g.num_vertices()
mean_indegree = g.num_edges() / g.num_vertices()
density = mean_degree / (g.num_vertices() - 1)

global_clustering_coefficient = gt.global_clustering(g)
reciprocity = gt.edge_reciprocity(g)

with open(f'{args.output_directory}/log.txt', 'w') as f:
    print(f'Graph located at: {args.graphml_file}',file=f)
    print(f'starting time: {datetime.time()}',file=f)
    print('==========================',file=f)
    print(f'Number of vertices: {g.num_vertices()}', file=f)
    print(f'Number of edges: {g.num_edges()}', file=f)
    print(f'Min degree: {min_degree}', file=f)
    print(f'Max degree: {max_degree}', file=f)
    print(f'Mean degree: {mean_degree}', file=f)
    print(f'Min indegree: {min_indegree}', file=f)
    print(f'Max indegree: {max_indegree}', file=f)
    print(f'Min outdegree: {min_outdegree}', file=f)
    print(f'Max outdegree: {max_outdegree}', file=f)
    print(f'Mean indegree = Mean outdegree: {mean_indegree}', file=f)
    print(f'Density: {density}', file=f)
    print(f'Global clustering coefficient: {global_clustering_coefficient}', file=f)
    print(f'Reciprocity: {reciprocity}', file=f)
    print('==========================', file=f)
    print(f'ending time: {datetime.time()}',file=f)

    print('Statistics log created successfully.')
    print(f'Output file: {args.output_directory}.txt')

# The following code is for plotting the degree distribution of the graph
degree_distribution = g.degree_property_map("total")
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(degree_distribution.a, bins=50, color='blue', alpha=0.7)
ax.set_title('Degree Distribution')
ax.set_xlabel('Degree')
ax.set_ylabel('Frequency')
ax.grid()
fig.savefig(f'{args.output_directory}/degree_distribution.png')
plt.close(fig)

# The following code is for plotting the indegree distribution of the graph
indegree_distribution = g.degree_property_map("in")
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(indegree_distribution.a, bins=50, color='green', alpha=0.7)
ax.set_title('Indegree Distribution')
ax.set_xlabel('Indegree')
ax.set_ylabel('Frequency')
ax.grid()
fig.savefig(f'{args.output_directory}/indegree_distribution.png')
plt.close(fig)

# The following code is for plotting the outdegree distribution of the graph
outdegree_distribution = g.degree_property_map("out")
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(outdegree_distribution.a, bins=50, color='red', alpha=0.7)
ax.set_title('Outdegree Distribution')
ax.set_xlabel('Outdegree')
ax.set_ylabel('Frequency')
ax.grid()
fig.savefig(f'{args.output_directory}/outdegree_distribution.png')
plt.close(fig)

# The following code is for plotting the clustering coefficient distribution of the graph
clustering_coefficient_distribution = gt.local_clustering(g)
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(clustering_coefficient_distribution.a, bins=50, color='purple', alpha=0.7)
ax.set_title('Clustering Coefficient Distribution')
ax.set_xlabel('Clustering Coefficient')
ax.set_ylabel('Frequency')
ax.grid()
fig.savefig(f'{args.output_directory}/clustering_coefficient_distribution.png')
plt.close(fig)

# The following code is for plotting the betweenness centrality distribution of the graph
betweenness_centrality = gt.betweenness(g)
vertex_betweenness = betweenness_centrality[0]
edge_betweenness = betweenness_centrality[1]
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(vertex_betweenness.a, bins=50, color='cyan', alpha=0.7)
ax.set_title('Vertex Betweenness Centrality Distribution')
ax.set_xlabel('Betweenness Centrality')
ax.set_ylabel('Frequency')
ax.grid()
fig.savefig(f'{args.output_directory}/vertex_betweenness_centrality_distribution.png')
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(edge_betweenness.a, bins=50, color='cyan', alpha=0.7)
ax.set_title('Edge Betweenness Centrality Distribution')
ax.set_xlabel('Betweenness Centrality')
ax.set_ylabel('Frequency')
ax.grid()
fig.savefig(f'{args.output_directory}/edge_betweenness_centrality_distribution.png')
plt.close(fig)

# The following code is for plotting the closeness centrality distribution of the graph
closeness_centrality = gt.closeness(g)
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(closeness_centrality.a, bins=50, color='magenta', alpha=0.7)
ax.set_title('Closeness Centrality Distribution')
ax.set_xlabel('Closeness Centrality')
ax.set_ylabel('Frequency')
ax.grid()
fig.savefig(f'{args.output_directory}/closeness_centrality_distribution.png')
plt.close(fig)

# The following code is for plotting the eigenvector centrality distribution of the graph
eigenvector_centrality = gt.eigenvector(g)[1]
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(eigenvector_centrality.a, bins=50, color='brown', alpha=0.7)
ax.set_title('Eigenvector Centrality Distribution')
ax.set_xlabel('Eigenvector Centrality')
ax.set_ylabel('Frequency')
ax.grid()
fig.savefig(f'{args.output_directory}/eigenvector_centrality_distribution.png')
plt.close(fig)

# The following code is for plotting the PageRank centrality distribution of the graph
pagerank_centrality = gt.pagerank(g)
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(pagerank_centrality.a, bins=50, color='pink', alpha=0.7)
ax.set_title('PageRank Centrality Distribution')
ax.set_xlabel('PageRank Centrality')
ax.set_ylabel('Frequency')
ax.grid()
fig.savefig(f'{args.output_directory}/pagerank_centrality_distribution.png')
plt.close(fig)

