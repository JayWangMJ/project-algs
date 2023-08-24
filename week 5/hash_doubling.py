# A simple hash table with table doubling and linear probing

import numpy as np
import time

class HashDoubling():
    def __init__(self, threshold = 0.75, hash_function = None):
        self.size = 2
        self.n = 0
        self.table = np.empty(2, dtype=object)
        self.threshold = threshold
        self._hash_function = hash_function
        if hash_function is None:
            self._hash_function = hash

    def hash_function(self, key, i):
        return (self._hash_function(key) + i) % self.size

    def _rehash(self):
        new_table = np.empty(2*self.size, dtype=object)
        for bucket in self.table:
            if bucket:
                self._insert(bucket, new_table)
        self.table = new_table
        self.size *= 2

    def _insert(self, key, table = None):
        if table is None:
            table = self.table
        i = 0
        m = len(table)
        while i < m:
            j = self.hash_function(key, i)
            if table[j] is None:
                table[j] = key
                break
            i += 1
        if i == m:
            print("hash table overflow")

    def insert(self, key):
        if self.n / self.size >= self.threshold:
            self._rehash()
        self._insert(key)
        self.n += 1
    
    def search(self, key):
        i = 0
        while i < self.size:
            j = self.hash_function(key, i)
            if self.table[j] is None:
                return None
            if self.table[j] == key:
                return j
            i += 1
        return None
    
if __name__ == "__main__":
    n = 10000
    keys = np.random.randint(0, 4120, n)
    ht = HashDoubling()
    start_time = time.time()
    for key in keys:
        ht.insert(key)
    print("Total time for insertion:", time.time() - start_time)
    search_keys = np.random.randint(0, 4120, n)
    start_time = time.time()
    for key in search_keys:
        ht.search(key)
    print("Total time for search:", time.time() - start_time)
