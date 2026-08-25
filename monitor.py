import subprocess

def is_container_running(container_name):
    """
    Checks if a Docker container with the given name is currently running.
    Returns True if running, False if stopped or not found.
    """
    result = subprocess.run(
        ["docker", "ps", "--filter", f"name={container_name}", "--filter", "status=running", "--format", "{{.Names}}"],
        capture_output=True,
        text=True
    )
    running_containers = result.stdout.strip().splitlines()
    return container_name in running_containers

if __name__ == "__main__":
    test_container = "test-container"  # we'll replace this with real container names later
    if is_container_running(test_container):
        print(f"[OK] Container '{test_container}' is running.")
    else:
        print(f"[ALERT] Container '{test_container}' is NOT running.")