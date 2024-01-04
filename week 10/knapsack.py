# Integer Kanpsack problem
# Input:
#   items: list of (size, value) pairs
#   size: total size
# Output:
#   max_value: maximum value with total weights <= size
#   selected: selected items
def knapsack(items, size):
    n = len(items)

    dp = [[0]*(size+1) for _ in range(n+1)]

    for x in range(size+1):
        for i in range(1, n+1):
            if items[i-1][0] <= x:
                dp[i][x] = max(dp[i-1][x], items[i-1][1]+dp[i-1][x-items[i-1][0]])
            else:
                dp[i][x] = dp[i-1][x]

    print(dp)

    # recover the solution
    selected = []
    i, w = n, size
    while i > 0 and w > 0:
        if dp[i][w] != dp[i-1][w]:
            selected.append(items[i-1])
            w -= items[i-1][0]
        i -= 1

    selected.reverse()

    return dp[n][size], selected

def knapsack_greedy(items, size):
    items.sort(key=lambda x: x[1]/x[0])
    items.reverse()
    v = 0
    selected = []
    w = size
    for item in items:
        if item[0] <= w:
            selected.append(item)
            v += item[1]
            w -= item[0]
    items.sort(key=lambda x: x[1])

    if v < items[-1][1]:
        v = items[-1][1]
        selected = items[-1]

    return v, selected

if __name__ == "__main__":
    items = [(2, 1), (2, 1), (3, 5)]
    size = 4
    v, selected = knapsack(items, size)
    print(f"Optimal v = {v}, selected = {selected}")
    v_greedy, selected_greedy = knapsack_greedy(items, size)
    print(f"Greedy algorithm gives v = {v_greedy}, selected = {selected_greedy}")