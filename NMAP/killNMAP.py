import subprocess
command = ['sudo', 'pkill', 'nmap']
p = subprocess.run(command, text=True, capture_output=True)
