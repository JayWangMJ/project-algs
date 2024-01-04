import random

class PerfectHashing:
    def __init__(self, keys):
        self.keys = keys
        self.first_level_table = [None for _ in range(len(keys))]
        self.second_level_tables = [[] for _ in range(len(keys))]
        self.second_hash_functions = [hash for _ in range(len(keys))]
        self.hash_functions = [hash, lambda x:hash(hash(x)**3), lambda x: hash(str(hash(x)%1517*2317))]

        self.build_perfect_hash()

    def first_level_hash_function(self, key):
        return hash(key) % len(self.keys)

    def second_level_hash_function(self, func, key, second_level_size):
        return func(key) % second_level_size

    def build_perfect_hash(self):
        # Build the first-level hash table
        for key in self.keys:
            index = self.first_level_hash_function(key)
            if self.first_level_table[index] is None:
                self.first_level_table[index] = [key]
            else:
                self.first_level_table[index].append(key)

        # Build second-level hash tables for non-empty buckets
        for i in range(len(self.first_level_table)):
            bucket = self.first_level_table[i]
            if bucket:
                second_level_size = len(bucket)**2  # Adjust the second-level size as needed

                success = False
                times = 0
                while not success:
                    if times == len(self.hash_functions):
                        print(f"WARNING! Collision not resolved after {len(self.hash_functions)} trials at {i}-th bucket:", bucket)
                        break
                    self.second_hash_functions[i] = self.hash_functions[times]
                    success = True
                    second_level_table = [None for _ in range(second_level_size)]
                    for key in bucket:
                        second_level_index = self.second_level_hash_function(self.second_hash_functions[i], key, second_level_size)
                        if second_level_table[second_level_index] is None:
                            second_level_table[second_level_index] = key
                        else:
                            success = False
                            times += 1
                            break
                    self.second_level_tables[i] = second_level_table

    def get_hashed_index(self, key):
        # Retrieve the hashed index for a key
        first_level_index = self.first_level_hash_function(key)
        second_level_index = self.second_level_hash_function(self.second_hash_functions[first_level_index], key, len(self.first_level_table[first_level_index])**2)
        return first_level_index, second_level_index


def test():
    keys = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]
    # keys = [1, 2, 5, 6]
    my_perfect_hash = PerfectHashing(keys)
    print("First level table: ", my_perfect_hash.first_level_table)
    print()
    print("Second level table: ", my_perfect_hash.second_level_tables)
    print()
    for key in keys:
        first_level_index, second_level_index = my_perfect_hash.get_hashed_index(key)
        print(f"Key: {key}, Hashed Indices: ({first_level_index}, {second_level_index})")

if __name__=="__main__":
    test()
