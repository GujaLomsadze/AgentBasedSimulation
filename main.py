import numpy as np
import networkx as nx
from functions.converters.yml_to_matrix import yml_to_matrix

adjacency_matrix = yml_to_matrix("data/nodes.json")

adjacency_matrix = np.array(adjacency_matrix)


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
