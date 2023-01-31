# import networkx as nx
# import matplotlib.pyplot as plt

# def plot(graph: nx.Graph,m: int) -> None:
#     """Plots thr graph using matplotlib

#     Args:
#         graph (Networkx graph): The graph to plot
#         m (integer): Number of vertices in the graph
#     """
#     pos=nx.spring_layout(graph) # positions for all nodes
#     nx.draw_networkx(graph,pos, label=None,node_size=400 ,node_color='#4b8bc8',font_size=12, font_color='k', font_family='sans-serif', font_weight='normal', alpha=1, bbox=None, ax=None)
#     nx.draw_networkx_edges(graph,pos)
#     nx.draw_networkx_nodes(graph,pos,
#                         nodelist=list(range(m,len(graph))),
#                         node_color='r',
#                         node_size=500,
#                     alpha=1)
#     plt.show()

# g = nx.Graph()
# g.add_edge(0,1)
# g.add_edge(0,2)
# g.add_edge(1,3)
# g.add_edge(1,2)
# g.add_edge(1,4)
# g.add_edge(3,6)
# g.add_edge(3,4)
# g.add_edge(2,4)
# g.add_edge(2,5)
# g.add_edge(4,5)
# g.add_edge(4,6)
# g.add_edge(5,6)

# plot(g,len(g))
# h = nx.induced_subgraph(g,[x for x in range(5)])
# plot(h,len(h))
import tkinter as tk
import tkinter.ttk as ttk
def main(self):
    f = tk.Frame(self.master,width=3)
    f.grid(row=2, column=0, columnspan=8, rowspan=10, pady=30, padx=30)
    f.config(width=5)
    self.tree = ttk.Treeview(f, selectmode="extended")
    scbHDirSel =tk.Scrollbar(f, orient=Tkinter.HORIZONTAL, command=self.tree.xview)
    scbVDirSel =tk.Scrollbar(f, orient=Tkinter.VERTICAL, command=self.tree.yview)
    self.tree.configure(yscrollcommand=scbVDirSel.set, xscrollcommand=scbHDirSel.set)           
    self.tree["columns"] = (self.columnListOutput)
    self.tree.column("#0", width=40)
    self.tree.heading("#0", text='SrNo', anchor='w')
    self.tree.grid(row=2, column=0, sticky=Tkinter.NSEW,in_=f, columnspan=10, rowspan=10)
    scbVDirSel.grid(row=2, column=10, rowspan=10, sticky=Tkinter.NS, in_=f)
    scbHDirSel.grid(row=14, column=0, rowspan=2, sticky=Tkinter.EW,in_=f)
    f.rowconfigure(0, weight=1)
    f.columnconfigure(0, weight=1)