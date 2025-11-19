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
    mst = kruskal(g)

    print("Edges in the MST")
    total_weight = get_total_weight(mst)
    for u in range(mst.get_card_V()):
        for edge in mst.get_adj_list(u):
            v = edge.get_v()
            if u < v:
                print(f"{u+1} - {v+1} (weight{edge.get_weight()})")
                total_weight +=edge.get_weight()
    print(f"Total MST weight:{total_weight}")

if __name__ == "__main__":
    main()

