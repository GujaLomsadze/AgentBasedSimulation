import random
import time
from collections import defaultdict

from functions.node_data_manipulation.change import update_link_style_parameter_in_redis, \
    increment_link_style_parameter_in_redis, decrement_link_style_parameter_in_redis
from functions.traversal.main import find_edge_ids_for_path


def traverse_weighted_graph_n_times(graph, start_node, N):
    """
    Traverses a weighted graph N times, considering self-edges.

    Args:
        graph: A NetworkX graph object.
        start_node: The starting node for the traversal.
        N: The number of times to traverse the graph.

    Yields:
        A list representing a single traversal path.
    """

    for _ in range(N):
        temp_path = []

        current_node = start_node
        while True:
            temp_path.append(current_node)

            # Get all neighbors, including self-loops
            neighbors = list(graph.neighbors(current_node))

            if len(neighbors) == 0:
                break

            # Calculate edge weight probabilities (handle self-edge weight)
            probabilities = []
            for neighbor in neighbors:
                if neighbor == current_node:  # Check for self-edge
                    weight = graph.get_edge_data(current_node, neighbor).get('weight',
                                                                             1.0)  # Get weight or default to 1.0
                else:
                    weight = graph[current_node][neighbor]['weight']
                probabilities.append(weight)

            # Normalize probabilities
            total_prob = sum(probabilities)
            probabilities = [p / total_prob for p in probabilities]

            # Terminate if at end node with self-edge
            if len(neighbors) == 1 and graph.has_edge(current_node, current_node):
                break

            # print(current_node, neighbors, probabilities)
            # Choose the next node based on probabilities
            next_node = random.choices(neighbors, weights=probabilities)[0]
            current_node = next_node

        yield temp_path


def traverse_any_given_graph_and_visualize(redis_conn, method, graph, edges, start_node, parameter,
                                           number_of_simulations,
                                           increment_amount):
    r = redis_conn

    live = False
    intensity = False

    if method == "live":
        live = True
    if method == "intensity":
        intensity = True

    traverse_paths = traverse_weighted_graph_n_times(graph=graph, start_node=start_node, N=number_of_simulations)

    for index, path in enumerate(traverse_paths):
        edge_ids = find_edge_ids_for_path(edges, path)

        if live:
            for edge_to_color in edge_ids:
                update_link_style_parameter_in_redis(r, link_id=edge_to_color, parameter=parameter, new_value=1000)

            time.sleep(0.1)
            for edge_to_color in edge_ids:
                update_link_style_parameter_in_redis(r, link_id=edge_to_color, parameter=parameter, new_value=0)

        if intensity:

            # TODO: INDEX IS ONE UNIQUE REQUEST PASSED THROUGH THE GRAPH
            # TODO: INDEX IS ONE UNIQUE REQUEST PASSED THROUGH THE GRAPH
            # TODO: INDEX IS ONE UNIQUE REQUEST PASSED THROUGH THE GRAPH
            # TODO: INDEX IS ONE UNIQUE REQUEST PASSED THROUGH THE GRAPH

            # if index % 1000 == 0:
            #     print("DECREMENT TIME")
            #     for stage_level, edge_to_color in enumerate(edge_ids):
            #         decrement_link_style_parameter_in_redis(r, link_id=edge_to_color,
            #                                                 parameter=parameter,
            #                                                 decrement_amount=increment_amount * index)

            for stage_level, edge_to_color in enumerate(edge_ids):
                increment_link_style_parameter_in_redis(r, link_id=edge_to_color,
                                                        parameter=parameter, increment_amount=increment_amount)


def simulate_errors(graph_in, error_rate, error_weight_in=0.01):
    """
    Simulates errors in a graph by adding self-edges to a random selection of nodes.

    Args:
        graph_in: A NetworkX graph object representing the data architecture.
        error_rate (float): The percentage (0.0 to 1.0) of nodes to introduce errors to.
        error_weight_in (float): Error probability for a given Node

    Returns:
        A new NetworkX graph object with the simulated errors added.
    """

    # Create a copy of the original graph to avoid modifying it directly
    G_with_errors = graph_in.copy()

    new_edges_w_errors = []

    # Select a random set of nodes for error injection
    num_nodes = G_with_errors.number_of_nodes()
    num_errors = int(error_rate * num_nodes)
    error_nodes = random.sample(list(G_with_errors.nodes()), num_errors)

    # Add self-edges to the selected nodes with a chance of error weight
    for node in error_nodes:
        edge_id = f"{node}_{node}"  # f-string for formatted string literal

        G_with_errors.add_edge(node, node, id=edge_id)
        G_with_errors.edges[node, node]['weight'] = error_weight_in
        new_edges_w_errors.append([node, node, edge_id])

    return G_with_errors, new_edges_w_errors
