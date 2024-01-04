import heapq
from collections import defaultdict

class Node:
    def __init__(self, char, frequency):
        self.char = char
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

# CLRS ch.16.3 p.431
# Input: frequencies dict of (char-freq) pairs
# Output: root the built Huffman tree
def build_huffman_tree(frequencies):
    queue = [Node(char, freq) for char, freq in frequencies.items()]
    n = len(queue)
    heapq.heapify(queue)

    for _ in range(n-1):
        left = heapq.heappop(queue)
        right = heapq.heappop(queue)

        merged = Node(None, left.frequency + right.frequency)
        merged.left = left
        merged.right = right

        heapq.heappush(queue, merged)

    return queue[0] # return the root of the tree

# Construct Huffman code of given node
# Encoded Huffman codes stored in codes
def build_huffman_codes(node, current_code, codes):
    if node is not None:
        if node.char is not None:
            codes[node.char] = current_code
        build_huffman_codes(node.left, current_code + '0', codes)
        build_huffman_codes(node.right, current_code + '1', codes)

# Encode data
def huffman_encoding(data):
    frequencies = defaultdict(int)
    for char in data:
        frequencies[char] += 1

    root = build_huffman_tree(frequencies)

    codes = {}
    build_huffman_codes(root, '', codes)

    encoded_data = ''.join(codes[char] for char in data)
    return encoded_data, root

# Decode code
def huffman_decoding(encoded_data, root):
    decoded_data = ''
    current_node = root

    for bit in encoded_data:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:
            decoded_data += current_node.char
            current_node = root

    return decoded_data

if __name__=="__main__":
    data = "hello world"
    encoded_data, huffman_tree = huffman_encoding(data)

    print("Original data:", data)
    print("Encoded data:", encoded_data)

    decoded_data = huffman_decoding(encoded_data, huffman_tree)
    print("Decoded data:", decoded_data)
