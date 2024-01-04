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

def kosaraju(G):
    def second_dfs(node, scc):
        visited.add(node)
        scc.append(node)
        for neighbor in G.neighbors(node):
            if neighbor not in visited:
                second_dfs(neighbor, scc)

    reversed_G = G.reverse()
    dfs(reversed_G)
    visited = set()
    sccs = []
    for node in sorted(reversed_G.nodes(data="finish"), key=lambda x: x[1], reverse=True):
        if node[0] not in visited:
            scc = []
            second_dfs(node[0], scc)
            sccs.append(scc)
    
    return sccs

def test():
    G = nx.DiGraph()
    G.add_edges_from([("A", "B"), ("B", "C"), ("B", "D"), ("B", "E"), ("C", "F"),\
                      ("E", "B"), ("E", "F"), ("E", "G"), ("F", "C"), ("F", "H"),\
                      ("G", "H"), ("G", "J"), ("H", "K"), ("I", "G"), ("J", "I"),\
                      ("K", "L"), ("L", "J")])
    sccs = kosaraju(G)
    for scc in sccs:
        print(scc)
        
    # pos = nx.spring_layout(G, seed=4120)
    pos = {"A": (0, 0), "B": (200, 0), "C": (400, 0), "D": (100, -200), "E": (200, -200),\
           "F": (400, -200), "G": (200, -400), "H": (400, -400), "I": (100, -600),\
            "J": (300, -600), "K": (400, -600), "L": (300, -800)}
    nx.draw(G, pos = pos, with_labels=True, font_weight='bold', node_color='skyblue', node_size=500, edge_color='gray', linewidths=2)
    plt.show()

if __name__=="__main__":
    test()