# Peak finding problem
# Input: an array of integers.
# Output: a peak element of the array, which is not smaller than its neighbors.

import numpy as np

N = 23  # len of the array
NUM_MIN = 0  # minimum number
NUM_MAX = 4120  # maximum number

# Lemma: there always exists a peak in any array
# Proof: think of starting from the first element 
# and keeping going right if the right is larger
# this will eventually stop at a peak

# Find any peak of a one dimension array using recursive binary search
# Consider the mid element:
#   If it is a peak, done.
#   Else if it is smaller than its left neighbour, then there must exist a peak
# in the left half, which is also a global peak.
#   Else there must exist a global peak in the right half.
def one_dim_peak_finding(a):
    n = len(a)
    # base case
    if n == 1:
        return a[0]
    # recursion
    else:
        mid = n // 2
        if a[mid - 1] > a[mid]:
            return one_dim_peak_finding(a[:mid])
        elif (mid < n - 1) and (a[mid] < a[mid + 1]):
            return one_dim_peak_finding(a[mid:])
        else:
            return a[mid]

# Find any peak of a two-d array using the one-d method
# For each column, find its global maximum elements.
# Find the peak of all the column max.     
def two_dim_peak_finding_use_one_dim(a):
    b = []
    for j in range(N):
        b.append(np.max(a[:, j]))
    return one_dim_peak_finding(b)

# Find the global max element in the window frame
def get_global_max_of_window_frame(a):
    n = a.shape[1]
    m =  NUM_MIN - 1
    m_idx = (-1, -1)
    for i in range(n):
        if a[0, i] > m:
            m = a[0, i]
            m_idx = (0, i)
        if a[n//2, i] > m:
            m = a[n//2, i]
            m_idx = (n//2, i)
        if a[n-1, i] > m:
            m = a[n-1, i]
            m_idx = (n-1, i)
        if a[i, 0] > m:
            m = a[i, 0]
            m_idx = (i, 0)
        if a[i, n//2] > m:
            m = a[i, n//2]
            m_idx = (i, n//2)
        if a[i, n-1] > m:
            m = a[i, n-1]
            m_idx = (i, n-1)
    return m_idx

# Get neighbors of an element.
# Always return a 4-element list (filled with NUM_MIN - 1).
# [up, down, left, right]
def get_neighbors(a, x, y):
    n = a.shape[1]  
    neighbors = [NUM_MIN - 1 for _ in range(4)]
    if x != 0:
        neighbors[0] = a[x-1, y]
    if x != n-1:
        neighbors[1] = a[x+1, y]
    if y != 0:
        neighbors[2] = a[x, y-1]
    if y != n-1:
        neighbors[3] = a[x, y+1]
    return neighbors


# Find ant peak of a 2d array using divide and conquer
def two_dim_peak_finding(a):
    n = a.shape[1]
    if n <= 3:
        return np.max(a)  # the window frame covers all elements
    else:
        # find the global max element in the window frame
        m_idx = get_global_max_of_window_frame(a)
        # check if m is a peak, first get its neighbours
        neighbors = get_neighbors(a, m_idx[0], m_idx[1])
        # if m is a peak
        if a[m_idx] >= np.max(neighbors):
            return a[m_idx]
        # else pick a sub-square among four candidates (up-left, up-right, bottom-left, bottom-right)
        else:
            if m_idx[0] == 0 and m_idx[1] < n//2:
                return two_dim_peak_finding(a[1:n//2, 1:n//2])  # up-left
            if m_idx[0] == 0 and m_idx[1] > n//2:
                return two_dim_peak_finding(a[1:n//2, n//2+1:n-1])  # up-right
            if m_idx[0] == n//2 and m_idx[1] < n//2:
                if neighbors[0] >= neighbors[1]:  # up-neighbor > down-neighbor
                    return two_dim_peak_finding(a[1:n//2, 1:n//2])
                else:
                    return two_dim_peak_finding(a[n//2+1:n-1, 1:n//2])  # bottom-left
            if m_idx[0] == n//2 and m_idx[1] > n//2:
                if neighbors[0] >= neighbors[1]: 
                    return two_dim_peak_finding(a[1:n//2, n//2+1:n-1])
                else:
                    return two_dim_peak_finding(a[n//2+1:n-1, n//2+1:n-1])  # bottom-right
            if m_idx[1] < n//2 and m_idx[1] == n//2:
                if neighbors[2] >= neighbors[3]:  # left-neighbor > right-neighbor
                    return two_dim_peak_finding(a[1:n//2, 1:n//2])
                else:
                    return two_dim_peak_finding(a[1:n//2, n//2+1:n-1])
            if m_idx[1] > n//2 and m_idx[1] == n//2:
                if neighbors[2] >= neighbors[3]:
                    return two_dim_peak_finding(a[n//2+1:n-1, 1:n//2]) 
                else:
                    return two_dim_peak_finding(a[n//2+1:n-1, n//2+1:n-1])
            if m_idx[0] == n - 1 and m_idx[1] < n//2:
                return two_dim_peak_finding(a[n//2+1:n-1, 1:n//2])
            if m_idx[0] == n - 1 and m_idx[1] > n//2:
                return two_dim_peak_finding(a[n//2+1:n-1, n//2+1:n-1])
            if m_idx[0] < n//2 and m_idx[1] == 0:
                return two_dim_peak_finding(a[1:n//2, 1:n//2])
            if m_idx[0] > n//2 and m_idx[1] == 0:
                return two_dim_peak_finding(a[n//2+1:n-1, 1:n//2])
            if m_idx[0] < n//2 and m_idx[1] == n - 1:
                return two_dim_peak_finding(a[1:n//2, n//2+1:n-1])
            if m_idx[0] > n//2 and m_idx[1] == n - 1:
                return two_dim_peak_finding(a[n//2+1:n-1, n//2+1:n-1])
            

if __name__ == "__main__":
    a = np.random.randint(NUM_MIN, NUM_MAX, N)
    print(a)
    print("1d peak finding:", one_dim_peak_finding(a))
    
    a = np.random.randint(NUM_MIN, NUM_MAX, (N, N))
    print(a)
    print("2d peak finding using 1d:", two_dim_peak_finding_use_one_dim(a))
    print("2d peak finding using recursion:", two_dim_peak_finding(a))


"""a = np.array([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 3, 3, 3, 2, 1, 2, 2, 2, 1],
        [1, 4, 5, 3, 2, 1, 2, 2, 2, 1],
        [1, 3, 3, 3, 2, 1, 2, 2, 2, 1],
        [1, 3, 3, 3, 2, 1, 2, 2, 2, 1],
        [1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 2, 2, 2, 1, 2, 2, 2, 1],
        [1, 2, 2, 2, 2, 1, 2, 2, 2, 1],
        [1, 2, 2, 2, 2, 1, 2, 2, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
])

print("2d peak finding using recursion:", two_dim_peak_finding(a))"""


"""a = np.array([
        [8, 24, 67, 87, 79],
        [48, 10, 94, 52, 98],
        [53, 66, 98, 14, 34],
        [24, 15, 60, 58, 16],
        [ 9, 93, 86,  2, 27]
    ])

mask = np.array([
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0]
    ]).astype(bool)

print(mask)

def find_neighbors(a, i, j):
    print(i, j)
    print(a[i-1:i+2, j-1:j+2])
    return a[i-1:i+2, j-1:j+2][mask]

print(find_neighbors(a, 2, 3))
print(find_neighbors(a, 0, 0))"""