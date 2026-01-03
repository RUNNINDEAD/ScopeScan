import subprocess
import threading
import time
import sys


def spinner(stop_event):
    frames = ["|", "/", "-", "\\"]
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\rScanning... {frames[i % len(frames)]}")
        sys.stdout.flush()
        i += 1
        time.sleep(0.15)

    # Clear spinner line
    sys.stdout.write("\r" + " " * 30 + "\r")
    sys.stdout.flush()


def run_scan(target: str) -> str:
    print(f"Starting Nmap scan on: {target}\n")

    cmd = ["nmap", "-O", "-Pn", "-sV", "-p-", "--open", target]
    stop_event = threading.Event()

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        spin_thread = threading.Thread(target=spinner, args=(stop_event,), daemon=True)
        spin_thread.start()

        stdout, stderr = proc.communicate()
        stop_event.set()
        spin_thread.join()

        output = stdout or ""
        if stderr:
            output += "\n--- STDERR ---\n" + stderr

        print("Scan completed.\n")
        print(output)

        return output

    except FileNotFoundError:
        stop_event.set()
        return "Nmap is not installed or not found in PATH.\n"

    except KeyboardInterrupt:
        stop_event.set()
        try:
            proc.terminate()
        except Exception:
            pass
        return "Scan cancelled by user.\n"
