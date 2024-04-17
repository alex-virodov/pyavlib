import numpy as np


def interleave(a, b):
    """Interleaves two one-dimensional arrays assuming the same length."""
    # https://stackoverflow.com/questions/5347065/interweaving-two-numpy-arrays
    c = np.empty((a.size + b.size,), dtype=a.dtype)
    c[0::2] = a
    c[1::2] = b
    return c

def printopts_no_column_limit():
    np.set_printoptions(linewidth=10_000)

def feq(a_str):
    # Replace '= ' with '=\n'
    return a_str.replace('=', '=\n', 1)

def list_of_tuples_to_tuple_of_lists(list_of_tuples):
    # https://stackoverflow.com/questions/7558908/unpacking-a-list-tuple-of-pairs-into-two-lists-tuples
    return tuple(zip(*list_of_tuples))


if __name__ == "__main__":
    a = np.array([1, 3, 5])
    b = np.array([2, 4, 6])
    print(interleave(a, b))

    list_of_tuples = [(1, 2), (3, 4), (5, 6), (7, 8)]
    print(f'{list_of_tuples=}')
    print(f'{list_of_tuples_to_tuple_of_lists(list_of_tuples)=}')