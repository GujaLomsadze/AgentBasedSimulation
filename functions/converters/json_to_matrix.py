import json


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


def json_to_matrix(file_path: str):
    """
    Function to generate weighted adjacency matrix based on a ZoomCharts Node configuration
    :param file_path: Path to the JSON file containing the graph configuration
    :return: Weighted adjacency matrix / None
    """

    # TODO: Implement check if file exists

    # Open the file and load its contents
    with open(file_path, 'r', encoding="utf8") as file:
        # TODO: Consider adding error handling for file read and JSON parsing
        data = json.load(file)

    nodes = [node["id"] for node in data['nodes']]
    node_names = [node["style"]["label"] for node in data['nodes']]

    # Assuming each link now includes a 'weight' key
    edges = [[link["from"], link["to"], link.get("weight", 1)] for link in
             data["links"]]  # Default weight is 1 if not specified

    # Assuming each link now includes a 'weight' key
    edges_rich = [[link["from"], link["to"], link["id"]] for link in
                  data["links"]]

    adjacency_matrix = generate_adjacency_matrix(nodes, edges)

    return adjacency_matrix, nodes, node_names, edges_rich
