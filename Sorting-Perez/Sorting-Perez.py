import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import time
import random
import threading

def bubble_sort_descending(arr):
    """Sorts an array in descending order using bubble sort."""
    start_time = time.time()
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] < arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    end_time = time.time()
    return arr, end_time - start_time

def selection_sort_descending(arr):
    """Sorts an array in descending order using selection sort."""
    start_time = time.time()
    n = len(arr)
    for i in range(n):
        max_idx = i
        for j in range(i + 1, n):
            if arr[j] > arr[max_idx]:
                max_idx = j
        arr[i], arr[max_idx] = arr[max_idx], arr[i]
    end_time = time.time()
    return arr, end_time - start_time

def insertion_sort_descending(arr):
    """Sorts an array in descending order using insertion sort."""
    start_time = time.time()
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] < key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    end_time = time.time()
    return arr, end_time - start_time

def merge_sort_descending(arr):
    """Sorts an array in descending order using merge sort."""
    start_time = time.time()

    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] >= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def merge_sort(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
        return merge(left, right)

    sorted_arr = merge_sort(arr)
    end_time = time.time()
    return sorted_arr, end_time - start_time

def quicksort_descending(arr):
    """Sorts an array in descending order using iterative quicksort."""
    start_time = time.time()

    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] >= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def quicksort(arr, low, high):
        stack = []
        stack.append((low, high))
        while stack:
            low, high = stack.pop()
            if low < high:
                pi = partition(arr, low, high)
                stack.append((low, pi - 1))
                stack.append((pi + 1, high))

    quicksort(arr, 0, len(arr) - 1)
    end_time = time.time()
    return arr, end_time - start_time

def random_quicksort_descending(arr):
    """Sorts an array in descending order using randomized quicksort."""
    start_time = time.time()

    def partition(arr, low, high):
        rand_pivot = random.randint(low, high)
        arr[rand_pivot], arr[high] = arr[high], arr[rand_pivot]
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] >= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def quicksort(arr, low, high):
        stack = []
        stack.append((low, high))
        while stack:
            low, high = stack.pop()
            if low < high:
                pi = partition(arr, low, high)
                stack.append((low, pi - 1))
                stack.append((pi + 1, high))

    quicksort(arr, 0, len(arr) - 1)
    end_time = time.time()
    return arr, end_time - start_time

def counting_sort_descending(arr):
    """Sorts an array in descending order using counting sort."""
    start_time = time.time()
    if not arr:
        return arr, 0.0

    max_val = max(arr)
    min_val = min(arr)
    range_of_elements = max_val - min_val + 1

    count = [0] * range_of_elements
    output = [0] * len(arr)

    for num in arr:
        count[num - min_val] += 1

    for i in range(1, len(count)):
        count[i] += count[i - 1]

    for num in arr:
        output[count[num - min_val] - 1] = num
        count[num - min_val] -= 1

    output.reverse()
    end_time = time.time()
    return output, end_time - start_time

def read_dataset(filename):
    """Reads a dataset from a text file."""
    with open(filename, 'r') as file:
        data = [int(line.strip()) for line in file if line.strip()]
    return data

class SortingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Sorting Algorithm Comparator")
        self.root.geometry("950x750")
        self.root.minsize(800, 600)
        self.root.maxsize(1600, 1200)
        self.dataset = []
        self.sorting = False

        # Calculate responsive font sizes
        screen_width = self.root.winfo_screenwidth()
        self.title_font_size = 18 if screen_width >= 1920 else 16 if screen_width >= 1366 else 14
        self.subtitle_font_size = 9 if screen_width >= 1920 else 8 if screen_width >= 1366 else 7
        self.label_font_size = 11 if screen_width >= 1920 else 10 if screen_width >= 1366 else 9
        self.body_font_size = 10 if screen_width >= 1920 else 9 if screen_width >= 1366 else 8

        # Set modern theme with enhanced styling
        style = ttk.Style()
        style.theme_use('clam')

        # Configure modern colors and styling
        style.configure('TFrame', background='#f8f9fa')
        style.configure('TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=8,
                       relief='flat',
                       borderwidth=0)
        style.map('TButton',
                 background=[('active', '#007bff'),
                           ('pressed', '#0056b3')])
        style.configure('TLabel',
                       background='#f8f9fa',
                       font=('Segoe UI', 10))
        style.configure('TCombobox',
                       font=('Segoe UI', 10),
                       padding=5)
        style.configure('Horizontal.TProgressbar',
                       background='#28a745',
                       troughcolor='#e9ecef',
                       borderwidth=0,
                       lightcolor='#28a745',
                       darkcolor='#28a745')

        # Main frame with responsive design
        main_frame = ttk.Frame(root, padding="20", style='TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Configure main frame for responsiveness
        main_frame.columnconfigure(0, weight=1)
        for i in range(6):  # Configure all rows
            main_frame.rowconfigure(i, weight=1 if i in [4] else 0)  # Results section expands

        # Enhanced title with responsive font
        title_label = ttk.Label(main_frame, text="🔄 Advanced Sorting Algorithm Comparator",
                               font=('Segoe UI', self.title_font_size, 'bold'), foreground='#2c3e50')
        title_label.grid(row=0, column=0, pady=(0, 25), sticky=tk.W)

        # Subtitle with responsive font
        subtitle_label = ttk.Label(main_frame, text="Compare performance of multiple sorting algorithms with real-time visualization",
                                  font=('Segoe UI', self.subtitle_font_size), foreground='#6c757d')
        subtitle_label.grid(row=1, column=0, pady=(0, 20), sticky=tk.W)

        # Control frame with responsive organization
        control_frame = ttk.Frame(main_frame, style='TFrame', relief='solid', borderwidth=1)
        control_frame.grid(row=2, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        control_frame.columnconfigure(0, weight=1)
        control_frame.columnconfigure(1, weight=1)
        control_frame.columnconfigure(2, weight=1)
        control_frame.configure(padding="15")

        # Responsive control layout - stack on smaller screens
        screen_width = self.root.winfo_screenwidth()
        if screen_width < 1200:  # Smaller screens - vertical layout
            # Load dataset section
            load_frame = ttk.Frame(control_frame, style='TFrame')
            load_frame.grid(row=0, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
            load_frame.columnconfigure(0, weight=1)
            ttk.Label(load_frame, text="📁 Dataset", font=('Segoe UI', self.label_font_size, 'bold')).grid(row=0, column=0, sticky=tk.W)
            self.load_button = ttk.Button(load_frame, text="Load Dataset",
                                         command=self.load_dataset)
            self.load_button.grid(row=1, column=0, pady=(5, 0), sticky=(tk.W, tk.E))

            # Algorithm selection section
            algo_frame = ttk.Frame(control_frame, style='TFrame')
            algo_frame.grid(row=1, column=0, pady=(10, 10), sticky=(tk.W, tk.E))
            algo_frame.columnconfigure(0, weight=1)
            ttk.Label(algo_frame, text="🎯 Algorithm", font=('Segoe UI', self.label_font_size, 'bold')).grid(row=0, column=0, sticky=tk.W)
            self.algorithm_var = tk.StringVar()
            self.algorithm_combo = ttk.Combobox(algo_frame, textvariable=self.algorithm_var,
                                               state='readonly', width=25)
            self.algorithm_combo['values'] = ('Bubble Sort', 'Selection Sort', 'Insertion Sort',
                                            'Merge Sort', 'Quicksort', 'Random Quicksort', 'Counting Sort')
            self.algorithm_combo.current(0)
            self.algorithm_combo.grid(row=1, column=0, pady=(5, 0), sticky=(tk.W, tk.E))

            # Sort button section
            sort_frame = ttk.Frame(control_frame, style='TFrame')
            sort_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
            sort_frame.columnconfigure(0, weight=1)
            ttk.Label(sort_frame, text="▶️ Action", font=('Segoe UI', 11, 'bold')).grid(row=0, column=0, sticky=tk.W)
            self.sort_button = ttk.Button(sort_frame, text="Run Sort",
                                         command=self.sort_dataset, state=tk.DISABLED)
            self.sort_button.grid(row=1, column=0, pady=(5, 0), sticky=(tk.W, tk.E))
        else:  # Larger screens - horizontal layout
            # Load dataset section
            load_frame = ttk.Frame(control_frame, style='TFrame')
            load_frame.grid(row=0, column=0, padx=(0, 20), sticky=tk.W)
            ttk.Label(load_frame, text="📁 Dataset", font=('Segoe UI', self.label_font_size, 'bold')).grid(row=0, column=0, sticky=tk.W)
            self.load_button = ttk.Button(load_frame, text="Load Dataset",
                                         command=self.load_dataset)
            self.load_button.grid(row=1, column=0, pady=(5, 0), sticky=tk.W)

            # Algorithm selection section
            algo_frame = ttk.Frame(control_frame, style='TFrame')
            algo_frame.grid(row=0, column=1, padx=(0, 20), sticky=tk.W)
            ttk.Label(algo_frame, text="🎯 Algorithm", font=('Segoe UI', self.label_font_size, 'bold')).grid(row=0, column=0, sticky=tk.W)
            self.algorithm_var = tk.StringVar()
            self.algorithm_combo = ttk.Combobox(algo_frame, textvariable=self.algorithm_var,
                                               state='readonly', width=22)
            self.algorithm_combo['values'] = ('Bubble Sort', 'Selection Sort', 'Insertion Sort',
                                            'Merge Sort', 'Quicksort', 'Random Quicksort', 'Counting Sort')
            self.algorithm_combo.current(0)
            self.algorithm_combo.grid(row=1, column=0, pady=(5, 0), sticky=tk.W)

            # Sort button section
            sort_frame = ttk.Frame(control_frame, style='TFrame')
            sort_frame.grid(row=0, column=2, sticky=tk.W)
            ttk.Label(sort_frame, text="▶️ Action", font=('Segoe UI', self.label_font_size, 'bold')).grid(row=0, column=0, sticky=tk.W)
            self.sort_button = ttk.Button(sort_frame, text="Run Sort",
                                         command=self.sort_dataset, state=tk.DISABLED)
            self.sort_button.grid(row=1, column=0, pady=(5, 0), sticky=tk.W)

        # Progress frame with better styling
        progress_frame = ttk.Frame(main_frame, style='TFrame', relief='solid', borderwidth=1)
        progress_frame.grid(row=3, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        progress_frame.columnconfigure(0, weight=1)
        progress_frame.configure(padding="15")

        ttk.Label(progress_frame, text="📊 Progress", font=('Segoe UI', self.label_font_size, 'bold')).grid(row=0, column=0, sticky=tk.W)
        self.progress_label = ttk.Label(progress_frame, text="Ready to sort", font=('Segoe UI', self.body_font_size, 'italic'), foreground='#6c757d')
        self.progress_label.grid(row=1, column=0, pady=(5, 10), sticky=(tk.W, tk.E))

        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate', style='Horizontal.TProgressbar')
        self.progress_bar.grid(row=2, column=0, sticky=(tk.W, tk.E))

        # Results frame with enhanced responsive styling
        results_frame = ttk.Frame(main_frame, style='TFrame', relief='solid', borderwidth=1)
        results_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(4, weight=1)
        results_frame.configure(padding="15")

        # Dataset info with responsive design
        ttk.Label(results_frame, text="📈 Results", font=('Segoe UI', self.label_font_size, 'bold')).grid(row=0, column=0, sticky=tk.W)
        self.dataset_label = ttk.Label(results_frame, text="No dataset loaded",
                                      font=('Segoe UI', self.body_font_size, 'bold'), foreground='#007bff')
        self.dataset_label.grid(row=1, column=0, pady=(5, 10), sticky=(tk.W, tk.E))

        # Results text area with responsive height
        screen_height = self.root.winfo_screenheight()
        text_height = max(15, min(30, int(screen_height / 40)))  # Responsive height based on screen

        self.result_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD,
                                                   font=("Consolas", 9), height=text_height,
                                                   relief='flat', borderwidth=1)
        self.result_text.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Statistics frame with enhanced styling
        stats_frame = ttk.Frame(main_frame, style='TFrame', relief='solid', borderwidth=1)
        stats_frame.grid(row=5, column=0, pady=(20, 0), sticky=(tk.W, tk.E))
        stats_frame.configure(padding="15")

        ttk.Label(stats_frame, text="📊 Statistics", font=('Segoe UI', self.label_font_size, 'bold')).grid(row=0, column=0, sticky=tk.W)

        self.time_label = ttk.Label(stats_frame, text="", font=('Segoe UI', self.body_font_size + 2, 'bold'),
                                   foreground='#28a745')
        self.time_label.grid(row=1, column=0, pady=(10, 5), sticky=tk.W)

        self.stats_label = ttk.Label(stats_frame, text="", font=('Segoe UI', self.body_font_size),
                                    foreground='#6c757d')
        self.stats_label.grid(row=2, column=0, sticky=tk.W)

        # Bind resize event for dynamic responsiveness
        self.root.bind('<Configure>', self.on_window_resize)

        # Sorting functions dictionary
        self.sort_functions = {
            'Bubble Sort': bubble_sort_descending,
            'Selection Sort': selection_sort_descending,
            'Insertion Sort': insertion_sort_descending,
            'Merge Sort': merge_sort_descending,
            'Quicksort': quicksort_descending,
            'Random Quicksort': random_quicksort_descending,
            'Counting Sort': counting_sort_descending,
        }

    def on_window_resize(self, event):
        """Handle window resize events for dynamic responsiveness."""
        if event.widget == self.root and (event.width != self.root.winfo_width() or event.height != self.root.winfo_height()):
            # Update text area height based on new window size
            try:
                new_height = max(15, min(30, int(event.height / 40)))
                self.result_text.config(height=new_height)
            except:
                pass  # Ignore resize errors

    def load_dataset(self):
        filename = filedialog.askopenfilename(title="Select Dataset File",
                                            filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            try:
                self.dataset = read_dataset(filename)
                self.dataset_label.config(text=f"📊 Dataset loaded: {len(self.dataset):,} elements")
                self.sort_button.config(state=tk.NORMAL)
                self.result_text.delete(1.0, tk.END)
                self.time_label.config(text="")
                self.stats_label.config(text="")
                self.progress_label.config(text="")

                # Show the entire unsorted dataset
                formatted_data = str(self.dataset).replace('[', '').replace(']', '')
                self.result_text.insert(tk.END, f"📋 Unsorted dataset ({len(self.dataset)} elements):\n\n")
                self.result_text.insert(tk.END, formatted_data + "\n\n")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load dataset: {str(e)}")

    def sort_dataset(self):
        if not self.dataset:
            messagebox.showerror("Error", "No dataset loaded")
            return

        algorithm = self.algorithm_var.get()
        if not algorithm:
            messagebox.showerror("Error", "Please select an algorithm")
            return

        if self.sorting:
            return

        self.sorting = True
        self.sort_button.config(state=tk.DISABLED)
        self.load_button.config(state=tk.DISABLED)
        self.algorithm_combo.config(state=tk.DISABLED)
        self.progress_label.config(text=f"⚡ Processing with {algorithm}...")
        self.progress_bar.start()
        self.time_label.config(text="")
        self.stats_label.config(text="")

        # Run sorting in a separate thread
        threading.Thread(target=self._perform_sort, args=(algorithm,), daemon=True).start()

    def _perform_sort(self, algorithm):
        sort_func = self.sort_functions[algorithm]
        sorted_data, time_taken = sort_func(self.dataset.copy())

        # Update UI in main thread
        self.root.after(0, lambda: self._update_ui_after_sort(sorted_data, time_taken, algorithm))

    def _update_ui_after_sort(self, sorted_data, time_taken, algorithm):
        self.progress_bar.stop()
        self.progress_label.config(text="")
        self.sort_button.config(state=tk.NORMAL)
        self.load_button.config(state=tk.NORMAL)
        self.algorithm_combo.config(state='readonly')
        self.sorting = False

        # Update time label
        self.time_label.config(text=f"⏱️ {algorithm} completed in {time_taken:.6f} seconds")

        # Update stats
        self.stats_label.config(text=f"Algorithm: {algorithm} | Elements: {len(sorted_data):,}")

        # Update results text
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"🔽 Sorted in descending order using {algorithm}:\n\n")

        # Format the sorted data nicely - show all elements
        formatted_data = str(sorted_data).replace('[', '').replace(']', '')
        self.result_text.insert(tk.END, formatted_data)

if __name__ == "__main__":
    root = tk.Tk()
    gui = SortingGUI(root)
    root.mainloop()