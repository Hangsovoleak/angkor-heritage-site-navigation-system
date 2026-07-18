import math

class Graph:
    def __init__(self, N):
        self.N = N
        self.adj_matrix = [[0] * N for _ in range(N)]
        self.vertex_data = [''] * N

        # Store Dijkstra results
        self.distances = []
        self.previous = []
        self.start = None

    # Graph Functions

    def add_edge(self, u, v, weight):
        self.adj_matrix[u][v] = weight
        self.adj_matrix[v][u] = weight

    def display(self):
        print("Adjacency Matrix")
        for row in self.adj_matrix:
            print(row)

    # 1. Run Dijkstra

    def dijkstra(self, start):
        self.start = start

        self.distances = [math.inf] * self.N
        self.previous = [None] * self.N

        self.distances[start] = 0

        visited = [False] * self.N

        for _ in range(self.N):

            # Find the unvisited vertex with minimum distance
            min_distance = math.inf
            min_vertex = -1

            for v in range(self.N):
                if not visited[v] and self.distances[v] < min_distance:
                    min_distance = self.distances[v]
                    min_vertex = v

            if min_vertex == -1:
                break

            visited[min_vertex] = True

            # Update neighbors
            for neighbor in range(self.N):

                weight = self.adj_matrix[min_vertex][neighbor]

                if weight > 0 and not visited[neighbor]:

                    new_distance = self.distances[min_vertex] + weight

                    if new_distance < self.distances[neighbor]:
                        self.distances[neighbor] = new_distance
                        self.previous[neighbor] = min_vertex

        return self.distances, self.previous

    # 2. Get Distance to One Temple

    def get_distance(self, destination):

        if self.distances == []:
            print("Run Dijkstra first.")
            return

        return self.distances[destination]

    # 3. Get All Distances

    def get_all_distances(self):

        if self.distances == []:
            print("Run Dijkstra first.")
            return

        print("\nShortest Distances\n")

        for i in range(self.N):
            print(f"{self.vertex_data[i]:20} : {self.distances[i]} km")

    # 4. Get Shortest Path

    def get_shortest_path(self, destination):

        if self.previous == []:
            print("Run Dijkstra first.")
            return

        path = []

        current = destination

        while current is not None:
            path.append(current)
            current = self.previous[current]

        path.reverse()

        return path

    # 5. Display Shortest Path

    def display_shortest_path(self, destination):

        path = self.get_shortest_path(destination)

        print("\n========== Shortest Path ==========\n")

        for i in range(len(path)):
            print(self.vertex_data[path[i]], end="")

            if i != len(path) - 1:
                print(" -> ", end="")

        print()

        print(f"\nTotal Distance : {self.distances[destination]} km")
        
g = Graph(7)

g.vertex_data = [
    "Temple 0",
    "Temple 1",
    "Temple 2",
    "Temple 3",
    "Temple 4",
    "Temple 5",
    "Temple 6"
]

g.add_edge(0,1,2)
g.add_edge(0,2,6)
g.add_edge(1,3,5)
g.add_edge(2,3,8)
g.add_edge(3,4,10)
g.add_edge(3,5,15)
g.add_edge(4,5,6)
g.add_edge(4,6,2)
g.add_edge(5,6,6)

# Start at Temple 3
g.dijkstra(3)

# Show all shortest distances
g.get_all_distances()

# Show one distance
print("\nDistance to Temple 6")
print(g.get_distance(6), "km")

# Show shortest path
g.display_shortest_path(6)