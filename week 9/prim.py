import networkx as nx
import matplotlib.pyplot as plt

def prim(G):
    # initialization
    s = list(G.nodes)[0]
    for node in G.nodes:
        G.nodes[node]["d"] = float("inf")
        G.nodes[node]["pi"] = None
    G.nodes[s]["d"] = 0
    mst = []

    visited = set()
    visited.add(s)
    for v in G.neighbors(s):
        G.nodes[v]["d"] = G.edges[(s, v)]["weight"]
        G.nodes[v]["pi"] = s

    while len(visited) < G.number_of_nodes():
        min_edge = None
        for node in G.nodes:
            if node not in visited:
                if min_edge is None or G.nodes[node]["d"] < min_edge[1]:
                    min_edge = (node, G.nodes[node]["d"])
        
        u = min_edge[0]
        for v in G.neighbors(u):
            if v in visited:
                continue
            if G.edges[(u, v)]["weight"] < G.nodes[v]["d"]:
                G.nodes[v]["d"] = G.edges[(u, v)]["weight"]
                G.nodes[v]["pi"] = u
        
        visited.add(u)
        mst.append((G.nodes[u]["pi"], u))

    return mst        
    # return G

def test():
    G = nx.Graph()
    edges = [
        ("A", "B", 5), ("A", "C", 6), ("A", "D", 4), ("B", "C", 1), ("B", "D", 2),\
        ("C", "D", 2), ("C", "E", 5), ("C", "F", 3), ("D", "F", 4), ("E", "F", 4)
    ]
    G.add_weighted_edges_from(edges)
    mst = prim(G)
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