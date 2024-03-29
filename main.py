import copy
import time
from pprint import pprint

from functions.analysis.main import calculate_transition_probabilities, \
    calculate_levels_and_probabilities, \
    adjust_color_by_level, replicate_nodes_in_graph_and_track_edges, calculate_evenness, identify_outliers, \
    grid_search_replication
from functions.converters.adj_to_networkx import create_directed_graph_from_adj_matrix
from functions.converters.json_to_matrix import json_to_matrix, graph_to_json
from functions.converters.graph_to_mermaid import export_to_mermaid
from functions.node_data_manipulation.change import update_node_style_parameter_in_redis, \
    update_link_style_parameter_in_redis, \
    increment_link_style_parameter_in_redis
from functions.readers.json_readers import read_json_file
from functions.redis_wrapped.conn import get_redis_connection
from functions.redis_wrapped.json_to_redis import json_to_redis, update_redis_with_graph
from functions.traversal.main import find_edge_ids_for_path
from simulations.sim import traverse_weighted_graph_n_times, traverse_any_given_graph_and_visualize, simulate_errors

json_nodes_filename = "data/nodes.json"  # TODO : Migrate to ArgParser

json_data = read_json_file(json_nodes_filename)

adj_matrix, nodes, node_names, edges = json_to_matrix(data=json_data)

node_id_label_map = {key: value for key, value in zip(nodes, node_names)}

graph = create_directed_graph_from_adj_matrix(adj_matrix_in=adj_matrix, node_names=nodes)

"""
============================================================================================ PARAMETERS
"""
start_node = 'n0'  # Assuming you want to start from node FE

parameter = "is_highlighted"  # Specify the parameter within style you want to change

sim_mode = "intensity"  # TODO : Move to ArgParser
increment_amount = 3  # TODO : Move to ArgParser

live = False
intensity = False

if sim_mode == "intensity":
    intensity = True

if sim_mode == "live":
    live = True

number_of_simulations = 1_000_000  # TODO : Migrate to ArgParser

"""
============================================================================================ PARAMETERS
"""

r = get_redis_connection()
r.flushall()

graph_with_errors, edges_with_errors = simulate_errors(graph_in=copy.deepcopy(graph), error_rate=1, error_weight_in=0.1)


graph = graph_with_errors
edges.extend(edges_with_errors)

# Move Json Data to Redis for faster traversal and change
json_to_redis(json_data=graph_to_json(graph), redis_conn=r)

traverse_any_given_graph_and_visualize(redis_conn=r, method=sim_mode, graph=graph, edges=edges,
                                       start_node=start_node,
                                       parameter=parameter, number_of_simulations=10000,
                                       increment_amount=increment_amount)

exit()

# TODO: Move this to ArgParser
FULL_PROBABILITY = True
REMOVE_STARTING_NODE = True

edge_probabilities = calculate_transition_probabilities(graph, start_node)
# full_probabilities = calculate_all_transition_probabilities(graph, start_node)


graph_cp = copy.deepcopy(graph)

# best_config, lowest_cv, best_adjusted_graph, best_new_edges = grid_search_replication(
#     graph_cp, start_node)
#
# print(best_config, lowest_cv)

# exit()

adjusted_graph, new_edges = replicate_nodes_in_graph_and_track_edges(graph_cp, start_node, replication_percentile=80,
                                                                     min_probability_threshold=0.1)
edges.extend(new_edges)  # Combine original edges with new edges

graph = adjusted_graph
# edges = new_edges

_good_green_hex = "#42f545"
updated_json_data = graph_to_json(graph)

# update_redis_with_graph(graph=adjusted_graph, redis_conn=r)

r.flushall()
json_to_redis(json_data=updated_json_data, redis_conn=r)

levels, full_probabilities = calculate_levels_and_probabilities(graph, start_node)

if FULL_PROBABILITY:
    transition_probabilities = full_probabilities
else:
    transition_probabilities = edge_probabilities

if REMOVE_STARTING_NODE:
    transition_probabilities.pop(start_node)

# pprint(transition_probabilities)

cv = calculate_evenness(transition_probabilities)
print(f"Coefficient of Variation: {cv:.2f}  (Closer to zero better)")

outlier_nodes = identify_outliers(transition_probabilities)  # TODO: Handle outlier nodes

# Find min and max probabilities
min_prob = min(transition_probabilities.values())
max_prob = max(transition_probabilities.values())

COLOR_IN_ADVANCE_EDGES = False  # The node ID you want to update


def color_the_pre_nodes():
    color_map = adjust_color_by_level(probabilities=transition_probabilities, node_levels=levels)
    # Display or use the colors
    for node, color in color_map.items():
        update_node_style_parameter_in_redis(redis_connection=r, node_id=node,
                                             parameter="fillColor", new_value=color)


if COLOR_IN_ADVANCE_EDGES:
    color_the_pre_nodes()

traverse_any_given_graph_and_visualize(redis_conn=r, method=sim_mode, graph=graph, edges=edges, start_node=start_node,
                                       parameter=parameter, number_of_simulations=number_of_simulations,
                                       increment_amount=increment_amount)

# new_value = "#ff0000"  # Specify the new color
# new_value = "#42f545"  # Specify the new color
#
# colors = ["#ff0000", "#42f545"]
#
# node_id = node_name_id[node_name]
# nodes_g = list(graph.nodes)
#
#
# for _ in range(1_000_000):
#     random_color = random.choice(colors)
#     random_graph_name = random.choice(nodes_g)
#     random_node_id = node_name_id[random_graph_name]
#
# update_node_style_parameter_in_redis(r, random_node_id, parameter, random_color)
