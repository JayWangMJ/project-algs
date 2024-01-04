import networkx as nx
import matplotlib.pyplot as plt

def bellman_ford(G, s):
    # initialization
    for node in G.nodes:
        G.nodes[node]["d"] = float("inf")
        G.nodes[node]["pi"] = None
    G.nodes[s]["d"] = 0

    # main loop, do relaxation
    for _ in range(G.number_of_nodes()-1):
        for (u, v, w) in G.edges(data="weight"):
            if G.nodes[u]["d"] + w < G.nodes[v]["d"]:
                G.nodes[v]["d"] = G.nodes[u]["d"] + w
                G.nodes[v]["pi"] = u

    # negative cycle detection
    for (u, v, w) in G.edges(data="weight"):
        if G.nodes[v]["d"] > G.nodes[u]["d"] + w:
            raise ValueError("Negative cycle detected")
            
    # return G
        
def test():
    G = nx.DiGraph()
    G.add_weighted_edges_from([
        (0, 1, 6), (0, 2, 5), (0, 3, 5), (1, 4, -1), (2, 1, -2),\
        (2, 4, 1), (3, 2, -2), (3, 5, -1), (4, 6, 3), (5, 6, 3),
    ])
    # G.add_edge(2, 0, weight=-200)
    bellman_ford(G, 0)
    for node in G.nodes:
        print(node, G.nodes[node])
    init_pos = {0: (0, 0), 1: (200, 200), 2: (200, 0), 3 : (200, -200),\
                4: (400, 200), 5: (400, -200), 6: (600, 0)}
    # pos = nx.spring_layout(G, pos=init_pos, fixed=[0, 1, 2, 3, 4, 5, 6])
    pos = init_pos
    nx.draw(G, pos = pos, with_labels=True, font_weight='bold', node_color='skyblue', node_size=500, edge_color='gray', linewidths=4)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
    plt.show()

if __name__=="__main__":
    test()