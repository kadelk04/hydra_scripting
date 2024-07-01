import os

def filterReports():
    # Base directory where the report directories are located
    base_reports_dir = "reports"

    # Find the latest directory in the reports base directory
    latest_report_dir = max([os.path.join(base_reports_dir, d) for d in os.listdir(base_reports_dir)], key=os.path.getmtime)

    # Output file for consolidated results
    output_file = "consolidated_ports_services.txt"

    # Dictionary to store ports and services for each IP
    ip_ports_services = {}

    # Loop through each file in the reports directory
    for filename in os.listdir(latest_report_dir):
        if filename.endswith("_Ports.txt"):
            ip_address = filename.split("_")[0]
            file_path = os.path.join(latest_report_dir, filename)
            
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if "/tcp" in line and "open" in line:
                        parts = line.split()
                        port = parts[0]
                        service = parts[2]
                        if ip_address not in ip_ports_services:
                            ip_ports_services[ip_address] = []
                        ip_ports_services[ip_address].append((port, service))

    # Write the consolidated results to the output file
    with open(output_file, 'w') as output:
        for ip, ports_services in ip_ports_services.items():
            for port, service in ports_services:
                output.write(f"{ip}:{port} ({service})\n")

    print(f"Consolidated results written to {output_file}")
