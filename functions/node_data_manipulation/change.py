import json


def update_node_style_parameter_in_redis(redis_connection, node_id, parameter, new_value):
    """
    Updates a specific style parameter for a node with the given ID in Redis.

    :param redis_connection: The Redis connection object.
    :param node_id: The ID of the node to update.
    :param parameter: The style parameter to update.
    :param new_value: The new value to set for the parameter.
    """
    node_key = f"node:{node_id}"
    style_key = f"style:{parameter}"

    # Check if the node exists in Redis
    if not redis_connection.exists(node_key):
        print(f"Node {node_id} not found in Redis.")
        return

    # Update the specific style parameter in Redis
    redis_connection.hset(node_key, style_key, json.dumps(new_value))
