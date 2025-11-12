#task 2b testing generated stations by aidanas alyta

import sys
import os
import random
import time


#Make sure the folder with the provided CLRS libraries can be found.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))           
LIB_DIR = os.path.join(BASE_DIR, "..", "clrsPython")    

if LIB_DIR not in sys.path:
    sys.path.insert(0, LIB_DIR)


# library import

from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra



# build a random connected undirected weighted graph

def build_random_connected_graph(n, avg_degree=6, w_min=1, w_max=10, rng=None):
    if rng is None:
        rng = random.Random()

    G = AdjacencyListGraph(n, directed=False, weighted=True)

    # connect each new station to a random earlier one to keep the graph connected
    for i in range(1, n):
        j = rng.randrange(0, i)
        w = rng.randint(w_min, w_max)
        G.insert_edge(j, i, w)

    # add extra random edges until we reach the desired density
    target_edges = int(n * avg_degree / 2.0)
    current_edges = G.get_card_E()
    attempts = 0

    while current_edges < target_edges and attempts < n * n:
        u = rng.randrange(0, n)
        v = rng.randrange(0, n)
        if u != v and not G.has_edge(u, v):
            w = rng.randint(w_min, w_max)
            try:
                G.insert_edge(u, v, w)
                current_edges += 1
            except RuntimeError:
                pass
        attempts += 1

    return G



# pick two different random station numbers

def pick_distinct_pair(n, rng):
    s = rng.randrange(0, n)
    t = rng.randrange(0, n - 1)
    if t >= s:
        t += 1
    return s, t



# turn predecessor list into an ordered path

def reconstruct_path(pi, s, t):
    path = []
    cur = t
    while cur is not None:
        path.insert(0, cur)
        if cur == s:
            break
        cur = pi[cur]
    return path


# main benchmarking function

def benchmark_dijkstra(ns, trials_per_n=200, avg_degree=6, w_min=1, w_max=10, seed=42):
    rng = random.Random(seed)

    print("=======================================================================")
    print("TASK 2b: Measuring Dijkstra's Performance on Random Tube Networks")
    print("=======================================================================")
    print("Average degree:", avg_degree, "| weight range:", w_min, "-", w_max,
          "| trials per network:", trials_per_n, "| seed:", seed)
    print("-----------------------------------------------------------------------")
    print("Columns: Stations, Edges, Average Time (ms)")
    print("-----------------------------------------------------------------------")

    for n in ns:
        # build random connected graph
        G = build_random_connected_graph(n, avg_degree=avg_degree,
                                         w_min=w_min, w_max=w_max, rng=rng)
        m = G.get_card_E()

        # measure Dijkstra average time
        times = []
        for _ in range(trials_per_n):
            s, t = pick_distinct_pair(n, rng)
            t_start = time.perf_counter()
            d, pi = dijkstra(G, s)
            t_end = time.perf_counter()
            elapsed_ms = (t_end - t_start) * 1000.0
            times.append(elapsed_ms)

        avg_ms = sum(times) / float(len(times))

        # print average results
        print(str(n) + " , " + str(m) + " , " + str(round(avg_ms, 3)))





# test with different amount of stations

if __name__ == "__main__":
    sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

    benchmark_dijkstra(
        ns=sizes,
        trials_per_n=200,
        avg_degree=6,
        w_min=1,
        w_max=10,
        seed=42
    )
