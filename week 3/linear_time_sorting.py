import numpy as np
from copy import deepcopy

k = 4120  # upper bound in counting sort
radix = 10  # radix(base) in radix sort
digits = 3  # number of digits in radix sort
num = 23  # number of elements to generate

def counting_sort(a):
    ret = []
    n = len(a)
    b = [[] for _ in range(k)]
    for j in range(n):
        b[a[j]].append(a[j])
    for i in range(k):
        if b[i]:
            ret.extend(b[i])
    return ret

def radix_sort(a):
    # assume the number is in big-endian, 
    # i.e. 174 is stored as [1, 7, 4]
    b = [[] for _ in range(radix)]  # auxilary counting sort table
    digit = digits - 1
    while digit >= 0:
        for i in range(len(a)):
            b[a[i, digit]].append(deepcopy(a[i])) # a is a pointer to a np array
        idx = 0
        for i in range(radix):
            while b[i]:
                a[idx] = b[i].pop(0)
                idx += 1
        digit -= 1
    return a

if __name__ == "__main__":
    print(counting_sort(np.random.randint(0, k, num)))
    print(radix_sort(np.random.randint(0, radix, (num, digits))))