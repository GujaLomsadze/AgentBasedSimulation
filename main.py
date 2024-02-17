from entities.nodes.classes import PostgreSQLInstance, NodejsService
from functions.converters.json_to_matrix import json_to_matrix

adjacency_matrix = json_to_matrix("data/nodes.json")

# get_graph_stats(adjacency_matrix=adjacency_matrix)

pg1 = PostgreSQLInstance(
    type="PostgreSQLInstance",
    name="PG_1",
    ip="10.0.55.200",
    port=5432,
    cpu_usage=20,
    active_connections=1
)

ms1 = NodejsService(
    type="Microservice N1",
    name="NS_1",
    ip="10.0.55.201",
    port=5432,
    cpu_usage=20,
)



