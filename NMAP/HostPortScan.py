#!/usr/bin/env python
import HostDiscovery
import FilterReports
import sys
import subprocess
import json
from datetime import datetime
import shutil

# ==================================================================
#                         Start of Script
# ==================================================================

def hostPortScan():

    ### CALLING discover_hosts() from HostDiscovery.py
    HostDiscovery.discover_hosts()

    print("\nStarting NMAP Host-Port Discovery Script")

    # Get current time for overview report
    start_time = datetime.now()
    dir_name = start_time.strftime('%Y-%m-%d_%H-%M-%S')


    # Create main reports directory
    reports_dir = HostDiscovery.os.path.join("reports", dir_name)
    HostDiscovery.os.makedirs(reports_dir, exist_ok=True)

    # Figure out the OS type of the current system
    # and figure out the gateway based on the OS type
    current_os = HostDiscovery.get_os()
    gateway = HostDiscovery.get_gateway(current_os)

    # Will append sudo to commands if on Linux
    if current_os == "Windows":
        prefix = ""
    else:
        prefix = "sudo -S "

    local_ip = HostDiscovery.get_local_ip()
    print(local_ip)

    host_count = 0
    with open("./hosts.txt") as hosts:
        line_count = 0
        for line in hosts:
            line_count += 1

    # Perform port scan for each host discovered
    max_current_ports, max_ports_host = 0, 0
    with open("./hosts.txt") as hosts:
        ######
        ###### TEMPORARY
        ######
        # all_hosts = hosts.readlines()
        # test_hosts = all_hosts[:-10]  # Exclude the last 5 hosts for testing
        for host in hosts:
            # Establish current target
            target = host.strip()
            current_ports = 0
            mac_address = None

            # Create output file names
            port_out = target+"_Ports.txt"

            print("\nStarting Port Scan For %s" % target)

            try:
                # Perform NMAP scan on ports 1 - 10000 on the Target IP with a timeout of 60 seconds
                p = subprocess.run("%snmap -sS -p 1-10000 %s" % (prefix, target),
                                shell=True, text=True, capture_output=True, timeout=60)
                ports = p.stdout.splitlines()
            except subprocess.TimeoutExpired:
                print(f"Port scan for {target} timed out. Skipping to next host.")
                continue

            # Create ports report file for current target
            ports_file = open("reports/%s/%s" %
                            (dir_name, port_out), "w")

            # Find the index of where the ports list starts
            # also writes the MAC Address at the top of the file
            port_idx = None
            for line in ports:
                print(line)
                if "PORT" in line:
                    print("================ %s " % line)
                    port_idx = ports.index(line)
                elif "MAC" in line:
                    print("================ %s" % line)
                    mac_address = line
                    ports_file.write(line + "\n")
                    ports.pop(ports.index(line))

            # Check if any ports were found
            if not port_idx:
                ports_file.write(
                    "All 10000 scanned ports on %s are in ignored states." % target)
            else:
                # Write all of the ports to file
                while True:
                    if len(ports[port_idx]) > 1:
                        ports_file.write(ports[port_idx] + "\n")
                        port_idx += 1
                        current_ports += 1
                    else:
                        break
            ports_file.close()

            # Check if current target has more open ports than current max
            if current_ports > max_current_ports:
                max_ports_host = target
                max_current_ports = current_ports

            print("Port Scan Finished For %s" % target)

    # Get end time for overview report
    end_time = datetime.now()
    time_diff = str(end_time - start_time).split(":")

    # Summary print
    print("\nThe scan began on %s, and ended at %s." % (start_time.strftime("%m/%d/%Y %H:%M:%S"), end_time.strftime("%m/%d/%Y %H:%M:%S")))
    print("The scan took a total of %s hours, %s minutes, and %.0f seconds" % (time_diff[0], time_diff[1], float(time_diff[2])))
    print("Found %d Hosts On The Network" % host_count)

    # Check that there are valid values before printing
    if not max_ports_host:
        print("\nNmap did not find any open ports for any hosts.")
    else:
        print("\nThe host %s has the highest number of open ports with %d open ports." % (max_ports_host, max_current_ports))


    FilterReports.filterReports()

    # # Delete the reports directory after the scan
    # shutil.rmtree(reports_dir)
    # print(f"\nDeleted reports directory: {reports_dir}")


hostPortScan()