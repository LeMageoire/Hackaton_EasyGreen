import os
import psutil
import time
import random
from numba import jit
from numba.typed import List
import ctypes
import matplotlib.pyplot as plt

# Load the shared library
lib = ctypes.CDLL('./libquicksort.so')
# Define the argument and return types of the C sort function
lib.sort.argtypes = (ctypes.POINTER(ctypes.c_int), ctypes.c_int)
lib.sort.restype = None
# JIT-compiled partition_comp function for quicksort_comp
@jit(nopython=True)
def partition_comp(arr, start, end):
    pivot = arr[start]
    low = start + 1
    high = end

    while True:
        while low <= high and arr[high] >= pivot:
            high = high - 1
        while low <= high and arr[low] <= pivot:
            low = low + 1
        if low <= high:
            arr[low], arr[high] = arr[high], arr[low]
        else:
            break

    arr[start], arr[high] = arr[high], arr[start]
    return high

# JIT-compiled quicksort_comp function
@jit(nopython=True)
def quicksort_comp(arr, start, end):
    if start < end:
        pivot_index = partition_comp(arr, start, end)
        quicksort_comp(arr, start, pivot_index)
        quicksort_comp(arr, pivot_index + 1, end)

# Standard Python implementation of quicksort
def quicksort(arr, start, end):
    if start < end:
        pivot_index = partition(arr, start, end)
        quicksort(arr, start, pivot_index)
        quicksort(arr, pivot_index + 1, end)

def partition(arr, start, end):
    pivot = arr[start]
    low = start + 1
    high = end

    while True:
        while low <= high and arr[high] >= pivot:
            high = high - 1
        while low <= high and arr[low] <= pivot:
            low = low + 1
        if low <= high:
            arr[low], arr[high] = arr[high], arr[low]
        else:
            break

    arr[start], arr[high] = arr[high], arr[start]
    return high
def quicksort_c(arr, start, end):
    data_array = (ctypes.c_int * len(arr))(*arr)
    # Call the C sort function
    lib.sort(data_array, len(data_array))

# Function to measure execution time
def measure_execution_time(func, data):
    start = time.time()
    func(data, 0, len(data) - 1)
    end = time.time()
    return end - start

# Main function to compare sorting algorithms
def compare_sorts(data_size):
    data = List([random.randint(-1000, 1000) for _ in range(data_size)])
    
    # Quicksort_comp
    qsc_time = measure_execution_time(quicksort_comp, data.copy())

    # Quicksort
    #qs_time = measure_execution_time(quicksort, data.copy())
    qs_time = 0
    # Quicksort_c
    qscc_time = measure_execution_time(quicksort_c, data.copy())


    # Print results
    print(f"Quicksort_comp - Time: {qsc_time:.4f} seconds")
    print(f"Quicksort - Time: {qs_time:.4f} seconds")
    print(f"Quicksort C - Time: {qscc_time:.4f} seconds")
    return qs_time, qsc_time, qscc_time

# First run to compile
compare_sorts(1)
print("\n\n\n")

xx = []
y_no_compil = []
y_jit = []
y_c = []
for x in range(10, 1000000, 5000):
    xx.append(x)
    no_compil, jit, c = compare_sorts(x)  # For example, if x represents thousands
    y_no_compil.append(no_compil)
    y_jit.append(jit)
    y_c.append(c)
# Create the plot
plt.figure(figsize=(10, 6))

plt.plot(xx, y_no_compil, label='No Compilation', marker='o')
plt.plot(xx, y_jit, label='JIT Compilation', marker='x')
plt.plot(xx, y_c, label='C Implementation', marker='^')

# Adding titles and labels
plt.title('Comparison of Sorting Algorithms')
plt.xlabel('Data Size')
plt.ylabel('Execution Time (seconds)')
plt.yscale('log')  # Set the x-axis to logarithmic scale

plt.legend()

# Show the plot
plt.show()