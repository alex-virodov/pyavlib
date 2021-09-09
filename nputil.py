import numpy as np

def interleave(a, b):
    """Interleaves two one-dimensional arrays assuming the same length."""
    # https://stackoverflow.com/questions/5347065/interweaving-two-numpy-arrays
    c = np.empty((a.size + b.size,), dtype=a.dtype)
    c[0::2] = a
    c[1::2] = b
    return c

if __name__ == "__main__":
    a = np.array([1, 3, 5])
    b = np.array([2, 4, 6])
    print(interleave(a, b))