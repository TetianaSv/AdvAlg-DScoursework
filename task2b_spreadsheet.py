#task 2b by aidanas alyta

import sys
import os
import csv


#Make sure the library folder is visible to Python

BASE_DIR = os.path.dirname(os.path.abspath(__file__))      # folder of this file
LIB_DIR  = os.path.join(BASE_DIR, "..", "clrsPython")  # path to CLRS library folder

if LIB_DIR not in sys.path:
    sys.path.insert(0, LIB_DIR)


#Import the required algorithms from CLRS library

from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra


#Load data from CSV file

def load_edges_from_csv(file_path):

    #Read the CSV file and extracts valid connections (edges).


    edges = []
    skipped = 0
    dupes = 0

    # Open CSV file for reading
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)  # Skip the header line (column titles)

        for row in reader:
            # Skip rows that don't have enough data
            if len(row) < 4:
                skipped += 1
                continue

            src = row[1].strip()
            dst = row[2].strip()
            mins = row[3].strip()

            # Skip rows with missing info
            if src == "" or dst == "" or mins == "":
                skipped += 1
                continue

            # Try to read the travel time as a number
            try:
                w = float(mins)
            except ValueError:
                skipped += 1
                continue

            # Add connection: (from, to, time)
            edges.append((src, dst, w))


    #Build station list and give each one a number

    stations = []
    seen = set()
    for u, v, _ in edges:
        if u not in seen:
            seen.add(u)
            stations.append(u)
        if v not in seen:
            seen.add(v)
            stations.append(v)

    id_by_name = {name.upper(): i for i, name in enumerate(stations)}  # name → number
    name_by_id = {i: name for i, name in enumerate(stations)}          # number → name


    #Create graph (the map)

    G = AdjacencyListGraph(len(stations), directed=False, weighted=True)

    for u_name, v_name, w in edges:
        u = id_by_name[u_name.upper()]
        v = id_by_name[v_name.upper()]
        # Avoid adding same edge twice
        if not G.has_edge(u, v):
            G.insert_edge(u, v, w)
        else:
            dupes += 1

    return G, id_by_name, name_by_id, skipped, dupes



#Rebuild path from Dijkstra’s output

def reconstruct_path(pi, s, t):
    path = []
    cur = t
    while cur is not None:
        path.insert(0, cur)
        if cur == s:
            break
        cur = pi[cur]
    return path


#Main interactive part

def main():
    # CSV file name (must be in the same folder)
    file_path = os.path.join(BASE_DIR, "london_underground_data.csv")

    print("Loading:", file_path)
    G, id_by_name, name_by_id, skipped, dupes = load_edges_from_csv(file_path)

    print("Stations:", G.get_card_V(), " | Connections:", G.get_card_E())
    print("Skipped rows:", skipped, " | Duplicates ignored:", dupes)
    print("")
    print("Type two station names to find the fastest route (blank to quit).")

    while True:
        src = input("Start station: ").strip()
        if src == "":
            break
        dst = input("Destination station: ").strip()
        if dst == "":
            break

        s_key = src.upper()
        t_key = dst.upper()

        # Make sure both stations exist
        if s_key not in id_by_name or t_key not in id_by_name:
            print("Unknown station name.")
            continue
        if s_key == t_key:
            print("Start and destination are the same.")
            continue

        s = id_by_name[s_key]
        t = id_by_name[t_key]

        # Run Dijkstra’s algorithm to find shortest travel times
        d, pi = dijkstra(G, s)

        # Reconstruct route from station IDs
        path_ids = reconstruct_path(pi, s, t)

        if len(path_ids) == 0 or d[t] == float('inf'):
            print("No path found.")
        else:
            path_names = [name_by_id[i] for i in path_ids]
            print("Route:", " -> ".join(path_names))
            print("Total time:", str(d[t]), "minutes")
        print("")

if __name__ == "__main__":
    main()
