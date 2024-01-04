import networkx as nx
import matplotlib.pyplot as plt
import heapq

def bi_dijkstra(G, s, t):
    # initialization
    for node in G.nodes:
        G.nodes[node]["f_d"] = float("inf")
        G.nodes[node]["f_pi"] = None
        G.nodes[node]["b_d"] = float("inf")
        G.nodes[node]["b_pi"] = None
    G.nodes[s]["f_d"] = 0
    G.nodes[t]["b_d"] = 0
    G_reversed = G.reverse()

    f_queue = [(0, s)]
    b_queue = [(0, t)]
    f_searched = set()
    b_searched = set()
    meet = False
    # main loop, do relaxation
    while f_queue and b_queue and not meet:
        # Forward search
        ele = heapq.heappop(f_queue)
        u = ele[1]
        # A node might be pushed in the queue multiple times with different u.d
        if ele[0] > G.nodes[u]["f_d"]:
            continue

        f_searched.add(u)
        
        for v in G.neighbors(u):
            w = G.edges[(u, v)]["weight"]
            if G.nodes[u]["f_d"] + w < G.nodes[v]["f_d"]:
                G.nodes[v]["f_d"] = G.nodes[u]["f_d"] + w
                G.nodes[v]["f_pi"] = u
                heapq.heappush(f_queue, (G.nodes[v]["f_d"], v))
        
        if u in b_searched:
            print("meet forward at", u)
            meet = True
            break

        # Backward search
        ele = heapq.heappop(b_queue)
        u = ele[1]
        # A node might be pushed in the queue multiple times with different u.d
        if ele[0] > G.nodes[u]["b_d"]:
            continue
        
        b_searched.add(u)

        for v in G_reversed.neighbors(u):
            w = G.edges[(v, u)]["weight"]
            if G.nodes[u]["b_d"] + w < G.nodes[v]["b_d"]:
                G.nodes[v]["b_d"] = G.nodes[u]["b_d"] + w
                G.nodes[v]["b_pi"] = u
                heapq.heappush(b_queue, (G.nodes[v]["b_d"], v))

        if u in f_searched:
            print("meet back at", u)
            meet = True
            break

    if meet:
        return sorted([(u, G.nodes[u]["f_d"]+G.nodes[u]["b_d"]) for u in f_searched], \
                      key=lambda x: x[1])[0][0]
    return None

def recover_sp(G, s, t, node):
    ret = [node]
    f = G.nodes[node]["f_pi"]
    b = G.nodes[node]["b_pi"]
    while ret[0] != s and ret[-1] != t:
        ret.insert(0, f)
        ret.append(b)
        f = G.nodes[f]["f_pi"]
        b = G.nodes[b]["b_pi"]
    while ret[0] != s:
        ret.insert(0, f)
        f = G.nodes[f]["f_pi"]
    while ret[-1] != t:
        ret.append(b)
        b = G.nodes[b]["b_pi"]
    return ret

def test():
    G = nx.DiGraph()
    edges = [
        ("s", "u", 3), ("s", "w", 5), ("u", "z", 3), ("w", "t", 5), ("z", "t", 3)
    ]
    G.add_weighted_edges_from(edges)
    meeted = bi_dijkstra(G, "s", "t")
    print("Node on the shortest path:", meeted)
    print(f"Shortes path from s to t {recover_sp(G, 's', 't', meeted)}")
    for node in G.nodes:
        print(node, G.nodes[node])
    init_pos = {"s": (0, 0), "t": (400, 0), "u": (100, 100), "z": (300, 100), "w": (200, -100)}
    # pos = nx.spring_layout(G, pos=init_pos, fixed=[0, 1, 2, 3, 4, 5, 6])
    pos = init_pos
    nx.draw(G, pos = pos, with_labels=True, font_weight='bold', node_color='skyblue', node_size=500, edge_color='gray', linewidths=4)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
    plt.show()

    for neighbor, weight in G["t"].items():
        print(neighbor, weight)

if __name__=="__main__":
    test()