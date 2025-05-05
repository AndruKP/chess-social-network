import csv
import xml.etree.ElementTree as ET
import argparse

FIELDNAMES = [
    "White", #0
    "Black", #1
    "Result", #2
    "BlackElo", #3
    "BlackRatingDiff", #4
    "BlackTitle", #5
    "ECO", #6
    "Event", #7
    "Opening", #8
    "Site", #9
    "Termination", #10
    "TimeControl", #11
    "UTCDate", #12
    "UTCTime", #13
    "WhiteElo", #14
    "WhiteRatingDiff", #15
    "WhiteTitle" #16
]

def csv_to_graphml(csv_file, graphml_file, graph_type):
    """
    Converts a CSV file to GraphML format

    Args:
        csv_file (str): Path to the input CSV file.
        graphml_file (str): Path to the output GraphML file.
        graph_type (str): Type of the graph.
    """

    if graph_type not in ['white_to_black', 'winner_to_loser']:
        raise ValueError(f"Bad graph type: graph_type = {graph_type}")

    # Create the root element for GraphML
    graphml = ET.Element("graphml", xmlns="http://graphml.graphdrawing.org/xmlns")
    graph = ET.SubElement(graphml, "graph", edgedefault="directed")
    
    ET.SubElement(graph, "key", id="id", **{
        "for": "edge", "attr.name": "id", "attr.type": "int"
    })
    
    ET.SubElement(graph, "key", id="gt", **{
        "for": "edge", "attr.name": "game type", "attr.type": "string"
    })

    # Read the CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        # headers = next(reader)  # Assume the first row contains headers

        # Keep track of nodes to avoid duplicates
        nodes = set()
        
        id_counter = 0
        
        # Add edges and nodes
        for row in reader:
            # FIXME: Adjust the indices based on your CSV structure
            white, black = row[0], row[1]
            result = row[2]
            attributes = row[3:]  # Additional attributes

            # Add source node if not already added
            if white not in nodes:
                ET.SubElement(graph, "node", id=white)
                nodes.add(white)

            # Add target node if not already added
            if black not in nodes:
                ET.SubElement(graph, "node", id=black)
                nodes.add(black)

            if graph_type == "white_to_black":             
                edge = ET.SubElement(graph, "edge", source=white, target=black)
                
            elif graph_type == "winner_to_loser":
                if result == '1-0':
                    edge = ET.SubElement(graph, "edge", source=white, target=black)
                elif result == '0-1':
                    edge = ET.SubElement(graph, "edge", source=black, target=white)
                else:
                    edge = ET.SubElement(graph, "edge", source=white, target=black, directed='false')

            # Add edge with attributes
            game_type = ""
            if "Bullet" in attributes[4] : game_type = 'B'
            if "Blitz" in attributes[4] : game_type = 'Z'
            if "Classical" in attributes[4] : game_type = 'C'

            ET.SubElement(edge, f"data", key=f"id").text = str(id_counter)
            ET.SubElement(edge, f"data", key=f"gt").text = game_type
            
            id_counter += 1

    # Write the GraphML to a file
    tree = ET.ElementTree(graphml)
    with open(graphml_file, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)


parser = argparse.ArgumentParser(description="Convert a CSV file to GraphML format.")
parser.add_argument("csv_file", help="Path to the input CSV file")
parser.add_argument("graphml_file", help="Path to the output GraphML file")
parser.add_argument("graph_type", choices=['white_to_black', 'winner_to_loser'], help="Type of directed edges")

# Parse arguments
args = parser.parse_args()

# Call the conversion function
csv_to_graphml(args.csv_file, args.graphml_file, args.graph_type)
