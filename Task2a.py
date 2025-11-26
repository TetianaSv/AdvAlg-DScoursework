# COMP1828 Coursework - Task 2a: Journey Planner Based on Journey Time
# Manual versus Code-Based Execution of a Shortest Path Algorithm

import sys
import os

# Setup path to mandatory library code
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.join(BASE_DIR, "..", "libraries_combined")

if LIB_DIR not in sys.path:
    sys.path.insert(0, LIB_DIR)

# Import required library functions (mandatory as per coursework spec)
from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra


def main():
    """
    Task 2a: Implements shortest path algorithm using Dijkstra's algorithm
    Data Structure: Adjacency List Graph (weighted, undirected)
    Algorithm: Dijkstra's shortest path algorithm

    Justification:
    - Adjacency List is efficient for sparse graphs (O(V+E) space)
    - Dijkstra's algorithm finds shortest paths in O((V+E)log V) time with binary heap
    - Suitable for weighted graphs with non-negative edge weights
    """

    # ===== SIMPLE DATASET CREATION (as per Task 2a specification) =====
    stations = ['A', 'B', 'C', 'D', 'E']

    # Edges: (station1, station2, journey_time_in_minutes)
    edges = [
        ('A', 'B', 1),
        ('A', 'D', 3),
        ('B', 'E', 3),
        ('B', 'C', 4),
        ('D', 'E', 2),
        ('E', 'C', 3)
    ]

    # ===== DATA STRUCTURE SETUP =====
    # Map station names to integer IDs for library compatibility
    id_by_name = {name: i for i, name in enumerate(stations)}
    name_by_id = {i: name for i, name in enumerate(stations)}

    # Create undirected weighted graph using library's AdjacencyListGraph
    num_vertices = len(stations)
    G = AdjacencyListGraph(num_vertices, directed=False, weighted=True)

    # Populate graph with edges
    for u, v, weight in edges:
        u_id = id_by_name[u]
        v_id = id_by_name[v]
        G.insert_edge(u_id, v_id, weight)

    print("=" * 60)
    print("TASK 2a: SHORTEST PATH ALGORITHM (DIJKSTRA)")
    print("=" * 60)
    print("\nSimple Dataset - Stations:", ", ".join(stations))
    print("\nConnections (with journey times in minutes):")
    for u, v, w in edges:
        print(f"  {u} ↔ {v}: {w} minutes")
    print()

    # ===== USER INPUT =====
    src = input("Enter starting station: ").strip().upper()
    dst = input("Enter destination station: ").strip().upper()

    # ===== INPUT VALIDATION =====
    if src not in id_by_name:
        print(f"Error: '{src}' is not a valid station name.")
        return
    if dst not in id_by_name:
        print(f"Error: '{dst}' is not a valid station name.")
        return
    if src == dst:
        print(f"Start and destination are the same station ({src}).")
        return

    # ===== RUN DIJKSTRA'S ALGORITHM (using mandatory library) =====
    src_id = id_by_name[src]
    dst_id = id_by_name[dst]

    # dijkstra returns: (distances, predecessors)
    distances, predecessors = dijkstra(G, src_id)

    # ===== RECONSTRUCT SHORTEST PATH =====
    path = []
    current = dst_id

    # Backtrack from destination to source using predecessor array
    while current is not None:
        path.insert(0, name_by_id[current])
        current = predecessors[current]

    # ===== OUTPUT RESULTS =====
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)

    if len(path) == 0 or distances[dst_id] == float('inf'):
        print(f"No path found from {src} to {dst}.")
    else:
        print(f"Shortest path from {src} to {dst}:")
        print(f"  Route: {' → '.join(path)}")
        print(f"  Total journey time: {distances[dst_id]} minutes")
        print(f"  Number of stops: {len(path) - 1}")

    print("=" * 60)


if __name__ == "__main__":
    main()