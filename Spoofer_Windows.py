import time
import psutil
import subprocess
import csv
import random
import re

# Define ANSI escape codes for colors
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

Possible_MAC_Addresses = []
originalMAC = []

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

    print(GREEN + "#"*400)
    for line in zip(draw_m(), draw_a(), draw_c(), draw_s(), draw_p(), draw_o(), draw_o(), draw_f(), draw_e(), draw_r()):
        print(GREEN + "".join(line))
    print(GREEN + "#"*400)

    developer_name = "Muhammad Ahmed"
    roll_number = "20I-1855"
    section = "CY-T"
    degree = "Bachelors in Software Engineering"
    campus = "Islamabad"
    course_subject = "Ethical Hacking Concepts and Practices"

    current_datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    print(GREEN + "#" * 60)
    print(f"Developer Name: {developer_name}")
    print(f"Roll Number: {roll_number}")
    print(f"Section: {section}")
    print(f"Degree: {degree}")
    print(f"Campus: {campus}")
    print(f"Course Subject: {course_subject}")
    print(f"Current Date and Time: {current_datetime}")
    print("NOTE: Please disable your antivirus if spoofing is not working correctly.")
    print("#" * 60 + RESET)
    
    print(GREEN + "-" * 60)
    print("MAC Spoofer Purpose:")
    print("This tool is designed for:")
    print("- Displaying Network Information")
    print("- Spoofing MAC Address")
    print("- Resetting MAC Address")
    print("-" * 60 + RESET)

def get_mac_addresses():
    # Retrieves and stores original MAC addresses of the system.
    interfaces = psutil.net_if_addrs()
    for interface, addrs in interfaces.items():
        for addr in addrs:
            if addr.family == psutil.AF_LINK and addr.address != "00:00:00:00:00:00":
                originalMAC.append((interface, addr.address))
                Possible_MAC_Addresses.append((interface, addr.address))

def spoof_mac_address(interface, instance, new_mac):
    # Spoofs the MAC address of the specified network interface.
    try:
        print(GREEN + f"Running command: netsh interface set interface {interface} admin=DISABLED" + RESET)
        subprocess.run(["netsh", "interface", "set", "interface", interface, "admin=DISABLED"], capture_output=True, text=True, check=True)

        print(GREEN + f"Running command: reg add HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class\\{{4D36E972-E325-11CE-BFC1-08002BE10318}}\\{instance:04} /v NetworkAddress /t REG_SZ /d {new_mac} /f" + RESET)
        subprocess.run(["reg", "add", f"HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class\\{{4D36E972-E325-11CE-BFC1-08002BE10318}}\\{instance:04}\\", "/v", "NetworkAddress", "/t", "REG_SZ", "/d", new_mac, "/f"], capture_output=True, text=True, check=True)

        print(GREEN + f"Running command: netsh interface set interface {interface} admin=ENABLED" + RESET)
        subprocess.run(["netsh", "interface", "set", "interface", interface, "admin=ENABLED"], capture_output=True, text=True, check=True)

    except subprocess.CalledProcessError as e:
        print(RED + f"Error: {e}" + RESET)

def get_local_mac_addresses():
    # Retrieves MAC addresses of local network devices using arp-scan.
    try:
        result = subprocess.run(["arp", "-a"], capture_output=True, text=True, check=True)
        lines = result.stdout.splitlines()
        mac_addresses = [line.split()[1] for line in lines if len(line.split()) >= 2 and '-' in line.split()[1]]

        for mac in mac_addresses:
            Possible_MAC_Addresses.append(("Local Address", mac))

    except subprocess.CalledProcessError as e:
        print(RED + f"Error running arp command: {e}" + RESET)

def read_csv_file(file_path):
    # Reads MAC addresses from a CSV file and appends to Possible_MAC_Addresses.
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) == 2 and all(row):
                    Possible_MAC_Addresses.append((row[0], row[1]))

    except FileNotFoundError:
        print(RED + "CSV file not found." + RESET)


def generate_random_mac():
    # Generates a random MAC address in the format XX-XX-XX-XX-XX-XX.
    random_mac = [random.randint(0x00, 0xff) for _ in range(6)]

    # Ensure the first octet is even
    random_mac[0] &= 0xFE

    # Set the locally administered bit (second-least-significant bit of the first octet)
    random_mac[0] |= 0x02

    return "-".join([f"{octet:02X}" for octet in random_mac])

def get_current_mac(interface):
    # Retrieves the current MAC address of the specified network interface.
    try:
        result = subprocess.run(["getmac", "/fo", "csv", "/nh", "/v"], capture_output=True, text=True, check=True)
        mac_match = re.search(rf'"{interface}",".*?","((?:[0-9A-Fa-f]{{2}}[:-]){{5}}(?:[0-9A-Fa-f]{{2}}))"', result.stdout)
        if mac_match:
            return mac_match.group(1)
    except subprocess.CalledProcessError as e:
        print(RED + f"Error getting current MAC address: {e}" + RESET)

def reset_mac_address(interface, instance, new_mac):
    # Resets the MAC address of the specified network interface to the original.
    try:

        print(GREEN + f"Running command: netsh interface set interface {interface} admin=DISABLED" + RESET)
        subprocess.run(["netsh", "interface", "set", "interface", interface, "admin=DISABLED"], capture_output=True, text=True, check=True)

        print(GREEN + f"Running command: reg add HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class\\{{4D36E972-E325-11CE-BFC1-08002BE10318}}\\{instance:04} /v NetworkAddress /t REG_SZ /d {new_mac} /f" + RESET)
        subprocess.run(["reg", "add", f"HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class\\{{4D36E972-E325-11CE-BFC1-08002BE10318}}\\{instance:04}\\", "/v", "NetworkAddress", "/t", "REG_SZ", "/d", new_mac, "/f"], capture_output=True, text=True, check=True)

        print(GREEN + f"Running command: netsh interface set interface {interface} admin=ENABLED" + RESET)
        subprocess.run(["netsh", "interface", "set", "interface", interface, "admin=ENABLED"], capture_output=True, text=True, check=True)

    except subprocess.CalledProcessError as e:
        print(RED + f"Error: {e}" + RESET)

def display_network_info(originalMAC, index):
    print(GREEN +"-" * 60)
    print("Network Information:")
    print(f"Original MAC Address: {originalMAC[index][1]}")
    
    # Displaying current MAC address of the system
    current_mac = get_current_mac(originalMAC[index][0])
    print(f"Current MAC Address: {current_mac}" + RESET)

def print_addresses(Possible_MAC_Addresses):
    # Displays MAC addresses available for spoofing.
    print(GREEN +"-" * 60)
    print("Possible MAC Addresses for Spoofing:")
    i = 1
    for mac in Possible_MAC_Addresses:
        print(f"{i}: {mac}")
        i += 1
    print("-" * 60 +RESET)

def select_network_interface():
    interfaces = psutil.net_if_addrs()
    print(GREEN + "-" * 60)
    print("Available Network Interfaces:")
    i = 1
    for interface in interfaces:
        print(f"{i}: {interface}")
        i += 1
    print("-" * 60)
    selection = input("Enter the number corresponding to the interface you want to spoof: " + RESET)
    try:
        interface_index = int(selection) - 1
        if interface_index >= 0 and interface_index < len(interfaces):
            return interface_index
        else:
            print(f"{RED}Invalid selection. Please enter a number within the range.{RESET}")
            return select_network_interface()
    except ValueError:
        print(f"{RED}Invalid input. Please enter a number.{RESET}")
        return select_network_interface()

def main_menu():
    # Displays the main menu and takes user input for actions.
    print(GREEN +"-" * 60)
    print("MAC Spoofer Menu:")
    print("-" * 60)
    print("- 0: Display Network Information")
    print("- 2: Spoof MAC Address")
    print("- 3: Reset MAC Address")
    print("- 4: Exit (MAC Address will be reset to original before exiting)")
    return input("Enter your choice (0-4): " + RESET)

if __name__ == "__main__":
    try:
        display_information()
        
        print(GREEN +"Fetching all MAC Addresses. Please wait..." + RESET)

        get_mac_addresses()

        get_local_mac_addresses()

        read_csv_file(".\Public_MAC_Addresses.csv")  # Replace with your CSV file path

        # Append a random MAC address to Possible_MAC_Addresses
        Possible_MAC_Addresses.append(("Random Address", generate_random_mac()))
        
        print(GREEN +"MAC Addresses fetched successfully!!! + RESET")

        selected_interface = select_network_interface()
        print(GREEN + f"Selected interface: {selected_interface}" + RESET)

        while True:
            user_choice = main_menu()

            if user_choice == "0":
                display_network_info(originalMAC, selected_interface)  
            elif user_choice == "2":
                print_addresses(Possible_MAC_Addresses)
                opt = int(input(GREEN +"Please select the MAC address to spoof (Enter Number): " + RESET))
                spoof_mac_address(originalMAC[selected_interface][0], selected_interface+1, Possible_MAC_Addresses[opt - 1][1])
            elif user_choice == "3":
                reset_mac_address(originalMAC[selected_interface][0], selected_interface, originalMAC[selected_interface][1])
            elif user_choice == "4":
                reset_mac_address(originalMAC[selected_interface][0], selected_interface, originalMAC[selected_interface][1])
                print(GREEN + "Thank you for using MAC Spoofer!!!" + RESET)
                break
            else:
                print(f"{RED}Invalid choice. Please enter a number between 0 and 4.{RESET}")

    except KeyboardInterrupt:
        print("\nARP monitoring stopped.")
