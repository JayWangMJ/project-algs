# A simple hash table with chaining

import numpy as np
import time

class HashTable():
    def __init__(self, size, hash_function = None):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.hash_function = hash_function
        if hash_function is None:
            self.hash_function = self._hash_function

    def _hash_function(self, key):
        return hash(key) % self.size
    
    def insert(self, key):
        self.table[self.hash_function(key)].append(key)

    def search(self, key):
        bucket = self.table[self.hash_function(key)]
        for k in bucket:
            if k == key:
                return k
        return None
    
    def average_size(self):
        return np.average([len(bucket) for bucket in self.table])
    
    def largest_size(self):
        return np.max([len(bucket) for bucket in self.table])
    
if __name__ == "__main__":
    n = 10000
    m = 1000
    keys = np.random.randint(0, 4120, n)
    ht = HashTable(m)
    start_time = time.time()
    for key in keys:
        ht.insert(key)
    print("Total time for insertion:", time.time() - start_time)
    search_keys = np.random.randint(0, 4120, n)
    start_time = time.time()
    for key in search_keys:
        ht.search(key)
    print("Total time for search:", time.time() - start_time)
    print("Largest bucket size:", ht.largest_size())
    print("Average size:", ht.average_size())
