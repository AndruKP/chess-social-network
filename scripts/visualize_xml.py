import graph_tool.all as gt
import argparse

parser = argparse.ArgumentParser(description="Create a visualisation of a graph in GraphML format.")
parser.add_argument("graphml_file", help="Path to the input GraphML file")
parser.add_argument("output_file", help="Path to the output pdf file")

args = parser.parse_args()

g = gt.load_graph(args.graphml_file)
pos = gt.sfdp_layout(g)

gt.graph_draw(g, pos, output=args.output_file, output_size = (2000, 2000))
