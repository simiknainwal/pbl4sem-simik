import heapq
import math

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
        self.blocked_edges: set[tuple[int, int]] = set()

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

    def found(self) -> bool:
        return self.distance != INT_MAX and len(self.path) > 0


class PathFinder:
    @staticmethod
    def find_shortest_path(graph: Graph, source: int, destination: int) -> PathResult:
        """Dijkstra's algorithm — direct port of PathFinder.cpp."""
        vertices = graph.get_number_of_nodes()
        distance = [INT_MAX] * vertices
        parent = [-1] * vertices

        # min-heap: (distance, node)
        pq = []
        distance[source] = 0
        heapq.heappush(pq, (0, source))

        while pq:
            d, u = heapq.heappop(pq)
            if u == destination:
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
        result.distance = distance[destination]

        if distance[destination] == INT_MAX:
            return result  # no path

        # Reconstruct path
        current = destination
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
        graph.set_node_name(lines[idx], i); idx += 1

    num_edges = int(lines[idx]); idx += 1
    original_weights: dict[tuple[int, int], int] = {}

    for _ in range(num_edges):
        parts = lines[idx].split(); idx += 1
        u, v, w = int(parts[0]), int(parts[1]), int(parts[2])
        graph.add_edge(u, v, w)
        original_weights[(min(u, v), max(u, v))] = w

    src_dst = lines[idx].split()
    source, destination = int(src_dst[0]), int(src_dst[1])

    return graph, source, destination, original_weights


def build_default_graph() -> tuple:
    """Returns the sample building from input.txt."""
    content = """6
Lobby
Hallway A
Hallway B
Lab
Server Room
EXIT
8
0 1 2
0 2 10
1 2 5
1 3 3
2 4 1
3 4 8
3 5 6
4 5 4
0 5"""
    return parse_input_file(content)
