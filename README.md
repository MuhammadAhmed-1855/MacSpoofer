# MAC Spoofer Tool

**Author:** Muhammad Ahmed  
**Roll Number:** 20I-1855  
**Section:** CY-T  
**Degree:** Bachelors in Software Engineering  
**Campus:** Islamabad  
**Course Subject:** Ethical Hacking Concepts and Practices

## Overview

The MAC Spoofer tool is a Python script developed by Muhammad Ahmed for the "Ethical Hacking Concepts and Practices" course. It provides a user-friendly interface for managing MAC addresses on a system. The tool allows users to display network information, spoof MAC addresses, and reset MAC addresses.

## Purpose

The MAC Spoofer tool serves the following purposes:

1. Display the original and current MAC addresses of the system.
2. Allow users to choose from a variety of MAC addresses for spoofing.
3. Restore the original MAC address of the system.

## Features

- ASCII art drawings of the letters "MAC Spoofer" enhance the visual appeal of the interface.
- Terminal-based menu for user interaction.
- Random MAC address generation with a locally administered bit set and an even first octet.
- MAC addresses are gathered using various methods, including ARP packet sniffing, reading original MAC addresses from the system, retrieving local MAC addresses using arp-scan, and reading MAC addresses from a CSV file (from public sources).
- Spoofing of the MAC address involves disabling the interface, changing the MAC address, and enabling the interface again.

## Dependencies

The tool relies on the following external libraries and commands:

- **scapy:** For packet manipulation.
- **psutil:** For system information retrieval.
- **subprocess:** For executing system commands.
- **csv:** For reading MAC addresses from a file.

### Wireshark Verified

- Wireshark running in the background.
- Execution of the Python file.
- MAC address spoofing with a selected MAC address (e.g., HONOR DEVICE MAC ADDRESS).
- Include a Wireshark screenshot showing the changed MAC address.

## Usage

- Run python file with administrator privileges.
- Wait for application to access MAC Addresses.
- Spoof MAC address by following menu items.
- MAC address will be reset to original before exiting app.

## Conclusion

The MAC Spoofer tool offers a comprehensive and user-friendly interface for managing MAC addresses, showcasing essential concepts related to network security and MAC address manipulation.
