#!/usr/bin/python3

# DO NOT DELETE THESE STATEMENTS
import topsort
from importlib import reload
reload(topsort)
from topsort import *
from mydigraph import *
import pytest

def show_elements(l):
    if l != None:
        return [x.element() for x in l]
    else:
        return []

# Write your testing functions here! Each testing function should have an
# informative name and test a specific aspect of your program's functionality.
# It is fine to have multiple assert statements in each function to test for
# various related conditions.

# DO NOT write your tests within the example test functions we provide!
# Our scripts will skip the test functions we provide, so write your own
# functions to test your code thoroughly.

# Here are some example test functions. Feel free to delete example_test_1
# and remove it from the list in get_tests().

def example_test_1():
    assert 1 == 1, 'Error: 1 does not equal 1!'


def simple_test():
    # Setup graph
    g = MyDigraph()
    v0 = g.insertVertex(GraphVertex(0))
    v1 = g.insertVertex(GraphVertex(1))
    v2 = g.insertVertex(GraphVertex(2))
    g.insertEdge(v0, v2, GraphEdge(0))
    g.insertEdge(v1, v2, GraphEdge(1))

    g.popup()
    # Run the algorithm
    topsorted = topological_sort(g)

    # Test its output
    print("Topologically sorted in the order: ", show_elements(topsorted))

    # There are two possible correct top sorts for this graph
    assert topsorted == [v0, v1, v2] or topsorted == [v1, v0, v2]


def acyclicGraphTest():
    """Purpose: This method tests that the correct exceptions
    are raised when the input graph is not acyclic.
    """
    with pytest raises Execption('GraphCycleException'):
        g = MyDigraph()
        v0 = g.insertVertex(GraphVertex(0))
        v1 = g.insertVertex(GraphVertex(1))
        v2 = g.insertVertex(GraphVertex(2))
        g.insertEdge(v0, v1, GraphEdge(0))
        g.insertEdge(v1, v2, GraphEdge(1))
        g.insertEdge(v2, v0, GraphEdge(2))

        topological_sort(g)


def multipleOrderTest():
    """Purpose: This method tests that only one of the possible 
    orders returned from the topsort algorithm.
    """
    g = MyDigraph()
    v0 = g.insertVertex(GraphVertex(0))
    v1 = g.insertVertex(GraphVertex(1))
    v2 = g.insertVertex(GraphVertex(2))
    v3 = g.insertVertex(GraphVertex(3))

    g.insertEdge(v0, v2, GraphEdge(0))
    g.insertEdge(v1, v2, GraphEdge(1))   
    g.insertEdge(v1, v3, GraphEdge(2))    

    assert topsorted == [v0, v1, v2] or topsorted == [v0,v1,v3]
 

def get_tests():
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # VERY IMPORTANT
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Add the names of each of your test functions to this list. It is very
    # important that you do this, or the TAs will not run your tests properly
    # and you will not receive full credit.
    #
    # DO NOT remove either example test from this list, just add new tests like so:
    #       [example, example, new test,...]
    # We will not be able to properly grade your coal tests if you do not follow
    # these instructions! You will lose points on your submission for failing
    # to follow these instructions.
    return [example_test_1, simple_test, exceptionTest, multipleOrderTest]

# DO NOT EDIT BELOW THIS LINE ==================================================

# The mainline runs all of the test functions in the list returned by get_tests
if __name__ == '__main__' :
    print('Running tests...')
    for test in get_tests():
        test()
    print('All tests passed!')
