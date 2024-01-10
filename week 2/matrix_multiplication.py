# Frievald's algorithm: given nxn binary matrices A, B, C, check that if AB=C or not.
# Input: nxn binary matrices A, B, C
# Ouput: True or Flase if AB=C

import numpy as np

def frievald(A, B, C):
    n = len(A)
    for _ in range(10):
        r = np.random.randint(0, 2, (n, 1))
        if np.any((A@(B@r)%2)%2 != (C@r)%2):
            return False
    return True


if __name__=="__main__":
    # generate random nxn binary matrices, all ops mod 2
    n = 4
    A = np.random.randint(0, 2, (n, n))
    B = np.random.randint(0, 2, (n, n))
    C = np.random.randint(0, 2, (n, n))
    # C = A@B%2
    print(f"Frievald-AB=C: {frievald(A, B, C)}")
    print(f"Direct Multiplication-AB=C: {np.all((A@B)%2==C)}")
