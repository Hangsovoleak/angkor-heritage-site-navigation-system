"""
graph.py
A weighted, undirected graph representing distances (km) between temples,
plus Dijkstra's algorithm to compute the shortest route between two of them.
"""

import heapq


class Graph:
    def __init__(self):
        self.adjacency = {}

    def add_temple(self, name):
        self.adjacency.setdefault(name, {})

    def add_edge(self, temple_a, temple_b, distance_km):
        self.add_temple(temple_a)
        self.add_temple(temple_b)
        self.adjacency[temple_a][temple_b] = distance_km
        self.adjacency[temple_b][temple_a] = distance_km

    def edge_weight(self, temple_a, temple_b):
        """Direct distance (km) if two temples are directly connected, else None."""
        return self.adjacency.get(temple_a, {}).get(temple_b)

    def dijkstra(self, start, end):
        """
        Returns (path, total_distance): path is the list of temple names
        from start to end with the smallest total weight. Returns
        (None, float('inf')) if no route exists.
        """
        if start not in self.adjacency or end not in self.adjacency:
            return None, float("inf")

        distances = {node: float("inf") for node in self.adjacency}
        previous = {node: None for node in self.adjacency}
        distances[start] = 0
        visited = set()
        priority_queue = [(0, start)]

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_node in visited:
                continue
            visited.add(current_node)

            if current_node == end:
                break

            for neighbor, weight in self.adjacency[current_node].items():
                if neighbor in visited:
                    continue
                candidate_distance = current_distance + weight
                if candidate_distance < distances[neighbor]:
                    distances[neighbor] = candidate_distance
                    previous[neighbor] = current_node
                    heapq.heappush(priority_queue, (candidate_distance, neighbor))

        if distances[end] == float("inf"):
            return None, float("inf")

        path = []
        node = end
        while node is not None:
            path.append(node)
            node = previous[node]
        path.reverse()

        return path, distances[end]