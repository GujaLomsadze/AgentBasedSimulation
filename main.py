import random
import time

import progressbar as progressbar
import seaborn as sns
import simpy as simpy
from matplotlib import pyplot as plt
import concurrent.futures

from functions.converters.adj_to_networkx import create_directed_graph_from_adj_matrix
from functions.converters.json_to_matrix import json_to_matrix
from functions.node_data_manipulation.change import update_node_style_parameter_in_redis, \
    increment_link_style_parameter_in_redis, update_link_style_parameter_in_redis, \
    increment_link_style_parameter_in_redis
from functions.readers.json_readers import read_json_file
from functions.redis_wrapped.json_to_redis import json_to_redis, reconstruct_json_from_redis
from functions.redis_wrapped.conn import get_redis_connection
from functions.traversal.main import find_edge_ids_for_path
from simulations.sim import traverse_weighted_graph_n_times
from pprint import pprint

json_nodes_filename = "data/nodes.json"

json_data = read_json_file(json_nodes_filename)

adj_matrix, nodes, node_names, edges = json_to_matrix(json_nodes_filename)

node_id_label_map = {key: value for key, value in zip(nodes, node_names)}

graph = create_directed_graph_from_adj_matrix(adj_matrix_in=adj_matrix, node_names=nodes)

env = simpy.Environment()

start_node = 'n0'  # Assuming you want to start from node FE

number_of_simulations = 1_000_000  # TODO : Migrate to ArgParser

traverse_paths = traverse_weighted_graph_n_times(graph=graph, start_node=start_node, N=number_of_simulations)

r = get_redis_connection()
r.flushall()

# Move Json Data to Redis for faster traversal and change
json_to_redis(json_data=json_data, redis_conn=r)

node_name = "FE"  # The node ID you want to update
link_id = "syslog"
parameter = "is_highlighted"  # Specify the parameter within style you want to change

sim_mode = "intensity"  # TODO : Move to ArgParser
increment_amount = 1
live = None
intensity = None

if sim_mode == "intensity":
    intensity = True

if sim_mode == "live":
    live = True

# print(edges)

for path in traverse_paths:
    path_decoded = [node_id_label_map[i] for i in path]
    edge_ids = find_edge_ids_for_path(edges, path)

    if live:
        for edge_to_color in edge_ids:
            update_link_style_parameter_in_redis(r, link_id=edge_to_color, parameter=parameter, new_value=1000)

        time.sleep(1)
        for edge_to_color in edge_ids:
            update_link_style_parameter_in_redis(r, link_id=edge_to_coglor, parameter=parameter, new_value=0)

    if intensity:
        for edge_to_color in edge_ids:
            increment_link_style_parameter_in_redis(r, link_id=edge_to_color,
                                                    parameter=parameter, increment_amount=increment_amount)


# # new_value = "#ff0000"  # Specify the new color
# # new_value = "#42f545"  # Specify the new color
#
# colors = ["#ff0000", "#42f545"]
#
# node_id = node_name_id[node_name]
# nodes_g = list(graph.nodes)


# for _ in range(1_000_000):
#     random_color = random.choice(colors)
#     random_graph_name = random.choice(nodes_g)
#     random_node_id = node_name_id[random_graph_name]
#
# update_node_style_parameter_in_redis(r, random_node_id, parameter, random_color)
