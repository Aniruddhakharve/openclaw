import subprocess


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
    Attempts to restart a stopped Docker container.

    Returns:
        True  - if the container was successfully restarted
                and verified as running.
        False - if the restart failed or the container
                was not running after the restart.
    """
    result = subprocess.run(
        ["docker", "restart", container_name],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"[ERROR] Docker restart failed: {result.stderr.strip()}")
        return False

    return is_container_running(container_name)


if __name__ == "__main__":
    test_container = "test-container"

    if is_container_running(test_container):
        print(f"[OK] Container '{test_container}' is running.")

    else:
        print(f"[ALERT] Container '{test_container}' is NOT running.")

        if restart_container(test_container):
            print(
                f"[RECOVERY] Container '{test_container}' "
                "restart command succeeded."
            )
        else:
            print(
                f"[ERROR] Failed to restart container "
                f"'{test_container}'."
            )