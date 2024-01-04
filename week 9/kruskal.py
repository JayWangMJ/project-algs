# Kruskal's algorithm to find MST 
# using union-find operations with path compression

import networkx as nx
import matplotlib.pyplot as plt

def kruskal(G):
    def makeset():
        for node in G.nodes:
            G.nodes[node]["pi"] = node
            G.nodes[node]["rank"] = 0

    def find(x):
        if G.nodes[x]["pi"] != x:
            G.nodes[x]["pi"] = find(G.nodes[x]["pi"]) # path compression
        return G.nodes[x]["pi"]
    
    def union(x, y):
        r_x = find(x)
        r_y = find(y)
        if r_x == r_y:
            return
        rank_x = G.nodes[x]["rank"]
        rank_y = G.nodes[y]["rank"]
        if rank_x > rank_y:
            G.nodes[r_y]["pi"] = r_x
        else:
            G.nodes[r_x]["pi"] = r_y
            if rank_x == rank_y:
                G.nodes[r_y]["rank"] += 1

    makeset()
    MST = []
    edges = sorted([(u, v, w) for (u, v, w) in G.edges(data="weight")], \
                   key = lambda x: x[2])
    for (u, v, _) in edges:
        if find(u) != find(v):
            MST.append((u, v))
            union(u, v)

    return MST

def test():
    G = nx.Graph()
    edges = [
        ("A", "B", 2), ("A", "C", 1), ("B", "C", 2), ("B", "D", 1), ("C", "D", 2),\
        ("C", "E", 3), ("D", "E", 3), ("D", "F", 4), ("E", "F", 1)
    ]
    G.add_weighted_edges_from(edges)
    mst = kruskal(G)
    print("MST:", mst)
    for node in G.nodes:
        print(node, G.nodes[node])
    init_pos = {"A": (0, 0), "B": (0, -200), "C": (200, 0),\
                "D": (200, -200), "E": (400, 0), "F": (400, -200)}
    pos = init_pos
    # nx.draw(G, pos = pos, with_labels=True, font_weight='bold', node_color='skyblue', node_size=500, edge_color='gray', linewidths=4)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_nodes(G, pos=pos, node_size=500)
    nx.draw_networkx_labels(G, pos=pos, font_weight="bold")

    nx.draw_networkx_edges(G, pos=pos, edge_color="gray", width=1)
    nx.draw_networkx_edges(G, pos=pos, edgelist=mst, edge_color="red", width=3)
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
    plt.show()

if __name__=="__main__":
    test()