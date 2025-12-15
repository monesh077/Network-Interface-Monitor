import psutil
import time

class NetworkMonitor:
    def __init__(self):
        self.last_upload = 0
        self.last_download = 0
        self.last_time = time.time()
        
        # Initialize with current values so we don't get a huge spike at start
        counters = psutil.net_io_counters()
        self.last_upload = counters.bytes_sent
        self.last_download = counters.bytes_recv

    def get_speed(self):
        """
        Calculates the speed since the last check.
        Returns: (download_speed_bps, upload_speed_bps, total_sent, total_recv)
        """
        counters = psutil.net_io_counters()
        current_upload = counters.bytes_sent
        current_download = counters.bytes_recv
        current_time = time.time()

        time_delta = current_time - self.last_time
        
        down_speed = 0
        up_speed = 0

        if time_delta > 0:
            up_speed = (current_upload - self.last_upload) / time_delta
            down_speed = (current_download - self.last_download) / time_delta

        # Update state for next calculation
        self.last_upload = current_upload
        self.last_download = current_download
        self.last_time = current_time

        return down_speed, up_speed, current_upload, current_download

    @staticmethod
    def format_bytes(size):
        """Converts bytes to readable formats (KB, MB, GB)"""
        for unit in ['', 'K', 'M', 'G', 'T']:
            if size < 1024:
                return f"{size:.2f} {unit}B"
            size /= 1024
        return f"{size:.2f} PB"