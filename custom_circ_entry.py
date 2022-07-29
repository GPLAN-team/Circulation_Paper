"""This file is the code to insert a spanning circulation for a given planar graph input (where entry need not be exterior edge)
"""
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy
import source.trial.bdy as bdy
from typing import List, Tuple
import circulation

class custom_circ:
    def __init__(self, graph) -> None:
        self.graph = graph
        self.span_circ = nx.Graph()
        self.adjacency = {}

    def custom_circ(self,f1: int, f2: int,s1: int = 1,s2: int = 2,v1: int = 1,v2: int = 2) -> nx.Graph:
        """
        Modifies the circulation graph having the spanning circulation to restrict it to user choice
        
        Args:
            f1 (int, optional): First endpoint of the target edge to end the circulation (maybe interior). Defaults to 1.
            f2 (int, optional): Second endpoint of the target edge to end the circulation (maybe interior). Defaults to 2.
            s1 (int, optional): First endpoint of the target edge to start the circulation (maybe interior). Defaults to 1.
            s2 (int, optional): Second endpoint of the target edge to start the circulation (maybe interior). Defaults to 2.
            v1 (int, optional): First endpoint of the exterior edge to start the circulation algorithm. Defaults to 1.
            v2 (int, optional): Second endpoint of the exterior edge to start the circulation algorithm. Defaults to 2.            
        """
        # Steps involved:
        # Step 1: Find spanning circulation
        # Step 2: Find corridor vertex on the edge s1--s2 and similarly f1--f2
        # Step 3: Change label of other corridor vertices to a large number

        # Step 1 (Note: later call the circ_algo from circulation.py instead of repeating code)

        graph = deepcopy(self.graph)
        print(nx.to_numpy_matrix(graph))
        # n is the number of vertices in the initial graph
        n = len(graph)
        m = n
        s = (v1-1 ,v2-1 , -1)

        # This dictionary tracks the pair of rooms each corridor is adjacent to
        # (key is vertex corresponding to corridor and values are a pair of rooms)
        adjacency = {}
        corridor_counter = 0
        queue = []
        queue.append(s)

        # Start of circulation algorithm
        while ( queue ):
            # Pops out the first element of the queue to subdivide the edge for V_n+1
            s = queue.pop(0)  
            for ne in list(nx.common_neighbors(graph,s[0],s[1])):
                if ne < m :
                    graph.add_edge(s[0],n)
                    graph.add_edge(s[1],n)
                    try:
                        graph.remove_edge(s[0],s[1])
                    except:
                        print("WARNING!! THE INITIAL CHOSEN ENTRY EDGE MUST BE EXTERIOR EDGE") # Warning displayed
                        return 0
                    
                    if s[2]>0:
                        # If condition satisfied this adds edge between current corridor vertex and previous one
                        graph.add_edge(n,s[2])
                    graph.add_edge(n,ne)
                    n+=1
                    # Adds the two tuples corresponding to the two triangles formed in the face considered
                    adjacency[corridor_counter] = [s[0],s[1]]
                    corridor_counter += 1
                    queue.append((ne,s[0],n-1))
                    queue.append((ne,s[1],n-1))
        
        # Change the key values to corridor vertex number
        corridor_vertices = [x+m for x in range(len(adjacency))]

        # Now the final_adjacency dictionary contains the pair of rooms adjacent to each corridor
        final_adjacency = dict(zip(corridor_vertices, list(adjacency.values())))

        # Now A stores the adjacency matrix of the graph, the nodelist parameter ensures the proper order of rows
        # corresponding to the node id
        A = nx.adjacency_matrix(graph, nodelist=range(m))

        # todense prints the matrix in proper format along with the data type
        print(A.todense())

        self.span_circ = graph
        self.adjacency = final_adjacency

        # Step 2

        min = 999
        max = -1

        # Loop to find the corridor vertex labels that mark start and end of custom circulation
        # We find the v1, v2 such that it is the nearest exterior edge to the start and so we have
        # i for s1--s2 < i for f1--f2
        for i in range(len(self.graph),len(self.span_circ)):
            # Gets the tuple corresponding to the key value (key = corridor_vertex = i(here))
            [a,b] = self.adjacency.get(i)
            if([a,b] == [s1,s2]):
                if (min > i):
                    i = min

            if([a,b] == [f1,f2]):
                if(max < i):
                    max = i
        
        # Step 3

        # for i in range(min,max+1):
