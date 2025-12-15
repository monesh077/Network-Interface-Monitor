import tkinter as tk
from ui import NetworkMonitorApp

if __name__ == "__main__":
    # Create the root window
    root = tk.Tk()
    
    # Initialize the Application
    app = NetworkMonitorApp(root)
    
    # Start the main event loop
    root.mainloop()