import heapq
from cmath import inf
import numpy as np

# Min-heap implementation with 0-indexing

'''
# Python built-in heapq functions
hq = [5, 4, 3, 2, 1]
heapq.heapify(hq)
print("The created heap is", list(hq))
heapq.heappush(hq, 0)
print("The heap after pushing 0 is",list(hq))
print("Pop the smallest item", heapq.heappop(hq))
print("Pop the smallest item", heapq.heappop(hq))
'''

class MinHeap():
    def __init__(self):
        self.heap = []

    def get_heap(self):
        return self.heap

    def heap_is_empty(self):
        return len(self.heap) == 0

    def heap_insert(self, item):
        self.heap.append(item)
        self.sift_up(len(self.heap) - 1)

    def heap_min(self):
        return self.heap[0]

    def heap_extract_min(self):
        '''last = self.heap.pop() # list.pop() will raise error if list is empty
        if self.heap: # if the original heap contains more than one item
            ret = self.heap_min()
            self.heap[0] = last
            self.sift_down(0)
            return ret
        return last'''
        ret = self.heap_min()
        self.heap_delete(ret)
        return ret

    def heap_delete(self, x):
        pos = self._find(x)
        # find runs in O(n) while below deletion process runs in O(log n)
        # always O(1) for finding min
        if pos == -1:
            raise ValueError("delete non-existing element")
        if pos == len(self.heap) - 1:
            self.heap.pop()
            return
        self.heap[pos], self.heap[len(self.heap) - 1] = self.heap[len(self.heap) - 1], self.heap[pos]
        self.heap.pop()
        if self.heap:
            if pos == 0:
                self.sift_down(pos)
            elif self.heap[pos] < self.heap[(pos - 1) // 2]:
                self.sift_up(pos)
            elif self.heap[pos] > self.heap[(pos - 1) // 2]:
                self.sift_down(pos)


    def heap_successor(self, x):
        ret = inf
        for i in range(0, len(self.heap)):
            if self.heap[i] > x and self.heap[i] < ret:
                ret = self.heap[i]
        return ret

    def heap_find(self, x):
        for i in range(len(self.heap)):
            if self.heap[i] == x:
                return i
        return -1

    def _find(self, x):
        for i in range(len(self.heap)):
            if self.heap[i] == x:
                return i
        return -1

    def heap_heapify(self, lst):
        # transform list into a heap, in-place, in O(len(lst)) time
        self.heap = lst
        for i in reversed(range(len(lst) // 2)):
            self.sift_down(i)

    # sift up the item at pos
    def sift_up(self, pos):
        newItem = self.heap[pos]
        while pos > 0:
            parentPos = (pos - 1) // 2
            parent = self.heap[parentPos]
            if newItem < parent:
                self.heap[pos] = parent
                pos = parentPos
                continue
            break
        self.heap[pos] = newItem
    
    # sift down the item at pos
    def sift_down(self, pos):
        size = len(self.heap)
        startPos = pos
        newItem = self.heap[pos]
        childPos = 2 * pos + 1 # left child
        while childPos < size:
            # set childPos to the smaller child
            rightChildPos = childPos + 1
            if rightChildPos < size and self.heap[rightChildPos] < self.heap[childPos]:
                childPos = rightChildPos
            if self.heap[pos] > self.heap[childPos]:
                self.heap[pos], self.heap[childPos] = self.heap[childPos], self.heap[pos]
            pos = childPos
            childPos = 2 * pos + 1

    def heap_sort(self):
        ret = []
        while self.heap:
            ret.append(self.heap_extract_min())
        self.heap = ret
        return ret
    
if __name__ == "__main__":    
    my_heap = MinHeap()
    my_heap.heap_heapify(list(np.random.randint(0, 4120, 23)))
    print("The heap is:", my_heap.get_heap())
    print("Extract min:", my_heap.heap_extract_min())
    print("The heap is:", my_heap.get_heap())
    my_heap.heap_insert(0)
    print("After insterting 2023:", my_heap.get_heap())
    print("Heap sort:", my_heap.heap_sort())