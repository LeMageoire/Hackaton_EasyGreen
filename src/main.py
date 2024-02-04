from numba import jit
import os
from numba.typed import List
import random
from test import *

def main():
    data_size = 50000
    data = List([random.randint(-1000, 1000) for _ in range(data_size)])
    quicksort(data,0, len(data) - 1)
    print(100*"\n")
    print("Thank you for all the fishs")
    exit(0)

if __name__ == '__main__':
    main()
