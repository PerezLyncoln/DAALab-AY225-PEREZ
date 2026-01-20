import time

def bubble_sort_descending(arr):
    """
    Sorts an array in descending order using the bubble sort algorithm.

    Args:
        arr: List of comparable elements to sort

    Returns:
        Tuple of (sorted list, time taken in seconds)
    """
    start_time = time.time()
    n = len(arr)

    # Traverse through all array elements
    for i in range(n):
        # Flag to optimize by detecting if array is already sorted
        swapped = False

        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # Swap if the element found is less than the next element (for descending)
            if arr[j] < arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        # If no swaps occurred, array is sorted
        if not swapped:
            break

    end_time = time.time()
    time_taken = end_time - start_time

    return arr, time_taken

def read_dataset(filename):
    """
    Reads a dataset from a text file, one number per line.

    Args:
        filename: Path to the text file

    Returns:
        List of integers
    """
    with open(filename, 'r') as file:
        data = [int(line.strip()) for line in file if line.strip()]
    return data

if __name__ == "__main__":
    # Read dataset from file
    dataset = read_dataset('dataset.txt')
    print(f"Original dataset size: {len(dataset)}")
    print(f"Unsorted Elements: {dataset[:10000]}")

    # Sort in descending order
    sorted_dataset, time_taken = bubble_sort_descending(dataset)

    print("""
=======================================================

=======================================================  
    """)
    print(f"Sorted in descending order.")
    print(f"Sorted Elements: {sorted_dataset[:10000]}")
    print(f"Time taken: {time_taken:.6f} seconds")