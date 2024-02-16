from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class Node:
    name: str
    type: str
    ip: str
    port: int
    cpu_usage: float = 0.0  # Percentage
    ram_usage: float = 0.0  # GB
    disk_usage: float = 0.0  # GB
    retention_time_hours: Optional[int] = None  # Retention time in hours
    rps: Optional[float] = None  # Requests Per Second
    qps: Optional[float] = None  # Queries Per Second
    tps: Optional[float] = None  # Transactions Per Second
    additional_metrics: Dict[str, float] = field(default_factory=dict)


@dataclass
class SpringBootMicroservice(Node):
    type: str = "SpringBootMicroservice"
    actuator_health: Optional[str] = None  # Health endpoint status


@dataclass
class NodejsService(Node):
    type: str = "NodejsService"
    event_loop_latency: Optional[float] = None  # Milliseconds


@dataclass
class PostgreSQLInstance(Node):
    type: str = "PostgreSQLInstance"
    active_connections: Optional[int] = None


@dataclass
class RedisInstance(Node):
    type: str = "RedisInstance"
    connected_clients: Optional[int] = None


@dataclass
class MongoDBInstance(Node):
    type: str = "MongoDBInstance"
    collections_count: Optional[int] = None
