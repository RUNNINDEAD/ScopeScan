from network import get_targets
from nmap_scan import run_scan
from arp import run_arp_scan
import os
import socket


def save_scan(target: str, output: str, filename: str | None = None):
    if output is None:
        output = ""

    safe_target = target.replace("/", "-")

    if not filename:
        filename = f"scan_{safe_target}.txt"

    scans_dir = "SavedScans"
    os.makedirs(scans_dir, exist_ok=True)
    filepath = os.path.join(scans_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Target: {target}\n")
        f.write("Scan Results:\n")
        f.write(output)

    print(f"\nScan saved to: {filepath}")


def pick_target(targets):
    print("\nTargets:")
    for i, host in enumerate(targets, 1):
        print(f"{i}. {host}")

    while True:
        selection = input(
            "Select target [Enter = 1, number, IP, or 'q' to quit]: "
        ).strip().lower()

        if selection == "":
            return targets[0]

        if selection == "q":
            return None

        if selection.isdigit():
            index = int(selection) - 1
            if 0 <= index < len(targets):
                return targets[index]

        if selection in targets:
            return selection

        print("Invalid selection. Please try again.")


def choose_target_input_method():
    while True:
        print("\nTarget selection method:")
        print("1. Discover hosts (Ping / ARP)")
        print("2. Enter hostname or IP manually")

        choice = input("Select option [1/2] or Enter = 1): ").strip()

        if choice == "" or choice == "1":
            return "discover"
        if choice == "2":
            return "manual"

        print("Invalid choice. Please select 1 or 2.")


def choose_discovery_method():
    while True:
        print("\nDiscovery method:")
        print("1. Ping")
        print("2. ARP (local network only)")

        method = input("Select method [1/2] or Enter = 1): ").strip()

        if method == "" or method == "1":
            return "ping"
        if method == "2":
            return "arp"

        print("Invalid selection.")


def manual_target_entry():
    while True:
        target = input("\nEnter hostname or IP (or 'q' to quit): ").strip()
        if target.lower() == "q":
            return None

        # Optional: basic hostname/IP validation
        try:
            socket.gethostbyname(target)
            return target
        except socket.gaierror:
            print("Invalid hostname or IP. Please try again.")


def main():
    try:
        mode = choose_target_input_method()

        if mode == "manual":
            target = manual_target_entry()
            if not target:
                print("Exiting...")
                return
            targets = [target]

        else:
            discovery = choose_discovery_method()

            if discovery == "arp":
                print("\nRunning ARP scan (local network)...")
                targets = run_arp_scan()
            else:
                targets = get_targets()

            if not targets:
                print("No targets were found.")
                return

            target = pick_target(targets)
            if not target:
                print("Exiting...")
                return

        choice = input("\nWould you like to run an Nmap scan? (y/n): ").strip().lower()

        if choice == "n":
            print("Okay — scan not started.")
            return
        elif choice != "y":
            print("Invalid choice.")
            return

        output = run_scan(target)

        if not output.strip():
            print("\nNo scan output returned.")

        save_choice = input("\nSave scan results to a file? (y/n): ").strip().lower()

        if save_choice == "y":
            custom_name = input("Enter filename (press Enter for default): ").strip()
            save_scan(target, output, filename=custom_name if custom_name else None)
        elif save_choice == "n":
            print("Scan results not saved.")
        else:
            print("Invalid choice. Scan results not saved.")

    except KeyboardInterrupt:
        print("\nExiting...")


if __name__ == "__main__":
    main()
