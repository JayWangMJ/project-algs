
# parenthesization for matrix multiplication
# Input: a[i]: (m, n) the i-th matrix is mxn
# Output: dp: the dp table
#   paren: the parent pointers
def parenthesization(a):
    n = len(a)
    dp = [[0]*n for _ in range(n)]
    paren = [[0]*n for _ in range(n)]
    for i in range(n):
        dp[i][i] = 0

    for l in range(2, n+1):
        for i in range(n-l+1):
            j = i + l - 1
            dp[i][j] = float("inf")
            for k in range(i, j):
                cost = dp[i][k] + dp[k+1][j] + a[i][0]*a[k][1]*a[j][1]
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    paren[i][j] = k

    return dp, paren

def print_optimal_parentheses(paren, i, j):
    if i == j:
        print(f"A{i + 1}", end="")
    else:
        print("(", end="")
        print_optimal_parentheses(paren, i, paren[i][j])
        print_optimal_parentheses(paren, paren[i][j] + 1, j)
        print(")", end="")   

if __name__=="__main__":
    A = [(5, 1), (1,5), (5, 1), (1, 4), (4, 2)]
    dp, paren = parenthesization(A)
    print(dp)
    # k*: 0-indexed
    print(paren)
    # recover solution
    print_optimal_parentheses(paren, 0, len(A)-1)