
# Longest common subsequence problem

def longest_common_subsequence(x, y):
    n = len(x)
    m = len(y)

    dp = [[0]*(m+1) for _ in range(n+1)]

    for i in range(1, n+1):
        for j in range(1, m+1):
            if x[i-1] == y[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    print(dp)

    lcs = []
    # lcs_length = dp[n][m]
    i = n
    j = m
    while i > 0 and j > 0:
        if x[i-1] == y[j-1]:
            lcs.append(x[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    lcs.reverse()
    return "".join(lcs)

if __name__ == "__main__":
    x = "ABCDBAB"
    y = "BDCABA"
    lcs = longest_common_subsequence(x, y)
    print(f"Longest common subsequence of x:{x}, and y:{y} is\n{lcs}")