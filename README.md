
---

# MAC Spoofer

MAC Spoofer is a Python script designed to display network information, spoof MAC addresses, and reset MAC addresses on a system. It provides a user-friendly interface for managing MAC addresses.

## Author

- **Author:** Muhammad Ahmed
- **Roll Number:** 20I-1855
- **Section:** CY-T
- **Degree:** Bachelors in Software Engineering
- **Campus:** Islamabad
- **Course Subject:** Ethical Hacking Concepts and Practices

## Features

- Display original and current MAC addresses of the system.
- Spoof MAC addresses from a variety of options.
- Reset MAC address to the original value.
- User-friendly terminal interface.
- Random MAC address generation.
- ARP packet sniffing for MAC address detection.
- Ability to read MAC addresses from a CSV file.

### Terminal Interface

 - Uses Terminal GUI

### Wireshark

 - Verified using Wireshark

## Dependencies

- For Linux:
  - [scapy](https://scapy.net/): Packet manipulation library.
  - [psutil](https://pypi.org/project/psutil/): System information retrieval library.
  - `subprocess` module (Python standard library): For executing system commands.
  - `csv` module (Python standard library): For reading MAC addresses from a file.
- For Windows:
  - Equivalent tools for network interface manipulation: Use `netsh` command.
  - Equivalent tools for viewing ARP cache: Use `arp` command.
  - Note: Windows does not have a direct equivalent of `sudo`. Run the script with elevated privileges (Run as Administrator) if required.
## Usage

1. Clone the repository to your local machine.
2. Ensure you have the required dependencies installed.
3. Execute the script using Python.
4. Follow the on-screen instructions to interact with the tool.

---
