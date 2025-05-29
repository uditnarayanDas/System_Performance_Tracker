import psutil
import time
import datetime
import csv
import os

# --- Configuration ---
LOG_INTERVAL_SECONDS = 5  # How often to log data (in seconds)
LOG_DURATION_MINUTES = 60  # How long to run the monitoring (in minutes)
LOG_FILE_NAME = "system_performance_log.csv"
LOG_FILE_DIRECTORY = "System performance/performance_logs" # Optional: subdirectory to store logs

# --- Helper Functions ---
def get_cpu_usage():
    """Returns the current system-wide CPU utilization as a percentage."""
    return psutil.cpu_percent(interval=None) # `interval=None` for non-blocking call

def get_memory_usage():
    """Returns the current system-wide memory utilization as a percentage."""
    memory_info = psutil.virtual_memory()
    return memory_info.percent

def setup_logging():
    """Creates the log directory (if specified) and prepares the CSV log file with headers."""
    if LOG_FILE_DIRECTORY:
        if not os.path.exists(LOG_FILE_DIRECTORY):
            try:
                os.makedirs(LOG_FILE_DIRECTORY)
                print(f"Created log directory: {LOG_FILE_DIRECTORY}")
            except OSError as e:
                print(f"Error creating directory {LOG_FILE_DIRECTORY}: {e}")
                # Fallback to current directory if subdir creation fails
                return LOG_FILE_NAME
        log_path = os.path.join(LOG_FILE_DIRECTORY, LOG_FILE_NAME)
    else:
        log_path = LOG_FILE_NAME

    file_exists = os.path.isfile(log_path)
    try:
        with open(log_path, 'a', newline='') as csvfile:
            log_writer = csv.writer(csvfile)
            if not file_exists or os.path.getsize(log_path) == 0: # Write header only if new file or empty
                log_writer.writerow(["Timestamp", "    CPU Usage (%)", "    Memory Usage (%)"])
        print(f"Logging to: {os.path.abspath(log_path)}")
        return log_path
    except IOError as e:
        print(f"Error opening or writing to log file {log_path}: {e}")
        print("Logging will proceed to console only if file logging fails.")
        return None


def log_performance_data(log_writer, timestamp, cpu_usage, memory_usage):
    """Writes a single row of performance data to the CSV file."""
    if log_writer:
        log_writer.writerow([timestamp, cpu_usage, memory_usage])
    else: # Fallback to console if file logging is not available
        print(f"{timestamp}, CPU: {cpu_usage}%, Memory: {memory_usage}%")

# --- Main Monitoring Logic ---
def monitor_system():
    """Monitors and logs CPU and memory usage for a specified duration."""
    log_path = setup_logging()
    log_file_object = None
    csv_writer = None

    if log_path:
        try:
            log_file_object = open(log_path, 'a', newline='')
            csv_writer = csv.writer(log_file_object)
        except IOError as e:
            print(f"Error opening log file for appending: {e}. Will log to console.")
            log_path = None # Ensure no further file operations if open failed

    start_time = time.time()
    end_time = start_time + (LOG_DURATION_MINUTES * 60)
    monitoring_count = 0

    print(f"Starting system performance monitoring for {LOG_DURATION_MINUTES} minutes...")
    print(f"Logging data every {LOG_INTERVAL_SECONDS} seconds.")
    print("Press Ctrl+C to stop early.")

    try:
        while time.time() < end_time:
            # Get current timestamp
            current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Get performance data
            cpu = get_cpu_usage()
            memory = get_memory_usage()

            # Log the data
            log_performance_data(csv_writer, current_timestamp, cpu, memory)

            if not log_path: # If file logging failed, print to console
                 print(f"{current_timestamp},           CPU: {cpu}%,        Memory: {memory}%")


            monitoring_count += 1
            # Wait for the next interval
            time.sleep(LOG_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    except Exception as e:
        print(f"\nAn error occurred during monitoring: {e}")
    finally:
        if log_file_object:
            log_file_object.close()
        duration_ran_seconds = time.time() - start_time
        print(f"\nMonitoring finished after {duration_ran_seconds:.2f} seconds.")
        print(f"Logged {monitoring_count} data points.")
        if log_path:
            print(f"Performance data saved to: {os.path.abspath(log_path)}")
        else:
            print("Performance data was logged to the console.")

if __name__ == "__main__":
    # --- Ensure psutil is installed ---
    try:
        import psutil
    except ImportError:
        print("The 'psutil' library is required to run this script.")
        print("Please install it by running: pip install psutil")
        exit()
    monitor_system()
    