# ScopeScan

ScopeScan is a lightweight, interactive network reconnaissance tool written in Python.  
It allows users to discover hosts, manually enter targets, run comprehensive Nmap scans, and optionally save results through a clean command-line interface.

This project is designed for learning, home labs, and defensive security practice.

---

## Requirements

- Must be run as **root** (required for ARP scanning and full Nmap functionality)
- Python **3.10+** installed
- Nmap installed and available in PATH

### Install dependencies (Debian / Ubuntu / Pop!_OS)

```bash
sudo apt update
sudo apt install nmap arp-scan python3
