import graph_tool.all as gt
import argparse
from tqdm import tqdm

def parse_resolution(res_str):
    try:
        width_str, height_str = res_str.lower().split('x')
        width = int(width_str)
        height = int(height_str)
        if width <= 0 or height <= 0:
            raise ValueError
        return width, height
    except ValueError:
        raise argparse.ArgumentTypeError("Resolution must be in the format WIDTHxHEIGHT, e.g., 1920x1080")


parser = argparse.ArgumentParser(description="Render a graph visualization of a graph in gt format.\
Note that you need to calculate and store in gt file graph layout.")
parser.add_argument("gt_file", help="Path to the input GraphML file")
parser.add_argument("output_file", help="Path to the output gt file")
parser.add_argument(
    '--resolution',
    type=parse_resolution,
    default="2000x2000",
    help='Resolution in WIDTHxHEIGHT format, e.g., 1920x1080'
)

args = parser.parse_args()
width, height = args.resolution

g = gt.load_graph(file_name=args.gt_file)

# good for 2013
#print("centrality calculation is started")
# vb, eb = gt.betweenness(g)
#print("centrality calculation is finished")

type_to_color = {
    'C':'red', #Classic 
    'B':'blue', #Bullet
    'Z':'green', #blitZ
    'N':'yellow' #correspoNdence
}

edge_type = g.edge_properties['game type']

edge_color = g.new_edge_property("string")
for e in tqdm(g.edges(), 'Edges colors', total=g.num_edges()):
    edge_color[e] = type_to_color[edge_type[e]]
    
dprms = dict(output_size=(width, height), output=args.output_file)

print('drawing started')
gt.graph_draw(g,
           pos=g.vp.pos,
           edge_color=edge_color,
           edge_pen_width=0.2,
        #    vertex_fill_color=state.b,
        vertex_size=gt.prop_to_size(g.degree_property_map('total'), 3, 12, power=.2),
           **dprms
)
print('drawing finished')