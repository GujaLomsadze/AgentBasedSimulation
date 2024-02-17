from functions.analysis.main import get_graph_stats
from functions.converters.json_to_matrix import json_to_matrix

adjacency_matrix = json_to_matrix("data/nodes.json")

get_graph_stats(adjacency_matrix=adjacency_matrix)
