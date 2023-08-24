# A simple implementation of Cuckoo hashing

import numpy as np

class CuckooHashTable():
    def __init__(self, size, hash_function_1=None, hash_function_2=None):
        self.size = size
        self.table = np.empty(self.size, dtype=object)
        self.hash_function_1 = hash_function_1
        self.hash_function_2 = hash_function_2
        if self.hash_function_1 is None:
            self.hash_function_1 = self._hash_function_1
        if self.hash_function_2 is None:
            self.hash_function_2 = self._hash_function_2

    def _hash_function_1(self, key):
        return key % self.size
    
    def _hash_function_2(self, key):
        A = (np.sqrt(5)-1)/2
        return int(self.size * ((key * A) % 1))
    
    def insert(self, key):
        state, outside = self._insert(key, self.hash_function_1(key), self.hash_function_2(key), self.table, used=[])
        if not state:
            print("table doubling...")
            self._table_doubling()
            self.insert(outside)
        else:
            print("After inserting", key, "the table is\n", self.table)

    def _table_doubling(self):
        self.size *= 2
        while True:
            newtable = np.empty(self.size, dtype=object)
            for bucket in self.table:
                if bucket:
                    state, _ = self._insert(bucket, self.hash_function_1(bucket), self.hash_function_2(bucket), newtable, used=[])
                if not state:
                    print("FATAL")
                    exit()
                    # do anything here? lol
            break
        self.table = newtable

    def _insert(self, key, hash_1, hash_2, table, used):
        if key in used:
            return False, key
        
        # position 1 empty
        if table[hash_1] is None:
            table[hash_1] = key
            return True, key
        
        # position 2 empty
        if table[hash_2] is None:
            table[hash_2] = key
            return True, key
        
        # both positions are full
        bumped = table[hash_1]
        table[hash_1] = key
        used.append(key)
        # bump the element to its other location
        bumped_hash_1 = self.hash_function_1(bumped)
        bumped_hash_2 = self.hash_function_2(bumped)
        if hash_1 == bumped_hash_1:
            return self._insert(bumped, bumped_hash_2, bumped_hash_1, table, used)
        return self._insert(bumped, bumped_hash_1, bumped_hash_2, table, used)
    

    def lookup(self, key):
        return self.table[self.hash_function_1(key)] == key\
                or self.table[self.hash_function_2(key)] == key
    
if __name__ == "__main__":
    # lecture example
    # A(0, 3): 20, C(1, 2): 91, 
    # B(3, 8):  3, H(4, 7): 74,
    # P(5, 8): 45, W(7, 4): 67, 
    # X(0, 4): 80
    ht = CuckooHashTable(10)
    keys = [20, 91, 3, 74, 45, 67, 80]
    for key in keys:
        ht.insert(key)
    ht.insert(2)
    ht.insert(6)
    ht.insert(9)
    ht.insert(4)