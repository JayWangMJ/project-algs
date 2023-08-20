"""
A van Emde Boas tree, also known as a vEB tree, implements an associative array (dictionary) 
with n-bit integer keys among the universe {0, 1, \cdots, u - 1}. 
It performs all operations (insert, delete, successor...) in O(loglog u) time.

A vEB tree for a universe with size u is implemented recursively by 
dividing the universe into \sqrt{u} size-\sqrt{u} vEB trees, 
where the ith subtree stores keys among {i\sqrt{u}, ..., (i + 1)\sqrt{u} - 1}.

A vEB tree stores following information:
* u, to store the universe size.
* min, to store the minimum element. It is stored outside the structure.
* max, to store the maximum element.
* cluster array, of size \sqrt{u} that points to children vEB trees.
* summary, an auxiliary vEB tree to keep track of emptiness of subtree/cluster.
"""

import numpy as np

class VEBTree():
    def __init__(self, u):
        self.u = u
        self.min = None
        self.max = None
        if u <= 2:
            self.summary = None
            self.clusters = None
        else:
            self.summary = VEBTree(np.ceil(np.sqrt(u)))
            self.clusters = [VEBTree(np.ceil(np.sqrt(u))) for _ in range(np.ceil(np.sqrt(u)))]

    def high(self, x):
        return np.floor(x / np.ceil(np.sqrt(self.u)))

    def low(self, x):
        return x % np.ceil(np.sqrt(self.u))

    def index(self, high, low):
        return high * np.ceil(np.sqrt(self.u)) + low

    def VEB_min(self):
        return self.min

    def VEB_extract_min(self):
        ret = self.VEB_min()
        self.VEB_delete(ret)
        return ret

    def VEB_max(self):
        return self.max

    def is_empty(self):
        return self.min is None

    def VEB_find(self, x):
        # find x in a VEB tree, return True/False
        if self.u <= x:
            return False
        if self.min == x or self.max == x:
            return True
        if self.u == 2: 
            # if the size is 2, x must be min or max
            return False
        return self.clusters[self.high(x)].VEB_find(self.low(x))

    def VEB_insert(self, x):
        '''
        insert x into a vEB tree
        if u == 2, it is redundant to create subtrees 
        since it already stores min and max
        '''
        if self.is_empty():
            self.min = self.max = x
            return
        if x < self.min:
            x, self.min = self.min, x
        if x > self.max:
            self.max = x
        if self.u > 2:
            if self.clusters[self.high(x)].is_empty():
                self.summary.VEB_insert(self.high(x))
            self.clusters[self.high(x)].VEB_insert(self.low(x))

    def VEB_delete(self, x):
        # if not self.contains(x):
        #    print("ERROR: %d is not in the tree!"%x)
        #    return
        
        # assume x is in the tree
        
        # if the tree has only one element, directly delete it
        if self.min == self.max:
            self.min = self.max = None
        # base case where the size is 2. It must have 2 distinct elements (0, 1).
        # delete one of them
        elif self.u == 2:
            if x == 0:
                self.min = self.max = 1
            else:
                self.min = self.max = 0
        # general case
        else:
            # find new min
            if x == self.min:
                i = self.summary.min
                # i must exist since the tree must have more than 2 elements to enter this block
                x = self.min = self.index(i, self.clusters[i].min)
            # delete x
            high = self.high(x)
            self.clusters[high].VEB_delete(self.low(x))
            # if the cluster becomes empty, update summary
            if self.clusters[high].is_empty():
                self.summary.VEB_delete(high)
            # update max if the previous max is deleted
            if x == self.max:
                # has only one element 
                if self.summary.max is None:
                    self.max = self.min
                else:
                    i = self.summary.max
                    self.max = self.index(i, self.clusters[i].max)

    def VEB_successor(self, x):
        # return the successor of x (the smallest element larger than x)
        # base case 
        if self.is_empty():
            return None
        # if u == 2, has successor only if x = 0 and contains 1
        if self.u == 2:
            if x == 0 and self.max == 1:
                return 1
            return None
        # general case
        if x < self.min:
            return self.min
        if x >= self.max:
            return None
        i = self.high(x)
        if (not self.clusters[i].is_empty()) and self.low(x) < self.clusters[i].max:
            j = self.clusters[i].VEB_successor(self.low(x))
        else:
            i = self.summary.VEB_successor(i)
            if i is None:
                return None
            j = self.clusters[i].min
        return self.index(i, j)

    def VEB_predecessor(self, x):
        '''
        return the predecessor of x (the largest element smaller than x)
        '''
        if self.is_empty():
            return None
        if self.u == 2:
            if x == 1 and self.min == 0:
                return 0
            return None
        if x > self.max:
            return self.max
        if x <= self.min:
            return None
        i = self.high(x)
        if (not self.clusters[i].is_empty()) and self.low(x) > self.clusters[i].min:
            j = self.clusters[i].VEB_predecessor(self.low(x))
        else:
            i = self.summary.VEB_predecessor(i)
            if i is None:
                return self.min # remember min is stored outside the structure!
            j = self.clusters[i].max
        return self.index(i, j)
    