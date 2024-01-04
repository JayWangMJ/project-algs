# Floyd-warshall algorithm to find the shortest paths
# between all pairs of nodes in a graph 
# Assume graph given in adjacency list form

def floyd_warshall(G):
    n = len(G)

    # Initialize the distance matrix    
    d = [[float("inf") for _ in range(n)] for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
        for (j, w) in G[i]:
            d[i][j] = w

    for m in range(n):
        for i in range(n):
            for j in range(n):
                d[i][j] = min(d[i][j], d[i][m]+d[m][j])

    return d

if __name__=="__main__":
    """
        -1>    (1)
            |      <
    (0)     3      4
            >      | 
        -2>    (2)
    """
    G = [
        [(1, 1), (2, 2)],
        [(2, 3)],
        [(1, 4)]
    ]

    d = floyd_warshall(G)
    print(d)