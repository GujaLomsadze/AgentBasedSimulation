import math
from collections import deque

import networkx as nx
import numpy as np


def create_graph_from_adjacency_matrix(adjacency_matrix):
    return nx.from_numpy_array(adjacency_matrix, create_using=nx.DiGraph)


def calculate_degrees(G):
    in_degrees = dict(G.in_degree())
    out_degrees = dict(G.out_degree())
    return in_degrees, out_degrees


def calculate_shortest_paths(G):
    return dict(nx.shortest_path_length(G))


def calculate_centrality_measures(G):
    betweenness_centrality = nx.betweenness_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    return betweenness_centrality, closeness_centrality


def calculate_clustering_coefficient(G):
    # For directed graphs, convert to undirected for clustering calculation
    undirected_G = G.to_undirected()
    return nx.average_clustering(undirected_G)


def calculate_graph_density(G):
    return nx.density(G)


def calculate_connectivity(G):
    # For directed graphs, this will calculate strongly connected components
    return [len(c) for c in sorted(nx.strongly_connected_components(G), key=len, reverse=True)]


def calculate_community_detection(G):
    # This requires converting to undirected graph for the community detection algorithm
    undirected_G = G.to_undirected()
    from networkx.algorithms import community
    communities = community.greedy_modularity_communities(undirected_G)
    return [list(community) for community in communities]


def get_graph_stats(adjacency_matrix):
    """
    Function to get Network basic analysis from Adjacency Matrix
    :param adjacency_matrix: Obvious.
    :return:
    """

    adjacency_matrix = np.array(adjacency_matrix)

    # Create a graph from the adjacency matrix
    G = create_graph_from_adjacency_matrix(adjacency_matrix)

    # Perform calculations
    in_degrees, out_degrees = calculate_degrees(G)
    shortest_paths = calculate_shortest_paths(G)
    betweenness_centrality, closeness_centrality = calculate_centrality_measures(G)
    clustering_coefficient = calculate_clustering_coefficient(G)
    density = calculate_graph_density(G)
    connectivity = calculate_connectivity(G)
    communities = calculate_community_detection(G)

    # Example output
    print(f"In-Degrees: {in_degrees}")
    print(f"Out-Degrees: {out_degrees}")
    print(f"Shortest Paths: {shortest_paths}")
    print(f"Betweenness Centrality: {betweenness_centrality}")
    print(f"Closeness Centrality: {closeness_centrality}")
    print(f"Clustering Coefficient: {clustering_coefficient}")
    print(f"Density: {density}")
    print(f"Connectivity: {connectivity}")
    print(f"Communities: {communities}")

    return in_degrees, out_degrees, shortest_paths, betweenness_centrality, \
           closeness_centrality, clustering_coefficient, density, connectivity, communities


def calculate_transition_probabilities(graph, start_node):
    """
    Calculates transition probabilities from the given start node to all ending nodes.
    This version includes cycle detection to prevent infinite recursion.

    Args:
        graph: A NetworkX DiGraph.
        start_node: The starting node for the transition calculation.

    Returns:
        A dictionary where keys are ending nodes and values are transition probabilities.
    """

    probabilities = {}
    ending_nodes = [node for node in graph.nodes() if graph.out_degree(node) == 0]
    visited = set()  # Keep track of visited nodes to avoid cycles

    def dfs(node, path_probability):
        if node in visited:
            return  # Avoid cycles
        visited.add(node)

        if node in ending_nodes:
            if node in probabilities:
                probabilities[node] += path_probability
            else:
                probabilities[node] = path_probability
            visited.remove(node)  # Backtrack: remove from visited set
            return

        for neighbor in graph.successors(node):
            probability = graph[node][neighbor].get('weight', 1)
            dfs(neighbor, path_probability * probability)

        visited.remove(node)  # Backtrack: remove from visited set

    dfs(start_node, 1.0)

    return probabilities


def calculate_all_transition_probabilities(graph, start_node):
    """
    Calculates transition probabilities from the given start node to all nodes in the graph.
    This version includes cycle detection to prevent infinite recursion and accumulates
    probabilities at each node.

    Args:
        graph: A NetworkX DiGraph.
        start_node: The starting node for the transition calculation.

    Returns:
        A dictionary where keys are node identifiers and values are transition probabilities.
    """

    # Initialize probabilities for all nodes with 0, except the start node with 1
    probabilities = {node: 0 for node in graph.nodes()}
    probabilities[start_node] = 1.0
    visited = set()  # Keep track of visited nodes to avoid cycles

    def dfs(node, path_probability):
        if node in visited:
            return  # Avoid cycles
        visited.add(node)

        # Distribute current path probability to all successors
        total_weight = sum(graph[node][neighbor].get('weight', 1) for neighbor in graph.successors(node))
        for neighbor in graph.successors(node):
            edge_weight = graph[node][neighbor].get('weight', 1)
            # Adjust the path_probability by the edge weight and total outgoing weight
            successor_probability = path_probability * (edge_weight / total_weight if total_weight else 0)
            probabilities[neighbor] += successor_probability
            dfs(neighbor, successor_probability)

        visited.remove(node)  # Backtrack: remove from visited set

    dfs(start_node, 1.0)

    return probabilities


def calculate_relative_depth_probabilities(graph, start_node):
    """
    Calculates transition probabilities from the given start node to all nodes in the graph,
    with each depth level computed relative to that level only.

    Args:
        graph: A NetworkX DiGraph.
        start_node: The starting node for the transition calculation.

    Returns:
        A dictionary where keys are node identifiers and values are transition probabilities.
    """
    probabilities = {node: 0 for node in graph.nodes()}  # Initialize probabilities
    probabilities[start_node] = 1.0  # Start node probability is 100%

    # Store nodes to visit with their associated path probability
    to_visit = [(start_node, 1.0)]

    while to_visit:
        current_level = []
        next_level = []

        # Process nodes at the current level
        for node, path_probability in to_visit:
            # Calculate total weight for normalization
            total_weight = sum(graph[node][neighbor].get('weight', 1) for neighbor in graph.successors(node))
            for neighbor in graph.successors(node):
                edge_weight = graph[node][neighbor].get('weight', 1)
                # Adjust path_probability for the edge weight relative to total outgoing weight
                if total_weight > 0:
                    relative_probability = (edge_weight / total_weight) * path_probability
                else:
                    relative_probability = 0
                probabilities[neighbor] += relative_probability
                next_level.append((neighbor, probabilities[neighbor]))

        to_visit = next_level  # Move to the next level

    return probabilities


def get_relative_color(probabilities):
    """
    Maps each probability to a color on a green-yellow-red scale based on its relative position.

    Args:
    - probabilities: A dictionary of node identifiers to their probabilities.

    Returns:
    - A dictionary of node identifiers to their color codes.
    """
    min_prob = min(probabilities.values())
    max_prob = max(probabilities.values())
    color_map = {}

    for node, prob in probabilities.items():
        if max_prob - min_prob == 0:
            # Avoid division by zero if all probabilities are the same
            relative_position = 0.5
        else:
            relative_position = (prob - min_prob) / (max_prob - min_prob)

        if relative_position <= 0.5:
            # Scale from green (0) to yellow (0.5)
            red = int(2 * relative_position * 255)
            green = 255
        else:
            # Scale from yellow (0.5) to red (1)
            red = 255
            green = int((1 - 2 * (relative_position - 0.5)) * 255)

        blue = 0
        color_map[node] = f"#{red:02x}{green:02x}{blue:02x}"

    return color_map


def calculate_distribution_skewness(probabilities):
    """
    Calculates the skewness of the probability distribution using entropy.
    A lower percentage indicates a more skewed distribution.

    Args:
    - probabilities: A dictionary of node identifiers to their probabilities.

    Returns:
    - A percentage representing the skewness of the distribution relative to a uniform distribution.
    """
    # Calculate entropy of the distribution
    entropy = -sum(prob * math.log(prob, 2) for prob in probabilities.values() if prob > 0)

    # Calculate the maximum possible entropy (for a uniform distribution)
    num_nodes = len(probabilities)
    max_entropy = math.log(num_nodes, 2) if num_nodes > 0 else 0

    # Calculate the skewness as a percentage of the maximum entropy
    skewness_percentage = (entropy / max_entropy) * 100 if max_entropy > 0 else 0

    return skewness_percentage


def adjust_color_by_level(probabilities, node_levels):
    """
    Adjusts the color mapping to consider probabilities relative to their level.

    Args:
    - probabilities: A dictionary of node identifiers to their probabilities.
    - node_levels: A dictionary of node identifiers to their levels.

    Returns:
    - A dictionary of node identifiers to their color codes.
    """
    # Determine min and max probabilities per level
    level_probabilities = {}
    for node, prob in probabilities.items():
        level = node_levels[node]
        if level in level_probabilities:
            level_probabilities[level]['min'] = min(level_probabilities[level]['min'], prob)
            level_probabilities[level]['max'] = max(level_probabilities[level]['max'], prob)
        else:
            level_probabilities[level] = {'min': prob, 'max': prob}

    # Map probabilities to colors, considering the min and max per level
    color_map = {}
    for node, prob in probabilities.items():
        level = node_levels[node]
        min_prob, max_prob = level_probabilities[level]['min'], level_probabilities[level]['max']
        if max_prob - min_prob == 0:
            relative_position = 0.5
        else:
            relative_position = (prob - min_prob) / (max_prob - min_prob)

        if relative_position <= 0.5:
            red = int(2 * relative_position * 255)
            green = 255
        else:
            red = 255
            green = int((1 - 2 * (relative_position - 0.5)) * 255)
        blue = 0
        color_map[node] = f"#{red:02x}{green:02x}{blue:02x}"

    return color_map


def calculate_levels_and_probabilities(graph, start_node):
    """
    Calculates levels in the graph and transition probabilities from the start node to all nodes,
    with probabilities at each level computed relative to that level only.

    Args:
        graph: A NetworkX DiGraph.
        start_node: The starting node for the transition calculation.

    Returns:
        A tuple containing two items:
        - A dictionary of nodes with their levels.
        - A dictionary where keys are node identifiers and values are transition probabilities.
    """
    levels = {}  # Node to level mapping
    probabilities = {node: 0 for node in graph.nodes()}  # Initialize probabilities
    probabilities[start_node] = 1.0  # Start node probability is 100%

    queue = deque([(start_node, 0)])  # Queue for BFS: (node, level)

    while queue:
        node, level = queue.popleft()
        if node not in levels:  # First visit to node
            levels[node] = level

            total_weight = sum(graph[node][neighbor].get('weight', 1) for neighbor in graph.successors(node))
            for neighbor in graph.successors(node):
                edge_weight = graph[node][neighbor].get('weight', 1)
                if total_weight > 0:
                    relative_probability = (edge_weight / total_weight) * probabilities[node]
                else:
                    relative_probability = 0

                probabilities[neighbor] += relative_probability

                queue.append((neighbor, level + 1))

    return levels, probabilities
