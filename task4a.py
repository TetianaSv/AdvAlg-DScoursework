from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal, get_total_weight

#Returns a list of edges that form the MST.
#The element of each edge in g is assumed to be its weight
def original_graph():
    g = AdjacencyListGraph(7, False, True)

    g.insert_edge(0, 6, 1)
    g.insert_edge(2, 3, 1)
    g.insert_edge(1, 6, 2)
    g.insert_edge(1, 2, 3)
    g.insert_edge(2, 6, 3)
    g.insert_edge(0, 1, 4)
    g.insert_edge(3, 4, 4)
    g.insert_edge(3, 6, 5)
    g.insert_edge(4, 6, 5)
    g.insert_edge(0, 5, 5)
    g.insert_edge(4, 5, 6)
    g.insert_edge(5, 6, 6)

    return g

def main():
    g = original_graph()
    mst = kruskal(g) #compute MST using CLRS

    print("Edges in the MST")
    total_weight = get_total_weight(mst) #compute the total weight of the MST
    for u in range(mst.get_card_V()): #iterate through all vertices of the MST
        for edge in mst.get_adj_list(u): #for each vertex, iterate through its adjacency list
            v = edge.get_v()
            if u < v: #Since the graph is undirected, each edge appears twice
                print(f"{u+1} - {v+1} (weight{edge.get_weight()})") #We print the edge only once, ensuring u < v.
    print(f"Total MST weight:{total_weight}")

if __name__ == "__main__":
    main()

