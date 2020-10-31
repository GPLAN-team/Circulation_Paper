import numpy as np
import networkx as nx
import itertools as itr
import operations as opr
import contraction

class K4:

    def __init__(self):
        self.vertices = []
        self.sep_tri = []
        self.interior_vertex = 0
        self.edge_to_be_removed = []
        self.neighbour_vertex = 0
        self.case = 0
        self.identified = 0
        self.all_edges_to_be_removed = []

def find_K4(graph):
    H = graph.directed
    graph1 = nx.from_numpy_matrix(graph.matrix)
    all_cliques= nx.enumerate_all_cliques(graph1)
    all_cycles=[x for x in all_cliques if len(x)==4 ]
    all_quads = []
    k4 =[]
    for cycle in all_cycles:
        if((cycle[0],cycle[2]) in H.edges and (cycle[1],cycle[3])  in H.edges ):
            if  not opr.list_comparer(cycle,all_quads,4):
                all_quads.append(cycle)
                temp = K4()
                temp.vertices = cycle
                values = find_sep_tri(cycle,graph)
                temp.sep_tri = values[0]
                temp.interior_vertex = values[1]
                value = get_edge_to_be_removed(graph,temp.sep_tri)
                temp.case = value[0]
                temp.edge_to_be_removed = value[1]
                if(temp.case != 2):
                    temp.all_edges_to_be_removed.append([temp.sep_tri[0],temp.sep_tri[1]])
                    temp.all_edges_to_be_removed.append([temp.sep_tri[1],temp.sep_tri[2]])
                    temp.all_edges_to_be_removed.append([temp.sep_tri[2],temp.sep_tri[0]])
                graph.k4.append(temp)

            

def find_sep_tri(cycle,graph):
    sep_tri =[]
    interior_vertex = 0
    for vertex in cycle:
        contraction.initialize_degrees(graph)
        if(graph.degrees[vertex] == 3):
            interior_vertex = vertex
            break
    for vertex in cycle:
        if(vertex!=interior_vertex):
            sep_tri.append(vertex)
    return sep_tri,interior_vertex

def get_edge_to_be_removed(graph,sep_tri):
    all_triangles = graph.triangles
    ab = [[sep_tri[0],sep_tri[1]],[sep_tri[1],sep_tri[2]],[sep_tri[2],sep_tri[0]]]
    case = 0
    edge_to_be_removed = []
    for subset in ab:
        count = 0
        for triangle in all_triangles:
            if(subset[0] in triangle and subset[1] in triangle):
                count +=1
        if(count == 4 and [subset[0],subset[1]] != edge_to_be_removed):
            case = 2
            edge_to_be_removed =[subset[0],subset[1]]
            break
        if(count == 3 and [subset[0],subset[1]] != edge_to_be_removed):
            case = 1
            edge_to_be_removed = [subset[0],subset[1]]
    if(case == 0):
        edge_to_be_removed = [sep_tri[0],sep_tri[1]]
    return case,edge_to_be_removed

    
def get_neigbouring_vertices(graph,k4,edge_to_be_removed):
    if(k4.case == 1):
        graph1 = nx.from_numpy_matrix(graph.matrix)
        all_cliques= nx.enumerate_all_cliques(graph1)
        all_triangles=[x for x in all_cliques if len(x)==3]
        for triangle in all_triangles:
            if(edge_to_be_removed[0] in triangle and edge_to_be_removed[1] in triangle):
                if(len([x for x in triangle if x not in k4.vertices])!=0 ):
                    k4.neighbour_vertex = [x for x in triangle if x not in k4.vertices][0]
    elif(k4.case == 2):
        for temp in graph.k4:
            if(temp.case == 2 and temp != k4):
                if(edge_to_be_removed[0] in temp.vertices and edge_to_be_removed[1] in temp.vertices):
                    k4.neighbour_vertex = temp.interior_vertex
                    temp.identified = 1


def resolve_K4(graph,k4,edge_to_be_removed,rdg_vertices,rdg_vertices2,to_be_merged_vertices):
    if(k4.case!= 0 and k4.identified!=1):
        get_neigbouring_vertices(graph,k4,edge_to_be_removed)
        k4.identified = 1
        rdg_vertices.append(edge_to_be_removed[0])
        rdg_vertices2.append(edge_to_be_removed[1])
        graph.node_count +=1		#extra vertex added
        new_adjacency_matrix = np.zeros([graph.node_count, graph.node_count], int)
        for i in range(len(graph.matrix)):
            for j in range(len(graph.matrix)):
                new_adjacency_matrix[i][j] = graph.matrix[i][j]
        to_be_merged_vertices.append(graph.node_count-1)
        new_adjacency_matrix[edge_to_be_removed[0]][edge_to_be_removed[1]] = 0
        new_adjacency_matrix[edge_to_be_removed[1]][edge_to_be_removed[0]] = 0
        new_adjacency_matrix[graph.node_count-1][edge_to_be_removed[0]] = 1
        new_adjacency_matrix[graph.node_count-1][edge_to_be_removed[1]] = 1
        new_adjacency_matrix[graph.node_count-1][k4.interior_vertex] = 1
        new_adjacency_matrix[graph.node_count-1][k4.neighbour_vertex] = 1
        new_adjacency_matrix[edge_to_be_removed[0]][graph.node_count-1] = 1
        new_adjacency_matrix[edge_to_be_removed[1]][graph.node_count-1] = 1
        new_adjacency_matrix[k4.interior_vertex][graph.node_count-1] = 1
        new_adjacency_matrix[k4.neighbour_vertex][graph.node_count-1] = 1
        graph.edge_count += 3
        graph.matrix = new_adjacency_matrix
        graph.north +=1
        graph.east +=1
        graph.west +=1
        graph.south +=1     
    elif(k4.case == 0):
        rdg_vertices.append(edge_to_be_removed[0])
        rdg_vertices2.append(edge_to_be_removed[1])
        graph.node_count +=1        #extra vertex added
        new_adjacency_matrix = np.zeros([graph.node_count, graph.node_count], int)
        for i in range(len(graph.matrix)):
            for j in range(len(graph.matrix)):
                new_adjacency_matrix[i][j] = graph.matrix[i][j]
        to_be_merged_vertices.append(graph.node_count-1)
        new_adjacency_matrix[edge_to_be_removed[0]][edge_to_be_removed[1]] = 0
        new_adjacency_matrix[edge_to_be_removed[1]][edge_to_be_removed[0]] = 0
        new_adjacency_matrix[graph.node_count-1][edge_to_be_removed[0]] = 1
        new_adjacency_matrix[graph.node_count-1][edge_to_be_removed[1]] = 1
        new_adjacency_matrix[graph.node_count-1][k4.interior_vertex] = 1
        new_adjacency_matrix[edge_to_be_removed[0]][graph.node_count-1] = 1
        new_adjacency_matrix[edge_to_be_removed[1]][graph.node_count-1] = 1
        new_adjacency_matrix[k4.interior_vertex][graph.node_count-1] = 1
        graph.edge_count += 2
        graph.matrix = new_adjacency_matrix
        graph.north +=1
        graph.east +=1
        graph.west +=1
        graph.south +=1