import networkx as nx
import matplotlib.pyplot as plt

# A minimal implementation for a graph represented in adjacency matrix form
class AdjacencyMatrix():
    def __init__(self, n):
        self.n = n
        self.mat = [[0]*n for _ in range(n)]

    def add_edge(self, v1, v2, weight=1):
        self.mat[v1][v2] = weight
        self.mat[v2][v1] = weight # Comment this out for directed graph

    def display(self):
        G = nx.Graph()
        G.add_nodes_from(range(self.n))
        G.add_weighted_edges_from([(u, v, w) for u, row in enumerate(self.mat) for v, w in enumerate(row) if w > 0])
        pos = nx.spring_layout(G, seed=4120)
        nx.draw(G, pos=pos, with_labels=True, font_weight='bold')
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
        plt.show()

# A minimal implementation for a graph represented in adjacency list form
class AdjacencyList():
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]

    def add_edge(self, v1, v2, weight=1):
        self.graph[v1].append((v2, weight))
        self.graph[v2].append((v1, weight)) # Comment this out for directed graph

    def display(self):
        G = nx.Graph() # G = nx.Digraph() for directed graph
        G.add_nodes_from(range(self.n))
        G.add_weighted_edges_from([(u, v, w) for u, neighbour in enumerate(self.graph) for (v, w) in neighbour if w > 0])
        pos = nx.spring_layout(G, seed=4120)
        nx.draw(G, pos=pos, with_labels=True, font_weight='bold')
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
        plt.show()

def test():
    g = AdjacencyMatrix(4)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.display()

    g2 = AdjacencyList(4)
    g2.add_edge(0, 1, 2)
    g2.add_edge(0, 2, 6)
    g2.add_edge(1, 2, 8)
    g2.add_edge(2, 3, 7)
    g2.display()

if __name__=="__main__":
    test()