import random
import time
import pandas as pd
from adjacency_list_graph import AdjacencyListGraph
from bfs import bfs
from print_path import print_path
import matplotlib.pyplot as plt

#Generate a random undirected graph with n vertices:
def gen_random_g(n: int, edge_probability: float = 0.05) -> AdjacencyListGraph:
    G = AdjacencyListGraph(n)
    #go over all unordered pairs of vertices (u, v) with u<v
    for u in range(n):
        for v in range(u + 1, n):
            #add an undirected edge with the probability
            if random.random() < edge_probability:
                G.insert_edge(u, v)
                G.insert_edge(v, u)
    return G

#Measuring of the average running time of BFS on graph G. Function must return the average time over all trials:
def av_bfs_time(G: AdjacencyListGraph, trials: int = 50) -> float:
    n = G.get_card_V()
    total = 0.0
    for _ in range(trials):
        src = random.randrange(n)     #pick a random source vertex
        t0 = time.time()     #measure the time to run BFS
        _dist, _pred = bfs(G, src)
        total += (time.time() - t0)
    return total / trials     #get the average running time

#generate a randon graph with the edge probability, measure the average BFS running time
def empirical_performance(sizes = tuple(range(100, 1001, 100)),
                          edge_probability: float =0.05,
                          trials: int = 50):
    results =[]
    for n in sizes:
        G = gen_random_g(n, edge_probability=edge_probability) #generate a random graph
        avt_t = av_bfs_time(G, trials=trials) #measure the average BFS running time
        print(f"n={n}, average BFS time={avt_t:.6f} sec")
        results.append((n, avt_t)) #store the pair (size, time)
    return results

#Construct a graph with London underground loaded data
def load_London_underground(file_path: str):
    df = pd.read_excel(file_path, header=None) #read the Excel file using Pandas
    if df.shape[1] < 3:
        raise ValueError("at least 3 columns") #check if data has 3 columns for correct work

    df.columns = ['Line', 'Station', 'Next_station'] +list(df.columns[3:]) #rename columns
    df = df.dropna(subset=['Station', 'Next_station']) #make data clean

    # collect all station names, convert it to a sorted list
    stations = sorted(set(df['Station']).union(df['Next_station']))
    station2id = {name: i for i, name in enumerate(stations)} #create dictionary
    id2station = stations #dictionary for reverse

    G = AdjacencyListGraph(len(stations))
    seen = set() #track inserted edges
    for _, row in df.iterrows(): #go over each row of the DataFrame
        u = station2id[row['Station']]
        v = station2id[row['Next_station']]
        if u == v:
            continue #skip self-loops
        a, b = (u, v) if u < v else (v, u) #normalize a, b to have always a<b
        if (a, b) in seen:
            continue
        seen.add((a, b))
        G.insert_edge(a, b)
        G.insert_edge(b, a) #insert edge by adding both directions

    return G, station2id, id2station

#Find and print the shortest path between 2 given station
def shortest_path(G, station2id, id2station, start_name: str, end_name: str):
    if start_name not in station2id or end_name not in station2id: #check given stations exist
        raise KeyError("Station not found")

    s = station2id[start_name]
    t = station2id[end_name]
    dist, pred = bfs(G, s) #run BFS

    if dist[t] == float('inf'):
        print(f"No path between '{start_name}' and '{end_name}'.")
        return
    path_labels = print_path(pred, s, t, lambda i: id2station[i]) #path from s to t using the predecessor array `pred`
    print(f"Fewest-stops from {start_name} and {end_name}:")
    print("->".join(path_labels))
    print(f"Number of stops: {dist[t]}")

if __name__ == "__main__":
    print("Empirical Performance Measurement:")
    #Call the empirical_performance function to measure the execution time of BFS
    results = empirical_performance(sizes=range(100, 1001,100), edge_probability=0.05, trials=50)
    print("\nLondon Underground Shortest Paths:")
    excel_path = 'London Underground data.xlsx'
    G_LU, station2id, id2station = load_London_underground(excel_path)
    #Calculate and print the route with the fewest-stops between the two given stations
    shortest_path(G_LU, station2id, id2station, "Covent Garden", "Leicester Square")
    shortest_path(G_LU, station2id, id2station, "Wimbledon", "Stratford")


outputs = empirical_performance(
    sizes=range(100, 1001, 100),
    edge_probability=0.05,
    trials=50
)
n_values = [n for n, t in outputs]
times = [t for n, t in outputs]

plt.plot(n_values, times, marker="o")
plt.xlabel("Number of stations (n)")
plt.ylabel("Average BFS execution time (sec)")
plt.title("Empirical BFS Performance on Random Graphs")
plt.grid(True)
plt.show()