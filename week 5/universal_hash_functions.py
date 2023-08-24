import numpy as np

class MatrixMethod():
    def __init__(self, u, b):
        self.u = u
        self.b = b
        self.h = np.random.randint(0, 2, (b, u))

    def hash_function(self, x):
        return np.dot(self.h, x)%2
    
class Product():
    def __init__(self, len_ = 4, b = 8, m = 257):
        self.len = len_
        self.b = b
        self.m = m
        self.a = np.random.randint(0, m, len_)

    def hash_function(self, x):
        return np.sum([self.a[i] * x[i] for i in range(self.len)]) % self.m

class LargePrime():
    def __init__(self, m, p = 7368787):
        self.m = m
        self.p = p
        self.a = np.random.randint(1, p)
        self.b = np.random.randint(0, p)

    def hash_function(self, k):
        return ((self.a * k + self.b) % self.p) % self.m


if __name__ == "__main__":
    matrix_method = MatrixMethod(u = 4, b = 3)
    print(matrix_method.hash_function(np.array([[1], [0], [1], [0]])))

    product = Product()
    print(product.hash_function([1, 2, 3, 4]))

    large_prime = LargePrime(m = 6, p = 17)
    print(large_prime.hash_function(8))