import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import numpy as np
import re
class canonical:
   
    def __init__(self):
        self.graphs = []
        self.G = nx.Graph()
        self.adjacencies = []
        # self.graph_data = dict.fromkeys(['iteration','marked','neighbors','currentCanonicalOrder'])
        self.graph_data = {}
        self.node_coordinate = [] 
        self.new_node_coordinate = {}
        self.priority_order = []
    def run(self):
        
        #inputting te graph
        self.G = nx.Graph()
        self.adjacencies = []
        n = int(input("Enter number of nodes: "))
        for i in range(n):
            self.G.add_node(i, id = -1, chord = 0, mark = False, out = False)
        t = list(tuple(map(int,input().split())) for r in range(int(input('enter no of self.adjacencies : '))))  
        self.G.add_edges_from(t) 
        self.graphs.append(self.G)
        
        v1 = int(input("Enter v1: "))
        v2 = int(input("Enter v2: "))
        vn = int(input("Enter vn: "))
        
        nx.draw_planar(self.G,with_labels=True, font_weight='bold')
        plt.savefig("inputgraph.png")
        plt.show()    #DEBUG TODOs
            
        #initialisations
        canord = np.zeros(n, dtype= int)
        self.canonical_order(canord, v1,v2,vn, n)   # TODO find v1,v2,vn

    def displayInputGraph(self,noOfNodes,edge_set,nodes_data):
        for i in nodes_data: #To get the Coordinates of the nodes 
            temp_node_data = []
            temp_node_data.append(i.pos_x)
            temp_node_data.append(i.pos_y)
            self.node_coordinate.append(temp_node_data)
    
        self.graph_data = {'iteration':np.zeros(noOfNodes),'marked': np.zeros(noOfNodes),'neighbors': [],'currentCanonicalOrder': np.zeros(noOfNodes*noOfNodes).reshape(noOfNodes,noOfNodes)}
        for i in range(noOfNodes):
            self.G.add_node(i, id = -1, chord = 0, mark = False, out = False)
        # t = list(tuple(map(int,input().split())) for r in range(graph.edgecnt))
        
        for x in edge_set:
            self.G.add_edge(x[0], x[1])
        
        # self.G.add_edges_from(t) 
        self.graphs.append(self.G)
        is_planar, G2 = nx.check_planarity(self.G, False)
        if(not is_planar):
            return False;

        # nx.draw(self.G,self.node_coordinate,with_labels=True, font_weight='bold')
        # plt.gca().invert_yaxis()
        # plt.savefig("inputgraph.png")
        # plt.show()    #Uncomment above 4 lines to see input graph
        return True

    def runWithArguments(self,noOfNodes,v1,v2,vn,priority_order,graph,edge_set):
        
        # print("v1 : {}".format(v1))
        # print("v1 : {}".format(v2))
        # print("v1 : {}".format(vn))
        
        # self.G.add_edges_from(t) 
        
        #initialisations
        canord = np.zeros(noOfNodes, dtype= int)
        if(priority_order!=""):
            self.priority_order = list(map(int, re.findall(r'\d+', priority_order)))
            if v1 in self.priority_order:
                self.priority_order.remove(v1)
            if v2 in self.priority_order: 
                self.priority_order.remove(v2)

        self.canonical_order(canord, v1,v2,vn,noOfNodes)   # TODO find v1,v2,vn


    def canonical_order(self,canord, v1,v2,vn,n):
        n = int(n)
        print("Priority_Order : {}".format(self.priority_order))
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
        self.graph_data['iteration'][0] = 1
        self.graph_data['marked'][0] = v1
        self.graph_data['currentCanonicalOrder'][0] = canord


        canord[v2] = 1;

        print("\n\nIteration {}".format(2))
        print("Marked: {}".format(v2))
        print("Canonical Order: {}".format(canord))

        self.graph_data['iteration'][1] = 2
        self.graph_data['marked'][1] = v2
        self.graph_data['currentCanonicalOrder'][1] = canord

        canord[vn] = n-1;

        for i in range(n-1, 1, -1):
            print("\n\nIteration {}".format(n+2-i))
            print("Chords : {}".format(chord))
            temp_array = np.logical_and(np.logical_and(np.logical_not(mark), out), np.logical_not(chord))
            # print(temp_array)
            poss_vertex = np.where(temp_array == True)[0].flatten()
            # print(poss_vertex)
            print("Options for Next Iteration: {}".format(poss_vertex)) 
            if len(self.priority_order)>0 and self.priority_order[0] in poss_vertex:
                vk = self.priority_order[0]
                self.priority_order.remove(self.priority_order[0])
            else:
                vk = poss_vertex[0]
                if vk in self.priority_order:
                    self.priority_order.remove(vk)
            canord[vk] = i
            mark[vk] = True
            print("Marked: {}".format(vk))
            neighbors = np.array( list(self.G.neighbors(vk)))
            print ("Neighbors of vk: {} ".format(neighbors))
            for j in neighbors:
                out[j] = True
            self.updatechord(chord, mark,out, v1,v2)
            print("Canonical Order: {}".format(canord))
            # self.displayGraph(canord,n)
            self.updateGraphData(n,i,vk,neighbors,canord)
     
        print("\nFinal Canonical Order: {}".format(canord))
        self.displayGraph(canord,n)
        # plt.show()    #DEBUG TODO
        

        fig, axes = plt.subplots(nrows=1, ncols=2)
        ax = axes.flatten()
        fig.set_size_inches(15.0, 5.25)
        ax[0].invert_yaxis()
        ax[0].set_title('Input Graph')
        ax[1].invert_yaxis()
        ax[1].set_title('Output Graph after Canonical Order')


        nx.draw(self.graphs[0],self.node_coordinate,with_labels=True, font_weight='bold',ax = ax[0])
        ax[0].set_axis_off()
        nx.draw(self.graphs[1],self.new_node_coordinate,with_labels=True, font_weight='bold',ax = ax[1])
        ax[1].set_axis_off()
        plt.savefig("./source/polygonal/lastcanonicalorder.png")
        plt.show() #ON

    def updateGraphData(self,n,i,vk,neighbors,canord):
        self.graph_data['iteration'][n+2-i-1] = n+2-i
        self.graph_data['marked'][n+2-i-1] = vk
        self.graph_data['neighbors'].append(neighbors)
        self.graph_data['currentCanonicalOrder'][n+2-i-1] = canord

       
    def displayGraph(self,canord,n):
        int2label ={}
        for i in range(n):
            int2label[i] = canord[i]
            self.new_node_coordinate[canord[i]] = self.node_coordinate[i]
        self.G = nx.relabel_nodes(self.G, int2label)
        self.graphs.append(self.G)
        # nx.draw(self.G,self.new_node_coordinate,with_labels=True, font_weight='bold') #Uncomment these 3 lines to see output graph
        # plt.gca().invert_yaxis()

    def updatechord(self,chord, mark,out,v1,v2):

        outer = np.logical_and(out, np.logical_not(mark))
        outer[v1] = True
        outer[v2] = True
        outer_surface = np.where(outer == True)[0]
        # print("Outer Surface {}".format(outer_surface)) #On For Debug
        out_neighbor_count = np.zeros(np.size(outer_surface), dtype= int)

        for i in range(0, np.size(outer_surface)):
            for j in range(0, np.size(outer_surface)):
                if(i!=j and self.G.has_edge(outer_surface[i],outer_surface[j])) :
                    out_neighbor_count[i] += 1
            if(out_neighbor_count[i]>2) :
                chord[outer_surface[i]] = True
            else :
                chord[outer_surface[i]] = False
        
        # print("Outer Neighbor Count {}".format(out_neighbor_count)) #On For Debug
        
        return 

if __name__ == "__main__":
    canonical().run()

    