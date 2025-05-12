import graph_tool.all as gt
import matplotlib.pyplot as plt
import argparse
import os
import datetime
import numpy as np
from scipy.stats import t


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

median_degree = np.median(degrees)
median_indegree = np.median(indegree)
median_outdegree = np.median(outdegree)

global_clustering_coefficient = gt.global_clustering(g)
reciprocity = gt.edge_reciprocity(g)

print('extracting the largest component')
ge = gt.extract_largest_component(g, directed=False)
print('The largest component is extracted')

#good for 2013
print('minimizing blockmodel description length')    
state = gt.minimize_blockmodel_dl(ge,
                                    state_args={'B':4},
                                    multilevel_mcmc_args=dict(B_max=4, niter=1)
                                    )
print('finished minimizing blockmodel description length')


print('calculating layout')
pos2 = gt.sfdp_layout(ge, groups=state.b, gamma=.02) 
ge.vp['block'] = state.get_blocks()
print('layout is calculated')

block_assortativity = gt.assortativity(ge, ge.vp['block'])

degree_assortativity = gt.scalar_assortativity(g, "total")

with open(f'{args.output_directory}/log.txt', 'w') as f:
    print(f'Graph located at: {args.graphml_file}',file=f)
    print(f'starting time: {datetime.time()}',file=f)
    print('==========================',file=f)
    print(f'Number of vertices: {g.num_vertices()}', file=f)
    print(f'Number of edges: {g.num_edges()}', file=f)
    print(f'Min degree: {min_degree}', file=f)
    print(f'Max degree: {max_degree}', file=f)
    print(f'Mean degree: {mean_degree}', file=f)
    print(f'Median degree: {median_degree}', file=f)
    print(f'Min indegree: {min_indegree}', file=f)
    print(f'Max indegree: {max_indegree}', file=f)
    print(f'Min outdegree: {min_outdegree}', file=f)
    print(f'Max outdegree: {max_outdegree}', file=f)
    print(f'Mean indegree = Mean outdegree: {mean_indegree}', file=f)
    print(f'Median indegree: {median_indegree}', file=f)
    print(f'Median outdegree: {median_outdegree}', file=f)
    print(f'Density: {density}', file=f)
    print(f'Global clustering coefficient: {global_clustering_coefficient}', file=f)
    print(f'Reciprocity: {reciprocity}', file=f)
    print(f"Assortativity by communities (blocks): {block_assortativity[0]} ± {block_assortativity[1]}", file=f)
    print(f"Assortativity by vertice degrees: {degree_assortativity[0]} ± {degree_assortativity[1]}", file=f)
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

def power_law_linreg(vals, counts):
    # Gets an array of points, filters empty bins out
    # Then returns a power-law curve to approximate the distribution
    fvals = vals[counts > 0]
    fcounts = counts[counts > 0]
    lvals = np.log(fvals)
    lcounts = np.log(fcounts)

    # Perform linear regression
    a, b = np.polyfit(lvals, lcounts, deg=1, w=fcounts)  # a is the slope, b is the intercept

    # Calculate residuals
    predicted = a * lvals + b
    residuals = lcounts - predicted

    # Calculate standard error of the slope
    n = len(lvals)  # Number of data points
    variance = np.sum(residuals**2) / (n - 2)  # Variance of residuals
    x_variance = np.sum((lvals - np.mean(lvals))**2)  # Variance of x (log values)
    slope_std_error = np.sqrt(variance / x_variance)  # Standard error of the slope

    # Calculate t-statistic for the slope
    t_stat = a / slope_std_error

    # Calculate p-value (two-tailed)
    p_value = 2 * (1 - t.cdf(abs(t_stat), df=n - 2))

    # Return slope, intercept, and p-value
    return (np.exp(b), a, p_value)


def do_plot(values, ax, color='blue'):
    filtered_vals = values[values > 0]
    #evenly spaced out bins on logarithmic scale
    bin_locs = np.logspace(np.log10(min(filtered_vals)),np.log10(max(filtered_vals)), num=50)
    #the histogram returns the counts in every bin
    hist_result = ax.hist(values, bins=bin_locs, color=color, alpha=0.7)
    counts = hist_result[0]
    #draw the power law curve
    coef1, coef2, pvalue = power_law_linreg(bin_locs[:-1], counts)
    coef = (coef1, coef2)

    ax.plot(bin_locs, coef[0] * bin_locs ** coef[1], 'r')
    print(pvalue)
    return pvalue


# Plot degree distribution
degree_distribution = g.degree_property_map("total")
fig, ax = plt.subplots(figsize=(10, 6))
p = do_plot(degree_distribution.a, ax, color='blue')
ax.set_title(f'Degree Distribution pvalue = {p}')
ax.set_xlabel('Degree')
ax.set_ylabel('Frequency')
ax.grid()
ax.set_xscale('log')
ax.set_yscale('log')
fig.savefig(f'{args.output_directory}/degree_distribution_loglog.png')
plt.close(fig)

# Plot indegree distribution
indegree_distribution = g.degree_property_map("in")
fig, ax = plt.subplots(figsize=(10, 6))
do_plot(indegree_distribution.a, ax, color='green')
ax.set_title(f'Indegree Distribution')
ax.set_xlabel('Indegree')
ax.set_ylabel('Frequency')
ax.grid()
ax.set_xscale('log')
ax.set_yscale('log')
fig.savefig(f'{args.output_directory}/indegree_distribution_loglog.png')
plt.close(fig)

# Plot outdegree distribution
outdegree_distribution = g.degree_property_map("out")
fig, ax = plt.subplots(figsize=(10, 6))
do_plot(outdegree_distribution.a, ax, color='red')
ax.set_title(f'Outdegree Distribution')
ax.set_xlabel('Outdegree')
ax.set_ylabel('Frequency')
ax.grid()
ax.set_xscale('log')
ax.set_yscale('log')
fig.savefig(f'{args.output_directory}/outdegree_distribution_loglog.png')
plt.close(fig)

# Plot PageRank centrality distribution
pagerank_centrality = gt.pagerank(g)
fig, ax = plt.subplots(figsize=(10, 6))
do_plot(pagerank_centrality.a, ax, color='pink')
ax.set_title(f'PageRank Centrality Distribution')
ax.set_xlabel('PageRank Centrality')
ax.set_ylabel('Frequency')
ax.grid()
ax.set_xscale('log')
ax.set_yscale('log')
fig.savefig(f'{args.output_directory}/pagerank_centrality_distribution_loglog.png')
plt.close(fig)
