#!/usr/bin/env python
import os
import sys
import subprocess
import json
from datetime import datetime
import shutil

# Returns string representation of OS type
def get_os():
    os_type = os.name
    if os_type == "nt":
        return "Windows"
    elif os_type == "posix":
        return os.uname().sysname

# Returns the Default Gateway for Linux OS
def linux_helper(command):
    ipconfig = os.popen(command).read().strip().split()
    
    inet_addresses = []
    
    # Iterate through the ipconfig output to find all "inet" occurrences
    for idx, value in enumerate(ipconfig):
        if value == "inet":
            inet_addresses.append(ipconfig[idx + 1])
    
    return inet_addresses

# Returns the Default Gateway for Windows OS
def windows_helper(command):
    ipconfig = os.popen(command).read().strip().splitlines()

    for current in ipconfig:
        current = current.strip().split()
        idx = current.index(":")

        if (len(current) - 1) > idx and len(current[idx + 1]) >= 7:
            win_gateway = current[idx + 1]

    return win_gateway

# Returns the string representation of the default gateway IP
# truncated so that it can be used for NMAP ping scan to find hosts
def get_gateway(current_os):
    # get the gateway based on OS
    if current_os == "Linux":
        gateway = linux_helper("ifconfig | grep broadcast")
    elif current_os == "Darwin":
        gateway = linux_helper("ifconfig | grep broadcast")
    else:
        gateway = windows_helper("ipconfig | findstr Gateway")

    # Truncates the last byte of the gateway
    processed_gateways = []

    for item in gateway:
        for c in reversed(item):
            if c == ".":
                break
            else:
                item = item[:-1]
        processed_gateways.append(item)
    
    return processed_gateways

def get_local_ip():
    return os.popen("hostname -I").read().strip()

# ==================================================================
#                         Start of Script
# ==================================================================
def discover_hosts():
    print("\nStarting NMAP Host Discovery Script")

    # Figure out the OS type of the current system
    # and figure out the gateway based on the OS type
    current_os = get_os()
    gateway = get_gateway(current_os)

    # Will append sudo to commands if on Linux
    if current_os == "Windows":
        prefix = ""
    else:
        prefix = "sudo -S "

    local_ip = get_local_ip()
    print(local_ip)

    host_count = 0
    hosts_file = open("./hosts.txt", "w")
    raw_hosts = []

    # Perform NMAP scan to find all hosts
    for item in gateway:
        words = os.popen("%s nmap -sn %s0/24" % (prefix, item)).read().strip().split()
        for word in words: 
            if item in word and word != local_ip:
                hosts_file.write(word + "\n")
                host_count += 1
    hosts_file.close()

    print("NMAP Host Discovery Completed")

    if not host_count:
        print("Nmap did not find any hosts with %s0/24 as the Default Gateway" % gateway)
        sys.exit()

    # # Perform port scan for each host discovered
    # max_current_ports, max_ports_host = 0, 0
    # with open("./hosts.txt") as hosts:
    #     ###### TEMPORARY
    #     all_hosts = hosts.readlines()
    #     test_hosts = all_hosts[:-10]  # Exclude the last 5 hosts for testing
    #     for host in test_hosts:
    #         # Establish current target
    #         target = host.strip()
    #         current_ports = 0
    #         mac_address = None

    #         # Create output file names
    #         port_out = target+"_Ports.txt"

    #         print("\nStarting Port Scan For %s" % target)

    #         # Perform NMAP scan on ports 1 - 10000 on the Target IP
    #         p = subprocess.run("%snmap -sS -p 1-10000 %s" % (prefix, target),
    #                            shell=True, text=True, capture_output=True)
    #         ports = p.stdout.splitlines()

    #         # Create ports report file for current target
    #         ports_file = open("reports/%s/%s" %
    #                           (dir_name, port_out), "w")

    #         # Find the index of where the ports list starts
    #         # also writes the MAC Address at the top of the file
    #         port_idx = None
    #         for line in ports:
    #             print(line)
    #             if "PORT" in line:
    #                 print("================ %s " % line)
    #                 port_idx = ports.index(line)
    #             elif "MAC" in line:
    #                 print("================ %s" % line)
    #                 mac_address = line
    #                 ports_file.write(line + "\n")
    #                 ports.pop(ports.index(line))

    #         # Check if any ports were found
    #         if not port_idx:
    #             ports_file.write(
    #                 "All 10000 scanned ports on %s are in ignored states." % target)
    #         else:
    #             # Write all of the ports to file
    #             while True:
    #                 if len(ports[port_idx]) > 1:
    #                     ports_file.write(ports[port_idx] + "\n")
    #                     port_idx += 1
    #                     current_ports += 1
    #                 else:
    #                     break
    #         ports_file.close()

    #         # Check if current target has more open ports than current max
    #         if current_ports > max_current_ports:
    #             max_ports_host = target
    #             max_current_ports = current_ports

    #         print("Port Scan Finished For %s" % target)

    # # Get end time for overview report
    # end_time = datetime.now()
    # time_diff = str(end_time - start_time).split(":")

    # # Summary print
    # print("\nThe scan began on %s, and ended at %s." % (start_time.strftime("%m/%d/%Y %H:%M:%S"), end_time.strftime("%m/%d/%Y %H:%M:%S")))
    # print("The scan took a total of %s hours, %s minutes, and %.0f seconds" % (time_diff[0], time_diff[1], float(time_diff[2])))
    # print("Found %d Hosts On The Network" % host_count)

    # # Check that there are valid values before printing
    # if not max_ports_host:
    #     print("\nNmap did not find any open ports for any hosts.")
    # else:
    #     print("\nThe host %s has the highest number of open ports with %d open ports." % (max_ports_host, max_current_ports))

    # # Delete the reports directory after the scan
    # shutil.rmtree(reports_dir)
    # print(f"\nDeleted reports directory: {reports_dir}")
