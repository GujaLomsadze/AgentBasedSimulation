import json


def generate_adjacency_matrix(nodes_in, edges_in):
    """
    Function to generate Adjacency matrix from list of nodes and 2D list of edges(links)
    :param nodes_in: List of nodes
    :param edges_in: List of edges
    :return: Adjacency matrix or error
    """
    node_index = {node: index for index, node in enumerate(nodes_in)}

    matrix_size = len(nodes_in)
    adjacency_matrix_out = [[0] * matrix_size for _ in range(matrix_size)]

    for edge in edges_in:
        source_index = node_index[edge[0]]
        target_index = node_index[edge[1]]
        adjacency_matrix_out[source_index][target_index] = 1

    return adjacency_matrix_out


def yml_to_matrix(file_path: str):
    """
    Function to generate Adjacency matrix based on a ZoomCharts Node configuration
    :param file_path: Obvious, no?
    :return: Adjacency matrix / None
    """

    # TODO: OS Path exists here obviously

    # Open the file and load its contents
    with open(file_path, 'r', encoding="utf8") as file:
        # TODO: Try-Except block yo

        data = json.load(file)

    # TODO: Sloppy code. Fix
    nodes = [node["id"] for node in data['nodes']]

    edges = [[link["from"], link["to"]] for link in data["links"]]

    adjacency_matrix = generate_adjacency_matrix(nodes, edges)

    return adjacency_matrix
