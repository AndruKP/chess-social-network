import graph_tool.all as gt
import argparse
import pickle

parser = argparse.ArgumentParser(description="Calculate a graph visualization of a graph in GraphML format.")
parser.add_argument("graphml_file", help="Path to the input GraphML file")
parser.add_argument("--nested", action='store_true', help="use `nested`")

args = parser.parse_args()

print('Start')
g = gt.load_graph(args.graphml_file)
print('The graph is loaded')

print('extracting the largest component')
g = gt.extract_largest_component(g, directed=False)
print('The largest component is extracted')

#good for 2013
if args.nested:
    print('minimizing nested blockmodel description length')    
    state = gt.minimize_nested_blockmodel_dl(g,
                                    #   state_args={'B':4},
                                    #   multilevel_mcmc_args=dict(B_max=4, niter=1)
                                      )
    print('finished minimizing nested blockmodel description length')
else:
    print('minimizing blockmodel description length')    
    state = gt.minimize_blockmodel_dl(g,
                                      state_args={'B':4},
                                      multilevel_mcmc_args=dict(B_max=4, niter=1)
                                      )
    print('finished minimizing blockmodel description length')

#good for 2013
print('calculating layout')
if args.nested:
    pos2 = gt.sfdp_layout(g, groups=state.levels[0].b, gamma=.02) 
    g.vp['block'] = state.levels[0].get_blocks()
else:
    pos2 = gt.sfdp_layout(g, groups=state.b, gamma=.02) 
    g.vp['block'] = state.get_blocks()
print('layout is calculated')

g.vp['pos'] = pos2

with open(f'{args.graphml_file.replace('xml','gt')}{'_nested' if args.nested else ''}.pickle', 'wb') as handle:
    pickle.dump(state, handle)

g.save(f'{args.graphml_file.replace('xml','gt')}{'_nested.gt' if args.nested else ''}')
