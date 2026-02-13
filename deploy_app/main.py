from flask import Flask, jsonify
import os
import time
from datetime import datetime, timezone

app = Flask(__name__)


# -------- CPU USING LOAD AVERAGE --------
def get_cpu_usage():
    load1, _, _ = os.getloadavg()      # 1-minute load average
    cpu_count = os.cpu_count()

    if cpu_count == 0:
        return 0.0

    cpu_percentage = (load1 / cpu_count) * 100
    return round(cpu_percentage, 2)


# -------- MEMORY USING /proc/meminfo --------
def get_memory_usage():
    with open("/proc/meminfo", "r") as f:
        lines = f.readlines()

    mem_total = int(lines[0].split()[1])       # MemTotal (kB)
    mem_available = int(lines[2].split()[1])  # MemAvailable (kB)

    used = mem_total - mem_available
    memory_percentage = (used / mem_total) * 100

    return round(memory_percentage, 2)


# -------- UPTIME USING /proc/uptime --------
def get_uptime():
    with open("/proc/uptime", "r") as f:
        uptime_seconds = float(f.readline().split()[0])

    return int(uptime_seconds)


# -------- HOME PAGE (UI) --------
@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>Cloud Run Monitor</title>
        </head>
        <body style="font-family: Arial; text-align: center; margin-top: 80px;">
            <h1>🚀 Cloud Run Monitoring Dashboard</h1>
            <p>System check complete.</p>

            <br>

            <a href="/analyze">
                <button style="
                    padding: 10px 20px;
                    font-size: 16px;
                    background-color: #4285F4;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;">
                    View System Analysis (JSON)
                </button>
            </a>
        </body>
    </html>
    """


# -------- ANALYZE ROUTE --------
@app.route("/analyze")
def analyze():
    timestamp = datetime.now(timezone.utc).isoformat()
    uptime_seconds = get_uptime()
    cpu_metric = get_cpu_usage()
    memory_metric = get_memory_usage()

    # Custom health score logic
    health_score = 100 - int((cpu_metric + memory_metric) / 2)
    health_score = max(0, min(100, health_score))

    if health_score >= 75:
        message = "System healthy"
    elif health_score >= 50:
        message = "System stable"
    else:
        message = "System under heavy load"

    return jsonify({
        "timestamp": timestamp,
        "uptime_seconds": uptime_seconds,
        "cpu_metric": cpu_metric,
        "memory_metric": memory_metric,
        "health_score": health_score,
        "message": message
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

