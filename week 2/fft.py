# Fast Fourier transform

import numpy as np

def fft(a):
    """
    Input: Coefficient representation of a polynomial A
    of degree <= n - 1, where n is a power of 2
    Output: Value representation of the polynomial
    """
    w_n = np.exp(2j * np.pi / len(a))
    return [np.round(i, 3) for i in recursive_fft(a, w_n)]

def ifft(y):
    """
    fft to calculate the reverse dft of value representation y
    """
    n = len(y)
    w_n = np.exp(-2j * np.pi / n)
    return [np.round(i/n, 3) for i in recursive_fft(y, w_n)]

def recursive_fft(a, w_n):
    """
    CLRS p.911
    A recursive implementation of FFT over an 1d array, 
    which is the coefficient representation of a polynomial 
    A of degree bound n, where n is a power of 2
    """
    n = len(a)
    if n == 1:
        return a
    w = 1
    a_even = a[::2]
    a_odd = a[1::2]
    y_even = recursive_fft(a_even, w_n**2)
    y_odd = recursive_fft(a_odd, w_n**2)
    for k in range(n//2):
        a[k] = y_even[k] + w * y_odd[k]
        a[k+n//2] = y_even[k] - w * y_odd[k]
        w *= w_n
    return a

def polynomial_multiply(a, b):
    """
    Input: Coefficient representations of two polynomial A and B,
    both are of degree <= n - 1, where n is a power of 2
    Output: Coefficient representation of A*B
    """
    print("Multiply polynomial A and B, where")
    print("A =", convert_str(a))
    print("B =", convert_str(b))
    n = len(a)
    c = []
    for _ in range(n):
        a.insert(0, 0)
        b.insert(0, 0)
    a_value = fft(a)
    b_value = fft(b)
    for i in range(2*n):
        c.append(a_value[i] * b_value[i])
    c = ifft(c)
    print("Result =", convert_str([np.round(i.real, 3) for i in c]))
    return c

def convert_str(a):
    """
    Input: coefficient representation of polynomial A
    Output: polynomal A
    e.g.: a = [1, 2, 3, 4], A = 1+2x+3x^2+4x^3
    """
    ret = ''
    power = 0
    for coef in a:
        if coef != 0:
            if coef > 0:
                sign = ' + ' if ret else ''
            else:
                sign = ' - ' if ret else '-'
            coef_str = '' if coef == 1 and power != 0 else str(coef)
            if power == 0:
                power_str = ''
            elif power == 1:
                power_str = 'x'
            else:
                power_str = 'x^' + str(power)
            ret += sign + coef_str + power_str
        power += 1
    return ret

if __name__ == "__main__":
    print(fft([1, 0, 1, -1]))
    print(fft([1, 0, 0, 0]))
    print(ifft([1, 1j, 3, -1j]))
    print(ifft([1, 1, 1, 1]))
    print(polynomial_multiply([1, 1, 1, 1], [1, 1, 1, 1]))
