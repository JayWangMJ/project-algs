import networkx as nx
import matplotlib.pyplot as plt

def dfs(G):
    for u in G.nodes:
        G.nodes[u]["color"] = "white"
        G.nodes[u]["parent"] = None
    time = 0
    for u in G.nodes:
        if G.nodes[u]["color"] == "white":
            time = dfs_visit(G, u, time)

def dfs_visit(G, u, time):
    time += 1
    G.nodes[u]["discover"] = time
    G.nodes[u]["color"] = "gray"
    for v in G.neighbors(u):
        if G.nodes[v]["color"] == "white":
            G.nodes[v]["parent"] = u
            time = dfs_visit(G, v, time)
    G.nodes[u]["color"] = "black"
    time += 1
    G.nodes[u]["finish"] = time
    return time

def topological_sort(G):
    dfs(G)
    sorted_nodes = sorted(G.nodes(data="finish"), key=lambda x: x[1], reverse=True)
    return sorted_nodes

def test():
    G = nx.DiGraph()
    G.add_edges_from([(1, 2), (1, 4), (2, 3), (4, 2), (4, 5), (4, 6), (5, 6)])
    sorted_nodes = topological_sort(G)
    for node in sorted_nodes:
        print(node[0], end=" ")
    # pos = nx.spring_layout(G, seed=4120)
    pos = {1: (0, 0), 2: (0, -200), 3: (200, -200), 4: (200, 0), 5: (400, 200), 6: (400, 0)}
    nx.draw(G, pos = pos, with_labels=True, font_weight='bold', node_color='skyblue', node_size=500, edge_color='gray', linewidths=2)
    plt.show()

if __name__=="__main__":
    test()