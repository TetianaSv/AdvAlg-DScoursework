import random
import time
import pandas as pd
from fontTools.misc.cython import returns
from numpy.ma.extras import average
from openpyxl.styles.builtins import total

from adjacency_list_graph import AdjacencyListGraph
from bfs import bfs
from print_path import print_path
from task3a import path_labels


def gen_random_g(n: int, edge_probability: float = 0.05) -> AdjacencyListGraph:
    G = AdjacencyListGraph(n)
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < edge_probability:
                G.insert_edge(u, v)
                G.insert_edge(v, u)
    return G

def av_bfs_time(G: AdjacencyListGraph, trials: int = 50) -> float:
    n = G.get_card_V()
    total = 0.0
    for _ in range(trials):
        src = random.randrange(n)
        t0 = time.time()
        _dist, _pred = bfs(G, src)
        total += (time.time() - t0)
    return total / trials

def empirical_performance(sizes = tuple(range(100, 1001, 100)),
                          edge_probability: float =0.05,
                          trials: int = 50):

    results =[]
    for n in sizes:
        G = gen_random_g(n, edge_probability=edge_probability)
        avt_t = av_bfs_time(G, trials=trials)
        print(f"n={n}, average BFS time={avt_t:.6f} sec")
        results.append((n, avt_t))
    return results


def load_London_undegraund(file_path: str):
    df = pd.read_excel(file_path, header=None)
    if df.shape[1] < 3:
        raise ValueError("at least 3 columns")

    df.columns = ['Line', 'Station', 'Next_station'] +list(df.columns[3:])
    df = df.dropna(subset=['Station', 'Next_station'])

    stations = sorted(set(df['Station']).union(df['Next_station']))
    station2id = {name: i for i, name in enumerate(stations)}
    id2station = stations

    G = AdjacencyListGraph(len(stations))
    seen = set()
    for _, row in df.iterrows():
        u = station2id[row['Station']]
        v = station2id[row['Next_station']]
        if u == v:
            continue
        a, b = (u, v) if u < v else (v, u)
        if (a, b) in seen:
            continue
        seen.add((a, b))
        G.insert_edge(a, b)
        G.insert_edge(b, a)

    return G, station2id, id2station


def shortest_path(G, station2id, id2station, start_name: str, end_name: str):
    if start_name not in station2id or end_name not in station2id:
        raise KeyError("Station not found")

    s = station2id[start_name]
    t = station2id[end_name]
    dist, pred = bfs(G, s)

    if dist[t] == float('inf'):
        print(f"No path between '{start_name}' and '{end_name}'.")
        return
    path_labels = print_path(pred, s, t, lambda i: id2station[i])
    print(f"Fewert-stops from {start_name} and {end_name}:")
    print("->".join(path_labels))
    print(f"Number of stops: {dist[t]}")


if __name__ == "__main__":
    print("Empirical Perfomance Measurement:")
    results = empirical_performance(sizes=range(100, 1001,100), edge_probability=0.05, trials=50)

    print("\nLondon Underground Shortest Paths:")
    excel_path = 'London Underground data.xlsx'
    G_LU, station2id, id2station = load_London_undegraund(excel_path)
    shortest_path(G_LU, station2id, id2station, "Covent Garden", "Leicester Square")
    shortest_path(G_LU, station2id, id2station, "Wimbledon", "Stratford")

