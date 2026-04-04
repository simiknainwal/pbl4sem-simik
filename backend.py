import heapq
import math
import os

INT_MAX = math.inf


class Graph:
    """
    Weighted undirected graph stored as an adjacency matrix.
    O(1) edge reads/writes, O(V^2) space — same tradeoff as the C++ version.
    """

    def __init__(self, num_nodes: int):
        self.number_of_nodes = num_nodes
        # Adjacency matrix initialised to 0 (no edge)
        self.adjacency_matrix = [[0] * num_nodes for _ in range(num_nodes)]
        self.node_names = [f"Node {i}" for i in range(num_nodes)]
        self.node_floors = [0] * num_nodes
        self.blocked_edges: set[tuple[int, int]] = set()

    def set_node_floor(self, floor: int, node: int):
        self.node_floors[node] = floor

    def get_node_floor(self, node: int) -> int:
        return self.node_floors[node]

    def add_edge(self, u: int, v: int, wt: int):
        self.adjacency_matrix[u][v] = wt
        self.adjacency_matrix[v][u] = wt

    def block_corridor(self, u: int, v: int):
        self.adjacency_matrix[u][v] = INT_MAX
        self.adjacency_matrix[v][u] = INT_MAX
        self.blocked_edges.add((min(u, v), max(u, v)))

    def unblock_corridor(self, u: int, v: int, original_weight: int):
        self.adjacency_matrix[u][v] = original_weight
        self.adjacency_matrix[v][u] = original_weight
        self.blocked_edges.discard((min(u, v), max(u, v)))

    def set_node_name(self, name: str, node: int):
        self.node_names[node] = name

    def get_node_name(self, node: int) -> str:
        return self.node_names[node]

    def get_edge_weight(self, u: int, v: int):
        return self.adjacency_matrix[u][v]

    def get_number_of_nodes(self) -> int:
        return self.number_of_nodes

    def is_blocked(self, u: int, v: int) -> bool:
        return (min(u, v), max(u, v)) in self.blocked_edges

    def get_all_edges(self) -> list[tuple[int, int, int]]:
        """Returns list of (u, v, weight) for all edges (u < v)."""
        edges = []
        for i in range(self.number_of_nodes):
            for j in range(i + 1, self.number_of_nodes):
                w = self.adjacency_matrix[i][j]
                if w != 0 and w != INT_MAX:
                    edges.append((i, j, w))
        return edges


class PathResult:
    def __init__(self):
        self.distance = INT_MAX
        self.path: list[int] = []
        self.destination_node = -1

    def found(self) -> bool:
        return self.distance != INT_MAX and len(self.path) > 0


class PathFinder:
    @staticmethod
    def find_shortest_path(graph: Graph, source: int, destinations: list[int]) -> PathResult:
        """Dijkstra's algorithm — direct port of PathFinder.cpp, updated for multiple destinations."""
        vertices = graph.get_number_of_nodes()
        distance = [INT_MAX] * vertices
        parent = [-1] * vertices

        # min-heap: (distance, node)
        pq = []
        distance[source] = 0
        heapq.heappush(pq, (0, source))

        best_dest = -1

        while pq:
            d, u = heapq.heappop(pq)
            if u in destinations:
                best_dest = u
                break
            if d > distance[u]:
                continue
            for i in range(vertices):
                weight = graph.get_edge_weight(u, i)
                if weight == INT_MAX or weight == 0:
                    continue
                if distance[u] != INT_MAX and distance[u] + weight < distance[i]:
                    distance[i] = distance[u] + weight
                    parent[i] = u
                    heapq.heappush(pq, (distance[i], i))

        result = PathResult()
        
        if best_dest == -1:
            return result  # no path to any destination

        result.distance = distance[best_dest]
        result.destination_node = best_dest

        # Reconstruct path
        current = best_dest
        while current != -1:
            result.path.append(current)
            current = parent[current]
        result.path.reverse()

        return result


def parse_input_file(content: str) -> Graph:
   
    lines = [l.strip() for l in content.strip().splitlines() if l.strip()]
    idx = 0

    num_nodes = int(lines[idx]); idx += 1
    graph = Graph(num_nodes)

    for i in range(num_nodes):
        parts = lines[idx].split("|")
        name = parts[0].strip()
        floor = int(parts[1].strip()) if len(parts) > 1 else 0
        graph.set_node_name(name, i)
        graph.set_node_floor(floor, i)
        idx += 1

    num_edges = int(lines[idx]); idx += 1
    original_weights: dict[tuple[int, int], int] = {}

    for _ in range(num_edges):
        parts = lines[idx].split(); idx += 1
        u, v, w = int(parts[0]), int(parts[1]), int(parts[2])
        graph.add_edge(u, v, w)
        original_weights[(min(u, v), max(u, v))] = w

    source = int(lines[idx]); idx += 1
    destinations = [int(x) for x in lines[idx].split()]

    return graph, source, destinations, original_weights


def build_default_graph() -> tuple:
    """Returns the sample building from input.txt."""
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input.txt')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return parse_input_file(content)



