# Subsetsum problem
# Input:
#   numbers: list of numbers
#   d: desired sum
# Output:
#   True or False
#   whether there exists a subset of numbers whose sum is d

def subsetsum(numbers, d):
    n = len(numbers)

    dp = [[False]*(d+1) for _ in range(n+1)]
    for i in range(n+1):
        dp[i][0] = True

    for x in range(1, d+1):
        for i in range(1, n+1):
            if numbers[i-1] > x:
                dp[i][x] = dp[i-1][x]
            else:
                dp[i][x] = dp[i-1][x] or dp[i-1][x-numbers[i-1]]

    print(dp)
    return dp[n][d]

if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]
    d = 5
    print(subsetsum(numbers, d))