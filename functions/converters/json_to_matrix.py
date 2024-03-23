import json
from pprint import pprint


def print_matrix(matrix):
    """
    Print the matrix in a formatted manner
    :param matrix: 2D List representing the matrix to be printed
    """
    for row in matrix:
        print(' '.join(map(str, row)))


def generate_adjacency_matrix(nodes_in, edges_in):
    """
    Function to generate weighted adjacency matrix from list of nodes and 2D list of edges(links) with weights
    :param nodes_in: List of nodes
    :param edges_in: List of edges with weights
    :return: Weighted adjacency matrix or error
    """
    node_index = {node: index for index, node in enumerate(nodes_in)}

    matrix_size = len(nodes_in)
    adjacency_matrix_out = [[0] * matrix_size for _ in range(matrix_size)]

    for edge in edges_in:
        source_index = node_index[edge[0]]
        target_index = node_index[edge[1]]
        weight = edge[2]  # Assuming the third element in each edge is the weight
        adjacency_matrix_out[source_index][target_index] = float(weight)

    return adjacency_matrix_out


def json_to_matrix(data):
    """
    Function to generate weighted adjacency matrix based on a ZoomCharts Node configuration
    :return: Weighted adjacency matrix / None
    """
    nodes = [node["id"] for node in data['nodes']]
    node_names = [node["style"]["label"] for node in data['nodes']]

    # Assuming each link now includes a 'weight' key
    edges = [[link["from"], link["to"], link.get("weight", 1)] for link in
             data["links"]]  # Default weight is 1 if not specified

    # Assuming each link now includes a 'weight' key
    edges_rich = [[link["from"], link["to"], f"{link['from']}_{link['to']}"] for link in
                  data["links"]]

    adjacency_matrix = generate_adjacency_matrix(nodes, edges)

    return adjacency_matrix, nodes, node_names, edges_rich


def graph_to_json(graph):
    # Initialize the structure
    json_data = {"nodes": [], "links": []}

    # Process nodes
    for node in graph.nodes(data=True):
        node_data = {
            "id": node[0],
            "loaded": True,
            "style": node[1].get('style', {
                "label": node[0],  # Use node ID as label if not specified
                "radius": 12157,
                "fillColor": "#42f545"  # Default values, adjust as necessary
            })
        }
        json_data["nodes"].append(node_data)

    # Process edges
    for u, v, data in graph.edges(data=True):
        link_data = {
            "id": data.get('id', f"{u}_{v}"),
            "from": u,
            "to": v,
            "name": data.get('name', f"{u} to {v}"),  # Default name, adjust as necessary
            "weight": str(data.get('weight', "1.0")),  # Default weight
            "style": data.get('style', {
                "toDecoration": "arrow"
            })
        }
        json_data["links"].append(link_data)

    with open("data/sample.json", "w") as outfile:
        json.dump(json_data, outfile)

    return json_data
