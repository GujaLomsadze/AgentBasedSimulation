import random

import seaborn as sns
from matplotlib import pyplot as plt

from functions.converters.adj_to_networkx import create_directed_graph_from_adj_matrix
from functions.converters.json_to_matrix import json_to_matrix
from functions.node_data_manipulation.change import update_node_style_parameter_in_redis
from functions.readers.json_readers import read_json_file
from functions.redis_wrapped.json_to_redis import json_to_redis, reconstruct_json_from_redis
from functions.redis_wrapped.conn import get_redis_connection
from simulations.sim import traverse_weighted_graph_N_times
from pprint import pprint

json_nodes_filename = "data/nodes.json"

json_data = read_json_file(json_nodes_filename)

adj_matrix, nodes, node_names = json_to_matrix(json_nodes_filename)

node_name_id = {key: value for key, value in zip(node_names, nodes)}

graph = create_directed_graph_from_adj_matrix(adj_matrix_in=adj_matrix, node_names=node_names)

# Example usage:
# Assuming visit_counts is the dictionary containing the visit counts


start_node = "FE"
N = 1_000_000  # Number of times to traverse the graph
visit_counts = traverse_weighted_graph_N_times(graph, start_node, N)

pprint(visit_counts)

# Sort the dictionary by keys (node names)
sorted_counts = {k: visit_counts[k] for k in sorted(visit_counts)}

# Plot the distribution
plt.figure(figsize=(12, 6))
sns.barplot(x=list(sorted_counts.keys()), y=list(sorted_counts.values()))
plt.xlabel('Node Names')
plt.ylabel('Visit Count')
plt.title('Distribution of Visit Counts by Node Names')
plt.xticks(rotation=90)
plt.show()
# r = get_redis_connection()
#
# # Move Json Data to Redis for faster traversal and change
# json_to_redis(json_data=json_data, redis_conn=r)
#
# node_name = "FE"  # The node ID you want to update
# parameter = "fillColor"  # Specify the parameter within style you want to change
#
# # new_value = "#ff0000"  # Specify the new color
# # new_value = "#42f545"  # Specify the new color
#
# colors = ["#ff0000", "#42f545"]
#
# node_id = node_name_id[node_name]
# nodes_g = list(graph.nodes)
#
# for _ in range(1_000_000):
#     random_color = random.choice(colors)
#     random_graph_name = random.choice(nodes_g)
#     random_node_id = node_name_id[random_graph_name]
#
#     update_node_style_parameter_in_redis(r, random_node_id, parameter, random_color)
