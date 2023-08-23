# String matching algorithms
# CLRS ch.32

import numpy as np

# input alphabet
SIGMA = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'G', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
         '0', '1', '2', '3','4', '5', '6', '7', '8', '9',
         ' ', ',', '.')

element_considered = 0

# check whether two strings are the same
# by comparing each char one by one
def check_same(x, y):
    global element_considered
    if len(x) != len(y):
        return False
    for i in range(len(x)):
        element_considered += 1
        if x[i] != y[i]:
            return False
    return True

# Naive string matching algorithm
# Preprocessing time: 0 
# Matching time (worst case): O((n-m+1)m)
# CLRS p.988
def naive_string_matcher(txt, pat):
    global element_considered
    element_considered = 0
    n = len(txt)
    m = len(pat)
    print("\nNaive string matcher...")
    for i in range(n - m + 1):
        if check_same(txt[i:i+m], pat):
            print("Pattern occurs at index", i)
    print("Number of elements considered:", element_considered)

# rabin-karp algorithm
# Preprocessing time: \Theta(m)
# Matching time (worst case): O((n-m+1)m)
# CLRS p.993
# d is the size of the input alphabet, default is 256 of ASCII table
# q is a prime number larger than m
def rabin_karp_matcher(txt, pat, q, d = 256):
    global element_considered
    n = len(txt)
    m = len(pat)
    # h = d**(m-1)%q
    h = 1
    p = 0
    t = 0
    element_considered = 0
    print("\nRabin-karp matcher...")
    for _ in range(m-1):
        h = (h*d)%q

    # preprocessing
    for i in range(m):
        p = (d * p + ord(pat[i])) % q
        t = (d * t + ord(txt[i])) % q
        element_considered += 1

    pre_element_considered = element_considered
    # matching
    for i in range(n - m + 1):
        if p == t:
            print("Hit at", i)
            if check_same(txt[i:i+m], pat):
                print("Pattern occurs at index", i)
        if i < n - m:
            t = ((d*(t - ord(txt[i])*h)) + ord(txt[i + m])) % q
            element_considered += 1
    print("Number of elements considered:", element_considered)
    print("where number of elements considered in preprocessing is", pre_element_considered)
    print("the number in matching process is", element_considered - pre_element_considered)

# finite automaton matcher
# Preprocessing time: O(m^3*|SIGMA|), can be reduced to O(m|\Sigma|)
# Matching time: \Theta(n)
# CLRS p.999
def finite_automaton_matcher(txt, pat, alphabet):
    global element_considered
    n = len(txt)
    m = len(pat)
    q = 0
    element_considered = 0

    print("\nFinite automaton matcher...")

    # preprocessing, calculate trasition funciton, which is a (m+1)x(|alphabet|) table
    transition_function = compute_transition_function(pat, alphabet)
    pre_element_considered = element_considered

    # matching
    for i in range(n):
        q = transition_function[q, alphabet.index(txt[i])]
        element_considered += 1
        if q == m:
            print("Pattern occurs at index", i - m + 1)
    print("Number of elements considered:", element_considered)
    print("where number of elements considered in preprocessing is", pre_element_considered)
    print("the number in matching process is", element_considered - pre_element_considered)

# compute trasition fuction of pattern over alphabet
# CLRS p.1001
def compute_transition_function(pat, alphabet):
    global element_considered
    m = len(pat)
    delta = np.zeros((m+1, len(alphabet)), dtype=int)
    for q in range(m+1):
        for i, a in enumerate(alphabet):
            k = min(m, q+1)
            while True:
                element_considered += 1
                if is_suffix(pat[:k], pat[:q]+a):
                    break
                k -= 1
            delta[q, i] = k
    return delta

# check whether x is a suffix of y
def is_suffix(x, y):
    global element_considered
    # print(x, y)
    n = len(x)
    if n == 0:
        element_considered += 1
        return True
    m = len(y)
    for i in range(n):
        element_considered += 1
        if x[n-1-i] != y[m-1-i]:
            return False
    return True

# Knuth-Morris-Pratt algorithm
# Preprocessing time amortized: \Theta(m)
# Matching time amortized: \Theta(n)
# CLRS p.1005
def KMP_matcher(txt, pat):
    global element_considered
    n = len(txt)
    m = len(pat)
    q = 0
    element_considered = 0

    print("\nKMP matcher...")

    prefix_function = compute_prefix_function(pat)
    pre_element_considered = element_considered
    # print(prefix_function)

    for i in range(n):
        while q > 0 and pat[q] != txt[i]:
            element_considered += 1
            q = prefix_function[q-1]
        element_considered += 1
        if pat[q] == txt[i]:
            q += 1
        if q == m:
            print("Pattern occurs at index", i - m + 1)
            q = prefix_function[q-1]
    print("Number of elements considered:", element_considered)
    print("where number of elements considered in preprocessing is", pre_element_considered)
    print("the number in matching process is", element_considered - pre_element_considered)

# compute prefix function
# CLRS p.1006
def  compute_prefix_function(pat):
    global element_considered
    m = len(pat)
    pi = np.zeros(m, dtype=int)
    # pi[0] = 0
    k = 0
    for q in range(1, m):
        while k > 0 and pat[k] != pat[q]:
            element_considered += 1
            k = pi[k-1]
        element_considered += 1
        if pat[k] == pat[q]:
            k += 1
        pi[q] = k
    return pi

if __name__ == "__main__":
    txt = "CSC4120 Design and analysis is the greatest course ever" # n = 56
    pat = "greatest course" # m = 15, match at 35
    naive_string_matcher(txt, pat)
    rabin_karp_matcher(txt, pat, 17)
    finite_automaton_matcher(txt, pat, SIGMA)
    KMP_matcher(txt, pat)
    # KMP_matcher("ababbbabababbbab", "aba")