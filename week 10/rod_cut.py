# rod cutting problem
# CLRS ch15.1, p.365,366

def memoized_cut_rod(p, n):
    r = [-1 for _ in range(n+1)]
    return memoized_cut_rod_aux(p, n, r)

def memoized_cut_rod_aux(p, n, r):
    if r[n] >= 0:
        return r[n]
    if n == 0:
        q = 0
    else: q = -1
    for i in range(n):
        q = max(q, p[i]+memoized_cut_rod_aux(p, n-i-1, r))
    r[n] = q
    return q

def bottom_up_cut_rod(p, n):
    r = [0]*(n+1)

    for j in range(1, n+1):
        q = -1 
        for i in range(j):
            q = max(q, p[i]+r[j-i-1])
        r[j] = q
    return r[n]

if __name__=="__main__":
    prices = [1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
    n = 4
    print(memoized_cut_rod(prices, n))
    print(bottom_up_cut_rod(prices, n))