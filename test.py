import networkx as nx
import matplotlib.pyplot as plt

def plot(graph: nx.Graph,m: int) -> None:
    """Plots thr graph using matplotlib

    Args:
        graph (Networkx graph): The graph to plot
        m (integer): Number of vertices in the graph
    """
    pos=nx.spring_layout(graph) # positions for all nodes
    nx.draw_networkx(graph,pos, label=None,node_size=400 ,node_color='#4b8bc8',font_size=12, font_color='k', font_family='sans-serif', font_weight='normal', alpha=1, bbox=None, ax=None)
    nx.draw_networkx_edges(graph,pos)
    nx.draw_networkx_nodes(graph,pos,
                        nodelist=list(range(m,len(graph))),
                        node_color='r',
                        node_size=500,
                    alpha=1)
    plt.show()

g = nx.Graph()
g.add_edge(0,1)
g.add_edge(0,2)
g.add_edge(1,3)
g.add_edge(1,2)
g.add_edge(1,4)
g.add_edge(3,6)
g.add_edge(3,4)
g.add_edge(2,4)
g.add_edge(2,5)
g.add_edge(4,5)
g.add_edge(4,6)
g.add_edge(5,6)

plot(g,len(g))
h = nx.induced_subgraph(g,[x for x in range(5)])
plot(h,len(h))