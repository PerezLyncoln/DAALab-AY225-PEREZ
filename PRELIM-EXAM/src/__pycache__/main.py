import csv
import os
import threading
import time
import queue
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# ---------------------- Sorting algorithms (from scratch) ----------------------

def bubble_sort(arr, key_func=lambda x: x, progress_callback=None):
    n = len(arr)
    # Work on a copy to avoid in-place surprises
    a = list(arr)
    if n <= 1:
        return a
    callback_freq = max(1, n // 100)  # Update progress ~100 times max to avoid overhead
    for i in range(n - 1):
        swapped = False
        # inner loop
        for j in range(n - 1 - i):
            if key_func(a[j]) > key_func(a[j + 1]):
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if progress_callback and i % callback_freq == 0:
            progress_callback((i + 1) / (n - 1))
        if not swapped:
            break
    if progress_callback:
        progress_callback(1.0)
    return a


def insertion_sort(arr, key_func=lambda x: x, progress_callback=None):
    a = list(arr)
    n = len(a)
    callback_freq = max(1, n // 100)  # Update progress ~100 times max to avoid overhead
    for i in range(1, n):
        key_item = a[i]
        key_val = key_func(key_item)
        j = i - 1
        while j >= 0 and key_func(a[j]) > key_val:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key_item
        if progress_callback and i % callback_freq == 0:
            progress_callback(i / max(1, n - 1))
    if progress_callback:
        progress_callback(1.0)
    return a


def merge_sort(arr, key_func=lambda x: x, progress_callback=None):
    """
    FIXED: Pre-compute keys to avoid redundant key_func calls during comparisons.
    This dramatically improves performance for large datasets.
    """
    a = list(arr)
    n = len(a)
    if n <= 1:
        if progress_callback:
            progress_callback(1.0)
        return a

    # Pre-compute all keys once - this is the critical optimization!
    # Instead of calling key_func thousands of times, we call it exactly once per element
    keyed_items = [(key_func(item), item) for item in a]
    
    # Track merges for progress updates
    merge_count = [0]
    total_merges_estimate = n.bit_length() * n  # rough estimate

    def merge(left, right):
        """Merge two sorted lists of (key, item) tuples"""
        i = j = 0
        out = []
        while i < len(left) and j < len(right):
            # Now we just compare the pre-computed keys!
            if left[i][0] <= right[j][0]:
                out.append(left[i])
                i += 1
            else:
                out.append(right[j])
                j += 1
        out.extend(left[i:])
        out.extend(right[j:])
        
        # Progress tracking
        merge_count[0] += 1
        if progress_callback and merge_count[0] % max(1, n // 100) == 0:
            progress_callback(min(0.95, merge_count[0] / max(1, total_merges_estimate)))
        return out

    def _merge_sort(lst):
        if len(lst) <= 1:
            return lst
        mid = len(lst) // 2
        left = _merge_sort(lst[:mid])
        right = _merge_sort(lst[mid:])
        return merge(left, right)

    # Sort using keyed items
    sorted_keyed = _merge_sort(keyed_items)
    
    # Extract just the items (without keys)
    res = [item for key, item in sorted_keyed]
    
    if progress_callback:
        progress_callback(1.0)
    return res


# ---------------------- CSV loading and helpers ----------------------

def find_csv_file():
    # Prefer data/generated_data.csv, else look for generated_data.csv in cwd
    cwd = os.path.abspath(os.getcwd())
    candidates = [
        os.path.join(cwd, "data", "generated_data.csv"),
        os.path.join(cwd, "generated_data.csv"),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


def load_csv(path, n_rows=None, progress_callback=None):
    rows = []
    start = time.perf_counter()
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if n_rows is None:
            for i, r in enumerate(reader):
                rows.append(r)
                if progress_callback and i % 1000 == 0:
                    progress_callback(None)  # indeterminate progress
        else:
            for i, r in enumerate(reader):
                if i >= n_rows:
                    break
                rows.append(r)
                if progress_callback and i % 1000 == 0:
                    progress_callback(None)  # indeterminate progress
    load_time = time.perf_counter() - start
    return rows, load_time


# ---------------------- GUI Application ----------------------

class SortBenchmarkApp:
    def __init__(self, root):
        self.root = root
        root.title("Sorting Benchmark Tool")
        root.geometry("900x600")
        
        # Set a modern theme if available
        try:
            root.tk.call('source', 'azure.tcl')
            root.tk.call('set_theme', 'dark')
        except:
            # Apply custom styling
            self._setup_custom_theme()
        
        # Configure root window
        root.configure(bg='#1a1a1f')
        
        # Configure ttk styles
        self.style = ttk.Style()
        self.style.theme_use('clam')  # More modern theme
        
        # Configure colors
        self.bg_color = '#1a1a1f'
        self.fg_color = '#e8e8ec'
        self.accent_color = '#5eead4'
        self.secondary_bg = '#22222a'
        self.highlight_color = '#5eead4'
        
        self._configure_styles()
        
        mainframe = ttk.Frame(root, padding="12 12 12 12")
        mainframe.pack(fill=tk.BOTH, expand=True)
        
        # Controls
        controls = ttk.LabelFrame(mainframe, text="⚙️  Controls", padding="12 8 12 8")
        controls.pack(fill=tk.X, padx=6, pady=(0, 6))
        
        # Algorithm selection
        alg_frame = ttk.Frame(controls)
        alg_frame.grid(column=0, row=0, sticky=tk.W, padx=(0, 16), pady=4)
        ttk.Label(alg_frame, text="Algorithm:", font=('Poppins', 9, 'bold')).pack(anchor=tk.W)
        self.alg_var = tk.StringVar(value="Merge Sort")
        alg_combo = ttk.Combobox(alg_frame, textvariable=self.alg_var, state="readonly",
                                  values=["Bubble Sort", "Insertion Sort", "Merge Sort"], 
                                  width=18, font=('Poppins', 9))
        alg_combo.pack(pady=(4, 0))
        
        # Column selection
        col_frame = ttk.Frame(controls)
        col_frame.grid(column=1, row=0, sticky=tk.W, padx=(0, 16), pady=4)
        ttk.Label(col_frame, text="Column:", font=('Poppins', 9, 'bold')).pack(anchor=tk.W)
        self.col_var = tk.StringVar(value="ID")
        col_combo = ttk.Combobox(col_frame, textvariable=self.col_var, state="readonly",
                                 values=["ID", "FirstName", "LastName"], 
                                 width=18, font=('Poppins', 9))
        col_combo.pack(pady=(4, 0))
        
        # Rows input
        rows_frame = ttk.Frame(controls)
        rows_frame.grid(column=2, row=0, sticky=tk.W, padx=(0, 16), pady=4)
        ttk.Label(rows_frame, text="Rows (N):", font=('Poppins', 9, 'bold')).pack(anchor=tk.W)
        self.n_var = tk.StringVar(value="10000")
        n_entry = ttk.Entry(rows_frame, textvariable=self.n_var, width=12, font=('Poppins', 9))
        n_entry.pack(pady=(4, 0))
        
        # Run button
        run_frame = ttk.Frame(controls)
        run_frame.grid(column=3, row=0, sticky=tk.W, padx=(0, 16), pady=4)
        ttk.Label(run_frame, text=" ", font=('Poppins', 9)).pack(anchor=tk.W)  # Spacer
        self.run_btn = ttk.Button(run_frame, text="▶ Run Benchmark", 
                                  command=self.on_run, style="Accent.TButton")
        self.run_btn.pack(pady=(4, 0))
        
        # CSV selection
        csv_frame = ttk.Frame(controls)
        csv_frame.grid(column=4, row=0, sticky=tk.W, pady=4)
        ttk.Label(csv_frame, text="CSV File:", font=('Poppins', 9, 'bold')).pack(anchor=tk.W)
        csv_btn_frame = ttk.Frame(csv_frame)
        csv_btn_frame.pack(fill=tk.X, pady=(4, 0))
        
        self.csv_path = None
        self.csv_path_var = tk.StringVar(value="No file selected")
        self.select_btn = ttk.Button(csv_btn_frame, text="📂 Select CSV...", 
                                     command=self.on_select_csv, width=15)
        self.select_btn.pack(side=tk.LEFT)
        
        # Path display
        self.path_label = ttk.Label(csv_btn_frame, textvariable=self.csv_path_var, 
                                   font=('Poppins', 8), foreground='#8a8a96')
        self.path_label.pack(side=tk.LEFT, padx=(8, 0))
        
        # Status area
        status_frame = ttk.Frame(mainframe, padding="8 8 8 8")
        status_frame.pack(fill=tk.X, padx=6, pady=6)
        
        # Status label with icon
        status_header = ttk.Frame(status_frame)
        status_header.pack(fill=tk.X, pady=(0, 8))
        
        ttk.Label(status_header, text="📊 Status:", 
                 font=('Poppins', 10, 'bold')).pack(side=tk.LEFT)
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(status_header, textvariable=self.status_var, 
                                     font=('Poppins', 10), foreground=self.highlight_color)
        self.status_label.pack(side=tk.LEFT, padx=(8, 0))
        
        # Progress bar
        progress_frame = ttk.Frame(status_frame)
        progress_frame.pack(fill=tk.X)
        
        self.progress = ttk.Progressbar(progress_frame, length=400, mode='determinate',
                                       style="Horizontal.TProgressbar")
        self.progress.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        # Progress percentage label
        self.progress_var = tk.StringVar(value="0%")
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_var,
                                       font=('Poppins', 9), foreground='#8a8a96')
        self.progress_label.pack(side=tk.RIGHT, padx=(0, 8))
        
        # Timings display
        timing_frame = ttk.LabelFrame(mainframe, text="⏱️  Performance Metrics", 
                                     padding="12 8 12 8")
        timing_frame.pack(fill=tk.X, padx=6, pady=6)
        
        # Create timing labels with better styling
        timing_grid = ttk.Frame(timing_frame)
        timing_grid.pack(fill=tk.X)
        
        self.load_time_var = tk.StringVar(value="Load: -")
        self.sort_time_var = tk.StringVar(value="Sort: -")
        self.total_time_var = tk.StringVar(value="Total: -")
        
        ttk.Label(timing_grid, textvariable=self.load_time_var, 
                 font=('Poppins', 10), padding="8 4 8 4").pack(side=tk.LEFT, padx=(0, 16))
        ttk.Label(timing_grid, textvariable=self.sort_time_var, 
                 font=('Poppins', 10), padding="8 4 8 4").pack(side=tk.LEFT, padx=(0, 16))
        ttk.Label(timing_grid, textvariable=self.total_time_var, 
                 font=('Poppins', 10, 'bold'), padding="8 4 8 4").pack(side=tk.LEFT)
        
        # Results area
        results_frame = ttk.LabelFrame(mainframe, text="📋 Results (First 10 sorted records)", 
                                      padding="8 8 8 8")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        
        # Treeview with scrollbar
        tree_frame = ttk.Frame(results_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        cols = ("ID", "FirstName", "LastName")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show='headings', height=12)
        
        # Configure columns
        col_widths = {"ID": 100, "FirstName": 200, "LastName": 200}
        for c in cols:
            self.tree.heading(c, text=c, anchor=tk.W)
            self.tree.column(c, width=col_widths[c], minwidth=80, anchor=tk.W)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Initialize timing variables
        self.load_time = 0
        self.sort_time = 0
        
        # Internal
        self.msg_queue = queue.Queue()
        self.worker_thread = None
        self.root.after(100, self._poll_queue)
    
    def _setup_custom_theme(self):
        """Set up custom theme colors and styles"""
        self.root.configure(bg='#1a1a1f')
        
    def _configure_styles(self):
        """Configure ttk styles for a modern look"""
        # Configure main styles
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.fg_color)
        self.style.configure('TLabelframe', background=self.bg_color, 
                           foreground=self.fg_color, borderwidth=1, bordercolor='#3a3a46', relief='solid')
        self.style.configure('TLabelframe.Label', background=self.bg_color, 
                           foreground=self.highlight_color, font=('Poppins', 10, 'bold'))
        
        # Configure button styles
        self.style.configure('TButton', font=('Poppins', 9), padding=6)
        self.style.configure('Accent.TButton', background=self.accent_color, 
                           foreground='#1a1a1f', font=('Poppins', 9, 'bold'))
        self.style.map('Accent.TButton',
                      background=[('active', '#7fffd6'), ('pressed', '#5eead4')])
        
        # Configure combobox
        self.style.configure('TCombobox', fieldbackground='#2a2a34', 
                           background='#2a2a34', padding=4, arrowcolor='#e8e8ec', foreground='#1a1a1f')
        self.style.map('TCombobox', foreground=[('readonly', '#1a1a1f')])
        
        # Configure entry
        self.style.configure('TEntry', padding=4, foreground='#1a1a1f')
        
        # Configure progress bar
        self.style.configure('Horizontal.TProgressbar', background=self.accent_color,
                           troughcolor=self.secondary_bg, borderwidth=0,
                           lightcolor=self.accent_color, darkcolor=self.accent_color)
        
        # Configure treeview
        self.style.configure('Treeview', background='#2a2a34', fieldbackground='#2a2a34',
                           foreground='#e8e8ec', rowheight=25)
        self.style.configure('Treeview.Heading', background=self.secondary_bg,
                           foreground=self.fg_color, font=('Poppins', 9, 'bold'),
                           relief='flat')
        self.style.map('Treeview', background=[('selected', self.accent_color)])
        
        # Configure scrollbar
        self.style.configure('Vertical.TScrollbar', background=self.secondary_bg,
                           troughcolor=self.bg_color, borderwidth=0,
                           arrowcolor=self.fg_color)

    def on_run(self):
        if self.worker_thread and self.worker_thread.is_alive():
            messagebox.showinfo("Please wait", "A benchmark is already in progress.")
            return
        alg = self.alg_var.get()
        col = self.col_var.get()
        try:
            N = int(self.n_var.get())
            if N <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Invalid N", "Please provide a positive integer for N.")
            return

        # Warning for O(n^2) algorithms
        if alg in ("Bubble Sort", "Insertion Sort") and N > 20000:
            cont = messagebox.askyesno("Large Dataset Warning",
                                       f"⚠️ {alg} with N={N} may take significant time.\n\nThis is an O(n²) algorithm. Continue anyway?",
                                       icon='warning')
            if not cont:
                return

        # prefer user-selected CSV, else fall back to the default lookup
        csv_path = getattr(self, 'csv_path', None) or find_csv_file()
        if not csv_path:
            messagebox.showerror("CSV not found",
                                 "Select a CSV file using 'Select CSV...' or place `generated_data.csv` in `data/` or the project root.")
            return

        # clear previous results
        for it in self.tree.get_children():
            self.tree.delete(it)
        self.load_time_var.set("Load: -")
        self.sort_time_var.set("Sort: -")
        self.total_time_var.set("Total: -")
        self.status_var.set("Initializing...")
        self.progress.config(mode='determinate')
        self.progress['value'] = 0
        self.progress_var.set("0%")

        # Launch worker thread
        args = (csv_path, N, alg, col)
        self.worker_thread = threading.Thread(target=self._worker, args=args, daemon=True)
        self.worker_thread.start()

    def _worker(self, csv_path, N, alg, col):
        try:
            self.msg_queue.put(("status", "📥 Loading CSV data..."))
            
            def load_progress_cb(pct):
                self.msg_queue.put(("progress", None))  # indeterminate
            
            rows, load_time = load_csv(csv_path, n_rows=N, progress_callback=load_progress_cb)
            self.load_time = load_time
            self.msg_queue.put(("load_time", load_time))
            if len(rows) == 0:
                self.msg_queue.put(("error", "No rows loaded from CSV."))
                return

            # choose key function
            if col == "ID":
                key_fn = lambda r: int(r.get('ID', 0)) if r.get('ID', '').strip() != '' else 0
            else:
                key_fn = lambda r: (r.get(col, '') or '').lower()

            # pick algorithm
            sort_fn = None
            if alg == "Bubble Sort":
                sort_fn = bubble_sort
            elif alg == "Insertion Sort":
                sort_fn = insertion_sort
            else:
                sort_fn = merge_sort

            # sorting with progress callback
            self.msg_queue.put(("status", f"⚡ Sorting with {alg}..."))
            start = time.perf_counter()

            def progress_cb(pct):
                # pct in [0.0, 1.0]
                self.msg_queue.put(("progress", pct))

            sorted_rows = sort_fn(rows, key_func=key_fn, progress_callback=progress_cb)

            sort_time = time.perf_counter() - start
            self.sort_time = sort_time
            self.msg_queue.put(("sort_done", sorted_rows[:10], sort_time))
        except Exception as e:
            self.msg_queue.put(("error", str(e)))

    def on_select_csv(self):
        path = filedialog.askopenfilename(
            title="Select CSV file", 
            filetypes=[("CSV files", "*.csv"), ("All files", "*")]
        )
        if path:
            self.csv_path = path
            # show a shortened path if it's long
            display = path
            if len(display) > 120:
                display = '...' + display[-117:]
            self.csv_path_var.set(display)
            self.status_var.set(f"📄 Loaded: {os.path.basename(path)}")

    def _poll_queue(self):
        try:
            while True:
                msg = self.msg_queue.get_nowait()
                self._handle_msg(msg)
        except queue.Empty:
            pass
        self.root.after(100, self._poll_queue)

    def _handle_msg(self, msg):
        typ = msg[0]
        if typ == 'status':
            self.status_var.set(msg[1])
            self.root.update_idletasks()
        elif typ == 'progress':
            pct = msg[1]
            if pct is None:
                # indeterminate progress - pulse animation
                if self.progress['mode'] != 'indeterminate':
                    self.progress.config(mode='indeterminate')
                self.progress.start(10)
                self.progress_var.set("Loading...")
            else:
                # determinate progress
                if self.progress['mode'] != 'determinate':
                    self.progress.config(mode='determinate')
                    self.progress.stop()
                self.progress['value'] = pct * 100
                self.progress_var.set(f"{int(pct*100)}%")
                self.status_var.set(f"Processing... {int(pct*100)}%")
            self.root.update_idletasks()
        elif typ == 'load_time':
            t = msg[1]
            self.load_time_var.set(f"📥 Load: {t:.4f} s")
            self.status_var.set("CSV loaded, starting sort...")
            self.root.update_idletasks()
        elif typ == 'sort_done':
            if self.progress['mode'] == 'indeterminate':
                self.progress.stop()
            top10, t = msg[1], msg[2]
            self.sort_time_var.set(f"⚡ Sort: {t:.4f} s")
            total_time = self.load_time + self.sort_time
            self.total_time_var.set(f"✅ Total: {total_time:.4f} s")
            self.progress['value'] = 100
            self.progress_var.set("100%")
            self.status_var.set("✅ Benchmark complete!")
            
            # Clear and insert new rows
            for it in self.tree.get_children():
                self.tree.delete(it)
            for r in top10:
                self.tree.insert('', tk.END, values=(
                    r.get('ID', ''), 
                    r.get('FirstName', ''), 
                    r.get('LastName', '')
                ))
            self.root.update_idletasks()
        elif typ == 'error':
            self.status_var.set("❌ Error")
            self.progress_var.set("Failed")
            messagebox.showerror("Error", msg[1], icon='error')
        else:
            # unknown
            pass


if __name__ == '__main__':
    root = tk.Tk()
    app = SortBenchmarkApp(root)
    root.mainloop()