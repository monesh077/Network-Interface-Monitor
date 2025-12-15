import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import deque
from monitor import NetworkMonitor  # Importing our logic

class NetworkMonitorApp:
    def __init__(self, root):
        self.root = root
        self.monitor = NetworkMonitor()  # Connect to the backend



        # UI Window Setup
        self.root.title("NetMon - Network Traffic Analyzer")
        self.root.geometry("750x550")
        self.root.configure(bg="#f4f4f4")

        # Graph Data Storage (Last 60 seconds)
        self.time_points = deque(maxlen=60)
        self.download_points = deque(maxlen=60)
        self.upload_points = deque(maxlen=60)

        self.setup_widgets()
        self.update_loop()

    def setup_widgets(self):
        # 1. Main Title
        title_frame = tk.Frame(self.root, bg="#f4f4f4")
        title_frame.pack(pady=10)
        tk.Label(title_frame, text="Network Interface Monitor", font=("Segoe UI", 16, "bold"), bg="#f4f4f4", fg="#333").pack()

        # 2. Stats Panel (The Cards)
        stats_frame = tk.Frame(self.root, bg="white", bd=1, relief="solid")
        stats_frame.pack(fill="x", padx=20, pady=5)

        # Download Label
        self.lbl_down = tk.Label(stats_frame, text="↓ Down: 0 KB/s", font=("Consolas", 12, "bold"), fg="#007acc", bg="white")
        self.lbl_down.pack(side="left", expand=True, pady=15)

        # Upload Label
        self.lbl_up = tk.Label(stats_frame, text="↑ Up: 0 KB/s", font=("Consolas", 12, "bold"), fg="#28a745", bg="white")
        self.lbl_up.pack(side="left", expand=True, pady=15)

        # 3. Total Usage Text
        self.lbl_total = tk.Label(self.root, text="Session Total: Sent: 0 MB | Recv: 0 MB", font=("Segoe UI", 10), bg="#f4f4f4", fg="#666")
        self.lbl_total.pack(pady=5)

        # 4. Matplotlib Graph
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Real-time Traffic Bandwidth")
        self.ax.set_xlabel("Time (seconds)")
        self.ax.set_ylabel("Speed (KB/s)")
        self.ax.grid(True, linestyle=':', alpha=0.6)
        
        # Plot lines
        self.line_dl, = self.ax.plot([], [], label="Download", color="#007acc", linewidth=1.5)
        self.line_ul, = self.ax.plot([], [], label="Upload", color="#28a745", linewidth=1.5)
        self.ax.legend(loc="upper left")

        # Add Graph Canvas to Window
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # 5. SIGNATURE FOOTER (The "Showcase" Section)
        # This creates a dark bar at the bottom with your details
        footer_frame = tk.Frame(self.root, bg="#333333", height=30)
        footer_frame.pack(side="bottom", fill="x")

        # EDIT YOUR NAME HERE
        my_signature = "Project by Ayush S | Engg. Student (CS-AI)"
        
        lbl_sig = tk.Label(
            footer_frame, 
            text=my_signature, 
            font=("Segoe UI", 9), 
            fg="white",      # White text
            bg="#333333"     # Dark grey background
        )
        lbl_sig.pack(side="right", padx=15, pady=5)
        
        # Optional: Add a "System Status" on the left of the footer
        lbl_status = tk.Label(footer_frame, text="● System Online", font=("Segoe UI", 8), fg="#00ff00", bg="#333333")
        lbl_status.pack(side="left", padx=15, pady=5)

    def update_loop(self):
        # 1. Fetch data from backend
        down_bps, up_bps, total_sent, total_recv = self.monitor.get_speed()

        # 2. Convert for display (KB/s)
        down_kb = down_bps / 1024
        up_kb = up_bps / 1024

        # 3. Update Text
        self.lbl_down.config(text=f"↓ Down: {self.monitor.format_bytes(down_bps)}/s")
        self.lbl_up.config(text=f"↑ Up: {self.monitor.format_bytes(up_bps)}/s")
        self.lbl_total.config(text=f"Session Total: Sent: {self.monitor.format_bytes(total_sent)} | Recv: {self.monitor.format_bytes(total_recv)}")

        # 4. Update Graph Data
        self.download_points.append(down_kb)
        self.upload_points.append(up_kb)
        
        # X-axis logic
        if not hasattr(self, 'tick_counter'): self.tick_counter = 0
        self.tick_counter += 1
        self.time_points.append(self.tick_counter)
        
        # Redraw lines
        self.line_dl.set_data(range(len(self.download_points)), self.download_points)
        self.line_ul.set_data(range(len(self.upload_points)), self.upload_points)
        
        # Rescale view dynamically
        self.ax.set_xlim(0, 60)
        current_max = max(max(self.download_points, default=0), max(self.upload_points, default=0))
        self.ax.set_ylim(0, max(10, current_max * 1.2)) 
        
        self.canvas.draw()

        # 5. Repeat every 1000ms
        self.root.after(1000, self.update_loop)