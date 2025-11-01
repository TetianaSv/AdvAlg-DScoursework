#importing deque function for BFS from collections library
from collections import deque

#graph dataset with nodes A-G
example_graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A', 'D', 'F'],
    'D': ['B', 'C', 'E'],
    'E': ['D', 'G'],
    'F': ['C', 'G'],
    'G': ['E', 'F']
}

def breadth_first_search(graph, start, destination):
    """
    finds the shortest path via least stops between start and destination in a graph.

    args:
        graph (dict): the graph represented as an adjacency list
        start (str): starting node/station
        destination (str): destination node/station

    returns:
        list: the shortest path from start to destination, or None if no path exists
    """

    #if start and destination are the same
    if start == destination:
        return [start]

    #tracks visited nodes and previous node
    visited = {start: None}
    queue = deque([start])
    
    while queue:
        current_station = queue.popleft()

        #if destination is found, use dictionary to trace path taken
        if current_station == destination:
            path = []
            while current_station is not None:
                path.append(current_station)
                current_station = visited[current_station]
            #returns traced path
            return path[::-1] 
        
        #visits all the adjacent nodes
        for adjacent in graph[current_station]:
            if adjacent not in visited:
                visited[adjacent] = current_station
                queue.append(adjacent)

    #if no path is found
    return None 


def display_all_possible_routes(graph):
    """display all possible routes in the network for reference"""
    print("Possible routes in network:\n")
    for station, connections in graph.items():
        print(f"{station} -> {', '.join(connections)}")
    print()


def main():
    """main function to run the journey planner"""
    print("Journey Planner For Least Stops\n")
    
    #displays network map
    display_all_possible_routes(example_graph)
    
    #gets user input
    print("Enter your journey details:")
    start = input("Starting station: ").upper().strip()
    destination = input("Destination station: ").upper().strip()
    
    #validates input
    if start not in example_graph or destination not in example_graph:
        print("Error: Please enter valid stations")
        return
    
    print(f"\nFinding shortest route from {start} to {destination}...\n")
    
    #finds the shortest path
    route = breadth_first_search(example_graph, start, destination)
    
    #display results
    if route:
        print(f"Shortest route: {' → '.join(route)}")
        print(f"Number of stops: {len(route) - 1}")
        print(f"Stations visited: {len(route)}")
        
        #displays step-by-step journey
        print("\nJourney breakdown:")
        for i, station in enumerate(route):
            if i == 0:
                print(f"Start at {station}")
            elif i == len(route) - 1:
                print(f"Arrive at {station}")
            else:
                print(f"Stop {i}: {station}")
                
    else:
        print("No route found between these stations!")


#verification of BFS
print("Verification:")
if __name__ == "__main__":
    start = 'A'
    destination = 'G'
    
    route = breadth_first_search(example_graph, start, destination)
    
    if route:
        print(f"Shortest route from {start} to {destination}: {' -> '.join(route)}")
        print(f"Total number of stops: {len(route) - 1}")
    else:
        print("No route found!")

print("\n \n")

#runs main
if __name__ == "__main__":
    main()