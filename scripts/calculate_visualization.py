import graph_tool.all as gt
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description="Calculate a graph visualization of a graph in GraphML format.")
parser.add_argument("graphml_file", help="Path to the input GraphML file")
parser.add_argument("output_file", help="Path to the output gt file")

args = parser.parse_args()

print('Start')
g = gt.load_graph(args.graphml_file)
print('The graph is loaded')

print('extracting the largest component')
g = gt.extract_largest_component(g, directed=False)
print('The largest component is extracted')

#good for 2013
print('minimizing blockmodel description length')
state = gt.minimize_blockmodel_dl(g,
                                    state_args={'B':4},
                                    multilevel_mcmc_args=dict(B_max=4, niter=1)
                                    )
print('finished minimizing blockmodel description length')

#good for 2013
print('calculating layout')
pos2 = gt.sfdp_layout(g,
                       groups=state.b,
                         gamma=.02) 
print('layout is calculated')

g.vp['pos'] = pos2
g.save(args.graphml_file.replace('xml','gt'))
