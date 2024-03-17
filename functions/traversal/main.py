def find_edge_ids_for_path(edges, path):
    """
    Retrieves a list of edge IDs for the given path of nodes, ensuring all transitions
    are accounted for, from the first node to the last.

    :param edges: List of edges where each edge is represented as [from, to, id]
    :param path: List of node IDs representing the path
    :return: List of edge IDs corresponding to the transitions between nodes in the path
    """
    edge_ids = []
    for i in range(len(path) - 1):  # Iterate through the path to get each transition
        from_node = path[i]
        to_node = path[i + 1]

        # Find and append the edge ID for each transition
        edge_id = next((edge[2] for edge in edges if edge[0] == from_node and edge[1] == to_node), None)
        if edge_id:
            edge_ids.append(edge_id)
        else:
            print(f"Could not find Edge ID for transition: {from_node} -> {to_node}")

    return edge_ids
