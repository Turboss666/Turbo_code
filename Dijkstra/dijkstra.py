from heapq import heappop, heappush
from math import inf

graph = {
        'A': [('B', 10), ('C', 3)],
        'C': [('D', 2)],
        'D': [('E', 10)],
        'E': [],
        'B': [('C', 3), ('D', 2)]
    }
## Finds shorthest path from start to all other vertices 
def djikstra(graph,start):
    distance = {}
    for vertex in graph:
        if vertex == start:
            distance[vertex] = 0
        else:
            distance[vertex] = inf

    vertex_to_explore = [(start,0)]
    while vertex_to_explore:
        print(vertex_to_explore)
        vertex_being_explored, current_distance = heappop(vertex_to_explore)
        for neighbor, weight in graph[vertex_being_explored]:
            new_distance = weight + current_distance
            if new_distance <= distance[neighbor]:
                distance[neighbor] = new_distance
                heappush(vertex_to_explore,(neighbor, new_distance))
    
    print(distance)
                
djikstra(graph,'B')