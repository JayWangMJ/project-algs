import networkx as nx
import matplotlib.pyplot as plt
import heapq

def dijkstra(G, s):
    # initialization
    for node in G.nodes:
        G.nodes[node]["d"] = float("inf")
        G.nodes[node]["pi"] = None
    G.nodes[s]["d"] = 0

    queue = [(0, s)]
    # main loop, do relaxation
    while queue:
        ele = heapq.heappop(queue)
        u = ele[1]
        # A node might be pushed in the queue multiple times with different u.d
        if ele[0] > G.nodes[u]["d"]:
            continue
        
        for v in G.neighbors(u):
            w = G.edges[(u, v)]["weight"]
            if G.nodes[u]["d"] + w < G.nodes[v]["d"]:
                G.nodes[v]["d"] = G.nodes[u]["d"] + w
                G.nodes[v]["pi"] = u
                heapq.heappush(queue, (G.nodes[v]["d"], v))
            
    # return G
        
def test():
    G = nx.DiGraph()
    edges = [
        ("s", "t", 10), ("s", "y", 5), ("t", "y", 2), ("t", "x", 1), ("y", "t", 3),\
        ("y", "x", 9), ("y", "z", 2), ("x", "z", 4), ("z", "x", 6), ("z", "s", 0)
    ]
    G.add_weighted_edges_from(edges)
    dijkstra(G, "s")
    for node in G.nodes:
        print(node, G.nodes[node])
    init_pos = {"s": (0, 0), "t": (200, 200), "y": (200, -200),\
                "x": (400, 200), "z": (400, -200)}
    # pos = nx.spring_layout(G, pos=init_pos, fixed=[0, 1, 2, 3, 4, 5, 6])
    pos = init_pos
    # nx.draw(G, pos = pos, with_labels=True, font_weight='bold', node_color='skyblue', node_size=500, edge_color='gray', linewidths=4)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_nodes(G, pos=pos, node_size=500)
    nx.draw_networkx_labels(G, pos=pos, font_weight="bold")
    straight_edges = [edges[i][0:2] for i in [0, 1, 3, 5, 6, 9]]
    curved_edges = [edges[i][0:2] for i in [2, 4, 7, 8]]
    nx.draw_networkx_edges(G, pos=pos, edgelist=straight_edges)
    nx.draw_networkx_edges(G, pos=pos, edgelist=curved_edges, connectionstyle="arc3,rad=0.25")
    # positions of labels are determined by pos of nodes
    # thus labels of multi-edges between two nodes overlap
    # need to modify the logic of drawing labels
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
    plt.show()

if __name__=="__main__":
    test()