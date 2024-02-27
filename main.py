import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

from entities.nodes.classes import PostgreSQLInstance, NodejsService
from functions.converters.json_to_matrix import json_to_matrix
from functions.converters.adj_to_networkx import create_directed_graph_from_adj_matrix

adjacency_matrix = json_to_matrix("data/nodes.json")

graph = create_directed_graph_from_adj_matrix(adj_matrix_in=adjacency_matrix)


def choose_next_node(G, cur_node):
    """
    Function to choose a next node based on a Probability from weights.
    Simulates Markov's Chain
    :param G: Graph
    :param cur_node: Current node name
    :return: Net node or None
    """
    neighbors = list(G.successors(cur_node))

    if not neighbors:
        return None  # Depth stopped here, no more continuation

    weights = [G[cur_node][neighbor]['weight'] for neighbor in neighbors]

    # Convert weights to probabilities
    total_weight = sum(weights)
    probabilities = [weight / total_weight for weight in weights]

    # Choose next node based on probabilities
    print(neighbors, probabilities)
    next_node = np.random.choice(neighbors, p=probabilities)
    return next_node


current_node = 1

steps = 11
print(f"Starting at node {current_node}")

for _ in range(steps):
    current_node = choose_next_node(graph, current_node)

    print(f"Moved to node {current_node}")
