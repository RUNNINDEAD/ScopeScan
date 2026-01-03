import subprocess


def run_arp_scan(interface: str | None = None) -> list[str]:
    """
    Runs an ARP scan and returns a list of discovered IP addresses.
    """
    cmd = ["sudo", "arp-scan", "--localnet"]

    if interface:
        cmd.extend(["-i", interface])

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        hosts = []
        for line in result.stdout.splitlines():
            if line and line[0].isdigit():
                ip = line.split()[0]
                hosts.append(ip)

        return hosts

    except FileNotFoundError:
        print("arp-scan is not installed.")
        return []
