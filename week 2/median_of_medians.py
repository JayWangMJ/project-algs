# Median finding problem
# Input: n different numbers, integer i
# Output: the element of rank i

import numpy as np

def select(s, rank):
    if len(s) <= 5:
        s = sorted(s)
        return s[rank-1]

    # first arrange S into columns of 5, drop the last column that's not full
    columns = []
    column = []
    for i in s:
        column.append(i)
        if len(column) == 5:
            columns.append(sorted(column))
            column = []
    
    medians = [column[2] for column in columns]
    median = select(medians, int(np.floor((len(medians)+1)/2)))

    B = []
    A = []
    for i in s:
        if i < median:
            B.append(i)
        elif i > median:
            A.append(i)
    k = len(B) + 1
    if k == rank:
        return median
    elif k > rank:
        return select(B, rank)
    else:
        return select(A, rank - k)
    
s = np.random.choice(range(4120), 23)
rank = 4
print(sorted(s))
print('rank', rank, "is:", select(s, rank))