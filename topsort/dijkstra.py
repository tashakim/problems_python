from heappriorityqueue import *
from mygraph import *

def dijkstra(g, src):
    """ Calculate the shortest path tree from the src in the input
    connected graph g using Dijkstra's algorithm. The elements attached
    to the edges should be the distances. Must run in O((|E| + |V|) log |V|)
    time using the provided HeapPriorityQueue data structure.

    Returns the shortest path tree in the form of a new MyGraph object.
    Do not modify the input MyGraph instance.

    Raise the InvalidInputException if input is None or if src is not in g.

    Note: To access the actual vertices in the HeapPriorityQueue,
    you need to call pop().value(), not just pop().
    """
    for v in g.vertices():
        # sets distance of all vertices to a very large value.
        v.distance = float('inf')
    src.distance = 0

    order = []ß
    order.append(src)
    
    while order is not None:
        visited = order.pop(0)
        for edge in g.incidentEdges(visited):
            adjacent = g.opposite(visited, edge)
            order.append(adjacent)
            g.removeEdge(edge)

            if(adjacent.distance > visited.distance +1):
                #updates adjacent node's distance
                adjacent.distance = visited.distance +1
            else: 
                return
    return MyGraph()


class InvalidInputException(Exception):
    def __str__(self):
        return "Invalid Input Given."
