import psutil
import time
import csv
import matplotlib.pyplot as plt
from datetime import datetime

# Define the CSV file to log data
LOG_FILE = "system_resources_log.csv"

# Initialize CSV logging with headers
def initialize_csv():
    with open(LOG_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "CPU (%)", "Memory (%)", "Disk Usage (%)",
                         "Network Sent (KB)", "Network Received (KB)",
                         "Upload Speed (KB/s)", "Download Speed (KB/s)"])

# Log current system metrics to CSV
def log_system_metrics(previous_net_io):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    current_net_io = psutil.net_io_counters()

    # Convert to KB
    network_sent = current_net_io.bytes_sent / 1024
    network_received = current_net_io.bytes_recv / 1024

    # Calculate bandwidth (Upload and Download speed in KB/s)
    upload_speed = (current_net_io.bytes_sent - previous_net_io.bytes_sent) / 1024
    download_speed = (current_net_io.bytes_recv - previous_net_io.bytes_recv) / 1024

    with open(LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, cpu_percent, memory_percent, disk_percent,
                         network_sent, network_received, upload_speed, download_speed])

    # Print current stats
    print(f"Time: {timestamp}, CPU: {cpu_percent}%, Memory: {memory_percent}%, Disk: {disk_percent}%, "
          f"Network Sent: {network_sent:.2f} KB, Network Received: {network_received:.2f} KB, "
          f"Upload Speed: {upload_speed:.2f} KB/s, Download Speed: {download_speed:.2f} KB/s")

    return current_net_io  # Return current network stats for the next calculation

# Function to show a graph of logged data
def show_graph():
    timestamps, cpu_data, memory_data, disk_data, net_sent_data, net_recv_data, upload_speed_data, download_speed_data = [], [], [], [], [], [], [], []

    with open(LOG_FILE, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            timestamps.append(row[0])
            cpu_data.append(float(row[1]))
            memory_data.append(float(row[2]))
            disk_data.append(float(row[3]))
            net_sent_data.append(float(row[4]))
            net_recv_data.append(float(row[5]))
            upload_speed_data.append(float(row[6]))
            download_speed_data.append(float(row[7]))

    # Plot the data
    plt.figure(figsize=(12, 10))

    plt.subplot(3, 2, 1)
    plt.plot(timestamps, cpu_data, label="CPU (%)", color="blue")
    plt.xticks(rotation=45)
    plt.legend()

    plt.subplot(3, 2, 2)
    plt.plot(timestamps, memory_data, label="Memory (%)", color="green")
    plt.xticks(rotation=45)
    plt.legend()

    plt.subplot(3, 2, 3)
    plt.plot(timestamps, disk_data, label="Disk Usage (%)", color="purple")
    plt.xticks(rotation=45)
    plt.legend()

    plt.subplot(3, 2, 4)
    plt.plot(timestamps, upload_speed_data, label="Upload Speed (KB/s)", color="orange")
    plt.plot(timestamps, download_speed_data, label="Download Speed (KB/s)", color="red")
    plt.xticks(rotation=45)
    plt.legend()

    plt.subplot(3, 2, 5)
    plt.plot(timestamps, net_sent_data, label="Total Network Sent (KB)", color="brown")
    plt.plot(timestamps, net_recv_data, label="Total Network Received (KB)", color="pink")
    plt.xticks(rotation=45)
    plt.legend()

    plt.tight_layout()
    plt.show()

# Initialize CSV file for the first run
initialize_csv()

# Continuous logging and monitoring
try:
    print("Starting System Resource Monitor. Press Ctrl+C to stop.")
    previous_net_io = psutil.net_io_counters()
    while True:
        previous_net_io = log_system_metrics(previous_net_io)
        time.sleep(5)  # Adjust as needed for logging interval
except KeyboardInterrupt:
    print("Logging stopped. Generating graphs...")
    show_graph()
