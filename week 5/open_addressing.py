import numpy as np
import time

# basic hash table with table doubling and linear probing
class HashDoubling():
    def __init__(self, threshold = 0.75, hash_function = None, init_size = 2):
        self.size = init_size
        self.n = 0
        self.table = np.empty(init_size, dtype=object)
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
    
    def display_table(self):
        print(self.table)
    
class LinearProbing(HashDoubling):
    def __init__(self, threshold = 0.75, hash_function = None, init_size = 2):
        super().__init__(threshold, hash_function, init_size)

class QuadraticProbing(HashDoubling):
    def __init__(self, c_1, c_2, threshold = 0.75, hash_function = None, init_size = 2):
        self.c_1 = c_1
        self.c_2 = c_2
        super().__init__(threshold, hash_function, init_size)

    def hash_function(self, key, i):
        return (self._hash_function(key) + self.c_1 * i + self.c_2 * (i**2)) % self.size
    
class DoubleHashing(HashDoubling):
    def __init__(self, threshold=0.75, hash_function=None, hash_function_2=None, init_size=2):
        self._hash_function_2 = hash_function_2
        if self._hash_function_2 is None:
            self._hash_function_2 = hash
        super().__init__(threshold, hash_function, init_size)

    def hash_function(self, key, i):
        return (self._hash_function(key) + i * self._hash_function_2(key)) % self.size
    
if __name__ == "__main__":
    print("Linear probing...")
    keys = [28, 47, 20, 36, 43, 23, 25, 54]
    linear_probing = LinearProbing(threshold=1, hash_function=lambda x:x%11, init_size=11)
    for key in keys:
        linear_probing.insert(key)
    linear_probing.display_table()

    print("Quadratic probing...")
    keys = [76, 40, 48, 5, 55]
    quadratic_probing = QuadraticProbing(c_1=0, c_2=1, threshold=1, hash_function=lambda x:x%7, init_size=7)
    for key in keys:
        quadratic_probing.insert(key)
    quadratic_probing.display_table()

    print("Double hashing...")
    keys = [79, 69, 72, 98, 50, 14]
    double_hashing = DoubleHashing(threshold=1, hash_function=lambda x:x%13, hash_function_2=lambda x: 1 + x % 11, init_size=13)
    for key in keys:
        double_hashing.insert(key)
    double_hashing.display_table()