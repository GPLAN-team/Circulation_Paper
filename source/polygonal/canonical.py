import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

graphs = []
G = nx.Graph()
adjacencies = []

def run():
    
    #inputting te graph
    G = nx.Graph()
    adjacencies = []
    n = int(input("Enter number of nodes: "))
    for i in range(n):
        G.add_node(i, id = -1, chord = 0, mark = False, out = False)
    t = list(tuple(map(int,input().split())) for r in range(int(input('enter no of adjacencies : '))))  
    G.add_edges_from(t) 
    graphs.append(G)
    
    v1 = int(input("Enter v1: "))
    v2 = int(input("Enter v2: "))
    vn = int(input("Enter vn: "))
    
    nx.draw_planar(G,with_labels=True, font_weight='bold')
    plt.savefig("inputgraph.png")
    plt.show()    #DEBUG TODO
           
    #initialisations
    canord = np.zeros(n, dtype= int)
    canonical_order(G,canord, v1,v2,vn, n)   # TODO find v1,v2,vn

def displayInputGraph(noOfNodes,edge_set):
    for i in range(noOfNodes):
        G.add_node(i, id = -1, chord = 0, mark = False, out = False)
    # t = list(tuple(map(int,input().split())) for r in range(graph.edgecnt))
    
    for x in edge_set:
        G.add_edge(x[0], x[1])
    
    # G.add_edges_from(t) 
    graphs.append(G)
    
    nx.draw_planar(G,with_labels=True, font_weight='bold')
    plt.savefig("inputgraph.png")
    plt.show()    #DEBUG TODO

def runWithArguments(noOfNodes,v1,v2,vn,graph,edge_set):
    
    # print("v1 : {}".format(v1))
    # print("v1 : {}".format(v2))
    # print("v1 : {}".format(vn))
    
    # G.add_edges_from(t) 
    
    #initialisations
    canord = np.zeros(noOfNodes, dtype= int)
    canonical_order(G,canord, v1,v2,vn, noOfNodes)   # TODO find v1,v2,vn


def canonical_order(G,canord, v1,v2,vn, n):
    n = int(n)

    mark = np.zeros((n,), dtype= bool)
    chord = np.zeros((n,), dtype= bool)
    out = np.zeros((n,), dtype= bool)
    
    canord[v1] = 0;
    
    mark[v1] = True
    mark[v2] = True
    
    out[v1] = True
    out[v2] = True    
    out[vn] = True

    print("\n\nIteration {}".format(1))
    print("Marked: {}".format(v1))
    print("Canonical Order: {}".format(canord))

    canord[v2] = 1;

    print("\n\nIteration {}".format(2))
    print("Marked: {}".format(v2))
    print("Canonical Order: {}".format(canord))

    canord[vn] = n-1;

    for i in range(n-1, 1, -1):
        print("\n\nIteration {}".format(n+2-i))
        temp_array = np.logical_and(np.logical_and(np.logical_not(mark), out), np.logical_not(chord))
        # print(temp_array)
        poss_vertex = np.where(temp_array == True)[0].flatten()
        # print(poss_vertex)
        print("Options for Next Iteration: {}".format(poss_vertex))
        vk = poss_vertex[0]
        canord[vk] = i
        mark[vk] = True
        print("Marked: {}".format(vk))
        neighbors = np.array( list(G.neighbors(vk)))
        print ("Neighbors of vk: {} ".format(neighbors))
        for j in neighbors:
            out[j] = True
        updatechord(G, chord, mark,out, n)
        print("Canonical Order: {}".format(canord))
        # displayGraph(G,canord,n)
        
    print("\nFinal Canonical Order: {}".format(canord))
    displayGraph(G,canord,n)
    # plt.show()    #DEBUG TODO
    

    # fig, axes = plt.subplots(nrows=1, ncols=2)
    # ax = axes.flatten()
    # for i in range(2):
    #     nx.draw_planar(graphs[i],with_labels=True, font_weight='bold', ax=ax[i])
    #     ax[i].set_axis_off()
    plt.show()


    
def displayGraph(G,canord,n):
    int2label ={}
    for i in range(n):
        int2label[i] = canord[i]
    G = nx.relabel_nodes(G, int2label)
    nx.draw_planar(G,with_labels=True, font_weight='bold')
    plt.savefig("outputCanonicalOrder.png")
    graphs.append(G)


def updatechord(G,chord, mark,out, n):

    chord
    outer = np.logical_and(out, np.logical_not(mark))
    outer[0] = True
    outer[1] = True
    outer_surface = np.where(outer == True)[0]
    # print(outer_surface)
    out_neighbor_count = np.zeros(np.size(outer_surface))

    for i in range(0, np.size(outer_surface)):
        for j in range(0, np.size(outer_surface)):
            if(G.has_edge(outer_surface[i],outer_surface[j])) :
                out_neighbor_count[i] += 1
        if(out_neighbor_count[i]>2) :
            chord[outer_surface[i]] = True
        else :
            chord[outer_surface[i]] = False
            # print (outer_surface[i])
       
    return 

if __name__ == "__main__":
    run()

    