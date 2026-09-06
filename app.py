import threading
import time

from flask import Flask, render_template
from monitor import (
    get_monitored_containers,
    get_container_status,
    get_container_health,
    get_container_image,
    get_container_uptime,
    get_container_restart_count,
    get_recovery_events,
    monitor_once,
)

app = Flask(__name__)


def monitoring_loop():
    """
    Runs the OpenClaw monitoring cycle continuously.
    """
    while True:
        monitor_once()
        time.sleep(10)


@app.route("/")
def home():
    containers = []

    for name in get_monitored_containers():
        status = get_container_status(name)
        health = get_container_health(name)
        image = get_container_image(name)
        uptime = get_container_uptime(name)
        restart_count = get_container_restart_count(name)

        containers.append(
            {
                "name": name,
                "status": status,
                "health": health,
                "image": image,
                "uptime": uptime,
                "restart_count": restart_count,
            }
        )

    running_count = sum(
        1 for container in containers
        if container["status"].startswith("Up")
    )

    stopped_count = len(containers) - running_count

    recovery_events = get_recovery_events()

    return render_template(
        "index.html",
        containers=containers,
        running_count=running_count,
        stopped_count=stopped_count,
        recovery_events=recovery_events,
    )

monitor_thread = threading.Thread(
    target=monitoring_loop,
    daemon=True,
)
monitor_thread.start()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
