from collections import defaultdict

memo = defaultdict(int)
def memoized_fib(n):
    if n in memo:
        return memo[n]
    if n <= 2: f = 1
    else: f = memoized_fib(n-1) + memoized_fib(n-2)
    memo[n] = f
    return f

def bottomup_fib(n):
    fib = [0]*(n+1)
    for k in range(1, n+1):
        if k<= 2: f = 1
        else: f = fib[k-1] + fib[k-2]
        fib[k] = f
    return fib[n]

if __name__ == "__main__":
    n = 8
    print(f"The {n}th Fibonacci number is: {memoized_fib(n)} (using memoization)")
    print(f"The {n}th Fibonacci number is: {bottomup_fib(n)} (using bottom-up method)")