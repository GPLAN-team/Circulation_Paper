from pickle import FALSE, TRUE
from random import randint
# from networkx.algorithms.centrality.betweenness_subset import betweenness_centrality_source
# from networkx.algorithms.core import core_number
from networkx.classes import graph
import cip
import operations as opr
import numpy as np
import news
import shortcutresolver as sr 
import contraction as cntr
import expansion as exp
import drawing as draw
import ptpg
import flip

# L-shaped function is called from the ptpg file. then the order of execution is:
# CIP
# Triplet
# Paths - conditions 
# Northeast
# Rel - conditions
# Flipping
# Draw

def LShapedFloorplan(graph):
    cip = find_cips(graph)
    if(len(cip) > 5):
        return "cips greater than 5"
    triplet = find_triplet(graph)
    path1 = find_paths(graph, triplet, cip)
    new_adjacency_mat = connect_northeast(graph, path1)
    graph.user_matrix = new_adjacency_mat
    graph.cip = find_cips(graph)
    new_adjacency_mat = add_NESW(graph, new_adjacency_mat, path1)
    graph.matrix = new_adjacency_mat
    print("=====graph.matrix after adding NESW======")
    print(graph.matrix)
    get_rel(graph, path1)
    # get_flippable(graph, triplet)
    get_floorplan(graph,triplet)

    
def find_cips(graph):
    cips = cip.find_cip(graph)
    print("====cip====")
    print(cips)
    return cips

def find_triplet(graph):

    H = opr.get_directed(graph)

    ordered_outer_vertices = opr.ordered_outer_boundary(graph)

    triplet = False

    for i in range(0,len(ordered_outer_vertices)-1):
        
        a = ordered_outer_vertices[i]

        if(i < len(ordered_outer_vertices)-2):
            b = ordered_outer_vertices[i+1]
            c = ordered_outer_vertices[i+2]

        elif(i == len(ordered_outer_vertices)-2):
            b = ordered_outer_vertices[i+1]
            c = ordered_outer_vertices[0]

        else:
            b = ordered_outer_vertices[0]
            c = ordered_outer_vertices[1]

        if((a,c) in H.edges()):
            continue

        triplet = True
        
        for v in H.nodes():
            if(v!=b and ((a,v) in H.edges() and (v,c) in H.edges)):
                triplet = False
                break
        
        if(triplet == True):
            break

    if(triplet):
        print("=====triplet=====")
        print(a,b,c)
        return (a,b,c)
    else:
        return -1

def find_paths(graph, triplet, cip):
    a = triplet[0]
    b = triplet[1]
    c = triplet[2]

    outer_vertices, outer_boundary = opr.get_outer_boundary_vertices(graph)

    from collections import defaultdict

    outer_boundary_adj_mat = defaultdict(list)
    clockwise_outer_boundary = []

    clockwise_outer_boundary.append(a)
    clockwise_outer_boundary.append(b)
    clockwise_outer_boundary.append(c)


    for edge in outer_boundary:
        outer_boundary_adj_mat[edge[0]].append(edge[1])

    visited = {}

    for i in outer_vertices:
        visited[i] = False

    visited[a] = True
    visited[b] = True
    visited[c] = True
    src = c
    print(outer_boundary_adj_mat)
    while len(clockwise_outer_boundary) < len(outer_vertices):
        if visited[outer_boundary_adj_mat[src][0]] == False :
            clockwise_outer_boundary.append(outer_boundary_adj_mat[src][0])
            visited[outer_boundary_adj_mat[src][0]] = True
            src = outer_boundary_adj_mat[src][0]
        else:
            clockwise_outer_boundary.append(outer_boundary_adj_mat[src][1])
            visited[outer_boundary_adj_mat[src][1]] = True
            src = outer_boundary_adj_mat[src][1]

    print("====clockwise outer boundary=====")
    print(clockwise_outer_boundary)

    #   4__P4__0
    #   |      |\
    #   |      | \ P0
    #   |      |  \
    # P3|      |___\1
    #   |           |
    #   |           | P1
    #   |___________|    
    #   3    P2      2

    
    tripletInCip = False
    for arr in cip:
        if a in arr and b in arr and c in arr:
            tripletInCip = True
            break

    path1 = []
    path1.append(a)
    path1.append(b)
    path1.append(c)

    possible_corners_in_cips= []
    
    for corner in cip:
        possible_corners_in_cips.extend(corner[1:len(corner)-1])

    print("=====possible_corners======")
    print(possible_corners_in_cips)


    if len(cip) == 5 and tripletInCip == False:
        for i in range(2,len(clockwise_outer_boundary)):
            print(i , " ===== " , clockwise_outer_boundary[i])
            if clockwise_outer_boundary[i] in possible_corners_in_cips:
                path1.extend(clockwise_outer_boundary[3:i+1])
                break
        
        if clockwise_outer_boundary[0] not in possible_corners_in_cips:
            for i in range( len(clockwise_outer_boundary)-1, 2, -1):
                if clockwise_outer_boundary[i] in possible_corners_in_cips:
                    path1.insert(clockwise_outer_boundary[i:len(clockwise_outer_boundary)], 0)
                    break

    if len(cip) == 4:
        for i in range(2,len(clockwise_outer_boundary)):
            print(i , " ===== " , clockwise_outer_boundary[i])
            if clockwise_outer_boundary[i] in possible_corners_in_cips:
                path1.extend(clockwise_outer_boundary[3:i+1])
                break

    print("PATH 1 =============")
    print(path1)
    if( path1_conditions(graph,path1,triplet)):
        return path1
        
    
def path1_conditions(graph, path1, triplet):
    a = triplet[0]
    b = triplet[1]
    c = triplet[2]
    flag = True

    for i in range(0, len(path1)):
        if( path1[i] == a):
            indA = i
            indB = i+1
            indC = i+2
            break
    
    leftOfB = []
    rightofB = []

    for i in range(0, graph.node_count):
        leftOfB.append(0)
        rightofB.append(0)
    
    for i in range(0, indB):
        leftOfB[path1[i]] = 1
        for j in range(0, graph.node_count):
            if graph.matrix[path1[i]][j] == 1:
                leftOfB[j] = 1
    
    for i in range(indC, len(path1)):
        rightofB[path1[i]] = 1
        for j in range(0, graph.node_count):
            if graph.matrix[path1[i]][j] == 1:
                rightofB[j] = 1


    for i in range(0,graph.node_count):
        if leftOfB[i] == 1 and rightofB == 1:
            flag = True
            break

    return flag


def connect_northeast(graph, path1):
    graph.original_node_count = graph.node_count

    graph.northeast = graph.node_count
    graph.node_count += 1

    new_adjacency_matrix = new_matrix(graph, graph.node_count)

    add_edges(graph, new_adjacency_matrix, path1, graph.northeast)

    print("======New Adj Mat=======")
    print(new_adjacency_matrix)

    return new_adjacency_matrix

def add_edges(graph, matrix, adj_vertices, new_vertex):
    for vertex in adj_vertices:
        graph.edge_count+=1
        matrix[vertex][new_vertex] = 1
        matrix[new_vertex][vertex] = 1

def new_matrix(graph, node_count):
	new_adjacency_mat = np.zeros([node_count, node_count], int)
	matrix = graph.matrix.copy()
	new_adjacency_mat[0:matrix.shape[0],0:matrix.shape[1]] = matrix
	return new_adjacency_mat

def boundary_path_single(paths, boundary, corner_points):
    for path in paths:
        corner_points.append(path[randint(0,len(path)-1)])
    while(len(corner_points)< 4):
        corner_vertex = boundary[randint(0,len(boundary)-1)]
        while(corner_vertex in corner_points):
            corner_vertex = boundary[randint(0,len(boundary)-1)]
        corner_points.append(corner_vertex)
    count = 0
    corner_points_index=[]
    for i  in boundary:
        if i in corner_points:
            print("corner points ")
            print(i)
            corner_points_index.append(count)
        count+=1
    boundary_paths = []
    boundary_paths.append(boundary[corner_points_index[0]:corner_points_index[1]+1])
    boundary_paths.append(boundary[corner_points_index[1]:corner_points_index[2]+1])
    boundary_paths.append(boundary[corner_points_index[2]:corner_points_index[3]+1])
    boundary_paths.append(boundary[corner_points_index[3]:len(boundary)]+ boundary[0:corner_points_index[0]+1])

    return boundary_paths

def get_rel(graph,path1):
	graph.contraction = []
	cntr.initialize_degrees(graph)
	cntr.initialize_good_vertices(graph)
	v, u = cntr.contract(graph)
	while v != -1:
		v, u = cntr.contract(graph)
	exp.get_trivial_rel(graph)
	while len(graph.contractions) != 0:
		k = 1
		k = exp.expand(graph)

	if (k == 0): 
		graph.node_count = graph.node_count_required
		graph.edge_count = graph.edge_count_required 
		new_adjacency_mat = add_NESW(graph, graph.user_matrix, path1)
		graph.matrix = new_adjacency_mat
		get_rel(graph, path1)
	print("REL")
	print(graph.matrix)


def get_floorplan(graph, triplet):
	a = triplet[0]
	b = triplet[1]
	c = triplet[2]
	b_ne = graph.matrix[b][graph.northeast]
		
	print(graph.matrix)
	graph.extra_vertices.append(graph.northeast)
	draw.construct_rdg(graph,[],[])

def add_NESW(graph, new_adjacency_mat, path1):
	graph.matrix = new_adjacency_mat
	graph.triangles = opr.get_all_triangles(graph)
	graph.outer_vertices, graph.outer_boundary = opr.get_outer_boundary_vertices(graph)
	cips = find_cips_L_shaped(graph)

	graph.node_count_required = graph.node_count
	graph.edge_count_required = graph.edge_count
	graph.north = graph.node_count
	graph.node_count += 1
	graph.east = graph.node_count
	graph.node_count += 1
	graph.south = graph.node_count
	graph.node_count += 1
	graph.west = graph.node_count
	graph.node_count += 1

	new_adjacency_matrix = new_matrix(graph, graph.node_count)

	for i in range(len(cips)):
		if (path1[0] in cips[i] and graph.northeast in cips[i]):
			n_cip = i
		if (path1[len(path1)-1] in cips[i] and graph.northeast in cips[i]):
			e_cip = i

	add_edges(graph,new_adjacency_matrix,cips[n_cip], graph.north)
	add_edges(graph,new_adjacency_matrix,cips[e_cip], graph.east)
	add_edges(graph,new_adjacency_matrix,cips[(n_cip+2)%4], graph.south)
	add_edges(graph,new_adjacency_matrix,cips[(e_cip+2)%4], graph.west)
	
	connect_news(new_adjacency_matrix, graph)

	print(new_adjacency_matrix)
	print(graph.edge_count)
	return new_adjacency_matrix

def find_cips_L_shaped(graph):
    cips = graph.cip
    corner_points = []
    corner_points.append(graph.northeast)
    if(graph.edge_count==3 and graph.node_count==3):
        graph.cip = [[0],[0,1],[1,2],[2,0]]
    else:
        if(len(cips) < 4):
            graph.cip = boundary_path_single(news.find_boundary_single(cips),opr.ordered_outer_boundary(graph), corner_points)
        else:
            shortcut = sr.get_shortcut(graph)
            while(len(shortcut)>4):
                index = randint(0,len(shortcut)-1)
                sr.remove_shortcut(shortcut[index],graph,graph.rdg_vertices,graph.rdg_vertices2,graph.to_be_merged_vertices)
                shortcut.pop(index)
            cips = cip.find_cip(graph)
            graph.cip = boundary_path_single(news.find_boundary_single(cips),opr.ordered_outer_boundary(graph), corner_points)
    cips = graph.cip
    print("Cips", cips)
    return cips

def connect_news(matrix, graph):
	matrix[graph.north][graph.west] = 1
	matrix[graph.west][graph.north] = 1
	matrix[graph.west][graph.south] = 1
	matrix[graph.south][graph.west] = 1
	matrix[graph.south][graph.east] = 1
	matrix[graph.east][graph.south] = 1
	matrix[graph.east][graph.north] = 1
	matrix[graph.north][graph.east] = 1