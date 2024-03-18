from scapy.all import *
import time
import psutil
import subprocess
import csv
import random
import re
import sys

# Set to store unique MAC addresses
unique_mac_addresses = set()
Possible_MAC_Addresses = []
originalMAC = []

# Define color codes
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def draw_m():
    return [
        "$       $",
        "$$     $$",
        "$ $   $ $",
        "$  $ $  $",
        "$   $   $",
        "$       $",
        "$       $"
    ]

def draw_a():
    return [
        "    $    ",
        "   $ $   ",
        "  $   $  ",
        " $     $ ",
        "$$$$$$$$$",
        "$       $",
        "$       $"
    ]

def draw_c():
    return [
        "  $$$$ ",
        " $    $",
        "$      ",
        "$      ",
        "$      ",
        " $    $",
        "  $$$$ "
    ]

def draw_s():
    return [
        " $$$$$ ",
        "$     $",
        "$      ",
        " $$$$$ ",
        "      $",
        " $    $",
        "  $$$$ "
    ]

def draw_p():
    return [
        "$$$$$$ ",
        "$     $",
        "$     $",
        "$$$$$$ ",
        "$      ",
        "$      ",
        "$      "
    ]

def draw_o():
    return [
        " $$$$$ ",
        "$     $",
        "$     $",
        "$     $",
        "$     $",
        "$     $",
        " $$$$$ "
    ]

def draw_f():
    return [
        "$$$$$$",
        "$     ",
        "$     ",
        "$$$$$$",
        "$     ",
        "$     ",
        "$     "
    ]

def draw_e():
    return [
        "$$$$$$",
        "$     ",
        "$     ",
        "$$$$$$",
        "$     ",
        "$     ",
        "$$$$$$"
    ]

def draw_r():
    return [
        "$$$$$$",
        "$    $",
        "$    $       $$$ $   $     $     $     $ $$   $$ $$$$$ $$$      ",
        "$$$$$$       $ $  $ $     $ $    $     $ $ $ $ $ $     $  $$   ",
        "$  $         $$    $     $   $   $$$$$$$ $  $  $ $$$   $   $  ",
        "$   $        $ $   $    $$$$$$$  $     $ $     $ $     $  $$   ",
        "$    $       $$$   $   $       $ $     $ $     $ $$$$$ $$$       "
    ]

def display_information():
    # Displays student and tool information.
    developer_name = "Muhammad Ahmed"
    roll_number = "20I-1855"
    section = "CY-T"
    degree = "Bachelors in Software Engineering"
    campus = "Islamabad"
    course_subject = "Ethical Hacking Concepts and Practices"

    current_datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    print(GREEN + "#"*400)
    for line in zip(draw_m(), draw_a(), draw_c(), draw_s(), draw_p(), draw_o(), draw_o(), draw_f(), draw_e(), draw_r()):
        print(GREEN + " ".join(line))
    print(GREEN + "#"*400)
    
    print(GREEN + f"Developer Name: {developer_name}")
    print(GREEN + f"Roll Number: {roll_number}")
    print(GREEN + f"Section: {section}")
    print(GREEN + f"Degree: {degree}")
    print(GREEN + f"Campus: {campus}")
    print(GREEN + f"Course Subject: {course_subject}")
    print(GREEN + f"Current Date and Time: {current_datetime}")
    
    print(GREEN + "-" * 50)
    print(GREEN + "MAC Spoofer Purpose:")
    print(GREEN + "This tool is designed for:")
    print(GREEN + "- Displaying Network Information")
    print(GREEN + "- Spoofing MAC Address")
    print(GREEN + "- Resetting MAC Address")
    print(GREEN + "-" * 50)

def arp_monitor_callback(pkt):
    # Callback function for ARP packet sniffing.
    if ARP in pkt and pkt[ARP].op in (1, 2):  # who-has or is-at
        mac_address = pkt[ARP].hwsrc
        ip_address = pkt[ARP].psrc

        if mac_address not in unique_mac_addresses:
            unique_mac_addresses.add(mac_address)
            Possible_MAC_Addresses.append(("ARP Sniff", mac_address))

def get_mac_addresses():
    # Retrieves and stores original MAC addresses of the system.
    interfaces = psutil.net_if_addrs()
    for interface, addrs in interfaces.items():
        for addr in addrs:
            if addr.family == psutil.AF_LINK and addr.address != "00:00:00:00:00:00":
                originalMAC.append((interface, addr.address))
                Possible_MAC_Addresses.append(("Original", addr.address))

def spoof_mac_address(interface, new_mac):
    # Spoofs the MAC address of the specified network interface.
    try:
        print(GREEN + f"Running command: sudo ifconfig {interface} down" + RESET)
        subprocess.call(["sudo", "ifconfig", interface, "down"])
        
        print(GREEN + f"Running command: sudo ifconfig {interface} hw ether {new_mac}" + RESET)
        subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
        
        print(GREEN + f"Running command: sudo ifconfig {interface} up" + RESET)
        subprocess.call(["sudo", "ifconfig", interface, "up"])
    except Exception as e:
        print(f"{RED}Error: {e}" + RESET)


def get_local_mac_addresses():
    # Retrieves MAC addresses of local network devices using arp-scan.
    try:
        result = subprocess.run(["sudo", "arp-scan", "-l"], capture_output=True, text=True, check=True)
        lines = result.stdout.splitlines()
        mac_addresses = [line.split()[1] for line in lines if len(line.split()) >= 2 and ':' in line.split()[1]]

        for mac in mac_addresses:
            Possible_MAC_Addresses.append(("Local Address", mac))

    except subprocess.CalledProcessError as e:
        print(f"{RED}Error running arp-scan: {e}")

def read_csv_file(file_path):
    # Reads MAC addresses from a CSV file and appends to Possible_MAC_Addresses.
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) == 2 and all(row):
                    Possible_MAC_Addresses.append((row[0], row[1]))

    except FileNotFoundError:
        print(f"{RED}CSV file not found.")

def generate_random_mac():
    # Generates a random MAC address in the format XX:XX:XX:XX:XX:XX.
    random_mac = [random.randint(0x00, 0xff) for _ in range(6)]

    # Ensure the first octet is even
    random_mac[0] &= 0xFE

    # Set the locally administered bit (second-least-significant bit of the first octet)
    random_mac[0] |= 0x02

    return ":".join([f"{octet:02X}" for octet in random_mac])

def get_current_mac(interface):
    # Retrieves the current MAC address of the specified network interface.
    try:
        result = subprocess.run(["ifconfig", interface], capture_output=True, text=True, check=True)
        mac_match = re.search(r"(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", result.stdout)
        if mac_match:
            return mac_match.group(0)
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error getting current MAC address: {e}")

def reset_mac_address(interface, new_mac):
    # Resets the MAC address of the specified network interface to the original.
    try:
        print(GREEN + f"Running command: sudo ifconfig {interface} down" + RESET)
        subprocess.call(["sudo", "ifconfig", interface, "down"])
        
        print(GREEN + f"Running command: sudo ifconfig {interface} hw ether {new_mac}" + RESET)
        subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
        
        print(GREEN + f"Running command: sudo ifconfig {interface} up" + RESET)
        subprocess.call(["sudo", "ifconfig", interface, "up"])
    except Exception as e:
        print(f"{RED}Error: {e}" + RESET)

def display_network_info():
    print(GREEN + "-" * 50)
    print(GREEN + "Network Information:")
    print(f"Original MAC Address: {originalMAC[0][1]}")
    
    # Displaying current MAC address of the system
    current_mac = get_current_mac(originalMAC[0][0])
    print(f"Current MAC Address: {current_mac}")

def print_addresses():
    # Displays MAC addresses available for spoofing.
    print(GREEN + "-" * 50)
    print(GREEN + "Possible MAC Addresses for Spoofing:")
    i = 1
    for mac in Possible_MAC_Addresses:
        print(f"{i}: {mac}")
        i += 1
    print(GREEN + "-" * 50)

def main_menu():
    # Displays the main menu and takes user input for actions.
    print(GREEN + "-" * 50)
    print(GREEN + "MAC Spoofer Menu:")
    print(GREEN + "-" * 50)
    print(GREEN + "- 0: Display Network Information")
    print(GREEN + "- 2: Spoof MAC Address")
    print(GREEN + "- 3: Reset MAC Address")
    print(GREEN + "- 4: Exit (MAC Address will be reset to original before exiting)")
    return input(GREEN + "Enter your choice (0-4): " + RESET)
    
def select_network_interface():
    interfaces = psutil.net_if_addrs()
    print(GREEN + "-" * 50)
    print(GREEN + "Available Network Interfaces:")
    i = 1
    interface_list = []
    for interface in interfaces:
        interface_list.append(interface)
        print(f"{i}: {interface}")
        i += 1
    print(GREEN + "-" * 50)
    selection = input(GREEN + "Enter the number corresponding to the interface you want to spoof: " + RESET)
    try:
        interface_index = int(selection) - 1
        if interface_index >= 0 and interface_index < len(interface_list):
            return interface_list[interface_index]
        else:
            print(f"{RED}Invalid selection. Please enter a number within the range.{RESET}")
            return select_network_interface()
    except ValueError:
        print(f"{RED}Invalid input. Please enter a number.{RESET}")
        return select_network_interface()
        

if __name__ == "__main__":
    try:
        # Set the timeout to 30 seconds
        timeout = 30

        display_information()
        
        print(GREEN + "Fetching all MAC Addresses. Please wait..." + RESET)

        # Sniff packets with the specified timeout
        sniff(prn=arp_monitor_callback, filter="arp", store=0, timeout=timeout)

        get_mac_addresses()

        get_local_mac_addresses()

        read_csv_file("Public_MAC_Addresses.csv")  # Replace with your CSV file path

        # Add a random MAC address to Possible_MAC_Addresses
        Possible_MAC_Addresses.append(("Random Address", generate_random_mac()))
        
        print(GREEN + "MAC Addresses fetched successfully!!!" + RESET)
        
        selected_interface = select_network_interface()

        while True:
            user_choice = main_menu()

            if user_choice == "0":
                display_network_info()
            elif user_choice == "2":
                print_addresses()
                opt = int(input(GREEN + "Please select the MAC address to spoof (Enter Number): " + RESET))
                spoof_mac_address(selected_interface, Possible_MAC_Addresses[opt - 1][1])
            elif user_choice == "3":
                reset_mac_address(selected_interface, originalMAC[0][1])
            elif user_choice == "4":
                reset_mac_address(selected_interface, originalMAC[0][1])
                print(GREEN + "Thank you for using MAC Spoofer!!!" + RESET)
                break
            else:
                print(RED + "Invalid choice. Please enter a number between 0 and 4." + RESET)

    except KeyboardInterrupt:
        print("\n" + RED + "ARP monitoring stopped." + RESET)
