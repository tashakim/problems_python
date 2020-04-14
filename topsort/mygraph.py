class NoSuchEdgeException(Exception):
    """This exception is raised when, even though all the edges/vertices
    passed in are valid, there is still no way to retrieve
    the edge requested"""
    pass

class NoSuchVertexException(Exception):
    """This exception is raised when, even though all the edges/vertices
    passed in are valid, there is still no way to retrieve
    the vertex requested"""
    pass

class InvalidEdgeException(Exception):
    """This exception is raised when an edge itself that is passed in
    is not an edge in the graph when it is supposed to be, or vice-versa,
    or is None"""
    pass

class InvalidVertexException(Exception):
    """This exception is raised when a vertex itself that is passed in
    is not a vertex in the graph when it is supposed to be, or vice-versa,
    or is None"""
    pass

class GraphException(Exception):
    """This exception is raised when performing some action would corrupt
    the structure of the graph"""
    pass

class ElementHolder(object):
    """This is a base class for any object that needs to contain or
    reference element (some generic object).

    Note that the ElementHolder will _always_ contain the object, so
    in a sense an ElementHolder is immutable."""
    __nextId = 0

    def __init__(self, label=None, element=None):
        """Constructs the object, with ELEMENT being the object that this
        will contain."""
        self.__element = element
        self.__id = self.__class__.__nextId
        if label is None:
            self.__label = "ID" + str(self.__id)
        else:
            self.__label = label
        self.__class__.__nextId += 1

    def __eq__(self, other):
        """Tests equality. The key thing to note is that two ElementHolders
        are equal if they have the same ID, _not_ if they contain the same
        object (since the ElementHolder class is an abstraction for a container;
        we are comparing whether two containers are the same, but different
        containers can contain the same object)"""
        return other!= None and self.id() == other.id()

    def __ne__(self, other):
        """Tests non-equality"""
        return not self == other

    def __hash__(self):
        """We hash based on the identifier, because this completely
        determines the ElementHolder."""
        return hash(self.id())

    def element(self):
        """Gets the element that this object holds."""
        return self.__element

    def copy(self):
        """Returns a shallow copy of this ElementHolder, meaning that only
        the object reference gets copied."""
        tmp = self.__class__(self.element(), self.label())
        tmp.__id = self.id()
        return tmp

    def id(self):
        """Returns an identifier number for the ElementHolder. The ID is all
        that determines the uniqueness of an ElementHolder. """
        return self.__id
    def label(self):
        """Returns a custom label for this ElementHolder."""
        return self.__label

class GraphVertex(ElementHolder):
    """Class that represents a vertex in a graph. A vertex can have an
    object associated with it (e.g. a weight), hence the reason from
    inheriting from ElementHolder."""
    def __str__(self):
        """Prints the vertex, giving information on the vertex itself and
        the element it contains."""
        return "v" + str(self.label()) + ":" + str(self.element())

class GraphEdge(ElementHolder):
    """Class that represents an edge in a graph. An edge can have an
    object associated with it (e.g. a weight), hence the reason from
    inheriting from ElementHolder."""
    def __str__(self):
        """Prints the edge, giving information on the vertex itself and
        the element it contains."""
        return "e" + str(self.label()) + ":" + str(self.element())

class MyGraph(object):
    """Class that represents a (simple) graph, with adjacency-matrix big-O times.

        Some notes about implementation:
        1) We implement the adjacency matrix not as an actual 2D array,
        but as a hash table of hash tables (in PythonSpeak, a dictionary
        of dictionaries). There are four main reasons for this:
            a) the code is cleaner; with a true 2D array there's a lot of bookkeeping to do
            b) it's more \"pythonesque\"
            c) 2D arrays would have to be of a fixed size unless you want to add a lot of ugly code
            d) it has the same big-O runtime for access, insertion, etc.
        2) Python is _wonderful_ about the decorator pattern. Just assign a tag somewhere
        in your program, like edge.toVertex = blah, and you've got your decorator.
        3) Instead of storing the edges and vertices in some sort of linked list, we use a
        cleaner implementation: a set (which is basically a dictionary without the values).
        This makes perfect sense considering the mathematical representation of a graph
        (and has the same big-O time as a linked list for the operations we need:
        insertion is O(1), iteration is O(n)).
        4) insertVertex() and insertEdge() actually take _vertices_ and _edges_
        as arguments, not elements from which vertices and edges are created. This allows
        you to have a vertex or edge in more than one graph (and you don't need to make
        them have the same connections in both graphs; it's just like the mathematical
        idealization of a graph)."""

    def __init__(self):
        """Initializes a blank graph."""
        self.clear()

    def __str__(self):
        """Returns a string representation of this graph, giving all the vertices, edges,
        the connections between them, and the associated elements."""
        sList = ["v: "]
        for v in self.vertices():
            sList.append(str(v.label()) + ":" + str(v.element()) + ", ")
        s = ''.join(sList)
        s = s[:len(s) - 2] # chop off last ', '

        sList = [s, "; e: "]
        for e in self.edges():
            a = self.endVertices(e)
            sList.append(str(e.label()) + ": " + str(e.element()) \
                         + ":(" + str(a[0].label()) + "->" + str(a[1].label()) + "), ")
        s = ''.join(sList)
        s = s[:len(s) - 2] # chop off last ', '

        return s

    def areAdjacent(self, v1, v2):
        """Tests whether V1 and V2 are connected by an edge in this graph.

        Throws InvalidVertexException if a vertex isn't in the graph.

        Runs in O(1)."""
        self.__testVertex(v1)
        self.__testVertex(v2)
        return (v1 in self.__adjMatrix and v2 in self.__adjMatrix[v1] and self.__adjMatrix[v1][v2] is not None)

    def insertVertex(self, v):
        """Puts a vertex V into the graph. Returns V.

        Throws InvalidVertexException if the vertex is already in the graph.

        Runs in O(1)."""
        self.__testVertex(v, wantInGraph=False, wantNotInGraph=True)

        self.__vertices.add(v)
        return v

    def insertEdge(self, v1, v2, e):
        """Puts an edge E into the graph, with endpoints V1 and V2. Returns E.

        Throws InvalidEdgeException if the edge is already in the graph.
        Throws InvalidVertexException if either vertex is _not_ in the graph.
        Throws GraphException if this insertion would make the graph non-simple.

        Runs in O(1)."""
        self.__testVertex(v1)
        self.__testVertex(v2)
        self.__testEdge(e, wantInGraph=False, wantNotInGraph=True)

        if v1 == v2:
            raise GraphException("can't have a vertex connected to itself")

        if self.areAdjacent(v1, v2):
            raise GraphException("vertices already have edge connecting them")

        self.__edges.add(e)
        if v1 not in self.__adjMatrix:
            self.__adjMatrix[v1] = {}
        if v2 not in self.__adjMatrix:
            self.__adjMatrix[v2] = {}
        self.__adjMatrix[v1][v2] = e
        self.__adjMatrix[v2][v1] = e

        e.fromVertex = v1
        e.toVertex = v2

        return e

    def removeVertex(self, v):
        """Removes a vertex V from the graph. But be careful: it will also remove
        any edge that is connected to the vertex, to keep the graph consistent.
        Returns the element associated with V.

        Throws InvalidVertexException if the vertex is not in the graph.

        Runs in O(|V|)."""

        self.__testVertex(v)

        for w in self.__vertices:
            if self.areAdjacent(v, w):
                self.removeEdge(self.connectingEdge(v, w))

        self.__vertices.remove(v)
        return v.element()

    def removeEdge(self, e):
        """Removes an edge E from the graph. Returns the element associated with E.

        Throws InvalidEdgeException if the edge is not in the graph.

        Runs in O(1)."""

        self.__testEdge(e)
        a = self.endVertices(e)

        self.__edges.remove(e)

        self.__adjMatrix[a[0]][a[1]] = None
        self.__adjMatrix[a[1]][a[0]] = None

        return e.element()

    def connectingEdge(self, v1, v2):
        """Returns the edge connecting two vertices V1 and V2.

        Throws InvalidVertexException if either vertex is not in the graph.
        Throws NoSuchEdgeException if there is no edge in the graph that connects these vertices.

        Runs in O(1)."""
        self.__testVertex(v1)
        self.__testVertex(v2)

        if not self.areAdjacent(v1, v2):
            raise NoSuchEdgeException("there is no edge between these vertices")

        return self.__adjMatrix[v1][v2]

    def incidentEdges(self, v):
        """Returns a list of the edges that a vertex V is connected to.

        Throws InvalidVertexException if the vertex is not in the graph.

        Runs in O(|V|)."""
        self.__testVertex(v)

        return [self.connectingEdge(v, w) for w in self.__vertices if w != v and self.areAdjacent(v, w)]

    def opposite(self, v, e):
        """Returns the vertex opposite another vertex V on an edge E.

        Throws InvalidVertexException if the vertex is not in the graph.
        Throws InvalidEdgeException if the edge is not in the graph.
        Throws NoSuchVertexException if the vertex is not on the edge (so the request doesn't make sense).

        Runs in O(1)."""
        self.__testVertex(v)
        self.__testEdge(e)

        if e.toVertex == v:
            return e.fromVertex
        elif e.fromVertex == v:
            return e.toVertex
        else:
            raise NoSuchVertexException("vertex is not on edge")

    def endVertices(self, e):
        """Returns both vertices on an edge E (in a list).

        Throws InvalidEdgeException if the edge is not in the graph.

        Runs in O(1)."""
        self.__testEdge(e)

        return [e.fromVertex, e.toVertex]

    def edges(self):
        """Returns the edges in the graph.

        Runs in O(|V|^2) (we need to create a new set of edges; we don't
        want the caller to be able to screw up the original set)."""
        return set(self.__edges)

    def vertices(self):
        """Returns the vertices in the graph.

        Runs in O(|V|) (we need to create a new set of vertices; we don't
        want the caller to be able to screw up the original set)."""
        return set(self.__vertices)

    def numVertices(self):
        """Returns the number of vertices in the graph.

        Runs in O(1)."""
        return len(self.__vertices)

    def numEdges(self):
        """Returns the number of edges in the graph.

        Runs in O(1)."""
        return len(self.__edges)

    def iterEdges(self):
        """This is like edges(), except that it returns just an iterator
        for the edges. This gives better performance, if we
        just need to iterate through the edges and don't need a full copy
        of the edges.

        Runs in O(1)."""

        return iter(self.__edges)

    def iterVertices(self):
        """This is like vertices(), except that it returns just an iterator
        for the vertices. This gives better performance, if we
        just need to iterate through the edges and don't need a full copy
        of the vertices.

        Runs in O(1)."""

        return iter(self.__vertices)

    def containsEdge(self, e):
        """Returns whether the graph contains an edge E.

        Runs in O(1)."""

        return e in self.__edges

    def containsVertex(self, v):
        """Returns whether the graph contains a vertex V.

        Runs in O(1)."""

        return v in self.__vertices

    def clear(self):
        """Totally empties the graph."""
        self.__edges = set()
        self.__vertices = set()
        self.__adjMatrix = {}

    def __testVertex(self, v, wantInGraph = True, wantNotInGraph=False):
        """Helper function that tests the \"validity\" of a vertex. A vertex
        is invalid if:
            1) it is None
            2) the calling method would add a vertex that is already in the graph.
            3) a vertex is requested which is not in the graph but must be for the method to work.
        """
        if v is None:
            raise InvalidVertexException("vertex is None")

        if wantInGraph and v not in self.__vertices:
            raise InvalidVertexException("vertex is not in this graph")
        elif wantNotInGraph and v in self.__vertices:
            raise InvalidVertexException("vertex is already in this graph")

    def __testEdge(self, e, wantInGraph = True, wantNotInGraph=False):
        """Helper function that tests the \"validity\" of an edge. An edge
        is invalid if:
            1) it is None
            2) the calling method would add an edge that is already in the graph.
            3) an edge is requested which is not in the graph but must be for the method to work.
        """
        if e is None:
            raise InvalidEdgeException("edge is None")

        if wantInGraph and e not in self.__edges:
            raise InvalidEdgeException("edge is not in this graph")
        elif wantNotInGraph and e in self.__edges:
            raise InvaildEdgeException("edge is already in this graph")

    def graphicVisit(self, f1, f2):
        """Takes in two defined functions f1 and f2. f1 is called on each vertex
        and f2 is called on each edge once by checking whether each vertex/edge's
        visited attribute is False."""
        from queue import Queue

        for v in self.vertices():
            v.visited = False
        for e in self.edges():
            e.visited = False

        for u in self.vertices():
            if not u.visited:
                Q = Queue()
                Q.put(u)
                while not Q.empty():
                    v = Q.get()
                    if v.visited:
                        continue
                    f1(v)
                    v.visited = True
                    for e in self.incidentEdges(v):
                        if not e.visited:
                            e.visited = True
                            f2(e)
                            ov = self.opposite(v, e)
                            Q.put(ov)

    def graphic(self):
        """Returns a representation of this graph as a .dot file.
        In other words, if you pass the string returned by this method into
        the program DOT (or, better yet, NEATO), you can get an image file
        of the graph."""
        self.strs = ["graph\n{\n"]

        def annex_vertex(v):
            self.strs.append("\t" + str(v.label()) + " [label=\"" \
                + str(v.label()) + "\"];\n")

        def annex_edge(e):
            a = self.endVertices(e)
            self.strs.append("\t" + str(a[0].label()) + "--" + str(a[1].label())\
                    + " [label=\"" \
                    + " " + str(e.label()) + ": " + str(e.element()) + "\"];\n")

        self.graphicVisit(annex_vertex, annex_edge)
        self.strs.append("}\n")
        if len(self.strs) == 2:
            return None
        return ''.join(self.strs)

    def popup(self):
        """Opens a new window with this graph rendered by DOT.
        Sequential calls to this function will show the window
        once at a time. """
        import os
        tmp = open("./.tmpgraph", "w+")
        graph = self.graphic()
        if graph == None:
            print('Error: can\'t visualize an empty MyGraph.')
            return
        tmp.write(graph)
        tmp.close()
        os.system("dot -Tpng ./.tmpgraph | display")

if __name__ == "__main__":
    g = MyGraph()
    v0 = GraphVertex(0)
    v1 = GraphVertex(1)
    v2 = GraphVertex(2)
    v3 = GraphVertex(3)
    v4 = GraphVertex(4)
    v5 = GraphVertex(5)
    g.insertVertex(v0)
    g.insertVertex(v1)
    g.insertVertex(v2)
    g.insertVertex(v3)
    g.insertVertex(v4)
    g.insertVertex(v5)
    g.insertEdge(v0, v1, GraphEdge(2))
    g.insertEdge(v0, v2, GraphEdge(3))
    g.insertEdge(v1, v2, GraphEdge(4))
    g.insertEdge(v3, v4, GraphEdge(8))
    g.popup()
