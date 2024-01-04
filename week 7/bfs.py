# Breadth first search
# Assume graph given in implicit form, 
# G.neighbors(u) returns neighbors of node u in G

import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def bfs(G, s):
    visited = set()
    frontier = deque([s])
    G.nodes[s]["level"] = 0
    G.nodes[s]["parent"] = s
    level = 1
    
    while frontier:
        next = deque()
        for u in frontier:
            if u not in visited:
                print(u, G.nodes[u])
                visited.add(u)
                for v in G.neighbors(u):
                    if v not in visited:
                        G.nodes[v]["level"] = level
                        G.nodes[v]["parent"] = u
                        next.append(v)
        frontier = next
        level += 1

def test():
    G = nx.Graph()
    G.add_edges_from([(1, 2), (1, 3), (2, 4), (2, 5), (3, 6)])

    print("BFS traversal starting from node 1:")
    bfs(G, 1)

    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()

if __name__=="__main__":    
    test()


