# Sorter using quick sort algorithm
# Provide three pivot choosing rules (QuickSort.rule):
#   1. pick the first element
#   2. pick the median (sorted) element
#   3. pick a random element
# Call QuickSort.quicksort(s) to sort an array s


import numpy as np
from time import time

class QuickSort():
    def __init__(self, rule=2):
        self.rule = rule

    def set_s(self, s):
        self.s = s
        print("set s")
        print(self.s)

    def set_pivot_rule(self, rule):
        self.rule = rule

    def get_pivot(self, low, high):
        # get the index of the pivot
        # basic: pick the first element
        if self.rule == 1:
            return low
        # median: pick the median element
        if self.rule == 2:
            return self._find_median(low, high)
        # random: pick a random element
        if self.rule == 3:
            return np.random.choice(range(low, high))
    
    def quick_sort(self, s = None):
        if s is not None:
            self.s = s
        self._quick_sort(0, len(self.s))
        return self.s

    def _quick_sort(self, low, high):
        if low >= high:
            return
        # get pivot
        pivot_idx = self.get_pivot(low, high)
        # partition
        rank = self._partition(low, high, pivot_idx)
        # divide and conquer
        self._quick_sort(low, rank-1)
        self._quick_sort(rank, high)

    def _partition(self, low, high, pivot):
        self.s[low], self.s[pivot] = self.s[pivot], self.s[low]
        pivot = low
        rank = low
        for i in range(low, high):
            if self.s[i] <= self.s[pivot]:
                self.s[rank], self.s[i] = self.s[i], self.s[rank]
                rank += 1
        self.s[rank-1], self.s[pivot] = self.s[pivot], self.s[rank-1]
        return rank

    def _find_median(self, low, high):
        # find median elements among elements self.s[low:high]
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
            
        s = self.s[low:high]
        median = select(s, int(np.floor((len(s)+1)/2)))
        for i in range(len(s)):
            if s[i] == median:
                return low + i
    
if __name__ == "__main__":
    # compare running time of different pivots
    my_quick_sorter_first = QuickSort(1)   
    my_quick_sorter_median = QuickSort(2)
    my_quick_sorter_random = QuickSort(3)    
    times = []
    s = np.random.randint(0, 4120, 1000)

    # pivot: first element
    start_time = time()
    for _ in range(100):
        my_quick_sorter_first.quick_sort(s)
    times.append(time()-start_time)
    print(f"Choosing first element as pivot, time: {times[-1]:.4f}s")

    # pivot: median
    start_time = time()
    for _ in range(100):
        my_quick_sorter_median.quick_sort(s)
    times.append(time()-start_time)
    print(f"Choosing median as pivot, time: {times[-1]:.4f}s")

    # pivot: random
    start_time = time()
    for _ in range(100):
        my_quick_sorter_random.quick_sort(s)
    times.append(time()-start_time)
    print(f"Choosing random element as pivot, time: {times[-1]:.4f}s")

    """
    One experiment:
    first: 4.0252s,
    median: 0.5656s,
    random: 0.6990s
    """