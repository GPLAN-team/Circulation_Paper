# import networkx as nx
# import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import *

root = Tk()
root.title("Test GUI GPLAN")
root.geometry("500x400")

# Create a Main Frame
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)

# Create Canvas
my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT,fill=BOTH,expand=1)

# Add Scrollbar to the canvas
my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

# Configure the canvas
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>',lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

# Create another frame inside the canvas
second_frame = Frame(my_canvas)

# Add that new frame to a window in the canvas
my_canvas.create_window((0,0), window=second_frame, anchor="nw")

corr_text = tk.Label(second_frame,text="Enter 1 if you want to remove corridor",justify=tk.CENTER).grid(row=1, column=2)
for i in range(50):
    Button(second_frame, text=f'Button {i}').grid(row=i, column=0, padx=10, pady=10)

root.mainloop()
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

# OZoneIzotopeSemiWhite = "#c0c4ca"
# buttonBackground = "#303336"
# buttonforeground = "#cdd0d7"
# BACKGROUND2 = "#1e1f21"

# class DropDownButton():
#     def __init__(self, parent, placement, opTions, **kw):
#         self.parent = parent
#         self.options = opTions

#         self.om_variable = tk.StringVar(self.parent)
#         self.om_variable.set(self.options[0])
#         self.om_variable.trace('w', self.option_select)

#         self.om = tk.OptionMenu(self.parent, self.om_variable, *self.options)
#         self.om["menu"].config(fg=buttonforeground, bg=buttonBackground, activebackground=OZoneIzotopeSemiWhite, activeforeground=BACKGROUND2, borderwidth = 0)
#         self.om.config(fg=buttonforeground, bg=buttonBackground, activebackground=OZoneIzotopeSemiWhite, activeforeground=BACKGROUND2, bd =0)
#         self.om.place(x = placement, y = 2)
#         self.om.bind("<Enter>", self.on_enter)
#         self.om.bind("<Leave>", self.on_leave)

#         self.om_variable1 = tk.StringVar(self.parent)
#         self.om_variable1.set(self.options[0])
#         self.om_variable1.trace('w', self.option_select1)

#         self.om1 = tk.OptionMenu(self.parent, self.om_variable1, *self.options)
#         self.om1["menu"].config(fg=buttonforeground, bg=buttonBackground, activebackground=OZoneIzotopeSemiWhite, activeforeground=BACKGROUND2, borderwidth = 0)
#         self.om1.config(fg=buttonforeground, bg=buttonBackground, activebackground=OZoneIzotopeSemiWhite, activeforeground=BACKGROUND2, bd =0)
#         self.om1.place(x = placement, y = 2)
#         self.om1.bind("<Enter>", self.on_enter1)
#         self.om1.bind("<Leave>", self.on_leave1)

#     def on_enter(self, event):
#         if self.om == self.options[0]:
#             print ("Floorplan generation")
#         elif self.om_variable.get() == self.options[1]:
#             print ("Rectangular")
#         else:
#             print("Irregular")

#     def on_leave(self, enter):
#         print ("leave")

#     def option_select(self, *args):
#         print (self.om_variable.get())
    
#     def on_enter1(self, event):
#         if self.om == self.options[0]:
#             print ("Circulation")
#         elif self.om_variable.get() == self.options[1]:
#             print ("Dimensioned")
#         else:
#             print("Add/Remove")

#     def on_leave1(self, enter):
#         print ("leave")

#     def option_select1(self, *args):
#         print (self.om_variable1.get())

# root = tk.Tk()
# DropDownButton(root, 55, ['Floorplan gen', 'Rectangular', 'Irregular'])
# DropDownButton(root, 200, ['Circulation', 'Dimensioned', 'Add/Remove'])
# root.mainloop()
