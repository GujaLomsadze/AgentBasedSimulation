import random

from functions.converters.adj_to_networkx import create_directed_graph_from_adj_matrix
from functions.converters.json_to_matrix import json_to_matrix
from functions.node_data_manipulation.change import update_node_style_parameter_in_redis
from functions.readers.json_readers import read_json_file
from functions.redis_wrapped.json_to_redis import json_to_redis, reconstruct_json_from_redis
from functions.redis_wrapped.conn import get_redis_connection

json_nodes_filename = "data/nodes.json"

json_data = read_json_file(json_nodes_filename)

adj_matrix, nodes, node_names = json_to_matrix(json_nodes_filename)

node_name_id = {key: value for key, value in zip(node_names, nodes)}

graph = create_directed_graph_from_adj_matrix(adj_matrix_in=adj_matrix, node_names=node_names)

r = get_redis_connection()

# Move Json Data to Redis for faster traversal and change
json_to_redis(json_data=json_data, redis_conn=r)

node_name = "FE"  # The node ID you want to update
parameter = "fillColor"  # Specify the parameter within style you want to change

# new_value = "#ff0000"  # Specify the new color
# new_value = "#42f545"  # Specify the new color

colors = ["#ff0000", "#42f545"]

node_id = node_name_id[node_name]
nodes_g = list(graph.nodes)

for _ in range(1_000_000):
    random_color = random.choice(colors)
    random_graph_name = random.choice(nodes_g)
    random_node_id = node_name_id[random_graph_name]

    update_node_style_parameter_in_redis(r, random_node_id, parameter, random_color)
