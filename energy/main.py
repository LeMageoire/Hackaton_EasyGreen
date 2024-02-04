from numba import jit
from numba.typed import List
import ctypes
import random
from test import *

def main():
	data_size = 50000
	data = List([random.randint(-1000, 1000) for _ in range(data_size)])
	data_array = (ctypes.c_int * len(data))(*data)
	exit(0)

if __name__ == '__main__':
	main()