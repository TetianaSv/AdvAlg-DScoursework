#task 4b
#Aidanas Alyta

import random
import time
import pandas as pd
import matplotlib.pyplot as plt

#import required libraries
from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal, get_total_weight
#dijkstra will be used for impact analysis for comparing task2b long journey (Uxbridge to Upminster)
from dijkstra import dijkstra

#Data generation
def build_random_connected_graph(num_stations, extra_edge_probability=0.02):

    G = AdjacencyListGraph(num_stations, directed=False, weighted=True)
    #linking each new station to a previous one
    for v in range(1, num_stations):
        u = random.randint(0, v - 1)     # connect v to some earlier station
        w = random.randint(1, 10)     # random weight
        G.insert_edge(u, v, w)

    #add extra random edges
    for u in range(num_stations):
        for v in range(u + 1, num_stations):
            if not G.has_edge(u, v):
                if random.random() < extra_edge_probability:
                    w = random.randint(1, 10)
                    G.insert_edge(u, v, w)

    return G

#measuring average compute time function
def measure_average_backbone_time(num_stations, trials=10):

    total_time = 0.0
    valid_trials = 0

    for _ in range(trials):

        G = build_random_connected_graph(num_stations)
        start = time.perf_counter()
        _ = kruskal(G)   # compute the core backbone
        end = time.perf_counter()

        total_time += (end - start)
        valid_trials += 1

    if valid_trials == 0:
        return 0.0

    average_time = total_time / valid_trials
    return average_time

def run_empirical_measurement():

    #Part 1 of 4b: measure time for different n and plot average time vs n.
    print("=== Task 4b: Empirical Performance Measurement ===")
    print("Stations | Time in ms")

    ns = []
    times_ms = []

    for n in range(100, 1100, 100):  # 100, 200, ..., 1000
        avg_time = measure_average_backbone_time(n, trials=10)
        avg_ms = round(avg_time * 1000, 3)
        ns.append(n)
        times_ms.append(avg_ms)
        print(str(n) + "\t\t" + str(avg_ms))

    # Plot average time vs n
    plt.figure()
    plt.plot(ns, times_ms, marker='o')
    plt.xlabel("Number of stations (n)")
    plt.ylabel("Average MST time (ms)")
    plt.title("Empirical MST running time vs network size n")
    plt.grid(True)
    # plt.show()

    #Part 2
def collect_undirected_edges(G):
    # turn an undirected graph into a list of edges (u, v, w), with u < v so each edge appears only once.
    edges = []
    V = G.get_card_V()
    for u in range(V):
        for edge in G.get_adj_list(u):
            v = edge.get_v()
            w = edge.get_weight()
            if u < v:
                edges.append((u, v, w))
    return edges

def print_edges(title, edges, name_by_id):
    print(title)
    if len(edges) == 0:
        print("  (none)")
        return
    for (u, v, w) in edges:
        print("  " + name_by_id[u] + " - " + name_by_id[v] + "  (weight = " + str(w) + ")")


# path reconstruction helper for impact analysis
def reconstruct_path(predecessors, s, t):
    # rebuild path from s to t using predecessor list
    path = []
    cur = t
    while cur is not None:
        path.insert(0, cur)
        if cur == s:
            break
        cur = predecessors[cur]
    if len(path) == 0 or path[0] != s:
        return []
    return path

def load_underground_excel (path):
    df = pd.read_excel(path)

    edges = []
    for _, row in df.iterrows():
        u = str(row[1]).strip()
        v = str(row[2]).strip()
        w = (row[3])
        if pd.isna(u) or pd.isna(v) or pd.isna(w):
            continue
        edges.append((u, v, float(w)))

    stations = sorted(set([u for u,_,_ in edges] + [v for _,v,_ in edges]))
    id_by_name = {name.upper(): i for i, name in enumerate(stations)}
    name_by_id = {i: name for i, name in enumerate(stations)}

    G = AdjacencyListGraph(len(stations), directed=False, weighted=True)

    for (u_name, v_name, w) in edges:
        u = id_by_name[u_name.upper()]
        v = id_by_name [v_name.upper()]

        if not G.has_edge(u, v):
            G.insert_edge(u, v, w)

    return G, id_by_name, name_by_id

def run_london_application():

    # Part 2 of 4b: Core backbone for London Underground + redundant edges + impact analysis.
    print("\n=== Task 4b: Application to London Underground Data ===\n")

    excel_path = 'London Underground data.xlsx'
    G, id_by_name, name_by_id = load_underground_excel(excel_path)

    all_edges = collect_undirected_edges(G)
    print("Total stations (vertices): " + str(G.get_card_V()))
    print("Total connections (edges): " + str(len(all_edges)))
    print("\n")

    # 1) MST (core backbone)
    mst_graph = kruskal(G)
    mst_edges = collect_undirected_edges(mst_graph)
    mst_weight = get_total_weight(mst_graph)

    print("Core backbone using MST")
    print("Number of backbone edges: " + str(len(mst_edges)))
    print("Total journey time (total backbone weight): " + str(mst_weight))
    print("")

    # 2) Redundant edges = all edges - MST edges
    mst_pairs = set((u, v) for (u, v, w) in mst_edges)
    all_pairs = set((u, v) for (u, v, w) in all_edges)

    weight_lookup = {}
    for (u, v, w) in all_edges:
        weight_lookup[(u, v)] = w

    redundant_pairs = sorted(list(all_pairs - mst_pairs))
    redundant_edges = [(u, v, weight_lookup[(u, v)]) for (u, v) in redundant_pairs]

    print("Total redundant connections that can be closed: " + str(len(redundant_edges)))
    print("")
    print("Redundant connections")
    r = 10  # show first 10 redundant connections
    to_show = redundant_edges[:r]
    print("Displaying", r, "out of", len(redundant_edges), "redundant connections")
    print_edges("These connections can be closed without disrupting the network:", to_show, name_by_id)

    # 3) Impact analysis: compare full network vs backbone-only network
    print("\nImpact analysis on backbone-only network")

    src_name = input("Start station: ").strip()
    if src_name == "":
        print("No journey entered. Finished.")
        return
    dst_name = input("Destination station: ").strip()
    if dst_name == "":
        print("No destination entered. Finished.")
        return

    src_key = src_name.upper()
    dst_key = dst_name.upper()

    if src_key not in id_by_name or dst_key not in id_by_name:
        print("One or both station names are not recognised.")
        return
    if src_key == dst_key:
        print("Start and destination are the same.")
        return

    s = id_by_name[src_key]
    t = id_by_name[dst_key]

    # Shortest path on FULL network
    dist_full, pi_full = dijkstra(G, s)
    path_full_ids = reconstruct_path(pi_full, s, t)

    print("\nOriginal journey result on full network:")
    if len(path_full_ids) == 0 or dist_full[t] == float('inf'):
        print("No path found in full network.")
    else:
        route_full_names = [name_by_id[vid] for vid in path_full_ids]
        print("Route on full network:")
        print("  " + " -> ".join(route_full_names))
        print("Total journey time on full network: " + str(dist_full[t]) + " minutes")

    # Shortest path on BACKBONE-ONLY network
    dist_mst, pi_mst = dijkstra(mst_graph, s)
    path_mst_ids = reconstruct_path(pi_mst, s, t)

    print("\nBackbone-only journey result:")
    if len(path_mst_ids) == 0 or dist_mst[t] == float('inf'):
        print("No path found in backbone-only network.")
    else:
        route_mst_names = [name_by_id[vid] for vid in path_mst_ids]
        print("Route on backbone:")
        print("  " + " -> ".join(route_mst_names))
        print("Total journey time on backbone: " + str(dist_mst[t]) + " minutes")

    # time difference
    if len(path_full_ids) != 0 and dist_full[t] != float('inf') and len(path_mst_ids) != 0 and dist_mst[t] != float('inf'):
        diff = dist_mst[t] - dist_full[t]
        print("\nDifference in journey time (backbone - full): " + str(diff) + " minutes")
        print("Use this in the report to discuss how redundant connections affect efficiency/resilience.")

# MAIN

def main():
    # Part 1: empirical performance
    run_empirical_measurement()

    # Part 2: real London Underground data application
    run_london_application()

if __name__ == "__main__":
    main()