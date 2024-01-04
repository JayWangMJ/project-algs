import math
import hashlib

class BloomFilter:
    def __init__(self, n, counting=False):
        self.n = n
        self.counting = counting
        self.set_default_attr()
        self.bit_array = [0 for _ in range(self.m)]

    def set_default_attr(self):
        self.m = 8*self.n
        self.k = math.floor(self.m/self.n*math.log(2))
        self.max_counter = 16

    def _hash(self, element, seed):
        hash_obj = hashlib.sha256()
        hash_obj.update((str(element)+str(seed)).encode("utf-8"))
        return int(hash_obj.hexdigest(), 16) % self.m
    
    def insert(self, element):
        for i in range(self.k):
            idx = self._hash(element, i)
            if not self.counting:
                self.bit_array[idx] = 1
            else:
                self.bit_array[idx] += 1
                self.bit_array[idx] = min(self.bit_array[idx], self.max_counter)

    def delete(self, element):
        if not self.counting:
            print("ERROR! Standard Bloom Filter does not support deletion")
            return
        for i in range(self.k):
            idx = self._hash(element, i)
            self.bit_array[idx] -= 1
            self.bit_array[idx] = max(self.bit_array[idx], 0)
    
    def check_membership(self, element):
        for i in range(self.k):
            idx = self._hash(element, i)
            if self.bit_array[idx] == 0:
                return False
        return True
    
def test():
    my_bloom_filter = BloomFilter(24)
    elements = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]
    for ele in elements:
        my_bloom_filter.insert(ele)
    
    check = ["apple", "kiwi", "orange", "grape"]
    print("-------Start Checking-------")
    print("Set:", elements)
    print("----------------------------")
    for ele in check:
        if my_bloom_filter.check_membership(ele):
            print(f"{ele} might exist in the set")
        else:
            print(f"{ele} does NOT exist in the set")

if __name__ == "__main__":
    test()