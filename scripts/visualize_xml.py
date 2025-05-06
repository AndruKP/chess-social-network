import graph_tool.all as gt
import argparse

parser = argparse.ArgumentParser(description="Create a visualisation of a graph in GraphML format.")
parser.add_argument("graphml_file", help="Path to the input GraphML file")
parser.add_argument("output_file", help="Path to the output pdf file")

args = parser.parse_args()

g = gt.load_graph(args.graphml_file)

g = gt.extract_largest_component(g, directed=False)
# pos = gt.sfdp_layout(g)

dprms = dict(#fmt="png",  
             output_size=(4800, 4800), 
             output=args.output_file)

# gt.graph_draw(g, pos, **dprms)
state = gt.minimize_blockmodel_dl(g)

vb, eb = gt.betweenness(g)
# state.levels[0].draw(pos=pos, **dprms)

pos2 = gt.sfdp_layout(g, groups=state.b, gamma=.02) 
state.draw(pos=pos2, edge_gradient=[], edge_color="#33333322", **dprms, 
                     vertex_fill_color=gt.prop_to_size(vb, 0, 1, power=.1),
            vertex_size=gt.prop_to_size(vb, 3, 12, power=.2), vorder=vb,)

# state.draw(**dprms)

# gt.graph_draw(g, pos, output=args.output_file, output_size = (2000, 2000))
