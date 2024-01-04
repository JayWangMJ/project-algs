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

def is_back_edge(G, u, v):
    return G.nodes[v]["discover"] < G.nodes[u]["discover"]\
          < G.nodes[u]["finish"] < G.nodes[v]["finish"]

def cycle_dectection(G):
    dfs(G)
    for (u, v) in G.edges:
        if is_back_edge(G, u, v):
            return True
    return True

def test():
    G = nx.DiGraph()
    G.add_edges_from([(1, 2), (2, 3), (3, 1)])
    if cycle_dectection(G):
        print("G contains a cycle")
    else:
        print("G is acyclic")
    pos = nx.shell_layout(G)
    nx.draw(G, pos = pos, with_labels=True, font_weight='bold', node_color='skyblue', node_size=500, edge_color='gray', linewidths=2)
    plt.show()

if __name__=="__main__":
    test()