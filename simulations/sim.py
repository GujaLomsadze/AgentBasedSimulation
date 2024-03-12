import random
from collections import defaultdict


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
