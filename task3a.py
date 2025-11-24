#Task 3a - Fewest Stops Journey Planer
from adjacency_list_graph import AdjacencyListGraph
from bfs import bfs
from print_path import print_path

G = {
    "A": ["B"],
    "B": ["A", "C", "D"],
    "C": ["B", "D"],
    "D": ["C", "E", "B"],
    "E": ["D"]
}

names = ["A", "B", "C", "D", "E"]
name2id = {name: i for i, name in enumerate(names)}

graph = AdjacencyListGraph(len(names))

for u in G:
    for v in G[u]:
        if name2id[u] < name2id[v]:
            graph.insert_edge(name2id[u], name2id[v])
            graph.insert_edge(name2id[v], name2id[u])

start = name2id["A"]
goal = name2id["E"]

dist, pred = bfs(graph, start)

if dist[goal] == float('inf'):
    print("Path not found")
else:
    print(f"Number of stops: {dist[goal]}")
    path_labels = print_path(pred, start, goal, lambda i: names[i])
    print("Route:", " -> ".join(path_labels))