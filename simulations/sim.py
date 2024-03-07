import random
from collections import defaultdict


def traverse_weighted_graph_N_times(graph, start_node, N):
    visit_counts = defaultdict(int)

    for _ in range(N):
        current_node = start_node
        visited = set()

        while True:
            visited.add(current_node)
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
            visit_counts[next_node] += 1
            current_node = next_node

        # Update visit counts for all visited nodes
        for node in visited:
            visit_counts[node] += 1

    return dict(visit_counts)
