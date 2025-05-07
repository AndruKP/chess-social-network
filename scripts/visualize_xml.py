import graph_tool.all as gt
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description="Create a visualisation of a graph in GraphML format.")
parser.add_argument("graphml_file", help="Path to the input GraphML file")
parser.add_argument("output_file", help="Path to the output pdf file")

args = parser.parse_args()

print('Start')
g = gt.load_graph(args.graphml_file)

print('The graph is loaded')

g = gt.extract_largest_component(g, directed=False)

print('The largest component is extracted')
# pos = gt.sfdp_layout(g)

dprms = dict(#fmt="png",  
            #output_size=9600 9600 # good for 2013            
            #  output_size=(2000, 2000), 
             output=args.output_file)

# gt.graph_draw(g, pos, **dprms)
# st = gt.BlockState(g, B=3)


#good for 2013
# state = gt.minimize_blockmodel_dl(g,
#                                    state_args={'B':4},
#                                      multilevel_mcmc_args=dict(B_max=5)
#                                      )

type_to_color = {
    'C':'red', #Classic 
    'B':'blue', #Bullet
    'Z':'green', #blitZ
    'N':'yellow' #correspoNdence
}

edge_type = g.edge_properties['game type']

edge_color = g.new_edge_property("string")
for e in tqdm(g.edges(), 'Edges colors'):
    try:
        edge_color[e] = type_to_color[edge_type[e]]
    except:
        print(e)



# good for 2013
# vb, eb = gt.betweenness(g)




# state.levels[0].draw(pos=pos, **dprms)


#good for 2013
# pos2 = gt.sfdp_layout(g, groups=state.b, gamma=.02) 
# state.draw(pos=pos2, **dprms,  edge_color=edge_color,ecmap=False,
#             #          vertex_fill_color=gt.prop_to_size(vb, 0, 1, power=.1),
#             # vertex_size=gt.prop_to_size(vb, 3, 12, power=.2), vorder=vb,
#             )
pos2 = gt.random_layout(g)
print('pos is ready')
gt.graph_draw(g,
           pos=pos2,
           edge_color=edge_color,
           edge_pen_width=0.2,
        #    vertex_fill_color=state.b,
        #    vertex_size=gt.prop_to_size(vb, 3, 12, power=.2),
           **dprms
)


# state.draw(**dprms)

# gt.graph_draw(g, pos, output=args.output_file, output_size = (2000, 2000))
