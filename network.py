import os
import socket


def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "Unknown"


def is_ip(address):
    try:
        socket.inet_aton(address)
        return True
    except socket.error:
        return False


def get_targets():

    hosts = input(
        "Enter target IPs/hostnames: "
    ).split(",")

    hosts = [host.strip() for host in hosts if host.strip()]

    for host in hosts:
        response = os.system(f"ping -c 2 {host} > /dev/null 2>&1")
        if response == 0:
            print(f"Ping successful for host {host}")

            if is_ip(host):
                hostname = get_hostname(host)
                print(f"Hostname Found: {hostname}")
            else:
                try:
                    ip = socket.gethostbyname(host)
                    print(f"Resolved IP address: {ip}")
                except socket.gaierror:
                    print(f"Could not resolve hostname: {host}")
        else:
            print(f"Failed to reach host {host}")

    return hosts


if __name__ == "__main__":
    get_targets()
