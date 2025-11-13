from adjacency_list_graph import AdjacencyListGraph
from bfs import bfs
from print_path import print_path

def create_graph_from_dict(graph_dict):
    """converts dictionary graph format to adjacency list graph used by library code"""
    #get all stations and sort them for consistent numbering
    stations = sorted(set(graph_dict.keys()).union(*[set(connections) for connections in graph_dict.values()]))
    station_to_id = {station: i for i, station in enumerate(stations)}
    
    #create undirected graph 
    graph = AdjacencyListGraph(len(stations), directed=False, weighted=False)
    
    #add all connections to the graph
    for station, connections in graph_dict.items():
        for connected_station in connections:
            # only add each connection once to avoid duplicates
            if station_to_id[station] < station_to_id[connected_station]:
                try:
                    graph.insert_edge(station_to_id[station], station_to_id[connected_station])
                except RuntimeError:
                    # connection already exists, skip it
                    pass
    return graph, stations, station_to_id

def display_all_possible_routes(graph, stations):
    """show all available routes in the network for reference"""
    print("Possible routes in network:\n")
    for i, station in enumerate(stations):
        connected_stations = []
        for connection in graph.get_adj_list(i):
            connected_stations.append(stations[connection.get_v()])
        print(f"{station} -> {', '.join(connected_stations)}")
    print()

def main():
    """main function to run the journey planner"""
    #network data with stations A-G and their connections
    network_data = {
        'A': ['B', 'C'],
        'B': ['A', 'D'],
        'C': ['A', 'D', 'F'],
        'D': ['B', 'C', 'E'],
        'E': ['D', 'G'],
        'F': ['C', 'G'],
        'G': ['E', 'F']
    }
    
    print("Journey Planner For Least Stops\n")
    
    #convert our network data to textbook graph format
    graph, stations, station_to_id = create_graph_from_dict(network_data)
    
    #show network map to user
    display_all_possible_routes(graph, stations)
    
    #user inputs start and destination
    print("Enter your journey details:")
    start_station = input("Starting station: ").upper().strip()
    end_station = input("Destination station: ").upper().strip()
    
    #check if stations exist in network
    if start_station not in station_to_id or end_station not in station_to_id:
        print("Error: Please enter valid stations")
        return
    
    print(f"\nFinding shortest route from {start_station} to {end_station}...\n")
    
    #use BFS to find shortest path
    start_id = station_to_id[start_station]
    end_id = station_to_id[end_station]
    
    distances, predecessors = bfs(graph, start_id)
    
    #check if route exists
    if distances[end_id] == float('inf'):
        print("No route found between these stations!")
        return
    
    #build the actual route using path function
    route_stations = print_path(predecessors, start_id, end_id, lambda i: stations[i])
    
    #show results to user
    if route_stations:
        print(f"Shortest route: {' > '.join(route_stations)}")
        print(f"Number of stops: {distances[end_id]}")
        print(f"Stations visited: {len(route_stations)}")
        
        #show step-by-step journey
        print("\nJourney breakdown:")
        for i, station in enumerate(route_stations):
            if i == 0:
                print(f"Start at {station}")
            elif i == len(route_stations) - 1:
                print(f"Arrive at {station}")
            else:
                print(f"Stop {i}: {station}")
    else:
        print("No route found between these stations!")

def verification():
    """test the system works with known route"""
    print("Verification:")
    network_data = {
        'A': ['B', 'C'],
        'B': ['A', 'D'],
        'C': ['A', 'D', 'F'],
        'D': ['B', 'C', 'E'],
        'E': ['D', 'G'],
        'F': ['C', 'G'],
        'G': ['E', 'F']
    }
    
    graph, stations, station_to_id = create_graph_from_dict(network_data)
    
    start = 'A'
    destination = 'G'
    
    start_id = station_to_id[start]
    destination_id = station_to_id[destination]
    
    distances, predecessors = bfs(graph, start_id)
    
    if distances[destination_id] != float('inf'):
        route_stations = print_path(predecessors, start_id, destination_id, lambda i: stations[i])
        print(f"Shortest route from {start} to {destination}: {' > '.join(route_stations)}")
        print(f"Total number of stops: {distances[destination_id]}")
    else:
        print("No route found!")

if __name__ == "__main__":
    #run verification test
    verification()
    print("\n" + "="*50 + "\n")
    
    #run main program

    main()
