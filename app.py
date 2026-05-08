from flask import Flask, render_template
import json
import subprocess
import platform

app = Flask(__name__)


def ping_server(ip):
    system = platform.system().lower()

    if system == 'windows':
        command = ["ping", "-n", "1", "-w", "1000", ip]
    else:
        command = ["ping", "-c", "1", ip]

    try:
        result = subprocess.rum(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=2
        )
        return result.returncode == 0
    except Exception:
        return False


@app.route('/')
def dashboard():
    with open("data/servers.json", "r") as file:
        servers = json.load(file)

    checked_server = []

    for server in servers:
        is_online = ping_server(server["ip"])
        checked_server.append({
            "name": server["name"],
            "ip": server["ip"],
            "status": "Online" if is_online else "Offline"
        })

    online_count = sum(
        1 for server in checked_server if server["status"] == "Online")
    offline_count = len(checked_server) - online_count

    return render_template(
        "dashboard.html",
        servers=checked_server,
        online_count=online_count,
        offline_count=offline_count
    )


if __name__ == "__main__":
    app.run(debug=True)
