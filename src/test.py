
from numba import jit
from numba import jit
from numba import jit

@jit
@jit
@jit
def quicksort(arr, start, end):
    if (start < end):
        pivot_index = partition(arr, start, end)
        quicksort(arr, start, pivot_index)
        quicksort(arr, (pivot_index + 1), end)

@jit
@jit
@jit
def partition(arr, start, end):
    pivot = arr[start]
    low = (start + 1)
    high = end
    while True:
        while ((low <= high) and (arr[high] >= pivot)):
            high = (high - 1)
        while ((low <= high) and (arr[low] <= pivot)):
            low = (low + 1)
        if (low <= high):
            (arr[low], arr[high]) = (arr[high], arr[low])
        else:
            break
    (arr[start], arr[high]) = (arr[high], arr[start])
    return high
