import subprocess
import json
import os
from datetime import datetime, timezone


def get_monitored_containers():
    """
    Returns the names of all Docker containers
    with the OpenClaw monitoring label.
    """
    result = subprocess.run(
        [
            "docker",
            "ps",
            "-a",
            "--filter",
            "label=io.openclaw.monitor=true",
            "--format",
            "{{.Names}}",
        ],
        capture_output=True,
        text=True,
    )

    return result.stdout.strip().splitlines()


def get_container_status(container_name):
    """
    Returns the current Docker status of a container.
    """
    result = subprocess.run(
        [
            "docker",
            "ps",
            "-a",
            "--filter",
            f"name={container_name}",
            "--format",
            "{{.Status}}",
        ],
        capture_output=True,
        text=True,
    )

    return result.stdout.strip()


def get_container_health(container_name):
    """
    Returns the Docker health status of a container.
    """
    result = subprocess.run(
        [
            "docker",
            "inspect",
            "--format",
            "{{if .State.Health}}{{.State.Health.Status}}{{else}}no-healthcheck{{end}}",
            container_name,
        ],
        capture_output=True,
        text=True,
    )

    return result.stdout.strip()


def get_container_image(container_name):
    """
    Returns the Docker image used by a container.
    """
    result = subprocess.run(
        [
            "docker",
            "inspect",
            "--format",
            "{{.Config.Image}}",
            container_name,
        ],
        capture_output=True,
        text=True,
    )

    return result.stdout.strip()



def get_container_uptime(container_name):
    """
    Returns how long a container has been running.
    """
    result = subprocess.run(
        [
            "docker",
            "inspect",
            "--format",
            "{{.State.StartedAt}}",
            container_name,
        ],
        capture_output=True,
        text=True,
    )

    started_at = result.stdout.strip()

    if not started_at:
        return "N/A"

    started_time = datetime.fromisoformat(
        started_at.replace("Z", "+00:00")
    )

    uptime = datetime.now(timezone.utc) - started_time

    total_seconds = int(uptime.total_seconds())

    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)

    if days > 0:
        return f"{days}d {hours}h {minutes}m"

    if hours > 0:
        return f"{hours}h {minutes}m"

    return f"{minutes}m"


def get_container_restart_count(container_name):
    """
    Returns the number of times a container has been restarted.
    """
    result = subprocess.run(
        [
            "docker",
            "inspect",
            "--format",
            "{{.RestartCount}}",
            container_name,
        ],
        capture_output=True,
        text=True,
    )

    return result.stdout.strip()



def is_container_running(container_name):
    """
    Checks if a Docker container with the given name is currently running.
    Returns True if running, False if stopped or not found.
    """
    result = subprocess.run(
        [
            "docker",
            "ps",
            "--filter",
            f"name={container_name}",
            "--filter",
            "status=running",
            "--format",
            "{{.Names}}",
        ],
        capture_output=True,
        text=True,
    )

    running_containers = result.stdout.strip().splitlines()

    return container_name in running_containers


def restart_container(container_name):
    """
    Restarts a stopped container and records the recovery result.
    """
    result = subprocess.run(
        ["docker", "restart", container_name],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(
            f"[ERROR] Failed to restart '{container_name}': "
            f"{result.stderr.strip()}"
        )

        record_recovery_event(container_name, False)
        return False

    if is_container_running(container_name):
        print(
            f"[RECOVERY] Container '{container_name}' "
            "restarted successfully."
        )

        record_recovery_event(container_name, True)
        return True

    print(
        f"[ERROR] Container '{container_name}' "
        "did not start after restart."
    )

    record_recovery_event(container_name, False)
    return False



RECOVERY_LOG_FILE = "data/recovery_log.json"

def record_recovery_event(container_name, success):
    """
    Records a container recovery event.
    """
    events = []

    if os.path.exists(RECOVERY_LOG_FILE):
        with open(RECOVERY_LOG_FILE, "r", encoding="utf-8") as file:
            events = json.load(file)

    event = {
        "container": container_name,
        "success": success,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    events.append(event)

    with open(RECOVERY_LOG_FILE, "w", encoding="utf-8") as file:
        json.dump(events, file, indent=4)


def get_recovery_events():
    """
    Returns all recorded recovery events.
    """
    if not os.path.exists(RECOVERY_LOG_FILE):
        return []

    with open(RECOVERY_LOG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


MAINTENANCE_FILE = "data/maintenance.json"


def is_container_in_maintenance(container_name):
    """
    Checks whether a container is currently in maintenance mode.
    """
    if not os.path.exists(MAINTENANCE_FILE):
        return False

    with open(MAINTENANCE_FILE, "r", encoding="utf-8") as file:
        maintenance_data = json.load(file)

    return container_name in maintenance_data.get("containers", [])


def monitor_once():
    """
    Performs one monitoring cycle.
    """
    monitored_containers = get_monitored_containers()

    print("[DISCOVERY] Monitored containers:")

    for container in monitored_containers:
        print(f" - {container}")

    print("\n[MONITOR] Checking container status...")

    for container in monitored_containers:
        if is_container_running(container):
            print(f"[OK] Container '{container}' is running.")

        else:
            if is_container_in_maintenance(container):
                print(
                    f"[MAINTENANCE] Container '{container}' "
                    "is in maintenance mode. Skipping restart."
                )
            else:
                print(
                    f"[ALERT] Container '{container}' "
                    "is NOT running."
                )
                restart_container(container)


if __name__ == "__main__":
    monitor_once()