
# 🖥️ System Performance Monitor

This is a lightweight Python script to monitor and log **CPU** and **memory usage** over time. It collects performance data at regular intervals and stores it in a CSV file for later analysis.

---

## 📂 Features

- Logs **CPU** and **RAM** usage percentage every few seconds
- Saves logs to a specified subdirectory in CSV format
- Runs silently in the background for a defined duration
- Gracefully handles interruptions and I/O errors

---

## 🛠️ Requirements

- Python 3.6+
- [psutil](https://pypi.org/project/psutil/)

Install the required dependency using:

```bash
pip install psutil
```

---

## 🚀 How to Run

```bash
python system_performance.py
```

The script will:

- Log system performance every `5 seconds` (configurable)
- Run for `60 minutes` by default (configurable)
- Save the output to `System performance/performance_logs/system_performance_log.csv`

---

## ⚙️ Configuration

You can modify the following variables at the top of `system_performance.py`:

```python
LOG_INTERVAL_SECONDS = 5        # Time between logs
LOG_DURATION_MINUTES = 60       # Total runtime
LOG_FILE_NAME = "system_performance_log.csv"
LOG_FILE_DIRECTORY = "System performance/performance_logs"
```

---

## 📈 Sample Output (CSV)

```csv
Timestamp,CPU Usage (%),Memory Usage (%)
2025-05-29 11:00:00,25.3,48.7
2025-05-29 11:00:05,22.1,47.9
...
```

---

## 💡 Use Cases

- Monitor system load while running intensive tasks
- Performance benchmarking
- Long-running server health monitoring
- Lightweight alternative to GUI-based system monitors

---

## 🧯 Error Handling

- If the target directory cannot be created, the script falls back to the current directory
- If file writing fails, logs are printed to the console
- Keyboard interrupts (Ctrl+C) are gracefully handled

---

## 📃 License

This project is open source and available under the [MIT License](LICENSE).
