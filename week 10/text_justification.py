# Dynamic programming algorithm for text justification problem
# Input: 
#   text: list of text words, e.g. ["hello", "world"]
#   page_width: integer, width of page

def text_justification(text, page_width):
    def get_length(i, j):
        ret = 0
        for m in range(i, j):
            ret += (len(text[i]) + 1)
        return ret-1
    def get_line_cost(i, j):
        length = get_length(i, j)
        if length > page_width:
            return float("inf")
        return (page_width - length)**2
    
    #length[i][j]: total space needed for words 1, ..., j
    n = len(text)
    length = [[0]*n for _ in range(n)]
    for i in range(n):
        length[i][i] = len(text[i])
        for j in range(i+1, n):
            length[i][j] = length[i][j-1] + len(text[j]) + 1

    # line_cost[i][j]: cost of putting words i to j(including) in one line
    line_cost = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            if length[i][j] > page_width:
                line_cost[i][j] = float("inf")
            else:
                line_cost[i][j] = (page_width-length[i][j])**2

    # DP algotirhm
    # DP[i] = min_{j} {line_cost(i, j-1)+DP[j], DP[i]}
    #   j = i+1, ..., n,  i = 0, ..., n-1
    # DP[n] = 0
    # cut[i]: cut at cut[i], i.e., line is i, i+1, ..., cut[i]-1
    dp = [0]*n
    cut = [n]*n
    for i in reversed(range(n)):
        dp[i] = line_cost[i][n-1]
        cut[i] = n
        for j in range(i+1, n):
            if line_cost[i][j-1] == float("inf"):
                continue
            if line_cost[i][j-1] + dp[j] < dp[i]:
                dp[i] = line_cost[i][j-1] + dp[j]
                cut[i] = j

    # construct the solution
    ret = []
    i = 0
    while i < n:
        j = cut[i]
        ret.append(' '.join(text[i:j]))
        i = j

    return ret

if __name__=="__main__":
    text = ["2023-2024", "Term 2", "CSC4120", "Design", "and", "Analysis", "of", "Algorithms."]
    page_width = 16
    justified_text = text_justification(text, page_width)
    for line in justified_text:
        print(line)