import redis


def get_redis_connection(redis_host='localhost', redis_port=6379, redis_password=None):
    """
    Establish and return a Redis connection.

    Parameters:
    - redis_host (str): Hostname of the Redis server.
    - redis_port (int): Port on which the Redis server is running.
    - redis_password (str): Password for the Redis server, if required.

    Returns:
    - Redis connection object that can be reused for executing commands.
    """
    connection = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

    return connection
