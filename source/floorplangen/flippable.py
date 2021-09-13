import numpy as np
import source.graphoperations.operations as opr

def get_flippable_edges(orig_matrix,news_matrix,nodecnt):
	edges = []
	for i in range(0,news_matrix.shape[0]):
		for j in range(0,news_matrix.shape[1]):
			if(news_matrix[i,j]!=0):
				if(news_matrix[i,j]==2):
					edges.append([i,j])
				elif(news_matrix[i,j]==3):
					edges.append([i,j])
	flippable_edge = []
	for edge in edges:
		if(edge[0]>= nodecnt or edge[1]>= nodecnt):
			continue
		x_nbr = np.where(orig_matrix[edge[0]] != 0)[0]
		y_nbr = np.where(orig_matrix[edge[1]] != 0)[0]
		intersection = np.intersect1d(x_nbr, y_nbr, assume_unique=True)
		if(news_matrix[edge[0],intersection[0]] == 3 or news_matrix[intersection[0],edge[0]] == 3 ):
			if(news_matrix[edge[0],intersection[1]] == 2 or news_matrix[intersection[1],edge[0]] == 2 ):
				 if(news_matrix[edge[1],intersection[1]] == 3 or news_matrix[intersection[1],edge[1]] == 3 ):
						 if(news_matrix[edge[1],intersection[0]] == 2 or news_matrix[intersection[0],edge[1]] == 2 ):
								flippable_edge.append(edge)
		elif(news_matrix[edge[0],intersection[0]] == 2 or news_matrix[intersection[0],edge[0]] == 2 ):
			if(news_matrix[edge[0],intersection[1]] == 3 or news_matrix[intersection[1],edge[0]] == 3 ):
				 if(news_matrix[edge[1],intersection[1]] == 2 or news_matrix[intersection[1],edge[1]] == 2 ):
						 if(news_matrix[edge[1],intersection[0]] == 3 or news_matrix[intersection[0],edge[1]] == 3 ):
								flippable_edge.append(edge)
	return flippable_edge

def get_flippable_vertices(matrix,news_matrix,nodecnt):
	degrees = [np.count_nonzero(news_matrix[node])
	 for node in range(news_matrix.shape[0])]
	flippable_vertex = []
	flippable_vertex_neighbours =[]
	four_degree_vertex = []
	for i in range(0,len(degrees)):
		if(degrees[i] == 4 and i <nodecnt):
			four_degree_vertex.append(i)

	for vertex in four_degree_vertex:
		neighbors = list(np.where(matrix[vertex] != 0)[0])
		temp = []
		temp.append(neighbors.pop())
		while(len(neighbors)!=0):
			for vertices in neighbors:
				if(matrix[temp[len(temp)-1],vertices]==1):
					temp.append(vertices)
					neighbors.remove(vertices)
					break
		if(news_matrix[temp[0],temp[1]] == 3 or news_matrix[temp[1],temp[0]] == 3 ):
			if(news_matrix[temp[1],temp[2]] == 2 or news_matrix[temp[2],temp[1]] == 2 ):
				 if(news_matrix[temp[2],temp[3]] == 3 or news_matrix[temp[3],temp[2]] == 3 ):
						 if(news_matrix[temp[3],temp[0]] == 2 or news_matrix[temp[0],temp[3]] == 2 ):
								flippable_vertex.append(vertex)
								flippable_vertex_neighbours.append(temp)
		elif(news_matrix[temp[0],temp[1]] == 2 or news_matrix[temp[1],temp[0]] == 2 ):
			if(news_matrix[temp[1],temp[2]] == 3 or news_matrix[temp[2],temp[1]] == 3 ):
				 if(news_matrix[temp[2],temp[3]] == 2 or news_matrix[temp[3],temp[2]] == 2 ):
						 if(news_matrix[temp[3],temp[0]] == 3 or news_matrix[temp[0],temp[3]] == 3 ):
								flippable_vertex.append(vertex)
								flippable_vertex_neighbours.append(temp)

	return flippable_vertex,flippable_vertex_neighbours

def resolve_flippable_edge(edge,rel):
	new_rel = rel.copy()
	if(new_rel[edge[0],edge[1]] == 2):
		if(opr.ordered_nbr_label(rel, rel.shape[0], edge[0], edge[1], True) == 3):
			# print("Case A")
			new_rel[edge[0],edge[1]] = 0
			new_rel[edge[0],edge[1]] = 3
		elif(opr.ordered_nbr_label(rel, rel.shape[0], edge[0], edge[1], True) == 2):
			# print("Case B")
			new_rel[edge[0],edge[1]] = 0
			new_rel[edge[1],edge[0]] = 3
	elif(new_rel[edge[0],edge[1]] == 3):
		if(opr.ordered_nbr_label(rel, rel.shape[0], edge[0], edge[1], True) == 3):
			# print("Case C")
			new_rel[edge[0],edge[1]] = 0
			new_rel[edge[0],edge[1]] = 2
		elif(opr.ordered_nbr_label(rel, rel.shape[0], edge[0], edge[1], True) == 2):
			# print("Case D")
			new_rel[edge[0],edge[1]] = 0
			new_rel[edge[1],edge[0]] = 2
	return new_rel

def resolve_flippable_vertex(vertex,neighbours,graph,rel):
	new_rel = rel.copy()
	clockwise_neighbour = opr.ordered_nbr(rel,rel.shape[0], vertex,neighbours[0],True)
	if(neighbours[1] != clockwise_neighbour):
		neighbours.reverse()
	while(new_rel[vertex,neighbours[0]] != 3):
		first_element = neighbours.pop(0)
		neighbours.append(first_element)
	if(opr.ordered_nbr(rel,rel.shape[0], neighbours[0],vertex,True) == 3):
		new_rel[vertex,neighbours[0]] = 2
		new_rel[vertex,neighbours[1]] = 3
		new_rel[neighbours[1],vertex] = 0
		new_rel[neighbours[2],vertex] = 2
		new_rel[vertex,neighbours[3]] = 0
		new_rel[neighbours[3],vertex] = 3
	elif(opr.ordered_nbr(rel,rel.shape[0], neighbours[0],vertex,True) == 2):
		new_rel[vertex,neighbours[0]] = 0
		new_rel[neighbours[0],vertex] = 2
		new_rel[neighbours[1],vertex] = 3
		new_rel[neighbours[2],vertex] = 0
		new_rel[vertex,neighbours[2]] = 2
		new_rel[vertex,neighbours[3]] = 3
	return new_rel