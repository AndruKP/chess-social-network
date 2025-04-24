import csv
import xml.etree.ElementTree as ET
import argparse

def csv_to_graphml(csv_file, graphml_file):
    """
    Converts a CSV file to GraphML format without using external libraries like networkx.

    Args:
        csv_file (str): Path to the input CSV file.
        graphml_file (str): Path to the output GraphML file.
    """
    # Create the root element for GraphML
    graphml = ET.Element("graphml", xmlns="http://graphml.graphdrawing.org/xmlns")
    graph = ET.SubElement(graphml, "graph", edgedefault="directed")

    # Read the CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        # headers = next(reader)  # Assume the first row contains headers

        # Keep track of nodes to avoid duplicates
        nodes = set()

        # Add edges and nodes
        for row in reader:
            # FIXME: Adjust the indices based on your CSV structure
            source, target = row[2], row[3]
            attributes = row[4:]  # Additional attributes

            # Add source node if not already added
            if source not in nodes:
                ET.SubElement(graph, "node", id=source)
                nodes.add(source)

            # Add target node if not already added
            if target not in nodes:
                ET.SubElement(graph, "node", id=target)
                nodes.add(target)

            # Add edge with attributes
            edge = ET.SubElement(graph, "edge", source=source, target=target)
            # for i, attr in enumerate(attributes):
            #     ET.SubElement(edge, f"data", key=f"attr{i}").text = attr

    # Write the GraphML to a file
    tree = ET.ElementTree(graphml)
    with open(graphml_file, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)


parser = argparse.ArgumentParser(description="Convert a CSV file to GraphML format.")
parser.add_argument("csv_file", help="Path to the input CSV file")
parser.add_argument("graphml_file", help="Path to the output GraphML file")

# Parse arguments
args = parser.parse_args()

# Call the conversion function
csv_to_graphml(args.csv_file, args.graphml_file)

