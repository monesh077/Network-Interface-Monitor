Overview NetMon is a real-time network interface monitoring tool built with Python. It visualizes your computer's download and upload speeds and tracks total session data usage. The application features a user-friendly GUI built with Tkinter and uses psutil to retrieve network statistics and matplotlib to plot traffic graphs.

Features - Real-time network speed monitoring (download and upload) - Session total data sent and received - Dynamic graph displaying bandwidth usage over time - User-friendly Tkinter GUI with clear stats display

Technologies Used - Python 3.x - psutil (for network stats) - matplotlib (for graph plotting) - Tkinter (for GUI)

Installation 1. Clone the repository: git clone https://github.com/yourusername/NetMon-Network-Traffic-Analyzer.git 2. Navigate to the project directory: cd NetMon-Network-Traffic-Analyzer 3. Install dependencies: pip install -r requirements.txt

Usage To run the application, execute: python main.py The GUI window will launch showing real-time network stats and traffic graph.

How It Works - The monitor.py module handles retrieving network interface data using psutil. - The ui.py module builds the GUI and plots real-time graphs with matplotlib. - The main.py script initializes and runs the Tkinter application.

Project Structure - monitor.py - Backend network data monitoring logic - ui.py - Frontend GUI and plotting logic - main.py - Application launcher - requirements.txt - Python dependencies

License This project is open source and available under the MIT License.
