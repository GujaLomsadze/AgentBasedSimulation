import random
import time
from collections import defaultdict

from functions.node_data_manipulation.change import update_link_style_parameter_in_redis, \
    increment_link_style_parameter_in_redis
from functions.traversal.main import find_edge_ids_for_path


def traverse_weighted_graph_n_times(graph, start_node, N):
    for _ in range(N):
        temp_path = []

        current_node = start_node
        while True:
            temp_path.append(current_node)
            neighbors = list(graph.successors(current_node))

            if len(neighbors) == 0:
                break

            # Calculate probabilities based on edge weights
            probabilities = [graph[current_node][neighbor]['weight'] for neighbor in neighbors]

            # Normalize probabilities to make sure they sum up to 1
            total_prob = sum(probabilities)
            probabilities = [p / total_prob for p in probabilities]

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

    for path in traverse_paths:
        edge_ids = find_edge_ids_for_path(edges, path)

        if live:
            for edge_to_color in edge_ids:
                update_link_style_parameter_in_redis(r, link_id=edge_to_color, parameter=parameter, new_value=1000)

            time.sleep(0.1)
            for edge_to_color in edge_ids:
                update_link_style_parameter_in_redis(r, link_id=edge_to_color, parameter=parameter, new_value=0)

        if intensity:
            for edge_to_color in edge_ids:
                increment_link_style_parameter_in_redis(r, link_id=edge_to_color,
                                                        parameter=parameter, increment_amount=increment_amount)
